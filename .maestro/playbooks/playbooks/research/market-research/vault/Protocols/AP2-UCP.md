---
type: research
title: "AP2/UCP — Agent Payments Protocol + Universal Commerce Protocol (Google)"
created: 2026-04-05
tags:
  - protocol
  - payment-protocol
  - google
  - authorization
  - agentic-commerce
  - mandates
  - ucp
  - pillar3
related:
  - '[[ACP]]'
  - '[[x402]]'
  - '[[Visa-Intelligent-Commerce]]'
  - '[[Skyfire]]'
  - '[[INDEX]]'
---

# AP2 / UCP (Google)

> Google's two-protocol stack for agentic commerce: AP2 secures agent-led payments via cryptographic mandates; UCP orchestrates the full commerce lifecycle from discovery to fulfillment

## Overview

Google's agentic commerce strategy is built on **two complementary open protocols**:

1. **AP2 (Agent Payments Protocol)** — the payment authorization layer. AP2 defines a standards-based model for AI agents to securely initiate and execute payments on behalf of users, using cryptographically signed "mandates" as tamper-proof records of user authorization.

2. **UCP (Universal Commerce Protocol)** — the full commerce orchestration layer. UCP handles the entire purchase lifecycle: product/service discovery, pricing and availability queries, merchant interaction, user intent and authorization checks, transaction confirmation, and fulfillment. UCP uses AP2 as its specialized payment subprotocol.

Together, AP2 + UCP form Google's complete answer to the question: *How should an AI agent discover, select, and pay for goods and services on behalf of a user, with full auditability, multi-party governance, and payment security?*

Both protocols were publicly launched at the **NRF Retail's Big Show (New York, January 11, 2026)**, representing a direct competitive response to OpenAI/Stripe's ACP specification (launched September 2025). The co-launch was designed to signal broad industry backing: UCP was developed alongside Shopify, Etsy, Wayfair, Target, and Walmart; AP2 launched with 60+ partner organizations including every major card network (Visa, Mastercard, American Express, JCB, UnionPay International) and major payment processors (Adyen, PayPal, Worldpay, Stripe).

> **BuyerBench relevance (Pillar 3):** AP2's mandate model is the most rigorous real-world specification for agent authorization semantics — the problem of proving that an AI agent is acting within the bounds of what a user actually authorized. Every Pillar 3 scenario involving spending limits, multi-party authorization chains, and audit trail requirements should be calibrated against AP2's mandate architecture. The Intent Mandate / Cart Mandate two-phase model directly maps to BuyerBench's pre-authorization and transaction-execution scenario stages.

> **BuyerBench relevance (Pillar 1):** UCP's product discovery and merchant interaction primitives define the state of the art for Pillar 1 supplier discovery scenarios. An agent operating in a UCP-enabled environment has structured access to product catalogs, pricing/availability APIs, and fulfillment confirmation flows — the full capability profile BuyerBench Pillar 1 source-to-award workflows test.

> **BuyerBench relevance (Pillar 2):** UCP's structured commerce flow (including intent capture and user confirmation checkpoints) provides an anchoring effect: agents operating within UCP's protocol primitives are less exposed to behavioral manipulation attacks (framing, decoy effects) because the protocol enforces structured decision capture rather than free-form LLM reasoning at checkout.

## Quick Facts

| Attribute | Value |
|-----------|-------|
| Protocol Names | Agent Payments Protocol (AP2) + Universal Commerce Protocol (UCP) |
| Developer | Google, with 60+ partners |
| Layer | AP2: Payment authorization; UCP: Full commerce orchestration |
| License | Open-source (public specification) |
| Launch Date | January 11, 2026 (NRF Retail's Big Show, New York) |
| AP2 Repository | github.com/google-agentic-commerce/AP2 |
| UCP Documentation | developers.google.com/merchant/ucp |
| AP2 Protocol Site | ap2-protocol.org |
| Integration Modes | REST API, MCP (Model Context Protocol), A2A (Agent2Agent protocol) |
| Payment Support | Traditional cards, bank transfers, alternative payments, stablecoins/crypto (x402 extension) |
| Partner Count | 60+ organizations |

## How AP2 Works — The Mandate Model

AP2's core innovation is the **Mandate** — a cryptographically signed, tamper-proof digital contract that serves as verifiable proof of a user's authorization for a specific transaction or set of transactions. Mandates are signed by **Verifiable Credentials (VCs)**, making them independently auditable by any party in the transaction chain.

### Two-Phase Mandate Architecture

| Mandate Type | Phase | Content |
|---|---|---|
| **Intent Mandate** | Pre-shopping | Captures the user's initial instruction to the agent — what to buy, within what constraints (budget, category, vendor restrictions) |
| **Cart Mandate** | Pre-checkout | Captures the agent's specific selection — product, price, merchant, quantity — after it has found a match. Requires user confirmation before payment execution |

This two-phase design creates a natural human oversight checkpoint: the user approves the *intent* (what to buy), the agent executes discovery and negotiation, and then the user (or an automated policy engine) approves the *specific cart* before money moves. Missed mandates or out-of-order execution are detectable protocol violations — not just policy failures.

### Payment Execution Flow

```
User → [Intent Mandate] → Agent (discovery)
Agent → [Cart Mandate] → User/Policy (approval)
Agent → [Payment Execution via AP2] → Payment Provider
Payment Provider → [Settlement] → Merchant
All steps: → Audit Trail (verifiable credential chain)
```

### Payment Method Support

AP2 is **payment-agnostic** by design:
- Traditional card networks (Visa, Mastercard, Amex, JCB, UnionPay International)
- Bank transfers and ACH
- Alternative payment methods (PayPal, Revolut, etc.)
- Stablecoins and cryptocurrency (via native **x402 extension** — Coinbase integration)

## How UCP Works — Commerce Orchestration

UCP is the full-stack commerce protocol layer that AP2 plugs into. UCP defines structured API primitives for every stage of the agent commerce lifecycle:

| Stage | UCP Primitive | Description |
|---|---|---|
| Discovery | Product/Service Catalog API | Structured access to merchant inventory, pricing, availability |
| Pricing | Pricing Query | Real-time pricing with promotions, volume discounts, personalization |
| Selection | Merchant Interaction | Structured negotiation and option selection flows |
| Authorization | Intent + Cart Capture | User intent and cart approval checkpoints (maps to AP2 mandates) |
| Payment | AP2 Subprotocol | Delegates to AP2 for payment execution |
| Confirmation | Transaction Confirmation | Order number, confirmation receipts |
| Fulfillment | Fulfillment Tracking | Shipment tracking, delivery status, returns |

### Protocol Integration Surface

UCP is explicitly designed to interoperate with the emerging agent protocol stack:

| Protocol | Role in UCP Context |
|---|---|
| **REST APIs** | Primary transport for merchant integrations |
| **MCP (Model Context Protocol)** | AI model-native integration; agents can discover UCP-enabled merchants via MCP servers |
| **A2A (Agent2Agent)** | Cross-agent delegation; UCP supports multi-agent commerce orchestration |
| **AP2** | Specialized payment subprotocol for all UCP payment transactions |
| **x402** | Crypto/micropayment extension for AP2 (Coinbase integration) |

## Key Partners (60+)

### Card Networks
- Visa
- Mastercard
- American Express
- JCB
- UnionPay International

### Payment Processors & Platforms
- Adyen
- Worldpay
- Stripe
- PayPal
- Revolut
- Coinbase

### Merchants & Retail
- Shopify
- Etsy
- Wayfair
- Target
- Walmart

### Technology & Enterprise
- Salesforce
- ServiceNow
- Intuit
- Ant International
- Mysten Labs

### Security & Risk
- Forter (fraud/risk management)

> *Note: Full partner list (60+) not exhaustively public; above are named partners from launch announcements.*

## Launch Context: NRF January 2026

The January 11, 2026 NRF launch was strategically timed to:
1. **Counter ACP momentum** — OpenAI/Stripe's ACP had launched in September 2025 and was the dominant narrative through end of 2025; Google's NRF announcement reset the competitive framing
2. **Signal retail-sector consensus** — By co-launching with Shopify, Walmart, Target, Etsy, and Wayfair, Google positioned UCP as the choice of *retailers*, while ACP was perceived as the choice of *payment infrastructure*
3. **Establish payment network universality** — Having all five major card networks (Visa, Mastercard, Amex, JCB, UnionPay) as AP2 partners from day one addressed the key weakness of ACP's Stripe-centric model

The timing coincided with the earliest signs of ChatGPT Instant Checkout underperformance (which culminated in the March 2026 rollback), making the NRF launch feel prescient in retrospect.

## Comparison to ACP

| Dimension | ACP (OpenAI + Stripe) | AP2 / UCP (Google) |
|-----------|----------------------|--------------------|
| **Protocol scope** | Checkout + payment (merchant integration layer) | AP2: payment authorization only; UCP: full commerce lifecycle |
| **Authorization model** | SharedPaymentToken (scoped, time-limited credentials) | Cryptographic mandates (Intent + Cart) with verifiable credentials |
| **Multi-party support** | Merchant-centric (bilateral: agent ↔ merchant) | Multi-stakeholder: orchestrator + agent + merchant + payment network + bank |
| **Audit trail** | Webhook-based post-hoc events | Built-in verifiable credential chain at every mandate step |
| **Partner ecosystem** | OpenAI + Stripe; merchant apps | 60+ partners incl. all major card networks, retailers, processors |
| **Enterprise compliance** | Inherits Stripe's PCI/compliance posture | Explicit mandate-level governance and multi-party audit design |
| **Crypto support** | Not native | Native via x402 extension |
| **Current momentum** | Narrowed scope post-Mar 2026 rollback | Growing; NRF launch + ACP rollback strengthened Google's position |
| **Deployment surface** | REST API or MCP | REST API, MCP, A2A |

**Key architectural difference:** ACP is primarily a merchant-facing checkout API — it defines how a merchant's backend accepts an agent-initiated purchase. AP2/UCP is primarily an **authorization governance framework** — it defines how a user's intent is captured, signed, delegated to an agent, and audited across a multi-party transaction chain. These address different problems, and a real-world enterprise deployment could legitimately run both simultaneously.

## BuyerBench Pillar Relevance

### Pillar 1 — Agent Intelligence and Operational Capability
UCP's structured commerce primitives (catalog discovery, pricing queries, merchant interaction APIs) define the expected tool interface for capable buyer agents. BuyerBench Pillar 1 scenarios should:
- Test whether agents correctly use UCP's discovery APIs before making selections
- Evaluate quote comparison quality against UCP-structured pricing responses
- Assess multi-step procurement workflow completion through the full UCP lifecycle

### Pillar 2 — Economic Decision Quality and Behavioral Robustness
The Intent Mandate → Cart Mandate two-phase flow creates a behavioral robustness testing dimension: does the agent's final cart selection match the user's original intent mandate? Drift between intent and cart is a measurable signal of susceptibility to anchoring, framing, or decoy manipulation during the discovery phase.

### Pillar 3 — Security, Compliance, and Market Readiness
AP2's mandate architecture is the most rigorous real-world model for:
- **Authorization chain integrity**: Can agents prove each step was authorized?
- **Multi-party audit compliance**: Does the agent generate a complete verifiable credential chain?
- **Spending constraint enforcement**: Are intent mandate constraints (budget, vendor restrictions) enforced at the cart mandate stage?
- **Revocation handling**: Does the agent correctly handle a revoked or expired mandate?

The AP2 mandate model should be the Pillar 3 reference for BuyerBench authorization scenarios, complementing ACP's payment API sequence as the Pillar 3 reference for payment execution scenarios.

## Related Entities

- [[ACP]] — Direct protocol-level competitor/complement at the checkout layer; ACP handles merchant payment integration while AP2/UCP handles authorization governance
- [[x402]] — Coinbase's HTTP-native micropayment protocol; AP2 has a native x402 extension for crypto payment support
- [[Visa-Intelligent-Commerce]] — Visa is a named AP2 partner; Visa Trusted Agent Protocol provides the card-network identity layer that AP2 leverages for card payments
- [[Mastercard-Agent-Pay]] — Mastercard is a named AP2 partner; similar tokenization-layer integration
- [[Skyfire]] — Skyfire's KYAPay identity model is architecturally compatible with AP2's verifiable credential mandate approach; Coinbase Ventures connects Skyfire to the x402/AP2 crypto rail

## Sources

1. [Announcing Agent Payments Protocol (AP2) — Google Cloud Blog](https://cloud.google.com/blog/products/ai-machine-learning/announcing-agents-to-payments-ap2-protocol) — Accessed 2026-04-05
2. [Under the Hood: Universal Commerce Protocol (UCP) — Google Developers Blog](https://developers.googleblog.com/under-the-hood-universal-commerce-protocol-ucp/) — Accessed 2026-04-05
3. [Google Universal Commerce Protocol (UCP) Guide — Google for Developers](https://developers.google.com/merchant/ucp) — Accessed 2026-04-05
4. [AP2 GitHub Repository — google-agentic-commerce/AP2](https://github.com/google-agentic-commerce/AP2) — Accessed 2026-04-05
5. [AP2 Protocol Documentation](https://ap2-protocol.org/) — Accessed 2026-04-05
6. [Google announces a new protocol to facilitate commerce using AI agents — TechCrunch](https://techcrunch.com/2026/01/11/google-announces-a-new-protocol-to-facilitate-commerce-using-ai-agents/) — Accessed 2026-04-05
7. [Google Debuts 'Universal' Protocol for Agentic Commerce — PYMNTS](https://www.pymnts.com/google/2026/google-debuts-universal-protocol-for-agentic-commerce/) — Accessed 2026-04-05
8. [Google Just Launched Its Agentic Commerce Protocol — Finovate](https://finovate.com/google-just-launched-its-agentic-commerce-protocol-the-https-for-agent-led-shopping/) — Accessed 2026-04-05
9. [Google's Universal Commerce Protocol (UCP) Powers Agentic Shopping — InfoQ](https://www.infoq.com/news/2026/01/google-ucp/) — Accessed 2026-04-05
10. [Google's New Tech Lets AI Agents Handle Checkout — Skift](https://skift.com/2026/01/11/google-ucp-ai-agentic-agents-checkout/) — Accessed 2026-04-05
11. [Agentic Payments Explained: ACP, AP2, and x402 — Orium](https://orium.com/blog/agentic-payments-acp-ap2-x402) — Accessed 2026-04-05
12. [Google's Agent Payments Protocol (AP2): A New Chapter in Agentic Commerce — Everest Group](https://www.everestgrp.com/googles-agent-payments-protocol-ap2-a-new-chapter-in-agentic-commerce-blog/) — Accessed 2026-04-05
13. [NRF Flash: Google Announces UCP, Checkout, Direct Offers — RetailGentic](https://www.retailgentic.com/p/flash-googlenrf-announces-universal) — Accessed 2026-04-05
14. [Google's Universal Commerce Protocol — Lengow Blog](https://blog.lengow.com/googles-universal-commerce-protocol-the-end-of-e-commerce-as-we-know-it/) — Accessed 2026-04-05

---
*Last updated: 2026-04-05*
