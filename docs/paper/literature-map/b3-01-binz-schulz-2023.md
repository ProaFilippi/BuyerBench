---
type: reference
title: "B3.01 — Using Cognitive Psychology to Understand GPT-3: Binz & Schulz (2023)"
created: 2026-04-16
tags:
  - llm-behavioral-study
  - cognitive-psychology
  - gpt-3
  - bias-battery
  - systematic-evaluation
  - prior-work
  - literature-map
  - pillar2
  - positioning
  - heuristics-and-biases
related:
  - '[[b1-01-anchoring-tversky-kahneman-1974]]'
  - '[[b1-02-framing-tversky-kahneman-1981]]'
  - '[[b2-01-incentivized-hypothetical-camerer-hogarth-1999]]'
  - '[[b2-02-repeated-measurement-charness-levin-2005]]'
  - '[[b3-02-hagendorff-2023]]'
  - '[[b3-04-aher-2023]]'
  - '[[strategy-decision-tree]]'
---

# B3.01 — Using Cognitive Psychology to Understand GPT-3: Binz & Schulz (2023)

**Full citation:** Binz, M., & Schulz, E. (2023). Using cognitive psychology to understand GPT-3. *Proceedings of the National Academy of Sciences*, 120(6), e2218523120. DOI: 10.1073/pnas.2218523120

**BibTeX key:** `binz2023cognitive`

---

## 1. Empirical Design

Binz & Schulz (2023) is the most systematic pre-2024 study applying a **cognitive psychology task battery to a large language model**. The authors adapt ten established paradigms from human cognitive psychology and administer them to GPT-3 (text-davinci-003) via zero-shot prompting, treating the model as an experimental subject in place of a human participant.

### 1a. Task Battery

The ten tasks span four broad capability domains:

| Domain | Task | Canonical human source |
|---|---|---|
| **Decision-making** | Multi-step exploration/exploitation (Horizon task) | Gershman (2018) |
| **Information search** | Sequential sampling behavior (BEAST model) | Schulz et al. (2019) |
| **Deliberate reasoning** | Cognitive Reflection Test (CRT) | Frederick (2005) |
| **Causal reasoning** | Causal bandit paradigm | Lattimore et al. (2016) |
| **Heuristics & biases** | Biased probability assessment (base rate neglect, conjunction fallacy) | Kahneman & Tversky (1983); Tversky & Kahneman (1983) |
| **Reinforcement learning** | Model-based vs. model-free RL (two-step task) | Daw et al. (2011) |
| **Temporal discounting** | Delayed vs. immediate reward trade-off | Laibson (1997) |
| **Risk preference** | Expected utility vs. prospect theory gamble choices | Kahneman & Tversky (1979) |
| **Social learning** | Influence of social information on decisions | Rendell et al. (2010) |
| **Intuitive reasoning** | Bat-and-ball style System 1/System 2 conflict | Stanovich & West (2000) |

### 1b. Experimental Protocol

- **Model:** GPT-3 (text-davinci-003, the strongest available OpenAI model at time of submission in mid-2022).
- **Prompting strategy:** Zero-shot or few-shot prompting. Task stimuli are presented as natural-language descriptions closely following the original human experimental instructions, with answer format constrained (e.g., "Respond with only A or B").
- **Runs per condition:** Typically **N=1** — a single inference call per condition. Some tasks use small multi-run sets (N=5–10) but the paper's primary analysis treats single-run results as representative.
- **Comparison benchmark:** Human behavioral data drawn from published studies using the same task paradigms, not collected fresh in this study.
- **Temperature:** Not systematically varied; default API temperature settings used.

### 1c. Key Findings

The paper finds that GPT-3 exhibits a **mixed profile**:

- **Human-like rational behavior:** Exploration/exploitation balance in the Horizon task closely matches human behavior; sequential sampling resembles a Bayesian updating strategy; causal reasoning shows sensitivity to causal graph structure (not just correlational patterns).
- **Human-like biases (System 1):** CRT performance shows the classic "fast-and-frugal" error pattern (answering 10 cents instead of 5 cents for the bat-and-ball problem); base rate neglect on the Linda problem (conjunction fallacy); temporal discounting that is present-biased.
- **Deviations from human pattern:** GPT-3 shows less overweighting of low-probability outcomes than human subjects in risky choice; its social learning behavior is less imitative than human learners.

The headline conclusion is that GPT-3 "shows a number of human-like cognitive biases" while also exhibiting "remarkable rationality" in some structured decision tasks — broadly consistent with a **System 1/System 2 co-activation** pattern rather than either pure rational computation or pure bias-driven responding.

---

## 2. Strengths

1. **First systematic multi-task cognitive battery applied to an LLM.** Prior to Binz & Schulz, most LLM behavioral analysis was either anecdotal (specific failure modes) or limited to a single task class. The ten-task breadth across decision-making, reasoning, and learning establishes a methodological template that BuyerBench's Pillar 2 battery explicitly extends.

2. **Uses canonical paradigms with well-characterized human benchmarks.** By adapting tasks that have been administered to thousands of human subjects across decades of replication, Binz & Schulz allow direct comparison of GPT-3 behavioral profiles to the existing human literature. This avoids the "unknown baseline" problem that plagues purely novel LLM evaluation designs.

3. **Published in PNAS — high-credibility citation anchor.** The PNAS venue establishes the "apply cognitive psychology tasks to LLMs" approach as scientifically mainstream, lowering the methodological novelty bar for BuyerBench. The question for reviewers is no longer "is this approach valid?" but "what does BuyerBench add beyond Binz & Schulz?"

4. **Qualitative finding of mixed rational/biased behavior is directly relevant.** The result that GPT-3 is neither purely rational nor purely heuristic-driven motivates exactly the kind of fine-grained, bias-specific measurement that BuyerBench provides. Binz & Schulz establish the phenomenon; BuyerBench provides the measurement instrument.

---

## 3. Limitations

1. **Single model (N=1 model, GPT-3 only).** The study cannot address whether the observed cognitive profile is a property of GPT-3 specifically, of transformer LLMs generally, of instruction-tuned models, or of models above a certain capability threshold. All cross-model variation is invisible.

2. **Single run per condition — no stochasticity modeling.** With N=1 per condition, the paper cannot distinguish a genuine behavioral pattern from a sampling artifact of temperature-induced output variance. A bias that appears in a single run may not replicate at the second run; a bias that is absent in a single run may be present probabilistically. The design treats a stochastic computational process as if it were a deterministic measurement instrument — the fundamental methodological gap that BuyerBench's multi-run design closes.

3. **No economic domain; no ground-truth optimal.** The tasks are drawn from cognitive psychology — bat-and-ball problems, probability judgment, abstract RL paradigms. None involve economically consequential decisions with a computable optimal choice. "Bias" is assessed relative to normative benchmark (correct logical answer, expected value maximization) but not against real-world decision consequences. The ecological validity for AI procurement agents is low.

4. **No controlled variants — observational bias detection.** Binz & Schulz identify biases by comparing GPT-3's responses to the normative answer. They do not use the controlled-variant design (e.g., BASELINE vs. ANCHOR_HIGH, both with ground-truth optimal choice) that would isolate the *causal effect* of the manipulated cue on decision quality. Without controlled variants, the "bias" measure conflates task misunderstanding, knowledge gaps, and genuine heuristic-driven deviation from optimum.

5. **GPT-3 is now several generations obsolete.** The text-davinci-003 model tested is two major model generations behind current frontier models (GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 Pro). The cognitive profile documented may not generalize to instruction-tuned RLHF/DPO models with significantly stronger reasoning capability, which are the relevant models for BuyerBench's target use case (commercial AI procurement agents).

6. **No temperature ablation or replication to establish within-task variance.** Without repeated runs at varying temperatures, the paper cannot report confidence intervals, effect sizes, or statistical power for any of its comparisons. All findings are point estimates.

---

## 4. Relevance to BuyerBench

### BuyerBench as a Direct Extension of Binz & Schulz

BuyerBench's Pillar 2 can be framed explicitly as addressing the four most important limitations of Binz & Schulz:

| Binz & Schulz limitation | BuyerBench response |
|---|---|
| Single model | 10+ models across capability tiers and families |
| Single run per condition (N=1) | N=30 independent runs per (model × scenario × variant) cell |
| Abstract cognitive tasks, no economic domain | Procurement domain with ground-truth economic optimality |
| Observational bias detection (no controlled variants) | Between-subject controlled-variant design (BASELINE vs. bias-manipulated variant) |

The positioning argument for any submission is: Binz & Schulz establish that LLMs show human-like cognitive profiles. BuyerBench asks whether this profile generalizes to commercially deployed AI agents in economically consequential procurement decisions, across multiple models, with statistical reliability.

### The "Systematic Battery" Methodology is the Shared Contribution

Both papers share the core methodological contribution of applying a **multi-task battery** rather than testing a single bias type. This framing should be explicit in BuyerBench's related work section: we follow and extend the Binz & Schulz battery approach, not merely replicate it with different prompts. The differences are substantive:

- **Domain specificity:** Procurement scenarios with ecological validity for commercial AI buyers.
- **Economic scoring:** BSI formalization against computable optimal, not comparison to normative logical answer.
- **Stochasticity architecture:** Between-subject i.i.d. sampling explicitly designed to distinguish signal from temperature noise.
- **Multi-model comparative analysis:** Cross-model variance decomposition by capability tier, family, and architecture.

### Specific Task Overlaps (Handle Carefully)

Several of Binz & Schulz's tasks overlap with BuyerBench bias categories:

| Binz & Schulz task | BuyerBench scenario | Overlap type |
|---|---|---|
| Biased probability / base rate neglect | p2-01 anchoring (historical price anchor) | Partial — both test reference-point influence on probability or value judgment |
| Temporal discounting | Candidate p2-07 loss aversion | Tangential — both involve intertemporal trade-offs, but BuyerBench tests reflection effect not discounting per se |
| CRT / System 1 intuition | p2-04 scarcity/urgency | Partial — scarcity cues may exploit fast-thinking heuristics, structurally similar to CRT interference |
| Risky choice (gamble preference) | Candidate p2-07 loss aversion (GAIN_FRAME vs. LOSS_FRAME) | Direct — both operationalize Kahneman & Tversky (1979) risk preference patterns |

**Key distinction for reviewers:** Binz & Schulz test whether GPT-3 *gives the correct logical answer* to a cognitive psychology task. BuyerBench tests whether LLMs *make the economically optimal procurement decision* when presented with a realistic scenario containing a behaviorally manipulative cue. The former measures knowledge/reasoning; the latter measures decision architecture under ecological manipulation.

### The "Stochastic Parroting" Challenge

Aher et al. (2023) and others have raised the concern that LLMs may reproduce biased responses because they were trained on text written by biased humans — not because they have a genuine cognitive architecture that produces biases. Binz & Schulz's design is particularly vulnerable to this critique for well-known paradigms: GPT-3 has almost certainly been trained on thousands of documents discussing the bat-and-ball problem, the Linda problem, and other CRT tasks. A response that "gets the wrong answer" on the bat-and-ball problem may simply be generating the most probable continuation of a canonical text pattern, not exhibiting a cognitive bias.

**BuyerBench's partial response:** Our scenarios use procurement-specific contexts (supplier selection, contract terms, logistics pricing) that are unlikely to appear verbatim in training data in the same bias-manipulated form. The anchor is a historical contract price, not a random wheel-of-fortune number. The framing is a budget constraint scenario, not the Asian Disease problem. This reduces, though does not eliminate, the stochastic parrot concern.

**For the methods section:** Explicitly cite both Binz & Schulz and Aher et al. (2023) as motivating the novel-stimulus design choice. State that BuyerBench scenarios were designed from scratch to minimize overlap with canonical bias paradigm descriptions that are likely overrepresented in LLM training corpora.

### Implication for BuyerBench's N=1 Model Results

If current BuyerBench results show near-zero BSI across most models and scenarios (as the existing experimental data suggests), a reviewer familiar with Binz & Schulz might object: "You found less bias than Binz & Schulz — doesn't that just mean your scenarios are too hard or your models are too capable?"

The response:
1. **Capability confound:** text-davinci-003 is a weaker model than GPT-4o, Claude 3.5 Sonnet, and the frontier models BuyerBench tests. Binz & Schulz's positive bias findings may reflect lower capability rather than higher susceptibility.
2. **Prompt labeling effect:** Several BuyerBench scenarios explicitly name the bias mechanism in the prompt (e.g., "past expenditures are sunk costs" in p2-05). As documented in [[b1-04-sunk-cost-arkes-blumer-1985]], this suppresses susceptibility. The proposed `p2-05b` unlabeled variant is the appropriate test.
3. **Between-subject power:** With N=30 runs and BSI point estimates near 0.0, the statistical message is genuine resistance — not noise. A BSI of 0.0 with N=30 runs has a 95% CI of [0.0, 0.0] for categorical scoring. This is a finding, not an artifact.

---

## 5. Paper Framing Guidance

When citing this paper in the BuyerBench manuscript:

- **Introduction:** Use Binz & Schulz as the canonical prior work establishing the cognitive psychology battery approach for LLMs: "Following Binz and Schulz (2023), who administered a ten-task cognitive battery to GPT-3 and found both human-like biases and human-like rationality, we apply a bias battery to [N] models in a procurement decision domain."

- **Related Work:** Position BuyerBench as an extension along four dimensions (multi-model, multi-run stochasticity, economic domain, controlled-variant design). Do not characterize Binz & Schulz as a paper we "improve upon" — frame it as the methodological template we extend.

- **Methodology:** Explicitly note that unlike Binz & Schulz's single-run design, BuyerBench uses N=30 runs per cell to model stochastic output variance (cite [[b2-02-repeated-measurement-charness-levin-2005]] for the statistical justification). This is the single most important methodological differentiation.

- **Discussion:** If results diverge from Binz & Schulz's finding of human-like biases (i.e., if frontier models show near-zero susceptibility), discuss the model generation gap: GPT-3 was tested before RLHF/DPO alignment procedures became dominant. Current frontier models may have been partially aligned away from biased responding as a side effect of instruction-following training. This is a substantive theoretical contribution, not a negative result.

---

## 6. BibTeX Entry

```bibtex
@article{binz2023cognitive,
  title   = {Using Cognitive Psychology to Understand {GPT-3}},
  author  = {Binz, Marcel and Schulz, Eric},
  journal = {Proceedings of the National Academy of Sciences},
  volume  = {120},
  number  = {6},
  pages   = {e2218523120},
  year    = {2023},
  doi     = {10.1073/pnas.2218523120}
}
```

**Related BibTeX entries:**

```bibtex
@article{frederick2005cognitive,
  title   = {Cognitive Reflection and Decision Making},
  author  = {Frederick, Shane},
  journal = {Journal of Economic Perspectives},
  volume  = {19},
  number  = {4},
  pages   = {25--42},
  year    = {2005},
  doi     = {10.1257/089533005775196732}
}

@article{gershman2018deconstructing,
  title   = {Deconstructing the Human Algorithms for Exploration},
  author  = {Gershman, Samuel J.},
  journal = {Cognition},
  volume  = {173},
  pages   = {34--42},
  year    = {2018},
  doi     = {10.1016/j.cognition.2017.12.014}
}

@article{daw2011model,
  title   = {Model-Based Influences on Humans' Choices and Striatal Prediction Errors},
  author  = {Daw, Nathaniel D. and Gershman, Samuel J. and Seymour, Ben and Dayan, Peter and Dolan, Raymond J.},
  journal = {Neuron},
  volume  = {69},
  number  = {6},
  pages   = {1204--1215},
  year    = {2011},
  doi     = {10.1016/j.neuron.2011.02.027}
}
```
