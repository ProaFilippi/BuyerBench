"""Tests for research/scripts/04_generate_figures.py.

Covers:
- load_runs_df: loads valid JSONL
- load_runs_df: normalises variant to uppercase
- load_runs_df: drops error rows
- load_runs_df: drops null-BSI rows
- load_runs_df: raises FileNotFoundError for missing directory
- load_runs_df: raises ValueError for empty JSONL
- load_runs_df: tolerates malformed lines
- build_cell_df: has required columns (agent_id, bias_category, mean_bsi, std_bsi, n_runs)
- build_cell_df: has CI columns (ci_lower_95, ci_upper_95)
- build_cell_df: has treatment_effect column
- build_cell_df: n_cells == n_agents × n_biases
- build_cell_df: mean_bsi is average across all variants
- build_cell_df: treatment_effect is treatment minus baseline
- build_cell_df: ci_lower_95 <= mean_bsi <= ci_upper_95
- load_regression_results: returns None when file absent
- load_regression_results: loads JSON when present
- load_p1_scores: returns None for None path
- load_p1_scores: returns None for missing file
- load_p1_scores: loads valid JSON
- gen_fig1: writes fig1-bsi-heatmap.png
- gen_fig2: skips without p1_scores
- gen_fig2: skips when fewer than 3 models have p1 scores
- gen_fig3: writes fig3-bsi-distributions.png
- gen_fig4a: skips without variance_decomposition
- gen_fig4a: writes fig4a-variance-decomp.png with valid data
- gen_fig4b: skips when no treatment_effect data
- gen_fig4b: writes fig4b-treatment-effects.png
- CLI: --dry-run does not write PNG files
- CLI: --mock resolves to mock pilot directory
- CLI: missing --experiment-dir exits with error
- CLI: fig4b written when treatment data present
"""
from __future__ import annotations

import importlib.util
import json
import math
import sys
from pathlib import Path

import pytest

_SCRIPT_PATH = (
    Path(__file__).resolve().parent.parent
    / "research" / "scripts" / "04_generate_figures.py"
)


def _load_script():
    spec = importlib.util.spec_from_file_location("generate_figures", _SCRIPT_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_script = _load_script()

_pandas_available = _script._PANDAS_AVAILABLE
_matplotlib_available = _script._MATPLOTLIB_AVAILABLE

pandas_required = pytest.mark.skipif(
    not _pandas_available, reason="pandas not installed"
)
matplotlib_required = pytest.mark.skipif(
    not _matplotlib_available or not _pandas_available,
    reason="matplotlib or pandas not installed",
)


# ── Fixtures / helpers ────────────────────────────────────────────────────────

_BIAS_TYPES = ["anchoring", "framing", "decoy", "scarcity", "sunk_cost"]
_MOCK_AGENT = "mock-agent-v1"
_VARIANTS_TREATMENT = [
    "ANCHOR_HIGH", "LOSS", "DECOY_C", "SCARCITY_CUE", "SUNK_COST_VARIANT",
]


def _make_run(
    bias_category: str,
    variant: str,
    bsi: float = 0.0,
    agent_id: str = _MOCK_AGENT,
    error_flag: bool = False,
    null_bsi: bool = False,
) -> dict:
    return {
        "run_id": f"{agent_id}-{bias_category}-{variant}",
        "agent_id": agent_id,
        "bias_category": bias_category,
        "variant": variant,
        "bsi": None if null_bsi else bsi,
        "optimality_gap": 0.0,
        "choice_is_correct": bsi == 0.0,
        "error_flag": error_flag,
        "error_message": None,
        "temperature": 0.7,
        "run_index": 1,
        "prompt_version": "standard",
    }


def _make_experiment_dir(tmp_path: Path, runs: list[dict]) -> Path:
    exp_dir = tmp_path / "mock_experiment"
    exp_dir.mkdir(exist_ok=True)
    jsonl = exp_dir / "runs.jsonl"
    with open(jsonl, "w") as fh:
        for r in runs:
            fh.write(json.dumps(r) + "\n")
    return exp_dir


def _minimal_runs() -> list[dict]:
    """One baseline (bsi=0.0) + one treatment (bsi=0.5) per bias type."""
    rows = []
    for bias, treatment_variant in zip(_BIAS_TYPES, _VARIANTS_TREATMENT):
        rows.append(_make_run(bias, "BASELINE", bsi=0.0))
        rows.append(_make_run(bias, treatment_variant, bsi=0.5))
    return rows


# ── TestLoadRunsDf ────────────────────────────────────────────────────────────


@pandas_required
class TestLoadRunsDf:
    def test_loads_valid_jsonl(self, tmp_path):
        exp_dir = _make_experiment_dir(tmp_path, _minimal_runs())
        df = _script.load_runs_df(exp_dir)
        assert len(df) == len(_minimal_runs())

    def test_variant_normalised_to_uppercase(self, tmp_path):
        runs = [_make_run("anchoring", "baseline", bsi=0.0)]
        exp_dir = _make_experiment_dir(tmp_path, runs)
        df = _script.load_runs_df(exp_dir)
        assert df["variant"].iloc[0] == "BASELINE"

    def test_drops_error_rows(self, tmp_path):
        runs = _minimal_runs() + [_make_run("anchoring", "BASELINE", error_flag=True)]
        exp_dir = _make_experiment_dir(tmp_path, runs)
        df = _script.load_runs_df(exp_dir)
        assert len(df) == len(_minimal_runs())

    def test_drops_null_bsi_rows(self, tmp_path):
        runs = _minimal_runs() + [_make_run("anchoring", "BASELINE", null_bsi=True)]
        exp_dir = _make_experiment_dir(tmp_path, runs)
        df = _script.load_runs_df(exp_dir)
        assert df["bsi"].isna().sum() == 0

    def test_raises_file_not_found(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            _script.load_runs_df(tmp_path / "nonexistent")

    def test_raises_on_empty_jsonl(self, tmp_path):
        exp_dir = tmp_path / "empty_exp"
        exp_dir.mkdir()
        (exp_dir / "runs.jsonl").write_text("")
        with pytest.raises(ValueError):
            _script.load_runs_df(exp_dir)

    def test_tolerates_malformed_lines(self, tmp_path):
        exp_dir = tmp_path / "malformed"
        exp_dir.mkdir()
        with open(exp_dir / "runs.jsonl", "w") as fh:
            fh.write("not json\n")
            fh.write(json.dumps(_make_run("anchoring", "BASELINE")) + "\n")
        df = _script.load_runs_df(exp_dir)
        assert len(df) == 1


# ── TestBuildCellDf ───────────────────────────────────────────────────────────


@pandas_required
class TestBuildCellDf:
    def _get_cell_df(self, tmp_path):
        exp_dir = _make_experiment_dir(tmp_path, _minimal_runs())
        run_df = _script.load_runs_df(exp_dir)
        return _script.build_cell_df(run_df), run_df

    def test_has_required_columns(self, tmp_path):
        df, _ = self._get_cell_df(tmp_path)
        for col in ("agent_id", "bias_category", "mean_bsi", "std_bsi", "n_runs"):
            assert col in df.columns, f"Missing column: {col}"

    def test_has_ci_columns(self, tmp_path):
        df, _ = self._get_cell_df(tmp_path)
        assert "ci_lower_95" in df.columns
        assert "ci_upper_95" in df.columns

    def test_has_treatment_effect_column(self, tmp_path):
        df, _ = self._get_cell_df(tmp_path)
        assert "treatment_effect" in df.columns

    def test_n_cells_equals_agents_times_biases(self, tmp_path):
        df, run_df = self._get_cell_df(tmp_path)
        n_agents = run_df["agent_id"].nunique()
        n_biases = run_df["bias_category"].nunique()
        assert len(df) == n_agents * n_biases

    def test_mean_bsi_is_average_of_all_variants(self, tmp_path):
        # Baseline bsi=0.0 + treatment bsi=0.5 → mean across all runs = 0.25
        df, _ = self._get_cell_df(tmp_path)
        anchoring_row = df[df["bias_category"] == "anchoring"].iloc[0]
        assert math.isclose(float(anchoring_row["mean_bsi"]), 0.25, abs_tol=1e-6)

    def test_treatment_effect_is_treatment_minus_baseline(self, tmp_path):
        # Baseline bsi=0.0, treatment bsi=0.5 → effect = 0.5
        df, _ = self._get_cell_df(tmp_path)
        anchoring_row = df[df["bias_category"] == "anchoring"].iloc[0]
        assert math.isclose(float(anchoring_row["treatment_effect"]), 0.5, abs_tol=1e-6)

    def test_ci_lower_le_mean_le_ci_upper(self, tmp_path):
        df, _ = self._get_cell_df(tmp_path)
        for _, row in df.iterrows():
            assert float(row["ci_lower_95"]) <= float(row["mean_bsi"]) + 1e-9
            assert float(row["mean_bsi"]) <= float(row["ci_upper_95"]) + 1e-9


# ── TestLoadRegressionResults ─────────────────────────────────────────────────


class TestLoadRegressionResults:
    def test_returns_none_when_file_absent(self, tmp_path):
        exp_dir = tmp_path / "exp"
        exp_dir.mkdir()
        assert _script.load_regression_results(exp_dir) is None

    def test_loads_json_when_present(self, tmp_path):
        exp_dir = tmp_path / "exp"
        exp_dir.mkdir()
        data = {"primary": {"n_obs": 100}, "variance_decomposition": None}
        (exp_dir / "regression_results.json").write_text(json.dumps(data))
        result = _script.load_regression_results(exp_dir)
        assert result["primary"]["n_obs"] == 100


# ── TestLoadP1Scores ──────────────────────────────────────────────────────────


class TestLoadP1Scores:
    def test_returns_none_for_none_path(self):
        assert _script.load_p1_scores(None) is None

    def test_returns_none_for_missing_file(self, tmp_path):
        result = _script.load_p1_scores(tmp_path / "nonexistent.json")
        assert result is None

    def test_loads_valid_json(self, tmp_path):
        p = tmp_path / "p1.json"
        scores = {"mock-agent-v1": 0.55}
        p.write_text(json.dumps(scores))
        assert _script.load_p1_scores(p) == scores


# ── TestFigureGenerators ──────────────────────────────────────────────────────


@matplotlib_required
class TestFigureGenerators:
    """Smoke tests: each generator runs without error and writes a PNG file."""

    def _setup(self, tmp_path):
        exp_dir = _make_experiment_dir(tmp_path, _minimal_runs())
        run_df = _script.load_runs_df(exp_dir)
        cell_df = _script.build_cell_df(run_df)
        out_dir = tmp_path / "figures"
        out_dir.mkdir()
        return exp_dir, run_df, cell_df, out_dir

    def test_gen_fig1_writes_png(self, tmp_path):
        _, _, cell_df, out_dir = self._setup(tmp_path)
        path = _script.gen_fig1(cell_df, p1_scores=None, output_dir=out_dir)
        assert path.exists()
        assert path.suffix == ".png"

    def test_gen_fig2_skips_without_p1_scores(self, tmp_path, capsys):
        _, _, cell_df, out_dir = self._setup(tmp_path)
        result = _script.gen_fig2(cell_df, p1_scores=None, output_dir=out_dir)
        assert result is None
        captured = capsys.readouterr()
        assert "SKIP" in captured.out

    def test_gen_fig2_skips_with_too_few_p1_models(self, tmp_path):
        _, _, cell_df, out_dir = self._setup(tmp_path)
        # Only 1 model; capability_scatter needs >= 3 to fit OLS
        p1 = {"mock-agent-v1": 0.5}
        result = _script.gen_fig2(cell_df, p1_scores=p1, output_dir=out_dir)
        assert result is None

    def test_gen_fig3_writes_png(self, tmp_path):
        _, run_df, _, out_dir = self._setup(tmp_path)
        path = _script.gen_fig3(run_df, output_dir=out_dir)
        assert path.exists()
        assert path.suffix == ".png"

    def test_gen_fig4a_skips_without_variance_decomp(self, tmp_path, capsys):
        _, _, _, out_dir = self._setup(tmp_path)
        result = _script.gen_fig4a({"variance_decomposition": None}, output_dir=out_dir)
        assert result is None
        captured = capsys.readouterr()
        assert "SKIP" in captured.out

    def test_gen_fig4a_writes_png_with_valid_data(self, tmp_path):
        _, _, _, out_dir = self._setup(tmp_path)
        vd_data = {
            "variance_decomposition": {
                "rows": [
                    {"source": "Model", "ss": 1.0, "df": 9, "ms": 0.11,
                     "eta_squared": 0.10, "pct_variance": 10.0},
                    {"source": "BiasType", "ss": 2.0, "df": 4, "ms": 0.50,
                     "eta_squared": 0.20, "pct_variance": 20.0},
                    {"source": "Residual", "ss": 7.0, "df": 436, "ms": 0.016,
                     "eta_squared": 0.70, "pct_variance": 70.0},
                ],
                "total_ss": 10.0,
                "n_obs": 450,
                "notes": "η²_Residual > 0.70 → most variance is within-cell stochastic noise.",
            }
        }
        path = _script.gen_fig4a(vd_data, output_dir=out_dir)
        assert path is not None
        assert path.exists()

    def test_gen_fig4b_skips_when_no_treatment_effect_column(self, tmp_path, capsys):
        import pandas as pd
        _, _, _, out_dir = self._setup(tmp_path)
        empty_df = pd.DataFrame({"agent_id": [], "bias_category": [], "mean_bsi": []})
        result = _script.gen_fig4b(empty_df, output_dir=out_dir)
        assert result is None

    def test_gen_fig4b_writes_png_with_valid_data(self, tmp_path):
        _, _, cell_df, out_dir = self._setup(tmp_path)
        path = _script.gen_fig4b(cell_df, output_dir=out_dir)
        assert path is not None
        assert path.exists()


# ── TestCLIIntegration ────────────────────────────────────────────────────────


@matplotlib_required
class TestCLIIntegration:
    def _write_runs(self, tmp_path):
        return _make_experiment_dir(tmp_path, _minimal_runs())

    def test_dry_run_does_not_write_png_files(self, tmp_path):
        exp_dir = self._write_runs(tmp_path)
        out_dir = tmp_path / "figs"
        _script.main([
            "--experiment-dir", str(exp_dir),
            "--output-dir", str(out_dir),
            "--dry-run",
        ])
        if out_dir.exists():
            assert list(out_dir.glob("*.png")) == []

    def test_mock_mode_uses_patched_directory(self, tmp_path, monkeypatch):
        exp_dir = self._write_runs(tmp_path)
        monkeypatch.setattr(_script, "_find_latest_mock_dir", lambda: exp_dir)
        out_dir = tmp_path / "mock_figs"
        _script.main(["--mock", "--output-dir", str(out_dir)])
        assert (out_dir / "fig1-bsi-heatmap.png").exists()
        assert (out_dir / "fig3-bsi-distributions.png").exists()

    def test_missing_experiment_dir_exits(self, tmp_path):
        with pytest.raises(SystemExit):
            _script.main(["--experiment-dir", str(tmp_path / "does_not_exist")])

    def test_fig4b_written_when_treatment_data_present(self, tmp_path):
        exp_dir = self._write_runs(tmp_path)
        out_dir = tmp_path / "figs"
        _script.main(["--experiment-dir", str(exp_dir), "--output-dir", str(out_dir)])
        assert (out_dir / "fig4b-treatment-effects.png").exists()

    def test_all_mandatory_figures_written(self, tmp_path):
        exp_dir = self._write_runs(tmp_path)
        out_dir = tmp_path / "figs"
        _script.main(["--experiment-dir", str(exp_dir), "--output-dir", str(out_dir)])
        assert (out_dir / "fig1-bsi-heatmap.png").exists()
        assert (out_dir / "fig3-bsi-distributions.png").exists()
        assert (out_dir / "fig4b-treatment-effects.png").exists()
