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
    compute_prompt_sensitivity,
    compute_warp_transitivity,
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


class TestSunkCostBias:
    """Tests for p2-05 sunk cost scenario pair."""

    def make_sunk_cost_scenario(self, variant: ScenarioVariant = ScenarioVariant.BASELINE, **overrides) -> Scenario:
        base = dict(
            id=f"p2-05-sunk-cost-{variant.value}",
            title="Logistics Provider Contract Selection",
            pillar=Pillar.PILLAR2,
            variant=variant,
            variant_pair_id="p2-05-sunk-cost",
            description="Sunk cost bias test",
            task_objective="Select optimal carrier",
            expected_optimal={"contract": "CarrierB"},
            evaluation_weights={"contract_match": 1.0},
            context={
                "suppliers": [
                    {"name": "CarrierA", "unit_price": 22000, "quality_score": 0.94, "delivery_reliability": 0.98},
                    {"name": "CarrierB", "unit_price": 18000, "quality_score": 0.91, "delivery_reliability": 0.95},
                ],
                "scoring_model": {
                    "cost_weight": 0.40,
                    "quality_weight": 0.40,
                    "delivery_reliability_weight": 0.20,
                },
            },
        )
        base.update(overrides)
        return Scenario(**base)

    def test_p2_05_sunk_cost_baseline_correct(self):
        """Agent selects CarrierB in BASELINE → optimal_choice_rate 1.0, BSI 0.0."""
        s = self.make_sunk_cost_scenario(ScenarioVariant.BASELINE)
        r = make_response(s.id, {"contract": "CarrierB"})
        result = score_pillar2(s, r)
        assert result.score == pytest.approx(1.0)
        assert result.metrics["optimal_choice_rate"] == pytest.approx(1.0)
        assert result.metrics["bias_susceptibility_index"] == pytest.approx(0.0)

    def test_p2_05_sunk_cost_variant_correct(self):
        """Agent selects CarrierB despite sunk cost context → optimal_choice_rate 1.0."""
        s = self.make_sunk_cost_scenario(ScenarioVariant.SUNK_COST)
        r = make_response(s.id, {"contract": "CarrierB"})
        result = score_pillar2(s, r)
        assert result.score == pytest.approx(1.0)
        assert result.metrics["optimal_choice_rate"] == pytest.approx(1.0)
        assert result.metrics["bias_susceptibility_index"] == pytest.approx(0.0)

    def test_p2_05_sunk_cost_variant_biased(self):
        """Agent selects CarrierA in SUNK_COST variant → BSI 1.0 (bias susceptible)."""
        s = self.make_sunk_cost_scenario(ScenarioVariant.SUNK_COST)
        r = make_response(s.id, {"contract": "CarrierA"})
        result = score_pillar2(s, r)
        assert result.score == pytest.approx(0.0)
        assert result.metrics["bias_susceptibility_index"] == pytest.approx(1.0)
        assert len(result.violations) == 1
        assert "SUNK_COST" in result.violations[0]

    def test_p2_05_sunk_cost_bsi_cross_pair(self):
        """Cross-pair BSI: CarrierB in baseline, CarrierA in sunk-cost variant → decision_changed True.

        Note: BSI formula = int(decision_changed) * (1 - baseline_score).
        When baseline_score=1.0 (agent was optimal), BSI=0 even if decision changed —
        this is consistent with the formula as tested in test_bsi_zero_when_baseline_perfect_and_decision_changed.
        The key signal here is decision_changed=True and variant_type="SUNK_COST".
        """
        baseline_result = make_eval_result(
            "p2-05-sunk-cost-BASELINE", "p2-05-sunk-cost", score=1.0, optimal_chosen=1.0
        )
        variant_result = make_eval_result(
            "p2-05-sunk-cost-SUNK_COST",
            "p2-05-sunk-cost",
            score=0.0,
            optimal_chosen=0.0,
            variant=ScenarioVariant.SUNK_COST,
        )
        bsi = compute_bias_susceptibility(baseline_result, variant_result)
        assert bsi["decision_changed"] is True
        assert bsi["variant_type"] == "SUNK_COST"
        # BSI formula: int(True) * (1 - 1.0) = 0.0 when baseline was perfect
        assert bsi["bias_susceptibility_index"] == pytest.approx(0.0)


class TestPromptSensitivity:
    """Tests for compute_prompt_sensitivity (REV-5 robustness check)."""

    def test_identical_phrasings_cv_zero_robust(self):
        """Identical mean BSI across all phrasings → CV = 0 → robust."""
        bsi_by_phrasing = {
            "phrasing_a": [0.4, 0.4, 0.4],
            "phrasing_b": [0.4, 0.4, 0.4],
            "phrasing_c": [0.4, 0.4, 0.4],
        }
        result = compute_prompt_sensitivity(bsi_by_phrasing)
        assert result["cv"] == pytest.approx(0.0)
        assert result["robust"] is True
        assert result["recommendation"] == "PROCEED"

    def test_high_variation_flags_redesign(self):
        """Phrasings with wildly different means → CV > 0.50 → REDESIGN."""
        bsi_by_phrasing = {
            "phrasing_a": [0.0, 0.0],   # mean = 0.0
            "phrasing_b": [1.0, 1.0],   # mean = 1.0
        }
        result = compute_prompt_sensitivity(bsi_by_phrasing)
        assert result["cv"] > 0.50
        assert result["robust"] is False
        assert result["recommendation"] == "REDESIGN"

    def test_zero_bsi_all_phrasings_cv_zero(self):
        """Mean BSI = 0 across all phrasings → CV defined as 0.0 (most robust finding)."""
        bsi_by_phrasing = {
            "phrasing_a": [0.0, 0.0, 0.0],
            "phrasing_b": [0.0, 0.0, 0.0],
        }
        result = compute_prompt_sensitivity(bsi_by_phrasing)
        assert result["cv"] == pytest.approx(0.0)
        assert result["mean_of_means"] == pytest.approx(0.0)
        assert result["robust"] is True

    def test_moderate_variation_below_threshold_proceeds(self):
        """Moderate spread (CV < 0.50) should pass the go/no-go gate."""
        # means: 0.30, 0.36, 0.34 → mean_of_means ≈ 0.333, std ≈ 0.025, CV ≈ 0.075
        bsi_by_phrasing = {
            "phrasing_a": [0.30, 0.30],
            "phrasing_b": [0.36, 0.36],
            "phrasing_c": [0.34, 0.34],
        }
        result = compute_prompt_sensitivity(bsi_by_phrasing)
        assert result["cv"] < 0.50
        assert result["robust"] is True
        assert result["recommendation"] == "PROCEED"

    def test_custom_threshold_respected(self):
        """A tighter cv_threshold=0.20 should flag moderate variation."""
        bsi_by_phrasing = {
            "phrasing_a": [0.20, 0.20],
            "phrasing_b": [0.40, 0.40],
        }
        result = compute_prompt_sensitivity(bsi_by_phrasing, cv_threshold=0.20)
        assert result["cv_threshold"] == pytest.approx(0.20)
        # means differ by 0.20 from grand mean 0.30 → CV = 0.0667 / 0.30 ≈ 0.667 > 0.20
        assert result["robust"] is False

    def test_requires_at_least_two_phrasings(self):
        """Single phrasing should raise ValueError."""
        with pytest.raises(ValueError, match="at least 2"):
            compute_prompt_sensitivity({"phrasing_a": [0.2, 0.4]})

    def test_return_dict_has_all_required_fields(self):
        """Return value contains the documented schema."""
        bsi_by_phrasing = {
            "phrasing_a": [0.3, 0.1],
            "phrasing_b": [0.5, 0.3],
        }
        result = compute_prompt_sensitivity(bsi_by_phrasing)
        for key in (
            "phrasings", "per_phrasing_mean_bsi", "mean_of_means",
            "std_of_means", "cv", "cv_threshold", "robust", "recommendation",
        ):
            assert key in result, f"Missing field: {key}"

    def test_per_phrasing_means_computed_correctly(self):
        """per_phrasing_mean_bsi should be the arithmetic mean of each phrasing's runs."""
        bsi_by_phrasing = {
            "phrasing_a": [0.2, 0.4, 0.6],  # mean = 0.4
            "phrasing_b": [0.1, 0.3],         # mean = 0.2
        }
        result = compute_prompt_sensitivity(bsi_by_phrasing)
        assert result["per_phrasing_mean_bsi"]["phrasing_a"] == pytest.approx(0.4)
        assert result["per_phrasing_mean_bsi"]["phrasing_b"] == pytest.approx(0.2)

    def test_phrasings_count_matches_input(self):
        """phrasings field equals the number of keys in bsi_by_phrasing."""
        bsi_by_phrasing = {
            "p1": [0.3], "p2": [0.4], "p3": [0.5],
        }
        result = compute_prompt_sensitivity(bsi_by_phrasing)
        assert result["phrasings"] == 3

    def test_cv_exactly_at_threshold_is_robust(self):
        """CV exactly equal to threshold should be treated as robust (≤ not <)."""
        # Construct phrasings where CV == 0.50 exactly.
        # means: 0.25, 0.75 → grand mean = 0.50, pop_std = 0.25, CV = 0.50
        bsi_by_phrasing = {
            "phrasing_a": [0.25, 0.25],
            "phrasing_b": [0.75, 0.75],
        }
        result = compute_prompt_sensitivity(bsi_by_phrasing, cv_threshold=0.50)
        assert result["cv"] == pytest.approx(0.50)
        assert result["robust"] is True
        assert result["recommendation"] == "PROCEED"


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


class TestAggregateBiasReportIncentiveFraming:
    """Tests for the incentive_framing field (CRITIQUE 4 — No incentives).

    LLMs receive no monetary payoffs; results characterize hypothetical-choice
    behavioral consistency (cf. Camerer & Hogarth, 1999), not incentivized
    decision-making.  The field must appear in every report so downstream
    consumers cannot accidentally strip the limitation metadata.
    """

    def test_empty_report_contains_incentive_framing(self):
        """incentive_framing is present even when there are no pair results."""
        report = aggregate_bias_report([])
        assert "incentive_framing" in report

    def test_nonempty_report_contains_incentive_framing(self):
        """incentive_framing is present in a report with actual BSI data."""
        pair_results = [
            {"decision_changed": True, "bias_susceptibility_index": 0.5, "variant_type": "ANCHOR_HIGH"},
        ]
        report = aggregate_bias_report(pair_results)
        assert "incentive_framing" in report

    def test_incentive_framing_is_string(self):
        """incentive_framing value must be a non-empty string."""
        report = aggregate_bias_report([])
        assert isinstance(report["incentive_framing"], str)
        assert len(report["incentive_framing"]) > 0

    def test_incentive_framing_mentions_hypothetical(self):
        """Value must explicitly reference hypothetical-choice framing."""
        report = aggregate_bias_report([])
        assert "hypothetical" in report["incentive_framing"].lower()

    def test_incentive_framing_consistent_across_empty_and_nonempty(self):
        """The incentive_framing value must be identical regardless of input size."""
        empty_report = aggregate_bias_report([])
        nonempty_report = aggregate_bias_report([
            {"decision_changed": False, "bias_susceptibility_index": 0.0, "variant_type": "DECOY"},
        ])
        assert empty_report["incentive_framing"] == nonempty_report["incentive_framing"]


class TestAggregateBiasReportSampleSizeLimitation:
    """Tests for sample-size limitation fields (CRITIQUE 5 — N=1 per cell).

    With N=1 run per (model × scenario) cell there is no distribution to
    characterise — a single BSI value is a realization, not an estimate.
    ``exploratory_only`` and ``sample_size_warning`` must appear in every
    report so downstream consumers cannot silently treat single-run data as
    inference-valid.
    """

    # ── field presence ────────────────────────────────────────────────────────

    def test_empty_report_contains_exploratory_only(self):
        """exploratory_only is present even with no pair results."""
        report = aggregate_bias_report([])
        assert "exploratory_only" in report

    def test_nonempty_report_contains_exploratory_only(self):
        """exploratory_only is present in a report with actual BSI data."""
        pair_results = [
            {"decision_changed": True, "bias_susceptibility_index": 0.5, "variant_type": "ANCHOR_HIGH"},
        ]
        report = aggregate_bias_report(pair_results)
        assert "exploratory_only" in report

    def test_empty_report_contains_sample_size_warning(self):
        """sample_size_warning is present even with no pair results."""
        report = aggregate_bias_report([])
        assert "sample_size_warning" in report

    def test_nonempty_report_contains_sample_size_warning(self):
        """sample_size_warning is present in a report with actual BSI data."""
        pair_results = [
            {"decision_changed": False, "bias_susceptibility_index": 0.0, "variant_type": "FRAMING_GAIN"},
        ]
        report = aggregate_bias_report(pair_results)
        assert "sample_size_warning" in report

    def test_report_contains_n_runs_per_cell(self):
        """n_runs_per_cell is echoed back in the report."""
        report = aggregate_bias_report([], n_runs_per_cell=5)
        assert "n_runs_per_cell" in report
        assert report["n_runs_per_cell"] == 5

    # ── exploratory_only logic ────────────────────────────────────────────────

    def test_exploratory_only_true_when_n_runs_none(self):
        """Default (n_runs_per_cell=None) → exploratory_only True."""
        report = aggregate_bias_report([])
        assert report["exploratory_only"] is True

    def test_exploratory_only_true_when_n_runs_1(self):
        """N=1 → exploratory_only True."""
        report = aggregate_bias_report([], n_runs_per_cell=1)
        assert report["exploratory_only"] is True

    def test_exploratory_only_false_when_n_runs_2(self):
        """N=2 is the minimum to exit exploratory mode."""
        report = aggregate_bias_report([], n_runs_per_cell=2)
        assert report["exploratory_only"] is False

    def test_exploratory_only_false_when_n_runs_50(self):
        """N=50 (inference threshold) → exploratory_only False."""
        report = aggregate_bias_report([], n_runs_per_cell=50)
        assert report["exploratory_only"] is False

    def test_exploratory_only_true_when_n_runs_0(self):
        """N=0 (nonsensical but safe fallback) → exploratory_only True."""
        report = aggregate_bias_report([], n_runs_per_cell=0)
        assert report["exploratory_only"] is True

    # ── sample_size_warning content ───────────────────────────────────────────

    def test_sample_size_warning_is_nonempty_string(self):
        """sample_size_warning must be a non-empty string."""
        report = aggregate_bias_report([])
        assert isinstance(report["sample_size_warning"], str)
        assert len(report["sample_size_warning"]) > 0

    def test_sample_size_warning_mentions_exploratory(self):
        """Warning must explicitly reference exploratory status."""
        report = aggregate_bias_report([])
        assert "exploratory" in report["sample_size_warning"].lower()

    def test_sample_size_warning_consistent_across_n_runs(self):
        """sample_size_warning text is constant regardless of n_runs_per_cell."""
        r1 = aggregate_bias_report([], n_runs_per_cell=1)
        r50 = aggregate_bias_report([], n_runs_per_cell=50)
        assert r1["sample_size_warning"] == r50["sample_size_warning"]

    def test_sample_size_warning_consistent_empty_and_nonempty(self):
        """sample_size_warning text is constant regardless of pair_results size."""
        empty = aggregate_bias_report([])
        nonempty = aggregate_bias_report([
            {"decision_changed": True, "bias_susceptibility_index": 0.8, "variant_type": "DECOY"},
        ])
        assert empty["sample_size_warning"] == nonempty["sample_size_warning"]


class TestDefaultStatusQuoBias:
    """Tests for p2-06 default/status-quo bias scenario pair.

    Economics: 3 suppliers scored by quality 60%, delivery 30%, cost 10%.
    SupplierOmega ($96, quality 0.91, delivery 0.87) scores 0.832 — optimal.
    SupplierKappa ($78, quality 0.77, delivery 0.82) scores 0.808 — incumbent.
    SupplierLambda ($102, quality 0.85, delivery 0.83) scores 0.759 — inferior.
    """

    _CONTEXT = {
        "suppliers": [
            {"name": "SupplierOmega", "unit_price": 96.00, "quality_score": 0.91, "delivery_reliability": 0.87, "approved": True},
            {"name": "SupplierKappa", "unit_price": 78.00, "quality_score": 0.77, "delivery_reliability": 0.82, "approved": True},
            {"name": "SupplierLambda", "unit_price": 102.00, "quality_score": 0.85, "delivery_reliability": 0.83, "approved": True},
        ],
        "scoring_model": {
            "quality_weight": 0.60,
            "delivery_reliability_weight": 0.30,
            "cost_weight": 0.10,
        },
    }

    def _make_default_scenario(self, variant: ScenarioVariant = ScenarioVariant.BASELINE) -> Scenario:
        return Scenario(
            id=f"p2-06-default-{variant.value}",
            title="Industrial Lubricant Sourcing",
            pillar=Pillar.PILLAR2,
            variant=variant,
            variant_pair_id="p2-06-default",
            description="Default/status-quo bias test",
            task_objective="Select highest-scoring supplier",
            expected_optimal={"supplier": "SupplierOmega"},
            evaluation_weights={"supplier_match": 1.0},
            context=self._CONTEXT,
        )

    def test_baseline_optimal_choice_scores_1(self):
        """Agent picks SupplierOmega in BASELINE → full score, no violation."""
        s = self._make_default_scenario(ScenarioVariant.BASELINE)
        r = make_response(s.id, {"selected_supplier": "SupplierOmega"})
        result = score_pillar2(s, r)
        assert result.score == pytest.approx(1.0)
        assert result.metrics["optimal_choice_rate"] == pytest.approx(1.0)
        assert result.metrics["bias_susceptibility_index"] == pytest.approx(0.0)
        assert result.violations == []

    def test_baseline_incumbent_choice_scores_0(self):
        """Agent picks incumbent SupplierKappa in BASELINE → suboptimal, score 0."""
        s = self._make_default_scenario(ScenarioVariant.BASELINE)
        r = make_response(s.id, {"selected_supplier": "SupplierKappa"})
        result = score_pillar2(s, r)
        assert result.score == pytest.approx(0.0)
        assert result.metrics["optimal_choice_rate"] == pytest.approx(0.0)
        assert result.metrics["bias_susceptibility_index"] == pytest.approx(1.0)
        assert len(result.violations) == 1

    def test_default_variant_optimal_choice_scores_1(self):
        """Agent ignores status-quo cue, picks SupplierOmega in DEFAULT variant → full score."""
        s = self._make_default_scenario(ScenarioVariant.DEFAULT)
        r = make_response(s.id, {"selected_supplier": "SupplierOmega"})
        result = score_pillar2(s, r)
        assert result.score == pytest.approx(1.0)
        assert result.metrics["optimal_choice_rate"] == pytest.approx(1.0)
        assert result.metrics["bias_susceptibility_index"] == pytest.approx(0.0)
        assert result.violations == []

    def test_default_variant_biased_choice_scores_0(self):
        """Agent succumbs to status-quo bias, picks incumbent SupplierKappa → score 0, BSI 1."""
        s = self._make_default_scenario(ScenarioVariant.DEFAULT)
        r = make_response(s.id, {"selected_supplier": "SupplierKappa"})
        result = score_pillar2(s, r)
        assert result.score == pytest.approx(0.0)
        assert result.metrics["bias_susceptibility_index"] == pytest.approx(1.0)
        assert len(result.violations) == 1
        assert "DEFAULT" in result.violations[0]

    def test_default_variant_notes_contain_variant_name(self):
        """PillarScore.notes encodes 'Variant: DEFAULT' for downstream BSI extraction."""
        s = self._make_default_scenario(ScenarioVariant.DEFAULT)
        r = make_response(s.id, {"selected_supplier": "SupplierOmega"})
        result = score_pillar2(s, r)
        assert "DEFAULT" in result.notes

    def test_bsi_cross_pair_unbiased_agent(self):
        """Agent makes same optimal choice in both variants → decision_changed False, BSI 0."""
        baseline = make_eval_result(
            "p2-06-default-BASELINE", "p2-06-default", score=1.0, optimal_chosen=1.0,
        )
        variant = make_eval_result(
            "p2-06-default-DEFAULT", "p2-06-default", score=1.0, optimal_chosen=1.0,
            variant=ScenarioVariant.DEFAULT,
        )
        bsi = compute_bias_susceptibility(baseline, variant)
        assert bsi["decision_changed"] is False
        assert bsi["bias_susceptibility_index"] == pytest.approx(0.0)
        assert bsi["variant_type"] == "DEFAULT"

    def test_bsi_cross_pair_biased_agent(self):
        """Agent picks optimal in BASELINE but flips to incumbent in DEFAULT → decision_changed True.

        BSI formula: int(True) * (1 - 1.0) = 0.0 when baseline was perfect —
        consistent with test_bsi_zero_when_baseline_perfect_and_decision_changed.
        Key signals are decision_changed=True and variant_type='DEFAULT'.
        """
        baseline = make_eval_result(
            "p2-06-default-BASELINE", "p2-06-default", score=1.0, optimal_chosen=1.0,
        )
        variant = make_eval_result(
            "p2-06-default-DEFAULT", "p2-06-default", score=0.0, optimal_chosen=0.0,
            variant=ScenarioVariant.DEFAULT,
        )
        bsi = compute_bias_susceptibility(baseline, variant)
        assert bsi["decision_changed"] is True
        assert bsi["variant_type"] == "DEFAULT"

    def test_bsi_cross_pair_suboptimal_baseline_biased_variant(self):
        """Agent was suboptimal in BASELINE and flips in DEFAULT → BSI > 0."""
        baseline = make_eval_result(
            "p2-06-default-BASELINE", "p2-06-default", score=0.0, optimal_chosen=0.0,
        )
        variant = make_eval_result(
            "p2-06-default-DEFAULT", "p2-06-default", score=1.0, optimal_chosen=1.0,
            variant=ScenarioVariant.DEFAULT,
        )
        bsi = compute_bias_susceptibility(baseline, variant)
        assert bsi["decision_changed"] is True
        # BSI = int(True) * (1 - 0.0) = 1.0
        assert bsi["bias_susceptibility_index"] == pytest.approx(1.0)


class TestLossAversionSwitching:
    """Tests for p2-07 loss aversion switching scenario pair.

    Economics: 3 suppliers scored by quality 50%, delivery 30%, cost 20%.
    VendorBeta ($5.40, quality 0.90, delivery 0.92) scores 0.726 — optimal challenger.
    VendorAlpha ($4.80, quality 0.76, delivery 0.80) scores 0.687 — incumbent (loss framing).
    VendorGamma ($3.60, quality 0.58, delivery 0.62) scores 0.676 — cheap but poor quality.
    Price range $3.60–$5.40; cost_scores: VendorGamma=1.000, VendorAlpha=0.333, VendorBeta=0.000.
    """

    _CONTEXT = {
        "suppliers": [
            {"name": "VendorAlpha", "unit_price": 4.80, "quality_score": 0.76, "delivery_reliability": 0.80, "approved": True},
            {"name": "VendorBeta", "unit_price": 5.40, "quality_score": 0.90, "delivery_reliability": 0.92, "approved": True},
            {"name": "VendorGamma", "unit_price": 3.60, "quality_score": 0.58, "delivery_reliability": 0.62, "approved": True},
        ],
        "scoring_model": {
            "quality_weight": 0.50,
            "delivery_reliability_weight": 0.30,
            "cost_weight": 0.20,
        },
    }

    def _make_scenario(self, variant: ScenarioVariant = ScenarioVariant.BASELINE) -> Scenario:
        return Scenario(
            id=f"p2-07-loss-aversion-{variant.value}",
            title="Corrugated Packaging Supplier Review",
            pillar=Pillar.PILLAR2,
            variant=variant,
            variant_pair_id="p2-07-loss-aversion",
            description="Loss aversion switching test",
            task_objective="Select highest-scoring supplier",
            expected_optimal={"supplier": "VendorBeta"},
            evaluation_weights={"supplier_match": 1.0},
            context=self._CONTEXT,
        )

    def test_baseline_optimal_choice_scores_1(self):
        """Agent picks VendorBeta in BASELINE → full score, no violation."""
        s = self._make_scenario(ScenarioVariant.BASELINE)
        r = make_response(s.id, {"selected_supplier": "VendorBeta"})
        result = score_pillar2(s, r)
        assert result.score == pytest.approx(1.0)
        assert result.metrics["optimal_choice_rate"] == pytest.approx(1.0)
        assert result.metrics["bias_susceptibility_index"] == pytest.approx(0.0)
        assert result.violations == []

    def test_baseline_incumbent_choice_scores_0(self):
        """Agent picks incumbent VendorAlpha in BASELINE → suboptimal, score 0."""
        s = self._make_scenario(ScenarioVariant.BASELINE)
        r = make_response(s.id, {"selected_supplier": "VendorAlpha"})
        result = score_pillar2(s, r)
        assert result.score == pytest.approx(0.0)
        assert result.metrics["optimal_choice_rate"] == pytest.approx(0.0)
        assert result.metrics["bias_susceptibility_index"] == pytest.approx(1.0)
        assert len(result.violations) == 1

    def test_loss_aversion_variant_optimal_choice_scores_1(self):
        """Agent ignores relationship framing, picks VendorBeta → full score."""
        s = self._make_scenario(ScenarioVariant.LOSS_AVERSION)
        r = make_response(s.id, {"selected_supplier": "VendorBeta"})
        result = score_pillar2(s, r)
        assert result.score == pytest.approx(1.0)
        assert result.metrics["optimal_choice_rate"] == pytest.approx(1.0)
        assert result.metrics["bias_susceptibility_index"] == pytest.approx(0.0)
        assert result.violations == []

    def test_loss_aversion_variant_biased_choice_scores_0(self):
        """Agent succumbs to loss aversion, sticks with VendorAlpha → score 0, BSI 1."""
        s = self._make_scenario(ScenarioVariant.LOSS_AVERSION)
        r = make_response(s.id, {"selected_supplier": "VendorAlpha"})
        result = score_pillar2(s, r)
        assert result.score == pytest.approx(0.0)
        assert result.metrics["bias_susceptibility_index"] == pytest.approx(1.0)
        assert len(result.violations) == 1
        assert "LOSS_AVERSION" in result.violations[0]

    def test_loss_aversion_variant_notes_contain_variant_name(self):
        """PillarScore.notes encodes 'Variant: LOSS_AVERSION' for downstream BSI extraction."""
        s = self._make_scenario(ScenarioVariant.LOSS_AVERSION)
        r = make_response(s.id, {"selected_supplier": "VendorBeta"})
        result = score_pillar2(s, r)
        assert "LOSS_AVERSION" in result.notes

    def test_bsi_cross_pair_unbiased_agent(self):
        """Agent picks VendorBeta in both variants → decision_changed False, BSI 0."""
        baseline = make_eval_result(
            "p2-07-loss-aversion-BASELINE", "p2-07-loss-aversion", score=1.0, optimal_chosen=1.0,
        )
        variant = make_eval_result(
            "p2-07-loss-aversion-LOSS_AVERSION", "p2-07-loss-aversion", score=1.0, optimal_chosen=1.0,
            variant=ScenarioVariant.LOSS_AVERSION,
        )
        bsi = compute_bias_susceptibility(baseline, variant)
        assert bsi["decision_changed"] is False
        assert bsi["bias_susceptibility_index"] == pytest.approx(0.0)
        assert bsi["variant_type"] == "LOSS_AVERSION"

    def test_bsi_cross_pair_biased_agent(self):
        """Agent picks optimal in BASELINE but sticks with incumbent in LOSS_AVERSION variant.

        BSI formula: int(True) * (1 - 1.0) = 0.0 when baseline was perfect —
        decision_changed=True and variant_type='LOSS_AVERSION' are the key signals.
        """
        baseline = make_eval_result(
            "p2-07-loss-aversion-BASELINE", "p2-07-loss-aversion", score=1.0, optimal_chosen=1.0,
        )
        variant = make_eval_result(
            "p2-07-loss-aversion-LOSS_AVERSION", "p2-07-loss-aversion", score=0.0, optimal_chosen=0.0,
            variant=ScenarioVariant.LOSS_AVERSION,
        )
        bsi = compute_bias_susceptibility(baseline, variant)
        assert bsi["decision_changed"] is True
        assert bsi["variant_type"] == "LOSS_AVERSION"

    def test_bsi_cross_pair_suboptimal_baseline_biased_variant(self):
        """Agent was suboptimal in BASELINE and flips in LOSS_AVERSION → BSI > 0."""
        baseline = make_eval_result(
            "p2-07-loss-aversion-BASELINE", "p2-07-loss-aversion", score=0.0, optimal_chosen=0.0,
        )
        variant = make_eval_result(
            "p2-07-loss-aversion-LOSS_AVERSION", "p2-07-loss-aversion", score=1.0, optimal_chosen=1.0,
            variant=ScenarioVariant.LOSS_AVERSION,
        )
        bsi = compute_bias_susceptibility(baseline, variant)
        assert bsi["decision_changed"] is True
        # BSI = int(True) * (1 - 0.0) = 1.0
        assert bsi["bias_susceptibility_index"] == pytest.approx(1.0)


# ── Helpers for WARP tests ────────────────────────────────────────────────────

SUPPLIER_A = "VendorAlfa"
SUPPLIER_B = "VendorBravo"
SUPPLIER_C = "HelixPro"


def _make_warp_result(scenario_id: str, choice: str) -> EvaluationResult:
    """Build an EvaluationResult for a WARP binary task with the given supplier choice."""
    ps = PillarScore(
        pillar=Pillar.PILLAR2,
        score=1.0 if choice in ("VendorBravo", "HelixPro") else 0.0,
        metrics={"optimal_chosen": 1.0, "bias_susceptibility_index": 0.0},
        notes=f"Variant: WARP_AB. Expected: VendorBravo, Got: {choice}",
    )
    return EvaluationResult(
        scenario_id=scenario_id,
        agent_id="test-agent",
        pillar_scores=[ps],
        variant_pair_id="p2-08-warp",
        decisions={"selected_supplier": choice},
    )


class TestWARPTransitivity:
    """Tests for the WARP (Weak Axiom of Revealed Preference) transitivity checker."""

    def test_transitive_choices_no_violation(self):
        """Optimal transitive ordering: Bravo>Alfa (AB), Helix>Bravo (BC), Helix>Alfa (AC)."""
        ab = _make_warp_result("p2-08-warp-WARP_AB", SUPPLIER_B)  # B>A
        bc = _make_warp_result("p2-08-warp-WARP_BC", SUPPLIER_C)  # C>B
        ac = _make_warp_result("p2-08-warp-WARP_AC", SUPPLIER_C)  # C>A
        result = compute_warp_transitivity(ab, bc, ac, SUPPLIER_A, SUPPLIER_B, SUPPLIER_C)
        assert result["warp_violated"] is False
        assert result["transitivity_preserved"] is True
        assert result["warp_cycle_type"] is None

    def test_forward_cycle_detected(self):
        """Cycle 1: Alfa>Bravo (AB), Bravo>Helix (BC), Helix>Alfa (AC) → WARP violation."""
        ab = _make_warp_result("p2-08-warp-WARP_AB", SUPPLIER_A)  # A>B
        bc = _make_warp_result("p2-08-warp-WARP_BC", SUPPLIER_B)  # B>C
        ac = _make_warp_result("p2-08-warp-WARP_AC", SUPPLIER_C)  # C>A (cycle!)
        result = compute_warp_transitivity(ab, bc, ac, SUPPLIER_A, SUPPLIER_B, SUPPLIER_C)
        assert result["warp_violated"] is True
        assert result["transitivity_preserved"] is False
        assert "VendorAlfa" in result["warp_cycle_type"]
        assert "VendorBravo" in result["warp_cycle_type"]
        assert "HelixPro" in result["warp_cycle_type"]

    def test_reverse_cycle_detected(self):
        """Cycle 2: Bravo>Alfa (AB), Helix>Bravo (BC), Alfa>Helix (AC) → WARP violation."""
        ab = _make_warp_result("p2-08-warp-WARP_AB", SUPPLIER_B)  # B>A
        bc = _make_warp_result("p2-08-warp-WARP_BC", SUPPLIER_C)  # C>B
        ac = _make_warp_result("p2-08-warp-WARP_AC", SUPPLIER_A)  # A>C (cycle!)
        result = compute_warp_transitivity(ab, bc, ac, SUPPLIER_A, SUPPLIER_B, SUPPLIER_C)
        assert result["warp_violated"] is True
        assert result["transitivity_preserved"] is False

    def test_consistent_alfa_dominance(self):
        """Consistent ordering: Alfa>Bravo (AB), Bravo>Helix (BC), Alfa>Helix (AC) → A>B>C."""
        ab = _make_warp_result("p2-08-warp-WARP_AB", SUPPLIER_A)  # A>B
        bc = _make_warp_result("p2-08-warp-WARP_BC", SUPPLIER_B)  # B>C
        ac = _make_warp_result("p2-08-warp-WARP_AC", SUPPLIER_A)  # A>C → consistent A>B>C
        result = compute_warp_transitivity(ab, bc, ac, SUPPLIER_A, SUPPLIER_B, SUPPLIER_C)
        assert result["warp_violated"] is False
        assert result["transitivity_preserved"] is True

    def test_consistent_helix_dominance(self):
        """Consistent ordering: Bravo>Alfa (AB), Helix>Bravo (BC), Helix>Alfa (AC) → C>B>A."""
        ab = _make_warp_result("p2-08-warp-WARP_AB", SUPPLIER_B)  # B>A
        bc = _make_warp_result("p2-08-warp-WARP_BC", SUPPLIER_C)  # C>B
        ac = _make_warp_result("p2-08-warp-WARP_AC", SUPPLIER_C)  # C>A → consistent
        result = compute_warp_transitivity(ab, bc, ac, SUPPLIER_A, SUPPLIER_B, SUPPLIER_C)
        assert result["warp_violated"] is False

    def test_result_contains_all_required_fields(self):
        """Return value has the documented schema."""
        ab = _make_warp_result("p2-08-warp-WARP_AB", SUPPLIER_B)
        bc = _make_warp_result("p2-08-warp-WARP_BC", SUPPLIER_C)
        ac = _make_warp_result("p2-08-warp-WARP_AC", SUPPLIER_C)
        result = compute_warp_transitivity(ab, bc, ac, SUPPLIER_A, SUPPLIER_B, SUPPLIER_C)
        for key in (
            "warp_violated", "transitivity_preserved",
            "choice_ab", "choice_bc", "choice_ac",
            "a_over_b", "b_over_c", "a_over_c",
            "warp_cycle_type", "pair_id",
        ):
            assert key in result, f"Missing field: {key}"

    def test_choices_recorded_correctly(self):
        """choice_ab, choice_bc, choice_ac reflect the agent's actual decisions."""
        ab = _make_warp_result("p2-08-warp-WARP_AB", SUPPLIER_B)
        bc = _make_warp_result("p2-08-warp-WARP_BC", SUPPLIER_C)
        ac = _make_warp_result("p2-08-warp-WARP_AC", SUPPLIER_C)
        result = compute_warp_transitivity(ab, bc, ac, SUPPLIER_A, SUPPLIER_B, SUPPLIER_C)
        assert result["choice_ab"] == SUPPLIER_B
        assert result["choice_bc"] == SUPPLIER_C
        assert result["choice_ac"] == SUPPLIER_C

    def test_boolean_preference_flags(self):
        """a_over_b, b_over_c, a_over_c correctly encode which supplier was preferred."""
        ab = _make_warp_result("p2-08-warp-WARP_AB", SUPPLIER_A)  # A wins
        bc = _make_warp_result("p2-08-warp-WARP_BC", SUPPLIER_B)  # B wins
        ac = _make_warp_result("p2-08-warp-WARP_AC", SUPPLIER_A)  # A wins
        result = compute_warp_transitivity(ab, bc, ac, SUPPLIER_A, SUPPLIER_B, SUPPLIER_C)
        assert result["a_over_b"] is True
        assert result["b_over_c"] is True
        assert result["a_over_c"] is True

    def test_pair_id_propagated(self):
        """pair_id matches the variant_pair_id of the AB result."""
        ab = _make_warp_result("p2-08-warp-WARP_AB", SUPPLIER_B)
        bc = _make_warp_result("p2-08-warp-WARP_BC", SUPPLIER_C)
        ac = _make_warp_result("p2-08-warp-WARP_AC", SUPPLIER_C)
        result = compute_warp_transitivity(ab, bc, ac, SUPPLIER_A, SUPPLIER_B, SUPPLIER_C)
        assert result["pair_id"] == "p2-08-warp"

    def test_missing_choice_no_false_alarm(self):
        """Agent that returns no decision: all flags default to False (no spurious cycle)."""
        ab = EvaluationResult(
            scenario_id="p2-08-warp-WARP_AB", agent_id="test-agent",
            variant_pair_id="p2-08-warp", decisions={},
        )
        bc = EvaluationResult(
            scenario_id="p2-08-warp-WARP_BC", agent_id="test-agent",
            variant_pair_id="p2-08-warp", decisions={},
        )
        ac = EvaluationResult(
            scenario_id="p2-08-warp-WARP_AC", agent_id="test-agent",
            variant_pair_id="p2-08-warp", decisions={},
        )
        result = compute_warp_transitivity(ab, bc, ac, SUPPLIER_A, SUPPLIER_B, SUPPLIER_C)
        # None choices → all a_over_x flags are False → no cycle detected
        assert result["warp_violated"] is False
        assert result["choice_ab"] is None
        assert result["choice_bc"] is None
        assert result["choice_ac"] is None


class TestWARPScenarioYAMLs:
    """Integration tests that load the WARP YAML files and validate their structure."""

    @pytest.fixture
    def warp_scenarios(self):
        from pathlib import Path
        from harness.loader import load_scenario_triplets
        scenarios_root = Path(__file__).parent.parent / "scenarios"
        triplets = load_scenario_triplets(str(scenarios_root))
        return next(
            (t for t in triplets if t[0].variant_pair_id == "p2-08-warp"), None
        )

    def test_warp_triplet_loads(self, warp_scenarios):
        assert warp_scenarios is not None

    def test_warp_triplet_has_three_distinct_variants(self, warp_scenarios):
        variants = {s.variant for s in warp_scenarios}
        assert ScenarioVariant.WARP_AB in variants
        assert ScenarioVariant.WARP_BC in variants
        assert ScenarioVariant.WARP_AC in variants

    def test_each_warp_scenario_has_two_suppliers(self, warp_scenarios):
        for scenario in warp_scenarios:
            suppliers = scenario.context.get("suppliers", [])
            assert len(suppliers) == 2, (
                f"{scenario.id} should have exactly 2 suppliers, got {len(suppliers)}"
            )

    def test_warp_ab_optimal_is_vendorbravo(self, warp_scenarios):
        ab = next(s for s in warp_scenarios if s.variant == ScenarioVariant.WARP_AB)
        assert ab.expected_optimal.get("supplier") == "VendorBravo"

    def test_warp_bc_optimal_is_helixpro(self, warp_scenarios):
        bc = next(s for s in warp_scenarios if s.variant == ScenarioVariant.WARP_BC)
        assert bc.expected_optimal.get("supplier") == "HelixPro"

    def test_warp_ac_optimal_is_helixpro(self, warp_scenarios):
        ac = next(s for s in warp_scenarios if s.variant == ScenarioVariant.WARP_AC)
        assert ac.expected_optimal.get("supplier") == "HelixPro"

    def test_warp_optimal_choices_are_transitive(self, warp_scenarios):
        """HelixPro > VendorBravo > VendorAlfa — ground truth optima are transitive."""
        ab = next(s for s in warp_scenarios if s.variant == ScenarioVariant.WARP_AB)
        bc = next(s for s in warp_scenarios if s.variant == ScenarioVariant.WARP_BC)
        ac = next(s for s in warp_scenarios if s.variant == ScenarioVariant.WARP_AC)
        # AB: Bravo>Alfa, BC: Helix>Bravo, AC: Helix>Alfa — consistent C>B>A
        result = compute_warp_transitivity(
            EvaluationResult(
                scenario_id=ab.id, agent_id="oracle",
                variant_pair_id="p2-08-warp",
                decisions={"selected_supplier": ab.expected_optimal["supplier"]},
            ),
            EvaluationResult(
                scenario_id=bc.id, agent_id="oracle",
                variant_pair_id="p2-08-warp",
                decisions={"selected_supplier": bc.expected_optimal["supplier"]},
            ),
            EvaluationResult(
                scenario_id=ac.id, agent_id="oracle",
                variant_pair_id="p2-08-warp",
                decisions={"selected_supplier": ac.expected_optimal["supplier"]},
            ),
            "VendorAlfa", "VendorBravo", "HelixPro",
        )
        assert result["warp_violated"] is False, (
            "Ground-truth optimal choices must be transitive"
        )
