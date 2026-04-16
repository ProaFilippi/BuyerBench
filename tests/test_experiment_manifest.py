"""Tests for UPGRADE-11: ExperimentManifest pre-run/post-run frozen config record."""
from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from results.experiment_manifest import (
    ExperimentManifest,
    _get_git_commit_hash,
    _infer_bias_counts,
    create_manifest,
    finalize_manifest,
    write_manifest,
)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _utc(s: str = "2026-04-16T10:00:00+00:00") -> datetime:
    return datetime.fromisoformat(s)


def _make_manifest(**kwargs) -> ExperimentManifest:
    defaults = dict(
        experiment_id="session-20260416-100000",
        n_models=2,
        n_scenarios=4,
        n_runs_per_cell=3,
        temperatures=[0.7],
        prompt_versions=["standard"],
        total_planned_runs=24,
        start_time_utc="2026-04-16T10:00:00+00:00",
        pillars=[2],
        output_dir="/tmp/test-run",
    )
    defaults.update(kwargs)
    return ExperimentManifest(**defaults)


# ── _get_git_commit_hash ──────────────────────────────────────────────────────

class TestGetGitCommitHash:
    def test_returns_string_on_success(self):
        with patch("subprocess.check_output") as mock_co:
            mock_co.side_effect = [b"abc1234\n", b""]  # HEAD hash, clean status
            result = _get_git_commit_hash()
        assert result == "abc1234"

    def test_appends_dirty_when_uncommitted_changes(self):
        with patch("subprocess.check_output") as mock_co:
            mock_co.side_effect = [b"abc1234\n", b" M some/file.py\n"]
            result = _get_git_commit_hash()
        assert result == "abc1234-dirty"

    def test_returns_none_on_subprocess_error(self):
        with patch("subprocess.check_output", side_effect=subprocess.CalledProcessError(1, "git")):
            result = _get_git_commit_hash()
        assert result is None

    def test_returns_none_when_git_not_found(self):
        with patch("subprocess.check_output", side_effect=FileNotFoundError):
            result = _get_git_commit_hash()
        assert result is None

    def test_returns_none_on_oserror(self):
        with patch("subprocess.check_output", side_effect=OSError("no git")):
            result = _get_git_commit_hash()
        assert result is None


# ── _infer_bias_counts ────────────────────────────────────────────────────────

class TestInferBiasCounts:
    def _make_scenario(self, pillar_val: str, pair_id: str | None):
        s = MagicMock()
        from buyerbench.models import Pillar
        s.pillar = Pillar.PILLAR2 if pillar_val == "PILLAR2" else Pillar.PILLAR1
        s.variant_pair_id = pair_id
        return s

    def test_returns_none_none_for_no_pillar2(self):
        scenarios = [self._make_scenario("PILLAR1", "p1-01")]
        assert _infer_bias_counts(scenarios) == (None, None)

    def test_counts_unique_bias_types(self):
        scenarios = [
            self._make_scenario("PILLAR2", "p2-01-anchoring"),
            self._make_scenario("PILLAR2", "p2-01-anchoring"),
            self._make_scenario("PILLAR2", "p2-02-framing"),
            self._make_scenario("PILLAR2", "p2-02-framing"),
        ]
        n_bias, n_variants = _infer_bias_counts(scenarios)
        assert n_bias == 2
        assert n_variants == 2

    def test_warp_triplet_gives_3_variants(self):
        scenarios = [
            self._make_scenario("PILLAR2", "p2-08-warp"),
            self._make_scenario("PILLAR2", "p2-08-warp"),
            self._make_scenario("PILLAR2", "p2-08-warp"),
        ]
        n_bias, n_variants = _infer_bias_counts(scenarios)
        assert n_bias == 1
        assert n_variants == 3

    def test_handles_none_pair_id(self):
        scenarios = [self._make_scenario("PILLAR2", None)]
        n_bias, n_variants = _infer_bias_counts(scenarios)
        assert n_bias is None

    def test_empty_list_returns_none_none(self):
        assert _infer_bias_counts([]) == (None, None)


# ── create_manifest ───────────────────────────────────────────────────────────

class TestCreateManifest:
    def _make_scenario(self, pair_id: str | None = "p2-01-anchoring"):
        from buyerbench.models import Pillar
        s = MagicMock()
        s.pillar = Pillar.PILLAR2
        s.variant_pair_id = pair_id
        return s

    def test_experiment_id_matches_session_id(self):
        m = create_manifest(
            session_id="session-20260416-100000",
            agents=["agent-a"],
            scenarios=[self._make_scenario()],
            n_runs=5,
            temperature=0.7,
            prompt_version="standard",
            pillars=[2],
            research_mode=False,
            output_dir="/tmp/out",
            started_at=_utc(),
        )
        assert m.experiment_id == "session-20260416-100000"

    def test_n_models_reflects_agent_count(self):
        m = create_manifest(
            session_id="s",
            agents=["a", "b", "c"],
            scenarios=[self._make_scenario()],
            n_runs=1,
            temperature=None,
            prompt_version="standard",
            pillars=[2],
            research_mode=False,
            output_dir="/tmp",
            started_at=_utc(),
        )
        assert m.n_models == 3

    def test_total_planned_runs(self):
        scenarios = [self._make_scenario() for _ in range(6)]
        m = create_manifest(
            session_id="s",
            agents=["a", "b"],
            scenarios=scenarios,
            n_runs=5,
            temperature=0.7,
            prompt_version="standard",
            pillars=[2],
            research_mode=False,
            output_dir="/tmp",
            started_at=_utc(),
        )
        # 2 agents × 6 scenarios × 5 runs = 60
        assert m.total_planned_runs == 60

    def test_research_mode_doubles_planned_runs(self):
        scenarios = [self._make_scenario() for _ in range(4)]
        m = create_manifest(
            session_id="s",
            agents=["a"],
            scenarios=scenarios,
            n_runs=3,
            temperature=0.7,
            prompt_version="standard",
            pillars=[2],
            research_mode=True,
            output_dir="/tmp",
            started_at=_utc(),
        )
        # 1 × 4 × 3 × 2 = 24
        assert m.total_planned_runs == 24

    def test_research_mode_adds_zero_temperature(self):
        m = create_manifest(
            session_id="s",
            agents=["a"],
            scenarios=[self._make_scenario()],
            n_runs=1,
            temperature=0.7,
            prompt_version="standard",
            pillars=[2],
            research_mode=True,
            output_dir="/tmp",
            started_at=_utc(),
        )
        assert 0.0 in m.temperatures
        assert 0.7 in m.temperatures

    def test_research_mode_at_t0_does_not_duplicate(self):
        """When temperature is already 0.0, research mode should not add a second 0.0."""
        m = create_manifest(
            session_id="s",
            agents=["a"],
            scenarios=[self._make_scenario()],
            n_runs=1,
            temperature=0.0,
            prompt_version="standard",
            pillars=[2],
            research_mode=True,
            output_dir="/tmp",
            started_at=_utc(),
        )
        assert m.temperatures == [0.0]

    def test_none_temperature_stored_as_none(self):
        m = create_manifest(
            session_id="s",
            agents=["a"],
            scenarios=[self._make_scenario()],
            n_runs=1,
            temperature=None,
            prompt_version="standard",
            pillars=[2],
            research_mode=False,
            output_dir="/tmp",
            started_at=_utc(),
        )
        assert m.temperatures == [None]

    def test_total_completed_runs_starts_at_zero(self):
        m = create_manifest(
            session_id="s",
            agents=["a"],
            scenarios=[self._make_scenario()],
            n_runs=1,
            temperature=0.7,
            prompt_version="standard",
            pillars=[2],
            research_mode=False,
            output_dir="/tmp",
            started_at=_utc(),
        )
        assert m.total_completed_runs == 0

    def test_end_time_utc_starts_as_none(self):
        m = create_manifest(
            session_id="s",
            agents=["a"],
            scenarios=[self._make_scenario()],
            n_runs=1,
            temperature=None,
            prompt_version="standard",
            pillars=[2],
            research_mode=False,
            output_dir="/tmp",
            started_at=_utc(),
        )
        assert m.end_time_utc is None

    def test_start_time_is_iso8601(self):
        t = _utc("2026-04-16T12:34:56+00:00")
        m = create_manifest(
            session_id="s",
            agents=["a"],
            scenarios=[self._make_scenario()],
            n_runs=1,
            temperature=None,
            prompt_version="standard",
            pillars=[1],
            research_mode=False,
            output_dir="/tmp",
            started_at=t,
        )
        assert m.start_time_utc == t.isoformat()

    def test_git_hash_captured(self):
        with patch(
            "results.experiment_manifest._get_git_commit_hash",
            return_value="deadbeef",
        ):
            m = create_manifest(
                session_id="s",
                agents=["a"],
                scenarios=[self._make_scenario()],
                n_runs=1,
                temperature=None,
                prompt_version="standard",
                pillars=[1],
                research_mode=False,
                output_dir="/tmp",
                started_at=_utc(),
            )
        assert m.git_commit_hash == "deadbeef"

    def test_design_tier_defaults_to_realistic(self):
        m = create_manifest(
            session_id="s",
            agents=["a"],
            scenarios=[self._make_scenario()],
            n_runs=1,
            temperature=None,
            prompt_version="standard",
            pillars=[1],
            research_mode=False,
            output_dir="/tmp",
            started_at=_utc(),
        )
        assert m.design_tier == "realistic"


# ── finalize_manifest ─────────────────────────────────────────────────────────

class TestFinalizeManifest:
    def _make_result(self, cost: float | None = None):
        r = MagicMock()
        r.api_cost_usd = cost
        return r

    def test_sets_total_completed_runs(self):
        m = _make_manifest()
        results = [self._make_result() for _ in range(7)]
        finalized = finalize_manifest(m, results, _utc("2026-04-16T11:00:00+00:00"))
        assert finalized.total_completed_runs == 7

    def test_sets_end_time_utc(self):
        m = _make_manifest()
        t = _utc("2026-04-16T11:30:00+00:00")
        finalized = finalize_manifest(m, [], t)
        assert finalized.end_time_utc == t.isoformat()

    def test_sums_api_costs_when_present(self):
        m = _make_manifest()
        results = [self._make_result(0.01), self._make_result(0.02), self._make_result(0.03)]
        finalized = finalize_manifest(m, results, _utc())
        assert finalized.total_api_cost_usd == pytest.approx(0.06)

    def test_total_cost_none_when_no_costs(self):
        m = _make_manifest()
        results = [self._make_result(None), self._make_result(None)]
        finalized = finalize_manifest(m, results, _utc())
        assert finalized.total_api_cost_usd is None

    def test_partial_costs_excluded(self):
        m = _make_manifest()
        results = [self._make_result(0.05), self._make_result(None), self._make_result(0.10)]
        finalized = finalize_manifest(m, results, _utc())
        assert finalized.total_api_cost_usd == pytest.approx(0.15)

    def test_does_not_mutate_original(self):
        m = _make_manifest()
        assert m.total_completed_runs == 0
        _ = finalize_manifest(m, [self._make_result()], _utc())
        assert m.total_completed_runs == 0  # original unchanged

    def test_empty_results(self):
        m = _make_manifest()
        finalized = finalize_manifest(m, [], _utc())
        assert finalized.total_completed_runs == 0
        assert finalized.total_api_cost_usd is None


# ── write_manifest ────────────────────────────────────────────────────────────

class TestWriteManifest:
    def test_creates_file_in_output_dir(self, tmp_path):
        m = _make_manifest(output_dir=str(tmp_path))
        path = write_manifest(m, str(tmp_path))
        assert path == tmp_path / "experiment_manifest.json"
        assert path.exists()

    def test_written_content_is_valid_json(self, tmp_path):
        m = _make_manifest(output_dir=str(tmp_path))
        path = write_manifest(m, str(tmp_path))
        data = json.loads(path.read_text())
        assert data["experiment_id"] == m.experiment_id

    def test_creates_output_dir_if_missing(self, tmp_path):
        new_dir = tmp_path / "nested" / "output"
        m = _make_manifest(output_dir=str(new_dir))
        write_manifest(m, str(new_dir))
        assert (new_dir / "experiment_manifest.json").exists()

    def test_overwrites_existing_manifest(self, tmp_path):
        m1 = _make_manifest(experiment_id="first", output_dir=str(tmp_path))
        write_manifest(m1, str(tmp_path))
        m2 = _make_manifest(experiment_id="second", output_dir=str(tmp_path))
        write_manifest(m2, str(tmp_path))
        data = json.loads((tmp_path / "experiment_manifest.json").read_text())
        assert data["experiment_id"] == "second"

    def test_json_contains_all_required_h2_fields(self, tmp_path):
        m = _make_manifest(
            output_dir=str(tmp_path),
            git_commit_hash="abc123",
            n_bias_types=5,
            n_variants_per_bias=2,
            total_planned_runs=500,
            total_completed_runs=500,
            total_api_cost_usd=12.34,
            end_time_utc="2026-04-16T11:00:00+00:00",
        )
        data = json.loads(write_manifest(m, str(tmp_path)).read_text())
        required = [
            "experiment_id", "design_tier", "n_models", "n_bias_types",
            "n_variants_per_bias", "n_runs_per_cell", "temperatures",
            "prompt_versions", "total_planned_runs", "total_completed_runs",
            "total_api_cost_usd", "pre_registration_url", "git_commit_hash",
            "start_time_utc", "end_time_utc",
        ]
        for field in required:
            assert field in data, f"Missing field: {field}"

    def test_none_temperature_serializes_to_json_null(self, tmp_path):
        m = _make_manifest(temperatures=[None], output_dir=str(tmp_path))
        data = json.loads(write_manifest(m, str(tmp_path)).read_text())
        assert data["temperatures"] == [None]


# ── CLI integration ───────────────────────────────────────────────────────────

class TestExperimentManifestCLI:
    """Integration tests: verify manifest is written by ``buyerbench run``."""

    def test_manifest_created_in_output_dir(self, tmp_path):
        from click.testing import CliRunner
        from buyerbench.__main__ import cli

        runner = CliRunner()
        result = runner.invoke(cli, [
            "run",
            "--agent", "mock-agent-v1",
            "--pillar", "1",
            "--output-dir", str(tmp_path),
        ])
        assert result.exit_code == 0
        manifest_path = tmp_path / "experiment_manifest.json"
        assert manifest_path.exists(), "experiment_manifest.json not found"

    def test_manifest_json_is_valid(self, tmp_path):
        from click.testing import CliRunner
        from buyerbench.__main__ import cli

        runner = CliRunner()
        runner.invoke(cli, [
            "run",
            "--agent", "mock-agent-v1",
            "--pillar", "1",
            "--output-dir", str(tmp_path),
        ])
        data = json.loads((tmp_path / "experiment_manifest.json").read_text())
        assert "experiment_id" in data
        assert "start_time_utc" in data
        assert "end_time_utc" in data

    def test_manifest_end_time_set_after_run(self, tmp_path):
        from click.testing import CliRunner
        from buyerbench.__main__ import cli

        runner = CliRunner()
        runner.invoke(cli, [
            "run",
            "--agent", "mock-agent-v1",
            "--pillar", "1",
            "--output-dir", str(tmp_path),
        ])
        data = json.loads((tmp_path / "experiment_manifest.json").read_text())
        assert data["end_time_utc"] is not None, "end_time_utc should be set after completion"

    def test_manifest_total_completed_runs_correct(self, tmp_path):
        from click.testing import CliRunner
        from buyerbench.__main__ import cli

        runner = CliRunner()
        runner.invoke(cli, [
            "run",
            "--agent", "mock-agent-v1",
            "--pillar", "2",
            "--output-dir", str(tmp_path),
        ])
        data = json.loads((tmp_path / "experiment_manifest.json").read_text())
        assert data["total_completed_runs"] > 0

    def test_dry_run_does_not_create_manifest(self, tmp_path):
        from click.testing import CliRunner
        from buyerbench.__main__ import cli

        runner = CliRunner()
        runner.invoke(cli, [
            "run",
            "--agent", "mock-agent-v1",
            "--pillar", "1",
            "--dry-run",
            "--output-dir", str(tmp_path),
        ])
        assert not (tmp_path / "experiment_manifest.json").exists(), \
            "Manifest should NOT be created in dry-run mode"

    def test_manifest_n_runs_per_cell_matches_flag(self, tmp_path):
        from click.testing import CliRunner
        from buyerbench.__main__ import cli

        runner = CliRunner()
        runner.invoke(cli, [
            "run",
            "--agent", "mock-agent-v1",
            "--pillar", "1",
            "--n-runs", "3",
            "--output-dir", str(tmp_path),
        ])
        data = json.loads((tmp_path / "experiment_manifest.json").read_text())
        assert data["n_runs_per_cell"] == 3

    def test_manifest_temperature_recorded(self, tmp_path):
        from click.testing import CliRunner
        from buyerbench.__main__ import cli

        runner = CliRunner()
        runner.invoke(cli, [
            "run",
            "--agent", "mock-agent-v1",
            "--pillar", "1",
            "--temperature", "0.7",
            "--output-dir", str(tmp_path),
        ])
        data = json.loads((tmp_path / "experiment_manifest.json").read_text())
        assert 0.7 in data["temperatures"]

    def test_manifest_prompt_version_recorded(self, tmp_path):
        from click.testing import CliRunner
        from buyerbench.__main__ import cli

        runner = CliRunner()
        runner.invoke(cli, [
            "run",
            "--agent", "mock-agent-v1",
            "--pillar", "1",
            "--prompt-version", "cot",
            "--output-dir", str(tmp_path),
        ])
        data = json.loads((tmp_path / "experiment_manifest.json").read_text())
        assert "cot" in data["prompt_versions"]

    def test_manifest_pillars_field_matches_filter(self, tmp_path):
        from click.testing import CliRunner
        from buyerbench.__main__ import cli

        runner = CliRunner()
        runner.invoke(cli, [
            "run",
            "--agent", "mock-agent-v1",
            "--pillar", "2",
            "--output-dir", str(tmp_path),
        ])
        data = json.loads((tmp_path / "experiment_manifest.json").read_text())
        assert data["pillars"] == [2]
