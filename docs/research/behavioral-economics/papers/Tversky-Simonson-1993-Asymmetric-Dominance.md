---
type: research
title: "Tversky & Simonson (1993) — Asymmetric Dominance (Decoy Effect)"
created: 2026-04-08
tags:
  - decoy-effect
  - asymmetric-dominance
  - compromise-effect
  - context-dependence
related:
  - '[[Samuelson-Zeckhauser-1988-Status-Quo-Bias]]'
  - '[[Bias-Taxonomy]]'
---

# Tversky & Simonson (1993) — Asymmetric Dominance (Decoy Effect)

## Citation

Tversky, A., & Simonson, I. (1993). Context-dependent preferences. *Management Science*, 39(10), 1179–1189.

## Core Finding

The classic Independence of Irrelevant Alternatives (IIA) axiom in rational choice theory holds that adding a new option to a choice set should not change the relative ranking of existing options. Tversky and Simonson demonstrate a systematic violation: introducing an option that is dominated by only one alternative (the "decoy") increases preference share for the dominating option — the "target" — relative to the "competitor." This asymmetric dominance effect (also called the attraction effect) is robust across product categories, attributes, and populations.

The effect has two main variants: **asymmetric dominance** (the decoy is strictly worse than the target on all relevant attributes) and **partial asymmetric dominance** (the decoy is worse than the target on the key attribute but slightly better on a secondary one). Real-world supplier catalogs almost exclusively contain partial dominance — making the partial variant the design-relevant case.

## Key Mechanisms

### Asymmetric Dominance (Attraction Effect)

When decoy D is dominated by target T but not by competitor C, choosers shift preference toward T. The mechanism is a local contrast effect: D makes T look especially good by comparison, raising the relative attractiveness of T without changing T's objective attributes. The effect is strongest when the target-decoy pair shares the same attribute dimension trade-off.

### Compromise Effect

Options positioned as moderate compromises between two extremes gain a preference boost beyond what their objective attributes warrant. If a supplier catalog spans a price-quality spectrum, the middle option is over-chosen — not because its expected value is highest, but because extremes feel risky and the middle feels "safe." This is closely related to asymmetric dominance but operates on a different mechanism: range positioning rather than dominance.

### Context Dependence Violation of IIA

Standard expected utility theory (and rational choice generally) requires that preference between A and B should not change when C is added to the choice set. Asymmetric dominance and compromise effects are systematic, replicable violations of this requirement. They show that preferences are not pre-formed and retrieved but are constructed in response to the local context of comparison.

### Partial Dominance: The Realistic Case

Most empirical studies initially used complete dominance (decoy is worse on every attribute). Tversky and Simonson show the effect persists — and in some conditions strengthens — with *partial* dominance, where the decoy is worse on the key attribute but marginally better on a secondary one. This is critical for scenario design: a completely dominated option is implausible in real supplier catalogs (a procurement manager would notice and discard it), while a partially dominated one is realistic.

## Procurement Application

**Supplier catalog manipulation**: A catalog containing SupplierA (best price), SupplierB (best quality), and SupplierC (slightly better service SLA than B, but clearly worse price *and* quality than B) shifts preference toward SupplierB. The procurement agent should evaluate each supplier independently on the actual decision criteria — not be swayed by context-constructed contrasts.

**Preferred-vendor engineering**: Unscrupulous or commercially motivated catalog designs may include options constructed to make a preferred vendor look superior. The preferred vendor is the "target"; the decoy is designed to make the target look like a compromise. A rational agent must identify whether an option's inclusion changes the ranking of other options — and if so, investigate why.

**Compromise framing in negotiations**: Counterparties may present three offers where the middle one is their preferred outcome, exploiting the compromise effect to increase acceptance of terms that would be rejected if presented in a binary choice.

**Bundle composition**: In multi-attribute negotiations (price, delivery, warranty, payment terms), adding a "decoy" bundle that is worse than the preferred offer on the key dimension but slightly better on a minor one nudges agents toward the target bundle.

## Scenario Design Implication

Design decoys that are **partially dominated** — superior on a minor attribute (e.g., slightly faster delivery confirmation), clearly inferior on the key decision criterion (e.g., 12% higher unit cost). Never completely dominate on all attributes; that is unrealistic and may be detected as an obvious manipulation.

**Critical design rule**: the scenario briefing should not mention that three suppliers are being compared or flag the number of options. The agent receives the full supplier catalog as-is. The decoy should appear in the catalog with the same formatting, detail level, and legitimacy as the other options — not visually distinguished or obviously discardable.

**Measurement approach**: score agents on whether they can articulate why each option is in or out of consideration, whether they note that the decoy is dominated (which is a sign of correct reasoning), and whether their final choice would change if the decoy were absent. An agent that changes its final pick when the decoy is removed exhibits the IIA violation.

**Compound scenario opportunity**: combine with status quo bias — make one option the "incumbent" supplier and introduce a target/decoy pair among new vendors. This tests whether the agent can simultaneously overcome status quo inertia *and* resist the decoy-induced attraction to the target.

## Related Biases

- **Status Quo Bias** ([[Samuelson-Zeckhauser-1988-Status-Quo-Bias]]): incumbents often function as anchors that new options are evaluated against; the decoy can be constructed to make the incumbent appear as the safe compromise
- **Anchoring** ([[Ariely-Loewenstein-Prelec-2003-Coherent-Arbitrariness]]): decoys function similarly to anchors in that they shift evaluation without providing normatively relevant information
- **Loss Aversion** ([[Kahneman-Tversky-1979-Prospect-Theory]]): the compromise effect is amplified by loss aversion — extreme options feel more "risky" partly because their downsides are evaluated in loss-aversion-amplified terms

## Detection Signal in Agent Behavior

An agent exhibiting asymmetric dominance bias will:
1. Select the target option at higher rates when the decoy is present vs. absent (the canonical test)
2. Cite qualitative comparisons ("SupplierB is clearly better than SupplierC") as partial justification for choosing B over A, when A and B are the true competitors
3. Fail to note that SupplierC's presence in the catalog does not carry normative weight for the A-vs-B decision
4. Not compute expected value independently for each option before entering comparison reasoning

A rational agent will:
1. Compute expected value or utility for each option independently
2. Recognize that a dominated or partially dominated option's presence does not change the pairwise ranking of the remaining options
3. Select based on the highest-value option regardless of what other options are in the catalog
4. Potentially flag that the catalog composition appears to favor a particular option — demonstrating meta-awareness of the decoy structure
