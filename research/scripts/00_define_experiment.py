"""
Script 00: Define Experiment Grid
==================================
Defines the full experiment grid for the Realistic Design (Section F.1).
Outputs: manifest.json, run_plan.csv, cost_estimate.txt under
         {output_dir}/{experiment_id}/.

Run: python research/scripts/00_define_experiment.py [--design realistic|flagship]

Typical workflow:
  1. python research/scripts/00_define_experiment.py          # define grid
  2. python -m research.experiments.run_experiment \\
         results/experiments/{experiment_id}/manifest.json --dry-run
  3. python -m research.experiments.run_experiment \\
         results/experiments/{experiment_id}/manifest.json
  4. python research/scripts/02_aggregate_results.py          # auto-invoked
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

# When invoked directly as a script (python research/scripts/00_define_experiment.py),
# Python may not have the repo root on sys.path.  Ensure it is present so that
# `research.*` imports resolve correctly regardless of invocation method.
_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

# Design constants live in grid.py so they are importable by tests and other modules.
from research.experiments.grid import DESIGNS, FLAGSHIP_DESIGN, PILOT_DESIGN, PILOT_FULL_DESIGN, REALISTIC_DESIGN  # noqa: F401
from research.experiments.manifest import create_manifest, freeze_manifest
from research.experiments.run_experiment import estimate_cost, generate_run_plan


# ── Main ──────────────────────────────────────────────────────────────────────


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="python research/scripts/00_define_experiment.py",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--design",
        choices=list(DESIGNS),
        default="realistic",
        help="Experiment scale: 'pilot' (mock-agent × 5 runs, infrastructure check), "
             "'pilot_full' (10 real models × 30 runs, ceiling-effect check ~$450), "
             "'realistic' (10 models × 50 runs), or "
             "'flagship' (10 models × 100 runs + CoT). Default: realistic.",
    )
    parser.add_argument(
        "--output-dir",
        default="results/experiments",
        metavar="DIR",
        help="Parent directory for experiment outputs. "
             "The manifest is written to {DIR}/{experiment_id}/manifest.json. "
             "Default: results/experiments",
    )
    parser.add_argument(
        "--no-pin-versions",
        action="store_true",
        help="Skip OpenRouter model-version pinning (useful for offline use / CI).",
    )
    args = parser.parse_args(argv)

    design = DESIGNS[args.design]
    output_dir = Path(args.output_dir)

    # 1. Build manifest (includes git hash + optional model-version pinning).
    print(f"Building {args.design!r} experiment manifest …")
    manifest = create_manifest(
        design,
        pin_model_versions=not args.no_pin_versions,
    )

    # 2. Freeze manifest to disk and create the experiment directory layout.
    manifest_path = freeze_manifest(manifest, output_dir)
    exp_dir = manifest_path.parent
    print(f"Manifest written : {manifest_path}")

    # 3. Generate the flat run plan and write run_plan.csv.
    manifest_dict = json.loads(manifest_path.read_text(encoding="utf-8"))
    runs = generate_run_plan(manifest_dict)
    run_plan_path = exp_dir / "run_plan.csv"
    with open(run_plan_path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(runs[0].keys()))
        writer.writeheader()
        writer.writerows(runs)
    print(f"Run plan written : {run_plan_path}  ({len(runs):,} runs)")

    # 4. Write cost estimate.
    cost = estimate_cost(len(runs), design["cost_per_run_usd"])
    cost_path = exp_dir / "cost_estimate.txt"
    cost_path.write_text(json.dumps(cost, indent=2), encoding="utf-8")
    print(
        f"Cost estimate    : ${cost['estimated_total_usd']:.2f} "
        f"for {cost['n_runs']:,} runs"
    )
    print(f"                   ({cost['note']})")
    print()
    print("Next steps:")
    print(f"  Dry run  : python -m research.experiments.run_experiment "
          f"{manifest_path} --dry-run")
    print(f"  Full run : python -m research.experiments.run_experiment "
          f"{manifest_path}")


if __name__ == "__main__":
    main()
