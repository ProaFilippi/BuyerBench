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
        # p3-07 (BACEN licensing gate) added: 35 + 1 = 36
        assert len(all_scenarios) == 36

    def test_pillar1_count(self, all_scenarios):
        p1 = [s for s in all_scenarios if s.pillar == Pillar.PILLAR1]
        assert len(p1) == 6

    def test_pillar2_count(self, all_scenarios):
        p2 = [s for s in all_scenarios if s.pillar == Pillar.PILLAR2]
        # p2-12 multistep anchor pair added: 23 + 2 = 25
        assert len(p2) == 25

    def test_pillar3_count(self, all_scenarios):
        p3 = [s for s in all_scenarios if s.pillar == Pillar.PILLAR3]
        # p3-07 (BACEN licensing gate) added
        assert len(p3) == 7

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
        # REV-4 added 3 new hard pairs (p2-09, p2-10, p2-11): 7 + 3 = 10
        assert len(scenario_pairs) == 10

    def test_expected_pair_ids_present(self, scenario_pairs):
        pair_ids = {a.variant_pair_id for a, _ in scenario_pairs}
        expected = {
            "p2-01-anchoring",
            "p2-02-framing",
            "p2-03-decoy",
            "p2-04-scarcity",
            "p2-05-sunk-cost",
            "p2-06-default",
            "p2-07-loss-aversion",
            # REV-4 hard-difficulty pairs
            "p2-09-compound",
            "p2-10-anchor-hard",
            "p2-11-scarcity-hard",
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

    def test_default_pair_has_baseline_and_default(self, scenario_pairs):
        default = next(
            (a, b) for a, b in scenario_pairs if a.variant_pair_id == "p2-06-default"
        )
        variants = {default[0].variant, default[1].variant}
        assert ScenarioVariant.BASELINE in variants
        assert ScenarioVariant.DEFAULT in variants

    def test_compound_pair_has_baseline_and_compound(self, scenario_pairs):
        compound = next(
            (a, b) for a, b in scenario_pairs if a.variant_pair_id == "p2-09-compound"
        )
        variants = {compound[0].variant, compound[1].variant}
        assert ScenarioVariant.BASELINE in variants
        assert ScenarioVariant.COMPOUND in variants

    def test_hard_anchor_pair_has_baseline_and_anchor_high(self, scenario_pairs):
        hard_anchor = next(
            (a, b) for a, b in scenario_pairs if a.variant_pair_id == "p2-10-anchor-hard"
        )
        variants = {hard_anchor[0].variant, hard_anchor[1].variant}
        assert ScenarioVariant.BASELINE in variants
        assert ScenarioVariant.ANCHOR_HIGH in variants

    def test_hard_scarcity_pair_has_baseline_and_scarcity(self, scenario_pairs):
        hard_scarcity = next(
            (a, b) for a, b in scenario_pairs if a.variant_pair_id == "p2-11-scarcity-hard"
        )
        variants = {hard_scarcity[0].variant, hard_scarcity[1].variant}
        assert ScenarioVariant.BASELINE in variants
        assert ScenarioVariant.SCARCITY in variants


class TestRev4HardDifficultyScenarios:
    """Validate REV-4 hard-difficulty scenario properties."""

    REV4_IDS = {
        "p2-09-compound-BASELINE",
        "p2-09-compound-COMPOUND",
        "p2-10-anchor-hard-BASELINE",
        "p2-10-anchor-hard-ANCHOR_HIGH",
        "p2-11-scarcity-hard-BASELINE",
        "p2-11-scarcity-hard-SCARCITY",
    }

    def _rev4_scenarios(self, all_scenarios):
        return [s for s in all_scenarios if s.id in self.REV4_IDS]

    def test_all_six_rev4_scenarios_are_present(self, all_scenarios):
        found = {s.id for s in all_scenarios if s.id in self.REV4_IDS}
        assert found == self.REV4_IDS

    def test_all_rev4_scenarios_are_difficulty_hard(self, all_scenarios):
        for s in self._rev4_scenarios(all_scenarios):
            assert s.difficulty == Difficulty.HARD, (
                f"{s.id}: REV-4 scenario must have difficulty=hard"
            )

    def test_all_rev4_scenarios_tagged_rev4(self, all_scenarios):
        for s in self._rev4_scenarios(all_scenarios):
            assert "rev4" in s.tags, (
                f"{s.id}: REV-4 scenario must include 'rev4' tag"
            )

    def test_hard_scenarios_have_six_or_more_suppliers(self, all_scenarios):
        for s in self._rev4_scenarios(all_scenarios):
            suppliers = s.context.get("suppliers", [])
            assert len(suppliers) >= 6, (
                f"{s.id}: REV-4 scenario must have ≥6 suppliers, got {len(suppliers)}"
            )

    def test_compound_scenario_has_compound_variant(self, all_scenarios):
        compound = next(
            s for s in all_scenarios if s.id == "p2-09-compound-COMPOUND"
        )
        assert compound.variant == ScenarioVariant.COMPOUND

    def test_hard_anchor_variant_has_category_background(self, all_scenarios):
        anchor = next(
            s for s in all_scenarios if s.id == "p2-10-anchor-hard-ANCHOR_HIGH"
        )
        assert "category_background" in anchor.context, (
            "Hard anchor ANCHOR_HIGH must have category_background anchor context"
        )

    def test_compound_variant_has_category_background_and_vendor_note(self, all_scenarios):
        compound = next(
            s for s in all_scenarios if s.id == "p2-09-compound-COMPOUND"
        )
        assert "category_background" in compound.context
        suppliers = compound.context.get("suppliers", [])
        has_vendor_note = any("vendor_note" in sup for sup in suppliers)
        assert has_vendor_note, "Compound scenario must have a scarcity vendor_note on at least one supplier"

    def test_hard_scarcity_variant_has_vendor_note(self, all_scenarios):
        scarcity = next(
            s for s in all_scenarios if s.id == "p2-11-scarcity-hard-SCARCITY"
        )
        suppliers = scarcity.context.get("suppliers", [])
        has_vendor_note = any("vendor_note" in sup for sup in suppliers)
        assert has_vendor_note, "Hard scarcity SCARCITY must have a scarcity vendor_note"

    def test_hard_scenarios_delta_to_second_best_is_small(self, all_scenarios):
        """All REV-4 hard scenarios document delta_to_second_best < 0.05."""
        hard_baselines = [
            s for s in all_scenarios
            if s.id in {
                "p2-09-compound-BASELINE",
                "p2-10-anchor-hard-BASELINE",
                "p2-11-scarcity-hard-BASELINE",
            }
        ]
        assert len(hard_baselines) == 3
        for s in hard_baselines:
            delta = s.expected_optimal.get("delta_to_second_best")
            assert delta is not None, f"{s.id}: must document delta_to_second_best"
            assert delta < 0.05, (
                f"{s.id}: delta_to_second_best={delta} must be < 0.05 (REV-4 requirement)"
            )

    def test_baseline_and_compound_share_supplier_economics(self, all_scenarios):
        """p2-09 BASELINE and COMPOUND have identical supplier lists."""
        base = next(s for s in all_scenarios if s.id == "p2-09-compound-BASELINE")
        comp = next(s for s in all_scenarios if s.id == "p2-09-compound-COMPOUND")
        base_suppliers = {
            s["name"]: (s["unit_price"], s["quality_score"], s["delivery_reliability"])
            for s in base.context["suppliers"]
        }
        comp_suppliers = {
            s["name"]: (s["unit_price"], s["quality_score"], s["delivery_reliability"])
            for s in comp.context["suppliers"]
        }
        assert base_suppliers == comp_suppliers, (
            "BASELINE and COMPOUND must have identical supplier economics"
        )

    def test_baseline_and_hard_anchor_share_supplier_economics(self, all_scenarios):
        """p2-10 BASELINE and ANCHOR_HIGH have identical supplier economics."""
        base = next(s for s in all_scenarios if s.id == "p2-10-anchor-hard-BASELINE")
        anch = next(s for s in all_scenarios if s.id == "p2-10-anchor-hard-ANCHOR_HIGH")
        base_prices = {s["name"]: s["unit_price"] for s in base.context["suppliers"]}
        anch_prices = {s["name"]: s["unit_price"] for s in anch.context["suppliers"]}
        assert base_prices == anch_prices

    def test_baseline_and_hard_scarcity_share_supplier_economics(self, all_scenarios):
        """p2-11 BASELINE and SCARCITY have identical supplier economics."""
        base = next(s for s in all_scenarios if s.id == "p2-11-scarcity-hard-BASELINE")
        scar = next(s for s in all_scenarios if s.id == "p2-11-scarcity-hard-SCARCITY")
        base_prices = {s["name"]: s["unit_price"] for s in base.context["suppliers"]}
        scar_prices = {s["name"]: s["unit_price"] for s in scar.context["suppliers"]}
        assert base_prices == scar_prices


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
