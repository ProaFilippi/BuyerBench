"""Tests for --agent all support, output_dir propagation, and skipped-agent handling.

Covers:
- run_scenario() respects explicit output_dir
- _write_skipped_results() writes correct JSON sentinel files
- `run --agent all` with no available agents writes status=skipped for all
- `run --agent all` with available agent runs normally and writes real results
- `run --agent <id>` still works single-agent (regression)
"""
from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

from buyerbench.__main__ import _write_skipped_results, cli


# ---------------------------------------------------------------------------
# run_scenario — output_dir parameter
# ---------------------------------------------------------------------------

class TestRunScenarioOutputDir:
    def test_saves_to_custom_output_dir(self, tmp_path):
        from agents.mock import MockAgent
        from harness.loader import load_all_scenarios
        from harness.runner import run_scenario

        scenarios_root = Path(__file__).parent.parent / "scenarios"
        scenarios = load_all_scenarios(str(scenarios_root))
        assert scenarios, "Need at least one scenario"

        agent = MockAgent()
        result = run_scenario(scenarios[0], agent, output_dir=str(tmp_path))

        expected = tmp_path / agent.agent_id / f"{scenarios[0].id}.json"
        assert expected.exists(), f"Expected result file not found: {expected}"

        data = json.loads(expected.read_text())
        assert data["scenario_id"] == scenarios[0].id
        assert data["agent_id"] == agent.agent_id

    def test_legacy_none_output_dir_saves_to_results(self, tmp_path, monkeypatch):
        """When output_dir=None, falls back to 'results/<agent_id>/'."""
        from agents.mock import MockAgent
        from harness.loader import load_all_scenarios
        from harness.runner import run_scenario

        # Redirect cwd so we don't pollute repo root
        monkeypatch.chdir(tmp_path)

        scenarios_root = Path(__file__).parent.parent / "scenarios"
        scenarios = load_all_scenarios(str(scenarios_root))
        agent = MockAgent()

        run_scenario(scenarios[0], agent, output_dir=None)

        expected = tmp_path / "results" / agent.agent_id / f"{scenarios[0].id}.json"
        assert expected.exists()


# ---------------------------------------------------------------------------
# _write_skipped_results
# ---------------------------------------------------------------------------

class TestWriteSkippedResults:
    def test_creates_one_file_per_scenario(self, tmp_path):
        from harness.loader import load_all_scenarios

        scenarios_root = Path(__file__).parent.parent / "scenarios"
        scenarios = load_all_scenarios(str(scenarios_root))

        _write_skipped_results("test-agent", scenarios, str(tmp_path))

        agent_dir = tmp_path / "test-agent"
        assert agent_dir.is_dir()
        written = list(agent_dir.glob("*.json"))
        assert len(written) == len(scenarios)

    def test_skipped_file_has_correct_fields(self, tmp_path):
        from harness.loader import load_all_scenarios

        scenarios_root = Path(__file__).parent.parent / "scenarios"
        scenarios = load_all_scenarios(str(scenarios_root))[:1]

        _write_skipped_results("my-agent", scenarios, str(tmp_path))

        path = tmp_path / "my-agent" / f"{scenarios[0].id}.json"
        data = json.loads(path.read_text())

        assert data["status"] == "skipped"
        assert data["agent_id"] == "my-agent"
        assert data["scenario_id"] == scenarios[0].id
        assert "reason" in data
        assert "timestamp" in data


# ---------------------------------------------------------------------------
# `run --agent all` CLI integration
# ---------------------------------------------------------------------------

class TestRunAllAgents:
    def test_all_skipped_when_no_api_keys(self, tmp_path):
        """When preflight reports no available agents, all 9 real agents get skipped."""
        runner = CliRunner()

        no_agents_env = {
            "clis": {
                "claude": {"installed": True, "version": "2.0.0", "error": None},
                "codex": {"installed": True, "version": "0.1.0", "error": None},
                "gemini": {"installed": True, "version": "0.1.0", "error": None},
            },
            "api_keys": {
                "Claude (ANTHROPIC_API_KEY)": {"set": False, "key_name": None},
                "Codex (OPENAI_API_KEY)": {"set": False, "key_name": None},
                "Gemini (GOOGLE_API_KEY / GEMINI_API_KEY)": {"set": False, "key_name": None},
            },
            "mcp_server": {"started": True, "error": None},
            "overall": False,
            "available_agents": [],
        }

        with patch("harness.preflight.check_environment", return_value=no_agents_env):
            result = runner.invoke(
                cli,
                ["run", "--agent", "all", "--pillar", "1",
                 "--output-dir", str(tmp_path)],
            )

        assert result.exit_code == 0, f"Unexpected exit:\n{result.output}"
        assert "SKIPPED" in result.output

        # All 9 real agents should have directories
        from agents.registry import AGENT_REGISTRY
        real_agents = [aid for aid in AGENT_REGISTRY if aid != "mock-agent-v1"]
        for aid in real_agents:
            agent_dir = tmp_path / aid
            assert agent_dir.is_dir(), f"No output dir for skipped agent {aid}"
            # Should have one skipped file per pillar-1 scenario (5 scenarios)
            skipped_files = list(agent_dir.glob("*.json"))
            assert len(skipped_files) == 5, (
                f"Expected 5 skipped files for {aid}, got {len(skipped_files)}"
            )
            for f in skipped_files:
                data = json.loads(f.read_text())
                assert data["status"] == "skipped"
                assert data["agent_id"] == aid

    def test_run_completes_with_summary_message(self, tmp_path):
        """Completion message mentions scenario count × agent count."""
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
                ["run", "--agent", "all", "--pillar", "1",
                 "--output-dir", str(tmp_path)],
            )

        assert "Run complete" in result.output
        assert "scenario" in result.output.lower()

    def test_single_agent_still_works(self, tmp_path):
        """Regression: running a single named agent still writes results correctly."""
        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["run", "--agent", "mock-agent-v1", "--pillar", "1",
             "--output-dir", str(tmp_path)],
        )
        assert result.exit_code == 0, f"Non-zero exit:\n{result.output}"
        agent_dir = tmp_path / "mock-agent-v1"
        assert agent_dir.is_dir()
        result_files = list(agent_dir.glob("*.json"))
        assert len(result_files) == 5  # 5 pillar-1 scenarios
        for f in result_files:
            data = json.loads(f.read_text())
            assert "scenario_id" in data
            assert "overall_pass" in data
