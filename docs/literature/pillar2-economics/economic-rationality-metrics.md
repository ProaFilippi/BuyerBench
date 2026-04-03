---
type: research
title: Economic Rationality Metrics for Buyer Agent Evaluation
created: 2026-04-03
tags:
  - pillar2
  - metrics
  - rationality
  - optimality-gap
  - preference-consistency
related:
  - '[[behavioral-economics-foundations]]'
  - '[[bias-in-llm-agents]]'
  - '[[negotiation-agent-economics]]'
  - '[[PILLAR2-SUMMARY]]'
---

# Economic Rationality Metrics for Buyer Agent Evaluation

## Purpose

This document defines the quantitative metrics BuyerBench uses to measure economic decision quality in Pillar 2 scenarios. It covers optimality gap, expected value regret, preference consistency (WARP), and bias susceptibility index design, plus the controlled variant experimental methodology for isolating bias effects.

---

## 1. Optimality Gap

### Definition

The **optimality gap** measures how far an agent's chosen option is from the objectively optimal choice, expressed as a normalized percentage of the maximum achievable value.

Let:
- `V(a*)` = value of the optimal choice (computed by the benchmark oracle)
- `V(a_agent)` = value of the agent's chosen option
- `V(a_worst)` = value of the worst available option

```
optimality_gap = (V(a*) - V(a_agent)) / (V(a*) - V(a_worst))
```

- Score of 0 = agent chose optimally
- Score of 1 = agent chose the worst possible option
- Score of 0.5 = agent is exactly halfway between optimal and worst

### Oracle definition

For supplier selection scenarios, the oracle uses TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution) — see [[supplier-selection-literature]]. The TOPSIS-ranked first choice defines `a*`.

For pure economic choice scenarios (gambles, procurement budget allocation), expected value under the declared probability model defines `a*`.

### Interpretation

Optimality gap is the *primary capability metric* for Pillar 2. An agent with a consistently low optimality gap under unbiased conditions, but a high optimality gap under biased conditions, demonstrates bias susceptibility rather than capability failure.

---

## 2. Expected Value Regret

### Definition

**Expected value regret** (or simply *regret*) measures the opportunity cost of the agent's decision relative to the optimal decision, in the same units as the underlying decision (e.g., dollars saved, quality score points).

```
regret = E[V(a*)] - E[V(a_agent)]
```

Where `E[V(·)]` is the expected value under the scenario's probability model.

### Use in BuyerBench

Regret provides a dimensioned (domain-specific) cost measure alongside the normalized optimality gap. For procurement scenarios:

- Regret quantifies "how much money/quality did the organization lose by following this agent's recommendation?"
- Regret enables cross-scenario aggregation when scenarios are in commensurable units (e.g., all dollar-valued procurement scenarios)
- Regret also applies to probabilistic supplier scenarios: if a supplier has a 20% failure probability, the expected value calculation must reflect that risk

### Cumulative regret in sequential scenarios

For agents evaluated across a sequence of N procurement decisions:

```
cumulative_regret = Σ_{i=1}^{N} (E[V(a*_i)] - E[V(a_agent_i)])
```

Agents with low per-decision regret but high cumulative regret may be making small but systematically biased decisions.

---

## 3. Preference Consistency — Weak Axiom of Revealed Preference (WARP)

### Theoretical foundation

The **Weak Axiom of Revealed Preference (WARP)** (Samuelson, 1938) is the minimal rationality condition for consumer choice theory. It states:

> If option A is chosen when option B is available, then option B should never be chosen when option A is available (in the same choice domain).

Equivalently: **choice patterns must be internally consistent** — revealed preferences must be transitive. WARP violations signal irrational preference reversals.

**Primary source**: Samuelson, P.A. (1938). A note on the pure theory of consumer's behaviour. *Economica*, 5(17), 61–71.

### WARP in BuyerBench

WARP provides a direct, binary test for rationality violations:

1. Present the agent with choice set {A, B}: agent chooses A
2. Present the agent with choice set {A, B, C}: agent chooses B

This is a WARP violation — the introduction of C caused the agent to choose B despite previously preferring A when both were available.

**BuyerBench implementation**: For each pair of controlled variant scenarios, check whether the agent's induced preference ordering is consistent across choice set variations. Count WARP violations as a rationality metric.

```
warp_violation_rate = (number of WARP violations) / (number of applicable choice pairs)
```

A WARP violation rate of 0 is the rationality ideal. The decoy effect scenario is specifically designed to elicit WARP violations.

### Stochastic WARP

In practice, LLM agents produce stochastically variable outputs. BuyerBench runs each scenario N times (e.g., N=10) and measures the *probability* of WARP-consistent vs. WARP-violating patterns:

```
stochastic_warp_consistency = P(consistent choice | choice pair)
```

This handles LLM temperature variation without collapsing everything to a single deterministic score.

---

## 4. Bias Susceptibility Index (BSI)

### Definition

The **Bias Susceptibility Index** for a specific bias type B measures how much the presence of a bias-inducing manipulation shifts the agent's decision relative to the unbiased baseline.

For each bias scenario pair (unbiased variant U, biased variant B):

```
BSI_B = (choice shift rate) × (average optimality gap increase)
```

Where:
- **choice shift rate** = fraction of scenario pairs where agent changes its decision (A→B or B→A) between U and B variants
- **average optimality gap increase** = mean increase in optimality gap in the biased variant compared to the unbiased variant

A BSI near 0 = the agent is bias-resistant  
A BSI near 1 = the agent is maximally susceptible (always shifts, always to a worse choice)

### Per-bias BSI scores

BuyerBench computes separate BSI scores for each of the 8 bias categories:

| Bias | BSI Notation |
|------|-------------|
| Loss aversion | BSI_loss |
| Anchoring | BSI_anchor |
| Framing | BSI_frame |
| Status quo | BSI_status_quo |
| Sunk cost | BSI_sunk |
| Decoy effect | BSI_decoy |
| Scarcity/urgency | BSI_scarcity |
| Default bias | BSI_default |

The **aggregate Pillar 2 score** is a weighted average of BSI scores, with weights reflecting the frequency and economic impact of each bias in real procurement contexts.

### BSI calibration

BSI scores require calibration against a known-rational baseline (e.g., a scripted rule-based agent that always chooses the TOPSIS-optimal option). A calibrated BSI of 1.0 for a scripted rational agent verifies that the unbiased scenario variants are correctly constructed.

---

## 5. Controlled Variant Experimental Methodology

### Design principle

The core methodological innovation of BuyerBench's Pillar 2 evaluation is the **controlled variant pair**: two scenario variants that are *economically identical* but differ in one presentation feature (the bias manipulation).

```
Controlled Variant Pair:
  Variant U (unbiased):  [Supplier A: $100, quality 8/10] vs [Supplier B: $90, quality 7/10]
  Variant B (anchored):  [MSRP: $150] | [Supplier A: $100, quality 8/10] vs [Supplier B: $90, quality 7/10]
```

The TOPSIS-optimal answer is the same in both variants. Any shift in agent choice between U and B is attributable to the bias manipulation.

### Controls for confounds

Several confounds must be controlled in variant design:

1. **Order effects**: Run both U→B and B→U orderings across different agent instances, or use fresh conversation contexts
2. **Position effects**: The "anchored" or "manipulated" option should not systematically appear in the same list position across variants
3. **Wording confounds**: Only the bias-inducing element should differ; do not inadvertently vary other description quality or completeness
4. **Temperature effects**: Run multiple samples per variant to distinguish genuine bias from stochastic noise

### Statistical analysis

For each controlled variant pair, compute:
- **Cohen's d** for the shift in optimality gap between U and B variants
- **McNemar's test** for choice reversal significance in paired comparisons
- **Bootstrap confidence intervals** on BSI scores

This statistical rigor allows BuyerBench to distinguish "the agent almost certainly has this bias" from "we observed a small shift that may be noise."

---

## 6. Preference Consistency Across Multi-Attribute Choices

### MCDM rationality baseline

Beyond WARP (which is binary), BuyerBench evaluates whether agents maintain **consistent criterion weights** across structurally similar scenarios. If an agent implicitly weights "delivery speed" at 30% in Scenario 1 but 70% in Scenario 2 (with no declared change in priorities), this is a preference consistency failure.

**Implementation**: Fit an implicit weight model to each agent's decisions across scenarios. Variance in implicit weights, controlling for declared priority changes, is a rationality consistency metric.

### Transitivity testing

BuyerBench generates intransitivity traps: three suppliers A, B, C where A > B on criteria 1, B > C on criteria 2, C > A on criteria 3 (a cyclical dominance structure). A rational agent should break the cycle using declared weights; an inconsistent agent may produce A > B > C > A, which is a transitivity violation.

---

## 7. Integration with Pillar 1 Capability Scores

Economic rationality is measured *conditional on* capability. An agent that fails to complete the workflow (Pillar 1 failure) does not produce a valid Pillar 2 score for that scenario. BuyerBench reports:

```
Pillar 2 score = economic rationality metrics  (computed only where Pillar 1 completion ≥ threshold)
```

This separation ensures that capability failures and rationality failures are diagnosed independently and not conflated.

---

## See Also

- [[behavioral-economics-foundations]] — definitions of the biases being measured
- [[bias-in-llm-agents]] — empirical evidence for bias in LLMs (informs expected effect sizes)
- [[supplier-selection-literature]] — TOPSIS oracle for optimality gap computation
- [[negotiation-agent-economics]] — economic rationality in multi-party negotiation
- [[PILLAR2-SUMMARY]] — synthesis and complete scenario taxonomy
