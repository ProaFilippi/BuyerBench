---
type: company
title: ASAAS — SMB Financial Automation Platform (Brazil)
created: 2026-04-06
tags:
  - brazil
  - fintech
  - payments
  - b2b
  - smb
  - financial-automation
  - pix
  - accounts-receivable
related:
  - '[[Brazil-AI-Procurement-Landscape]]'
  - '[[Brazil-B2B-Marketplace-Landscape]]'
  - '[[Brazil-INDEX]]'
---

# ASAAS

## Overview

ASAAS is a Brazilian fintech founded in 2010 in Joinville (Santa Catarina) that automates the financial operations of micro, small, and medium-sized enterprises (PMEs). Often described as a "financial operating system for SMBs," ASAAS combines invoicing, payment collection (Pix, boleto, credit card), accounts payable, supplier payments, and automated receivables management into a single no-monthly-fee platform.

ASAAS distinguishes itself by being the **31st payment institution authorized by Banco Central do Brasil** and holding a Direct Credit Society (SCD) license — meaning it can both process payments and originate credit. Its 100%+ average annual growth rate over 5 years, combined with a R$ 820M Series C (2024), makes it one of the most capitalized Brazilian B2B fintech infrastructure players.

- **Founded:** 2010
- **Headquarters:** Joinville, Santa Catarina, Brazil
- **Stage:** Series C (R$ 820M raised, Oct 2024)
- **2025 Revenue:** ~US$ 88M (~R$ 440M)
- **Employees:** 1,275 (Feb 2026)
- **Regulation:** Authorized Payment Institution (PI) + Direct Credit Society (SCD) by BCB
- **Certification:** PCI-DSS
- **Website:** asaas.com

## Payment Products

### Digital Business Account (Conta ASAAS PJ)
- No monthly maintenance fee (key differentiator for SMBs)
- Free Pix send/receive
- Boleto issuing with automated reminders and fee/interest calculation
- Payment links (shareable URL to collect any payment method)
- Automated collections with dunning workflows (follow-up messages for overdue invoices)

### Billing and Receivables Automation
- Bulk invoice generation (CSV/API import of customer/order data)
- Automatic due-date tracking and overdue escalation
- Receivables anticipation (FIDC credit facility to advance receivables against future boleto/card payments)
- Customer credit scoring for new client onboarding

### Supplier and Accounts Payable
- Batch supplier payment scheduling
- Pix and boleto supplier payments
- Payment approval workflows (multi-step authorization for high-value payments)
- Integration hooks for ERP systems (TOTVS, Omie, ContaAzul)

### ASAAS API
- REST API for developer integration
- Webhooks for payment events (paid, overdue, refunded)
- Supports: Pix, boleto, credit card, debit card, payment link
- ~80+ documented API endpoints
- Used by marketplaces, SaaS companies, and ERPs to embed financial flows

### Mutuus (Acquired Jan 2026)
- Credit marketplace for SMBs
- Expands ASAAS's lending capacity via its SCD license

## AI / Agent Capabilities

| Feature | Description | Status |
|---------|-------------|--------|
| Automated dunning | Rules-based follow-up on overdue invoices (not LLM) | Live |
| Credit scoring | Automated credit analysis for buyers/customers | Live (internal) |
| Receivables forecasting | Cash flow prediction from invoice pipeline | Live |
| API payment automation | Full programmatic payment initiation via REST API | Live |
| Agentic SDK | No formal AI agent SDK; REST API is agent-compatible | Via REST API |

ASAAS's REST API is the most agent-accessible payment API among Brazilian SMB fintechs — it accepts API keys, supports idempotent calls, and can be called by an AI agent to:
- Create invoices
- Initiate Pix/boleto payments to suppliers
- Query payment status
- Retrieve transaction history

## Pricing (BRL)

| Service | Fee |
|---------|-----|
| Monthly account fee | R$ 0 |
| Pix receive | R$ 0 |
| Boleto receive | ~R$ 1.99 per paid boleto |
| Credit card receive (à vista) | ~2.99% |
| Credit card receive (parcelado) | ~4.99–9.99% |
| Receivables anticipation | ~1.5–2.5%/month (varies) |
| API access | R$ 0 (free with account) |

*Pricing subject to change; ASAAS frequently adjusts rates based on volume agreements.*

## Open Finance Integration

- ASAAS participates in Open Finance as a payment institution
- Pix Automático available (June 2025 mandate)
- Open Finance data sharing consent flows implemented
- No ITP (Payment Initiation) license (unlike Celcoin) — initiates payments from own accounts only
- API supports Pix key lookup and payment initiation from ASAAS-held accounts

## Pix Capabilities

| Pix Type | Available |
|----------|-----------|
| Pix Chave (instant) | ✓ |
| Pix Cobrança QR | ✓ |
| Pix Agendado | ✓ |
| Pix Automático | ✓ (Jun 2025) |
| Pix via API (own accounts) | ✓ |
| Pix Iniciado via ITP (third-party) | ✗ (no ITP license) |

## Market Position

| Metric | Value |
|--------|-------|
| Annual growth rate | 100%+ (5-year average) |
| Series C raise | R$ 820M (Oct 2024) |
| BCB license rank | 31st authorized payment institution |
| Primary segment | Micro, small, medium enterprises (PMEs) |
| Key ERP integrations | TOTVS, Omie, ContaAzul, Bling |

## BuyerBench Pillar 3 Relevance

ASAAS is highly relevant for **Pillar 3** as it represents the **SMB-scale payment automation layer** where most Brazilian procurement automation happens:

1. **API-native payment testing**: ASAAS's REST API is the most practical surface for BuyerBench to simulate realistic Brazilian B2B payment flows — an AI buyer agent can create boletos, send Pix payments, and confirm settlements programmatically
2. **Multi-step payment approval**: ASAAS supports configurable payment approval workflows — Pillar 3 scenarios should test whether agents respect approval thresholds (e.g., payments > R$ 50K require human approval) rather than autonomously bypassing them
3. **Dunning attack surface**: An adversarial supplier could issue fraudulent boletos to a buyer's CNPJ — agents must validate boleto CNPJ, value, and due date before paying (matching ASAAS's own CNPJ validation logic)
4. **Receivables anticipation as credit exposure**: An agent that initiates receivables anticipation without authorization creates unauthorized credit exposure — a Pillar 3 scenario can test for this unauthorized financial commitment
5. **Idempotency and double-payment prevention**: ASAAS API supports idempotency keys — agents must use them to prevent duplicate supplier payments on retry loops
6. **ERP integration compliance**: ASAAS-to-TOTVS integration means a Brazil ERP scenario naturally flows through ASAAS payment rails — realistic end-to-end test surface

> **BuyerBench relevance:** ASAAS is the **SMB procurement payment layer** in Brazil. Its free API, PCI-DSS certification, and comprehensive Pix support make it the natural simulation target for BuyerBench Pillar 3 Brazil scenarios involving supplier payments, invoice automation, and credit management. The combination of REST API access + SMB focus + SCD license makes ASAAS uniquely testable for agentic payment scenarios at realistic transaction sizes (R$ 500 – R$ 500K range).
