---
type: paper
title: "Behavioral Bias Susceptibility of LLM-Based Procurement Agents: A Pre-Registered Multi-Model Benchmark Study"
created: 2026-04-17
status: working-paper
experiment_id: buyerbench-pillar2-realistic-v1
tags:
  - pillar2
  - behavioral-economics
  - llm-bias
  - procurement
  - pre-registered
  - working-paper
related:
  - '[[PAPER-STATUS]]'
  - '[[prereg_osf]]'
  - '[[g-econometric-strategy]]'
  - '[[d1-primary-research-question]]'
  - '[[f1-realistic-design]]'
---

# Behavioral Bias Susceptibility of LLM-Based Procurement Agents: A Pre-Registered Multi-Model Benchmark Study

**Authors:** [Author list TBD]

**Pre-registration:** OSF registration ID [TBD — register `docs/preregistration/prereg_osf.md` before data collection]

**Code and data:** `https://github.com/[org]/BuyerBench` (MIT License)

**Version:** Working paper. All result placeholders marked `{{RESULT:...}}` require data from the pre-registered N=50/cell experiment (experiment ID: `buyerbench-pillar2-realistic-v1`). No result figures should be populated before data collection is complete and Gate 1 clearance is confirmed.

> **Scope statement (REV-7):** This paper evaluates the *final selection stage* of LLM-based buyer agents — specifically, the economic judgment made when structured procurement options are presented — and not the full agent pipeline (retrieval, API calls, multi-turn context). Claims about "AI buyer agents" in this paper are scoped to this final decision module. See Section 3.1 for full justification.

> **Data status (REV-3):** All result cells marked `{{RESULT:...}}` are populated from the N=50 pre-registered experiment. Single-run pilot data (N=1 per cell) are EXPLORATORY ONLY and are not cited as evidence for any claim. See Section 3.4.

---

## Abstract

Large language models are increasingly deployed as buyer agents that execute supplier selection and procurement decisions autonomously. Whether these agents make economically rational decisions — or whether they are susceptible to the same cognitive biases documented in human decision-makers — is an open empirical question with direct consequences for procurement outcomes. We present a pre-registered, multi-model benchmark study measuring behavioral bias susceptibility across five canonical bias types (anchoring, framing, decoy, scarcity, and sunk cost) in ten frontier LLMs operating on structured procurement selection tasks. Using the Bias Susceptibility Index (BSI) — the probability of a bias-induced decision change weighted by its economic cost — we evaluate each model across N=50 independent runs per (model × bias type × variant) cell (5,000 total runs), providing the first stochasticity-aware, within-model estimate of procurement decision bias in LLMs. We test four pre-registered confirmatory hypotheses (H1: bias universality; H3: decoy reliability; H5: framing asymmetry; H7: stochastic variance proportionality), applying Benjamini-Hochberg false discovery rate correction at q=0.05. *Optimality is defined relative to each scenario's stated evaluation weights; we test internal rationality, not external optimality.* Preliminary infrastructure validation with N=1 pilot data confirms the measurement pipeline is valid; full results will be reported at the pre-specified N=50.

**[TIER-A]** At N=50 per cell: `{{RESULT: X}}/10` models show BSI > 0.10 on at least one bias type (BH-corrected p < 0.05). The decoy effect produces BSI higher than the cross-bias mean (H3 Dunnett: d = `{{RESULT: h3_dunnett_d}}`, p = `{{RESULT: h3_dunnett_p}}`). Within-cell variance is positively correlated with mean BSI across cells (H7: β₁ = `{{RESULT: H7_beta}}`, p = `{{RESULT: H7_p}}`), consistent with the pre-specified boundary-response interpretive frame for H7 (mechanism not directly tested).

**[TIER-B]** Descriptively, among the five bias types, the decoy effect shows the highest mean BSI (`{{RESULT: mean_BSI_decoy}}`), followed by `{{RESULT: second_highest_bias_type}}` (N=10 models; cross-bias ranking is descriptive, not pre-registered).

---

## 1. Introduction

### 1.1 Motivation

Procurement decision-making is being delegated to AI agents. Enterprise platforms including SAP Joule/Ariba, Coupa AI, and Ivalua IVA embed LLM copilots that not only recommend but execute supplier selection decisions. Consumer-facing deployments — Amazon Rufus, Google Agentic Checkout, Klarna AI — are accumulating transaction volumes that make delegation economically consequential at scale. Payment network programs from Visa (Intelligent Commerce) and Mastercard (Agent Pay) are building infrastructure explicitly designed for agent-initiated transactions, cementing the shift from recommendation to execution.

This deployment trajectory makes a fundamental research question urgent: *are LLM-based procurement decision-making modules economically rational?* The behavioral economics literature documents a robust taxonomy of cognitive biases in human procurement and purchasing behavior — anchoring to irrelevant price references [@kahneman1974judgment], preference reversals under gain/loss framing [@tversky1981framing], choice distortions introduced by asymmetrically dominated decoy options [@huber1982adding], urgency-driven degradation under artificial scarcity signals [@cialdini1984influence], and forward-decision contamination by sunk costs [@arkes1985psychology]. If LLM agents exhibit analogous biases, procurement outcomes under delegation will systematically deviate from the stated objectives of the organizations that deploy them.

Whether LLMs exhibit these biases is an empirically contested question. A growing literature (2023–2025) documents bias-like patterns in LLM responses [@hagendorff2023human; @echterhoff2024anchoring; @tjuatja2024llm], but these studies use generic economic scenarios or abstract choice problems — not the structured, multi-attribute supplier selection tasks that characterize actual procurement workflows. The procurement context introduces features absent from prior work: explicit scoring rubrics with stated weights, multi-dimensional trade-offs across price/quality/delivery, constrained choice sets, and policy-level requirements that may suppress or redirect bias susceptibility. Whether human-documented biases transfer to this domain is an open empirical question.

This paper provides the first pre-registered, stochasticity-controlled, multi-model measurement of behavioral bias susceptibility in LLMs on procurement-domain supplier selection tasks.

### 1.2 Scope and Limitations

**Pipeline scope:** We evaluate the *final selection stage* of LLM-based buyer agent workflows — the judgment call made when an agent receives a structured set of supplier options and must select among them. This scope deliberately excludes upstream pipeline components (retrieval, database queries, API calls, multi-turn negotiation) to isolate the bias signal at the decision point. Real deployed buyer agents include these upstream components; their interaction with the decision module is a meaningful direction for future work but is not evaluated here. Claims about "AI buyer agents" in this paper refer to this scoped evaluation surface. See Section 3.1.

**Internal rationality:** Optimality is defined relative to each scenario's *stated* evaluation weights. We test whether agents optimize the objective function as specified in the task, not whether that objective function is itself normatively correct. This is an *internal* consistency test analogous to revealed preference analysis — we ask whether the agent's decision is coherent with the rubric it was given. This framing is defensible and falsifiable; it does not require us to adjudicate the correctness of the weights themselves.

**Hypothetical choice:** LLM agents receive no monetary payoffs. The biases measured are behavioral patterns in hypothetical-choice conditions. This framing is methodologically analogous to the large hypothetical-choice literature in behavioral economics; Camerer and Hogarth (1999) report that hypothetical and incentivized designs produce comparable effect sizes for most bias categories. We measure "behavioral consistency in hypothetical-choice procurement tasks" — not incentivized decision-theoretic failures.

### 1.3 Contributions

This paper makes four contributions:

1. **Pre-registered multi-model bias battery**: The first pre-registered, stochasticity-controlled measurement of behavioral bias susceptibility in LLM procurement agents across five bias types (anchoring, framing, decoy, scarcity, sunk cost) and ten frontier models. Pre-registration predates data collection (OSF ID: [TBD]).

2. **Bias Susceptibility Index (BSI)**: A computable, scenario-grounded metric for cognitive bias susceptibility that accounts for decision stochasticity. BSI weights bias-induced decision changes by their economic cost, enabling comparison across bias types, models, and experimental conditions.

3. **Stochasticity-aware estimation**: By running N=50 independent trials per cell, we provide within-model distributional estimates of BSI rather than point estimates. This enables proper statistical inference and reveals whether apparent "rationality" (BSI=0) reflects genuine robustness or stochastic measurement luck at N=1.

4. **Structured procurement domain**: The first bias susceptibility data in LLMs for a domain with explicit multi-attribute scoring rubrics — a structural feature absent from prior work that may substantially suppress human-documented bias magnitudes. Whether structured rubrics attenuate, amplify, or redirect bias susceptibility is a testable prediction of this design.

### 1.4 Paper Outline

Section 2 surveys related work across human behavioral economics, LLM cognitive bias research, and procurement AI evaluation. Section 3 describes the experimental design, scenario battery, BSI measurement procedure, and statistical analysis plan. Section 4 presents empirical results organized by hypothesis tier. Section 5 discusses implications, limitations, and future work. Section 6 concludes.

---

## 2. Related Work

### 2.1 Behavioral Biases in Human Decision-Making

The behavioral economics literature establishes robust evidence for systematic deviations from expected utility maximization across five bias categories central to procurement decision-making.

**Anchoring** [@kahneman1974judgment; @tversky1974judgment] describes the tendency for initial numerical values — even arbitrary ones — to anchor subsequent judgments. In procurement contexts, reference prices, prior transaction records, and stated "market rates" have been shown to anchor willingness-to-pay and evaluation thresholds [@ariely2003coherent]. The anchoring effect is among the most robustly replicated in human behavioral economics, with meta-analytic effect sizes reaching d ≈ 2.7 in laboratory settings.

**Framing effects** [@tversky1981framing; @kahneman1979prospect] produce preference reversals when economically equivalent choices are presented as gains versus losses. Prospect theory predicts that loss frames activate disproportionate risk aversion; the same procurement outcome — a 10% cost reduction versus a 10% cost increase avoided — should produce different agent behavior under loss aversion. The canonical risky-choice framing effect shows reversal rates of approximately 60 percentage points in human subjects, yielding d ≈ 1.8.

**Decoy effects** [@huber1982adding; @simonson1989choice] describe preference shifts toward a "target" option introduced by an asymmetrically dominated "decoy" option that is inferior to the target but not to the competitor. The effect is driven by relative advantages becoming locally salient. Human meta-analyses report share increases of approximately 15–20 percentage points for the target option, with d ≈ 0.4.

**Scarcity and urgency effects** [@worchel1975effects; @cialdini1984influence] document decision quality degradation under artificial scarcity cues (limited quantity, deadline pressure). Procurement contexts are particularly susceptible: supplier "limited allocation" signals and "closing tonight" deadlines are common manipulation techniques. Effect sizes range from d ≈ 0.60–0.80 in field experiments.

**Sunk cost fallacy** [@arkes1985psychology; @thaler1980toward] describes the tendency to factor irrecoverable past costs into forward decisions. In procurement, prior investment in a vendor relationship, approved supplier status, or prior contract spend should be irrelevant to the forward utility of a new transaction — yet they systematically bias human evaluators toward incumbent suppliers. Human susceptibility rates are approximately 54% in experimental paradigms (d ≈ 0.85).

### 2.2 Cognitive Biases in Large Language Models

A growing empirical literature documents bias-like patterns in LLM outputs. **Anchoring** is among the best-supported effects: @echterhoff2024anchoring showed that GPT-3.5 and GPT-4 produce price estimates anchored to explicitly arbitrary reference values, with effect sizes comparable to human studies. @tjuatja2024llm found preference reversals in frontier models on gain/loss framing problems adapted from @tversky1981framing. @scherrer2024moral documented default/status-quo bias — disproportionate endorsement of labeled "default" options. @hagendorff2023human observed a "reverse capability" effect: higher-capability GPT-4 showed more System 1-consistent responses than GPT-3 on cognitive reflection tasks, suggesting that instruction-following and debiasing are separable properties.

These findings share a common limitation: they use generic economic gambles or abstract consumer choice scenarios. Structured procurement scenarios — with explicit multi-attribute rubrics, constrained choice sets, and stated evaluation weights — differ systematically from the stimuli used in prior work. Explicit rubrics may redirect System 1 pattern-matching toward System 2 deliberate scoring, potentially suppressing bias effects that appear robustly in unstructured settings. Conversely, the anchor injection that is "obviously irrelevant" in an abstract gamble may appear contextually plausible in a procurement scenario (a "market reference price" is a real entity; a random number is not), potentially amplifying susceptibility. This bidirectional prediction is an empirical question that existing work cannot resolve.

Two key methodological limitations in the existing literature motivate the design choices in this paper. First, **single-run designs**: most existing LLM bias studies evaluate each condition once. LLMs are stochastic; a model with 40% bias susceptibility will appear unbiased in 60% of single-run evaluations. Single-run BSI=0 is uninformative [@loken2017measurement]. N≥30 per cell is the minimum for distributionally meaningful estimates. Second, **absence of pre-registration**: with 10 models × 5 bias types × 2 variants = 100 cells, ~5 false positives are expected at α=0.05 without correction. Pre-registration and BH-FDR correction are necessary to distinguish signal from researcher degrees of freedom [@simmons2011false].

BuyerBench addresses both limitations through N=50 per cell with pre-registered BH-FDR correction.

### 2.3 Procurement AI and Buyer Agent Evaluation

The buyer agent landscape includes enterprise procurement platforms (SAP Joule/Ariba, Coupa AI, Ivalua IVA, Zip), consumer shopping agents (Amazon Rufus, Google Agentic Checkout, Klarna AI), and open-source reference implementations (NegMAS for negotiation, Stripe Agent Toolkit for payment operations). All commercial platforms make capability claims without third-party evaluation data. No prior evaluation framework tests behavioral bias susceptibility in procurement agents.

Existing agent benchmarks do not address this gap. AgentBench [@liu2023agentbench] evaluates general task completion. GAIA [@mialon2023gaia] tests factual retrieval and reasoning. WebArena [@zhou2023webarena] evaluates web-task completion in sandboxed environments. None of these benchmarks includes procurement supplier selection tasks, controlled variant bias manipulations, or within-model distributional estimation of bias susceptibility.

The BuyerBench framework [@buyerbench2026], of which this study is Pillar 2, provides the first multi-dimensional evaluation framework for buyer agents including capability assessment (Pillar 1), economic decision quality (Pillar 2, this paper), and security/compliance evaluation (Pillar 3). This paper focuses exclusively on Pillar 2.

### 2.4 Benchmark Methodology and Rigor

The LLM evaluation literature has identified several threats to benchmark validity [@loken2017measurement; @simmons2011false; @opensciencecollaboration2015]: benchmark contamination from training data, researcher degrees of freedom in post-hoc analysis, absence of pre-registration, and single-run measurement masking stochastic variation.

Our design addresses these threats as follows. **Contamination:** Scenario economics are parameterized at evaluation time (price values, quantity levels, supplier identities); the bias manipulation is applied at runtime, not stored in the model's training data. No exact scenario prompt appears in publicly available training corpora. **Researcher degrees of freedom:** All hypotheses, test specifications, correction procedures, and null-result framings are pre-registered on OSF before data collection. **Stochastic masking:** N=50 runs per cell provides within-cell distributional estimates enabling proper statistical inference. **Multiple comparisons:** BH-FDR correction at q=0.05 is applied across the full primary test family (10 models × 5 bias types = 50 tests).

---

## 3. Methodology

### 3.1 Experimental Design and Pipeline Scope

**Scope:** We evaluate the *final selection stage* of the LLM procurement decision pipeline — the judgment produced when an agent receives a structured set of supplier options with explicit price, quality, and delivery attributes and must select the optimal supplier given stated evaluation weights. This stage is the proximate locus of behavioral bias: anchors, framing manipulations, and decoy options are all injected at this presentation layer. Upstream pipeline components (supplier database retrieval, API-based quote collection, multi-turn negotiation, invoice processing) are not evaluated. This scope choice enables clean identification of the bias signal without confounding tool-use efficiency, retrieval accuracy, or multi-turn context management. See Section 5.3 for limitations arising from this scope restriction.

**Design:** Between-condition controlled experiment. Each (model × scenario × variant) cell receives N=50 independent, stateless API calls. BASELINE and TREATMENT variants for a given bias type are evaluated in separate calls — no agent sees both variants in the same session. This prevents demand effects from within-session contrast [@greenwald1976within]. Supplier order is randomized per run using a reproducible per-run seed (`supplier_order_seed = HMAC-SHA256(base_seed, scenario_id | variant | run_index)` folded to [0, 2³¹)), controlling for positional bias. Seeds are stored for exact replayability.

**Models:** Ten frontier LLMs via OpenRouter API (see Table 1). All models registered before data collection; no post-hoc model additions permitted.

**Temperature:** T=0.7 (primary experiment). Robustness pass at T=0.0 (N=30 per cell) verifies that results are not stochastic sampling artifacts.

### 3.2 Bias Scenario Battery

Five bias type batteries (Table 2) each consist of a BASELINE scenario and one or more TREATMENT variants with identical underlying economics and differing presentation manipulations. All scenarios are loaded from `scenarios/` YAML files with explicit evaluation weights. Additional hard-difficulty variants (p2-09 through p2-11; compound, 6–8 suppliers, δ < 0.05) are included to test ceiling effects from domain-structure suppression.

**Table 2. Bias Scenario Battery**

| Battery ID | Bias Type | Variant Pair | Manipulation | Δ-optimal (δ) |
|---|---|---|---|---|
| p2-01 | Anchoring | BASELINE / ANCHOR_HIGH | $75/unit market reference injected above $50 range | 0.08–0.15 |
| p2-02 | Framing | FRAMING_GAIN / FRAMING_LOSS | Same saving framed as gain vs. cost increase avoided | 0.06–0.12 |
| p2-03 | Decoy | BASELINE / DECOY | Asymmetrically dominated third option added | 0.08–0.15 |
| p2-04 | Scarcity | BASELINE / SCARCITY | "Limited allocation, 4 slots remaining, closes EOD" | 0.08–0.15 |
| p2-05 | Sunk Cost | BASELINE / SUNK_COST | Prior $12,000 rejected supplier investment introduced | 0.08–0.15 |
| p2-09 | Compound (hard) | BASELINE / COMPOUND | Anchor + scarcity simultaneously; 6 suppliers; δ=0.031 | 0.031 |
| p2-10 | Anchoring (hard) | BASELINE / ANCHOR_HIGH | 7 suppliers; anchor at $148 (2.2× catalog max); δ=0.039 | 0.039 |
| p2-11 | Scarcity (hard) | BASELINE / SCARCITY | 8 suppliers; scarcity on cheapest; δ=0.005 | 0.005 |

*Note: δ = composite score gap between optimal and second-best supplier. Hard variants (p2-09 through p2-11) are included for ceiling-effect detection; their results are reported separately and do not enter the primary confirmatory analysis.*

**Worked example (anchoring pair, p2-01):**

*BASELINE prompt fragment:* "You are evaluating suppliers for a 500-unit order. Supplier Alpha: $48/unit, Quality B+, 5-day delivery. Supplier Beta: $52/unit, Quality A, 7-day delivery. Supplier Gamma: $55/unit, Quality A+, 10-day delivery. Evaluation weights: cost 40%, quality 40%, delivery 20%. Select the optimal supplier."

*TREATMENT (ANCHOR_HIGH) prompt fragment:* Identical to BASELINE with one insertion: "The industry reference price for this category is currently $75/unit." The anchor is economically uninformative — it does not change the supplier options, their prices, or the evaluation weights. A rational agent selects the same supplier in both conditions.

### 3.3 BSI Measurement Procedure

**Run-level BSI** (single paired run):

$$\text{BSI}_{\text{run}} = \mathbb{1}[\text{decision\_changed}] \times (1 - s_{\text{baseline}})$$

where $s_{\text{baseline}} \in [0, 1]$ is the composite optimality score of the baseline decision (weighted average of cost, quality, and delivery performance relative to optimal). This formulation weights bias effects by their economic cost: a decision change with $s_{\text{baseline}} = 1.0$ yields BSI = 0 (the baseline was already optimal; changing the decision costs nothing). A decision change with $s_{\text{baseline}} = 0.5$ yields BSI = 0.5 (the baseline was suboptimal; the bias-induced change adds decision cost). The maximum BSI = 1.0 occurs when the agent changes from an already-optimal baseline decision to a non-optimal treatment decision with $s_{\text{baseline}} \approx 0$.

**Key non-obvious property:** BSI = 0 when $s_{\text{baseline}} = 1.0$ *even if the agent changes its decision*. This intentionally prevents double-counting: if both baseline and treatment yield the optimal choice (perhaps different optimal suppliers with identical composite scores), no bias cost has occurred. The BSI measures economic harm from susceptibility, not susceptibility per se.

**Cell-level BSI** (N runs per cell):

$$\widehat{\text{BSI}}(m, b) = \frac{1}{N} \sum_{i=1}^{N} \text{BSI}_{\text{run}, i}(m, b)$$

The cell-level estimator is the sample mean of N independent run-level BSI values. The 95% confidence interval uses the t-distribution with N−1 degrees of freedom: $\widehat{\text{BSI}} \pm t_{0.975, N-1} \cdot \hat{\sigma} / \sqrt{N}$.

**BSI is computed against the scenario's stated evaluation weights** (cost weight, quality weight, delivery weight as specified in the scenario YAML). Optimality is internal to the task specification. A scenario that assigns 60% weight to quality and 20% each to cost and delivery defines a quality-weighted optimal; BSI measures deviation from that stated optimum. The BuyerBench evaluator (`evaluators/pillar2.py`) implements this formula exactly; the research analysis module (`research/analysis/bsi.py`) validates consistency against the production implementation via automated cross-checks.

### 3.4 Statistical Analysis Plan

All analyses pre-specified in OSF registration `buyerbench-pillar2-realistic-v1`. Deviations will be documented in Section 5.4.

**Confirmatory analyses (BH-FDR correction applied at q=0.05):**

- *H1 (Bias Universality):* One-sample t-test per bias type: $H_0: \widehat{\text{BSI}}(b) = 0$. Test family: 5 bias types × 10 models = 50 tests. At least one rejection with BH-FDR q < 0.05 confirms H1.
- *H3 (Decoy Reliability):* One-sample t-test (decoy BSI > 0) plus Dunnett's test contrasting mean decoy BSI against the grand mean of remaining 4 bias types.
- *H5 (Framing Asymmetry):* Paired t-test: $\widehat{\text{BSI}}_{\text{LOSS}} > \widehat{\text{BSI}}_{\text{GAIN}}$ across models.
- *H7 (Stochastic Variance):* OLS regression: $\hat{\sigma}_{\text{cell}} \sim \beta_0 + \beta_1 \cdot \widehat{\text{BSI}}_{\text{cell}}$. Significant positive $\hat{\beta}_1$ confirms H7.

**Primary regression (Level 1 WLS, G.2):**

$$\widehat{\text{BSI}}_{mbv} = \alpha + \beta_{\text{treat}} \cdot \mathbb{1}[v=\text{TREATMENT}] + \sum_b \gamma_b \cdot \mathbb{1}[\text{bias}=b] + \sum_m \delta_m \cdot \mathbb{1}[\text{model}=m] + \varepsilon_{mbv}$$

Weights: $w_{mbv} = n_{\text{valid}}$ per cell. Standard errors: clustered at the model level (10 clusters; HC3 sandwich). WARP scenarios excluded from this specification.

**Variance decomposition (G.2):** ANOVA-style SS partition into Model, BiasType, Treatment, and Residual components. $\eta^2$ effect sizes reported. If $\eta^2_{\text{Residual}} > 0.70$, the stochastic noise qualification applies: "within-cell stochastic variance accounts for the majority of observed BSI variation; reported mean BSI estimates have wide intervals and should be interpreted with caution."

**Exploratory analyses (descriptive only; no inferential claims):**

- H2 (Capability-Bias Tradeoff): Spearman $\rho$ between Pillar 1 score and mean BSI across 10 models. OLS scatter is descriptive (N=10 is below inference threshold).
- H8 (CoT × Bias Type): ANOVA on BSI across `standard` / `cot` / `expert_role` prompt versions. Available from CoT experiment (design tier: `cot_experiment`).
- H9 (Bias Profiles): Cronbach's α on [BSI_anchor, BSI_frame, BSI_decoy, BSI_scar, BSI_sunk] across 10 models. Hierarchical clustering.

**Sample size and power (pre-specified):** N=50 per cell achieves ≥70% power for d=0.4 and ≥80% power for d≥0.5 (one-sided t-test, α=0.05). All results at d < 0.5 are labeled as "suggestive; power < 0.70" per pre-registration.

**Minimum inclusion threshold:** Models with < 80% valid runs (n_valid < 40 of 50) are flagged and excluded from aggregate analyses. Their cell-level results are still reported.

### 3.5 Robustness Checks

**Prompt sensitivity (REV-5):** Prior to the main experiment, a 5-run pilot tested three minor prompt phrasings (synonym substitutions in role assignment and task instruction language) per scenario pair. The coefficient of variation (CV) of BSI across phrasings is computed per scenario; CV > 0.50 triggers a "REDESIGN" gate — the scenario is considered hypersensitive to wording and is not included in confirmatory analysis. Results: `{{RESULT: prompt_sensitivity_summary}}`. All CV values are reported in Appendix D.

**Temperature robustness (T=0.0 pass):** A secondary experiment at T=0.0 (N=30 per cell; `ROBUSTNESS_T0_DESIGN`) verifies that BSI results are not temperature-dependent. If BSI collapses at T=0.0 but persists at T=0.7, the finding is temperature-sensitive and must be qualified as such. Results: `{{RESULT: T0_pass_summary}}`.

**Supplier order control:** Each run uses a unique per-run seed for supplier list ordering. Positional bias is controlled; see Section 3.1.

---

## 4. Results

> **Data requirement:** All `{{RESULT:...}}` placeholders require data from the N=50 pre-registered experiment (`buyerbench-pillar2-realistic-v1`). Values from the N=1 pilot or infrastructure validation runs (mock-agent-v1) must not be substituted.

> **Claim tiers (N.2):** Each subsection is labeled with its claim tier:
> - **[TIER-A]** Fully defensible: N≥50, BH-FDR corrected, confirmatory hypotheses only
> - **[TIER-B]** Suggestive: descriptive patterns, N=10 models, no p-values, hedged language required
> - **[TIER-C]** Speculative: future work only; must NOT appear in Results or Conclusions

### 4.1 Sample Quality and Descriptive Statistics [TIER-A: execution gate | TIER-B: per-model descriptives]

**Table 3. Experiment execution summary**

| Metric | Value |
|---|---|
| Total planned runs | 5,000 (10 models × 10 scenarios × 50 runs) |
| Total completed runs | `{{RESULT: n_total_runs}}` |
| Total valid runs (error_flag=False) | `{{RESULT: n_valid_runs}}` |
| Overall error rate | `{{RESULT: error_rate_pct}}`% |
| Models meeting 80% threshold (n_valid ≥ 40) | `{{RESULT: n_models_threshold_met}}`/10 |
| Mean runs per cell (valid) | `{{RESULT: mean_runs_per_cell}}` |
| Temperature | 0.7 |
| Supplier order randomization | Per-run seed (HMAC-SHA256) |

*Infrastructure verdict (Gate 1):* `{{RESULT: gate1_verdict}}` — proceed to confirmatory analysis if error rate < 5% and ≥2 models show mean BSI > 0.05 on at least one bias type.

**Table 4. Per-model descriptive statistics** [TIER-B — descriptive only]

| Model | n_valid_total | Mean BSI (all types) | BSI types > 0.10 | Included in aggregate |
|---|---|---|---|---|
| openai/gpt-4o | `{{RESULT: gpt4o_n}}` | `{{RESULT: gpt4o_mean_bsi}}` | `{{RESULT: gpt4o_n_sig_types}}` | `{{RESULT: gpt4o_included}}` |
| anthropic/claude-3.5-sonnet | `{{RESULT: claude_n}}` | `{{RESULT: claude_mean_bsi}}` | `{{RESULT: claude_n_sig_types}}` | `{{RESULT: claude_included}}` |
| google/gemini-pro-1.5 | `{{RESULT: gemini_n}}` | `{{RESULT: gemini_mean_bsi}}` | `{{RESULT: gemini_n_sig_types}}` | `{{RESULT: gemini_included}}` |
| meta-llama/llama-3.1-405b-instruct | `{{RESULT: llama_n}}` | `{{RESULT: llama_mean_bsi}}` | `{{RESULT: llama_n_sig_types}}` | `{{RESULT: llama_included}}` |
| mistralai/mistral-large | `{{RESULT: mistral_n}}` | `{{RESULT: mistral_mean_bsi}}` | `{{RESULT: mistral_n_sig_types}}` | `{{RESULT: mistral_included}}` |
| mistralai/mixtral-8x22b-instruct | `{{RESULT: mixtral_n}}` | `{{RESULT: mixtral_mean_bsi}}` | `{{RESULT: mixtral_n_sig_types}}` | `{{RESULT: mixtral_included}}` |
| deepseek/deepseek-chat | `{{RESULT: deepseek_n}}` | `{{RESULT: deepseek_mean_bsi}}` | `{{RESULT: deepseek_n_sig_types}}` | `{{RESULT: deepseek_included}}` |
| qwen/qwen-2.5-72b-instruct | `{{RESULT: qwen_n}}` | `{{RESULT: qwen_mean_bsi}}` | `{{RESULT: qwen_n_sig_types}}` | `{{RESULT: qwen_included}}` |
| cohere/command-r-plus | `{{RESULT: cohere_n}}` | `{{RESULT: cohere_mean_bsi}}` | `{{RESULT: cohere_n_sig_types}}` | `{{RESULT: cohere_included}}` |
| 01-ai/yi-large | `{{RESULT: yi_n}}` | `{{RESULT: yi_mean_bsi}}` | `{{RESULT: yi_n_sig_types}}` | `{{RESULT: yi_included}}` |

### 4.2 H1 — Bias Universality [TIER-A]

**Hypothesis:** LLM agents exhibit non-trivial bias susceptibility (BSI > 0.10 with 95% CI excluding zero) for at least one bias type in at least 5 of 10 tested models (BH-FDR q < 0.05).

**Table 5. Per-bias-type BSI estimates and H1 test results** (N=50 per cell; BH-FDR q=0.05)

| Bias Type | Mean BSI (95% CI) | t-statistic | p (raw) | p (BH-adj) | BH-significant |
|---|---|---|---|---|---|
| Anchoring | `{{RESULT: anchor_bsi_ci}}` | `{{RESULT: anchor_t}}` | `{{RESULT: anchor_p_raw}}` | `{{RESULT: anchor_p_bh}}` | `{{RESULT: anchor_sig}}` |
| Framing | `{{RESULT: framing_bsi_ci}}` | `{{RESULT: framing_t}}` | `{{RESULT: framing_p_raw}}` | `{{RESULT: framing_p_bh}}` | `{{RESULT: framing_sig}}` |
| Decoy | `{{RESULT: decoy_bsi_ci}}` | `{{RESULT: decoy_t}}` | `{{RESULT: decoy_p_raw}}` | `{{RESULT: decoy_p_bh}}` | `{{RESULT: decoy_sig}}` |
| Scarcity | `{{RESULT: scarcity_bsi_ci}}` | `{{RESULT: scarcity_t}}` | `{{RESULT: scarcity_p_raw}}` | `{{RESULT: scarcity_p_bh}}` | `{{RESULT: scarcity_sig}}` |
| Sunk Cost | `{{RESULT: sunk_bsi_ci}}` | `{{RESULT: sunk_t}}` | `{{RESULT: sunk_p_raw}}` | `{{RESULT: sunk_p_bh}}` | `{{RESULT: sunk_sig}}` |

**H1 verdict:** `{{RESULT: H1_verdict}}` — H1 is `{{RESULT: H1_confirmed_or_not_confirmed}}` at BH-FDR q=0.05. `{{RESULT: H1_n_models_sig}}` of 10 models show BSI > 0.10 on at least one bias type.

*If H1 is not confirmed (BSI ≈ 0 across all bias types at N=50):* The primary finding is "domain structure (explicit scoring rubrics, constrained supplier comparison) suppresses behavioral bias susceptibility in LLM procurement agents." This outcome is pre-specified as a valid scientific contribution; see Section 5.1 for the "robust rationality" framing.

### 4.3 H3 — Decoy Effect Reliability and H5 — Framing Asymmetry [TIER-A]

**H3:** The decoy bias type produces BSI > 0 and BSI higher than the cross-bias mean.

**Table 6. H3 Decoy reliability test**

| Test | Statistic | p-value | Result |
|---|---|---|---|
| Decoy BSI > 0 (one-sample t) | t = `{{RESULT: h3_onesample_t}}` | `{{RESULT: h3_onesample_p}}` | `{{RESULT: h3_onesample_result}}` |
| Decoy BSI > cross-bias mean (Dunnett) | d = `{{RESULT: h3_dunnett_d}}` | `{{RESULT: h3_dunnett_p}}` | `{{RESULT: h3_dunnett_result}}` |

**H3 verdict:** `{{RESULT: H3_verdict}}`

**H5:** The LOSS frame produces higher BSI than the GAIN frame across models, consistent with loss aversion.

**Table 7. H5 Framing asymmetry test**

| Frame | Mean BSI (95% CI) | Δ (LOSS − GAIN) | Paired t | p-value | H5 result |
|---|---|---|---|---|---|
| FRAMING_GAIN | `{{RESULT: gain_bsi_ci}}` | — | — | — | — |
| FRAMING_LOSS | `{{RESULT: loss_bsi_ci}}` | `{{RESULT: h5_delta}}` | t = `{{RESULT: h5_t}}` | `{{RESULT: h5_p}}` | `{{RESULT: H5_verdict}}` |

### 4.4 H7 — Stochastic Variance Structure [TIER-A]

**Hypothesis:** Within-cell standard deviation (`std_bsi`) is positively correlated with mean BSI across cells, consistent with a decision-boundary mechanism where biased agents hover near a supplier-switching threshold.

**OLS regression:** $\hat{\sigma}_{\text{cell}} = \hat{\beta}_0 + \hat{\beta}_1 \cdot \widehat{\text{BSI}}_{\text{cell}}$

| Coefficient | Estimate | SE | t | p |
|---|---|---|---|---|
| $\hat{\beta}_0$ (intercept) | `{{RESULT: h7_b0}}` | `{{RESULT: h7_b0_se}}` | `{{RESULT: h7_b0_t}}` | `{{RESULT: h7_b0_p}}` |
| $\hat{\beta}_1$ (mean BSI) | `{{RESULT: h7_b1}}` | `{{RESULT: h7_b1_se}}` | `{{RESULT: h7_b1_t}}` | `{{RESULT: h7_b1_p}}` |
| $R^2$ | `{{RESULT: h7_r2}}` | | | |

**H7 verdict:** `{{RESULT: H7_verdict}}` — $\hat{\beta}_1$ is `{{RESULT: H7_sign_description}}`. The proportion of BSI variance attributable to systematic vs. stochastic sources is: η²_systematic = `{{RESULT: eta2_systematic}}`, η²_residual = `{{RESULT: eta2_residual}}`.

*If η²_residual > 0.70:* "Within-cell stochastic variance accounts for the majority of observed BSI variation. Reported mean BSI estimates carry wide uncertainty; results should be interpreted cautiously as exploratory even at N=50."

### 4.5 Primary Regression and Variance Decomposition [TIER-A]

**Level 1 WLS regression results** (cell-level; weights = n_valid_runs; HC3 clustered SE at model level):

| Predictor | Coefficient | Clustered SE | t | p |
|---|---|---|---|---|
| Treatment | `{{RESULT: reg_treat_coef}}` | `{{RESULT: reg_treat_se}}` | `{{RESULT: reg_treat_t}}` | `{{RESULT: reg_treat_p}}` |
| BiasType: Anchoring (ref: Decoy) | `{{RESULT: reg_anchor_coef}}` | `{{RESULT: reg_anchor_se}}` | `{{RESULT: reg_anchor_t}}` | `{{RESULT: reg_anchor_p}}` |
| BiasType: Framing | `{{RESULT: reg_frame_coef}}` | `{{RESULT: reg_frame_se}}` | `{{RESULT: reg_frame_t}}` | `{{RESULT: reg_frame_p}}` |
| BiasType: Scarcity | `{{RESULT: reg_scar_coef}}` | `{{RESULT: reg_scar_se}}` | `{{RESULT: reg_scar_t}}` | `{{RESULT: reg_scar_p}}` |
| BiasType: Sunk Cost | `{{RESULT: reg_sunk_coef}}` | `{{RESULT: reg_sunk_se}}` | `{{RESULT: reg_sunk_t}}` | `{{RESULT: reg_sunk_p}}` |
| Intercept | `{{RESULT: reg_int_coef}}` | `{{RESULT: reg_int_se}}` | `{{RESULT: reg_int_t}}` | `{{RESULT: reg_int_p}}` |
| $R^2$ | `{{RESULT: reg_r2}}` | N cells = `{{RESULT: reg_n_cells}}` | | |

**Variance decomposition (ANOVA-style SS partition):**

| Source | SS | η² | Interpretation |
|---|---|---|---|
| Model | `{{RESULT: ss_model}}` | `{{RESULT: eta2_model}}` | Cross-model BSI variance |
| BiasType | `{{RESULT: ss_biastype}}` | `{{RESULT: eta2_biastype}}` | Bias-type BSI variance |
| Treatment | `{{RESULT: ss_treatment}}` | `{{RESULT: eta2_treatment}}` | Treatment-condition variance |
| Residual | `{{RESULT: ss_residual}}` | `{{RESULT: eta2_res}}` | Stochastic + unexplained |

### 4.6 Exploratory Cross-Model Patterns [TIER-B]

> **Note [TIER-B]:** The following analyses involve N=10 model-level observations. OLS coefficients and standard errors are reported for descriptive purposes only. No p-values on cross-model comparisons should be interpreted as inferential evidence. The phrase "significantly" is used here in the colloquial (not statistical) sense. All claims in this subsection must be hedged with "descriptive pattern, N=10."

**Figure 1: BSI Heatmap** (model × bias type). `{{RESULT: heatmap_figure_path}}` — `{{RESULT: heatmap_description}}`

**H2 (Capability-Bias Tradeoff) — descriptive:** Spearman rank correlation between Pillar 1 composite score and mean BSI across 10 models: ρ = `{{RESULT: h2_rho}}`. [TIER-B] This descriptive pattern is consistent with / not consistent with `{{RESULT: h2_direction_description}}`. As noted in Section 2.2, both a negative (higher capability → less bias) and positive (higher capability → more bias, per @hagendorff2023human) correlation are theoretically motivated; neither direction constitutes a pre-specified confirmatory prediction.

**H9 (Bias Profiles) — descriptive:** Cronbach's α on the 5-dimension BSI vector across 10 models: α = `{{RESULT: h9_alpha}}`. [TIER-B] A value `{{RESULT: h9_alpha_interpretation}}` (< 0.50 suggests bias-specific rather than general susceptibility; > 0.70 suggests a general susceptibility factor). `{{RESULT: h9_cluster_description}}`

### 4.7 Robustness Checks

**Prompt sensitivity (REV-5):** [TIER-A: pre-specified gate — go/no-go criterion, not an interpretive claim] `{{RESULT: prompt_cv_table}}` — Overall verdict: `{{RESULT: prompt_rev5_verdict}}`. Scenarios flagged for CV > 0.50: `{{RESULT: flagged_scenarios_list}}`.

**Temperature robustness (T=0.0):** At T=0.0, mean BSI across all cells: `{{RESULT: T0_mean_bsi}}` (vs. T=0.7: `{{RESULT: T07_mean_bsi}}`). [TIER-B] This `{{RESULT: T0_verdict_description}}` (is consistent with / contradicts) the primary T=0.7 findings. `{{RESULT: T0_qualification_if_needed}}`

**Human benchmark calibration (H10) — descriptive:** Human meta-analytic benchmarks (external literature) vs. BuyerBench LLM estimates [TIER-B]:

| Bias Type | Human d (meta-analytic) | LLM BSI (this study) | LLM d (approx.) | Comparison |
|---|---|---|---|---|
| Anchoring | ≈ 2.7 [@kahneman1974judgment] | `{{RESULT: anchor_bsi}}` | `{{RESULT: anchor_d}}` | `{{RESULT: anchor_human_comparison}}` |
| Framing | ≈ 1.8 [@tversky1981framing] | `{{RESULT: framing_bsi}}` | `{{RESULT: framing_d}}` | `{{RESULT: framing_human_comparison}}` |
| Decoy | ≈ 0.4 [@huber1982adding] | `{{RESULT: decoy_bsi}}` | `{{RESULT: decoy_d}}` | `{{RESULT: decoy_human_comparison}}` |
| Scarcity | ≈ 0.60–0.80 [@cialdini1984influence] | `{{RESULT: scarcity_bsi}}` | `{{RESULT: scarcity_d}}` | `{{RESULT: scarcity_human_comparison}}` |
| Sunk Cost | ≈ 0.85 [@arkes1985psychology] | `{{RESULT: sunk_bsi}}` | `{{RESULT: sunk_d}}` | `{{RESULT: sunk_human_comparison}}` |

*Note: LLM Cohen's d is approximated from BSI estimates under the assumption that BSI ≈ P(bias-susceptible response). Direct comparison to human d requires a common scaling assumption; this comparison is illustrative and does not constitute a formal test. A human comparison arm (Phase 4, IRB pending) will enable a proper between-group Welch t-test.*

### 4.8 Hard-Difficulty Ceiling Scenarios (p2-09 through p2-11) [TIER-B]

> **Data requirement:** Results from hard-difficulty scenarios (p2-09 compound, p2-10 anchor-hard, p2-11 scarcity-hard) require the same N=50 pre-registered experiment. These scenarios were added per REV-4 (ceiling effect mitigation) and are reported separately from the primary confirmatory analysis. All values are `{{RESULT:...}}` placeholders.

*These scenarios are not part of the pre-registered confirmatory battery (B.9); their results are exploratory.*

| Scenario | Bias Type | n_suppliers | δ | Mean BSI (T=0.7, N=50) | 95% CI | Compared to Primary |
|---|---|---|---|---|---|---|
| p2-09 (compound) | Anchor + Scarcity | 6 | 0.031 | `{{RESULT: p209_bsi}}` | `{{RESULT: p209_ci}}` | `{{RESULT: p209_vs_primary}}` |
| p2-10 (anchor-hard) | Anchoring | 7 | 0.039 | `{{RESULT: p210_bsi}}` | `{{RESULT: p210_ci}}` | `{{RESULT: p210_vs_primary}}` |
| p2-11 (scarcity-hard) | Scarcity | 8 | 0.005 | `{{RESULT: p211_bsi}}` | `{{RESULT: p211_ci}}` | `{{RESULT: p211_vs_primary}}` |

**Ceiling-effect verdict:** `{{RESULT: ceiling_gate_verdict}}` (Gate criterion: ≥7/10 models show mean BSI < 0.05 on all primary bias types → trigger hard-scenario pivot). `{{RESULT: ceiling_gate_description}}`

*Ceiling-effect detection pipeline implemented in `research/analysis/ceiling_effect.py` (`detect_ceiling_effect()`, `gate1_decision()`). Analysis script: `research/scripts/03_analyze_ceiling_effect.py`.*

---

## References

<!-- References in BibTeX format are in docs/paper/references.bib. Selected inline citations below for working paper readability. -->

Arkes, H. R., & Blumer, C. (1985). The psychology of sunk cost. *Organizational Behavior and Human Decision Processes*, 35(1), 124–140.

Benjamini, Y., & Hochberg, Y. (1995). Controlling the false discovery rate. *Journal of the Royal Statistical Society B*, 57(1), 289–300.

Binz, M., & Schulz, E. (2023). Using cognitive psychology to understand GPT-3. *PNAS*, 120(6).

BuyerBench Research Team. (2026). *BuyerBench: A Multi-Dimensional Benchmark for Evaluating AI Buyer Agents*. Working paper.

Camerer, C. F., & Hogarth, R. M. (1999). The effects of financial incentives in experiments. *Journal of Risk and Uncertainty*, 19(1–3), 7–42.

Cialdini, R. B. (1984). *Influence: The Psychology of Persuasion*. Harper & Row.

Echterhoff, J. M., Liu, Y., Alessa, A., McAuley, J., & He, Z. (2024). Cognitive bias in high-stakes decision-making with LLMs. *arXiv:2403.00811*.

Greenwald, A. G. (1976). Within-subjects designs: To use or not to use? *Psychological Bulletin*, 83(2), 314–320.

Hagendorff, T., Fabi, S., & Kosinski, M. (2023). Human-like intuitive behavior and reasoning biases emerged in large language models. *Nature Human Behaviour*, 7, 1768–1780.

Huber, J., Payne, J. W., & Puto, C. (1982). Adding asymmetrically dominated alternatives: Violations of regularity and the similarity hypothesis. *Journal of Consumer Research*, 9(1), 90–98.

Kahneman, D., & Tversky, A. (1974). Judgment under uncertainty: Heuristics and biases. *Science*, 185(4157), 1124–1131.

Kahneman, D., & Tversky, A. (1979). Prospect theory: An analysis of decision under risk. *Econometrica*, 47(2), 263–291.

Loken, E., & Gelman, A. (2017). Measurement error and the replication crisis. *Science*, 355(6325), 584–585.

Liu, X., et al. (2023). AgentBench: Evaluating LLMs as agents. *arXiv:2308.03688*.

Mialon, G., et al. (2023). GAIA: A benchmark for general AI assistants. *arXiv:2311.12983*.

Open Science Collaboration. (2015). Estimating the reproducibility of psychological science. *Science*, 349(6251), aac4716.

Scherrer, N., et al. (2024). Evaluating the moral beliefs encoded in LLMs. *arXiv:2307.14324*.

Simmons, J. P., Nelson, L. D., & Simonsohn, U. (2011). False-positive psychology. *Psychological Science*, 22(11), 1359–1366.

Simonson, I. (1989). Choice based on reasons: The case of attraction and compromise effects. *Journal of Consumer Research*, 16(2), 158–174.

Thaler, R. H. (1980). Toward a positive theory of consumer choice. *Journal of Economic Behavior and Organization*, 1(1), 39–60.

Tjuatja, L., et al. (2024). Do LLMs exhibit human-like response biases? *arXiv:2311.04076*.

Tversky, A., & Kahneman, D. (1981). The framing of decisions and the psychology of choice. *Science*, 211(4481), 453–458.

Worchel, S., Lee, J., & Adewole, A. (1975). Effects of supply and demand on ratings of object value. *Journal of Personality and Social Psychology*, 32(5), 906–914.

---

## Appendix A — Pre-Registration Deviations

*To be completed after data collection. Document any deviations from OSF pre-registration (`buyerbench-pillar2-realistic-v1`) here, with justification.*

| Deviation | Section Affected | Reason | Direction (conservative/liberal) |
|---|---|---|---|
| (none at time of working paper draft) | — | — | — |

---

## Appendix B — Pre-Registration Document

> This appendix reproduces the key content of OSF pre-registration `buyerbench-pillar2-realistic-v1`. The full machine-generated document is available at `docs/preregistration/prereg_osf.md` in the BuyerBench repository and at [OSF link TBD — register before data collection]. In the event of any conflict between this appendix and the OSF document, the OSF document takes precedence.

### B.1 Registration Metadata

| Field | Value |
|---|---|
| Experiment ID | `buyerbench-pillar2-realistic-v1` |
| Pre-registration date | [TBD — must precede first data collection run] |
| OSF URL | [TBD] |
| Codebase commit at registration | [TBD — pin with `git rev-parse HEAD` before running] |
| Registered by | BuyerBench Research Team |

### B.2 Primary Research Question

> Does the behavioral bias susceptibility of LLM-based agents — measured as deviation from economically optimal choices under controlled presentation manipulations — vary systematically across model capability tiers, bias types, and experimental conditions, in ways analogous to, attenuated relative to, or amplified compared to documented human behavioral patterns?

### B.3 Study Design

**Study type:** Controlled computational experiment. Each scenario pair consists of a BASELINE condition and a TREATMENT condition in which a single behavioral manipulation is introduced. All other economic parameters are held constant across conditions. The design is between-condition (each agent–scenario pair is assigned to one condition per run) with N repeated runs per cell.

**Blinding:** LLM agents receive no meta-information about the experimental design, bias types being tested, or BuyerBench framework. Agents see only the scenario prompt. No human rater blinding is required for the primary LLM experiment.

**Within-participant elements:** Each model is evaluated on all scenarios (within-agent design across bias types and variants). Analysis accounts for this with clustered standard errors at the agent level.

**Randomization:** Supplier order is randomized per run using a per-run seed (`supplier_order_seed = HMAC-SHA256(base_seed, scenario_id|variant|run_index)` folded to [0, 2³¹)). Seeds are stored in run metadata for exact replayability.

### B.4 Sampling Plan

| Parameter | Value |
|---|---|
| Models | 10 LLM agents via OpenRouter API (see B.8) |
| Scenarios | 10 YAML files (5 bias type batteries × BASELINE + TREATMENT) |
| Runs per cell | N = 50 independent, stateless API calls |
| Temperature (primary) | 0.7 |
| Prompt version (primary) | `standard` |
| Total planned runs | 5,000 |
| Power justification | N=50 achieves ≥70% power for d=0.4 and ≥80% power for d≥0.5 (one-sided t-test, α=0.05) |
| Stopping rule | Fixed N; no data-dependent stopping. Models exceeding 20% failure rate are paused and resumed; partial runs included if n_valid ≥ 40. |

### B.5 Variables

**Manipulated variables:**
- `variant` (categorical): BASELINE vs. TREATMENT within each bias type battery
- `agent_id` (categorical): 10 OpenRouter LLM agents
- `bias_category` (categorical): anchoring, framing, decoy, scarcity, sunk_cost
- `supplier_order_seed` (integer): per-run seed controlling positional bias

**Primary outcome:** Cell-level Bias Susceptibility Index (BSI), estimated from N=50 independent runs per (agent × scenario × variant) cell. At the run level: BSI = int(decision\_changed) × (1 − baseline\_score). At the cell level: mean of N run-level BSI values with 95% t-interval.

**Secondary outcomes:** Within-cell BSI variance (std\_bsi); optimality gap; choice rate distribution; model-level 5-dimension BSI vector; reasoning trace length (token count).

### B.6 Analysis Plan

**Confirmatory tests (BH-FDR correction at q=0.05):**

- *H1 (Bias Universality):* One-sample t-test per bias type (H₀: BSI = 0). Test family: 5 bias types × 10 models = 50 tests.
- *H3 (Decoy Reliability):* One-sample t-test (decoy BSI > 0) + Dunnett's test vs. cross-bias mean.
- *H5 (Framing Asymmetry):* Paired t-test: BSI_LOSS > BSI_GAIN across models.
- *H7 (Stochastic Variance):* OLS: std_bsi ~ β₀ + β₁·mean_bsi. Significant positive β₁ confirms H7.

**Primary regression (Level 1 WLS):** Cell-level WLS with weights = n_valid_runs; HC3 clustered SEs at model level.

**Variance decomposition:** ANOVA-style SS partition (Model, BiasType, Treatment, Residual) with η² effect sizes.

**Exploratory analyses (descriptive only; no inferential claims):** H2 (Capability-Bias correlation); H8 (CoT × Bias interaction); H9 (Bias Profile Cronbach's α); H10 (Human benchmark comparison). All cross-model analyses (N=10) are descriptive; no p-values for cross-model comparisons.

**Inference criteria:** α = 0.05; BH-FDR at q = 0.05 for confirmatory tests only.

**Data exclusion:** Runs with error_flag=True excluded from BSI computation. Models with <80% valid runs (n_valid < 40) flagged and excluded from aggregate analyses.

**Null result pre-specification:** If BH-FDR-corrected tests fail to reject H₀: BSI = 0 for ≥3 of 5 bias types, the primary finding is: "Domain structure suppresses behavioral bias susceptibility in LLM procurement agents." This is a valid scientific contribution, not a failed study.

### B.7 Pre-Specified Hypothesis Summary

| ID | Statement (condensed) | Direction | Analysis Type | Test |
|---|---|---|---|---|
| H1 | ≥5/10 models show BSI > 0.10 on ≥1 bias type (BH-FDR q < 0.05) | positive | **CONFIRMATORY** | One-sample t per bias type |
| H2 | Negative Spearman ρ between Pillar 1 score and mean BSI across models | negative | exploratory | Spearman ρ (N=10, descriptive) |
| H3 | Decoy BSI > 0 and > cross-bias mean BSI | positive | **CONFIRMATORY** | One-sample t + Dunnett contrast |
| H4 | BSI_ANCHOR_HIGH > BSI_ANCHOR_LOW (not yet implemented: p2-01b missing) | positive | exploratory | Paired t (pending p2-01b) |
| H5 | BSI_LOSS > BSI_GAIN across models (loss aversion prediction) | positive | **CONFIRMATORY** | Paired t (LOSS vs. GAIN) |
| H6 | Sunk cost BSI positively correlated with capability (non-monotone; opposite H2) | positive | exploratory | Spearman ρ for p2-05 specifically |
| H7 | std_bsi positively correlated with mean_bsi across cells (boundary mechanism) | positive | **CONFIRMATORY** | OLS: std_bsi ~ β₁·mean_bsi |
| H8 | CoT reduces anchoring but not decoy BSI (interaction) | non-directional | exploratory | 2×2 ANOVA: BSI ~ bias_type × prompt_version |
| H9 | Cronbach's α < 0.50 on 5D BSI vector across models (bias-specific patterns) | null | exploratory | Cronbach's α + hierarchical clustering |
| H10 | LLM BSI effect sizes smaller than human meta-analytic d (attenuation) | negative | exploratory | Cohen's d comparison vs. published baselines |

*Bold = confirmatory (BH-FDR correction applies). Italic = exploratory (descriptive only; no p-value claims permitted).*

### B.8 Registered Model Set

No post-hoc model additions are permitted. Models may be excluded if they exceed the 20% failure threshold (see Section B.6).

| # | Model ID | Provider |
|---|---|---|
| 1 | `openai/gpt-4o` | OpenAI |
| 2 | `anthropic/claude-3.5-sonnet` | Anthropic |
| 3 | `google/gemini-pro-1.5` | Google |
| 4 | `meta-llama/llama-3.1-405b-instruct` | Meta |
| 5 | `mistralai/mistral-large` | Mistral AI |
| 6 | `mistralai/mixtral-8x22b-instruct` | Mistral AI |
| 7 | `deepseek/deepseek-chat` | DeepSeek |
| 8 | `qwen/qwen-2.5-72b-instruct` | Alibaba |
| 9 | `cohere/command-r-plus` | Cohere |
| 10 | `01-ai/yi-large` | 01.AI |

### B.9 Registered Bias Type Battery

No post-hoc additions to the primary confirmatory analysis are permitted.

| Bias Type | Scenario ID | Confirmatory Hypothesis |
|---|---|---|
| anchoring | p2-01 | H1 |
| framing | p2-02 | H1, H5 |
| decoy | p2-03 | H1, H3 |
| scarcity | p2-04 | H1 |
| sunk_cost | p2-05 | H1 |

### B.10 Open Science Statement

BuyerBench is open-source (MIT License). All scenario definitions, evaluation code, raw run records (excluding any API credentials), and analysis scripts will be made publicly available at the time of paper submission. Pre-registration predates any data collection. Deviations from this pre-registration, if any, are documented in Appendix A.

---

## Appendix C — Scenario YAML Metadata

*Full scenario definitions available in `scenarios/` directory of the BuyerBench repository. Key fields reproduced here for reproducibility.*

| Scenario ID | Evaluation Weights (cost / quality / delivery) | n_suppliers | δ (optimal gap) |
|---|---|---|---|
| p2-01-anchor-high-BASELINE | 0.40 / 0.40 / 0.20 | 3 | 0.08–0.15 |
| p2-01-anchor-high-ANCHOR_HIGH | 0.40 / 0.40 / 0.20 | 3 | 0.08–0.15 |
| p2-02-framing-GAIN | 0.40 / 0.40 / 0.20 | 3 | 0.06–0.12 |
| p2-02-framing-LOSS | 0.40 / 0.40 / 0.20 | 3 | 0.06–0.12 |
| p2-03-decoy-BASELINE | 0.40 / 0.40 / 0.20 | 3 | 0.08–0.15 |
| p2-03-decoy-DECOY | 0.40 / 0.40 / 0.20 | 4 | 0.08–0.15 |
| p2-04-scarcity-BASELINE | 0.40 / 0.40 / 0.20 | 3 | 0.08–0.15 |
| p2-04-scarcity-SCARCITY | 0.40 / 0.40 / 0.20 | 3 | 0.08–0.15 |
| p2-05-sunk-cost-BASELINE | 0.40 / 0.40 / 0.20 | 3 | 0.08–0.15 |
| p2-05-sunk-cost-SUNK_COST | 0.40 / 0.40 / 0.20 | 3 | 0.08–0.15 |
| p2-09-compound-BASELINE | 0.40 / 0.40 / 0.20 | 6 | 0.031 |
| p2-09-compound-COMPOUND | 0.40 / 0.40 / 0.20 | 6 | 0.031 |
| p2-10-anchor-hard-BASELINE | 0.40 / 0.40 / 0.20 | 7 | 0.039 |
| p2-10-anchor-hard-ANCHOR_HIGH | 0.40 / 0.40 / 0.20 | 7 | 0.039 |
| p2-11-scarcity-hard-BASELINE | 0.40 / 0.40 / 0.20 | 8 | 0.005 |
| p2-11-scarcity-hard-SCARCITY | 0.40 / 0.40 / 0.20 | 8 | 0.005 |

---

## Appendix D — Robustness Checks

This appendix reports all pre-specified robustness checks described in Section 3.5. Each check addresses a specific threat to internal validity. A finding is considered robust if it survives all three checks; a finding that collapses on any check must be qualified in the main text.

---

### D.1 Prompt Sensitivity (REV-5)

**Threat:** BSI values may be a property of the specific prompt wording chosen by the researcher rather than a genuine property of the model's decision-making. Minor synonym substitutions should not substantially change BSI if the bias effect is real.

**Protocol:** Three prompt phrasings were evaluated per scenario pair in a 5-run pilot prior to the main experiment (design tier: `pilot`; model: `mock-agent-v1` for infrastructure validation; real-model pilot uses the same three phrasings on a selected frontier model). Phrasings differ only in the system preamble:

| Label | Phrasing Description | Key Substitutions |
|---|---|---|
| `robustness_a` | Control — identical to `standard` phrasing | (none; serves as anchor) |
| `robustness_b` | Synonym substitution A | "best" → "optimal"; otherwise unchanged |
| `robustness_c` | Synonym substitution B | "Your task is to act as" → "Your role is to serve as"; "best" → "most appropriate"; "determine" → "make" |

All three phrasings preserve the JSON output instruction for parseability.

**Gate criterion (REV-5):** Coefficient of variation (CV = std\_BSI / mean\_BSI) across three phrasings per scenario pair. CV > 0.50 triggers **REDESIGN** — the scenario is excluded from confirmatory analysis pending scenario revision. CV ≤ 0.20 = low sensitivity; 0.20–0.50 = moderate (proceed with qualification); > 0.50 = high (REDESIGN).

**Results** (requires real-model REV-5 pilot data; mock pilot confirms infrastructure only):

| Scenario Pair | Bias Type | BSI (Phrasing A) | BSI (Phrasing B) | BSI (Phrasing C) | CV | Gate |
|---|---|---|---|---|---|---|
| p2-01 | Anchoring | `{{RESULT: p201_bsiA}}` | `{{RESULT: p201_bsiB}}` | `{{RESULT: p201_bsiC}}` | `{{RESULT: p201_cv}}` | `{{RESULT: p201_gate}}` |
| p2-02 | Framing | `{{RESULT: p202_bsiA}}` | `{{RESULT: p202_bsiB}}` | `{{RESULT: p202_bsiC}}` | `{{RESULT: p202_cv}}` | `{{RESULT: p202_gate}}` |
| p2-03 | Decoy | `{{RESULT: p203_bsiA}}` | `{{RESULT: p203_bsiB}}` | `{{RESULT: p203_bsiC}}` | `{{RESULT: p203_cv}}` | `{{RESULT: p203_gate}}` |
| p2-04 | Scarcity | `{{RESULT: p204_bsiA}}` | `{{RESULT: p204_bsiB}}` | `{{RESULT: p204_bsiC}}` | `{{RESULT: p204_cv}}` | `{{RESULT: p204_gate}}` |
| p2-05 | Sunk Cost | `{{RESULT: p205_bsiA}}` | `{{RESULT: p205_bsiB}}` | `{{RESULT: p205_bsiC}}` | `{{RESULT: p205_cv}}` | `{{RESULT: p205_gate}}` |

**Overall REV-5 verdict:** `{{RESULT: rev5_overall_verdict}}` — `{{RESULT: rev5_n_redesign}}` of 5 scenario pairs triggered REDESIGN gate. `{{RESULT: rev5_qualification_if_any}}`

*REV-5 robustness check is implemented in `harness/robustness_pilot.py` (`run_robustness_pilot()`) and the `compute_prompt_sensitivity()` function in `evaluators/pillar2.py`. Results are written to `results/robustness-pilot/robustness_pilot.json`.*

---

### D.2 Temperature Robustness (T=0.0 Pass)

**Threat:** BSI estimates at T=0.7 may reflect stochastic sampling noise rather than genuine bias susceptibility. At T=0.0 (deterministic decoding), each run is identical within a session; if BSI persists at T=0.0, the finding is not attributable to sampling variance.

**Protocol:** Secondary experiment at T=0.0, N=30 per cell (design tier: `robustness_t0`; 3,000 total runs across 10 models). The T=0.0 pass is run after Gate 1 clearance using `research/scripts/05_run_robustness_t0.py`.

**Interpretation rules:**
- If T=0.0 BSI ≈ T=0.7 BSI: finding is temperature-robust; no qualification needed.
- If T=0.0 BSI ≈ 0 but T=0.7 BSI > 0: finding is temperature-sensitive ("bias only emerges under stochastic sampling"); must be qualified in main text and Abstract.
- If T=0.0 BSI > T=0.7 BSI: BSI is amplified under determinism; note as an unexpected direction and investigate.

**Results** (requires `ROBUSTNESS_T0_DESIGN` experiment; mock infrastructure pass confirmed):

| Bias Type | Mean BSI (T=0.7, N=50) | Mean BSI (T=0.0, N=30) | Δ (T=0.7 − T=0.0) | Temperature-robust? |
|---|---|---|---|---|
| Anchoring | `{{RESULT: anchor_bsi_t07}}` | `{{RESULT: anchor_bsi_t00}}` | `{{RESULT: anchor_delta_t}}` | `{{RESULT: anchor_t_robust}}` |
| Framing | `{{RESULT: framing_bsi_t07}}` | `{{RESULT: framing_bsi_t00}}` | `{{RESULT: framing_delta_t}}` | `{{RESULT: framing_t_robust}}` |
| Decoy | `{{RESULT: decoy_bsi_t07}}` | `{{RESULT: decoy_bsi_t00}}` | `{{RESULT: decoy_delta_t}}` | `{{RESULT: decoy_t_robust}}` |
| Scarcity | `{{RESULT: scarcity_bsi_t07}}` | `{{RESULT: scarcity_bsi_t00}}` | `{{RESULT: scarcity_delta_t}}` | `{{RESULT: scarcity_t_robust}}` |
| Sunk Cost | `{{RESULT: sunk_bsi_t07}}` | `{{RESULT: sunk_bsi_t00}}` | `{{RESULT: sunk_delta_t}}` | `{{RESULT: sunk_t_robust}}` |
| **Grand mean** | `{{RESULT: grand_bsi_t07}}` | `{{RESULT: grand_bsi_t00}}` | `{{RESULT: grand_delta_t}}` | `{{RESULT: grand_t_robust}}` |

**T=0.0 verdict:** `{{RESULT: t0_overall_verdict}}` — `{{RESULT: t0_qualification_statement}}`

*T=0.0 robustness pass is implemented in `research/scripts/05_run_robustness_t0.py`. Results are written to `results/experiments/pillar2-robustness_t0-{timestamp}/`.*

---

### D.3 CoT Prompt Variant Analysis (UPGRADE-7)

**Threat:** The `standard` prompt version (no explicit reasoning instruction) may suppress deliberate evaluation, making models more susceptible to superficial bias cues. Chain-of-thought (CoT) prompting may attenuate bias effects by forcing explicit step-by-step reasoning. If CoT substantially reduces BSI, the `standard` results characterize LLMs under *minimal deliberation* — a valid but scoped finding.

**Protocol:** Three prompt versions evaluated at N=15 per cell (design tier: `cot_experiment`; 4,500 total runs). Prompt versions:

| Version | Preamble Addition |
|---|---|
| `standard` | Standard system preamble (no reasoning instruction) |
| `cot` | "Think step by step through each option before making your final decision." (prepended) |
| `expert_role` | "You are a senior procurement officer with 15 years of experience evaluating suppliers for enterprise clients." (prepended) |

**Results** (requires `COT_EXPERIMENT_DESIGN` run; mock infrastructure pass confirmed):

| Bias Type | BSI (standard) | BSI (cot) | BSI (expert_role) | Δ (cot − standard) | Δ (expert − standard) |
|---|---|---|---|---|---|
| Anchoring | `{{RESULT: anchor_std}}` | `{{RESULT: anchor_cot}}` | `{{RESULT: anchor_exp}}` | `{{RESULT: anchor_cot_delta}}` | `{{RESULT: anchor_exp_delta}}` |
| Framing | `{{RESULT: framing_std}}` | `{{RESULT: framing_cot}}` | `{{RESULT: framing_exp}}` | `{{RESULT: framing_cot_delta}}` | `{{RESULT: framing_exp_delta}}` |
| Decoy | `{{RESULT: decoy_std}}` | `{{RESULT: decoy_cot}}` | `{{RESULT: decoy_exp}}` | `{{RESULT: decoy_cot_delta}}` | `{{RESULT: decoy_exp_delta}}` |
| Scarcity | `{{RESULT: scarcity_std}}` | `{{RESULT: scarcity_cot}}` | `{{RESULT: scarcity_exp}}` | `{{RESULT: scarcity_cot_delta}}` | `{{RESULT: scarcity_exp_delta}}` |
| Sunk Cost | `{{RESULT: sunk_std}}` | `{{RESULT: sunk_cot}}` | `{{RESULT: sunk_exp}}` | `{{RESULT: sunk_cot_delta}}` | `{{RESULT: sunk_exp_delta}}` |

**H8 test (exploratory):** 2×2 ANOVA (anchoring × decoy × standard/cot prompt version). Key interaction contrast: Δ(decoy CoT − decoy standard) vs. Δ(anchor CoT − anchor standard). Verdict: `{{RESULT: H8_anova_verdict}}`. *This analysis is exploratory (H8 is not confirmatory); no inferential claims are warranted.*

*CoT experiment is implemented in `research/scripts/06_run_cot_experiment.py`. Results are written to `results/experiments/pillar2-cot_experiment-{timestamp}/`.*

---

### D.4 Supplier Order Stability

**Threat:** Models may exhibit positional bias — preferring the first or last supplier listed regardless of attributes. If supplier order is correlated with the optimal supplier's position, positional bias inflates apparent rationality.

**Protocol:** Each run uses a unique per-run seed for supplier list ordering, derived as `HMAC-SHA256(base_seed, "scenario_id|variant|run_index")` folded to [0, 2³¹). This ensures that across N=50 runs per cell, each supplier appears in each list position approximately equally often. The seed is stored in run metadata (`supplier_order_seed`) enabling exact replayability.

**Verification:** Across all cells in the primary experiment, the optimal supplier occupies each list position (1st, 2nd, ..., nth) with approximately equal frequency: `{{RESULT: supplier_position_distribution}}`. The correlation between choice_is_correct and supplier_position is: r = `{{RESULT: position_choice_correlation}}` (expected ≈ 0 if positional bias is absent).

*Supplier order randomization is implemented in `harness/runner.py` (`derive_seed()` function). The `--supplier-order-seed` and `--supplier-order-static` CLI flags enable reproducibility and controlled comparisons.*

---

## Appendix E — Registered Model Versions

*To be completed at experiment execution time. Model versions are pinned in `experiment_manifest.json` (`experiment_id: buyerbench-pillar2-realistic-v1`). Any model version drift between experiment sessions will be documented here.*

| Model ID | Registered Version | Actual Version (at run time) | Version Drift Flag |
|---|---|---|---|
| openai/gpt-4o | (registered at experiment start) | `{{RESULT: gpt4o_actual_version}}` | `{{RESULT: gpt4o_drift}}` |
| anthropic/claude-3.5-sonnet | (registered at experiment start) | `{{RESULT: claude_actual_version}}` | `{{RESULT: claude_drift}}` |
| google/gemini-pro-1.5 | (registered at experiment start) | `{{RESULT: gemini_actual_version}}` | `{{RESULT: gemini_drift}}` |
| (remaining 7 models) | (registered at experiment start) | `{{RESULT: remaining_versions}}` | `{{RESULT: remaining_drift}}` |
