---
type: research
title: "Section F.2 — Flagship Paper Design"
created: 2026-04-16
tags:
  - experimental-design
  - pillar2
  - llm-bias
  - behavioral-economics
  - flagship-design
  - factorial-design
  - human-comparison
  - power-analysis
related:
  - '[[f1-realistic-design]]'
  - '[[e6-design-comparison-matrix]]'
  - '[[d1-primary-research-question]]'
  - '[[d2-secondary-research-questions]]'
  - '[[g-econometric-strategy]]'
  - '[[b1-06-status-quo-bias-samuelson-zeckhauser-1988]]'
  - '[[b1-07-loss-aversion-kahneman-tversky-1979]]'
  - '[[b4-02-nudge-thaler-sunstein-2008]]'
---

# Section F.2 — Flagship Paper Design

---

## Summary

This document formalizes the **Flagship Paper Design** for BuyerBench Pillar 2. It extends the [[f1-realistic-design]] with three prompt versions, three additional bias types, multi-level anchoring, a human comparison arm, a full temperature sweep, and N=50 per cell. It is the design required for a top-field journal (JEBO) or human-comparison publication.

**Target journal:** JEBO or Experimental Economics (with human arm: QJE-adjacent)  
**Claim level:** "LLM bias susceptibility is heterogeneous across model capability, bias type, and prompt structure; high-capability models show lower susceptibility on average but exhibit distinctive vulnerability profiles."

---

## Components Beyond the Realistic Design

| Component | Specification | Rationale |
|---|---|---|
| **Prompt versions** | 3: (1) standard, (2) chain-of-thought instruction, (3) expert-role framing | Tests H8 (CoT reduces anchoring but not decoy); enables prompt × bias interaction; required for multi-factor variance decomposition |
| **Additional bias types** | 3: default/status quo (p2-06), loss aversion switching (p2-07), WARP transitivity battery | Extends from 5 → 8 bias categories; covers [[b1-06-status-quo-bias-samuelson-zeckhauser-1988]] and [[b1-07-loss-aversion-kahneman-tversky-1979]]; WARP battery tests preference consistency (H9) |
| **Anchor levels (p2-01)** | 3 levels: low ($60), baseline ($75), high ($91) | Enables dose-response curve for H4; tests "insufficient adjustment" mechanism at both above and below market rate |
| **Human comparison arm** | 100 subjects on Prolific; same scenarios; standard survey format | Required for H10 (LLM vs. human BSI comparison); addresses QJE-adjacent reviewers; IRB submission begins immediately |
| **Temperature sweep** | Runs at T ∈ {0.0, 0.3, 0.7, 1.0} | Maps full stochasticity surface; enables SRQ3 variance decomposition; detects T-sensitivity of results |
| **N per cell** | 50 (vs. 30 in Realistic Design) | Power = 0.70 at d=0.4; marginal but publishable; gold-standard N=100 exceeds budget for this phase |

---

## Prompt Version Specifications

### Prompt 1 — Standard

The base procurement scenario prompt from the existing BuyerBench harness. No additional reasoning instructions. Identical to the prompt used in the [[f1-realistic-design]].

**Role in design:** The control condition for prompt variation. All other prompt versions are compared against this baseline.

### Prompt 2 — Chain-of-Thought (CoT) Instruction

Appends the following instruction to the standard prompt:

> "Before making your final supplier selection, think step by step through the relevant criteria. Show your reasoning explicitly before stating your decision."

**Motivation:** H8 predicts CoT reduces anchoring (explicit step-by-step reasoning may catch and correct the anchor) but may *not* reduce decoy effects (the comparison process itself may reinforce the decoy manipulation by explicitly surfacing the dominated option's relative quality). The contrast between H8's two directional predictions within a single design is a distinctive theoretical contribution.

**Caution:** CoT prompting may itself trigger demand effects if the reasoning trace reveals the manipulation. Post-collection analysis should check reasoning traces for manipulation-detection language ("I notice the anchor...", "This looks like a decoy...") and flag as a potential false-negative confound.

### Prompt 3 — Expert-Role Framing

Prepends the following system role instruction:

> "You are a senior procurement officer with 20 years of experience managing supplier relationships and optimizing procurement costs. Apply your professional expertise to evaluate the following scenario."

**Motivation:** Tests whether domain expertise framing shifts BSI — either attenuating bias via expert-role RLHF patterns, or amplifying it via satisficing heuristics that experienced professionals use. Prior literature (Echterhoff et al., 2024) does not test expert role framing; this is a novel contribution.

**Confound risk:** If models' training data contains "how experienced procurement officers think" content, role framing may activate training-data recall rather than genuine reasoning modification. This is the prompt-based analogue of the stochastic parroting concern from [[b3-04-aher-2023]].

---

## Additional Bias Type Specifications

### p2-06 — Default / Status Quo Bias

Based on [[b1-06-status-quo-bias-samuelson-zeckhauser-1988]]:
- **BASELINE:** Agent selects from 4 suppliers with no stated prior relationship (equal status)
- **STATUS_QUO:** SupplierAlpha is designated as the current contract holder (expiring in 30 days); the agent must actively switch to change the outcome
- **Human benchmark:** ~20–30 pp susceptibility for a 4-option set (Samuelson & Zeckhauser, 1988)
- **BSI scoring:** BSI = |P(select Alpha | STATUS_QUO) − P(select Alpha | BASELINE)|; economically optimal choice is pre-computed per scenario

### p2-07 — Loss Aversion Switching

Based on [[b1-07-loss-aversion-kahneman-tversky-1979]]:
- **GAIN_FRAME:** "By switching to SupplierBeta you will save $11,250 per quarter"
- **LOSS_FRAME:** "By staying with SupplierAlpha you will forgo $11,250 in quarterly savings"
- Underlying economics are identical (EV gap = $11,250/quarter); only the reference frame changes
- **Human benchmark:** Reflection effect ~70–80 pp preference reversal in Kahneman & Tversky (1979)
- **Caution:** p2-07 must be distinguished from p2-02 (framing); p2-02 tests attribute framing with a hard budget constraint; p2-07 tests risky choice framing under the reflection effect

### WARP Battery (p2-08)

Tests Weak Axiom of Revealed Preference (transitivity):
- **Trial 1:** Binary choice — SupplierA vs. SupplierB; agent chooses A
- **Trial 2:** Binary choice — SupplierB vs. SupplierC; agent chooses B
- **Trial 3:** Binary choice — SupplierA vs. SupplierC; if agent chooses C → WARP violation (A>B, B>C, but C>A)
- Each trial is a separate API call in a fresh session (between-session design prevents carry-over)
- BSI for WARP = P(transitivity violation) across 30 run-triplets
- **Interpretation:** WARP violations are unambiguous rationality failures — no theoretical alternative explanation unlike anchoring or framing

---

## Multi-Level Anchoring (p2-01b/c)

The Realistic Design uses a single high anchor ($91 vs. $75 baseline). The Flagship Design adds a low anchor and tests dose-response:

| Condition | Anchor Value | Direction | Predicted Effect |
|---|---|---|---|
| **p2-01-low-anchor** | $60 (20% below market) | Downward pull | Agent selects lower-cost suppliers than optimal |
| **p2-01-baseline** | $75 (market rate) | No anchor | Agent selects optimally |
| **p2-01-high-anchor** | $91 (21% above market) | Upward pull | Agent selects higher-cost suppliers than optimal |

**Identification:** If anchoring produces a dose-response curve (stronger anchor → larger BSI), this supports H4 and the "insufficient adjustment" mechanism from [[b1-01-anchoring-tversky-kahneman-1974]]. A flat response across anchor distances would instead suggest a binary "anchor detected / not detected" pattern rather than a continuous adjustment failure.

---

## Human Comparison Arm

### Design

- **Platform:** Prolific (preferred over MTurk for sample quality and reproducibility; consistent with replication-crisis response documented in [[b5-01-open-science-collaboration-2015]])
- **N target:** 100 subjects
- **Scenario exposure:** Same text-based procurement scenarios as LLMs; translated to standard survey format (forced choice between named suppliers with attribute table)
- **Incentive structure:** Prolific standard completion payment (~$1.50–$2.00 per 10-minute survey); no performance-contingent bonus (matches LLM incentive structure; see [[b2-01-incentivized-hypothetical-camerer-hogarth-1999]] — bias tasks are in the effort-inelastic category where incentives do not reliably eliminate bias)
- **Scenarios:** 5 core bias pairs (BASELINE vs. TREATMENT) × 2 = 10 scenario variants; each subject sees 1 scenario per bias type (between-subject across bias variants; within-subject across bias types)

### IRB Status

IRB submission must begin immediately upon green-light for the Flagship Design. IRB approval in procurement survey research typically takes 2–6 months (expedited review likely given minimal risk). All LLM data collection can proceed before IRB approval; human arm is the critical path for the flagship timeline.

### Analysis

- **Primary test:** Independent two-sample test per bias type: LLM_BSI distribution vs. Human_BSI distribution
- **Effect size:** Cohen's d for BSI difference between populations
- **Expected direction (H10):** LLM BSI < Human BSI for most bias types (RLHF attenuates natural cognitive shortcuts); exceptions possible for domain-specific biases where LLM training data has less procurement context
- **Calibration:** Human BSI baselines from [[b1-01-anchoring-tversky-kahneman-1974]] through [[b1-05-scarcity-cialdini-worchel-1975]] provide literature anchors; the Prolific sample provides BuyerBench-specific human baselines for the exact scenarios

---

## Full Factorial Cell Count

### LLM Arm

| Factor | Levels |
|---|---|
| Bias types | 8 (5 core + 3 new) |
| Variants | 2 (BASELINE, TREATMENT) |
| Models | 10 |
| Prompt versions | 3 |
| Temperatures | 4 (0.0, 0.3, 0.7, 1.0) |
| Runs per cell | 50 |

**Full factorial:** 8 × 2 × 10 × 3 × 4 × 50 = **96,000 runs**  
**Fractional factorial (recommended):** Stratified sample at 20,000 runs using a fractional factorial design preserving main effects and two-way interactions  
**Estimated LLM cost (full):** $14,400  
**Estimated LLM cost (fractional):** $3,000

### Human Arm

- 100 subjects × 10 scenarios = **1,000 observations**
- Estimated cost: ~$200 (Prolific completion payments + platform fee)

---

## Identification Logic

| Effect | Strategy | Comparison |
|---|---|---|
| **Bias effect** | Within-model paired comparison of BSI(variant) vs. BSI(baseline) | Held constant: model, prompt version, temperature |
| **Model effect** | Between-model comparison of BSI within bias type | Held constant: bias type, variant, prompt, temperature |
| **Prompt effect** | 3-level within-model comparison | Held constant: bias type, variant, model, temperature |
| **Temperature effect** | Variance decomposition across 4 temperature levels | Held constant: bias type, variant, model, prompt |
| **Human comparison** | Independent two-sample test per bias type | LLM_BSI(T=0.7, standard prompt) vs. Human_BSI |
| **Anchor dose-response** | Regression of BSI on continuous anchor distance | Within p2-01 scenario family; held constant: model, prompt, temperature |

---

## Engineering Requirements

| Requirement | Priority | Status |
|---|---|---|
| Prompt variant support in harness | Critical | Not yet implemented; required before Flagship run |
| Multi-temperature sweep automation | Critical | Requires `--temperature-sweep` flag in `buyerbench run` |
| WARP multi-turn session support | Critical | Requires new session orchestration for triplet-based WARP battery |
| Human survey platform integration | Required for human arm | Out of scope for Phase 1; manual CSV export acceptable |
| Fractional factorial design matrix | Recommended | Standard Python `pyDOE2` or R `AlgDesign` package |

---

## BibTeX Cross-Reference

Key citations unique to the Flagship Design (see also [[f1-realistic-design]] for shared citations):

- Kahneman & Tversky (1979) — loss aversion / reflection effect; [[b1-07-loss-aversion-kahneman-tversky-1979]]
- Samuelson & Zeckhauser (1988) — status quo bias design; [[b1-06-status-quo-bias-samuelson-zeckhauser-1988]]
- Thaler & Sunstein (2008) — default/nudge framing; [[b4-02-nudge-thaler-sunstein-2008]]
- Tversky & Simonson (1993) — WARP / IIA in multi-alternative choice
- Camerer & Hogarth (1999) — incentive-free human arm justification; [[b2-01-incentivized-hypothetical-camerer-hogarth-1999]]
- Echterhoff et al. (2024) — most relevant prior work to exceed; [[b3-06-echterhoff-2024]]
