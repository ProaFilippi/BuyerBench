---
type: reference
title: "B1.03 — Decoy Effect (IIA Violation): Huber, Payne & Puto (1982)"
created: 2026-04-16
tags:
  - decoy-effect
  - attraction-effect
  - iia-violation
  - behavioral-bias
  - literature-map
  - pillar2
  - rational-choice-theory
  - consumer-choice
related:
  - '[[b1-01-anchoring-tversky-kahneman-1974]]'
  - '[[b1-02-framing-tversky-kahneman-1981]]'
  - '[[b1-04-sunk-cost-arkes-blumer-1985]]'
  - '[[BuyerBench-P2-Gap-Analysis]]'
  - '[[strategy-decision-tree]]'
---

# B1.03 — Decoy Effect (IIA Violation): Huber, Payne & Puto (1982)

**Full citation:** Huber, J., Payne, J. W., & Puto, C. (1982). Adding asymmetrically dominated alternatives: Violations of regularity and the similarity hypothesis. *Journal of Consumer Research*, 9(1), 90–98. DOI: 10.1086/208899

**BibTeX key:** `huber1982adding`

---

## 1. Empirical Design

Huber, Payne & Puto (1982) provided the first systematic laboratory demonstration that adding a dominated alternative to a choice set can *increase* preference for the option that dominates it — a direct violation of two foundational rationality axioms. The paper challenged both the **regularity assumption** (adding alternatives cannot increase the share of existing alternatives) and the **similarity hypothesis** (additions are predicted to draw disproportionately from similar options).

**The asymmetric dominance manipulation:**

The key manipulation is the introduction of an **asymmetrically dominated decoy** — an option that is inferior to one competitor on all or most attributes (and thus dominated), but is *not* dominated by the other competitor. This asymmetric positioning causes the decoy to "throw" comparative advantage toward the dominating option, increasing its preference share beyond what would be predicted from a simple two-alternative set.

**Experimental structure:** Six different product domains were tested — beer, cars, restaurants, lottery tickets, films, and television sets — to establish cross-domain robustness. For each domain, a two-alternative baseline set was established (A vs. B), then a third asymmetrically dominated alternative (a decoy D_A dominated by A but not B, or D_B dominated by B but not A) was added.

| Condition | Choice set | Prediction (IIA) | Observed |
|---|---|---|---|
| Baseline | {A, B} | — | ~50% each |
| Decoy favoring A | {A, B, D_A} | A% unchanged or decreases | A% *increases* significantly |
| Decoy favoring B | {A, B, D_B} | B% unchanged or decreases | B% *increases* significantly |

**N:** Approximately 153 undergraduate subjects (sample sizes varied across product domains; mean ~25 per condition per domain).

**Incentive structure:** Hypothetical product choices with no monetary stakes or real purchase consequence. Subjects chose which product they would prefer to buy given the presented attributes and prices.

**Manipulation operationalization:** For each domain, attributes were reduced to two quantifiable dimensions (e.g., price and quality rating). Decoys were positioned in attribute space to be dominated by target on both dimensions, or dominated on one dimension and equal on the other (partial dominance), while remaining non-dominated relative to the competitor.

**Effect magnitude:** Preference share for the target option increased by 10–30 percentage points in the decoy-present condition across product categories. The effect was statistically significant across all six domains, establishing cross-domain reliability despite the small within-domain sample sizes. The largest effects appeared for beer (21 pp increase), restaurants (27 pp increase), and lottery tickets (16 pp increase).

**Theoretical framing — two violated axioms:**

1. **Regularity:** In a stochastic choice framework, the probability of choosing any alternative cannot *increase* when new alternatives are added to the set. Adding D_A should leave P(A | {A,B,D_A}) ≤ P(A | {A,B}). Huber et al. demonstrated P(A | {A,B,D_A}) > P(A | {A,B}) — direct regularity violation.

2. **Independence of Irrelevant Alternatives (IIA):** Rational choice theory requires that preference rankings between any two options be unaffected by the presence or absence of a third option (Arrow's IIA). Adding D_A — which is irrelevant in the sense that it would never be chosen if it were truly dominated — should not change A vs. B preference. It does.

**Mechanism hypothesized by authors:** Asymmetric dominance makes the comparison between A and D_A salient, and this comparison is unambiguously in A's favor. This locally generated advantage spills over into the A vs. B comparison through attribute weighting: the A-beats-D_A comparison highlights the attributes on which A is strong, and those attributes then receive higher weight in the subsequent A vs. B evaluation.

---

## 2. Strengths

1. **First systematic IIA violation in consumer choice:** Prior to Huber et al. (1982), IIA was widely assumed to hold in consumer product choices. This paper established that the assumption fails in a predictable, theoretically grounded direction — a contribution that generated over 800 citations and launched a sub-field in consumer behavior and decision science.

2. **Cross-domain replication within a single paper:** Testing six distinct product categories (beer, cars, restaurants, lotteries, films, TVs) within a single experimental design provides cross-domain robustness uncommon in single-paper behavioral demonstrations. This is a methodological strength that addresses paradigm-specificity concerns.

3. **Falsification of two distinct axioms simultaneously:** The paper targets both the regularity assumption and the similarity hypothesis (Tversky, 1972), providing dual-falsification evidence from a single manipulation. This theoretical precision makes the findings harder to explain away as artifacts.

4. **Clean attribute-space operationalization:** By reducing each product domain to two quantifiable attributes and positioning decoys geometrically in attribute space, the paper achieves precise experimental control over the dominance relationship. The attribute-space diagram became the canonical visualization of the decoy effect and is directly adoptable in BuyerBench's weighted-scoring scenario design.

5. **Theoretical generativity:** The paper stimulated a rich follow-on literature including the compromise effect (Simonson, 1989), phantom decoys (Pratkanis & Farquhar, 1992), and formal models of context-dependent preferences (Tversky & Simonson, 1993). The original framework is therefore well-situated in a mature theoretical tradition with known moderators.

6. **Publication venue:** Published in the *Journal of Consumer Research*, the field's premier outlet, and has remained in continuous citation across behavioral economics, marketing, decision science, and now AI behavioral research.

---

## 3. Limitations

1. **Incentive-free design:** All choices were hypothetical; participants faced no real purchase consequences. This raises the standard concern that hypothetical preference elicitation overstates bias relative to real-stakes decisions. Under financial incentives or professional accountability (e.g., a procurement manager buying components that affect manufacturing output), the decoy effect may attenuate.

2. **Small within-domain N:** With approximately 25 participants per condition per domain, individual product-domain results are underpowered. The cross-domain consistency provides empirical credibility, but formal meta-analytic inference across domains was not conducted in the original paper.

3. **Two-attribute product representation:** Collapsing products to two dimensions (price and quality-like rating) is a strong abstraction. Real procurement decisions involve many attributes simultaneously, and the decoy effect's magnitude in high-dimensional attribute spaces is not fully resolved in the literature.

4. **Student sample / lab setting:** Undergraduate convenience samples may not generalize to professional procurement decision-makers with domain expertise, institutional heuristics, or established vendor relationships. Domain experts may be more resistant to decoy attraction because they have richer attribute weighting schemas and external reference points.

5. **Demand effects:** The within-session design (participants saw only one product domain and condition) limits demand effects, but the general awareness among business school students that "irrelevant alternatives" are normatively irrelevant might suppress the effect in more sophisticated populations.

6. **Mechanism underspecification:** The contextual advantage explanation (locally generated dominance spills over into global preference) was proposed but not formally tested against alternatives. Subsequent work (Tversky & Simonson, 1993; Simonson & Tversky, 1992) developed more formal models, but the original paper's mechanism account remained descriptive.

---

## 4. Relevance to BuyerBench

### Operationalization: Scenario `p2-03-decoy`

BuyerBench scenario `p2-03` directly operationalizes the asymmetric dominance manipulation in a procurement-native context — multi-attribute supplier evaluation weighted by quality (60%), delivery reliability (30%), and cost (10%).

**Controlled manipulation:**

| Variant | Supplier set | Key structural feature |
|---|---|---|
| `BASELINE` | SupplierAlpha, SupplierBeta | Two-option choice; Alpha scores 0.816, Beta scores 0.799 |
| `DECOY` | SupplierAlpha, SupplierBeta, SupplierGamma | Gamma added as decoy; dominated by Alpha (quality 0.89 < Alpha 0.92; delivery 0.79 < Alpha 0.88); Alpha 0.833, Beta 0.799, Gamma 0.771 |

**Structural isomorphism with Huber et al. (1982):**

SupplierGamma plays the role of D_A in Huber et al.'s notation — it is dominated by Alpha on all three weighted attributes (quality, delivery, cost), while Beta does not dominate Gamma on delivery (Beta 0.85 > Gamma 0.79) or cost (Beta $31 < Gamma $49). Gamma is thus asymmetrically dominated by Alpha but not by Beta, creating the classic decoy structure.

**Normatively correct behavior:** The optimal choice is SupplierAlpha in *both* variants. The decoy (Gamma) should be a genuine irrelevant alternative — it is fully dominated and would never be the utility-maximizing choice. A rational agent ignores it.

**IIA violation failure modes in LLMs:** An LLM exhibiting the decoy effect would show one or more of the following:
1. **Decoy selection** (BSI = 1.0): Choosing SupplierGamma despite it being fully dominated — a direct failure of rationality not even captured by the classic IIA framing (choosing the dominated option, not just inflating the dominator's share).
2. **Correct-to-wrong shift** (BSI = 1.0): Choosing Alpha in BASELINE but Gamma or Beta in DECOY — a choice reversal driven by the addition of a dominated alternative.
3. **Wrong-to-correct shift**: Choosing Beta in BASELINE but Alpha in DECOY — technically consistent with the decoy mechanism (Gamma boosts Alpha), but this is a correct shift, not a bias.
4. **Execution failure** (BSI = 1.0 due to null decision): The expanded three-supplier prompt causes parsing or reasoning failure in the model, resulting in no valid supplier selection.

**Current BuyerBench results — GPT-4o case:**

In the experimental results, only one model (GPT-4o via OpenRouter) showed a non-zero BSI on the decoy scenario. However, inspection of the raw output reveals this is **most likely an execution/parsing failure, not a genuine IIA violation**:

- BASELINE result: Correctly selects SupplierAlpha (score 1.0, BSI 0.0)
- DECOY result: Returns a null/empty `decisions.supplier` field (score 0.0, BSI 1.0), despite the raw output text appearing to select Alpha

This failure mode is distinct from the Huber et al. (1982) decoy effect. The paper must distinguish between:
- **Genuine IIA violations** (choice reversal from Alpha to Beta, or Gamma selection as a preference): true behavioral bias
- **Execution degradation** (correct reasoning but structured-output parsing failure under expanded prompt): infrastructure confound

**Paper framing implication:** The GPT-4o decoy failure is potentially interesting as an *operational robustness* finding (Pillar 1 capability intersecting with Pillar 2 bias measurement), but it cannot be cited as a behavioral IIA violation without ruling out the execution explanation. At N ≥ 30 runs per model per variant, the proportion of null responses vs. genuine Beta/Gamma selections will distinguish these failure modes. If GPT-4o consistently produces null decisions in DECOY but not BASELINE, the finding is: *adding a third supplier option causes GPT-4o's structured response extraction to fail* — a capability/robustness finding, not a bias finding.

### Ecological validity improvement over the original paradigm

Huber et al. (1982) used simplified two-attribute consumer products (beer quality vs. price, car MPG vs. price). BuyerBench's procurement context offers several improvements:

1. **Three-attribute weighted scoring** (quality 60%, delivery 30%, cost 10%) is a realistic procurement evaluation rubric, increasing ecological validity compared to arbitrary two-attribute product descriptions.
2. **The decoy is operationally realistic** (a supplier with good certifications but worse metrics) — a procurement professional might genuinely encounter such a vendor option, making the irrelevance of Gamma less immediately obvious than a dominated beer brand.
3. **Ground-truth optimality is computable**: Unlike consumer product preference (which is inherently subjective), the weighted evaluation function defines a clear optimal answer, allowing unambiguous BSI scoring.

However, BuyerBench also inherits a key limitation: because the scenario uses explicit numerical weights in the prompt (quality 60%, delivery 30%, cost 10%), a computationally capable model can mechanically score all suppliers and identify Alpha without needing to process contextual cues. This may *suppress* the decoy effect relative to human subjects who intuitively process comparative advantages rather than mechanically computing weighted sums.

### Human benchmark effect sizes for comparison

| Study | Domain | Effect |
|---|---|---|
| Huber, Payne & Puto (1982) | Consumer products (beer, cars, etc.) | 10–27 pp preference share increase for target in decoy condition |
| Tversky & Simonson (1993) | Consumer products | ~20 pp increase; compromise effect comparable in magnitude |
| Heath & Chatterjee (1995) | Meta-analysis (N=50 experiments) | Mean share increase ≈ 12.5 pp |
| Ariely & Wallsten (1995) | Gambles | Effect present but attenuated relative to consumer goods |
| Doyle et al. (1999) | Consumer products | Replicated across UK, US, and Singapore samples |

BuyerBench's BSI measures a binary outcome (optimal supplier chosen or not) rather than a preference share shift. To align with the human literature, the paper should report:
- **P(correct choice | DECOY) vs. P(correct choice | BASELINE)** per model
- **Net share shift** in choice proportions across N ≥ 30 runs per cell
- **BSI_pair** = indicator that a model changed from correct in BASELINE to incorrect in DECOY

### Stochasticity note

The decoy effect in Huber et al. (1982) was measured once per subject, between-subjects. BuyerBench's repeated-run design enables:

1. **Within-model IIA violation rate**: Across N runs of the DECOY variant, what proportion of runs select each supplier? A model with a 20% Gamma selection rate vs. 0% in BASELINE shows a stochastically estimable decoy effect analogous to Huber et al.'s preference share shift.
2. **Choice instability under decoy presence**: If a model shows high variance in DECOY (sometimes Alpha, sometimes Beta, sometimes Gamma) vs. low variance in BASELINE (consistently Alpha), that instability itself is a finding — the decoy creates decision uncertainty even when it doesn't systematically shift preference.
3. **Temperature interaction**: Does higher temperature (more stochastic outputs) amplify or dampen the decoy effect? A prior that higher temperature produces more randomized choices (and thus less systematic bias) predicts a negative temperature × decoy interaction — testable with the multi-temperature factorial design.

### Critical scenario design note for the paper

Unlike the anchoring and framing scenarios, the decoy scenario tests a *structural* rationality property (IIA) rather than a magnitude bias. This has two implications:

1. **The correct interpretation of BSI ≈ 0.0 across all models is different here.** For anchoring, BSI = 0.0 means "not anchored." For decoy, BSI = 0.0 means "IIA holds" — a positive result for rational agency. The paper should frame BuyerBench's p2-03 results as a test of **preference axiom compliance**, not simply bias avoidance.

2. **A theoretically interesting null result:** If all high-capability models show BSI ≈ 0.0 on p2-03, that is strong evidence that LLMs using explicit weighted scoring rubrics comply with IIA in the decoy paradigm. This contrasts with human behavior and suggests that *explicit quantitative prompting may eliminate the decoy effect* — a design intervention finding with practical implications for AI procurement system design.

---

## 5. Paper Framing Guidance

When citing this paper in the BuyerBench manuscript:

- **Introduction/motivation:** Use Huber et al. (1982) as the canonical IIA violation demonstration. Establish that IIA is a core rationality axiom, that its violation in human choice has been robustly documented, and that testing whether LLM agents respect IIA is a natural question for AI behavioral economics research. The procurement domain is particularly relevant because real supply chain decisions routinely involve three-or-more-supplier choice sets where decoy dynamics could emerge.

- **Related work:** Position relative to Ariely & Wallsten (1995) and Heath & Chatterjee (1995) meta-analytic results to establish human baseline effect sizes. Note that no prior LLM behavioral study has specifically tested IIA compliance in procurement contexts. Echterhoff et al. (2024) is the most relevant prior LLM bias study to compare against — their framing is broader but unlikely to include a formal decoy IIA test in a domain with computable optimals.

- **Methodology:** Cite Huber et al. (1982) for the asymmetric dominance manipulation structure and the attribute-space positioning logic. Note that BuyerBench operationalizes the three-supplier decoy structure in a weighted-evaluation procurement context, preserving the key structural feature (Gamma dominated by Alpha, not by Beta) while extending to a professional domain with ground-truth optimality.

- **Results:** 
  - If models show IIA violations (BSI > 0.0 from genuine choice reversals, not execution failures): Compare effect sizes to Huber et al.'s 10–27 pp range; discuss whether the magnitude is smaller (consistent with explicit rubric suppressing the effect) or comparable (suggesting LLMs are as susceptible as human consumers).
  - If all models comply with IIA (BSI ≈ 0.0): Frame as "LLMs with explicit weighted evaluation rubrics demonstrate IIA compliance in the decoy paradigm, in contrast to human behavior." This is a substantively interesting finding — the explicit quantitative prompt may function as a cognitive intervention that eliminates the comparison-driven bias mechanism.
  - Regardless: Distinguish execution failures (null decision output) from genuine IIA violations in the analysis and reporting. GPT-4o's p2-03 failure should be classified as an operational robustness failure, not a behavioral bias, pending N ≥ 30 replication.

- **Limitations:** Acknowledge that the explicit three-attribute weighted rubric in BuyerBench's p2-03 prompt may suppress the decoy effect relative to the human literature, because models can mechanically compute weighted scores rather than relying on comparative heuristics. A future variant without explicit weights (requiring the model to infer attribute importance from context) would provide a more ecologically comparable manipulation to Huber et al. (1982).

- **Future work:** Propose a `p2-03b` variant without explicit percentage weights in the prompt — requiring the model to infer evaluation criteria from contextual signals — to test whether the decoy effect emerges when explicit scoring rubrics are removed. Also propose a multi-option IIA battery testing WARP compliance (see Design Option E.4 in PILLAR2-RESEARCH-02).

---

## 6. BibTeX Entry

```bibtex
@article{huber1982adding,
  title   = {Adding Asymmetrically Dominated Alternatives: Violations of Regularity and the Similarity Hypothesis},
  author  = {Huber, Joel and Payne, John W. and Puto, Christopher},
  journal = {Journal of Consumer Research},
  volume  = {9},
  number  = {1},
  pages   = {90--98},
  year    = {1982},
  doi     = {10.1086/208899}
}
```

**Related BibTeX entries to add:**

```bibtex
@article{tversky1993context,
  title   = {Context-dependent preferences},
  author  = {Tversky, Amos and Simonson, Itamar},
  journal = {Management Science},
  volume  = {39},
  number  = {10},
  pages   = {1179--1189},
  year    = {1993},
  doi     = {10.1287/mnsc.39.10.1179}
}

@article{simonson1989choice,
  title   = {Choice based on reasons: The case of attraction and compromise effects},
  author  = {Simonson, Itamar},
  journal = {Journal of Consumer Research},
  volume  = {16},
  number  = {2},
  pages   = {158--174},
  year    = {1989},
  doi     = {10.1086/209205}
}

@article{heath1995asymmetric,
  title   = {Asymmetric dominance effects: Toward a unified model of brand choice},
  author  = {Heath, Timothy B. and Chatterjee, Subimal},
  journal = {Journal of Consumer Research},
  volume  = {22},
  number  = {4},
  pages   = {520--533},
  year    = {1995},
  doi     = {10.1086/209464}
}
```
