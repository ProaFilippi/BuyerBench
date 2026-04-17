"""Tests for PILOT_FULL_DESIGN and the pilot_full design tier.

Covers:
- PILOT_FULL_DESIGN constant integrity (grid.py)
- ExperimentManifest accepts 'pilot_full' as design_tier
- ExperimentManifest rejects unknown tiers
- Grid arithmetic: 10 × 5 × 2 × 1 temp × 1 prompt × 30 = 3,000 runs
- DESIGNS registry contains pilot_full
- 01_run_pilot_full.py --mock --dry-run: manifest, run_plan, cost output
- Run-plan uniqueness and column coverage for pilot_full
- Cost estimate: 3,000 × $0.15 = $450 (real), 0 (mock)
"""
from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path

import pytest

from research.experiments.grid import DESIGNS, PILOT_FULL_DESIGN, REALISTIC_DESIGN
from research.experiments.schemas import ExperimentManifest


# ── PILOT_FULL_DESIGN constants ───────────────────────────────────────────────


class TestPilotFullDesignConstants:
    def test_design_tier_is_pilot_full(self):
        assert PILOT_FULL_DESIGN["design_tier"] == "pilot_full"

    def test_n_runs_per_cell_is_30(self):
        assert PILOT_FULL_DESIGN["n_runs_per_cell"] == 30

    def test_has_ten_real_models(self):
        assert len(PILOT_FULL_DESIGN["models"]) == 10

    def test_all_models_are_openrouter(self):
        for m in PILOT_FULL_DESIGN["models"]:
            assert m.startswith("openrouter-"), f"Unexpected model: {m}"

    def test_same_bias_scenarios_as_realistic(self):
        assert PILOT_FULL_DESIGN["bias_scenarios"] == REALISTIC_DESIGN["bias_scenarios"]

    def test_same_temperatures_as_realistic(self):
        assert PILOT_FULL_DESIGN["temperatures"] == REALISTIC_DESIGN["temperatures"]

    def test_same_prompt_versions_as_realistic(self):
        assert PILOT_FULL_DESIGN["prompt_versions"] == REALISTIC_DESIGN["prompt_versions"]

    def test_cost_per_run_usd(self):
        assert PILOT_FULL_DESIGN["cost_per_run_usd"] == 0.15

    def test_designs_registry_contains_pilot_full(self):
        assert "pilot_full" in DESIGNS

    def test_designs_registry_pilot_full_is_correct(self):
        assert DESIGNS["pilot_full"] is PILOT_FULL_DESIGN

    def test_total_runs_arithmetic(self):
        # 10 models × 5 bias types × 2 variants × 1 temp × 1 prompt × 30 runs
        n = (
            len(PILOT_FULL_DESIGN["models"])
            * len(PILOT_FULL_DESIGN["bias_scenarios"])
            * 2  # variants per bias
            * len(PILOT_FULL_DESIGN["temperatures"])
            * len(PILOT_FULL_DESIGN["prompt_versions"])
            * PILOT_FULL_DESIGN["n_runs_per_cell"]
        )
        assert n == 3000

    def test_estimated_cost(self):
        n = 3000
        cost = n * PILOT_FULL_DESIGN["cost_per_run_usd"]
        assert abs(cost - 450.0) < 0.01


# ── ExperimentManifest validation ─────────────────────────────────────────────


class TestExperimentManifestPilotFull:
    def _base_kwargs(self, tier: str) -> dict:
        return dict(
            experiment_id=f"pillar2-{tier}-20260417-120000",
            design_tier=tier,
            n_models=10,
            n_bias_types=5,
            n_variants_per_bias=2,
            n_runs_per_cell=30,
            temperatures=[0.7],
            prompt_versions=["standard"],
            models=list(PILOT_FULL_DESIGN["models"]),
            bias_scenarios=dict(PILOT_FULL_DESIGN["bias_scenarios"]),
            total_planned_runs=3000,
            total_completed_runs=0,
            total_api_cost_usd=0.0,
            git_commit_hash="abc123",
        )

    def test_pilot_full_tier_accepted(self):
        m = ExperimentManifest(**self._base_kwargs("pilot_full"))
        assert m.design_tier == "pilot_full"

    def test_realistic_tier_still_accepted(self):
        kw = self._base_kwargs("realistic")
        kw["n_runs_per_cell"] = 50
        kw["total_planned_runs"] = 5000
        m = ExperimentManifest(**kw)
        assert m.design_tier == "realistic"

    def test_flagship_tier_still_accepted(self):
        kw = self._base_kwargs("flagship")
        kw["n_runs_per_cell"] = 100
        kw["total_planned_runs"] = 40000
        m = ExperimentManifest(**kw)
        assert m.design_tier == "flagship"

    def test_pilot_tier_still_accepted(self):
        kw = self._base_kwargs("pilot")
        kw["n_models"] = 1
        kw["n_runs_per_cell"] = 5
        kw["total_planned_runs"] = 50
        m = ExperimentManifest(**kw)
        assert m.design_tier == "pilot"

    def test_unknown_tier_raises_value_error(self):
        with pytest.raises(ValueError, match="design_tier"):
            ExperimentManifest(**self._base_kwargs("unknown_tier"))

    def test_experiment_id_uses_design_tier(self):
        m = ExperimentManifest(**self._base_kwargs("pilot_full"))
        assert "pilot_full" in m.experiment_id


# ── 01_run_pilot_full.py: mock dry-run end-to-end ────────────────────────────

_SCRIPT_PATH = (
    Path(__file__).resolve().parent.parent
    / "research" / "scripts" / "01_run_pilot_full.py"
)


def _load_script():
    spec = importlib.util.spec_from_file_location("run_pilot_full", _SCRIPT_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_script = _load_script()


class TestRunPilotFullScript:
    @pytest.fixture(scope="class")
    def exp_dir(self, tmp_path_factory):
        out = tmp_path_factory.mktemp("pilot_full_mock")
        _script.main(
            [
                "--mock",
                "--dry-run",
                "--no-pin-versions",
                "--output-dir", str(out),
            ]
        )
        # dry-run writes manifest + run_plan but does NOT execute models
        subdirs = [d for d in out.iterdir() if d.is_dir()]
        assert len(subdirs) == 1, f"Expected 1 experiment dir, got {subdirs}"
        return subdirs[0]

    def test_manifest_json_exists(self, exp_dir):
        assert (exp_dir / "manifest.json").exists()

    def test_run_plan_csv_exists(self, exp_dir):
        assert (exp_dir / "run_plan.csv").exists()

    def test_cost_estimate_txt_exists(self, exp_dir):
        assert (exp_dir / "cost_estimate.txt").exists()

    def test_manifest_design_tier(self, exp_dir):
        m = json.loads((exp_dir / "manifest.json").read_text())
        assert m["design_tier"] == "pilot_full"

    def test_manifest_experiment_id_prefix(self, exp_dir):
        m = json.loads((exp_dir / "manifest.json").read_text())
        assert m["experiment_id"].startswith("pillar2-pilot_full-")

    def test_manifest_model_is_mock(self, exp_dir):
        m = json.loads((exp_dir / "manifest.json").read_text())
        assert m["models"] == ["mock-agent-v1"]

    def test_manifest_n_runs_per_cell(self, exp_dir):
        m = json.loads((exp_dir / "manifest.json").read_text())
        assert m["n_runs_per_cell"] == 30

    def test_manifest_total_planned_runs(self, exp_dir):
        m = json.loads((exp_dir / "manifest.json").read_text())
        # 1 mock model × 5 bias types × 2 variants × 1 temp × 1 prompt × 30 runs = 300
        assert m["total_planned_runs"] == 300

    def test_run_plan_row_count(self, exp_dir):
        with open(exp_dir / "run_plan.csv") as f:
            rows = list(csv.DictReader(f))
        assert len(rows) == 300

    def test_run_plan_all_run_ids_unique(self, exp_dir):
        with open(exp_dir / "run_plan.csv") as f:
            run_ids = [row["run_id"] for row in csv.DictReader(f)]
        assert len(run_ids) == len(set(run_ids)), "Duplicate run_ids in pilot_full plan"

    def test_run_plan_run_ids_are_12_chars(self, exp_dir):
        with open(exp_dir / "run_plan.csv") as f:
            for row in csv.DictReader(f):
                assert len(row["run_id"]) == 12

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
