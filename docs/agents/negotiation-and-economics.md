---
type: reference
title: Negotiation and Economic Simulation Agent Profiles
created: 2026-04-03
tags:
  - agent-profile
  - negotiation
  - economics
  - open-source
related:
  - '[[INDEX]]'
  - '[[AGENT-LANDSCAPE-SUMMARY]]'
---

# Negotiation and Economic Simulation Agent Profiles

Profiles for E13–E16: NegMAS, GeniusWeb/Genius, ANAC, and AI Economist.
These are primarily academic / open-source systems focused on negotiation
mechanics and economic simulation.  NegMAS is directly integrated into
BuyerBench via the `negmas` adapter (see `agents/negmas_agent.py`).

---

## E13 — NegMAS

**Category:** Negotiation  
**Ownership:** Academic-led open-source project (Yasser Mohammad)  
**Licence:** BSD-3-Clause  
**Pricing:** Free / open-source  
**Maturity:** Research / education

### What it is
NegMAS (Negotiation Multi-Agent System) is a Python library for building and
evaluating autonomous negotiation agents embedded in simulation environments.
It supports multiple negotiation protocols (alternating offers, auctions,
mediated mechanisms), utility function modelling, and opponent modelling.
The library is used in ANAC competition infrastructure and academic research.

### BuyerBench integration
**Directly integrated** via `agents/negmas_agent.py`.

The NegMASAgent maps BuyerBench Pillar 1 multi-criteria scenarios to NegMAS
`LinearUtilityFunction` evaluations.  Supplier selection is framed as a
utility maximisation problem:

```
U = cost_weight × cost_score
  + quality_weight × quality_score
  + delivery_weight × delivery_reliability
```

where `cost_score = (max_price - unit_price) / price_range` (normalised).

### BuyerBench pillar relevance

| Pillar | Relevance | Notes |
|---|---|---|
| P1 — Capability | **Very High** | Utility-function maximisation is the core Pillar 1 evaluation task |
| P2 — Economic Rationality | **High** | NegMAS utility models can be systematically tested under biased input perturbations |
| P3 — Security | **Low** | No payment flow; academic framework |

### Evaluation results (BuyerBench run: 2026-04-03)

Evaluated on all 5 Pillar 1 scenarios using `agents/negmas_agent.py` in
simulation mode:

| Scenario | Score | Pass |
|---|---|---|
| p1-01 Supplier Selection | 1.00 | ✓ |
| p1-02 Multi-Criteria Sourcing | 1.00 | ✓ |
| p1-03 Quote Comparison | 0.20 | ✗ |
| p1-04 Policy-Constrained Procurement | 0.00 | ✗ |
| p1-05 Multi-Step Workflow | 0.00 | ✗ |

**Observations:** NegMAS excels at structured utility maximisation (p1-01, p1-02)
but the current adapter does not yet handle unstructured quote parsing (p1-03)
or multi-step workflow execution requiring external tool calls (p1-04, p1-05).
Future work: extend the adapter with structured tool invocations for workflow
scenarios.

### Expected strengths
- Mathematically principled utility functions → economically consistent decisions
- Well-studied negotiation protocols → strong baseline for Pillar 1 sourcing

### Expected weaknesses
- No natural language reasoning → cannot handle unstructured scenario contexts
- Bilateral negotiation framing mismatches multi-supplier scenarios without adaptation
- Opponent modelling requires counterparty agents not present in BuyerBench

---

## E14 — GeniusWeb / Genius

**Category:** Negotiation  
**Ownership:** TU Delft Intelligent Interaction group  
**Licence:** Unspecified (academic platform)  
**Pricing:** Free (academic)  
**Maturity:** Research / education

### What it is
GeniusWeb is an open architecture for negotiation over the internet, providing
protocols (SAOP, MOPAC) and a Java reference implementation for building and
running negotiation agents.  Genius (the predecessor) is widely used in
negotiation research competitions.

### BuyerBench pillar relevance

| Pillar | Relevance | Notes |
|---|---|---|
| P1 — Capability | **Moderate** | Negotiation mechanics map to Negotiator functional role |
| P2 — Economic Rationality | **High** | Bid/utility tracking enables bias susceptibility measurement |
| P3 — Security | **Low** | Academic framework; no payment integration |

### Direct evaluation assessment
**Evaluable with significant adaptation.**  Java-native implementation creates
cross-language integration friction.  The GeniusWeb REST protocol could be
wrapped in a Python subprocess adapter similar to CLI agents, but the effort
is high relative to NegMAS's native Python interface.

**Recommended use:** Reference baseline for negotiation scenarios; use NegMAS
adapter for BuyerBench-integrated evaluation.

---

## E15 — Automated Negotiation League (ANAC)

**Category:** Negotiation (competition ecosystem)  
**Ownership:** Brown University-hosted ecosystem  
**Licence:** Unspecified (academic competition)  
**Pricing:** Free (academic)  
**Maturity:** Research

### What it is
ANAC (Automated Negotiating Agents Competition) and ANL (Automated Negotiation
League) are annual international competitions for negotiating agents.  The
ecosystem provides structured competition domains, evaluation harnesses, and
historical leaderboards dating back to 2010.

### BuyerBench pillar relevance

| Pillar | Relevance | Notes |
|---|---|---|
| P1 — Capability | **Moderate** | Competition agents are well-optimised for structured procurement-like domains |
| P2 — Economic Rationality | **Very High** | ANAC leaderboard enables comparison of economic performance across many agents |
| P3 — Security | **Low** | Competition environment; no payment integration |

### Direct evaluation assessment
**Evaluable as reference baseline.**  Published ANAC agents (available in
NegMAS/GeniusWeb ecosystems) can be run against BuyerBench Pillar 1 scenarios
using the NegMAS adapter infrastructure already in place.

**Limitation:** Objective hacking is a known issue in competition agents; ANAC
performance does not reliably predict real-world commercial procurement quality.

---

## E16 — AI Economist (Salesforce Foundation Framework)

**Category:** Economic simulation  
**Ownership:** Salesforce Research (academic / open-source)  
**Licence:** BSD-3-Clause  
**Pricing:** Free / open-source  
**Maturity:** Research

### What it is
The AI Economist framework is a modular Python simulation environment for
socio-economic policy research.  Originally developed to study AI-designed tax
policy, it supports multi-agent reinforcement learning in configurable economic
environments.  Agents can learn policies through RL interaction with the
simulated economy.

### BuyerBench pillar relevance

| Pillar | Relevance | Notes |
|---|---|---|
| P1 — Capability | **Low** | Policy learning focus; not a procurement execution agent |
| P2 — Economic Rationality | **Very High** | Ideal for studying how RL agents behave under systematic bias perturbations |
| P3 — Security | **None** | No payment integration |

### Direct evaluation assessment
**Valuable for Pillar 2 fundamental research**, particularly for studying
whether RL-trained buyer agents develop economically irrational preferences
under biased reward signals.  BSD-3-Clause licence is permissive.

**Limitation:** Strong modelling assumptions; findings may not transfer to
LLM-based buyer agents.  The "synthetic-to-real" gap is a known limitation
of this research line.
