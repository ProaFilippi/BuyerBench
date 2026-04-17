"""Tests for research/scripts/00_define_experiment.py.

The design constants (REALISTIC_DESIGN, FLAGSHIP_DESIGN, DESIGNS) are defined in
``research/experiments/grid.py`` and re-exported by the script.  Tests import
from ``grid.py`` directly to avoid the digit-prefix import limitation.

The ``main()`` orchestration function is loaded via ``importlib`` since
``00_define_experiment.py`` cannot be imported as a standard Python identifier.

Covers:
- grid.py: REALISTIC_DESIGN and FLAGSHIP_DESIGN constant integrity
- main(): end-to-end output for both design tiers (offline, --no-pin-versions)
- Correct output files: manifest.json, run_plan.csv, cost_estimate.txt
- Experiment directory layout: raw/, figures/, tables/ sub-directories
- Run-plan count arithmetic: 10 × 5 × 2 × 1 × 1 × 50 = 5,000 (realistic)
- Manifest field consistency (n_models, total_planned_runs, design_tier, git_commit_hash)
- Duplicate run_id check: every run in the plan has a unique 12-char run_id
"""
from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path

import pytest

# Import constants from the importable grid module.
from research.experiments.grid import DESIGNS, FLAGSHIP_DESIGN, PILOT_DESIGN, REALISTIC_DESIGN


# ── Load the script module via importlib (digit-prefix filename) ──────────────

_SCRIPT_PATH = (
    Path(__file__).resolve().parent.parent
    / "research" / "scripts" / "00_define_experiment.py"
)


def _load_script():
    spec = importlib.util.spec_from_file_location("define_experiment", _SCRIPT_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_script = _load_script()


# ── Helpers ───────────────────────────────────────────────────────────────────


def run_main(design: str, tmp_path: Path) -> Path:
    """Call main() with --no-pin-versions and return the experiment directory."""
    out_dir = tmp_path / "experiments"
    _script.main(["--design", design, "--output-dir", str(out_dir), "--no-pin-versions"])
    subdirs = [d for d in out_dir.iterdir() if d.is_dir()]
    assert len(subdirs) == 1, f"Expected 1 experiment dir, got {subdirs}"
    return subdirs[0]


# ── Design constants ──────────────────────────────────────────────────────────


class TestDesignConstants:
    def test_realistic_has_ten_models(self):
        assert len(REALISTIC_DESIGN["models"]) == 10

    def test_realistic_has_five_bias_types(self):
        assert len(REALISTIC_DESIGN["bias_scenarios"]) == 5

    def test_realistic_each_bias_has_baseline_and_treatment(self):
        for bias, variants in REALISTIC_DESIGN["bias_scenarios"].items():
            assert "baseline" in variants, f"{bias} missing 'baseline'"
            assert "treatment" in variants, f"{bias} missing 'treatment'"

    def test_realistic_n_runs_per_cell(self):
        assert REALISTIC_DESIGN["n_runs_per_cell"] == 50

    def test_realistic_primary_temperature(self):
        assert 0.7 in REALISTIC_DESIGN["temperatures"]

    def test_realistic_prompt_versions_contains_standard(self):
        assert "standard" in REALISTIC_DESIGN["prompt_versions"]

    def test_flagship_shares_same_models(self):
        assert set(REALISTIC_DESIGN["models"]) == set(FLAGSHIP_DESIGN["models"])

    def test_flagship_has_more_runs_per_cell(self):
        assert FLAGSHIP_DESIGN["n_runs_per_cell"] > REALISTIC_DESIGN["n_runs_per_cell"]

    def test_flagship_has_extra_temperature(self):
        assert len(FLAGSHIP_DESIGN["temperatures"]) > len(REALISTIC_DESIGN["temperatures"])

    def test_flagship_has_extra_prompt_versions(self):
        assert len(FLAGSHIP_DESIGN["prompt_versions"]) > len(REALISTIC_DESIGN["prompt_versions"])

    def test_all_model_ids_are_openrouter(self):
        for model in REALISTIC_DESIGN["models"]:
            assert model.startswith("openrouter-"), f"Unexpected model id: {model}"

    def test_designs_dict_contains_all_tiers(self):
        assert "realistic" in DESIGNS
        assert "flagship" in DESIGNS
        assert "pilot_full" in DESIGNS
        assert "pilot" in DESIGNS

    def test_designs_dict_values_are_correct(self):
        from research.experiments.grid import PILOT_FULL_DESIGN
        assert DESIGNS["realistic"] is REALISTIC_DESIGN
        assert DESIGNS["flagship"] is FLAGSHIP_DESIGN
        assert DESIGNS["pilot_full"] is PILOT_FULL_DESIGN
        assert DESIGNS["pilot"] is PILOT_DESIGN

    def test_anchoring_scenario_ids_match_actual_files(self):
        anchoring = REALISTIC_DESIGN["bias_scenarios"]["anchoring"]
        assert anchoring["baseline"] == "p2-01-anchor-high-BASELINE"
        assert anchoring["treatment"] == "p2-01-anchor-high-ANCHOR_HIGH"

    def test_framing_scenario_ids_match_actual_files(self):
        framing = REALISTIC_DESIGN["bias_scenarios"]["framing"]
        assert framing["baseline"] == "p2-02-framing-GAIN"
        assert framing["treatment"] == "p2-02-framing-LOSS"

    def test_scenario_ids_are_strings(self):
        for bias, variants in REALISTIC_DESIGN["bias_scenarios"].items():
            for variant, scenario_id in variants.items():
                assert isinstance(scenario_id, str) and scenario_id, (
                    f"{bias}.{variant} has empty/invalid scenario_id"
                )


# ── main() end-to-end: realistic design ──────────────────────────────────────


class TestMainRealistic:
    @pytest.fixture(scope="class")
    def exp_dir(self, tmp_path_factory):
        out = tmp_path_factory.mktemp("realistic_exp")
        return run_main("realistic", out)

    def test_manifest_json_exists(self, exp_dir):
        assert (exp_dir / "manifest.json").exists()

    def test_run_plan_csv_exists(self, exp_dir):
        assert (exp_dir / "run_plan.csv").exists()

    def test_cost_estimate_txt_exists(self, exp_dir):
        assert (exp_dir / "cost_estimate.txt").exists()

    def test_subdirectories_created(self, exp_dir):
        for subdir in ("raw", "figures", "tables"):
            assert (exp_dir / subdir).is_dir(), f"Missing subdir: {subdir}"

    def test_manifest_design_tier(self, exp_dir):
        m = json.loads((exp_dir / "manifest.json").read_text())
        assert m["design_tier"] == "realistic"

    def test_manifest_n_models(self, exp_dir):
        m = json.loads((exp_dir / "manifest.json").read_text())
        assert m["n_models"] == 10

    def test_manifest_total_planned_runs(self, exp_dir):
        m = json.loads((exp_dir / "manifest.json").read_text())
        # 10 models × 5 bias types × 2 variants × 1 temp × 1 prompt × 50 runs
        assert m["total_planned_runs"] == 5000

    def test_manifest_has_git_commit_hash(self, exp_dir):
        m = json.loads((exp_dir / "manifest.json").read_text())
        assert m["git_commit_hash"] not in ("", None)

    def test_manifest_experiment_id_prefix(self, exp_dir):
        m = json.loads((exp_dir / "manifest.json").read_text())
        assert m["experiment_id"].startswith("pillar2-realistic-")

    def test_manifest_pinned_versions_is_dict(self, exp_dir):
        m = json.loads((exp_dir / "manifest.json").read_text())
        assert isinstance(m.get("pinned_model_versions", {}), dict)

    def test_run_plan_row_count(self, exp_dir):
        with open(exp_dir / "run_plan.csv") as f:
            rows = list(csv.DictReader(f))
        assert len(rows) == 5000

    def test_run_plan_required_columns(self, exp_dir):
        with open(exp_dir / "run_plan.csv") as f:
            columns = set(csv.DictReader(f).fieldnames or [])
        expected = {
            "run_id", "agent_id", "scenario_id", "bias_category",
            "variant", "run_index", "temperature", "prompt_version",
            "supplier_order_seed",
        }
        assert expected.issubset(columns)

    def test_run_plan_all_run_ids_unique(self, exp_dir):
        with open(exp_dir / "run_plan.csv") as f:
            run_ids = [row["run_id"] for row in csv.DictReader(f)]
        assert len(run_ids) == len(set(run_ids)), "Duplicate run_ids detected"

    def test_run_plan_run_ids_are_12_chars(self, exp_dir):
        with open(exp_dir / "run_plan.csv") as f:
            for row in csv.DictReader(f):
                assert len(row["run_id"]) == 12

    def test_run_plan_run_index_range(self, exp_dir):
        with open(exp_dir / "run_plan.csv") as f:
            indices = [int(row["run_index"]) for row in csv.DictReader(f)]
        assert min(indices) == 1
        assert max(indices) == 50

    def test_run_plan_covers_all_models(self, exp_dir):
        with open(exp_dir / "run_plan.csv") as f:
            agents = {row["agent_id"] for row in csv.DictReader(f)}
        assert agents == set(REALISTIC_DESIGN["models"])

    def test_run_plan_covers_all_bias_categories(self, exp_dir):
        with open(exp_dir / "run_plan.csv") as f:
            biases = {row["bias_category"] for row in csv.DictReader(f)}
        assert biases == set(REALISTIC_DESIGN["bias_scenarios"].keys())

    def test_run_plan_covers_both_variants(self, exp_dir):
        with open(exp_dir / "run_plan.csv") as f:
            variants = {row["variant"] for row in csv.DictReader(f)}
        assert variants == {"baseline", "treatment"}

    def test_cost_estimate_total(self, exp_dir):
        cost = json.loads((exp_dir / "cost_estimate.txt").read_text())
        assert cost["n_runs"] == 5000
        assert abs(cost["estimated_total_usd"] - 750.0) < 0.01

    def test_cost_estimate_has_note(self, exp_dir):
        cost = json.loads((exp_dir / "cost_estimate.txt").read_text())
        assert "note" in cost and cost["note"]


# ── main() end-to-end: flagship design ───────────────────────────────────────


class TestMainFlagship:
    @pytest.fixture(scope="class")
    def exp_dir(self, tmp_path_factory):
        out = tmp_path_factory.mktemp("flagship_exp")
        return run_main("flagship", out)

    def test_manifest_design_tier(self, exp_dir):
        m = json.loads((exp_dir / "manifest.json").read_text())
        assert m["design_tier"] == "flagship"

    def test_manifest_experiment_id_prefix(self, exp_dir):
        m = json.loads((exp_dir / "manifest.json").read_text())
        assert m["experiment_id"].startswith("pillar2-flagship-")

    def test_manifest_total_planned_runs(self, exp_dir):
        m = json.loads((exp_dir / "manifest.json").read_text())
        # 10 × 5 × 2 × 2 temps × 2 prompt_versions × 100 = 40,000
        assert m["total_planned_runs"] == 40000

    def test_run_plan_row_count(self, exp_dir):
        with open(exp_dir / "run_plan.csv") as f:
            rows = list(csv.DictReader(f))
        assert len(rows) == 40000

    def test_run_plan_all_run_ids_unique(self, exp_dir):
        with open(exp_dir / "run_plan.csv") as f:
            run_ids = [row["run_id"] for row in csv.DictReader(f)]
        assert len(run_ids) == len(set(run_ids))

    def test_cost_estimate_uses_flagship_rate(self, exp_dir):
        cost = json.loads((exp_dir / "cost_estimate.txt").read_text())
        # Flagship uses $0.20/run
        assert abs(cost["estimated_total_usd"] - 40000 * 0.20) < 0.01


# ── main() end-to-end: pilot design ─────────────────────────────────────────


class TestMainPilot:
    @pytest.fixture(scope="class")
    def exp_dir(self, tmp_path_factory):
        out = tmp_path_factory.mktemp("pilot_exp")
        return run_main("pilot", out)

    def test_manifest_design_tier(self, exp_dir):
        m = json.loads((exp_dir / "manifest.json").read_text())
        assert m["design_tier"] == "pilot"

    def test_manifest_experiment_id_prefix(self, exp_dir):
        m = json.loads((exp_dir / "manifest.json").read_text())
        assert m["experiment_id"].startswith("pillar2-pilot-")

    def test_manifest_single_mock_model(self, exp_dir):
        m = json.loads((exp_dir / "manifest.json").read_text())
        assert m["models"] == ["mock-agent-v1"]

    def test_manifest_n_runs_per_cell(self, exp_dir):
        m = json.loads((exp_dir / "manifest.json").read_text())
        assert m["n_runs_per_cell"] == 5

    def test_manifest_total_planned_runs(self, exp_dir):
        m = json.loads((exp_dir / "manifest.json").read_text())
        # 1 model × 5 bias types × 2 variants × 1 temp × 1 prompt × 5 runs = 50
        assert m["total_planned_runs"] == 50

    def test_run_plan_row_count(self, exp_dir):
        with open(exp_dir / "run_plan.csv") as f:
            rows = list(csv.DictReader(f))
        assert len(rows) == 50

    def test_run_plan_all_run_ids_unique(self, exp_dir):
        with open(exp_dir / "run_plan.csv") as f:
            run_ids = [row["run_id"] for row in csv.DictReader(f)]
        assert len(run_ids) == len(set(run_ids))

    def test_run_plan_agent_is_mock(self, exp_dir):
        with open(exp_dir / "run_plan.csv") as f:
            agents = {row["agent_id"] for row in csv.DictReader(f)}
        assert agents == {"mock-agent-v1"}

    def test_cost_estimate_is_zero(self, exp_dir):
        cost = json.loads((exp_dir / "cost_estimate.txt").read_text())
        assert cost["estimated_total_usd"] == 0.0


# ── Design constants: pilot ───────────────────────────────────────────────────


class TestPilotDesignConstants:
    def test_pilot_has_one_model(self):
        assert len(PILOT_DESIGN["models"]) == 1
        assert PILOT_DESIGN["models"][0] == "mock-agent-v1"

    def test_pilot_n_runs_per_cell_is_5(self):
        assert PILOT_DESIGN["n_runs_per_cell"] == 5

    def test_pilot_cost_is_zero(self):
        assert PILOT_DESIGN["cost_per_run_usd"] == 0.0

    def test_pilot_design_tier(self):
        assert PILOT_DESIGN["design_tier"] == "pilot"

    def test_pilot_shares_bias_scenarios_with_realistic(self):
        assert PILOT_DESIGN["bias_scenarios"] == REALISTIC_DESIGN["bias_scenarios"]


# ── Duplicate-manifest protection ────────────────────────────────────────────


def test_freeze_manifest_raises_on_duplicate(tmp_path):
    """Running main() twice with same experiment_id raises FileExistsError."""
    from research.experiments.manifest import create_manifest, freeze_manifest

    m = create_manifest(REALISTIC_DESIGN, pin_model_versions=False)
    out_dir = tmp_path / "dup_test"
    freeze_manifest(m, out_dir)

    with pytest.raises(FileExistsError):
        freeze_manifest(m, out_dir)
