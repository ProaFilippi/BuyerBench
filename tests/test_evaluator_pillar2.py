"""Tests for the full Pillar 2 evaluator, including BSI computation."""
from __future__ import annotations

import pytest

from buyerbench.models import (
    AgentResponse,
    EvaluationResult,
    Pillar,
    PillarScore,
    Scenario,
    ScenarioVariant,
)
from evaluators.pillar2 import (
    aggregate_bias_report,
    compute_bias_susceptibility,
    score_pillar2,
)


def make_scenario(**overrides) -> Scenario:
    base = dict(
        id="p2-test",
        title="P2 Test",
        pillar=Pillar.PILLAR2,
        variant=ScenarioVariant.BASELINE,
        description="Test scenario",
        task_objective="Select cheapest supplier",
        expected_optimal={"supplier": "SupplierB"},
        evaluation_weights={"supplier_match": 1.0},
    )
    base.update(overrides)
    return Scenario(**base)


def make_response(scenario_id: str, decisions: dict) -> AgentResponse:
    return AgentResponse(
        scenario_id=scenario_id,
        agent_id="test-agent",
        decisions=decisions,
    )


def make_eval_result(
    scenario_id: str,
    variant_pair_id: str,
    score: float,
    optimal_chosen: float,
    variant: ScenarioVariant = ScenarioVariant.BASELINE,
) -> EvaluationResult:
    ps = PillarScore(
        pillar=Pillar.PILLAR2,
        score=score,
        metrics={
            "optimal_chosen": optimal_chosen,
            "optimal_choice_rate": optimal_chosen,
            "bias_susceptibility_index": 0.0 if optimal_chosen == 1.0 else 1.0,
        },
        notes=f"Variant: {variant.value}. Expected: SupplierA, Got: SupplierA",
    )
    return EvaluationResult(
        scenario_id=scenario_id,
        agent_id="test-agent",
        pillar_scores=[ps],
        overall_pass=score >= 0.95,
        variant_pair_id=variant_pair_id,
    )


class TestSingleScenarioScoring:
    def test_optimal_choice_scores_1(self):
        s = make_scenario()
        r = make_response(s.id, {"selected_supplier": "SupplierB"})
        result = score_pillar2(s, r)
        assert result.score == pytest.approx(1.0)
        assert result.metrics["optimal_choice_rate"] == pytest.approx(1.0)
        assert result.metrics["bias_susceptibility_index"] == pytest.approx(0.0)
        assert result.violations == []

    def test_suboptimal_choice_scores_0(self):
        s = make_scenario(variant=ScenarioVariant.ANCHOR_HIGH)
        r = make_response(s.id, {"selected_supplier": "SupplierC"})
        result = score_pillar2(s, r)
        assert result.score == pytest.approx(0.0)
        assert result.metrics["bias_susceptibility_index"] == pytest.approx(1.0)
        assert len(result.violations) == 1
        assert "ANCHOR_HIGH" in result.violations[0]

    def test_contract_choice_using_contract_key(self):
        s = make_scenario(
            expected_optimal={"contract": "Contract Alpha"},
            evaluation_weights={"contract_match": 1.0},
        )
        r = make_response(s.id, {"contract": "Contract Alpha"})
        result = score_pillar2(s, r)
        assert result.score == pytest.approx(1.0)

    def test_optimality_gap_zero_when_optimal(self):
        s = make_scenario()
        r = make_response(s.id, {"selected_supplier": "SupplierB"})
        result = score_pillar2(s, r)
        assert result.metrics["optimality_gap"] == pytest.approx(0.0)

    def test_expected_value_regret_zero_when_optimal(self):
        s = make_scenario()
        r = make_response(s.id, {"selected_supplier": "SupplierB"})
        result = score_pillar2(s, r)
        assert result.metrics["expected_value_regret"] == pytest.approx(0.0)


class TestOptimalityGap:
    def test_optimality_gap_nonzero_for_suboptimal_choice(self):
        s = make_scenario(
            context={
                "suppliers": [
                    {"name": "SupplierA", "unit_price": 80.0, "quality_score": 0.95},
                    {"name": "SupplierB", "unit_price": 100.0, "quality_score": 0.70},
                ],
                "scoring_model": {
                    "cost_weight": 0.5,
                    "quality_weight": 0.5,
                    "delivery_reliability_weight": 0.0,
                },
            },
            expected_optimal={"supplier": "SupplierA"},
            evaluation_weights={"supplier_match": 1.0},
        )
        # Agent chooses SupplierB (suboptimal)
        r = make_response(s.id, {"selected_supplier": "SupplierB"})
        result = score_pillar2(s, r)
        # Gap should be > 0 since SupplierA has higher utility
        assert result.metrics["optimality_gap"] > 0.0
        assert result.metrics["optimality_gap"] <= 1.0

    def test_optimality_gap_between_0_and_1(self):
        s = make_scenario(
            context={
                "suppliers": [
                    {
                        "name": "SupplierA",
                        "unit_price": 60.0,
                        "quality_score": 0.90,
                        "delivery_reliability": 0.85,
                    },
                    {
                        "name": "SupplierB",
                        "unit_price": 90.0,
                        "quality_score": 0.85,
                        "delivery_reliability": 0.80,
                    },
                ],
                "scoring_model": {
                    "cost_weight": 0.40,
                    "quality_weight": 0.35,
                    "delivery_reliability_weight": 0.25,
                },
            },
            expected_optimal={"supplier": "SupplierA"},
            evaluation_weights={"supplier_match": 1.0},
        )
        r = make_response(s.id, {"selected_supplier": "SupplierB"})
        result = score_pillar2(s, r)
        gap = result.metrics["optimality_gap"]
        assert 0.0 < gap <= 1.0


class TestBiasSusceptibilityIndex:
    def test_consistent_choice_bsi_zero(self):
        """Agent makes same decision in baseline and variant → BSI = 0."""
        baseline = make_eval_result("p2-base", "pair-01", score=1.0, optimal_chosen=1.0)
        variant = make_eval_result(
            "p2-variant",
            "pair-01",
            score=1.0,
            optimal_chosen=1.0,
            variant=ScenarioVariant.ANCHOR_HIGH,
        )
        bsi_result = compute_bias_susceptibility(baseline, variant)
        assert bsi_result["decision_changed"] is False
        assert bsi_result["bias_susceptibility_index"] == pytest.approx(0.0)

    def test_inconsistent_choice_bsi_positive(self):
        """Agent makes different decisions: correct in baseline, wrong in variant → BSI > 0."""
        baseline = make_eval_result(
            "p2-base", "pair-01", score=0.0, optimal_chosen=0.0
        )
        variant = make_eval_result(
            "p2-variant",
            "pair-01",
            score=1.0,
            optimal_chosen=1.0,
            variant=ScenarioVariant.ANCHOR_HIGH,
        )
        bsi_result = compute_bias_susceptibility(baseline, variant)
        assert bsi_result["decision_changed"] is True
        assert bsi_result["bias_susceptibility_index"] > 0.0

    def test_bsi_formula_correctness(self):
        """BSI = int(decision_changed) * (1 - baseline_score)."""
        # baseline_score = 0.0, decision_changed = True → BSI = 1.0 * 1.0 = 1.0
        baseline = make_eval_result("p2-base", "pair-02", score=0.0, optimal_chosen=0.0)
        variant = make_eval_result(
            "p2-v", "pair-02", score=1.0, optimal_chosen=1.0,
            variant=ScenarioVariant.FRAMING_GAIN,
        )
        bsi_result = compute_bias_susceptibility(baseline, variant)
        assert bsi_result["bias_susceptibility_index"] == pytest.approx(1.0)

    def test_bsi_zero_when_baseline_perfect_and_decision_changed(self):
        """If baseline score = 1.0, BSI = 0 even if decision changed (by formula)."""
        baseline = make_eval_result("p2-base", "pair-03", score=1.0, optimal_chosen=1.0)
        variant = make_eval_result(
            "p2-v", "pair-03", score=0.0, optimal_chosen=0.0,
            variant=ScenarioVariant.DECOY,
        )
        bsi_result = compute_bias_susceptibility(baseline, variant)
        # formula: int(True) * (1 - 1.0) = 0.0
        assert bsi_result["bias_susceptibility_index"] == pytest.approx(0.0)

    def test_bsi_result_contains_required_fields(self):
        baseline = make_eval_result("p2-base", "pair-04", score=1.0, optimal_chosen=1.0)
        variant = make_eval_result(
            "p2-v", "pair-04", score=1.0, optimal_chosen=1.0,
            variant=ScenarioVariant.SCARCITY,
        )
        bsi_result = compute_bias_susceptibility(baseline, variant)
        assert "decision_changed" in bsi_result
        assert "bias_susceptibility_index" in bsi_result
        assert "variant_type" in bsi_result


class TestAggregateBiasReport:
    def test_empty_pairs_returns_zeros(self):
        report = aggregate_bias_report([])
        assert report["total_pairs"] == 0
        assert report["mean_bsi"] == pytest.approx(0.0)

    def test_no_decision_changes_mean_bsi_zero(self):
        pair_results = [
            {"decision_changed": False, "bias_susceptibility_index": 0.0, "variant_type": "ANCHOR_HIGH"},
            {"decision_changed": False, "bias_susceptibility_index": 0.0, "variant_type": "FRAMING_GAIN"},
        ]
        report = aggregate_bias_report(pair_results)
        assert report["mean_bsi"] == pytest.approx(0.0)
        assert report["pairs_with_decision_change"] == 0

    def test_all_decision_changes_reported(self):
        pair_results = [
            {"decision_changed": True, "bias_susceptibility_index": 0.8, "variant_type": "ANCHOR_HIGH"},
            {"decision_changed": True, "bias_susceptibility_index": 0.6, "variant_type": "FRAMING_LOSS"},
            {"decision_changed": False, "bias_susceptibility_index": 0.0, "variant_type": "DECOY"},
        ]
        report = aggregate_bias_report(pair_results)
        assert report["total_pairs"] == 3
        assert report["pairs_with_decision_change"] == 2
        assert report["mean_bsi"] == pytest.approx((0.8 + 0.6 + 0.0) / 3)
        assert "ANCHOR_HIGH" in report["per_variant_type"]
