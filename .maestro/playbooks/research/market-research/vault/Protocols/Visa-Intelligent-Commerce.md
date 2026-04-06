---
type: protocol
title: "Visa Intelligent Commerce + Trusted Agent Protocol"
created: 2026-04-05
tags:
  - payment-protocol
  - visa
  - tokenization
  - identity
  - KYA
  - agentic-commerce
  - pillar3
related:
  - '[[Mastercard-Agent-Pay]]'
  - '[[ACP]]'
  - '[[Skyfire]]'
  - '[[AP2-UCP]]'
  - '[[INDEX]]'
---

# Visa Intelligent Commerce + Trusted Agent Protocol

> Visa's two-layer program for agentic commerce: an open developer API platform (Intelligent Commerce, April 2025) paired with a cryptographic agent identity framework (Trusted Agent Protocol, October 2025) — backed by Visa's existing tens of billions of payment tokens

## Overview

**Visa Intelligent Commerce (VIC)** is Visa's program for opening its payment network to AI agent developers. Launched on April 30, 2025 at the Visa Global Product Drop, VIC provides APIs and tools that embed Visa's core payment capabilities — tokenized credentials, identity verification, spending controls, and authorization — directly into AI agent architectures. It is grounded in Visa's existing 30-year AI investment and positions Visa as infrastructure for the agentic commerce layer rather than a specific protocol standard.

Six months later, on **October 14, 2025**, Visa extended VIC with the **Trusted Agent Protocol (TAP)**: an open, ecosystem-led framework that addresses the specific trust-and-identity gap in agent-initiated transactions. TAP gives merchants a structured mechanism to distinguish legitimate AI agents acting for real consumers from malicious bots, and provides agents a standardized way to present their spending authority and behavioral parameters at checkout.

By December 2025, Visa announced that hundreds of secure agent-initiated transactions had been successfully completed across pilot partners, with Visa publicly predicting that millions of consumers will use AI agents to complete purchases by the **holiday 2026 season**.

> **BuyerBench relevance (Pillar 3):** VIC + TAP define the card-network-level compliance layer for agentic payments. TAP's three-element structure (Agent Intent + Consumer Recognition + Payment Information) maps directly to BuyerBench Pillar 3 scenarios for authentication/authorization enforcement and secure transaction sequencing. TAP's cryptographic signature model (HTTP Message Signatures) represents a production standard against which BuyerBench can calibrate "correct" agent identity assertion behavior.

> **BuyerBench relevance (Pillar 1):** Visa's Intelligent Commerce partner ecosystem (Skyfire, Nekuda, Ramp, PayOS) represents the real-world agent-enabler landscape BuyerBench Pillar 1 scenarios should model — specifically, how AI buyer agents interface with existing payment infrastructure during supplier discovery and purchase execution.

## Quick Facts

| Attribute | Value |
|-----------|-------|
| Program Name | Visa Intelligent Commerce (VIC) |
| Trust Framework | Trusted Agent Protocol (TAP) |
| Owner | Visa Inc. |
| VIC Launch | April 30, 2025 (Global Product Drop) |
| TAP Launch | October 14, 2025 |
| Token Infrastructure | Tens of billions of existing Visa tokens |
| Partner Count | 100+ globally; 30+ active in VIC sandbox; 20+ agents/agent-enablers directly integrating |
| Core Technical Standard | HTTP Message Signature + Web Auth alignment |
| Developer Portal | developer.visa.com/capabilities/trusted-agent-protocol |

## KYA (Know Your Agent) Identity Layer

**Know Your Agent (KYA)** is Visa's conceptual framework for establishing verified identity in agentic commerce — the AI-agent analogue to KYC (Know Your Customer) in traditional finance.

KYA centers on:

1. **Cryptographic agent identity** — an agent must have a verifiable, machine-readable identity credential that is cryptographically signed and linkable to an authenticated human or enterprise principal
2. **Root of trust** — the KYA chain establishes a trust anchor that ties together:
   - The authenticated consumer or business (principal)
   - The AI agent acting on their behalf (delegate)
   - The payment credential the agent is authorized to use (scope)
   - The boundaries of the agent's authority (spend limits, merchant categories, timing)
3. **Trust delegation, not credential exposure** — the agent carries delegated authorization, not raw card data; the underlying payment credential is never exposed to the agent or merchant

KYA is implemented technically through TAP (see next section) but represents a broader policy principle: any agentic payment network must be able to answer "who authorized this agent, what are they authorized to do, and can I verify that claim cryptographically?"

> **BuyerBench relevance:** KYA maps directly to BuyerBench Pillar 3's authentication and authorization enforcement scenarios. A compliant agent must correctly assert and scope its own authority — failing to do so (e.g., claiming broader permissions than granted, or presenting credentials without a traceable principal) should be detectable as a policy violation.

## Launch Timeline

### Phase 1 — Visa Intelligent Commerce (April 30, 2025)

- Announced at Visa Global Product Drop as a developer-facing initiative
- Released APIs for embedding payment functions into AI agents: identity verification, spending controls, tokenized credential management, authorization flows
- Launch partners: Anthropic, IBM, Microsoft, Mistral AI, OpenAI, Perplexity, Samsung, Stripe
- Early pilot agent-enablers: Skyfire, Nekuda, PayOS, Ramp (closed beta, US)
- Key demo: Skyfire-powered Consumer Reports product recommendation agent purchasing Bose headphones via browser automation, using VIC + KYAPay

### Phase 2 — Trusted Agent Protocol (October 14, 2025)

- Introduced TAP alongside 10+ initial ecosystem partners
- TAP launched as an **open framework** built on existing web infrastructure (HTTP Message Signatures, Web Auth) — not a proprietary Visa-only standard
- Designed to minimize UX disruption while adding agent identity verification at checkout
- Framing: "making agentic commerce feel familiar and safe" — extending Visa's existing consumer trust (50+ years) to agent-driven transactions

### Phase 3 — Pilot Validation (December 2025)

- Visa announced hundreds of secure agent-initiated transactions completed successfully
- Partners across consumer and B2B dimensions; Skyfire's KYAPay protocol demonstrated integration with VIC
- Visa stated publicly: "millions of consumers will use AI agents to complete purchases by holiday 2026"

### Phase 4 — AWS Integration (December 2025)

- Visa and AWS launched VIC integration with Amazon Bedrock AgentCore
- Enables developers building on AWS to incorporate Visa's agentic payment capabilities directly into Bedrock-hosted agents

## Trusted Agent Protocol — Technical Architecture

### Three-Element Structure

TAP defines a structured payload that an AI agent presents to a merchant at checkout, comprising three elements:

| Element | Description | Purpose |
|---------|-------------|---------|
| **Agent Intent** | Declaration that the agent is trusted and acting with purchase intent | Distinguishes legitimate shopping agents from web scrapers or malicious bots |
| **Consumer Recognition** | Data elements indicating whether the consumer has an existing merchant account | Enables personalized checkout, loyalty integration, and risk scoring |
| **Payment Information** | Tokenized payment credential, billing/shipping address | Carries everything the merchant needs to complete the transaction without exposing raw card data |

### Technical Foundation

- Built on **HTTP Message Signature** standard (RFC 9421 / IETF draft)
- Aligned with **Web Authentication (WebAuthn)** for credential binding
- Uses Visa's existing **tokenization infrastructure** — merchants receive a token (one-time card token, digital card, or card data hash) rather than a live PAN
- The agent's cryptographic signature can carry parameters: spend limits, merchant category restrictions, timing windows, behavioral patterns

### Trust Verification Flow

```
Consumer → [Authorizes agent, sets spending parameters]
Agent → [Receives delegated credential + TAP payload authority]
Agent → [Signs TAP payload with cryptographic identity]
Agent → Merchant: POST checkout with TAP-signed headers
Merchant → [Verifies HTTP Message Signature against agent's public key]
Merchant → [Validates Agent Intent + Consumer Recognition + Payment Info]
Merchant → [Processes tokenized payment via Visa network]
Visa → [Authorization, risk scoring, fraud signals]
```

### Fraud Differentiation

TAP's primary merchant-facing value proposition is distinguishing **legitimate AI agents** (operating transparently, with cryptographically verifiable human authorization) from **malicious bots** (operating without principal authorization, attempting to abuse checkout flows). This addresses a specific merchant fear: that AI agents create a new attack surface for fraud and unauthorized transactions.

## Partner Ecosystem

### AI Platform Partners (VIC Launch, April 2025)
- **Anthropic** — Claude model integration
- **Microsoft** — Copilot + Azure AI agents
- **OpenAI** — ChatGPT agent framework
- **Mistral AI** — European AI model provider
- **Perplexity** — Shopping assistant agent
- **Samsung** — Device-level AI agent integration
- **Stripe** — Payment processing backbone (also ACP co-developer)
- **IBM** — Enterprise AI agent deployments

### Agent-Enabler Pilots (US Closed Beta)
- **Skyfire** — Consumer-facing agentic purchase via KYAPay + VIC; demonstrated Bose headphone purchase via Consumer Reports agent
- **Nekuda** — Agentic commerce infrastructure
- **PayOS** — Agent-native payment orchestration
- **Ramp** — B2B spend management; agentic corporate purchasing

### TAP Ecosystem Partners (October 2025+)
- **Nuvei** — Payment processing, active TAP supporter
- **AWS / Amazon Bedrock** — AgentCore integration (December 2025)
- 10+ additional ecosystem partners at TAP launch (full list not publicly disclosed)

### Cross-Protocol Positioning
- VIC is compatible with and complementary to AP2/UCP (Google), ACP (OpenAI+Stripe), and x402 (Coinbase) — Visa's rails can serve as the underlying payment execution layer beneath any of these protocol stacks

## Token Model

Visa's tokenization infrastructure is the backbone of VIC's security posture:

| Token Type | Use Case |
|------------|----------|
| **One-time card token** | Single-transaction authorization, highest security |
| **Digital card (network token)** | Persistent agent-held credential, scoped to agent identity |
| **Card data hash** | Merchant-side recognition without card number exposure |

Key properties:
- Tokens are **scoped**: bound to specific spend limits, merchant categories, time windows
- Tokens are **revocable**: the consumer can revoke agent authorization without canceling the underlying payment method
- Tokens inherit Visa's existing **network-level fraud detection** (Visa Advanced Authorization, real-time risk scoring)

Visa already operates **tens of billions of tokens** from its existing digital wallet and card-on-file infrastructure — VIC/TAP extend this infrastructure to agent use cases rather than building a new token ecosystem from scratch.

## Comparison to Mastercard Agent Pay

| Dimension | Visa Intelligent Commerce + TAP | Mastercard Agent Pay |
|-----------|--------------------------------|----------------------|
| **Announcement date** | April 2025 (VIC) + Oct 2025 (TAP) | October 2025 (same day as TAP) |
| **Technical foundation** | HTTP Message Signatures + WebAuthn | Tokenization + agent identity verification |
| **Identity model** | KYA (Know Your Agent) — cryptographic root of trust | Agent identity registration + credential binding |
| **Partner depth** | 100+ partners globally; major AI platforms at launch | Major card issuers, fintechs, enterprise partners |
| **Open standard** | TAP is open / ecosystem-led | Agent Pay uses Mastercard's Multi-Token Network |
| **Token infrastructure** | Extends existing Visa token ecosystem (tens of billions of tokens) | Mastercard Multi-Token Network (new layer) |
| **Key differentiator** | "Familiar and safe" — merchant UX continuity | Identity-first, financial-services compliance emphasis |
| **AWS integration** | Yes (Bedrock AgentCore, Dec 2025) | Not prominently announced |

Both networks announced agent payment frameworks on the same day in October 2025, signaling coordinated network-level positioning. Neither is a direct competitor — together they establish that all major card networks have an agentic payment identity story, reducing merchant hesitation about agent-initiated payments.

## BuyerBench Pillar Relevance

### Pillar 1 — Agent Intelligence and Operational Capability
- VIC's partner ecosystem (Skyfire, Nekuda, Ramp, PayOS) represents the real commercial landscape for AI buyer agents; Pillar 1 scenarios should test agents operating within VIC-compliant checkout flows
- TAP's Consumer Recognition element creates a scenario opportunity: does an agent correctly assert or look up a buyer's existing merchant account to trigger loyalty/discount integration?

### Pillar 2 — Economic Decision Quality and Behavioral Robustness
- Spend limits and merchant category restrictions in TAP create scope constraints that interact with economic optimization — an agent operating near a spend limit faces a different decision context than an unconstrained agent
- Scenario type: does an agent correctly identify when a purchase would exceed its TAP-scoped authorization, and does it escalate vs. proceed?

### Pillar 3 — Security, Compliance, and Market Readiness
- **TAP is a Pillar 3 reference standard**: BuyerBench's authentication/authorization scenarios should be calibrated against TAP's three-element structure
- **KYA compliance testing**: does the agent correctly establish and present its identity chain (principal → agent → credential → scope)?
- **Tokenization correctness**: does the agent present a token rather than raw card data? Does it respect token scope constraints?
- **Bot/agent distinction**: does the agent correctly signal legitimate intent in a way that passes TAP's merchant-side verification? (A failing agent may be blocked as a malicious bot)
- **Revocation handling**: what happens when a consumer revokes the agent's authorization mid-transaction?

## Related Entities
- [[Mastercard-Agent-Pay]] — Launched same day as TAP; card network co-competitor establishing parallel agentic payment infrastructure
- [[ACP]] — OpenAI + Stripe checkout protocol; Stripe is a VIC partner, making Stripe-processed ACP transactions potentially VIC-compatible
- [[Skyfire]] — KYAPay protocol demonstrated live integration with VIC; Skyfire is a key early VIC agent-enabler pilot partner
- [[AP2-UCP]] — Google's authorization and trust protocol; complementary to VIC (AP2 handles multi-party spending mandates; VIC handles Visa-network-level identity and tokenization)

## Sources

1. [Find and Buy with AI: Visa Unveils New Era of Commerce — Visa Newsroom](https://usa.visa.com/about-visa/newsroom/press-releases.releaseId.21361.html) — Accessed 2026-04-05
2. [Visa Introduces Trusted Agent Protocol — Visa Investor Relations](https://investor.visa.com/news/news-details/2025/Visa-Introduces-Trusted-Agent-Protocol-An-Ecosystem-Led-Framework-for-AI-Commerce/default.aspx) — Accessed 2026-04-05
3. [Visa and Partners Complete Secure AI Transactions — Visa Newsroom](https://usa.visa.com/about-visa/newsroom/press-releases.releaseId.21961.html) — Accessed 2026-04-05
4. [Trusted Agent Protocol — Visa Developer Portal](https://developer.visa.com/capabilities/trusted-agent-protocol/overview) — Accessed 2026-04-05
5. [Skyfire Demonstrates Secure Agentic Commerce Purchase Using KYAPay + VIC — BusinessWire](https://www.businesswire.com/news/home/20251218520399/en/Skyfire-Demonstrates-Secure-Agentic-Commerce-Purchase-Using-the-KYAPay-Protocol-and-Visa-Intelligent-Commerce) — Accessed 2026-04-05
6. [Visa Maps a Path to Agentic Commerce That Feels Familiar — and Safe — PYMNTS](https://www.pymnts.com/news/artificial-intelligence/2025/visa-maps-a-path-to-agentic-commerce-that-feels-familiar-and-safe/) — Accessed 2026-04-05
7. [Introducing Visa Intelligent Commerce on AWS — AWS Machine Learning Blog](https://aws.amazon.com/blogs/machine-learning/introducing-visa-intelligent-commerce-on-aws-enabling-agentic-commerce-with-amazon-bedrock-agentcore/) — Accessed 2026-04-05
8. [Deep Dive: The Role of Visa's Trusted Agent Protocol — Medium / Sam Boboev](https://samboboev.medium.com/deep-dive-the-role-of-visas-trusted-agent-protocol-in-agentic-commerce-2a78e61efce7) — Accessed 2026-04-05
9. [Visa, Mastercard offer support for AI agents — Digital Commerce 360](https://www.digitalcommerce360.com/2025/05/06/visa-mastercard-ai-agentic-commerce/) — Accessed 2026-04-05
10. [Visa Gives AI Shopping Agents 'Intelligent Commerce' Superpowers — PYMNTS](https://www.pymnts.com/visa/2025/visa-powers-ai-shopping-agents-with-intelligent-commerce-payment-rails/) — Accessed 2026-04-05
11. [Nuvei Supports Visa Trusted Agent Protocol — Nuvei](https://www.nuvei.com/posts/nuvei-supports-visa-trusted-agent-protocol-to-advance-agentic-commerce) — Accessed 2026-04-05

---
*Last updated: 2026-04-05*
