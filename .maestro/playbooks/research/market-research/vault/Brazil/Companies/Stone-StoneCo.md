---
type: company
title: Stone (StoneCo) — Payment Acquirer and B2B Financial Platform
created: 2026-04-06
tags:
  - brazil
  - fintech
  - payments
  - b2b
  - payment-acquirer
  - pix
  - conta-pj
related:
  - '[[Brazil-AI-Procurement-Landscape]]'
  - '[[Brazil-B2B-Marketplace-Landscape]]'
  - '[[Brazil-INDEX]]'
---

# Stone (StoneCo)

## Overview

Stone (officially StoneCo Ltd., NASDAQ: STNE) is Brazil's second-largest payment acquirer and one of the country's leading fintech companies. Founded in 2012 in Rio de Janeiro, Stone disrupted the duopoly of Cielo and Rede with SMB-friendly maquininhas (card terminals), transparent pricing, and 24/7 human support. By 2025 it had grown to ~14% merchant acquiring market share (vs. Cielo's ~60%), while expanding into banking (Conta Stone PJ), credit, ERP software (TOTVS competitor for SMBs via Linx), and financial management.

- **Founded:** 2012
- **Headquarters:** São Paulo, Brazil (originally Rio de Janeiro)
- **Listed:** NASDAQ: STNE
- **2025 Guidance:** Adjusted gross profit > R$ 7.05 billion; ≥14% YoY growth
- **Website:** stone.com.br

## Payment Products

### Conta Stone PJ
A free digital business account integrated with Stone's acquiring infrastructure:
- Zero monthly maintenance fee
- Integrated with card terminal revenue flows
- Pix (send, receive, QR codes, scheduled)
- Boleto issuing
- Supplier and bill payments
- Expense management and financial reporting
- 24/7 human customer support (differentiating feature vs. purely digital banks)

### Stone Card Acquiring
- Card terminals (Maquininha Stone) for in-person and mobile payments
- POS terminal rental-free options for qualifying merchants
- Integrated with Conta Stone for same-day settlement
- Pix via QR code directly from terminal

### Ton (Sub-Brand for Micro-Entrepreneurs)
- Simplified acquiring platform for microempreendedores individuais (MEI) and autonomous sellers
- Lower-cost card machines with competitive rates
- Virtual customer service 24/7 (AI-assisted customer support via chatbot)
- Mobile app as primary interface

### Linx (Acquired 2021)
- Brazil's largest retail management software company (acquired by Stone for ~US$1.1B)
- ERPs for retail, restaurants, pharma, and auto sectors
- Integrates payment flows directly with Stone acquiring

## AI / Agent Capabilities

| Feature | Description | Status |
|---------|-------------|--------|
| Ton virtual support | AI-assisted customer service chatbot for Ton micro-merchants | Live |
| Financial management analytics | Predictive cash flow insights in Conta Stone app | Live |
| Credit scoring | Automated credit analysis for Stone Capital loans | Internal |
| AI for fraud | Real-time fraud detection on acquiring network | Internal |
| Agentic B2B payment API | No public autonomous payment agent API | Not available |

Stone's AI is focused on **operational efficiency and customer service**, not an open agentic payment API for developers. Its 2025 earnings announcement mentioned previewing AI news — specifics not yet public.

## Pricing (BRL)

| Service | Fee |
|---------|-----|
| Conta Stone monthly fee | R$ 0 (free) |
| Pix (send/receive) | R$ 0 |
| Boleto issuing | Fee varies (typically R$ 1–4 per paid boleto) |
| Card acquiring — débito | ~0.99–1.49% (varies by volume) |
| Card acquiring — crédito à vista | ~2.69–3.49% |
| Card acquiring — crédito parcelado | ~3.99–5.99% (2–12x) |
| Ton machines | From R$ 0/month for qualifying micro-merchants |

*Note: Stone does not publicly post exact current acquiring rates — they are negotiated based on volume and business type.*

## Open Finance Integration

- Stone participates in Brazil's Open Finance framework as a payment institution regulated by Banco Central
- Supports Pix as a direct participant
- Pix Automático available (June 2025 mandate)
- No open developer API for third-party agent-initiated payments via Stone accounts (as of 2026)

## Pix Capabilities

| Pix Type | Available |
|----------|-----------|
| Pix Chave (instant transfer) | ✓ |
| Pix Cobrança (structured QR invoice) | ✓ |
| Pix Agendado (scheduled) | ✓ |
| Pix Automático (recurring) | ✓ (Jun 2025) |
| Pix QR Code (terminal) | ✓ |
| Pix por Aproximação (NFC) | ✓ (Maquininha Stone) |
| Pix Iniciado via API (ITP) | ✗ (no open third-party API) |

## Market Position

| Metric | Value |
|--------|-------|
| Acquiring market share | ~14% (2025) |
| Cielo market share | ~60% (2025) |
| Rede market share | ~25% (2025) |
| TOTVS partnership | Linx integration covers retail ERP |
| 2025 headcount | ~20,000 employees |

## BuyerBench Pillar 3 Relevance

Stone is relevant for **Pillar 3** security and compliance scenario design:

1. **Payment acquirer API simulation**: Stone's acquiring flows (authorization → capture → settlement) map directly to BuyerBench's secure transaction flow scenarios (correct sequencing and authorization checks)
2. **Multi-entity payment routing**: Scenarios where a buyer agent pays via Pix to a Stone-registered merchant should verify CNPJ matching and acquire correct NF-e receipts
3. **Fraud detection baseline**: Stone processes billions of BRL monthly; its fraud detection heuristics (velocity checks, CNPJ verification, amount anomalies) inform realistic Pillar 3 adversarial scenarios
4. **PJ account separation**: A compliance scenario can test whether an AI buyer agent correctly routes payments through the Conta PJ (not PF) account, respecting Brazilian regulatory separation of business and personal finances
5. **Linx/ERP integration**: Stone's Linx ERP creates a realistic end-to-end procurement scenario: purchase order → Linx ERP → Stone payment → Nota Fiscal issuance

> **BuyerBench relevance:** Stone represents the acquirer layer of Brazil's payment stack. Pillar 3 scenarios testing payment authorization, fraud rejection, and supplier verification should model Stone-style acquiring flows — including the 2-step "authorization + capture" pattern and settlement timing expectations (D+1 for credit, instant for Pix).
