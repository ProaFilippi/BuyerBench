"""Tests for research/scripts/08_run_flagship.py.

Covers:
- FLAGSHIP_DESIGN constants: design_tier, n_runs_per_cell, temperatures, models
- FLAGSHIP_DESIGN: 8 bias types including default, loss_aversion, warp (17 slots)
- FLAGSHIP_DESIGN: total_runs = 10 × 17 × 2 temps × 2 prompts × 100 = 68,000
- FLAGSHIP_DESIGN valid design_tier in ExperimentManifest._VALID_TIERS
- FLAGSHIP_DESIGN in DESIGNS registry
- GATE3 constants: min_models, min_bias_types, ci_floor
- compute_gate3_from_cells: proceed=True when ≥3 models qualify
- compute_gate3_from_cells: proceed=False when <3 models qualify
- compute_gate3_from_cells: robust_rationality_pivot=True when no models qualify
- compute_gate3_from_cells: per-model bias counts correct
- compute_gate3_from_cells: handles cells.json with {"cells": [...]} wrapper
- analyze_gate3: raises FileNotFoundError when cells.json absent
- analyze_gate3: writes gate3.json and returns gate3 dict
- load_gate3_result: reads from gate3.json when present
- load_gate3_result: raises KeyError when gate3 key missing in gate3.json
- load_gate3_result: computes on-the-fly from cells.json when gate3.json absent
- load_gate3_result: raises FileNotFoundError when neither file present
- check_gate3: SystemExit(1) when gate3.proceed is False
- check_gate3: no exit when gate3.proceed is True
- CLI: --mock --dry-run end-to-end (manifest, run_plan, cost, design_tier)
- CLI: --skip-gate3 --dry-run end-to-end (real models present)
- CLI: missing --full-dir without flags raises SystemExit
- CLI: --full-dir with failed gate raises SystemExit(1)
- CLI: --analyze-gate3 computes and exits 0
- Mock run: design_tier == "flagship", models == ["mock-agent-v1"]
- Mock run: n_runs_per_cell == 100, temperatures == [0.7, 0.0]
- Mock run: prompt_versions == ["standard", "cot"]
- Mock run: total_planned_runs == 6800 (1 × 17 × 2 × 2 × 100)
- Mock run: run_plan row count == 6800, all run_ids unique, 12-char
- Mock run: run_plan has both temperature values
- Mock run: run_plan has both prompt_versions
- Mock run: run_index max == 100
- Mock run: cost_estimate == 0.0 for mock, n_runs == 6800
"""
from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path

import pytest

_SCRIPT_PATH = (
    Path(__file__).resolve().parent.parent
    / "research" / "scripts" / "08_run_flagship.py"
)


def _load_script():
    spec = importlib.util.spec_from_file_location("run_flagship", _SCRIPT_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_script = _load_script()


# ── FLAGSHIP_DESIGN constants ─────────────────────────────────────────────────


class TestFlagshipDesignConstants:
    def setup_method(self):
        import sys
        repo = Path(__file__).resolve().parent.parent
        if str(repo) not in sys.path:
            sys.path.insert(0, str(repo))
        from research.experiments.grid import FLAGSHIP_DESIGN
        self.design = FLAGSHIP_DESIGN

    def test_design_tier_is_flagship(self):
        assert self.design["design_tier"] == "flagship"

    def test_n_runs_per_cell_is_100(self):
        assert self.design["n_runs_per_cell"] == 100

    def test_temperatures_are_07_and_00(self):
        assert set(self.design["temperatures"]) == {0.7, 0.0}

    def test_prompt_versions_are_standard_and_cot(self):
        assert set(self.design["prompt_versions"]) == {"standard", "cot"}

    def test_has_10_real_models(self):
        assert len(self.design["models"]) == 10

    def test_all_models_are_openrouter(self):
        assert all(m.startswith("openrouter-") for m in self.design["models"])

    def test_has_8_bias_types(self):
        assert len(self.design["bias_scenarios"]) == 8

    def test_includes_default_bias(self):
        assert "default" in self.design["bias_scenarios"]

    def test_includes_loss_aversion_bias(self):
        assert "loss_aversion" in self.design["bias_scenarios"]

    def test_includes_warp_triplet(self):
        warp = self.design["bias_scenarios"]["warp"]
        assert set(warp.keys()) == {"warp_ab", "warp_bc", "warp_ac"}

    def test_total_scenario_slots_is_17(self):
        slots = sum(len(v) for v in self.design["bias_scenarios"].values())
        assert slots == 17  # 5×2 + 2 + 2 + 3

    def test_total_runs_is_68000(self):
        n_models = len(self.design["models"])
        n_slots = sum(len(v) for v in self.design["bias_scenarios"].values())
        n_temps = len(self.design["temperatures"])
        n_prompts = len(self.design["prompt_versions"])
        n_runs = self.design["n_runs_per_cell"]
        assert n_models * n_slots * n_temps * n_prompts * n_runs == 68_000

    def test_design_tier_in_valid_tiers(self):
        from research.experiments.schemas import ExperimentManifest
        assert "flagship" in ExperimentManifest._VALID_TIERS

    def test_design_in_designs_registry(self):
        from research.experiments.grid import DESIGNS
        assert "flagship" in DESIGNS


# ── Gate 3 constants ──────────────────────────────────────────────────────────


class TestGate3Constants:
    def test_min_models_is_3(self):
        assert _script.GATE3_MIN_MODELS == 3

    def test_min_bias_types_is_2(self):
        assert _script.GATE3_MIN_BIAS_TYPES == 2

    def test_ci_floor_is_zero(self):
        assert _script.GATE3_BSI_CI_FLOOR == 0.0


# ── compute_gate3_from_cells ──────────────────────────────────────────────────


def _make_cells_json(tmp_path: Path, cells: list[dict], wrap: bool = False) -> Path:
    cells_path = tmp_path / "cells.json"
    payload = {"cells": cells} if wrap else cells
    cells_path.write_text(json.dumps(payload), encoding="utf-8")
    return cells_path


def _treatment_cell(agent_id: str, bias_cat: str, ci_lower: float) -> dict:
    return {
        "agent_id": agent_id,
        "bias_category": bias_cat,
        "variant": "treatment",
        "ci_lower_95": ci_lower,
        "mean_bsi": max(ci_lower, 0.0),
    }


class TestComputeGate3FromCells:
    def test_proceed_true_when_3_models_qualify(self, tmp_path):
        cells = []
        for model in ["m1", "m2", "m3"]:
            for bias in ["anchoring", "framing"]:
                cells.append(_treatment_cell(model, bias, ci_lower=0.10))
        path = _make_cells_json(tmp_path, cells)
        result = _script.compute_gate3_from_cells(path)
        assert result["proceed"] is True

    def test_proceed_false_when_only_2_models_qualify(self, tmp_path):
        cells = []
        for model in ["m1", "m2"]:
            for bias in ["anchoring", "framing"]:
                cells.append(_treatment_cell(model, bias, ci_lower=0.10))
        path = _make_cells_json(tmp_path, cells)
        result = _script.compute_gate3_from_cells(path)
        assert result["proceed"] is False

    def test_proceed_false_when_only_1_bias_per_model(self, tmp_path):
        cells = []
        for model in ["m1", "m2", "m3", "m4"]:
            cells.append(_treatment_cell(model, "anchoring", ci_lower=0.15))
        path = _make_cells_json(tmp_path, cells)
        result = _script.compute_gate3_from_cells(path)
        assert result["proceed"] is False

    def test_robust_rationality_pivot_when_no_bias(self, tmp_path):
        cells = [_treatment_cell("m1", "anchoring", ci_lower=0.0)]
        path = _make_cells_json(tmp_path, cells)
        result = _script.compute_gate3_from_cells(path)
        assert result["robust_rationality_pivot"] is True

    def test_robust_rationality_false_when_some_bias(self, tmp_path):
        cells = [_treatment_cell("m1", "anchoring", ci_lower=0.10)]
        path = _make_cells_json(tmp_path, cells)
        result = _script.compute_gate3_from_cells(path)
        assert result["robust_rationality_pivot"] is False

    def test_per_model_counts_correct(self, tmp_path):
        cells = [
            _treatment_cell("m1", "anchoring", 0.10),
            _treatment_cell("m1", "framing", 0.10),
            _treatment_cell("m2", "anchoring", 0.10),
        ]
        path = _make_cells_json(tmp_path, cells)
        result = _script.compute_gate3_from_cells(path)
        counts = result["per_model_bias_counts"]
        assert counts["m1"] == 2
        assert counts["m2"] == 1

    def test_handles_wrapped_cells_json(self, tmp_path):
        cells = [_treatment_cell("m1", "anchoring", 0.10) for _ in range(3)]
        for m in ["m2", "m3"]:
            cells.append(_treatment_cell(m, "anchoring", 0.10))
            cells.append(_treatment_cell(m, "framing", 0.10))
        path = _make_cells_json(tmp_path, cells, wrap=True)
        result = _script.compute_gate3_from_cells(path)
        assert "proceed" in result

    def test_result_schema_complete(self, tmp_path):
        cells = []
        path = _make_cells_json(tmp_path, cells)
        result = _script.compute_gate3_from_cells(path)
        for key in [
            "proceed", "n_models_with_bias", "qualifying_models",
            "per_model_bias_counts", "criterion_detail", "recommendation",
            "robust_rationality_pivot", "gate3_min_models", "gate3_min_bias_types",
        ]:
            assert key in result, f"Missing key: {key}"

    def test_ci_exactly_zero_does_not_qualify(self, tmp_path):
        cells = [_treatment_cell("m1", "anchoring", ci_lower=0.0)]
        path = _make_cells_json(tmp_path, cells)
        result = _script.compute_gate3_from_cells(path)
        assert result["n_models_with_bias"] == 0

    def test_baseline_cells_not_counted(self, tmp_path):
        cells = [{"agent_id": "m1", "bias_category": "anchoring",
                  "variant": "baseline", "ci_lower_95": 0.50, "mean_bsi": 0.5}]
        path = _make_cells_json(tmp_path, cells)
        result = _script.compute_gate3_from_cells(path)
        assert result["n_models_with_bias"] == 0


# ── analyze_gate3 ─────────────────────────────────────────────────────────────


class TestAnalyzeGate3:
    def test_raises_file_not_found_when_cells_absent(self, tmp_path):
        with pytest.raises(FileNotFoundError, match="cells.json"):
            _script.analyze_gate3(tmp_path)

    def test_writes_gate3_json(self, tmp_path):
        cells = [_treatment_cell("m" + str(i), bias, 0.10)
                 for i in range(3) for bias in ["anchoring", "framing"]]
        _make_cells_json(tmp_path, cells)
        _script.analyze_gate3(tmp_path)
        assert (tmp_path / "gate3.json").exists()

    def test_gate3_json_has_gate3_key(self, tmp_path):
        _make_cells_json(tmp_path, [])
        _script.analyze_gate3(tmp_path)
        data = json.loads((tmp_path / "gate3.json").read_text())
        assert "gate3" in data

    def test_returns_gate3_dict(self, tmp_path):
        _make_cells_json(tmp_path, [])
        result = _script.analyze_gate3(tmp_path)
        assert isinstance(result, dict)
        assert "proceed" in result


# ── load_gate3_result ─────────────────────────────────────────────────────────


class TestLoadGate3Result:
    def test_reads_from_gate3_json_when_present(self, tmp_path):
        gate3 = {"proceed": True, "n_models_with_bias": 4,
                 "criterion_detail": "ok", "recommendation": "PASS",
                 "robust_rationality_pivot": False, "qualifying_models": {},
                 "per_model_bias_counts": {}, "gate3_min_models": 3,
                 "gate3_min_bias_types": 2}
        (tmp_path / "gate3.json").write_text(
            json.dumps({"gate3": gate3}), encoding="utf-8"
        )
        result = _script.load_gate3_result(tmp_path)
        assert result == gate3

    def test_raises_key_error_when_gate3_key_missing(self, tmp_path):
        (tmp_path / "gate3.json").write_text(
            json.dumps({"other": "data"}), encoding="utf-8"
        )
        with pytest.raises(KeyError, match="gate3"):
            _script.load_gate3_result(tmp_path)

    def test_computes_from_cells_when_gate3_json_absent(self, tmp_path):
        _make_cells_json(tmp_path, [])
        result = _script.load_gate3_result(tmp_path)
        assert "proceed" in result

    def test_raises_file_not_found_when_neither_file_present(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            _script.load_gate3_result(tmp_path)


# ── check_gate3 ───────────────────────────────────────────────────────────────


def _make_gate3_json(tmp_path: Path, proceed: bool) -> Path:
    gate3 = {
        "proceed": proceed,
        "n_models_with_bias": 4 if proceed else 1,
        "criterion_detail": "4 model(s) qualify (need ≥3)" if proceed else "1 model(s) qualify (need ≥3)",
        "recommendation": "Gate 3 PASSED." if proceed else "Gate 3 FAILED.",
        "robust_rationality_pivot": False,
        "qualifying_models": {},
        "per_model_bias_counts": {},
        "gate3_min_models": 3,
        "gate3_min_bias_types": 2,
    }
    gate3_path = tmp_path / "gate3.json"
    gate3_path.write_text(json.dumps({"gate3": gate3}), encoding="utf-8")
    return tmp_path


class TestCheckGate3:
    def test_exits_when_gate3_not_passed(self, tmp_path):
        full_dir = _make_gate3_json(tmp_path, proceed=False)
        with pytest.raises(SystemExit) as exc_info:
            _script.check_gate3(full_dir)
        assert exc_info.value.code == 1

    def test_no_exit_when_gate3_passed(self, tmp_path):
        full_dir = _make_gate3_json(tmp_path, proceed=True)
        _script.check_gate3(full_dir)  # should not raise


# ── CLI: error conditions ─────────────────────────────────────────────────────


class TestCLIErrorCases:
    def test_missing_full_dir_without_flags_raises(self, tmp_path):
        with pytest.raises(SystemExit):
            _script.main([
                "--dry-run",
                "--no-pin-versions",
                "--output-dir", str(tmp_path),
            ])

    def test_full_dir_with_failed_gate_raises_system_exit(self, tmp_path):
        full_dir = tmp_path / "full"
        full_dir.mkdir()
        _make_gate3_json(full_dir, proceed=False)
        out = tmp_path / "output"
        out.mkdir()
        with pytest.raises(SystemExit) as exc_info:
            _script.main([
                "--full-dir", str(full_dir),
                "--dry-run",
                "--no-pin-versions",
                "--output-dir", str(out),
            ])
        assert exc_info.value.code == 1

    def test_analyze_gate3_requires_full_dir(self, tmp_path):
        with pytest.raises(SystemExit):
            _script.main(["--analyze-gate3", "--output-dir", str(tmp_path)])

    def test_analyze_gate3_exits_0_on_success(self, tmp_path):
        full_dir = tmp_path / "full"
        full_dir.mkdir()
        _make_cells_json(full_dir, [])
        with pytest.raises(SystemExit) as exc_info:
            _script.main(["--analyze-gate3", "--full-dir", str(full_dir)])
        assert exc_info.value.code == 0


# ── CLI: --mock --dry-run end-to-end ─────────────────────────────────────────


class TestRunFlagshipMockDryRun:
    @pytest.fixture(scope="class")
    def exp_dir(self, tmp_path_factory):
        out = tmp_path_factory.mktemp("flagship_mock")
        _script.main([
            "--mock",
            "--dry-run",
            "--no-pin-versions",
            "--output-dir", str(out),
        ])
        subdirs = [d for d in out.iterdir() if d.is_dir()]
        assert len(subdirs) == 1, f"Expected 1 experiment dir, got {subdirs}"
        return subdirs[0]

    def test_manifest_json_exists(self, exp_dir):
        assert (exp_dir / "manifest.json").exists()

    def test_run_plan_csv_exists(self, exp_dir):
        assert (exp_dir / "run_plan.csv").exists()

    def test_cost_estimate_txt_exists(self, exp_dir):
        assert (exp_dir / "cost_estimate.txt").exists()

    def test_manifest_design_tier_is_flagship(self, exp_dir):
        m = json.loads((exp_dir / "manifest.json").read_text())
        assert m["design_tier"] == "flagship"

    def test_manifest_experiment_id_prefix(self, exp_dir):
        m = json.loads((exp_dir / "manifest.json").read_text())
        assert m["experiment_id"].startswith("pillar2-flagship-")

    def test_manifest_model_is_mock(self, exp_dir):
        m = json.loads((exp_dir / "manifest.json").read_text())
        assert m["models"] == ["mock-agent-v1"]

    def test_manifest_n_runs_per_cell_is_100(self, exp_dir):
        m = json.loads((exp_dir / "manifest.json").read_text())
        assert m["n_runs_per_cell"] == 100

    def test_manifest_temperatures_has_both(self, exp_dir):
        m = json.loads((exp_dir / "manifest.json").read_text())
        assert set(m["temperatures"]) == {0.7, 0.0}

    def test_manifest_prompt_versions_has_both(self, exp_dir):
        m = json.loads((exp_dir / "manifest.json").read_text())
        assert set(m["prompt_versions"]) == {"standard", "cot"}

    def test_manifest_total_planned_runs(self, exp_dir):
        # 1 mock × 17 slots × 2 temps × 2 prompts × 100 runs = 6,800
        m = json.loads((exp_dir / "manifest.json").read_text())
        assert m["total_planned_runs"] == 6800

    def test_run_plan_row_count(self, exp_dir):
        with open(exp_dir / "run_plan.csv") as f:
            rows = list(csv.DictReader(f))
        assert len(rows) == 6800

    def test_run_plan_all_run_ids_unique(self, exp_dir):
        with open(exp_dir / "run_plan.csv") as f:
            run_ids = [row["run_id"] for row in csv.DictReader(f)]
        assert len(run_ids) == len(set(run_ids)), "Duplicate run_ids in flagship plan"

    def test_run_plan_run_ids_are_12_chars(self, exp_dir):
        with open(exp_dir / "run_plan.csv") as f:
            for row in csv.DictReader(f):
                assert len(row["run_id"]) == 12

    def test_run_plan_has_both_temperatures(self, exp_dir):
        with open(exp_dir / "run_plan.csv") as f:
            temps = {float(row["temperature"]) for row in csv.DictReader(f)}
        assert temps == {0.7, 0.0}

    def test_run_plan_has_both_prompt_versions(self, exp_dir):
        with open(exp_dir / "run_plan.csv") as f:
            prompts = {row["prompt_version"] for row in csv.DictReader(f)}
        assert prompts == {"standard", "cot"}

    def test_run_plan_run_index_max_is_100(self, exp_dir):
        with open(exp_dir / "run_plan.csv") as f:
            indices = [int(row["run_index"]) for row in csv.DictReader(f)]
        assert max(indices) == 100

    def test_cost_estimate_is_zero_for_mock(self, exp_dir):
        cost = json.loads((exp_dir / "cost_estimate.txt").read_text())
        assert cost["estimated_total_usd"] == 0.0

    def test_cost_estimate_n_runs(self, exp_dir):
        cost = json.loads((exp_dir / "cost_estimate.txt").read_text())
        assert cost["n_runs"] == 6800


# ── CLI: --skip-gate3 --dry-run ───────────────────────────────────────────────


class TestSkipGate3DryRun:
    @pytest.fixture(scope="class")
    def exp_dir(self, tmp_path_factory):
        out = tmp_path_factory.mktemp("flagship_skip_gate3")
        _script.main([
            "--skip-gate3",
            "--dry-run",
            "--no-pin-versions",
            "--output-dir", str(out),
        ])
        subdirs = [d for d in out.iterdir() if d.is_dir()]
        assert len(subdirs) == 1
        return subdirs[0]

    def test_manifest_exists(self, exp_dir):
        assert (exp_dir / "manifest.json").exists()

    def test_design_tier_is_flagship(self, exp_dir):
        m = json.loads((exp_dir / "manifest.json").read_text())
        assert m["design_tier"] == "flagship"

    def test_real_models_present(self, exp_dir):
        m = json.loads((exp_dir / "manifest.json").read_text())
        assert len(m["models"]) == 10
        assert all(mod.startswith("openrouter-") for mod in m["models"])

    def test_temperatures_has_both(self, exp_dir):
        m = json.loads((exp_dir / "manifest.json").read_text())
        assert set(m["temperatures"]) == {0.7, 0.0}


# ── CLI: --full-dir with cleared gate ────────────────────────────────────────


class TestFullDirClearedGate:
    @pytest.fixture(scope="class")
    def exp_dir(self, tmp_path_factory):
        root = tmp_path_factory.mktemp("flagship_gate_pass")
        full_dir = root / "realistic"
        full_dir.mkdir()
        _make_gate3_json(full_dir, proceed=True)
        out = root / "output"
        out.mkdir()
        _script.main([
            "--full-dir", str(full_dir),
            "--dry-run",
            "--no-pin-versions",
            "--output-dir", str(out),
        ])
        subdirs = [d for d in out.iterdir() if d.is_dir()]
        assert len(subdirs) == 1
        return subdirs[0]

    def test_manifest_exists(self, exp_dir):
        assert (exp_dir / "manifest.json").exists()

    def test_design_tier_is_flagship(self, exp_dir):
        m = json.loads((exp_dir / "manifest.json").read_text())
        assert m["design_tier"] == "flagship"
