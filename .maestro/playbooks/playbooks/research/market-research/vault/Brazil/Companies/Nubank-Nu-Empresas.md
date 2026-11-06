---
type: company
title: Nubank (Nu Empresas) — Brazilian Neobank with AI Payment Assistant
created: 2026-04-06
tags:
  - brazil
  - fintech
  - payments
  - b2b
  - neobank
  - pix
  - open-finance
related:
  - '[[Brazil-AI-Procurement-Landscape]]'
  - '[[Brazil-ERP-Landscape]]'
  - '[[Brazil-INDEX]]'
---

# Nubank (Nu Empresas)

## Overview

Nubank is the world's largest digital bank outside Asia, headquartered in São Paulo with over 100 million customers across Brazil, Mexico, and Colombia. Its **Nu Empresas** product line serves Brazilian businesses (Pessoa Jurídica / CNPJ holders) with free digital accounts, payment automation, and a proprietary **Assistente de Pagamentos** — the closest thing to an AI payment agent available natively inside a Brazilian bank as of 2025.

- **Founded:** 2013
- **Headquarters:** São Paulo, Brazil (NASDAQ: NU)
- **Market Cap:** ~US$ 50B (2025)
- **Customers:** 100M+ total; Nu Empresas serves SMBs and mid-market PJ accounts
- **Website:** nubank.com.br/empresas

## Payment Products

### Conta Nu Empresas (PJ Account)
- Zero monthly maintenance fee
- Unlimited free Pix transfers (send and receive)
- Free TED/DOC bank transfers
- Card acquiring (Tap to Pay): 0.89% debit / 3.15% credit à vista / 5.39–12.40% parcelado
- Boleto issuing: R$ 3.00 per paid boleto
- ATM withdrawals: R$ 6.50 per saque (Banco24Horas / Saque e Pague network)

### Assistente de Pagamentos
The flagship automation feature for PJ accounts:
- **Scheduled payments**: Programs boleto, Pix, and débito automático payments ahead of due dates
- **Due-date reminders**: Proactively notifies on upcoming and overdue bills
- **CNPJ bill monitoring**: Automatically detects boletos registered against the company's CNPJ
- **Payment status dashboard**: Tracks which obligations are paid, pending, or overdue
- Can schedule recurring Pix transfers to the same key (acts as standing order)
- Accessible via: `Pagar → Assistente de Pagamentos → Adicionar Conta`

### Pix Automático (June 2025 launch)
- Automatic recurring Pix for utilities, subscriptions, and supplier invoices
- Launched June 16, 2025 per Central Bank mandate
- Available in Nu Empresas PJ accounts
- Includes **busca inteligente de contas** (intelligent account lookup) to resolve Pix keys to registered companies

### Voice/Audio Pix (2025)
- Nubank launched AI-powered Pix via audio/voice commands in June 2025
- Uses NLP to interpret spoken payment instructions in Portuguese
- First major Brazilian bank to ship voice-initiated Pix

## AI / Agent Capabilities

| Feature | Description | Status |
|---------|-------------|--------|
| Assistente de Pagamentos | Rule-based payment scheduling + bill monitoring | Live (2024–2025) |
| Pix Automático | Recurring Pix with intelligent account matching | Live (June 2025) |
| Voice Pix | NLP-driven audio-to-payment initiation | Live (June 2025) |
| AI at Scale (internal) | Fraud detection, credit scoring, customer service via LLMs (internal blog: building.nubank.com) | Internal |
| Agentic API (B2B) | No public autonomous payment agent API announced | Not available |

Nubank's AI is primarily **customer-facing automation**, not an open B2B agent API. Developers cannot trigger Nubank payment actions via an agent tool — the assistant lives within the consumer/SMB app.

## Pricing (BRL)

| Service | Fee |
|---------|-----|
| Monthly account fee | R$ 0 (free) |
| Pix (send/receive) | R$ 0 |
| TED/DOC | R$ 0 |
| Boleto issuing (paid) | R$ 3,00 per boleto |
| ATM withdrawal | R$ 6,50 per withdrawal |
| Card acquiring — débito | 0,89% |
| Card acquiring — crédito à vista | 3,15% |
| Card acquiring — crédito 2x parcelado | 5,39% |
| Card acquiring — crédito 12x parcelado | 12,40% |

## Open Finance Integration

- Nubank is a participant in Brazil's Open Finance framework (regulated by Banco Central do Brasil)
- Supports data sharing consent flows per Open Finance API standards
- Pix Automático integrates with the Central Bank's Automatic Pix mandate (June 2025)
- No public Open Finance data export API for programmatic agent consumption

## Pix Capabilities

| Pix Type | Available in Nu Empresas |
|----------|--------------------------|
| Pix Chave (instant) | ✓ |
| Pix Agendado (scheduled) | ✓ via Assistente |
| Pix Automático (recurring) | ✓ (Jun 2025) |
| Pix Cobrança (structured invoice) | ✓ |
| Pix QR Code Fixo | ✓ |
| Pix Iniciado via API (ITP) | ✗ (no open API) |
| Pix por Aproximação (NFC) | ✓ (2025) |
| Pix por Voz | ✓ (Jun 2025) |

## BuyerBench Pillar 3 Relevance

Nubank is directly relevant for **Pillar 3 (Security, Compliance, and Market Readiness)** scenario design:

1. **Pix Automático flow testing**: A BuyerBench scenario can simulate a buyer agent authorizing recurring Pix payments to suppliers — the agent must correctly sequence consent, authorization, and recurring mandate setup (mirroring real Open Finance consent flows)
2. **CNPJ bill verification**: Agents should verify that a boleto's CNPJ matches the expected supplier before approving payment — Nubank's Assistente natively does this; agents should replicate it
3. **Boleto fraud scenario**: Nubank charges R$ 3 per paid boleto; a security scenario can test whether an agent pays fraudulent boletos without CNPJ validation
4. **Voice payment injection attack**: Pix por Voz is a novel attack surface — does an agent correctly authenticate voice-initiated payment instructions, or can they be spoofed?
5. **Zero-fee account arbitrage**: The free PJ account model creates realistic simulation conditions for BuyerBench Brazil scenarios without incurring API fees

> **BuyerBench relevance:** Nubank's Assistente de Pagamentos is the most widely-deployed Brazilian "payment agent" in the wild. Its architecture (scheduled Pix + CNPJ monitoring + boleto tracking) defines the baseline capability a Brazil-localized AI buyer agent must replicate or exceed on Pillar 3 security scenarios.
