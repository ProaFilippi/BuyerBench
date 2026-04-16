---
type: reference
title: "B2.03 — Within-Subject vs. Between-Subject Design: Greenwald (1976)"
created: 2026-04-16
tags:
  - experimental-methods
  - within-subject
  - between-subject
  - demand-characteristics
  - sensitization
  - carry-over
  - design-choice
  - literature-map
  - pillar2
  - methodology
  - validity
related:
  - '[[b2-02-repeated-measurement-charness-levin-2005]]'
  - '[[b2-01-incentivized-hypothetical-camerer-hogarth-1999]]'
  - '[[b1-01-anchoring-tversky-kahneman-1974]]'
  - '[[b1-02-framing-tversky-kahneman-1981]]'
  - '[[strategy-decision-tree]]'
---

# B2.03 — Within-Subject vs. Between-Subject Design: Greenwald (1976)

**Full citation:** Greenwald, A. G. (1976). Within-subjects designs: To use or not to use? *Psychological Bulletin*, 83(2), 314–320. DOI: 10.1037/0033-2909.83.2.314

**BibTeX key:** `greenwald1976within`

---

## 1. Empirical Design

Greenwald (1976) is a **methodological analysis paper**, not a primary experiment. It provides a formal framework for choosing between within-subject (repeated-measures) and between-subject experimental designs, and identifies the conditions under which each design is appropriate or inappropriate.

**The central problem Greenwald addresses:**

Within-subject designs assign each participant to multiple experimental conditions in sequence. This dramatically improves statistical power because each participant serves as their own control, eliminating between-person variance from the error term. However, it introduces a family of confounds that between-subject designs avoid. Greenwald systematically categorizes these threats:

### 1a. Demand Characteristics (Primary Concern)

**Demand characteristics** (Orne, 1962) are cues in the experimental environment that convey the study's hypothesis or desired behavior to participants. In a within-subject design, participants observe *multiple conditions by design* — and this multi-condition exposure is itself the most powerful demand characteristic generator:

- A subject who sees both the BASELINE condition (no manipulative cue) and the HIGH_ANCHOR condition (inflated reference price) in the same session can trivially infer that the experiment is studying the effect of price information on judgment.
- Once the hypothesis is visible, subjects may **comply** (trying to confirm what they think the experimenter wants), **counter-comply** (deliberate resistance to the perceived manipulation), or **demand-reduce** (actively discount the cue they now recognize as experimental).
- All three responses contaminate the measured treatment effect relative to what it would have been in a naive single-exposure context.

Greenwald's contribution is formalizing that demand characteristics are not merely an inconvenience: they systematically bias effect size estimates in the direction of the response the participant believes is expected. For bias studies specifically, this means within-subject designs will *understate* susceptibility to familiar biases (subjects resist) and may *overstate* susceptibility to novel framing effects (subjects comply with unusual stimuli they cannot classify as a known paradigm).

### 1b. Carry-Over Effects (Sensitization and Carryover)

**Sensitization** occurs when exposure to one experimental condition permanently alters how a participant responds to subsequent conditions. Greenwald distinguishes two subtypes:

1. **Procedural carry-over:** Familiarity with the task format reduces procedural error in later conditions, producing artificially better performance irrespective of the experimental manipulation (see also [[b2-02-repeated-measurement-charness-levin-2005]]).
2. **Substantive carry-over:** The content of an earlier condition changes the cognitive state (reference point, expectation, affective tone) that a subject brings to a later condition.

For behavioral bias research, substantive carry-over is especially damaging: if a subject first sees a LOW_ANCHOR condition that establishes a low reference price in memory, their response to the HIGH_ANCHOR condition in the same session is not the same as a naive subject's first exposure to the high anchor — the first anchor has already partially anchored their reference point.

**Counterbalancing** (ABBA or Latin-square ordering) controls procedural carry-over but cannot eliminate substantive carry-over when the manipulation involves a reference-point shift, because reference points are cognitively durable and not erased by seeing a different condition afterward.

### 1c. Practice and Fatigue Effects

Within-subject designs conflate condition order with practice/fatigue level. Even with counterbalancing, each participant's session has a start and an end:

- **Practice effects:** Participants improve with task familiarity across trials, independent of the manipulation.
- **Fatigue effects:** Attention and motivation decrease across long sessions.

Both effects create within-session trends that partially confound the comparison between early-administered and late-administered conditions.

### 1d. Greenwald's Design Decision Rule

Greenwald proposes that a within-subject design is appropriate only when **all three** of the following hold:

1. **The manipulation is non-reactive:** Exposure to one condition does not change how participants process subsequent conditions (no sensitization, no carry-over).
2. **Demand characteristics are negligible:** Participants cannot infer the hypothesis from the pattern of conditions, or can infer it but cannot act on that inference in a way that biases results.
3. **Counterbalancing eliminates order effects:** Full counterbalancing is feasible (small number of conditions), and the residual order effects are demonstrably non-systematic.

When any one of these conditions fails, Greenwald recommends a **between-subject design** — despite its reduced statistical power — because the confound-free comparison is scientifically preferable to a statistically powerful but internally invalid one.

---

## 2. Strengths

1. **Taxonomy of within-subject confounds is comprehensive and durable.** Greenwald's framework distinguishes demand characteristics, sensitization, carry-over, practice, and fatigue as distinct threats with distinct mechanisms. This taxonomy has been cited as foundational by behavioral economists, social psychologists, and experimental economists for fifty years, making it a high-credibility anchor for design justification in any empirical paper.

2. **Provides a falsifiable decision rule, not just a heuristic.** The three-condition rule (non-reactive, non-demanding, counterbalanceable) is specific enough to apply mechanically. For bias research in BuyerBench, checking each condition against each bias type produces a principled, documentable design choice — not a vague preference for "cleaner" designs.

3. **The paper is brief, high-authority, and widely understood.** At 7 pages in *Psychological Bulletin*, it is easy to read and cite. Reviewers at behavioral economics journals (JEBO, Experimental Economics) and AI venues (NeurIPS, ICML) are familiar with this foundational text — citing it positions BuyerBench's design choice as standard methodological practice, not an idiosyncratic choice.

4. **Implicitly supports the claim that between-subject designs can produce valid inference with lower N.** By arguing that within-subject designs introduce systematic biases that inflate or deflate effect sizes, Greenwald provides a normative basis for choosing between-subject even at a cost to raw statistical power. A between-subject estimate with honest variance is more scientifically valid than a within-subject estimate contaminated by demand effects.

---

## 3. Limitations

1. **Published in 1976; no discussion of computational agent subjects.** The paper predates any consideration of non-human experimental subjects such as language models. The demand characteristics and carry-over arguments are explicitly framed around human psychological processes (inference about experimenter intent, affective state, fatigue). Direct application to LLMs requires adapting the framework (Section 4 below).

2. **No formal model of the trade-off between bias and variance.** Greenwald describes the qualitative conditions for each design's validity but does not provide a formal statistical model of how much demand-characteristics bias contaminates effect size estimates. This means a reviewer can legitimately ask: "How much does within-subject design inflate bias effect sizes in practice?" The paper cannot answer this quantitatively.

3. **The demand-characteristics concept itself has been debated.** Later work (e.g., Nichols & Maner, 2008) argued that demand characteristics do not reliably produce the pattern of results Orne (1962) described, and that many within-subject designs in social psychology are robust to demand effects. This does not undermine Greenwald's framework for bias battery designs — where the manipulation is precisely the signal participants would most readily perceive — but a reviewer may cite this literature as a counter-argument.

4. **Between-subject designs require larger N.** Greenwald acknowledges this but does not provide power calculation guidance. For BuyerBench, the N=30 runs-per-cell specification (see [[strategy-decision-tree]]) must be justified independently; citing Greenwald establishes the design choice but does not automatically validate the sample size.

---

## 4. Relevance to BuyerBench

### The Core Design Choice

BuyerBench's Pillar 2 evaluation uses **between-subject variant assignment**: for a given bias type and model, each run is assigned to *either* the BASELINE condition *or* the manipulated VARIANT condition (e.g., ANCHOR_HIGH), never both. No single context window ever contains both conditions.

This is the correct design choice under Greenwald's framework, and the justification maps cleanly across his three criteria:

| Greenwald criterion | BuyerBench status | Justification |
|---|---|---|
| Non-reactive manipulation | FAILS for within-subject | An LLM context containing both BASELINE and ANCHOR_HIGH prompts would make the manipulation visible to the model (see demand effects below) |
| Demand characteristics negligible | FAILS for within-subject | In-context contrast between conditions signals the experimental structure; chain-of-thought models may meta-reason about the comparison |
| Counterbalancing eliminates order effects | INAPPLICABLE | LLMs are stationary (no learning, no fatigue) — but the demand-characteristics concern remains even without order effects |

**Conclusion:** The between-subject design is appropriate not because LLMs experience fatigue or practice effects (they do not), but because the *demand-characteristics and sensitization mechanisms have a direct LLM analogue* — detailed below.

### LLM Demand Characteristics: The In-Context Signal Problem

Human demand characteristics arise because participants **infer the hypothesis** from the stimulus pattern and adjust behavior accordingly. For LLMs, an analogous process operates through **in-context pattern recognition**:

1. **Contrastive framing signal.** If a single LLM prompt contains both a neutral baseline version and a manipulated version of a scenario (e.g., "In Scenario A, the historical price is $100k. In Scenario B, the historical price is $180k. Evaluate each."), the contrast between A and B is itself a signal. Chain-of-thought reasoning models (GPT-4o, Claude 3.5 Sonnet, Gemini Pro) are explicitly trained to notice differences and reason about them. A capable model will identify the anchor manipulation, reason about its normative irrelevance, and produce responses that *correct for* the anchor — not because it is economically rational, but because the within-context comparison makes the experimental intent transparent.

2. **Hypothesis-confirmation in reasoning traces.** Models with chain-of-thought outputs may literally generate text like "This appears to be testing whether I would be influenced by the prior price" before rendering a response that carefully ignores the anchor. This behavior produces BSI ≈ 0.0 not because the model is truly bias-resistant, but because the within-context design revealed the manipulation and triggered meta-level correction.

3. **Adversarial calibration.** LLMs trained on RLHF and similar alignment procedures are explicitly rewarded for resisting manipulation, providing helpful responses, and not being "tricked" by adversarial prompts. Placing both BASELINE and ANCHOR_HIGH in the same context may activate this adversarial-resistance training signal, suppressing the measured bias effect entirely.

**The between-subject design avoids all three mechanisms.** Each run sees a single scenario variant in isolation, with no contrastive signal, no visible experimental structure, and no opportunity for meta-level hypothesis-inference. The model must make a procurement decision as presented — not as analyzed against a comparison condition.

### Residual In-Context Demand Effects (Even in Between-Subject)

Even in BuyerBench's between-subject design, some in-context demand signals are present:

- The scenario framing (e.g., "A historical contract with CarrierA was signed at $72,000") makes the potential sunk cost signal explicit.
- Highly capable models may recognize the bias category from the scenario structure even without a comparison condition (e.g., recognizing "this describes sunk cost fallacy" from prior training on behavioral economics texts).

This is the **training data contamination concern** — distinct from Greenwald's demand characteristics but related. The between-subject design addresses Greenwald-style contamination (cross-condition inference within a session) but cannot fully address contamination from training-data exposure to the canonical paradigms. BuyerBench's response is to use procurement-specific scenarios rather than canonical psychology paradigms (the Asian Disease problem, the theater ticket scenario), reducing the probability that the LLM has seen the exact stimulus in training — as documented in individual literature notes for each bias type.

### Why Not Within-Subject for LLMs?

A reviewer might argue: "LLMs don't experience demand characteristics the way humans do — the concerns that motivate Greenwald's recommendation don't apply to computational agents. Therefore, within-subject designs are fine for LLMs, and you're sacrificing statistical power unnecessarily."

The response, grounded in the in-context signal analysis above, is:

1. **LLMs have an *analogous* demand-characteristic mechanism** (in-context contrast inference and adversarial resistance) that produces the same directional bias in effect size estimates as Orne (1962) documented for humans — suppression of true susceptibility when the experimental structure is visible.

2. **The statistical power advantage of within-subject is eliminated for stationary agents.** The power gain from within-subject designs comes from treating participants as their own controls, which removes between-person variance from the error term. For LLMs, "between-run" variance for the same model is pure temperature sampling variance — not between-person heterogeneity. This variance is present in both the within- and between-subject estimator. The within-subject design provides no variance reduction for LLMs because the variance it eliminates (individual differences) does not exist in stationary computational agents.

3. **Between-subject design with N=30 per cell is adequately powered.** As shown in [[b2-02-repeated-measurement-charness-levin-2005]], N=30 independent i.i.d. runs per cell gives ±0.18 BSI confidence interval half-width. The between-subject design's statistical disadvantage relative to within-subject, which is its primary downside in human experiments, does not materialize here because the runs are i.i.d. — not correlated within subjects as in human between-subject studies.

**Conclusion:** Between-subject design is not a concession for LLM experiments — it provides equal statistical information as within-subject (given stationarity) while eliminating the in-context demand signal that would suppress measured bias effects.

### Practical Design Implications

1. **Each run batch for a given (model × scenario × variant) cell must use a fresh context.** No run in the ANCHOR_HIGH batch should share conversation history with any run in the BASELINE batch. API calls should be stateless and non-concurrent within a session.

2. **Prompts should not signal the experimental comparison.** Scenario prompts should not contain language like "unlike the standard market price…" or "despite the prior contract value of $X…" that implicitly flags the manipulation as a deviation from an unstated baseline. The manipulation should appear as ecological background information, not as a contrastive signal.

3. **Do not include chain-of-thought instructions that elicit meta-reasoning about the task.** Instructions like "explain whether any cognitive biases might be affecting your judgment" explicitly invite the model to activate its bias-correction training — a within-prompt demand effect. The scenario prompt should request a procurement decision and a brief business justification, without signaling that bias detection is the evaluation criterion.

4. **Report variant assignment in the methodology section.** Explicitly state that each run is assigned to exactly one variant condition, cite Greenwald (1976) for the design justification, and note that this design eliminates within-session demand characteristic contamination while preserving statistical validity under the i.i.d. stationarity assumption.

---

## 5. Paper Framing Guidance

When citing this paper in the BuyerBench manuscript:

- **Methodology section:** One dedicated paragraph. State that BuyerBench uses a between-subject variant assignment (each model × run sees exactly one variant of each bias scenario, never the comparison condition), cite Greenwald (1976) for the design choice, and briefly note that the within-subject alternative is contraindicated because the contrast between conditions within a single LLM context constitutes a demand characteristic that would suppress measured bias susceptibility via in-context meta-reasoning. Cross-reference with [[b2-02-repeated-measurement-charness-levin-2005]] for the i.i.d. stationarity argument.

- **Limitations section (secondary):** Acknowledge that even the between-subject design cannot fully eliminate in-context demand effects from the scenario framing itself (a model that recognizes the sunk cost paradigm structure from training data may suppress susceptibility). Distinguish this training-data contamination concern from Greenwald-style cross-condition contamination.

- **Discussion:** If models show BSI ≈ 0.0 across bias types, one alternative explanation is that the scenarios are ecologically structured in a way that makes the bias category recognizable to highly capable models, and the between-subject design is insufficient to prevent meta-level correction. This interpretation is testable by the proposed unlabeled scenario variants (e.g., p2-05b without the "sunk costs are irrelevant" constraint, p2-04b with higher-intensity scarcity manipulation).

- **Do not frame the design as "conservative."** Framing between-subject as "we chose a more conservative design to avoid demand effects" implies the design sacrifices sensitivity. For LLMs, it does not (as argued above). Frame it as "the methodologically appropriate design given the demand-characteristic analogue in LLM context-window inference."

---

## 6. BibTeX Entry

```bibtex
@article{greenwald1976within,
  title   = {Within-Subjects Designs: To Use or Not to Use?},
  author  = {Greenwald, Anthony G.},
  journal = {Psychological Bulletin},
  volume  = {83},
  number  = {2},
  pages   = {314--320},
  year    = {1976},
  doi     = {10.1037/0033-2909.83.2.314}
}
```

**Related BibTeX entries:**

```bibtex
@article{orne1962social,
  title   = {On the Social Psychology of the Psychological Experiment: With Particular Reference to Demand Characteristics and Their Implications},
  author  = {Orne, Martin T.},
  journal = {American Psychologist},
  volume  = {17},
  number  = {11},
  pages   = {776--783},
  year    = {1962},
  doi     = {10.1037/h0043424}
}

@article{nichols2008good,
  title   = {The Good-Subject Effect: Investigating Participant Demand Characteristics},
  author  = {Nichols, Austin Lee and Maner, Jon K.},
  journal = {Journal of General Psychology},
  volume  = {135},
  number  = {2},
  pages   = {151--165},
  year    = {2008},
  doi     = {10.3200/GENP.135.2.151-165}
}

@article{charness2005optimal,
  title   = {When Optimal Choices Feel Wrong: A Laboratory Study of Bayesian Updating, Complexity, and Affect},
  author  = {Charness, Gary and Levin, Dan},
  journal = {American Economic Review},
  volume  = {95},
  number  = {4},
  pages   = {1300--1309},
  year    = {2005},
  doi     = {10.1257/0002828054825583}
}

@article{shadish2002experimental,
  title   = {Experimental and Quasi-Experimental Designs for Generalized Causal Inference},
  author  = {Shadish, William R. and Cook, Thomas D. and Campbell, Donald T.},
  journal = {Houghton Mifflin},
  year    = {2002}
}
```
