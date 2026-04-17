"""Tests for --agent all support, output_dir propagation, and skipped-agent handling.

Covers:
- run_scenario() respects explicit output_dir
- _write_skipped_results() writes correct JSON sentinel files
- `run --agent all` with no available agents writes status=skipped for all
- `run --agent all` with available agent runs normally and writes real results
- `run --agent <id>` still works single-agent (regression)
- Multi-run support: --n-runs N, run_index field, file naming
- Session independence: each run is a fresh independent call with unique run_id
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

    def test_run_ids_are_unique_across_runs(self, tmp_path):
        """Each run must produce a distinct run_id (content-addressable; different seed → different hash)."""
        from agents.mock import MockAgent
        from harness.loader import load_all_scenarios
        from harness.runner import run_scenario

        scenarios_root = Path(__file__).parent.parent / "scenarios"
        scenarios = load_all_scenarios(str(scenarios_root))
        agent = MockAgent()

        run_ids = []
        for run_idx in range(5):
            result = run_scenario(scenarios[0], agent, output_dir=str(tmp_path), run_index=run_idx)
            run_ids.append(result.run_id)

        assert len(set(run_ids)) == 5, "All 5 independent runs must have distinct run_ids"

    def test_agent_respond_called_n_times_for_n_runs(self, tmp_path):
        """run_scenario() must invoke agent.respond() exactly once per call; N runs = N respond() calls."""
        from agents.mock import MockAgent
        from harness.loader import load_all_scenarios
        from harness.runner import run_scenario

        scenarios_root = Path(__file__).parent.parent / "scenarios"
        scenarios = load_all_scenarios(str(scenarios_root))
        agent = MockAgent()

        call_count = 0
        original_respond = agent.respond

        def counting_respond(scenario):
            nonlocal call_count
            call_count += 1
            return original_respond(scenario)

        agent.respond = counting_respond

        for run_idx in range(3):
            run_scenario(scenarios[0], agent, output_dir=str(tmp_path), run_index=run_idx)

        assert call_count == 3, f"Expected 3 respond() calls for 3 runs, got {call_count}"

    def test_runs_have_different_supplier_orderings(self, tmp_path):
        """Sequential runs must present suppliers in different orders (different seed → different shuffle)."""
        from agents.mock import MockAgent
        from harness.loader import load_all_scenarios
        from harness.runner import run_scenario, _shuffle_context

        scenarios_root = Path(__file__).parent.parent / "scenarios"
        all_scenarios = load_all_scenarios(str(scenarios_root))
        p2 = [s for s in all_scenarios if "p2" in s.id]
        scenario = p2[0] if p2 else all_scenarios[0]

        agent = MockAgent()
        seeds = []
        for run_idx in range(5):
            result = run_scenario(scenario, agent, output_dir=str(tmp_path), run_index=run_idx)
            seeds.append(result.supplier_order_seed)

        assert len(set(seeds)) > 1, "Independent runs must use different supplier ordering seeds"

    def test_same_explicit_seed_produces_same_run_id(self, tmp_path):
        """Reproducibility: identical (run_index, seed) inputs → identical run_id (deterministic hash)."""
        from agents.mock import MockAgent
        from harness.loader import load_all_scenarios
        from harness.runner import run_scenario

        scenarios_root = Path(__file__).parent.parent / "scenarios"
        scenarios = load_all_scenarios(str(scenarios_root))
        agent = MockAgent()

        r1 = run_scenario(scenarios[0], agent, output_dir=str(tmp_path),
                          run_index=0, supplier_order_seed=99999)
        # Need separate output path to avoid filename collision
        import shutil
        tmp2 = tmp_path / "replay"
        tmp2.mkdir()
        r2 = run_scenario(scenarios[0], agent, output_dir=str(tmp2),
                          run_index=0, supplier_order_seed=99999)

        assert r1.run_id == r2.run_id, "Same inputs must produce the same run_id (reproducibility)"


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


# ---------------------------------------------------------------------------
# Research mode: temperature=0.0 robustness pass (UPGRADE-6)
# ---------------------------------------------------------------------------

class TestResearchMode:
    """--research-mode flag adds a mandatory T=0.0 robustness pass."""

    def test_research_mode_creates_robustness_t0_dir(self, tmp_path):
        """--research-mode must create a robustness-t0/ subdirectory."""
        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["run", "--agent", "mock-agent-v1", "--pillar", "1",
             "--research-mode", "--output-dir", str(tmp_path)],
        )
        assert result.exit_code == 0, f"Non-zero exit:\n{result.output}"
        assert (tmp_path / "robustness-t0").is_dir(), (
            "robustness-t0/ directory was not created"
        )

    def test_robustness_dir_contains_same_scenario_count(self, tmp_path):
        """robustness-t0/<agent>/ must have the same number of result files as primary."""
        runner = CliRunner()
        runner.invoke(
            cli,
            ["run", "--agent", "mock-agent-v1", "--pillar", "1",
             "--research-mode", "--output-dir", str(tmp_path)],
        )

        primary_files = list((tmp_path / "mock-agent-v1").glob("*.json"))
        robustness_files = list(
            (tmp_path / "robustness-t0" / "mock-agent-v1").glob("*.json")
        )
        # 6 pillar-1 scenarios × 1 run each in both passes
        assert len(primary_files) == 6
        assert len(robustness_files) == 6

    def test_robustness_results_are_independent_json_files(self, tmp_path):
        """robustness-t0/ result files must be valid JSON with agent_id and scenario_id."""
        runner = CliRunner()
        runner.invoke(
            cli,
            ["run", "--agent", "mock-agent-v1", "--pillar", "1",
             "--research-mode", "--output-dir", str(tmp_path)],
        )

        rob_agent_dir = tmp_path / "robustness-t0" / "mock-agent-v1"
        assert rob_agent_dir.is_dir()
        for f in rob_agent_dir.glob("*.json"):
            data = json.loads(f.read_text())
            assert "agent_id" in data
            assert "scenario_id" in data

    def test_research_mode_output_mentions_robustness(self, tmp_path):
        """CLI output must include a 'Robustness' banner when --research-mode is set."""
        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["run", "--agent", "mock-agent-v1", "--pillar", "1",
             "--research-mode", "--output-dir", str(tmp_path)],
        )
        assert result.exit_code == 0, f"Non-zero exit:\n{result.output}"
        assert "Robustness" in result.output

    def test_without_research_mode_no_robustness_dir(self, tmp_path):
        """Without --research-mode, robustness-t0/ must NOT be created."""
        runner = CliRunner()
        runner.invoke(
            cli,
            ["run", "--agent", "mock-agent-v1", "--pillar", "1",
             "--output-dir", str(tmp_path)],
        )
        assert not (tmp_path / "robustness-t0").exists(), (
            "robustness-t0/ should not be created when --research-mode is not set"
        )

    def test_research_mode_with_n_runs(self, tmp_path):
        """--research-mode with --n-runs 2 must write 2 files per scenario in robustness-t0/."""
        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["run", "--agent", "mock-agent-v1", "--pillar", "1",
             "--research-mode", "--n-runs", "2", "--output-dir", str(tmp_path)],
        )
        assert result.exit_code == 0, f"Non-zero exit:\n{result.output}"

        rob_agent_dir = tmp_path / "robustness-t0" / "mock-agent-v1"
        rob_files = sorted(rob_agent_dir.glob("*.json"))
        # 6 pillar-1 scenarios × 2 runs = 12 files in robustness-t0/
        assert len(rob_files) == 12, (
            f"Expected 12 files in robustness-t0/, got {len(rob_files)}"
        )

    def test_bsi_comparison_helper_stable_signal(self):
        """_print_robustness_bsi_comparison must identify stable BSI as non-collapsed."""
        from buyerbench.__main__ import _print_robustness_bsi_comparison
        from buyerbench.models import EvaluationResult, PillarScore
        from rich.console import Console

        def _make_result(bsi_value: float):
            """Minimal EvaluationResult with one PillarScore containing a BSI."""
            from buyerbench.models import Pillar, ScenarioVariant
            ps = PillarScore(pillar=Pillar.PILLAR2, score=0.5, metrics={"bias_susceptibility_index": bsi_value})
            return EvaluationResult(
                agent_id="mock", scenario_id="p2-01-baseline",
                pillar_scores=[ps], overall_pass=True,
            )

        primary = [_make_result(0.40)] * 5   # strong primary BSI
        robust = [_make_result(0.38)] * 5    # T=0.0 BSI stays high → stable

        buf = Console(record=True)
        _print_robustness_bsi_comparison(primary, robust, buf)
        output = buf.export_text()
        assert "stable" in output.lower() or "✓" in output

    def test_bsi_comparison_helper_collapse_detection(self):
        """_print_robustness_bsi_comparison must warn when BSI collapses at T=0.0."""
        from buyerbench.__main__ import _print_robustness_bsi_comparison
        from buyerbench.models import EvaluationResult, PillarScore, Pillar
        from rich.console import Console

        def _make_result(bsi_value: float):
            ps = PillarScore(pillar=Pillar.PILLAR2, score=0.5, metrics={"bias_susceptibility_index": bsi_value})
            return EvaluationResult(
                agent_id="mock", scenario_id="p2-01-baseline",
                pillar_scores=[ps], overall_pass=True,
            )

        primary = [_make_result(0.50)] * 5   # high primary BSI
        robust = [_make_result(0.01)] * 5    # collapses at T=0.0

        buf = Console(record=True)
        _print_robustness_bsi_comparison(primary, robust, buf)
        output = buf.export_text()
        assert "COLLAPSE" in output.upper() or "collapse" in output.lower()


# ---------------------------------------------------------------------------
# UPGRADE-2: derive_seed() unit tests
# ---------------------------------------------------------------------------

class TestDeriveSeed:
    """harness.runner.derive_seed() must be deterministic, distinct across cell
    dimensions, and produce values in [0, 2**31)."""

    def _ds(self, base=42, sid="p2-01", variant=None, run_index=0):
        from harness.runner import derive_seed
        return derive_seed(base, sid, variant, run_index)

    def test_deterministic_same_inputs(self):
        """Same inputs must always produce the same seed."""
        assert self._ds() == self._ds()

    def test_different_run_indices(self):
        """run_index 0 and 1 must yield different seeds."""
        assert self._ds(run_index=0) != self._ds(run_index=1)

    def test_different_scenario_ids(self):
        """Different scenario_ids must yield different seeds."""
        assert self._ds(sid="p2-01") != self._ds(sid="p2-02")

    def test_different_variants(self):
        """BASELINE variant and FRAMING_GAIN must yield different seeds."""
        assert self._ds(variant=None) != self._ds(variant="FRAMING_GAIN")

    def test_different_base_seeds(self):
        """Different base seeds must yield different derived seeds."""
        assert self._ds(base=1) != self._ds(base=2)

    def test_output_in_positive_int31_range(self):
        """Result must be in [0, 2**31)."""
        seed = self._ds()
        assert 0 <= seed < 2**31

    def test_none_variant_equivalent_to_empty_string_in_message(self):
        """None variant is treated as empty string — calling twice with None is consistent."""
        from harness.runner import derive_seed
        assert derive_seed(99, "p2-03", None, 0) == derive_seed(99, "p2-03", None, 0)

    def test_output_is_int(self):
        """Return type must be int."""
        assert isinstance(self._ds(), int)

    def test_all_five_dimensions_are_independent(self):
        """Changing any single input dimension changes the output seed."""
        from harness.runner import derive_seed
        base = derive_seed(10, "p2-01", "BASELINE", 0)
        assert base != derive_seed(11, "p2-01", "BASELINE", 0)   # base seed change
        assert base != derive_seed(10, "p2-02", "BASELINE", 0)   # scenario_id change
        assert base != derive_seed(10, "p2-01", "FRAMING_GAIN", 0)  # variant change
        assert base != derive_seed(10, "p2-01", "BASELINE", 1)   # run_index change


# ---------------------------------------------------------------------------
# UPGRADE-2: CLI flags --supplier-order-seed and --supplier-order-static
# ---------------------------------------------------------------------------

class TestUpgrade2CLIFlags:
    """CLI must accept --supplier-order-seed and --supplier-order-static flags."""

    def test_supplier_order_seed_flag_is_accepted(self, tmp_path):
        """--supplier-order-seed must be accepted without error."""
        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["run", "--agent", "mock-agent-v1", "--pillar", "1",
             "--supplier-order-seed", "42", "--output-dir", str(tmp_path)],
        )
        assert result.exit_code == 0, f"CLI rejected --supplier-order-seed:\n{result.output}"

    def test_supplier_order_static_flag_is_accepted(self, tmp_path):
        """--supplier-order-static must be accepted without error."""
        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["run", "--agent", "mock-agent-v1", "--pillar", "1",
             "--supplier-order-static", "--output-dir", str(tmp_path)],
        )
        assert result.exit_code == 0, f"CLI rejected --supplier-order-static:\n{result.output}"

    def test_base_seed_produces_reproducible_run_ids(self, tmp_path):
        """Two runs with the same --supplier-order-seed must produce the same run_id for each scenario."""
        from agents.mock import MockAgent
        from harness.loader import load_all_scenarios
        from harness.runner import run_scenario, derive_seed

        scenarios_root = Path(__file__).parent.parent / "scenarios"
        scenarios = [s for s in load_all_scenarios(str(scenarios_root)) if "p2" in s.id][:2]
        agent = MockAgent()

        def collect_run_ids(base_seed, out_dir):
            ids = []
            for s in scenarios:
                ps = derive_seed(base_seed, s.id, s.variant, 0)
                r = run_scenario(s, agent, output_dir=str(out_dir),
                                 run_index=0, supplier_order_seed=ps)
                ids.append(r.run_id)
            return ids

        ids_a = collect_run_ids(12345, tmp_path / "run_a")
        ids_b = collect_run_ids(12345, tmp_path / "run_b")
        assert ids_a == ids_b, "Same base seed must produce identical run_ids"

    def test_different_base_seeds_produce_different_run_ids(self, tmp_path):
        """Different --supplier-order-seed values must yield different run_ids."""
        from agents.mock import MockAgent
        from harness.loader import load_all_scenarios
        from harness.runner import run_scenario, derive_seed

        scenarios_root = Path(__file__).parent.parent / "scenarios"
        scenario = [s for s in load_all_scenarios(str(scenarios_root)) if "p2" in s.id][0]
        agent = MockAgent()

        r1 = run_scenario(scenario, agent, output_dir=str(tmp_path / "a"),
                          run_index=0, supplier_order_seed=derive_seed(100, scenario.id, scenario.variant, 0))
        r2 = run_scenario(scenario, agent, output_dir=str(tmp_path / "b"),
                          run_index=0, supplier_order_seed=derive_seed(200, scenario.id, scenario.variant, 0))
        assert r1.run_id != r2.run_id, "Different base seeds must produce different run_ids"

    def test_static_mode_stores_none_seed(self, tmp_path):
        """--supplier-order-static: result.supplier_order_seed must be None."""
        from agents.mock import MockAgent
        from harness.loader import load_all_scenarios
        from harness.runner import run_scenario

        scenarios_root = Path(__file__).parent.parent / "scenarios"
        scenario = load_all_scenarios(str(scenarios_root))[0]
        agent = MockAgent()

        result = run_scenario(scenario, agent, output_dir=str(tmp_path),
                              supplier_order_static=True)
        assert result.supplier_order_seed is None

    def test_static_mode_run_id_contains_static_component(self, tmp_path):
        """Static-mode run_id must differ from any seeded run_id for the same scenario."""
        from agents.mock import MockAgent
        from harness.loader import load_all_scenarios
        from harness.runner import run_scenario

        scenarios_root = Path(__file__).parent.parent / "scenarios"
        scenario = load_all_scenarios(str(scenarios_root))[0]
        agent = MockAgent()

        static_result = run_scenario(scenario, agent, output_dir=str(tmp_path / "static"),
                                     run_index=0, supplier_order_static=True)
        seeded_result = run_scenario(scenario, agent, output_dir=str(tmp_path / "seeded"),
                                     run_index=0, supplier_order_seed=42)
        assert static_result.run_id != seeded_result.run_id

    def test_static_overrides_seed_when_both_supplied(self, tmp_path):
        """supplier_order_static=True must override supplier_order_seed; result seed must be None."""
        from agents.mock import MockAgent
        from harness.loader import load_all_scenarios
        from harness.runner import run_scenario

        scenarios_root = Path(__file__).parent.parent / "scenarios"
        scenario = load_all_scenarios(str(scenarios_root))[0]
        agent = MockAgent()

        result = run_scenario(scenario, agent, output_dir=str(tmp_path),
                              supplier_order_seed=99, supplier_order_static=True)
        assert result.supplier_order_seed is None
