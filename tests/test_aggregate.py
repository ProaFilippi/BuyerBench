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
        assert len(suite_results) == 18

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
        assert len(paired) == 8, "8 pillar2 scenarios have variant_pair_ids"

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
        assert summary["total_scenarios"] == 18


class TestMockAgentScores:
    """MockAgent always returns expected_optimal → must score ≥ 0.95 on all scenarios."""

    def test_all_pillar1_scores_above_threshold(self, suite_results):
        p1_results = [r for r in suite_results if r.pillar_scores[0].pillar == Pillar.PILLAR1]
        assert len(p1_results) == 5

        for r in p1_results:
            score = r.pillar_scores[0].score
            assert score >= 0.95, (
                f"Scenario {r.scenario_id}: score {score:.4f} below 0.95. "
                f"Metrics: {r.pillar_scores[0].metrics}. "
                f"Violations: {r.pillar_scores[0].violations}"
            )

    def test_all_pillar2_scores_above_threshold(self, suite_results):
        p2_results = [r for r in suite_results if r.pillar_scores[0].pillar == Pillar.PILLAR2]
        assert len(p2_results) == 8

        for r in p2_results:
            score = r.pillar_scores[0].score
            assert score >= 0.95, (
                f"Scenario {r.scenario_id}: score {score:.4f} below 0.95. "
                f"Metrics: {r.pillar_scores[0].metrics}"
            )

    def test_all_pillar3_scores_above_threshold(self, suite_results):
        p3_results = [r for r in suite_results if r.pillar_scores[0].pillar == Pillar.PILLAR3]
        assert len(p3_results) == 5

        for r in p3_results:
            score = r.pillar_scores[0].score
            assert score >= 0.95, (
                f"Scenario {r.scenario_id}: score {score:.4f} below 0.95. "
                f"Metrics: {r.pillar_scores[0].metrics}. "
                f"Violations: {r.pillar_scores[0].violations}"
            )

    def test_all_scenarios_score_above_threshold(self, suite_results):
        """Unified check: all 18 scenarios score ≥ 0.95 with MockAgent."""
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
