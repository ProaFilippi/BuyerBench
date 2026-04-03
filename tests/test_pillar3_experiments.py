"""Tests for Pillar 3 experiment execution and security summary computation.

Covers:
- compute_security_summary_from_experiment_dir on a directory of valid EvaluationResult JSONs
- compute_security_summary_from_experiment_dir when all results are skipped sentinels
- compute_security_summary_from_experiment_dir handles mixed valid/skipped results
- `run --pillar 3` writes security-compliance-summary.json after the run
- The full pillar 3 run via MockAgent produces 5 result files per agent
- Injection resistance table is populated from p3-05 results
"""
from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from agents.mock import MockAgent
from buyerbench.__main__ import cli, _write_skipped_results
from evaluators.aggregate import compute_security_summary_from_experiment_dir
from harness.loader import load_all_scenarios
from harness.runner import run_scenario


SCENARIOS_ROOT = str(Path(__file__).parent.parent / "scenarios")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _p3_scenarios():
    return [s for s in load_all_scenarios(SCENARIOS_ROOT) if s.pillar.value == "PILLAR3"]


# ---------------------------------------------------------------------------
# compute_security_summary_from_experiment_dir — valid results (MockAgent)
# ---------------------------------------------------------------------------

class TestComputeSecuritySummaryFromExperimentDirValid:
    """Security summary computation on a temp experiment dir with MockAgent results."""

    @pytest.fixture(scope="class")
    def experiment_dir(self, tmp_path_factory):
        """Build an experiment dir with MockAgent Pillar 3 results."""
        exp = tmp_path_factory.mktemp("exp_p3_valid")
        agent = MockAgent()
        for scenario in _p3_scenarios():
            run_scenario(scenario, agent, output_dir=str(exp))
        return exp

    def test_returns_dict_with_expected_keys(self, experiment_dir):
        result = compute_security_summary_from_experiment_dir(experiment_dir)
        assert isinstance(result, dict)
        for key in (
            "experiment_dir", "generated_at", "total_result_files",
            "skipped_result_files", "valid_result_files",
            "agents_evaluated", "agents_skipped",
            "per_agent_security", "injection_resistance_table",
            "cross_agent_summary",
        ):
            assert key in result, f"Missing key: {key}"

    def test_counts_correct_total_files(self, experiment_dir):
        result = compute_security_summary_from_experiment_dir(experiment_dir)
        # 5 Pillar 3 scenarios × 1 agent
        assert result["total_result_files"] == 5

    def test_no_skipped_files_for_mock_agent(self, experiment_dir):
        result = compute_security_summary_from_experiment_dir(experiment_dir)
        assert result["skipped_result_files"] == 0
        assert result["valid_result_files"] == 5

    def test_mock_agent_in_agents_evaluated(self, experiment_dir):
        result = compute_security_summary_from_experiment_dir(experiment_dir)
        assert "mock-agent-v1" in result["agents_evaluated"]

    def test_per_agent_security_has_five_scenarios(self, experiment_dir):
        result = compute_security_summary_from_experiment_dir(experiment_dir)
        agent_sec = result["per_agent_security"]["mock-agent-v1"]
        assert len(agent_sec["results_by_scenario"]) == 5

    def test_per_agent_security_has_aggregate_metrics(self, experiment_dir):
        result = compute_security_summary_from_experiment_dir(experiment_dir)
        agent_sec = result["per_agent_security"]["mock-agent-v1"]
        assert "mean_compliance_adherence_rate" in agent_sec
        assert "mean_security_violation_frequency" in agent_sec
        assert 0.0 <= agent_sec["mean_compliance_adherence_rate"] <= 1.0

    def test_injection_resistance_table_has_entry_for_p3_05(self, experiment_dir):
        result = compute_security_summary_from_experiment_dir(experiment_dir)
        table = result["injection_resistance_table"]
        # MockAgent picks optimal — should produce one entry for p3-05
        assert len(table) >= 1
        entry = table[0]
        assert "agent_id" in entry
        assert "scenario_id" in entry
        assert "injection_followed" in entry
        assert "injected_instruction_not_followed" in entry
        assert "injection_flagged_in_reasoning" in entry
        assert "correct_supplier_selected" in entry

    def test_mock_agent_resists_injection(self, experiment_dir):
        """MockAgent returns expected_optimal, so injection should NOT be followed."""
        result = compute_security_summary_from_experiment_dir(experiment_dir)
        table = result["injection_resistance_table"]
        for entry in table:
            if entry["agent_id"] == "mock-agent-v1":
                assert entry["injected_instruction_not_followed"] is True
                assert entry["injection_followed"] is False

    def test_cross_agent_summary_has_required_keys(self, experiment_dir):
        result = compute_security_summary_from_experiment_dir(experiment_dir)
        summary = result["cross_agent_summary"]
        assert "mean_compliance_adherence_rate" in summary
        assert "injection_resistance_rate" in summary
        assert "total_injection_evaluations" in summary
        assert "injection_resisted_count" in summary

    def test_injection_resistance_rate_is_one_for_mock_agent(self, experiment_dir):
        """MockAgent always resists injection → rate should be 1.0."""
        result = compute_security_summary_from_experiment_dir(experiment_dir)
        summary = result["cross_agent_summary"]
        assert summary["injection_resistance_rate"] == 1.0


# ---------------------------------------------------------------------------
# compute_security_summary_from_experiment_dir — all skipped sentinels
# ---------------------------------------------------------------------------

class TestComputeSecuritySummaryFromExperimentDirAllSkipped:
    """Security summary when every result file is a status=skipped sentinel."""

    @pytest.fixture(scope="class")
    def experiment_dir(self, tmp_path_factory):
        exp = tmp_path_factory.mktemp("exp_p3_skipped")
        _write_skipped_results("claude-code-baseline", _p3_scenarios(), str(exp))
        _write_skipped_results("codex-baseline", _p3_scenarios(), str(exp))
        return exp

    def test_skipped_count_matches_files(self, experiment_dir):
        result = compute_security_summary_from_experiment_dir(experiment_dir)
        # 2 agents × 5 scenarios = 10 files, all skipped
        assert result["total_result_files"] == 10
        assert result["skipped_result_files"] == 10
        assert result["valid_result_files"] == 0

    def test_no_agents_evaluated(self, experiment_dir):
        result = compute_security_summary_from_experiment_dir(experiment_dir)
        assert result["agents_evaluated"] == []

    def test_agents_skipped_lists_agent_dirs(self, experiment_dir):
        result = compute_security_summary_from_experiment_dir(experiment_dir)
        assert set(result["agents_skipped"]) == {"claude-code-baseline", "codex-baseline"}

    def test_injection_resistance_table_is_empty(self, experiment_dir):
        result = compute_security_summary_from_experiment_dir(experiment_dir)
        assert result["injection_resistance_table"] == []

    def test_cross_agent_summary_null_injection_rate(self, experiment_dir):
        result = compute_security_summary_from_experiment_dir(experiment_dir)
        summary = result["cross_agent_summary"]
        assert summary["injection_resistance_rate"] is None
        assert summary["total_injection_evaluations"] == 0


# ---------------------------------------------------------------------------
# compute_security_summary_from_experiment_dir — mixed valid + skipped
# ---------------------------------------------------------------------------

class TestComputeSecuritySummaryFromExperimentDirMixed:
    @pytest.fixture(scope="class")
    def experiment_dir(self, tmp_path_factory):
        exp = tmp_path_factory.mktemp("exp_p3_mixed")
        # MockAgent provides real results
        agent = MockAgent()
        for scenario in _p3_scenarios():
            run_scenario(scenario, agent, output_dir=str(exp))
        # Another agent is skipped
        _write_skipped_results("codex-baseline", _p3_scenarios(), str(exp))
        return exp

    def test_correct_valid_and_skipped_counts(self, experiment_dir):
        result = compute_security_summary_from_experiment_dir(experiment_dir)
        assert result["valid_result_files"] == 5
        assert result["skipped_result_files"] == 5

    def test_only_mock_agent_in_evaluated(self, experiment_dir):
        result = compute_security_summary_from_experiment_dir(experiment_dir)
        assert "mock-agent-v1" in result["agents_evaluated"]
        assert "codex-baseline" not in result["agents_evaluated"]
        assert "codex-baseline" in result["agents_skipped"]

    def test_injection_table_only_has_mock_agent(self, experiment_dir):
        result = compute_security_summary_from_experiment_dir(experiment_dir)
        agents_in_table = {row["agent_id"] for row in result["injection_resistance_table"]}
        assert "mock-agent-v1" in agents_in_table
        assert "codex-baseline" not in agents_in_table


# ---------------------------------------------------------------------------
# `run --pillar 3` integration: writes security-compliance-summary.json
# ---------------------------------------------------------------------------

class TestRunPillar3WritesSecuritySummary:
    def test_security_summary_written_for_mock_agent(self, tmp_path):
        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["run", "--agent", "mock-agent-v1", "--pillar", "3",
             "--output-dir", str(tmp_path)],
        )
        assert result.exit_code == 0, f"Non-zero exit:\n{result.output}"

        sec_path = tmp_path / "security-compliance-summary.json"
        assert sec_path.exists(), "security-compliance-summary.json not created"

        data = json.loads(sec_path.read_text())
        assert data["valid_result_files"] == 5
        assert "mock-agent-v1" in data["agents_evaluated"]

    def test_security_summary_written_after_all_skipped(self, tmp_path):
        """Security summary is also written (zero valid) when all agents are skipped."""
        runner = CliRunner()

        no_agents_env = {
            "clis": {},
            "api_keys": {},
            "mcp_server": {"started": True, "error": None},
            "overall": False,
            "available_agents": [],
        }

        with patch("harness.preflight.check_environment", return_value=no_agents_env):
            result = runner.invoke(
                cli,
                ["run", "--agent", "all", "--pillar", "3",
                 "--output-dir", str(tmp_path)],
            )

        assert result.exit_code == 0, f"Non-zero exit:\n{result.output}"

        sec_path = tmp_path / "security-compliance-summary.json"
        assert sec_path.exists(), "security-compliance-summary.json not created"

        data = json.loads(sec_path.read_text())
        assert data["skipped_result_files"] > 0
        assert data["valid_result_files"] == 0

    def test_run_pillar3_produces_5_result_files(self, tmp_path):
        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["run", "--agent", "mock-agent-v1", "--pillar", "3",
             "--output-dir", str(tmp_path)],
        )
        assert result.exit_code == 0, f"Non-zero exit:\n{result.output}"

        agent_dir = tmp_path / "mock-agent-v1"
        assert agent_dir.is_dir()
        result_files = list(agent_dir.glob("*.json"))
        assert len(result_files) == 5

    def test_no_security_summary_for_pillar1_run(self, tmp_path):
        """Security summary should NOT be written for non-Pillar-3 runs."""
        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["run", "--agent", "mock-agent-v1", "--pillar", "1",
             "--output-dir", str(tmp_path)],
        )
        assert result.exit_code == 0, f"Non-zero exit:\n{result.output}"

        sec_path = tmp_path / "security-compliance-summary.json"
        assert not sec_path.exists(), (
            "Security summary should not be created for Pillar 1 runs"
        )

    def test_injection_resistance_table_in_output(self, tmp_path):
        """The security summary includes an injection_resistance_table for p3-05."""
        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["run", "--agent", "mock-agent-v1", "--pillar", "3",
             "--output-dir", str(tmp_path)],
        )
        assert result.exit_code == 0, f"Non-zero exit:\n{result.output}"

        data = json.loads((tmp_path / "security-compliance-summary.json").read_text())
        table = data["injection_resistance_table"]
        assert len(table) >= 1
        entry = table[0]
        assert entry["agent_id"] == "mock-agent-v1"
        assert "p3-05" in entry["scenario_id"]
        assert entry["injected_instruction_not_followed"] is True
        assert entry["injection_followed"] is False
