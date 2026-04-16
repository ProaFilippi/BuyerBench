---
type: research
title: "Section D.2 — Secondary Research Questions: Operationalization"
created: 2026-04-16
tags:
  - hypotheses
  - srq
  - pillar2
  - bsi
  - llm-bias
  - behavioral-economics
  - operationalization
  - statistical-design
related:
  - '[[d1-primary-research-question]]'
  - '[[c-research-gap]]'
  - '[[b6-synthesis]]'
  - '[[b5-02-simmons-nelson-simonsohn-2011]]'
  - '[[b5-03-loken-gelman-2017]]'
  - '[[b3-03-hagendorff-2023]]'
  - '[[b3-04-aher-2023]]'
  - '[[b1-01-anchoring-tversky-kahneman-1974]]'
  - '[[b1-02-framing-tversky-kahneman-1981]]'
  - '[[b1-03-decoy-effect-huber-payne-puto-1982]]'
  - '[[b1-04-sunk-cost-arkes-blumer-1985]]'
  - '[[b1-05-scarcity-cialdini-worchel-1975]]'
---

# Section D.2 — Secondary Research Questions (Operationalization)

---

## Overview

Five secondary research questions (SRQs) decompose the primary research question (PRQ) into independently answerable sub-problems. Each SRQ maps to one or more of the D.3 hypotheses (H1–H10) and defines the specific variables, statistical tests, and data requirements needed to answer it. The SRQs are secondary in the sense that they have narrower scope than the PRQ, but each is independently publishable as a result in a findings table and provides the evidentiary building blocks for the integrated PRQ answer.

**Relationship to PRQ dimensions:**

| SRQ | PRQ Dimension | Primary Hypotheses | Status |
|---|---|---|---|
| SRQ1 | D2: Variation across bias types | H1, H3, H5 | Requires N≥30 per cell |
| SRQ2 | D3: Variation across capability tiers | H2, H6 | Requires full 10-model run |
| SRQ3 | D4: Stochastic vs. systematic variance | H7 | Requires repeated runs at multiple T |
| SRQ4 | D4: Experimental condition moderation | H8 | Requires CoT prompt variants |
| SRQ5 | D3: Model-specific bias profiles | H9 | Requires full bias battery across all models |

---

## SRQ1 — Which bias types produce statistically significant susceptibility?

> **Question:** Which of the 5 tested bias types (anchoring, framing, decoy, scarcity, sunk cost) produce statistically significant bias susceptibility in LLM agents across repeated trials?

### Operationalization

**Unit of observation:** (model, bias_type, run)

**Dependent variable:** `BSI` (Bias Susceptibility Index): proportion of runs in the variant condition where the agent chose the non-optimal option relative to the baseline condition.

```
BSI = P(non-optimal | VARIANT) − P(non-optimal | BASELINE)
```

Estimated at the cell level (model × bias_type) from N ≥ 30 independent runs per variant.

**Independent variable:** `bias_type` (5-category factor: anchoring, framing, decoy, scarcity, sunk cost)

**Statistical test:**
1. Per-bias-type test: One-sample t-test (or Wilcoxon signed-rank if normality violated) testing H₀: BSI = 0 for each bias type, aggregated across models. Apply BH-FDR correction across 5 tests (α = .05, q = .05).
2. Cross-bias-type test: One-way ANOVA (or Kruskal-Wallis) on cell-level BSI estimates across the 5 bias categories. This tests whether bias types differ in magnitude.
3. Post-hoc pairwise: Tukey HSD or Dunn test for significant ANOVA/Kruskal results.

**Expected pattern (directional priors):**
- Decoy: BSI > 0 (b1-03, Huber et al. 1982; one model already failed in pilot data)
- Scarcity: BSI > 0 (b1-05, Cialdini and Worchel 1975; supply shortage framing)
- Anchoring: Indeterminate — current scenarios have only one anchor magnitude level (HIGH). H4 flags this as a design limitation.
- Framing: BSI > 0 but small; structured procurement rubrics partially suppress framing effects
- Sunk cost: Non-monotonic by capability tier (see SRQ2); aggregate BSI may obscure this

**Null outcome pre-specification:** If BH-FDR-corrected tests fail to reject H₀: BSI = 0 for ≥ 3 bias types at N = 30, the finding is "domain structure suppresses bias susceptibility across most bias categories" — a valid contribution, not a failed study.

**Data requirements:**
- 5 bias type batteries, each with 1 baseline + 1 variant condition (p2-01 through p2-05)
- N = 30 runs per (model × variant) cell
- 10 models × 2 variants × 30 runs = 600 total runs per bias type; 3,000 total

**Scenario mapping:**
| Bias Type | Scenario ID | Baseline | Variant |
|---|---|---|---|
| Anchoring | p2-01 | No anchor price | HIGH anchor ($X above market) |
| Framing | p2-02 | GAIN frame | LOSS frame |
| Decoy | p2-03 | 2 suppliers | 3 suppliers (asymmetrically dominated decoy) |
| Scarcity | p2-04 | Normal availability | Scarcity cue ("only 2 units remain") |
| Sunk Cost | p2-05 | No prior spend mentioned | Prior spend mentioned ("$50K already invested") |

**Limitations:**
- Single domain (procurement supplier selection) limits external validity. The identified bias effects may be domain-specific.
- Anchoring requires a new scenario variant (p2-01b: LOW anchor) to test H4 (magnitude proportionality). Until then, SRQ1 can only test whether HIGH anchoring exists, not whether anchoring effects scale with magnitude.

---

## SRQ2 — Does model capability predict lower bias susceptibility?

> **Question:** Does model capability (as proxied by Pillar 1 scores or model parameter count) predict lower bias susceptibility?

### Operationalization

**Unit of observation:** model (N = 10)

**Dependent variable:** `mean_BSI` — model-level average of BSI estimates aggregated across all 5 bias types and all runs.

**Independent variables:**
- Primary: `pillar1_score` — Pillar 1 composite score (agent capability: supplier discovery, quote comparison, workflow execution). This is an internal BuyerBench measure.
- Secondary: `log_parameter_count` — log of reported parameter count (from model documentation). Used as an external capability proxy when Pillar 1 scores are unavailable or to triangulate findings.

**Statistical tests:**
1. Spearman rank correlation between `pillar1_score` and `mean_BSI` (non-parametric; robust for N = 10 models)
2. OLS regression: `mean_BSI ~ β₀ + β₁·pillar1_score + ε` — **flagged as descriptive only** (N = 10 is below inference threshold for OLS; CIs will be wide and estimates unreliable)
3. Sensitivity analysis: Re-run correlation with `log_parameter_count` as IV; compare direction and magnitude

**Expected direction:** Negative (higher capability → lower BSI). Rationale: more capable models have more robust world-models, are better calibrated to ignore irrelevant framing cues, and are more likely to follow explicit optimization rubrics.

**Competing prediction (from Hagendorff et al. 2023):** Positive or non-monotonic — higher-capability models show *more* System 1-like errors in some cognitive tasks because they generate more fluent, "human-like" reasoning that is susceptible to the same heuristics as human cognition. The structured procurement domain may suppress this mechanism, but it must be considered.

**Non-monotone prediction for sunk cost (H6):** High-capability models may show *more* sunk cost susceptibility than low-capability models because they can reason explicitly about prior investments, engaging a richer narrative that amplifies the sunk cost framing. The SRQ2 aggregate correlation may obscure this interaction; disaggregate by bias type.

**Statistical caution:** N = 10 models severely limits regression inference. Any results must be labeled "suggestive patterns (N = 10; descriptive only)" and not interpreted causally. The companion hypothesis H9 (model-specific bias profiles) and the disaggregated bias-type correlation matrix provide more reliable evidence than a single aggregate regression.

**Data requirements:**
- Pillar 1 benchmark results for all 10 models (requires Pillar 1 full run)
- BSI estimates at N = 30 per (model × bias type × variant) cell
- Model parameter counts from documentation for the 10 OpenRouter models

---

## SRQ3 — How much variance is stochastic vs. systematic?

> **Question:** How much of observed output variance is attributable to stochastic sampling vs. systematic bias?

### Operationalization

**Unit of observation:** (model, bias_type) cell

**Dependent variables:**
- `within_cell_variance` — variance of BSI estimates across repeated runs within a (model × bias_type × variant) cell, holding all inputs constant. This is the stochastic component.
- `between_condition_BSI` — the mean difference in BSI between baseline and variant conditions. This is the systematic component.

**Decomposition approach:** Variance decomposition (analogous to ANOVA):
```
Total variance = Stochastic variance (within cell, T>0) + Systematic variance (between conditions) + Residual
```

**Statistical tests:**
1. Levene test for equality of variance across baseline vs. variant conditions (tests whether variant conditions are more variable, not just shifted)
2. Intraclass correlation coefficient (ICC) — proportion of total BSI variance explained by the bias manipulation (condition), vs. model identity, vs. residual stochastic noise
3. Temperature ablation: Run each scenario at T ∈ {0.0, 0.3, 0.7, 1.0} across a subset of models (3+ models). Fit `within_cell_variance ~ f(temperature)` to characterize how much of the variance is temperature-induced.

**H7 as mechanism:** Hypothesis H7 predicts that stochastic variance is *proportional* to BSI magnitude — i.e., boundary-state responses (those near the 50/50 choice threshold) are both more biased and more variable. Test this with a variance-mean regression: `within_cell_variance ~ β₀ + β₁·mean_BSI + ε`. A significant positive β₁ supports the H7 mechanism and validates BSI as a noisy-but-unbiased estimator of systematic bias.

**Key implication for paper design:** If most variance is stochastic (within-cell > between-condition), then observed BSI estimates at N = 30 may be dominated by noise. Increase N or report wide CIs explicitly. Conversely, if most variance is systematic (between-condition >> within-cell), N = 30 is sufficient and the bias effects are reliable across runs.

**Data requirements:**
- N = 30 runs per (model × bias_type × variant) cell — needed to estimate within-cell variance reliably
- Temperature ablation subset: 3 models × 5 bias types × 4 temperature levels × 30 runs = 1,800 additional runs (feasibility analysis required before committing)

**Interpretation guidance:**
- If within-cell variance at T=0 is > 0: model's output is non-deterministic even at temperature 0 (possible due to sampling in some APIs). Document this as a data quality issue.
- If within-cell variance at T=0 is 0: all variance at T>0 is attributable to stochastic sampling; cleanly separable from systematic bias.

---

## SRQ4 — Does chain-of-thought prompting attenuate or amplify bias susceptibility?

> **Question:** Does chain-of-thought (CoT) prompting attenuate or amplify bias susceptibility?

### Operationalization

**Unit of observation:** (model, bias_type, prompt_type, run)

**Dependent variable:** `BSI` per (model × bias_type × prompt_type) cell

**Independent variable:** `cot_prompt` (binary: standard vs. chain-of-thought)

**Experimental design:** 2×2 factorial for the two bias types expected to respond most differently to CoT:
- **Cell 1:** Anchoring × Standard prompt
- **Cell 2:** Anchoring × CoT prompt
- **Cell 3:** Decoy × Standard prompt
- **Cell 4:** Decoy × CoT prompt

CoT prompt format: Add a reasoning step instruction to the standard prompt: "Before selecting a supplier, think through each option step-by-step and explain your reasoning explicitly before making a final decision."

**Expected pattern (H8):**
- Anchoring: BSI decreases under CoT. Rationale: CoT forces explicit numerical comparison, which counteracts the anchor's role as a reference point. The agent is forced to articulate *why* it deviates from the anchor before choosing.
- Decoy: BSI *increases* (or stays the same) under CoT. Rationale: explicit comparison reasoning amplifies the asymmetric dominance relationship that makes the decoy effective — the agent explicitly compares all three options and the dominated option makes the target look better in the step-by-step trace.

**Statistical test:** 2×2 ANOVA with interaction term (bias_type × prompt_type). The key contrast is the interaction: CoT should lower BSI for anchoring but not for decoy.

**Identification requirement:** This SRQ **requires new prompt variants** (the CoT instruction prefix) that do not currently exist in the BuyerBench harness. The Flagship Design (Design Option 3) must implement:
1. A `prompt_type` parameter in the scenario runner (standard | cot | expert-framed)
2. The CoT instruction variant for each scenario in the p2-xx battery

**Null outcome:** If CoT has no effect on BSI for either bias type, the finding is "structured procurement prompts already contain sufficient constraint to suppress System 2 engagement; additional CoT instructions provide no incremental rationality benefit." This is interpretable given that BuyerBench scenarios include explicit supplier comparison rubrics.

**Data requirements:**
- 4 factorial cells × 30 runs × 10 models = 1,200 additional runs per bias type pair tested
- New CoT prompt variant for each p2-xx scenario

---

## SRQ5 — Are bias susceptibility profiles correlated across bias types within a model?

> **Question:** Are bias susceptibility profiles correlated across bias types within a model, or are they bias-specific?

### Operationalization

**Unit of observation:** model

**Dependent variable (multi-dimensional):** `BSI_vector` = [BSI_anchor, BSI_frame, BSI_decoy, BSI_scar, BSI_sunk] — a 5-dimensional profile per model, with each component estimated from N = 30 runs.

**Analysis:** Inter-bias correlation matrix and reliability analysis:
1. **Spearman correlation matrix** across the 5 BSI dimensions, computed across the 10-model sample. A positive correlation between (e.g.) anchoring and framing BSI suggests models share a common "bias susceptibility factor." A near-zero matrix suggests idiosyncratic vulnerability profiles.
2. **Cronbach's alpha** across the 5-dimension BSI vector per model. High alpha (> 0.70) would suggest a general bias susceptibility trait; low alpha (< 0.50) would suggest bias-type-specific patterns — each model has distinct vulnerabilities.
3. **Hierarchical clustering** of models by BSI profile (Ward method; Euclidean distance in the 5-dimension BSI space). Visualize as dendrogram. Models that cluster together share similar bias vulnerability patterns.

**Expected pattern (H9):** Low inter-bias correlation within model (Cronbach alpha < 0.50). Different training regimes and RLHF reward functions produce different "bias landscapes" — a model that is robust to anchoring may still be susceptible to decoy effects. There is no theoretical reason to expect a general factor.

**Alternative (if positive correlation is found):** A general bias susceptibility factor would imply that model "rationality" is a single underlying trait measurable by any bias battery — analogous to g-factor arguments in cognitive psychology. This is a stronger and more surprising finding that would attract broader attention but would also require careful methodological critique.

**N limitation:** 10 models is a small sample for computing a stable 5×5 correlation matrix. Cross-validation or bootstrap CIs around the correlation estimates are required to assess stability. Results must be framed as exploratory/descriptive.

**Data requirements:**
- Complete BSI estimates for all 5 bias types × all 10 models (requires the full Design Option 1 battery)
- No new scenarios or prompt variants required

---

## Summary: Data Requirements Across All SRQs

| SRQ | New Scenarios Needed | New Prompt Variants | Min Additional Runs | Feasibility |
|---|---|---|---|---|
| SRQ1 | p2-01b (LOW anchor for H4) | None | 3,000 runs (full battery) | Feasible ($450) |
| SRQ2 | None | None | Covered by SRQ1 data + Pillar 1 run | Feasible |
| SRQ3 | None | None | 1,800 (temperature ablation subset) | Feasible if budget allows |
| SRQ4 | None | CoT variants for p2-01, p2-03 | 1,200 per bias type pair | Requires harness work |
| SRQ5 | None | None | Covered by SRQ1 data | Feasible |

**MVP path:** Run SRQ1 (3,000 runs) + SRQ2 and SRQ5 (same data) to produce the minimum viable paper. SRQ3 (temperature ablation) and SRQ4 (CoT variants) are the flagship additions requiring additional engineering.

---

## Identification Gaps Summary

| Gap | Blocking SRQ | Action Required | Priority |
|---|---|---|---|
| Only 1 anchor magnitude level | SRQ1 (anchoring effect), H4 | Create p2-01b: LOW anchor variant | HIGH |
| No CoT prompt variants | SRQ4 (H8) | Add `prompt_type` param to harness; write CoT prefix | MEDIUM |
| N = 10 models too small for regression | SRQ2 (H2) | Label all regression results as descriptive; use Spearman | LOW (design constraint) |
| Temperature ablation not implemented | SRQ3 (H7) | Add temperature parameter to run config; test T ∈ {0.0, 0.3, 0.7, 1.0} | MEDIUM |
| No Pillar 1 scores for all 10 models | SRQ2 (H2) | Run Pillar 1 benchmark for full OpenRouter model set | HIGH |

---

## BibTeX Quick Reference

```bibtex
@article{hagendorff2023human,
  author  = {Hagendorff, Thilo and Fabi, Sarah and Kosinski, Michal},
  title   = {Human-like intuitive behavior and reasoning biases emerged in large language models},
  journal = {Nature Human Behaviour},
  year    = {2023},
  volume  = {7},
  pages   = {1768--1780}
}

@article{huber1982adding,
  author  = {Huber, Joel and Payne, John W. and Puto, Christopher},
  title   = {Adding Asymmetrically Dominated Alternatives: Violations of Regularity and the Similarity Hypothesis},
  journal = {Journal of Consumer Research},
  year    = {1982},
  volume  = {9},
  number  = {1},
  pages   = {90--98}
}

@article{tversky1974judgment,
  author  = {Tversky, Amos and Kahneman, Daniel},
  title   = {Judgment under Uncertainty: Heuristics and Biases},
  journal = {Science},
  year    = {1974},
  volume  = {185},
  number  = {4157},
  pages   = {1124--1131}
}

@article{aher2023using,
  author  = {Aher, Gati V. and Arriaga, Rosa I. and Kalai, Adam Tauman},
  title   = {Using Large Language Models to Simulate Multiple Humans and Replicate Human Subjects Studies},
  journal = {arXiv preprint arXiv:2208.10264},
  year    = {2023}
}
```
