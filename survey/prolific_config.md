---
type: reference
title: "Prolific Study Configuration — BuyerBench Human Comparison Arm"
created: 2026-04-17
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
   - Version A completion code: **{COMPLETION_CODE_A}** (generate in Prolific)
   - Version B completion code: **{COMPLETION_CODE_B}** (generate in Prolific)

---

## Data Export and Parsing

After data collection is complete:

1. Export responses from Qualtrics: Data & Analysis → Export & Import → Export Data → CSV (with choice text).
2. Ensure the export includes the `_buyerbench` metadata embedded in each question.
3. Parse responses using:

```python
from results.human_survey import parse_prolific_csv, aggregate_human_cells
from harness.loader import load_all_scenarios

scenario_map = {s.id: s for s in load_all_scenarios("scenarios")}
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
