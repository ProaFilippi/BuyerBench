"""Tests for research/scripts/05_run_robustness_t0.py.

Covers:
- ROBUSTNESS_T0_DESIGN constants: design_tier, temperatures, n_runs_per_cell, models
- load_gate1_result: FileNotFoundError when ceiling_effect.json absent
- load_gate1_result: KeyError when gate1 key missing from JSON
- load_gate1_result: returns gate1 sub-dict when file is valid
- load_gate1_result: returns proceed=False correctly
- check_gate1: SystemExit(1) when gate1.proceed is False
- check_gate1: no exit when gate1.proceed is True
- CLI: --mock --dry-run end-to-end (manifest, run_plan, cost, design_tier)
- CLI: --skip-gate1 --dry-run end-to-end (no pilot-dir required)
- CLI: missing --pilot-dir without --skip-gate1 or --mock raises SystemExit
- CLI: --pilot-dir with failed gate raises SystemExit(1)
- CLI: --pilot-dir with cleared gate proceeds to manifest creation
- Mock run: design_tier == "robustness_t0", models == ["mock-agent-v1"]
- Mock run: n_runs_per_cell == 30, temperatures == [0.0]
- Mock run: total_planned_runs == 300 (1 × 5 × 2 × 30)
- Mock run: run_plan row count == 300, all run_ids unique, 12-char
- Mock run: all run specs have temperature == 0.0
- Mock run: run_index max == 30
- Mock run: cost_estimate == 0.0 for mock, n_runs == 300
"""
from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path

import pytest

_SCRIPT_PATH = (
    Path(__file__).resolve().parent.parent
    / "research" / "scripts" / "05_run_robustness_t0.py"
)


def _load_script():
    spec = importlib.util.spec_from_file_location("run_robustness_t0", _SCRIPT_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_script = _load_script()


# ── ROBUSTNESS_T0_DESIGN constants ────────────────────────────────────────────


class TestRobustnessT0DesignConstants:
    def setup_method(self):
        import sys
        repo = Path(__file__).resolve().parent.parent
        if str(repo) not in sys.path:
            sys.path.insert(0, str(repo))
        from research.experiments.grid import ROBUSTNESS_T0_DESIGN
        self.design = ROBUSTNESS_T0_DESIGN

    def test_design_tier_is_robustness_t0(self):
        assert self.design["design_tier"] == "robustness_t0"

    def test_temperatures_is_zero(self):
        assert self.design["temperatures"] == [0.0]

    def test_n_runs_per_cell_is_30(self):
        assert self.design["n_runs_per_cell"] == 30

    def test_has_10_real_models(self):
        assert len(self.design["models"]) == 10

    def test_all_models_are_openrouter(self):
        assert all(m.startswith("openrouter-") for m in self.design["models"])

    def test_has_5_bias_types(self):
        assert len(self.design["bias_scenarios"]) == 5

    def test_total_runs_is_3000(self):
        n_models = len(self.design["models"])
        n_bias = len(self.design["bias_scenarios"])
        n_variants = 2
        n_temps = len(self.design["temperatures"])
        n_prompts = len(self.design["prompt_versions"])
        n_runs = self.design["n_runs_per_cell"]
        assert n_models * n_bias * n_variants * n_temps * n_prompts * n_runs == 3000

    def test_design_tier_in_valid_tiers(self):
        from research.experiments.schemas import ExperimentManifest
        valid = ExperimentManifest._VALID_TIERS
        assert "robustness_t0" in valid

    def test_design_in_designs_registry(self):
        from research.experiments.grid import DESIGNS
        assert "robustness_t0" in DESIGNS


# ── load_gate1_result ─────────────────────────────────────────────────────────


class TestLoadGate1Result:
    def test_raises_file_not_found_when_no_ceiling_json(self, tmp_path):
        with pytest.raises(FileNotFoundError, match="ceiling_effect.json"):
            _script.load_gate1_result(tmp_path)

    def test_raises_key_error_when_gate1_key_missing(self, tmp_path):
        ceiling = tmp_path / "ceiling_effect.json"
        ceiling.write_text(json.dumps({"gate": "PROCEED", "n_models": 3}), encoding="utf-8")
        with pytest.raises(KeyError, match="gate1"):
            _script.load_gate1_result(tmp_path)

    def test_returns_gate1_subdict(self, tmp_path):
        gate1 = {
            "proceed": True,
            "criterion1_pass": True,
            "criterion2_pass": True,
            "criterion1_detail": "ok",
            "criterion2_detail": "ok",
            "recommendation": "PASS",
            "error_rate": 0.0,
            "n_models_with_variation": 3,
        }
        ceiling = tmp_path / "ceiling_effect.json"
        ceiling.write_text(json.dumps({"gate": "PROCEED", "gate1": gate1}), encoding="utf-8")
        result = _script.load_gate1_result(tmp_path)
        assert result == gate1

    def test_returns_proceed_false_correctly(self, tmp_path):
        gate1 = {
            "proceed": False,
            "criterion1_pass": True,
            "criterion2_pass": False,
            "criterion1_detail": "ok",
            "criterion2_detail": "FAIL",
            "recommendation": "FAIL",
            "error_rate": 0.0,
            "n_models_with_variation": 0,
        }
        ceiling = tmp_path / "ceiling_effect.json"
        ceiling.write_text(json.dumps({"gate": "CEILING", "gate1": gate1}), encoding="utf-8")
        result = _script.load_gate1_result(tmp_path)
        assert result["proceed"] is False


# ── check_gate1 ───────────────────────────────────────────────────────────────


def _make_ceiling_json(tmp_path: Path, proceed: bool) -> Path:
    gate1 = {
        "proceed": proceed,
        "criterion1_pass": True,
        "criterion2_pass": proceed,
        "criterion1_detail": "Error rate 0.0% (< 5% threshold) — PASS",
        "criterion2_detail": (
            "3 model(s) show mean_BSI > 0.05 on ≥1 bias type (need ≥2) — PASS"
            if proceed
            else "0 model(s) show mean_BSI > 0.05 on ≥1 bias type (need ≥2) — FAIL"
        ),
        "recommendation": "Gate 1 PASSED." if proceed else "Gate 1 FAILED.",
        "error_rate": 0.0,
        "n_models_with_variation": 3 if proceed else 0,
    }
    ceiling = tmp_path / "ceiling_effect.json"
    ceiling.write_text(json.dumps({"gate": "PROCEED", "gate1": gate1}), encoding="utf-8")
    return tmp_path


class TestCheckGate1:
    def test_exits_when_gate1_not_passed(self, tmp_path):
        pilot_dir = _make_ceiling_json(tmp_path, proceed=False)
        with pytest.raises(SystemExit) as exc_info:
            _script.check_gate1(pilot_dir)
        assert exc_info.value.code == 1

    def test_no_exit_when_gate1_passed(self, tmp_path):
        pilot_dir = _make_ceiling_json(tmp_path, proceed=True)
        _script.check_gate1(pilot_dir)  # should not raise


# ── CLI: error conditions ─────────────────────────────────────────────────────


class TestCLIErrorCases:
    def test_missing_pilot_dir_without_flags_raises(self, tmp_path):
        with pytest.raises(SystemExit):
            _script.main([
                "--dry-run",
                "--no-pin-versions",
                "--output-dir", str(tmp_path),
            ])

    def test_pilot_dir_with_failed_gate_raises_system_exit(self, tmp_path):
        pilot_dir = tmp_path / "pilot"
        pilot_dir.mkdir()
        _make_ceiling_json(pilot_dir, proceed=False)
        out = tmp_path / "output"
        out.mkdir()
        with pytest.raises(SystemExit) as exc_info:
            _script.main([
                "--pilot-dir", str(pilot_dir),
                "--dry-run",
                "--no-pin-versions",
                "--output-dir", str(out),
            ])
        assert exc_info.value.code == 1


# ── CLI: --mock --dry-run end-to-end ─────────────────────────────────────────


class TestRunRobustnessT0MockDryRun:
    @pytest.fixture(scope="class")
    def exp_dir(self, tmp_path_factory):
        out = tmp_path_factory.mktemp("robt0_mock")
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

    def test_manifest_design_tier_is_robustness_t0(self, exp_dir):
        m = json.loads((exp_dir / "manifest.json").read_text())
        assert m["design_tier"] == "robustness_t0"

    def test_manifest_experiment_id_prefix(self, exp_dir):
        m = json.loads((exp_dir / "manifest.json").read_text())
        assert m["experiment_id"].startswith("pillar2-robustness_t0-")

    def test_manifest_model_is_mock(self, exp_dir):
        m = json.loads((exp_dir / "manifest.json").read_text())
        assert m["models"] == ["mock-agent-v1"]

    def test_manifest_n_runs_per_cell_is_30(self, exp_dir):
        m = json.loads((exp_dir / "manifest.json").read_text())
        assert m["n_runs_per_cell"] == 30

    def test_manifest_temperatures_is_zero(self, exp_dir):
        m = json.loads((exp_dir / "manifest.json").read_text())
        assert m["temperatures"] == [0.0]

    def test_manifest_total_planned_runs(self, exp_dir):
        # 1 mock model × 5 bias types × 2 variants × 1 temp × 1 prompt × 30 runs = 300
        m = json.loads((exp_dir / "manifest.json").read_text())
        assert m["total_planned_runs"] == 300

    def test_run_plan_row_count(self, exp_dir):
        with open(exp_dir / "run_plan.csv") as f:
            rows = list(csv.DictReader(f))
        assert len(rows) == 300

    def test_run_plan_all_run_ids_unique(self, exp_dir):
        with open(exp_dir / "run_plan.csv") as f:
            run_ids = [row["run_id"] for row in csv.DictReader(f)]
        assert len(run_ids) == len(set(run_ids)), "Duplicate run_ids in robustness_t0 plan"

    def test_run_plan_run_ids_are_12_chars(self, exp_dir):
        with open(exp_dir / "run_plan.csv") as f:
            for row in csv.DictReader(f):
                assert len(row["run_id"]) == 12

    def test_run_plan_all_temperatures_are_zero(self, exp_dir):
        with open(exp_dir / "run_plan.csv") as f:
            for row in csv.DictReader(f):
                assert float(row["temperature"]) == 0.0

    def test_run_plan_run_index_max_is_30(self, exp_dir):
        with open(exp_dir / "run_plan.csv") as f:
            indices = [int(row["run_index"]) for row in csv.DictReader(f)]
        assert max(indices) == 30

    def test_cost_estimate_is_zero_for_mock(self, exp_dir):
        cost = json.loads((exp_dir / "cost_estimate.txt").read_text())
        assert cost["estimated_total_usd"] == 0.0

    def test_cost_estimate_n_runs(self, exp_dir):
        cost = json.loads((exp_dir / "cost_estimate.txt").read_text())
        assert cost["n_runs"] == 300


# ── CLI: --skip-gate1 --dry-run ───────────────────────────────────────────────


class TestSkipGate1DryRun:
    @pytest.fixture(scope="class")
    def exp_dir(self, tmp_path_factory):
        out = tmp_path_factory.mktemp("robt0_skip_gate1")
        _script.main([
            "--skip-gate1",
            "--dry-run",
            "--no-pin-versions",
            "--output-dir", str(out),
        ])
        subdirs = [d for d in out.iterdir() if d.is_dir()]
        assert len(subdirs) == 1
        return subdirs[0]

    def test_manifest_exists(self, exp_dir):
        assert (exp_dir / "manifest.json").exists()

    def test_design_tier_is_robustness_t0(self, exp_dir):
        m = json.loads((exp_dir / "manifest.json").read_text())
        assert m["design_tier"] == "robustness_t0"

    def test_real_models_present(self, exp_dir):
        m = json.loads((exp_dir / "manifest.json").read_text())
        assert len(m["models"]) == 10
        assert all(mod.startswith("openrouter-") for mod in m["models"])

    def test_temperatures_is_zero(self, exp_dir):
        m = json.loads((exp_dir / "manifest.json").read_text())
        assert m["temperatures"] == [0.0]


# ── CLI: --pilot-dir with cleared gate ───────────────────────────────────────


class TestPilotDirClearedGate:
    @pytest.fixture(scope="class")
    def exp_dir(self, tmp_path_factory):
        root = tmp_path_factory.mktemp("robt0_pilot_gate_pass")
        pilot_dir = root / "pilot_full"
        pilot_dir.mkdir()
        _make_ceiling_json(pilot_dir, proceed=True)
        out = root / "output"
        out.mkdir()
        _script.main([
            "--pilot-dir", str(pilot_dir),
            "--skip-gate1",
            "--dry-run",
            "--no-pin-versions",
            "--output-dir", str(out),
        ])
        subdirs = [d for d in out.iterdir() if d.is_dir()]
        assert len(subdirs) == 1
        return subdirs[0]

    def test_manifest_exists(self, exp_dir):
        assert (exp_dir / "manifest.json").exists()

    def test_design_tier_is_robustness_t0(self, exp_dir):
        m = json.loads((exp_dir / "manifest.json").read_text())
        assert m["design_tier"] == "robustness_t0"
