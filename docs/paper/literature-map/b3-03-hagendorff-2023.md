---
type: reference
title: "B3.03 — Human-like Intuitive Behavior and Reasoning Biases in LLMs: Hagendorff, Fabi & Kosinski (2023)"
created: 2026-04-16
tags:
  - llm-behavioral-study
  - cognitive-biases
  - system1-system2
  - crt
  - conjunction-fallacy
  - intuitive-reasoning
  - capability-bias-tradeoff
  - nature-human-behaviour
  - prior-work
  - literature-map
  - pillar2
  - positioning
related:
  - '[[b3-01-binz-schulz-2023]]'
  - '[[b3-04-aher-2023]]'
  - '[[b1-02-framing-tversky-kahneman-1981]]'
  - '[[b1-01-anchoring-tversky-kahneman-1974]]'
  - '[[b2-01-incentivized-hypothetical-camerer-hogarth-1999]]'
  - '[[b2-03-within-between-subject-greenwald-1976]]'
  - '[[strategy-decision-tree]]'
---

# B3.03 — Human-like Intuitive Behavior and Reasoning Biases in LLMs: Hagendorff, Fabi & Kosinski (2023)

**Full citation:** Hagendorff, T., Fabi, S., & Kosinski, M. (2023). Human-like intuitive behavior and reasoning biases emerged in large language models. *Nature Human Behaviour*, 7, 1693–1708. DOI: 10.1038/s41562-023-01714-4

**BibTeX key:** `hagendorff2023humanlike`

---

## 1. Empirical Design

Hagendorff et al. (2023) is the most important LLM bias study in a top psychology or behavioral science venue published between Binz & Schulz (2023) and Echterhoff et al. (2024). The paper's central thesis — and its most provocative empirical finding — is that **more capable LLMs exhibit *more* human-like cognitive bias**, not less, suggesting that the alignment training procedures used to make models more human-like in capability also import human-like System 1 heuristics.

### 1a. Task Battery

The paper administers a **nine-task battery** covering three cognitive bias categories, with human data drawn from established published benchmarks:

| Category | Task | Canonical human source |
|---|---|---|
| **Intuitive/Bat-and-ball errors** | Cognitive Reflection Test (3 items: bat-and-ball, lily pad, machine) | Frederick (2005) |
| **Intuitive/Bat-and-ball errors** | Inverse CRT (items designed to elicit correct fast answers) | Adapted from Frederick (2005) |
| **Heuristics & biases** | Conjunction fallacy (Linda problem) | Tversky & Kahneman (1983) |
| **Heuristics & biases** | Base rate neglect (Bayesian probability) | Bar-Hillel (1980) |
| **Intuitive moral reasoning** | Trolley problem variants (personal vs. impersonal harm) | Thomson (1985); Greene et al. (2001) |
| **Intuitive moral reasoning** | Crying baby dilemma | Greene et al. (2001) |
| **Social heuristics** | Dictator game / ultimatum game variants | Güth et al. (1982) |
| **Social heuristics** | One-shot prisoner's dilemma | Axelrod (1984) |
| **Framing** | Asian Disease risky-choice variants | Tversky & Kahneman (1981) |

The CRT and its inverse are the design's key innovation. The standard CRT has a fast-and-wrong intuitive answer (10 cents) and a slow-and-correct deliberative answer (5 cents). The **inverse CRT** presents structurally identical problems where the fast, intuitive answer *is* correct — allowing the authors to distinguish System 1 activation from simple error-proneness.

### 1b. Experimental Protocol

- **Models tested:** 9 LLMs spanning multiple generations: text-ada-001, text-babbage-001, text-curie-001, text-davinci-001/002/003 (GPT-3 series), GPT-3.5 Turbo, GPT-4, and LLaMA-1 (7B and 13B). This makes it **the most multi-model pre-2024 study** in the behavioral bias literature.
- **Prompting strategy:** Zero-shot prompting with the original human task instructions adapted to natural language. For moral dilemmas, exact wording from the Greene et al. experimental materials is used.
- **Runs per condition:** The paper does not explicitly report systematic multi-run sampling; for most tasks the primary analysis treats a small number of runs (typically N=5–20 per model per condition) as representative. Variance across runs is not the central focus.
- **Comparison benchmark:** Human performance data drawn from original published studies. No fresh human data collection.
- **Temperature:** Not systematically varied.

### 1c. Key Findings

The headline finding, reported prominently and replicated across several task types:

> **GPT-4 shows *more* System 1-type errors than GPT-3 or GPT-3.5 on CRT and conjunction fallacy tasks.**

Specifically:
- On the standard 3-item CRT, GPT-4 gave the intuitive (wrong) answer more frequently than GPT-3 or GPT-3.5 Turbo, even though GPT-4 is substantially more capable by all other benchmarks.
- On the inverse CRT (where the intuitive answer is correct), GPT-4 also outperformed GPT-3 — indicating the effect is genuine System 1 sensitivity, not just error-proneness.
- On the Linda conjunction fallacy, GPT-4 showed higher conjunction error rates than smaller models, again consistent with human-like System 1 reasoning.
- On moral dilemmas, GPT-4 showed higher personal distress responses (consistent with emotional/intuitive processing) compared to GPT-3's more utilitarian, affect-flat response pattern.

The paper's explanatory framework: RLHF and instruction-following alignment training makes models more human-like in general — and this imports human cognitive architecture, including its System 1 shortcuts, not merely its System 2 capabilities.

---

## 2. Strengths

1. **Multi-model comparative analysis — the most important methodological advance over Binz & Schulz.** By testing nine models spanning four generations and two architecture families (GPT-3 series + LLaMA-1), Hagendorff et al. can ask whether bias susceptibility varies with model capability and alignment. The Binz & Schulz N=1 model limitation is directly addressed. For BuyerBench, this paper establishes the precedent for multi-model cross-capability comparison.

2. **The "more capable = more biased" finding is a genuine theoretical contribution.** The counterintuitive capability-bias positive correlation — confirmed via the inverse CRT design that rules out simple error-proneness — is the most important finding in the pre-2024 LLM bias literature for BuyerBench's positioning. It inverts the naive assumption that scaling would reduce bias susceptibility.

3. **Published in Nature Human Behaviour — highest-impact venue in the LLM behavioral science literature.** This is the authoritative citation for the claim that LLMs exhibit human-like intuitive reasoning biases. Any BuyerBench submission that does not cite this paper will receive a reviewer correction.

4. **Inverse CRT design cleverly separates System 1 activation from error-proneness.** The inverse CRT — where the intuitive answer happens to be correct — is an elegant within-paper control. Models that show elevated inverse-CRT accuracy (fast correct answers) alongside elevated standard-CRT errors (fast wrong answers) are exhibiting genuine System 1 sensitivity, not merely random error. This design principle is worth adopting in BuyerBench's unlabeled scenario variants.

5. **Multi-task battery in a single paper.** The nine-task scope establishes methodological credibility that a single-task study cannot. For BuyerBench, this is a useful template: a battery paper carries more weight than a one-bias study even at the same venue.

---

## 3. Limitations

1. **Abstract cognitive tasks — no economic domain, no ground-truth economic optimality.** Like Binz & Schulz, Hagendorff et al. use classic cognitive psychology paradigms (bat-and-ball, Linda problem, trolley problem). These have no ecological validity for AI procurement agents, and "correct" is defined as the logically normative answer, not as an economically optimal decision in a consequential real-world context.

2. **No controlled-variant design for bias isolation.** The paper compares model performance to the normative answer, not model performance under a biased cue versus an identical unbiased baseline. Without controlled variants (BASELINE vs. ANCHOR/SCARCITY/DECOY), the design cannot isolate whether a deviation is caused by the manipulated cue or by general task difficulty, knowledge gaps, or prompt ambiguity.

3. **No systematic stochasticity modeling.** Despite testing multiple models, the paper does not systematically administer N=30 independent runs per (model × task × condition) cell and model within-model variance. This means that single-condition point estimates from smaller run sets may not be statistically reliable, and the observed cross-model differences could partially reflect run-to-run sampling variance rather than genuine cross-model behavioral differences.

4. **GPT-4 training data contamination is a critical confound.** The standard CRT items (bat-and-ball, lily pads, machines) are among the most discussed cognitive psychology tasks in online text, with explicit discussion of both the wrong intuitive answer and the right deliberative answer. GPT-4's training data almost certainly contains thousands of documents that describe the CRT error and its resolution. A model that generates "10 cents" may be reproducing a common pattern in training text that frames the CRT error as the intuitive answer to present — not exhibiting genuine System 1 cognition. The inverse CRT partially mitigates this but cannot eliminate the concern.

5. **Moral dilemma results lack direct procurement relevance.** Trolley problems and crying baby dilemmas are valuable for understanding moral cognition but have no obvious pathway to buyer agent evaluation. Including them in the battery dilutes the economic decision-making focus.

6. **LLaMA-1 models are substantially underperforming relative to GPT-3.5 and GPT-4 on most benchmarks.** Including them in the multi-model comparison conflates capability differences with architecture differences. The performance gradient from text-ada-001 → GPT-4 is not a clean capability scaling curve — it also reflects different generations of alignment training, fine-tuning approaches, and RLHF procedures.

---

## 4. Relevance to BuyerBench

### BuyerBench as a Direct Extension of Hagendorff et al.

| Hagendorff et al. limitation | BuyerBench response |
|---|---|
| Abstract cognitive tasks (CRT, Linda) | Procurement domain with ecological validity for commercial AI buyers |
| No ground-truth economic optimality | Computable optimal supplier choice; BSI normalized against optimum |
| Observational bias detection (no controlled variants) | Between-subject controlled-variant design (BASELINE vs. bias variant) |
| Limited stochasticity modeling | N=30 i.i.d. runs per (model × scenario × variant) cell |
| Training data contamination (canonical CRT items) | Novel procurement stimuli designed to minimize verbatim overlap with bias paradigm descriptions |

### The "More Capable = More Biased" Finding — Critical Positioning Opportunity

Hagendorff et al.'s most important result for BuyerBench is the **capability-bias positive correlation**: GPT-4 shows *more* System 1-type bias than GPT-3 on CRT and conjunction fallacy tasks.

BuyerBench's current experimental data shows a different pattern: **near-zero BSI across most models, including frontier models (GPT-4o, Claude 3.5 Sonnet)**. There are two competing interpretations that BuyerBench must address:

1. **The Hagendorff et al. result does not generalize to procurement domains.** System 1 heuristics may be activated by abstract probability tasks (bat-and-ball) but suppressed in structured procurement decision problems with explicit rubrics, budget constraints, and multi-attribute evaluation. This would be a positive theoretical contribution: domain structure moderates bias susceptibility even in highly capable models.

2. **BuyerBench's current scenarios are biased toward constraint-following.** The explicit rubric structure and named-fallacy suppression in several scenarios (especially p2-05 sunk cost) may account for the near-zero BSI. The proposed unlabeled variants (`p2-01b`, `p2-05b`) are necessary to test whether frontier models are genuinely bias-resistant or merely prompted into explicit constraint-following.

The paper framing should acknowledge the Hagendorff et al. finding directly and test it in the procurement domain: **"Hagendorff et al. (2023) found that capability correlates positively with System 1 bias susceptibility in abstract cognitive tasks. We test whether this relationship holds in economically consequential procurement decisions."**

### Task-Level Overlap with BuyerBench

| Hagendorff et al. task | BuyerBench scenario | Mapping |
|---|---|---|
| CRT (bat-and-ball) | p2-04 scarcity/urgency | Partial — scarcity exploits the same fast-thinking/intuitive heuristic channel that the CRT probes |
| Conjunction fallacy (Linda problem) | No direct analogue (candidate p2-08?) | The conjunction error — treating a detailed description as more probable — could be operationalized as a supplier with a detailed but inferior profile being preferred over a simpler, superior one |
| Asian Disease framing | p2-02 contract framing | Partial — p2-02 tests attribute framing in a constrained choice, not risky-choice framing per Tversky & Kahneman (1981); same caution from b1-02 note applies |
| Moral dilemmas | None (out of scope for procurement) | Not relevant; BuyerBench focuses on economic rather than moral reasoning |

### The "Novel Stimulus" Design Principle

Hagendorff et al.'s reliance on canonical paradigms (bat-and-ball, Linda) creates a training-data-contamination confound that is particularly acute for GPT-4, which was trained on text written *after* CRT items became widely discussed online. BuyerBench's design choice to use procurement-specific stimuli (supplier catalogs, contract terms, market pricing) rather than canonical psychology tasks is directly motivated by this limitation.

For the BuyerBench methodology section, explicitly state:

> "Following Hagendorff et al. (2023), who noted the training-data contamination risk inherent in canonical cognitive psychology paradigms, BuyerBench scenarios were constructed from novel procurement contexts to minimize the probability that any model has been trained on documents describing the correct response to the specific manipulated cue."

### The Inverse CRT Design Principle — Applicable to BuyerBench

The inverse CRT — structurally identical to the standard CRT but with the intuitive answer being correct — is a powerful within-paper control. BuyerBench could adopt an analogous **"inverse bias" control variant**: a scenario where the most superficially compelling choice (the one that triggers the heuristic) is also the economically optimal choice. A model that shows elevated selection of the optimal choice in the bias-aligned variant relative to the baseline would provide a within-study control ruling out the alternative hypothesis that observed BSI=0 reflects prompt compliance rather than economic reasoning.

---

## 5. Paper Framing Guidance

When citing this paper in the BuyerBench manuscript:

- **Introduction:** Use Hagendorff et al. as the anchor citation for the "more capable = more biased" counterintuitive finding: "Hagendorff et al. (2023) found, in a Nature Human Behaviour study, that more capable LLMs (GPT-4) exhibited *more* human-like System 1 biases than less capable models — suggesting that alignment training imports human cognitive shortcuts alongside human-like capabilities." This frames BuyerBench's question: does this pattern hold in procurement domains?

- **Related Work:** Position BuyerBench as extending Hagendorff et al. along the four dimensions above (domain specificity, economic scoring, controlled variants, stochasticity modeling). Note explicitly that Hagendorff et al. is the most multi-model pre-2024 study in the behavioral bias literature, and that BuyerBench updates the model set to the current frontier (GPT-4o, Claude 3.5/3.7, Gemini 1.5 Pro, Llama 3.x).

- **Methodology:** If BuyerBench adopts an inverse-bias control variant, cite Hagendorff et al.'s inverse CRT as the design inspiration.

- **Results:** If BuyerBench finds near-zero BSI in frontier models, cite Hagendorff et al.'s positive capability-bias correlation as a prior finding that BuyerBench *tests in a new domain* and finds does not generalize to structured procurement decisions. This is a positive theoretical contribution — domain structure moderates the System 1 activation that Hagendorff et al. document in abstract tasks.

- **Discussion:** If BuyerBench finds a positive capability-bias relationship in some scenarios (e.g., scarcity/urgency), cite Hagendorff et al. as supporting evidence that alignment does not uniformly suppress bias susceptibility. If BuyerBench finds a negative or null capability-bias relationship, frame this as a domain-specificity finding: procurement tasks with explicit structure may suppress the intuitive-reasoning channel that CRT tasks activate.

---

## 6. BibTeX Entry

```bibtex
@article{hagendorff2023humanlike,
  title   = {Human-like Intuitive Behavior and Reasoning Biases Emerged in Large Language Models},
  author  = {Hagendorff, Thilo and Fabi, Sarah and Kosinski, Michal},
  journal = {Nature Human Behaviour},
  volume  = {7},
  pages   = {1693--1708},
  year    = {2023},
  doi     = {10.1038/s41562-023-01714-4}
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

@article{tversky1983extensional,
  title   = {Extensional versus Intuitive Reasoning: The Conjunction Fallacy in Probability Judgment},
  author  = {Tversky, Amos and Kahneman, Daniel},
  journal = {Psychological Review},
  volume  = {90},
  number  = {4},
  pages   = {293--315},
  year    = {1983},
  doi     = {10.1037/0033-295X.90.4.293}
}

@article{greene2001fmri,
  title   = {An {fMRI} Investigation of Emotional Engagement in Moral Judgment},
  author  = {Greene, Joshua D. and Sommerville, R. Brian and Nystrom, Leigh E. and Darley, John M. and Cohen, Jonathan D.},
  journal = {Science},
  volume  = {293},
  number  = {5537},
  pages   = {2105--2108},
  year    = {2001},
  doi     = {10.1126/science.1062872}
}

@article{stanovich2000individual,
  title   = {Individual Differences in Reasoning: Implications for the Rationality Debate},
  author  = {Stanovich, Keith E. and West, Richard F.},
  journal = {Behavioral and Brain Sciences},
  volume  = {23},
  number  = {5},
  pages   = {645--665},
  year    = {2000},
  doi     = {10.1017/S0140525X00003435}
}
```
