---
type: research
title: "Shafir, Diamond & Tversky (1997) — Money Illusion"
created: 2026-04-08
tags:
  - money-illusion
  - nominal-vs-real
  - inflation-confusion
  - currency
related:
  - '[[Kahneman-Tversky-1979-Prospect-Theory]]'
  - '[[Bias-Taxonomy]]'
---

# Shafir, Diamond & Tversky (1997) — Money Illusion

## Citation

Shafir, E., Diamond, P., & Tversky, A. (1997). Money illusion. *Quarterly Journal of Economics*, 112(2), 341–374.

## Core Finding

People evaluate economic transactions, contracts, and outcomes primarily in **nominal** (face-value) terms rather than **real** (inflation-adjusted) terms, even when they possess the information needed to compute the real value. This "money illusion" — long assumed by neoclassical economics to be a simple cognitive error that education eliminates — is shown by Shafir, Diamond, and Tversky to be a systematic, robust phenomenon driven by the vividness and accessibility of nominal figures relative to abstract adjusted values.

The most striking demonstration: subjects rate someone receiving a 2% nominal wage increase during 4% inflation as "doing better" than someone receiving a 0% nominal raise in a 0% inflation environment — even when directly informed of the inflation rates. The first person has suffered a 2% real pay cut; the second has maintained real purchasing power. Nominal salience dominates real-value reasoning even for financially literate respondents.

Shafir et al. propose a dual-representation account: people maintain both nominal and real representations of value but weight the nominal representation more heavily because it is perceptually immediate and requires no computation.

## Key Mechanisms

### Nominal Salience

Nominal prices are concrete, immediately observable, and require no computation. Real prices require knowing a reference period, an inflation index, and performing a deflation calculation. Under cognitive load, time pressure, or unfamiliar economic contexts (foreign currencies, long contract horizons), people default to nominal comparisons.

This is not pure ignorance — subjects often *know* about inflation or exchange rates but fail to integrate that knowledge into their judgment. The bias is strongest when the nominal difference is large and visible (a $10,000 raise feels significant) and the real adjustment is expressed in abstract percentage terms.

### Nominal Framing in Contracts

Contract evaluation is particularly vulnerable because contracts state nominal values by definition — the legal instrument specifies dollar amounts, not real purchasing power commitments. Workers, suppliers, and buyers who re-evaluate contracts at renewal treat the nominal value of the prior contract as the reference point, without adjusting for intervening inflation.

This means a contract renewed at +3% in a +4% inflation environment is perceived as a *gain* (3% more money) when it is economically a *loss* (−1% real). The reference point distortion compounds: the nominal figure from the prior period anchors the new negotiation without inflation adjustment.

### Multi-Currency Confusion

When transactions occur across currencies, money illusion extends to exchange rate confusion. Agents compare nominal values in different currencies without correctly applying conversion rates, particularly when rates have shifted since the last comparison. A supplier quoting in EUR when the buyer operates in USD creates a nominal vs. real divide: the EUR quote may appear identical to a prior quote while representing a meaningful change in USD real cost due to rate movement.

### The "Below Inflation" Framing Exploit

An offer framed as a "below-inflation price increase" exploits money illusion bidirectionally: the buyer perceives nominal increase (bad) while the seller claims real decrease (good). Both parties may be operating in the same nominal reality but arguing from different real-value reference frames. Rational evaluation requires converting all comparisons to the same real-value basis before assessing acceptability.

## Procurement Application

**Year-over-year contract renewal**: a vendor proposes a 3% unit price increase at renewal. In a 5% inflation environment, this is a real price decrease of ~2%. An agent applying money illusion evaluates the 3% nominal increase as a price rise and negotiates to reduce it — potentially paying more in real terms to avoid nominal change.

**Multi-currency vendor comparison**: a scenario requiring comparison of three suppliers quoting in USD, EUR, and GBP requires currency conversion before price comparison. Agents applying nominal comparison (without conversion) will incorrectly rank suppliers whenever current exchange rates differ from the implicit rates used when nominal figures were established.

**Cost-of-living adjustment (COLA) clauses**: standard COLA clauses in long-term supply contracts adjust nominal prices for inflation automatically. A procurement agent evaluating whether to include a COLA clause must reason in real terms — evaluating the expected real cost trajectory under vs. without the clause. Money illusion drives agents to prefer nominal price certainty (fixed-price contract) even when a COLA-adjusted contract has lower expected real cost variance.

**Inflation-adjusted vs. nominal savings reporting**: internal procurement reporting often uses nominal savings (this year's price vs. last year's price). An agent optimizing for nominal savings metrics may negotiate outcomes that appear favorable in nominal terms but represent real price increases relative to purchasing power, particularly across multi-year horizons.

## Scenario Design Implication

Present a contract renewal scenario with an **explicit inflation context** embedded naturalistically — e.g., a CFO memo that mentions inflation projections in a different section of the briefing, or a vendor proposal letter that references "current market conditions." The nominal price change and the real price change should diverge meaningfully.

**Critical design rule**: do not frame the scenario as a test of inflation understanding. The inflation rate should appear as a contextual data point in the scenario materials — a number the agent *has* but may not integrate into its evaluation. The task should be stated in nominal terms ("evaluate this renewal proposal") without prompting real-value calculation.

**Measurement approach**: score agents on:
1. Whether they identify and apply the inflation data to compute real price change
2. Whether their recommendation would differ if the nominal price change were identical but inflation were zero
3. Whether they flag the nominal-vs-real distinction in their reasoning trace
4. In multi-currency scenarios: whether they apply current exchange rates before comparing nominal prices

**Compound scenario opportunity**: combine with anchoring ([[Ariely-Loewenstein-Prelec-2003-Coherent-Arbitrariness]]) — set the prior year's nominal contract value as the anchor. An agent anchoring on the nominal prior value and adjusting for inflation will under-adjust (the classic anchoring failure) while an agent ignoring inflation entirely will anchor on a nominal figure that is not comparable to real current values.

## Related Biases

- **Loss Aversion / Prospect Theory** ([[Kahneman-Tversky-1979-Prospect-Theory]]): nominal changes are evaluated against nominal reference points; a real decrease that appears as a nominal increase is coded as a gain even when purchasing power is lost — loss aversion then makes the agent reluctant to accept nominal increases even when they represent real savings
- **Anchoring** ([[Ariely-Loewenstein-Prelec-2003-Coherent-Arbitrariness]]): prior nominal contract values anchor re-negotiation independent of inflation; the anchor is in nominal terms, so real-value changes are invisible until adjustment is explicitly performed
- **Status Quo Bias** ([[Samuelson-Zeckhauser-1988-Status-Quo-Bias]]): nominal price stability is a form of status quo framing — a contract that "hasn't changed in price" feels like the default even when real costs have risen substantially over time

## Detection Signal in Agent Behavior

An agent exhibiting money illusion will:
1. Evaluate a contract renewal based on the nominal price change (e.g., "+3%") without computing real change against provided inflation data
2. In a multi-currency scenario, compare nominal prices across currencies without applying current exchange rates
3. Recommend against a COLA-adjusted contract because "prices go up" without computing the expected real cost under both contract types
4. Treat nominal savings (year-over-year price reduction in nominal dollars) as equivalent to real savings without inflation adjustment

A rational agent will:
1. Identify all inflation, CPI, or exchange rate data present in scenario materials and apply them before making comparisons
2. Convert all prices to a common real-value basis (same period, same currency) before ranking options
3. Explicitly distinguish nominal and real values in its reasoning trace when they diverge
4. Recognize that "below-inflation" price increases represent real decreases and evaluate them as favorable, not adverse, developments
