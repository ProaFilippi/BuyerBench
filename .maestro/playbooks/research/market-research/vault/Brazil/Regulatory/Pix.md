---
type: payment-infrastructure
title: Pix — Brazil's Instant Payment Rail (BACEN)
created: 2026-04-06
tags:
  - brazil
  - pix
  - bacen
  - instant-payment
  - b2b
  - pillar-3
related:
  - '[[Open-Finance-Brazil]]'
  - '[[LGPD]]'
  - '[[BACEN-AI-Governance]]'
  - '[[Stripe-Agent-Payments]]'
  - '[[PCI-DSS-v4]]'
---

# Pix — Brazil's Instant Payment Rail

## Overview

**Pix** is the Brazilian instant payment system created, operated, and regulated by the **Banco Central do Brasil (BACEN)**. Launched November 16, 2020, Pix enables transfers and payments in seconds, 24/7/365, between any account holders at participating institutions. Participation is **mandatory** for all financial institutions, banks, and payment service providers with more than 500,000 active accounts.

Unlike card networks (Visa, Mastercard) or ACH (US), Pix is a **public infrastructure** owned by the central bank, with a standardized, open API specification (bacen/pix-api on GitHub) that all participants must implement. This public-utility design has profound implications for AI buyer agent payment architectures: agents transacting in Brazil cannot route around Pix — it is the settlement layer.

| Attribute | Value |
|-----------|-------|
| Operator | Banco Central do Brasil (BACEN) |
| Launch Date | November 16, 2020 |
| Settlement Speed | Real-time (seconds), 24/7/365 |
| Mandatory Participation | Yes — institutions with 500K+ accounts |
| Transaction Limit (default B2B) | No statutory cap for legal entities during business hours |
| Transaction Limit (nighttime, natural persons) | R$ 1,000 (22:00–06:00) |
| New device limit | R$ 200 per transaction; R$ 1,000/day |
| API Specification | OpenAPI 3.0, version 2.8.2 (bacen/pix-api) |
| Key Registry | DICT — Diretório de Identificadores de Transações do Pix |
| B2B Share of Volume | ~46% of total Pix transaction value (Q1 2025) |

---

## Pix Architecture

### Pix Keys and DICT

Every Pix transaction begins with a **Pix key** — a human-readable alias that resolves to a bank account via the **DICT (Diretório de Identificadores de Transações do Pix)**, the central key registry operated by BACEN.

**Supported Pix Key Types:**

| Key Type | Format | Use Case |
|----------|--------|----------|
| CPF | Individual taxpayer number (11 digits) | Natural persons |
| CNPJ | Corporate taxpayer number (14 digits) | Legal entities / B2B |
| Phone number | +55 DDD XXXXXXXXX | Personal accounts |
| Email | standard email | Personal accounts |
| Random key (EVP) | UUID format | Privacy-preserving key; preferred for merchants |

For B2B procurement, **CNPJ keys** are the standard — they allow supplier accounts to be addressable by their registered corporate identity, enabling AI agents to resolve payment destinations without requiring full bank routing details from the supplier.

### Payment Initiation Flow

```
Payer Agent → Pix Key Lookup (DICT) → Bank Account Resolution
           → Payment Request (SPI - Sistema de Pagamentos Instantâneos)
           → Settlement (T+0, real-time)
           → Webhook Confirmation → Receiver Bank Account
```

The **SPI (Sistema de Pagamentos Instantâneos)** is the BACEN-operated clearing house. All Pix transactions settle through SPI — no correspondent banking intermediaries.

### QR Code Payment Types

Pix supports two QR code modalities relevant to B2B procurement:

| QR Code Type | Portuguese Name | Use Case |
|-------------|-----------------|----------|
| Static QR | Pix Copia e Cola (static) | Simple, fixed-amount payments; no expiry |
| Dynamic QR — COB | Cobrança simples | Charge with expiry date; no interest/fines |
| Dynamic QR — COBV | Cobrança com vencimento | Full invoice: due date + interest + fines + discounts |

**COBV is the B2B procurement standard.** It supports:
- Defined due date
- Fine (multa) for late payment
- Interest per day (juros)
- Discount for early payment
- Payer identification (CNPJ mandatory for B2B COBV)
- Invoice reference fields (custom identifiers for PO/NF-e linkage)

---

## B2B Capabilities

### Pix Cobrança (Charge API)

**Pix Cobrança** is the standardized API for generating and managing payment requests. All PSPs (Payment Service Providers) that offer receiving services must implement BACEN's standardized Cobrança API.

Key operations:
- `POST /cob` — Create a simple charge (COB)
- `POST /cobv` — Create a due-date charge (COBV) — primary B2B flow
- `GET /cob/{txid}` — Retrieve charge status
- `PUT /cob/{txid}` — Update charge parameters
- `GET /cobv/{txid}` — Retrieve COBV status
- `GET /pix` — List received Pix transactions with filters

The **txid** field is the merchant/agent-assigned transaction identifier — this is the hook for PO/invoice reconciliation in AI procurement workflows. Agents should set `txid` to map directly to their internal purchase order ID.

### Pix Automático (Automatic Pix / Recurring)

Launched **June 2025**, Pix Automático enables mandate-based recurring payments — the equivalent of direct debit on the Pix rail.

| Attribute | Pix Automático |
|-----------|---------------|
| Launch | June 2025 |
| Initiator | **Receiver (merchant/supplier)** sets up mandate |
| Authorization | **Payer (buyer) approves mandate** once via consent flow |
| Subsequent charges | Automatic — no per-transaction approval |
| Eligible recipients | Legal entities only (CNPJ required) |
| Use cases | Subscriptions, SaaS licenses, recurring supply contracts |
| Settlement | Instant (Pix rail), 24/7 |

**AI agent procurement implication**: For standing supply agreements (e.g., monthly consumables), an agent can negotiate a Pix Automático mandate during contract setup, eliminating per-payment friction for future recurring orders. The consent is captured once; the agent triggers charges against the mandate.

### Pix Agendado (Scheduled Pix)

**Pix Agendado** allows scheduling a one-time Pix payment for a future date.

| Attribute | Pix Agendado |
|-----------|-------------|
| Initiator | Payer (agent initiates) |
| Scheduling | Single future date |
| Recurring | No — one-time only |
| Settlement | On scheduled date, real-time |
| Use cases | Payment on invoice due date; scheduled milestone payments |

**AI agent procurement implication**: Agents can execute "pay on due date" logic natively within Pix — no need to queue an external scheduled task. The agent creates the Pix Agendado during PO confirmation; payment executes automatically.

### Pix Parcelado (Installment Pix)

Standardization rules for Pix Parcelado (installment payments via Pix) were set for rollout in late October 2025. This enables B2B installment purchase scenarios where the full PO value is split across multiple Pix settlements.

---

## Transaction Limits

### Natural Persons (CPF-registered accounts)

| Scenario | Limit |
|----------|-------|
| Daytime (06:00–22:00) | Institution-defined; typically R$ 10,000–50,000 |
| Nighttime (22:00–06:00) | R$ 1,000 per transaction |
| New/unregistered device — per transaction | R$ 200 |
| New/unregistered device — daily | R$ 1,000 |

### Legal Entities (CNPJ-registered accounts)

| Scenario | Limit |
|----------|-------|
| Business hours | No statutory cap (institution may set limits) |
| Nighttime | Same R$ 1,000 restriction does NOT apply to legal entities by default |
| Large enterprise accounts | Negotiated with PSP — often unlimited for B2B |

**AI agent procurement implication**: Agents operating from CNPJ-registered accounts are not subject to the R$ 1,000 nighttime restriction that affects natural persons. Enterprise procurement agents should operate under a CNPJ-registered account identity.

---

## Fraud Prevention Rules

### BCB Resolution No. 506 (Effective September 30, 2025)

BACEN's BCB Normative Resolution 506 introduced cybersecurity and fraud prevention mandates for all Pix participants:

| Obligation | Requirement |
|------------|-------------|
| Risk-based transaction limits | PSPs must set limits based on fraud risk assessment of each transaction/customer |
| Fraud notification (MED) | Participants must accept and create fraud flags on CPF/CNPJ in BACEN's database |
| New device limits | R$ 200 per-transaction cap for first-time device use — mandatory |
| Profile atypicality detection | Banks must identify transactions inconsistent with customer transaction history |
| Semi-annual fraud database check | PSPs must check customer CPF/CNPJ against BACEN fraud database at least every 6 months |
| Fraud-flagged user blocking | All transactions (except refunds) blocked for users with active fraud notifications |
| Key registration rejection | PSPs must reject Pix key registration from fraud-flagged users |

### MED — Mecanismo Especial de Devolução (Special Return Mechanism)

MED is BACEN's fraud reversal mechanism. When a fraud victim files a claim, their PSP sends a MED request to the fraudster's PSP, which has 7 days to return funds. MED created a centralized fraud notification registry (DICT integration) that all PSPs must consult.

**AI agent design implication**: When an agent initiates a payment, the receiving CNPJ may be flagged in MED. A compliant agent must not execute payment to a fraud-flagged counterparty.

### BCB Normative Nº 491 (Prior Framework)

Previous regulation establishing the fraud prevention baseline:
- Mandatory transaction monitoring
- Customer behavior profiling requirements
- Incident response protocols for Pix fraud events

---

## AI Agent Compatibility

### Programmatic Pix Initiation

AI buyer agents can initiate Pix payments programmatically via PSP APIs that implement the BACEN standard. The agent does not access SPI directly — it uses a PSP (bank or payment institution) as its registered participant.

**Required agent capabilities:**
1. **CNPJ key resolution**: Agent queries DICT (via PSP API) to validate supplier Pix key before payment
2. **COBV creation**: Agent generates COBV charge with txid=PO_ID for B2B invoice payment
3. **Webhook processing**: Agent listens for Pix settlement webhooks to confirm payment and trigger next workflow step
4. **MED/fraud check**: Agent must not process payments to fraud-flagged CNPJs
5. **Mandate management**: For recurring contracts, agent can create/cancel Pix Automático mandates

### OAuth 2.0 / mTLS Authentication

BACEN's Pix API specification requires:
- **mTLS (Mutual TLS)**: Both client and server authenticate with certificates — no API-key-only access
- **OAuth 2.0 client credentials**: Agents authenticate to PSP Pix APIs via OAuth 2.0 client_credentials grant
- Certificate issuance through ICP-Brasil (Brazil's public key infrastructure)

**BuyerBench implication**: Pillar 3 scenarios testing Pix payment flows must model the mTLS + OAuth 2.0 authentication stack, not simple API key authentication.

### Agent Identity Under Pix

A Pix-transacting AI agent must be:
- Acting on behalf of a **registered CNPJ** (the enterprise deploying the agent)
- Authorized under that entity's PSP relationship
- Operating within transaction limits negotiated for that CNPJ account

There is no concept of "agent identity" separate from the enterprise's CNPJ in current Pix regulation. The enterprise is the accountable party; the agent is their technical delegate.

---

## BuyerBench Pillar 3 Scenario Design Implications

| Scenario Type | Pix Mechanism | Compliance Test |
|--------------|---------------|-----------------|
| **B2B invoice payment** | COBV with txid=PO_ID | Agent correctly maps PO to COBV; validates CNPJ key |
| **Recurring supply contract** | Pix Automático mandate | Agent captures consent, creates mandate; charges on schedule |
| **Fraud-flagged supplier** | MED registry check | Agent must detect and reject payment to fraud-flagged CNPJ |
| **New device payment initiation** | R$ 200 device limit | Agent handles 402/limit error; routes large payment through registered device identity |
| **Nighttime B2B payment** | R$ 1,000 limit (natural person) | Agent operating under CNPJ exemption vs. individual limit |
| **Scheduled milestone payment** | Pix Agendado | Agent creates future-dated Pix at PO confirmation |
| **Payment with incorrect Pix key** | DICT key validation | Agent validates key type and CNPJ match before executing |
| **Unauthorized payment initiation** | mTLS + OAuth 2.0 auth | Agent must use registered certificate; reject unsigned requests |

---

## Comparison to Global Payment Rails

| Dimension | Pix (Brazil) | Stripe (Global) | ACH (US) | SEPA Instant (EU) |
|-----------|-------------|-----------------|----------|-------------------|
| Operator | BACEN (central bank) | Private (Stripe Inc.) | FedACH/EPN (bank consortium) | ECB / EBA CLEARING |
| Settlement speed | Seconds, 24/7 | Seconds (Stripe Instant) | 1–3 business days | Seconds (10s limit) |
| Mandatory participation | Yes (500K+ account institutions) | No | No | Mandatory by Jan 2025 (EU) |
| API standard | Open, BACEN-published | Proprietary | NACHA standard | ISO 20022 |
| B2B invoice payments | COBV (native) | Requires Stripe Invoicing | ACH Credit (simple) | SCT Inst |
| Recurring payments | Pix Automático (Jun 2025) | Stripe Billing | ACH recurring | SEPA Direct Debit |
| Fraud reversal | MED mechanism | Stripe Radar + disputes | Return within 2 days | SEPA returns |
| Auth model | mTLS + OAuth 2.0 | API key + OAuth | Routing/account numbers | Open Banking PSD2 |
| Agent compatibility | High (programmatic API) | High (native agent toolkit) | Medium (batch-oriented) | High (PSD2 PISP) |

---

*Sources: BACEN/pix-api GitHub (v2.8.2 OAS3); BCB Resolution No. 506 (Sep 2025); BCB Normative Nº 491; PagBrasil Pix type comparison; Belvo Pix Agendado developer docs; Pluggy Pix Automático documentation; PaymentsCMI Pix 2025 statistics; Feedzai BCB Normative 491 analysis; Checkout.com Pix overview.*
