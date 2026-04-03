"""Scenario-level validation tests for the full BuyerBench scenario suite.

Tests confirm that every scenario file:
  - Loads without validation errors
  - Contains required non-empty fields
  - Carries the new schema fields (tags, difficulty, evaluation_weights)
  - Satisfies pillar-specific invariants
  - Has Pillar 2 paired variants sharing the same variant_pair_id
"""
from pathlib import Path

import pytest

from buyerbench.models import Difficulty, Pillar, ScenarioVariant
from harness.loader import load_all_scenarios, load_scenario_pairs


SCENARIOS_ROOT = Path(__file__).parent.parent / "scenarios"

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def all_scenarios():
    return load_all_scenarios(str(SCENARIOS_ROOT))


@pytest.fixture(scope="module")
def scenario_pairs():
    return load_scenario_pairs(str(SCENARIOS_ROOT))


# ---------------------------------------------------------------------------
# Suite-wide tests
# ---------------------------------------------------------------------------


class TestSuiteCompleteness:
    def test_total_scenario_count(self, all_scenarios):
        assert len(all_scenarios) == 18

    def test_pillar1_count(self, all_scenarios):
        p1 = [s for s in all_scenarios if s.pillar == Pillar.PILLAR1]
        assert len(p1) == 5

    def test_pillar2_count(self, all_scenarios):
        p2 = [s for s in all_scenarios if s.pillar == Pillar.PILLAR2]
        assert len(p2) == 8

    def test_pillar3_count(self, all_scenarios):
        p3 = [s for s in all_scenarios if s.pillar == Pillar.PILLAR3]
        assert len(p3) == 5

    def test_ids_are_unique(self, all_scenarios):
        ids = [s.id for s in all_scenarios]
        assert len(ids) == len(set(ids)), "Duplicate scenario IDs detected"


class TestRequiredFields:
    @pytest.mark.parametrize(
        "scenario",
        load_all_scenarios(str(SCENARIOS_ROOT)),
        ids=lambda s: s.id,
    )
    def test_id_non_empty(self, scenario):
        assert scenario.id, f"{scenario.id}: id must be non-empty"

    @pytest.mark.parametrize(
        "scenario",
        load_all_scenarios(str(SCENARIOS_ROOT)),
        ids=lambda s: s.id,
    )
    def test_title_non_empty(self, scenario):
        assert scenario.title, f"{scenario.id}: title must be non-empty"

    @pytest.mark.parametrize(
        "scenario",
        load_all_scenarios(str(SCENARIOS_ROOT)),
        ids=lambda s: s.id,
    )
    def test_task_objective_non_empty(self, scenario):
        assert scenario.task_objective, f"{scenario.id}: task_objective must be non-empty"

    @pytest.mark.parametrize(
        "scenario",
        load_all_scenarios(str(SCENARIOS_ROOT)),
        ids=lambda s: s.id,
    )
    def test_expected_optimal_non_empty(self, scenario):
        assert scenario.expected_optimal, (
            f"{scenario.id}: expected_optimal must be non-empty"
        )


class TestNewSchemaFields:
    @pytest.mark.parametrize(
        "scenario",
        load_all_scenarios(str(SCENARIOS_ROOT)),
        ids=lambda s: s.id,
    )
    def test_tags_present_and_non_empty(self, scenario):
        assert isinstance(scenario.tags, list), f"{scenario.id}: tags must be a list"
        assert len(scenario.tags) > 0, f"{scenario.id}: tags must not be empty"

    @pytest.mark.parametrize(
        "scenario",
        load_all_scenarios(str(SCENARIOS_ROOT)),
        ids=lambda s: s.id,
    )
    def test_difficulty_is_valid(self, scenario):
        assert scenario.difficulty in Difficulty, (
            f"{scenario.id}: difficulty must be a valid Difficulty enum value"
        )

    @pytest.mark.parametrize(
        "scenario",
        load_all_scenarios(str(SCENARIOS_ROOT)),
        ids=lambda s: s.id,
    )
    def test_evaluation_weights_are_floats(self, scenario):
        for key, val in scenario.evaluation_weights.items():
            assert isinstance(val, (int, float)), (
                f"{scenario.id}: evaluation_weights[{key}] must be numeric"
            )
            assert 0.0 <= val <= 1.0, (
                f"{scenario.id}: evaluation_weights[{key}]={val} must be in [0, 1]"
            )


class TestPillar2PairedVariants:
    def test_four_variant_pairs_exist(self, scenario_pairs):
        assert len(scenario_pairs) == 4

    def test_expected_pair_ids_present(self, scenario_pairs):
        pair_ids = {a.variant_pair_id for a, _ in scenario_pairs}
        expected = {
            "p2-01-anchoring",
            "p2-02-framing",
            "p2-03-decoy",
            "p2-04-scarcity",
        }
        assert pair_ids == expected

    def test_each_pair_has_two_distinct_variants(self, scenario_pairs):
        for a, b in scenario_pairs:
            assert a.variant != b.variant, (
                f"Pair {a.variant_pair_id}: both scenarios have the same variant"
            )

    def test_pillar2_scenarios_all_have_variant_pair_id(self, all_scenarios):
        p2 = [s for s in all_scenarios if s.pillar == Pillar.PILLAR2]
        for s in p2:
            assert s.variant_pair_id is not None, (
                f"{s.id}: Pillar 2 scenario is missing variant_pair_id"
            )

    def test_anchoring_pair_has_baseline_and_anchor_high(self, scenario_pairs):
        anchoring = next(
            (a, b) for a, b in scenario_pairs if a.variant_pair_id == "p2-01-anchoring"
        )
        variants = {anchoring[0].variant, anchoring[1].variant}
        assert ScenarioVariant.BASELINE in variants
        assert ScenarioVariant.ANCHOR_HIGH in variants

    def test_framing_pair_has_gain_and_loss(self, scenario_pairs):
        framing = next(
            (a, b) for a, b in scenario_pairs if a.variant_pair_id == "p2-02-framing"
        )
        variants = {framing[0].variant, framing[1].variant}
        assert ScenarioVariant.FRAMING_GAIN in variants
        assert ScenarioVariant.FRAMING_LOSS in variants

    def test_decoy_pair_has_baseline_and_decoy(self, scenario_pairs):
        decoy = next(
            (a, b) for a, b in scenario_pairs if a.variant_pair_id == "p2-03-decoy"
        )
        variants = {decoy[0].variant, decoy[1].variant}
        assert ScenarioVariant.BASELINE in variants
        assert ScenarioVariant.DECOY in variants

    def test_scarcity_pair_has_baseline_and_scarcity(self, scenario_pairs):
        scarcity = next(
            (a, b) for a, b in scenario_pairs if a.variant_pair_id == "p2-04-scarcity"
        )
        variants = {scarcity[0].variant, scarcity[1].variant}
        assert ScenarioVariant.BASELINE in variants
        assert ScenarioVariant.SCARCITY in variants


class TestPillar1Specifics:
    def test_all_p1_scenarios_have_context_suppliers_or_steps(self, all_scenarios):
        p1 = [s for s in all_scenarios if s.pillar == Pillar.PILLAR1]
        for s in p1:
            has_suppliers = "suppliers" in s.context or "supplier_catalog" in s.context
            has_quotes = "quotes" in s.context
            has_contracts = "contract_options" in s.context
            assert has_suppliers or has_quotes or has_contracts, (
                f"{s.id}: Pillar 1 scenario must have supplier/quote context"
            )

    def test_p1_scenarios_have_no_variant_pair_id(self, all_scenarios):
        p1 = [s for s in all_scenarios if s.pillar == Pillar.PILLAR1]
        for s in p1:
            assert s.variant_pair_id is None, (
                f"{s.id}: Pillar 1 scenario should not have a variant_pair_id"
            )


class TestPillar3Specifics:
    def test_all_p3_scenarios_have_security_requirements(self, all_scenarios):
        p3 = [s for s in all_scenarios if s.pillar == Pillar.PILLAR3]
        for s in p3:
            assert len(s.security_requirements) > 0, (
                f"{s.id}: Pillar 3 scenario must have security_requirements"
            )

    def test_p3_scenarios_have_no_variant_pair_id(self, all_scenarios):
        p3 = [s for s in all_scenarios if s.pillar == Pillar.PILLAR3]
        for s in p3:
            assert s.variant_pair_id is None, (
                f"{s.id}: Pillar 3 scenario should not have a variant_pair_id"
            )
