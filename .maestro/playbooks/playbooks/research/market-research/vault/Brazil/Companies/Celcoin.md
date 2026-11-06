---
type: company
title: Celcoin — Open Finance BaaS Infrastructure (Brazil)
created: 2026-04-06
tags:
  - brazil
  - fintech
  - payments
  - b2b
  - baas
  - open-finance
  - pix
  - infrastructure
related:
  - '[[Brazil-AI-Procurement-Landscape]]'
  - '[[Brazil-ERP-Landscape]]'
  - '[[Brazil-INDEX]]'
---

# Celcoin

## Overview

Celcoin is Brazil's leading **Banking-as-a-Service (BaaS)** and Open Finance infrastructure provider. Unlike consumer fintechs (Nubank, Stone), Celcoin is a **B2B platform company**: it provides regulated financial infrastructure — Pix, Open Finance APIs, payment initiation, card issuing, credit, and account services — to banks, fintechs, enterprises, and non-regulated companies that want to embed financial products.

Celcoin operates as a **Direct Pix Participant** (Participante Direto do Pix) and an **ITP (Iniciador de Transação de Pagamento)** — meaning it can both hold accounts and initiate payments on behalf of third parties, making it the closest Brazilian equivalent to a "payment orchestration layer" for autonomous agents.

- **Founded:** 2016
- **Headquarters:** São Paulo, Brazil
- **Clients:** 6,000+ banks, fintechs, and enterprises
- **Monthly volume:** R$ 30 billion+ in transactions; 400M+ transactions/month
- **Regulation:** Authorized by Banco Central do Brasil as Payment Institution (IP) and ITP
- **Website:** celcoin.com.br

## Payment Products

### cel_banking (BaaS Core)
- White-label digital account infrastructure
- Bank liquidation services
- Pix direct participation (hold accounts, initiate transfers)
- Credit products
- Card issuing (white-label)
- Data sharing (Open Finance consent flows)

### Open Finance API Suite (~80 endpoints)
Complete Open Finance-compliant API coverage:

| Product | Description |
|---------|-------------|
| Pix Inteligente | Intelligent Pix routing with fallback logic |
| Pix Automático | Recurring Pix mandate setup and execution (Jun 2025) |
| Pix por Aproximação | NFC proximity Pix |
| Pix Biometria | Biometric-authenticated Pix (pioneered in Brazil) |
| Pix Recorrente | Subscription/standing order Pix |
| ITP — Iniciação de Pagamento | Third-party payment initiation via Open Finance consent |
| Financial Data (OFDA) | Account balances, transactions, credit card data, loans |
| Cadastro Expresso | Rapid KYC/onboarding via Open Finance data |
| Detentora de Conta | Account holding and management services |
| IPVA/Multas API | Government fee payment (vehicle tax, traffic fines) |

### Open Finance ITP (Payment Initiation)
Celcoin's ITP capability is the key differentiator for AI agent integration:
- Authorized by Banco Central to initiate payments on behalf of users via Open Finance consent
- Supports Pix via Open Finance (not just direct Pix key transfers)
- Regulatory compliance: implements Central Bank Normative Instruction No. 615 / Open Finance APIs Manual v7.0 (2025)
- Enables third-party apps (including potential AI agents) to initiate Pix payments after user consent

## AI / Agent Capabilities

Celcoin does not market AI agent products publicly. However, its infrastructure is the **natural foundation layer for autonomous payment agents** in Brazil:

| Capability | AI Agent Relevance |
|------------|-------------------|
| ITP API | Agent can initiate Pix payments after obtaining Open Finance consent from buyer |
| Pix Automático API | Agent can schedule recurring supplier payments without per-transaction human approval |
| Financial Data API | Agent can read bank account balance, transaction history, and credit exposure for decision-making |
| Biometric Pix | Agent authentication can integrate biometric step for high-value payments |
| ~80 payment endpoints | Covers full procure-to-pay lifecycle: account lookup → payment initiation → status polling → reconciliation |

No public AI agent SDK or autonomous payment framework from Celcoin as of 2026. The API is designed for **human-authorized, developer-integrated flows** — adapting it for fully autonomous agents requires implementing consent management on top.

## Pricing (BRL)

Celcoin does not publish public pricing. Pricing is negotiated B2B based on:
- Monthly transaction volume
- Product mix (BaaS core, ITP, data APIs)
- Client type (bank, fintech, enterprise)

Typical BaaS pricing in Brazil ranges from R$ 0.05–0.50 per transaction for Pix, with monthly platform minimums for regulated license access. No public rack rates confirmed.

## Open Finance Integration

Celcoin is a **central player** in Brazil's Open Finance ecosystem:
- Participante Direto do Pix — holds accounts and settles directly with BCB
- ITP-authorized — initiates payments via Open Finance consent flows
- OFDA (Open Finance Data Aggregator) — accesses financial data across participating institutions
- Implements Open Finance APIs v7.0 (2025 mandate)
- Processes R$ 4B+/month in Pix transactions alone (prior 2024 figure; current volume higher)
- 6,000+ clients means broad coverage of Brazil's financial ecosystem

## Pix Capabilities

| Pix Type | Available via Celcoin API |
|----------|--------------------------|
| Pix Chave (instant) | ✓ |
| Pix Cobrança QR (invoice) | ✓ |
| Pix Agendado | ✓ |
| Pix Automático (recurring) | ✓ (Jun 2025) |
| Pix Iniciado via ITP (Open Finance) | ✓ (authorized by BCB) |
| Pix Biometria | ✓ (pioneered) |
| Pix por Aproximação | ✓ |
| Pix Inteligente (smart routing) | ✓ |

## Regulatory Status

| License | Status |
|---------|--------|
| Payment Institution (IP) | Authorized by BCB |
| ITP (Iniciador de Transação de Pagamento) | Authorized by BCB (Dec 2023) |
| Open Finance OFDA | Active participant |
| PCI-DSS | Certified |
| LGPD | Compliant data handling |

## BuyerBench Pillar 3 Relevance

Celcoin is the **highest-relevance infrastructure player** for Pillar 3 scenario design:

1. **ITP consent flow scenario**: A buyer agent using Celcoin's ITP must first obtain Open Finance consent from the buyer before initiating any payment — BuyerBench should test whether agents correctly implement the consent step before payment initiation (not bypassing it)
2. **Pix Automático authorization**: Recurring supplier payments via Pix Automático require explicit mandate setup — scenarios should verify agents request and store mandates rather than re-authorizing each payment
3. **Biometric step enforcement**: High-value Pix Biometria transactions require biometric authentication — agents must escalate to human approval rather than bypassing this step autonomously
4. **Financial data access**: Celcoin's OFDA APIs give agents read access to real-time account balances — Pillar 3 should test whether agents query balance before committing to large purchases (preventing overdraft/credit abuse)
5. **ITP rate limiting and CNPJ matching**: Celcoin's 80-endpoint API has rate limits and CNPJ verification steps — realistic Pillar 3 scenarios should model these constraints
6. **~80 endpoint coverage**: Full procure-to-pay cycle testable: discover supplier bank key → initiate Pix → poll status → confirm NF-e receipt → reconcile

> **BuyerBench relevance:** Celcoin represents the **infrastructure layer** that would power any serious Brazil-localized AI buyer agent. Its ITP + Pix Automático + OFDA capabilities define the technical requirements for a compliant autonomous procurement payment flow. BuyerBench Pillar 3 scenarios should model the Celcoin consent/authorization architecture as the reference compliance model for Brazilian B2B payment agents.
