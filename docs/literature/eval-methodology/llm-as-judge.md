---
type: research
title: LLM-as-Judge — Methods, Biases, and Relevance to BuyerBench
created: 2026-04-03
tags:
  - evaluation
  - llm-judge
  - scoring
related:
  - '[[agent-evaluation-overview]]'
  - '[[evaluation-metrics-taxonomy]]'
---

# LLM-as-Judge — Methods, Biases, and Relevance to BuyerBench

## Overview

LLM-as-judge refers to using a large language model to evaluate the outputs of another model (or agent). This approach is attractive when human annotation is expensive, when outputs are open-ended, or when the evaluation rubric requires natural language understanding. It has become a standard evaluation method since Zheng et al.'s MT-Bench and Chatbot Arena work (2023).

---

## Core Methods

### Pairwise Comparison
Two responses are presented to a judge LLM, which is asked to choose the better one. Used in Chatbot Arena (crowdsourced human voting + LLM judge) and Alpaca Eval. Avoids absolute scoring biases but introduces positional sensitivity.

### Absolute Scoring / G-Eval
A judge LLM assigns a numeric score (e.g., 1–5) to a single response against a rubric. Liu et al.'s G-Eval (2023) uses chain-of-thought prompting to decompose evaluation into explicit criteria before scoring, improving consistency.

### Reference-Based Judging
The judge is given a reference (gold answer or rubric) alongside the response and evaluates adherence, accuracy, or completeness. Less susceptible to self-enhancement bias when reference comes from a different source.

### Critique-and-Score
The judge generates a natural language critique first, then produces a score. This forces the model to surface evidence before committing to a rating. Used in Constitutional AI evaluations and related RLHF pipelines.

---

## Known Biases

### Positional Bias
In pairwise comparisons, LLM judges systematically prefer responses in certain positions (typically the first response presented). Zheng et al. (2023) showed GPT-4's judgment can flip when positions are swapped. **Mitigation**: always run both orderings and average, or use calibrated tie-breaking.

### Verbosity Bias
LLM judges favor longer, more elaborate responses, even when shorter responses are more accurate or appropriate. This is particularly dangerous in procurement contexts where a concise, correct decision should outrank a verbose, hedged one.

### Self-Enhancement Bias
A model asked to judge outputs tends to prefer outputs that match its own style or position. GPT-4 judging GPT-4 outputs, or Claude judging Claude outputs, is susceptible. **Mitigation**: use a different model family as judge, or use multiple judges and aggregate.

### Sycophancy and Authority Bias
Judges may agree with a stated position in the prompt (if one is embedded) rather than evaluating on merit. Authority framing ("an expert says X") can inflate scores for responses aligned with X.

### Rubric Ambiguity
Open-ended rubrics produce high variance. Without structured criteria and explicit scoring anchors, different runs of the same judge model produce inconsistent scores.

---

## Relevance to BuyerBench Scoring

BuyerBench's Pillar 1 (capability) and Pillar 3 (compliance) scoring relies primarily on **objective, deterministic metrics** — task completion, workflow accuracy, policy violation counts. These do not require LLM judges and are not susceptible to judge biases.

However, **Pillar 2 (economic decision quality)** surfaces a subtler need: evaluating *reasoning quality* in addition to the outcome. An agent that selects the correct supplier for the wrong reason (e.g., relying on anchored pricing rather than objective evaluation) should score lower than an agent that correctly reasons through the decision.

For reasoning quality assessment, BuyerBench can optionally employ LLM-as-judge with the following mitigations:
1. Use a **rubric-based absolute scoring** approach (G-Eval style) with explicit criteria for procurement reasoning
2. Use a **different model family** as the judge from the agent under evaluation
3. Apply **double-scoring with swapped orderings** for any pairwise comparisons
4. Report **judge model identity** alongside scores to enable reproducibility

LLM judges are treated as optional auxiliary scorers — not the primary evaluation mechanism — to avoid over-reliance on a single judge's biases.

---

## Key Papers

| Paper | Year | Contribution |
|-------|------|-------------|
| Zheng et al., "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena" | 2023 | Foundational pairwise and GPT-4 judge methodology; bias analysis |
| Liu et al., "G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment" | 2023 | Chain-of-thought rubric decomposition for structured scoring |
| Wang et al., "Large Language Models are not Fair Evaluators" | 2023 | Systematic positional bias; calibration methods |
| Shen et al., "Large Language Model Alignment: A Survey" | 2023 | RLHF, Constitutional AI, and judge-in-the-loop training approaches |

---

## See Also

- [[agent-evaluation-overview]] — broader benchmark taxonomy
- [[evaluation-metrics-taxonomy]] — how metrics map to BuyerBench pillars
