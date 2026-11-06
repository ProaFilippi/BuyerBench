---
type: person
title: "Yasser Mohammad"
created: 2026-04-06
tags:
  - researcher
  - academic
  - negmas
  - negotiation
  - supply-chain
  - pillar1
  - pillar2
related:
  - '[[NegMAS]]'
  - '[[ACES-AI-Agent-Buying]]'
---

# Yasser Mohammad

> Creator of NegMAS (Negotiation Multi-Agent System) — the official engine of ANAC (Automated Negotiation Agents Competition) for 16 years and the `negmas` agent reference implementation in BuyerBench

## Role

Researcher, NEC Corporation / National Institute of Advanced Industrial Science and Technology (AIST); formerly Özyeğin University (Istanbul)

## Background

Yasser Mohammad (GitHub: `yasserfarouk`) is a computer scientist and researcher specializing in multi-agent systems, automated negotiation, and supply chain simulation. He is the primary creator and maintainer of NegMAS, which he developed across multiple academic affiliations including NEC Corporation (Tokyo), AIST (Tokyo), Assiut University (Egypt), and Özyeğin University (Istanbul, Turkey).

| Field | Detail |
|-------|--------|
| Primary Affiliation | NEC Corporation, Japan |
| Additional Affiliations | AIST (Tokyo), Assiut University (Egypt), Özyeğin University (Istanbul) |
| Specialization | Multi-agent systems, automated negotiation, supply chain AI |
| GitHub | [github.com/yasserfarouk](https://github.com/yasserfarouk) |
| Personal Site | [yasserm.com](http://www.yasserm.com/software/) |

## Key Contributions to Agentic Commerce

### NegMAS (Negotiation Multi-Agent System)

NegMAS is a Python library for developing autonomous negotiation agents embedded in simulation environments. It supports bilateral and multilateral negotiations, multiple negotiation protocols (SAOMechanism, MechanismState, etc.), and complex multi-agent simulations where negotiations are interdependent.

**Why NegMAS matters for buyer agents:**
- **Situated negotiations**: Unlike abstract game-theory solvers, NegMAS agents negotiate in dynamic environments where external factors (supplier capacity, market price shifts) affect utility in real time
- **Supply chain focus**: The SCML (Supply Chain Management League) module enables full multi-echelon supplier negotiation simulation
- **Configurable utility functions**: Enables controlled Pillar 2 bias experiments by allowing utility function manipulation while holding agent negotiation behavior constant

### ANAC Leadership

NegMAS has been the official negotiation engine for the **Automated Negotiation Agents Competition (ANAC)** — a 16-year running competition at IJCAI — since its adoption. This gives NegMAS its status as the community-standard benchmark for autonomous negotiation research.

### Key NegMAS Capabilities

| Module | Purpose |
|--------|---------|
| `SAOMechanism` | Bilateral alternating-offers negotiation (standard buyer-seller) |
| `SCML` | Supply Chain Management League — multi-echelon simulation |
| `Negotiator` | Base class for custom negotiation agents |
| `UtilityFunction` | Configurable preference modeling for bias research |

### Co-Creators

- **Shinji Nakadai** — NEC Corporation, Japan
- **Amy Greenwald** — Brown University (computer science, mechanism design)

## Published Papers

- *"NegMAS: A Platform for Automated Negotiations"* — PRIMA 2020, Springer
- *"NegMAS: A Platform for Situated Negotiations"* — Springer (PRIMA chapter)
- PyPI package: [negmas 0.9.6](https://pypi.org/project/negmas/0.9.6/)
- GitHub: [github.com/yasserfarouk/negmas](https://github.com/yasserfarouk/negmas)

## BuyerBench Pillar Relevance

> **BuyerBench relevance:** NegMAS is the `negmas` agent in BuyerBench (agent ID: `negmas`) — a Python-native reference implementation that requires no API credentials and demonstrates economically grounded negotiation behavior. For **Pillar 1**, SCML scenarios provide realistic multi-supplier environments. For **Pillar 2**, NegMAS's configurable utility functions allow researchers to test whether agents exhibit irrational bias even when the objectively optimal negotiation outcome is mathematically computable.

## Sources

- [GitHub: yasserfarouk/negmas](https://github.com/yasserfarouk/negmas)
- [NegMAS: A Platform for Automated Negotiations (Springer)](https://link.springer.com/chapter/10.1007/978-3-030-69322-0_23)
- [yasserm.com/software](http://www.yasserm.com/software/)
- [PyPI negmas](https://pypi.org/project/negmas/0.9.6/)
