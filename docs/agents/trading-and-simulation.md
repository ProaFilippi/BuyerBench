---
type: reference
title: Trading and Simulation Agent Profiles
created: 2026-04-03
tags:
  - agent-profile
  - trading
  - simulation
  - open-source
related:
  - '[[INDEX]]'
  - '[[AGENT-LANDSCAPE-SUMMARY]]'
---

# Trading and Simulation Agent Profiles

Profiles for E08–E12: Freqtrade, Hummingbot, LEAN, FinRL, and ABIDES.
These are open-source and in principle evaluable; however, their domain focus
(financial markets, crypto, equities) differs from procurement.  Pillar 1
decision-making patterns (evaluate → select → execute) are directly relevant,
as is Pillar 2 (economic rationality under constraints).  Pillar 3 security
scenarios are partially applicable for agents that handle real financial
credentials.

---

## E08 — Freqtrade

**Category:** Trading & investment  
**Ownership:** Community project (freqtrade GitHub org)  
**Licence:** GPL-3.0  
**Pricing:** Free / open-source  
**Maturity:** Production (OSS)

### What it is
Freqtrade is an open-source cryptocurrency trading bot with full backtesting,
live trading, and strategy optimisation capabilities.  Strategies are Python
functions that define buy/sell signals.  The bot integrates with major crypto
exchanges via CCXT and can be controlled via Telegram or web UI.

### BuyerBench pillar relevance

| Pillar | Relevance | Notes |
|---|---|---|
| P1 — Capability | **Moderate** | Strategy execution maps to Evaluator + Executor roles; but optimisation objective is financial gain, not procurement cost |
| P2 — Economic Rationality | **High** | Freqtrade strategies can be tested against framing/anchoring perturbations via modified signal inputs |
| P3 — Security | **Partial** | Exchange API key handling is a direct P3 analogue (credential handling, least-privilege scoping) |

### Direct evaluation assessment
**Evaluable with adaptation.**  Freqtrade's Python API allows programmatic
strategy backtesting.  A BuyerBench adapter could:
1. Map supplier selection to asset selection using the Freqtrade strategy interface
2. Test economic rationality by modifying input signals (anchoring variants)
3. Evaluate API key scoping patterns against Pillar 3 credential requirements

**Blocker:** Domain mismatch (crypto vs. procurement) limits direct scenario
applicability without translation layer.

### Expected strengths
- Mature backtesting framework → reliable economic decision quality measurement
- Configurable risk controls → measurable policy adherence

### Expected weaknesses
- GPL-3.0 licence creates downstream attribution requirements
- Exchange API abuse risk if run against live environments
- No natural language interface → scenarios must be translated to signal functions

---

## E09 — Hummingbot

**Category:** Trading & investment  
**Ownership:** Hummingbot Foundation  
**Licence:** Apache-2.0  
**Pricing:** Free / open-source  
**Maturity:** Production (OSS)

### What it is
Hummingbot is a modular open-source framework for building and running
automated trading strategies on centralised (CEX) and decentralised (DEX)
exchanges.  It supports market-making, arbitrage, and directional strategies
via a Python plugin architecture.

### BuyerBench pillar relevance

| Pillar | Relevance | Notes |
|---|---|---|
| P1 — Capability | **Moderate** | Buy/sell execution mechanics map to Executor role |
| P2 — Economic Rationality | **High** | Market-making strategy parameters expose anchoring and loss-aversion susceptibility |
| P3 — Security | **Moderate** | Key custody and least-privilege API key management directly testable |

### Direct evaluation assessment
**Evaluable with adaptation.**  Apache-2.0 licence is permissive; Python API
allows programmatic strategy configuration.  Mapping procurement scenarios to
Hummingbot strategies requires translating supplier selection to bid/ask spread
decisions — non-trivial but tractable.

---

## E10 — LEAN Algorithmic Trading Engine (QuantConnect)

**Category:** Trading & investment  
**Ownership:** QuantConnect  
**Licence:** Apache-2.0  
**Pricing:** Free / open-source engine; QuantConnect cloud platform priced separately  
**Maturity:** Production (OSS + platform)

### What it is
LEAN is a production-grade event-driven algorithmic trading engine written in
C# with Python algorithm support.  It powers the QuantConnect cloud research
platform and supports backtesting and live trading across equities, futures,
options, crypto, and forex.

### BuyerBench pillar relevance

| Pillar | Relevance | Notes |
|---|---|---|
| P1 — Capability | **Moderate** | Algorithm execution framework maps to Evaluator + Executor |
| P2 — Economic Rationality | **High** | LEAN's research environment allows controlled scenario injection for bias testing |
| P3 — Security | **Low-Moderate** | Production deployments handle brokerage credentials; test mode uses paper trading |

### Direct evaluation assessment
**Evaluable but complex.**  C#-native core with Python binding; integration
into BuyerBench's Python ecosystem requires cross-language subprocess calling
or using the Python algorithm interface.  High-value for Pillar 2 economic
rationality testing due to LEAN's precise backtesting controls.

---

## E11 — FinRL

**Category:** Trading & investment (RL-based)  
**Ownership:** AI4Finance Foundation  
**Licence:** MIT  
**Pricing:** Free / open-source  
**Maturity:** Research-to-production tooling

### What it is
FinRL is an open-source deep reinforcement learning framework for automated
stock trading.  It provides standard financial market environments, data
pipelines, and RL agent implementations (DQN, PPO, A2C, SAC) for research
and education.

### BuyerBench pillar relevance

| Pillar | Relevance | Notes |
|---|---|---|
| P1 — Capability | **Low-Moderate** | RL policy execution maps loosely to Evaluator role |
| P2 — Economic Rationality | **Very High** | RL agents trained under biased reward signals exhibit systematic decision failures; directly measurable |
| P3 — Security | **Low** | Research-focused; no payment credential handling |

### Direct evaluation assessment
**Most relevant for Pillar 2 research.**  FinRL's RL training loop can be
instrumented to measure susceptibility to reward-signal manipulation (analogous
to behavioural bias injection).  MIT licence is highly permissive.

**Limitation:** Significant sim-to-real gap; patterns measured in FinRL
environments may not transfer to procurement agent behaviour.

---

## E12 — ABIDES

**Category:** Trading & investment simulation  
**Ownership:** Georgia Tech (academic); open-source community  
**Licence:** BSD-3-Clause  
**Pricing:** Free / open-source  
**Maturity:** Research (mature in academia)

### What it is
ABIDES (Agent-Based Interactive Discrete Event Simulation) is a highly
realistic market microstructure simulator designed for AI agent research.
It uses a message-based discrete event architecture modelled on real exchange
protocols (NASDAQ ITCH/OUCH) and supports latency-aware multi-agent market
simulations.

### BuyerBench pillar relevance

| Pillar | Relevance | Notes |
|---|---|---|
| P1 — Capability | **Low** | Simulation focus; not a buyer-agent execution framework |
| P2 — Economic Rationality | **High** | Ideal environment for testing agent behaviour under market manipulation, scarcity signals, and adversarial pricing |
| P3 — Security | **Low** | No payment flow implementation |

### Direct evaluation assessment
**Valuable for Pillar 2 adversarial market testing.**  ABIDES's controlled
market environment allows injecting anchor prices, artificial scarcity signals,
and decoy assets — directly corresponding to BuyerBench Pillar 2 scenarios.
BSD-3-Clause licence is permissive.

**Limitation:** Purely a simulator; agents must be separately implemented to
interface with ABIDES's exchange protocol.
