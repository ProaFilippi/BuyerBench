"""
Script 07: Prepare Prolific Survey for Human Comparison Arm
===========================================================
Generates Qualtrics QSF files and supporting documents for the BuyerBench
Pillar 2 human comparison arm (H10 of the pre-registered design).

DESIGN OVERVIEW
---------------
Between-subjects across variants (BASELINE vs TREATMENT), within-subjects
across bias types (each subject sees one variant of all 5 bias types).

Two survey versions are generated:

  Version A — BASELINE : subjects make procurement decisions without any
               bias manipulation (anchoring, framing, decoy, scarcity, sunk
               cost all in their neutral "reference" form).
  Version B — TREATMENT: subjects see the identical supplier options but with
               the bias manipulation active (high anchor, loss frame, decoy
               option, scarcity cue, sunk cost information).

With N=50 subjects per version (100 total), each (bias_type × variant) cell
has n ≈ 50 observations — sufficient for Wilson CI width of ±0.14 at p=0.5.

ATTENTION CHECKS
----------------
Two attention check questions are embedded at positions 2 and 5 in the final
question sequence (after the 2nd and 4th scenarios):
  ATTN1 — obvious price comparison (correct answer: $12 not $89)
  ATTN2 — direct instruction confirmation

Subjects who fail ≥1 attention check are excluded from aggregate BSI
calculations (see ``survey_manifest.json`` → ``attention_check_exclusion_rule``).

OUTPUTS
-------
All files are written to ``--output-dir`` (default: ``survey/``):

  survey_A_baseline.json     Qualtrics QSF — 5 BASELINE scenarios + ATTN1/2
  survey_B_treatment.json    Qualtrics QSF — 5 TREATMENT scenarios + ATTN1/2
  survey_manifest.json       Scenario metadata for parse_prolific_csv()
  prolific_config.md         Prolific study configuration template
  scenario_previews.md       Human-readable vignette previews for PI review

RUN
---
  python research/scripts/07_prepare_prolific_survey.py [--output-dir survey] [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from harness.loader import load_all_scenarios  # noqa: E402
from research.experiments.grid import REALISTIC_DESIGN  # noqa: E402
from results.human_survey import (  # noqa: E402
    ATTENTION_CHECK_QUESTIONS,
    export_scenario_to_survey,
    export_scenarios_to_qualtrics_with_attention_checks,
    generate_survey_manifest,
)


# ── Prolific config template ──────────────────────────────────────────────────

_PROLIFIC_CONFIG_TEMPLATE = """\
---
type: reference
title: "Prolific Study Configuration — BuyerBench Human Comparison Arm"
created: {created_date}
tags:
  - human-arm
  - prolific
  - survey-configuration
related:
  - '[[f2-flagship-design]]'
  - '[[prereg_osf]]'
---

# Prolific Study Configuration — Procurement Decision Study

> **Internal note:** This document contains the configuration for the BuyerBench
> Pillar 2 human comparison arm (H10). It is NOT a participant-facing document.
> The survey itself uses neutral language with no mention of AI or benchmarking.

---

## Study Metadata

| Field | Value |
|---|---|
| **Study title (Prolific-facing)** | Procurement Decision-Making Study (10 min) |
| **Internal identifier** | BuyerBench-P2-HumanArm-v1 |
| **Target N** | 100 subjects (50 per survey version) |
| **Estimated duration** | 8–12 minutes |
| **Completion payment** | £1.50 (~$1.90 USD) — ~£9/hour, Prolific minimum |
| **Platform** | Prolific (prolific.com) |
| **Survey platform** | Qualtrics (import QSF files before creating study) |

---

## Study Description (shown on Prolific)

> **Title:** Procurement Decision-Making Study
>
> **Description:** We are studying how people make purchasing decisions in
> professional procurement contexts. You will be presented with a series of
> supplier selection scenarios and asked to choose the best supplier based on
> the information provided. There are no right or wrong answers from our
> perspective — we are interested in your natural decision-making process.
> The study takes approximately 8–12 minutes.
>
> **Reward:** £1.50 for completing the full study.

---

## Eligibility Criteria (Prolific Filters)

| Criterion | Filter Setting |
|---|---|
| **Language** | English fluency: Fluent |
| **Country of residence** | UK, US, Australia, Canada (English-speaking; consistent with Prolific norms for procurement studies) |
| **Employment status** | Any (procurement experience is NOT required) |
| **Age** | 18–65 |
| **Approval rate** | ≥ 95 % (experienced Prolific participants) |
| **Previous submissions** | ≥ 20 approved submissions |

> **Rationale:** No domain expertise screener — the study tests naïve
> procurement intuitions analogous to the LLM-as-agent setting. Experienced
> procurement professionals would introduce expertise bias.

---

## Survey Versions

Two separate Prolific studies should be created (or one study with custom URL
routing splitting 50/50):

| Version | QSF File | Content | Prolific Study |
|---|---|---|---|
| **Version A — BASELINE** | `survey_A_baseline.json` | 5 neutral scenarios + 2 attention checks | Study link points to Qualtrics survey A |
| **Version B — TREATMENT** | `survey_B_treatment.json` | 5 bias-manipulated scenarios + 2 attention checks | Study link points to Qualtrics survey B |

**Split procedure:** Create two Prolific studies, each targeting N=50 subjects,
and run them simultaneously to balance collection. Alternatively, use Prolific's
"groups" feature to randomly assign participants to survey version A or B.

---

## Qualtrics Setup Instructions

1. Log in to Qualtrics.
2. Create Project → Import a QSF file → upload `survey_A_baseline.json`.
3. Rename the project: "Procurement Study — Version A (Baseline)" (internal name).
4. Activate the survey and copy the anonymous survey link.
5. Repeat for `survey_B_treatment.json` (Version B).
6. Paste the anonymous links into the respective Prolific studies.
7. Set the Prolific completion code in each Qualtrics survey end page:
   - Version A completion code: **{{COMPLETION_CODE_A}}** (generate in Prolific)
   - Version B completion code: **{{COMPLETION_CODE_B}}** (generate in Prolific)

---

## Data Export and Parsing

After data collection is complete:

1. Export responses from Qualtrics: Data & Analysis → Export & Import → Export Data → CSV (with choice text).
2. Ensure the export includes the `_buyerbench` metadata embedded in each question.
3. Parse responses using:

```python
from results.human_survey import parse_prolific_csv, aggregate_human_cells
from harness.loader import load_all_scenarios

scenario_map = {{s.id: s for s in load_all_scenarios("scenarios")}}
observations = parse_prolific_csv(
    "survey/prolific_responses_A.csv",
    scenario_map=scenario_map,
)
human_report = aggregate_human_cells(observations)
```

4. Concatenate Version A and Version B responses before calling `aggregate_human_cells`.
5. See `survey_manifest.json` for exact column names expected by `parse_prolific_csv`.

---

## Attention Check Exclusion

Exclude subjects who fail ≥1 attention check before computing BSI:

```python
# Attention check failure is automatically handled by aggregate_human_cells()
# when exclude_failed_attention=True (the default).
# Subjects with attention_check_passed=False are excluded from n_valid_subjects.
```

The `attention_check_col` column in the Prolific export must be mapped to the
attention check response. Qualtrics scoring logic or post-hoc Python scoring
can flag failures — see `survey_manifest.json` for the `ATTN1` / `ATTN2`
correct answers and expected response encoding.

---

## IRB Note

> ⚠️ **IRB submission required before data collection begins.**
> The survey involves human subjects. Submit an IRB application to your
> institution's review board before activating the Prolific studies.
> Anticipated review category: **Exempt** (minimal-risk online survey with
> no sensitive data collection). Estimated review time: 2–8 weeks.
>
> LLM data collection can proceed before IRB approval; the human arm is
> the critical path for the flagship timeline.

---

## Pre-Registration Note

> The human comparison arm (H10) is registered as **exploratory** in the
> BuyerBench pre-registration document (`docs/preregistration/prereg_osf.md`).
> Analysis plan: independent two-sample comparison of LLM BSI vs. human BSI
> per bias type; effect size via Cohen's d; no correction for multiple
> comparisons (exploratory, pre-specified).
"""

# ── Scenario preview generator ────────────────────────────────────────────────


def _generate_scenario_previews(
    version_a_scenarios: list,
    version_b_scenarios: list,
) -> str:
    """Build a human-readable Markdown preview of all vignettes for PI review."""
    lines: list[str] = [
        "---",
        "type: reference",
        "title: Survey Scenario Previews — Human Comparison Arm",
        "---",
        "",
        "# Survey Scenario Previews",
        "",
        "> **Purpose:** These are the exact vignettes that will be shown to Prolific",
        "> participants (after QSF rendering). Review carefully for demand effects,",
        "> unintentional cues, and correct optimal answers before activating the study.",
        "",
        "---",
        "",
        "## Version A — BASELINE",
        "",
    ]
    for i, sc in enumerate(version_a_scenarios, start=1):
        vignette = export_scenario_to_survey(sc)
        lines += [
            f"### A{i}. {vignette['title']}",
            "",
            f"**Scenario ID:** `{vignette['scenario_id']}`  ",
            f"**Variant:** `{vignette['variant']}`  ",
            f"**Bias category:** `{vignette['bias_category'] or 'n/a'}`  ",
            f"**Optimal choice:** `{vignette['optimal_choice']}`",
            "",
            f"*{vignette['preamble']}*",
            "",
            vignette["context_text"],
            "",
        ]
        if vignette["constraints_text"]:
            lines.append(f"**Requirements:** {vignette['constraints_text']}")
            lines.append("")
        lines.append(f"**Question:** {vignette['question']}")
        lines.append("")
        for choice in vignette["choices"]:
            marker = "✓" if choice == vignette["optimal_choice"] else "○"
            lines.append(f"  {marker} {choice}")
        lines += ["", "---", ""]

    lines += [
        "## Version B — TREATMENT",
        "",
    ]
    for i, sc in enumerate(version_b_scenarios, start=1):
        vignette = export_scenario_to_survey(sc)
        lines += [
            f"### B{i}. {vignette['title']}",
            "",
            f"**Scenario ID:** `{vignette['scenario_id']}`  ",
            f"**Variant:** `{vignette['variant']}`  ",
            f"**Bias category:** `{vignette['bias_category'] or 'n/a'}`  ",
            f"**Optimal choice:** `{vignette['optimal_choice']}`",
            "",
            f"*{vignette['preamble']}*",
            "",
            vignette["context_text"],
            "",
        ]
        if vignette["constraints_text"]:
            lines.append(f"**Requirements:** {vignette['constraints_text']}")
            lines.append("")
        lines.append(f"**Question:** {vignette['question']}")
        lines.append("")
        for choice in vignette["choices"]:
            marker = "✓" if choice == vignette["optimal_choice"] else "○"
            lines.append(f"  {marker} {choice}")
        lines += ["", "---", ""]

    lines += [
        "## Attention Check Questions",
        "",
    ]
    for attn in ATTENTION_CHECK_QUESTIONS:
        lines += [
            f"### {attn['attn_id']}",
            "",
            attn["question_text"].replace("<br>", "\n").replace("<b>", "**").replace("</b>", "**"),
            "",
            "**Choices:**",
        ]
        for choice in attn["choices"]:
            marker = "✓" if choice == attn["correct_choice"] else "○"
            lines.append(f"  {marker} {choice}")
        lines += ["", "---", ""]

    return "\n".join(lines)


# ── Main ──────────────────────────────────────────────────────────────────────


def load_core_scenarios(
    scenarios_dir: str | Path = "scenarios",
) -> tuple[list, list]:
    """Load Version A (BASELINE) and Version B (TREATMENT) scenario lists.

    Uses ``REALISTIC_DESIGN.bias_scenarios`` to determine which scenario IDs
    are the baseline and treatment for each of the 5 core bias types.

    Returns:
        Tuple of ``(version_a_scenarios, version_b_scenarios)`` — each a list
        of :class:`~buyerbench.models.Scenario` objects in bias-type order.
    """
    all_scenarios = load_all_scenarios(str(scenarios_dir))
    scenario_index = {sc.id: sc for sc in all_scenarios}

    bias_scenarios = REALISTIC_DESIGN["bias_scenarios"]
    version_a: list = []
    version_b: list = []

    for bias_type, ids in bias_scenarios.items():
        baseline_id = ids["baseline"]
        treatment_id = ids["treatment"]

        if baseline_id not in scenario_index:
            raise KeyError(
                f"Baseline scenario '{baseline_id}' not found in '{scenarios_dir}'. "
                f"Available IDs: {sorted(scenario_index)}"
            )
        if treatment_id not in scenario_index:
            raise KeyError(
                f"Treatment scenario '{treatment_id}' not found in '{scenarios_dir}'. "
                f"Available IDs: {sorted(scenario_index)}"
            )

        version_a.append(scenario_index[baseline_id])
        version_b.append(scenario_index[treatment_id])

    return version_a, version_b


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="python research/scripts/07_prepare_prolific_survey.py",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--output-dir",
        default="survey",
        metavar="DIR",
        help="Directory for survey output files (default: survey/).",
    )
    parser.add_argument(
        "--scenarios-dir",
        default="scenarios",
        metavar="DIR",
        help="Scenarios root directory (default: scenarios/).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print plan without writing any files.",
    )
    args = parser.parse_args(argv)

    output_dir = Path(args.output_dir)
    scenarios_dir = Path(args.scenarios_dir)

    print(f"[07] Loading core bias scenarios from '{scenarios_dir}' …")
    version_a, version_b = load_core_scenarios(scenarios_dir)

    bias_types = list(REALISTIC_DESIGN["bias_scenarios"].keys())
    print(f"[07] Loaded {len(version_a)} bias types: {', '.join(bias_types)}")
    for sc_a, sc_b in zip(version_a, version_b):
        print(f"     A: {sc_a.id}  /  B: {sc_b.id}")

    print(f"[07] Attention checks: {len(ATTENTION_CHECK_QUESTIONS)} questions at positions [2, 5]")

    if args.dry_run:
        print("[07] Dry-run mode — no files written.")
        print(f"[07] Would write to: {output_dir.resolve()}/")
        print(f"     survey_A_baseline.json")
        print(f"     survey_B_treatment.json")
        print(f"     survey_manifest.json")
        print(f"     prolific_config.md")
        print(f"     scenario_previews.md")
        return

    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate QSF files
    print("[07] Generating survey_A_baseline.json …")
    path_a = export_scenarios_to_qualtrics_with_attention_checks(
        version_a,
        output_dir / "survey_A_baseline.json",
        survey_name="Procurement Decision Study — Version A",
        attention_check_positions=[2, 5],
    )
    print(f"     Written: {path_a}")

    print("[07] Generating survey_B_treatment.json …")
    path_b = export_scenarios_to_qualtrics_with_attention_checks(
        version_b,
        output_dir / "survey_B_treatment.json",
        survey_name="Procurement Decision Study — Version B",
        attention_check_positions=[2, 5],
    )
    print(f"     Written: {path_b}")

    # Generate manifest
    print("[07] Generating survey_manifest.json …")
    bias_mapping = {
        bias_type: {
            "baseline": ids["baseline"],
            "treatment": ids["treatment"],
        }
        for bias_type, ids in REALISTIC_DESIGN["bias_scenarios"].items()
    }
    manifest = generate_survey_manifest(
        version_a,
        version_b,
        bias_mapping=bias_mapping,
        attention_check_positions=[2, 5],
        n_subjects_target=100,
        n_per_version=50,
    )
    manifest_path = output_dir / "survey_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2))
    print(f"     Written: {manifest_path}")

    # Generate Prolific config
    print("[07] Generating prolific_config.md …")
    from datetime import date

    config_text = _PROLIFIC_CONFIG_TEMPLATE.format(
        created_date=date.today().isoformat(),
    )
    config_path = output_dir / "prolific_config.md"
    config_path.write_text(config_text)
    print(f"     Written: {config_path}")

    # Generate scenario previews
    print("[07] Generating scenario_previews.md …")
    previews_text = _generate_scenario_previews(version_a, version_b)
    previews_path = output_dir / "scenario_previews.md"
    previews_path.write_text(previews_text)
    print(f"     Written: {previews_path}")

    print("[07] Done. Survey package ready.")
    print(f"     Output directory: {output_dir.resolve()}/")
    print()
    print("Next steps:")
    print("  1. Review scenario_previews.md for demand effects")
    print("  2. Submit IRB application (see prolific_config.md → IRB Note)")
    print("  3. Import QSF files into Qualtrics and test the survey")
    print("  4. After IRB approval: create Prolific studies (N=50 each)")
    print("  5. After data collection: python research/scripts/08_analyze_human_arm.py")


if __name__ == "__main__":
    main()
