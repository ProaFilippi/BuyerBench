"""Tests for multi-step scenario support: WorkflowStep, run_multi_step_scenario,
compute_anchor_propagation_index, and YAML loading of p2-12 scenarios."""
from __future__ import annotations

from pathlib import Path

import pytest

from buyerbench.models import (
    EvaluationResult,
    Pillar,
    PillarScore,
    Scenario,
    ScenarioVariant,
    WorkflowStep,
)
from evaluators.pillar2 import BiasMetrics, compute_anchor_propagation_index
from harness.loader import load_scenario
from harness.runner import run_multi_step_scenario


SCENARIOS_DIR = Path(__file__).parent.parent / "scenarios" / "pillar2"


def _make_eval_result(
    scenario_id: str,
    steps_output: list[dict],
    selected_supplier: str,
    variant_pair_id: str = "p2-12-multistep-anchor",
) -> EvaluationResult:
    ps = PillarScore(pillar=Pillar.PILLAR2, score=1.0, metrics={"optimal_chosen": 1.0})
    return EvaluationResult(
        scenario_id=scenario_id,
        agent_id="test-agent",
        pillar_scores=[ps],
        variant_pair_id=variant_pair_id,
        decisions={
            "selected_supplier": selected_supplier,
            "steps_output": steps_output,
        },
    )


class TestWorkflowStep:
    def test_workflow_step_basic(self):
        step = WorkflowStep(
            step_id=1,
            name="Catalog Review",
            task_objective="Review suppliers.",
            context={"key": "value"},
            expected_output={"preliminary_rankings": ["A", "B"]},
        )
        assert step.step_id == 1
        assert step.name == "Catalog Review"
        assert step.expected_output == {"preliminary_rankings": ["A", "B"]}

    def test_workflow_step_defaults(self):
        step = WorkflowStep(step_id=2, name="Step 2", task_objective="Do something.")
        assert step.context == {}
        assert step.expected_output == {}

    def test_scenario_with_workflow(self):
        s = Scenario(
            id="test-ms",
            title="Test Multi-Step",
            pillar=Pillar.PILLAR2,
            variant=ScenarioVariant.BASELINE,
            description="A test multi-step scenario.",
            task_objective="Execute workflow.",
            workflow_type="sequential",
            workflow=[
                WorkflowStep(step_id=1, name="Step1", task_objective="Do step 1."),
                WorkflowStep(step_id=2, name="Step2", task_objective="Do step 2.",
                             expected_output={"selected_supplier": "SupplierA"}),
            ],
        )
        assert s.workflow is not None
        assert len(s.workflow) == 2
        assert s.workflow_type == "sequential"

    def test_single_step_scenario_workflow_none(self):
        s = Scenario(
            id="test-single",
            title="Single",
            pillar=Pillar.PILLAR2,
            variant=ScenarioVariant.BASELINE,
            description="Single-step.",
            task_objective="Do it.",
        )
        assert s.workflow is None
        assert s.workflow_type is None


class TestLoadMultiStepScenarios:
    def test_load_baseline(self):
        path = SCENARIOS_DIR / "p2-12-multistep-anchor-BASELINE.yaml"
        scenario = load_scenario(str(path))
        assert scenario.id == "p2-12-multistep-anchor-BASELINE"
        assert scenario.pillar == Pillar.PILLAR2
        assert scenario.variant == ScenarioVariant.BASELINE
        assert scenario.workflow_type == "sequential"
        assert scenario.workflow is not None
        assert len(scenario.workflow) == 3

    def test_load_anchor_high(self):
        path = SCENARIOS_DIR / "p2-12-multistep-anchor-ANCHOR_HIGH.yaml"
        scenario = load_scenario(str(path))
        assert scenario.id == "p2-12-multistep-anchor-ANCHOR_HIGH"
        assert scenario.variant == ScenarioVariant.ANCHOR_HIGH
        assert scenario.workflow is not None
        assert len(scenario.workflow) == 3

    def test_baseline_workflow_steps(self):
        path = SCENARIOS_DIR / "p2-12-multistep-anchor-BASELINE.yaml"
        scenario = load_scenario(str(path))
        steps = scenario.workflow
        assert steps[0].step_id == 1
        assert steps[0].name == "Initial Catalog Review"
        assert steps[1].step_id == 2
        assert steps[1].name == "RFQ Shortlisting"
        assert steps[1].expected_output["shortlist"] == ["SupplierD", "SupplierB", "SupplierF"]
        assert steps[2].step_id == 3
        assert steps[2].expected_output["selected_supplier"] == "SupplierD"

    def test_anchor_high_step1_has_category_background(self):
        path = SCENARIOS_DIR / "p2-12-multistep-anchor-ANCHOR_HIGH.yaml"
        scenario = load_scenario(str(path))
        step1_context = scenario.workflow[0].context
        assert "category_background" in step1_context
        assert "148" in step1_context["category_background"]

    def test_anchor_high_steps_2_3_no_anchor(self):
        path = SCENARIOS_DIR / "p2-12-multistep-anchor-ANCHOR_HIGH.yaml"
        scenario = load_scenario(str(path))
        step2_context = scenario.workflow[1].context
        step3_context = scenario.workflow[2].context
        assert "category_background" not in step2_context
        assert "category_background" not in step3_context

    def test_expected_optimal_supplier_d(self):
        for fname in ["p2-12-multistep-anchor-BASELINE.yaml", "p2-12-multistep-anchor-ANCHOR_HIGH.yaml"]:
            scenario = load_scenario(str(SCENARIOS_DIR / fname))
            assert scenario.expected_optimal["supplier"] == "SupplierD"


class TestRunMultiStepScenario:
    def _make_multi_step_scenario(self) -> Scenario:
        return Scenario(
            id="test-ms-run",
            title="Test Multi-Step Run",
            pillar=Pillar.PILLAR2,
            variant=ScenarioVariant.BASELINE,
            description="Multi-step test.",
            task_objective="Execute workflow.",
            expected_optimal={"supplier": "SupplierA", "selected_supplier": "SupplierA"},
            workflow_type="sequential",
            workflow=[
                WorkflowStep(
                    step_id=1,
                    name="Step 1",
                    task_objective="Review catalog.",
                    context={"step1_key": "val1"},
                    expected_output={"preliminary_rankings": ["SupplierA", "SupplierB"]},
                ),
                WorkflowStep(
                    step_id=2,
                    name="Step 2",
                    task_objective="Shortlist.",
                    context={"step2_key": "val2"},
                    expected_output={"shortlist": ["SupplierA", "SupplierB"]},
                ),
                WorkflowStep(
                    step_id=3,
                    name="Step 3",
                    task_objective="Select final.",
                    context={},
                    expected_output={"supplier": "SupplierA", "selected_supplier": "SupplierA"},
                ),
            ],
        )

    def test_mock_agent_multi_step(self):
        from agents.mock import MockAgent
        scenario = self._make_multi_step_scenario()
        agent = MockAgent()
        response = run_multi_step_scenario(scenario, agent)
        assert response.agent_id == "mock-agent-v1"
        assert response.scenario_id == "test-ms-run"
        assert "steps_output" in response.decisions
        assert len(response.decisions["steps_output"]) == 3

    def test_steps_output_captures_per_step(self):
        from agents.mock import MockAgent
        scenario = self._make_multi_step_scenario()
        agent = MockAgent()
        response = run_multi_step_scenario(scenario, agent)
        steps = response.decisions["steps_output"]
        assert "preliminary_rankings" in steps[0]
        assert "shortlist" in steps[1]
        assert "selected_supplier" in steps[2]

    def test_final_decision_from_last_step(self):
        from agents.mock import MockAgent
        scenario = self._make_multi_step_scenario()
        agent = MockAgent()
        response = run_multi_step_scenario(scenario, agent)
        assert response.decisions.get("selected_supplier") == "SupplierA"

    def test_prior_step_output_injected_as_context(self):
        """Verify that each step scenario receives previous_step_output in context."""
        contexts_seen: list[dict] = []

        class ContextCapturingAgent:
            agent_id = "context-capturer"

            def respond(self, scenario: Scenario):
                from buyerbench.models import AgentResponse
                contexts_seen.append(dict(scenario.context))
                return AgentResponse(
                    scenario_id=scenario.id,
                    agent_id=self.agent_id,
                    decisions=dict(scenario.expected_optimal),
                )

        from harness.runner import run_multi_step_scenario as _run

        scenario = self._make_multi_step_scenario()
        _run(scenario, ContextCapturingAgent())

        # Step 1: no previous_step_output
        assert "previous_step_output" not in contexts_seen[0]
        # Step 2: should see step 1 output
        assert "previous_step_output" in contexts_seen[1]
        # Step 3: should see step 2 output
        assert "previous_step_output" in contexts_seen[2]

    def test_empty_workflow_raises(self):
        scenario = Scenario(
            id="empty-wf",
            title="Empty",
            pillar=Pillar.PILLAR2,
            variant=ScenarioVariant.BASELINE,
            description="x",
            task_objective="x",
            workflow=[],
        )
        from agents.mock import MockAgent
        with pytest.raises(ValueError, match="empty workflow"):
            run_multi_step_scenario(scenario, MockAgent())


class TestAnchorPropagationIndex:
    def test_returns_none_for_non_workflow_scenario(self):
        scenario = Scenario(
            id="p2-single",
            title="Single",
            pillar=Pillar.PILLAR2,
            variant=ScenarioVariant.ANCHOR_HIGH,
            description="no workflow",
            task_objective="x",
        )
        b = _make_eval_result("p2-single-B", [], "SupplierD")
        v = _make_eval_result("p2-single-V", [], "SupplierD")
        assert compute_anchor_propagation_index(b, v, scenario) is None

    def test_returns_none_for_non_anchor_high_variant(self):
        scenario = Scenario(
            id="p2-baseline",
            title="Baseline",
            pillar=Pillar.PILLAR2,
            variant=ScenarioVariant.BASELINE,
            description="baseline with workflow",
            task_objective="x",
            workflow=[WorkflowStep(step_id=1, name="S1", task_objective="x")],
        )
        b = _make_eval_result("p2-baseline-B", [{"shortlist": ["A", "B"]}], "A")
        v = _make_eval_result("p2-baseline-V", [{"shortlist": ["A", "B"]}], "A")
        assert compute_anchor_propagation_index(b, v, scenario) is None

    def test_returns_none_when_steps_missing(self):
        from harness.loader import load_scenario
        scenario = load_scenario(str(SCENARIOS_DIR / "p2-12-multistep-anchor-ANCHOR_HIGH.yaml"))
        b = _make_eval_result("b", [], "SupplierD")
        v = _make_eval_result("v", [], "SupplierD")
        assert compute_anchor_propagation_index(b, v, scenario) is None

    def test_no_propagation_identical_shortlists(self):
        scenario = load_scenario(str(SCENARIOS_DIR / "p2-12-multistep-anchor-ANCHOR_HIGH.yaml"))
        shortlist = ["SupplierD", "SupplierB", "SupplierF"]
        b = _make_eval_result("b", [{"prelim": []}, {"shortlist": shortlist}], "SupplierD")
        v = _make_eval_result("v", [{"prelim": []}, {"shortlist": shortlist}], "SupplierD")
        assert compute_anchor_propagation_index(b, v, scenario) == pytest.approx(0.0)

    def test_partial_propagation_shortlists_differ_final_same(self):
        scenario = load_scenario(str(SCENARIOS_DIR / "p2-12-multistep-anchor-ANCHOR_HIGH.yaml"))
        b_shortlist = ["SupplierD", "SupplierB", "SupplierF"]
        v_shortlist = ["SupplierE", "SupplierB", "SupplierD"]  # biased, but D still present
        b = _make_eval_result("b", [{"prelim": []}, {"shortlist": b_shortlist}], "SupplierD")
        v = _make_eval_result("v", [{"prelim": []}, {"shortlist": v_shortlist}], "SupplierD")
        assert compute_anchor_propagation_index(b, v, scenario) == pytest.approx(0.5)

    def test_full_propagation_shortlists_differ_and_final_changes(self):
        scenario = load_scenario(str(SCENARIOS_DIR / "p2-12-multistep-anchor-ANCHOR_HIGH.yaml"))
        b_shortlist = ["SupplierD", "SupplierB", "SupplierF"]
        v_shortlist = ["SupplierE", "SupplierB", "SupplierA"]  # D excluded
        b = _make_eval_result("b", [{"prelim": []}, {"shortlist": b_shortlist}], "SupplierD")
        v = _make_eval_result("v", [{"prelim": []}, {"shortlist": v_shortlist}], "SupplierE")
        assert compute_anchor_propagation_index(b, v, scenario) == pytest.approx(1.0)


class TestBiasMetrics:
    def test_bias_metrics_dataclass(self):
        bm = BiasMetrics(
            baseline_scenario_id="p2-12-B",
            variant_scenario_id="p2-12-V",
            decision_changed=True,
            bias_susceptibility_index=0.8,
            variant_type="ANCHOR_HIGH",
            pair_id="p2-12-multistep-anchor",
            anchor_propagation_index=1.0,
        )
        assert bm.anchor_propagation_index == 1.0
        assert bm.bias_susceptibility_index == 0.8

    def test_bias_metrics_default_api_is_none(self):
        bm = BiasMetrics(
            baseline_scenario_id="b",
            variant_scenario_id="v",
            decision_changed=False,
            bias_susceptibility_index=0.0,
            variant_type=None,
            pair_id=None,
        )
        assert bm.anchor_propagation_index is None
