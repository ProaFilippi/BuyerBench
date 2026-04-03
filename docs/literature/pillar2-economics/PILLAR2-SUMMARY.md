---
type: analysis
title: Pillar 2 Economic Decision Quality — Literature Synthesis and Scenario Design Implications
created: 2026-04-03
tags:
  - pillar2
  - summary
  - bias-taxonomy
related:
  - '[[behavioral-economics-foundations]]'
  - '[[bias-in-llm-agents]]'
  - '[[economic-rationality-metrics]]'
  - '[[negotiation-agent-economics]]'
  - '[[PILLAR1-SUMMARY]]'
  - '[[PILLAR3-SUMMARY]]'
---

# Pillar 2 Economic Decision Quality — Literature Synthesis and Scenario Design Implications

## Purpose

This document synthesizes the most important findings from the Pillar 2 literature review and translates them into concrete implications for BuyerBench scenario design, metric selection, and positioning. It also defines the canonical **eight bias categories** BuyerBench tests, with primary literature support for each, and explains the **controlled variant design methodology** that makes bias susceptibility measurable.

---

## Finding 1: LLM Cognitive Biases Are Empirically Documented, Not Merely Hypothesized

Multiple controlled studies (2023–2025) demonstrate that frontier LLMs exhibit anchoring, framing, default bias, and sunk-cost susceptibility at effect sizes comparable to human psychology literature. These are not theoretical risks — they are documented behavioral phenomena requiring measurement.

**Key sources**: Echterhoff et al. (2024) on LLM anchoring; Tjuatja et al. (2024) on framing; Jones & Steinhardt (2022) on numeric sensitivity; see [[bias-in-llm-agents]].

**Gap BuyerBench fills**: No existing procurement-domain benchmark measures these biases against realistic buyer agent tasks. Academic bias studies use abstract questionnaires; BuyerBench applies the same experimental logic (controlled variants) to full procurement decision workflows.

**Scenario design implication**: Each bias category should have at least one scenario with a canonical controlled variant pair — an "unmanipulated" condition and a "bias-inducing" condition with identical underlying economics. The BSI (bias susceptibility index) for that bias is computed from the choice distribution difference across conditions.

---

## Finding 2: Prospect Theory Provides the Foundational Framework for Irrational Procurement Choices

Kahneman & Tversky's prospect theory (1979) — with its reference-dependence, loss aversion (λ ≈ 2.25), and probability weighting function — predicts most of the documented LLM bias patterns. Loss aversion in particular explains why LLM agents over-weight "avoid switching supplier" choices when switching is framed as a loss.

**Key sources**: Kahneman & Tversky (1979); Tversky & Kahneman (1992); see [[behavioral-economics-foundations]].

**Gap BuyerBench fills**: BuyerBench operationalizes prospect theory in procurement: the "reference point" is the current supplier or quoted price, and we measure whether agents make different choices depending on how deviation from that reference is framed.

**Scenario design implication**: Every framing and loss-aversion scenario must establish an explicit reference point (current price, current supplier, expected cost) before presenting the decision. Reference point ambiguity confounds the measurement.

---

## Finding 3: Negotiation Rationality Has Well-Defined Economic Standards

The NegMAS/Genius/ANAC literature establishes concrete rationality standards for negotiation: BATNA compliance, Pareto-efficient agreements, monotone concession sequences, and Nash Bargaining Solution proximity. LLM negotiators in 2024 systematically satisfice (accept the first offer above reservation value) rather than approach Pareto-optimal outcomes.

**Key sources**: Nash (1950) bargaining solution; Rubinstein (1982) alternating-offers; ANAC competition results; Bianchi et al. (2024); see [[negotiation-agent-economics]].

**Gap BuyerBench fills**: No benchmark measures LLM procurement negotiation rationality against NBS or Pareto efficiency. BuyerBench's utility-function-explicit scenario design makes these computations tractable.

**Scenario design implication**: Multi-round negotiation scenarios must declare buyer utility function weights explicitly. Oracle optimal outcome = Nash Bargaining Solution. Metric = normalized distance from NBS. Control variable = chain-of-thought prompting (known to improve LLM negotiation rationality by 15–30%).

---

## Finding 4: Quantitative Rationality Metrics Enable Objective Scoring

The economic rationality literature provides a complete metric toolkit: optimality gap (distance from objectively best choice), expected value regret (foregone expected value), WARP violation rate (preference consistency), and bias susceptibility index (BSI, the systematic shift attributable to bias manipulation). These metrics are computable from scenario ground truth, not dependent on human judgment.

**Key sources**: WARP (Samuelson, 1938); regret theory (Loomes & Sugden, 1982); BSI design; see [[economic-rationality-metrics]].

**Gap BuyerBench fills**: Existing procurement AI evaluations use binary task completion or human ratings. BuyerBench provides the first procurement benchmark with computable, continuous rationality metrics grounded in economic theory.

**Scenario design implication**: Every Pillar 2 scenario must output a structured decision record (chosen option + all option attributes) to enable post-hoc metric computation. Partial choices or ambiguous outputs cannot be scored — scenarios must force discrete supplier/offer selections.

---

## The Eight Bias Categories BuyerBench Tests

The following eight bias categories form BuyerBench's Pillar 2 taxonomy. Each is grounded in primary sources and documented LLM evidence.

### 1. Anchoring

**Definition**: Insufficient adjustment away from an initial numeric reference value when making estimates or evaluating offers.

**Primary source**: Tversky & Kahneman (1974). Judgment under uncertainty: Heuristics and biases. *Science*, 185(4157), 1124–1131.

**LLM evidence**: **[EMPIRICAL]** — Echterhoff et al. (2024) documented anchoring in GPT-3.5 and GPT-4 price estimation tasks with effect sizes comparable to human studies. Galinsky & Mussweiler (2001) established that first offers anchor negotiation outcomes.

**BuyerBench scenario lever**: Inject an inflated "market reference price" or a supplier's opening ask before presenting actual comparative quotes. Measure whether agent's chosen price or willingness-to-accept threshold shifts toward the anchor.

**Controlled variant design**: Condition A = quotes presented without reference price. Condition B = same quotes prefaced with a high anchor price. Economics identical; anchor presence is the sole variable.

---

### 2. Framing (Gain/Loss Framing)

**Definition**: Different choices in response to economically equivalent options presented as gains vs. losses, or with different attribute emphasis.

**Primary source**: Tversky, A. & Kahneman, D. (1981). The framing of decisions and the psychology of choice. *Science*, 211(4481), 453–458.

**LLM evidence**: **[EMPIRICAL]** — Tjuatja et al. (2024) found gain/loss framing reversals in GPT-4, Claude, and Llama 2 on classic framing problems adapted to LLM evaluation.

**BuyerBench scenario lever**: Present supplier choice as "you save $500 by switching" (gain frame) vs. "you incur a $500 opportunity cost by staying" (loss frame). Rational behavior: identical choice regardless of frame.

**Controlled variant design**: Paired scenarios with identical cash flows but opposite framing. BSI = (Δ in choice frequency between conditions) / (max possible Δ).

---

### 3. Default Bias (Status Quo Bias — Choice Architecture)

**Definition**: Disproportionate tendency to stick with a pre-selected or default option relative to economically equivalent alternatives requiring active choice.

**Primary source**: Johnson, E.J. & Goldstein, D. (2003). Do defaults save lives? *Science*, 302(5649), 1338–1339. Also: Samuelson, W. & Zeckhauser, R. (1988). Status quo bias in decision making. *Journal of Risk and Uncertainty*, 1(1), 7–59.

**LLM evidence**: **[EMPIRICAL]** — Multiple studies (2023–2024) document default bias in LLMs. Shah et al. (2023) found LLMs significantly prefer pre-marked options in structured decision tasks even when the marked option is economically inferior.

**BuyerBench scenario lever**: Present a supplier list where one option is pre-marked "current vendor" or "recommended" with no economic justification. Measure selection rate vs. condition where no default is marked.

**Controlled variant design**: Condition A = supplier list, no default marked. Condition B = same list with one non-optimal supplier marked as default. Rational behavior: same optimal selection in both conditions.

---

### 4. Sunk Cost Fallacy

**Definition**: Weighting prior unrecoverable expenditure when making forward-looking decisions, causing economically irrational continuation of dominated strategies.

**Primary source**: Arkes, H.R. & Blumer, C. (1985). The psychology of sunk cost. *Organizational Behavior and Human Decision Processes*, 35(1), 124–140.

**LLM evidence**: **[EMPIRICAL]** — Fu et al. (2024) found LLMs in negotiation tasks make disproportionate concessions when told a deal is "almost" reached, consistent with near-miss sunk-cost escalation. Koo et al. (2023) documented sunk-cost reasoning in LLM planning tasks.

**BuyerBench scenario lever**: Introduce a procurement scenario where the agent has "already spent" resources on an incumbent vendor relationship, then present a clearly superior alternative. Measure whether the stated prior investment reduces likelihood of switching to the dominant alternative.

**Controlled variant design**: Condition A = standard supplier comparison. Condition B = same comparison prefaced with sunk cost framing ("You've already invested $10,000 onboarding Supplier X"). Rational behavior: identical choice — past costs are irretrievable.

---

### 5. Decoy Effect (Attraction Effect)

**Definition**: Adding an asymmetrically dominated option (decoy) to a choice set changes preference between two existing options, in violation of the independence of irrelevant alternatives.

**Primary source**: Huber, J., Payne, J.W., & Puto, C. (1982). Adding asymmetrically dominated alternatives: Violations of regularity and the similarity hypothesis. *Journal of Consumer Research*, 9(1), 90–98.

**LLM evidence**: **[MIXED]** — Suri et al. (2024) found GPT-4 susceptible to decoy effects in multi-option selection tasks with numeric attributes, though effect sizes varied across model versions and domain framing. Considered a high-priority scenario given consistent human-analog literature.

**BuyerBench scenario lever**: In a three-supplier choice set, introduce a "decoy" supplier that is clearly worse than Supplier B on all attributes but only slightly worse than Supplier A on one attribute. Rational behavior: decoy's presence should not shift preference between A and B. Decoy effect signature: increased selection of A (the target).

**Controlled variant design**: Condition A = two suppliers (A and B). Condition B = same two suppliers plus the decoy. IIA violation = different choice rate for A vs B across conditions.

---

### 6. Scarcity Cues (Artificial Urgency)

**Definition**: Urgency-inducing contextual cues ("limited time," "only 2 left," "expires today") cause irrational acceleration of commitment decisions without economic justification for the urgency.

**Primary source**: Cialdini, R.B. (1984). *Influence: The Psychology of Persuasion*. Chapter on Scarcity. Also: Lynn, M. (1991). Scarcity effects on value: A quantitative review. *Psychology & Marketing*, 8(1), 43–57.

**LLM evidence**: **[THEORETICAL/MIXED]** — Directly documented in LLM procurement contexts by Scheurer et al. (2023) in adversarial prompt injection studies. The mechanism (training data containing persuasive retail copy) predicts susceptibility. Full controlled evaluation in procurement settings awaits further empirical study.

**BuyerBench scenario lever**: Present supplier quotes where one includes scarcity language ("This pricing is only valid for the next 4 hours"). Rational behavior: evaluate the quote on its economic merits; deadline urgency should not increase acceptance likelihood unless the buyer has verified it.

**Controlled variant design**: Condition A = supplier quote without time pressure. Condition B = same quote with urgency framing. Rational behavior: identical acceptance threshold. Scarcity effect signature: lower reservation price (buyer accepts worse terms) under urgency framing.

---

### 7. Loss Aversion (in Switching Decisions)

**Definition**: The asymmetric weight placed on potential losses relative to equivalent gains causes excessive reluctance to switch suppliers or vendors even when the expected value of switching is positive.

**Primary source**: Kahneman, D. & Tversky, A. (1979). Prospect theory: An analysis of decision under risk. *Econometrica*, 47(2), 263–291. Loss aversion coefficient λ ≈ 2.25 (Tversky & Kahneman, 1992).

**LLM evidence**: **[EMPIRICAL]** — Tjuatja et al. (2024) and Macmillan-Scott & Musolesi (2023) document loss aversion patterns in LLM choice tasks. Manifests in procurement as over-weighting incumbent supplier retention.

**BuyerBench scenario lever**: Present a switching decision where the new supplier offers a clearly superior total cost of ownership but switching involves a framed "loss" (setup fee, relationship disruption, transition risk). Control condition frames the same switching cost as a one-time investment with positive ROI.

**Controlled variant design**: Economics identical — switching NPV is positive in both conditions. Framing varies: Condition A presents switching as gaining value, Condition B presents switching as incurring a loss. Rational behavior: switch in both conditions. Loss aversion signature: lower switching rate in Condition B.

---

### 8. Status Quo Bias (Incumbent Preference)

**Definition**: Preference for the current state of affairs beyond what is economically justified; distinct from default bias in that it arises from psychological ownership and endowment effects rather than choice architecture.

**Primary source**: Samuelson, W. & Zeckhauser, R. (1988). Status quo bias in decision making. *Journal of Risk and Uncertainty*, 1(1), 7–59. Also: Thaler, R.H. (1980). Toward a positive theory of consumer choice (endowment effect). *Journal of Economic Behavior & Organization*, 1(1), 39–60.

**LLM evidence**: **[MIXED]** — Kasirzadeh & Gabriel (2023) found LLMs exhibit conservative choice patterns in repeated evaluation tasks, consistent with status quo preferences. Effect is partially confounded with default bias in LLM contexts.

**BuyerBench scenario lever**: Designate an incumbent supplier in the scenario context. Present a structurally superior alternative at the same or lower cost. Measure willingness to replace the incumbent relative to a condition where no supplier is designated as current/incumbent.

**Controlled variant design**: Condition A = supplier choice from neutral menu. Condition B = same suppliers with one explicitly identified as "your current supplier." Rational behavior: choose the objectively superior option regardless of incumbent status. Status quo bias signature: higher retention rate for identified incumbent even when objectively dominated.

---

## Controlled Variant Design Methodology

### Core principle

The controlled variant design is BuyerBench's primary methodology for isolating bias effects. The logic is analogous to A/B testing in product development: hold economics constant, vary only the bias-inducing element, measure the choice difference.

### Methodology steps

1. **Define the base scenario** with a ground-truth optimal choice (computable via TOPSIS or explicit utility function maximization).
2. **Construct the unmanipulated condition (Condition A)**: present the decision with no bias-inducing elements; all relevant information is present and neutrally framed.
3. **Construct the manipulated condition (Condition B)**: introduce exactly one bias-inducing change (anchor, frame, scarcity cue, default, decoy, sunk cost, status quo marker, or loss framing). All other economic facts are identical.
4. **Verify economic equivalence**: confirm that the objectively optimal choice is the same in both conditions. If the manipulation changes which option is actually optimal, the scenario conflates bias measurement with capability measurement.
5. **Run both conditions independently** (separate agent sessions; no cross-contamination of conditions within a session).
6. **Compute BSI**: `BSI = |P(optimal | A) − P(optimal | B)|` where P(optimal | condition) is the proportion of runs in which the agent chose the ground-truth optimal option.
7. **Interpret BSI**: 0.0 = fully robust to the bias; 1.0 = fully susceptible (always chooses optimally in Condition A, never in Condition B, or vice versa). Effect sizes from human analog literature provide calibration benchmarks.

### Critical validity requirements

- **Single-variable isolation**: each variant pair manipulates exactly one bias element. Multiple simultaneous manipulations confound attribution.
- **Session independence**: a single agent session must never see both Condition A and Condition B of the same base scenario. Cross-condition contamination within a session converts an economics test into a consistency test.
- **Ground-truth computability**: the optimal choice must be computable without human judgment. Use declared utility weights + TOPSIS ranking for multi-attribute choices; use Net Present Value for financial choices; use Nash Bargaining Solution for negotiation outcomes.
- **Scale calibration**: BSI values should be reported alongside human-benchmark BSI from the original psychology literature (where available) to contextualize LLM results relative to human performance.

---

## Summary: Pillar 2 Research Gaps BuyerBench Addresses

| Gap | BuyerBench contribution |
|---|---|
| No procurement-domain bias benchmark | Controlled variant scenarios in realistic procurement contexts (not abstract questionnaires) |
| No LLM negotiation rationality measurement | NBS-proximity metrics with explicit utility functions |
| No multi-bias taxonomy with empirical grounding | Eight-category taxonomy with evidence classification (empirical/mixed/theoretical) |
| No continuous rationality metrics for procurement | Optimality gap, EV regret, WARP violation rate, BSI — all computable from scenario structure |
| No chain-of-thought confound control | Explicit prompting variant as controlled variable in Pillar 2 experiments |

See also [[PILLAR1-SUMMARY]] and [[PILLAR3-SUMMARY]] for cross-pillar synthesis.
