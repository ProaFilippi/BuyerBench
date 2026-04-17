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
        # REV-4 added 6 hard scenarios: 29 + 6 = 35
        assert len(suite_results) == 35

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
        # REV-4 added 6 more paired scenarios: 17 + 6 = 23
        assert len(paired) == 23, "23 pillar2 scenarios have variant_pair_ids"

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
        # REV-4 added 6 hard scenarios: 29 + 6 = 35
        assert summary["total_scenarios"] == 35


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
        # REV-4 added 6 hard scenarios: 17 + 6 = 23
        assert len(p2_results) == 23

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
        """Unified check: all 35 scenarios score ≥ 0.95 with MockAgent."""
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


# ---------------------------------------------------------------------------
# UPGRADE-4: JSON file logging tests (run_index, temperature, timestamp, tokens)
# ---------------------------------------------------------------------------

class TestUpgrade4RunMetadataLogging:
    """Verify that all four UPGRADE-4 metadata fields are present and correct in the
    written JSON file after run_scenario() completes."""

    @pytest.fixture
    def scenario(self, all_scenarios):
        return all_scenarios[0]

    def test_run_index_present_in_json(self, scenario, mock_agent, tmp_path):
        """run_index must appear as a top-level key in the output JSON file."""
        from harness.runner import run_scenario
        import json

        run_scenario(scenario, mock_agent, output_dir=tmp_path, run_index=0)
        json_file = tmp_path / mock_agent.agent_id / f"{scenario.id}-run000.json"
        data = json.loads(json_file.read_text())
        assert "run_index" in data

    def test_run_index_matches_parameter(self, scenario, mock_agent, tmp_path):
        """The run_index stored in JSON must equal the run_index argument passed to run_scenario()."""
        from harness.runner import run_scenario
        import json

        run_scenario(scenario, mock_agent, output_dir=tmp_path, run_index=5)
        json_file = tmp_path / mock_agent.agent_id / f"{scenario.id}-run005.json"
        data = json.loads(json_file.read_text())
        assert data["run_index"] == 5

    def test_temperature_field_present_in_json(self, scenario, mock_agent, tmp_path):
        """temperature must appear as a top-level key in the output JSON file."""
        from harness.runner import run_scenario
        import json

        run_scenario(scenario, mock_agent, output_dir=tmp_path)
        agent_dir = tmp_path / mock_agent.agent_id
        json_file = sorted(agent_dir.glob("*.json"))[0]
        data = json.loads(json_file.read_text())
        assert "temperature" in data

    def test_temperature_value_propagated_when_set(self, scenario, tmp_path):
        """When AgentResponse carries temperature=0.7, the JSON file must record 0.7."""
        from buyerbench.models import AgentResponse
        from evaluators.aggregate import run_evaluation
        from harness.runner import run_scenario
        import json

        # Construct a response with an explicit temperature
        response = AgentResponse(
            scenario_id=scenario.id,
            agent_id="test-agent-temp",
            decisions=scenario.expected_optimal,
            raw_output="",
            temperature=0.7,
        )
        result = run_evaluation(scenario, response)
        result.run_index = 0
        result.run_id = "abcd1234abcd1234"

        dest = tmp_path / response.agent_id
        dest.mkdir(parents=True, exist_ok=True)
        (dest / f"{scenario.id}-run000.json").write_text(result.model_dump_json(indent=2))

        data = json.loads((dest / f"{scenario.id}-run000.json").read_text())
        assert data["temperature"] == pytest.approx(0.7)

    def test_timestamp_present_in_json(self, scenario, mock_agent, tmp_path):
        """timestamp must appear as a top-level key in the output JSON file."""
        from harness.runner import run_scenario
        import json

        run_scenario(scenario, mock_agent, output_dir=tmp_path)
        agent_dir = tmp_path / mock_agent.agent_id
        json_file = sorted(agent_dir.glob("*.json"))[0]
        data = json.loads(json_file.read_text())
        assert "timestamp" in data

    def test_timestamp_is_iso_format_string(self, scenario, mock_agent, tmp_path):
        """timestamp in JSON must be an ISO 8601 string, not None or a numeric epoch."""
        from harness.runner import run_scenario
        from datetime import datetime
        import json

        run_scenario(scenario, mock_agent, output_dir=tmp_path)
        agent_dir = tmp_path / mock_agent.agent_id
        json_file = sorted(agent_dir.glob("*.json"))[0]
        data = json.loads(json_file.read_text())
        ts = data["timestamp"]
        assert isinstance(ts, str), f"Expected string, got {type(ts)}: {ts}"
        # Must parse as a datetime without error
        parsed = datetime.fromisoformat(ts)
        assert parsed is not None

    def test_timestamp_is_utc(self, scenario, mock_agent, tmp_path):
        """timestamp in JSON must include a UTC timezone indicator (+00:00 or Z)."""
        from harness.runner import run_scenario
        import json

        run_scenario(scenario, mock_agent, output_dir=tmp_path)
        agent_dir = tmp_path / mock_agent.agent_id
        json_file = sorted(agent_dir.glob("*.json"))[0]
        data = json.loads(json_file.read_text())
        ts = data["timestamp"]
        assert "+00:00" in ts or ts.endswith("Z"), f"Expected UTC offset in: {ts}"

    def test_token_count_input_present_in_json(self, scenario, mock_agent, tmp_path):
        """token_count_input must appear as a top-level key in the output JSON file."""
        from harness.runner import run_scenario
        import json

        run_scenario(scenario, mock_agent, output_dir=tmp_path)
        agent_dir = tmp_path / mock_agent.agent_id
        json_file = sorted(agent_dir.glob("*.json"))[0]
        data = json.loads(json_file.read_text())
        assert "token_count_input" in data

    def test_token_count_output_present_in_json(self, scenario, mock_agent, tmp_path):
        """token_count_output must appear as a top-level key in the output JSON file."""
        from harness.runner import run_scenario
        import json

        run_scenario(scenario, mock_agent, output_dir=tmp_path)
        agent_dir = tmp_path / mock_agent.agent_id
        json_file = sorted(agent_dir.glob("*.json"))[0]
        data = json.loads(json_file.read_text())
        assert "token_count_output" in data

    def test_token_counts_default_zero_for_cli_and_mock_agents(self, scenario, mock_agent, tmp_path):
        """CLI/mock agents cannot introspect subprocess token usage; defaults must be 0."""
        from harness.runner import run_scenario
        import json

        run_scenario(scenario, mock_agent, output_dir=tmp_path)
        agent_dir = tmp_path / mock_agent.agent_id
        json_file = sorted(agent_dir.glob("*.json"))[0]
        data = json.loads(json_file.read_text())
        assert data["token_count_input"] == 0
        assert data["token_count_output"] == 0

    def test_token_counts_propagated_when_nonzero(self, scenario, tmp_path):
        """When AgentResponse carries non-zero token counts, JSON must record them."""
        from buyerbench.models import AgentResponse
        from evaluators.aggregate import run_evaluation
        import json

        response = AgentResponse(
            scenario_id=scenario.id,
            agent_id="test-agent-tokens",
            decisions=scenario.expected_optimal,
            raw_output="",
            token_count_input=512,
            token_count_output=128,
        )
        result = run_evaluation(scenario, response)
        result.run_index = 0
        result.run_id = "dead1234beef5678"

        dest = tmp_path / response.agent_id
        dest.mkdir(parents=True, exist_ok=True)
        json_path = dest / f"{scenario.id}-run000.json"
        json_path.write_text(result.model_dump_json(indent=2))

        data = json.loads(json_path.read_text())
        assert data["token_count_input"] == 512
        assert data["token_count_output"] == 128

    def test_all_four_upgrade4_field_groups_in_json(self, scenario, mock_agent, tmp_path):
        """All four UPGRADE-4 field categories (run_index, temperature, timestamp, tokens)
        must be present in every JSON result file."""
        from harness.runner import run_scenario
        import json

        run_scenario(scenario, mock_agent, output_dir=tmp_path, run_index=2)
        json_file = tmp_path / mock_agent.agent_id / f"{scenario.id}-run002.json"
        data = json.loads(json_file.read_text())
        for field in ("run_index", "temperature", "timestamp", "token_count_input", "token_count_output"):
            assert field in data, f"UPGRADE-4 field '{field}' missing from JSON output"


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


# ---------------------------------------------------------------------------
# UPGRADE-5: cell-level aggregate output integration tests
# ---------------------------------------------------------------------------

class TestUpgrade5CellLevelAggregateOutput:
    """Integration tests for UPGRADE-5: verify the run_scenario() → aggregate_cells()
    pipeline produces correct cell-level statistics from multi-run experiments."""

    @pytest.fixture
    def p2_scenario(self, all_scenarios):
        """Return the first Pillar 2 scenario with a variant_pair_id for pairing tests."""
        return next(
            s for s in all_scenarios
            if "PILLAR2" in str(s.pillar) and s.variant_pair_id is not None
        )

    def test_n_runs_produces_one_cell(self, p2_scenario, mock_agent, tmp_path):
        """N runs of the same scenario by the same agent must aggregate into exactly one cell."""
        from harness.runner import run_scenario
        from results.aggregate_cells import aggregate_cells

        results = [
            run_scenario(p2_scenario, mock_agent, output_dir=tmp_path, run_index=i)
            for i in range(5)
        ]
        report = aggregate_cells(results)
        assert report.n_cells == 1

    def test_n_runs_reflected_in_cell_n_runs(self, p2_scenario, mock_agent, tmp_path):
        """CellAggregate.n_runs must equal the number of runs submitted."""
        from harness.runner import run_scenario
        from results.aggregate_cells import aggregate_cells

        results = [
            run_scenario(p2_scenario, mock_agent, output_dir=tmp_path, run_index=i)
            for i in range(7)
        ]
        report = aggregate_cells(results)
        assert report.cells[0].n_runs == 7

    def test_n_total_runs_matches_input(self, p2_scenario, mock_agent, tmp_path):
        """CellAggregateReport.n_total_runs must equal the total number of results."""
        from harness.runner import run_scenario
        from results.aggregate_cells import aggregate_cells

        N = 6
        results = [
            run_scenario(p2_scenario, mock_agent, output_dir=tmp_path, run_index=i)
            for i in range(N)
        ]
        report = aggregate_cells(results)
        assert report.n_total_runs == N

    def test_cell_id_is_deterministic(self, p2_scenario, mock_agent, tmp_path):
        """The cell_id for the same (agent, scenario, variant) must be identical across calls."""
        from harness.runner import run_scenario
        from results.aggregate_cells import aggregate_cells

        results_a = [
            run_scenario(p2_scenario, mock_agent, output_dir=tmp_path / "a", run_index=i)
            for i in range(3)
        ]
        results_b = [
            run_scenario(p2_scenario, mock_agent, output_dir=tmp_path / "b", run_index=i)
            for i in range(3)
        ]
        id_a = aggregate_cells(results_a).cells[0].cell_id
        id_b = aggregate_cells(results_b).cells[0].cell_id
        assert id_a == id_b

    def test_cell_contains_agent_id(self, p2_scenario, mock_agent, tmp_path):
        """CellAggregate.agent_id must match the agent that produced the runs."""
        from harness.runner import run_scenario
        from results.aggregate_cells import aggregate_cells

        results = [
            run_scenario(p2_scenario, mock_agent, output_dir=tmp_path, run_index=i)
            for i in range(3)
        ]
        cell = aggregate_cells(results).cells[0]
        assert cell.agent_id == mock_agent.agent_id

    def test_write_cell_aggregates_creates_file(self, p2_scenario, mock_agent, tmp_path):
        """write_cell_aggregates() must create cell_aggregates.json in the output dir."""
        import json
        from harness.runner import run_scenario
        from results.aggregate_cells import aggregate_cells, write_cell_aggregates

        results = [
            run_scenario(p2_scenario, mock_agent, output_dir=tmp_path, run_index=i)
            for i in range(3)
        ]
        report = aggregate_cells(results)
        out_path = write_cell_aggregates(report, tmp_path)
        assert out_path.exists()

    def test_cell_aggregates_json_is_valid(self, p2_scenario, mock_agent, tmp_path):
        """cell_aggregates.json must be parseable and contain 'cells' and 'n_total_runs'."""
        import json
        from harness.runner import run_scenario
        from results.aggregate_cells import aggregate_cells, write_cell_aggregates

        results = [
            run_scenario(p2_scenario, mock_agent, output_dir=tmp_path, run_index=i)
            for i in range(4)
        ]
        report = aggregate_cells(results)
        out_path = write_cell_aggregates(report, tmp_path)
        data = json.loads(out_path.read_text())
        assert "cells" in data
        assert "n_total_runs" in data
        assert data["n_total_runs"] == 4

    def test_two_scenarios_produce_two_cells(self, all_scenarios, mock_agent, tmp_path):
        """Running N runs each on two different scenarios must produce exactly 2 cells."""
        from harness.runner import run_scenario
        from results.aggregate_cells import aggregate_cells

        p2_scenarios = [
            s for s in all_scenarios
            if "PILLAR2" in str(s.pillar) and s.variant_pair_id is not None
        ][:2]
        assert len(p2_scenarios) == 2, "Need at least 2 Pillar 2 paired scenarios"

        results = []
        for s in p2_scenarios:
            for i in range(3):
                results.append(
                    run_scenario(s, mock_agent, output_dir=tmp_path, run_index=i)
                )
        report = aggregate_cells(results)
        assert report.n_cells == 2

    def test_n_valid_runs_excludes_errors(self, p2_scenario, mock_agent, tmp_path):
        """n_valid_runs must be less than n_runs when some runs carry error_flag=True."""
        from buyerbench.models import EvaluationResult
        from harness.runner import run_scenario
        from results.aggregate_cells import aggregate_cells

        results = [
            run_scenario(p2_scenario, mock_agent, output_dir=tmp_path, run_index=i)
            for i in range(4)
        ]
        # Mark one result as an error
        results[0].error_flag = True

        report = aggregate_cells(results)
        cell = report.cells[0]
        assert cell.n_runs == 4
        assert cell.n_valid_runs == 3

    def test_mean_bsi_is_float_in_zero_one(self, p2_scenario, mock_agent, tmp_path):
        """CellAggregate.mean_bsi must be a float in [0.0, 1.0]."""
        from harness.runner import run_scenario
        from results.aggregate_cells import aggregate_cells

        results = [
            run_scenario(p2_scenario, mock_agent, output_dir=tmp_path, run_index=i)
            for i in range(5)
        ]
        cell = aggregate_cells(results).cells[0]
        assert isinstance(cell.mean_bsi, float)
        assert 0.0 <= cell.mean_bsi <= 1.0

    def test_ci_lower_le_mean_le_upper(self, p2_scenario, mock_agent, tmp_path):
        """95% CI must satisfy ci_lower_95 <= mean_bsi <= ci_upper_95."""
        from harness.runner import run_scenario
        from results.aggregate_cells import aggregate_cells

        results = [
            run_scenario(p2_scenario, mock_agent, output_dir=tmp_path, run_index=i)
            for i in range(6)
        ]
        cell = aggregate_cells(results).cells[0]
        assert cell.ci_lower_95 <= cell.mean_bsi <= cell.ci_upper_95

    def test_aggregate_cells_from_dir_matches_in_memory(self, p2_scenario, mock_agent, tmp_path):
        """aggregate_cells_from_dir() must produce the same n_cells as in-memory aggregation."""
        from harness.runner import run_scenario
        from results.aggregate_cells import aggregate_cells, aggregate_cells_from_dir

        results = [
            run_scenario(p2_scenario, mock_agent, output_dir=tmp_path, run_index=i)
            for i in range(4)
        ]
        in_memory = aggregate_cells(results)
        from_dir = aggregate_cells_from_dir(tmp_path)
        assert from_dir.n_cells == in_memory.n_cells
        assert from_dir.n_total_runs == in_memory.n_total_runs
