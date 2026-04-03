"""Tests for Pillar 2 experiment execution and BSI computation from experiment dirs.

Covers:
- compute_bsi_from_experiment_dir on a directory of valid EvaluationResult JSONs
- compute_bsi_from_experiment_dir when all results are skipped sentinels
- compute_bsi_from_experiment_dir handles mixed valid/skipped results
- `run --pillar 2` writes bias-susceptibility-summary.json after the run
- The full pillar 2 run via MockAgent produces 8 result files per agent
"""
from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from agents.mock import MockAgent
from buyerbench.__main__ import cli, _write_skipped_results
from evaluators.aggregate import compute_bsi_from_experiment_dir
from harness.loader import load_all_scenarios
from harness.runner import run_scenario


SCENARIOS_ROOT = str(Path(__file__).parent.parent / "scenarios")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _p2_scenarios():
    return [s for s in load_all_scenarios(SCENARIOS_ROOT) if s.pillar.value == "PILLAR2"]


# ---------------------------------------------------------------------------
# compute_bsi_from_experiment_dir — valid results (MockAgent)
# ---------------------------------------------------------------------------

class TestComputeBsiFromExperimentDirValid:
    """BSI computation on a temp experiment dir populated with MockAgent results."""

    @pytest.fixture(scope="class")
    def experiment_dir(self, tmp_path_factory):
        """Build an experiment dir with MockAgent Pillar 2 results."""
        exp = tmp_path_factory.mktemp("exp_p2_valid")
        agent = MockAgent()
        for scenario in _p2_scenarios():
            run_scenario(scenario, agent, output_dir=str(exp))
        return exp

    def test_returns_dict_with_expected_keys(self, experiment_dir):
        result = compute_bsi_from_experiment_dir(experiment_dir)
        assert isinstance(result, dict)
        for key in ("experiment_dir", "generated_at", "total_result_files",
                    "skipped_result_files", "valid_result_files",
                    "agents_evaluated", "per_agent_bsi", "cross_agent_summary"):
            assert key in result, f"Missing key: {key}"

    def test_counts_correct_total_files(self, experiment_dir):
        result = compute_bsi_from_experiment_dir(experiment_dir)
        # 8 Pillar 2 scenarios × 1 agent
        assert result["total_result_files"] == 8

    def test_no_skipped_files_for_mock_agent(self, experiment_dir):
        result = compute_bsi_from_experiment_dir(experiment_dir)
        assert result["skipped_result_files"] == 0
        assert result["valid_result_files"] == 8

    def test_mock_agent_in_agents_evaluated(self, experiment_dir):
        result = compute_bsi_from_experiment_dir(experiment_dir)
        assert "mock-agent-v1" in result["agents_evaluated"]

    def test_per_agent_bsi_has_four_pairs(self, experiment_dir):
        result = compute_bsi_from_experiment_dir(experiment_dir)
        agent_bsi = result["per_agent_bsi"]["mock-agent-v1"]
        # MockAgent runs 4 variant pairs
        assert len(agent_bsi["pair_bsi_results"]) == 4

    def test_mock_agent_bsi_is_zero_for_all_pairs(self, experiment_dir):
        """MockAgent always picks optimal → decision never changes → BSI = 0."""
        result = compute_bsi_from_experiment_dir(experiment_dir)
        agent_bsi = result["per_agent_bsi"]["mock-agent-v1"]
        for pair in agent_bsi["pair_bsi_results"]:
            assert pair["bias_susceptibility_index"] == 0.0
            assert pair["decision_changed"] is False

    def test_cross_agent_summary_has_four_pairs(self, experiment_dir):
        result = compute_bsi_from_experiment_dir(experiment_dir)
        summary = result["cross_agent_summary"]
        assert summary["total_pairs"] == 4

    def test_cross_agent_mean_bsi_is_zero(self, experiment_dir):
        result = compute_bsi_from_experiment_dir(experiment_dir)
        assert result["cross_agent_summary"]["mean_bsi"] == 0.0


# ---------------------------------------------------------------------------
# compute_bsi_from_experiment_dir — all skipped sentinels
# ---------------------------------------------------------------------------

class TestComputeBsiFromExperimentDirAllSkipped:
    """BSI computation when every result file is a status=skipped sentinel."""

    @pytest.fixture(scope="class")
    def experiment_dir(self, tmp_path_factory):
        exp = tmp_path_factory.mktemp("exp_p2_skipped")
        _write_skipped_results("claude-code-baseline", _p2_scenarios(), str(exp))
        _write_skipped_results("codex-baseline", _p2_scenarios(), str(exp))
        return exp

    def test_skipped_count_matches_files(self, experiment_dir):
        result = compute_bsi_from_experiment_dir(experiment_dir)
        # 2 agents × 8 scenarios = 16 files, all skipped
        assert result["total_result_files"] == 16
        assert result["skipped_result_files"] == 16
        assert result["valid_result_files"] == 0

    def test_no_agents_evaluated(self, experiment_dir):
        result = compute_bsi_from_experiment_dir(experiment_dir)
        assert result["agents_evaluated"] == []

    def test_agents_skipped_lists_agent_dirs(self, experiment_dir):
        result = compute_bsi_from_experiment_dir(experiment_dir)
        assert set(result["agents_skipped"]) == {"claude-code-baseline", "codex-baseline"}

    def test_cross_agent_summary_is_empty(self, experiment_dir):
        result = compute_bsi_from_experiment_dir(experiment_dir)
        summary = result["cross_agent_summary"]
        assert summary["total_pairs"] == 0
        assert summary["mean_bsi"] == 0.0


# ---------------------------------------------------------------------------
# compute_bsi_from_experiment_dir — mixed valid + skipped
# ---------------------------------------------------------------------------

class TestComputeBsiFromExperimentDirMixed:
    @pytest.fixture(scope="class")
    def experiment_dir(self, tmp_path_factory):
        exp = tmp_path_factory.mktemp("exp_p2_mixed")
        # MockAgent provides real results
        agent = MockAgent()
        for scenario in _p2_scenarios():
            run_scenario(scenario, agent, output_dir=str(exp))
        # Another agent is skipped
        _write_skipped_results("codex-baseline", _p2_scenarios(), str(exp))
        return exp

    def test_correct_valid_and_skipped_counts(self, experiment_dir):
        result = compute_bsi_from_experiment_dir(experiment_dir)
        assert result["valid_result_files"] == 8
        assert result["skipped_result_files"] == 8

    def test_only_mock_agent_in_evaluated(self, experiment_dir):
        result = compute_bsi_from_experiment_dir(experiment_dir)
        assert "mock-agent-v1" in result["agents_evaluated"]
        assert "codex-baseline" not in result["agents_evaluated"]
        assert "codex-baseline" in result["agents_skipped"]


# ---------------------------------------------------------------------------
# `run --pillar 2` integration: writes bias-susceptibility-summary.json
# ---------------------------------------------------------------------------

class TestRunPillar2WritesBsiSummary:
    def test_bsi_summary_written_for_mock_agent(self, tmp_path):
        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["run", "--agent", "mock-agent-v1", "--pillar", "2",
             "--output-dir", str(tmp_path)],
        )
        assert result.exit_code == 0, f"Non-zero exit:\n{result.output}"

        bsi_path = tmp_path / "bias-susceptibility-summary.json"
        assert bsi_path.exists(), "bias-susceptibility-summary.json not created"

        data = json.loads(bsi_path.read_text())
        assert data["valid_result_files"] == 8
        assert data["cross_agent_summary"]["total_pairs"] == 4

    def test_bsi_summary_written_after_all_skipped(self, tmp_path):
        """BSI summary is also written (with zero valid results) when all agents are skipped."""
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
                ["run", "--agent", "all", "--pillar", "2",
                 "--output-dir", str(tmp_path)],
            )

        assert result.exit_code == 0, f"Non-zero exit:\n{result.output}"

        bsi_path = tmp_path / "bias-susceptibility-summary.json"
        assert bsi_path.exists(), "bias-susceptibility-summary.json not created"

        data = json.loads(bsi_path.read_text())
        assert data["skipped_result_files"] > 0
        assert data["valid_result_files"] == 0

    def test_run_pillar2_produces_8_result_files(self, tmp_path):
        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["run", "--agent", "mock-agent-v1", "--pillar", "2",
             "--output-dir", str(tmp_path)],
        )
        assert result.exit_code == 0, f"Non-zero exit:\n{result.output}"

        agent_dir = tmp_path / "mock-agent-v1"
        assert agent_dir.is_dir()
        result_files = list(agent_dir.glob("*.json"))
        assert len(result_files) == 8

    def test_no_bsi_summary_for_pillar1_run(self, tmp_path):
        """BSI summary should NOT be written for non-Pillar-2 runs."""
        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["run", "--agent", "mock-agent-v1", "--pillar", "1",
             "--output-dir", str(tmp_path)],
        )
        assert result.exit_code == 0, f"Non-zero exit:\n{result.output}"

        bsi_path = tmp_path / "bias-susceptibility-summary.json"
        assert not bsi_path.exists(), "BSI summary should not be created for Pillar 1 runs"
