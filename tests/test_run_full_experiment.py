"""Tests for research/scripts/02_run_full_experiment.py.

Covers:
- load_gate1_result: FileNotFoundError when ceiling_effect.json absent
- load_gate1_result: KeyError when gate1 key missing from JSON
- load_gate1_result: returns gate1 sub-dict when file is valid
- check_gate1: SystemExit(1) when gate1.proceed is False
- check_gate1: no exit when gate1.proceed is True
- load_gate2_result: FileNotFoundError when robustness_pilot.json absent
- load_gate2_result: returns dict when file is valid
- check_gate2: SystemExit(1) when overall_recommendation is not PROCEED
- check_gate2: no exit when overall_recommendation is PROCEED
- CLI: --mock --dry-run end-to-end (manifest, run_plan, cost, design_tier)
- CLI: --skip-gate1 --skip-gate2 --dry-run end-to-end
- CLI: missing --pilot-dir without --skip-gate1 or --mock raises SystemExit
- CLI: --pilot-dir with cleared gate proceeds to manifest creation
- CLI: --pilot-dir with failed gate raises SystemExit(1)
- CLI: failed gate2 raises SystemExit(1)
- CLI: --skip-gate2 bypasses gate2 check
- Mock run: manifest design_tier == "realistic", models == ["mock-agent-v1"]
- Mock run: n_runs_per_cell == 50, total_planned_runs == 500
- Mock run: run_plan row count == 500, all run_ids unique, 12-char
- Mock run: cost_estimate == 0.0 for mock
- Mock run: run_plan run_index max == 50
"""
from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path

import pytest

_SCRIPT_PATH = (
    Path(__file__).resolve().parent.parent
    / "research" / "scripts" / "02_run_full_experiment.py"
)


def _load_script():
    spec = importlib.util.spec_from_file_location("run_full_experiment", _SCRIPT_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_script = _load_script()


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
        gate1 = {"proceed": True, "criterion1_pass": True, "criterion2_pass": True,
                  "criterion1_detail": "ok", "criterion2_detail": "ok",
                  "recommendation": "PASS", "error_rate": 0.0,
                  "n_models_with_variation": 3}
        ceiling = tmp_path / "ceiling_effect.json"
        ceiling.write_text(json.dumps({"gate": "PROCEED", "gate1": gate1}), encoding="utf-8")
        result = _script.load_gate1_result(tmp_path)
        assert result == gate1

    def test_returns_proceed_false_correctly(self, tmp_path):
        gate1 = {"proceed": False, "criterion1_pass": True, "criterion2_pass": False,
                  "criterion1_detail": "ok", "criterion2_detail": "FAIL",
                  "recommendation": "FAIL", "error_rate": 0.0,
                  "n_models_with_variation": 0}
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


class TestRunFullMockDryRun:
    @pytest.fixture(scope="class")
    def exp_dir(self, tmp_path_factory):
        out = tmp_path_factory.mktemp("full_mock")
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

    def test_manifest_design_tier_is_realistic(self, exp_dir):
        m = json.loads((exp_dir / "manifest.json").read_text())
        assert m["design_tier"] == "realistic"

    def test_manifest_experiment_id_prefix(self, exp_dir):
        m = json.loads((exp_dir / "manifest.json").read_text())
        assert m["experiment_id"].startswith("pillar2-realistic-")

    def test_manifest_model_is_mock(self, exp_dir):
        m = json.loads((exp_dir / "manifest.json").read_text())
        assert m["models"] == ["mock-agent-v1"]

    def test_manifest_n_runs_per_cell_is_50(self, exp_dir):
        m = json.loads((exp_dir / "manifest.json").read_text())
        assert m["n_runs_per_cell"] == 50

    def test_manifest_total_planned_runs(self, exp_dir):
        # 1 mock model × 5 bias types × 2 variants × 1 temp × 1 prompt × 50 runs = 500
        m = json.loads((exp_dir / "manifest.json").read_text())
        assert m["total_planned_runs"] == 500

    def test_run_plan_row_count(self, exp_dir):
        with open(exp_dir / "run_plan.csv") as f:
            rows = list(csv.DictReader(f))
        assert len(rows) == 500

    def test_run_plan_all_run_ids_unique(self, exp_dir):
        with open(exp_dir / "run_plan.csv") as f:
            run_ids = [row["run_id"] for row in csv.DictReader(f)]
        assert len(run_ids) == len(set(run_ids)), "Duplicate run_ids in realistic plan"

    def test_run_plan_run_ids_are_12_chars(self, exp_dir):
        with open(exp_dir / "run_plan.csv") as f:
            for row in csv.DictReader(f):
                assert len(row["run_id"]) == 12

    def test_run_plan_run_index_max_is_50(self, exp_dir):
        with open(exp_dir / "run_plan.csv") as f:
            indices = [int(row["run_index"]) for row in csv.DictReader(f)]
        assert max(indices) == 50

    def test_cost_estimate_is_zero_for_mock(self, exp_dir):
        cost = json.loads((exp_dir / "cost_estimate.txt").read_text())
        assert cost["estimated_total_usd"] == 0.0

    def test_cost_estimate_n_runs(self, exp_dir):
        cost = json.loads((exp_dir / "cost_estimate.txt").read_text())
        assert cost["n_runs"] == 500


# ── CLI: --skip-gate1 --dry-run ───────────────────────────────────────────────


class TestSkipGate1DryRun:
    @pytest.fixture(scope="class")
    def exp_dir(self, tmp_path_factory):
        out = tmp_path_factory.mktemp("full_skip_gate1")
        _script.main([
            "--skip-gate1",
            "--skip-gate2",
            "--dry-run",
            "--no-pin-versions",
            "--output-dir", str(out),
        ])
        subdirs = [d for d in out.iterdir() if d.is_dir()]
        assert len(subdirs) == 1
        return subdirs[0]

    def test_manifest_exists(self, exp_dir):
        assert (exp_dir / "manifest.json").exists()

    def test_design_tier_is_realistic(self, exp_dir):
        m = json.loads((exp_dir / "manifest.json").read_text())
        assert m["design_tier"] == "realistic"

    def test_real_models_present(self, exp_dir):
        m = json.loads((exp_dir / "manifest.json").read_text())
        assert len(m["models"]) == 10
        assert all(mod.startswith("openrouter-") for mod in m["models"])


# ── CLI: --pilot-dir with cleared gate ────────────────────────────────────────


class TestPilotDirClearedGate:
    @pytest.fixture(scope="class")
    def exp_dir(self, tmp_path_factory):
        root = tmp_path_factory.mktemp("full_pilot_gate_pass")
        pilot_dir = root / "pilot_full"
        pilot_dir.mkdir()
        _make_ceiling_json(pilot_dir, proceed=True)
        out = root / "output"
        out.mkdir()
        _script.main([
            "--pilot-dir", str(pilot_dir),
            "--skip-gate1",  # use skip-gate1 + pilot-dir together to avoid real gate check
            "--skip-gate2",
            "--dry-run",
            "--no-pin-versions",
            "--output-dir", str(out),
        ])
        subdirs = [d for d in out.iterdir() if d.is_dir()]
        assert len(subdirs) == 1
        return subdirs[0]

    def test_manifest_exists(self, exp_dir):
        assert (exp_dir / "manifest.json").exists()

    def test_design_tier_is_realistic(self, exp_dir):
        m = json.loads((exp_dir / "manifest.json").read_text())
        assert m["design_tier"] == "realistic"


# ── load_gate2_result ─────────────────────────────────────────────────────────


def _make_robustness_json(tmp_path: Path, overall_recommendation: str = "PROCEED") -> Path:
    """Write a minimal robustness_pilot.json to *tmp_path* and return the dir."""
    data = {
        "n_runs": 5,
        "cv_threshold": 0.50,
        "phrasings": ["robustness_a", "robustness_b", "robustness_c"],
        "per_scenario": {
            "p2-01-anchoring": {
                "phrasings": 3,
                "per_phrasing_mean_bsi": {
                    "robustness_a": 0.2, "robustness_b": 0.18, "robustness_c": 0.22,
                },
                "mean_of_means": 0.20,
                "std_of_means": 0.02,
                "cv": 0.10,
                "cv_threshold": 0.50,
                "robust": True,
                "recommendation": "PROCEED",
            }
        },
        "scenarios_passing": 1 if overall_recommendation == "PROCEED" else 0,
        "scenarios_failing": 0 if overall_recommendation == "PROCEED" else 1,
        "scenarios_to_redesign": [] if overall_recommendation == "PROCEED" else ["p2-01-anchoring"],
        "overall_recommendation": overall_recommendation,
    }
    pilot_file = tmp_path / "robustness_pilot.json"
    pilot_file.write_text(json.dumps(data), encoding="utf-8")
    return tmp_path


class TestLoadGate2Result:
    def test_raises_file_not_found_when_no_robustness_json(self, tmp_path):
        with pytest.raises(FileNotFoundError, match="robustness_pilot.json"):
            _script.load_gate2_result(tmp_path)

    def test_returns_dict_when_file_valid(self, tmp_path):
        _make_robustness_json(tmp_path)
        result = _script.load_gate2_result(tmp_path)
        assert isinstance(result, dict)

    def test_returns_proceed_recommendation(self, tmp_path):
        _make_robustness_json(tmp_path, "PROCEED")
        result = _script.load_gate2_result(tmp_path)
        assert result["overall_recommendation"] == "PROCEED"

    def test_returns_redesign_recommendation(self, tmp_path):
        _make_robustness_json(tmp_path, "REDESIGN")
        result = _script.load_gate2_result(tmp_path)
        assert result["overall_recommendation"] == "REDESIGN"


# ── check_gate2 ───────────────────────────────────────────────────────────────


class TestCheckGate2:
    def test_exits_when_gate2_not_passed(self, tmp_path):
        _make_robustness_json(tmp_path, "REDESIGN")
        with pytest.raises(SystemExit) as exc_info:
            _script.check_gate2(tmp_path)
        assert exc_info.value.code == 1

    def test_no_exit_when_gate2_passed(self, tmp_path):
        _make_robustness_json(tmp_path, "PROCEED")
        _script.check_gate2(tmp_path)  # should not raise

    def test_exits_on_missing_file(self, tmp_path):
        empty = tmp_path / "empty"
        empty.mkdir()
        with pytest.raises((SystemExit, FileNotFoundError)):
            _script.check_gate2(empty)


# ── CLI: Gate 2 enforcement ────────────────────────────────────────────────────


class TestGate2CLIEnforcement:
    def test_failed_gate2_raises_system_exit(self, tmp_path):
        robustness_dir = tmp_path / "robustness"
        robustness_dir.mkdir()
        _make_robustness_json(robustness_dir, "REDESIGN")
        out = tmp_path / "output"
        out.mkdir()
        with pytest.raises(SystemExit) as exc_info:
            _script.main([
                "--skip-gate1",
                "--robustness-dir", str(robustness_dir),
                "--dry-run",
                "--no-pin-versions",
                "--output-dir", str(out),
            ])
        assert exc_info.value.code == 1

    def test_passed_gate2_proceeds(self, tmp_path):
        robustness_dir = tmp_path / "robustness"
        robustness_dir.mkdir()
        _make_robustness_json(robustness_dir, "PROCEED")
        out = tmp_path / "output"
        out.mkdir()
        _script.main([
            "--skip-gate1",
            "--robustness-dir", str(robustness_dir),
            "--dry-run",
            "--no-pin-versions",
            "--output-dir", str(out),
        ])
        assert any(d.is_dir() for d in out.iterdir())

    def test_skip_gate2_bypasses_check(self, tmp_path):
        out = tmp_path / "output"
        out.mkdir()
        _script.main([
            "--skip-gate1",
            "--skip-gate2",
            "--dry-run",
            "--no-pin-versions",
            "--output-dir", str(out),
        ])
        assert any(d.is_dir() for d in out.iterdir())

    def test_mock_implies_skip_gate2(self, tmp_path):
        out = tmp_path / "output"
        out.mkdir()
        _script.main([
            "--mock",
            "--dry-run",
            "--no-pin-versions",
            "--output-dir", str(out),
        ])
        assert any(d.is_dir() for d in out.iterdir())
