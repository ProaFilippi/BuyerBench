"""
Script 09: Unified Research Gate Status Dashboard
==================================================
Checks the status of all four O.3 Decision Gates from available experiment
artifacts and prints a consolidated go/no-go dashboard.

Gates (Section O.3):
  Gate 1  (after pilot_full):         infrastructure health + BSI variation
  Gate 2  (after robustness pilot):   prompt sensitivity CV < 60%
  Gate 3  (after N=50 full run):      ≥3/10 models show detectable bias
  Gate 4  (before submission):        N.2 claim-tier filter applied to paper

Artifacts read:
  Gate 1 — <pilot-dir>/ceiling_effect.json
  Gate 2 — <robustness-dir>/robustness_pilot.json
  Gate 3 — <full-dir>/gate3.json  (or computed from cells.json)
  Gate 4 — manual checklist (displayed, not auto-checked)

Auto-discovery (when flags are omitted):
  Gate 1 — latest ``pillar2-pilot_full-*`` in results/experiments/
  Gate 2 — results/robustness-pilot/robustness_pilot.json
  Gate 3 — latest ``pillar2-realistic-*`` in results/experiments/

Usage:
  # Show all gates (auto-discover):
  python research/scripts/09_check_all_gates.py

  # Specify experiment directories explicitly:
  python research/scripts/09_check_all_gates.py \\
      --pilot-dir   results/experiments/pillar2-pilot_full-YYYYMMDD-HHMMSS \\
      --robustness-dir results/robustness-pilot \\
      --full-dir    results/experiments/pillar2-realistic-YYYYMMDD-HHMMSS

  # Check only one gate:
  python research/scripts/09_check_all_gates.py --gate 1 --pilot-dir <dir>

  # Write a Markdown status report:
  python research/scripts/09_check_all_gates.py --report docs/paper/GATE-STATUS.md
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

# Gate 2 threshold mirrors harness/robustness_pilot.py
GATE2_CV_THRESHOLD: float = 0.60

# Default search root for experiment directories
_DEFAULT_EXPERIMENTS_DIR = _REPO_ROOT / "results" / "experiments"
_DEFAULT_ROBUSTNESS_FILE = _REPO_ROOT / "results" / "robustness-pilot" / "robustness_pilot.json"


# ── Status sentinel ────────────────────────────────────────────────────────────

class GateStatus:
    PASS = "PASS"
    FAIL = "FAIL"
    PENDING = "PENDING"   # artifact exists but real-model data not yet collected
    MISSING = "MISSING"   # required artifact not found


# ── Auto-discovery ─────────────────────────────────────────────────────────────

def _latest_matching_dir(pattern: str, search_root: Path = _DEFAULT_EXPERIMENTS_DIR) -> Optional[Path]:
    """Return the most recently modified directory matching *pattern* in *search_root*."""
    if not search_root.is_dir():
        return None
    matches = sorted(
        (d for d in search_root.iterdir() if d.is_dir() and d.name.startswith(pattern)),
        key=lambda d: d.stat().st_mtime,
        reverse=True,
    )
    return matches[0] if matches else None


def _auto_discover(
    pilot_dir: Optional[Path],
    robustness_dir: Optional[Path],
    full_dir: Optional[Path],
) -> tuple[Optional[Path], Optional[Path], Optional[Path]]:
    """Fill in any ``None`` paths via auto-discovery."""
    if pilot_dir is None:
        pilot_dir = _latest_matching_dir("pillar2-pilot_full-")
    if robustness_dir is None and _DEFAULT_ROBUSTNESS_FILE.parent.is_dir():
        robustness_dir = _DEFAULT_ROBUSTNESS_FILE.parent
    if full_dir is None:
        full_dir = _latest_matching_dir("pillar2-realistic-")
    return pilot_dir, robustness_dir, full_dir


# ── Gate checkers ──────────────────────────────────────────────────────────────

def check_gate1(pilot_dir: Optional[Path]) -> dict:
    """Load and interpret the Gate 1 result from *pilot_dir*/ceiling_effect.json.

    Returns a dict with keys: ``status``, ``proceed``, ``criterion1``,
    ``criterion2``, ``recommendation``, ``source_file``, ``n_models``,
    ``mock_only`` (True if only mock-agent-v1 data detected).
    """
    if pilot_dir is None:
        return {
            "status": GateStatus.MISSING,
            "proceed": False,
            "recommendation": (
                "No pilot_full experiment directory found.  "
                "Run: python research/scripts/01_run_pilot_full.py"
            ),
            "source_file": None,
        }

    ceiling_path = Path(pilot_dir) / "ceiling_effect.json"
    if not ceiling_path.exists():
        return {
            "status": GateStatus.MISSING,
            "proceed": False,
            "recommendation": (
                f"ceiling_effect.json not found in {pilot_dir}.  "
                "Run: python research/scripts/03_analyze_ceiling_effect.py "
                f"--experiment-dir {pilot_dir}"
            ),
            "source_file": str(ceiling_path),
        }

    data = json.loads(ceiling_path.read_text(encoding="utf-8"))
    gate1 = data.get("gate1", {})

    proceed = gate1.get("proceed", False)
    n_models = data.get("n_models", 0)

    # Detect mock-only run (single model, all BSI=0 — deterministic)
    mock_only = (n_models <= 1) or (
        data.get("gate", "") == "INSUFFICIENT"
        and n_models < 3
    )

    if mock_only:
        status = GateStatus.PENDING
    elif proceed:
        status = GateStatus.PASS
    else:
        status = GateStatus.FAIL

    return {
        "status": status,
        "proceed": proceed,
        "criterion1_pass": gate1.get("criterion1_pass"),
        "criterion1_detail": gate1.get("criterion1_detail", ""),
        "criterion2_pass": gate1.get("criterion2_pass"),
        "criterion2_detail": gate1.get("criterion2_detail", ""),
        "recommendation": gate1.get("recommendation", data.get("recommendation", "")),
        "source_file": str(ceiling_path),
        "n_models": n_models,
        "mock_only": mock_only,
        "ceiling_gate": data.get("gate", ""),
    }


def check_gate2(robustness_dir: Optional[Path]) -> dict:
    """Load and interpret the Gate 2 result from *robustness_dir*/robustness_pilot.json.

    Returns a dict with keys: ``status``, ``proceed``, ``overall_recommendation``,
    ``scenarios_passing``, ``scenarios_failing``, ``mock_only``, ``recommendation``,
    ``source_file``.
    """
    if robustness_dir is None:
        return {
            "status": GateStatus.MISSING,
            "proceed": False,
            "recommendation": (
                "No robustness pilot directory found.  "
                "Run: python -m buyerbench robustness-pilot --agent <model>"
            ),
            "source_file": None,
        }

    pilot_file = Path(robustness_dir) / "robustness_pilot.json"
    if not pilot_file.exists():
        return {
            "status": GateStatus.MISSING,
            "proceed": False,
            "recommendation": (
                f"robustness_pilot.json not found in {robustness_dir}.  "
                "Run: python -m buyerbench robustness-pilot --agent <model> "
                f"--output-dir {robustness_dir}"
            ),
            "source_file": str(pilot_file),
        }

    data = json.loads(pilot_file.read_text(encoding="utf-8"))
    overall = data.get("overall_recommendation", "")
    proceed = overall == "PROCEED"
    scenarios_failing = data.get("scenarios_failing", 0)

    # Check if all per-phrasing BSIs are exactly 0 (mock-only pattern)
    all_zero = all(
        scenario.get("mean_of_means", -1) == 0.0
        for scenario in data.get("per_scenario", {}).values()
    )
    mock_only = all_zero and data.get("n_runs", 0) > 0

    if mock_only:
        status = GateStatus.PENDING
    elif proceed:
        status = GateStatus.PASS
    else:
        status = GateStatus.FAIL

    failing_scenarios = data.get("scenarios_to_redesign", [])
    if proceed:
        recommendation = (
            f"Gate 2 PASSED — all {data.get('scenarios_passing', 0)} scenario(s) "
            f"show CV ≤ {data.get('cv_threshold', GATE2_CV_THRESHOLD):.0%}.  "
            "Proceed to full N=50 experiment."
        )
    else:
        recommendation = (
            f"Gate 2 FAILED — {scenarios_failing} scenario(s) show high prompt "
            f"sensitivity (CV > {data.get('cv_threshold', GATE2_CV_THRESHOLD):.0%}).  "
            f"Redesign prompt wording for: {', '.join(failing_scenarios)}.  "
            "Do not proceed until CV drops below threshold."
        )

    return {
        "status": status,
        "proceed": proceed,
        "overall_recommendation": overall,
        "scenarios_passing": data.get("scenarios_passing", 0),
        "scenarios_failing": scenarios_failing,
        "cv_threshold": data.get("cv_threshold", GATE2_CV_THRESHOLD),
        "mock_only": mock_only,
        "recommendation": recommendation,
        "source_file": str(pilot_file),
    }


def check_gate3(full_dir: Optional[Path]) -> dict:
    """Load and interpret the Gate 3 result from *full_dir*/gate3.json.

    Returns a dict with keys: ``status``, ``proceed``, ``n_models_with_bias``,
    ``robust_rationality_pivot``, ``recommendation``, ``source_file``.
    """
    if full_dir is None:
        return {
            "status": GateStatus.MISSING,
            "proceed": False,
            "recommendation": (
                "No full realistic N=50 experiment directory found.  "
                "Run: python research/scripts/02_run_full_experiment.py "
                "--pilot-dir <pilot_dir>"
            ),
            "source_file": None,
        }

    full_dir = Path(full_dir)
    gate3_path = full_dir / "gate3.json"
    cells_path = full_dir / "cells.json"

    if not gate3_path.exists() and not cells_path.exists():
        return {
            "status": GateStatus.MISSING,
            "proceed": False,
            "recommendation": (
                f"Neither gate3.json nor cells.json found in {full_dir}.  "
                "Run: python research/scripts/08_run_flagship.py "
                f"--full-dir {full_dir} --analyze-gate3"
            ),
            "source_file": str(gate3_path),
        }

    if gate3_path.exists():
        raw = json.loads(gate3_path.read_text(encoding="utf-8"))
        gate3 = raw.get("gate3", raw)
        source = str(gate3_path)
    else:
        # cells.json exists but gate3.json not generated yet — guide the user
        return {
            "status": GateStatus.MISSING,
            "proceed": False,
            "recommendation": (
                f"cells.json found in {full_dir} but gate3.json not yet generated.  "
                "Run: python research/scripts/08_run_flagship.py "
                f"--full-dir {full_dir} --analyze-gate3"
            ),
            "source_file": str(cells_path),
        }

    proceed = gate3.get("proceed", False)
    pivot = gate3.get("robust_rationality_pivot", False)

    if proceed:
        status = GateStatus.PASS
    else:
        status = GateStatus.FAIL

    return {
        "status": status,
        "proceed": proceed,
        "n_models_with_bias": gate3.get("n_models_with_bias", 0),
        "robust_rationality_pivot": pivot,
        "criterion_detail": gate3.get("criterion_detail", ""),
        "recommendation": gate3.get("recommendation", ""),
        "source_file": source,
    }


def build_gate4_checklist() -> list[dict]:
    """Return the Gate 4 (pre-submission) checklist items.

    Each item has keys: ``label``, ``instruction``, ``note``.
    Gate 4 is always manual — no artifact can confirm it automatically.
    """
    return [
        {
            "label": "Pre-registration posted on OSF",
            "instruction": "Upload docs/preregistration/prereg_osf.md to OSF and obtain a DOI.",
            "note": "Required before any data collection with real models.",
        },
        {
            "label": "Claim tiers applied to all result statements",
            "instruction": (
                "Each result statement in Sections 4–5 must carry an explicit "
                "tier label (Tier A: confirmatory data; Tier B: descriptive; "
                "Tier C: future work only).  No Tier C claims in main text."
            ),
            "note": "See N.2 / evaluators/pillar2.py CLAIM TIER HIERARCHY.",
        },
        {
            "label": "BH-FDR correction applied to confirmatory tests",
            "instruction": (
                "Run research/analysis/corrections.py on H1, H3, H5, H7 only.  "
                "Report both raw p-values and BH-adjusted q-values."
            ),
            "note": "Corrections module: results/stats_pipeline.py.",
        },
        {
            "label": "Prompt sensitivity table in Appendix D.1 filled",
            "instruction": (
                "Replace {{RESULT:...}} placeholders in Appendix D with "
                "actual CV values from results/robustness-pilot/robustness_pilot.json."
            ),
            "note": "Gate 2 clearance populates this table.",
        },
        {
            "label": "Temperature robustness table in Appendix D.2 filled",
            "instruction": (
                "Replace {{RESULT:...}} placeholders in Appendix D.2 with "
                "actual BSI comparison across T=0.7 and T=0.0 runs."
            ),
            "note": "Requires robustness_t0 experiment completion.",
        },
        {
            "label": "Model version registry in Appendix E filled",
            "instruction": (
                "Record exact model IDs, version strings, and access dates "
                "for all 10 OpenRouter models used in the full experiment."
            ),
            "note": "Populated automatically when --no-pin-versions is NOT passed.",
        },
        {
            "label": "OSF pre-registration deviation log completed",
            "instruction": (
                "Fill in Appendix A with any deviations from the pre-registered plan.  "
                "Document whether each deviation was pre-specified or post-hoc."
            ),
            "note": "Even zero deviations must be stated explicitly.",
        },
        {
            "label": "No Tier C claims in abstract or main text",
            "instruction": (
                "Final scan: grep for mechanistic claims, architectural inferences, "
                "and cross-domain generalizations.  Move or delete any found."
            ),
            "note": "Tier C examples: 'because the model learned', 'suggests in general'.",
        },
    ]


# ── Formatter ─────────────────────────────────────────────────────────────────

_STATUS_ICONS = {
    GateStatus.PASS: "✓",
    GateStatus.FAIL: "✗",
    GateStatus.PENDING: "○",
    GateStatus.MISSING: "—",
}

_STATUS_LABELS = {
    GateStatus.PASS: "PASS",
    GateStatus.FAIL: "FAIL",
    GateStatus.PENDING: "PENDING (mock data only)",
    GateStatus.MISSING: "MISSING (artifact not found)",
}


def _print_gate(
    num: int,
    title: str,
    result: dict,
    verbose: bool = True,
) -> None:
    icon = _STATUS_ICONS.get(result["status"], "?")
    label = _STATUS_LABELS.get(result["status"], result["status"])
    print(f"  Gate {num}  {icon}  {label}   — {title}")
    if verbose:
        rec = result.get("recommendation", "")
        if rec:
            print(f"           {rec}")
        src = result.get("source_file")
        if src:
            print(f"           Artifact: {src}")
        print()


def _print_gate4(checklist: list[dict], verbose: bool = True) -> None:
    print(f"  Gate 4  ○  MANUAL CHECKLIST   — Pre-submission claim-tier filter")
    if verbose:
        print()
        for i, item in enumerate(checklist, 1):
            print(f"    {i}. [ ] {item['label']}")
            print(f"           {item['instruction']}")
            if item.get("note"):
                print(f"           Note: {item['note']}")
        print()


def _render_markdown(
    gate1: dict,
    gate2: dict,
    gate3: dict,
    gate4_checklist: list[dict],
) -> str:
    """Render a Markdown gate-status report."""

    def _badge(status: str) -> str:
        return {
            GateStatus.PASS: "✅ PASS",
            GateStatus.FAIL: "❌ FAIL",
            GateStatus.PENDING: "⏳ PENDING",
            GateStatus.MISSING: "⚠️ MISSING",
        }.get(status, status)

    lines = [
        "---",
        "type: report",
        "title: Research Gate Status Dashboard",
        "created: 2026-04-17",
        "tags:",
        "  - buyerbench",
        "  - research",
        "  - gates",
        "related:",
        "  - '[[PILLAR2-RESEARCH-07]]'",
        "---",
        "",
        "# Research Gate Status Dashboard",
        "",
        "Auto-generated by `research/scripts/09_check_all_gates.py`.  "
        "See Section O.3 of PILLAR2-RESEARCH-07 for gate definitions.",
        "",
        "| Gate | Status | Description |",
        "|------|--------|-------------|",
        f"| Gate 1 | {_badge(gate1['status'])} | Infrastructure health + BSI variation (after pilot_full) |",
        f"| Gate 2 | {_badge(gate2['status'])} | Prompt sensitivity CV < 60% (after robustness pilot) |",
        f"| Gate 3 | {_badge(gate3['status'])} | ≥3/10 models show detectable bias (after N=50 full run) |",
        "| Gate 4 | ⏳ MANUAL | N.2 claim-tier filter applied to paper (before submission) |",
        "",
    ]

    def _gate_section(num: int, title: str, result: dict) -> list[str]:
        s = [f"## Gate {num} — {title}", ""]
        s.append(f"**Status:** {_badge(result['status'])}")
        if result.get("source_file"):
            s.append(f"**Artifact:** `{result['source_file']}`")
        if result.get("recommendation"):
            s.append(f"**Recommendation:** {result['recommendation']}")
        if result.get("mock_only"):
            s.append("")
            s.append("> ⚠️  Artifact produced by **mock-agent-v1** only.  "
                     "BSI is deterministically 0 — PENDING until real-model runs are available.  "
                     "Set `OPENROUTER_API_KEY` and re-run the relevant experiment script.")
        s.append("")
        return s

    lines += _gate_section(
        1,
        "Infrastructure Health + BSI Variation (pilot_full)",
        gate1,
    )
    if gate1.get("criterion1_detail"):
        lines.append(f"- Criterion 1: {gate1['criterion1_detail']}")
    if gate1.get("criterion2_detail"):
        lines.append(f"- Criterion 2: {gate1['criterion2_detail']}")
    lines.append("")

    lines += _gate_section(
        2,
        "Prompt Sensitivity CV < 60% (robustness pilot)",
        gate2,
    )
    if gate2.get("scenarios_passing") is not None:
        lines.append(f"- Scenarios passing: {gate2['scenarios_passing']}")
    if gate2.get("scenarios_failing") is not None:
        lines.append(f"- Scenarios failing: {gate2['scenarios_failing']}")
    lines.append("")

    lines += _gate_section(
        3,
        "≥3/10 Models Show Detectable Bias (full N=50 run)",
        gate3,
    )
    if gate3.get("criterion_detail"):
        lines.append(f"- Detail: {gate3['criterion_detail']}")
    if gate3.get("robust_rationality_pivot"):
        lines.append("")
        lines.append(
            "> 💡  **Robust Rationality Pivot:** No models show detectable bias at N=50.  "
            "Reframe as 'LLMs exhibit surprising resistance to standard procurement biases' — "
            "still publishable with different framing."
        )
    lines.append("")

    lines += [
        "## Gate 4 — Pre-Submission Claim-Tier Filter (manual)",
        "",
        "Apply the N.2 claim-tier hierarchy to every result statement before submission.  "
        "Each item below must be confirmed manually.",
        "",
    ]
    for i, item in enumerate(gate4_checklist, 1):
        lines.append(f"- [ ] **{item['label']}**")
        lines.append(f"  - {item['instruction']}")
        if item.get("note"):
            lines.append(f"  - *Note:* {item['note']}")
    lines.append("")

    lines += [
        "## Next Steps",
        "",
        "```",
        "# Gate 1 — pilot with real models:",
        "OPENROUTER_API_KEY=<key> python research/scripts/01_run_pilot_full.py",
        "python research/scripts/03_analyze_ceiling_effect.py \\",
        "    --experiment-dir results/experiments/<pilot_full_id>",
        "",
        "# Gate 2 — prompt robustness pilot with real model:",
        "python -m buyerbench robustness-pilot --agent openrouter-anthropic-claude-3.5-sonnet \\",
        "    --pair-id p2-01-anchoring p2-02-framing p2-03-decoy p2-04-scarcity p2-05-sunk-cost",
        "",
        "# Gate 3 — after N=50 realistic experiment:",
        "python research/scripts/08_run_flagship.py \\",
        "    --full-dir results/experiments/<realistic_id> --analyze-gate3",
        "",
        "# Re-run this dashboard after each step:",
        "python research/scripts/09_check_all_gates.py",
        "```",
        "",
    ]

    return "\n".join(lines)


# ── CLI ────────────────────────────────────────────────────────────────────────

def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="python research/scripts/09_check_all_gates.py",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--pilot-dir",
        type=Path,
        default=None,
        metavar="DIR",
        help=(
            "Path to a completed pilot_full experiment directory "
            "(contains ceiling_effect.json).  Auto-discovered if omitted."
        ),
    )
    parser.add_argument(
        "--robustness-dir",
        type=Path,
        default=None,
        metavar="DIR",
        help=(
            "Path to directory containing robustness_pilot.json.  "
            "Auto-discovered if omitted."
        ),
    )
    parser.add_argument(
        "--full-dir",
        type=Path,
        default=None,
        metavar="DIR",
        help=(
            "Path to a completed full realistic N=50 experiment directory "
            "(contains gate3.json or cells.json).  Auto-discovered if omitted."
        ),
    )
    parser.add_argument(
        "--gate",
        type=int,
        choices=[1, 2, 3, 4],
        default=None,
        metavar="N",
        help="Check only gate N (1–4).  Default: all gates.",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=None,
        metavar="FILE",
        help="Write a Markdown gate-status report to FILE.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Print only status lines; suppress recommendations and artifact paths.",
    )
    args = parser.parse_args(argv)

    verbose = not args.quiet

    pilot_dir, robustness_dir, full_dir = _auto_discover(
        args.pilot_dir, args.robustness_dir, args.full_dir
    )

    # Compute requested gates
    gate1 = check_gate1(pilot_dir) if args.gate in (None, 1) else None
    gate2 = check_gate2(robustness_dir) if args.gate in (None, 2) else None
    gate3 = check_gate3(full_dir) if args.gate in (None, 3) else None
    gate4_checklist = build_gate4_checklist() if args.gate in (None, 4) else None

    sep = "=" * 70
    print()
    print(sep)
    print("  BuyerBench Pillar 2 — Research Gate Status (Section O.3)")
    print(sep)
    print()

    if gate1 is not None:
        _print_gate(1, "Infrastructure + BSI Variation (pilot_full)", gate1, verbose)
    if gate2 is not None:
        _print_gate(2, "Prompt Sensitivity CV < 60% (robustness pilot)", gate2, verbose)
    if gate3 is not None:
        _print_gate(3, "≥3/10 Models Detectable Bias (full N=50 run)", gate3, verbose)
    if gate4_checklist is not None:
        _print_gate4(gate4_checklist, verbose)

    # Summary line
    all_results = {
        k: v for k, v in {1: gate1, 2: gate2, 3: gate3}.items() if v is not None
    }
    statuses = [r["status"] for r in all_results.values()]
    n_pass = statuses.count(GateStatus.PASS)
    n_fail = statuses.count(GateStatus.FAIL)
    n_pending = statuses.count(GateStatus.PENDING)
    n_missing = statuses.count(GateStatus.MISSING)

    print(sep)
    print(
        f"  Summary: {n_pass} PASS  |  {n_fail} FAIL  |  "
        f"{n_pending} PENDING  |  {n_missing} MISSING"
    )
    if n_pending > 0 or n_missing > 0:
        print()
        print("  To advance pending/missing gates:")
        print("    Gate 1: python research/scripts/01_run_pilot_full.py")
        print("    Gate 2: python -m buyerbench robustness-pilot --agent <model>")
        print("    Gate 3: python research/scripts/02_run_full_experiment.py --pilot-dir <dir>")
    print(sep)
    print()

    # Write Markdown report if requested
    if args.report and all(r is not None for r in [gate1, gate2, gate3, gate4_checklist]):
        md = _render_markdown(gate1, gate2, gate3, gate4_checklist)
        out = Path(args.report)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(md, encoding="utf-8")
        print(f"  Markdown report written to: {out}")
        print()

    # Exit with error if any gate explicitly FAILED (not PENDING/MISSING)
    if n_fail > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
