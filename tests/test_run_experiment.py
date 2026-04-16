"""Tests for research.experiments.run_experiment.

Covers the pure-function layer of the run orchestration:
- generate_run_plan: correct cell expansion from a manifest dict
- load_completed_run_ids: reading run_ids from existing JSONL
- append_run_record / round-trip: serialize + deserialize a RunRecord
- build_run_record: happy path and error path construction
- estimate_cost: numeric formula
- _build_parser: CLI argument contract
- run_experiment dry-run: stdout output, no filesystem mutations beyond manifest
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from research.experiments.run_experiment import (
    _build_parser,
    append_run_record,
    build_run_record,
    estimate_cost,
    generate_run_plan,
    load_completed_run_ids,
    run_experiment,
)
from research.experiments.schemas import RunRecord


# ── Fixtures ──────────────────────────────────────────────────────────────────


MINIMAL_MANIFEST = {
    "experiment_id": "pillar2-test-20260416-000000",
    "design_tier": "realistic",
    "n_models": 2,
    "n_bias_types": 2,
    "n_variants_per_bias": 2,
    "n_runs_per_cell": 2,
    "temperatures": [0.7],
    "prompt_versions": ["standard"],
    "models": [
        "openrouter-openai-gpt-4o",
        "openrouter-anthropic-claude-3.5-sonnet",
    ],
    "bias_scenarios": {
        "anchoring": {
            "baseline": "p2-01-anchoring-BASELINE",
            "treatment": "p2-01-anchoring-ANCHOR_HIGH",
        },
        "framing": {
            "baseline": "p2-02-framing-FRAMING_GAIN",
            "treatment": "p2-02-framing-FRAMING_LOSS",
        },
    },
    "total_planned_runs": 0,
    "total_completed_runs": 0,
    "total_api_cost_usd": 0.0,
    "git_commit_hash": "abc123",
}


def _make_manifest_file(tmp_path: Path, manifest: dict | None = None) -> Path:
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps(manifest or MINIMAL_MANIFEST))
    return path


def _make_run_record(**overrides) -> RunRecord:
    defaults = dict(
        run_id="abc123def456",
        session_id="pillar2-test-20260416-000000",
        agent_id="openrouter-openai-gpt-4o",
        model_family="openai-gpt-4o",
        model_version="gpt-4o-2024-11-20",
        scenario_id="p2-01-anchoring-BASELINE",
        bias_category="anchoring",
        variant="baseline",
        run_index=1,
        temperature=0.7,
        prompt_version="standard",
        supplier_order_seed=42,
        timestamp_utc=datetime(2026, 4, 16, 12, 0, 0, tzinfo=timezone.utc),
        agent_output_raw="I choose SupplierA.",
        extracted_choice="SupplierA",
        choice_is_correct=True,
        optimal_choice="SupplierA",
        bsi=0.0,
        optimality_gap=0.0,
        token_count_input=150,
        token_count_output=40,
        api_cost_usd=0.012,
        error_flag=False,
        error_message=None,
    )
    defaults.update(overrides)
    return RunRecord(**defaults)


# ── generate_run_plan ─────────────────────────────────────────────────────────


class TestGenerateRunPlan:
    def test_total_run_count(self):
        # 2 models × 2 biases × 2 variants × 1 temp × 1 prompt × 2 runs = 16
        runs = generate_run_plan(MINIMAL_MANIFEST)
        assert len(runs) == 16

    def test_run_ids_are_deterministic(self):
        runs_a = generate_run_plan(MINIMAL_MANIFEST)
        runs_b = generate_run_plan(MINIMAL_MANIFEST)
        assert [r["run_id"] for r in runs_a] == [r["run_id"] for r in runs_b]

    def test_run_ids_are_unique(self):
        runs = generate_run_plan(MINIMAL_MANIFEST)
        ids = [r["run_id"] for r in runs]
        assert len(ids) == len(set(ids))

    def test_run_id_is_12_chars(self):
        runs = generate_run_plan(MINIMAL_MANIFEST)
        for r in runs:
            assert len(r["run_id"]) == 12, f"run_id wrong length: {r['run_id']!r}"

    def test_run_index_range(self):
        runs = generate_run_plan(MINIMAL_MANIFEST)
        indices = [r["run_index"] for r in runs]
        assert min(indices) == 1
        assert max(indices) == MINIMAL_MANIFEST["n_runs_per_cell"]

    def test_all_agents_present(self):
        runs = generate_run_plan(MINIMAL_MANIFEST)
        agents = {r["agent_id"] for r in runs}
        assert agents == set(MINIMAL_MANIFEST["models"])

    def test_all_bias_categories_present(self):
        runs = generate_run_plan(MINIMAL_MANIFEST)
        cats = {r["bias_category"] for r in runs}
        assert cats == set(MINIMAL_MANIFEST["bias_scenarios"].keys())

    def test_all_variants_present(self):
        runs = generate_run_plan(MINIMAL_MANIFEST)
        variants = {r["variant"] for r in runs}
        assert variants == {"baseline", "treatment"}

    def test_supplier_order_seed_is_uint32(self):
        runs = generate_run_plan(MINIMAL_MANIFEST)
        for r in runs:
            assert 0 <= r["supplier_order_seed"] < 2**32

    def test_multiple_temperatures(self):
        manifest = {**MINIMAL_MANIFEST, "temperatures": [0.0, 0.7], "n_runs_per_cell": 1}
        runs = generate_run_plan(manifest)
        # 2 models × 2 biases × 2 variants × 2 temps × 1 prompt × 1 run = 16
        assert len(runs) == 16
        temps = {r["temperature"] for r in runs}
        assert temps == {0.0, 0.7}

    def test_multiple_prompt_versions(self):
        manifest = {**MINIMAL_MANIFEST, "prompt_versions": ["standard", "cot"], "n_runs_per_cell": 1}
        runs = generate_run_plan(manifest)
        pvs = {r["prompt_version"] for r in runs}
        assert pvs == {"standard", "cot"}


# ── load_completed_run_ids ────────────────────────────────────────────────────


class TestLoadCompletedRunIds:
    def test_empty_when_file_missing(self, tmp_path):
        ids = load_completed_run_ids(tmp_path / "nonexistent.jsonl")
        assert ids == set()

    def test_reads_run_ids(self, tmp_path):
        jsonl = tmp_path / "runs.jsonl"
        jsonl.write_text(
            '{"run_id": "aaa111bbb222", "agent_id": "x"}\n'
            '{"run_id": "ccc333ddd444", "agent_id": "y"}\n'
        )
        ids = load_completed_run_ids(jsonl)
        assert ids == {"aaa111bbb222", "ccc333ddd444"}

    def test_skips_malformed_lines(self, tmp_path):
        jsonl = tmp_path / "runs.jsonl"
        jsonl.write_text(
            '{"run_id": "good000000ab"}\n'
            'not valid json\n'
            '{"missing_key": true}\n'
        )
        ids = load_completed_run_ids(jsonl)
        assert ids == {"good000000ab"}

    def test_empty_file(self, tmp_path):
        jsonl = tmp_path / "runs.jsonl"
        jsonl.write_text("")
        assert load_completed_run_ids(jsonl) == set()


# ── append_run_record ─────────────────────────────────────────────────────────


class TestAppendRunRecord:
    def test_creates_file_if_missing(self, tmp_path):
        jsonl = tmp_path / "runs.jsonl"
        record = _make_run_record()
        append_run_record(record, jsonl)
        assert jsonl.exists()

    def test_appends_multiple_records(self, tmp_path):
        jsonl = tmp_path / "runs.jsonl"
        record_a = _make_run_record(run_id="aaabbbcccddd")
        record_b = _make_run_record(run_id="eeefffggghh0")
        append_run_record(record_a, jsonl)
        append_run_record(record_b, jsonl)
        lines = [l for l in jsonl.read_text().splitlines() if l.strip()]
        assert len(lines) == 2

    def test_round_trip_run_id(self, tmp_path):
        jsonl = tmp_path / "runs.jsonl"
        record = _make_run_record(run_id="roundtrip000")
        append_run_record(record, jsonl)
        ids = load_completed_run_ids(jsonl)
        assert "roundtrip000" in ids

    def test_datetime_serialized_as_string(self, tmp_path):
        jsonl = tmp_path / "runs.jsonl"
        record = _make_run_record()
        append_run_record(record, jsonl)
        line = jsonl.read_text().strip()
        data = json.loads(line)
        assert isinstance(data["timestamp_utc"], str)


# ── build_run_record ──────────────────────────────────────────────────────────


class TestBuildRunRecord:
    def _minimal_run_spec(self, **overrides) -> dict:
        spec = {
            "run_id": "aabbccddeeff",
            "agent_id": "openrouter-openai-gpt-4o",
            "scenario_id": "p2-01-anchoring-BASELINE",
            "bias_category": "anchoring",
            "variant": "baseline",
            "run_index": 1,
            "temperature": 0.7,
            "prompt_version": "standard",
            "supplier_order_seed": 12345,
        }
        spec.update(overrides)
        return spec

    def test_error_record_when_result_is_none(self):
        spec = self._minimal_run_spec()
        record = build_run_record(spec, None, "test-session")
        assert record.error_flag is True
        assert record.error_message is not None
        assert record.bsi == 0.0

    def test_happy_path_extracts_bsi(self):
        spec = self._minimal_run_spec()
        result = {
            "pillar_scores": [{"metrics": {"bias_susceptibility_index": 0.6, "optimality_gap": 0.1}}],
            "agent_response_raw": "SupplierA",
            "agent_response": {"decisions": {"selected_supplier": "SupplierA"}},
            "scenario": {"optimal_choice": "SupplierA"},
            "usage": {"input_tokens": 100, "output_tokens": 30, "cost_usd": 0.02},
            "model_version": "gpt-4o-2024-11-20",
        }
        record = build_run_record(spec, result, "test-session")
        assert record.bsi == pytest.approx(0.6)
        assert record.optimality_gap == pytest.approx(0.1)
        assert record.error_flag is False
        assert record.choice_is_correct is True

    def test_bsi_clamped_to_unit_interval(self):
        spec = self._minimal_run_spec()
        result = {
            "pillar_scores": [{"metrics": {"bias_susceptibility_index": 1.5}}],
            "agent_response": {},
            "usage": {},
        }
        record = build_run_record(spec, result, "test-session")
        assert record.bsi == 1.0

    def test_optimality_gap_floored_at_zero(self):
        spec = self._minimal_run_spec()
        result = {
            "pillar_scores": [{"metrics": {"optimality_gap": -0.05}}],
            "agent_response": {},
            "usage": {},
        }
        record = build_run_record(spec, result, "test-session")
        assert record.optimality_gap == 0.0

    def test_model_family_derived_from_agent_id(self):
        spec = self._minimal_run_spec(agent_id="openrouter-openai-gpt-4o")
        record = build_run_record(spec, None, "test-session")
        assert record.model_family == "openai-gpt-4o"

    def test_model_family_no_prefix(self):
        spec = self._minimal_run_spec(agent_id="mock-agent-v1")
        record = build_run_record(spec, None, "test-session")
        assert record.model_family == "agent-v1"

    def test_session_id_preserved(self):
        spec = self._minimal_run_spec()
        record = build_run_record(spec, None, "my-session-id")
        assert record.session_id == "my-session-id"

    def test_run_spec_fields_preserved(self):
        spec = self._minimal_run_spec(run_index=5, temperature=0.3)
        record = build_run_record(spec, None, "s")
        assert record.run_index == 5
        assert record.temperature == pytest.approx(0.3)
        assert record.supplier_order_seed == 12345


# ── estimate_cost ─────────────────────────────────────────────────────────────


class TestEstimateCost:
    def test_default_rate(self):
        cost = estimate_cost(100)
        assert cost["n_runs"] == 100
        assert cost["estimated_total_usd"] == pytest.approx(15.0)

    def test_custom_rate(self):
        cost = estimate_cost(200, cost_per_run_usd=0.05)
        assert cost["estimated_total_usd"] == pytest.approx(10.0)

    def test_returns_dict_with_note(self):
        cost = estimate_cost(1)
        assert "note" in cost


# ── _build_parser ─────────────────────────────────────────────────────────────


class TestBuildParser:
    def test_manifest_positional(self):
        parser = _build_parser()
        args = parser.parse_args(["path/to/manifest.json"])
        assert args.manifest == Path("path/to/manifest.json")

    def test_dry_run_default_false(self):
        parser = _build_parser()
        args = parser.parse_args(["manifest.json"])
        assert args.dry_run is False

    def test_dry_run_flag(self):
        parser = _build_parser()
        args = parser.parse_args(["manifest.json", "--dry-run"])
        assert args.dry_run is True

    def test_resume_flag(self):
        parser = _build_parser()
        args = parser.parse_args(["manifest.json", "--resume"])
        assert args.resume is True

    def test_output_dir_default_none(self):
        parser = _build_parser()
        args = parser.parse_args(["manifest.json"])
        assert args.output_dir is None

    def test_output_dir_set(self):
        parser = _build_parser()
        args = parser.parse_args(["manifest.json", "--output-dir", "/tmp/exp"])
        assert args.output_dir == Path("/tmp/exp")


# ── run_experiment dry-run ────────────────────────────────────────────────────


class TestRunExperimentDryRun:
    def test_dry_run_prints_plan(self, tmp_path, capsys):
        manifest_path = _make_manifest_file(tmp_path)
        run_experiment(manifest_path, dry_run=True)
        captured = capsys.readouterr()
        assert "DRY RUN" in captured.out
        assert "16" in captured.out  # 16 planned runs

    def test_dry_run_does_not_create_runs_jsonl(self, tmp_path):
        manifest_path = _make_manifest_file(tmp_path)
        run_experiment(manifest_path, dry_run=True)
        assert not (tmp_path / "runs.jsonl").exists()

    def test_dry_run_reports_cost_estimate(self, tmp_path, capsys):
        manifest_path = _make_manifest_file(tmp_path)
        run_experiment(manifest_path, dry_run=True)
        captured = capsys.readouterr()
        assert "$" in captured.out

    def test_dry_run_with_custom_output_dir(self, tmp_path, capsys):
        out_dir = tmp_path / "custom_out"
        manifest_path = _make_manifest_file(tmp_path)
        run_experiment(manifest_path, output_dir=out_dir, dry_run=True)
        assert not (out_dir / "runs.jsonl").exists()


# ── run_experiment resume ─────────────────────────────────────────────────────


class TestRunExperimentResume:
    def test_resume_skips_completed_ids(self, tmp_path):
        """With all run_ids pre-populated in JSONL, the experiment loop is empty."""
        manifest_path = _make_manifest_file(tmp_path)
        runs = generate_run_plan(MINIMAL_MANIFEST)

        # Pre-populate runs.jsonl with all run_ids so nothing is pending
        jsonl = tmp_path / "runs.jsonl"
        for r in runs:
            record = build_run_record(r, None, "pillar2-test-20260416-000000")
            append_run_record(record, jsonl)

        invocations: list[dict] = []

        def fake_invoke(run_spec, run_output_dir):
            invocations.append(run_spec)
            return None

        with patch(
            "research.experiments.run_experiment._invoke_buyerbench",
            side_effect=fake_invoke,
        ):
            run_experiment(manifest_path, output_dir=tmp_path, resume=True)

        assert invocations == [], "Expected zero invocations when all runs already done"

    def test_resume_only_runs_missing_cells(self, tmp_path):
        """With half the runs pre-populated, only the other half should be invoked."""
        manifest_path = _make_manifest_file(tmp_path)
        runs = generate_run_plan(MINIMAL_MANIFEST)
        half = len(runs) // 2

        jsonl = tmp_path / "runs.jsonl"
        for r in runs[:half]:
            record = build_run_record(r, None, "pillar2-test-20260416-000000")
            append_run_record(record, jsonl)

        invocations: list[str] = []

        def fake_invoke(run_spec, run_output_dir):
            invocations.append(run_spec["run_id"])
            return None

        with patch(
            "research.experiments.run_experiment._invoke_buyerbench",
            side_effect=fake_invoke,
        ):
            run_experiment(manifest_path, output_dir=tmp_path, resume=True)

        expected_ids = {r["run_id"] for r in runs[half:]}
        assert set(invocations) == expected_ids


# ── run_experiment: JSONL output ──────────────────────────────────────────────


class TestRunExperimentJsonlOutput:
    def test_runs_jsonl_created_after_run(self, tmp_path):
        manifest_path = _make_manifest_file(tmp_path, {**MINIMAL_MANIFEST, "n_runs_per_cell": 1})
        with patch(
            "research.experiments.run_experiment._invoke_buyerbench",
            return_value=None,
        ):
            run_experiment(manifest_path, output_dir=tmp_path)
        assert (tmp_path / "runs.jsonl").exists()

    def test_runs_jsonl_line_count_matches_plan(self, tmp_path):
        manifest = {**MINIMAL_MANIFEST, "n_runs_per_cell": 1}
        manifest_path = _make_manifest_file(tmp_path, manifest)
        expected = len(generate_run_plan(manifest))

        with patch(
            "research.experiments.run_experiment._invoke_buyerbench",
            return_value=None,
        ):
            run_experiment(manifest_path, output_dir=tmp_path)

        lines = [
            l for l in (tmp_path / "runs.jsonl").read_text().splitlines() if l.strip()
        ]
        assert len(lines) == expected

    def test_manifest_updated_with_end_time(self, tmp_path):
        manifest_path = _make_manifest_file(tmp_path, {**MINIMAL_MANIFEST, "n_runs_per_cell": 1})
        with patch(
            "research.experiments.run_experiment._invoke_buyerbench",
            return_value=None,
        ):
            run_experiment(manifest_path, output_dir=tmp_path)

        updated = json.loads(manifest_path.read_text())
        assert updated.get("end_time_utc") is not None
