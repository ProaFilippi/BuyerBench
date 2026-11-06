---
type: product
title: "NegMAS — Negotiation Multi-Agent System"
created: 2026-04-05
tags:
  - open-source
  - negotiation
  - multi-agent
  - benchmark
  - python
  - anac
  - supply-chain
  - pillar1
  - pillar2
related:
  - '[[Zycus]]'
  - '[[ACP]]'
  - '[[INDEX]]'
---

# NegMAS — Negotiation Multi-Agent System

> The open-source Python platform for situated autonomous negotiation — the official engine behind ANAC international competitions and a supply-chain negotiation simulation environment relevant to all three BuyerBench pillars

## Overview

**NegMAS** (NEGotiation MultiAgent System, alternatively: NEGotiations Managed by Agent Simulations) is an open-source Python library for developing, evaluating, and benchmarking autonomous negotiation agents embedded in simulation environments. Authored by Yasser Mohammad at Brown University, it is the technical backbone for the **Automated Negotiating Agents Competition (ANAC)** — the premier international research competition for bilateral and multilateral negotiation agents, co-located with IJCAI/AAMAS annually since 2010.

Unlike commercial procurement AI platforms (Salesforce Agentforce, Procure AI, Zycus Merlin ANA), NegMAS is purely a **research and evaluation framework**: it provides the negotiation mechanisms, utility function models, tournament evaluation infrastructure, and multi-agent simulation world (SCML) needed to study, compare, and benchmark negotiation strategies without operational constraints.

The library is actively maintained as of 2026, with the current release being **NegMAS 0.15.4** (January 16, 2026). It is installable via pip, documented on ReadTheDocs, and has a companion Java bridge (`jnegmas`) for interoperability with the established Genius platform (the ANAC legacy system for Java-based negotiation agents).

> **BuyerBench relevance (Pillar 1):** NegMAS's Supply Chain Management League (SCML) is the closest open-source equivalent to a realistic buyer-agent benchmark. SCML agents negotiate buying (raw materials) and selling (finished goods) across a multi-stage supply chain, optimizing factory profit — mapping directly to BuyerBench Pillar 1 workflow accuracy and supplier selection scenarios. NegMAS is already integrated as a BuyerBench agent adapter (`negmas` agent ID in CLAUDE.md).

> **BuyerBench relevance (Pillar 2):** The Automated Negotiation League (ANL) within ANAC uses bilateral alternating-offers with configurable utility functions that can encode framing, anchoring, and loss-aversion variants. BuyerBench Pillar 2 can use NegMAS's SAOMechanism with manipulated utility functions to stress-test whether AI buyer agents are susceptible to opponent negotiation tactics that exploit known behavioral biases (e.g., high opening anchors, scarcity framing, sunk-cost commitment pressure).

## Quick Facts

| Attribute | Value |
|-----------|-------|
| Library Name | NegMAS |
| Full Name | Negotiation Multi-Agent System |
| Author | Yasser Mohammad (yasserfarouk), Brown University |
| License | MIT (open source) |
| Current Version | 0.15.4 (2026-01-16) |
| Python Support | Python 3.8+ |
| GitHub | github.com/yasserfarouk/negmas |
| PyPI | pypi.org/project/negmas |
| Documentation | negmas.readthedocs.io/en/latest |
| ANAC Integration | Official engine for ANL and SCML leagues |
| Genius Bridge | jnegmas (Java interop for legacy Genius agents) |
| BuyerBench Agent ID | `negmas` (Python-native, no credentials required) |

## Architecture

NegMAS is organized around three core conceptual layers:

### 1. Agents

**Negotiators** are the autonomous agents in NegMAS. Each negotiator has:
- A **utility function** (UtilityFunction) — a preference model over possible outcomes in the negotiation domain
- A **negotiation strategy** — the decision logic for generating offers, responding to offers, and ending negotiations
- Optional **theory-of-mind** modeling — predicting opponents' utility functions from observed behavior

Pre-built negotiators include:
- `AspirationNegotiator` — time-based concession with aspiration levels
- `ToughNegotiator` / `OnlyBestNegotiator` — hardline strategies; never concedes
- `NaiveTitForTatNegotiator` — reactive tit-for-tat concession
- `BoulwareLindaNegotiator` — Boulware curve (slow early, fast late concessions)
- `NegotiatorUtility`-based custom agents using any callable utility function

### 2. Mechanisms

**Mechanisms** define the rules of negotiation. Key built-in mechanisms:

| Mechanism | Description |
|-----------|-------------|
| `SAOMechanism` | **Stacked Alternating Offers** — the default; negotiators alternate offers until unanimous acceptance, walkout, or timeout |
| `GBMechanism` | Generalized Bargaining — configurable acceptance and offer protocols |
| `VetoMechanism` | Multi-party negotiation with veto rights |
| `STACKELBERGMechanism` | Stackelberg leader-follower offer protocol |
| `TAUMechanism` | Tentative Agreement + Updating |

`SAOMechanism` is used in ANAC ANL and is the canonical mechanism for buyer-seller bilateral negotiation in BuyerBench scenarios.

### 3. World (SCML)

The **Supply Chain Management League World** (`SCML2020World`, `SCML2024World`, etc.) is a multi-agent simulation environment where:
- Agents manage factories in a multi-stage supply chain
- Each factory **buys** inputs (raw materials or semi-finished goods) and **sells** outputs (processed goods or finished products)
- Negotiations are **situated**: each buying and selling negotiation is linked to real production schedules, inventory, and financial state
- Agents maximize profit across all interconnected negotiations simultaneously

This world-level simulation is the primary instrument for **Pillar 1 supply chain buyer agent evaluation** in BuyerBench — it directly models the economic optimization problem that enterprise procurement AI must solve.

## ANAC Competition Integration

NegMAS is the official engine for the **Automated Negotiating Agents Competition (ANAC)**, now in its **16th edition (ANAC 2025)**, co-located with IJCAI 2025 in Montreal, Canada (August 21, 2025). ANAC has run annually since 2010, making it the longest-running international benchmark for autonomous negotiation.

### ANAC 2025 Leagues

| League | Description | NegMAS Component |
|--------|-------------|-----------------|
| **Automated Negotiation League (ANL 2025)** | Sequential multi-deal bilateral negotiation; agents face multiple opponents in sequence; rewarded for optimal deal combinations across the sequence | `SAOMechanism` + `ANLWorld` |
| **Supply Chain Management League (SCML 2025)** | Factory manager agent negotiates buying and selling in a simulated supply chain; maximizes net profit | `SCML2025World` |

The `anl2025` package (autoneg/anl2025 on GitHub) is a thin wrapper around NegMAS that provides the ANL 2025 competition scaffolding, submission templates, and evaluation harness. This wrapper pattern directly mirrors how BuyerBench adapters wrap agents.

### Historical Competition Data

NegMAS ships with benchmark scenarios drawn from **ANAC 2010 through ANAC 2018** Genius competition data (stored in `tests/data` and `notebooks/data`). These domains are two-sided bilateral negotiations over multi-issue spaces (price, quantity, delivery terms, etc.) and serve as a standardized test set for comparing new negotiators against the historical ANAC field.

## Key Algorithms Supported

NegMAS's utility function and strategy components support the following classic negotiation algorithms out of the box, plus extension points for custom strategies:

| Algorithm / Model | Type |
|------------------|------|
| Aspiration-based concession (time-dependent) | Concession strategy |
| Boulware / Conceder curves | Concession strategy |
| Tit-for-Tat variants | Reactive strategy |
| Nash Bargaining Solution | Theoretical optimum |
| Pareto-frontier discovery | Multi-agent optimality |
| Kalai-Smorodinsky solution | Fairness-aware solution |
| Inverse utility learning | Opponent modeling |
| ANAC Genius agent bridge | Java-based legacy strategies |

## Installation and Quickstart

### Installation

```bash
# Core library
pip install negmas

# With Genius bridge (requires Java JDK)
pip install negmas[genius]

# With visualization
pip install negmas[visualization]

# All optional dependencies
pip install negmas[all]
```

### Quickstart: Bilateral Buyer-Seller Negotiation

```python
from negmas import SAOMechanism
from negmas.negotiators import AspirationNegotiator
from negmas.outcomes import make_issue

# Define a 2-issue domain: price (50–200) and quantity (1–10)
issues = [
    make_issue(values=(50, 200), name="price"),
    make_issue(values=(1, 10), name="quantity"),
]

# Create SAO mechanism (alternating offers, 50-step time horizon)
mechanism = SAOMechanism(issues=issues, n_steps=50)

# Add buyer: prefers low price, high quantity
buyer = AspirationNegotiator(name="buyer")
mechanism.add(buyer, ufun=lambda x: (1 - (x["price"] - 50) / 150) * (x["quantity"] / 10))

# Add seller: prefers high price, low quantity
seller = AspirationNegotiator(name="seller")
mechanism.add(seller, ufun=lambda x: ((x["price"] - 50) / 150) * (1 - x["quantity"] / 10))

# Run negotiation
state = mechanism.run()
print(f"Agreement: {state.agreement}, Rounds: {state.step}")
```

### Tournament Evaluation

```python
from negmas.tournaments import neg_tournament, cartesian_tournament

# Compare negotiators against common opponents
results = neg_tournament(
    competitors=[MyBuyerAgent, AspirationNegotiator],
    n_repetitions=10,
    n_steps=100,
)

# Run all competitors against each other
results = cartesian_tournament(
    competitors=[AgentA, AgentB, AgentC],
    n_repetitions=5,
)
```

## Relevance as BuyerBench Test Harness Component

NegMAS is already integrated into BuyerBench as the `negmas` agent adapter — the only Python-native agent in the benchmark suite that requires no external API credentials. This makes it uniquely useful as a **baseline and sanity-check agent**: when BuyerBench needs to verify that a scenario is correctly specified (i.e., that a reasonable agent can succeed at it), NegMAS provides a deterministic, well-characterized agent that can be expected to perform optimally on well-formed bilateral negotiation problems.

Specific integration patterns:

| BuyerBench Use Case | NegMAS Component |
|--------------------|-----------------|
| Pillar 1 supplier selection benchmark | SCML World — buy/sell negotiation with supply chain constraints |
| Pillar 1 quote comparison baseline | `neg_tournament()` with catalog-priced offers modeled as utility functions |
| Pillar 2 bias susceptibility testing | SAOMechanism with utility functions encoding anchoring / framing variants |
| Pillar 2 consistency across variants | `cartesian_tournament()` comparing outcomes across framing conditions |
| Protocol correctness verification | SAOMechanism protocol adherence (step sequencing, timeout behavior) |

**Comparison to Zycus Merlin ANA:** Zycus's Merlin ANA is the commercial enterprise counterpart — a closed, production-deployed autonomous supplier negotiation agent operating in real procurement environments with human oversight and ERP integration. NegMAS is the open-source research equivalent: configurable, transparent, and optimized for academic benchmarking rather than enterprise deployment. BuyerBench scenarios should use NegMAS as the **algorithmic floor** (what a theoretically optimal negotiator achieves) and Merlin ANA benchmarks as the **commercial ceiling** (what state-of-the-art enterprise systems demonstrate in production).

## BuyerBench Pillar Relevance

### Pillar 1 — Agent Intelligence and Operational Capability

NegMAS SCML directly tests the core Pillar 1 scenario type: a buyer agent receiving a sourcing objective, discovering suppliers (upstream factories), negotiating price/quantity/delivery terms, and executing transactions — all within a simulated operational environment with real supply/demand constraints. The `negmas` BuyerBench adapter should be used to establish baseline workflow completion rates before evaluating proprietary agents.

### Pillar 2 — Economic Decision Quality and Behavioral Robustness

NegMAS's configurable utility functions make it the ideal instrument for Pillar 2 bias injection. By constructing utility function pairs that are economically identical but presented differently (e.g., framing a $50 discount as a "gain" vs. the same outcome framed as avoiding a $50 loss), BuyerBench can use NegMAS's SAOMechanism to quantify whether AI buyer agents under test are susceptible to framing effects, anchoring bias (high first-offer influence), or sunk-cost fallacy (over-committing to failing negotiation threads). NegMAS's tournament infrastructure also makes it practical to run statistically significant sample sizes (50–100 negotiation runs per variant) without incurring API costs.

### Pillar 3 — Security, Compliance, and Market Readiness

NegMAS does not natively model payment security or compliance. However, NegMAS SCML negotiations generate **binding financial commitments** (contracts for goods at agreed prices), and BuyerBench Pillar 3 can instrument these to test whether an AI buyer agent:
- Refuses to execute contracts that exceed pre-authorized spending limits
- Correctly attributes payments to the right negotiation sessions (no cross-session credential leakage)
- Generates auditable contract trails sufficient to reconstruct a procurement decision tree

## Related Entities

- [[Zycus]] — Commercial counterpart: Merlin ANA is the production autonomous supplier negotiation agent; NegMAS is the open-source research equivalent. Pillar 1+2 comparison baseline.
- [[ACP]] — ACP defines the payment execution layer that NegMAS-negotiated contracts would ultimately route through in a real agentic commerce stack. NegMAS handles the negotiation; ACP handles the transaction.
- [[Procure-AI]] — Enterprise procurement orchestration; Procure AI's 50+ agents represent the commercial Pillar 1 capability ceiling; NegMAS provides the open-source algorithmic floor.
- [[Fairmarkit]] — Fairmarkit's demand-to-award sourcing agents represent a scaled commercial version of the multi-supplier selection problem NegMAS models in research settings.

## Sources

1. [NegMAS GitHub Repository](https://github.com/yasserfarouk/negmas) — yasserfarouk/negmas; accessed 2026-04-05
2. [NegMAS PyPI Package](https://pypi.org/project/negmas/) — v0.15.4, released 2026-01-16; accessed 2026-04-05
3. [NegMAS Documentation (ReadTheDocs)](https://negmas.readthedocs.io/en/latest/) — v0.15.4 stable docs; accessed 2026-04-05
4. [NegMAS: A Platform for Situated Negotiations (ResearchGate)](https://www.researchgate.net/publication/351452859_NegMAS_A_Platform_for_Situated_Negotiations) — Mohammad, Y. (2021); foundational paper; accessed 2026-04-05
5. [ANAC 2025 — 16th Automated Negotiating Agents Competition](https://web.tuat.ac.jp/~katfuji/ANAC2025/) — IJCAI 2025, Montreal, Aug 21 2025; accessed 2026-04-05
6. [ANL 2025 Competition Documentation](https://autoneg.github.io/anl2025/) — Automated Negotiation League 2025; accessed 2026-04-05
7. [ANAC at AAMAS 2025 — IFAAMAS Proceedings](https://www.ifaamas.org/Proceedings/aamas2025/pdfs/p3000.pdf) — Competition proceedings; accessed 2026-04-05
8. [ANAC Live Competition (SCML)](https://scml.cs.brown.edu/) — Brown University SCML live competition platform; accessed 2026-04-05
9. [Running a Negotiation Tutorial — NegMAS Docs](https://negmas.readthedocs.io/en/v0.11.3/tutorials/01.running_simple_negotiation.html) — SAOMechanism quickstart; accessed 2026-04-05
10. [jnegmas — Java Interface to NegMAS](https://github.com/yasserfarouk/jnegmas) — Genius bridge repository; accessed 2026-04-05

---
*Last updated: 2026-04-05*
