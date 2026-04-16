---
type: research
title: "Section F.1 — Realistic Working Paper Design"
created: 2026-04-16
tags:
  - experimental-design
  - pillar2
  - llm-bias
  - behavioral-economics
  - working-paper
  - realistic-design
  - power-analysis
related:
  - '[[e6-design-comparison-matrix]]'
  - '[[d1-primary-research-question]]'
  - '[[d2-secondary-research-questions]]'
  - '[[g-econometric-strategy]]'
  - '[[f2-flagship-design]]'
  - '[[b2-03-within-between-subject-greenwald-1976]]'
  - '[[b5-02-simmons-nelson-simonsohn-2011]]'
  - '[[b5-03-loken-gelman-2017]]'
---

# Section F.1 — Realistic Working Paper Design

---

## Summary

This document formalizes the **Realistic Working Paper Design** for BuyerBench Pillar 2. It is the minimum viable experimental design capable of producing a publishable contribution at Tier 3–4 (JEBO / Experimental Economics / JBDM). All design decisions documented here were pre-registered before data collection.

**Target journal:** Experimental Economics or Journal of Economic Psychology  
**Claim level:** "We provide the first multi-model, stochasticity-aware measurement of behavioral bias susceptibility in LLM agents operating in economically structured procurement tasks."

---

## Scope

| Dimension | Specification | Rationale |
|---|---|---|
| **Bias types** | 5 (anchoring, framing, decoy, scarcity, sunk cost) | Covers all existing BuyerBench Pillar 2 scenarios (p2-01–p2-05); 5 distinct bias categories maps onto H1–H10 hypothesis set |
| **Models** | 10 (existing OpenRouter registry) | Sufficient for cross-model comparison; N=10 enables descriptive capability regression (H2) with appropriate hedging |
| **Runs per cell** | 30 | Achieves power ≈ 0.52 for d=0.4 (underpowered) and power ≈ 0.80 for d=0.6 (adequate); all results labeled "exploratory" per Loken & Gelman (2017) Type M analysis |
| **Temperature** | Fixed at 0.7 (primary); robustness at 0.0 and 1.0 | 0.7 is the de facto default for instruction-tuned models; secondary robustness sweeps test temperature sensitivity of results |
| **Design structure** | Between-subject | Each session sees either BASELINE or TREATMENT variant; never both in same context; prevents demand effects documented in [[b2-03-within-between-subject-greenwald-1976]] |
| **Prompt versions** | Standard only (no CoT variants) | Minimizes engineering complexity; CoT variants are reserved for [[f2-flagship-design]] |

---

## Statistical Summary

| Metric | Value |
|---|---|
| **Total LLM runs** | 5 bias × 2 variants × 10 models × 30 runs = **3,000 agent invocations** |
| **Estimated API cost** | $450 (at ~$0.15/run average across OpenRouter models) |
| **Estimated wall time** | 8–12 hours with parallelism |
| **Power at d=0.4** | ~0.52 — underpowered; label all results as exploratory |
| **Power at d=0.6** | ~0.80 — adequate; primary inference threshold for this design |
| **Target upgrade** | Increase to N=50/cell → power ≈ 0.70 at d=0.4; cost increases to $750 |

> **Design caveat:** The Realistic Design at N=30 is intentionally labeled exploratory for the d=0.4 target effect. Confidence intervals, not p-values, are the primary reporting format. Results significant at N=30 are interpreted cautiously pending N=50 replication. See [[g-econometric-strategy]] Section G.8 for full power analysis.

---

## Controls

### Session Independence

Each run is executed in a **fresh API session** with no prior conversation history. This eliminates cross-run learning confounds documented in [[b2-02-repeated-measurement-charness-levin-2005]] and ensures that within-cell variance across 30 runs reflects pure stochastic sampling from the model's distribution, not sequential updating. Technically enforced by BuyerBench harness: no `messages` history is passed between distinct run invocations.

### Prompt Randomization

Within each scenario prompt, **supplier ordering is randomized** across runs. This controls for positional bias (first-listed vs. last-listed option effects), ensuring that positional preference does not confound the bias manipulation. The BASELINE and TREATMENT variant structure is preserved across all orderings; only the list order of suppliers is shuffled.

Implementation: `harness/prompt.py` injects a randomized permutation of supplier blocks at scenario load time. Run metadata records the order permutation for post-hoc positional effect checks.

### Run Metadata Logging

Every run records:
- Timestamp (ISO 8601)
- Temperature setting
- Token count (prompt and completion)
- Model identifier string (pinned version)
- Run index within cell
- Supplier order permutation seed

This enables post-hoc session-order effect checks (is run #1 systematically different from run #30?) and guards against model version drift within a collection window.

---

## Primary Outputs

| Output | Type | Description |
|---|---|---|
| **BSI per cell** | Float [0, 1] | Bias Susceptibility Index computed per (model, bias_type, variant) triplet; see [[g-econometric-strategy]] G.1 for formal definition |
| **Choice correctness** | Binary {0, 1} | Whether the agent selected the economically optimal supplier on each run; ground-truth optimal is pre-computed per scenario |
| **Output text** | String | Full agent response for qualitative analysis; preserved for reasoning-trace secondary measure |
| **Run metadata** | Structured JSON | Timestamp, temperature, token count, model version, positional permutation seed |

---

## What This Design Allows

| Capability | Supported | Notes |
|---|---|---|
| Main effects of bias_type on BSI | ✅ Yes | One-way ANOVA or Kruskal-Wallis across 5 bias categories; BH-FDR corrected |
| Main effects of model on BSI | ✅ Yes | Between-model comparison; fixed effects; 10-model comparison |
| Inter-model variance decomposition | ✅ Yes | ANOVA-style SS partition: what fraction of total variance is model vs. bias type vs. residual? |
| Within-cell (stochastic) variance | ✅ Yes | N=30 per cell provides direct estimate of σ²_stoch(m,b); see H7 |
| Basic hypothesis tests for H1, H3, H5, H7, H9 | ✅ Yes | See [[d2-secondary-research-questions]] |
| H2 capability regression | ✅ Partial | N=10 models; treat as descriptive OLS only — no inference claims |

---

## What This Design Cannot Support

| Limitation | Reason | Design Upgrade Required |
|---|---|---|
| **Causal claims about why biases appear** | No mechanism manipulation; observed correlation only | Requires mechanism-targeted CoT variants (→ [[f2-flagship-design]]) |
| **Human comparison** | No human subjects arm | Requires IRB approval, Prolific study design (→ [[f2-flagship-design]]) |
| **Interaction effects (prompt × bias type)** | Single prompt version; no within-model prompt variation | Requires 3-prompt factorial design (→ [[f2-flagship-design]]) |
| **Generalizability beyond procurement** | Single domain | Requires multi-domain replication study (out of scope for this paper) |
| **Dose-response anchor claims** | Single anchor level for p2-01 | Requires p2-01b/c anchor magnitude variants (→ H4 in [[d1-primary-research-question]]) |
| **Temperature surface** | Only 3 temperature levels (0.0, 0.7, 1.0) | Requires 4-level sweep (→ [[f2-flagship-design]]) |

---

## Recommended Upgrade Path

If budget permits, upgrade to **N=50/cell** before data collection begins:
- Cost: $750 total (vs. $450 for N=30)
- Power gain: 0.52 → 0.70 at d=0.4
- Enables publication at Tier 2 (Experimental Economics) rather than Tier 3–4 (JEP / JBDM)
- N=50 remains within the "one weekend" execution window with parallelism

Upgrade N=50 is the **recommended minimum** for any working paper submission.

---

## BibTeX Cross-Reference

Key citations supporting design decisions in this document:

- Tversky & Kahneman (1974) — anchoring operationalization (p2-01); [[b1-01-anchoring-tversky-kahneman-1974]]
- Huber, Payne & Puto (1982) — decoy design (p2-03); [[b1-03-decoy-effect-huber-payne-puto-1982]]
- Greenwald (1976) — between-subject design rationale; [[b2-03-within-between-subject-greenwald-1976]]
- Loken & Gelman (2017) — Type M inflation for N=30; [[b5-03-loken-gelman-2017]]
- Simmons, Nelson & Simonsohn (2011) — pre-registration requirement; [[b5-02-simmons-nelson-simonsohn-2011]]
- Open Science Collaboration (2015) — N=30 minimum viable power analysis; [[b5-01-open-science-collaboration-2015]]
