---
type: research
title: "ACP — Agentic Commerce Protocol (OpenAI + Stripe)"
created: 2026-04-04
tags:
  - protocol
  - standard
  - agentic-commerce
  - payments
  - openai
  - stripe
  - checkout
  - pillar3
related:
  - '[[Skyfire]]'
  - '[[AP2-UCP]]'
  - '[[x402]]'
  - '[[INDEX]]'
---

# ACP (Agentic Commerce Protocol)

> The open standard for programmatic agent-to-merchant checkout, co-developed by OpenAI and Stripe — the first production-deployed AI agent payment protocol

## Overview

The **Agentic Commerce Protocol (ACP)** is an open-source, Apache 2.0–licensed specification that defines a standardized interaction model for AI agents to discover, select, and purchase goods and services on behalf of buyers. Co-developed by OpenAI and Stripe, ACP provides the checkout and merchant integration layer for agentic commerce: a common "language" that lets any compatible AI agent transact with any ACP-implementing merchant without bespoke integrations.

ACP launched at scale in September 2025 as the technical foundation of **ChatGPT Instant Checkout**, OpenAI's in-chat shopping feature. At launch, ChatGPT users in the US could buy from Etsy sellers and (imminently) from over one million Shopify merchants — all within the chat interface. ACP is available as both a REST API and an MCP (Model Context Protocol) server endpoint, enabling deployment across agent architectures.

In March 2026, OpenAI **removed the built-in Instant Checkout experience** from ChatGPT — primarily due to poor consumer adoption rather than technical failure — following its $50B strategic partnership with Amazon on February 27, 2026. However, the **ACP specification itself was not deprecated**: the protocol remains active, open-source, and under continuing development (version 2026-01-30 is the current stable release). Merchants can still deploy ACP-powered checkout experiences via dedicated ChatGPT apps. ACP's governance has also shifted: from a tightly OpenAI-controlled product feature toward a more independent open standard under broader community governance.

> **BuyerBench relevance (Pillar 3):** ACP is the primary production reference implementation for BuyerBench Pillar 3 secure transaction flow scenarios. Its four-step checkout sequence (CreateCheckoutRequest → UpdateCheckoutRequest → CompleteCheckoutRequest → CancelCheckoutRequest), SharedPaymentToken credential model, HMAC webhook signing, and Stripe Radar fraud integration collectively define what "correct" agent payment API behavior looks like in the real world. Every BuyerBench Pillar 3 scenario involving payment authorization sequencing, credential handling, and fraud detection should be calibrated against ACP's published specification.

> **BuyerBench relevance (Pillar 1):** ACP's merchant-facing product discovery and selection flow directly maps to Pillar 1 supplier discovery scenarios. An agent operating in an ACP-enabled environment can browse product catalogs, compare offers, and initiate checkout through structured API calls — the same capability profile BuyerBench's source-to-award workflow scenarios test.

## Quick Facts

| Attribute | Value |
|-----------|-------|
| Protocol Name | Agentic Commerce Protocol (ACP) |
| Type | Open specification / checkout API |
| Developers | OpenAI (Founding Maintainer) + Stripe (Founding Maintainer) |
| License | Apache 2.0 (open source) |
| Initial Release | 2025-09-29 |
| Current Stable Version | 2026-01-30 |
| Repository | github.com/agentic-commerce-protocol/agentic-commerce-protocol |
| Official Documentation | agenticcommerce.dev / docs.stripe.com/agentic-commerce/protocol |
| Integration Modes | REST API or MCP server |
| Live Deployment | ChatGPT Instant Checkout (Sep 2025 – Mar 2026); merchant apps ongoing |

## Protocol Architecture

### Core Purpose

ACP serves three stakeholder groups simultaneously:
1. **Businesses** — access high-intent buyers through AI agent channels while remaining the merchant-of-record
2. **AI agents** — embed native commerce flows without taking on payment or fulfillment responsibilities
3. **Payment providers** — process agentic transactions through established infrastructure (e.g., Stripe)

### Checkout Flow (Four-Step Sequence)

ACP defines a strict four-step checkout lifecycle:

| Step | Endpoint | Description |
|------|----------|-------------|
| 1 | `CreateCheckoutRequest` | Agent initiates the purchase; establishes session |
| 2 | `UpdateCheckoutRequest` | Agent or buyer modifies selections (quantities, variants, address) |
| 3 | `CompleteCheckoutRequest` | Agent submits the SharedPaymentToken; payment is processed |
| 4 | `CancelCheckoutRequest` | Agent or buyer aborts; session is closed |

Post-completion, webhook events notify the agent of fulfillment status updates asynchronously.

### Authentication & Authorization Model

ACP implements a **dual-layer security model**:

**Transport layer:**
- All API requests require HTTPS
- Bearer token authentication (`Authorization: Bearer {token}`) on all requests
- Signing keys provisioned during merchant onboarding

**Event layer:**
- Webhook events must include an HMAC signature header
- Signature verification ensures agent-originated events cannot be spoofed by third parties

**Payment credential layer (SharedPaymentToken):**
- The AI agent provisions a **Stripe SharedPaymentToken (SPT)** scoped to a specific amount and merchant before submitting `CompleteCheckoutRequest`
- The SPT transfers payment authorization from the buyer's stored credentials to the merchant *without exposing the underlying card or payment data*
- SPTs are time-limited, amount-capped, and merchant-restricted — a fine-grained tokenization scheme that limits blast radius if a token is intercepted

### Fraud Detection

When ACP is used with Stripe as the payment processor, fraud detection is powered by **Stripe Radar**:
- SPTs relay Stripe's machine learning risk signals to the merchant at transaction time
- Risk signals include: likelihood of fraudulent dispute, card testing probability, stolen card likelihood, and card issuer decline predictions
- Stripe Radar's model is trained on global transaction data from Stripe's full merchant network (billions of data points), enabling cross-merchant fraud signal sharing
- Merchants remain the merchant-of-record and retain primary fraud management responsibility

### Compliance Scope

- ACP card-based transactions route through Stripe's payment infrastructure, which is PCI DSS–compliant; merchants using ACP's standard integration benefit from Stripe's PCI scope reduction
- ACP does not itself define compliance obligations but defers to the implementing payment processor (Stripe) for PCI, 3DS2, and network rules

## Versioning History

ACP uses date-based versioning (YYYY-MM-DD):

| Version | Date | Key Changes |
|---------|------|-------------|
| v1 | 2025-09-29 | Initial release — core checkout flow, SPT, basic webhooks |
| v2 | 2025-12-12 | Fulfillment enhancements — richer post-purchase tracking |
| v3 | 2026-01-16 | Capability negotiation — agents can query merchant capabilities before checkout |
| v4 (current) | 2026-01-30 | Extensions, discounts, payment handlers — promotion/coupon support, pluggable payment backends |
| Unreleased | Active dev | Community contributions ongoing |

## Governance

ACP is **jointly governed by OpenAI and Stripe as Founding Maintainers**, with a stated roadmap toward broader community governance under a neutral foundation. Decision-making follows a consensus-based model with defined escalation procedures. All contributors must sign a Contributor License Agreement (CLA). The governance path mirrors open standards like OpenAPI: begin under corporate sponsorship, migrate to independent foundation as ecosystem matures.

The March 2026 Instant Checkout rollback tested the governance model in practice: because ACP is Apache 2.0–licensed and specification-level, OpenAI's business decision to deprioritize the ChatGPT Instant Checkout *feature* did not force a protocol shutdown. Third-party implementers retain the right to continue using and extending the spec regardless of OpenAI's product choices — a meaningful guarantee for enterprise merchants evaluating ACP adoption risk.

## Commercial Deployment: ChatGPT Instant Checkout (Sep 2025 – Mar 2026)

### Launch Context

OpenAI deployed ACP in September 2025 as **ChatGPT Instant Checkout**, allowing US users to buy from Etsy sellers, Shopify merchants, and select retailers directly within the chat interface. Launch partners included Etsy, Shopify, Glossier, Vuori, Spanx, and SKIMS. OpenAI charged merchants a **4% transaction fee**.

### Adoption & Failure

The feature was removed on **March 4, 2026**, just six months after launch. Key failure factors:

| Factor | Detail |
|--------|--------|
| Consumer adoption | ChatGPT users were researching products but not completing purchases inside the app |
| Conversion rates | Walmart's internal data: 3× lower conversion for in-chat checkout vs. "click out to merchant site" |
| Missing features | No real-time inventory, no coupons/promotions, no loyalty integration, no store pickup — basic retail functionality absent |
| Merchant resistance | Retailers resisted losing control of the checkout experience and customer relationship (merchant-of-record concerns) |
| Operational gaps | As of February 2026, OpenAI had not even implemented US state sales tax collection |
| Etsy experience | "Nascent channel for many shoppers" — minimal sales volume despite being a launch partner |

### Post-Rollback Status

After March 4, 2026, OpenAI pivoted to an **app-based model**: major retailers (Walmart, Etsy, Sephora, DoorDash, Instacart, CarMax, Lowe's, Expedia) now operate dedicated ChatGPT apps that link back to their own checkout flows. ACP's role narrows from a universal in-chat checkout rail to a protocol option that app developers can optionally implement. The **Amazon strategic partnership ($50B, Feb 27, 2026)** appears to have influenced this pivot — Amazon's model is "send users to Amazon" rather than "buy inside ChatGPT."

### BuyerBench Protocol Governance Scenario

The Instant Checkout rollback is a unique scenario type BuyerBench should model: a technically functional protocol disabled by a business-layer decision. This tests whether AI buyer agents correctly handle protocol deprecation signals, adapt to governance changes, and respect authorization boundaries that shift based on platform-level policy rather than technical error codes.

## Competitive Position

### Protocol Layer Mapping

ACP, AP2 (Google), and x402 (Coinbase) are not direct competitors — they address different protocol layers:

| Protocol | Layer | Focus |
|----------|-------|-------|
| **ACP** | Checkout / Merchant Integration | Full shopping cart-to-payment flow; REST or MCP |
| **AP2 / UCP** | Authorization / Trust | Portable, digitally-signed spending mandates; multi-party governance |
| **x402** | Execution / Micropayment | HTTP-native pay-per-use; crypto settlement (USDC) |

Merchants may need to support both ACP and AP2 simultaneously in 2026 — they are complementary layers in the emerging agentic commerce stack, not mutually exclusive choices.

### ACP vs. AP2 Key Differences

| Dimension | ACP (OpenAI + Stripe) | AP2 / UCP (Google) |
|-----------|----------------------|--------------------|
| **Authorization model** | Custom merchant approval logic + SPT | Portable, revocable, digitally-signed mandates |
| **Multi-party support** | Merchant-centric (bilateral) | Multi-stakeholder (orchestrator + agent + merchant + bank) |
| **Audit trail** | Webhook-based post-hoc events | Built-in compliance audit trail and governance logs |
| **Partner ecosystem** | OpenAI + Stripe, merchant apps | 60+ partners incl. Mastercard, PayPal, Walmart, Target |
| **Enterprise compliance** | Inherits Stripe's PCI/compliance posture | AP2 explicitly designed for multi-party auditability |
| **Current status** | Narrowed scope (Mar 2026 rollback) | Growing momentum with UCP/NRF Jan 2026 launch |

### Key Competitors
- [[AP2-UCP]] — Google's authorization and trust protocol; 60+ partners, growing enterprise adoption, launched UCP at NRF Jan 2026
- [[x402]] — Coinbase's HTTP micropayment execution protocol; crypto-native, minimal design, machine-to-machine focus
- [[Skyfire]] — Not a protocol competitor, but a complementary payment rails layer that KYAPay identity could pair with ACP checkout flows
- [[Mastercard Agent Pay]] — Card-network-level agentic payment tokenization; competes at the credential layer

## Related Entities
- [[Skyfire]] — Skyfire's KYAPay identity layer could serve as an agent identity/authorization frontend for ACP checkout flows; both are Pillar 3 reference implementations
- [[AP2-UCP]] — Direct protocol-level competitor/complement; AP2 handles authorization semantics that ACP defers to the payment processor
- [[x402]] — Complementary crypto-native micropayment execution layer; a16z/Coinbase overlap with Skyfire investors
- [[Procure AI]] — Enterprise procurement agents like Procure AI's 50+ autonomous agents would integrate ACP for payment execution in a full source-to-pay workflow
- [[PCI-DSS-v4]] — ACP's card payment processing inherits PCI DSS obligations; Stripe's SPT model is designed to minimize merchant PCI scope
- [[FATF-AML-CFT]] — If ACP extends to crypto rails (x402 integration), FATF Travel Rule obligations may apply

## Sources

1. [Agentic Commerce Protocol — Official Site](https://www.agenticcommerce.dev/) — Accessed 2026-04-04
2. [ACP GitHub Repository (Apache 2.0)](https://github.com/agentic-commerce-protocol/agentic-commerce-protocol) — Accessed 2026-04-04
3. [Stripe ACP Documentation](https://docs.stripe.com/agentic-commerce/protocol) — Accessed 2026-04-04
4. [Stripe Blog: Developing an open standard for agentic commerce](https://stripe.com/blog/developing-an-open-standard-for-agentic-commerce) — Accessed 2026-04-04
5. [OpenAI Developers: Agentic Commerce Protocol](https://developers.openai.com/commerce) — Accessed 2026-04-04
6. [What went wrong with ChatGPT's Instant Checkout — Modern Retail](https://www.modernretail.co/technology/what-went-wrong-with-chatgpts-instant-checkout/) — Accessed 2026-04-04
7. [OpenAI's plans to make ChatGPT more like Amazon — TechCrunch](https://techcrunch.com/2026/03/24/openais-plans-to-make-chatgpt-more-like-amazon-arent-going-so-well/) — Accessed 2026-04-04
8. [Agentic Payments Explained: ACP, AP2, and x402 — Orium](https://orium.com/blog/agentic-payments-acp-ap2-x402) — Accessed 2026-04-04
9. [Forrester: What It Means That The Leader In "Agentic Commerce" Just Pulled Back](https://www.forrester.com/blogs/what-it-means-that-the-leader-in-agentic-commerce-just-pulled-back/) — Accessed 2026-04-04
10. [OpenAI + Amazon: Power Couple — Forrester](https://www.forrester.com/blogs/power-couple-openai-amazon-may-have-just-won-consumer-agentic-commerce/) — Accessed 2026-04-04
11. [OpenAI ACP vs Google UCP: The Protocol War — FourWeekMBA](https://fourweekmba.com/openai-acp-vs-google-ucp-the-agentic-commerce-protocol-war/) — Accessed 2026-04-04
12. [ACP vs AP2: Standards War — FourWeekMBA](https://fourweekmba.com/acp-vs-ap2-the-agentic-commerce-standards-war-that-will-reshape-the-web/) — Accessed 2026-04-04

---
*Last updated: 2026-04-04*
