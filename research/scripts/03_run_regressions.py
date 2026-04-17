"""
Script 03: Run Regressions
============================
Loads ``runs.jsonl`` from an experiment directory and runs the full regression
pipeline:

  - Primary mixed-effects model (BSI ~ BiasType + Model + Treatment +
    BiasType×Model + (1|run_id)) via ``research/analysis/regression.py``
  - Variance decomposition ANOVA (Model + BiasType + Treatment + [Temperature])
  - BH-FDR correction on all primary-model p-values
  - Optional capability OLS (mean_BSI ~ P1Score) when ``--p1-scores`` is supplied

Writes ``regression_results.json`` to the experiment directory.

Run:
    python research/scripts/03_run_regressions.py \\
           --experiment-dir results/experiments/pillar2/<id>

    # With Pillar 1 capability scores (optional):
    python research/scripts/03_run_regressions.py \\
           --experiment-dir results/experiments/pillar2/<id> \\
           --p1-scores path/to/p1_scores.json

Notes
-----
- Error rows (``error_flag=true``) are excluded before regression.
- Variant names are normalised to uppercase before passing to
  ``regression.py`` (``runs.jsonl`` stores them lower-cased).
- Requires ``pandas`` and optionally ``statsmodels`` (install with
  ``pip install -e ".[dev]"``).
"""
from __future__ import annotations

import argparse
import dataclasses
import json
import sys
from dataclasses import asdict
from pathlib import Path

# ── pandas / statsmodels availability ─────────────────────────────────────────

try:
    import pandas as pd
    _PANDAS_AVAILABLE = True
except ImportError:
    _PANDAS_AVAILABLE = False

# ── Project imports ───────────────────────────────────────────────────────────

_REPO = Path(__file__).resolve().parent.parent.parent
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from research.analysis.regression import (
    RegressionResult,
    VarianceDecompositionResult,
    apply_bh_correction,
    run_capability_regression,
    run_primary_regression,
    run_variance_decomposition,
)


# ─────────────────────────────────────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────────────────────────────────────


def load_runs_jsonl(experiment_dir: Path) -> list[dict]:
    """Load all records from ``runs.jsonl``, skipping malformed lines."""
    path = experiment_dir / "runs.jsonl"
    if not path.exists():
        raise FileNotFoundError(f"runs.jsonl not found in {experiment_dir}")
    records: list[dict] = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return records


def build_regression_dataframe(records: list[dict]) -> "pd.DataFrame":  # type: ignore[name-defined]
    """Convert run records to a pandas DataFrame ready for regression.

    Normalises ``variant`` to uppercase so regression.py variant checks
    (BASELINE, FRAMING_GAIN, WARP_AB, ...) work correctly.

    Excludes rows with ``error_flag=True`` or missing ``bsi``.
    """
    if not _PANDAS_AVAILABLE:
        raise ImportError(
            "pandas is required.  Install with: pip install pandas"
        )
    rows = []
    for r in records:
        if r.get("error_flag"):
            continue
        bsi = r.get("bsi")
        if bsi is None:
            continue
        rows.append(
            {
                "run_id": r.get("run_id", ""),
                "agent_id": r.get("agent_id", ""),
                "bias_category": r.get("bias_category", ""),
                "variant": str(r.get("variant", "")).upper(),
                "bsi": float(bsi),
                "temperature": r.get("temperature"),
                "prompt_version": r.get("prompt_version", "standard"),
                "run_index": r.get("run_index", 0),
            }
        )
    if not rows:
        raise ValueError("No valid (non-error) rows found in runs.jsonl.")
    df = pd.DataFrame(rows)
    # Ensure numeric types
    df["bsi"] = df["bsi"].astype(float)
    return df


# ─────────────────────────────────────────────────────────────────────────────
# SERIALISATION HELPERS
# ─────────────────────────────────────────────────────────────────────────────


def _result_to_dict(result: RegressionResult) -> dict:
    return asdict(result)


def _vd_to_dict(vd: VarianceDecompositionResult) -> dict:
    return asdict(vd)


# ─────────────────────────────────────────────────────────────────────────────
# CORE PIPELINE
# ─────────────────────────────────────────────────────────────────────────────


def run_regression_pipeline(
    df: "pd.DataFrame",  # type: ignore[name-defined]
    p1_scores: dict[str, float] | None = None,
) -> dict:
    """Run the full regression pipeline and return a results dict.

    Steps:
      1. Primary mixed-effects regression (BSI ~ BiasType + Model + Treatment
         + BiasType×Model + (1|run_id)).
      2. BH-FDR correction on all primary-regression p-values.
      3. Variance decomposition ANOVA.
      4. Optional capability OLS when p1_scores is supplied.

    Args:
        df: Run-level DataFrame with columns run_id, agent_id, bias_category,
            variant, bsi, temperature.  Variant must be uppercase already.
        p1_scores: Optional mapping {agent_id: P1_score} for H2 capability
            regression.  When ``None`` the capability step is skipped.

    Returns:
        Dict with keys ``primary``, ``variance_decomposition``, ``bh_correction``,
        ``capability`` (may be None), ``summary``.
    """
    # ── Step 1: Primary mixed-effects regression ─────────────────────────────
    primary = run_primary_regression(df)

    # ── Step 2: BH-FDR correction on primary p-values ────────────────────────
    raw_pvalues = [c.p_value for c in primary.coefficients]
    adjusted, rejected = apply_bh_correction(raw_pvalues)

    # Annotate coefficients in-place
    for i, coef in enumerate(primary.coefficients):
        coef.p_value_bh = round(adjusted[i], 6)
        coef.significant_bh = bool(rejected[i])

    # ── Step 3: Variance decomposition ───────────────────────────────────────
    vd = run_variance_decomposition(df)

    # ── Step 4: Optional capability regression ────────────────────────────────
    capability = None
    if p1_scores:
        capability = run_capability_regression(df, p1_scores)

    # ── Step 5: Build summary ─────────────────────────────────────────────────
    n_significant_bh = sum(1 for c in primary.coefficients if c.significant_bh)
    treat_coef = next(
        (c for c in primary.coefficients if "treatment" in c.name.lower()), None
    )

    vd_table = []
    if vd:
        for row in vd.rows:
            vd_table.append(
                {
                    "source": row.source,
                    "pct_variance": row.pct_variance,
                    "eta_squared": row.eta_squared,
                }
            )

    summary = {
        "n_obs": primary.n_obs,
        "backend": primary.backend,
        "n_coefficients": len(primary.coefficients),
        "n_significant_bh": n_significant_bh,
        "treatment_estimate": round(treat_coef.estimate, 4) if treat_coef else None,
        "treatment_p_value_bh": round(treat_coef.p_value_bh, 6) if (treat_coef and treat_coef.p_value_bh is not None) else None,
        "treatment_significant_bh": treat_coef.significant_bh if treat_coef else None,
        "random_effects_variance": primary.random_effects_variance,
        "primary_aic": primary.aic,
        "primary_bic": primary.bic,
        "variance_decomposition": vd_table,
        "capability_regression_available": capability is not None,
        "warnings": primary.warnings + (capability.warnings if capability else []),
    }

    return {
        "primary": _result_to_dict(primary),
        "bh_correction": {
            "raw_pvalues": [round(p, 6) for p in raw_pvalues],
            "adjusted_pvalues": [round(p, 6) for p in adjusted],
            "rejected": rejected,
            "n_rejected": sum(rejected),
            "alpha": 0.05,
        },
        "variance_decomposition": _vd_to_dict(vd) if vd else None,
        "capability": _result_to_dict(capability) if capability else None,
        "summary": summary,
    }


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the Pillar 2 regression pipeline on an experiment directory."
    )
    parser.add_argument(
        "--experiment-dir",
        required=True,
        type=Path,
        help="Path to a completed experiment directory containing runs.jsonl.",
    )
    parser.add_argument(
        "--p1-scores",
        type=Path,
        default=None,
        help=(
            "Path to a JSON file mapping {agent_id: p1_score} for the optional "
            "capability regression (H2).  Must be a flat JSON object."
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help=(
            "Path for the output JSON file.  "
            "Default: <experiment-dir>/regression_results.json"
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Load data and validate inputs but do not run regressions or write output.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = _parse_args(argv)
    experiment_dir = args.experiment_dir.resolve()

    if not experiment_dir.exists():
        print(f"ERROR: experiment directory not found: {experiment_dir}", file=sys.stderr)
        sys.exit(1)

    # ── Load data ─────────────────────────────────────────────────────────────
    print(f"Loading runs.jsonl from {experiment_dir} ...")
    records = load_runs_jsonl(experiment_dir)
    print(f"  Loaded {len(records)} raw records.")

    if not _PANDAS_AVAILABLE:
        print("ERROR: pandas is required.  pip install pandas", file=sys.stderr)
        sys.exit(1)

    df = build_regression_dataframe(records)
    n_excluded = len(records) - len(df)
    print(
        f"  {len(df)} rows after excluding errors/nulls "
        f"({n_excluded} excluded)."
    )
    print(
        f"  Agents: {sorted(df['agent_id'].unique())}"
    )
    print(
        f"  Bias types: {sorted(df['bias_category'].unique())}"
    )
    print(
        f"  Variants: {sorted(df['variant'].unique())}"
    )

    # ── Load optional P1 scores ───────────────────────────────────────────────
    p1_scores: dict[str, float] | None = None
    if args.p1_scores:
        with open(args.p1_scores, encoding="utf-8") as fh:
            p1_scores = json.load(fh)
        print(f"  P1 scores loaded for {len(p1_scores)} agents.")

    if args.dry_run:
        print("\nDry-run: skipping regression execution.")
        return

    # ── Run pipeline ─────────────────────────────────────────────────────────
    print("\nRunning regression pipeline ...")
    results = run_regression_pipeline(df, p1_scores=p1_scores)

    # ── Print summary ─────────────────────────────────────────────────────────
    s = results["summary"]
    print("\n── Regression Summary ────────────────────────────────────────────")
    print(f"  Backend           : {s['backend']}")
    print(f"  N observations    : {s['n_obs']}")
    print(f"  N coefficients    : {s['n_coefficients']}")
    print(f"  BH-significant    : {s['n_significant_bh']}")
    if s["treatment_estimate"] is not None:
        print(f"  Treatment β       : {s['treatment_estimate']:.4f}  "
              f"p_adj={s['treatment_p_value_bh']}  "
              f"sig={s['treatment_significant_bh']}")
    if s["random_effects_variance"] is not None:
        print(f"  Random effects σ² : {s['random_effects_variance']:.6f}")
    if s["primary_aic"] is not None:
        print(f"  AIC / BIC         : {s['primary_aic']} / {s['primary_bic']}")
    print("\n── Variance Decomposition ───────────────────────────────────────")
    for row in s.get("variance_decomposition") or []:
        print(f"  {row['source']:12s}  η²={row['eta_squared']:.4f}  "
              f"({row['pct_variance']:.1f}%)")
    if s["capability_regression_available"]:
        cap_r2 = results["capability"]["r_squared"]
        print(f"\n── Capability Regression (H2, descriptive) ─────────────────────")
        print(f"  R² = {cap_r2}")
    if s["warnings"]:
        print("\n── Warnings ─────────────────────────────────────────────────────")
        for w in s["warnings"]:
            print(f"  ⚠  {w}")

    # ── Write output ──────────────────────────────────────────────────────────
    output_path = args.output or (experiment_dir / "regression_results.json")
    with open(output_path, "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=2)
    print(f"\nResults written to: {output_path}")


if __name__ == "__main__":
    main()
