"""Tests for research/analysis/bsi.py — BSI formula reconciliation with evaluators/pillar2.py."""
from __future__ import annotations

import math
import pytest

from research.analysis.bsi import (
    BSI_FORMULA,
    _PRODUCTION_MODULE,
    _extract_p2_metrics,
    _t_critical_95,
    bsi_from_result_pair,
    cell_bsi_stats,
    compute_bsi,
    decision_changed,
    validate_formula_consistency,
    _PANDAS_AVAILABLE,
)

pandas_required = pytest.mark.skipif(not _PANDAS_AVAILABLE, reason="pandas not installed")


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────


def _make_result_dict(
    scenario_id: str = "p2-01-baseline",
    agent_id: str = "mock-agent",
    variant: str = "BASELINE",
    variant_pair_id: str = "p2-01",
    score: float = 1.0,
    optimal_chosen: float = 1.0,
    run_index: int = 0,
) -> dict:
    return {
        "scenario_id": scenario_id,
        "agent_id": agent_id,
        "variant": variant,
        "variant_pair_id": variant_pair_id,
        "run_index": run_index,
        "pillar_scores": [
            {
                "pillar": "PILLAR2",
                "score": score,
                "metrics": {
                    "optimal_chosen": optimal_chosen,
                    "optimal_choice_rate": optimal_chosen,
                    "optimality_gap": 0.0,
                    "expected_value_regret": 0.0,
                    "bias_susceptibility_index": 0.0 if optimal_chosen == 1.0 else 1.0,
                },
                "violations": [],
                "notes": f"Variant: {variant}. Expected: SupplierA, Got: SupplierA",
            }
        ],
    }


# ─────────────────────────────────────────────────────────────────────────────
# FORMULA CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────


class TestFormulaConstants:
    def test_bsi_formula_string_present(self):
        assert isinstance(BSI_FORMULA, str)
        assert len(BSI_FORMULA) > 0

    def test_bsi_formula_mentions_decision_changed(self):
        assert "decision_changed" in BSI_FORMULA

    def test_bsi_formula_mentions_baseline_score(self):
        assert "baseline_score" in BSI_FORMULA

    def test_production_module_string(self):
        assert "pillar2" in _PRODUCTION_MODULE
        assert "compute_bias_susceptibility" in _PRODUCTION_MODULE


# ─────────────────────────────────────────────────────────────────────────────
# CORE FORMULA: compute_bsi
# ─────────────────────────────────────────────────────────────────────────────


class TestComputeBsi:
    def test_no_change_both_correct(self):
        """No decision change → BSI = 0 regardless of scores."""
        assert compute_bsi(1.0, 1.0, 1.0) == pytest.approx(0.0)

    def test_no_change_both_wrong(self):
        """No decision change → BSI = 0 regardless of scores."""
        assert compute_bsi(0.0, 0.0, 0.0) == pytest.approx(0.0)

    def test_wrong_to_right_flip_bsi_one(self):
        """Baseline wrong (score=0), variant right → BSI = 1.0."""
        assert compute_bsi(0.0, 1.0, 0.0) == pytest.approx(1.0)

    def test_right_to_wrong_flip_bsi_zero(self):
        """Baseline perfect (score=1.0), variant wrong → BSI = 0.0 by formula.

        This is the documented 'zero when baseline perfect' property.
        See module docstring for rationale.
        """
        assert compute_bsi(1.0, 0.0, 1.0) == pytest.approx(0.0)

    def test_partial_baseline_score(self):
        """Baseline score=0.5, decision changed → BSI = 0.5."""
        bsi = compute_bsi(0.0, 1.0, 0.5)
        assert bsi == pytest.approx(0.5)

    def test_high_baseline_score_attenuates_bsi(self):
        """BSI is scaled by (1 - baseline_score); high baseline → low BSI."""
        bsi_low_base = compute_bsi(0.0, 1.0, 0.2)
        bsi_high_base = compute_bsi(0.0, 1.0, 0.8)
        assert bsi_low_base > bsi_high_base

    def test_returns_float(self):
        assert isinstance(compute_bsi(0.0, 1.0, 0.0), float)

    def test_bsi_in_zero_one_range(self):
        for bo, vo, bs in [(0.0, 1.0, 0.0), (1.0, 0.0, 0.5), (0.0, 0.0, 0.3), (1.0, 1.0, 1.0)]:
            bsi = compute_bsi(bo, vo, bs)
            assert 0.0 <= bsi <= 1.0, f"BSI={bsi} out of range for ({bo}, {vo}, {bs})"


# ─────────────────────────────────────────────────────────────────────────────
# decision_changed helper
# ─────────────────────────────────────────────────────────────────────────────


class TestDecisionChanged:
    def test_same_values_no_change(self):
        assert decision_changed(1.0, 1.0) is False
        assert decision_changed(0.0, 0.0) is False

    def test_different_values_changed(self):
        assert decision_changed(0.0, 1.0) is True
        assert decision_changed(1.0, 0.0) is True

    def test_returns_bool(self):
        assert isinstance(decision_changed(0.0, 1.0), bool)


# ─────────────────────────────────────────────────────────────────────────────
# _extract_p2_metrics
# ─────────────────────────────────────────────────────────────────────────────


class TestExtractP2Metrics:
    def test_extracts_basic_fields(self):
        rd = _make_result_dict(score=1.0, optimal_chosen=1.0)
        m = _extract_p2_metrics(rd)
        assert m["score"] == pytest.approx(1.0)
        assert m["optimal_chosen"] == pytest.approx(1.0)
        assert m["agent_id"] == "mock-agent"
        assert m["variant"] == "BASELINE"
        assert m["variant_pair_id"] == "p2-01"
        assert m["run_index"] == 0

    def test_extracts_suboptimal(self):
        rd = _make_result_dict(score=0.0, optimal_chosen=0.0, variant="ANCHOR_HIGH")
        m = _extract_p2_metrics(rd)
        assert m["score"] == pytest.approx(0.0)
        assert m["optimal_chosen"] == pytest.approx(0.0)

    def test_empty_pillar_scores_defaults(self):
        rd = {"scenario_id": "x", "agent_id": "a", "pillar_scores": []}
        m = _extract_p2_metrics(rd)
        assert m["score"] == pytest.approx(0.0)
        assert m["optimal_chosen"] == pytest.approx(0.0)

    def test_missing_metrics_key(self):
        rd = {
            "scenario_id": "x",
            "agent_id": "a",
            "pillar_scores": [{"pillar": "PILLAR2", "score": 0.8, "violations": []}],
        }
        m = _extract_p2_metrics(rd)
        assert m["score"] == pytest.approx(0.8)
        assert m["optimal_chosen"] == pytest.approx(0.8)  # falls back to score


# ─────────────────────────────────────────────────────────────────────────────
# bsi_from_result_pair
# ─────────────────────────────────────────────────────────────────────────────


class TestBsiFromResultPair:
    def test_consistent_choice_bsi_zero(self):
        b = _make_result_dict(score=1.0, optimal_chosen=1.0)
        v = _make_result_dict(score=1.0, optimal_chosen=1.0, variant="ANCHOR_HIGH")
        result = bsi_from_result_pair(b, v)
        assert result["decision_changed"] is False
        assert result["bsi"] == pytest.approx(0.0)

    def test_wrong_to_right_flip_bsi_one(self):
        """Baseline wrong, variant right → BSI = 1.0."""
        b = _make_result_dict(score=0.0, optimal_chosen=0.0)
        v = _make_result_dict(score=1.0, optimal_chosen=1.0, variant="FRAMING_LOSS")
        result = bsi_from_result_pair(b, v)
        assert result["decision_changed"] is True
        assert result["bsi"] == pytest.approx(1.0)

    def test_right_to_wrong_flip_bsi_zero(self):
        """Right-to-wrong flip: BSI = 0.0 when baseline was perfect (formula property)."""
        b = _make_result_dict(score=1.0, optimal_chosen=1.0)
        v = _make_result_dict(score=0.0, optimal_chosen=0.0, variant="DECOY")
        result = bsi_from_result_pair(b, v)
        assert result["decision_changed"] is True
        assert result["bsi"] == pytest.approx(0.0)

    def test_result_contains_required_fields(self):
        b = _make_result_dict()
        v = _make_result_dict(variant="SCARCITY", score=0.0, optimal_chosen=0.0)
        result = bsi_from_result_pair(b, v)
        expected_keys = {
            "baseline_scenario_id", "variant_scenario_id", "agent_id",
            "variant_pair_id", "variant_type", "run_index",
            "baseline_optimal_chosen", "variant_optimal_chosen",
            "baseline_score", "decision_changed", "bsi",
        }
        assert expected_keys.issubset(result.keys())

    def test_variant_type_extracted(self):
        b = _make_result_dict()
        v = _make_result_dict(variant="SUNK_COST")
        result = bsi_from_result_pair(b, v)
        assert result["variant_type"] == "SUNK_COST"

    def test_agent_id_propagated(self):
        b = _make_result_dict(agent_id="agent-X")
        v = _make_result_dict(agent_id="agent-X", variant="ANCHOR_HIGH")
        result = bsi_from_result_pair(b, v)
        assert result["agent_id"] == "agent-X"

    def test_partial_baseline_score(self):
        b = _make_result_dict(score=0.4, optimal_chosen=0.0)
        v = _make_result_dict(score=1.0, optimal_chosen=1.0, variant="ANCHOR_HIGH")
        result = bsi_from_result_pair(b, v)
        assert result["bsi"] == pytest.approx(0.6)

    def test_bsi_matches_compute_bsi(self):
        """bsi_from_result_pair must use the same formula as compute_bsi."""
        b = _make_result_dict(score=0.3, optimal_chosen=0.0)
        v = _make_result_dict(score=1.0, optimal_chosen=1.0, variant="ANCHOR_HIGH")
        pair_result = bsi_from_result_pair(b, v)
        direct_bsi = compute_bsi(0.0, 1.0, 0.3)
        assert pair_result["bsi"] == pytest.approx(direct_bsi)


# ─────────────────────────────────────────────────────────────────────────────
# cell_bsi_stats
# ─────────────────────────────────────────────────────────────────────────────


class TestCellBsiStats:
    def test_empty_list_returns_zeros(self):
        stats = cell_bsi_stats([])
        assert stats["n"] == 0
        assert stats["mean_bsi"] == pytest.approx(0.0)
        assert stats["exploratory_only"] is True

    def test_single_value(self):
        stats = cell_bsi_stats([1.0])
        assert stats["n"] == 1
        assert stats["mean_bsi"] == pytest.approx(1.0)
        assert stats["ci_lower_95"] == pytest.approx(1.0)
        assert stats["ci_upper_95"] == pytest.approx(1.0)
        assert stats["exploratory_only"] is True

    def test_all_zero_bsi(self):
        stats = cell_bsi_stats([0.0, 0.0, 0.0, 0.0])
        assert stats["mean_bsi"] == pytest.approx(0.0)
        assert stats["std_bsi"] == pytest.approx(0.0)
        assert stats["decision_change_rate"] == pytest.approx(0.0)

    def test_all_one_bsi(self):
        stats = cell_bsi_stats([1.0, 1.0, 1.0, 1.0])
        assert stats["mean_bsi"] == pytest.approx(1.0)
        assert stats["decision_change_rate"] == pytest.approx(1.0)

    def test_mixed_bsi_mean(self):
        bsi_vals = [1.0, 0.0, 1.0, 0.0]
        stats = cell_bsi_stats(bsi_vals)
        assert stats["mean_bsi"] == pytest.approx(0.5)
        assert stats["decision_change_rate"] == pytest.approx(0.5)

    def test_ci_lower_leq_mean_leq_upper(self):
        bsi_vals = [0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 1.0]
        stats = cell_bsi_stats(bsi_vals)
        assert stats["ci_lower_95"] <= stats["mean_bsi"] <= stats["ci_upper_95"]

    def test_ci_bounds_clamped_to_0_1(self):
        """CI bounds must always be in [0, 1]."""
        stats = cell_bsi_stats([1.0, 1.0])
        assert stats["ci_lower_95"] >= 0.0
        assert stats["ci_upper_95"] <= 1.0

    def test_n_equals_50_not_exploratory(self):
        bsi_vals = [0.0] * 25 + [1.0] * 25
        stats = cell_bsi_stats(bsi_vals)
        assert stats["n"] == 50
        assert stats["exploratory_only"] is False

    def test_n_equals_2_not_exploratory(self):
        stats = cell_bsi_stats([0.0, 1.0])
        assert stats["exploratory_only"] is False

    def test_required_keys_present(self):
        stats = cell_bsi_stats([0.5, 0.5])
        required = {"n", "mean_bsi", "std_bsi", "ci_lower_95", "ci_upper_95",
                    "decision_change_rate", "exploratory_only"}
        assert required.issubset(stats.keys())


# ─────────────────────────────────────────────────────────────────────────────
# _t_critical_95
# ─────────────────────────────────────────────────────────────────────────────


class TestTCritical95:
    def test_large_df_returns_z(self):
        """df >= 30 → z = 1.960 approximation."""
        assert _t_critical_95(31) == pytest.approx(1.960)
        assert _t_critical_95(100) == pytest.approx(1.960)

    def test_small_df_larger_than_z(self):
        """For small n, critical value should exceed 1.96."""
        assert _t_critical_95(3) > 1.96
        assert _t_critical_95(10) > 1.96

    def test_n1_extreme(self):
        """n=1 → df=0 → clamped to df=1 (12.706)."""
        assert _t_critical_95(1) == pytest.approx(12.706)


# ─────────────────────────────────────────────────────────────────────────────
# build_bsi_dataframe (pandas required)
# ─────────────────────────────────────────────────────────────────────────────


@pandas_required
class TestBuildBsiDataframe:
    from research.analysis.bsi import build_bsi_dataframe

    def _pairs(self, n_pairs=2, n_runs=1):
        from research.analysis.bsi import build_bsi_dataframe  # noqa: F401 (needed for import)
        dicts = []
        for pair_idx in range(n_pairs):
            pair_id = f"p2-0{pair_idx + 1}-anchoring"
            for run_i in range(n_runs):
                dicts.append(_make_result_dict(
                    scenario_id=f"{pair_id}-BASELINE",
                    variant_pair_id=pair_id,
                    variant="BASELINE",
                    score=1.0,
                    optimal_chosen=1.0,
                    run_index=run_i,
                ))
                dicts.append(_make_result_dict(
                    scenario_id=f"{pair_id}-ANCHOR_HIGH",
                    variant_pair_id=pair_id,
                    variant="ANCHOR_HIGH",
                    score=0.0,
                    optimal_chosen=0.0,
                    run_index=run_i,
                ))
        return dicts

    def test_builds_dataframe(self):
        from research.analysis.bsi import build_bsi_dataframe
        df = build_bsi_dataframe(self._pairs())
        assert len(df) > 0

    def test_required_columns_present(self):
        from research.analysis.bsi import build_bsi_dataframe
        df = build_bsi_dataframe(self._pairs())
        required = {"agent_id", "variant_pair_id", "bias_category", "variant", "bsi"}
        assert required.issubset(df.columns)

    def test_one_row_per_variant_pair(self):
        """n=1 runs × 1 pair → 1 row (one variant row matched to baseline)."""
        from research.analysis.bsi import build_bsi_dataframe
        df = build_bsi_dataframe(self._pairs(n_pairs=1, n_runs=1))
        assert len(df) == 1

    def test_n_runs_per_pair(self):
        """n_runs per pair → n_runs rows per pair."""
        from research.analysis.bsi import build_bsi_dataframe
        df = build_bsi_dataframe(self._pairs(n_pairs=1, n_runs=5))
        assert len(df) == 5

    def test_bsi_column_values_in_range(self):
        from research.analysis.bsi import build_bsi_dataframe
        df = build_bsi_dataframe(self._pairs(n_pairs=2, n_runs=3))
        assert df["bsi"].between(0.0, 1.0).all()

    def test_bias_category_derived_from_variant_pair_id(self):
        from research.analysis.bsi import build_bsi_dataframe
        df = build_bsi_dataframe(self._pairs(n_pairs=1))
        # "p2-01-anchoring" → bias_category = "anchoring"
        assert df["bias_category"].iloc[0] == "anchoring"

    def test_no_baselines_raises(self):
        from research.analysis.bsi import build_bsi_dataframe
        # All variant rows, no baselines — should raise ValueError
        variants_only = [
            _make_result_dict(variant="ANCHOR_HIGH", variant_pair_id="p2-01")
        ]
        with pytest.raises(ValueError):
            build_bsi_dataframe(variants_only)

    def test_empty_list_raises(self):
        from research.analysis.bsi import build_bsi_dataframe
        with pytest.raises((ValueError, Exception)):
            build_bsi_dataframe([])


# ─────────────────────────────────────────────────────────────────────────────
# validate_formula_consistency
# ─────────────────────────────────────────────────────────────────────────────


class TestValidateFormulaConsistency:
    def test_returns_dict(self):
        result = validate_formula_consistency()
        assert isinstance(result, dict)

    def test_consistent_field_is_true(self):
        """Research formula must match production formula for all canonical cases."""
        result = validate_formula_consistency()
        assert result["consistent"] is True, (
            f"Formula inconsistency detected: {result['discrepancies']}"
        )

    def test_no_discrepancies(self):
        result = validate_formula_consistency()
        assert result["discrepancies"] == []

    def test_cases_checked_positive(self):
        result = validate_formula_consistency()
        assert result["cases_checked"] > 0

    def test_formula_field_matches_constant(self):
        result = validate_formula_consistency()
        assert result["formula"] == BSI_FORMULA

    def test_production_module_field(self):
        result = validate_formula_consistency()
        assert "pillar2" in result["production_module"]

    def test_required_keys(self):
        result = validate_formula_consistency()
        assert {"consistent", "cases_checked", "production_module", "formula", "discrepancies"}.issubset(
            result.keys()
        )


# ─────────────────────────────────────────────────────────────────────────────
# FORMULA PROPERTY: zero-when-baseline-perfect
# This is the most important documented non-obvious property.
# ─────────────────────────────────────────────────────────────────────────────


class TestZeroWhenBasePerfectProperty:
    """Verify the documented 'BSI=0 when baseline_score=1.0' property at every layer."""

    def test_core_formula(self):
        """compute_bsi: baseline_score=1.0 → BSI=0 regardless of decision change."""
        assert compute_bsi(1.0, 0.0, 1.0) == pytest.approx(0.0)

    def test_result_pair_level(self):
        """bsi_from_result_pair: same property."""
        b = _make_result_dict(score=1.0, optimal_chosen=1.0)
        v = _make_result_dict(score=0.0, optimal_chosen=0.0, variant="DECOY")
        result = bsi_from_result_pair(b, v)
        assert result["decision_changed"] is True  # change IS detected
        assert result["bsi"] == pytest.approx(0.0)  # BSI is still 0

    def test_decision_changed_still_flagged(self):
        """Even when BSI=0 due to formula, decision_changed captures the flip."""
        b = _make_result_dict(score=1.0, optimal_chosen=1.0)
        v = _make_result_dict(score=0.0, optimal_chosen=0.0, variant="ANCHOR_HIGH")
        result = bsi_from_result_pair(b, v)
        assert result["decision_changed"] is True

    def test_symmetric_case_gives_nonzero(self):
        """Complementary case (wrong baseline, changed decision) gives BSI=1.0."""
        assert compute_bsi(0.0, 1.0, 0.0) == pytest.approx(1.0)
