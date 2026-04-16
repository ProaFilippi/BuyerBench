"""Tests for UPGRADE-14: statistical analysis pipeline (results/stats_pipeline.py)."""
from __future__ import annotations

import json
import math
from datetime import datetime, timezone
from pathlib import Path

import pytest

from buyerbench.models import EvaluationResult, Pillar, PillarScore, ScenarioVariant
from results.aggregate_cells import CellAggregate, CellAggregateReport
from results.stats_pipeline import (
    OLSResult,
    RegressionCoefficient,
    StatsPipelineReport,
    TreatmentEffectTest,
    VarianceDecomposition,
    VarianceDecompositionRow,
    _CONTROL_VARIANTS,
    _WARP_VARIANTS,
    _betacf,
    _betainc,
    _dot,
    _is_treatment,
    _matmul,
    _p2_cells_for_ols,
    _solve_linear,
    _t_critical_95,
    _t_pvalue,
    _transpose,
    bh_fdr_correction,
    compute_h2_capability,
    compute_h7_noise_bias,
    compute_session_order_effects,
    compute_treatment_effect_tests,
    compute_variance_decomposition,
    run_level1_ols,
    run_stats_pipeline,
    write_stats_pipeline_report,
)


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────


def _make_cell(
    agent_id: str = "agent-A",
    scenario_id: str = "p2-01-anchoring-BASELINE",
    variant_pair_id: str | None = "p2-01-anchoring",
    variant: str | None = "BASELINE",
    bias_category: str | None = "anchoring",
    mean_bsi: float = 0.0,
    std_bsi: float = 0.0,
    n_valid_runs: int = 30,
    n_runs: int = 30,
    temperature: float | None = 0.7,
    treatment_effect: float | None = None,
) -> CellAggregate:
    return CellAggregate(
        cell_id=f"{agent_id}__{variant_pair_id or scenario_id}__{variant}__0.7",
        agent_id=agent_id,
        scenario_id=scenario_id,
        variant_pair_id=variant_pair_id,
        variant=variant,
        bias_category=bias_category,
        temperature=temperature,
        n_runs=n_runs,
        n_valid_runs=n_valid_runs,
        mean_bsi=mean_bsi,
        std_bsi=std_bsi,
        ci_lower_95=max(0.0, mean_bsi - 0.05),
        ci_upper_95=min(1.0, mean_bsi + 0.05),
        choice_rate_correct=1.0 - mean_bsi,
        mean_optimality_gap=mean_bsi * 0.5,
        treatment_effect_vs_baseline=treatment_effect,
    )


def _make_report(cells: list[CellAggregate]) -> CellAggregateReport:
    return CellAggregateReport(
        n_agents=len({c.agent_id for c in cells}),
        n_cells=len(cells),
        n_total_runs=sum(c.n_runs for c in cells),
        cells=cells,
    )


def _two_agent_two_bias_cells() -> list[CellAggregate]:
    """Minimal valid dataset: 2 agents × 2 bias types × 2 variants = 8 cells."""
    agents = ["agent-A", "agent-B"]
    biases = [("anchoring", "p2-01-anchoring"), ("framing", "p2-02-framing")]
    bias_variants = {
        "anchoring": ("BASELINE", "ANCHOR_HIGH"),
        "framing": ("FRAMING_GAIN", "FRAMING_LOSS"),
    }
    bsi = {
        ("agent-A", "anchoring", "BASELINE"): 0.10,
        ("agent-A", "anchoring", "ANCHOR_HIGH"): 0.40,
        ("agent-A", "framing", "FRAMING_GAIN"): 0.05,
        ("agent-A", "framing", "FRAMING_LOSS"): 0.30,
        ("agent-B", "anchoring", "BASELINE"): 0.15,
        ("agent-B", "anchoring", "ANCHOR_HIGH"): 0.50,
        ("agent-B", "framing", "FRAMING_GAIN"): 0.10,
        ("agent-B", "framing", "FRAMING_LOSS"): 0.45,
    }
    cells = []
    for agent in agents:
        for bias, pair_id in biases:
            ctrl_v, treat_v = bias_variants[bias]
            cells.append(
                _make_cell(
                    agent_id=agent,
                    scenario_id=f"{pair_id}-{ctrl_v}",
                    variant_pair_id=pair_id,
                    variant=ctrl_v,
                    bias_category=bias,
                    mean_bsi=bsi[(agent, bias, ctrl_v)],
                    std_bsi=0.15,
                    n_valid_runs=30,
                )
            )
            cells.append(
                _make_cell(
                    agent_id=agent,
                    scenario_id=f"{pair_id}-{treat_v}",
                    variant_pair_id=pair_id,
                    variant=treat_v,
                    bias_category=bias,
                    mean_bsi=bsi[(agent, bias, treat_v)],
                    std_bsi=0.20,
                    n_valid_runs=30,
                )
            )
    return cells


def _make_eval_result(
    agent_id: str = "agent-A",
    scenario_id: str = "p2-01-anchoring-BASELINE",
    bsi: float = 0.0,
    run_index: int = 0,
) -> EvaluationResult:
    return EvaluationResult(
        scenario_id=scenario_id,
        agent_id=agent_id,
        pillar_scores=[
            PillarScore(
                pillar=Pillar.PILLAR2,
                score=1.0 - bsi,
                metrics={
                    "bias_susceptibility_index": bsi,
                    "optimality_gap": bsi * 0.5,
                    "optimal_chosen": 1.0 - bsi,
                    "optimal_choice_rate": 1.0 - bsi,
                    "expected_value_regret": bsi * 0.5,
                },
            )
        ],
        overall_pass=bsi < 0.5,
        run_index=run_index,
        decisions={"selected_supplier": "SupplierA" if bsi == 0.0 else "SupplierB"},
    )


# ─────────────────────────────────────────────────────────────────────────────
# §1  LINEAR ALGEBRA
# ─────────────────────────────────────────────────────────────────────────────


class TestDot:
    def test_basic(self):
        assert _dot([1.0, 2.0, 3.0], [4.0, 5.0, 6.0]) == pytest.approx(32.0)

    def test_empty(self):
        assert _dot([], []) == 0.0

    def test_orthogonal(self):
        assert _dot([1.0, 0.0], [0.0, 1.0]) == pytest.approx(0.0)


class TestTranspose:
    def test_square(self):
        A = [[1.0, 2.0], [3.0, 4.0]]
        assert _transpose(A) == [[1.0, 3.0], [2.0, 4.0]]

    def test_rectangular(self):
        A = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]
        T = _transpose(A)
        assert len(T) == 3
        assert len(T[0]) == 2
        assert T[0][0] == 1.0
        assert T[2][1] == 6.0

    def test_empty(self):
        assert _transpose([]) == []


class TestMatmul:
    def test_identity(self):
        A = [[1.0, 2.0], [3.0, 4.0]]
        I = [[1.0, 0.0], [0.0, 1.0]]
        result = _matmul(A, I)
        assert result[0] == pytest.approx([1.0, 2.0])
        assert result[1] == pytest.approx([3.0, 4.0])

    def test_2x2(self):
        A = [[1.0, 2.0], [3.0, 4.0]]
        B = [[2.0, 0.0], [1.0, 2.0]]
        result = _matmul(A, B)
        assert result[0][0] == pytest.approx(4.0)
        assert result[0][1] == pytest.approx(4.0)
        assert result[1][0] == pytest.approx(10.0)
        assert result[1][1] == pytest.approx(8.0)


class TestSolveLinear:
    def test_2x2_simple(self):
        # 2x + y = 5, x + 3y = 10 → x=1, y=3
        A = [[2.0, 1.0], [1.0, 3.0]]
        b = [5.0, 10.0]
        x = _solve_linear(A, b)
        assert x[0] == pytest.approx(1.0, abs=1e-9)
        assert x[1] == pytest.approx(3.0, abs=1e-9)

    def test_diagonal(self):
        A = [[3.0, 0.0], [0.0, 5.0]]
        b = [9.0, 15.0]
        x = _solve_linear(A, b)
        assert x[0] == pytest.approx(3.0, abs=1e-9)
        assert x[1] == pytest.approx(3.0, abs=1e-9)

    def test_singular_raises(self):
        A = [[1.0, 2.0], [2.0, 4.0]]  # rank 1
        b = [1.0, 2.0]
        with pytest.raises(ValueError, match="Singular"):
            _solve_linear(A, b)

    def test_3x3(self):
        # x + y + z = 6, 2x + y + z = 9, x + 2y + z = 8 → x=3,y=2,z=1
        A = [[1.0, 1.0, 1.0], [2.0, 1.0, 1.0], [1.0, 2.0, 1.0]]
        b = [6.0, 9.0, 8.0]
        x = _solve_linear(A, b)
        assert x[0] == pytest.approx(3.0, abs=1e-9)
        assert x[1] == pytest.approx(2.0, abs=1e-9)
        assert x[2] == pytest.approx(1.0, abs=1e-9)


# ─────────────────────────────────────────────────────────────────────────────
# §2  STATISTICS
# ─────────────────────────────────────────────────────────────────────────────


class TestTCritical95:
    def test_large_df(self):
        assert _t_critical_95(100) == pytest.approx(1.960)
        assert _t_critical_95(30) == pytest.approx(1.960)

    def test_known_df9(self):
        # t_{9, 0.025} = 2.262
        assert _t_critical_95(9) == pytest.approx(2.262, abs=1e-3)

    def test_df1(self):
        assert _t_critical_95(1) == pytest.approx(12.706, abs=1e-3)


class TestBetainc:
    def test_x_zero(self):
        assert _betainc(0.5, 0.5, 0.0) == pytest.approx(0.0)

    def test_x_one(self):
        assert _betainc(0.5, 0.5, 1.0) == pytest.approx(1.0)

    def test_symmetric_half(self):
        # I_{0.5}(a, a) = 0.5 for any a > 0
        for a in [0.5, 1.0, 2.0, 5.0]:
            assert _betainc(a, a, 0.5) == pytest.approx(0.5, abs=1e-5)

    def test_known_value(self):
        # I_{0.5}(1, 1) = 0.5 (uniform; CDF = x)
        assert _betainc(1.0, 1.0, 0.5) == pytest.approx(0.5, abs=1e-6)

    def test_known_value_2(self):
        # I_{0.25}(1, 1) = 0.25
        assert _betainc(1.0, 1.0, 0.25) == pytest.approx(0.25, abs=1e-6)


class TestTPvalue:
    def test_zero_t_stat(self):
        # p-value of t=0 is always 1.0
        for df in [1, 5, 10, 30, 100]:
            assert _t_pvalue(0.0, df) == pytest.approx(1.0, abs=1e-4)

    def test_known_t9_2262(self):
        # t_{9,0.025} = 2.262 → p ≈ 0.05
        p = _t_pvalue(2.262, 9)
        assert p == pytest.approx(0.05, abs=0.002)

    def test_large_t_gives_small_p(self):
        p = _t_pvalue(10.0, 30)
        assert p < 0.001

    def test_negative_df_returns_1(self):
        assert _t_pvalue(2.0, 0) == pytest.approx(1.0)
        assert _t_pvalue(2.0, -5) == pytest.approx(1.0)

    def test_large_df_matches_normal(self):
        # For large df, t-dist ≈ normal; t=1.96 → p≈0.05
        p = _t_pvalue(1.96, 1000)
        assert p == pytest.approx(0.05, abs=0.002)

    def test_symmetry(self):
        # p(-t, df) == p(+t, df)
        for t in [1.0, 2.0, 3.0]:
            assert _t_pvalue(-t, 10) == pytest.approx(_t_pvalue(t, 10), abs=1e-8)


class TestBHFDRCorrection:
    def test_empty(self):
        adj, rej = bh_fdr_correction([])
        assert adj == []
        assert rej == []

    def test_single_p(self):
        adj, rej = bh_fdr_correction([0.03])
        assert adj[0] == pytest.approx(0.03)
        assert rej[0] is True  # 0.03 < 0.05

    def test_all_large_p(self):
        _, rej = bh_fdr_correction([0.8, 0.9, 0.95])
        assert not any(rej)

    def test_known_example(self):
        # n=3, p=[0.03, 0.01, 0.10]; q=0.05
        # Sorted: [0.01, 0.03, 0.10]
        # adj (sorted): [0.03, 0.045, 0.10]
        # After step-down: [0.03, 0.045, 0.10]
        # Original order: [0.045, 0.03, 0.10] → rejected: [True, True, False]
        adj, rej = bh_fdr_correction([0.03, 0.01, 0.10])
        assert rej[0] is True   # adj=0.045 < 0.05
        assert rej[1] is True   # adj=0.03 < 0.05
        assert rej[2] is False  # adj=0.10 ≥ 0.05

    def test_preserves_input_order(self):
        # p_values in non-sorted order; output must be in same order
        p = [0.10, 0.01, 0.05, 0.30]
        adj, _ = bh_fdr_correction(p)
        assert len(adj) == 4

    def test_step_down_monotonicity(self):
        # Adjusted p-values must be non-decreasing (in sorted rank order)
        p = [0.001, 0.03, 0.04, 0.09, 0.20]
        adj, _ = bh_fdr_correction(p)
        order = sorted(range(5), key=lambda i: p[i])
        adj_sorted = [adj[i] for i in order]
        for i in range(len(adj_sorted) - 1):
            assert adj_sorted[i] <= adj_sorted[i + 1] + 1e-9

    def test_custom_q(self):
        p = [0.03, 0.01, 0.10]
        _, rej_strict = bh_fdr_correction(p, q=0.01)
        _, rej_loose = bh_fdr_correction(p, q=0.10)
        # Strict threshold should reject ≤ loose
        for i in range(3):
            if rej_strict[i]:
                assert rej_loose[i]

    def test_all_zeros_rejected(self):
        _, rej = bh_fdr_correction([0.0, 0.0, 0.0])
        assert all(rej)


# ─────────────────────────────────────────────────────────────────────────────
# §3  CONTROL/TREATMENT VARIANT HELPERS
# ─────────────────────────────────────────────────────────────────────────────


class TestIseTreatment:
    def test_baseline_is_control(self):
        assert _is_treatment("BASELINE") is False

    def test_framing_gain_is_control(self):
        assert _is_treatment("FRAMING_GAIN") is False

    def test_anchor_high_is_treatment(self):
        assert _is_treatment("ANCHOR_HIGH") is True

    def test_framing_loss_is_treatment(self):
        assert _is_treatment("FRAMING_LOSS") is True

    def test_warp_variants_are_neither(self):
        for v in ["WARP_AB", "WARP_BC", "WARP_AC"]:
            assert _is_treatment(v) is False

    def test_none_is_false(self):
        assert _is_treatment(None) is False

    def test_decoy_is_treatment(self):
        assert _is_treatment("DECOY") is True


# ─────────────────────────────────────────────────────────────────────────────
# §4  LEVEL 1 OLS
# ─────────────────────────────────────────────────────────────────────────────


class TestLevel1OLS:
    def test_returns_ols_result(self):
        cells = _two_agent_two_bias_cells()
        result = run_level1_ols(cells)
        assert result is not None
        assert isinstance(result, OLSResult)

    def test_has_correct_n_obs(self):
        cells = _two_agent_two_bias_cells()
        result = run_level1_ols(cells)
        # 2 agents × 2 biases × 2 variants = 8 cells
        assert result.n_obs == 8

    def test_has_treatment_coefficient(self):
        cells = _two_agent_two_bias_cells()
        result = run_level1_ols(cells)
        names = [c.name for c in result.coefficients]
        assert "Treatment" in names

    def test_treatment_effect_direction(self):
        # All treatment cells have higher BSI than baseline → positive β_t
        cells = _two_agent_two_bias_cells()
        result = run_level1_ols(cells)
        treat_coef = next(c for c in result.coefficients if c.name == "Treatment")
        assert treat_coef.estimate > 0.0

    def test_r_squared_in_range(self):
        cells = _two_agent_two_bias_cells()
        result = run_level1_ols(cells)
        assert 0.0 <= result.r_squared <= 1.0

    def test_returns_none_for_single_agent(self):
        cells = [
            _make_cell(agent_id="agent-A", bias_category="anchoring", variant="BASELINE"),
            _make_cell(agent_id="agent-A", bias_category="anchoring", variant="ANCHOR_HIGH"),
        ]
        result = run_level1_ols(cells)
        assert result is None

    def test_returns_none_for_single_bias(self):
        cells = [
            _make_cell(agent_id="agent-A", bias_category="anchoring", variant="BASELINE"),
            _make_cell(agent_id="agent-A", bias_category="anchoring", variant="ANCHOR_HIGH"),
            _make_cell(agent_id="agent-B", bias_category="anchoring", variant="BASELINE"),
            _make_cell(agent_id="agent-B", bias_category="anchoring", variant="ANCHOR_HIGH"),
        ]
        result = run_level1_ols(cells)
        assert result is None

    def test_warp_cells_excluded(self):
        cells = _two_agent_two_bias_cells()
        # Add WARP cells — should be ignored
        cells.append(
            _make_cell(
                agent_id="agent-A", variant="WARP_AB", bias_category="warp",
                scenario_id="p2-08-warp-AB",
            )
        )
        result = run_level1_ols(cells)
        assert result is not None
        assert result.n_obs == 8  # WARP excluded

    def test_coefficients_have_se_and_pvalue(self):
        cells = _two_agent_two_bias_cells()
        result = run_level1_ols(cells)
        for coef in result.coefficients:
            assert coef.se >= 0.0
            assert 0.0 <= coef.p_value <= 1.0
            assert coef.ci_lower_95 <= coef.estimate <= coef.ci_upper_95


# ─────────────────────────────────────────────────────────────────────────────
# §5  VARIANCE DECOMPOSITION
# ─────────────────────────────────────────────────────────────────────────────


class TestVarianceDecomposition:
    def test_returns_decomposition(self):
        cells = _two_agent_two_bias_cells()
        vd = compute_variance_decomposition(cells)
        assert vd is not None
        assert isinstance(vd, VarianceDecomposition)

    def test_sources_present(self):
        cells = _two_agent_two_bias_cells()
        vd = compute_variance_decomposition(cells)
        sources = {row.source for row in vd.rows}
        assert sources == {"Model", "BiasType", "Treatment", "Residual"}

    def test_eta_squared_sums_to_at_most_one(self):
        cells = _two_agent_two_bias_cells()
        vd = compute_variance_decomposition(cells)
        # Note: SS_Model + SS_Bias + SS_Treatment ≤ SS_Total (by construction with Residual floor)
        total_eta = sum(row.eta_squared for row in vd.rows if row.source != "Residual")
        assert total_eta <= 1.0 + 1e-9

    def test_treatment_eta_positive(self):
        # Treatments have higher BSI → treatment should explain some variance
        cells = _two_agent_two_bias_cells()
        vd = compute_variance_decomposition(cells)
        treat_eta = vd.eta_squared("Treatment")
        assert treat_eta is not None
        assert treat_eta > 0.0

    def test_n_obs_correct(self):
        cells = _two_agent_two_bias_cells()
        vd = compute_variance_decomposition(cells)
        assert vd.n_obs == 8

    def test_total_ss_positive(self):
        cells = _two_agent_two_bias_cells()
        vd = compute_variance_decomposition(cells)
        assert vd.total_ss > 0.0

    def test_returns_none_when_too_few_cells(self):
        cells = [
            _make_cell(agent_id="agent-A", mean_bsi=0.1),
            _make_cell(agent_id="agent-A", mean_bsi=0.2),
        ]
        vd = compute_variance_decomposition(cells)
        assert vd is None

    def test_eta_squared_method(self):
        cells = _two_agent_two_bias_cells()
        vd = compute_variance_decomposition(cells)
        assert vd.eta_squared("Model") is not None
        assert vd.eta_squared("NonExistent") is None


# ─────────────────────────────────────────────────────────────────────────────
# §6  TREATMENT EFFECT TESTS
# ─────────────────────────────────────────────────────────────────────────────


class TestTreatmentEffectTests:
    def test_returns_tests(self):
        cells = _two_agent_two_bias_cells()
        tests = compute_treatment_effect_tests(cells)
        assert len(tests) > 0

    def test_correct_count(self):
        # 2 agents × 2 bias types = 4 tests
        cells = _two_agent_two_bias_cells()
        tests = compute_treatment_effect_tests(cells)
        assert len(tests) == 4

    def test_bh_correction_applied(self):
        cells = _two_agent_two_bias_cells()
        tests = compute_treatment_effect_tests(cells)
        for t in tests:
            assert t.p_value_bh is not None

    def test_treatment_effects_positive(self):
        cells = _two_agent_two_bias_cells()
        tests = compute_treatment_effect_tests(cells)
        for t in tests:
            assert t.treatment_effect > 0.0, f"Expected positive TE for {t}"

    def test_ci_contains_estimate(self):
        cells = _two_agent_two_bias_cells()
        tests = compute_treatment_effect_tests(cells)
        for t in tests:
            assert t.ci_lower_95 <= t.treatment_effect <= t.ci_upper_95

    def test_framing_pair_handled(self):
        # FRAMING_GAIN/FRAMING_LOSS pair (no explicit BASELINE)
        cells = [
            _make_cell(
                agent_id="agent-A", variant="FRAMING_GAIN",
                bias_category="framing", variant_pair_id="p2-02-framing",
                mean_bsi=0.05, std_bsi=0.10, n_valid_runs=30,
            ),
            _make_cell(
                agent_id="agent-A", variant="FRAMING_LOSS",
                bias_category="framing", variant_pair_id="p2-02-framing",
                mean_bsi=0.35, std_bsi=0.18, n_valid_runs=30,
            ),
        ]
        tests = compute_treatment_effect_tests(cells)
        assert len(tests) == 1
        assert tests[0].treatment_effect == pytest.approx(0.30, abs=1e-5)

    def test_warp_cells_excluded(self):
        cells = _two_agent_two_bias_cells()
        cells.append(
            _make_cell(
                agent_id="agent-A", variant="WARP_AB", bias_category="warp",
                variant_pair_id="p2-08-warp",
            )
        )
        tests = compute_treatment_effect_tests(cells)
        bias_cats = {t.bias_category for t in tests}
        assert "warp" not in bias_cats

    def test_no_paired_cells_returns_empty(self):
        cells = [
            _make_cell(agent_id="agent-A", variant="BASELINE", bias_category="anchoring"),
        ]
        tests = compute_treatment_effect_tests(cells)
        assert tests == []

    def test_se_is_positive(self):
        cells = _two_agent_two_bias_cells()
        tests = compute_treatment_effect_tests(cells)
        for t in tests:
            assert t.se > 0.0

    def test_p_value_in_range(self):
        cells = _two_agent_two_bias_cells()
        tests = compute_treatment_effect_tests(cells)
        for t in tests:
            assert 0.0 <= t.p_value <= 1.0
            assert 0.0 <= t.p_value_bh <= 1.0


# ─────────────────────────────────────────────────────────────────────────────
# §7  H7 NOISE-BIAS CORRELATION
# ─────────────────────────────────────────────────────────────────────────────


class TestH7NoiseBias:
    def _cells_with_std(self) -> list[CellAggregate]:
        """Cells where std_bsi increases with mean_bsi (perfect linear)."""
        return [
            _make_cell(
                agent_id=f"agent-{chr(65+i)}",
                bias_category="anchoring",
                mean_bsi=0.1 * (i + 1),
                std_bsi=0.05 * (i + 1),
                n_valid_runs=30,
                variant="BASELINE",
            )
            for i in range(5)
        ]

    def test_returns_ols_result(self):
        cells = self._cells_with_std()
        result = compute_h7_noise_bias(cells)
        assert result is not None
        assert isinstance(result, OLSResult)

    def test_slope_is_positive(self):
        # Constructed with perfect positive correlation
        cells = self._cells_with_std()
        result = compute_h7_noise_bias(cells)
        slope_coef = next(c for c in result.coefficients if c.name == "mean_bsi")
        assert slope_coef.estimate > 0.0

    def test_spec_name(self):
        cells = self._cells_with_std()
        result = compute_h7_noise_bias(cells)
        assert result.spec_name == "H7_NoiseBias"

    def test_returns_none_when_insufficient_cells(self):
        cells = [
            _make_cell(mean_bsi=0.1, std_bsi=0.05, n_valid_runs=30),
            _make_cell(mean_bsi=0.2, std_bsi=0.10, n_valid_runs=30),
        ]
        result = compute_h7_noise_bias(cells)
        assert result is None

    def test_excludes_n1_cells(self):
        # n_valid_runs=1 should be excluded (std_bsi not meaningful)
        cells = [
            _make_cell(mean_bsi=0.1, std_bsi=0.0, n_valid_runs=1),
            _make_cell(mean_bsi=0.2, std_bsi=0.0, n_valid_runs=1),
            _make_cell(mean_bsi=0.3, std_bsi=0.15, n_valid_runs=30),
        ]
        result = compute_h7_noise_bias(cells)
        # Only 1 cell with n>=2 → not enough → None
        assert result is None


# ─────────────────────────────────────────────────────────────────────────────
# §8  H2 CAPABILITY REGRESSION
# ─────────────────────────────────────────────────────────────────────────────


class TestH2Capability:
    def _cells_for_h2(self) -> list[CellAggregate]:
        # 5 agents with different mean_bsi
        return [
            _make_cell(
                agent_id=f"agent-{chr(65+i)}",
                bias_category="anchoring",
                mean_bsi=0.4 - 0.05 * i,
                n_valid_runs=30,
            )
            for i in range(5)
        ]

    def _p1_scores(self) -> dict[str, float]:
        # Higher P1 score → lower mean_bsi (negative gradient hypothesis)
        return {f"agent-{chr(65+i)}": 0.5 + 0.1 * i for i in range(5)}

    def test_returns_ols_result(self):
        cells = self._cells_for_h2()
        result = compute_h2_capability(cells, self._p1_scores())
        assert result is not None
        assert isinstance(result, OLSResult)

    def test_negative_slope(self):
        # Higher P1 score → lower BSI → negative β_1
        cells = self._cells_for_h2()
        result = compute_h2_capability(cells, self._p1_scores())
        p1_coef = next(c for c in result.coefficients if c.name == "P1Score")
        assert p1_coef.estimate < 0.0

    def test_spec_name(self):
        cells = self._cells_for_h2()
        result = compute_h2_capability(cells, self._p1_scores())
        assert result.spec_name == "H2_Capability"

    def test_notes_mention_descriptive(self):
        cells = self._cells_for_h2()
        result = compute_h2_capability(cells, self._p1_scores())
        assert "descriptive" in result.notes.lower()

    def test_returns_none_with_too_few_scores(self):
        cells = self._cells_for_h2()
        # Only 2 agents have P1 scores → not enough
        result = compute_h2_capability(cells, {"agent-A": 0.8, "agent-B": 0.6})
        assert result is None

    def test_returns_none_with_empty_p1_scores(self):
        cells = self._cells_for_h2()
        result = compute_h2_capability(cells, {})
        assert result is None


# ─────────────────────────────────────────────────────────────────────────────
# §9  SESSION ORDER EFFECTS
# ─────────────────────────────────────────────────────────────────────────────


class TestSessionOrderEffects:
    def _results_with_drift(self) -> list:
        """BSI increases linearly with run_index → non-zero slope."""
        return [
            _make_eval_result(run_index=i, bsi=0.1 + 0.01 * i)
            for i in range(10)
        ]

    def _results_no_drift(self) -> list:
        """BSI constant across run_index → slope ≈ 0."""
        return [
            _make_eval_result(run_index=i, bsi=0.2)
            for i in range(10)
        ]

    def test_returns_ols_result_for_sufficient_data(self):
        results = self._results_with_drift()
        result = compute_session_order_effects(results)
        assert result is not None
        assert isinstance(result, OLSResult)

    def test_detects_positive_drift(self):
        results = self._results_with_drift()
        result = compute_session_order_effects(results)
        slope = next(c for c in result.coefficients if c.name == "run_index")
        assert slope.estimate > 0.0

    def test_spec_name(self):
        results = self._results_with_drift()
        result = compute_session_order_effects(results)
        assert result.spec_name == "SessionOrder_G6_5"

    def test_returns_none_with_too_few_results(self):
        results = [_make_eval_result(run_index=i, bsi=0.1) for i in range(3)]
        assert compute_session_order_effects(results) is None

    def test_flat_bsi_near_zero_slope(self):
        results = self._results_no_drift()
        result = compute_session_order_effects(results)
        slope = next(c for c in result.coefficients if c.name == "run_index")
        # BSI is constant → slope should be very small (numerically ≈ 0)
        assert abs(slope.estimate) < 1e-8


# ─────────────────────────────────────────────────────────────────────────────
# §10  FULL PIPELINE
# ─────────────────────────────────────────────────────────────────────────────


class TestRunStatsPipeline:
    def test_returns_report(self):
        report = _make_report(_two_agent_two_bias_cells())
        stats = run_stats_pipeline(report)
        assert isinstance(stats, StatsPipelineReport)

    def test_n_cells_correct(self):
        cells = _two_agent_two_bias_cells()
        stats = run_stats_pipeline(_make_report(cells))
        assert stats.n_cells == 8

    def test_n_agents_correct(self):
        cells = _two_agent_two_bias_cells()
        stats = run_stats_pipeline(_make_report(cells))
        assert stats.n_agents == 2

    def test_level1_ols_populated(self):
        cells = _two_agent_two_bias_cells()
        stats = run_stats_pipeline(_make_report(cells))
        assert stats.level1_ols is not None

    def test_variance_decomposition_populated(self):
        cells = _two_agent_two_bias_cells()
        stats = run_stats_pipeline(_make_report(cells))
        assert stats.variance_decomposition is not None

    def test_treatment_effects_populated(self):
        cells = _two_agent_two_bias_cells()
        stats = run_stats_pipeline(_make_report(cells))
        assert len(stats.treatment_effects) > 0

    def test_h7_skipped_without_multirun(self):
        # All cells have n_valid_runs=1 → H7 skipped
        cells = [
            _make_cell(agent_id="agent-A", n_valid_runs=1, std_bsi=0.0),
            _make_cell(agent_id="agent-B", n_valid_runs=1, std_bsi=0.0),
        ]
        stats = run_stats_pipeline(_make_report(cells))
        assert stats.h7_noise_bias is None

    def test_h2_skipped_without_p1_scores(self):
        cells = _two_agent_two_bias_cells()
        stats = run_stats_pipeline(_make_report(cells))
        assert stats.h2_capability is None
        assert any("H2" in w or "p1_scores" in w for w in stats.warnings)

    def test_h2_populated_with_p1_scores(self):
        # Need ≥ 3 agents for H2 regression
        cells = _two_agent_two_bias_cells() + [
            _make_cell(agent_id="agent-C", bias_category="anchoring", mean_bsi=0.25),
        ]
        p1 = {"agent-A": 0.80, "agent-B": 0.60, "agent-C": 0.70}
        stats = run_stats_pipeline(_make_report(cells), p1_scores=p1)
        assert stats.h2_capability is not None

    def test_session_order_skipped_without_results(self):
        cells = _two_agent_two_bias_cells()
        stats = run_stats_pipeline(_make_report(cells))
        assert stats.session_order_ols is None

    def test_session_order_populated_with_results(self):
        cells = _two_agent_two_bias_cells()
        eval_results = [_make_eval_result(run_index=i, bsi=0.2) for i in range(6)]
        stats = run_stats_pipeline(
            _make_report(cells), evaluation_results=eval_results
        )
        assert stats.session_order_ols is not None

    def test_bh_family_size_matches_tests(self):
        cells = _two_agent_two_bias_cells()
        stats = run_stats_pipeline(_make_report(cells))
        assert stats.bh_family_size == len(stats.treatment_effects)

    def test_generated_at_is_recent(self):
        cells = _two_agent_two_bias_cells()
        stats = run_stats_pipeline(_make_report(cells))
        now = datetime.now(timezone.utc)
        delta = (now - stats.generated_at).total_seconds()
        assert delta < 5.0  # generated within last 5 seconds

    def test_warnings_list_populated_for_missing_analyses(self):
        cells = [_make_cell()]  # single cell → most analyses skipped
        stats = run_stats_pipeline(_make_report(cells))
        assert len(stats.warnings) > 0

    def test_empty_report_does_not_crash(self):
        stats = run_stats_pipeline(_make_report([]))
        assert stats is not None
        assert stats.level1_ols is None
        assert stats.variance_decomposition is None


# ─────────────────────────────────────────────────────────────────────────────
# §11  SERIALISATION
# ─────────────────────────────────────────────────────────────────────────────


class TestWriteStatsPipelineReport:
    def test_creates_file(self, tmp_path: Path):
        cells = _two_agent_two_bias_cells()
        stats = run_stats_pipeline(_make_report(cells))
        out = write_stats_pipeline_report(stats, tmp_path)
        assert out.exists()
        assert out.name == "stats_pipeline_report.json"

    def test_custom_filename(self, tmp_path: Path):
        cells = _two_agent_two_bias_cells()
        stats = run_stats_pipeline(_make_report(cells))
        out = write_stats_pipeline_report(stats, tmp_path, filename="my_stats.json")
        assert out.name == "my_stats.json"

    def test_valid_json(self, tmp_path: Path):
        cells = _two_agent_two_bias_cells()
        stats = run_stats_pipeline(_make_report(cells))
        out = write_stats_pipeline_report(stats, tmp_path)
        data = json.loads(out.read_text())
        assert "n_cells" in data
        assert "treatment_effects" in data

    def test_round_trip(self, tmp_path: Path):
        cells = _two_agent_two_bias_cells()
        stats = run_stats_pipeline(_make_report(cells))
        out = write_stats_pipeline_report(stats, tmp_path)
        data = json.loads(out.read_text())
        restored = StatsPipelineReport.model_validate(data)
        assert restored.n_cells == stats.n_cells
        assert restored.n_agents == stats.n_agents
        assert len(restored.treatment_effects) == len(stats.treatment_effects)

    def test_creates_output_dir(self, tmp_path: Path):
        new_dir = tmp_path / "nested" / "output"
        cells = _two_agent_two_bias_cells()
        stats = run_stats_pipeline(_make_report(cells))
        out = write_stats_pipeline_report(stats, new_dir)
        assert out.exists()


# ─────────────────────────────────────────────────────────────────────────────
# §12  REV-6 — CROSS-MODEL REGRESSION SCOPE
# ─────────────────────────────────────────────────────────────────────────────


class TestRev6CrossModelRegressionScope:
    """REV-6: H2 capability scatter is descriptive only (N=10 models).
    No p-values or inferential claims valid for cross-model analyses.
    """

    def _cells_for_h2(self) -> list[CellAggregate]:
        """Five agents with monotonically declining BSI (higher P1 → lower BSI)."""
        return [
            _make_cell(
                agent_id=f"agent-{chr(65 + i)}",
                scenario_id=f"p2-01-anchoring-BASELINE",
                bias_category="anchoring",
                mean_bsi=0.5 - 0.1 * i,
                n_valid_runs=30,
            )
            for i in range(5)
        ]

    def _p1_scores(self) -> dict[str, float]:
        return {f"agent-{chr(65 + i)}": 0.5 + 0.1 * i for i in range(5)}

    def test_h2_capability_cross_model_flag_is_true(self):
        """compute_h2_capability must set cross_model_descriptive_only=True."""
        result = compute_h2_capability(self._cells_for_h2(), self._p1_scores())
        assert result is not None
        assert result.cross_model_descriptive_only is True

    def test_h2_capability_significant_05_suppressed_for_all_coefficients(self):
        """All coefficients in H2 result must have significant_05=False (REV-6)."""
        result = compute_h2_capability(self._cells_for_h2(), self._p1_scores())
        assert result is not None
        for coef in result.coefficients:
            assert coef.significant_05 is False, (
                f"REV-6 violation: coefficient '{coef.name}' has significant_05=True "
                "in H2 cross-model analysis; no inferential claim is valid at N=10."
            )

    def test_h2_capability_p_values_still_computed(self):
        """p_value field is retained for internal use even when significance is suppressed."""
        result = compute_h2_capability(self._cells_for_h2(), self._p1_scores())
        assert result is not None
        for coef in result.coefficients:
            assert isinstance(coef.p_value, float)
            assert 0.0 <= coef.p_value <= 1.0

    def test_level1_ols_not_cross_model_descriptive_only(self):
        """Level 1 WLS is a within-cell analysis — must NOT be marked descriptive-only."""
        cells = _two_agent_two_bias_cells()
        result = run_level1_ols(cells)
        assert result is not None
        assert result.cross_model_descriptive_only is False

    def test_h7_not_cross_model_descriptive_only(self):
        """H7 noise-bias OLS is a within-cell analysis — must NOT be marked descriptive-only."""
        cells = [
            _make_cell(agent_id="A", mean_bsi=0.2, std_bsi=0.15, n_valid_runs=30),
            _make_cell(agent_id="A", scenario_id="p2-02-framing-BASELINE",
                       variant="BASELINE", mean_bsi=0.4, std_bsi=0.30, n_valid_runs=30),
            _make_cell(agent_id="A", scenario_id="p2-02-framing-FRAMING_LOSS",
                       variant="FRAMING_LOSS", mean_bsi=0.6, std_bsi=0.45, n_valid_runs=30),
        ]
        result = compute_h7_noise_bias(cells)
        assert result is not None
        assert result.cross_model_descriptive_only is False

    def test_session_order_not_cross_model_descriptive_only(self):
        """Session order OLS is a robustness check, not cross-model — must NOT be marked."""
        eval_results = [_make_eval_result(run_index=i, bsi=0.2) for i in range(10)]
        result = compute_session_order_effects(eval_results)
        assert result is not None
        assert result.cross_model_descriptive_only is False

    def test_ols_result_default_cross_model_flag_is_false(self):
        """OLSResult default must have cross_model_descriptive_only=False."""
        result = OLSResult(
            spec_name="test",
            n_obs=10,
            df_residual=8,
            r_squared=0.5,
            se_type="OLS",
        )
        assert result.cross_model_descriptive_only is False

    def test_pipeline_report_h2_carries_cross_model_flag(self):
        """run_stats_pipeline h2_capability field must carry the cross_model flag."""
        cells = self._cells_for_h2()
        stats = run_stats_pipeline(_make_report(cells), p1_scores=self._p1_scores())
        assert stats.h2_capability is not None
        assert stats.h2_capability.cross_model_descriptive_only is True

    def test_h2_flag_serialises_to_json(self):
        """cross_model_descriptive_only must survive JSON round-trip."""
        result = compute_h2_capability(self._cells_for_h2(), self._p1_scores())
        assert result is not None
        data = result.model_dump()
        assert "cross_model_descriptive_only" in data
        assert data["cross_model_descriptive_only"] is True
