from pathlib import Path

import pytest

from buyerbench.models import Pillar, Scenario
from harness.loader import load_all_scenarios, load_scenario, load_scenario_pairs, load_scenario_triplets


SCENARIOS_ROOT = Path(__file__).parent.parent / "scenarios"

SCENARIO_FILES = [
    SCENARIOS_ROOT / "pillar1" / "p1-01-supplier-selection-basic.yaml",
    SCENARIOS_ROOT / "pillar2" / "p2-01-anchor-high-BASELINE.yaml",
    SCENARIOS_ROOT / "pillar3" / "p3-01-fraud-detection-basic.yaml",
]


class TestLoadScenario:
    @pytest.mark.parametrize("path", SCENARIO_FILES)
    def test_each_scenario_loads(self, path):
        s = load_scenario(str(path))
        assert isinstance(s, Scenario)
        assert s.id
        assert s.title
        assert s.task_objective

    def test_p1_scenario_fields(self):
        s = load_scenario(str(SCENARIO_FILES[0]))
        assert s.pillar == Pillar.PILLAR1
        assert s.expected_optimal.get("supplier") == "SupplierC"
        assert "suppliers" in s.context

    def test_p2_scenario_fields(self):
        s = load_scenario(str(SCENARIO_FILES[1]))
        assert s.pillar == Pillar.PILLAR2
        assert s.expected_optimal.get("supplier") == "SupplierB"

    def test_p3_scenario_fields(self):
        s = load_scenario(str(SCENARIO_FILES[2]))
        assert s.pillar == Pillar.PILLAR3
        assert "TXN-002" in s.expected_optimal.get("fraudulent_ids", [])
        assert len(s.security_requirements) > 0


class TestLoadAllScenarios:
    def test_loads_exactly_eighteen_scenarios(self):
        # p3-07 (BACEN licensing gate) added: 35 + 1 = 36
        scenarios = load_all_scenarios(str(SCENARIOS_ROOT))
        assert len(scenarios) == 36

    def test_all_pillars_represented(self):
        scenarios = load_all_scenarios(str(SCENARIOS_ROOT))
        pillars = {s.pillar for s in scenarios}
        assert Pillar.PILLAR1 in pillars
        assert Pillar.PILLAR2 in pillars
        assert Pillar.PILLAR3 in pillars


class TestLoadScenarioPairs:
    def test_returns_four_pairs(self):
        # p2-12 multistep anchor pair added: 10 + 1 = 11
        pairs = load_scenario_pairs(str(SCENARIOS_ROOT))
        assert len(pairs) == 11

    def test_each_pair_is_two_scenarios(self):
        pairs = load_scenario_pairs(str(SCENARIOS_ROOT))
        for pair in pairs:
            assert len(pair) == 2
            assert isinstance(pair[0], Scenario)
            assert isinstance(pair[1], Scenario)

    def test_pair_members_share_variant_pair_id(self):
        pairs = load_scenario_pairs(str(SCENARIOS_ROOT))
        for a, b in pairs:
            assert a.variant_pair_id == b.variant_pair_id
            assert a.variant_pair_id is not None

    def test_pair_members_have_different_variants(self):
        pairs = load_scenario_pairs(str(SCENARIOS_ROOT))
        for a, b in pairs:
            assert a.variant != b.variant


class TestLoadScenarioTriplets:
    def test_returns_one_triplet(self):
        triplets = load_scenario_triplets(str(SCENARIOS_ROOT))
        assert len(triplets) == 1

    def test_each_triplet_is_three_scenarios(self):
        triplets = load_scenario_triplets(str(SCENARIOS_ROOT))
        for triplet in triplets:
            assert len(triplet) == 3
            assert all(isinstance(s, Scenario) for s in triplet)

    def test_triplet_members_share_variant_pair_id(self):
        triplets = load_scenario_triplets(str(SCENARIOS_ROOT))
        for a, b, c in triplets:
            assert a.variant_pair_id == b.variant_pair_id == c.variant_pair_id
            assert a.variant_pair_id is not None

    def test_triplet_members_have_distinct_variants(self):
        triplets = load_scenario_triplets(str(SCENARIOS_ROOT))
        for a, b, c in triplets:
            assert a.variant != b.variant
            assert b.variant != c.variant
            assert a.variant != c.variant

    def test_warp_triplet_sorted_alphabetically(self):
        triplets = load_scenario_triplets(str(SCENARIOS_ROOT))
        warp_triplet = next(
            (t for t in triplets if t[0].variant_pair_id == "p2-08-warp"), None
        )
        assert warp_triplet is not None
        variants = [s.variant.value for s in warp_triplet]
        assert variants == sorted(variants)  # WARP_AB, WARP_AC, WARP_BC alphabetically
