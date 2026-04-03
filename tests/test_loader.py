from pathlib import Path

import pytest

from buyerbench.models import Pillar, Scenario
from harness.loader import load_all_scenarios, load_scenario


SCENARIOS_ROOT = Path(__file__).parent.parent / "scenarios"

SCENARIO_FILES = [
    SCENARIOS_ROOT / "pillar1" / "p1-supplier-selection-basic.yaml",
    SCENARIOS_ROOT / "pillar2" / "p2-anchoring-price-comparison.yaml",
    SCENARIOS_ROOT / "pillar3" / "p3-fraud-detection-basic.yaml",
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
    def test_loads_exactly_three_scenarios(self):
        scenarios = load_all_scenarios(str(SCENARIOS_ROOT))
        assert len(scenarios) == 3

    def test_all_pillars_represented(self):
        scenarios = load_all_scenarios(str(SCENARIOS_ROOT))
        pillars = {s.pillar for s in scenarios}
        assert Pillar.PILLAR1 in pillars
        assert Pillar.PILLAR2 in pillars
        assert Pillar.PILLAR3 in pillars
