import pytest
from pydantic import ValidationError

from buyerbench.models import (
    AgentResponse,
    EvaluationResult,
    Pillar,
    PillarScore,
    Scenario,
    ScenarioVariant,
)


def make_scenario(**overrides):
    base = dict(
        id="test-001",
        title="Test Scenario",
        pillar=Pillar.PILLAR1,
        variant=ScenarioVariant.BASELINE,
        description="A test scenario",
        task_objective="Do something optimal",
        expected_optimal={"supplier": "SupplierA"},
    )
    base.update(overrides)
    return base


class TestScenario:
    def test_valid_instantiation(self):
        s = Scenario(**make_scenario())
        assert s.id == "test-001"
        assert s.pillar == Pillar.PILLAR1
        assert s.variant == ScenarioVariant.BASELINE
        assert s.expected_optimal == {"supplier": "SupplierA"}
        assert s.constraints == []
        assert s.security_requirements == []

    def test_defaults(self):
        s = Scenario(**make_scenario())
        assert isinstance(s.context, dict)
        assert s.context == {}

    def test_invalid_pillar(self):
        with pytest.raises(ValidationError):
            Scenario(**make_scenario(pillar="INVALID_PILLAR"))

    def test_invalid_variant(self):
        with pytest.raises(ValidationError):
            Scenario(**make_scenario(variant="NOT_A_VARIANT"))

    def test_missing_required_field(self):
        data = make_scenario()
        del data["id"]
        with pytest.raises(ValidationError):
            Scenario(**data)


class TestAgentResponse:
    def test_valid_instantiation(self):
        r = AgentResponse(
            scenario_id="test-001",
            agent_id="mock-agent",
            decisions={"selected_supplier": "SupplierA"},
            reasoning_trace="I chose A because it was cheapest.",
        )
        assert r.scenario_id == "test-001"
        assert r.decisions["selected_supplier"] == "SupplierA"
        assert r.latency_ms == 0.0

    def test_defaults(self):
        r = AgentResponse(scenario_id="s", agent_id="a")
        assert r.decisions == {}
        assert r.tool_calls == []
        assert r.raw_output == ""

    def test_missing_required_fields(self):
        with pytest.raises(ValidationError):
            AgentResponse(scenario_id="s")  # missing agent_id


class TestPillarScore:
    def test_score_bounds(self):
        with pytest.raises(ValidationError):
            PillarScore(pillar=Pillar.PILLAR1, score=1.5)
        with pytest.raises(ValidationError):
            PillarScore(pillar=Pillar.PILLAR1, score=-0.1)

    def test_valid(self):
        ps = PillarScore(pillar=Pillar.PILLAR2, score=0.75, metrics={"bias": 0.25})
        assert ps.score == 0.75
