"""
Script 04: Generate All Paper Figures (Pillar 2)
=================================================
Reads experiment data (runs.jsonl, optionally regression_results.json) and
generates all 4 research figures for the Pillar 2 paper:

  fig1-bsi-heatmap.png         — Model × bias-type BSI heatmap
  fig2-capability-scatter.png  — Pillar 1 score vs. mean BSI scatter
  fig3-bsi-distributions.png   — Within-cell BSI violin distributions
  fig4a-variance-decomp.png    — BSI variance decomposition bar chart
  fig4b-treatment-effects.png  — Treatment-effect forest plot

Run:
  python research/scripts/04_generate_figures.py \\
    --experiment-dir results/experiments/pillar2-realistic-<id> \\
    [--p1-scores results/p1_scores.json] \\
    [--output-dir docs/paper/figures/research] \\
    [--mock]      # use latest mock pilot for pipeline validation
    [--dry-run]   # validate data without writing files

Figure 2 requires --p1-scores.
Figure 4a requires a completed regression run (03_run_regressions.py).
Both skip gracefully when data is unavailable.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

try:
    import matplotlib
    matplotlib.use("Agg")
    _MATPLOTLIB_AVAILABLE = True
except ImportError:
    _MATPLOTLIB_AVAILABLE = False

try:
    import pandas as _pd
    _PANDAS_AVAILABLE = True
except ImportError:
    _PANDAS_AVAILABLE = False

_DEFAULT_OUTPUT_DIR = _REPO_ROOT / "docs" / "paper" / "figures" / "research"

DPI = 300

_BASELINE_VARIANTS = frozenset({"BASELINE", "FRAMING_GAIN", "GAIN"})


# ── I/O helpers ───────────────────────────────────────────────────────────────


def _find_latest_mock_dir() -> Path:
    """Return the most recently modified mock pilot experiment directory."""
    base = _REPO_ROOT / "results" / "experiments"
    candidates = sorted(
        base.glob("pillar2-pilot-*"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if not candidates:
        raise FileNotFoundError(
            f"No mock pilot experiment found under {base}. "
            "Run: python research/scripts/00_define_experiment.py --no-pin-versions"
        )
    return candidates[0]


def _display_path(path: Path) -> str:
    """Return repo-relative path when possible, otherwise absolute."""
    try:
        return str(path.relative_to(_REPO_ROOT))
    except ValueError:
        return str(path)


def load_runs_df(experiment_dir: Path):
    """Load runs.jsonl into a pandas DataFrame, dropping error rows and null BSI."""
    import pandas as pd

    jsonl_path = experiment_dir / "runs.jsonl"
    if not jsonl_path.exists():
        raise FileNotFoundError(f"runs.jsonl not found at {jsonl_path}")

    records = []
    with open(jsonl_path) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                pass

    df = pd.DataFrame(records)
    if df.empty:
        raise ValueError(f"No records found in {jsonl_path}")

    # Normalise variant to uppercase (JSONL stores lowercase; figure modules expect uppercase)
    if "variant" in df.columns:
        df["variant"] = df["variant"].str.upper()

    if "error_flag" in df.columns:
        df = df[~df["error_flag"].fillna(False)]
    if "bsi" in df.columns:
        df = df[df["bsi"].notna()]

    return df.reset_index(drop=True)


def _t_critical_95(n: int) -> float:
    _table = {
        1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571,
        6: 2.447, 7: 2.365, 8: 2.306, 9: 2.262, 10: 2.228,
        11: 2.201, 12: 2.179, 13: 2.160, 14: 2.145, 15: 2.131,
        20: 2.086, 25: 2.060, 29: 2.045,
    }
    df = max(1, n - 1)
    if df >= 30:
        return 1.960
    return _table.get(df, 2.000)


def build_cell_df(run_df):
    """Build a per-(agent × bias_category) aggregate DataFrame from run-level data.

    Computes mean_bsi, std_bsi, 95 % CI bounds, n_runs, and treatment_effect
    (mean treatment-variant BSI minus mean baseline BSI for each cell).
    """
    import pandas as pd

    grp = run_df.groupby(["agent_id", "bias_category"])
    mean_bsi = grp["bsi"].mean().rename("mean_bsi")
    std_bsi = grp["bsi"].std(ddof=1).fillna(0.0).rename("std_bsi")
    n_runs = grp["bsi"].count().rename("n_runs")

    cell_df = pd.concat([mean_bsi, std_bsi, n_runs], axis=1).reset_index()

    def _ci(values):
        n = len(values)
        if n < 2:
            m = float(values.mean()) if len(values) else 0.0
            return pd.Series({"ci_lower_95": m, "ci_upper_95": m})
        m = values.mean()
        s = values.std(ddof=1)
        t = _t_critical_95(n)
        margin = t * s / math.sqrt(n)
        return pd.Series({
            "ci_lower_95": max(0.0, m - margin),
            "ci_upper_95": min(1.0, m + margin),
        })

    ci_df = grp["bsi"].apply(_ci).unstack()
    cell_df = cell_df.join(ci_df, on=["agent_id", "bias_category"])

    # Treatment effect = mean(treatment_bsi) − mean(baseline_bsi)
    baseline_df = run_df[run_df["variant"].isin(_BASELINE_VARIANTS)]
    treatment_df = run_df[~run_df["variant"].isin(_BASELINE_VARIANTS)]

    b_mean = baseline_df.groupby(["agent_id", "bias_category"])["bsi"].mean()
    t_mean = treatment_df.groupby(["agent_id", "bias_category"])["bsi"].mean()
    treatment_effect = (t_mean - b_mean).rename("treatment_effect")

    cell_df = cell_df.join(treatment_effect, on=["agent_id", "bias_category"])
    return cell_df


def load_regression_results(experiment_dir: Path) -> dict | None:
    path = experiment_dir / "regression_results.json"
    if not path.exists():
        return None
    with open(path) as fh:
        return json.load(fh)


def load_p1_scores(p1_scores_path: Path | None) -> dict[str, float] | None:
    if p1_scores_path is None:
        return None
    if not p1_scores_path.exists():
        print(f"  [WARN] --p1-scores file not found: {p1_scores_path}", file=sys.stderr)
        return None
    with open(p1_scores_path) as fh:
        return json.load(fh)


# ── Figure generators ─────────────────────────────────────────────────────────


def gen_fig1(cell_df, p1_scores, output_dir: Path) -> Path:
    from research.figures.heatmap import plot_bsi_heatmap
    import matplotlib.pyplot as plt

    fig = plot_bsi_heatmap(cell_df, p1_scores=p1_scores)
    out = output_dir / "fig1-bsi-heatmap.png"
    fig.savefig(out, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {_display_path(out)}")
    return out


def gen_fig2(cell_df, p1_scores, output_dir: Path) -> Path | None:
    if p1_scores is None:
        print("  [SKIP] fig2-capability-scatter — no --p1-scores provided.")
        return None

    from research.figures.capability_scatter import plot_capability_scatter
    import matplotlib.pyplot as plt

    try:
        fig = plot_capability_scatter(cell_df, p1_scores)
    except ValueError as exc:
        print(f"  [SKIP] fig2-capability-scatter — {exc}", file=sys.stderr)
        return None

    out = output_dir / "fig2-capability-scatter.png"
    fig.savefig(out, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {_display_path(out)}")
    return out


def gen_fig3(run_df, output_dir: Path) -> Path:
    from research.figures.distribution_plot import plot_bsi_distributions
    import matplotlib.pyplot as plt

    fig = plot_bsi_distributions(run_df)
    out = output_dir / "fig3-bsi-distributions.png"
    fig.savefig(out, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {_display_path(out)}")
    return out


def gen_fig4a(regression_results: dict, output_dir: Path) -> Path | None:
    vd_data = regression_results.get("variance_decomposition")
    if not vd_data or not vd_data.get("rows"):
        print("  [SKIP] fig4a-variance-decomp — no variance_decomposition in regression results.")
        return None

    from research.figures.variance_plot import plot_variance_decomposition
    from results.stats_pipeline import VarianceDecomposition, VarianceDecompositionRow
    import matplotlib.pyplot as plt

    rows = [
        VarianceDecompositionRow(
            source=r["source"],
            ss=r["ss"],
            df=r["df"],
            ms=r["ms"],
            eta_squared=r.get("eta_squared", 0.0),
            pct_variance=r.get("pct_variance", 0.0),
        )
        for r in vd_data["rows"]
    ]
    vd_result = VarianceDecomposition(
        rows=rows,
        total_ss=vd_data.get("total_ss", 0.0),
        n_obs=vd_data.get("n_obs", 0),
        notes=vd_data.get("notes", ""),
    )

    fig = plot_variance_decomposition(vd_result)
    out = output_dir / "fig4a-variance-decomp.png"
    fig.savefig(out, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {_display_path(out)}")
    return out


def gen_fig4b(cell_df, output_dir: Path) -> Path | None:
    if "treatment_effect" not in cell_df.columns or cell_df["treatment_effect"].isna().all():
        print("  [SKIP] fig4b-treatment-effects — no treatment_effect data available.")
        return None

    from research.figures.variance_plot import plot_treatment_effects
    import matplotlib.pyplot as plt

    df = cell_df.copy()
    if "ci_lower_95" not in df.columns:
        df["ci_lower_95"] = df["mean_bsi"]
        df["ci_upper_95"] = df["mean_bsi"]

    try:
        fig = plot_treatment_effects(df)
    except ValueError as exc:
        print(f"  [SKIP] fig4b-treatment-effects — {exc}", file=sys.stderr)
        return None

    out = output_dir / "fig4b-treatment-effects.png"
    fig.savefig(out, dpi=DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {_display_path(out)}")
    return out


# ── CLI ───────────────────────────────────────────────────────────────────────


def _parse_args(argv=None):
    p = argparse.ArgumentParser(
        description="Generate all Pillar 2 research paper figures (Figures 1–4)."
    )
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--experiment-dir",
        metavar="DIR",
        type=Path,
        help="Path to a completed experiment directory containing runs.jsonl.",
    )
    group.add_argument(
        "--mock",
        action="store_true",
        help=(
            "Use the latest mock pilot experiment directory for pipeline validation. "
            "Figures show expected structure with mock BSI values (all zeros for mock-agent)."
        ),
    )
    p.add_argument(
        "--p1-scores",
        metavar="JSON",
        type=Path,
        default=None,
        help=(
            "Path to a JSON file mapping agent_id → Pillar 1 capability score. "
            "Required for Figure 2 (capability scatter)."
        ),
    )
    p.add_argument(
        "--output-dir",
        metavar="DIR",
        type=Path,
        default=_DEFAULT_OUTPUT_DIR,
        help=f"Directory to write PNG figures (default: {_DEFAULT_OUTPUT_DIR}).",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Load and validate data without writing any figure files.",
    )
    return p.parse_args(argv)


def main(argv=None):
    args = _parse_args(argv)

    if args.mock:
        exp_dir = _find_latest_mock_dir()
        print(f"[--mock] Using experiment directory: {exp_dir.name}")
    else:
        exp_dir = args.experiment_dir
        if not exp_dir.exists():
            sys.exit(f"Error: --experiment-dir not found: {exp_dir}")

    print(f"\nLoading runs from {exp_dir / 'runs.jsonl'} ...")
    try:
        run_df = load_runs_df(exp_dir)
    except (FileNotFoundError, ValueError) as exc:
        sys.exit(f"Error loading runs: {exc}")

    print(f"  {len(run_df)} valid runs loaded.")

    cell_df = build_cell_df(run_df)
    n_models = cell_df["agent_id"].nunique()
    n_biases = cell_df["bias_category"].nunique()
    print(f"  {len(cell_df)} cells aggregated ({n_models} models × {n_biases} bias types).")

    regression_results = load_regression_results(exp_dir)
    if regression_results:
        print("  Regression results loaded.")
    else:
        print("  [INFO] No regression_results.json found — Figure 4a will be skipped.")

    p1_scores = load_p1_scores(args.p1_scores)
    if p1_scores:
        print(f"  P1 scores loaded for {len(p1_scores)} models.")
    else:
        print("  [INFO] No P1 scores provided — Figure 2 will be skipped.")

    if args.dry_run:
        print("\n[--dry-run] Data validated successfully. No figures written.")
        return

    output_dir: Path = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"\nWriting figures to {output_dir} ...")

    gen_fig1(cell_df, p1_scores, output_dir)
    gen_fig2(cell_df, p1_scores, output_dir)
    gen_fig3(run_df, output_dir)
    if regression_results:
        gen_fig4a(regression_results, output_dir)
    gen_fig4b(cell_df, output_dir)

    print("\nDone. All figures generated.")


if __name__ == "__main__":
    main()
