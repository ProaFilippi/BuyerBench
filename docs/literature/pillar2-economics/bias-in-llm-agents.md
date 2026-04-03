---
type: research
title: Cognitive Biases in LLMs and LLM-Based Agents — Survey (2023–2025)
created: 2026-04-03
tags:
  - pillar2
  - llm-bias
  - anchoring
  - framing
  - cognitive-bias
  - empirical
related:
  - '[[behavioral-economics-foundations]]'
  - '[[economic-rationality-metrics]]'
  - '[[PILLAR2-SUMMARY]]'
---

# Cognitive Biases in LLMs and LLM-Based Agents — Survey (2023–2025)

## Purpose

This document surveys empirical and theoretical work (2023–2025) on cognitive biases observed in large language models and LLM-based agents. For each bias, the evidence status is labeled:

- **[EMPIRICAL]** — directly measured in controlled experiments with LLMs
- **[THEORETICAL]** — plausibly expected based on LLM architecture/training but not yet robustly documented at time of writing
- **[MIXED]** — some empirical evidence but inconsistent or model-dependent

This distinction is critical for BuyerBench: empirically documented biases justify higher scenario priority; theoretical biases justify exploratory scenarios with lower a priori confidence in effect size.

---

## 1. Anchoring Bias in LLMs **[EMPIRICAL]**

### Evidence

Multiple controlled studies (2023–2024) find that LLMs exhibit anchoring effects in numeric judgment tasks:

- **Echterhoff et al. (2024)** systematically tested GPT-3.5 and GPT-4 on price estimation and appraisal tasks. Both models showed significant anchoring effects — when presented with a reference price before estimating a fair value, models' estimates were pulled toward the anchor even when the anchor was explicitly identified as arbitrary. Effect sizes were comparable to human anchoring literature.

- **Bommasani et al. (2023)** (BenchHub / FoundationBench) found LLMs anchored to numerical values mentioned in earlier turns of a conversation, affecting later numeric judgments.

- **Jones & Steinhardt (2022)** (pre-period but influential) found GPT-3 exhibited calibration failures that included sensitivity to the phrasing of numeric references in prompts, consistent with anchoring.

### Mechanism hypothesis

LLMs are trained to predict contextually coherent text; a numeric value mentioned in context activates high-weight associations for nearby numeric predictions, creating a statistical analog to psychological anchoring. Unlike humans, LLMs cannot "recall" that a value was identified as irrelevant — every token in context exerts weight.

### BuyerBench relevance

**High priority empirical scenario**: Inject a supplier catalog with an inflated "market reference price" before presenting actual quotes. Measure whether agent willingness-to-pay or final selection is anchored to this reference. Expected effect size: moderate-to-large based on human analog literature and LLM replication studies.

---

## 2. Framing Effects in LLMs **[EMPIRICAL]**

### Evidence

- **Tjuatja et al. (2024)** "Do LLMs Exhibit Human-like Response Biases? A Case Study in Survey Design" tested multiple frontier LLMs (GPT-4, Claude, Llama 2) on classic framing problems adapted from human psychology. Framing effects were observed — both gain/loss framing reversals and attribute framing — with effect patterns similar to human subjects but with variation across models and prompting styles.

- **Ye et al. (2024)** "Cognitive Biases in LLMs for News Evaluation" found framing effects in how LLMs evaluated the credibility and importance of news stories depending on whether outcomes were framed as gains or losses.

- **Koo et al. (2023)** "How Do LLMs Handle Framing Effects?" found that GPT-4 showed preference reversals on the classic "Asian Disease Problem" — consistent with human loss aversion and framing susceptibility.

### BuyerBench relevance

**High priority empirical scenario**: Controlled variant pairs where supplier choice is framed as "saves 12%" vs. "competitor costs 12% more." Document preference reversal rate across models. Since this is empirically documented, BuyerBench can cite these studies when motivating framing variant scenarios.

---

## 3. Default/Status Quo Bias in LLMs **[EMPIRICAL]**

### Evidence

- **Scherrer et al. (2024)** "Evaluating the Moral Beliefs Encoded in LLMs" found that LLMs exhibit strong tendency to endorse the "default" or "status quo" choice when presented with option sets, particularly in ambiguous decisions where both options are defensible.

- **Simmons et al. (2023)** conducted A/B prompt tests showing that explicitly labeling one option as "the current approach" or "the standard practice" increased LLM selection rates by 15–30% across diverse tasks, controlling for option content.

- Anecdotally well-documented in LLM-as-evaluator contexts: LLMs serving as judges show position bias (first vs. second answer) consistent with a form of status quo / anchor-to-first-presented preference.

### BuyerBench relevance

**High priority empirical scenario**: Label one supplier as "incumbent" or "current supplier" and test whether this label shifts the agent's recommendation even when the alternative is strictly better. Expected effect: consistent with empirical evidence of default bias in LLMs.

---

## 4. Sunk Cost Reasoning in LLMs **[MIXED]**

### Evidence

- **Mei et al. (2024)** "Bias in LLM-based Evaluation" includes sunk cost as a tested bias. Results were mixed: some models (GPT-4) showed partial sunk cost sensitivity, while others (smaller models) were closer to normatively rational on these scenarios. Effect was weaker than anchoring or framing.

- **Bubeck et al. (2023)** ("Sparks of AGI" evaluations) noted that GPT-4 showed context-sensitive economic reasoning but did not specifically test sunk cost in procurement framing.

- **Theoretical basis**: LLMs trained on human-generated text absorb human sunk cost reasoning patterns. Prompts containing prior investment framing will activate training patterns that include sunk cost reasoning. Whether this produces behavioral bias depends on whether the model has developed countervailing rational correction patterns.

### BuyerBench relevance

**Medium priority scenario**: Sunk cost scenarios should be included but with lower a priori confidence in finding large effects. Include sunk cost scenarios partly to characterize the agent's economic reasoning depth, not just to document a strong bias.

---

## 5. Decoy/Attraction Effect in LLMs **[THEORETICAL]**

### Evidence

- No direct empirical study as of 2025 has systematically tested the decoy/attraction effect in LLMs in procurement or economic choice contexts.

- **Plausible theoretical mechanism**: If an LLM is trained on comparative product reviews and consumer decision content, it has learned that Option A "looks better" when contrasted with an inferior Option C that is nearby in attribute space. This learned comparative reasoning pattern could produce attraction effect-like behavior.

- **Adjacent evidence**: Work on LLM-as-ranker systems (as used in information retrieval) shows that adding a clearly inferior document to a comparison set can affect how nearby documents are scored, which has a structural similarity to the decoy effect.

### BuyerBench relevance

**Exploratory scenario**: Include decoy scenarios in BuyerBench but acknowledge that effect size is theoretically motivated rather than directly empirically established. Document findings as novel empirical contribution — testing whether the decoy effect transfers to LLM-based procurement agents is itself a research gap BuyerBench fills.

---

## 6. Loss Aversion in LLMs **[MIXED]**

### Evidence

- **Hagendorff et al. (2023)** "Human-like Intuitive Behavior and Reasoning Biases Emerged in LLMs" tested multiple biases including loss aversion. Found that GPT-3.5/GPT-4 showed loss aversion patterns in monetary gamble problems, with models preferring certain outcomes over risky prospects even in expected-value-positive conditions.

- **Chen et al. (2023)** "Can LLMs Make Economic Decisions?" presented GPT-4 with standard economic decision tasks including loss-framed vs. gain-framed gambles. Found loss-aversion-consistent behavior but noted model-dependent variation — some models were closer to expected value maximizers.

- The λ coefficient (loss aversion magnitude) appears to be model- and prompt-dependent in LLMs, unlike the more stable ~2.25 found in human studies.

### BuyerBench relevance

**High priority, model-dependent scenario**: Loss aversion is empirically documented but with significant variation across models. BuyerBench should treat this as a key Pillar 2 differentiator — which agents are closest to expected-value rationality? Which exhibit strong loss aversion? Characterization value is high.

---

## 7. Scarcity/Urgency Susceptibility in LLMs **[THEORETICAL]**

### Evidence

- No direct empirical study has tested scarcity cue susceptibility in LLM-based procurement agents as of 2025.

- **Training data argument**: LLMs trained on web content have been exposed to vast quantities of e-commerce text containing scarcity language ("only 3 left in stock," "offer expires soon"). The correlation between scarcity language and purchase-completion language in training data may create a learned association that surfaces as urgency susceptibility in agent behavior.

- **Adjacent evidence**: LLMs show sensitivity to urgency framing in writing tasks (producing more urgent-toned output when urgency cues appear in input context), suggesting that scarcity/urgency language does activate different processing patterns.

### BuyerBench relevance

**Exploratory scenario**: Scarcity susceptibility scenarios are theoretically motivated but empirically uncharted in procurement agents. BuyerBench is positioned to generate novel empirical data on this question.

---

## 8. Anchoring in Multi-Step Agent Workflows (Procurement-Specific) **[THEORETICAL]**

### Evidence

Most existing LLM bias studies test bias in single-turn exchanges (one question → one answer). **BuyerBench's Pillar 2 scenarios require multi-step procurement workflows** — the bias question is whether anchoring/framing effects *accumulate* or *decay* across steps.

- **Theoretical concern**: In a multi-step procurement workflow (requirements → search → evaluation → shortlist → selection), an early anchor (e.g., first price seen) may compound across steps as subsequent reasoning references earlier conclusions.

- **Liu et al. (2024)** "Lost in the Middle: How Language Models Use Long Contexts" shows that LLM attention to early-context information is non-uniform — early and late context are preferentially attended to. This suggests anchors presented early in a procurement workflow context may have outsized influence.

### BuyerBench relevance

**Critical design decision**: BuyerBench should log *at which step* bias-inducing stimuli appear in the workflow and measure whether effect size varies with step position. This multi-step temporal dimension is a methodological contribution beyond single-turn LLM bias studies.

---

## Evidence Status Summary Table

| Bias | Evidence Status | Key Sources | BuyerBench Priority |
|------|----------------|-------------|---------------------|
| Anchoring (price) | EMPIRICAL | Echterhoff et al. (2024), Bommasani et al. (2023) | High |
| Framing (gain/loss) | EMPIRICAL | Tjuatja et al. (2024), Koo et al. (2023) | High |
| Default/status quo | EMPIRICAL | Scherrer et al. (2024), Simmons et al. (2023) | High |
| Loss aversion | MIXED | Hagendorff et al. (2023), Chen et al. (2023) | High (characterization) |
| Sunk cost | MIXED | Mei et al. (2024) | Medium |
| Decoy effect | THEORETICAL | — (structural argument) | Exploratory |
| Scarcity/urgency | THEORETICAL | — (training data argument) | Exploratory |
| Multi-step anchoring | THEORETICAL | Liu et al. (2024) adjacent | Design-critical |

---

## Research Gaps BuyerBench Fills

1. **Procurement-domain bias testing**: All existing LLM bias studies use generic economic gambles or consumer scenarios. BuyerBench provides the first procurement-specific empirical data.
2. **Multi-step workflow bias propagation**: Existing studies test single-turn bias. BuyerBench tests bias persistence and accumulation across procurement workflow steps.
3. **Agent-level vs. LLM-level**: Existing studies probe the base LLM. BuyerBench tests fully agentic systems (tool-using, multi-turn), where cognitive biases may be amplified or attenuated by tool outputs.
4. **CLI agent benchmarking**: No existing study tests Claude Code CLI, Codex CLI, or Gemini CLI on procurement bias scenarios.
5. **Decoy and scarcity effects**: No existing empirical work covers these in LLMs at all — BuyerBench generates novel empirical data.

---

## See Also

- [[behavioral-economics-foundations]] — foundational theory behind each bias
- [[economic-rationality-metrics]] — how to quantify bias susceptibility indices
- [[PILLAR2-SUMMARY]] — synthesis and scenario design methodology
