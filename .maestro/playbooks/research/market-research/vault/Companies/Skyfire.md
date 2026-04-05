---
type: research
title: "Skyfire — Identity and Payment Rails for Autonomous AI Agents"
created: 2026-04-04
tags:
  - company
  - payments
  - ai-agent-infrastructure
  - kya
  - identity
  - agentic-commerce
  - pillar3
related:
  - '[[Procure-AI]]'
  - '[[Fairmarkit]]'
  - '[[Omnea]]'
  - '[[Zycus]]'
  - '[[INDEX]]'
---

# Skyfire

> Payment rails and verified identity for the AI agent economy — KYA, multi-rail wallets, and the open KYAPay protocol

## Overview

Skyfire Systems is the creator of the world's first payment network built specifically for the AI agent economy. Founded in 2024, the company provides AI agents with three foundational capabilities: verified identity (Know Your Agent / KYA), programmable multi-rail wallets, and autonomous transaction execution — the full stack needed for an AI agent to independently research, select, and pay for goods and services without exposing human credentials or requiring per-transaction human approval.

Skyfire launched publicly in August 2024 with an $8.5M seed round, added $1M from the a16z Crypto Startup Accelerator (CSX Fall 2024 cohort), and exited beta in March 2025 with an enterprise-ready 1.0 platform. In June 2025, Skyfire open-sourced the **KYAPay protocol** — its identity and payment verification specification — making it an open standard for agent commerce. In December 2025, Skyfire demonstrated a fully functional live proof-of-concept: a Consumer Reports AI agent researched and purchased Bose headphones on Bose.com using KYAPay combined with Visa's Intelligent Commerce and Trusted Agent Protocol.

Skyfire's strategic position is uniquely *infrastructure-layer*, not application-layer: it does not build buyer agents but provides the financial rails on which buyer agents (including Procure AI, and potentially any autonomous procurement tool) transact. This makes it a critical reference for BuyerBench Pillar 3 — the payment security, authorization, and fraud detection pillar.

> **BuyerBench relevance (Pillar 3):** Skyfire is the most direct commercial reference implementation for BuyerBench's Pillar 3 secure transaction flow scenarios. Its KYA identity model defines what "agent authorization" looks like in production: how agents are credentialed, how spending limits are enforced, how human oversight checkpoints are implemented ("just-in-time decisioning"), and how fraud is detected via behavioral/contextual signals (Cequence partnership). Every Pillar 3 scenario involving payment authorization, credential handling, and fraud detection should be evaluated against Skyfire's architecture as a real-world baseline.

> **BuyerBench relevance (Pillar 1):** Skyfire's multi-rail payment execution (cards, ACH, wires, USDC) creates tool-use scenarios for Pillar 1: an agent that successfully identifies a supplier and negotiates a price must also correctly route and execute the payment through an infrastructure layer like Skyfire — completing the source-to-pay loop that Pillar 1 capability scenarios test.

## Quick Facts

| Attribute | Value |
|-----------|-------|
| Founded | 2024 |
| Headquarters | San Francisco, CA, USA |
| Employees | Small team (early-stage) |
| Funding | $9.5M total (2 rounds, 18 investors) |
| Seed Round | $8.5M (Aug 2024 — Neuberger Berman, Inception Capital, Arrington Capital + others) |
| Accelerator | a16z CSX Fall 2024 ($1M, part of cohort) |
| Additional Investors | Coinbase Ventures, Neuberger Berman |
| Stage | Seed / Early-stage |
| Website | skyfire.xyz |

## Products & Services

### KYA (Know Your Agent) Identity System
Skyfire's core identity product assigns every AI agent a verified, persistent digital identity. The KYA model:
- Creates a verifiable track record of agent activity across transactions
- Enables services to restrict access to "verified and trusted agents only"
- Allows merchants and service providers to confidently accept non-human actors as paying customers
- Is OAuth2/OIDC compatible, enabling integration with existing authentication infrastructure
- Underpins the KYAPay open protocol (see below)

### KYAPay Open Protocol (Launched June 2025)
Skyfire's open specification (Apache-licensed) for agent identity and payment verification:
- Verifies to both the consumer and the merchant that the AI agent is acting on behalf of a real, authorized user
- Enables "secure access to a Visa credential, allowing the AI agent to complete checkout without exposing sensitive consumer credentials"
- Designed as an open standard — analogous to how OAuth2 standardized human-to-service authentication, KYAPay standardizes agent-to-merchant authorization

### Programmable Agent Wallets
Each AI agent registered on Skyfire gets a programmable wallet with:
- **Multi-rail funding sources**: debit cards, credit cards, ACH, international wires, and USDC (USD-backed stablecoin via Coinbase)
- **Spending limits**: per-agent budget controls set by the operator (per-transaction and over-time limits)
- **Unique agent identifier**: distinguishes individual AI agents as first-class financial participants
- **Transaction monitoring dashboard**: operators track agent spend, identify demand patterns, and audit activity

### Just-In-Time Decisioning
A risk-adaptive human oversight mechanism:
- When an agent hits a transaction above a configured size threshold, it triggers a real-time approval request to the human operator
- Allows operators to intervene selectively at high-value or unusual transaction moments without blocking routine low-value autonomous execution
- Critical design pattern for Pillar 3 escalation and authorization scenarios

### Skyfire for Enterprise (Launched March 2025)
Enterprise tier launched at 1.0 exit from beta:
- Organizations create and manage wallets across agent fleets
- Set team-wide payment policies (category restrictions, vendor allowlists, spend caps)
- Programmatic monetization: APIs for service providers to accept payments from paying agents using a no-code solution
- Revenue stream creation for LLM, dataset, and API providers selling agent-accessible services

### Agent Checkout
Skyfire's consumer-facing transaction execution layer:
- Enables fully autonomous completion of shopping and purchasing workflows
- Provides agents with verified identity for web access and account creation
- Tokenized credit cards + real-time micropayments + instant programmatic checkout
- Tested in the live Consumer Reports → Bose headphones demo (Dec 2025)

## Leadership

- **Buck Woody** — CEO and Co-Founder (per TechCrunch / BusinessWire launch coverage; background in fintech infrastructure)
- Early team drawn from fintech, payments, and crypto rails backgrounds (consistent with Neuberger Berman + Coinbase Ventures investor alignment)

## Funding History

| Date | Round | Amount | Lead Investor |
|------|-------|--------|---------------|
| Aug 2024 | Seed | $8.5M | Neuberger Berman |
| Fall 2024 | Accelerator (a16z CSX) | ~$1M | a16z Crypto (CSX program) |
| **Total** | | **$9.5M** | **18 investors total** |

**Key Investors:** Neuberger Berman, Inception Capital, Arrington Capital, a16z Crypto Startup Accelerator (CSX), Coinbase Ventures

**Strategic significance of investors:**
- **Neuberger Berman**: Traditional asset manager ($460B AUM) leading a seed round signals institutional financial-sector validation of agent payment infrastructure
- **a16z CSX**: The crypto startup accelerator arm of a16z — connects Skyfire to the crypto/Web3 payment protocol ecosystem (directly relevant to x402 / USDC rail strategy)
- **Coinbase Ventures**: Validates the USDC stablecoin payment rail and links Skyfire to the x402 HTTP-native micropayment protocol that Coinbase co-developed

## Recent Developments

- **2025-12-18**: Skyfire demonstrates live end-to-end agentic commerce purchase — Consumer Reports AI agent buys Bose headphones on Bose.com using KYAPay + Visa Intelligent Commerce + Visa Trusted Agent Protocol. First publicly demonstrated fully autonomous agent purchase across identity verification, product research, and payment execution layers simultaneously.
- **2025-06-26**: Skyfire launches **open KYAPay protocol** with Agent Checkout — turns AI agents into full participants in the digital economy via open-source payment and identity specification.
- **2025-04-22**: Skyfire × **Cequence Security** partnership — Cequence's bot management and API security (multi-dimensional ML for behavioral, contextual, and intent-based signals) integrates Skyfire-issued agent identifiers to help businesses distinguish verified Skyfire agents from scrapers and malicious automation.
- **2025-03-06**: Skyfire **exits beta** and launches 1.0 enterprise platform — introduces Skyfire for Enterprise (wallets, team-wide policies), "just-in-time decisioning" for high-value transactions, and Programmatic Monetization for APIs/LLMs.
- **2024-10-24**: AI Agents Race to Join Skyfire Payments Network — Pricing Culture, Bazaars, Zinc, Linkup, and others join the Skyfire Payment Network during beta; thousands of instant global transactions daily.
- **2024-08-21**: Skyfire **publicly launches** with $8.5M seed funding — introduces the concept of KYA (Know Your Agent) and the multi-rail programmable wallet for AI agents.

## Security & Fraud Architecture

### Identity Layer (KYA / KYAPay)
- Each Skyfire agent carries a cryptographically issued identifier that merchants and services can verify
- The identifier links to a human user's authorization delegation — establishing a chain of accountability from human principal to AI agent
- Compatible with OAuth2/OIDC flows used in existing API security tooling

### Spending Controls
- Per-transaction and per-period spending limits configured by operator per agent
- Category restrictions and vendor allowlists enforced at wallet policy level (Enterprise tier)
- Just-in-time decisioning for transactions exceeding operator-defined thresholds

### Fraud Prevention (Cequence Partnership)
- Cequence's ML-based bot management evaluates behavioral, contextual, and intent-based signals at API layer
- Skyfire-issued identifiers are fed into Cequence's model as first-class trust signals
- Legitimate paying agents are allowed through; scraping bots and fraudulent automation are blocked
- Security teams can define allow/deny rules based on agent identity type, not just IP or user-agent heuristics

### Multi-Rail Compliance Surface
| Payment Rail | Compliance Implications |
|---|---|
| Card (Visa/Mastercard) | PCI DSS v4.0, EMV 3DS2 tokenization, Visa Trusted Agent Protocol |
| ACH / Bank Wire | FinCEN BSA/AML obligations; Reg E |
| USDC (Coinbase) | FATF Travel Rule (for transactions >$1,000), Coinbase VASP compliance |
| Crypto (x402-adjacent) | FATF AML/CFT guidance; limited PCI DSS applicability; novel fraud detection landscape |

## Competitive Position

Skyfire occupies a unique **infrastructure-only** niche — it is not competing with buyer agent application companies (Procure AI, Omnea, Fairmarkit) but rather enabling them. Its primary competition is:

1. **Visa Intelligent Commerce + Trusted Agent Protocol** — Skyfire is a *partner* to Visa, not a direct competitor; however, if Visa builds a full end-to-end KYA stack, Skyfire's independent value diminishes.
2. **Mastercard Agent Pay** — parallel infrastructure play at the card network layer; competes for the same "who verifies AI agent identity at transaction time" problem.
3. **Stripe** — Stripe is co-developing ACP (with OpenAI) and has existing agent payment toolkits; represents the merchant-side payment infrastructure competitor.
4. **Crossmint** — Web3-native competitor providing AI agents with virtual cards and crypto wallets; similar KYA-style agent identity approach with crypto-first orientation.
5. **x402 (Coinbase)** — Not a direct competitor but an adjacent protocol that could disintermediate Skyfire on the crypto rail by providing HTTP-native micropayments without a wallet infrastructure layer.

### Key Differentiators
- **First mover** in purpose-built agent payment infrastructure (launched Aug 2024, ahead of Visa/Mastercard agent protocols by >1 year)
- **Open protocol** (KYAPay) lowers adoption friction for merchants and agent builders — Skyfire builds network effects, not just lock-in
- **Multi-rail** (cards + ACH + crypto) positions Skyfire above any single-rail competitor
- **Cequence partnership** — uniquely combines agent identity with API-layer security, addressing the fraud detection problem that pure-wallet competitors don't address at the transport layer

## Related Entities

- [[Visa Intelligent Commerce + Trusted Agent Protocol]] — Strategic partner; KYAPay is built on top of Visa's Trusted Agent Protocol identity model for card-based transactions
- [[Mastercard Agent Pay]] — Indirect competitor at the payment rails layer; Mastercard's tokenization model is an alternative to Skyfire's wallet approach
- [[x402]] — Coinbase Ventures investment connects Skyfire to the x402 crypto payment protocol ecosystem; x402 is Skyfire's USDC rail's theoretical upstream protocol
- [[ACP (Agents Commerce Protocol)]] — Skyfire could serve as a payment execution backend for ACP-based checkout flows; OpenAI/Stripe ACP vs. Skyfire/Visa KYAPay represents the two dominant agent checkout stacks
- [[Procure AI]] — Potential integration partner: Procure AI's autonomous procurement agents need Skyfire-style payment execution rails to close the source-to-pay loop
- [[PCI DSS v4.0]] — Skyfire's card payment handling on Visa/Mastercard rails must comply with PCI DSS v4.0 (full enforcement from April 2025)
- [[FATF Guidance on AML/CFT]] — Skyfire's USDC/crypto rail exposure triggers FATF Travel Rule obligations for transactions above the $1,000 threshold

## Sources

1. [Introducing Skyfire: Payment Rails for AI](https://www.businesswire.com/news/home/20240821247203/en/Introducing-Skyfire-Payment-Rails-for-AI) — BusinessWire, Aug 2024
2. [Skyfire lets AI agents spend your money](https://techcrunch.com/2024/08/21/skyfire-lets-ai-agents-spend-your-money/) — TechCrunch, Aug 2024
3. [AI payment processing startup Skyfire launches with $8.5M in funding](https://siliconangle.com/2024/08/21/ai-payment-processing-startup-skyfire-launches-8-5m-funding/) — SiliconANGLE, Aug 2024
4. [AI Agents Race to Join Skyfire Payments Network](https://www.businesswire.com/news/home/20241024532897/en/AI-Agents-Race-to-Join-Skyfire-Payments-Network) — BusinessWire, Oct 2024
5. [Skyfire Exits Beta with Enterprise-Ready Payment Network for AI Agents](https://www.businesswire.com/news/home/20250306938250/en/Skyfire-Exits-Beta-with-Enterprise-Ready-Payment-Network-for-AI-Agents) — BusinessWire, Mar 2025
6. [Skyfire and Cequence Partner to Enable Secure, Autonomous Access for AI Agents](https://www.businesswire.com/news/home/20250422691031/en/Skyfire-and-Cequence-Partner-to-Enable-Secure-Autonomous-Access-for-AI-Agents) — BusinessWire, Apr 2025
7. [Skyfire Launches Open KYAPay Protocol With Agent Checkout](https://www.businesswire.com/news/home/20250626772489/en/Skyfire-Launches-Open-KYAPay-Protocol-With-Agent-Checkout) — BusinessWire, Jun 2025
8. [Skyfire Demonstrates Secure Agentic Commerce Purchase Using the KYAPay Protocol and Visa Intelligent Commerce](https://www.businesswire.com/news/home/20251218520399/en/Skyfire-Demonstrates-Secure-Agentic-Commerce-Purchase-Using-the-KYAPay-Protocol-and-Visa-Intelligent-Commerce) — BusinessWire, Dec 2025
9. [KYA & Payments for Agents — Skyfire.xyz Product Page](https://skyfire.xyz/product/) — Skyfire, accessed 2026-04-04
10. [Skyfire Launches: Identity and Payments for Autonomous AI Agents](https://skyfire.xyz/skyfire-launches-identity-and-payments-for-autonomous-ai-agents/) — Skyfire Blog, Aug 2024
11. [New Skyfire Solution Enables AI Agents to Authenticate Themselves as Genuine Paying Customers](https://thefintechtimes.com/new-skyfire-solution-enables-ai-agents-to-authenticate-themselves-as-genuine-paying-customers/) — Fintech Times, 2025
12. [AI Agents Now Have Their Own Credit Cards — Inside the Race to Build the Stripe for Autonomous Commerce](https://blockeden.xyz/blog/2026/03/16/crossmint-ai-agent-virtual-cards-autonomous-payments-kya-stripe-for-agents/) — BlockEden.xyz, Mar 2026 (competitive context — Crossmint comparison)
13. [Skyfire — 2026 Company Profile, Funding & Investors](https://tracxn.com/d/companies/skyfire/__-gSNwLdAbLR2EH3jQO5ja24BZ2dqjmKWC_BS3-4pf1s) — Tracxn, 2026

---
*Last updated: 2026-04-04*
