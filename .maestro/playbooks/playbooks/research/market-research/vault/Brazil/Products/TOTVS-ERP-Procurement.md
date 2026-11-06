---
type: product
title: TOTVS ERP — Procurement & Fluig Voyager 2.0
created: 2026-04-06
tags:
  - brazil
  - erp
  - procurement
  - ai-automation
  - workflow
  - b2b-marketplace
related:
  - '[[Brazil-AI-Procurement-Landscape]]'
  - '[[Brazil-ERP-Landscape]]'
  - '[[INDEX]]'
---

# TOTVS ERP — Procurement & Fluig Voyager 2.0

## Overview

TOTVS S.A. (B3: TOTS3) is Brazil's dominant ERP vendor with approximately 50% market share in the Brazilian mid-market. Founded in 1983 and headquartered in São Paulo, TOTVS serves 70,000+ companies across retail, manufacturing, agribusiness, healthcare, education, and services. Its procurement capability is delivered through two main product lines: the **TOTVS ERP** (core purchasing/supply chain module) and **TOTVS Fluig** (process and document management platform), with the **Fluig Voyager 2.0** release (September 2025) adding generative AI capabilities.

**Headquarters:** São Paulo, Brazil  
**Listed:** B3 (São Paulo Stock Exchange), ticker TOTS3  
**Revenue:** R$ ~4.5B ARR (2025 estimate)  
**Clients:** 70,000+ companies  
**R&D investment (5 years):** R$ 1.14 billion  
**SaaS growth:** 18% YoY (2025)

## Key Capabilities

### TOTVS ERP — Procurement Module
- Full procure-to-pay (P2P) cycle: requisition → RFQ → purchase order → goods receipt → invoice matching → payment.
- Multi-entity and multi-currency support; Brazilian tax calculation engine (ICMS, IPI, PIS/COFINS) built in.
- Supplier portal for CNPJ validation, certificate tracking, and document management.
- Integration with Nota Fiscal Eletrônica (NF-e) issuance and SEFAZ (Secretaria da Fazenda) validation.
- Supplier evaluation and performance scoring dashboards.
- Native Pix and boleto payment disbursement modules.

### TOTVS Fluig Voyager 2.0 (September 2025)
Fluig is TOTVS's process management and low-code platform (BPM + DMS + collaboration). Voyager 2.0 introduces:
- **Natural language workflow builder**: Users describe a procurement process in Portuguese; generative AI generates the Fluig workflow and form structure.
- **AI assistant for document review**: Automated extraction and validation of supplier documents, certifications, and compliance artifacts.
- **Predictive escalation**: ML-based detection of approval bottlenecks and SLA breaches.
- **Integration hub**: 200+ connectors including SAP, Oracle, Salesforce, and Mercado Livre APIs.
- **Conversational AI for requisitions**: Employees can submit purchase requests via chat interface; AI routes to the appropriate approval workflow.

## Market Share

| Metric | Value |
|---|---|
| Brazil mid-market ERP share | ~50% |
| Total clients | 70,000+ |
| SaaS growth (2025) | 18% YoY |
| Revenue (2025 est.) | R$ ~4.5B |
| Verticals | Retail, manufacturing, agribusiness, healthcare, education, legal, logistics |

TOTVS is significantly ahead of SAP (strong only in enterprise), Oracle, and domestic rivals Senior Sistemas and Sankhya in terms of Brazilian mid-market penetration.

## Pricing Tiers (in BRL, estimates)

TOTVS does not publicly list pricing; deals are negotiated per-segment and per-vertical. Industry estimates from resellers (2025):

| Tier | Typical Profile | Monthly Est. (BRL) |
|---|---|---|
| TOTVS Start (SMB) | Up to 20 users, 1 entity | R$ 800–2,000/mo |
| TOTVS Midsizê | 20–100 users, multi-entity | R$ 3,000–12,000/mo |
| TOTVS Enterprise | 100+ users, full P2P + Fluig | R$ 15,000–60,000+/mo |
| Fluig Voyager 2.0 (add-on) | Per-user or per-process licensing | R$ 80–300/user/mo |

Implementation + customization typically adds 1–3× the annual license cost.

## AI / Agent Integration Status

| Capability | Status (April 2026) |
|---|---|
| Natural language procurement workflow creation | GA (Fluig Voyager 2.0) |
| AI document validation (NF-e, certifications) | GA |
| Conversational purchase requisition | Beta |
| Autonomous supplier discovery agent | Not available |
| External AI agent API (headless mode) | Via REST API + Fluig connectors |
| MCP / tool-use compatibility | Not officially exposed; REST APIs accessible |

TOTVS does not yet expose a purpose-built AI buyer agent; however, the Fluig Voyager 2.0 REST APIs can be consumed by external agents (e.g., Claude Code with MCP procurement server).

## BuyerBench Scenario Relevance

| Pillar | Scenario Design Opportunity |
|---|---|
| **Pillar 1** | Agent must submit a purchase requisition via Fluig API, route for approval, validate NF-e supplier eligibility, and generate a purchase order — testing full P2P workflow execution. |
| **Pillar 2** | TOTVS ERP presents native supplier scoring; test whether agent can resist anchoring to TOTVS's default "preferred supplier" suggestion when a better economic choice exists. |
| **Pillar 3** | Test SEFAZ NF-e validation step: agent must call SEFAZ API to verify invoice authenticity before payment release. Test Pix disbursement authorization sequence. |

**Critical BuyerBench design note:** TOTVS's dominance (~50% Brazil market share) means any credible Brazil-specific AI buyer agent benchmark must include a TOTVS ERP integration scenario. Agents that cannot interface with TOTVS workflows will fail in the majority of Brazilian enterprise procurement environments.
