---
type: reference
title: Journal Strategy Decision Tree — BuyerBench Pillar 2
created: 2026-04-15
tags:
  - journal-strategy
  - submission-planning
  - behavioral-economics
  - pillar2
related:
  - '[[tier1-top-general-interest-journals]]'
  - '[[tier2-field-behavioral-journals]]'
  - '[[tier3-adjacent-journals]]'
  - '[[tier4-primary-submission-strategy]]'
  - '[[tier5-fallback-journals]]'
  - '[[SUBMISSION-CHECKLIST]]'
---

# Journal Strategy Decision Tree

This document is the **quick-reference dispatch table** for selecting a submission venue. It consolidates the decision logic from the full tier analyses into a single actionable flow. Before submitting, run through the gates in order; the first gate that matches your evidence state determines the correct venue.

For the detailed rationale behind any gate, see the referenced tier document.

---

## Primary Decision Gate

```
GATE 1 — Sample Size
  N ≥ 50 runs per (bias type × model) cell?
      YES  → pass to GATE 2
      NO   → N ≥ 30?
                YES  → pass to GATE 2 with "exploratory" framing flag
                NO   → STOP → go to FALLBACK GATE (below)

GATE 2 — Bias and Model Coverage
  ≥ 6 bias types with controlled-variant pairs?
      YES  → pass to GATE 3
      NO   → ≥ 5 bias types?
                YES  → pass to GATE 3 with coverage-limitation note
                NO   → STOP → go to FALLBACK GATE (below)

  ≥ 8 models spanning ≥ 2 capability tiers?
      YES  → pass to GATE 3
      NO   → STOP → route to JBDM (not JEBO)

GATE 3 — Analysis Completeness
  Mixed-effects regression implemented?          YES / NO
  Multiple comparison correction (FDR) applied?  YES / NO
  Variance decomposition reported?               YES / NO
  BSI metric formally defined?                   YES / NO
  Stochasticity / temperature analysis present?  YES / NO
  Code + data publicly released?                 YES / NO

  All 6 YES  → Submit to JEBO (primary target)
  4–5 YES    → Submit to JEBO with planned-revision note
               OR route to Experimental Economics
  < 4 YES    → Route to JBDM or Tier 5; hold JEBO submission
```

---

## Fallback Gate (N < 30 or < 5 Bias Types)

```
If N < 30 per cell OR < 5 bias types:
    → Treat current runs as a PILOT only
    → Do NOT submit to JEBO or Experimental Economics
    → Applicable venues:
        < 5 bias types, ≥ 3 types    → Journal of Behavioral Decision Making (JBDM)
        N < 30 per cell but N ≥ 15   → Journal of Economic Psychology (JEP)
                                        with "preliminary evidence" framing
        Any N, null result confirmed → PLOS ONE (unconditional publication floor)
        Any N, exploratory            → Working paper (SSRN) before peer submission
    → After expanding data: re-run from GATE 1
```

---

## Quick-Reference Routing Table

| Evidence State | Primary Venue | Secondary Venue | Notes |
|---|---|---|---|
| N ≥ 50 per cell; ≥ 6 bias types; ≥ 8 models | **JEBO** | Experimental Economics | Full analysis suite required |
| N = 30–49 per cell; ≥ 5 bias types; ≥ 8 models | **JEBO** (exploratory) | JBDM | Use "exploratory" framing; no confirmatory H1/H2 |
| N = 30–49; ≥ 5 bias types; < 8 models | **JBDM** | DSS (Tier 3) | Add models before JEBO attempt |
| N < 30 per cell | **JEP** | PLOS ONE | Pilot only; expand before flagship submission |
| Null result (bias indistinguishable from noise) | **PLOS ONE** | JEP | PLOS ONE accepts null results unconditionally |
| WARP battery completed (N ≥ 50 per model) | **GEB** | — | Separate paper; do not bundle with bias battery |
| < 3 bias types | Working paper only | — | Not peer-submittable until bias coverage expands |

---

## Minimum Viable Paper Specification

The minimum evidence threshold for a **credible JEBO submission** is:

```
5 bias types
× 10 models
× 30 runs per (bias type × model) cell
= 1,500 total agent-run observations
```

### Feasibility

| Dimension | Estimate |
|---|---|
| API cost at $0.15/run (OpenRouter) | ~$225 |
| Execution time | One weekend (parallelized via OpenRouter) |
| Analysis time | ~2 weeks (mixed-effects models, variance decomp, power) |
| Writing time (to journal-quality draft) | 4–6 weeks |
| Total time from data collection to JEBO submission | ~10–12 weeks |

### Preferred ("strong") Specification

```
5 bias types
× 10 models
× 50 runs per cell
= 2,500 total observations
+ temperature ablation (3 settings: 0.0, 0.5, 1.0)
+ human comparison arm (100 MTurk subjects × 10 scenarios ≈ $500–700)
```

This preferred specification raises the submission from "JEBO with caveats" to "JEBO with clear acceptance probability" and opens Experimental Economics as a co-equal target.

---

## Routing Logic Explained

**Why JEBO at N = 50 (not N = 30)?**
N = 30 per cell achieves ~60% power at d = 0.5 (medium effect). This is technically publishable but reviewers will raise power concerns. N = 50 achieves ~80% power — the conventional minimum for confirmatory behavioral economics research. At $0.15/run, the additional 20 runs per cell costs $300 more (total $375 vs. $225). This is almost always worth the upgrade.

**Why Journal of Economic Psychology at N < 30?**
JEP publishes descriptive behavioral studies without the power requirements of JEBO or Experimental Economics. A pilot paper at JEP with N = 15–29 per cell can be framed as "preliminary evidence of bias susceptibility in LLM agents" — establishing a citable finding while the flagship data collection sprint is planned. JEP papers are citable by JEBO reviewers, making the pilot publication a strategic investment, not a consolation prize.

**Why PLOS ONE for null results?**
If the data shows no statistically significant bias susceptibility across models and bias types, the behavioral economics journals will reject on "insufficient contribution" grounds, not methodology. PLOS ONE accepts methodologically sound null results without requiring a positive finding. A BuyerBench null result — "LLM agents show no measurable systematic bias in procurement decisions at N = 1,500 observations" — is a valuable counterpoint to prior work and publishable there. See [[tier5-fallback-journals]] for the null-result strategy.

**Why not target Tier 1 journals (AER, QJE)?**
Tier 1 general-interest journals require a theoretical mechanism that revises mainstream economic theory — not just measurement. A bias battery without a structural model explaining *why* biases appear (or disappear) at different capability levels is insufficient for Tier 1. This is a 5–10 year research program, not a first-paper target. See [[tier1-top-general-interest-journals]] for the full analysis.

---

## Pre-Submission Checklist (Gate 3 Expanded)

Before submitting to any venue above JBDM, verify all of the following:

### Evidence
- [ ] N ≥ 30 (target 50) runs per (bias type × model) cell documented
- [ ] ≥ 5 bias types with controlled-variant pairs (baseline vs. manipulated)
- [ ] ≥ 8 models spanning at least 2 capability tiers

### Statistical Analysis
- [ ] Mixed-effects regression: `BSI ~ bias_type + capability_tier + (1|model) + (1|run)`
- [ ] FDR correction (Benjamini-Hochberg) across all hypothesis tests
- [ ] Variance decomposition: % of BSI variance by model vs. bias_type vs. residual
- [ ] Cohen's d with 95% CI for each bias × model cell
- [ ] Post-hoc power analysis: minimum detectable effect at observed N

### Methodology and Replication
- [ ] Full prompt templates in supplementary materials
- [ ] API version, temperature, model IDs, and seeds documented
- [ ] Code and data released on GitHub with DOI (Zenodo or OSF)
- [ ] Incentive compatibility section (LLMs cannot receive monetary payoffs)

### Positioning
- [ ] Introduction foregrounds the behavioral economics research question
- [ ] Literature review covers canonical human bias studies + LLM behavioral studies
- [ ] Discussion positions against Echterhoff et al. (2024) (most relevant prior work)
- [ ] BSI metric formally defined with equations and human calibration benchmarks

---

## Cross-References

- Detailed journal-by-journal fit analysis:
  - [[tier1-top-general-interest-journals]] — AER, QJE, JPE, Econometrica (5–10 year horizon)
  - [[tier2-field-behavioral-journals]] — JEBO, Experimental Economics, JBDM, GEB (primary targets)
  - [[tier3-adjacent-journals]] — JAIR, AI & Society, DSS, Management Science IS
  - [[tier4-primary-submission-strategy]] — Concrete JEBO preparation and rejection cascade
  - [[tier5-fallback-journals]] — JEP, JDM, PLOS ONE (null result and pilot strategies)
- Data collection plan and cost estimates: [[PILLAR2-RESEARCH-02]] Section E
- BSI metric formal definition: [[economic-rationality-metrics]]
- Statistical analysis plan: [[PILLAR2-RESEARCH-03]]
- Submission tracking: [[SUBMISSION-CHECKLIST]]
