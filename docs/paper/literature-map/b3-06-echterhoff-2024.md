---
type: reference
title: "B3.06 — Cognitive Bias in High-Stakes Decision-Making with LLMs: Echterhoff et al. (2024)"
created: 2026-04-16
tags:
  - llm-behavioral-study
  - cognitive-bias
  - high-stakes-decision
  - bias-mitigation
  - anchoring
  - framing
  - status-quo-bias
  - primacy-bias
  - group-attribution-bias
  - emnlp
  - most-relevant-prior-work
  - literature-map
  - pillar2
  - positioning
related:
  - '[[b3-01-binz-schulz-2023]]'
  - '[[b3-03-hagendorff-2023]]'
  - '[[b3-04-aher-2023]]'
  - '[[b3-05-jones-steinhardt-2022]]'
  - '[[b1-01-anchoring-tversky-kahneman-1974]]'
  - '[[b1-02-framing-tversky-kahneman-1981]]'
  - '[[b1-06-status-quo-bias-samuelson-zeckhauser-1988]]'
  - '[[strategy-decision-tree]]'
---

# B3.06 — Cognitive Bias in High-Stakes Decision-Making with LLMs: Echterhoff et al. (2024)

**Full citation:** Echterhoff, J., Liu, Y., Alessa, A., McAuley, J., & He, Z. (2024). Cognitive Bias in Decision-Making with LLMs. In *Findings of the Association for Computational Linguistics: EMNLP 2024*, pp. 12640–12653. Miami, Florida, USA. arXiv:2403.00811.

> **Priority flag:** This is the most relevant published prior work for BuyerBench Pillar 2 positioning. Any paper submission must explicitly cite, situate, and extend this work. The title overlap ("cognitive bias," "high-stakes," "decision-making," "LLMs") requires a precise differentiation statement in the introduction.

---

## 1. Empirical Design

Echterhoff et al. introduce **BiasBuster**, a framework for evaluating and mitigating cognitive bias in LLM-assisted decision-making. The paper operationalizes five cognitive biases across a single high-stakes decision domain — **student college admissions** — and proposes a self-debiasing mitigation strategy.

### 1.1 Bias Taxonomy

The paper organizes biases into three categories:

| Category | Bias Type | Mechanism |
|---|---|---|
| **Sequential** | Anchoring | Prior decisions in a batch influence subsequent ones (recency/anchor drift) |
| **Prompt-induced** | Status quo bias | Presence of a designated default option inflates its selection rate |
| **Prompt-induced** | Framing bias | Equivalent admission decisions differ under "admit?" vs. "reject?" framing |
| **Prompt-induced** | Group attribution bias | Demographic attributes (gender) alter ability assessments despite identical profiles |
| **Inherent** | Primacy bias | Options listed earlier in a choice set are selected disproportionately |

### 1.2 Domain and Dataset

**Scenario:** Synthetic student profiles varying on country of origin, university, major, GPA, extracurricular activities, and demographic attributes. A college admissions officer LLM agent must decide whether to admit each student.

**Dataset scale:** 16,800 decision instances total:
- Anchoring: 5,425 prompts (batched sequential decisions)
- Status quo / primacy: 1,008 prompts
- Framing: 2,000 prompts
- Group attribution: 1,000 prompts

Student profiles are synthetic but realistic; no ground-truth admission decision exists — correctness is undefined.

### 1.3 Models Tested

Four models evaluated:
- **Commercial:** GPT-3.5-turbo, GPT-4
- **Open-source:** LLaMA 2 (7B and 13B parameters)

GPT-4 evaluation is constrained to ≤400 prompts per experiment for cost reasons.

### 1.4 Bias Detection Methodology

Each bias type uses a bespoke detection method:

- **Anchoring:** Normalized Euclidean distance between a model's general admission rate baseline and its per-student admission rate given varying sequential positions. Drift across positions signals anchoring to prior decisions.
- **Status quo bias:** Four-option single-choice prompt with one option designated default. Unbiased uniform selection would produce 25% per option; excess selection of the default is the bias signal.
- **Framing bias:** Identical student profile, two prompts — "Should this student be admitted?" vs. "Should this student be rejected?" Admission rate difference between frames is the bias signal.
- **Group attribution bias:** Two profiles identical except gender; difference in LLM-assessed mathematics ability is the bias signal.
- **Primacy bias:** Position-frequency analysis of selected option labels (A, B, C, D). Higher selection rate for early positions signals primacy.

### 1.5 Key Quantitative Findings

| Bias | Finding | Model |
|---|---|---|
| Framing | +40 pp admission rate in rejection-framed prompts vs. admission-framed | GPT-4 |
| Group attribution | 32% fewer females assessed as mathematically capable | LLaMA 2-7B |
| Primacy | Systematic preference for options A/B over C/D across all models | All |
| Status quo | **Inverse** status quo effect — models preferred non-default options | All |
| Anchoring | Batch admission rates drift with sequential position (lower confidence, neighbor influence) | GPT-3.5 / LLaMA |

**Anomalous status quo finding:** Models showed *anti-*status quo behavior (preferring non-default options), opposite to the human benchmark from Samuelson & Zeckhauser (1988). The authors note this without a theoretical account; it may reflect instruction-following overrides in RLHF-tuned models or demand characteristics from the "default" label.

### 1.6 Bias Mitigation Strategies

Three approaches tested:

1. **Zero-shot instruction:** "Be mindful of not being biased by cognitive bias." — Weak and inconsistent effects.
2. **Few-shot contrastive/counterfactual examples:** Failure cases and correct examples provided. Caused extreme output distributions (0%/100% admission rates) in weaker models; introduced *new* biases.
3. **Self-help (proposed novel method):** LLM rewrites the prompt to remove bias-inducing language, then re-answers using the rewritten version. More reliable than few-shot; effectiveness correlates with model capacity.
   - GPT-4: Reduced group attribution bias elements to 0%; strong primacy improvement.
   - LLaMA 2-13B: Reduced framing bias elements to 0%.
   - LLaMA 2-7B: High decision inconsistency (40–52% answer change rate), limiting applicability.

---

## 2. Strengths

**"High-stakes" framing and domain realism.** Echterhoff et al. advances beyond the abstract cognitive task paradigm (Binz & Schulz, 2023; Hagendorff et al., 2023) by situating bias evaluation in a realistic decision scenario — college admissions — with socially consequential outputs. This is the closest pre-BuyerBench paper in spirit: it accepts that AI-assisted decisions matter, not just that LLMs exhibit interesting patterns.

**Bias mitigation arm.** No prior paper in the LLM bias literature provides a rigorous comparison of bias mitigation strategies. The self-help debiasing method is a genuine novel contribution: it requires no manually curated examples, is model-agnostic in principle, and degrades gracefully with model capacity. This is the part of the paper that BuyerBench should *not* replicate — it belongs to Echterhoff et al. as the primary citation for mitigation.

**Multi-bias coverage in a single domain.** Five bias types operationalized within a single scenario domain enables cross-bias comparisons and avoids the fragmentation of the Jones & Steinhardt (2022) taxonomy study, which scattered across multiple task types.

**EMNLP 2024 venue.** Publication in Findings of EMNLP is a credible peer-reviewed track. This is not a preprint-only result; it has survived ACL-community review. BuyerBench must explicitly position relative to it.

**Largest dataset in this space.** 16,800 prompts is substantially larger than Hagendorff et al. (2023) or Binz & Schulz (2023). For model evaluation purposes, the anchoring battery (5,425 prompts) is particularly rich.

---

## 3. Limitations

**No ground-truth economic optimality — the fundamental gap BuyerBench fills.** The single most important limitation for BuyerBench positioning: there is no correct answer in the college admissions domain. The "correct" decision for each student profile is undefined; the paper measures *consistency* across conditions, not *deviation from an optimal choice*. This means Echterhoff et al. cannot compute a Bias Susceptibility Index — there is no rational baseline to deviate from. Every bias measure is purely relative (this frame produces X% vs. Y%), not absolute (this model is Z% less likely to select the economically optimal option).

**Single domain with no economic structure.** College admissions involves no prices, no budget constraints, no quantifiable supplier trade-off, and no profit or cost consequence. Procurement decisions are structurally distinct: the agent must compare options on quantifiable economic attributes (price, delivery time, quality metrics) under a hard budget constraint. The cognitive architecture required to make good procurement decisions may differ from admissions judgments in ways that matter for bias susceptibility.

**No controlled-variant design.** Echterhoff et al.'s bias manipulations confound the bias signal with surface-level prompt differences. The framing manipulation ("admit?" vs. "reject?") changes the valence of the response requested, the implied action, and the surface vocabulary simultaneously — multiple potential drivers of the observed effect. BuyerBench's between-subject controlled variant design holds *everything* constant except the bias-triggering manipulation.

**No stochasticity modeling.** The paper does not report temperature settings for most experiments, does not perform multi-run variance estimation, and does not model within-condition variance as a potential confound. A +40 pp framing effect with no confidence interval cannot be assessed for statistical reliability against a JEBO reviewer.

**Four models, including outdated open-source.** LLaMA 2-7B and 13B are substantially less capable than 2024–2025 frontier models. GPT-4 evaluation is severely budget-constrained (≤400 prompts per experiment). The generalization of findings to Claude 3.5 Sonnet, Gemini 1.5 Pro, or the LLaMA 3.x family is unestablished.

**Admissions domain training data contamination.** College admissions decision-making is heavily documented in GPT training data (common application essays, admissions guides, diversity debates). LLM behavior in this domain may partly reflect memorized distributional priors rather than genuine decision-making architecture.

**Status quo anomaly is unexplained.** The finding that models exhibit *anti-*status quo bias is presented without a theoretical account. This is both a methodological concern (is the detection method measuring what it intends to measure?) and a missed empirical contribution.

---

## 4. BuyerBench Relevance

### 4.1 How BuyerBench Extends Echterhoff et al.

BuyerBench directly extends Echterhoff et al. across six dimensions:

| Dimension | Echterhoff et al. (2024) | BuyerBench |
|---|---|---|
| **Domain** | College admissions (no economic structure) | Procurement decisions (prices, budgets, quantified trade-offs) |
| **Optimality criterion** | None — no correct answer; measures consistency only | Ground-truth economic optimal computable from scenario parameters |
| **Bias metric** | Relative frequency shift (pp difference between conditions) | Bias Susceptibility Index (BSI): normalized deviation from rational optimum |
| **Controlled-variant design** | No — framing and other confounds co-vary with manipulation | Yes — between-subject; only the bias-triggering element differs; economics held constant |
| **Stochasticity** | Single-run; no variance estimation | N=30 runs per cell; within-cell variance estimated; mixed-effects BSI model |
| **Model coverage** | 4 models (GPT-3.5-turbo, GPT-4, LLaMA 2-7B, 13B) | 10 frontier models (GPT-4o, Claude 3.5, Gemini 1.5, LLaMA 3.x, Mistral, Qwen, Cohere, Yi) |
| **Bias taxonomy** | 5 types (anchoring, framing, status quo, group attribution, primacy) | 5 implemented (anchoring, framing, decoy, scarcity, sunk cost) + 2 proposed (status quo, loss aversion) |
| **Mitigation arm** | Yes — zero-shot, few-shot, self-help | Out of scope for this paper; Echterhoff et al. is the primary citation for mitigation |

### 4.2 The Ground-Truth Optimality Gap Is the Core Extension

Echterhoff et al.'s core limitation — no ground-truth correct answer — is not a methodological oversight. It is structurally inherent to the college admissions domain: reasonable people disagree about who to admit, and no objective criterion resolves that disagreement. This means their metric is necessarily *consistency-based* rather than *rationality-based*.

BuyerBench's procurement scenarios have an objectively computable rational choice given the scenario parameters (lowest cost meeting quality threshold, under budget constraint). This enables:

1. **Absolute deviation measurement.** BSI = |P(rational|bias) − P(rational|baseline)| / P(rational|baseline) is a theoretically grounded index, not an ad hoc frequency delta.
2. **Human-benchmark comparison.** Human subjects' BSI on structurally equivalent procurement vignettes can be measured and compared to LLM BSI. Echterhoff et al. cannot do this — there is no human "correct" admissions answer to benchmark against.
3. **Economic consequence quantification.** A procurement agent with BSI = 0.3 on anchoring causes a quantifiable expected dollar loss per decision cycle. Echterhoff et al.'s framing effect (40 pp admissions difference) has no attached economic consequence unit.

### 4.3 Bias Taxonomy Overlap and Gaps

BuyerBench and Echterhoff et al. share partial taxonomy overlap:

| Bias | Echterhoff et al. | BuyerBench |
|---|---|---|
| Anchoring | ✓ (sequential batch form) | ✓ p2-01 (prior price as anchor, not sequential decision) |
| Framing | ✓ (admit/reject question form) | ✓ p2-02 (gain/loss contract framing) |
| Status quo bias | ✓ (default option designation) | Proposed p2-06 (incumbent supplier designation) |
| Group attribution bias | ✓ (gender → ability assessment) | Not in scope (no demographic attributes in procurement) |
| Primacy bias | ✓ (option position preference) | Not directly tested (supplier order controlled in BASELINE) |
| Decoy effect (IIA) | ✗ | ✓ p2-03 (asymmetrically dominated third option) |
| Scarcity/urgency | ✗ | ✓ p2-04 (temporal and capacity scarcity cues) |
| Sunk cost | ✗ (not in Echterhoff et al.) | ✓ p2-05 (prior investment framing) |
| Loss aversion | ✗ | Proposed p2-07 |

**Key additions BuyerBench makes to the bias taxonomy:** decoy effect (IIA violation), scarcity/urgency, and sunk cost are absent from Echterhoff et al. — precisely the biases most ecologically relevant to procurement. BuyerBench's taxonomy is more procurement-domain-native.

**Key addition Echterhoff et al. makes that BuyerBench does not:** group attribution bias (demographic fairness) and primacy bias (option ordering). These are not procurement-decision biases but social/display biases. They are outside BuyerBench scope by design — BuyerBench evaluates economic rationality, not demographic fairness.

### 4.4 Positioning Statement for Paper Introduction

> "Echterhoff et al. (2024) provide the most structurally proximate prior work, evaluating cognitive bias in LLM-assisted college admissions decisions across five bias categories. Their 'BiasBuster' framework documents substantial framing effects (+40 pp), group attribution bias, and primacy effects, and proposes a self-debiasing mitigation strategy. However, college admissions has no ground-truth rational decision: the study can only measure *consistency* across conditions, not *deviation from an economically optimal choice*. BuyerBench addresses this gap by situating the evaluation in procurement decision-making, where the rational supplier selection is computably optimal given scenario parameters. This enables three contributions that BiasBuster cannot provide: (1) a normalized Bias Susceptibility Index measuring deviation from the economic optimum rather than frequency shifts; (2) a controlled between-subject variant design where only the bias-triggering element differs; and (3) statistical power estimation accounting for stochastic LLM output variance. Together these extensions move the question from 'do LLMs exhibit human-like biases?' to 'are LLM procurement agents economically irrational under manipulated market signals?'"

### 4.5 Handling the Status Quo Anomaly

Echterhoff et al.'s anomalous finding — inverse status quo behavior (models prefer non-default options) — is directly testable with BuyerBench's proposed p2-06-status-quo scenario. If BuyerBench also finds anti-status-quo behavior in the procurement domain, this replicates and extends the Echterhoff et al. anomaly with an economic consequence interpretation. If BuyerBench finds normal status-quo bias (models favor the incumbent supplier), this would contradict Echterhoff et al. and generate a domain-moderation finding. Either outcome is publishable and extends the literature.

### 4.6 What BuyerBench Should NOT Replicate

- **Mitigation arm:** Echterhoff et al. owns the mitigation methodology space. BuyerBench should not attempt to replicate or compete with the self-help debiasing contribution. If BuyerBench includes any mitigation discussion, it must explicitly cite and defer to Echterhoff et al. as the primary reference and position BuyerBench as the *measurement* framework (how bad is the problem?) rather than the *remedy* framework (how do we fix it?).
- **Admissions domain:** Avoid any procurement framing that resembles admissions (e.g., "approve/reject vendor applications"). The surface similarity would invite reviewer questions about whether BuyerBench is merely replicating Echterhoff et al. in a different setting.
- **Group attribution bias:** This is Echterhoff et al.'s unique contribution that maps to algorithmic fairness and demographic bias. BuyerBench's scope is economic rationality, not demographic fairness.

### 4.7 Paper Framing Guidance

**Introduction:** Lead with Echterhoff et al. (2024) as the "closest prior work" that motivates BuyerBench. Do not introduce BuyerBench as if Echterhoff et al. does not exist — reviewers will know. Frame the extension as: admissions → procurement (domain + economic structure), consistency → BSI (metric), single-run → stochasticity-aware (methodology).

**Related Work:** Group Echterhoff et al. with Hagendorff et al. (2023) and Binz & Schulz (2023) under "LLM bias in decision tasks." Distinguish by: (a) presence/absence of economic optimality, (b) domain realism for procurement vs. cognitive lab tasks vs. admissions, (c) methodology (controlled variants vs. adversarial probes vs. within-subject conditions).

**Methodology:** Cite Echterhoff et al.'s domain as motivating precedent ("following the high-stakes decision framing of Echterhoff et al., 2024, we evaluate..."), then immediately distinguish the between-subject controlled variant design from their single-condition approach.

**Results:** If BuyerBench's bias effects are smaller than Echterhoff et al.'s (e.g., near-zero BSI vs. their +40 pp framing effect), the likely explanation is domain structure: BuyerBench scenarios include explicit budget constraints, tabular data, and weighted rubrics that activate System 2 reasoning; Echterhoff et al.'s prompts are more open-ended. This is a positive finding: *structured procurement tasks with explicit rubrics appear to suppress the bias susceptibility documented by Echterhoff et al. in less-structured admissions decisions.*

**Discussion / Future Work:** Acknowledge that BuyerBench does not include a mitigation arm. Recommend Echterhoff et al.'s self-help debiasing method as the natural next step for practitioners once BuyerBench identifies bias-susceptible model–bias-type combinations.

---

## 5. BibTeX

```bibtex
@inproceedings{echterhoff2024cognitive,
  title={Cognitive Bias in Decision-Making with {LLMs}},
  author={Echterhoff, Jessica and Liu, Yao and Alessa, Abeer and McAuley, Julian and He, Zexue},
  booktitle={Findings of the Association for Computational Linguistics: {EMNLP} 2024},
  pages={12640--12653},
  year={2024},
  address={Miami, Florida, USA},
  publisher={Association for Computational Linguistics},
  url={https://arxiv.org/abs/2403.00811}
}

@article{samuelson1988status,
  title={Status quo bias in decision making},
  author={Samuelson, William and Zeckhauser, Richard},
  journal={Journal of Risk and Uncertainty},
  volume={1},
  number={1},
  pages={7--59},
  year={1988},
  publisher={Springer}
}

@inproceedings{hagendorff2023human,
  title={Human-like intuitive behavior and reasoning biases emerged in large language models but disappeared in {ChatGPT}},
  author={Hagendorff, Thilo and Fabi, Sarah and Kosinski, Michal},
  booktitle={Nature Computational Science},
  volume={3},
  pages={833--838},
  year={2023},
  publisher={Nature Publishing Group}
}

@inproceedings{binz2023using,
  title={Using cognitive psychology to understand {GPT}-3},
  author={Binz, Marcel and Schulz, Eric},
  booktitle={Proceedings of the National Academy of Sciences},
  volume={120},
  number={6},
  pages={e2218523120},
  year={2023}
}

@inproceedings{jones2022capturing,
  title={Capturing Failures of Large Language Models via Human Cognitive Biases},
  author={Jones, Erik and Steinhardt, Jacob},
  booktitle={Advances in Neural Information Processing Systems},
  volume={35},
  pages={11785--11799},
  year={2022},
  publisher={Curran Associates, Inc.}
}
```
