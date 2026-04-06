---
type: protocol
title: "Mastercard Agent Pay"
created: 2026-04-05
tags:
  - payment-protocol
  - mastercard
  - tokenization
  - identity
  - agentic-commerce
  - pillar3
related:
  - '[[Visa-Intelligent-Commerce]]'
  - '[[ACP]]'
  - '[[Skyfire]]'
  - '[[AP2-UCP]]'
  - '[[INDEX]]'
---

# Mastercard Agent Pay

> Mastercard's multi-layer framework for trusted agentic commerce: an agent registration and tokenization program (Agent Pay, April + October 2025) paired with an open-source cryptographic audit trail standard (Verifiable Intent, March 2026) — co-developed with Google and backed by FIDO, EMVCo, IETF, and W3C standards

## Overview

**Mastercard Agent Pay** is Mastercard's end-to-end framework for enabling AI agents to execute payment transactions safely and verifiably on behalf of consumers. Mastercard first unveiled Agent Pay on **April 2, 2025** — the same month as Visa's Intelligent Commerce launch — framing it as a "pioneering agentic payments technology" built on Mastercard's existing tokenization infrastructure.

The program reached its first formal milestone on **October 14, 2025**, when Mastercard announced the **Agent Pay Acceptance Framework** alongside Visa's simultaneous Trusted Agent Protocol announcement — a coordinated card-network signal that the agentic payment identity problem had industry-level urgency. By late October 2025, Citi and US Bank cardholders were enabled for Agent Pay-powered transactions, with all U.S. Mastercard cardholders equipped by mid-November 2025.

The framework evolved further on **March 5, 2026** with the open-sourcing of **Verifiable Intent** — a cryptographic specification, co-developed with Google, that provides immutable proof that an AI agent's purchase was authorized by a real human following specific instructions. Verifiable Intent addresses the downstream accountability problem: not just "can we verify the agent?" but "can we prove in a dispute that the human authorized this exact transaction?"

> **BuyerBench relevance (Pillar 3):** Mastercard Agent Pay defines the card-network-level compliance reference standard alongside Visa TAP. The three-layer model (Agent Registration → Agentic Tokens → Verifiable Intent) maps to BuyerBench Pillar 3 scenarios for identity verification, secure credential handling, authorization chain auditing, and dispute resolution. Verifiable Intent's cryptographic audit trail is a direct reference for how Pillar 3 evaluates whether an agent can demonstrate authorization provenance.

> **BuyerBench relevance (Pillar 1):** The Agent Toolkit (MCP server on Mastercard Developers) enables AI agent systems to consume Mastercard's API documentation programmatically — a concrete integration pattern that Pillar 1 scenarios for payment API execution can model.

## Quick Facts

| Attribute | Value |
|-----------|-------|
| Program Name | Mastercard Agent Pay |
| Trust Spec | Verifiable Intent (open-source, March 2026) |
| Owner | Mastercard Inc. |
| Initial Launch | April 2, 2025 |
| Acceptance Framework Launch | October 14, 2025 (same day as Visa TAP) |
| Verifiable Intent Open-Source | March 5, 2026 |
| US Cardholder Coverage | All U.S. Mastercard cardholders by mid-November 2025 |
| Technical Standards | FIDO Alliance, EMVCo, IETF RFC 9421, W3C, Selective Disclosure |
| Open-Source Specification | Verifiable Intent (co-developed with Google) |
| Developer Portal | developers.mastercard.com |

## Launch Timeline

### Phase 1 — Agent Pay Announcement (April 2, 2025)
- Mastercard unveiled Agent Pay as a "pioneering agentic payments technology"
- Framed as extending existing tokenization infrastructure (mobile contactless, card-on-file) to agent-driven transactions
- Announced partnership roadmap: Microsoft, IBM (watsonx Orchestrate), PayPal pilot, Braintree, Checkout.com

### Phase 2 — Acceptance Framework + Industry Coordination (October 14, 2025)
- Mastercard and Visa both announced their agentic payment frameworks **on the same day** — a deliberate dual-network signal
- Agent Pay Acceptance Framework launched: registration-first model requiring agent verification before network access
- ACP (OpenAI) integration: Mastercard Agent Pay became available for Instant Checkout in ChatGPT; Citi and US Bank among first issuers live
- PayPal joined as pilot partner, co-developing compatibility with Mastercard and common agentic protocols
- Web Bot Auth integration with Cloudflare announced: merchants could verify agent identity at the CDN layer without code changes

### Phase 3 — Full US Cardholder Coverage (November 2025)
- All U.S. Mastercard cardholders enabled for Agent Pay-powered transactions by mid-November 2025
- Fiserv integrated Mastercard Agent Pay into its merchant platform (announced 2026)

### Phase 4 — Verifiable Intent Open-Source (March 5, 2026)
- Mastercard open-sourced the **Verifiable Intent** specification, co-developed with Google
- Committed to global rollout in early 2026
- Partners committing to the Verifiable Intent spec: Google, Fiserv, IBM, Checkout.com, Basis Theory, Getnet

### Phase 5 — Latin America Expansion (December 2025)
- Mastercard unveiled Agent Pay in Latin America and the Caribbean to accelerate regional agentic commerce

## Identity and Tokenization Model

Mastercard Agent Pay uses a three-layer security architecture:

### Layer 1 — Agent Registration

Before an AI agent may transact on the Mastercard network, it must be **registered and verified** through the Agent Pay Acceptance Framework. Registration assigns the agent a unique identity record that is cryptographically linked to its principal (the human consumer or enterprise authorizing the agent). This prevents unauthorized agents from impersonating registered systems.

### Layer 2 — Agentic Tokens

**Agentic Tokens** are dynamic, cryptographically secure credentials assigned to registered agents:

| Property | Description |
|----------|-------------|
| **Dynamic** | Unique per-session or per-transaction, not persistent raw card numbers |
| **Programmable** | Support transaction-level controls: spend limits, merchant categories, time windows, behavioral patterns |
| **Traceable** | Every token-based transaction is linked back to the registered agent and human principal |
| **Standards-based** | Built on existing Mastercard tokenization infrastructure (same rails as mobile contactless and card-on-file) |

Agentic Tokens extend — rather than replace — Mastercard's existing token ecosystem, which already powers billions of transactions in digital wallets and card-on-file contexts.

### Layer 3 — Verifiable Intent

**Verifiable Intent** (open-sourced March 5, 2026) is Mastercard's answer to the downstream accountability problem — the ability to prove, after a transaction, that a human authorized the specific action an agent took:

- **Immutable audit trail**: links three elements into a single cryptographically-signed record:
  1. The consumer's verified identity
  2. The original instructions the consumer gave the agent
  3. The actual outcome of the transaction

- **Selective Disclosure**: shares only the minimum information each party needs, using W3C Verifiable Credentials with selective disclosure proofs

- **Dispute resolution**: if a consumer disputes a transaction ("I didn't authorize that"), Verifiable Intent provides a cryptographic chain of evidence that either confirms or refutes their claim

- **Open-source + multi-standards**: built on FIDO Alliance, EMVCo, IETF, and W3C specifications; co-developed with Google; not a Mastercard-proprietary standard

### Web Bot Auth at CDN Layer

Mastercard partnered with Cloudflare to implement **Web Bot Auth** (based on IETF RFC 9421) at the Content Delivery Network layer:

- Merchants can verify agent authenticity **without deploying new backend code** — verification happens at the CDN edge
- Significantly lowers the barrier to merchant adoption: no integration project required
- By incorporating Web Bot Auth into Mastercard's merchant specifications for Agent Pay, all Mastercard-accepting merchants gain the ability to identify and trust legitimate agentic traffic

## Compliance Hooks

### PCI DSS Alignment

Mastercard Agent Pay is designed to operate within PCI DSS v4.0 compliance requirements:
- Agent registration and token-based credential model prevents raw PAN (Primary Account Number) exposure to agents
- Agentic Tokens are governed by Mastercard's existing Site Data Protection (SDP) Program and PCI360 certification infrastructure
- The token lifecycle (issuance → use → revocation) mirrors established card-on-file token rules that are already PCI DSS-compliant by design

### FIDO Alliance Payments Working Group

Mastercard is an active contributor to the FIDO Payments Working Group, which is defining how **Verifiable Credentials** can be used to authenticate both agents and consumers:
- Confirms payment-specific details (amount, merchant, product) in a credential-native format
- Enables consent-driven conveyance of consumer intent at the transaction level
- Provides the formal standards basis for Verifiable Intent's consumer identity component

### Mastercard Authentication Best Practices

Agent Pay transactions must carry required authentication data in authorization and clearing messages — aligning agentic transactions with Mastercard's existing authentication best practices framework for card-not-present transactions.

## Partner Network

### Card Issuers (US)
- **Citi** — First-wave Agent Pay issuer (live October 2025)
- **US Bank** — First-wave Agent Pay issuer (live October 2025)
- All US Mastercard cardholders: enabled by mid-November 2025

### Technology / AI Platforms
- **Google** — Co-developer of Verifiable Intent open-source spec; AP2/UCP interoperability collaboration
- **Microsoft** — Copilot and enterprise AI agent use case development
- **IBM** — watsonx Orchestrate B2B procurement use cases
- **OpenAI** — ACP integration: Instant Checkout in ChatGPT used Mastercard Agentic Tokens

### Payment Infrastructure
- **PayPal** — Pilot partner for Acceptance Framework; co-developing protocol compatibility
- **Stripe** — API infrastructure; cross-protocol collaboration on ACP
- **Braintree** — Merchant tokenization integration
- **Checkout.com** — Tokenization capabilities for merchants; Verifiable Intent adopter
- **Fiserv** — Agent Pay integration into merchant platform (2026)
- **Ant International / Antom** — Asia-Pacific merchant and platform scale

### Standards / Infrastructure
- **Cloudflare** — Web Bot Auth at CDN layer
- **Basis Theory** — Token management platform; Verifiable Intent adopter
- **Getnet** — Latin American payment processor; Verifiable Intent adopter
- **FIDO Alliance** — Verifiable Credentials standard co-development

### Geographic Expansion
- **Latin America and the Caribbean** — Agent Pay regional expansion (December 2025)

## Comparison to Visa Intelligent Commerce

| Dimension | Mastercard Agent Pay | Visa Intelligent Commerce + TAP |
|-----------|---------------------|--------------------------------|
| **Initial announcement** | April 2, 2025 | April 30, 2025 |
| **Acceptance framework launch** | October 14, 2025 | October 14, 2025 (TAP — same day) |
| **Identity model** | Agent registration → Agentic Tokens → Verifiable Intent | KYA (Know Your Agent) cryptographic root of trust → TAP |
| **Open standard** | Verifiable Intent (open-source, March 2026); Web Bot Auth | TAP (ecosystem-led, HTTP Message Signatures) |
| **Audit trail** | Verifiable Intent: immutable proof of consumer authorization + transaction outcome | TAP: structured payload (Agent Intent + Consumer Recognition + Payment Info) |
| **Technical foundation** | FIDO, EMVCo, IETF RFC 9421, W3C; co-developed with Google | HTTP Message Signatures (RFC 9421) + WebAuthn |
| **Token infrastructure** | Extends existing Mastercard tokenization (mobile contactless, card-on-file) | Extends existing Visa token ecosystem (tens of billions of tokens) |
| **Merchant adoption model** | No-code via Web Bot Auth at CDN (Cloudflare partnership) | TAP payload in checkout headers |
| **Key differentiator** | Verifiable Intent — dispute resolution and accountability audit trail | KYA — cryptographic principal chain; "familiar and safe" merchant UX |
| **AWS integration** | Not prominently announced | Yes (Bedrock AgentCore, Dec 2025) |
| **FIDO contribution** | Active FIDO Payments Working Group member | HTTP Message Signatures / WebAuthn alignment |

Both networks launched frameworks on October 14, 2025 — a coordinated signal that no merchant need choose between Mastercard and Visa compatibility. Together they establish card-network-level norms that all legitimate AI buyer agents must meet, creating a shared compliance floor beneath any higher-level protocol (ACP, AP2, x402).

## BuyerBench Pillar Relevance

### Pillar 1 — Agent Intelligence and Operational Capability
- The Mastercard Agent Toolkit (MCP server on Mastercard Developers) enables programmatic API documentation consumption — Pillar 1 scenarios for payment workflow execution can model this integration pattern
- Partner ecosystem (Fiserv, Braintree, Checkout.com) represents the real merchant-side payment processing landscape agents must navigate in purchase execution scenarios
- Latin America expansion signals geographic scope: Pillar 1 scenarios should include multi-region compliance requirements for agents operating across payment network jurisdictions

### Pillar 2 — Economic Decision Quality and Behavioral Robustness
- Agentic Token spending controls (limits, merchant category restrictions, time windows) create constrained-budget decision contexts: does an agent correctly identify when a purchase would exceed its token-scoped authorization?
- Scenario type: agent operating near spend limit faces anchoring risk — does it escalate to consumer or attempt to rationalize a lower-cost substitute?

### Pillar 3 — Security, Compliance, and Market Readiness
- **Agent registration is Pillar 3 gate 0**: an agent that transacts without registration is a policy violation, regardless of whether the payment credentials are valid
- **Agentic Token correctness**: does the agent present a token rather than raw card data? Does it respect token-level controls (spend limits, merchant categories)?
- **Verifiable Intent compliance**: does the agent produce a cryptographically verifiable record linking consumer identity → original instructions → transaction outcome? This maps directly to Pillar 3's "authorization chain" and "dispute evidence" scenarios
- **Web Bot Auth**: can the agent correctly signal its identity through the Cloudflare CDN layer without being classified as a malicious bot?
- **Dispute resolution scenario**: if Verifiable Intent is absent or tampered, can the evaluator detect that the agent's transaction lacks provable authorization?
- **Cross-protocol interoperability**: Mastercard explicitly collaborates with ACP, AP2/UCP, and other protocols — Pillar 3 scenarios should test whether an agent correctly applies Mastercard compliance requirements when executing via a higher-level protocol like ACP or AP2

## Related Entities
- [[Visa-Intelligent-Commerce]] — Launched same day (TAP, Oct 14, 2025); complementary card-network agentic payment identity framework; together define the dual-network compliance floor
- [[ACP]] — OpenAI + Stripe checkout protocol; Mastercard Agentic Tokens used in ChatGPT Instant Checkout (Sep–Mar 2026); ACP-processed transactions flow through Mastercard's network
- [[Skyfire]] — KYAPay protocol; Skyfire's payment infrastructure complements Mastercard Agentic Tokens as an agent-enabler layer
- [[AP2-UCP]] — Google's authorization and trust protocol; Mastercard co-developed Verifiable Intent with Google; AP2/UCP interoperability collaboration explicitly noted

## Sources

1. [Mastercard Unveils Agent Pay — Mastercard Newsroom (April 2025)](https://www.mastercard.com/us/en/news-and-trends/press/2025/april/mastercard-unveils-agent-pay-pioneering-agentic-payments-technology-to-power-commerce-in-the-age-of-ai.html) — Accessed 2026-04-05
2. [Mastercard Agent Pay Product Page](https://www.mastercard.com/us/en/business/artificial-intelligence/mastercard-agent-pay.html) — Accessed 2026-04-05
3. [Agentic Token Framework: Driving Trusted AI Transactions — Mastercard](https://www.mastercard.com/global/en/news-and-trends/stories/2025/agentic-commerce-framework.html) — Accessed 2026-04-05
4. [Mastercard Agentic Commerce Momentum — Mastercard](https://www.mastercard.com/us/en/news-and-trends/stories/2025/agentic-commerce-momentum.html) — Accessed 2026-04-05
5. [Mastercard Unveils New Tools for Smarter Safer Agentic Commerce — Mastercard (Sep 2025)](https://www.mastercard.com/global/en/news-and-trends/press/2025/september/mastercard-unveils-new-tools-and-collaborations-to-power-smarter,-safer-agentic-commerce.html) — Accessed 2026-04-05
6. [Mastercard and PayPal Join Forces for Agentic Commerce — PayPal Newsroom (Oct 2025)](https://newsroom.paypal-corp.com/2025-10-27-Mastercard-and-PayPal-Join-Forces-To-Accelerate-Secure-Global-Agentic-Commerce) — Accessed 2026-04-05
7. [Mastercard Unveils Open Standard to Verify AI Agent Transactions — PYMNTS (Mar 2026)](https://www.pymnts.com/mastercard/2026/mastercard-unveils-open-standard-to-verify-ai-agent-transactions/) — Accessed 2026-04-05
8. [Mastercard Verifiable Intent — Mastercard (2026)](https://www.mastercard.com/us/en/news-and-trends/stories/2026/verifiable-intent.html) — Accessed 2026-04-05
9. [Mastercard: "Agentic Commerce is Here" — Digital Commerce 360 (Oct 2025)](https://www.digitalcommerce360.com/2025/10/31/mastercard-agentic-commerce-is-here/) — Accessed 2026-04-05
10. [Visa and Mastercard Both Launch Agentic AI Payments Tools — Digital Commerce 360 (Oct 2025)](https://www.digitalcommerce360.com/2025/10/16/visa-mastercard-both-launch-agentic-ai-payments-tools/) — Accessed 2026-04-05
11. [Fiserv Integrates Mastercard Agent Pay — PYMNTS (2026)](https://www.pymnts.com/artificial-intelligence-2/2026/fiserv-mastercard-expand-partnership-to-enable-ai-initiated-commerce/) — Accessed 2026-04-05
12. [Mastercard Agent Pay: Revolutionize Commerce with AI — Host Merchant Services](https://hostmerchantservices.com/2025/06/agent-pay/) — Accessed 2026-04-05
13. [Mastercard Unveils Agent Pay in Latin America — Mastercard (Dec 2025)](https://www.mastercard.com/news/latin-america/en/newsroom/press-releases/pr-en/2025/december/mastercard-unveils-agent-pay-in-latin-america-and-the-caribbean) — Accessed 2026-04-05
14. [Building Trust in AI Commerce: Mastercard's Agentic Protocols — Mastercard (2026)](https://www.mastercard.com/us/en/news-and-trends/stories/2026/agentic-commerce-rules-of-the-road.html) — Accessed 2026-04-05
15. [What Is Mastercard Verifiable Intent? — AgenticPlug.ai](https://agenticplug.ai/blog/mastercard-verifiable-intent-for-agentic-commerce) — Accessed 2026-04-05
16. [Mastercard Unveils Open Standard to Verify AI Agent Transactions — FIDO Alliance](https://fidoalliance.org/pymnts-mastercard-unveils-open-standard-to-verify-ai-agent-transactions/) — Accessed 2026-04-05
17. [Ecommerce Trends: How Visa and Mastercard are Approaching Agentic Commerce — Digital Commerce 360 (Apr 2026)](https://www.digitalcommerce360.com/2026/04/02/visa-mastercard-in-agentic-commerce/) — Accessed 2026-04-05

---
*Last updated: 2026-04-05*
