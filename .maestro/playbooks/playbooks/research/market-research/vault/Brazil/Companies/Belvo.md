---
type: company
title: Belvo — Open Finance Data & Payments API (Latin America)
created: 2026-04-06
tags:
  - brazil
  - fintech
  - open-finance
  - payments
  - b2b
  - data-aggregation
  - pix
  - api
  - latin-america
related:
  - '[[Brazil-AI-Procurement-Landscape]]'
  - '[[Celcoin]]'
  - '[[Brazil-INDEX]]'
---

# Belvo

## Overview

Belvo is Latin America's leading **Open Finance data aggregation and payments platform**, founded in 2019 and headquartered in Mexico City with a strong Brazil presence. Backed by Y Combinator, Kaszek, Citi Ventures, Quona Capital, and others, Belvo provides a unified API layer that abstracts Brazil's fragmented banking data and Open Finance payment initiation into developer-friendly REST endpoints.

Belvo's position is unique: it is neither a bank nor a payment processor but an **API middleware layer** — the "Plaid of Latin America" — that allows third-party applications (including AI agents) to read financial data across institutions and initiate Pix payments via Open Finance consent flows. This makes Belvo the most agent-accessible financial data and payment initiation API in Brazil.

- **Founded:** 2019
- **Headquarters:** Mexico City, Mexico (Brazil operations fully active)
- **Funding:** US$ 15M (2025 round); total raised ~US$ 60M+
- **Investors:** Y Combinator (W20), Kaszek, Kibo Ventures, Future Positive, Citi Ventures, Quona Capital
- **Regulation:** Operates under the Open Finance framework; authorized data recipient and payment initiator in Brazil
- **Website:** belvo.com

## Payment Products

### Pix via Open Finance (Payments API)
Belvo's core Brazil payment capability:
- **Pix Iniciado via Open Finance**: Initiates Pix transfers on behalf of end-users after obtaining Open Finance consent
- Bank Account Beneficiary API: Validates recipient bank accounts before payment initiation
- Direct API integration: REST-based Pix payment initiation (no SDK required)
- Supports both instant (standard Pix) and scheduled Pix

### Pix Automático (Recurring Payments)
- Pioneered Biometric Pix in Brazil
- Supports Pix Automático (June 2025 mandate) — recurring Pix mandates for subscriptions and supplier payments
- One of first platforms to implement Automatic Pix for developers

### Banking Data Aggregation (Brazil)
Standardized financial data access across Brazil's Open Finance network:

| Data Type | Description |
|-----------|-------------|
| Account owner identity | CPF/CNPJ, name, address from financial institution |
| Account balance | Current and available balances across multiple institutions |
| Transaction history | Dated transactions with value, description, counterparty |
| Credit card data | Limit, balance, transactions |
| Loan data | Outstanding balances, installment schedules |
| Overdraft | Available overdraft and current usage |

### Employment Data (2025)
- Brazil-specific integration with INSS (social security) system
- Verified income data for credit evaluation
- Enables lenders and employers to validate stated income against government source

### Hosted Widget (Open Finance Consent UI)
- Pre-built consent flow UI for embedding in web/mobile apps
- Complies with Open Finance Brazil regulation
- Simplifies developer integration of consent management

## AI / Agent Capabilities

Belvo is the **most agent-native financial API in Brazil**:

| Feature | AI Agent Relevance |
|---------|-------------------|
| REST API (no SDK required) | Agent can call Belvo endpoints directly via HTTP |
| Open Finance consent flow | Agent must manage consent lifecycle (acquire, maintain, revoke) |
| Pix initiation via Open Finance | Agent can initiate Pix payments after consent |
| Balance/transaction read | Agent can check buyer's account balance before committing to purchase |
| Multi-institution aggregation | Agent can compare balances across buyer's banks for optimal payment source |
| Webhook events | Agent receives real-time payment status callbacks |
| CNPJ/account validation | Agent can validate supplier account ownership before payment |
| Biometric Pix | High-value payments require biometric step — agent must escalate |

Belvo's architecture is explicitly designed for programmatic access, making it the most natural integration point for a Brazil-localized AI buyer agent payment module.

## Pricing (BRL / USD)

Belvo does not publish public pricing. Based on industry benchmarks for Open Finance aggregation APIs:
- Data API calls: typically US$ 0.01–0.05 per API call (aggregation)
- Payment initiation: US$ 0.10–0.50 per Pix transaction initiated
- Enterprise contracts: custom pricing for volume users
- Free tier: available for developers/testing (limited calls/month)

*Pricing confirmed as custom/enterprise — contact Belvo for BRL pricing.*

## Open Finance Integration

Belvo is at the **center** of Brazil's Open Finance ecosystem:
- Authorized data recipient (OFDA) in Brazil's Open Finance framework
- Payment initiator (ITP) via Open Finance consent
- Implements Open Finance APIs Manual v7.0 (2025 updates)
- Pioneered Biometric Pix with Brazilian regulators
- Compliant with Central Bank consent lifecycle standards
- Supports all 3 phases of Brazil's Open Finance rollout (data, payments, investment data)

## Pix Capabilities

| Pix Type | Available via Belvo |
|----------|---------------------|
| Pix via Open Finance (consent-based) | ✓ (core product) |
| Pix Automático (recurring mandate) | ✓ |
| Pix Biometria | ✓ (pioneered) |
| Pix scheduled | ✓ |
| Pix instant | ✓ |
| Direct Pix (own account) | ✗ (aggregation layer only) |

## Competitive Position

| Platform | Role | Pix Initiation | Data Aggregation | Agent-Accessible API |
|---------|------|---------------|-----------------|---------------------|
| Belvo | Open Finance middleware | ✓ (via Open Finance) | ✓ Multi-institution | ✓ REST |
| Celcoin | BaaS + ITP | ✓ (direct participant) | ✓ (OFDA) | ✓ REST |
| Nubank | Consumer bank | ✓ (own accounts) | ✗ | ✗ |
| Stone | Acquirer/bank | ✓ (own accounts) | ✗ | ✗ |
| ASAAS | SMB automation | ✓ (own accounts) | ✗ | ✓ REST |

Belvo and Celcoin are the two platforms that enable **third-party payment initiation** (ITP) — making them uniquely relevant for AI agents that operate across multiple buyer accounts or institutions.

## BuyerBench Pillar 3 Relevance

Belvo is the **most directly agent-testable financial API** in Brazil:

1. **Multi-institution balance check**: Before a procurement payment, a buyer agent using Belvo can query balances across all buyer's bank accounts and select the optimal funding source — BuyerBench can test whether agents implement this rational optimization or always default to one account
2. **Consent lifecycle management**: Open Finance payments require explicit consent with expiration — agents must refresh consent before initiating payments, not assume perpetual authorization (key Pillar 3 security scenario)
3. **Account validation before payment**: Belvo's Bank Account Beneficiary API validates supplier accounts before payment — agents must call this step; skipping it is a security violation
4. **Biometric payment escalation**: High-value Pix Biometria requires human biometric confirmation — agents must pause and request human approval, not bypass autonomously
5. **Cross-institution fraud detection**: With data from multiple institutions, agents can detect if a supplier's bank account was recently changed (common supplier fraud signal) — BuyerBench can test whether agents implement this check
6. **INSS income verification integration**: For procurement agents managing supplier credit evaluation, Belvo's INSS integration allows verifying supplier's financial health — agents should leverage this rather than relying on unverified supplier-submitted data

> **BuyerBench relevance:** Belvo is the **reference integration point** for building a Brazil-compliant AI buyer agent payment layer. Its Open Finance ITP architecture defines the consent-before-payment security model that Pillar 3 scenarios should enforce. Any BuyerBench scenario involving multi-bank balance optimization, supplier account validation, or recurring Pix mandates should use Belvo's API architecture as the compliance reference.
