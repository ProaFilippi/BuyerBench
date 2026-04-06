---
type: product
title: Compras.gov.br / PNCP — Brazilian Federal Procurement Portal
created: 2026-04-06
tags:
  - brazil
  - b2b-marketplace
  - procurement
  - government
  - public-sector
  - licitações
related:
  - '[[Brazil-AI-Procurement-Landscape]]'
  - '[[INDEX]]'
---

# Compras.gov.br / PNCP

## Overview

**Compras.gov.br** is the Brazilian federal government's integrated procurement ecosystem, administered by the Ministry of Management and Innovation in Public Services (MGI). Originally launched as **Comprasnet**, it was rebranded and relaunched as Compras.gov.br to align with the **New Procurement Law (Lei 14.133/2021)**, which completed five years of effectiveness in April 2026. It is one of the largest public procurement platforms in the world by transaction volume.

**Portal Nacional de Contratações Públicas (PNCP)** is the centralized publication hub mandated by Law 14.133/2021, where all public agencies must publish notices, bids, contracts, and amendments — replacing fragmented state- and municipal-level portals.

**Operator:** Brazilian Federal Government (MGI / SERPRO)  
**Legislation:** Lei 14.133/2021 (New Procurement Law)  
**Platform maturity:** Operational since 2000s (Comprasnet era); Compras.gov.br relaunch 2021–2025  
**Scope:** Federal, state (São Paulo via compras.sp.gov.br), and municipal procurement  
**Access:** Free — open to all registered CNPJ entities as suppliers

## Key Capabilities

### Compras.gov.br (Buyer-Side)
- **Integrated procurement lifecycle**: planning, bidding (pregão eletrônico), contracting, execution, and payments.
- **SICAF (Supplier Registration System)**: Centralized supplier registry with automatic CNPJ validation, certificate verification (tax clearances, INSS, FGTS, labor court).
- **Pregão Eletrônico (e-Auction)**: Reverse auction format — suppliers compete by lowering prices in real-time; dominant modality for commodity goods.
- **Ata de Registro de Preços (Price Registration Record)**: Framework agreements that allow multiple agencies to buy at pre-negotiated prices without running a new tender.
- **Compras.gov.br App**: Mobile application for supplier participation in bids, developed in partnership with SEBRAE.
- **Painel de Compras**: Public analytics dashboard with spend data across all federal agencies (updated through July 2025).

### PNCP (Publication Hub)
- Central registry for all public procurement notices in Brazil (all three levels of government under Law 14.133/2021).
- REST API available for programmatic access to contracts, bids, and supplier data.
- Replaces the need for suppliers and platforms to monitor dozens of independent portals.

## Market Share

| Metric | Value |
|---|---|
| Annual government procurement volume (Brazil) | ~R$ 100–150B/year (federal level) |
| Agencies registered on Compras.gov.br | All federal agencies (~2,500+) |
| Supplier registrations (SICAF) | Hundreds of thousands of CNPJs |
| Law coverage | Mandatory for all federal agencies since 2023; states transitioning |

Brazil's public sector represents the single largest institutional buyer in the country. Any AI buyer agent targeting institutional/enterprise procurement must interface with Compras.gov.br and PNCP APIs.

## Pricing in BRL

- **Supplier registration (SICAF):** Free.
- **Bid participation:** Free for suppliers.
- **Private-sector e-procurement platforms** that integrate with PNCP (e.g., Portal de Compras Públicas, ComprasBR) charge suppliers for enhanced monitoring features: approximately R$ 99–499/month for full-alert coverage.

## AI / Agent Features

The platform itself has no native AI agent capabilities as of April 2026. However:
- PNCP's public REST API exposes structured bid and contract data — a natural tool-use target for AI procurement agents.
- Third-party platforms (e.g., Nomos for legislative monitoring, Portal de Compras Públicas for bid alerts) layer AI summarization and compliance checking on top of PNCP data.
- The market opportunity for an AI buyer agent that monitors PNCP, qualifies suppliers, and auto-submits competitive bids is significant and largely unaddressed.

## BuyerBench Scenario Relevance

| Pillar | Scenario Design Opportunity |
|---|---|
| **Pillar 1** | Agent must query PNCP API to discover active bids matching a procurement specification, validate supplier eligibility via SICAF, and prepare a bid response — testing supplier discovery and workflow execution in a government context. |
| **Pillar 2** | Pregão eletrônico reverse-auction dynamics: test whether agent overbids under scarcity pressure or anchors to the opening price rather than calculating true economic optimum. |
| **Pillar 3** | SICAF compliance verification: agent must confirm tax clearance certificates (CND, FGTS, INSS) are valid and not expired before proceeding. Test rejection of suppliers with irregular tax status. |

**Key Brazil-specific compliance hook:** Government suppliers in Brazil must maintain continuous SICAF regularity — all tax certificates must be valid at the time of contracting. An AI agent that fails to verify certificate expiration dates will generate legally void contracts, a critical Pillar 3 failure mode.
