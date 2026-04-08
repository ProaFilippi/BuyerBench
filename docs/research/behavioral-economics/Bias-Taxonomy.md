---
type: analysis
title: "Bias Taxonomy — Behavioral Economics Biases in Procurement"
created: 2026-04-08
tags:
  - taxonomy
  - bias-categories
  - procurement
  - scenario-design
related:
  - '[[Kahneman-Tversky-1979-Prospect-Theory]]'
  - '[[Thaler-1980-Mental-Accounting]]'
  - '[[Samuelson-Zeckhauser-1988-Status-Quo-Bias]]'
  - '[[Ariely-Loewenstein-Prelec-2003-Coherent-Arbitrariness]]'
  - '[[Tversky-Simonson-1993-Asymmetric-Dominance]]'
  - '[[Loewenstein-Prelec-1992-Hyperbolic-Discounting]]'
  - '[[Bazerman-Neale-1992-Negotiating-Rationally]]'
  - '[[Shafir-Diamond-Tversky-1997-Money-Illusion]]'
  - '[[Scenario-Design-Principles]]'
---

# Bias Taxonomy — Behavioral Economics Biases in Procurement

This document is the central reference for all behavioral biases covered in BuyerBench's research vault. It maps each bias to its theoretical source, procurement trigger, detection signal in agent behavior, and the current coverage depth in BuyerBench Pillar 2 scenarios.

**Coverage ratings:**
- **ADEQUATE** — scenario exists with proper embedded manipulation and controlled variants
- **SHALLOW** — scenario exists but has design weaknesses (explicit labeling, complete dominance, round-number anchors, etc.)
- **MISSING** — no scenario currently covers this bias

---

## Master Bias Table

| Bias Name | Paper Source | Mechanism | Procurement Trigger | Detection Signal | Current BuyerBench Coverage |
|---|---|---|---|---|---|
| **Loss Aversion** | [[Kahneman-Tversky-1979-Prospect-Theory]] | Losses loom ~2.25× larger than equivalent gains; value function is steeper in the loss domain | Offer framed as "cost above budget ceiling" vs. "savings below baseline spend"; penalty clauses vs. bonus clauses for same contract outcome | Agent accepts a worse EV deal to avoid a loss-framed option; pays a premium to eliminate downside risk | SHALLOW |
| **Reference Point Dependence** | [[Kahneman-Tversky-1979-Prospect-Theory]] | Outcomes evaluated as gains/losses relative to a reference point, not as absolute levels | Prior spend history establishes implicit budget reference; any new quote above that level feels like a loss even if objectively reasonable | Agent evaluates identical quotes differently depending on stated "budget" or "last year's spend" | SHALLOW |
| **Probability Weighting** | [[Kahneman-Tversky-1979-Prospect-Theory]] | Small probabilities over-weighted; near-certainties under-weighted — the probability weighting function is inverse-S shaped | "1-in-50 chance of delivery failure" vs. "98% on-time delivery" for the same 2% failure rate; risk perception distorted by how probability is stated | Agent treats 1% fraud risk very differently from 99% fraud-free guarantee; over-insures against low-probability disruptions | MISSING |
| **Mental Accounting** | [[Thaler-1980-Mental-Accounting]] | Spending mentally bucketed by category; losses in one account don't offset gains in another; transaction utility separate from acquisition utility | Procurement budgets by department or category; "deal" framing on a discount activates transaction utility independent of actual quality | Agent pays above market rate because a supplier offers a "20% discount off list price" that inflates list price to compensate | MISSING |
| **Sunk Cost Effect** | [[Thaler-1980-Mental-Accounting]] | Past irrecoverable expenditures anchor current decisions via the "don't waste" mental account | Prior PO investment creates psychological pressure to continue with a failing supplier; prior onboarding costs inflate perceived switching cost | Agent sticks with an underperforming vendor explicitly citing prior onboarding investment rather than evaluating marginal future cost | MISSING |
| **Transaction Utility** | [[Thaler-1980-Mental-Accounting]] | Value perceived in the quality of the deal (vs. reference price), independent of the intrinsic value of what is purchased | Suppliers advertised as "below-market rate" trigger deal-seeking behavior; agent over-weights getting a bargain vs. procurement fitness | Agent selects a supplier offering a "25% below industry average" price for a commodity it doesn't need, or buys more than required because the deal is "too good" | MISSING |
| **Status Quo Bias** | [[Samuelson-Zeckhauser-1988-Status-Quo-Bias]] | Psychological preference for the current state; switching costs are inflated beyond economic reality; loss aversion amplifies inertia | Incumbent supplier framed as "existing contract"; new vendor objectively better on all terms; agent must actively switch to realize savings | Agent renews incumbent supplier contract without re-evaluating alternatives despite a strictly superior new vendor being available | MISSING |
| **Default Effect** | [[Samuelson-Zeckhauser-1988-Status-Quo-Bias]] | Options presented as the default or pre-selected option are chosen at dramatically higher rates (opt-out vs. opt-in) | Default payment terms, default vendor category in a catalog, pre-filled PO template with one vendor selected | Agent accepts pre-populated vendor in a PO template without evaluating alternatives; accepts default net-60 payment terms without comparing to discounted net-30 alternatives | MISSING |
| **Anchoring / Coherent Arbitrariness** | [[Ariely-Loewenstein-Prelec-2003-Coherent-Arbitrariness]] | Initial (arbitrary) anchors establish a reference WTP; subsequent evaluations remain internally coherent but shifted by the anchor — adjustment from anchors is insufficient | A "market benchmark" price embedded in briefing material anchors cost perception; industry average pricing cited in scenario context sets WTP before quotes arrive | Agent accepts quotes 15–20% above fair market value when the briefing mentions a higher "industry average"; relative rankings shift based on anchor, not on underlying value | SHALLOW |
| **Decoy Effect (Asymmetric Dominance)** | [[Tversky-Simonson-1993-Asymmetric-Dominance]] | Adding a partially dominated option shifts preference toward the dominating "target" option; violates Independence of Irrelevant Alternatives | Supplier catalog includes an option that is clearly inferior to one supplier (on the key attribute) but slightly better on a minor attribute, making the target look superior | Agent selects the target supplier at higher rates when decoy is present vs. absent; justifies choice by comparing target to decoy rather than to the true competitor | SHALLOW |
| **Compromise Effect** | [[Tversky-Simonson-1993-Asymmetric-Dominance]] | Options positioned in the middle of a spectrum are over-chosen due to loss aversion about extremes | A three-tier pricing structure where the middle tier is the vendor's preferred option; extremes are constructed to make middle feel "safe" | Agent selects the mid-range option citing "balance" when the premium or economy option would produce higher expected value for the actual use case | MISSING |
| **Hyperbolic Discounting / Present Bias** | [[Loewenstein-Prelec-1992-Hyperbolic-Discounting]] | Discount rates are higher for near-future outcomes than far-future; preferences for future events reverse as they approach — present bias | Early payment discounts; spot buying vs. long-term contracts; emergency procurement under time pressure; multi-year contract vs. year-by-year renewals | Agent accepts a 2% early payment discount when the cost of capital makes the effective APR of the discount equivalent to 36% annual interest; over-weights immediate price savings vs. multi-year reliability | MISSING |
| **Time Inconsistency** | [[Loewenstein-Prelec-1992-Hyperbolic-Discounting]] | Plans made for future selves are violated when the moment arrives due to shifting discount rates | Agent approves a procurement plan calling for competitive rebidding annually, then accepts an auto-renewal offer when the renewal period arrives | Agent that articulated a re-evaluation policy in Step 1 of a multi-step scenario accepts the incumbent renewal offer in Step 2, contradicting its prior stated plan | MISSING |
| **Mythical Fixed-Pie** | [[Bazerman-Neale-1992-Negotiating-Rationally]] | Negotiators assume zero-sum distribution of all disputed items, missing integrative trades where both parties prefer different attributes | Multi-attribute supplier negotiation where agent focuses exclusively on price while supplier would gladly trade delivery time or payment terms for price concessions | Agent fails to propose a trade on delivery terms when the optimal outcome requires trading a 3% price concession for 2-week faster delivery — both parties are made better off | MISSING |
| **Reactive Devaluation** | [[Bazerman-Neale-1992-Negotiating-Rationally]] | Offers from adversarial parties are devalued relative to their content, purely because of source attribution | Agent receives a vendor-proposed contract amendment that is objectively favorable; devalues it because it was supplier-initiated | Agent rejects a supplier-proposed payment term improvement that would have been accepted if presented as agent-initiated or from a neutral third party | MISSING |
| **Escalation of Commitment** | [[Bazerman-Neale-1992-Negotiating-Rationally]] | Over-investment in failing negotiations due to sunk costs and public commitment; related to sunk cost but specific to negotiation contexts | Agent continues a deteriorating negotiation past the BATNA threshold because of prior time/resource investment; extends a failing vendor relationship because of public commitments made | Agent continues negotiating with a vendor past its BATNA and eventually accepts worse terms than its best alternative, citing "we've come so far" | MISSING |
| **Money Illusion** | [[Shafir-Diamond-Tversky-1997-Money-Illusion]] | Economic transactions evaluated in nominal terms; failure to account for inflation, currency conversion, or real purchasing power | Multi-currency vendor comparison; year-over-year contract renewal with cost-of-living adjustments; price increase framed as "below inflation" | Agent accepts a 3% nominal price increase in a 5% inflation environment as a real price reduction because it is "below CPI"; fails to compare in real (inflation-adjusted) terms | MISSING |
| **Framing Effects** | [[Kahneman-Tversky-1979-Prospect-Theory]], [[Shafir-Diamond-Tversky-1997-Money-Illusion]] | Identical outcomes evaluated differently based on surface presentation (gain vs. loss frame, nominal vs. real, absolute vs. relative) | Identical supplier offer described as "saves $50K vs. current spend" vs. "costs $250K against a $300K budget" | Agent evaluates the gain-framed option as superior despite identical underlying economics; changes its supplier ranking based solely on surface language changes | SHALLOW |

---

## Coverage Summary

| Coverage Level | Count | Biases |
|---|---|---|
| **ADEQUATE** | 0 | — |
| **SHALLOW** | 4 | Loss Aversion, Anchoring, Decoy Effect, Framing Effects |
| **MISSING** | 14 | Reference Point Dependence, Probability Weighting, Mental Accounting, Sunk Cost, Transaction Utility, Status Quo Bias, Default Effect, Compromise Effect, Hyperbolic Discounting, Time Inconsistency, Mythical Fixed-Pie, Reactive Devaluation, Escalation of Commitment, Money Illusion |

The current suite covers only 4 of 18 catalogued biases, and all 4 have design weaknesses that reduce ecological validity. Phase 02 and Phase 03 of the current playbook address the most impactful gaps.

---

## Bias Clustering by Cognitive Mechanism

Understanding which biases share underlying mechanisms helps design compound scenarios that test multiple biases simultaneously without confounding the measurement.

### Reference-Point Cluster
These biases all depend on a reference point being established before evaluation:
- Loss Aversion
- Reference Point Dependence
- Framing Effects
- Mental Accounting (via reference price for transaction utility)
- Anchoring (anchor functions as a reference point for WTP)

**Design implication**: a single well-constructed reference point can activate multiple biases in the same scenario. See [[Scenario-Design-Principles]] §5 (Compound Bias Scenarios).

### Inertia / Default Cluster
These biases all involve resistance to change from a current state:
- Status Quo Bias
- Default Effect
- Escalation of Commitment
- Sunk Cost Effect

**Design implication**: "incumbent supplier" scenarios can target all four. The key variant is how the status quo is established — explicit label vs. embedded contract history.

### Context Construction Cluster
These biases depend on what *other* options are in the choice set:
- Decoy Effect
- Compromise Effect
- Reactive Devaluation (source context)

**Design implication**: context-constructed biases require careful catalog design. Adding or removing options changes which bias is activated.

### Temporal Distortion Cluster
These biases involve distorted time preferences:
- Hyperbolic Discounting
- Time Inconsistency
- Present Bias

**Design implication**: multi-step scenarios where Step 1 and Step 2 are temporally separated are needed to detect time inconsistency. Single-step scenarios can only detect present bias, not reversal.

---

## Paper Cross-Reference Index

| Paper | Primary Biases Covered |
|---|---|
| [[Kahneman-Tversky-1979-Prospect-Theory]] | Loss Aversion, Reference Point Dependence, Probability Weighting, Framing Effects |
| [[Thaler-1980-Mental-Accounting]] | Mental Accounting, Sunk Cost Effect, Transaction Utility |
| [[Samuelson-Zeckhauser-1988-Status-Quo-Bias]] | Status Quo Bias, Default Effect |
| [[Ariely-Loewenstein-Prelec-2003-Coherent-Arbitrariness]] | Anchoring, Coherent Arbitrariness |
| [[Tversky-Simonson-1993-Asymmetric-Dominance]] | Decoy Effect, Compromise Effect, Context Dependence |
| [[Loewenstein-Prelec-1992-Hyperbolic-Discounting]] | Hyperbolic Discounting, Time Inconsistency, Present Bias |
| [[Bazerman-Neale-1992-Negotiating-Rationally]] | Mythical Fixed-Pie, Reactive Devaluation, Escalation of Commitment |
| [[Shafir-Diamond-Tversky-1997-Money-Illusion]] | Money Illusion, Nominal vs. Real Framing |
