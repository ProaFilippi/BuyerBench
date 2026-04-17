"""
Script 10: Gate 4 — Pre-Submission Claim-Tier Paper Scanner
===========================================================
Scans the Pillar 2 working paper for Tier C violations in the main text
and counts unresolved result placeholders.

Gate 4 enforces the N.2 claim-tier hierarchy (Section N.2, PILLAR2-RESEARCH-07):
  Tier A — Fully Defensible: N≥50, BH-FDR, pre-registered confirmatory hypotheses
  Tier B — Suggestive: descriptive patterns, N=10 models, no p-values, must qualify
  Tier C — Speculative: future work only; must NOT appear in:
    Abstract, Sections 1–6, or References

Tier C examples (violation patterns):
  - Mechanistic attribution ("because the model", "architecture causes")
  - Unhedged cross-domain generalization ("generalizes beyond procurement")
  - Categorical behavioral claims ("all LLMs always show")
  - Scaffolding labels not stripped ("[TIER-C]" left in text)

Gate verdict:
  PASS    — zero Tier C violations in main text
  PENDING — zero violations but unresolved {{RESULT:...}} placeholders remain
             (paper template not yet populated; check again after data collection)
  FAIL    — one or more Tier C violations detected in main text

Usage:
  python research/scripts/10_gate4_paper_scan.py
  python research/scripts/10_gate4_paper_scan.py --paper docs/paper/pillar2-working-paper.md
  python research/scripts/10_gate4_paper_scan.py --quiet
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Optional

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

# Default paper path (relative to repo root)
PAPER_PATH = _REPO_ROOT / "docs" / "paper" / "pillar2-working-paper.md"

# Regex that marks the start of appendix content (split point)
_APPENDIX_START_RE = re.compile(r"^##\s+Appendix\s+", re.MULTILINE | re.IGNORECASE)

# Unresolved result placeholder pattern
_PLACEHOLDER_RE = re.compile(r"\{\{RESULT:[^}]+\}\}")

# ── Tier C violation patterns ──────────────────────────────────────────────────
# Each entry: (compiled_regex, category_slug, human_description)
# Patterns target language that is unambiguously Tier C when found in main text:
#   1. Scaffolding labels not stripped from the document
#   2. Direct attribution of behavior to model architecture
#   3. Unhedged cross-domain generalization
#   4. Categorical "all LLMs" behavioral claims

TIER_C_PATTERNS: list[tuple[re.Pattern, str, str]] = [
    (
        re.compile(r"\[TIER-C\]", re.IGNORECASE),
        "scaffolding-label",
        "[TIER-C] scaffolding label not stripped from main text",
    ),
    (
        re.compile(
            r"\b(caused by|due to)\s+(the\s+)?"
            r"(transformer|self-attention|rlhf|reinforcement learning from human feedback"
            r"|fine-?tuning|pre-?training)\b",
            re.IGNORECASE,
        ),
        "architectural-inference",
        "Causal attribution to model architecture components (Tier C — mechanism not tested)",
    ),
    (
        re.compile(
            r"\b(generali[sz]e|transfer)s?\s+(to|beyond|across)\s+"
            r"(all|other|any|non-procurement|different|every)\b",
            re.IGNORECASE,
        ),
        "cross-domain-generalization",
        "Unhedged generalization beyond the procurement domain (Tier C)",
    ),
    (
        re.compile(
            r"\ball\s+(llms?|language models?|ai\s+systems?|neural\s+models?)\s+"
            r"(always|are\s+always|will\s+always|inherently|universally)\b",
            re.IGNORECASE,
        ),
        "categorical-always",
        "Categorical behavioral claim ('all LLMs always …') (Tier C — over-broad)",
    ),
    (
        re.compile(
            r"\bthe\s+(underlying\s+)?mechanism\s+(is|involves|requires|operates)\b"
            r"(?!\s+not\b)",
            re.IGNORECASE,
        ),
        "mechanism-confirmed",
        "Positive mechanism confirmation without 'not directly tested' qualifier (Tier C)",
    ),
    (
        re.compile(
            r"\b(confirms?|proves?|demonstrates?)\s+(that\s+)?(the\s+)?mechanism\b",
            re.IGNORECASE,
        ),
        "mechanism-proof",
        "Claiming the mechanism is proven or confirmed (Tier C — mechanism not tested)",
    ),
    (
        re.compile(
            r"\bbecause\s+(the\s+)?(model|llm|system|agent)\s+"
            r"(learned|was\s+trained|has\s+been\s+trained)\b",
            re.IGNORECASE,
        ),
        "training-causal",
        "Causal attribution to model training as direct explanation (Tier C)",
    ),
]


# ── Core scanner functions ─────────────────────────────────────────────────────

def split_main_and_appendix(text: str) -> tuple[str, str]:
    """Split *text* into (main_text, appendix_text) at the first ``## Appendix`` heading.

    If no appendix heading is found, the entire text is returned as main_text
    with an empty appendix_text.
    """
    m = _APPENDIX_START_RE.search(text)
    if m is None:
        return text, ""
    return text[: m.start()], text[m.start() :]


def scan_tier_c_violations(
    main_text: str,
    patterns: list[tuple[re.Pattern, str, str]] = TIER_C_PATTERNS,
) -> list[dict]:
    """Scan *main_text* for Tier C violations.

    Returns a list of dicts, one per matched line:
      ``line_number``, ``line``, ``category``, ``description``, ``match``.
    Only lines with at least one pattern match are included.
    """
    violations: list[dict] = []
    for lineno, line in enumerate(main_text.splitlines(), start=1):
        for pattern, category, description in patterns:
            m = pattern.search(line)
            if m:
                violations.append(
                    {
                        "line_number": lineno,
                        "line": line.strip(),
                        "category": category,
                        "description": description,
                        "match": m.group(0),
                    }
                )
                break  # one violation report per line (first match wins)
    return violations


def count_result_placeholders(text: str) -> int:
    """Return the number of unresolved ``{{RESULT:...}}`` placeholders in *text*."""
    return len(_PLACEHOLDER_RE.findall(text))


def run_gate4_scan(paper_path: Path = PAPER_PATH) -> dict:
    """Run the full Gate 4 paper scan.

    Returns a dict with keys:
      ``status``          — "PASS" | "PENDING" | "FAIL" | "MISSING"
      ``proceed``         — bool (True for PASS only)
      ``n_violations``    — int
      ``violations``      — list[dict] from scan_tier_c_violations
      ``n_placeholders``  — int (unresolved {{RESULT:...}} in main text)
      ``source_file``     — str
      ``recommendation``  — str
    """
    paper_path = Path(paper_path)
    if not paper_path.exists():
        return {
            "status": "MISSING",
            "proceed": False,
            "n_violations": 0,
            "violations": [],
            "n_placeholders": 0,
            "source_file": str(paper_path),
            "recommendation": (
                f"Working paper not found at {paper_path}.  "
                "Expected: docs/paper/pillar2-working-paper.md"
            ),
        }

    text = paper_path.read_text(encoding="utf-8")
    main_text, _ = split_main_and_appendix(text)

    violations = scan_tier_c_violations(main_text)
    n_placeholders = count_result_placeholders(main_text)
    n_violations = len(violations)

    if n_violations > 0:
        status = "FAIL"
        proceed = False
        recommendation = (
            f"Gate 4 FAILED — {n_violations} Tier C violation(s) found in main text.  "
            "Move or reframe all flagged statements before submission.  "
            "See violation list for line numbers."
        )
    elif n_placeholders > 0:
        status = "PENDING"
        proceed = False
        recommendation = (
            f"Gate 4 PENDING — no Tier C violations found, but {n_placeholders} "
            f"unresolved {{{{RESULT:...}}}} placeholder(s) remain in main text.  "
            "Populate results from experiment data, then re-run this scan."
        )
    else:
        status = "PASS"
        proceed = True
        recommendation = (
            "Gate 4 PASSED — no Tier C violations and no unresolved result placeholders.  "
            "Paper main text is ready for final N.2 claim-tier review before submission."
        )

    return {
        "status": status,
        "proceed": proceed,
        "n_violations": n_violations,
        "violations": violations,
        "n_placeholders": n_placeholders,
        "source_file": str(paper_path),
        "recommendation": recommendation,
    }


# ── CLI ────────────────────────────────────────────────────────────────────────

def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="python research/scripts/10_gate4_paper_scan.py",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--paper",
        type=Path,
        default=PAPER_PATH,
        metavar="FILE",
        help=(
            "Path to the working paper Markdown file.  "
            f"Default: docs/paper/pillar2-working-paper.md"
        ),
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Print only the status line; suppress violation details.",
    )
    args = parser.parse_args(argv)

    result = run_gate4_scan(args.paper)

    status = result["status"]
    icons = {"PASS": "✓", "PENDING": "○", "FAIL": "✗", "MISSING": "—"}
    icon = icons.get(status, "?")

    sep = "=" * 70
    print()
    print(sep)
    print("  BuyerBench Pillar 2 — Gate 4: Claim-Tier Paper Scan")
    print(sep)
    print()
    print(f"  {icon}  {status}   {result['recommendation']}")
    print()

    if not args.quiet:
        print(f"  Paper:          {result['source_file']}")
        print(f"  Violations:     {result['n_violations']}")
        print(f"  Placeholders:   {result['n_placeholders']}")
        print()

        if result["violations"]:
            print("  Tier C Violations Found:")
            for v in result["violations"]:
                print(f"    Line {v['line_number']:4d}: [{v['category']}] {v['description']}")
                print(f"           Match: {v['match']!r}")
                print(f"           Line:  {v['line'][:120]}")
            print()

    print(sep)
    print()

    if status == "FAIL":
        sys.exit(1)


if __name__ == "__main__":
    main()
