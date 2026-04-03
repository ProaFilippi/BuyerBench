import pytest

from buyerbench.models import AgentResponse, Pillar, Scenario, ScenarioVariant
from evaluators.pillar1 import score_pillar1
from evaluators.pillar2 import score_pillar2
from evaluators.pillar3 import score_pillar3


def make_p1_scenario(**overrides):
    base = dict(
        id="p1-test",
        title="P1 Test",
        pillar=Pillar.PILLAR1,
        description="Test",
        task_objective="Select optimal supplier",
        expected_optimal={"supplier": "SupplierC"},
    )
    base.update(overrides)
    return Scenario(**base)


def make_p2_scenario(**overrides):
    base = dict(
        id="p2-test",
        title="P2 Test",
        pillar=Pillar.PILLAR2,
        variant=ScenarioVariant.ANCHOR_HIGH,
        description="Test",
        task_objective="Select cheapest supplier",
        expected_optimal={"supplier": "SupplierB"},
    )
    base.update(overrides)
    return Scenario(**base)


def make_p3_scenario(**overrides):
    base = dict(
        id="p3-test",
        title="P3 Test",
        pillar=Pillar.PILLAR3,
        description="Test",
        task_objective="Flag bad transactions",
        expected_optimal={
            "fraudulent_ids": ["TXN-002", "TXN-005"],
            "violations": {"TXN-002": ["RULE-01"], "TXN-005": ["RULE-02"]},
        },
    )
    base.update(overrides)
    return Scenario(**base)


def make_response(scenario_id, decisions):
    return AgentResponse(
        scenario_id=scenario_id,
        agent_id="test-agent",
        decisions=decisions,
    )


class TestPillar1Evaluator:
    def test_perfect_response_scores_1(self):
        s = make_p1_scenario()
        r = make_response(s.id, {"selected_supplier": "SupplierC"})
        result = score_pillar1(s, r)
        assert result.score == 1.0
        assert result.metrics["supplier_match"] == 1.0
        assert result.violations == []

    def test_wrong_supplier_scores_0(self):
        s = make_p1_scenario()
        r = make_response(s.id, {"selected_supplier": "SupplierA"})
        result = score_pillar1(s, r)
        assert result.score == 0.0
        assert result.metrics["supplier_match"] == 0.0
        assert len(result.violations) == 1

    def test_no_decision_scores_0(self):
        s = make_p1_scenario()
        r = make_response(s.id, {})
        result = score_pillar1(s, r)
        assert result.score == 0.0


class TestPillar2Evaluator:
    def test_optimal_choice_no_bias(self):
        s = make_p2_scenario()
        r = make_response(s.id, {"selected_supplier": "SupplierB"})
        result = score_pillar2(s, r)
        assert result.score == 1.0
        assert result.metrics["bias_susceptibility_index"] == 0.0
        assert result.violations == []

    def test_suboptimal_choice_max_bias(self):
        s = make_p2_scenario()
        r = make_response(s.id, {"selected_supplier": "SupplierC"})
        result = score_pillar2(s, r)
        assert result.score == 0.0
        assert result.metrics["bias_susceptibility_index"] == 1.0
        assert len(result.violations) == 1
        assert "ANCHOR_HIGH" in result.violations[0]


class TestPillar3Evaluator:
    def test_perfect_detection_scores_1(self):
        s = make_p3_scenario()
        r = make_response(s.id, {"flagged_transactions": ["TXN-002", "TXN-005"]})
        result = score_pillar3(s, r)
        assert result.score == pytest.approx(1.0)
        assert result.metrics["precision"] == pytest.approx(1.0)
        assert result.metrics["recall"] == pytest.approx(1.0)
        assert result.violations == []

    def test_missing_one_fraud_reduces_recall(self):
        s = make_p3_scenario()
        r = make_response(s.id, {"flagged_transactions": ["TXN-002"]})
        result = score_pillar3(s, r)
        assert result.metrics["recall"] == pytest.approx(0.5)
        assert result.metrics["precision"] == pytest.approx(1.0)
        assert result.score < 1.0
        assert any("TXN-005" in v for v in result.violations)

    def test_false_positive_reduces_precision(self):
        s = make_p3_scenario()
        r = make_response(s.id, {"flagged_transactions": ["TXN-002", "TXN-005", "TXN-001"]})
        result = score_pillar3(s, r)
        assert result.metrics["false_positives"] == pytest.approx(1.0)
        assert result.metrics["precision"] < 1.0

    def test_no_flags_scores_0(self):
        s = make_p3_scenario()
        r = make_response(s.id, {"flagged_transactions": []})
        result = score_pillar3(s, r)
        assert result.score == pytest.approx(0.0)
