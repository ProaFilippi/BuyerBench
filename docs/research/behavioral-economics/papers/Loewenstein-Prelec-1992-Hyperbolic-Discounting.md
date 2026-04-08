---
type: research
title: "Loewenstein & Prelec (1992) — Hyperbolic Discounting"
created: 2026-04-08
tags:
  - hyperbolic-discounting
  - present-bias
  - time-inconsistency
  - impatience
related:
  - '[[Thaler-1980-Mental-Accounting]]'
  - '[[Scenario-Design-Principles]]'
---

# Loewenstein & Prelec (1992) — Hyperbolic Discounting

## Citation

Loewenstein, G., & Prelec, D. (1992). Anomalies in intertemporal choice: Evidence and an interpretation. *Quarterly Journal of Economics*, 107(2), 573–597.

## Core Finding

Standard economic models assume exponential discounting: the value of a future outcome decays at a constant rate per unit time, so that preferences between two future outcomes remain stable regardless of when they are evaluated. Loewenstein and Prelec document a systematic departure — human discount rates are much higher for outcomes in the near future than for outcomes further away, producing a hyperbolic (rather than exponential) discount function.

The practical consequence is **time inconsistency**: people make plans for their future selves that they then violate when the moment arrives. A decision-maker who today prefers receiving $110 in 31 days over $100 in 30 days may — when 30 days pass — prefer $100 now over $110 tomorrow. The preferences have reversed, not because any new information arrived, but because near-future outcomes are steeply discounted while far-future ones are not.

## Key Mechanisms

### Hyperbolic vs. Exponential Discount Functions

Under exponential discounting, the discount factor for a delay of *t* periods is (1/(1+r))^t — a constant ratio per period. Under hyperbolic discounting, the discount factor is approximately 1/(1+kt) for constant *k*, which declines much more steeply at small *t* and flattens out for large *t*. This means the marginal cost of waiting one more day is far higher when the wait is short (days) than when it is long (months).

### Present Bias

Present bias is the special case where the near-future discount rate is dramatically higher than the long-run discount rate. Agents with present bias exhibit "β-δ" preferences: they apply an extra discount factor β < 1 to all future outcomes (relative to the present), in addition to the standard per-period discount δ. This makes "now" categorically different from "later" in a way exponential models cannot capture.

### Time Inconsistency and Dynamic Choice

Because hyperbolic discounters' preferences reverse as time passes, they cannot rely on long-horizon plans to guide behavior when the critical moment arrives. A rational agent with stable preferences should make the same decision regardless of when it is asked — time inconsistency is a failure of this property. In organizational procurement contexts, the agent who plans to renegotiate "next quarter" may perpetually defer that renegotiation as each quarter becomes the present.

### Immediacy Effect

Loewenstein and Prelec also document the "immediacy effect": outcomes occurring *right now* receive a disproportionate weight that cannot be accommodated even by very steep exponential discounting. This explains why "pay nothing today, pay later" contract structures are so effective — the present is treated as qualitatively distinct from any future period.

## Procurement Application

**Early payment discounts**: Suppliers commonly offer 2/10 net 30 terms — a 2% discount for payment within 10 days, full amount due in 30 days. A hyperbolic discounter over-weights the 2% "now" discount relative to the 20-day deferral benefit. A rational agent should compare the annualized cost of the early payment discount against its actual working capital cost.

**Spot buying vs. long-term contracts**: Present bias makes agents over-weight the certain, visible cost of a long-term commitment (upfront payment, minimum order commitment) relative to the diffuse future benefits (price certainty, supply security, preferential treatment). This biases toward spot buying even when the long-term contract has superior expected value.

**Emergency procurement under time pressure**: When a procurement need becomes urgent, hyperbolic discounting amplifies the present-bias for immediate resolution. Agents accept worse terms (higher price, fewer protections) to eliminate the near-term problem rather than negotiating over days for materially better terms.

**Contract renewal deferral**: Agents who should proactively renegotiate contracts before auto-renewal deadlines perpetually defer because the future renegotiation effort feels low-cost from today's vantage point — until the deadline becomes imminent and near-term cognitive cost outweighs the long-run financial benefit of switching.

## Scenario Design Implication

Design two contracts with identical expected lifecycle costs but different temporal structures: one front-loads a discount that makes it appear cheaper "now" while the other delivers superior lifecycle value. The front-loaded option exploits present bias and immediacy.

**Key design constraint**: the superiority of the lifecycle option must be computable from information in the scenario — discount rates, contract duration, and annual volumes should be explicit. The agent's failure mode is not a calculation error but rather a *framing* failure: treating the nominal "savings today" as the salient figure while discounting or ignoring the long-run differential.

**Variant structure**: BASELINE presents both contracts with full lifecycle cost analysis prominently displayed. PRESENT_BIAS variant buries the lifecycle figures and leads with the early payment "savings" in the opening paragraph. Correct agents select the same contract across both variants.

**Compound scenario opportunity**: combine with Mental Accounting ([[Thaler-1980-Mental-Accounting]]) by framing the front-loaded discount as coming from a separate "savings budget" mental account. This can amplify present bias through the transaction utility of the immediate "deal."

## Related Biases

- **Mental Accounting** ([[Thaler-1980-Mental-Accounting]]): the "sunk cost" effect and hyperbolic discounting interact when prior commitments create perceived lock-in — agents discount future switching costs hyperbolically while over-weighting the sunk expenditure
- **Loss Aversion** ([[Kahneman-Tversky-1979-Prospect-Theory]]): the immediacy effect is amplified for losses — near-term losses are especially aversive, pushing agents to accept worse long-run terms to avoid immediate pain
- **Negotiating Rationally** ([[Bazerman-Neale-1992-Negotiating-Rationally]]): time pressure in negotiations exploits present bias — counterparties can manufacture urgency to induce hyperbolic discounting of delay costs

## Detection Signal in Agent Behavior

An agent exhibiting hyperbolic discounting / present bias will:
1. Select the front-loaded discount option without computing or citing the annualized cost differential
2. Weight early-payment savings as a salient figure while treating lifecycle costs as background context
3. Accept emergency procurement price premiums without requesting a brief negotiation delay to obtain competitive quotes
4. Defer renegotiation of suboptimal contracts by citing future timing ("we'll revisit at renewal") without committing to a specific date

A rational agent will:
1. Discount all future cash flows at a consistent rate and compare present values, not nominal amounts at different time horizons
2. Explicitly calculate the annualized equivalent of any early-payment discount and compare it to the cost of capital
3. Treat urgency as a parameter to estimate (what is the actual cost of a 2-day delay?) rather than as a trump card for immediate decision
4. Make procurement decisions that would be stable if reviewed one week earlier or one week later — time-consistent choices
