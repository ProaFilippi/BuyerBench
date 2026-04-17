"""
Script 03: Ceiling Effect Analysis
====================================
Analyzes a completed pilot_full (or pilot) experiment for ceiling effects:
are scenario difficulties sufficient to reveal bias in frontier LLMs?

Gate decision (Section O.3, Day 10):
  PROCEED  — < CEILING_THRESHOLD models score mean_BSI < FLOOR_BSI on all bias types.
  CEILING  — ≥ CEILING_THRESHOLD models score mean_BSI < FLOOR_BSI on all bias types.
             REV-4 hard-difficulty scenarios required before the full N=50 run.

Run: python research/scripts/03_analyze_ceiling_effect.py \\
         --experiment-dir results/experiments/pillar2-pilot_full-YYYYMMDD-HHMMSS

Typical workflow (after 01_run_pilot_full.py):
  1. python research/scripts/01_run_pilot_full.py            # run N=30 pilot
  2. python research/scripts/03_analyze_ceiling_effect.py \\
         --experiment-dir <exp_dir>                          # analyze results
  3. If PROCEED: python research/scripts/00_define_experiment.py  # define N=50
  4. If CEILING: add harder scenarios via REV-4, then repeat from step 1.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from research.analysis.ceiling_effect import (  # noqa: E402
    CEILING_THRESHOLD,
    FLOOR_BSI,
    analyze_ceiling_effect,
)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="python research/scripts/03_analyze_ceiling_effect.py",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--experiment-dir",
        type=Path,
        required=True,
        metavar="DIR",
        help="Path to a completed experiment directory containing runs.jsonl.",
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=CEILING_THRESHOLD,
        metavar="N",
        help=f"Models scoring floor-level on ALL bias types to trigger CEILING. "
             f"Default: {CEILING_THRESHOLD}.",
    )
    parser.add_argument(
        "--floor",
        type=float,
        default=FLOOR_BSI,
        metavar="F",
        help=f"Mean BSI below which a model is considered floor-level. "
             f"Default: {FLOOR_BSI}.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        metavar="FILE",
        help="Write the JSON result to this file (default: <experiment_dir>/ceiling_effect.json).",
    )
    args = parser.parse_args(argv)

    exp_dir: Path = args.experiment_dir.resolve()
    if not exp_dir.is_dir():
        print(f"Error: experiment directory not found: {exp_dir}", file=sys.stderr)
        sys.exit(1)

    runs_jsonl = exp_dir / "runs.jsonl"
    if not runs_jsonl.exists():
        print(
            f"Error: runs.jsonl not found in {exp_dir}. "
            "Run the experiment first.",
            file=sys.stderr,
        )
        sys.exit(1)

    output_path: Path = args.output or (exp_dir / "ceiling_effect.json")

    print(f"Analyzing ceiling effect for: {exp_dir}")
    print(f"  Threshold : {args.threshold} models")
    print(f"  Floor BSI : {args.floor}")
    print()

    result = analyze_ceiling_effect(
        exp_dir,
        threshold=args.threshold,
        floor=args.floor,
        output_path=output_path,
    )

    # ── Print summary ─────────────────────────────────────────────────────────
    sep = "=" * 64
    print(sep)
    gate = result["gate"]
    gate_icon = {"PROCEED": "✓", "CEILING": "!", "INSUFFICIENT": "?"}.get(gate, gate)
    print(f"  GATE: {gate_icon}  {gate}")
    print(sep)
    print(f"  Models analyzed : {result['n_models']}")
    print(f"  Valid runs      : {result['n_valid_runs']} / {result['n_total_runs']}")
    print(f"  Floor models    : {result['n_floor_models']} / {result['n_models']}")
    print()
    print(f"  {result['recommendation']}")
    print()

    if result["per_model"]:
        print("  Per-model breakdown:")
        for model_id, bias_map in sorted(result["per_model"].items()):
            all_floor = bias_map.get("all_floor", False)
            flag = " [FLOOR]" if all_floor else ""
            bias_str = "  ".join(
                f"{k}={v:.3f}"
                for k, v in bias_map.items()
                if k != "all_floor"
            )
            print(f"    {model_id:<55s}{flag}")
            print(f"      {bias_str}")
    print()

    # Print Gate 1 decision
    gate1 = result.get("gate1", {})
    if gate1:
        g1_icon = "✓" if gate1.get("proceed") else "✗"
        print(f"  Gate 1 (O.3): {g1_icon}  {'PROCEED' if gate1.get('proceed') else 'HOLD'}")
        print(f"    {gate1.get('criterion1_detail', '')}")
        print(f"    {gate1.get('criterion2_detail', '')}")
        print(f"    → {gate1.get('recommendation', '')}")
        print()

    print(f"  Results written to: {output_path}")
    print()

    # Print next-step guidance
    if gate == "PROCEED" and gate1.get("proceed", False):
        print("Next steps:")
        print("  ✓ Gate 1 PASSED — proceed to full N=50 realistic experiment.")
        print("    python research/scripts/00_define_experiment.py --design realistic")
    elif gate == "CEILING" or (gate == "PROCEED" and not gate1.get("proceed", True)):
        print("Next steps:")
        print("  ! Before the full N=50 run:")
        if gate == "CEILING":
            print("    1. Deploy REV-4 hard-difficulty scenarios (p2-09, p2-10, p2-11).")
        if gate1 and not gate1.get("criterion1_pass", True):
            print("    1. Investigate infrastructure errors (error rate too high).")
        print("    2. Re-run the pilot_full experiment.")
        print("    3. Re-analyze with this script.")
    elif gate == "INSUFFICIENT":
        print("Next steps:")
        print(f"  ? Add more models to reach ≥{args.threshold} for the gate decision.")


if __name__ == "__main__":
    main()
