"""Tests for --agent all support, output_dir propagation, and skipped-agent handling.

Covers:
- run_scenario() respects explicit output_dir
- _write_skipped_results() writes correct JSON sentinel files
- `run --agent all` with no available agents writes status=skipped for all
- `run --agent all` with available agent runs normally and writes real results
- `run --agent <id>` still works single-agent (regression)
- Multi-run support: --n-runs N, run_index field, file naming
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

        expected = tmp_path / agent.agent_id / f"{scenarios[0].id}-run000.json"
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

        expected = tmp_path / "results" / agent.agent_id / f"{scenarios[0].id}-run000.json"
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
            # Should have one skipped file per pillar-1 scenario (6 scenarios)
            skipped_files = list(agent_dir.glob("*.json"))
            assert len(skipped_files) == 6, (
                f"Expected 6 skipped files for {aid}, got {len(skipped_files)}"
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
        assert len(result_files) == 6  # 6 pillar-1 scenarios
        for f in result_files:
            data = json.loads(f.read_text())
            assert "scenario_id" in data
            assert "overall_pass" in data


# ---------------------------------------------------------------------------
# Multi-run support (UPGRADE-1)
# ---------------------------------------------------------------------------

class TestMultiRunSupport:
    def test_run_index_stored_on_result(self, tmp_path):
        """run_scenario() must store run_index on the returned EvaluationResult."""
        from agents.mock import MockAgent
        from harness.loader import load_all_scenarios
        from harness.runner import run_scenario

        scenarios_root = Path(__file__).parent.parent / "scenarios"
        scenarios = load_all_scenarios(str(scenarios_root))
        agent = MockAgent()

        result_0 = run_scenario(scenarios[0], agent, output_dir=str(tmp_path), run_index=0)
        result_3 = run_scenario(scenarios[0], agent, output_dir=str(tmp_path), run_index=3)

        assert result_0.run_index == 0
        assert result_3.run_index == 3

    def test_file_named_with_run_index(self, tmp_path):
        """Output file must be <scenario_id>-run<NNN>.json."""
        from agents.mock import MockAgent
        from harness.loader import load_all_scenarios
        from harness.runner import run_scenario

        scenarios_root = Path(__file__).parent.parent / "scenarios"
        scenarios = load_all_scenarios(str(scenarios_root))
        agent = MockAgent()

        run_scenario(scenarios[0], agent, output_dir=str(tmp_path), run_index=0)
        run_scenario(scenarios[0], agent, output_dir=str(tmp_path), run_index=1)

        agent_dir = tmp_path / agent.agent_id
        expected_0 = agent_dir / f"{scenarios[0].id}-run000.json"
        expected_1 = agent_dir / f"{scenarios[0].id}-run001.json"

        assert expected_0.exists(), f"run000 file missing: {expected_0}"
        assert expected_1.exists(), f"run001 file missing: {expected_1}"

    def test_run_index_persisted_in_json(self, tmp_path):
        """run_index must be serialised into the JSON result file."""
        from agents.mock import MockAgent
        from harness.loader import load_all_scenarios
        from harness.runner import run_scenario

        scenarios_root = Path(__file__).parent.parent / "scenarios"
        scenarios = load_all_scenarios(str(scenarios_root))
        agent = MockAgent()

        run_scenario(scenarios[0], agent, output_dir=str(tmp_path), run_index=7)

        json_file = tmp_path / agent.agent_id / f"{scenarios[0].id}-run007.json"
        data = json.loads(json_file.read_text())
        assert data["run_index"] == 7

    def test_n_runs_cli_flag(self, tmp_path):
        """--n-runs 3 must produce 3 result files per scenario."""
        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["run", "--agent", "mock-agent-v1", "--pillar", "1",
             "--n-runs", "3", "--output-dir", str(tmp_path)],
        )
        assert result.exit_code == 0, f"Non-zero exit:\n{result.output}"

        agent_dir = tmp_path / "mock-agent-v1"
        assert agent_dir.is_dir()
        result_files = sorted(agent_dir.glob("*.json"))
        # 6 pillar-1 scenarios × 3 runs = 18 files
        assert len(result_files) == 18, f"Expected 18 files, got {len(result_files)}"

    def test_n_runs_run_index_sequential(self, tmp_path):
        """With --n-runs 3, run indices stored in JSON files must be 0, 1, 2."""
        runner = CliRunner()
        runner.invoke(
            cli,
            ["run", "--agent", "mock-agent-v1", "--pillar", "1",
             "--n-runs", "3", "--output-dir", str(tmp_path)],
        )

        agent_dir = tmp_path / "mock-agent-v1"
        # Collect all unique run_index values across result files
        run_indices: set[int] = set()
        for f in agent_dir.glob("*.json"):
            data = json.loads(f.read_text())
            if "run_index" in data:
                run_indices.add(data["run_index"])

        assert run_indices == {0, 1, 2}

    def test_default_n_runs_is_one(self, tmp_path):
        """Without --n-runs, behaviour is identical to N=1 (backward compat)."""
        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["run", "--agent", "mock-agent-v1", "--pillar", "1",
             "--output-dir", str(tmp_path)],
        )
        assert result.exit_code == 0

        agent_dir = tmp_path / "mock-agent-v1"
        result_files = list(agent_dir.glob("*.json"))
        assert len(result_files) == 6  # 6 pillar-1 scenarios × 1 run


# ---------------------------------------------------------------------------
# Supplier order randomisation (UPGRADE-2)
# ---------------------------------------------------------------------------

class TestSupplierOrderRandomisation:
    """run_scenario() must generate and persist a supplier_order_seed per run."""

    def _scenario_with_suppliers(self):
        from harness.loader import load_all_scenarios
        scenarios_root = Path(__file__).parent.parent / "scenarios"
        scenarios = load_all_scenarios(str(scenarios_root))
        # Any scenario with a list-of-dicts in context is fine; use first Pillar 2
        p2 = [s for s in scenarios if "p2" in s.id]
        return p2[0] if p2 else scenarios[0]

    def test_seed_stored_on_result(self, tmp_path):
        """run_scenario() must store a non-None supplier_order_seed on result."""
        from agents.mock import MockAgent
        from harness.runner import run_scenario

        scenario = self._scenario_with_suppliers()
        agent = MockAgent()
        result = run_scenario(scenario, agent, output_dir=str(tmp_path))
        assert result.supplier_order_seed is not None
        assert isinstance(result.supplier_order_seed, int)

    def test_seed_persisted_in_json(self, tmp_path):
        """supplier_order_seed must be serialised into the JSON result file."""
        from agents.mock import MockAgent
        from harness.runner import run_scenario

        scenario = self._scenario_with_suppliers()
        agent = MockAgent()
        run_scenario(scenario, agent, output_dir=str(tmp_path), run_index=0)

        json_file = tmp_path / agent.agent_id / f"{scenario.id}-run000.json"
        data = json.loads(json_file.read_text())
        assert "supplier_order_seed" in data
        assert data["supplier_order_seed"] is not None

    def test_explicit_seed_used_when_provided(self, tmp_path):
        """When supplier_order_seed is passed, that exact value must be stored."""
        from agents.mock import MockAgent
        from harness.runner import run_scenario

        scenario = self._scenario_with_suppliers()
        agent = MockAgent()
        result = run_scenario(scenario, agent, output_dir=str(tmp_path),
                              supplier_order_seed=12345)
        assert result.supplier_order_seed == 12345

    def test_different_seeds_generated_per_run(self, tmp_path):
        """Sequential runs without an explicit seed must produce different seeds."""
        from agents.mock import MockAgent
        from harness.runner import run_scenario

        scenario = self._scenario_with_suppliers()
        agent = MockAgent()
        seeds = set()
        for run_idx in range(5):
            result = run_scenario(scenario, agent, output_dir=str(tmp_path),
                                  run_index=run_idx)
            seeds.add(result.supplier_order_seed)
        # With 5 runs across a 2^31 space, collisions are astronomically unlikely
        assert len(seeds) > 1, "Expected distinct seeds across independent runs"

    def test_original_scenario_context_not_mutated(self, tmp_path):
        """run_scenario() must not mutate the original scenario's context."""
        from agents.mock import MockAgent
        from harness.runner import run_scenario

        scenario = self._scenario_with_suppliers()
        # Capture original context by value
        import copy
        original_context = copy.deepcopy(scenario.context)

        agent = MockAgent()
        run_scenario(scenario, agent, output_dir=str(tmp_path))

        assert scenario.context == original_context
