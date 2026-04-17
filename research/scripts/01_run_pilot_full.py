"""
Script 01: Run Pilot Full Experiment (N=30 per cell)
======================================================
Defines the PILOT_FULL_DESIGN manifest (10 real models × 5 bias types
× 2 variants × 30 runs = 3,000 runs ≈ $450) and immediately executes it.

Use this before the full N=50 realistic run to:
  - Detect ceiling effects (Section O.1 Day 9–10 decision gate)
  - Estimate per-model bias signatures with moderate statistical power
  - Identify any infrastructure or API issues before committing to the full run

Prerequisites:
  - OPENROUTER_API_KEY must be set (or pass --mock for local validation)
  - pip install -e ".[dev]" completed

Flags:
  --dry-run    Print plan + cost estimate without invoking any models.
  --resume     Skip already-completed runs (restart after crash).
  --mock       Substitute mock-agent-v1 for all models (free; pipeline validation).
  --output-dir Override experiment output directory (default: results/experiments).

Run: python research/scripts/01_run_pilot_full.py [--dry-run] [--mock]
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from research.experiments.grid import PILOT_FULL_DESIGN  # noqa: E402
from research.experiments.manifest import create_manifest, freeze_manifest  # noqa: E402
from research.experiments.run_experiment import (  # noqa: E402
    estimate_cost,
    generate_run_plan,
    run_experiment,
)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="python research/scripts/01_run_pilot_full.py",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print plan and cost estimate without invoking any models.",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Skip run_ids already present in runs.jsonl (restart after crash).",
    )
    parser.add_argument(
        "--mock",
        action="store_true",
        help=(
            "Replace all 10 real models with mock-agent-v1. "
            "Free and fast; use for pipeline validation without API credentials."
        ),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("results/experiments"),
        metavar="DIR",
        help="Parent directory for experiment outputs (default: results/experiments).",
    )
    parser.add_argument(
        "--no-pin-versions",
        action="store_true",
        help="Skip OpenRouter model-version pinning (useful for offline / CI use).",
    )
    args = parser.parse_args(argv)

    design = dict(PILOT_FULL_DESIGN)
    if args.mock:
        design = {
            **design,
            "models": ["mock-agent-v1"],
            "cost_per_run_usd": 0.00,
        }
        print("[--mock] Substituting mock-agent-v1 for all real models.")

    output_dir: Path = args.output_dir

    # 1. Build and freeze manifest.
    print(f"Building pilot_full manifest (N={design['n_runs_per_cell']} per cell)…")
    manifest = create_manifest(
        design,
        pin_model_versions=not args.no_pin_versions,
    )
    manifest_path = freeze_manifest(manifest, output_dir)
    exp_dir = manifest_path.parent
    print(f"Manifest written : {manifest_path}")

    # 2. Generate run plan and write run_plan.csv.
    manifest_dict = json.loads(manifest_path.read_text(encoding="utf-8"))
    runs = generate_run_plan(manifest_dict)
    run_plan_path = exp_dir / "run_plan.csv"
    with open(run_plan_path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(runs[0].keys()))
        writer.writeheader()
        writer.writerows(runs)
    print(f"Run plan written : {run_plan_path}  ({len(runs):,} runs)")

    # 3. Write cost estimate.
    cost = estimate_cost(len(runs), design["cost_per_run_usd"])
    cost_path = exp_dir / "cost_estimate.txt"
    cost_path.write_text(json.dumps(cost, indent=2), encoding="utf-8")
    print(
        f"Cost estimate    : ${cost['estimated_total_usd']:.2f} for {cost['n_runs']:,} runs"
    )
    print()

    # 4. Execute or display dry-run summary.
    run_experiment(
        manifest_path=manifest_path,
        output_dir=exp_dir,
        dry_run=args.dry_run,
        resume=args.resume,
    )

    if not args.dry_run:
        print()
        print("Next step — analyze ceiling effect:")
        print(
            f"  python research/scripts/03_analyze_ceiling_effect.py "
            f"--experiment-dir {exp_dir}"
        )


if __name__ == "__main__":
    main()
