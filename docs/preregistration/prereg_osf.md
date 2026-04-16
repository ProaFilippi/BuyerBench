---
title: "BuyerBench Pillar 2: Behavioral Bias Susceptibility of LLM-Based Procurement Agents — Pre-Registration Document"
authors: "BuyerBench Research Team"
generated_at: "2026-04-16T11:43:07.368238+00:00"
experiment_id: "buyerbench-pillar2-realistic-v1"
git_commit: "unknown"
design_tier: "realistic"
---

# BuyerBench Pillar 2: Behavioral Bias Susceptibility of LLM-Based Procurement Agents — Pre-Registration Document

**Authors:** BuyerBench Research Team  
**Generated:** 2026-04-16T11:43:07.368238+00:00  
**Experiment ID:** `buyerbench-pillar2-realistic-v1`  

---

## 1. Study Information


### 1.1 Study Title

BuyerBench Pillar 2: Behavioral Bias Susceptibility of LLM-Based Procurement Agents — Pre-Registration Document

### 1.2 Description

BuyerBench is an open-source benchmark framework for evaluating the behavioral rationality of large language model (LLM) agents in structured procurement tasks. Pillar 2 tests whether LLM agents make economically optimal supplier selection decisions under controlled behavioral manipulations (anchoring, framing, decoy, scarcity, and sunk cost effects), following the experimental design and econometric strategy documented in the BuyerBench research repository.

### 1.3 Primary Research Question

> Does the behavioral bias susceptibility of LLM-based agents — measured as deviation from economically optimal choices under controlled presentation manipulations — vary systematically across model capability tiers, bias types, and experimental conditions, in ways analogous to, attenuated relative to, or amplified compared to documented human behavioral patterns?

### 1.4 Has data collection begun?

No. This document is completed before data collection commences.


---

## 2. Design Plan


### 2.1 Study Type

Controlled computational experiment. Each scenario pair consists of a BASELINE condition and a TREATMENT condition in which a single behavioral manipulation is introduced. All other economic parameters are held constant across conditions. The design is between-condition (each agent–scenario pair is assigned to one condition per run) with N repeated runs per cell.

### 2.2 Blinding

LLM agents receive no meta-information about the experimental design, bias types being tested, or BuyerBench framework. Agents see only the scenario prompt. No human rater blinding is required for the primary LLM experiment; blinding applies to human comparison arm (Phase 4, requires IRB).

### 2.3 Is there any within-participant design element?

Yes — each model is evaluated on all scenarios (within-agent design across bias types and variants). Analysis accounts for this with clustered standard errors at the agent level (Level 1 WLS specification).

### 2.4 Randomization

Supplier order is randomized per run using a per-run seed (`supplier_order_seed`) stored in the run metadata. This controls for positional bias (preference for items appearing first or last). Seed values are recorded for exact replayability.


---

## 3. Sampling Plan


### 3.1 Existing Data

Registration prior to collection of data: This pre-registration is submitted before any data collection for the registered experiment begins.

### 3.2 Explanation of Existing Data

N/A — no existing data at registration time.

### 3.3 Data Collection Procedures

**Models:** 10 LLM agents via OpenRouter API.  
**Scenarios:** 10 scenario YAML files across 5 bias type batteries.  
**Runs per cell:** N = 50 independent, stateless API calls per (agent × scenario) cell.  
**Temperature(s):** 0.7  
**Prompt version(s):** standard  
**Total planned runs:** 5,000

### 3.4 Sample Size

Primary analysis: N = 50 runs per (agent × scenario × variant) cell.  
Justification: Power analysis (Section G.8 of econometric strategy document) — N = 50 achieves ≥ 70% power for a BSI effect size of d = 0.4 (one-sided t-test, α = 0.05). Adequate power (≥ 80%) is achieved at d ≥ 0.5 with this N.

### 3.5 Sample Size Rationale

The primary expected effect size is d ≈ 0.4, informed by attenuated LLM replication of human behavioral effects (Binz & Schulz 2023; Hagendorff et al. 2023). Human meta-analytic baselines for the five tested bias types range from d = 0.4 (decoy) to d = 2.7 (anchoring); LLM effects in structured domains are expected to be substantially attenuated by explicit scoring rubrics.

### 3.6 Stopping Rule

Data collection stops when all planned 50 runs per (agent × scenario × variant) cell have completed without error. If API rate limits cause > 20% failure rate for a given model, that model's data collection is paused and resumed in a new session; partial runs are included if n_valid_runs ≥ 40 (80% threshold). No data-dependent stopping rule is applied — the pre-specified N is fixed.


---

## 4. Variables


### 4.1 Manipulated Variables

- **`variant`** (categorical): BASELINE vs. TREATMENT within each bias type battery. Treatment variants: ANCHOR_HIGH, FRAMING_GAIN/FRAMING_LOSS, DECOY, SCARCITY, SUNK_COST.
- **`agent_id`** (categorical): 10 OpenRouter LLM agents (between-model comparison).
- **`bias_category`** (categorical): anchoring, framing, decoy, scarcity, sunk_cost (5 bias types; within-model across-type analysis).
- **`supplier_order_seed`** (integer): Per-run randomization seed for supplier list ordering (controls positional bias).

### 4.2 Measured Variables

**Primary outcome:** Bias Susceptibility Index (BSI) per (model × bias type × variant) cell, estimated from N = 50 independent runs. BSI = |P(non-optimal | VARIANT) − P(non-optimal | BASELINE)|, where optimality is defined by the scenario scoring rubric (quality × weight + delivery × weight + cost × weight).


**Secondary outcomes:**

- Within-cell variance of BSI (std_bsi) — stochastic noise component
- Optimality gap — economic distance from optimal supplier choice
- Choice rate distribution — frequency of each supplier selection across runs
- Model-level BSI profile — 5-dimension vector of bias-type-specific means
- Reasoning trace length — token count as a proxy for deliberate reasoning

### 4.3 Indices

**BSI (Bias Susceptibility Index):** Implemented in `evaluators/pillar2.py`. At cell level (N runs): BSI = P(non-optimal | TREATMENT) − P(non-optimal | BASELINE). At run level (single run): BSI = int(decision_changed) × (1 − baseline_score), where baseline_score is the optimality score of the BASELINE run. **Optimality gap:** Economic distance between chosen and optimal supplier, computed as |score_optimal − score_chosen| / score_optimal.


---

## 5. Analysis Plan


### 5.1 Statistical Models

**Level 1 WLS (G.2):** `BSI ~ Treatment + BiasType + Model`, cell-level weighted least squares (weights = n_valid_runs per cell) with clustered sandwich standard errors at the model level. WARP variants excluded from this specification.


**Variance decomposition (G.2):** ANOVA-style SS partition into Model, BiasType, Treatment, and Residual components with η² effect sizes. If η²_Residual > 0.70, the stochastic noise qualification from Section G.2 applies.


**Per-(bias_category × agent_id) treatment effect tests (G.1):** Welch t-test comparing BSI estimates between TREATMENT and BASELINE arms; BH-FDR correction at q = 0.05 across all primary tests.

### 5.2 Transformations

BSI values are in [0, 1] by construction. No transformation is pre-specified. If within-cell BSI distributions show severe non-normality (Shapiro-Wilk p < 0.05 at N = 30), Wilcoxon signed-rank tests will be substituted for one-sample t-tests (reported alongside parametric results for comparison).

### 5.3 Inference Criteria

**Alpha level:** 0.05  
**Family-wise correction:** BH-FDR at q = 0.05  
**Primary significance threshold:** BSI > 0.10 with 95% CI excluding zero, two-sided, α = 0.05 with BH-FDR correction at q = 0.05 across the primary test family (10 models × 5 bias types = 50 tests).  

### 5.4 Data Exclusion

- Runs with error_flag = True (API failures, malformed responses) are excluded from BSI computation; included in n_runs but counted in n_error_runs.
- Runs where extracted_choice is None (unparseable output) are excluded from choice_is_correct and optimality_gap calculations.
- Models with < 80% valid runs across all cells are flagged for exclusion from aggregate analyses; their individual results are still reported.
- Attention check failures in the human comparison arm (Phase 4) are excluded before human BSI computation.

### 5.5 Missing Data

API call failures are logged with error_flag = True and error_message. Excluded from BSI and optimality_gap calculations but included in n_runs. If a model exceeds 20% failure rate across its cells, that model's results are flagged in the report and excluded from aggregate cross-model analyses. No imputation is applied.

### 5.6 Exploratory Analyses

The following analyses are pre-specified as exploratory (not confirmatory):

- H2 capability regression (OLS: mean_BSI ~ pillar1_score) — N = 10 is below inference threshold; labeled descriptive.
- H9 model-specific bias profiles — Cronbach's alpha and hierarchical clustering across 5-dimension BSI vectors; N = 10 limits stability.
- Session order effects (G.6.5): BSI ~ run_index to detect within-session drift.
- Temperature moderation (Phase 3): if multiple temperature levels are collected, BSI ~ temperature × bias_type interaction is exploratory.

### 5.7 Null Result Pre-specification

If BH-FDR-corrected tests fail to reject H₀: BSI = 0 for ≥ 3 of 5 bias types at the planned N, the primary finding is: 'Domain structure (explicit scoring rubrics, constrained supplier comparison) suppresses behavioral bias susceptibility in LLM procurement agents.' This outcome is a scientifically valid contribution and will be reported as such, not treated as a failed study.


---

## 6. Pre-Specified Hypotheses


All hypotheses are pre-specified before data collection. No post-hoc hypothesis additions are permitted. Each hypothesis maps to a PRQ dimension from Section D.1 of the research design.


### 6.H1 — Bias Universality

**PRQ Dimension:** D1: Existence  
**Direction:** positive  

**Statement:** LLM agents exhibit non-trivial bias susceptibility (BSI > 0.10 with 95% CI excluding zero) for at least one bias type, in at least five of ten tested models.


**Test:** Per-bias-type one-sample t-test (H₀: BSI = 0) aggregated across models; BH-FDR correction at q = 0.05 across 5 tests.


**Null outcome:** If BSI ≈ 0 across all bias types, the finding is 'domain structure suppresses bias susceptibility' — a valid contribution, not a failed study.


**Data requirement:** N ≥ 30 runs per (model × bias type × variant) cell.


### 6.H2 — Capability-Bias Tradeoff

**PRQ Dimension:** D3: Capability variation  
**Direction:** negative  

**Statement:** There is a negative Spearman rank correlation between Pillar 1 composite score (agent capability proxy) and mean BSI across bias types at the model level.


**Test:** Spearman rank correlation (ρ) between pillar1_score and mean_BSI across N = 10 models. OLS regression flagged as descriptive only (N = 10 is below inference threshold).


**Null outcome:** Higher-capability models show equal or greater bias susceptibility, consistent with Hagendorff et al. (2023) 'reverse capability' effect in cognitive tasks.


**Data requirement:** Pillar 1 scores for all 10 models + full Pillar 2 BSI battery.


### 6.H3 — Decoy Effect Reliability

**PRQ Dimension:** D2: Bias type variation  
**Direction:** positive  

**Statement:** The decoy bias type (p2-03) produces a BSI significantly greater than zero and higher than the mean BSI across all other bias types.


**Test:** One-sample t-test (decoy BSI > 0); pairwise contrast between decoy mean_BSI and grand mean across remaining 4 bias types (Dunnett or Tukey HSD post-hoc).


**Null outcome:** Decoy manipulation fails to reliably shift supplier choice in structured procurement scenarios — explicit cost/quality rubrics suppress asymmetric dominance effects.


**Data requirement:** N ≥ 30 per (model × variant) cell for p2-03.


### 6.H4 — Anchoring Magnitude Proportionality

**PRQ Dimension:** D2: Bias type variation  
**Direction:** positive  

**Statement:** BSI for high-magnitude anchoring (p2-01, ANCHOR_HIGH) is greater than for low-magnitude anchoring (p2-01b, ANCHOR_LOW), demonstrating proportionality.


**Test:** Paired t-test comparing BSI_HIGH vs BSI_LOW across models.


**Null outcome:** Anchoring effect magnitude does not scale with anchor distance from market price; LLMs may exhibit threshold-based rather than continuous anchoring susceptibility.


**Data requirement:** Requires p2-01b (ANCHOR_LOW scenario) — not yet implemented. H4 is flagged as a design limitation until p2-01b is run.


### 6.H5 — Framing Asymmetry (Loss > Gain)

**PRQ Dimension:** D2: Bias type variation  
**Direction:** positive  

**Statement:** The LOSS frame (p2-02, FRAMING_LOSS) produces higher BSI than the GAIN frame (p2-02, FRAMING_GAIN), consistent with loss aversion predictions.


**Test:** Paired t-test: mean BSI under FRAMING_LOSS vs FRAMING_GAIN across models.


**Null outcome:** No framing asymmetry — LLMs respond symmetrically to gain and loss frames, suggesting RLHF training has suppressed loss aversion in structured domains.


**Data requirement:** N ≥ 30 per (model × variant) cell for p2-02.


### 6.H6 — Sunk Cost × Capability Non-Monotone Interaction

**PRQ Dimension:** D2/D3: Bias × capability interaction  
**Direction:** positive  

**Statement:** High-capability models show greater sunk cost susceptibility than low-capability models, producing a positive (not negative) capability–BSI slope for p2-05.


**Test:** Spearman correlation between pillar1_score and BSI_sunk_cost. Expected sign: positive (opposite to H2 overall direction).


**Null outcome:** Sunk cost susceptibility decreases with capability (consistent with H2), suggesting structured rubrics override narrative cost-justification reasoning.


**Data requirement:** Pillar 1 scores + N ≥ 30 per (model × variant) cell for p2-05.


### 6.H7 — Stochastic Variance Proportional to BSI

**PRQ Dimension:** D4: Stochastic vs. systematic variance  
**Direction:** positive  

**Statement:** Within-cell variance (std_bsi) is positively correlated with mean BSI across all cells, consistent with a boundary-response mechanism.


**Test:** OLS regression: std_bsi ~ β₀ + β₁·mean_bsi. Significant positive β₁ supports H7.


**Null outcome:** No variance–mean relationship; BSI variance is uniform across susceptibility levels, suggesting stochastic noise is independent of bias signal.


**Data requirement:** N ≥ 2 runs per cell to estimate within-cell variance.


### 6.H8 — CoT Reduces Anchoring but Not Decoy

**PRQ Dimension:** D4: Prompt moderation  
**Direction:** non directional  

**Statement:** Chain-of-thought prompting reduces anchoring BSI (p2-01) but does not reduce — and may increase — decoy BSI (p2-03), producing a significant bias_type × prompt_version interaction.


**Test:** 2×2 ANOVA: BSI ~ bias_type × prompt_version (standard | cot). Key interaction contrast: Δ(decoy CoT − decoy standard) > Δ(anchor CoT − anchor standard).


**Null outcome:** CoT has no differential effect — structured procurement prompts already engage sufficient deliberate reasoning to suppress both effects equally.


**Data requirement:** CoT prompt variants for p2-01 and p2-03 (requires UPGRADE-7).


### 6.H9 — Model-Specific Bias Profiles

**PRQ Dimension:** D3: Model-specific patterns  
**Direction:** null  

**Statement:** Cronbach's alpha across the 5-dimension BSI vector (one dimension per bias type) is low (< 0.50) across the 10-model sample, indicating bias-specific rather than general susceptibility patterns.


**Test:** Cronbach's alpha on [BSI_anchor, BSI_frame, BSI_decoy, BSI_scar, BSI_sunk] across N = 10 models. Spearman inter-bias correlation matrix. Hierarchical clustering (Ward linkage, Euclidean distance in 5D BSI space).


**Null outcome:** High alpha (> 0.70) implies a general bias susceptibility factor — a surprising finding that would suggest 'rationality' is a single latent trait.


**Data requirement:** Complete BSI estimates for all 5 bias types × all 10 models.


### 6.H10 — Human Benchmark Calibration

**PRQ Dimension:** D5: Human comparison  
**Direction:** negative  

**Statement:** LLM BSI effect sizes (Cohen's d vs. 0) are smaller than human meta-analytic benchmarks for the same bias categories from behavioral economics literature.


**Test:** Per-bias-type Cohen's d comparison between BuyerBench LLM estimates and published human baselines: anchoring (d ≈ 2.7), framing (d ≈ 1.8), decoy (d ≈ 0.4), sunk cost (d ≈ 0.85), scarcity (d ≈ 0.60–0.80). For human arm data: independent two-sample Welch t-test on BSI.


**Null outcome:** LLM effect sizes match or exceed human benchmarks — LLMs are as or more susceptible than humans to behavioral biases in structured procurement tasks.


**Data requirement:** Multi-run BSI estimates for all 5 bias types. Human comparison arm requires UPGRADE-13 + IRB approval (Phase 4).


---

## 7. Other


### 7.1 Registered Model Set

The following models are registered as the comparison set. No post-hoc model additions are permitted. Models may be excluded if they exceed the 20% failure threshold (see 5.4).

- `openai/gpt-4o`
- `anthropic/claude-3.5-sonnet`
- `google/gemini-pro-1.5`
- `meta-llama/llama-3.1-405b-instruct`
- `mistralai/mistral-large`
- `mistralai/mixtral-8x22b-instruct`
- `deepseek/deepseek-chat`
- `qwen/qwen-2.5-72b-instruct`
- `cohere/command-r-plus`
- `01-ai/yi-large`

### 7.2 Registered Bias Type Battery

The following bias categories are registered. No post-hoc bias type additions to the primary confirmatory analysis are permitted.

- anchoring
- framing
- decoy
- scarcity
- sunk_cost

### 7.3 Codebase Version

Registered codebase commit: `unknown`.  
Experiment configuration frozen in `experiment_manifest.json` (experiment_id: `buyerbench-pillar2-realistic-v1`).

### 7.4 Open Science Statement

BuyerBench is open-source (MIT License). All scenario definitions, evaluation code, raw run records (excluding any API credentials), and analysis scripts will be made publicly available at the time of paper submission. Pre-registration predates any data collection. Deviations from this pre-registration, if any, will be documented in the paper under 'Deviations from Pre-Registration'.

### 7.5 References

- Tversky, A. & Kahneman, D. (1974). Judgment under uncertainty: Heuristics and biases. *Science*, 185(4157), 1124–1131.
- Tversky, A. & Kahneman, D. (1981). The framing of decisions and the psychology of choice. *Science*, 211(4481), 453–458.
- Huber, J., Payne, J. W. & Puto, C. (1982). Adding asymmetrically dominated alternatives. *Journal of Consumer Research*, 9(1), 90–98.
- Arkes, H. R. & Blumer, C. (1985). The psychology of sunk cost. *Organizational Behavior and Human Decision Processes*, 35(1), 124–140.
- Binz, M. & Schulz, E. (2023). Using cognitive psychology to understand GPT-3. *PNAS*, 120(6).
- Hagendorff, T., Fabi, S. & Kosinski, M. (2023). Human-like intuitive behavior and reasoning biases emerged in large language models. *Nature Human Behaviour*, 7, 1768–1780.
- Open Science Collaboration (2015). Estimating the reproducibility of psychological science. *Science*, 349(6251), aac4716.
- Simmons, J. P., Nelson, L. D. & Simonsohn, U. (2011). False-positive psychology. *Psychological Science*, 22(11), 1359–1366.
- Loken, E. & Gelman, A. (2017). Measurement error and the replication crisis. *Science*, 355(6325), 584–585.
- Benjamini, Y. & Hochberg, Y. (1995). Controlling the false discovery rate. *Journal of the Royal Statistical Society B*, 57(1), 289–300.
