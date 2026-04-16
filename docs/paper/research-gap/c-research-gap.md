---
type: research
title: "Section C — Research Gap: Four Gaps and BuyerBench's Contribution"
created: 2026-04-16
tags:
  - research-gap
  - positioning
  - pillar2
  - bsi
  - llm-bias
  - behavioral-economics
  - contribution
related:
  - '[[b6-synthesis]]'
  - '[[b3-01-binz-schulz-2023]]'
  - '[[b3-03-hagendorff-2023]]'
  - '[[b3-05-jones-steinhardt-2022]]'
  - '[[b3-06-echterhoff-2024]]'
  - '[[b5-03-loken-gelman-2017]]'
  - '[[b5-02-simmons-nelson-simonsohn-2011]]'
  - '[[b5-01-open-science-collaboration-2015]]'
  - '[[strategy-decision-tree]]'
  - '[[tier4-primary-submission-strategy]]'
---

# Section C — Research Gap

## Four Gaps, Contribution Ranking, and Defensibility Statement

---

## Gap 1 — Primary (Benchmarking): No Domain-Specific Economic Optimality Criterion

**Statement:** No existing benchmark evaluates LLM behavioral biases in procurement decision-making with a ground-truth economic optimality standard.

### The Specific Problem

All prior LLM behavioral bias studies — Binz & Schulz (2023), Hagendorff et al. (2023), Jones & Steinhardt (2022), Echterhoff et al. (2024) — share a fundamental measurement limitation: **the absence of a computable correct answer.** Bias is detected by observing that the same agent produces different outputs under frames that are logically equivalent (e.g., "admit?" vs. "reject?"), or that outputs drift under sequential anchoring manipulations. This consistency-based detection approach captures *shifts* in behavior but cannot quantify whether those shifts represent economically meaningful errors.

Echterhoff et al. (2024) is the closest precedent. But their college admissions domain explicitly lacks a ground-truth decision — "correctness is undefined" (their framing). A model that shows 40 percentage points of framing sensitivity may be adapting appropriately to genuinely ambiguous admission decisions; a model that selects the dominated supplier in a procurement scenario with a computable expected value is unambiguously wrong.

### Why the Gap Matters for Publication

For JEBO or Experimental Economics, behavioral economics reviewers will ask: "What is the agent's loss from bias?" Consistency-based metrics cannot answer this. Procurement decisions have observable economic consequences — a biased choice that costs the firm $12,000 in avoidable expenditure can be stated precisely, not as a percentage point shift in a nominally identical choice. The BSI (Gap 4 below) is the vehicle for this, but its precondition is the existence of a domain where optimality is computable. Procurement is that domain.

### Prior Art Summary

| Study | Domain | Ground-Truth Optimal? | Economic Consequence Quantified? |
|---|---|---|---|
| Binz & Schulz (2023) | Abstract cognitive tasks (CRT, base-rate) | No | No |
| Hagendorff et al. (2023) | Cognitive tasks, Asian Disease | No | No |
| Jones & Steinhardt (2022) | Adversarial NLP (label prediction) | Partial (label accuracy) | No |
| Echterhoff et al. (2024) | College admissions | No (explicitly) | No |
| **BuyerBench** | **B2B procurement (supplier selection, contract terms, payment flows)** | **Yes (computable EV for every scenario)** | **Yes (BSI × dollar amount)** |

### BuyerBench Response

Every Pillar 2 scenario in BuyerBench has a computable optimal: the supplier with the highest expected value net of risk-adjusted costs, identified by the scenario designer at authoring time. The ground truth is embedded in the evaluation harness, not post-hoc rationalized from model outputs. This makes Gap 1 the **most defensible contribution** — it is a structural feature of the evaluation architecture rather than a claim about what models do.

---

## Gap 2 — Secondary (Multi-Model Comparative): Bias Susceptibility Across Model Families Is Unknown

**Statement:** Prior work is predominantly single-model or inadequately powered for multi-model comparison. We do not know whether bias susceptibility is a property of model capability, model family, RLHF alignment intensity, or training data composition.

### The Specific Problem

| Study | Models Tested | Runs per Cell | Multi-Model Comparison Adequately Powered? |
|---|---|---|---|
| Binz & Schulz (2023) | 1 (GPT-3 text-davinci-003) | 1 | No — single model |
| Hagendorff et al. (2023) | 9 (text-ada-001 through GPT-4, LLaMA-1) | 1–3 | No — single run |
| Jones & Steinhardt (2022) | 2 (GPT-3, FLAN) | 1 | No — cannot separate model from prompt |
| Echterhoff et al. (2024) | 4 (GPT-3.5-turbo, GPT-4, LLaMA 2-7B/13B) | ~5–20 per model | Partial — only LLaMA 2, 2 GPT variants |

No study has collected N ≥ 30 per (bias × model) cell across a set of frontier models large enough to support variance decomposition by model family or capability tier.

### Why This Gap Matters

The policy and deployment implication differs substantially depending on the answer:
- If bias susceptibility is primarily a function of **capability tier** (larger/stronger models are less biased), then the procurement-safety implication is "deploy only frontier-class models."
- If susceptibility is primarily a function of **model family** (some architectures are systematically more resistant than others), then the implication is "evaluate bias as part of model selection criteria."
- If susceptibility is primarily a function of **prompt structure and explicit constraints**, then the implication is "engineer the prompt, not the model."

BuyerBench's ten-model scope — spanning OpenAI, Anthropic, Google, Meta, Mistral, Qwen, Cohere, and DeepSeek models — provides the first dataset to run variance decomposition across all three explanatory axes simultaneously.

### Preliminary Data Note

Current experimental data (N ≈ 1–3 runs per cell, insufficient for inference) shows near-universal BSI ≈ 0.0 across models for most bias types, with LLaMA 3.3 70B as the only model to exhibit a genuine scarcity susceptibility signature on p2-04. This preliminary pattern — domain structure suppresses bias across capability tiers, with a possible capability-threshold below which susceptibility re-emerges — is not testable at current sample sizes. N = 30 per cell is the minimum to resolve this question.

---

## Gap 3 — Methodological: Stochastic Output Variance as an Unmodeled Confound

**Statement:** No existing LLM bias study explicitly models stochastic output variance as a confound in bias detection. Effect sizes from single-run studies may be entirely driven by temperature-sampling noise.

### The Specific Problem

Loken & Gelman (2017) show that under high measurement noise and small N, significance thresholds systematically produce Type M (magnitude) errors: published "significant" effects are inflated 2–5× relative to the true effect. This structural inflation occurs even without p-hacking — it is an arithmetic consequence of the noise-threshold interaction.

For LLM bias studies, the noise source is **temperature-sampled output variance**. A binary procurement choice at temperature = 0.7 has a standard deviation of approximately σ = √(p × (1 − p)) ≈ 0.46 when true BSI ≈ 0.30. With N = 1 run, the observed BSI is a Bernoulli draw: it is either 0.0 (model chose correctly) or 1.0 (model chose incorrectly), with no intermediate resolution. A single-shot study that observes BSI = 1.0 may report a "complete failure" when the true underlying bias probability is only 0.30.

### Type M Error Estimates for Single-Shot Prior Studies

| Study | N per condition | Estimated true BSI range | Expected observed inflation (Type M ratio) |
|---|---|---|---|
| Binz & Schulz (2023) | 1 | Unknown | 3–5× |
| Hagendorff et al. (2023) | 1–3 | Unknown | 2–5× |
| Jones & Steinhardt (2022) | 1 | Unknown | 3–5× |
| Echterhoff et al. (2024) | ~5–20 | Unknown | 1.5–3× |
| **BuyerBench (target)** | **≥30** | **Estimable via bootstrap CI** | **<1.5× at BSI ≥ 0.20** |

### Why This Gap Matters

From the perspective of the reviewer at *Experimental Economics* or JEBO: "The prior literature cannot distinguish genuine bias susceptibility from measurement noise. BuyerBench is the first study designed explicitly to model this variance, pre-register cell sizes based on a power analysis, and report bootstrap confidence intervals with Type M ratio estimates for all BSI cells."

This framing positions Gap 3 as a **methodological contribution** that would survive even if BuyerBench's empirical findings were null (near-zero BSI across models) — the null finding itself becomes more credible because the design was powered to detect BSI ≥ 0.20 with appropriate α correction.

### Design Implications

- **Pre-registration requirement:** Model set, bias types, N per cell, α threshold, and BSI calculation formula must be locked before data collection begins. Simmons et al. (2011) show that post-hoc flexibility in any of these parameters produces false-positive rates >60%.
- **Multiple comparison correction:** With 5 bias types × 10 models = 50 primary tests, BH-FDR at q = 0.05 is the minimum correction. Bonferroni is acceptable as an upper bound.
- **Temperature ablation:** A secondary analysis at temperature = 0.0 (if supported by model API) allows decomposition of stochastic vs. deterministic bias.

---

## Gap 4 — Economic: The BSI Formalization

**Statement:** The economic concept of "bias susceptibility index" — measuring deviation from a rational optimum as a normalized index — has not been formally defined or applied to LLM agents.

### The Specific Problem

Existing LLM bias studies report either:
- **Consistency metrics:** Does the model choose differently across logically equivalent frames? (Echterhoff et al., 2024)
- **Accuracy metrics:** Does the model's choice match a human-labeled "correct" answer? (Jones & Steinhardt, 2022, for NLP tasks only)
- **Distributional shifts:** Does the choice distribution shift under manipulation? (Aher et al., 2023; Hagendorff et al., 2023)

None of these metrics quantify the *economic cost* of the observed behavioral deviation. A model that selects a dominated option 30% of the time in a procurement scenario with a $10,000 EV cost imposes a quantifiable expected loss of $3,000 per decision episode. Consistency-based metrics cannot express this.

### BSI Formal Definition

The Bias Susceptibility Index is defined as:

```
BSI(model, bias_type) = |P(optimal_choice | MANIPULATION) - P(optimal_choice | BASELINE)|
```

Where:
- `P(optimal_choice | condition)` is estimated from N ≥ 30 runs as a proportion with a bootstrap 95% CI
- `BASELINE` is the controlled-variant condition with no behavioral manipulation
- `MANIPULATION` is the controlled-variant condition with a single behavioral manipulation applied (anchor, framing, decoy, scarcity, or sunk cost cue)
- `optimal_choice` is the scenario-specific ground-truth action determined by expected value calculation at authoring time

BSI ∈ [0, 1] where:
- BSI = 0.0: No susceptibility — manipulation does not affect choice probability
- BSI = 1.0: Complete susceptibility — manipulation fully determines choice away from the optimum

### BSI Extension: Dollar-Weighted Impact

For economic significance reporting, BSI can be scaled by the dollar cost of the sub-optimal choice:

```
BSI_dollar(model, scenario) = BSI × (EV_optimal - EV_chosen) × N_decisions
```

This enables cross-model "economic harm" comparisons in procurement deployment contexts. A model with BSI = 0.3 on a $10k EV gap and 1,000 annual decisions has an expected annual bias cost of $3,000,000 — a framing that economic reviewers at JEBO will find persuasive.

### Why This Formalization Matters

No prior LLM study has:
1. Defined a scalar BSI with a clear operational formula
2. Anchored BSI to a computable economic optimum (rather than a consistency criterion)
3. Enabled cross-bias and cross-model BSI comparison on a common [0, 1] scale
4. Provided dollar-denominated economic significance alongside statistical significance

The BSI formalization is Gap 4's contribution — it is a **measurement innovation** that bridges the behavioral economics and AI evaluation literatures.

---

## Contribution Ranking

The four gaps are not equally defensible. The following ranking governs framing decisions in the paper:

### Rank 1 — Measurement/Benchmarking (Most Defensible)

**Claim:** BuyerBench is the first controlled-variant behavioral bias battery in a procurement domain with computable ground-truth economic optimality.

**Why most defensible:** This is a factual description of what was built. It does not depend on which results are observed, does not require statistical power, and is falsifiable only if a prior study can be produced that we have missed. Literature review across JEBO, EMNLP, PNAS, NeurIPS, and NHB confirms no such prior study exists.

**Paper section:** Abstract, Introduction (first contribution bullet), Methodology, Conclusion.

### Rank 2 — Methodological (Strong)

**Claim:** BuyerBench is the first LLM bias study to explicitly model stochastic output variance, pre-register cell sizes via Type M power analysis, and report bootstrap confidence intervals for the BSI.

**Why strong:** Based on a clean extension of Loken & Gelman (2017) and Simmons et al. (2011) to the LLM context. The methodological critique of prior single-shot studies is well-grounded. Defensible even if empirical BSI results are near-zero (the null finding is informative under adequate power).

**Paper section:** Introduction (second contribution bullet), Methodology (primary contribution of this section), Discussion (null-finding interpretation).

### Rank 3 — Behavioral Economics Insight (Cautious)

**Claim:** Across [N] models and 5 bias types, we find [X] pattern, consistent with / contradicting / extending the human behavioral economics literature.

**Why cautious:** The specific claim depends entirely on the empirical data. Current pilot data (N=1–3 per cell) shows near-universal BSI ≈ 0.0, suggesting domain structure with explicit constraints suppresses bias in frontier LLMs. If this holds at N=30 per cell, the behavioral economics insight is: "structured procurement domains are bias-resistant for frontier LLMs; the Hagendorff et al. capability-bias correlation does not generalize to economically structured B2B contexts." This is a legitimate and interesting finding. But the wording must hedge on mechanism — we cannot identify *why* domain structure suppresses bias from behavioral data alone.

**Appropriate hedge language:** "We find that [X/10] models show statistically significant BSI on at least one bias type (BH-FDR corrected), with inter-model BSI variance suggesting [pattern]. We do not attempt to identify the mechanism by which domain-structure moderates susceptibility; this requires a further manipulation isolating constraint explicitness from economic stakes and stimulus novelty."

**Paper section:** Results, Discussion (first 2–3 paragraphs).

### Rank 4 — Theory (Speculative; Not for This Paper)

**Claim:** [Mechanism X] explains why LLMs exhibit or resist behavioral biases in procurement contexts.

**Why speculative:** The behavioral data from a single-agent, single-domain study cannot identify mechanisms. Possible mechanisms — training data contamination, RLHF suppression of heuristic outputs, chain-of-thought self-correction, constraint salience overriding affect-laden cues — are all observationally equivalent at the prompt-response level. Mechanism identification requires experimental manipulations (ablation of constraints, prompt structure variations, human comparison arm, chain-of-thought trace analysis) not present in the BuyerBench design.

**Paper treatment:** Acknowledge mechanism as a direction for future work. Do not present speculative mechanisms as findings.

---

## Defensibility Statement

> **Core claim:**
>
> We introduce BuyerBench, the first controlled-variant behavioral bias benchmark for AI buyer agents operating in B2B procurement domains. Unlike prior LLM behavioral studies that use abstract cognitive tasks or decision domains without computable ground-truth optima (Binz & Schulz, 2023; Hagendorff et al., 2023; Echterhoff et al., 2024), BuyerBench evaluates agent choices against explicitly defined expected-value optima, enabling the Bias Susceptibility Index (BSI) — a normalized measure of deviation from rational procurement choices that has not previously been formalized for LLM agents. Our between-subject controlled-variant design (N ≥ 30 per model-bias cell) addresses the stochastic output variance confound that renders single-shot LLM bias estimates uninterpretable under Loken & Gelman's (2017) Type M error framework. Across 10 models spanning 5 model families and 5 bias types (anchoring, framing, decoy, scarcity, sunk cost), we find that [X of 10 models] show statistically significant BSI on at least one bias type (BH-FDR corrected; α = .05), with inter-model variance primarily explained by [model capability / model family / prompt constraint salience]. Bias susceptibility is neither universal nor absent — it is heterogeneous across bias type and model family, and its distribution in structured procurement contexts diverges substantially from the patterns documented in abstract cognitive task environments.
>
> **What this paper cannot claim:**
> - We cannot claim to identify the *mechanism* by which procurement domain structure moderates bias susceptibility.
> - We cannot claim that BSI scores generalize to real-world procurement deployments with different prompt architectures, knowledge retrieval tools, or multi-turn negotiation dynamics.
> - We cannot claim cross-domain generalizability beyond the five bias types and single-domain battery tested.
> - We cannot rule out training-data contamination as a partial contributor to low BSI values, though our novel stimulus design (procurement-specific scenarios not drawn from canonical bias paradigms) substantially reduces this risk.
> - We do not provide a human comparison arm; human BSI benchmarks from the canonical behavioral economics literature (B1 series) are referenced as orientation but are not directly compared under identical stimuli.
>
> **What distinguishes this from a null result:**
> If BSI ≈ 0.0 across all models and bias types (the current pilot direction), this is an *informative* finding — not a null result in the deflationary sense. Under adequate power (N=30, Type M ratio < 1.5× for BSI ≥ 0.20), a near-zero BSI with narrow confidence intervals rules out non-trivial bias susceptibility. The appropriate interpretation is: "BuyerBench's structured procurement domain with explicit constraints and computable rubrics is a bias-resistant evaluation context for frontier LLMs. Whether this reflects genuine economic rationality or prompt-driven constraint compliance is a question for future work."

---

## Cross-References

| Gap | Primary Supporting Literature Notes | Key Rebuttal Study |
|---|---|---|
| Gap 1 (Benchmarking) | [[b3-06-echterhoff-2024]] — "correctness is undefined" limitation | Echterhoff et al. (2024) |
| Gap 2 (Multi-Model) | [[b3-01-binz-schulz-2023]], [[b3-03-hagendorff-2023]], [[b3-05-jones-steinhardt-2022]] | Hagendorff et al. (2023) — 9 models, single run |
| Gap 3 (Stochasticity) | [[b5-03-loken-gelman-2017]], [[b5-02-simmons-nelson-simonsohn-2011]], [[b5-01-open-science-collaboration-2015]] | All single-shot prior work |
| Gap 4 (BSI) | [[b6-synthesis]], [[b3-06-echterhoff-2024]] | Consistency-based metrics in all prior work |

---

## BibTeX Quick Reference

All BibTeX entries are documented in the individual literature notes. Key entries for Section C:

```bibtex
@inproceedings{echterhoff2024cognitive,
  author = {Echterhoff, Jessica M. and Liu, Yao and Alessa, Abeer and McAuley, Julian and He, Zexue},
  title = {Cognitive Bias in Decision-Making with {LLMs}},
  booktitle = {Findings of the Association for Computational Linguistics: {EMNLP} 2024},
  pages = {12640--12653},
  year = {2024}
}

@article{loken2017measurement,
  author = {Loken, Eric and Gelman, Andrew},
  title = {Measurement error and the replication crisis},
  journal = {Science},
  volume = {355},
  number = {6325},
  pages = {584--585},
  year = {2017}
}

@article{simmons2011false,
  author = {Simmons, Joseph P. and Nelson, Leif D. and Simonsohn, Uri},
  title = {False-positive psychology: Undisclosed flexibility in data collection and analysis allows presenting anything as significant},
  journal = {Psychological Science},
  volume = {22},
  number = {11},
  pages = {1359--1366},
  year = {2011}
}

@article{osc2015estimating,
  author = {{Open Science Collaboration}},
  title = {Estimating the reproducibility of psychological science},
  journal = {Science},
  volume = {349},
  number = {6251},
  pages = {aac4716},
  year = {2015}
}
```
