---
type: product
title: Mercado Livre Negócios
created: 2026-04-06
tags:
  - brazil
  - b2b-marketplace
  - procurement
  - wholesale
  - e-commerce
related:
  - '[[Brazil-AI-Procurement-Landscape]]'
  - '[[Brazil-ERP-Landscape]]'
  - '[[INDEX]]'
---

# Mercado Livre Negócios

## Overview

Mercado Livre Negócios is the B2B (business-to-business) unit of Mercado Livre (MELI), Latin America's dominant e-commerce platform. Officially launched in Brazil in September 2025 after a testing phase that began in October 2024, the platform extends Mercado Livre's consumer marketplace into corporate procurement — offering CNPJ-authenticated bulk purchasing with exclusive pricing and compliance tooling (NF-e selection).

**Parent company:** Mercado Libre Inc. (NASDAQ: MELI), headquartered in Uruguay  
**Brazil launch:** September 2025  
**Latin America footprint:** Brazil, Argentina, Mexico, Chile  
**Registered users (LatAm, as of Sep 2025):** 4 million+ corporate accounts

## Key Capabilities

- **CNPJ-gated purchasing**: Companies register a valid CNPJ; the platform validates legal representation documents before granting access to corporate pricing.
- **NF-e (Nota Fiscal Eletrônica) seller filter**: Buyers can filter to only purchase from sellers who issue electronic invoices, simplifying accounting and tax reconciliation.
- **Wholesale pricing & bulk discounts**: Up to 50% discount compared to consumer prices; available even for single-unit corporate purchases.
- **Collaborator permissions**: Organizations can delegate purchase authorization to multiple employees with role-based access control.
- **Fast fulfillment**: ~74% of B2B orders delivered within 48 hours via Mercado Livre's existing logistics network (Mercado Envios).
- **Product breadth**: Over 1.3 million SKUs across office supplies, technology, food & beverage, cleaning, furniture, and automotive parts.
- **Automatic invoicing and activity reporting**: Centralized "Purchases" dashboard for spend tracking and audit.

## Market Share & Scale

| Metric | Value |
|---|---|
| Parent platform GMV (Brazil, 2024) | Part of R$ 200B+ total e-commerce |
| B2B e-commerce CAGR Brazil (to 2031) | 18.42% |
| B2B SKUs available at launch | 1.3 million+ |
| LatAm corporate users (Sep 2025) | 4 million+ |

Mercado Livre dominates Brazilian consumer e-commerce; Negócios represents its first systematic move into the corporate procurement space where TOTVS, SAP Ariba, and niche SRM platforms have historically operated.

## Pricing in BRL

- **Buyer access:** Free — no subscription fee for CNPJ-registered companies.
- **Seller listing:** Standard Mercado Livre seller fees apply (category-dependent commission, typically 10–16% of transaction value). B2B wholesale sellers may negotiate tiered rate agreements.
- **Discounts:** Up to 50% below consumer prices for corporate accounts.
- **Mercado Pago integration:** Payments via Pix, boleto, and credit card; Mercado Pago supports split payment and deferred terms for B2B buyers.

Specific B2B subscription or SaaS pricing tiers had not been publicly disclosed as of April 2026.

## AI / Agent Features

As of launch, Mercado Livre Negócios does not expose a dedicated AI buyer agent layer. However:
- The parent platform uses ML for personalized recommendations and dynamic pricing.
- Mercado Pago's fraud detection and Smart Checkout use AI/ML models.
- The CNPJ-gated API and Mercado Livre's public Marketplace API allow programmatic purchasing — making it a potential integration target for external AI buyer agents (e.g., Freedom, Pipefy).

## BuyerBench Scenario Relevance

| Pillar | Scenario Design Opportunity |
|---|---|
| **Pillar 1** | Agent must search Mercado Livre Negócios catalog, identify NF-e-eligible suppliers, and place a CNPJ-authenticated bulk order. |
| **Pillar 2** | Present decoy pricing (consumer price vs. wholesale price); test whether agent correctly disambiguates and selects corporate-discounted SKU. |
| **Pillar 3** | Test NF-e compliance verification: agent must reject sellers who do not issue Nota Fiscal. Pix payment flow testing. |

**Key Brazil-specific compliance hook:** An AI buyer agent operating in Brazil must verify NF-e issuance eligibility before finalizing purchase — a mandatory tax compliance step with no direct equivalent in US/EU benchmarks. Mercado Livre Negócios makes this a first-class workflow.
