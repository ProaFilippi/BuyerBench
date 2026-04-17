"""Tests for research/analysis/ceiling_effect.py.

Covers:
- Constants: CEILING_THRESHOLD, FLOOR_BSI, MIN_MODELS_FOR_GATE
- compute_model_bias_means: empty, single model, multi-model, error exclusion
- detect_ceiling_effect: PROCEED, CEILING, INSUFFICIENT gate decisions
- detect_ceiling_effect: per_model breakdown, all_floor flags
- detect_ceiling_effect: custom threshold/floor parameters
- detect_ceiling_effect: exactly-at-threshold boundary (≥, not >)
- analyze_ceiling_effect: loads from runs.jsonl, writes output JSON
- analyze_ceiling_effect: empty jsonl → INSUFFICIENT
- load_runs_from_jsonl: malformed lines skipped silently
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import pytest

from research.analysis.ceiling_effect import (
    CEILING_THRESHOLD,
    FLOOR_BSI,
    MIN_MODELS_FOR_GATE,
    analyze_ceiling_effect,
    compute_model_bias_means,
    detect_ceiling_effect,
    load_runs_from_jsonl,
)


# ── Constants ─────────────────────────────────────────────────────────────────


class TestConstants:
    def test_ceiling_threshold_is_seven(self):
        assert CEILING_THRESHOLD == 7

    def test_floor_bsi_is_0_05(self):
        assert abs(FLOOR_BSI - 0.05) < 1e-9

    def test_min_models_for_gate_is_three(self):
        assert MIN_MODELS_FOR_GATE == 3


# ── compute_model_bias_means ──────────────────────────────────────────────────


def _run(agent_id, bias_cat, bsi, error=False):
    return {
        "agent_id": agent_id,
        "bias_category": bias_cat,
        "bsi": bsi,
        "error_flag": error,
    }


class TestComputeModelBiasMeans:
    def test_empty_records_returns_empty(self):
        assert compute_model_bias_means([]) == {}

    def test_single_record(self):
        result = compute_model_bias_means([_run("model-a", "anchoring", 0.4)])
        assert result == {"model-a": {"anchoring": pytest.approx(0.4)}}

    def test_two_records_same_cell_averaged(self):
        records = [
            _run("model-a", "anchoring", 0.4),
            _run("model-a", "anchoring", 0.8),
        ]
        result = compute_model_bias_means(records)
        assert result["model-a"]["anchoring"] == pytest.approx(0.6)

    def test_error_records_excluded(self):
        records = [
            _run("model-a", "anchoring", 0.9, error=True),
            _run("model-a", "anchoring", 0.2),
        ]
        result = compute_model_bias_means(records)
        assert result["model-a"]["anchoring"] == pytest.approx(0.2)

    def test_two_models_two_biases(self):
        records = [
            _run("model-a", "anchoring", 0.3),
            _run("model-a", "framing", 0.1),
            _run("model-b", "anchoring", 0.8),
            _run("model-b", "framing", 0.0),
        ]
        result = compute_model_bias_means(records)
        assert set(result.keys()) == {"model-a", "model-b"}
        assert result["model-a"]["anchoring"] == pytest.approx(0.3)
        assert result["model-b"]["framing"] == pytest.approx(0.0)

    def test_all_errors_returns_empty(self):
        records = [_run("model-a", "anchoring", 0.5, error=True)]
        assert compute_model_bias_means(records) == {}

    def test_records_with_missing_agent_id_skipped(self):
        records = [{"agent_id": "", "bias_category": "anchoring", "bsi": 0.5, "error_flag": False}]
        assert compute_model_bias_means(records) == {}


# ── detect_ceiling_effect ─────────────────────────────────────────────────────


def _ten_floor_models():
    """10 models all scoring BSI=0 on all 5 bias types → CEILING."""
    bias_types = ["anchoring", "framing", "decoy", "scarcity", "sunk_cost"]
    return {
        f"model-{i:02d}": {b: 0.0 for b in bias_types}
        for i in range(10)
    }


def _ten_mixed_models():
    """3 floor models, 7 with some non-zero BSI → PROCEED."""
    bias_types = ["anchoring", "framing", "decoy", "scarcity", "sunk_cost"]
    result = {
        f"model-{i:02d}": {b: 0.0 for b in bias_types}
        for i in range(3)  # 3 floor models
    }
    for i in range(3, 10):  # 7 with ≥1 non-zero
        result[f"model-{i:02d}"] = {b: 0.2 for b in bias_types}
    return result


class TestDetectCeilingEffect:
    def test_all_floor_models_returns_ceiling(self):
        result = detect_ceiling_effect(_ten_floor_models())
        assert result["gate"] == "CEILING"

    def test_proceed_when_below_threshold(self):
        result = detect_ceiling_effect(_ten_mixed_models())
        assert result["gate"] == "PROCEED"

    def test_insufficient_when_too_few_models(self):
        model_bias = {"model-a": {"anchoring": 0.0}}
        result = detect_ceiling_effect(model_bias)
        assert result["gate"] == "INSUFFICIENT"

    def test_n_floor_models_counted_correctly(self):
        result = detect_ceiling_effect(_ten_floor_models())
        assert result["n_floor_models"] == 10

    def test_n_models_in_result(self):
        result = detect_ceiling_effect(_ten_floor_models())
        assert result["n_models"] == 10

    def test_rev4_needed_on_ceiling(self):
        result = detect_ceiling_effect(_ten_floor_models())
        assert result["rev4_needed"] is True

    def test_rev4_not_needed_on_proceed(self):
        result = detect_ceiling_effect(_ten_mixed_models())
        assert result["rev4_needed"] is False

    def test_per_model_all_floor_flag_true_for_floor_model(self):
        result = detect_ceiling_effect(_ten_floor_models())
        for model_data in result["per_model"].values():
            assert model_data["all_floor"] is True

    def test_per_model_all_floor_flag_false_for_non_floor_model(self):
        result = detect_ceiling_effect(_ten_mixed_models())
        non_floor = [
            m for m, d in result["per_model"].items()
            if not d["all_floor"]
        ]
        assert len(non_floor) == 7

    def test_custom_threshold_lower_triggers_ceiling_with_fewer_models(self):
        # 3 floor models, threshold=3 → CEILING
        model_bias = {
            f"model-{i:02d}": {"anchoring": 0.0}
            for i in range(10)
        }
        for i in range(3, 10):
            model_bias[f"model-{i:02d}"] = {"anchoring": 0.5}
        result = detect_ceiling_effect(model_bias, threshold=3)
        assert result["gate"] == "CEILING"

    def test_custom_floor_higher_classifies_more_models_as_floor(self):
        # All models at BSI=0.08, which is < 0.10 but > 0.05
        model_bias = {f"model-{i}": {"anchoring": 0.08} for i in range(10)}
        default_result = detect_ceiling_effect(model_bias, floor=0.05)
        # With default floor=0.05: 0.08 is NOT floor
        assert default_result["n_floor_models"] == 0
        # With floor=0.10: 0.08 IS floor
        high_floor_result = detect_ceiling_effect(model_bias, floor=0.10)
        assert high_floor_result["n_floor_models"] == 10

    def test_exact_threshold_boundary_triggers_ceiling(self):
        # Exactly 7 floor models, threshold=7 → CEILING (≥, not >)
        bias_types = ["anchoring", "framing"]
        model_bias = {}
        for i in range(7):
            model_bias[f"floor-{i:02d}"] = {b: 0.0 for b in bias_types}
        for i in range(3):
            model_bias[f"high-{i:02d}"] = {b: 0.5 for b in bias_types}
        result = detect_ceiling_effect(model_bias, threshold=7)
        assert result["gate"] == "CEILING"
        assert result["n_floor_models"] == 7

    def test_one_below_threshold_is_proceed(self):
        # Exactly 6 floor models, threshold=7 → PROCEED
        bias_types = ["anchoring", "framing"]
        model_bias = {}
        for i in range(6):
            model_bias[f"floor-{i:02d}"] = {b: 0.0 for b in bias_types}
        for i in range(4):
            model_bias[f"high-{i:02d}"] = {b: 0.5 for b in bias_types}
        result = detect_ceiling_effect(model_bias, threshold=7)
        assert result["gate"] == "PROCEED"

    def test_threshold_floor_in_result(self):
        result = detect_ceiling_effect(_ten_floor_models(), threshold=5, floor=0.02)
        assert result["threshold"] == 5
        assert result["floor"] == pytest.approx(0.02)

    def test_recommendation_is_non_empty_string(self):
        result = detect_ceiling_effect(_ten_floor_models())
        assert isinstance(result["recommendation"], str) and result["recommendation"]

    def test_model_not_all_floor_if_one_bias_above_floor(self):
        # Model with anchoring=0.0 but framing=0.2 → not all_floor
        model_bias = {
            "model-a": {"anchoring": 0.0, "framing": 0.2},
        }
        for i in range(9):
            model_bias[f"floor-{i}"] = {"anchoring": 0.0, "framing": 0.0}
        result = detect_ceiling_effect(model_bias)
        assert result["per_model"]["model-a"]["all_floor"] is False


# ── load_runs_from_jsonl ──────────────────────────────────────────────────────


class TestLoadRunsFromJsonl:
    def test_nonexistent_file_returns_empty(self, tmp_path):
        result = load_runs_from_jsonl(tmp_path / "no_such_file.jsonl")
        assert result == []

    def test_valid_jsonl_loaded(self, tmp_path):
        path = tmp_path / "runs.jsonl"
        path.write_text(
            '{"agent_id": "m1", "bsi": 0.1}\n'
            '{"agent_id": "m2", "bsi": 0.5}\n',
            encoding="utf-8",
        )
        records = load_runs_from_jsonl(path)
        assert len(records) == 2
        assert records[0]["agent_id"] == "m1"

    def test_malformed_line_skipped(self, tmp_path):
        path = tmp_path / "runs.jsonl"
        path.write_text(
            '{"agent_id": "m1", "bsi": 0.1}\n'
            'NOT_JSON_AT_ALL\n'
            '{"agent_id": "m2", "bsi": 0.5}\n',
            encoding="utf-8",
        )
        records = load_runs_from_jsonl(path)
        assert len(records) == 2

    def test_empty_lines_skipped(self, tmp_path):
        path = tmp_path / "runs.jsonl"
        path.write_text("\n\n\n", encoding="utf-8")
        assert load_runs_from_jsonl(path) == []


# ── analyze_ceiling_effect ────────────────────────────────────────────────────


def _write_runs_jsonl(path: Path, records: list[dict]) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        for rec in records:
            fh.write(json.dumps(rec) + "\n")


class TestAnalyzeCeilingEffect:
    def _ten_floor_records(self) -> list[dict]:
        bias_types = ["anchoring", "framing", "decoy", "scarcity", "sunk_cost"]
        records = []
        for i in range(10):
            for bias in bias_types:
                records.append({
                    "agent_id": f"model-{i:02d}",
                    "bias_category": bias,
                    "bsi": 0.0,
                    "error_flag": False,
                })
        return records

    def test_returns_ceiling_on_floor_data(self, tmp_path):
        _write_runs_jsonl(tmp_path / "runs.jsonl", self._ten_floor_records())
        result = analyze_ceiling_effect(tmp_path)
        assert result["gate"] == "CEILING"

    def test_n_total_runs_in_result(self, tmp_path):
        records = self._ten_floor_records()
        _write_runs_jsonl(tmp_path / "runs.jsonl", records)
        result = analyze_ceiling_effect(tmp_path)
        assert result["n_total_runs"] == len(records)

    def test_n_valid_runs_excludes_errors(self, tmp_path):
        records = self._ten_floor_records()
        records[0]["error_flag"] = True
        _write_runs_jsonl(tmp_path / "runs.jsonl", records)
        result = analyze_ceiling_effect(tmp_path)
        assert result["n_valid_runs"] == len(records) - 1

    def test_experiment_dir_in_result(self, tmp_path):
        _write_runs_jsonl(tmp_path / "runs.jsonl", self._ten_floor_records())
        result = analyze_ceiling_effect(tmp_path)
        assert "experiment_dir" in result

    def test_output_json_written(self, tmp_path):
        _write_runs_jsonl(tmp_path / "runs.jsonl", self._ten_floor_records())
        out = tmp_path / "ceiling_effect.json"
        analyze_ceiling_effect(tmp_path, output_path=out)
        assert out.exists()
        data = json.loads(out.read_text())
        assert data["gate"] == "CEILING"

    def test_empty_jsonl_returns_insufficient(self, tmp_path):
        (tmp_path / "runs.jsonl").write_text("", encoding="utf-8")
        result = analyze_ceiling_effect(tmp_path)
        assert result["gate"] == "INSUFFICIENT"

    def test_proceed_gate_with_varied_bsi(self, tmp_path):
        bias_types = ["anchoring", "framing"]
        records = []
        for i in range(10):
            bsi_val = 0.0 if i < 3 else 0.3
            for bias in bias_types:
                records.append({
                    "agent_id": f"model-{i:02d}",
                    "bias_category": bias,
                    "bsi": bsi_val,
                    "error_flag": False,
                })
        _write_runs_jsonl(tmp_path / "runs.jsonl", records)
        result = analyze_ceiling_effect(tmp_path, threshold=7)
        assert result["gate"] == "PROCEED"
