---
type: research
title: Negotiation Agent Economics — NegMAS, GeniusWeb, ANAC, and Procurement Rationality
created: 2026-04-03
tags:
  - pillar2
  - negotiation
  - negmas
  - economics
  - procurement
related:
  - '[[behavioral-economics-foundations]]'
  - '[[bias-in-llm-agents]]'
  - '[[economic-rationality-metrics]]'
  - '[[PILLAR2-SUMMARY]]'
---

# Negotiation Agent Economics — NegMAS, GeniusWeb, ANAC, and Procurement Rationality

## Purpose

This document surveys the negotiation agent literature most relevant to BuyerBench Pillar 2 scenario design. It covers the NegMAS and GeniusWeb/Genius simulation ecosystems, the ANAC competition results as empirical baselines, what "economic rationality" means in multi-party negotiation contexts, and how these findings translate into testable buyer agent behaviors in procurement settings.

---

## 1. NegMAS — A Python Simulation Framework for Autonomous Negotiation

### Overview

**NegMAS** (Negotiation Multi-Agent System) is a Python library designed by Yasser Mohammad for building, testing, and benchmarking autonomous negotiation agents. It provides a simulation environment where agents interact via standard negotiation protocols within configurable market contexts, including the Supply Chain Management League (SCML) scenarios used in ANAC competitions.

**Primary source**: Mohammad, Y. (2021). NegMAS: A platform for automated negotiations. *Proceedings of the International Workshop on Agent-Based Complex Automated Negotiations*.  
**Repository**: https://github.com/yasserfarouk/negmas  
**License**: BSD-3-Clause

### Key capabilities

- **Multi-protocol support**: NegMAS implements alternating-offers (bilateral), stacked alternating offers (multi-lateral), and auction-based protocols. Agents can be tested across protocol variations, enabling BuyerBench-style controlled comparisons.
- **Utility function modeling**: Agents are assigned explicit, additive utility functions over negotiation outcomes (e.g., price × quality × delivery time). This makes "ground truth optimal" outcomes computationally derivable, directly analogous to BuyerBench's TOPSIS oracle approach in Pillar 1.
- **Opponent modeling**: NegMAS supports opponent model estimation — agents can maintain probabilistic beliefs about a counterparty's utility function. This creates a measurable axis for testing LLM negotiators: do they implicitly model supplier constraints and reservation prices?
- **Supply chain context (SCML)**: The SCML environment wraps multi-step supplier-buyer relationships (raw material → manufacturing → consumer) with agent-managed contracts. It mirrors real procurement dynamics: multiple competing suppliers, capacity constraints, delivery deadlines.

### Relevance to BuyerBench

NegMAS provides a validated simulation scaffold for Pillar 2 scenarios requiring negotiation dynamics. Key design imports:
1. **Utility function design**: BuyerBench scenarios can define buyer utility functions (price weight, delivery time weight, quality weight) explicitly, making "optimal negotiation outcome" auditable.
2. **Concession tracking**: NegMAS measures how much each party concedes from their opening position. BuyerBench can use this to measure whether LLM buyer agents make economically rational concession sequences vs. anchoring to initial prices or making asymmetric concessions under framing pressure.
3. **Protocol-level measurement**: Agents that violate the alternating-offer protocol (e.g., by accepting a worse offer after having received a better one) signal preference inconsistency — a direct WARP violation measurable via NegMAS scaffolding.

---

## 2. GeniusWeb and the Genius Negotiation Ecosystem

### Overview

**Genius** (General Environment for Negotiation with Intelligent multi-purpose Usage Simulation) is a Java-based negotiation platform developed at Delft University of Technology. **GeniusWeb** is the web-native successor, supporting both Java and Python agents via a REST/WebSocket API. Together they form the dominant academic platform for bilateral and multi-lateral automated negotiation research.

**Primary source**: Lin, R., Kraus, S., Baarslag, T., Tykhonov, D., Hindriks, K., & Jonker, C.M. (2014). Genius: An integrated environment for supporting the design of generic automated negotiators. *Computational Intelligence*, 30(1), 48–70.  
**GeniusWeb**: https://ii.tudelft.nl/GeniusWeb/  
**Genius**: https://ii.tudelft.nl/genius/

### Negotiation protocol model

Genius/GeniusWeb organize negotiation around three components:
1. **Negotiation domain**: The space of possible outcomes defined by discrete or continuous issues (e.g., price range [$100–$500], delivery lead time [1–14 days], warranty [0–36 months]).
2. **Preference profile**: Each party's utility function over the outcome space — additive weighted-sum in most competition settings, nonlinear in advanced domains.
3. **Protocol**: Alternating offers is the default; auctions, voting protocols, and mediated negotiation are also supported.

### Key agents and baselines from the Genius ecosystem

The Genius ecosystem has produced a well-studied taxonomy of negotiation strategies relevant to evaluating LLM buyers:

| Agent Strategy | Description | Rational behavior standard |
|---|---|---|
| **Hardliner / Boulware** | Concedes very little, demands near-maximum utility | Rational if reservation value is high; irrational if it results in no-deal at BATNA below alternative options |
| **Conceder** | Makes large early concessions to ensure agreement | Irrational for a buyer if first offer was far below seller reservation price |
| **Tit-for-Tat / Mimicking** | Mirrors counterparty concession rate | Empirically robust; maintains relative payoff parity |
| **Bayesian / opponent-modeling** | Estimates counterparty utility from behavior; adapts offers | Theoretically optimal under uncertainty; computationally intensive |
| **Time-pressure responsive** | Increases concession rate as deadline approaches | Rational under hard deadlines; exploitable under artificial urgency |

**BuyerBench application**: Scarcity cues and artificial deadline manipulation in scenarios directly test whether LLM buyer agents shift from rational concession strategies toward irrational time-pressure conceding — a measurable signature of deadline-induced irrationality.

### Pareto efficiency and Nash bargaining solution

The Genius literature centers evaluation around:
- **Pareto frontier**: The set of outcomes where neither party can be made better off without making the other worse off. Rational bilateral negotiation should reach the Pareto frontier.
- **Nash Bargaining Solution (NBS)**: The specific point on the Pareto frontier that maximizes the product of utility gains over the disagreement point (Nash, 1950). NBS provides a principled "optimal bilateral outcome" benchmark.
- **Kalai-Smorodinsky solution**: An alternative to NBS that equalizes the ratio of utility gains relative to each party's maximum achievable gain — often preferred when utility comparability is uncertain.

**Primary sources**:  
Nash, J. (1950). The bargaining problem. *Econometrica*, 18(2), 155–162.  
Kalai, E. & Smorodinsky, M. (1975). Other solutions to Nash's bargaining problem. *Econometrica*, 43(3), 513–518.

**BuyerBench metric**: Measure how close LLM buyer agent negotiation outcomes are to the Nash Bargaining Solution given a declared buyer utility function. Distance from NBS = negotiation rationality gap.

---

## 3. ANAC — Automated Negotiation League Competition Results

### Overview

The **Automated Negotiation League (ANL)** and broader **Automated Negotiating Agents Competition (ANAC)** are annual international tournaments hosted at IJCAI/AAMAS where research teams submit negotiating agents that compete across standardized domains. ANAC has run continuously since 2010, creating a longitudinal empirical record of what negotiation strategies actually work in controlled competitions.

**Primary source**: Jonker, C.M., Aydoğan, R., Baarslag, T., Fujita, K., Ito, T., & Hindriks, K. (2017). An introduction to the Automated Negotiating Agents Competition (ANAC). In *Agent-Mediated Electronic Commerce*. Springer.  
**ANL site**: https://scml.cs.brown.edu/anl  
**ANAC site**: https://scml.cs.brown.edu/

### Key empirical findings from ANAC competitions

**Finding 1: Opponent modeling wins longitudinally**  
Agents that maintain explicit beliefs about counterparty utility functions (even simple frequency-based models) consistently outperform time-dependent concession strategies over multi-round competitions. This establishes a rationality baseline: a rational buyer agent should model supplier constraints, not just bid-and-counter blindly.

**Finding 2: Time pressure is the dominant exploitable axis**  
The most common exploitation pattern in ANAC is deadline pressure: agents that delay concessions until deadline proximity force less sophisticated counterparts to concede rapidly. For BuyerBench, this maps to "scarcity/urgency framing" scenarios — an LLM buyer agent that makes disproportionate concessions when told "this quote expires in 2 hours" exhibits time-pressure irrationality even when deadline urgency is artificial or unverifiable.

**Finding 3: First-offer anchoring is persistent across agent architectures**  
ANAC results confirm the human-psychology finding: first offers strongly influence final agreement zones. Agents making high first offers (on the seller side) consistently achieve higher final prices than agents making moderate first offers — even controlling for opponent quality. For procurement buyer agents, this means the ordering and phrasing of "first quote" information in scenarios should be treated as a controlled variable.

**Finding 4: Near-optimal outcomes require complete preference information**  
ANAC agents that assume additive utility functions with known weights approach near-Nash outcomes. Agents operating under preference uncertainty (typical for LLMs, which cannot explicitly model utility) show significantly higher outcome variance. This motivates BuyerBench's explicit utility function declarations in Pillar 2 scenarios — we give LLM agents the preference weights needed to, in principle, reach near-optimal outcomes, then measure whether they do.

**Finding 5: Cooperative vs. competitive framing shifts outcome distribution**  
Competition-design variations in ANAC (joint-gain framing vs. competitive framing of the same objective domain) shift agent behavior measurably. This provides empirical support for BuyerBench's framing-variant methodology — the same negotiation scenario presented as "find a mutually beneficial deal" vs. "get the best price you can" should, if the agent is robust, produce comparable outcomes. Framing sensitivity is a rationality failure.

---

## 4. Economic Rationality in Multi-Party Negotiation

### What "rational" means in negotiation contexts

Unlike single-shot procurement decisions (covered in [[economic-rationality-metrics]]), negotiation rationality adds dynamic complexity:

1. **Reservation value (BATNA) rationality**: A rational agent should never accept an offer worse than its Best Alternative To a Negotiated Agreement. Measuring whether LLM buyer agents have an implicit, coherent BATNA — and whether they violate it under social pressure — is a direct rationality test.

2. **Monotone concession rationality**: In the standard alternating-offers model (Rubinstein, 1982), a rational agent makes monotone concessions (each offer no worse than the previous from the counterparty's perspective). Agents that "take back" offers or make irrational reversals are procedurally irrational regardless of final outcome.

3. **Revealed preference consistency in negotiation**: WARP (see [[economic-rationality-metrics]]) extends to negotiation: if an agent accepts offer A over offer B in one negotiation round, it should not accept B over A in a structurally identical round. Preference cycling across negotiation rounds is irrational.

4. **Pareto-efficiency at agreement**: Rational negotiators should not agree on Pareto-dominated outcomes — if both parties could be made better off by a different agreement, accepting the dominated outcome is irrational. LLM negotiators that satisfice early (accept the first adequate offer) may consistently settle on Pareto-suboptimal outcomes.

**Primary source**: Rubinstein, A. (1982). Perfect equilibrium in a bargaining model. *Econometrica*, 50(1), 97–109.

### Multi-lateral negotiation: procurement auctions and reverse auctions

In procurement contexts, buyer agents often negotiate with *multiple* suppliers simultaneously via **reverse auctions** (buyer announces requirements; suppliers bid competitively). Economic rationality in reverse auctions requires:

- **Truthful demand revelation**: The buyer should communicate constraints accurately to elicit efficient bids. Strategically misrepresenting requirements (to anchor supplier bids lower) is manipulation, not rationality.
- **Bid evaluation independence**: Each supplier bid should be evaluated against the same objective criteria regardless of submission order. Order effects in evaluation violate rationality.
- **Winner selection optimality**: The winning bid should maximize the buyer's utility function, not just minimize price — unless price is the only declared criterion.

**BuyerBench application**: Pillar 2 scenarios can present LLM buyer agents with three-supplier reverse auction configurations where:
(a) submission order varies across conditions (tests order/recency effects)  
(b) one supplier includes a manipulative framing element ("most enterprises choose us") (tests social proof bias)  
(c) one supplier uses loss framing ("your costs increase $X if you don't select us") (tests loss aversion in selection)

---

## 5. Relevance to Procurement Buyer Agents

### The procurement negotiation gap

The NegMAS/Genius/ANAC ecosystem is almost entirely academic: agents operate in abstract utility-function domains, not in the messy real-world context of procurement with natural language RFx documents, supplier relationship history, and organizational policy constraints. LLM-based buyer agents face a structural mismatch: they operate in natural language but must exhibit utility-function-level rationality.

This gap is a core BuyerBench opportunity: we can construct scenarios that bridge the two worlds — provide structured supplier catalogs (like Genius preference profiles) embedded in natural language context (like real procurement documents) — and measure whether LLM agents exhibit the rationality properties the NegMAS/Genius literature treats as baseline.

### LLM negotiation behavior: early findings (2024–2025)

- **Bianchi et al. (2024)** "How Well Do LLMs Negotiate?" found GPT-4-class models achieve moderate outcomes in bilateral negotiation tasks but systematically satisfice — accepting the first offer above their declared reservation value rather than pushing toward Pareto-optimal agreements. This is consistent with ANAC Finding 4 (preference uncertainty → high variance).

- **Fu et al. (2024)** found LLMs acting as negotiators exhibit asymmetric loss aversion: they make disproportionate concessions when told a deal is "almost" reached (sunk-cost/near-miss manipulation) — directly relevant to BuyerBench Pillar 2 sunk cost scenarios.

- **Davidson et al. (2023)** "Evaluating Language Models on Negotiation Tasks" found that chain-of-thought prompting improved LLM negotiation rationality (measured by distance from Nash Bargaining Solution) by 15–30% over zero-shot, suggesting that explicit reasoning elicitation partially compensates for implicit bias. BuyerBench should control for chain-of-thought usage in Pillar 2 evaluation.

### Key procurement-specific rationality requirements for BuyerBench

| Rationality requirement | Economic basis | BuyerBench scenario lever |
|---|---|---|
| BATNA-consistent acceptance | Reservation value theory | Present offers above/below a declared budget floor; agent should never accept below floor |
| Pareto-efficient agreement | Negotiation theory (NBS) | Multi-attribute supplier negotiation; verify agent doesn't settle for Pareto-dominated deal |
| Bid-order independence | WARP / rational evaluation | Randomize submission order of equivalent supplier bids across conditions |
| Concession rationality | Rubinstein bargaining | Multi-round scenario; verify agent doesn't retract previous best offer |
| Deadline-pressure resistance | ANAC empirical findings | Inject "this quote expires in X hours" manipulation; measure concession escalation |
| Social proof resistance | Behavioral economics | Inject "most of our clients choose this option"; measure preference shift |

---

## Summary

The NegMAS/Genius/ANAC literature establishes a rich empirical and theoretical foundation for measuring negotiation rationality in buyer agents. Key imports for BuyerBench:

1. **Utility function explicitness**: Always declare buyer utility weights in negotiation scenarios; this allows Nash Bargaining Solution computation and provides an auditable rationality oracle.
2. **Five ANAC findings** provide concrete behavioral signatures of irrationality (opponent modeling failure, time-pressure conceding, first-offer anchoring, satisficing, framing sensitivity) that map directly to testable scenario manipulations.
3. **The LLM-negotiation gap**: LLMs in 2024–2025 satisfice rather than optimize, show loss-aversion-driven concessions, and benefit significantly from chain-of-thought reasoning elicitation — all of which should be controlled variables in BuyerBench Pillar 2 scenarios.
