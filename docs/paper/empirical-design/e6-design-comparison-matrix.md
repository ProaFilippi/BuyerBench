---
type: analysis
title: "Section E.6 — Empirical Design Comparison Matrix"
created: 2026-04-16
tags:
  - empirical-design
  - research-design
  - pillar2
  - llm-bias
  - behavioral-economics
  - power-analysis
  - comparison-matrix
related:
  - '[[d1-primary-research-question]]'
  - '[[d2-secondary-research-questions]]'
  - '[[c-research-gap]]'
  - '[[b5-02-simmons-nelson-simonsohn-2011]]'
  - '[[b3-03-hagendorff-2023]]'
  - '[[b3-04-aher-2023]]'
---

# Section E.6 — Empirical Design Comparison Matrix

---

## Overview

This document formalizes the tradeoff comparison across the five candidate empirical designs introduced in Sections E.1–E.5. The comparison is structured as a pre-data-collection decision tool: by committing to an explicit multi-dimensional evaluation before running any experiment, we guard against post-hoc rationalization toward whichever design produced the most favorable results.

**Scoring conventions:**

- **Identification Strength (1–5):** How well does the design isolate the causal/associational claim? Higher = more defensible causal story, better control for confounds.
- **Statistical Power (1–5):** Expected power at minimum feasible sample size. Higher = more likely to detect true effects at α=.05, d=0.5 (medium effect); penalized for structural limits (e.g., small N of models).
- **Engineering Cost (1–5):** Implementation burden, where **lower score = cheaper/faster to build**. Scores 1–2 = reuse existing harness; 3 = moderate new work; 4–5 = significant new infrastructure.
- **Time to Execute:** Wall-clock time from green-light to publishable data, including design, data collection, and analysis.
- **Publication Tier Enabled:** Tier classification from the BuyerBench journal strategy (1 = top-field flagship; 4 = working paper).
- **Key Risk:** The single most threatening failure mode.

---

## Design Comparison Matrix

| Dimension | E.1 Bias Battery (Baseline) | E.2 Economic Games | E.3 Multi-Factor Factorial | E.4 WARP / Preference Consistency | E.5 Human Comparison Arm |
|---|---|---|---|---|---|
| **Identification Strength** | 3 / 5 | 3 / 5 | 5 / 5 | 5 / 5 | 5 / 5 |
| **Statistical Power** | 3 / 5 | 3 / 5 | 5 / 5 | 3 / 5 | 4 / 5 |
| **Engineering Cost** | 1 / 5 | 3 / 5 | 4 / 5 | 3 / 5 | 5 / 5 |
| **Time to Execute** | 1–2 weeks | 3–4 weeks | 4–6 weeks | 2–4 weeks | 3–8 months |
| **Publication Tier Enabled** | 3–4 | 3–4 | 1–2 | 2–3 | 1 |
| **Key Risk** | Single domain; no human baseline | Incentive incompatibility + prior-art saturation | Prompt variant engineering complexity | Prompt-order confounds require high N | IRB delay (2–6 months) |

---

## Dimension-by-Dimension Analysis

### Identification Strength

| Design | Score | Rationale |
|---|---|---|
| E.1 Bias Battery | 3 | Good internal validity via controlled within-agent variant comparison. Weak external validity: single procurement domain; no cross-context replication. |
| E.2 Economic Games | 3 | High theoretical grounding (SPNE, Nash) provides sharp predictions. Penalized because incentive incompatibility is a *fundamental* threat: LLMs face no real consequences, so observed behavior may not reflect genuine preference structure. |
| E.3 Multi-Factor Factorial | 5 | Full 2^k factorial allows decomposition of main effects and all interactions (model × bias type × prompt × temperature × task complexity). Variance partitioning answer: "How much of BSI is model vs. bias type vs. prompt?" |
| E.4 WARP Battery | 5 | WARP is a core rationality axiom with minimal theoretical assumptions. A violation is logically definitive: the agent is not consistent. High falsifiability with no auxiliary assumptions. |
| E.5 Human Arm | 5 | Strongest design. Direct between-group comparison of BSI distributions (LLM vs. human) answers the PRQ's "analogous / attenuated / amplified" trichotomy with behavioral evidence rather than speculation. |

**Takeaway:** E.2's theoretical appeal is offset by the incentive incompatibility problem. E.1 is the weakest identificationally but is the only option executable immediately.

---

### Statistical Power

| Design | Score | Rationale |
|---|---|---|
| E.1 Bias Battery | 3 | At N=30 runs/cell: power ≈ 0.80 for d=0.5. Adequate for main effects. Underpowered for interaction terms (requires N≥50/cell). H2 (capability regression) has N=10 models — dangerously small regardless of per-cell N. |
| E.2 Economic Games | 3 | Shared power limitation with E.1 at model level. The LLM-as-player validity concern means even high power does not guarantee interpretable results. |
| E.3 Multi-Factor Factorial | 5 | N=3,000 total runs (5 bias × 3 prompt × 10 models × 10 temps × 2 complexity). Well-powered for main effects (d≈0.3), interaction terms (d≈0.5), and variance decomposition. At $0.15/run → $450. |
| E.4 WARP Battery | 3 | Between-session 3-alternative design requires very high per-model N (≥50 runs × 3 pairwise pairs) to detect transitivity violations reliably. Within-session designs are confounded by context order. |
| E.5 Human Arm | 4 | 100 human subjects × 10 scenarios = 1,000 observations; power ≈ 0.80 for d=0.50. Adequate for main LLM-vs.-human comparison. Penalized by variance in human responses (procurement domain unfamiliarity for MTurk workers). |

**Takeaway:** E.3 dominates on power. E.1 is the minimum viable threshold (80% for medium effects). E.4's clean theory does not rescue its power limitations.

---

### Engineering Cost

| Design | Score | Rationale |
|---|---|---|
| E.1 Bias Battery | 1 | Fully executable with existing BuyerBench harness + 5 existing scenario pairs. Zero new engineering beyond running more iterations. |
| E.2 Economic Games | 3 | Requires a multi-round conversation harness (stateful sessions, running payoff tracking, game tree management). Not in current architecture. ~2–3 weeks of harness work. |
| E.3 Multi-Factor Factorial | 4 | Requires: (a) CoT prompt variants per scenario, (b) prompt versioning infrastructure in harness, (c) temperature sweep configuration, (d) task complexity variants. Substantial but tractable. ~3–4 weeks of engineering. |
| E.4 WARP Battery | 3 | Requires new 3-supplier comparison scenarios (currently only 2-option layouts) and a between-session run controller. Scenario design is the primary bottleneck. ~2 weeks. |
| E.5 Human Arm | 5 | IRB application (1–3 weeks prep, 2–6 months approval). Prolific/MTurk survey instrument design. Attention check + comprehension questions. Payment processing. Pilot run. ~$500–$600 in participant payments. |

**Takeaway:** E.1 is uniquely low-cost. E.5's cost is dominated by IRB timeline (non-engineering), not financial cost. E.3's engineering cost is the major barrier to the flagship design.

---

### Time to Execute

| Design | Estimate | Critical Path |
|---|---|---|
| E.1 Bias Battery | **1–2 weeks** | Configure N=30 runs per cell; execute via OpenRouter; generate report. |
| E.2 Economic Games | **3–4 weeks** | Multi-round harness engineering → scenario design → data collection. |
| E.3 Multi-Factor Factorial | **4–6 weeks** (after baseline) | Prompt variant design → harness extension → full 3,000-run sweep. Can be parallelized with E.1. |
| E.4 WARP Battery | **2–4 weeks** | New scenario variants → between-session run protocol → analysis. |
| E.5 Human Arm | **3–8 months** | IRB submission and approval dominates all other phases. Data collection is fast once approved. |

**Takeaway:** E.5's IRB dependency means it must be submitted in parallel with all other work. A 6-month wait before data collection makes E.5 a separate track, not a blocker.

---

### Publication Tier Enabled

| Design | Tier | Justification |
|---|---|---|
| E.1 Bias Battery | **3–4** | Sufficient for a well-powered, multiplicity-corrected empirical note in a field journal (e.g., *JAAMAS*, *ICAIF*, *Decision*). Not sufficient for top-tier without human comparison. |
| E.2 Economic Games | **3–4** | Prior work (Aher et al. 2023) covers the core economic games angle. A procurement-domain replication with new models may reach Tier 3 as a replication + extension. |
| E.3 Multi-Factor Factorial | **1–2** | Full factorial with variance decomposition + interaction analysis unlocks top-field venues (*Management Science*, *JBF*, *JMLR*, *NeurIPS*). The "model × bias type × prompt" interaction story is novel. |
| E.4 WARP Battery | **2–3** | WARP violation documentation is publishable in behavioral economics or AI venues. Strong as a section within a flagship paper; weaker as a standalone. |
| E.5 Human Arm | **1** | Human-LLM behavioral comparison is the gold standard for top-tier venues. Enables direct contribution to the behavioral economics literature, not just AI benchmarking. |

**Takeaway:** E.3 + E.5 together constitute the Tier 1 flagship. E.1 alone is the minimum publishable unit. E.4 elevates any paper that includes it as a section.

---

### Key Risks

| Design | Key Risk | Mitigation |
|---|---|---|
| E.1 Bias Battery | All models show BSI=0 (null result) → "LLMs are surprisingly robust" reframing required | Pre-specify null framing in pre-registration; pilot at N=5 per model before committing to N=30 |
| E.2 Economic Games | Incentive incompatibility renders results uninterpretable; reviewers may reject as invalid behavioral test | Frame as "preference elicitation" not "behavioral economics"; lean on Aher (2023) precedent; position as supplementary |
| E.3 Multi-Factor Factorial | Prompt variant engineering is harder than expected; harness brittleness at scale (3,000 runs) | Modular prompt templating; dry-run 100 runs before committing; checkpoint + resume support in harness |
| E.4 WARP Battery | Prompt-order effects within session confound transitivity violations; between-session design requires high N | Between-session design mandatory; randomize presentation order; pre-specify order controls |
| E.5 Human Arm | IRB delay (2–6 months); MTurk workers unfamiliar with procurement domain → noisy responses | Submit IRB in parallel with E.1 execution; use domain-simplified framing in survey instrument; include comprehension checks |

---

## Recommended Sequencing

Based on the matrix, the recommended execution order is:

```
Phase 1 (Weeks 1–2):   Execute E.1 Bias Battery at N=30/cell
                        → Establishes baseline BSI estimates for all 10 models
                        → Minimum publishable unit
                        → Validates harness for scale-up

Phase 2 (Weeks 2–4):   Add E.4 WARP Battery as a Section of the same paper
                        → New scenario variants required (low cost)
                        → Elevates paper to Tier 2–3 as standalone

Phase 3 (Weeks 3–7):   Build and execute E.3 Multi-Factor Factorial
                        → Requires E.1 data to inform prompt variant selection
                        → Flagship design; unlocks Tier 1–2

Parallel Track:         Submit IRB for E.5 Human Arm immediately
                        → Submit while Phases 1–3 are running
                        → Target Prolific data collection to coincide with E.3 completion
                        → Combine E.3 + E.5 into Tier 1 flagship paper
```

**Do NOT build E.2 (Economic Games) as a primary design.** Include one Ultimatum Game scenario as a supplementary probe to the E.3 factorial if prior work comparability is desired.

---

## Design Decision: Pre-Registered Commitment

> **Pre-registered decision (2026-04-16):**
>
> - **Primary design:** E.1 (Bias Battery, N=30/cell) with E.4 (WARP Battery) as Section 2.
> - **Flagship design:** E.3 (Multi-Factor Factorial) as Phase 3 upgrade after baseline validation.
> - **Gold standard arm:** E.5 (Human Comparison) submitted to IRB in parallel.
> - **Secondary/supplementary only:** E.2 (Economic Games).
>
> This decision is locked prior to any data collection. Post-hoc design changes require explicit documentation of the deviation and motivation.

---

## Risk Heatmap Summary

| Design | Identification | Power | Cost | Speed | Tier | Overall Recommendation |
|---|---|---|---|---|---|---|
| E.1 Bias Battery | ★★★☆☆ | ★★★☆☆ | ★★★★★ | ★★★★★ | 3–4 | **START HERE — minimum viable** |
| E.2 Economic Games | ★★★☆☆ | ★★★☆☆ | ★★★☆☆ | ★★★☆☆ | 3–4 | **Supplementary only** |
| E.3 Multi-Factor Factorial | ★★★★★ | ★★★★★ | ★★☆☆☆ | ★★☆☆☆ | 1–2 | **Phase 3 flagship — high ROI** |
| E.4 WARP Battery | ★★★★★ | ★★★☆☆ | ★★★☆☆ | ★★★★☆ | 2–3 | **Phase 2 section — easy win** |
| E.5 Human Arm | ★★★★★ | ★★★★☆ | ★☆☆☆☆ | ★☆☆☆☆ | 1 | **Parallel track — submit IRB now** |

*Note: Engineering cost stars represent affordability (5 stars = very affordable; 1 star = expensive/slow to build).*
