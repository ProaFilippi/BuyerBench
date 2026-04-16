"""Tests for the aggregate evaluator and run_suite integration."""
from __future__ import annotations

from pathlib import Path

import pytest

from agents.mock import MockAgent
from buyerbench.models import EvaluationResult, Pillar
from evaluators.aggregate import run_evaluation, run_suite
from harness.loader import load_all_scenarios


SCENARIOS_ROOT = str(Path(__file__).parent.parent / "scenarios")


@pytest.fixture(scope="module")
def all_scenarios():
    return load_all_scenarios(SCENARIOS_ROOT)


@pytest.fixture(scope="module")
def mock_agent():
    return MockAgent()


@pytest.fixture(scope="module")
def suite_results(all_scenarios, mock_agent, tmp_path_factory):
    """Run the full suite with MockAgent in a temp directory."""
    tmp = tmp_path_factory.mktemp("results")
    import os

    orig_dir = os.getcwd()
    os.chdir(tmp)
    try:
        results = run_suite(all_scenarios, mock_agent)
    finally:
        os.chdir(orig_dir)
    return results


class TestRunSuiteBasics:
    def test_returns_18_results(self, suite_results):
        assert len(suite_results) == 26

    def test_all_results_are_evaluation_results(self, suite_results):
        for r in suite_results:
            assert isinstance(r, EvaluationResult)

    def test_all_results_have_agent_id(self, suite_results):
        for r in suite_results:
            assert r.agent_id == "mock-agent-v1"

    def test_results_cover_all_pillars(self, suite_results):
        pillars = {ps.pillar for r in suite_results for ps in r.pillar_scores}
        assert Pillar.PILLAR1 in pillars
        assert Pillar.PILLAR2 in pillars
        assert Pillar.PILLAR3 in pillars

    def test_variant_pair_ids_preserved(self, suite_results):
        paired = [r for r in suite_results if r.variant_pair_id]
        assert len(paired) == 14, "14 pillar2 scenarios have variant_pair_ids"

    def test_summary_json_created(self, all_scenarios, mock_agent, tmp_path):
        import os

        orig_dir = os.getcwd()
        os.chdir(tmp_path)
        try:
            run_suite(all_scenarios, mock_agent)
        finally:
            os.chdir(orig_dir)

        summary_path = tmp_path / "results" / "mock-agent-v1" / "summary.json"
        assert summary_path.exists()

        import json

        with open(summary_path) as f:
            summary = json.load(f)

        assert "agent_id" in summary
        assert "total_scenarios" in summary
        assert summary["total_scenarios"] == 26


class TestMockAgentScores:
    """MockAgent always returns expected_optimal → must score ≥ 0.95 on all scenarios."""

    def test_all_pillar1_scores_above_threshold(self, suite_results):
        p1_results = [r for r in suite_results if r.pillar_scores[0].pillar == Pillar.PILLAR1]
        assert len(p1_results) == 6

        for r in p1_results:
            score = r.pillar_scores[0].score
            assert score >= 0.95, (
                f"Scenario {r.scenario_id}: score {score:.4f} below 0.95. "
                f"Metrics: {r.pillar_scores[0].metrics}. "
                f"Violations: {r.pillar_scores[0].violations}"
            )

    def test_all_pillar2_scores_above_threshold(self, suite_results):
        p2_results = [r for r in suite_results if r.pillar_scores[0].pillar == Pillar.PILLAR2]
        assert len(p2_results) == 14

        for r in p2_results:
            score = r.pillar_scores[0].score
            assert score >= 0.95, (
                f"Scenario {r.scenario_id}: score {score:.4f} below 0.95. "
                f"Metrics: {r.pillar_scores[0].metrics}"
            )

    def test_all_pillar3_scores_above_threshold(self, suite_results):
        p3_results = [r for r in suite_results if r.pillar_scores[0].pillar == Pillar.PILLAR3]
        assert len(p3_results) == 6

        for r in p3_results:
            score = r.pillar_scores[0].score
            assert score >= 0.95, (
                f"Scenario {r.scenario_id}: score {score:.4f} below 0.95. "
                f"Metrics: {r.pillar_scores[0].metrics}. "
                f"Violations: {r.pillar_scores[0].violations}"
            )

    def test_all_scenarios_score_above_threshold(self, suite_results):
        """Unified check: all 26 scenarios score ≥ 0.95 with MockAgent."""
        failures = []
        for r in suite_results:
            for ps in r.pillar_scores:
                if ps.score < 0.95:
                    failures.append(
                        f"{r.scenario_id} ({ps.pillar.value}): score={ps.score:.4f}, "
                        f"violations={ps.violations}"
                    )
        assert not failures, "MockAgent failed on:\n" + "\n".join(failures)


class TestRunEvaluation:
    def test_run_evaluation_single_scenario(self, all_scenarios, mock_agent):
        scenario = all_scenarios[0]
        response = mock_agent.respond(scenario)
        result = run_evaluation(scenario, response)
        assert isinstance(result, EvaluationResult)
        assert result.scenario_id == scenario.id
        assert len(result.pillar_scores) == 1

    def test_overall_pass_for_mock_agent(self, all_scenarios, mock_agent):
        scenario = next(s for s in all_scenarios if "basic" in s.id or s.pillar == Pillar.PILLAR1)
        response = mock_agent.respond(scenario)
        result = run_evaluation(scenario, response)
        assert result.pillar_scores[0].score >= 0.95


# ---------------------------------------------------------------------------
# UPGRADE-4: metadata propagation tests
# ---------------------------------------------------------------------------

class TestRunMetadataPropagation:
    """Tests that UPGRADE-4 metadata fields are correctly propagated through the pipeline."""

    def _make_pillar2_scenario(self, all_scenarios):
        return next(s for s in all_scenarios if s.pillar == Pillar.PILLAR2)

    def test_variant_set_on_result(self, all_scenarios, mock_agent):
        """variant field on EvaluationResult must reflect the scenario's ScenarioVariant."""
        scenario = all_scenarios[0]
        response = mock_agent.respond(scenario)
        result = run_evaluation(scenario, response)
        assert result.variant == scenario.variant.value

    def test_bias_category_inferred_for_pillar2(self, all_scenarios, mock_agent):
        """bias_category must be derived from variant_pair_id for Pillar 2 scenarios."""
        scenario = self._make_pillar2_scenario(all_scenarios)
        response = mock_agent.respond(scenario)
        result = run_evaluation(scenario, response)
        if result.variant_pair_id:
            assert result.bias_category is not None
            # e.g. "p2-01-anchoring" → "anchoring"; "p2-05-sunk-cost" → "sunk_cost"
            assert "_" not in result.bias_category or result.bias_category.replace("_", "-") in (result.variant_pair_id or "")

    def test_bias_category_none_without_variant_pair_id(self, all_scenarios, mock_agent):
        """bias_category must be None for scenarios without a variant_pair_id."""
        scenario = next(s for s in all_scenarios if not s.variant_pair_id)
        response = mock_agent.respond(scenario)
        result = run_evaluation(scenario, response)
        assert result.bias_category is None

    def test_metadata_defaults_for_mock_agent(self, all_scenarios, mock_agent):
        """MockAgent returns no API metadata; fields must use safe defaults."""
        scenario = all_scenarios[0]
        response = mock_agent.respond(scenario)
        result = run_evaluation(scenario, response)
        assert result.temperature is None
        assert result.token_count_input == 0
        assert result.token_count_output == 0
        assert result.api_cost_usd is None
        assert result.error_flag is False
        assert result.model_version is None

    def test_temperature_propagated_from_response(self, all_scenarios):
        """temperature on AgentResponse must be propagated to EvaluationResult."""
        from buyerbench.models import AgentResponse, Pillar, Scenario, ScenarioVariant

        scenario = all_scenarios[0]
        response = AgentResponse(
            scenario_id=scenario.id,
            agent_id="test-agent",
            decisions=scenario.expected_optimal,
            raw_output="",
            temperature=0.7,
        )
        result = run_evaluation(scenario, response)
        assert result.temperature == 0.7

    def test_error_fields_propagated_from_response(self, all_scenarios):
        """error_flag and error_message must propagate from AgentResponse."""
        from buyerbench.models import AgentResponse

        scenario = all_scenarios[0]
        response = AgentResponse(
            scenario_id=scenario.id,
            agent_id="test-agent",
            decisions={},
            raw_output="API error: 500",
            error_flag=True,
            error_message="Internal Server Error",
        )
        result = run_evaluation(scenario, response)
        assert result.error_flag is True
        assert result.error_message == "Internal Server Error"

    def test_latency_ms_propagated_from_response(self, all_scenarios, mock_agent):
        """latency_ms must propagate from AgentResponse to EvaluationResult."""
        from buyerbench.models import AgentResponse

        scenario = all_scenarios[0]
        response = AgentResponse(
            scenario_id=scenario.id,
            agent_id="test-agent",
            decisions=scenario.expected_optimal,
            raw_output="",
            latency_ms=250.5,
        )
        result = run_evaluation(scenario, response)
        assert result.latency_ms == 250.5

    def test_run_id_computed_in_run_scenario(self, all_scenarios, mock_agent, tmp_path):
        """run_id must be a 16-character hex string computed in run_scenario()."""
        from harness.runner import run_scenario

        scenario = all_scenarios[0]
        result = run_scenario(scenario, mock_agent, output_dir=tmp_path)
        assert len(result.run_id) == 16
        assert all(c in "0123456789abcdef" for c in result.run_id)

    def test_run_id_deterministic_given_same_inputs(self, all_scenarios, mock_agent, tmp_path):
        """Same (agent_id, scenario_id, variant, run_index, seed) must produce same run_id."""
        from harness.runner import run_scenario

        scenario = all_scenarios[0]
        seed = 42
        result1 = run_scenario(scenario, mock_agent, output_dir=tmp_path, run_index=0, supplier_order_seed=seed)
        result2 = run_scenario(scenario, mock_agent, output_dir=tmp_path, run_index=0, supplier_order_seed=seed)
        assert result1.run_id == result2.run_id

    def test_run_id_differs_for_different_run_index(self, all_scenarios, mock_agent, tmp_path):
        """Different run_index must produce different run_id even with same seed."""
        from harness.runner import run_scenario

        scenario = all_scenarios[0]
        seed = 99
        result0 = run_scenario(scenario, mock_agent, output_dir=tmp_path, run_index=0, supplier_order_seed=seed)
        result1 = run_scenario(scenario, mock_agent, output_dir=tmp_path, run_index=1, supplier_order_seed=seed)
        assert result0.run_id != result1.run_id


class TestInferBiasCategory:
    """Unit tests for the _infer_bias_category helper."""

    def test_anchoring(self):
        from evaluators.aggregate import _infer_bias_category
        assert _infer_bias_category("p2-01-anchoring") == "anchoring"

    def test_framing(self):
        from evaluators.aggregate import _infer_bias_category
        assert _infer_bias_category("p2-02-framing") == "framing"

    def test_sunk_cost_dash_to_underscore(self):
        from evaluators.aggregate import _infer_bias_category
        assert _infer_bias_category("p2-05-sunk-cost") == "sunk_cost"

    def test_none_input(self):
        from evaluators.aggregate import _infer_bias_category
        assert _infer_bias_category(None) is None

    def test_short_id_returns_none(self):
        from evaluators.aggregate import _infer_bias_category
        assert _infer_bias_category("p2-01") is None

    def test_decoy(self):
        from evaluators.aggregate import _infer_bias_category
        assert _infer_bias_category("p2-03-decoy") == "decoy"

    def test_scarcity(self):
        from evaluators.aggregate import _infer_bias_category
        assert _infer_bias_category("p2-04-scarcity") == "scarcity"
