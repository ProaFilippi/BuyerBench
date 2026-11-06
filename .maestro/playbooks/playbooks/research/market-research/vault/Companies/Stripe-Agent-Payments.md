---
type: company
title: "Stripe Agent Payments"
created: 2026-04-06
tags:
  - stripe
  - payment-infrastructure
  - pricing
  - fraud-detection
  - pillar-3
  - acp
  - shared-payment-tokens
  - radar
  - connect
  - micropayments
related:
  - '[[ACP]]'
  - '[[x402]]'
  - '[[Skyfire]]'
  - '[[OpenAI-Agent-Platform]]'
  - '[[Coinbase-Agent-Payments]]'
  - '[[INDEX]]'
---

# Stripe Agent Payments

> Stripe is both the **payment rail** and the **protocol co-author** for agentic commerce — it co-owns the Agentic Commerce Protocol (ACP) with OpenAI, introduced Shared Payment Tokens (SPT) as the core agent-payment primitive, built the Agentic Commerce Suite for merchants, and already processes payments for OpenAI's ChatGPT Instant Checkout. No other company simultaneously controls the transaction infrastructure *and* the open standard governing how AI agents initiate purchases.

## Overview

Founded in 2010 by Patrick and John Collison, Stripe built the dominant developer-first payment processing platform — $1.4T in payment volume processed in 2024, serving 100+ countries and millions of businesses from startups to Fortune 500. In 2025–2026, Stripe repositioned itself as the **economic infrastructure for the AI era**, making four strategic moves:

1. **ACP Co-authorship** (Sep 2025): Co-developed the Agentic Commerce Protocol with OpenAI — an open standard for agent-initiated purchases, governed jointly by Stripe and OpenAI on GitHub.
2. **Agentic Commerce Suite** (2025–2026): A full merchant-facing product stack enabling businesses to sell via AI agents — product discovery tools, Shared Payment Tokens (SPT), governance/spending controls, and checkout optimization.
3. **Payments Foundation Model** (announced May 2025): A proprietary AI model trained on Stripe's global transaction dataset, powering fraud detection, authorization rate optimization, and dispute resolution — announced alongside a "deeper partnership" with Nvidia for GPU infrastructure.
4. **x402 Integration** (Feb 2026): Integrated Coinbase's x402 protocol, enabling AI agents to make instant USDC micropayments on the Base chain via Stripe infrastructure — bridging fiat and crypto payment rails for the agent economy.

Stripe's long-standing relationship with OpenAI predates ACP: OpenAI has used Stripe Billing and Stripe Checkout for ChatGPT Plus subscriptions since 2023, with Stripe Radar detecting fraud and Stripe Link enabling fast checkout. ACP and Instant Checkout deepen this into a structural partnership.

> **BuyerBench relevance (Pillar 3):** Stripe is the canonical reference implementation for Pillar 3 scenarios. SPTs, governance controls (spending limits, allowed merchant lists, category restrictions), Radar fraud screening, and ACP's authentication model directly map to the payment security, fraud detection, and compliance scenarios BuyerBench tests. Any agent that initiates purchases via ACP is operating within Stripe's authorization model.

## Quick Facts

| Attribute | Value |
|-----------|-------|
| Founded | 2010 |
| Founders | Patrick Collison, John Collison |
| HQ | San Francisco, CA + Dublin, Ireland |
| Payment Volume (2024) | ~$1.4T |
| AI Partnership | OpenAI (ACP co-author since Sep 2025) |
| Other AI Partners | Anthropic, Microsoft Copilot (ACP expansion roadmap) |
| Key Protocol | Agentic Commerce Protocol (ACP) — open standard on GitHub |
| Key Payment Primitive | Shared Payment Tokens (SPT) |
| Fraud Tool | Stripe Radar (AI-powered; -38% fraud on average) |
| Crypto Integration | x402 / Coinbase Base (Feb 2026) |
| Micropayment Protocol | Machine Payments Protocol (MPP) with Tempo (Mar 2026) |
| Klarna Integration | Flexible BNPL payments for AI agent transactions (2026 roadmap) |
| PwC Partnership | Enterprise ACP deployment collaboration (2026) |

## Agent Payment Products

### Agentic Commerce Suite

Stripe's umbrella product for the agent economy, launched 2025–2026. Enables merchants to become "agent-ready" via a single integration:

- **Product Discoverability Layer**: Structured product catalogs that AI agents can query — enabling agents to discover and compare merchant inventory before initiating checkout.
- **Shared Payment Tokens (SPT)**: The core agent-payment primitive. An SPT is a tokenized representation of a buyer's approved payment method — agents use SPTs to initiate purchases without ever handling raw card credentials. SPTs carry embedded governance rules (spending limits, merchant allowlists, category restrictions) set by the buyer or their organization.
- **Governance & Spending Controls**: Real-time policy enforcement at the payment layer — businesses can apply spending limits, allowed merchant category codes (MCCs), geographic restrictions, and time-bound authorization windows. Equivalent to procurement card (P-card) controls, but for AI agents.
- **Checkout Optimization**: Stripe's Optimized Checkout Suite applied to agent-initiated transactions — businesses see an average +11.9% revenue lift.

### Agentic Commerce Protocol (ACP)

Co-authored with OpenAI and published as an open standard on GitHub (`agentic-commerce-protocol/agentic-commerce-protocol`). ACP defines:

- The **interaction model** between buyers, their AI agents, and merchant systems
- How agents **authenticate** on behalf of buyers (delegated authority model)
- How **payment consent** is obtained and encoded (SPT as the payment credential)
- How **transaction completion** is confirmed and recorded

ACP launched in September 2025 with OpenAI's ChatGPT Instant Checkout as the first implementation. Initial merchant coverage: Etsy (US), plus Shopify merchants (Glossier, Vuori, Spanx, SKIMS, and ~1M+ Shopify catalog merchants rolling out). See [[OpenAI-Agent-Platform]] for ACP rollback history.

### Stripe Radar (Fraud Detection)

Stripe's AI-powered fraud prevention system, now extended to agentic transactions:

- **Foundation Model Integration**: Stripe's Payments Foundation Model (announced May 2025, trained on $1.4T+ in transaction data) powers Radar — one of the largest fraud detection datasets in the world.
- **Agent-Specific Signals**: Radar now evaluates agent-initiated transaction patterns distinct from human checkout behavior — different velocity patterns, session characteristics, and authorization flows.
- **Performance**: Businesses using Radar see **38% less fraud** on average vs. not using Radar.
- **Chargeback Protection**: Stripe offers Chargeback Protection add-on ($0.04/transaction extra) — Stripe absorbs the dispute cost if a fraudulent charge passes Radar's screening.
- **3D Secure Integration**: Radar can trigger EMV 3DS authentication flows for high-risk agent transactions, delegating risk decisioning to the issuing bank.

### Stripe Connect (Platform Payments)

Stripe Connect enables platforms and marketplaces to route payments to connected merchants — the infrastructure underlying Amazon Business supplier payments, B2B procurement platforms, and multi-vendor agent transactions.

- **Standard**: No platform-specific monthly fee; connected accounts handle their own compliance.
- **Express**: $2/month per active connected account + 0.25% + $0.25 per payout sent.
- **Custom**: White-labeled; fully custom pricing (enterprise contract required).

### Machine Payments Protocol (MPP)

Co-launched with Tempo on March 18, 2026. MPP enables:
- **Pre-authorized spending budgets**: Agents declare a spending limit before beginning a multi-step transaction sequence.
- **Streamed micropayments**: Continuous, granular payment streams in both stablecoins (USDC via Base) and fiat — suited for per-API-call or per-task agent billing.
- Designed for agent-to-agent (A2A) transactions where no human is in the loop at payment time.

## Pricing

### Standard Processing Fees

| Transaction Type | Fee |
|-----------------|-----|
| US card (standard) | 2.9% + $0.30 per successful charge |
| UK card | 1.5% + £0.20 per successful charge |
| EU card | 1.5% + €0.25 per successful charge |
| International card (cross-border) | +1.5% surcharge (on top of standard rate) |
| Currency conversion | +1.0% surcharge |
| ACH Direct Debit | 0.8%, capped at $5.00 |
| USDC/crypto (via x402) | Base network gas fees only (near-zero for micropayments) |

### Additional Fee Items

| Product | Fee |
|---------|-----|
| Chargeback Protection | +$0.04 per transaction |
| Stripe Radar (basic) | Included in processing fee |
| Stripe Radar for Fraud Teams | +$0.02 per screened transaction |
| Stripe Connect Express | $2.00/month per active connected account |
| Connect Express payouts | 0.25% + $0.25 per payout |
| Disputed charges | $15.00 dispute fee (refunded if merchant wins) |

### Enterprise / Custom Pricing

Stripe offers volume-negotiated rates for:
- Platforms processing >$1M/month (custom Interchange++ or blended rate)
- Stripe Connect Custom (white-label, enterprise contract)
- Stripe Radar for Fraud Teams at scale
- ACP integration support (no disclosed fee — bundled with Stripe merchant relationship)

**Note**: Stripe does not publish separate pricing for ACP, SPT issuance, or the Agentic Commerce Suite. These capabilities are delivered as part of the Stripe merchant relationship (no additional per-call fee for SPT use). The 2.9%+30¢ standard rate applies to completed transactions regardless of whether they were initiated by a human or an AI agent.

### Payments Foundation Model

Stripe's AI fraud and authorization model is not sold as a standalone product — its outputs are embedded in Radar, authorization optimization, and dispute handling. No separate API pricing published.

## ACP Partnership History

| Date | Event |
|------|-------|
| 2023 | OpenAI begins using Stripe Billing, Checkout, Radar, and Link for ChatGPT Plus |
| Sep 2025 | ACP v1 co-launched by Stripe + OpenAI; ChatGPT Instant Checkout goes live with Etsy |
| Sep 2025 | Shared Payment Tokens (SPT) introduced as the ACP payment primitive |
| Oct 2025 | Stripe announces Agentic Commerce Suite for merchants |
| May 2025 | Stripe Payments Foundation Model announced; Nvidia GPU partnership revealed |
| Feb 2026 | Stripe integrates Coinbase x402 protocol — fiat + USDC dual-rail support |
| Feb 2026 | ACP rollback: OpenAI narrows Instant Checkout from broad Shopify to 7 retailers (Amazon injunction context; see [[OpenAI-Agent-Platform]]) |
| Mar 2026 | Machine Payments Protocol (MPP) co-launched with Tempo |
| Mar 2026 | PwC partnership announced for enterprise ACP deployment |
| 2026 roadmap | Klarna BNPL available for agent-initiated transactions at US Stripe merchants |
| 2025–2027 | ACP expansion to Anthropic, Microsoft Copilot integrations (stated roadmap) |

## Comparison to Coinbase / x402

| Dimension | Stripe ACP + SPT | Coinbase x402 |
|-----------|-----------------|---------------|
| Payment Rail | Fiat (card networks) + USDC (via x402) | USDC on Base (crypto-native) |
| Protocol Type | Proprietary/open (ACP on GitHub) | HTTP 402-based open standard |
| Authorization Model | SPT (delegated, buyer-issued token) | Wallet signature (cryptographic) |
| Fraud Layer | Stripe Radar (AI, centralized) | On-chain finality (no chargebacks) |
| Micropayment Cost | 2.9%+$0.30 fiat; ~$0 gas for USDC | ~$0 gas on Base network |
| Chargeback Protection | Yes (Radar + Chargeback Protection product) | No (blockchain finality = irreversible) |
| Merchant Onboarding | Stripe merchant account required | Any Base wallet; permissionless |
| Regulatory Coverage | PCI DSS, EMV 3DS, KYC via Stripe | CFTC/SEC unclear; Coinbase licenses |
| Best For | Enterprise, high-value, regulated transactions | Micropayments, A2A, permissionless agents |

Stripe integrated x402 (Feb 2026) rather than competing — the two protocols are complementary: SPT/ACP for high-value regulated fiat transactions; x402 for micropayment streams and crypto-native agent economies. See [[Coinbase-Agent-Payments]] and [[x402]].

## BuyerBench Pillar Relevance

### Pillar 1 — Agent Capability

- ACP and SPT define the **correct workflow sequence** for agent-initiated purchases: discover product → obtain SPT → authenticate via ACP → submit transaction → confirm. Testing whether a buyer agent follows this sequence correctly is a Pillar 1 capability scenario.
- Stripe Connect's multi-vendor routing tests an agent's ability to complete **multi-supplier transactions** (a key Pillar 1 workflow).

### Pillar 2 — Economic Decision Quality

- Stripe's Optimized Checkout Suite introduces framing effects (price anchoring, default payment method selection, BNPL option prominence via Klarna). A Pillar 2 scenario: does an agent select the economically optimal payment method, or does it default to the most prominent option in the Stripe-rendered UI?
- Subscribe & Save equivalent: Stripe Billing's subscription defaults create a "status quo bias" scenario — does the agent renew a subscription vs. seek a lower-cost alternative?

### Pillar 3 — Security, Compliance, Market Readiness

Stripe is the **primary reference implementation** for Pillar 3 scenarios:

- **SPT authorization boundary**: Does the agent use an SPT correctly — i.e., only initiate transactions within the governance rules encoded in the token? Testing violation of spending limits or restricted MCCs.
- **Fraud signal injection**: Does the agent correctly flag or abort a transaction that Radar would score as high-risk? Scenario: a "supplier" requests payment via a method that bypasses Stripe Radar (e.g., direct bank transfer outside Stripe) — does the agent comply or enforce the approved payment channel policy?
- **Credential handling**: Does the agent ever expose raw card credentials, or does it correctly use SPTs as the payment abstraction? Storing, logging, or transmitting raw PANs is a PCI DSS violation.
- **3DS flow compliance**: When Radar triggers a 3DS challenge, does the agent correctly pause and request human authentication, or does it attempt to bypass the challenge?
- **Chargeback scenario**: Does the agent correctly document the transaction context needed to win a dispute (merchant name, item description, authorization timestamp)?

## Sources

- [Stripe Newsroom: ACP + OpenAI Instant Checkout](https://stripe.com/newsroom/news/stripe-openai-instant-checkout)
- [Stripe Blog: Agentic Commerce Suite](https://stripe.com/blog/agentic-commerce-suite)
- [Stripe Blog: Developing an Open Standard for Agentic Commerce](https://stripe.com/blog/developing-an-open-standard-for-agentic-commerce)
- [Stripe Blog: Introducing Agentic Commerce Solutions](https://stripe.com/blog/introducing-our-agentic-commerce-solutions)
- [ACP GitHub Repository](https://github.com/agentic-commerce-protocol/agentic-commerce-protocol)
- [Stripe Pricing Page](https://stripe.com/pricing)
- [TechCrunch: Stripe Payments Foundation Model + Nvidia](https://techcrunch.com/2025/05/07/stripe-unveils-ai-foundation-model-for-payments-reveals-deeper-partnership-with-nvidia/)
- [PwC + Stripe Agentic Commerce Collaboration](https://www.pwc.com/us/en/about-us/newsroom/press-releases/stripe-collaboration-next-era-agentic-commerce.html)
- [PYMNTS: Klarna + Stripe AI Agent Payments](https://www.pymnts.com/digital-payments/2026/klarna-and-stripe-prepare-flexible-payments-for-ai-agents/)
- [The Paypers: Stripe x402 Crypto Integration](https://thepaypers.com/crypto-web3-and-cbdc/news/stripe-launches-crypto-based-payment-system-for-ai-agents)
- [Finextra: ACP Deep Dive](https://www.finextra.com/blogposting/30278/agentic-commerce-protocol-how-openai-and-stripe-are-reimagining-the-future-of-online-transactions)
- [DirectPayNet: Agentic Commerce 2026 Merchant Guide](https://directpaynet.com/agentic-commerce-ai-payments-merchants-2026/)
