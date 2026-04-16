---
type: reference
title: "B3.05 — Capturing Failures of LLMs via Human Cognitive Biases: Jones & Steinhardt (2022)"
created: 2026-04-16
tags:
  - llm-behavioral-study
  - cognitive-bias-taxonomy
  - failure-analysis
  - anchoring
  - framing
  - availability-heuristic
  - representativeness
  - neurips
  - prior-work
  - literature-map
  - pillar2
  - positioning
related:
  - '[[b3-01-binz-schulz-2023]]'
  - '[[b3-03-hagendorff-2023]]'
  - '[[b3-04-aher-2023]]'
  - '[[b3-06-echterhoff-2024]]'
  - '[[b1-01-anchoring-tversky-kahneman-1974]]'
  - '[[b1-02-framing-tversky-kahneman-1981]]'
  - '[[strategy-decision-tree]]'
---

# B3.05 — Capturing Failures of Large Language Models via Human Cognitive Biases: Jones & Steinhardt (2022)

**Full citation:** Jones, E., & Steinhardt, J. (2022). Capturing Failures of Large Language Models via Human Cognitive Biases. In *Advances in Neural Information Processing Systems* (NeurIPS 2022), Vol. 35, pp. 11785–11799. UC Berkeley.

---

## 1. Empirical Design

Jones & Steinhardt propose that the cognitive bias taxonomy from judgment-and-decision-making (JDM) psychology is a productive *discovery heuristic* for generating LLM failure hypotheses. Their core contribution is methodological: rather than cataloguing failures inductively, they use Kahneman & Tversky's bias catalogue as a hypothesis-generation engine, then test each hypothesis empirically.

**Taxonomy coverage.** The paper maps LLM failures to nine cognitive bias categories drawn from the behavioral economics and cognitive psychology literature:

| Cognitive Bias | Mechanism Tested in LLMs |
|---|---|
| Anchoring | Sensitivity to irrelevant numerical quantities in context |
| Availability heuristic | Over-reliance on surface-frequent patterns from training data |
| Representativeness | Ignoring base rates; prototype-matching over statistical inference |
| Framing effects | Output changes when semantically equivalent inputs are surface-reformatted |
| Ambiguity aversion | Refusal or degraded performance under underspecified inputs |
| Attribute substitution | Substituting an easier question for the target question |
| Confirmation bias | Preferential elaboration of information consistent with a leading premise |
| Functional fixedness | Failure to apply objects/concepts in novel, non-canonical roles |
| Sunk cost fallacy | Persistence in a direction based on prior stated commitment |

**Empirical protocol.** For each bias, the authors construct targeted evaluation sets — adversarial prompt variants designed to trigger the bias — against a held-out task where a "correct" or "consistent" answer exists. Models evaluated: GPT-3 (text-davinci-001/002), Codex, and several FLAN variants. Evaluation is primarily binary: does the model output shift in the bias-predicted direction when the manipulated cue is introduced?

**Key quantitative findings:**
- Anchoring: GPT-3 shows 15–28 pp increase in stated numerical estimates when an irrelevant anchor number appears in context.
- Availability: Error rates correlate significantly with n-gram frequency in training corpora (ρ ≈ 0.4–0.6 across tasks).
- Framing: 20–35 pp preference shifts observed for semantically equivalent question reformulations across QA and classification tasks.
- Representativeness: Models ignore explicit base rate information when prototype descriptions are provided (replicating the Linda problem pattern in open-ended generation).
- Sunk cost: Models preferentially continue a stated flawed plan when prior investment is mentioned (tested via story continuation tasks).

**Sample construction.** Evaluation sets are small (N ≈ 50–200 items per bias category), constructed via hand-crafted adversarial prompt pairs. No multi-run stochasticity modeling. One model configuration per condition.

---

## 2. Strengths

**Taxonomy bridge.** Jones & Steinhardt is the canonical reference for importing the cognitive bias framework into the NeurIPS/ML literature. Prior to this paper, bias analysis in NLP was largely ad hoc (robustness to paraphrase, sensitivity to word order). This paper established cognitive biases as a legitimate organizing principle for LLM failure analysis, enabling a shared vocabulary between behavioral economics and AI evaluation.

**Discovery heuristic value.** The "use bias taxonomy as hypothesis generator" methodology is genuinely productive and reproducible — other researchers can extend the taxonomy to novel bias types without requiring a theoretical model of *why* the bias occurs.

**Multi-bias coverage.** Nine bias types in a single paper, with each empirically instantiated, provides a comprehensive prior-work baseline that a single-bias study cannot match. BuyerBench cites this as evidence that the bias space is well-mapped at the level of existence proofs.

**Model-agnostic framing.** The paper explicitly does not claim to characterize a single model; it characterizes a class of failure modes, making the findings more durable across model generations than papers centered on a specific release.

---

## 3. Limitations

**NLP task domain, not economic decision domain.** The core limitation for BuyerBench positioning is that Jones & Steinhardt tests cognitive biases as *text-processing errors* in NLP tasks (question answering, reading comprehension, story continuation). There is no economic decision structure — no options with quantifiable values, no ground-truth rational optimum, no trade-off under constraint. The "correct" answer is defined by NLP task labels, not by economic rationality.

**No controlled-variant design.** Their adversarial prompts introduce multiple confounds simultaneously (different surface form, different vocabulary, different implied context). There is no between-subject controlled variant where *only* the bias-triggering manipulation differs while the underlying economics remain identical. This means effect sizes cannot be cleanly attributed to the bias mechanism rather than to general prompt sensitivity.

**Single-run, no stochasticity modeling.** Each condition is evaluated with a fixed greedy or low-temperature decode. No temperature sampling, no within-condition variance estimation. There is no statistical model for whether the observed effect sizes exceed sampling noise. A ±5 pp difference with no confidence interval is not a publishable claim in JEBO.

**Small per-category N.** N ≈ 50–200 items per bias type, often hand-constructed, with no pre-registration or power analysis. The dataset is not released in a form that enables easy replication or extension.

**Synchronic snapshot (GPT-3 era).** All tested models predate instruction tuning, RLHF, and chain-of-thought prompting as standard practice. The documented susceptibility magnitudes may not generalize to frontier models (GPT-4, Claude 3.5+). Hagendorff et al. (2023) found mixed trends across generations.

**Taxonomy is a catalogue, not a theory.** The paper identifies that LLMs *exhibit* these failures but does not provide a mechanistic account of *why*. It cannot distinguish between (a) training data contamination (the bias-triggering probe appears frequently in training corpora), (b) RLHF importing human-like heuristics, and (c) the probe genuinely activating a learned cognitive shortcut.

---

## 4. BuyerBench Relevance

### 4.1 Positioning BuyerBench in the Jones & Steinhardt Lineage

Jones & Steinhardt establishes the NeurIPS-tradition precedent that cognitive bias taxonomy is a valid organizing principle for LLM evaluation. BuyerBench extends this in four structurally distinct ways:

| Dimension | Jones & Steinhardt (2022) | BuyerBench |
|---|---|---|
| **Domain** | Generic NLP tasks (QA, classification, generation) | Structured procurement decisions with quantified costs, suppliers, and budgets |
| **Optimality criterion** | NLP task label accuracy | Economically rational choice (computable ground-truth optimal given scenario constraints) |
| **Bias detection method** | Adversarial prompt pairs (multiple confounds) | Controlled variants: between-subject, one manipulation, identical economics |
| **Stochasticity** | Single-run, fixed temperature | N=30 runs per cell; within-cell variance estimation; mixed-effects BSI model |
| **Model coverage** | GPT-3 family + FLAN variants (3–5 models) | 10 frontier models across GPT-4o, Claude 3.5, Gemini 1.5, LLaMA 3.x, Mistral, Qwen, Yi, Cohere |
| **Economic metric** | Accuracy on NLP task labels | Bias Susceptibility Index (BSI) = |P(correct\|bias) − P(correct\|baseline)| / P(correct\|baseline) |
| **Inference level** | Descriptive (biases exist) | Statistical (bias magnitude, inter-model variance decomposition, significance testing) |

### 4.2 The Critical Distinction: Text Errors vs. Economic Decision Errors

Jones & Steinhardt's "anchoring" experiment measures whether a model produces a numerically shifted answer when an irrelevant anchor appears in context. BuyerBench's p2-01 anchoring experiment measures whether a model *selects the wrong supplier* — a binary decision with an objectively correct answer computable from the economic parameters. These are categorically different:

- Jones & Steinhardt: anchoring as input sensitivity in text generation
- BuyerBench: anchoring as choice distortion in structured procurement decisions under constraint

This distinction matters for three reasons:
1. **Economic consequences are real.** A procurement agent choosing the wrong supplier has a quantifiable dollar cost. Text output shifts do not.
2. **Ground-truth is objective.** Given BuyerBench's scenario parameters, there is one and only one rational supplier choice. Jones & Steinhardt's "correct" answers are NLP label conventions.
3. **BSI is a theoretically grounded metric.** The Bias Susceptibility Index normalizes deviation from the rational optimum, enabling cross-bias and cross-model comparison on a common scale. Jones & Steinhardt report raw accuracy deltas with no normalization.

### 4.3 Taxonomy Alignment Table

BuyerBench's current bias battery maps to the Jones & Steinhardt taxonomy as follows:

| BuyerBench Scenario | Jones & Steinhardt Bias Category | Overlap Assessment |
|---|---|---|
| p2-01 anchoring | Anchoring | Direct — same mechanism, different domain and decision structure |
| p2-02 framing | Framing effects | Partial — J&S tests risky choice framing; p2-02 tests attribute/context framing under hard constraint |
| p2-03 decoy effect | Representativeness (partial) | Partial — IIA violation is a distinct mechanism not explicitly named in J&S |
| p2-04 scarcity/urgency | Availability heuristic | Partial — scarcity is a distinct cue type (not frequency-based); J&S availability is training-data-frequency |
| p2-05 sunk cost | Sunk cost fallacy | Direct — J&S documents this in story continuation; BuyerBench tests it in financial re-contracting |
| *p2-06 status quo (proposed)* | Not explicitly covered | Gap — J&S does not cover SQB as a distinct category |
| *p2-07 loss aversion (proposed)* | Framing effects (partial) | Partial — loss aversion is the underlying mechanism for the reflection effect; J&S framing is more surface-level |

**Gap finding:** The decoy effect (IIA violation), status quo bias, and loss aversion as a distinct mechanism from framing are not fully covered in the Jones & Steinhardt taxonomy. BuyerBench adds economic-structure-specific biases that the NLP task framework cannot easily operationalize.

### 4.4 Current BuyerBench Empirical Results vs. Jones & Steinhardt Predictions

Jones & Steinhardt predicts that modern LLMs should exhibit all nine bias types. BuyerBench's current data (N=9–10 models, 2 runs per condition) shows near-zero BSI across most bias types, with a single exception (LLaMA 3.3 70B on p2-04 scarcity). This discrepancy is theoretically meaningful and should be reported prominently:

**Hypothesis: Structured rubric + explicit constraint suppresses cognitive bias activation.** BuyerBench scenarios include explicit budget constraints, tabular supplier data, and weighted rubric scoring instructions. Jones & Steinhardt's adversarial probes are minimally constrained, open-ended, or classification tasks. The structural difference may activate System 2 processing in frontier models that overrides the System 1 heuristics Jones & Steinhardt identifies. This is a positive theoretical contribution: *domain structure and explicit constraints are bias-suppression mechanisms for frontier LLMs — but this finding is fragile and sensitive to prompt design.*

**Implication for paper framing:** Do not frame BuyerBench as replicating Jones & Steinhardt in a new domain. Frame it as testing whether Jones & Steinhardt's NLP-domain findings generalize to structured economic decision-making — and reporting the conditions under which they do not.

### 4.5 Paper Framing Guidance

**Introduction:** "Jones & Steinhardt (2022) demonstrated that LLMs exhibit hallmarks of human cognitive biases across a range of NLP tasks, establishing cognitive bias taxonomy as a productive framework for LLM failure analysis. Their work, however, operates in the text-processing domain where correctness is defined by task labels rather than economic rationality. Whether these patterns persist when the task has a computable economically optimal solution — as in procurement decision-making — remains an open question."

**Related Work:** Cite Jones & Steinhardt alongside Hagendorff et al. (2023) and Binz & Schulz (2023) as the three foundational prior-work anchors. Distinguish by: (a) NLP domain vs. economic domain, (b) adversarial probes vs. controlled variants, (c) single-run description vs. stochasticity-aware inference. Position BuyerBench as extending the J&S *taxonomy* into a new evaluative framework with economic structure and statistical rigor.

**Methodology:** "Following Jones & Steinhardt (2022)'s taxonomy, we operationalize five canonical bias categories — anchoring, framing, decoy effect, scarcity/urgency, and sunk cost — as procurement scenario variants. Unlike J&S's adversarial probe methodology, we use a controlled between-subject design where the economic parameters are held constant across baseline and bias-manipulation conditions."

**Results:** If near-zero BSI is confirmed at N=30 per cell, this is a direct empirical rebuttal of the J&S prediction in the structured economic domain. The headline finding becomes: "Contrary to Jones & Steinhardt (2022)'s findings in the NLP domain, frontier LLMs show near-zero bias susceptibility in structured procurement decisions under explicit constraint — suggesting that domain structure and rubric-guided reasoning are effective bias-suppression mechanisms."

**Discussion:** Explicitly address the "does this mean LLMs are rational?" question. Answer: No — they are constraint-following, not necessarily rational. The absence of bias susceptibility under structured prompting does not generalize to open-ended procurement settings without explicit rubrics.

---

## 5. BibTeX

```bibtex
@inproceedings{jones2022capturing,
  title={Capturing Failures of Large Language Models via Human Cognitive Biases},
  author={Jones, Erik and Steinhardt, Jacob},
  booktitle={Advances in Neural Information Processing Systems},
  volume={35},
  pages={11785--11799},
  year={2022},
  publisher={Curran Associates, Inc.},
  url={https://proceedings.neurips.cc/paper_files/paper/2022/file/4b9088e8a5827e07e9fbfb4f2be7e02e-Paper-Conference.pdf}
}

@article{kahneman2011thinking,
  title={Thinking, Fast and Slow},
  author={Kahneman, Daniel},
  year={2011},
  publisher={Farrar, Straus and Giroux},
  address={New York}
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

@article{tversky1974judgment,
  title={Judgment under uncertainty: Heuristics and biases},
  author={Tversky, Amos and Kahneman, Daniel},
  journal={Science},
  volume={185},
  number={4157},
  pages={1124--1131},
  year={1974}
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
```
