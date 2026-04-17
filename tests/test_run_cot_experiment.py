"""Tests for research/scripts/06_run_cot_experiment.py.

Covers:
- COT_EXPERIMENT_DESIGN constants: design_tier, prompt_versions, n_runs_per_cell, models
- COT_EXPERIMENT_DESIGN in DESIGNS registry
- "cot_experiment" accepted as valid ExperimentManifest design_tier
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
- Mock run: design_tier == "cot_experiment"
- Mock run: prompt_versions == ["standard", "cot", "expert_role"]
- Mock run: n_runs_per_cell == 15
- Mock run: total_planned_runs == 450 (1 × 5 × 2 × 3 × 15)
- Mock run: run_plan row count == 450, all run_ids unique, 12-char
- Mock run: all 3 prompt_versions present in run_plan
- Mock run: run_index max == 15
- Mock run: cost_estimate == 0.0 for mock, n_runs == 450
"""
from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path

import pytest

_SCRIPT_PATH = (
    Path(__file__).resolve().parent.parent
    / "research" / "scripts" / "06_run_cot_experiment.py"
)


def _load_script():
    spec = importlib.util.spec_from_file_location("run_cot_experiment", _SCRIPT_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_script = _load_script()


# ── COT_EXPERIMENT_DESIGN constants ───────────────────────────────────────────


class TestCotExperimentDesignConstants:
    def setup_method(self):
        import sys
        repo = Path(__file__).resolve().parent.parent
        if str(repo) not in sys.path:
            sys.path.insert(0, str(repo))
        from research.experiments.grid import COT_EXPERIMENT_DESIGN
        self.design = COT_EXPERIMENT_DESIGN

    def test_design_tier_is_cot_experiment(self):
        assert self.design["design_tier"] == "cot_experiment"

    def test_prompt_versions_are_all_three(self):
        assert self.design["prompt_versions"] == ["standard", "cot", "expert_role"]

    def test_n_runs_per_cell_is_15(self):
        assert self.design["n_runs_per_cell"] == 15

    def test_has_10_real_models(self):
        assert len(self.design["models"]) == 10

    def test_all_models_are_openrouter(self):
        assert all(m.startswith("openrouter-") for m in self.design["models"])

    def test_has_5_bias_types(self):
        assert len(self.design["bias_scenarios"]) == 5

    def test_temperature_is_point_seven(self):
        assert self.design["temperatures"] == [0.7]

    def test_total_runs_is_4500(self):
        n_models = len(self.design["models"])
        n_biases = len(self.design["bias_scenarios"])
        n_variants = 2
        n_prompt_versions = len(self.design["prompt_versions"])
        n_runs = self.design["n_runs_per_cell"]
        total = n_models * n_biases * n_variants * n_prompt_versions * n_runs
        assert total == 4500

    def test_cost_per_run_is_0_15(self):
        assert self.design["cost_per_run_usd"] == 0.15

    def test_in_designs_registry(self):
        from research.experiments.grid import DESIGNS
        assert "cot_experiment" in DESIGNS

    def test_designs_registry_points_to_correct_design(self):
        from research.experiments.grid import COT_EXPERIMENT_DESIGN, DESIGNS
        assert DESIGNS["cot_experiment"] is COT_EXPERIMENT_DESIGN

    def test_valid_manifest_tier(self):
        from research.experiments.schemas import ExperimentManifest
        m = ExperimentManifest(
            experiment_id="test-cot",
            design_tier="cot_experiment",
            n_models=1,
            n_bias_types=1,
            n_variants_per_bias=2,
            n_runs_per_cell=15,
        )
        assert m.design_tier == "cot_experiment"


# ── Gate 1 load / check ───────────────────────────────────────────────────────


class TestLoadGate1Result:
    def test_missing_file_raises(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            _script.load_gate1_result(tmp_path)

    def test_missing_gate1_key_raises(self, tmp_path):
        (tmp_path / "ceiling_effect.json").write_text(json.dumps({"other": 1}))
        with pytest.raises(KeyError):
            _script.load_gate1_result(tmp_path)

    def test_returns_gate1_sub_dict(self, tmp_path):
        payload = {"gate1": {"proceed": True, "criterion1_detail": "ok", "criterion2_detail": "ok", "recommendation": "PROCEED"}}
        (tmp_path / "ceiling_effect.json").write_text(json.dumps(payload))
        result = _script.load_gate1_result(tmp_path)
        assert result["proceed"] is True

    def test_returns_proceed_false(self, tmp_path):
        payload = {"gate1": {"proceed": False, "criterion1_detail": "fail", "criterion2_detail": "fail", "recommendation": "HOLD"}}
        (tmp_path / "ceiling_effect.json").write_text(json.dumps(payload))
        result = _script.load_gate1_result(tmp_path)
        assert result["proceed"] is False


class TestCheckGate1:
    def _make_gate1_dir(self, tmp_path, proceed: bool) -> Path:
        payload = {
            "gate1": {
                "proceed": proceed,
                "criterion1_detail": "ok" if proceed else "fail",
                "criterion2_detail": "ok" if proceed else "fail",
                "recommendation": "PROCEED" if proceed else "HOLD",
            }
        }
        (tmp_path / "ceiling_effect.json").write_text(json.dumps(payload))
        return tmp_path

    def test_raises_system_exit_when_gate1_not_passed(self, tmp_path):
        d = self._make_gate1_dir(tmp_path, proceed=False)
        with pytest.raises(SystemExit):
            _script.check_gate1(d)

    def test_no_exit_when_gate1_passed(self, tmp_path):
        d = self._make_gate1_dir(tmp_path, proceed=True)
        _script.check_gate1(d)  # must not raise


# ── CLI integration — mock dry-run ────────────────────────────────────────────


class TestCotExperimentCLI:
    def test_missing_pilot_dir_without_skip_raises(self, tmp_path):
        with pytest.raises(SystemExit):
            _script.main(["--output-dir", str(tmp_path)])

    def test_pilot_dir_with_failed_gate_raises(self, tmp_path):
        payload = {"gate1": {"proceed": False, "criterion1_detail": "fail", "criterion2_detail": "fail", "recommendation": "HOLD"}}
        (tmp_path / "ceiling_effect.json").write_text(json.dumps(payload))
        with pytest.raises(SystemExit):
            _script.main(["--pilot-dir", str(tmp_path), "--output-dir", str(tmp_path)])

    def test_pilot_dir_with_cleared_gate_proceeds(self, tmp_path):
        payload = {"gate1": {"proceed": True, "criterion1_detail": "ok", "criterion2_detail": "ok", "recommendation": "PROCEED"}}
        (tmp_path / "ceiling_effect.json").write_text(json.dumps(payload))
        _script.main(["--pilot-dir", str(tmp_path), "--mock", "--dry-run",
                      "--no-pin-versions", "--output-dir", str(tmp_path)])

    def test_skip_gate1_dry_run_no_pilot_dir(self, tmp_path):
        _script.main(["--skip-gate1", "--dry-run", "--no-pin-versions",
                      "--output-dir", str(tmp_path)])

    def test_mock_dry_run_creates_manifest(self, tmp_path):
        _script.main(["--mock", "--dry-run", "--no-pin-versions", "--output-dir", str(tmp_path)])
        manifests = list(tmp_path.glob("**/manifest.json"))
        assert len(manifests) == 1

    def test_mock_dry_run_design_tier(self, tmp_path):
        _script.main(["--mock", "--dry-run", "--no-pin-versions", "--output-dir", str(tmp_path)])
        manifest = json.loads(next(tmp_path.glob("**/manifest.json")).read_text())
        assert manifest["design_tier"] == "cot_experiment"

    def test_mock_dry_run_prompt_versions(self, tmp_path):
        _script.main(["--mock", "--dry-run", "--no-pin-versions", "--output-dir", str(tmp_path)])
        manifest = json.loads(next(tmp_path.glob("**/manifest.json")).read_text())
        assert manifest["prompt_versions"] == ["standard", "cot", "expert_role"]

    def test_mock_dry_run_n_runs_per_cell(self, tmp_path):
        _script.main(["--mock", "--dry-run", "--no-pin-versions", "--output-dir", str(tmp_path)])
        manifest = json.loads(next(tmp_path.glob("**/manifest.json")).read_text())
        assert manifest["n_runs_per_cell"] == 15

    def test_mock_dry_run_run_plan_row_count(self, tmp_path):
        _script.main(["--mock", "--dry-run", "--no-pin-versions", "--output-dir", str(tmp_path)])
        run_plan = next(tmp_path.glob("**/run_plan.csv"))
        with open(run_plan, newline="") as fh:
            rows = list(csv.DictReader(fh))
        # 1 mock model × 5 bias × 2 variants × 3 prompt_versions × 15 runs = 450
        assert len(rows) == 450

    def test_mock_dry_run_all_run_ids_unique(self, tmp_path):
        _script.main(["--mock", "--dry-run", "--no-pin-versions", "--output-dir", str(tmp_path)])
        run_plan = next(tmp_path.glob("**/run_plan.csv"))
        with open(run_plan, newline="") as fh:
            rows = list(csv.DictReader(fh))
        run_ids = [r["run_id"] for r in rows]
        assert len(run_ids) == len(set(run_ids))

    def test_mock_dry_run_run_ids_are_12_chars(self, tmp_path):
        _script.main(["--mock", "--dry-run", "--no-pin-versions", "--output-dir", str(tmp_path)])
        run_plan = next(tmp_path.glob("**/run_plan.csv"))
        with open(run_plan, newline="") as fh:
            rows = list(csv.DictReader(fh))
        assert all(len(r["run_id"]) == 12 for r in rows)

    def test_mock_dry_run_all_prompt_versions_present(self, tmp_path):
        _script.main(["--mock", "--dry-run", "--no-pin-versions", "--output-dir", str(tmp_path)])
        run_plan = next(tmp_path.glob("**/run_plan.csv"))
        with open(run_plan, newline="") as fh:
            rows = list(csv.DictReader(fh))
        pv_found = {r["prompt_version"] for r in rows}
        assert pv_found == {"standard", "cot", "expert_role"}

    def test_mock_dry_run_max_run_index_is_15(self, tmp_path):
        _script.main(["--mock", "--dry-run", "--no-pin-versions", "--output-dir", str(tmp_path)])
        run_plan = next(tmp_path.glob("**/run_plan.csv"))
        with open(run_plan, newline="") as fh:
            rows = list(csv.DictReader(fh))
        assert max(int(r["run_index"]) for r in rows) == 15

    def test_mock_dry_run_cost_is_zero(self, tmp_path):
        _script.main(["--mock", "--dry-run", "--no-pin-versions", "--output-dir", str(tmp_path)])
        cost_file = next(tmp_path.glob("**/cost_estimate.txt"))
        cost = json.loads(cost_file.read_text())
        assert cost["estimated_total_usd"] == 0.0
        assert cost["n_runs"] == 450

    def test_skip_gate1_dry_run_has_real_models(self, tmp_path):
        _script.main(["--skip-gate1", "--dry-run", "--no-pin-versions", "--output-dir", str(tmp_path)])
        manifest = json.loads(next(tmp_path.glob("**/manifest.json")).read_text())
        assert all(m.startswith("openrouter-") for m in manifest["models"])
