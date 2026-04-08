---
type: research
title: "Bazerman & Neale (1992) — Negotiating Rationally"
created: 2026-04-08
tags:
  - negotiation
  - mythical-fixed-pie
  - reactive-devaluation
  - overconfidence
  - procurement
related:
  - '[[Thaler-1980-Mental-Accounting]]'
  - '[[Loewenstein-Prelec-1992-Hyperbolic-Discounting]]'
---

# Bazerman & Neale (1992) — Negotiating Rationally

## Citation

Bazerman, M. H., & Neale, M. A. (1992). *Negotiating Rationally*. Free Press.

Primary empirical grounding draws on: Neale, M. A., & Bazerman, M. H. (1991). *Cognition and Rationality in Negotiation*. Free Press; and Bazerman, M. H., & Carroll, J. S. (1987). Negotiator cognition. *Research in Organizational Behavior*, 9, 247–288.

## Core Finding

Negotiators systematically deviate from rational strategy through a cluster of cognitive errors that are individually well-documented but especially destructive in combination. The three central errors are: (1) the **mythical fixed-pie assumption** — treating all negotiated items as zero-sum when parties often have different priorities across issue dimensions; (2) **reactive devaluation** — discounting offers because of who made them, not what they contain; and (3) **overconfidence and escalation of commitment** — over-investing in negotiations once started, driven by sunk costs and reputational concerns. Together these cause negotiators to leave value on the table, reject good deals, and persist in bad ones.

A key prescription: rational negotiation requires mapping the full issue space, identifying which items *you* care most about vs. which items *they* care most about, and trading concessions on low-priority items for gains on high-priority ones — the structure of a Pareto-improving deal.

## Key Mechanisms

### Mythical Fixed-Pie Assumption

Negotiators default to a zero-sum mental model: for every unit I gain, you lose one. This is false in the majority of realistic multi-attribute negotiations where parties have asymmetric preferences across dimensions. A buyer who cares primarily about price and a supplier who cares primarily about payment schedule can construct a deal where the buyer gets a price discount in exchange for net-60 terms — both parties are better off, but only if they escape the fixed-pie frame.

The error is persistent even in experienced negotiators. It manifests as over-focus on the single most salient issue (typically price) while neglecting other negotiable dimensions (delivery lead time, warranty scope, volume commitments, payment terms, service SLAs).

### Reactive Devaluation

Offers are evaluated not only on their content but on their source. Identical offers are rated less favorably when they are attributed to an adversarial counterpart than to a neutral third party. The mechanism is a motivated reasoning effect: if *they* are offering it, it must be good for them and therefore bad for me.

In procurement, this appears as blanket rejection of vendor-proposed terms — even when those terms are objectively advantageous — because agents treat vendor proposals as inherently suspect. The rational response is to evaluate proposals on their merits and independently verify any claims, not to downweight all counterpart proposals as a category.

### Overconfidence

Negotiators systematically overestimate their BATNA (Best Alternative to Negotiated Agreement) and their probability of winning disputes. This overconfidence reduces willingness to make concessions that would be mutually beneficial, extends negotiations unnecessarily, and increases the frequency of impasse (where both parties would have been better off with any deal).

In procurement, overconfidence manifests as unrealistic reserve price estimates, excessive anchoring on first offers (believing the anchor signals the full ZOPA), and refusal to accept market-rate pricing based on inflated estimates of the organization's buyer power.

### Escalation of Commitment

Once negotiation effort accumulates, parties over-invest in reaching a deal — or in prevailing — beyond what the outcome justifies. The mechanism is dual: sunk cost reasoning (I've already spent X hours on this, I can't walk away) and consistency motivation (backing down would be a loss of face). This is closely related to the sunk cost fallacy in [[Thaler-1980-Mental-Accounting]]: past negotiation investment is a sunk cost and should not influence whether the current offer is accepted.

## Procurement Application

**Multi-attribute supplier negotiations**: a procurement agent negotiating a software licensing renewal faces price, support tier, usage caps, and payment schedule as independent negotiable dimensions. The vendor may care more about payment schedule (cash flow) than about license price. An agent stuck in the fixed-pie frame negotiates only on price, leaving value-creating trades unmade.

**Payment term trade-offs**: early payment discounts (2/10 net 30 structures) are a classic dimension where buyer and seller have asymmetric preferences. A buyer with idle cash surplus can offer accelerated payment for a price reduction — a net positive trade for both parties. An agent applying fixed-pie reasoning will not propose this exchange; it will treat payment terms as boilerplate.

**Reactive devaluation in vendor proposals**: a vendor proposes an audit clause in the MSA. A reactive-devaluation-prone agent rejects it as "a trap" without reading it; a rational agent evaluates it against the organization's actual audit needs and negotiates the specific language that matters.

**Escalation in competitive bids**: once a preferred vendor is selected and negotiation begins, sunk cost reasoning may cause an agent to accept progressively worse terms to avoid the appearance of "failed" procurement — especially under deadline pressure. Combined with hyperbolic discounting ([[Loewenstein-Prelec-1992-Hyperbolic-Discounting]]), the time pressure of an expiring contract creates compounding irrationality.

## Scenario Design Implication

Design a negotiation scenario where the **optimal move is a cross-dimension trade**, not simple price minimization. The scenario briefing should present a multi-attribute choice set (price, delivery, payment terms, warranty) where the agent's organization has an explicit stated priority ranking — and where the best deal involves *conceding* on a low-priority dimension to gain on the high-priority one.

**Critical design rule**: the framing must be naturalistic — present the scenario as a live negotiation with a vendor counter-proposal, not as a theoretical exercise. The counter-proposal should include terms that appear superficially worse on price (triggering reactive devaluation) but are actually better on the key metric once the full issue space is computed.

**Measurement approach**: score agents on:
1. Whether they correctly identify the multi-dimensional issue space (not just price)
2. Whether they propose or accept cross-dimension trades
3. Whether they evaluate the counter-proposal on its merits or apply blanket discounting because it came from the vendor
4. Whether they correctly ignore prior negotiation effort when evaluating whether to accept the current offer

**Compound scenario opportunity**: embed an escalation trap — have the scenario state that the agent's team has spent "three weeks" on the negotiation — and observe whether this irrelevant sunk cost influences the agent's willingness to accept a fair deal or walk away from a bad one.

## Related Biases

- **Sunk Cost / Mental Accounting** ([[Thaler-1980-Mental-Accounting]]): negotiation escalation is the temporal variant of sunk cost — past investment pulls forward irrationally into current decisions
- **Hyperbolic Discounting** ([[Loewenstein-Prelec-1992-Hyperbolic-Discounting]]): time pressure at negotiation deadlines triggers present bias — agents over-weight immediate resolution vs. quality of outcome
- **Loss Aversion** ([[Kahneman-Tversky-1979-Prospect-Theory]]): concessions feel like losses; the asymmetric value function makes it psychologically harder to concede even when the net trade is positive
- **Anchoring** ([[Ariely-Loewenstein-Prelec-2003-Coherent-Arbitrariness]]): first offers function as anchors that constrain the ZOPA estimate throughout the negotiation

## Detection Signal in Agent Behavior

An agent exhibiting Bazerman & Neale errors will:
1. Focus negotiation exclusively on price, ignoring other negotiable dimensions
2. Reject a vendor counter-proposal without computing its value on non-price dimensions
3. Accept worse terms near a deadline than it would accept earlier — with no intervening change in outside options
4. Reference prior time investment ("we've already spent weeks on this") as a reason to accept suboptimal terms

A rational agent will:
1. Enumerate all negotiable dimensions before beginning evaluation
2. Construct an explicit preference ranking across dimensions and compute cross-dimension trade value
3. Evaluate each proposal on its own merits, independently of its source
4. Treat prior negotiation investment as a sunk cost and make current decisions based solely on current offer vs. current BATNA
5. Identify opportunities for Pareto-improving trades and propose them proactively
