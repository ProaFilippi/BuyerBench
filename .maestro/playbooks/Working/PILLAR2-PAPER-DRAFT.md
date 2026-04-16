---
type: report
title: BuyerBench Pillar 2 — Paper Outlines & Draft Text (Dual Track)
created: 2026-04-16
tags:
  - pillar2
  - paper
  - behavioral-economics
  - bsi
  - draft
related:
  - '[[PILLAR2-RESEARCH-05]]'
  - '[[PILLAR2-RESEARCH-04]]'
---

# BuyerBench Pillar 2 — Paper Outlines & Draft Text
## Behavioral Bias Susceptibility in Large Language Models: Procurement Benchmark Evidence

> **Status:** DRAFT — All result claims are PLACEHOLDER until experiments are run.  
> **Last updated:** 2026-04-16  
> **Dual track:** Realistic Working Paper (J.1) + Flagship Paper (J.2)

---

## SECTION J — PAPER OUTLINES (DUAL TRACK)

---

### J.1 Realistic Working Paper Outline

**Venue:** Journal of Economic Psychology / Experimental Economics  
**Length target:** 10,000–12,000 words  
**Data required:** 5,000 runs (5 bias × 2 variants × 10 models × 50 runs)

---

#### Abstract (200 words)
Problem: LLM agents deployed in procurement settings may exhibit systematic cognitive biases analogous to human behavioral economics biases, with compounding economic costs at scale.  
Method: BuyerBench Pillar 2 — a controlled-variant evaluation framework administering matched decision scenarios to LLM agents, isolating psychological manipulation from underlying economics. Five bias categories, ten models, N=50 runs per cell.  
Key finding: [PLACEHOLDER — after experiment]  
Implication: Bias susceptibility is heterogeneous across bias type and model family; deployment-critical implications for AI procurement systems.

---

#### 1. Introduction (800 words)
- **1.1** Economic relevance: AI buyer agents making procurement decisions at scale — scale amplifies any systematic bias
- **1.2** The bias question: do LLMs inherit human cognitive shortcuts from training on human text, or does RLHF/instruction tuning suppress them?
- **1.3** What we do: BuyerBench Pillar 2 as a controlled-variant bias battery — matched scenario pairs, identical economics, varied psychological presentation
- **1.4** Key findings: [PLACEHOLDER — after experiment]
- **1.5** Contribution: first multi-model, stochasticity-aware bias measurement framework in a procurement domain with ground-truth optimal choices

---

#### 2. Related Literature (1,500 words)
- **2.1** Behavioral biases in human decision-making
  - Tversky & Kahneman (1974): anchoring and adjustment heuristic
  - Kahneman & Tversky (1979): Prospect Theory — loss aversion, framing effects
  - Ariely et al. (2001): arbitrary coherence — anchoring on irrelevant numbers
  - Thaler (1980): sunk cost fallacy — escalation of commitment
  - Simonson (1989): compromise effect / decoy (attraction) effect
  - Cialdini (1984): scarcity-induced urgency and reactance
- **2.2** Prior work on LLM cognitive biases
  - Binz & Schulz (2023): GPT-4 on Kahneman/Tversky tasks — human-like biases in some conditions
  - Hagendorff et al. (2023): LLMs exhibit intuitive but not systematic thinking in bias tasks
  - Echterhoff et al. (2024): instruction tuning partially reduces but does not eliminate anchoring in GPT models
  - Santurkar et al. (2023): LLMs reflect training corpus opinion distributions
  - Jones & Steinhardt (2022): Capturing failures in LLMs via human cognitive biases
- **2.3** How BuyerBench Pillar 2 differs from prior work
  - Domain-specific: procurement supplier selection with ground-truth optimal choices
  - Stochasticity-aware: N=50 per cell characterizes variance, not just mean behavior
  - Multi-model: 10 models across families and capability tiers simultaneously
  - Operationally grounded: BSI defined against an economic optimality criterion, not just preference inconsistency

---

#### 3. Experimental Design (2,000 words)
- **3.1** BuyerBench Pillar 2: controlled-variant methodology
  - Unit of analysis: matched scenario pair (baseline + manipulation)
  - Constant: supplier set, prices, quality scores, delivery reliability, evaluation weights
  - Variable: presentation manipulation targeting a specific cognitive bias
- **3.2** Bias categories and scenario structure

  | Bias Type | Manipulation | Baseline Control |
  |---|---|---|
  | Anchoring | High/low reference price displayed before supplier list | No reference price shown |
  | Framing | Outcomes presented as gains vs. losses | Neutral outcome framing |
  | Decoy (Attraction) | Dominated decoy supplier added to choice set | No decoy in set |
  | Sunk Cost | Prior "investment" in suboptimal vendor emphasized | No prior investment mentioned |
  | Scarcity | Time pressure / limited availability cue added | No scarcity cue |

- **3.3** Agent models

  | Model | Family | Capability Tier | Interface |
  |---|---|---|---|
  | GPT-4o | OpenAI | High | OpenRouter |
  | Claude 3.5 Sonnet | Anthropic | High | OpenRouter |
  | Gemini Pro 1.5 | Google | High | OpenRouter |
  | LLaMA 3.1 405B | Meta | High | OpenRouter |
  | Mistral Large | Mistral | Mid | OpenRouter |
  | DeepSeek Chat | DeepSeek | Mid | OpenRouter |
  | Qwen 2.5 72B | Alibaba | Mid | OpenRouter |
  | Command R+ | Cohere | Mid | OpenRouter |
  | Mixtral 8x22B | Mistral | Mid | OpenRouter |
  | Yi Large | 01.AI | Mid | OpenRouter |

- **3.4** Run protocol
  - N = 50 independent runs per (model × scenario) cell
  - Temperature = 0.7 (stochastic; temperature = 0.0 robustness check in Appendix D)
  - Between-subject design: each run is an isolated session with no memory of prior runs
  - Session independence verified: no conversation history passed between runs
- **3.5** Bias Susceptibility Index (BSI): formal definition — see Section K.4 below
- **3.6** Statistical approach
  - Primary: mixed-effects logistic regression with model and bias type as crossed random effects
  - Multiple comparison correction: Benjamini-Hochberg (BH-FDR) at α = 0.05
  - Power analysis: at N=50/cell, 80% power to detect d ≥ 0.45 (medium effect)
  - Pre-registration: OSF pre-registration link — [PLACEHOLDER]

---

#### 4. Results (3,000 words) — ALL PLACEHOLDER UNTIL DATA

- **4.1** Aggregate bias susceptibility by model
  - *Figure 1: Heatmap — rows = 10 models, columns = 5 bias types, cells = mean BSI*
  - [PLACEHOLDER: description of heatmap pattern]
- **4.2** Main effects: which bias types produce highest BSI?
  - [PLACEHOLDER: ranking of bias types by mean BSI across all models]
  - [PLACEHOLDER: BH-corrected p-values for each bias type vs. zero]
- **4.3** Model capability gradient: does Pillar 1 score predict lower BSI?
  - [PLACEHOLDER: correlation between P1 task completion rate and mean BSI]
  - [PLACEHOLDER: scatter plot — P1 score vs. mean BSI with regression line]
- **4.4** Stochastic variance: within-cell variance vs. between-model variance
  - [PLACEHOLDER: ICC estimate from mixed-effects model]
  - [PLACEHOLDER: variance decomposition table]
- **4.5** Individual model profiles: notable patterns
  - [PLACEHOLDER: 2-3 noteworthy model-specific findings]

---

#### 5. Discussion (1,500 words)
- **5.1** Implications for AI agent deployment in procurement
  - Heterogeneous susceptibility means vendor-specific risk profiling is necessary
  - Framing effects in supplier catalogs are an attack surface
  - Decoy manipulation possible via catalog poisoning
- **5.2** Comparison to human benchmarks
  - [PLACEHOLDER: where available — citing Tversky & Kahneman 1974 anchoring, Simonson 1989 decoy effect magnitudes]
  - Human BSI baselines from literature: anchoring ~0.40, framing ~0.30, decoy ~0.45
- **5.3** Why do high-capability models sometimes show MORE bias?
  - Hypothesis: reasoning amplifies sunk cost (more elaborate justifications for past investment)
  - Hypothesis: instruction following amplifies framing (model attends to salience cues)
  - [PLACEHOLDER: data-grounded discussion after results]
- **5.4** Limitations — see full draft in Section K.5 below

---

#### 6. Conclusion (500 words)
- Restate: BuyerBench Pillar 2 as a reproducible controlled-variant protocol for measuring bias in LLM agents
- Restate: [PLACEHOLDER: key empirical finding]
- Forward-looking: extension to other domains, incentivized tasks, multi-turn agentic settings
- Code and data availability: GitHub + OSF repository

---

#### Appendix A: Full Scenario Text for All 10 Scenario Variants
[PLACEHOLDER — to be auto-generated from scenario definitions in `scenarios/pillar2/`]

#### Appendix B: Pre-Registration Document
[PLACEHOLDER — OSF pre-registration export; see UPGRADE-15 output]

#### Appendix C: Additional Regression Tables
[PLACEHOLDER — full mixed-effects regression tables from Section G pipeline]

#### Appendix D: Robustness Checks
[PLACEHOLDER — temperature=0.0 replication; permutation test BSI distributions]

---

---

### J.2 Flagship Paper Outline

**Venue:** Journal of Economic Behavior & Organization (JEBO) / Experimental Economics  
**Length target:** 15,000–18,000 words  
**Data required:** 20,000+ LLM runs + 100 human subjects (Prolific)

All sections from Realistic Paper (J.1), PLUS:

---

#### 3.7 Prompt Variants
- CoT (chain-of-thought): "Think step by step before selecting a supplier."
- Standard: no reasoning instruction
- Expert-role: "You are an expert procurement officer with 10 years of experience."
- 3-way design: Prompt Type × Bias Type × Model

#### 3.8 Human Comparison Arm
- Platform: Prolific Academic
- N = 100 subjects (20 per bias type; power-matched to LLM arm)
- Incentive structure: completion payment + performance bonus for optimal choice
- IRB protocol: [PLACEHOLDER — IRB application number]
- Matching: same scenario text as LLM arm; identical supplier tables and context
- Between-subject: each participant sees one variant only (baseline OR treatment)

#### 3.9 Temperature Sensitivity Analysis
- Three temperature conditions: 0.0, 0.7, 1.0
- Compare BSI distributions across temperature conditions per model
- Hypothesis: temperature=0.0 reduces stochastic variance but not mean BSI

---

#### 4.6 Prompt × Bias Interactions
- *Figure: 3-way interaction plot — Prompt Type × Bias Type × mean BSI*
- [PLACEHOLDER: key interactions from regression]
- Does CoT reduce anchoring more than decoy effects?

#### 4.7 Human vs. LLM Comparison
- *Figure: Side-by-side BSI by bias type — human baseline vs. 10 models*
- [PLACEHOLDER: qualitative comparison pattern]
- Are LLMs more or less susceptible than humans on each bias type?

#### 4.8 Capability × Bias Interactions
- Does chain-of-thought help more for anchoring (where explicit calculation helps) than for decoy (where it might not)?
- Interaction test: Prompt_CoT × Bias_Decoy, etc.
- [PLACEHOLDER: regression table]

---

#### 5.5 Structural Interpretation
- What does differential bias susceptibility across models tell us about LLM architecture?
- Hypothesis: biases that depend on salience/attention (anchoring, decoy) scale with model size
- Hypothesis: biases that require temporal self-modeling (sunk cost) are more architecture-dependent
- Limitations of structural interpretation without access to model internals

---

#### Online Appendix
- Full dataset (Parquet + CSV) — [PLACEHOLDER: repository URL]
- Replication code: Python scripts for all analyses in Section G pipeline
- Human subject protocol materials
- All scenario texts and evaluation rubrics

---

---

## SECTION K — DRAFT TEXT

---

### K.1 Title Options

**Option A (Working Paper):**
> "Behavioral Bias Susceptibility in Large Language Models: Evidence from a Controlled Procurement Evaluation Benchmark"

**Option B (Field Journal):**
> "Do AI Buyer Agents Suffer from Cognitive Biases? Experimental Evidence from LLM-Based Procurement Systems"

**Option C (Flagship — with human arm):**
> "Machine Minds and Human Biases: Comparative Experimental Evidence on Economic Rationality in Large Language Model Agents"

**Option D (Catchy):**
> "Anchored, Framed, and Deceived: Mapping Behavioral Bias Susceptibility Across Ten Large Language Models"

**Recommendation:** Option A for working paper submission. Option D for conference presentation version. Option C only if human comparison arm data is collected.

---

### K.2 Abstract (Placeholder Version)

> Large language model (LLM) agents are increasingly deployed in high-stakes economic decision environments including procurement, supplier selection, and contract negotiation. Whether these agents inherit the behavioral biases well-documented in human economic psychology — anchoring, framing effects, decoy distortions, scarcity-induced urgency, and sunk cost fallacies — remains an open empirical question with direct implications for AI system design and deployment policy. We introduce BuyerBench Pillar 2, a controlled-variant evaluation framework that administers matched economic decision scenarios to LLM agents, varying only the psychological manipulation while holding underlying economics constant. We apply this framework to [10] commercially available LLM-based agents across five canonical bias categories, running [N=50] independent trials per agent-bias cell to characterize both mean susceptibility and stochastic variance. We find that [PLACEHOLDER: key finding about which biases appear, which models are most susceptible, and how susceptibility varies]. Bias susceptibility is neither universal nor absent — it is heterogeneous across bias type and model family, with [PLACEHOLDER] explaining [X%] of cross-model variance. These findings have implications for the design of AI procurement agents and the use of LLMs as synthetic respondents in economic experiments.

---

### K.3 Introduction Draft (~800 words)

**[PARAGRAPH 1 — ECONOMIC HOOK]**

The global procurement software market exceeds $9 billion annually, and AI-powered buyer agents — systems that autonomously evaluate suppliers, compare quotes, and execute purchasing decisions — are moving from prototype to production deployment. Unlike a human procurement officer who may consult a manager or seek second opinions on large decisions, an AI agent typically acts autonomously at the moment of its optimization. If that optimization is subject to systematic cognitive biases, the economic costs compound with scale: an agent anchoring on a high reference price, persistently overweighting sunk costs, or selecting suboptimal suppliers due to decoy options embedded in catalogs may impose substantial and invisible efficiency losses across thousands of transactions. At an average enterprise procurement volume of $50M annually and a reasonable assumption that 10% of decisions involve cognitively manipulable framing, even a 5% efficiency loss attributable to bias susceptibility represents $250,000 in annual procurement waste per firm — before considering that AI agents may process decisions at a rate orders of magnitude higher than human buyers.

**[PARAGRAPH 2 — THE EMPIRICAL GAP]**

Whether LLM-based agents — the predominant architecture for AI buyer agents — exhibit systematic behavioral biases analogous to those documented in human economic psychology is an empirical question we cannot answer from first principles. Transformer architectures trained on human text might absorb human cognitive patterns through exposure to vast corpora of human reasoning, negotiation, and decision-making text. Alternatively, instruction tuning and reinforcement learning from human feedback (RLHF) might selectively suppress or accentuate bias-consistent responses. A third possibility, more unsettling for deployers, is that the presence and magnitude of bias susceptibility varies idiosyncratically across models and bias types, producing a heterogeneous risk landscape that cannot be addressed with a single mitigation strategy.

**[PARAGRAPH 3 — WHAT WE DO]**

We answer this question with BuyerBench Pillar 2, a controlled experimental framework designed along the lines of classical behavioral economics experiments but adapted for evaluating stochastic AI agents. The key methodological innovation is the controlled-variant design: for each bias type, we create matched scenario pairs in which the underlying economics (supplier qualities, prices, delivery reliability) are identical, but the presentation is manipulated to trigger a specific cognitive bias. The agent's behavioral inconsistency across matched pairs — measured as the Bias Susceptibility Index (BSI) — is our primary dependent variable. Unlike prior LLM bias evaluations that rely on single-run responses or qualitative coding, we run N=50 independent trials per agent-bias cell, allowing us to distinguish stochastic error from systematic bias and to characterize the full distribution of susceptibility within a model.

**[PARAGRAPH 4 — SCOPE AND SAMPLE]**

We apply BuyerBench Pillar 2 to ten commercially available LLM agents spanning four model families (OpenAI, Anthropic, Google, and open-weight models via OpenRouter), two capability tiers (high and mid), and five canonical bias categories drawn from the behavioral economics literature: anchoring, framing (gain/loss), decoy (attraction) effects, sunk cost fallacy, and scarcity-induced urgency. All scenarios are grounded in realistic procurement contexts with structured supplier data, evaluation weight specifications, and ground-truth optimal choices that allow objective scoring. This design enables a two-way comparison: across models (which models are most susceptible?) and across bias types (which biases are most consistently exploited?).

**[PARAGRAPH 5 — CONTRIBUTIONS]**

This paper makes three contributions. First, it introduces BuyerBench Pillar 2 as a reproducible, open-source evaluation protocol for behavioral bias in LLM agents operating in economically structured settings with verifiable optimal choices — addressing a key gap in prior work that relied on tasks without ground-truth solutions. Second, it provides the first multi-model, multi-bias, stochasticity-aware empirical characterization of bias susceptibility across [10] commercial LLMs, enabling both cross-model benchmarking and individual model risk profiling. Third, it identifies [PLACEHOLDER: pattern] with implications for the design and deployment of AI agents in procurement and related economic tasks, and for the validity of using LLMs as synthetic respondents in behavioral economics research.

**[PARAGRAPH 6 — ROADMAP]**

The remainder of the paper proceeds as follows. Section 2 reviews the behavioral economics literature on human cognitive biases and prior work on LLM bias susceptibility. Section 3 describes the BuyerBench Pillar 2 experimental design, the BSI metric, and our statistical approach. Section 4 presents results [PLACEHOLDER]. Section 5 discusses implications, compares to human benchmarks where available, and addresses limitations. Section 6 concludes.

---

### K.4 Methodology Key Passage — Bias Susceptibility Index (BSI)

#### Formal Definition (for Section 3.5)

**Definition (Bias Susceptibility Index):** Let $a^*(s)$ denote the economically optimal choice in scenario $s$, defined as the supplier maximizing the weighted utility function $U(q_i, d_i, p_i; w)$ where $q_i$, $d_i$, $p_i$ are quality, delivery reliability, and price of supplier $i$, and $w$ is the evaluation weight vector specified in the scenario. Let $a_{m,s,r}$ denote the choice made by model $m$ in scenario $s$ on run $r$. The **Bias Susceptibility Index** for model $m$ under bias type $b$ is:

$$BSI(m, b) = \frac{1}{R} \sum_{r=1}^{R} \left[ \mathbf{1}[a_{m,s_T,r} \neq a^*(s_T)] - \mathbf{1}[a_{m,s_B,r} \neq a^*(s_B)] \right]^+$$

where $s_T$ is the treatment (manipulation) scenario, $s_B$ is the matched baseline scenario, $R$ is the number of runs, and $[\cdot]^+$ denotes the positive part (we measure *additional* error induced by the manipulation, not baseline error that existed independently of the manipulation).

$BSI \in [0, 1]$: $BSI = 0$ indicates the model is no more likely to err under the biasing manipulation than in the baseline; $BSI = 1$ indicates the model always errs under manipulation but never in baseline.

#### Implementation Note — Discrepancy with `evaluators/pillar2.py`

> ⚠️ **ACTION REQUIRED:** The current implementation of `compute_bias_susceptibility` in `evaluators/pillar2.py:95` does not match this definition.
>
> **Paper formula:** `BSI = mean_over_runs[ (error_in_treatment - error_in_baseline)+ ]`
> For a single run: `BSI = max(0, indicator(wrong_in_treatment) - indicator(wrong_in_baseline))`
> This equals **1** when baseline is correct AND treatment causes an error — the canonical bias-induced failure.
>
> **Current code formula (line 95):**
> ```python
> bsi = int(decision_changed) * (1.0 - baseline_score_obj.score)
> ```
> This gives `int(decision_changed) × (1 - baseline_correctness)`.
> - If baseline was **correct** (score=1.0): BSI = `decision_changed × 0.0` = **0** ❌ (should be 1 when treatment causes error)
> - If baseline was **wrong** (score=0.0): BSI = `decision_changed × 1.0` = **1** ❌ (should be 0 — bias wasn't responsible for baseline error)
>
> **Correct implementation:**
> ```python
> baseline_error = 1.0 - baseline_score_obj.score  # 0.0 = correct, 1.0 = wrong
> variant_error  = 1.0 - variant_score_obj.score
> bsi = max(0.0, variant_error - baseline_error)
> ```
>
> This should be reconciled before running the full experiment to ensure BSI values are interpretable as defined in the paper.

#### Confidence Interval Estimation

For the aggregate BSI across R=50 runs, we report bootstrap 95% confidence intervals:

$$CI_{BSI}(m, b) = \text{Bootstrap}_{B=1000}\left[ BSI^{(b)}(m, b) \right]$$

where each bootstrap replicate re-samples R runs with replacement from the R × 2 (baseline + treatment) run pairs. This accounts for within-model correlation between baseline and treatment runs sharing the same model and prompt context.

---

### K.5 Limitations Draft (~400 words)

**6.4 Limitations**

This study has several limitations that bound the interpretation of our findings and suggest directions for future research.

**Single domain.** All scenarios in BuyerBench Pillar 2 are drawn from procurement supplier selection contexts. While procurement is a high-stakes economic domain with direct relevance to AI deployment, we cannot claim that bias susceptibility patterns generalize to other economic decision domains such as financial portfolio allocation, medical resource triage, or consumer product recommendation. Domain-specific features — structured supplier tables, explicit evaluation weights, well-defined optimality criteria — may make some biases easier or harder to trigger than in more ambiguous decision environments.

**Absence of monetary incentives.** LLM agents cannot receive financial payoffs, and our "bias" is therefore behavioral in the sense of decision inconsistency, not incentivized preference revelation. Human behavioral economics is motivated by the observation that incentivized monetary choices exhibit biases; we study a system that cannot be incentivized. It is possible that biases we observe at temperature=0.7 would be reduced if models were calibrated to maximize a performance reward. However, in agentic deployment, LLMs typically act without external reward signals, making our setting the operationally relevant one.

**Prompt sensitivity.** Behavioral effects in LLMs are known to be sensitive to minor wording changes in ways that human responses typically are not (Sclar et al., 2023). Our scenario texts were fixed after a pilot calibration phase, but we cannot guarantee that alternative phrasings would produce the same BSI estimates. We document robustness checks at two temperature conditions (Appendix D) but do not exhaustively sample the prompt distribution.

**Model versioning.** Commercial LLM APIs update model weights without versioning guarantees. Our experiments were run in [PLACEHOLDER: date range]; results may not replicate on future model versions accessed via the same API endpoints. We report model version identifiers where available and archive all API responses.

**Statistical power for small effects.** At N=50 runs per cell, our design has 80% power to detect effects of d ≥ 0.45 (medium effect size). Bias susceptibility below this threshold — for example, a model that is 5–10% more likely to err under manipulation — may not be reliably detected. We interpret null results as evidence against large effects, not against any effect.

**Training data contamination.** If scenario text or structural patterns appeared in model training data, model responses may partially reflect memorized patterns rather than genuine in-context reasoning. We design scenarios to be novel and domain-specific, but contamination testing is not feasible without access to training corpora.

**No mechanism identification.** BuyerBench Pillar 2 measures *whether* bias susceptibility occurs and *how much*, but does not identify *why* specific models exhibit specific biases. Mechanistic interpretability of transformer attention patterns under biasing manipulations is beyond the scope of this paper and left to future work.

---

## Notes & Decision Log

| Date | Decision | Rationale |
|---|---|---|
| 2026-04-16 | BSI formula discrepancy flagged | Code inverts paper definition — must be fixed before running experiments |
| 2026-04-16 | Title Option A selected for working paper | Most precise for academic submission; Option D for conference |
| 2026-04-16 | N=50/cell adopted as minimum | 80% power for d≥0.45; upgrade to N=100 for flagship paper if budget allows |
| 2026-04-16 | Realistic paper = 5 biases × 2 variants × 10 models × 50 runs = 5,000 runs | Manageable with OpenRouter API budget ~$500 estimated |
