"""Tests for research/analysis/regression.py (PILLAR2-RESEARCH-06 L.6)."""
from __future__ import annotations

import math
from typing import Any

import pytest

from research.analysis.regression import (
    RegressionCoefficient,
    RegressionResult,
    VarianceDecompositionResult,
    VariancePartition,
    _PANDAS_AVAILABLE,
    _STATSMODELS_AVAILABLE,
    _betacf,
    _betainc,
    _is_treatment,
    _solve_linear,
    _t_critical_95,
    _t_pvalue,
    _wls_fallback,
    apply_bh_correction,
    run_capability_regression,
    run_primary_regression,
    run_variance_decomposition,
)

# All tests that require pandas are skipped when pandas is absent (CI without extras).
pandas_required = pytest.mark.skipif(not _PANDAS_AVAILABLE, reason="pandas not installed")


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────


def _make_df(
    agents: list[str] | None = None,
    biases: list[str] | None = None,
    n_runs: int = 4,
    treatment_bsi: float = 0.50,
    baseline_bsi: float = 0.10,
):
    """Build a minimal run-level DataFrame: agents × biases × {BASELINE, TREATMENT}."""
    if not _PANDAS_AVAILABLE:
        return None
    import pandas as pd

    agents = agents or ["agent-A", "agent-B"]
    biases = biases or ["anchoring", "framing"]

    rows = []
    run_counter = 0
    for agent in agents:
        for bias in biases:
            for variant, bsi in [("BASELINE", baseline_bsi), ("ANCHOR_HIGH", treatment_bsi)]:
                for i in range(n_runs):
                    run_counter += 1
                    rows.append(
                        {
                            "run_id": f"run-{run_counter:04d}",
                            "agent_id": agent,
                            "bias_category": bias,
                            "variant": variant,
                            "bsi": bsi + 0.01 * i,  # tiny jitter so std > 0
                            "temperature": 0.7,
                        }
                    )
    return pd.DataFrame(rows)


def _make_df_single_agent():
    if not _PANDAS_AVAILABLE:
        return None
    import pandas as pd
    rows = [
        {"run_id": f"r{i}", "agent_id": "agent-A", "bias_category": "anchoring",
         "variant": "BASELINE", "bsi": 0.1, "temperature": 0.7}
        for i in range(4)
    ]
    return pd.DataFrame(rows)


def _make_df_with_warp():
    """DataFrame that includes WARP_AB rows (should be dropped)."""
    if not _PANDAS_AVAILABLE:
        return None
    base = _make_df()
    import pandas as pd
    warp_rows = pd.DataFrame([
        {"run_id": "warp-1", "agent_id": "agent-A", "bias_category": "warp",
         "variant": "WARP_AB", "bsi": 0.3, "temperature": 0.7},
        {"run_id": "warp-2", "agent_id": "agent-B", "bias_category": "warp",
         "variant": "WARP_AB", "bsi": 0.4, "temperature": 0.7},
    ])
    return pd.concat([base, warp_rows], ignore_index=True)


def _make_p1_scores(agents: list[str] | None = None) -> dict[str, float]:
    agents = agents or ["agent-A", "agent-B"]
    return {a: 0.5 + 0.1 * i for i, a in enumerate(sorted(agents))}


# ─────────────────────────────────────────────────────────────────────────────
# §1  INTERNAL HELPERS
# ─────────────────────────────────────────────────────────────────────────────


class TestIsTreatment:
    def test_baseline_is_control(self):
        assert _is_treatment("BASELINE") is False

    def test_framing_gain_is_control(self):
        assert _is_treatment("FRAMING_GAIN") is False

    def test_warp_variants_are_control(self):
        for v in ["WARP_AB", "WARP_BC", "WARP_AC"]:
            assert _is_treatment(v) is False

    def test_anchor_high_is_treatment(self):
        assert _is_treatment("ANCHOR_HIGH") is True

    def test_framing_loss_is_treatment(self):
        assert _is_treatment("FRAMING_LOSS") is True

    def test_decoy_is_treatment(self):
        assert _is_treatment("DECOY") is True

    def test_none_is_false(self):
        assert _is_treatment(None) is False


class TestTCritical:
    def test_large_df(self):
        assert _t_critical_95(100) == pytest.approx(1.960)

    def test_known_df9(self):
        assert _t_critical_95(9) == pytest.approx(2.262, abs=1e-3)

    def test_df1(self):
        assert _t_critical_95(1) == pytest.approx(12.706, abs=1e-3)


class TestBetainc:
    def test_x_zero(self):
        assert _betainc(0.5, 0.5, 0.0) == pytest.approx(0.0)

    def test_x_one(self):
        assert _betainc(0.5, 0.5, 1.0) == pytest.approx(1.0)

    def test_symmetric_half(self):
        for a in [1.0, 2.0, 5.0]:
            assert _betainc(a, a, 0.5) == pytest.approx(0.5, abs=1e-5)


class TestTPvalue:
    def test_zero_t_stat(self):
        for df in [1, 5, 30]:
            assert _t_pvalue(0.0, df) == pytest.approx(1.0, abs=1e-4)

    def test_known_t9_2262(self):
        p = _t_pvalue(2.262, 9)
        assert p == pytest.approx(0.05, abs=0.002)

    def test_negative_df_returns_1(self):
        assert _t_pvalue(2.0, 0) == pytest.approx(1.0)

    def test_large_t_small_p(self):
        assert _t_pvalue(10.0, 30) < 0.001


class TestSolveLinear:
    def test_2x2(self):
        # 2x + y = 5, x + 3y = 10 → x=1, y=3
        x = _solve_linear([[2.0, 1.0], [1.0, 3.0]], [5.0, 10.0])
        assert x[0] == pytest.approx(1.0, abs=1e-9)
        assert x[1] == pytest.approx(3.0, abs=1e-9)

    def test_singular_raises(self):
        with pytest.raises(ValueError, match="Singular"):
            _solve_linear([[1.0, 2.0], [2.0, 4.0]], [1.0, 2.0])


class TestWlsFallback:
    def test_returns_regression_result(self):
        X = [[1.0, 0.0], [1.0, 0.0], [1.0, 1.0], [1.0, 1.0]]
        y = [0.1, 0.1, 0.4, 0.4]
        w = [1.0] * 4
        result = _wls_fallback(X, y, w, ["Intercept", "Treatment"], "Test")
        assert isinstance(result, RegressionResult)

    def test_treatment_coefficient_positive(self):
        X = [[1.0, 0.0], [1.0, 0.0], [1.0, 1.0], [1.0, 1.0]]
        y = [0.1, 0.1, 0.4, 0.4]
        w = [1.0] * 4
        result = _wls_fallback(X, y, w, ["Intercept", "Treatment"], "Test")
        treat = next(c for c in result.coefficients if c.name == "Treatment")
        assert treat.estimate > 0.0

    def test_r_squared_in_range(self):
        X = [[1.0, 0.0], [1.0, 0.0], [1.0, 1.0], [1.0, 1.0]]
        y = [0.1, 0.1, 0.4, 0.4]
        result = _wls_fallback(X, y, [1.0] * 4, ["Intercept", "Treatment"], "Test")
        assert 0.0 <= result.r_squared <= 1.0

    def test_backend_label(self):
        X = [[1.0, x] for x in [0.0, 0.5, 1.0, 1.5]]
        y = [0.1, 0.2, 0.3, 0.4]
        result = _wls_fallback(X, y, [1.0] * 4, ["Intercept", "X"], "Test")
        assert result.backend == "fallback_wls"


# ─────────────────────────────────────────────────────────────────────────────
# §2  APPLY_BH_CORRECTION
# ─────────────────────────────────────────────────────────────────────────────


class TestApplyBHCorrection:
    def test_empty(self):
        adj, rej = apply_bh_correction([])
        assert adj == []
        assert rej == []

    def test_single_p_rejected(self):
        adj, rej = apply_bh_correction([0.03])
        assert rej[0] is True
        assert adj[0] == pytest.approx(0.03)

    def test_all_large_p_not_rejected(self):
        _, rej = apply_bh_correction([0.8, 0.9, 0.95])
        assert not any(rej)

    def test_known_example(self):
        # p=[0.03, 0.01, 0.10]; sorted=[0.01, 0.03, 0.10]
        # adj=[0.03, 0.045, 0.10] → reject=[True, True, False]
        adj, rej = apply_bh_correction([0.03, 0.01, 0.10])
        assert rej[0] is True
        assert rej[1] is True
        assert rej[2] is False

    def test_preserves_input_order(self):
        p = [0.10, 0.01, 0.05, 0.30]
        adj, rej = apply_bh_correction(p)
        assert len(adj) == 4
        assert len(rej) == 4

    def test_custom_alpha(self):
        p = [0.03, 0.01, 0.10]
        _, rej_strict = apply_bh_correction(p, alpha=0.01)
        _, rej_loose = apply_bh_correction(p, alpha=0.10)
        for i in range(3):
            if rej_strict[i]:
                assert rej_loose[i]

    def test_all_zeros_rejected(self):
        _, rej = apply_bh_correction([0.0, 0.0, 0.0])
        assert all(rej)

    def test_monotone_adjusted(self):
        # Adjusted p-values must be non-decreasing in sorted rank order
        p = [0.001, 0.03, 0.04, 0.09, 0.20]
        adj, _ = apply_bh_correction(p)
        order = sorted(range(5), key=lambda i: p[i])
        adj_sorted = [adj[i] for i in order]
        for i in range(len(adj_sorted) - 1):
            assert adj_sorted[i] <= adj_sorted[i + 1] + 1e-9

    def test_consistent_with_stats_pipeline(self):
        """Cross-check with the production implementation for identical output."""
        from results.stats_pipeline import bh_fdr_correction as prod_bh
        p = [0.04, 0.002, 0.15, 0.08, 0.30]
        research_adj, research_rej = apply_bh_correction(p)
        prod_adj, prod_rej = prod_bh(p)
        assert research_adj == pytest.approx(prod_adj, abs=1e-10)
        assert research_rej == prod_rej


# ─────────────────────────────────────────────────────────────────────────────
# §3  RUN_PRIMARY_REGRESSION
# ─────────────────────────────────────────────────────────────────────────────


@pandas_required
class TestRunPrimaryRegression:
    def test_returns_regression_result(self):
        df = _make_df()
        result = run_primary_regression(df)
        assert isinstance(result, RegressionResult)

    def test_has_treatment_coefficient(self):
        df = _make_df()
        result = run_primary_regression(df)
        names = [c.name for c in result.coefficients]
        # Regardless of backend, a treatment-related coefficient must be present
        assert any("treatment" in name.lower() for name in names)

    def test_treatment_coefficient_positive(self):
        # All treatment rows have higher BSI → β_treatment > 0
        df = _make_df(treatment_bsi=0.60, baseline_bsi=0.10)
        result = run_primary_regression(df)
        treat_coef = next(
            c for c in result.coefficients
            if "treatment" in c.name.lower()
        )
        assert treat_coef.estimate > 0.0

    def test_n_obs_correct(self):
        df = _make_df(n_runs=5)
        # 2 agents × 2 biases × 2 variants × 5 runs = 40
        result = run_primary_regression(df)
        assert result.n_obs == 40

    def test_warp_rows_excluded(self):
        df = _make_df_with_warp()
        n_non_warp = len(df[~df["variant"].isin(["WARP_AB", "WARP_BC", "WARP_AC"])])
        result = run_primary_regression(df)
        assert result.n_obs == n_non_warp

    def test_missing_column_raises(self):
        df = _make_df()
        df = df.drop(columns=["bias_category"])
        with pytest.raises(ValueError, match="bias_category"):
            run_primary_regression(df)

    def test_backend_field_set(self):
        df = _make_df()
        result = run_primary_regression(df)
        assert result.backend in (
            "statsmodels_mixedlm",
            "statsmodels_ols",
            "fallback_wls",
            "PrimaryMixedLM_WLS",
        )

    def test_coefficients_have_se_and_pvalue(self):
        df = _make_df()
        result = run_primary_regression(df)
        for coef in result.coefficients:
            assert coef.se >= 0.0
            assert 0.0 <= coef.p_value <= 1.0
            assert coef.ci_lower_95 <= coef.estimate <= coef.ci_upper_95

    def test_spec_name_is_primary(self):
        df = _make_df()
        result = run_primary_regression(df)
        assert "primary" in result.spec_name.lower() or "mixedlm" in result.spec_name.lower()

    def test_custom_column_names(self):
        import pandas as pd
        df = _make_df().rename(columns={
            "bsi": "score",
            "agent_id": "model_id",
            "bias_category": "bias",
            "variant": "condition",
        })
        result = run_primary_regression(
            df,
            bsi_col="score",
            model_col="model_id",
            bias_col="bias",
            variant_col="condition",
        )
        assert isinstance(result, RegressionResult)

    def test_empty_after_warp_filter_raises(self):
        import pandas as pd
        # All rows are WARP variants
        df = pd.DataFrame([
            {"run_id": "w1", "agent_id": "A", "bias_category": "warp",
             "variant": "WARP_AB", "bsi": 0.3, "temperature": 0.7},
        ])
        with pytest.raises(ValueError):
            run_primary_regression(df)


# ─────────────────────────────────────────────────────────────────────────────
# §4  RUN_CAPABILITY_REGRESSION
# ─────────────────────────────────────────────────────────────────────────────


@pandas_required
class TestRunCapabilityRegression:
    def _enough_agents_df(self):
        # Need ≥ 3 agents with P1 scores
        return _make_df(agents=["agent-A", "agent-B", "agent-C"])

    def _enough_p1(self):
        return {"agent-A": 0.80, "agent-B": 0.60, "agent-C": 0.70}

    def test_returns_regression_result(self):
        df = self._enough_agents_df()
        result = run_capability_regression(df, self._enough_p1())
        assert isinstance(result, RegressionResult)

    def test_returns_none_with_too_few_agents(self):
        df = _make_df()  # only 2 agents
        result = run_capability_regression(df, _make_p1_scores())
        assert result is None

    def test_returns_none_with_no_p1(self):
        df = self._enough_agents_df()
        result = run_capability_regression(df, {})
        assert result is None

    def test_spec_name(self):
        df = self._enough_agents_df()
        result = run_capability_regression(df, self._enough_p1())
        assert result.spec_name == "H2_Capability"

    def test_p1score_coef_exists(self):
        df = self._enough_agents_df()
        result = run_capability_regression(df, self._enough_p1())
        assert any(c.name == "P1Score" for c in result.coefficients)

    def test_notes_mention_descriptive(self):
        df = self._enough_agents_df()
        result = run_capability_regression(df, self._enough_p1())
        assert "descriptive" in result.notes.lower()

    def test_n_obs_equals_n_agents_with_p1(self):
        df = self._enough_agents_df()
        p1 = self._enough_p1()
        result = run_capability_regression(df, p1)
        # One observation per agent (after aggregation)
        assert result.n_obs == 3

    def test_negative_slope_when_higher_p1_lower_bsi(self):
        import pandas as pd
        # Build data where agent with higher P1 has lower BSI
        agents = [f"agent-{c}" for c in "ABCDE"]
        rows = []
        for i, agent in enumerate(agents):
            bsi = 0.50 - 0.08 * i  # decreasing with agent index
            for _ in range(4):
                rows.append({
                    "run_id": f"{agent}-r",
                    "agent_id": agent,
                    "bias_category": "anchoring",
                    "variant": "BASELINE",
                    "bsi": bsi,
                    "temperature": 0.7,
                })
        df = pd.DataFrame(rows)
        p1 = {f"agent-{c}": 0.5 + 0.1 * i for i, c in enumerate("ABCDE")}
        result = run_capability_regression(df, p1)
        p1_coef = next(c for c in result.coefficients if c.name == "P1Score")
        assert p1_coef.estimate < 0.0


# ─────────────────────────────────────────────────────────────────────────────
# §5  RUN_VARIANCE_DECOMPOSITION
# ─────────────────────────────────────────────────────────────────────────────


@pandas_required
class TestRunVarianceDecomposition:
    def test_returns_decomposition(self):
        df = _make_df()
        vd = run_variance_decomposition(df)
        assert isinstance(vd, VarianceDecompositionResult)

    def test_sources_present(self):
        df = _make_df()
        vd = run_variance_decomposition(df)
        sources = {row.source for row in vd.rows}
        assert "Model" in sources
        assert "BiasType" in sources
        assert "Treatment" in sources
        assert "Residual" in sources

    def test_temperature_source_when_multiple_temps(self):
        import pandas as pd
        df = _make_df()
        df_temp2 = df.copy()
        df_temp2["temperature"] = 0.0
        combined = pd.concat([df, df_temp2], ignore_index=True)
        vd = run_variance_decomposition(combined)
        sources = {row.source for row in vd.rows}
        assert "Temperature" in sources

    def test_no_temperature_source_for_single_temp(self):
        df = _make_df()  # all temperature=0.7
        vd = run_variance_decomposition(df)
        sources = {row.source for row in vd.rows}
        assert "Temperature" not in sources

    def test_eta_squared_sums_to_at_most_one(self):
        df = _make_df()
        vd = run_variance_decomposition(df)
        total_eta = sum(row.eta_squared for row in vd.rows if row.source != "Residual")
        assert total_eta <= 1.0 + 1e-9

    def test_treatment_eta_positive(self):
        df = _make_df(treatment_bsi=0.60, baseline_bsi=0.10)
        vd = run_variance_decomposition(df)
        treat_eta = vd.eta_squared("Treatment")
        assert treat_eta is not None
        assert treat_eta > 0.0

    def test_n_obs_correct(self):
        df = _make_df(n_runs=3)
        # 2 agents × 2 biases × 2 variants × 3 runs = 24 (WARP excluded = 0 here)
        vd = run_variance_decomposition(df)
        assert vd.n_obs == 24

    def test_returns_none_too_few_rows(self):
        import pandas as pd
        df = pd.DataFrame([
            {"agent_id": "A", "bias_category": "anch", "variant": "BASELINE", "bsi": 0.1, "temperature": 0.7},
            {"agent_id": "A", "bias_category": "anch", "variant": "BASELINE", "bsi": 0.2, "temperature": 0.7},
        ])
        vd = run_variance_decomposition(df)
        assert vd is None

    def test_warp_rows_excluded_from_count(self):
        df = _make_df_with_warp()
        n_non_warp = len(df[~df["variant"].isin(["WARP_AB", "WARP_BC", "WARP_AC"])])
        vd = run_variance_decomposition(df)
        assert vd.n_obs == n_non_warp

    def test_eta_squared_method(self):
        df = _make_df()
        vd = run_variance_decomposition(df)
        assert vd.eta_squared("Model") is not None
        assert vd.eta_squared("NonExistent") is None

    def test_total_ss_positive(self):
        df = _make_df(treatment_bsi=0.5, baseline_bsi=0.1)
        vd = run_variance_decomposition(df)
        assert vd.total_ss > 0.0

    def test_skip_temperature_when_col_none(self):
        df = _make_df()
        vd = run_variance_decomposition(df, temperature_col=None)
        sources = {row.source for row in vd.rows}
        assert "Temperature" not in sources
