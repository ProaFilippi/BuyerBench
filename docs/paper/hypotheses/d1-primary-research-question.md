---
type: research
title: "Section D.1 — Primary Research Question: Formal Operationalization"
created: 2026-04-16
tags:
  - hypotheses
  - prq
  - pillar2
  - bsi
  - llm-bias
  - behavioral-economics
  - operationalization
related:
  - '[[c-research-gap]]'
  - '[[b6-synthesis]]'
  - '[[b5-03-loken-gelman-2017]]'
  - '[[b5-01-open-science-collaboration-2015]]'
  - '[[b3-06-echterhoff-2024]]'
  - '[[b3-03-hagendorff-2023]]'
  - '[[strategy-decision-tree]]'
---

# Section D.1 — Primary Research Question (Formal Operationalization)

---

## The PRQ

> "Does the behavioral bias susceptibility of LLM-based agents — measured as deviation from economically optimal choices under controlled presentation manipulations — vary systematically across model capability tiers, bias types, and experimental conditions, in ways analogous to, attenuated relative to, or amplified compared to documented human behavioral patterns?"

---

## Why Formal Operationalization is Required

A well-formed empirical PRQ must be falsifiable. The above sentence contains five embedded empirical claims and three alternative outcome frames. Without decomposing it into measurable sub-questions, the PRQ admits an infinite variety of confirmatory interpretations ("it varies because X" or "it's attenuated because Y") regardless of what the data show. The operationalization below pins each clause to a specific dependent variable, independent variable, and expected result — converting the prose statement into a testable research program.

---

## Dimensional Decomposition

The PRQ contains five independently testable dimensions:

### Dimension 1 — Existence: Does bias susceptibility occur at all?

**Empirical question:** Do LLM agents deviate from economically optimal choices under controlled presentation manipulations with greater frequency than under baseline?

**Operationalization:** BSI = |P(optimal | MANIPULATION) − P(optimal | BASELINE)|, estimated from N ≥ 30 runs per (model × bias type × variant) cell. A non-trivial BSI (> 0.10 with 95% CI excluding zero) is the minimum threshold for claiming bias susceptibility exists.

**Null framing:** If BSI ≈ 0.0 across all 10 models and all 5 bias types at N = 30, the paper's contribution inverts: "LLMs in structured procurement tasks are surprisingly robust to canonical behavioral bias manipulations." This is a scientifically valid finding, not a failure.

**Primary hypothesis:** H1 (Bias Universality). Hypothesis H7 (variance proportional to susceptibility) provides a complementary existence test via the within-cell variance signature.

**Human benchmark:** See b1-01 through b1-05. Minimum expected human BSI range: 0.20–0.70 across the five bias types in the battery.

---

### Dimension 2 — Variation Across Bias Types: Are some biases more powerful than others?

**Empirical question:** Is the mean BSI statistically different across bias types (anchoring, framing, decoy, scarcity, sunk cost)?

**Operationalization:** One-way ANOVA (or Kruskal-Wallis if normality violated) on BSI estimates across 5 bias type categories, with Bonferroni or BH-FDR correction for 10 pairwise comparisons.

**Expected pattern:** Decoy effects (H3) and scarcity cues (b1-05) are expected to show higher BSI than sunk cost (b1-04) and framing (b1-02) based on the prompt-constraint design of existing scenarios. Anchoring (H4) is indeterminate because only one anchor magnitude level currently exists.

**Primary hypotheses:** H1 (overall variation across types), H3 (decoy as most reliable), H5 (framing asymmetry).

---

### Dimension 3 — Variation Across Model Capability Tiers: Do better models show less bias?

**Empirical question:** Is there a negative relationship between model capability (proxied by Pillar 1 score or parameter count) and mean BSI across bias types?

**Operationalization:** Spearman rank correlation between Pillar 1 composite score and mean_BSI across models. OLS regression with capability proxy as IV and mean_BSI as DV, flagged as descriptive (N = 10 models is below inference threshold for regression).

**Caution:** Hagendorff et al. (2023) find the *opposite* pattern — higher-capability GPT-4 shows more System 1 errors than GPT-3 on cognitive tasks. BuyerBench's structured procurement domain may exhibit a different capability-bias relationship because explicit rubrics and constraints suppress System 1 activation regardless of capability tier. Both outcomes are theoretically motivated and must be framed accordingly.

**Primary hypothesis:** H2 (Capability-Bias Tradeoff). H6 (Sunk Cost × Capability interaction) provides a non-monotone counterexample that enriches the capability story.

---

### Dimension 4 — Variation Across Experimental Conditions: Do prompt design choices modulate bias?

**Empirical question:** Does chain-of-thought (CoT) prompting, temperature setting, or task complexity alter BSI?

**Operationalization:**
- *Temperature ablation:* Run each scenario at T ∈ {0.0, 0.3, 0.7, 1.0}; measure BSI and within-cell variance. Stochastic variance is expected to increase monotonically with T; BSI may not.
- *CoT manipulation:* Run standard vs. chain-of-thought prompt variants; compare BSI per bias type (see H8).
- *Task complexity:* If a simplified scenario variant exists, compare BSI with baseline.

**Primary hypothesis:** H8 (CoT reduces anchoring but not decoy). H7 (stochastic variance proportional to BSI) is the mechanism-level prediction underlying the temperature ablation.

---

### Dimension 5 — Calibration Against Human Benchmarks: Are LLMs more or less biased than humans?

**Empirical question:** Are the BuyerBench estimated Cohen's d effect sizes (BSI vs. 0) larger or smaller than the meta-analytic human benchmarks for the same bias categories?

**Operationalization:** For each bias type, compute Cohen's d from the BuyerBench multi-run distribution. Compare to human meta-analytic estimates from b1-01 (anchoring: r ≈ 0.80 → d ≈ 2.7), b1-02 (framing: ~60 pp reversal in risky choice → d ≈ 1.8), b1-03 (decoy: ~15 pp share increase → d ≈ 0.4), b1-04 (sunk cost: ~54% susceptibility → d ≈ 0.85), b1-05 (scarcity: d ≈ 0.60–0.80).

**Identification caveat:** This comparison requires a human comparison arm (Design Option 5) or explicit citation of the human meta-analytic baselines as external benchmarks. The latter is feasible from existing literature; the former requires IRB and recruiting budget.

**Primary hypothesis:** H10 (Human Benchmark Calibration). Near-zero BuyerBench BSI across all models at N = 30 would imply LLM effect sizes are far smaller than human baselines for the structured procurement domain — a defensible "domain structure suppresses bias" finding.

---

## Outcome Frame Decision Tree

The PRQ specifies three possible outcome directions. The following decision tree formalizes the framing choice before data collection:

```
                  ┌─────────────────────────────────────────┐
                  │  Are BSI estimates significantly > 0     │
                  │  for ≥ 2 bias types across ≥ 5 models?  │
                  └─────────────────┬───────────────────────┘
                                    │
               YES ─────────────────┴───────────────── NO
                │                                        │
   ┌────────────▼────────────┐              ┌────────────▼────────────┐
   │ Are LLM effect sizes    │              │ N=30 CI excludes d>0.2? │
   │ LARGER than human       │              └────────────┬────────────┘
   │ meta-analytic d?        │                           │
   └────────────┬────────────┘                YES ───────┴───── NO
                │                               │               │
        YES ────┴──── NO              ┌─────────▼───┐   ┌──────▼──────────┐
         │             │              │ "Surprisingly│   │ Power failure:  │
   "Amplified"  "Analogous or         │ robust" paper│   │ run N=50 or     │
   frame (rare, │ attenuated"         └─────────────-┘   │ expand battery  │
   unexpected)  │ framing (primary                       └─────────────────┘
                │ expected outcome)
   ```

---

## Hypothesis Coverage Map

The table below shows which of D.3's ten hypotheses addresses each PRQ dimension.

| PRQ Dimension | Primary Hypotheses | Secondary Hypotheses |
|---|---|---|
| D1: Existence | H1 (Bias Universality) | H7 (variance signature) |
| D2: Across bias types | H3 (Decoy), H5 (Framing), H6 (Sunk Cost × Capability) | H1, H4 (Anchoring magnitude) |
| D3: Across capability tiers | H2 (Capability-Bias Tradeoff) | H6 (non-monotone interaction) |
| D4: Across experimental conditions | H8 (CoT × bias type) | H7 (temperature × variance) |
| D5: Human calibration | H10 (Human Benchmark Calibration) | H9 (model-specific profiles) |

**Coverage gap:** H9 (bias profiles are model-specific, not universal) addresses a secondary SRQ (SRQ5) but has no direct mapping to the PRQ dimensions above. It enriches the cross-model analysis (D3) but is more of a descriptive characterization than a test of the PRQ.

---

## Identification Requirements Summary

| Requirement | Current Status | Action Needed |
|---|---|---|
| N ≥ 30 per (model × bias type × variant) cell | Not yet run at N=30 | Design Option 1 (baseline design) required |
| 5 bias types in battery | ✅ p2-01 through p2-05 | None for MVP |
| 10 models in comparison set | ✅ OpenRouter battery defined | Execute run |
| Multiple anchor magnitudes for H4 | ❌ Only one anchor level (HIGH) | New scenario variant: p2-01b with LOW anchor |
| CoT prompt variants for H8 | ❌ Not yet designed | New prompt variants required for D4 flagship design |
| Human benchmark table for H10 | ✅ Available from B1 series | Compile from b1-01 through b1-05 literature notes |
| IRB approval for human arm | ❌ Not started | Begin parallel IRB submission (6–24 month horizon) |
| BH-FDR pre-registration | ❌ Not formalized | Pre-register bias types, model set, BSI threshold |

---

## Pre-Registration Template

To satisfy OSC (2015) and Simmons et al. (2011) standards, the following must be locked before data collection:

1. **Bias types tested:** anchoring, framing, decoy, scarcity, sunk cost (5 types; no post-hoc additions)
2. **Model set:** the 10 OpenRouter models defined in CLAUDE.md (no post-hoc model additions)
3. **BSI threshold for "significant":** d ≥ 0.20, two-sided, α = .05 with BH-FDR correction at q = .05 across 50 primary tests (10 models × 5 bias types)
4. **Primary outcome:** BSI per (model × bias type) cell, estimated from N = 30 independent runs
5. **Secondary outcomes:** within-cell variance, reasoning trace length, option-selection distribution
6. **Outcome frame decision:** pre-specify that null result (BSI ≈ 0 across all cells at N=30) will be reported as "domain structure suppresses bias susceptibility" — not as a failed study

---

## Paper Framing Guidance

**Introduction:** Open with the PRQ as stated, then immediately situate it against the three possible outcome frames. State which frame the data most support. Do not write the introduction before the data are collected.

**Section 3 (Hypotheses):** Cite this document's dimensional decomposition. Present H1–H10 as organized tests of the five PRQ dimensions, not as a flat list. This shows reviewers the hierarchical structure of the research design.

**Limitations:** Explicitly acknowledge that D4 (experimental conditions) is only partially addressed in the MVP design — CoT variants and temperature ablation above T=0.7 require the flagship design (Design Option 3). Flag H4 (anchoring magnitude) as a limitation until p2-01b is run.

**Discussion:** The human calibration frame (D5, H10) should anchor the discussion. Whatever BuyerBench finds, the comparison to human baselines is the primary theoretical contribution — it places LLM behavior on the same scale as seventy years of human behavioral economics data.

---

## BibTeX Quick Reference

```bibtex
@article{kahneman1979prospect,
  author  = {Kahneman, Daniel and Tversky, Amos},
  title   = {Prospect Theory: An Analysis of Decision under Risk},
  journal = {Econometrica},
  year    = {1979},
  volume  = {47},
  number  = {2},
  pages   = {263--291}
}

@article{hagendorff2023human,
  author  = {Hagendorff, Thilo and Fabi, Sarah and Kosinski, Michal},
  title   = {Human-like intuitive behavior and reasoning biases emerged in large language models},
  journal = {Nature Human Behaviour},
  year    = {2023},
  volume  = {7},
  pages   = {1mouse768--1780}
}

@article{echterhoff2024cognitive,
  author  = {Echterhoff, Jessica M. and Liu, Yao and Alessa, Abeer and McAuley, Julian and He, Zexue},
  title   = {Cognitive Bias in High-Stakes Decision-Making with {LLMs}},
  journal = {arXiv preprint arXiv:2403.00811},
  year    = {2024}
}

@article{loken2017measurement,
  author  = {Loken, Eric and Gelman, Andrew},
  title   = {Measurement error and the replication crisis},
  journal = {Science},
  year    = {2017},
  volume  = {355},
  number  = {6325},
  pages   = {584--585}
}

@article{opensciencecollaboration2015,
  author  = {{Open Science Collaboration}},
  title   = {Estimating the reproducibility of psychological science},
  journal = {Science},
  year    = {2015},
  volume  = {349},
  number  = {6251},
  pages   = {aac4716}
}
```
