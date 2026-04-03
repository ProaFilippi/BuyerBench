---
type: reference
title: Agent Profiles Index
created: 2026-04-03
tags:
  - index
  - agents
related:
  - '[[AGENT-LANDSCAPE-SUMMARY]]'
---

# Agent Profiles Index

This index links all agent profile documents in `docs/agents/`.
See `[[AGENT-LANDSCAPE-SUMMARY]]` for the full cross-agent comparison table.

## Profile Documents

| File | Agents covered | Category |
|---|---|---|
| [[enterprise-procurement]] | E04 SAP Joule/Ariba, E05 Coupa, E06 Ivalua IVA, E07 Zip | Enterprise SaaS |
| [[consumer-shopping]] | E01 Amazon Rufus, E02 Klarna, E03 Google Agentic Checkout | Consumer-facing |
| [[trading-and-simulation]] | E08 Freqtrade, E09 Hummingbot, E10 LEAN, E11 FinRL, E12 ABIDES | Open-source trading |
| [[negotiation-and-economics]] | E13 NegMAS, E14 GeniusWeb/Genius, E15 ANAC, E16 AI Economist | Academic / OSS |
| [[payment-protocols]] | E17 AP2, E18 UCP, E19 ACP, E20 Stripe Agent Toolkit, E21 Visa VIC, E22 Visa TAP, E23 Mastercard Agent Pay | Payment protocols |

## Evaluation Stubs

| File | Covers |
|---|---|
| [[evaluation-stubs/enterprise-procurement-evaluation-plan]] | SAP, Coupa, Ivalua, Zip — evaluation methodology when access obtained |
| [[evaluation-stubs/consumer-agents-evaluation-plan]] | Rufus, Klarna, Google — Playwright browser automation methodology |

## BuyerBench Evaluation Status

| Agent | Status | Adapter |
|---|---|---|
| NegMAS (E13) | **Evaluated** | `agents/negmas_agent.py` |
| Stripe Agent Toolkit (E20) | **Evaluated** | `agents/stripe_toolkit_agent.py` |
| SAP Joule/Ariba (E04) | Stub Designed | See enterprise-procurement-evaluation-plan |
| Coupa (E05) | Stub Designed | See enterprise-procurement-evaluation-plan |
| Ivalua IVA (E06) | Stub Designed | See enterprise-procurement-evaluation-plan |
| Zip (E07) | Stub Designed | See enterprise-procurement-evaluation-plan |
| Amazon Rufus (E01) | Stub Designed | See consumer-agents-evaluation-plan |
| Klarna (E02) | Stub Designed | See consumer-agents-evaluation-plan |
| Google Agentic Checkout (E03) | Stub Designed | See consumer-agents-evaluation-plan |
| Freqtrade (E08) | Not Yet Evaluated | Domain adaptation required |
| Hummingbot (E09) | Not Yet Evaluated | Domain adaptation required |
| LEAN (E10) | Not Yet Evaluated | Domain adaptation required |
| FinRL (E11) | Not Yet Evaluated | P2 research value; future work |
| ABIDES (E12) | Not Yet Evaluated | P2 simulation; future work |
| GeniusWeb/Genius (E14) | Not Yet Evaluated | Java integration required |
| ANAC (E15) | Not Yet Evaluated | Via NegMAS adapter (future) |
| AI Economist (E16) | Not Yet Evaluated | P2 research; future work |
| AP2 (E17) | Not Yet Evaluated | Protocol adapter future work |
| UCP (E18) | Not Yet Evaluated | Protocol adapter future work |
| ACP (E19) | Not Yet Evaluated | Partial coverage via Stripe adapter |
| Visa VIC (E21) | Not Applicable | Access-gated; no public sandbox |
| Visa TAP (E22) | Not Applicable | Access-gated |
| Mastercard Agent Pay (E23) | Not Applicable | Access-gated |
