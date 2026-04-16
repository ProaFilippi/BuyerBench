---
type: analysis
title: "Section G — Econometric Strategy"
created: 2026-04-16
tags:
  - econometric-strategy
  - pillar2
  - llm-bias
  - behavioral-economics
  - regression
  - power-analysis
  - pre-registration
  - robustness-checks
  - falsification
  - multiple-hypothesis-correction
related:
  - '[[f1-realistic-design]]'
  - '[[f2-flagship-design]]'
  - '[[d1-primary-research-question]]'
  - '[[d2-secondary-research-questions]]'
  - '[[g-econometric-strategy]]'
  - '[[b5-01-open-science-collaboration-2015]]'
  - '[[b5-02-simmons-nelson-simonsohn-2011]]'
  - '[[b5-03-loken-gelman-2017]]'
  - '[[b2-02-repeated-measurement-charness-levin-2005]]'
---

# Section G — Econometric Strategy

---

## Overview

This document specifies the complete econometric strategy for BuyerBench Pillar 2. It covers:

- **G.1** — Primary estimands (what we are estimating)
- **G.2** — Primary regression equations (how we estimate it)
- **G.3** — Fixed vs. random effects decision (identification choice)
- **G.4** — Standard errors and clustering (inference choice)
- **G.5** — Multiple hypothesis correction
- **G.6** — Robustness checks (mandatory)
- **G.7** — Falsification tests
- **G.8** — Power analysis
- **G.9** — Pre-registration plan

All specifications in this document are locked before data collection. Any deviation from these pre-specified procedures must be labeled as exploratory in the paper.

---

## G.1 Primary Estimands

The primary quantities of interest are defined formally before data collection. Each estimand maps to one or more hypotheses in [[d1-primary-research-question]] and [[d2-secondary-research-questions]].

### τ_bias(b, m) — Within-Model Bias Treatment Effect

```
τ_bias(b, m) = E[BSI | bias=b, model=m, variant=TREATMENT]
             − E[BSI | bias=b, model=m, variant=BASELINE]
```

**Interpretation:** The expected increase in Bias Susceptibility Index when the agent receives the manipulation (TREATMENT) relative to the unmanipulated version (BASELINE), for a specific model m and bias type b.

**Identification:** Controlled variant pairing; repeated runs (N=30 or 50) for noise reduction. The between-subject design (see [[f1-realistic-design]]) ensures no carry-over contamination between BASELINE and TREATMENT arms.

**This is the core estimand.** All primary hypothesis tests (H1, H3, H5) reduce to tests of τ_bias(b, m) > 0 for various (b, m) combinations.

---

### σ²_stoch(m, b) — Within-Cell Stochastic Variance

```
σ²_stoch(m, b) = Var[BSI | model=m, bias=b] across runs
```

**Interpretation:** The variance of BSI attributable to pure stochastic sampling noise — how much the model's output distribution varies across identically-specified runs. This is not behavioral variance; it is measurement variance.

**Identification:** N=30 independent runs per cell yield a direct empirical estimate. Models are **stationary** (no cross-session learning; see [[b2-02-repeated-measurement-charness-levin-2005]]), so within-cell variance is i.i.d. temperature noise.

**Connection to H7:** H7 predicts σ²_stoch(m, b) is positively correlated with τ_bias(b, m) — biased decisions are noisier because the agent is near a decision boundary.

---

### σ²_model — Between-Model Variance

```
σ²_model = Var[E[BSI | model=m]] across models
```

**Interpretation:** How much of the total BSI variance is attributable to systematic differences between models (as opposed to within-model stochasticity or bias-type effects).

**Identification:** Variance decomposition (ANOVA-style SS partition) across 10 models. This is the inter-model heterogeneity measure; high σ²_model supports H9 (model-specific vulnerability profiles).

---

### Δ_capability — Capability-BSI Gradient

```
Δ_capability = ∂E[BSI] / ∂P1_score
```

**Interpretation:** The marginal change in expected BSI per unit increase in Pillar 1 capability score. A negative Δ_capability supports H2 (higher capability → lower bias susceptibility).

**Identification:** OLS regression across N=10 models. This is treated as **descriptive** throughout the paper — with N=10, no inference claims are made. Δ_capability is reported as a suggestive pattern with wide confidence intervals.

---

## G.2 Primary Regression Equations

### Level 1 — Run-Level OLS

```
BSI_{i,m,b,r} = α + β_b · BiasType_b + β_m · Model_m + β_t · Treatment_i
              + β_bm · (BiasType_b × Model_m)
              + β_tm · (Treatment_i × Model_m)
              + ε_{i,m,b,r}
```

**Notation:**
- i = scenario instance (bias_type × variant combination)
- m = model index
- b = bias type index
- r = run index within cell
- Treatment_i ∈ {0, 1} — 1 if the variant is TREATMENT (manipulated), 0 if BASELINE
- ε_{i,m,b,r} — residual; standard errors clustered at model level (see G.4)

**Key coefficients:**
- β_t: average treatment effect of bias manipulation across all models and bias types
- β_bm: interaction showing whether treatment effect varies by (bias_type, model) combination — heterogeneous treatment effects
- β_tm: interaction showing whether treatment effect varies by model — identifies which models are susceptible

**Reported as:** Table of β coefficients with clustered SEs, t-statistics, BH-FDR-corrected p-values, and 95% confidence intervals.

---

### Hierarchical (Mixed-Effects) Extension

```
BSI_{i,m,b,r} = α + X_i β + Z_m u_m + Z_b v_b + ε_{i,m,b,r}

u_m ~ N(0, Σ_model)   [random effects for model]
v_b ~ N(0, Σ_bias)    [random effects for bias type]
```

**When to use this specification:** If the primary OLS in Level 1 shows heteroskedasticity across models or bias types (Breusch-Pagan test, p < .05), switch to mixed-effects. The hierarchical model also provides variance component estimates (Σ_model and Σ_bias) that directly address SRQ3 and SRQ5.

**Implementation:** `lme4` in R or `statsmodels.MixedLM` in Python. REML estimation for variance components; ML estimation for fixed-effect comparisons.

**Reported as:** Supplementary table alongside the main OLS for transparency.

---

### H2 Specification — Capability-BSI Relationship

```
mean_BSI_m = α + β_1 · P1Score_m + β_2 · log(Parameters_m) + β_3 · ModelFamily_m + ε_m
```

**Covariates:**
- P1Score_m: Pillar 1 aggregate capability score for model m
- log(Parameters_m): log of model parameter count (proxy for scale; log transformation for proportional effects)
- ModelFamily_m: Categorical indicator for model family (OpenAI, Anthropic, Google, Meta, Mistral) — controls for training recipe and RLHF style

**Critical caveat:** N=10 observations. Present as **descriptive OLS only**; do not report inference statistics or p-values as causal estimates. Report R² and point estimates with wide CIs. Use the phrase "suggestive pattern" not "evidence for" in the paper.

**Purpose:** The capability regression is primarily a visualization tool (scatter plot of P1Score vs. mean_BSI with model labels) and a descriptive quantification. Its value is illustrative, not inferential.

---

### Variance Decomposition (ANOVA-Style)

```
BSI = μ + Model_effect + BiasType_effect + Prompt_effect + Temperature_effect + Residual
```

**Reported as:** SS partition table (Flagship Design only; Level 1 + Temperature are required):

| Source | SS | df | MS | F | η² | Interpretation |
|---|---|---|---|---|---|---|
| Model | SS_model | 9 | MS_model | F_model | η²_model | Fraction of total BSI variance explained by model identity |
| BiasType | SS_bias | 4 | MS_bias | F_bias | η²_bias | Fraction explained by bias type |
| Prompt | SS_prompt | 2 | MS_prompt | F_prompt | η²_prompt | Fraction explained by prompt version |
| Temperature | SS_temp | 3 | MS_temp | F_temp | η²_temp | Fraction explained by temperature |
| Residual | SS_res | N-1-df_above | MS_res | — | — | Within-cell stochastic noise |

**Interpretation:** The η² column is the paper's primary answer to SRQ3. If η²_residual > 0.70, most BSI variance is stochastic noise — a finding that significantly qualifies any bias detection claims.

---

## G.3 Fixed vs. Random Effects Decision

The choice between fixed and random effects reflects what claim we are making about the entities in our sample.

### Model Effects: **Fixed Effects**

**Rationale:** We are comparing specific named models (GPT-4o, Claude 3.5 Sonnet, Gemini Pro 1.5, etc.). The inference target is the behavior of these specific models — not an inference about "a population of LLMs from which we sampled." Including model FE makes β_m directly interpretable as "how much more biased is model m than the average model."

**Implementation:** Model dummy variables in OLS; no random effects for model.

**Reviewer response:** A reviewer may argue for random effects to increase generalizability. Respond: "We treat models as fixed because our scientific interest is in specific commercial systems deployed in procurement contexts. Generalization to a population of hypothetical LLMs is not our inference target — practitioners need to know about GPT-4o, not about a latent LLM distribution."

### Bias Type Effects: **Fixed Effects**

**Rationale:** We test 5 specific bias categories, not a random sample from a universe of biases. The inference target is the BSI for anchoring specifically, framing specifically, etc. Random effects would shrink estimates toward a grand mean — inappropriate when we have strong theoretical priors about each bias type from [[b1-01-anchoring-tversky-kahneman-1974]] through [[b1-05-scarcity-cialdini-worchel-1975]].

**Implementation:** Bias type dummy variables in OLS.

### Run Effects: **Random**

**Rationale:** Each run is a stochastic draw from the model's output distribution. Runs within a cell are exchangeable (independent, identically distributed given the model and scenario). Random run effects are the residual variance structure.

**Note:** This is not a free modeling choice — it follows directly from the BuyerBench design's stationary-agent architecture (no cross-session learning; confirmed by [[b2-02-repeated-measurement-charness-levin-2005]] design precedent).

### Documentation for Reviewers

Include a dedicated paragraph in the methods section (not just a footnote) documenting the FE/RE rationale. Reviewers at JEBO and Experimental Economics will specifically check whether model effects should be random, and the "specific named models" argument must be made explicit before reviewers ask.

---

## G.4 Standard Errors and Clustering

### Primary Clustering Strategy

Cluster standard errors at the **model level** (10 clusters).

**Rationale:** Runs within the same model are correlated — they share the same underlying weight distribution, training data, and RLHF policy. This within-model correlation violates the OLS assumption of i.i.d. residuals. Clustering at the model level accounts for this correlation.

**Small-cluster warning:** 10 clusters is at the boundary of reliable cluster-robust inference. The literature (Cameron & Miller, 2015) recommends ≥ 20–30 clusters for asymptotic theory to apply. With 10 clusters:
- Wild cluster bootstrap (WCB) is more reliable than asymptotic cluster-robust SEs for significance testing
- Conservative critical values (t_{G-1} = t_9 distribution) should be used
- All main text p-values should use WCB; asymptotic clustered SEs are in the supplementary appendix

**Reported as:** Both clustered SEs and heteroscedasticity-robust (HC3) SEs in the main table. A footnote documents the small-cluster limitation and references Cameron & Miller (2015) for the WCB procedure.

### Within-Model Tests

For tests comparing BASELINE vs. TREATMENT within a single model (the core τ_bias(b, m) estimand), use **pair bootstrap:**

1. Within each cell (model m, bias type b), resample runs with replacement
2. For each bootstrap sample, compute the test statistic (BSI_treatment − BSI_baseline)
3. Repeat 10,000 times to obtain the bootstrap distribution
4. Report the empirical 2.5th and 97.5th percentile as the 95% CI

This is the most assumption-free inference procedure for the N=30 per cell design and is robust to the non-normal distribution of BSI (bounded [0, 1]).

---

## G.5 Multiple Hypothesis Correction

### Primary Family: H1–H10

**Correction procedure:** Benjamini-Hochberg (BH) False Discovery Rate at q = 0.05

**Family composition:** 10 primary hypotheses, each generating 1–2 test statistics. Treat as a single family for correction purposes.

**Rationale for BH over Bonferroni:** Bonferroni is excessively conservative at N_tests = 10 and would require each individual test to achieve p < 0.005. Given that our priors strongly favor finding at least some significant effects (bias research literature shows consistent effects at d > 0.5 for human subjects), controlling FDR rather than FWER is the appropriate trade-off.

### Secondary Family: Within-Bias-Type Model Comparisons

For pairwise model comparisons within each bias type:
- 10 models × 5 bias types = 50 individual BSI estimates
- C(10, 2) = 45 pairwise model comparisons per bias type × 5 bias types = 225 pairwise tests

**Correction procedure:** BH-FDR at q = 0.05 applied within each bias-type family (45 tests per family, 5 families = 5 separate corrections). Alternatively: Bonferroni within each family for conservatism.

### Pre-Registration Requirement

Both the primary and secondary correction procedures must be **pre-registered before data collection**. Post-hoc selection of correction procedures is a researcher degree of freedom documented in [[b5-02-simmons-nelson-simonsohn-2011]].

### Reporting

Report **both** corrected and uncorrected p-values in the appendix. The main text reports BH-corrected results only, with a note explaining the correction and linking to the appendix for uncorrected p-values (standard practice in behavioral economics papers).

---

## G.6 Robustness Checks (Mandatory)

These checks are pre-specified. If any check fails (shows sensitivity), the result must be flagged in the paper body — not buried in appendix or omitted.

### Temperature Robustness

**Protocol:** Re-run primary regressions at temp=0.0 (deterministic mode) for all models that support it.

**Interpretation:**
- If results at temp=0.0 are qualitatively similar to temp=0.7 → findings are not temperature-sensitive; temperature controls the noise floor but not the bias direction.
- If results collapse at temp=0.0 (BSI → 0 uniformly) → findings are temperature-dependent; the bias susceptibility is an artifact of high-entropy sampling, not a stable preference structure. This must be prominently flagged.

**Expected outcome:** Most bias results at temp=0.0 will show low BSI because deterministic decoding selects the mode of the distribution. But if a model shows high BSI even at temp=0.0, this is a strong finding (deterministic bias signature).

### Prompt Wording Robustness

**Protocol:** Re-run a subset of scenarios (1–2 per bias type) with minor surface rephrasing: different supplier names (e.g., "SupplierNovus" instead of "SupplierAlpha"), different dollar amounts ($95k vs. $100k), different geographic locations.

**Interpretation:**
- If BSI changes substantially across surface variants → the bias effect is surface-level sensitive; our measure captures prompt-specific patterns, not generalizable bias structure.
- If BSI is stable → the bias effect is robust to surface wording; supports generalizability claim.

**Note:** Minor rephrasing should not change the underlying economic structure (optimal choice, EV gap, manipulation direction). Only surface labels change.

### Model Version Stability

**Protocol:** If API access permits, test two versions of the same model family (e.g., GPT-4o vs. GPT-4o-mini; Claude 3.5 Sonnet vs. Claude 3.5 Haiku).

**Interpretation:** Does the ordering of BSI across models hold within a family? If GPT-4o-mini shows higher BSI than GPT-4o, this supports H2 (capability-BSI negative gradient within family). If the ordering reverses → H2 is fragile to fine-grained capability differences within a family.

**Caveat:** API model version strings must be pinned at collection time. If OpenRouter changes underlying model versions between collection windows, document and treat as a robustness test rather than a confound.

### Outlier Robustness

**Protocol:** Drop the top 5% and bottom 5% of BSI scores by run; re-estimate primary regressions.

**Interpretation:** If results are driven by extreme individual runs (BSI = 0.0 or 1.0 for every run in a cell), the findings may reflect execution failures rather than genuine bias patterns. The outlier trim identifies whether central tendency results hold when extreme cells are excluded.

**Expected finding:** Near-zero BSI cells (most models on most scenarios) are not outliers — they are the central result. The trim should primarily affect cells with execution failures (BSI = 1.0 from parse errors, not genuine bias).

### Session Order Effects

**Protocol:** Regress BSI on run_index (1–30 within each cell). If the coefficient on run_index is significantly non-zero → BSI is drifting within the collection window.

**Expected result:** Flat (coefficient ≈ 0). BuyerBench sessions are stateless; models have no memory of prior runs. A significant order effect would indicate API-level effects (e.g., model load/cache effects) or within-collection model version updates. Flag if detected.

---

## G.7 Falsification Tests

Falsification tests check whether the measurement instrument itself is valid — not whether the hypotheses are true. A failing falsification test invalidates the BSI measure entirely.

### Placebo Test

**Design:** Create "null variants" where the manipulation is present in surface text but the economics are identical to baseline. Example: change supplier names (Alpha → Nexus, Beta → Vertex) while keeping all prices and attributes identical.

**Prediction:** BSI = 0 on null variants. If BSI > 0 → the measurement instrument captures surface-text sensitivity, not economic manipulation.

**Interpretation:** A non-zero placebo BSI is the most threatening possible failure mode — it would mean every positive result in the main analysis could be explained by irrelevant surface changes rather than the intended manipulation. Run this test before the main data collection.

### Null Model Test

**Design:** Run MockAgent (deterministic rule-based agent, always selects the economically optimal supplier) on all scenarios at N=30.

**Prediction:** MockAgent BSI = 0 by construction (it always selects optimally regardless of presentation). If MockAgent BSI > 0 → the scenario evaluation logic contains a bug (e.g., incorrect ground-truth assignment, parsing error in the evaluator).

**Implementation:** This test is already executable at zero API cost. It should be run as part of CI validation and before every main data collection run.

### Reversed Optimal Test

**Design:** For a subset of scenarios, invert which option is "correct" — relabel the inferior supplier as "optimal" in the evaluator while keeping the prompt identical.

**Prediction:** All models should score BSI ≈ 1.0 under the reversed optimal evaluation (since they are now always "wrong" by the inverted rubric). If models partially score correctly under the inverted rubric → some models' choices correlate with the true economic optimum via reasoning that bypasses the bias detection mechanism. This would indicate a measurement validity issue.

**Note:** The reversed optimal test is not about detecting bias — it is about verifying that the evaluator is measuring what it claims to measure.

---

## G.8 Power Analysis

### Target Effect Size

**d = 0.4 (moderate effect)**

Justification: Human behavioral bias studies typically report d = 0.7–1.0 (anchoring: r ≈ 0.8 per Tversky & Kahneman; framing reversal: ~50 pp switch; sunk cost: ~54% susceptibility at Arkes & Blumer). We expect LLM effects to be attenuated due to RLHF and explicit constraint-following, justifying a more conservative target of d = 0.4.

### Power Parameters

- α = 0.05 (two-tailed)
- Target power = 0.80
- Required N per cell: ~100 observations (from G*Power for two-sample t-test, d = 0.4)

### Power by Sample Size

| N per cell | Power at d=0.4 | Power at d=0.5 | Power at d=0.6 | Label |
|---|---|---|---|---|
| 30 | 0.52 | 0.67 | 0.80 | **Underpowered for d=0.4; exploratory** |
| 50 | 0.70 | 0.83 | 0.92 | **Marginal for d=0.4; adequate for d=0.5+** |
| 100 | 0.86 | 0.95 | 0.99 | **Adequate; gold standard** |

### Design Decision

| Design | N/cell | Label | Use case |
|---|---|---|---|
| Minimum viable (Realistic) | 30 | Exploratory | Use CIs not p-values; no inference claims at d=0.4 |
| Recommended working paper | 50 | Marginal | Inference claims for d≥0.5 effects; hedge d=0.4 |
| Flagship | 100 | Adequate | Full inference; supports all H1–H10 tests |

**Bottom line:** At N=30/cell, report CI-based estimation, not NHST. Upgrade to N=50 before publication submission. Flagship design requires N=100.

### Minimum Viable Sample Table

| Target d | N per cell | Total runs (5 bias × 2 variants × 10 models) | Est. cost |
|---|---|---|---|
| 0.6 (strong) | 30 | 3,000 | $450 |
| 0.5 (moderate) | 50 | 5,000 | $750 |
| 0.4 (modest) | 100 | 10,000 | $1,500 |

### Gold-Standard Sample

N=100/cell + 3 prompt versions + 3 temperatures = 45,000 LLM runs (~$6,750)

This is the minimum for a flagship JEBO submission with full variance decomposition and interaction tests.

### Type M Error Analysis (Loken & Gelman, 2017)

Based on [[b5-03-loken-gelman-2017]], single-shot prior studies (N=1 per cell) exhibit Type M (magnitude inflation) ratios of 3–5× for true BSI ≈ 0.20. At N=30/cell, the Type M ratio drops below 1.5× for true BSI ≥ 0.20, meaning our multi-run design is at minimum a 2–3× improvement in measurement reliability over all prior single-shot LLM bias studies (Binz & Schulz, 2023; Hagendorff et al., 2023; Jones & Steinhardt, 2022).

---

## G.9 Pre-Registration Plan

### Registry

**Platform:** AEA RCT Registry or OSF (Open Science Framework)  
**Timing:** Register before any data collection begins — at minimum before the first OpenRouter API call for the main experiment. Pilot/exploration runs are permissible before registration only if they are clearly labeled as exploratory and no main-experiment conclusions are drawn from them.

### Pre-Registered Content

The following must be locked in the registration document:

1. **Primary hypotheses (H1–H10):** Full text as specified in [[d1-primary-research-question]] and [[d2-secondary-research-questions]]
2. **Primary estimands:** τ_bias(b, m), σ²_stoch(m, b), σ²_model, Δ_capability as specified in G.1
3. **Regression specifications:** Level 1 OLS, hierarchical extension, H2 capability specification as specified in G.2
4. **Fixed vs. random effects choices:** As specified in G.3
5. **Correction procedures:** BH-FDR at q=0.05 for primary family; BH or Bonferroni for secondary family; as specified in G.5
6. **Robustness checks:** All 5 checks in G.6 pre-specified as mandatory
7. **Falsification tests:** Placebo, null model, reversed optimal tests as specified in G.7
8. **Model set:** Exact model identifier strings (pinned versions)
9. **Bias scenario set:** Exact scenario IDs (p2-01 through p2-05 for Realistic; p2-01 through p2-08 for Flagship)
10. **BSI threshold for primary claims:** d ≥ 0.20 (effect size threshold below which we treat results as consistent with null)

### Labeling Requirements in the Paper

| Analysis type | Label requirement |
|---|---|
| Registered hypothesis tests | "Pre-registered" in table headers |
| Registered robustness checks | "Mandatory robustness check (pre-registered)" |
| Exploratory analyses | "Exploratory analysis (not pre-registered)" |
| Findings from pilot runs | "Preliminary/pilot; not pre-registered" |

### Registered vs. Exploratory Table

Include a dedicated table in the paper appendix listing every analysis with its pre-registration status. This is standard practice for JEBO submissions and increasingly required by Experimental Economics. The table signals rigorous methodology and prevents p-hacking accusations for the exploratory results.

---

## Summary: Key Econometric Decisions (Quick Reference)

| Decision | Choice | Rationale |
|---|---|---|
| Primary estimand | τ_bias(b, m) — within-model treatment effect | Core PRQ; identified by controlled variant design |
| Regression specification | OLS with model FE and bias type FE; hierarchical extension as robustness | Named models → FE; named bias types → FE |
| Model effects | Fixed | Specific commercial systems; not a population draw |
| Bias type effects | Fixed | 5 specific categories; not a population draw |
| Run effects | Random (residual) | i.i.d. stochastic draws from stationary model distribution |
| SE clustering | Model level (10 clusters); WCB for inference | Within-model correlation; small-cluster WCB correction |
| MHT correction | BH-FDR q=0.05 (primary family); BH or Bonferroni (secondary) | Pre-registered before data collection |
| Power at N=30 | 0.52 at d=0.4 → exploratory label; report CIs | Upgrade to N=50 for publication |
| Pre-registration | AEA RCT Registry or OSF; before data collection | Required for JEBO-tier credibility |

---

## BibTeX Quick Reference

| Citation | Key claim in this document |
|---|---|
| Loken & Gelman (2017) | Type M error analysis; N=30 minimum viable threshold; [[b5-03-loken-gelman-2017]] |
| Simmons, Nelson & Simonsohn (2011) | Pre-registration requirement; researcher degrees of freedom; [[b5-02-simmons-nelson-simonsohn-2011]] |
| Open Science Collaboration (2015) | N=30 power analysis; CI reporting for exploratory results; [[b5-01-open-science-collaboration-2015]] |
| Charness & Levin (2005) | Stationary-agent design justification (no learning confound); [[b2-02-repeated-measurement-charness-levin-2005]] |
| Greenwald (1976) | Between-subject design rationale; demand effects in within-subject designs; [[b2-03-within-between-subject-greenwald-1976]] |
| Benjamini & Hochberg (1995) | BH-FDR correction procedure |
| Cameron & Miller (2015) | Small-cluster warning; wild cluster bootstrap recommendation |
