---
type: reference
title: "B1.02 — Framing Effects: Tversky & Kahneman (1981)"
created: 2026-04-16
tags:
  - framing-effects
  - behavioral-bias
  - literature-map
  - pillar2
  - prospect-theory
  - risky-choice
related:
  - '[[b1-01-anchoring-tversky-kahneman-1974]]'
  - '[[b1-03-decoy-effect-huber-payne-puto-1982]]'
  - '[[b1-04-sunk-cost-arkes-blumer-1985]]'
  - '[[BuyerBench-P2-Gap-Analysis]]'
  - '[[strategy-decision-tree]]'
---

# B1.02 — Framing Effects: Tversky & Kahneman (1981)

**Full citation:** Tversky, A., & Kahneman, D. (1981). The framing of decisions and the psychology of choice. *Science*, 211(4481), 453–458. DOI: 10.1126/science.211.4481.453

**BibTeX key:** `tversky1981framing`

---

## 1. Empirical Design

Tversky and Kahneman (1981) demonstrated that preferences between logically equivalent options reverse depending on whether outcomes are described in terms of gains or losses — a direct violation of rational choice theory's description invariance axiom. The canonical demonstration is the **Asian Disease problem**:

> "Imagine that the United States is preparing for the outbreak of an unusual Asian disease, which is expected to kill 600 people. Two alternative programs to combat the disease have been proposed."

**Gain frame (Study 1, N = 152 Stanford undergraduates):**
- Program A: 200 people will be saved (certain)
- Program B: 1/3 probability that 600 people will be saved, 2/3 probability that nobody will be saved

**Loss frame (Study 2, N = 155 University of British Columbia undergraduates):**
- Program C: 400 people will die (certain)
- Program D: 1/3 probability that nobody will die, 2/3 probability that 600 people will die

**The critical structural fact:** Programs A and C are logically equivalent (200 saved = 400 die out of 600). Programs B and D are logically equivalent (1/3 chance of full survival = 1/3 chance nobody dies). Yet:

| Condition | Program chosen | Choice rate |
|---|---|---|
| Gain frame | A (certain survival) | 72% |
| Loss frame | D (risky gamble) | 78% |

A preference reversal of 50 percentage points (72% vs. 22% for the certain option across frames) is produced solely by re-describing the identical outcomes. This violates **description invariance**: rational choice theory requires that logically equivalent descriptions of the same options produce the same preferences.

**Additional demonstrations in the paper:**
1. **Money problem:** Gaining $30 certain vs. 80% chance of gaining $45. Gain frame produced risk-aversion; presented as a two-stage gamble (already guaranteed $30, decide to gamble it), the same expected value produced risk-seeking.
2. **Survival vs. mortality statistics:** Cancer treatment expressed as 5-year survival rate vs. mortality rate produced different preferences even among physicians, surgeons, and statistically trained graduate students.
3. **Insurance framing:** "Probabilistic insurance" (50% chance of full coverage) vs. deductible framing systematically affected willingness to pay despite identical actuarial values.

**N across all studies:** Approximately 150–300 per study, across student and non-student populations (physicians, statistically trained academics). The physician replication is particularly important — expert status did not eliminate framing susceptibility.

**Incentive structure:** Hypothetical throughout. No monetary payoff for choices. The authors note this as a standard limitation; subsequent work has shown framing effects persist under incentivized conditions (see Section 3).

**Theoretical grounding:** The paper connects framing to **Prospect Theory** (Kahneman & Tversky, 1979, Econometrica), specifically to the S-shaped value function with a steeper slope in the loss domain than in the gain domain. Losses loom larger than equivalent gains, producing risk-seeking under loss frames (the gamble is preferred to a certain loss) and risk-aversion under gain frames (the certain gain is preferred to a gamble).

---

## 2. Strengths

1. **Description invariance violation:** The Asian Disease problem constitutes a direct, clean falsification of the standard rationality axiom. Equivalent descriptions yield non-equivalent preferences. This is not merely a "cognitive error" — it is a structural challenge to expected utility theory that generated four decades of theoretical and empirical response.

2. **Expert replication:** The physician and surgeon replication (survival rate vs. mortality rate framing) demonstrates that domain expertise and statistical training do not eliminate the effect. This significantly strengthens external validity for professional decision-making contexts, including procurement.

3. **Multiple domains:** Framing effects appear across public health, financial choice, insurance, and consumer goods domains within the single paper. The breadth argues against paradigm-specific artifacts.

4. **Clean manipulation:** The two framing variants are presented as between-subjects — each participant sees only one version — eliminating within-subject demand effects that would arise if participants saw both frames simultaneously. BuyerBench's controlled-variant design directly inherits this logic.

5. **Publication venue and citations:** Published in *Science*, now one of the most-cited papers in decision science and economics (>40,000 citations per Google Scholar). The framing paradigm is foundational to the behavioral economics literature that produced a Nobel Prize (Kahneman, 2002).

6. **Theory-linked mechanism:** Unlike many behavioral phenomena, framing has a formal theoretical grounding in Prospect Theory's value function. This makes the effect predictable (when it should and should not appear) and allows structural estimation — a methodological advantage BuyerBench can exploit.

---

## 3. Limitations

1. **Student samples, hypothetical stakes:** The primary Asian Disease study used university students with no real-world consequences. While the physician replication partially addresses this, procurement professionals making actual purchasing decisions may exhibit smaller framing effects when stakes are real and when they have institutional accountability.

2. **Binary choice structure:** The Asian Disease problem forces a choice between exactly two options. BuyerBench's p2-02 also has two options, preserving this feature. However, real procurement decisions typically involve multi-option choice sets, where framing effects may interact with decoy effects (see b1-03) in complex ways not captured by the binary paradigm.

3. **Pure equivalence assumption:** The gain and loss frames in the Asian Disease problem are *logically* identical but may not be *psychologically* treated as identical by reflective agents. A model that explicitly computes "200 saved = 400 die" recovers equivalence through deduction — suggesting that framing effects may be smaller in agents (human or AI) with high deliberative processing capacity. This is a testable prediction for BuyerBench across model capability tiers.

4. **Cross-cultural and cross-domain generalization:** While robust in Western academic contexts, framing effects have variable magnitude across cultures, domains, and choice types. Levin, Schneider & Gaeth (1998) identified at least three distinct framing subtypes (risky choice framing, attribute framing, goal framing) with different effect-size profiles and moderators. The original T&K paradigm is specifically risky choice framing.

5. **Demand effects risk:** Despite the between-subjects design, participants who have taken economics or decision theory courses may have prior exposure to the Asian Disease problem or similar demonstrations, potentially suppressing the effect in student samples. For LLMs, training data exposure to this exact problem is a significant confound (see Section 4).

6. **No temporal dynamics:** The experiment is a one-shot choice. Whether framing effects persist, attenuate, or reverse over repeated decisions with feedback is not addressed. This parallels BuyerBench's one-shot-per-run design; the multi-run stochastic approach partially compensates.

---

## 4. Relevance to BuyerBench

### Operationalization: Scenario `p2-02-framing`

BuyerBench scenario `p2-02` operationalizes framing in a procurement-native context, but with a critical design difference from the T&K (1981) paradigm that must be explicitly addressed in the paper.

**The controlled manipulation:**

| Variant | Frame type | Email context |
|---|---|---|
| `FRAMING_GAIN` | Gain (surplus recovery) | VP Finance: Alpha "brings us well within target and frees up a $5k buffer" |
| `FRAMING_LOSS` | Loss (budget exception threat) | Procurement Lead: Beta "puts us $25,000 over our approved quarterly ceiling" — budget exception required |

**The structural difference from the T&K paradigm:**

T&K (1981) tests **risky choice framing** — two options with identical expected values are presented as either certain gains or certain losses. Preferences reverse because the value function is concave in gains (risk-aversion) and convex in losses (risk-seeking).

BuyerBench `p2-02` tests **context/attribute framing** — the underlying economics are not EV-equivalent. Contract Alpha ($150,000) is within budget ($155,000); Contract Beta ($180,000) exceeds budget by $25,000. Contract Alpha is the **objectively optimal choice** under both frames. There is no rational basis for choosing Beta.

This means:
- A **framing-resistant rational agent** chooses Alpha in both variants (BSI = 0.0 across both cells).
- A **framing-susceptible agent** would show *no preference reversal* (unlike the T&K paradigm), but might show *differential confidence, reasoning quality, or response structure* between frames.
- **Binary BSI scoring cannot detect framing susceptibility** in p2-02 unless a model actually chooses Beta — which would be a budget-constraint violation, not a framing effect per se.

In the current BuyerBench results, all successfully executing models chose Alpha in both variants (BSI = 0.0), consistent with this analysis. The framing manipulation was absorbed into reasoning language (GAIN condition reasoning mentions "buffer"; LOSS condition reasoning mentions "budget exception") but did not alter the decision.

**Design implication for the paper:** The paper must distinguish between:
1. **Framing resistance** (the desired finding from p2-02): agents correctly choose Alpha regardless of how the budget situation is framed.
2. **Risky choice framing susceptibility** (what T&K 1981 measured): agents reverse preferences between EV-equivalent risky and certain options under gain/loss presentation.

BuyerBench p2-02 tests (1), not (2). This is a stronger test of rational constrained optimization (budget constraint enforcement regardless of context) but a weaker test of the classic T&K framing paradigm. The paper should position p2-02 as a **context framing** test following Levin, Schneider & Gaeth's (1998) attribute framing subtype — where the framing emphasizes positive vs. negative attributes of an option — rather than claiming to replicate the risky choice paradigm.

**Training data confound for LLMs:** The Asian Disease problem is extremely well-known and almost certainly appears verbatim in LLM training corpora. This means LLM responses to direct Asian Disease prompts cannot be interpreted as genuine framing susceptibility — models may have memorized the "correct" answer from behavioral economics literature. BuyerBench's procurement domain provides a **confound-resistant operationalization**: the specific contract figures ($150k, $180k, $155k budget) and company names (Cordale Operations, AlphaVend Solutions, BetaServ Pro) are novel, preventing pattern-matching to memorized experimental stimuli. This is a major methodological advantage over studies that administer the original T&K problems to LLMs.

### Human benchmark effect sizes for comparison

For paper positioning, the relevant comparison benchmarks from the human literature are:

| Study | Domain | Effect |
|---|---|---|
| Tversky & Kahneman (1981) | Public health (Asian Disease) | 72% vs. 22% certain option across frames (Δ = 50pp) |
| McNeil et al. (1982) | Medical treatment (survival vs. mortality rates) | Physicians: 18% vs. 44% surgery choice across frames |
| Levin & Gaeth (1988) | Consumer goods (beef % lean vs. % fat) | Significant preference reversal under attribute framing |
| Druckman (2001) | Meta-analysis, risky choice framing | d ≈ 0.40 across studies |

BuyerBench's p2-02 BSI measures binary outcome (optimal contract selected vs. not). The current data show BSI ≈ 0.0 for all well-functioning models, suggesting LLMs show strong framing resistance in the context framing paradigm — possibly because the hard budget constraint ($155k ceiling, Beta at $180k) makes the optimal choice transparent regardless of framing language. This null result is itself interpretable and should be reported: **budget-constraint enforcement appears robust to context framing in all tested models**.

### Candidate scenario upgrade for risky choice framing

To test T&K-style risky choice framing, a future `p2-02b` variant would need:
- Two procurement options with **identical expected cost** but different risk profiles (e.g., Option A: $155k fixed-price contract; Option B: $140k base + 10% chance of $150k penalty = EV $155k)
- GAIN frame: "By choosing Option A, you lock in savings relative to last quarter's $180k spend"
- LOSS frame: "By choosing Option A, you incur $15k above the base cost that Option B avoids in 90% of scenarios"
- This would directly replicate the risky choice framing paradigm in a procurement domain and allow a fair comparison to T&K (1981) effect sizes.

### Stochasticity note

The between-subjects controlled-variant design in T&K (1981) is preserved in BuyerBench: each (model × temperature-sample) sees either FRAMING_GAIN or FRAMING_LOSS, never both. With N ≥ 30 runs per cell:
- **Choice consistency within a variant:** Does a model always choose Alpha under GAIN, or does it sometimes flip to Beta? Within-variant consistency measures response stochasticity independent of framing.
- **Cross-variant BSI comparison:** If models show BSI = 0.0 in both variants (as in current data), the framing resistance finding is stochastically stable — not a one-shot artifact.
- **Reasoning trace analysis:** Even when choices are identical, reasoning traces may reveal framing absorption: GAIN-frame traces may use gain-coded language ("saves budget", "creates buffer") while LOSS-frame traces use loss-coded language ("avoids exception", "prevents overrun"). Trace-level coding is a secondary analysis avenue for the paper.

---

## 5. Paper Framing Guidance

When citing this paper in the BuyerBench manuscript:

- **Introduction/motivation:** Use T&K (1981) as the canonical framing reference and the Asian Disease problem as the paradigm-defining demonstration. Establish that this effect is one of the most robust challenges to rational choice theory, motivating its inclusion in the bias battery.

- **Related work:** Distinguish BuyerBench from studies that administer the original Asian Disease problem to LLMs (training data contamination risk). Position p2-02 as a **procurement-domain operationalization of context framing** (Levin et al., 1998 taxonomy) with a novel stimulus set resistant to memorized responses.

- **Methodology:** Cite T&K (1981) for the between-subjects controlled-variant design logic. Note that the original paper's manipulation (semantically re-describing identical outcomes) is preserved in spirit but adapted to a context framing rather than risky choice framing structure. Clearly state what p2-02 tests: whether LLM procurement decisions are influenced by the *affective valence of the budget context* (surplus vs. deficit framing) rather than the underlying economic parameters.

- **Results:** If models show BSI ≈ 0.0 on p2-02 (current finding): frame as framing resistance in context framing — LLMs correctly enforce budget constraints regardless of how the budget situation is described. This is normatively correct behavior. Compare to human expert populations (physicians are NOT immune to framing — McNeil et al., 1982) and note that LLMs may outperform humans on this specific bias type when the optimal choice is constraint-determined.

- **Limitations:** Acknowledge that p2-02 does not test risky choice framing (T&K's specific paradigm). If the paper's scope covers only context framing, scope that clearly. If the paper aims to cover risky choice framing, flag the need for a `p2-02b` upgrade scenario with EV-equivalent risky options.

- **Future work:** Propose the EV-equivalent risky choice scenario (`p2-02b`) as the direct T&K replication in procurement domain, distinct from the context framing test in `p2-02`.

---

## 6. BibTeX Entry

```bibtex
@article{tversky1981framing,
  title   = {The Framing of Decisions and the Psychology of Choice},
  author  = {Tversky, Amos and Kahneman, Daniel},
  journal = {Science},
  volume  = {211},
  number  = {4481},
  pages   = {453--458},
  year    = {1981},
  doi     = {10.1126/science.211.4481.453}
}
```

**Related BibTeX entries to add:**

```bibtex
@article{levin1998framing,
  title   = {All frames are not created equal: A typology and critical analysis of framing effects},
  author  = {Levin, Irwin P. and Schneider, Sandra L. and Gaeth, Gary J.},
  journal = {Organizational Behavior and Human Decision Processes},
  volume  = {76},
  number  = {2},
  pages   = {149--188},
  year    = {1998},
  doi     = {10.1006/obhd.1998.2804}
}

@article{mcneil1982elicitation,
  title   = {On the elicitation of preferences for alternative therapies},
  author  = {McNeil, Barbara J. and Pauker, Stephen G. and Sox, Harold C. and Tversky, Amos},
  journal = {New England Journal of Medicine},
  volume  = {306},
  number  = {21},
  pages   = {1259--1262},
  year    = {1982},
  doi     = {10.1056/NEJM198205273062103}
}
```
