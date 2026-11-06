# AI Buyer Agents and Autonomous Procurement Research Vault

> Research initiated: 2026-04-04
> Last updated: 2026-04-06 (Phase 06 Complete — 4 synthesis documents added; vault now fully interconnected with competitive landscape, pricing registry, Brazil analysis, and scenario recommendations)
> Agent: CladiBuyer Benchmarker

## Start Here — Navigation Guide

> **New to this vault?** Start with one of these four entry points depending on your goal:

| Goal | Best Entry Point |
|------|-----------------|
| Understand who competes with whom | [[Competitive-Landscape]] — 4-layer market map, competitive clusters, head-to-head tables, 22-event timeline (2025–2026) |
| Know what things cost | [[Pricing-Registry]] — Global + Brazil pricing tables; model API costs, agent runtime, consumer subscriptions, per-transaction fees |
| Understand the Brazil opportunity | [[Brazil/Brazil-vs-Global-Analysis]] — Market size, infrastructure contrast, regulatory divergence, localization gaps, market-entry priorities |
| Design new BuyerBench scenarios | [[BuyerBench-Scenario-Recommendations]] — 20 new scenario proposals across Pillars 1–3 + 5 Brazil-specific scenarios with ACES-calibrated benchmarks |

For full entity navigation, continue reading the sections below. For the Brazil sub-vault, see [[Brazil/INDEX]].

---

## Overview

This vault contains structured research about the **AI Buyer Agents and Autonomous Procurement** market — AI-driven systems that select, negotiate for, and/or execute purchases on behalf of users or organizations. Gartner projects $15T+ in B2B purchases will flow through AI agents by 2028. The payment protocol layer (ACP, AP2/UCP, x402, Visa, Mastercard) is undergoing active standardization as of 2026.

### Market Subfamilies
- Enterprise procurement agents (source-to-pay AI) — Salesforce, SAP, Procure AI, Omnea
- Consumer shopping agents (delegated checkout, auto-buy) — Amazon Rufus/Alexa+, OpenAI ACP, Perplexity Comet
- Trading and investment buyer agents (market execution bots, crypto)
- Negotiation buyer agents (alternating offers, auctions) — NegMAS/ANAC ecosystem
- Payment-capable agents and commerce protocols (AP2, UCP, ACP, x402, Visa, Mastercard)

## Market Snapshot (2026-04-04)

| Metric | Value | Source |
|--------|-------|--------|
| AI Agents market size (2025) | ~$7.63B | Grand View Research |
| AI Agents market size (2026) | ~$10.91B | Grand View Research |
| Agentic Commerce TAM (2025) | ~$135B | McKinsey / NextMSC |
| Agentic Commerce projected (2030) | ~$1.7T | NextMSC |
| B2B purchases via AI agents by 2028 | $15T+ | Gartner |
| AI ecommerce traffic growth YoY (to Black Friday 2025) | +520% | Conductor |
| Enterprise AI agent adoption (Q3 2025) | 42% of orgs | KPMG Pulse Survey |
| Amazon Rufus active users | 300M | Forrester |

## Recent Developments

- **2026-03-10**: Amazon wins injunction blocking Perplexity Comet from Amazon marketplace
- **2026-02-27**: OpenAI + Amazon $50B strategic partnership in agentic commerce
- **2026-03-04**: OpenAI removes Instant Checkout (ACP) from ChatGPT
- **2025-10-16**: Visa and Mastercard both launch agentic AI payment infrastructure on same day
- **2025-10**: Visa Trusted Agent Protocol launched (open, 10+ partners)
- **2025-09**: OpenAI ACP + Stripe go live in ChatGPT (4% merchant fee)
- **2025-04**: Visa Intelligent Commerce launched with Anthropic, Microsoft, OpenAI, Perplexity
- **2025**: Google releases AP2 + UCP with 60+ partners

## Quick Navigation

### Companies
- [[Companies/Procure-AI|Procure AI]] — AI-native procurement automation platform; 50+ autonomous agents across source-to-pay; $13M seed (Headline, Nov 2025); founded 2020; London/Paris/Frankfurt
- [[Companies/Omnea|Omnea]] — AI SRM / procurement orchestration; vendor onboarding + cross-functional approval workflows; $50M Series B (Insight Partners + Khosla Ventures, Sep 2025); founded 2022; London
- [[Companies/Zycus|Zycus]] — Global source-to-pay suite; Merlin ANA (Autonomous Negotiation Agent) is first enterprise-deployed autonomous supplier negotiation agent; ~2,500 employees; founded 1998; Princeton NJ / Mumbai
- [[Companies/Fairmarkit|Fairmarkit]] — AI agents for autonomous sourcing (demand-to-award); $78M raised; 150,000+ events with zero human touch per year at enterprise scale; Boston, founded 2017; 5× ProcureTech100
- [[Companies/Skyfire|Skyfire]] — AI agent payment infrastructure (KYA identity + KYAPay open protocol + multi-rail wallets); $9.5M seed (Neuberger Berman, a16z CSX, Coinbase Ventures); live Visa Intelligent Commerce demo (Dec 2025); Pillar 3 payment rails reference
- [[Companies/Amazon-Agentic-Commerce|Amazon Agentic Commerce]] — Nova model family ($0.035–$0.80/M tokens); AgentCore Runtime ($0.0895/vCPU-hr); Amazon Business AI tools (bundled); $50B OpenAI partnership (Feb 2026); Perplexity CFAA injunction (Mar 2026); **Pillars 1+2+3 infrastructure layer**
- [[Companies/OpenAI-Agent-Platform|OpenAI Agent Platform]] — GPT-5 family ($0.05–$1.75/M input tokens); Operator browser agent (Pro $200/mo); Agents SDK (Mar 2025); ACP Instant Checkout launched Sep 2025 → removed Mar 2026; Frontier enterprise platform; **Pillars 1+2+3 (agent under test + platform)**
- [[Companies/Google-Agentic-Commerce|Google Agentic Commerce]] — Project Mariner browser agent (83.5% WebVoyager); Gemini 2.5 Pro ($1.25/M input tokens); Vertex AI Agent Engine ($0.00994/vCPU-hr); AP2/UCP payment protocol layer; $185B CapEx; **Pillars 1+3 (infrastructure + protocol)**
- [[Companies/Stripe-Agent-Payments|Stripe Agent Payments]] — ACP co-author + primary payment rail; SPT (Shared Payment Token) agent-payment primitive; standard 2.9%+$0.30; Radar +$0.02/txn; Payments Foundation Model (trained on $1.4T+ volume); **Pillar 3 primary payment rail reference**
- [[Companies/Coinbase-Agent-Payments|Coinbase Agent Payments]] — x402 protocol creator; USDC on Base at $0 facilitator fee; Agentic Wallets ($0.005/op); x402 Foundation (Coinbase, Stripe, Cloudflare, AWS, Anthropic); GENIUS Act compliant; **Pillar 3 crypto payment rail + irreversibility testing**

### Products & Services
- [[Products/Amazon-Rufus-BuyForMe|Amazon Rufus / Buy for Me / Alexa+]] — 3-product AI shopping stack; 300M Rufus users; cross-site Buy for Me (Nova+Claude); $10–12B GMV lift; Alexa+ GA Feb 2026; Amazon won injunction vs. Perplexity Mar 2026; **Pillar 3: user consent ≠ platform authorization**
- [[Products/ChatGPT-Operator|ChatGPT Operator / Shopping]] — Browser automation agent (Jan 2025); ACP Instant Checkout live Sep 2025 → removed Mar 2026 (poor conversion, merchant control concerns); ChatGPT Agent mode Feb 2026; Responses API + CUA pricing documented; **Pillar 3: protocol-available-but-disabled failure mode**
- [[Products/Perplexity-Comet|Perplexity Comet]] — AI-native browser agent; cross-site autonomous purchase; GA Oct 2025; Buy with Pro (PayPal); Comet Plus $5/mo; Amazon injunction Mar 2026 (CFAA precedent); appealed Apr 2026; **Pillar 3: agent-identity masking reference + CFAA authorization precedent**
- [[Products/Salesforce-Agentforce|Salesforce Agentforce]] — Enterprise AI agent platform; 3 pricing models ($2/conversation, Flex Credits $0.10/action, AELA $125+/user); Buyer Agent + Supply Chain Agent + Import Specialist; no native payment rail; Agent Script determinism; **Pillar 3: least-privilege + audit trail positive reference**
- [[Products/NegMAS|NegMAS]] — Open-source negotiation framework; official ANAC engine (16 years, IJCAI 2025); SAOMechanism bilateral buyer-seller; SCML supply chain; BuyerBench `negmas` agent ID; **Pillar 1 supply chain benchmark + Pillar 2 bias testing via configurable utility functions**

### Protocols & Standards
- [[Technologies/ACP|ACP (Agentic Commerce Protocol)]] — OpenAI + Stripe; Apache 2.0; four-step checkout API + SharedPaymentToken + Stripe Radar fraud detection; live as ChatGPT Instant Checkout Sep 2025; removed Mar 2026 (poor adoption); spec ongoing under community governance; **Pillar 3 reference implementation**
- [[Protocols/AP2-UCP|AP2 / UCP (Google)]] — Co-launched NRF Jan 11 2026; 60+ partners incl. all 5 major card networks; AP2 = cryptographic Intent+Cart mandates (VC-signed authorization); UCP = full commerce orchestration (discovery→fulfillment); native x402 crypto extension; REST/MCP/A2A compatible; **Pillar 3 authorization protocol reference**
- [[Protocols/x402|x402 (Coinbase)]] — HTTP 402 micropayment protocol; launched Sep 2025 (Coinbase+Cloudflare); USDC pay-per-request; EIP-712/EIP-3009 gasless signing; ~2s settlement on Base; x402 Foundation (Coinbase, Cloudflare, AWS, Anthropic, Circle); AP2 crypto extension; **Pillar 3 crypto payment rail + FATF Travel Rule applicability**
- [[Protocols/Visa-Intelligent-Commerce|Visa Intelligent Commerce + Trusted Agent Protocol]] — VIC launched Apr 30 2025 (100+ partners incl. Anthropic, OpenAI, Microsoft); TAP launched Oct 14 2025 — open framework (HTTP Message Signatures + WebAuthn); KYA cryptographic identity (principal→agent→credential→scope); tens of billions of existing Visa tokens extended; **Pillar 3 authentication/authorization reference standard**
- [[Protocols/Mastercard-Agent-Pay|Mastercard Agent Pay]] — Launched Oct 14 2025 (same day as Visa TAP); 3-layer model (Agent Registration → Agentic Tokens → Verifiable Intent open-source spec); US cardholders enabled mid-Nov 2025; Web Bot Auth via Cloudflare CDN; Verifiable Intent immutable audit trail; **Pillar 3 dispute resolution + audit trail reference**

### Key People
- [[People/Amine-Allouah|Amine Allouah]] — Lead author, ACES paper (arXiv:2508.02630); Columbia Business School PhD; designed the RCT benchmark that documented 5× position bias and endorsement effects in AI buyer agents; **Pillar 2 empirical foundation**
- [[People/Omar-Besbes|Omar Besbes]] — Senior author, ACES paper; Columbia Business School professor (DRO division); revenue management and market microstructure expert; **Pillar 2 theoretical grounding**
- [[People/Yasser-Mohammad|Yasser Mohammad]] — Creator of NegMAS + SCML; official ANAC engine (16 years, IJCAI); NEC/AIST researcher; configurable utility functions for bias research; **BuyerBench `negmas` agent reference implementation**
- [[People/Kevin-Frechette|Kevin Frechette]] — CEO and Co-Founder of Fairmarkit (Boston, 2017); 150,000+ zero-human-touch events/year; prior IBM/Dell; lead practitioner voice on autonomous procurement at enterprise scale; **Pillar 1 scenario design reference**
- [[People/Amir-Sarhangi|Amir Sarhangi]] — CEO and Co-Founder of Skyfire; prior VP Product at Ripple ($50B+ processed) and Jibe Mobile (acq. by Google → Android RCS); designed KYAPay open protocol for AI agent identity; **Pillar 3 identity-first payment architecture**
- [[People/Rubail-Birwadker|Rubail Birwadker]] — SVP Head of Growth Products & Partnerships, Visa; oversees Visa Intelligent Commerce (100+ partners), Trusted Agent Protocol, crypto/stablecoins; at Visa since 2011; **Pillar 3 VIC/TAP authorization reference**
- [[People/Jorn-Lambert|Jorn Lambert]] — Chief Product Officer, Mastercard; launched Agent Pay (Apr 2025) + Verifiable Intent open-source spec + Web Bot Auth (Cloudflare CDN); formerly CDO at Mastercard since 2002; **Pillar 3 audit trail and dispute resolution reference**

### Technologies
_No technologies researched yet._

### Market Trends
_No trends researched yet._

### Synthesis Documents

> Phase 06 synthesis documents — these cross-reference the entire vault and answer high-level strategic questions.

- [[Competitive-Landscape|Global Competitive Landscape]] — 4-layer market map (procurement platforms → agent runtimes → payment infrastructure → standards/protocols); 4 competitive clusters; 12 head-to-head comparison tables; 22-event timeline Apr 2025–Apr 2026; 8 identified white-space gaps; wiki-links to all 37 vault entities
- [[Pricing-Registry|Global + Brazil Pricing Registry]] — Model API pricing (Amazon Nova, OpenAI GPT-5, Gemini 2.5); agent runtime costs (AgentCore vs. Vertex AI: 9× gap); consumer subscription tiers ($0–$249.99/mo); Salesforce Agentforce 3 pricing models; Stripe + Coinbase per-transaction schedules; Brazil BRL table (Nubank, Stone, ASAAS, Celcoin, Belvo, TOTVS, Mercado Livre, Pipefy)
- [[Brazil/Brazil-vs-Global-Analysis|Brazil vs. Global Analysis]] — Brazil TAM ($1.4–1.65B) vs. global ($9.5B procurement software); Pix vs. card rails; TOTVS vs. SAP/Oracle; LGPD vs. GDPR; three-tier market-entry framework; 11 Brazil-specific BuyerBench scenario archetypes
- [[BuyerBench-Scenario-Recommendations|BuyerBench Scenario Design Recommendations]] — 4 Pillar 1 new scenarios (P1-19 through P1-22); 6 Pillar 2 ACES-calibrated bias scenarios (P2-10 through P2-15); 5 Pillar 3 security scenarios (P3-07 through P3-11); 5 Brazil-specific scenarios (BR-01 through BR-05); 20-scenario priority roadmap

### Brazil Market Sub-Vault

> Brazil is the largest B2B e-commerce market in Latin America (~R$234B, 18.42% CAGR), with unique infrastructure (Pix instant payments, Open Finance mandate, NF-e fiscal documents, LGPD). Phase 04 built a parallel Brazil vault profiling 25+ entities.

**Navigate:** [[Brazil/INDEX|Brazil INDEX]] — full entity list, coverage stats, key market themes (25 entities, ~83% coverage)

| Document | Summary |
|---|---|
| [[Brazil/Brazil-vs-Global-Analysis\|Brazil vs. Global Analysis]] *(synthesis)* | Market size comparison, Pix vs. card rails, LGPD vs. GDPR, market-entry priority framework — Phase 06 synthesis document |
| [[Brazil/Market-Context/Brazil-AI-Procurement-Landscape\|Brazil AI Procurement Landscape]] | 4 domestic AI startups profiled: Freedom (R$14.5M), Zinit (US$8M), Linkana (YC W20), Pipefy (~$150M) |
| [[Brazil/Market-Context/Brazil-B2B-Marketplace-Landscape\|Brazil B2B Marketplace Landscape]] | 5 platforms: Mercado Livre Negócios, TOTVS+Fluig, Compras.gov.br/PNCP, B2Brazil, Nomos |
| [[Brazil/Market-Context/Brazil-ERP-Landscape\|Brazil ERP Landscape]] | TOTVS (50% share + Agente de Compras), SAP Joule, Senior, Sankhya, Oracle — pricing in BRL, AI agent matrix |
| [[Brazil/Market-Context/Brazil-Fintech-Payment-Landscape\|Brazil Fintech Payment Landscape]] | Nubank, Stone, Celcoin, ASAAS, Belvo — Pix/Open Finance stack for autonomous procurement payments |
| [[Brazil/Market-Context/Global-Players-Brazil-Presence\|Global Players Brazil Presence]] | Salesforce Agentforce, OpenAI API, Microsoft Copilot Studio, SAP Ariba+Joule, Zycus Merlin, Coupa — localization gap analysis, BRL pricing matrix |

### Research Papers
- [[Research-Papers/ACES-AI-Agent-Buying|ACES (arXiv 2508.02630)]] — RCT benchmark for AI buyer agent behavioral bias; 5× position bias, +1.0–+1.9 endorsement effect, −1.6 to −2.2 price elasticity; **Pillar 2 design foundation**
- [[Research-Papers/LLM-Agent-Benchmarking-Survey|LLM Agent Benchmarking Survey (arXiv 2507.21504)]] — KDD 2025 survey; two-dimensional taxonomy (objectives × process); maps to BuyerBench 3-pillar structure
- [[Research-Papers/AgentBench|AgentBench (arXiv 2308.03688)]] — ICLR 2024; 8 task environments; GPT-4 ~4× better than OSS; harness architecture template for **Pillar 1**
- [[Research-Papers/WebArena|WebArena (arXiv 2307.13854)]] — ICLR 2024; 5-site realistic web env; 812 tasks; 14.4% GPT-4 vs 78% human baseline; functional correctness evaluation; **Pillar 1** gap analysis
- [[Research-Papers/WebShop|WebShop (arXiv 2207.01206)]] — NeurIPS 2022; 1.18M Amazon products; partial-credit reward; 29% best model vs 59% human; **Pillar 1 reward design template**

### Security & Compliance Frameworks
- [[Security-Compliance/PCI-DSS-v4|PCI DSS v4.0 (v4.0.1)]] — Full enforcement Mar 31 2025; 12 req domains; NHI management mandate (Req 8); AI Principles guidance; tokenization scope-reduction; **Pillar 3 payment security baseline**
- [[Security-Compliance/EMV-3DS2|EMV 3-D Secure (3DS2)]] — Card-not-present authentication; frictionless vs. challenge flows; decoupled auth (MIT exemption) for agent-initiated checkout; ACP/SPT as frictionless-by-design solution; **Pillar 3 authentication reference**
- [[Security-Compliance/NIST-AI-RMF|NIST AI RMF 1.0]] — Voluntary but quasi-mandatory (EO 14110 + OMB M-24-10); GOVERN/MAP/MEASURE/MANAGE functions; GenAI Profile (NIST AI 600-1); CAISI agent-identity initiative (Feb 2026); **Pillar 3 AI governance baseline**
- [[Security-Compliance/ISO-42001|ISO/IEC 42001:2023]] — World's first certifiable AI management system standard (Dec 2023); Harmonized Structure; 42 controls across 9 domains; IBM Granite model-scoped certification precedent; **Pillar 3 AI governance certification pathway**
- [[Security-Compliance/FATF-AML-CFT|FATF AML/CFT (40 Recommendations)]] — Travel Rule (USD 1,000 wire / same for VASPs; EU zero-threshold); Dec 2025 AI Horizon Scan names autonomous agents as ML/TF vector; sunrise + unhosted wallet gaps; **Pillar 3 crypto payment rail compliance**

## Research Tools

### Agents
- [[Agents/company-researcher|Company Researcher]]
- [[Agents/product-researcher|Product Researcher]]
- [[Agents/person-researcher|Person Researcher]]
- [[Agents/technology-researcher|Technology Researcher]]
- [[Agents/trend-researcher|Trend Researcher]]

### Commands
- `/research` - Research a specific entity

## Statistics

### Global Vault

| Category | Discovered | Researched |
|----------|------------|------------|
| Companies | 10 | 10 (100%) |
| Protocols & Standards | 5 | 5 (100%) |
| Products & Platforms | 5 | 5 (100%) |
| People | 7 | 7 (100%) |
| Technologies | 0 | 0 |
| Trends | 0 | 0 |
| Research Papers | 5 | 5 (100%) |
| Security & Compliance Frameworks | 5 | 5 (100%) |
| **Total Entities** | **37** | **37 (100%)** |

### Brazil Sub-Vault

| Category | Discovered | Researched |
|----------|------------|------------|
| Companies (Brazil) | 9 | 9 (100%) |
| Products (Brazil) | 5 | 5 (100%) |
| Regulatory/Compliance (Brazil) | 5 | 5 (100%) |
| Market Context Documents | 5 | 5 (100%) |
| People (Brazil) | 1 | 1 (100%) |
| **Total Brazil Entities** | **25** | **~25 (~83% coverage)** |

### Synthesis Documents (Phase 06)

| Document | Type | Status |
|----------|------|--------|
| [[Competitive-Landscape]] | Analysis | Complete — 2026-04-06 |
| [[Pricing-Registry]] | Reference | Complete — 2026-04-06 |
| [[Brazil/Brazil-vs-Global-Analysis]] | Analysis | Complete — 2026-04-06 |
| [[BuyerBench-Scenario-Recommendations]] | Report | Complete — 2026-04-06 |

## Research Summary

**Research Period:** 2026-04-04 — 2026-04-06
**Total Loops:** 12 (Loop 00001, iterations 1–12) + Phase 01 (2026-04-05) + Phase 02 (2026-04-05) + Phase 03 (2026-04-06)
**Agent:** CladiBuyer Benchmarker

### Coverage Statistics

| Category | Discovered | Researched | Gap |
|----------|------------|------------|-----|
| Companies | 10 | 10 (100%) | 0 — 5 original + 5 Phase 03 platform profiles (Amazon, OpenAI, Google, Stripe, Coinbase) |
| Protocols & Standards | 5 | 5 (100%) | 0 — ACP, AP2/UCP, x402, Visa, Mastercard all profiled |
| Products & Platforms | 5 | 5 (100%) | 0 — Amazon, ChatGPT Operator, Perplexity Comet, Agentforce, NegMAS all profiled |
| People | 7 | 7 (100%) | 0 — Allouah, Besbes, Mohammad, Frechette, Sarhangi, Birwadker, Lambert profiled |
| Research Papers | 5 | 5 (100%) | All 5 profiled: ACES, LLM Eval Survey, AgentBench, WebArena, WebShop |
| Security & Compliance Frameworks | 5 | 5 (100%) | All 5 profiled: PCI DSS v4.0, EMV 3DS2, NIST AI RMF, ISO 42001, FATF AML/CFT |
| **Total** | **37** | **37 (100%)** | **All entities researched — vault coverage complete** |

### Researched Entities (with Research Files)

| Entity | Type | Research File | Key Pillar Relevance |
|--------|------|---------------|----------------------|
| Procure AI | Company | `vault/Companies/Procure-AI.md` | Pillar 1 (50+ autonomous agents, source-to-pay) |
| Omnea | Company | `vault/Companies/Omnea.md` | Pillar 1 + 2 ($75M+, CFO economic optimization) |
| Zycus | Company | `vault/Companies/Zycus.md` | Pillar 1 + 2 (Merlin ANA autonomous negotiation) |
| Fairmarkit | Company | `vault/Companies/Fairmarkit.md` | Pillar 1 + 2 (150K+ zero-touch events, 2025 Index) |
| Skyfire | Company | `vault/Companies/Skyfire.md` | **Pillar 3** (KYA, KYAPay, multi-rail, fraud detection) |
| ACP | Protocol | `vault/Technologies/ACP.md` | **Pillar 3** (4-step checkout API, SPT credential model, Stripe Radar fraud, rollback scenario) |
| AP2 / UCP | Protocol | `vault/Protocols/AP2-UCP.md` | **Pillar 3** (VC-signed Intent+Cart mandates, 60+ partners, crypto extension) |
| x402 | Protocol | `vault/Protocols/x402.md` | **Pillar 3** (HTTP 402 micropayments, EIP-712 gasless signing, FATF applicability) |
| Visa Intelligent Commerce | Protocol | `vault/Protocols/Visa-Intelligent-Commerce.md` | **Pillar 3** (KYA identity, TAP open framework, WebAuthn, AWS Bedrock integration) |
| Mastercard Agent Pay | Protocol | `vault/Protocols/Mastercard-Agent-Pay.md` | **Pillar 3** (Verifiable Intent audit trail, Cloudflare Web Bot Auth, dispute resolution) |
| Amazon Rufus / Buy for Me | Product | `vault/Products/Amazon-Rufus-BuyForMe.md` | Pillar 1 + **Pillar 3** (user consent ≠ platform auth precedent, CFAA injunction) |
| ChatGPT Operator / Shopping | Product | `vault/Products/ChatGPT-Operator.md` | **Pillar 3** (ACP rollback failure modes, protocol-available-but-disabled scenario) |
| Perplexity Comet | Product | `vault/Products/Perplexity-Comet.md` | **Pillar 3** (agent-identity masking violation, CFAA precedent, cross-platform auth) |
| Salesforce Agentforce | Product | `vault/Products/Salesforce-Agentforce.md` | Pillar 1 + **Pillar 3** (least-privilege, Agent Script determinism, JSON audit trail) |
| NegMAS | Product | `vault/Products/NegMAS.md` | Pillar 1 + 2 (SCML supply chain, SAOMechanism bilateral, bias utility functions) |
| PCI DSS v4.0 | Security/Compliance Framework | `vault/Security-Compliance/PCI-DSS-v4.md` | **Pillar 3** (NHI identity/auth Req 8, tokenization scope-reduction, AI Principles guidance) |
| EMV 3-D Secure (3DS2) | Security/Compliance Framework | `vault/Security-Compliance/EMV-3DS2.md` | **Pillar 3** (frictionless vs. challenge flows, decoupled auth, MIT exemption, ACP SPT solution) |
| NIST AI RMF 1.0 | Security/Compliance Framework | `vault/Security-Compliance/NIST-AI-RMF.md` | **Pillar 3** (GOVERN/MAP/MEASURE/MANAGE, GenAI Profile 600-1, CAISI agent identity initiative) |
| ISO/IEC 42001:2023 | Security/Compliance Framework | `vault/Security-Compliance/ISO-42001.md` | **Pillar 3** (42 controls, 9 domains, certification pathway, IBM Granite model-scoped cert) |
| FATF AML/CFT | Security/Compliance Framework | `vault/Security-Compliance/FATF-AML-CFT.md` | **Pillar 3** (Travel Rule, AI Horizon Scan Dec 2025, autonomous-agent ML/TF vector, x402 compliance) |
| Amazon Agentic Commerce | Company | `vault/Companies/Amazon-Agentic-Commerce.md` | Pillars 1+2+3 (Nova pricing, AgentCore, agent cost multiplier 5–10×, Perplexity CFAA dual-auth precedent) |
| OpenAI Agent Platform | Company | `vault/Companies/OpenAI-Agent-Platform.md` | Pillars 1+2+3 (GPT-5 family, Operator, Agents SDK, ACP rollback, Frontier enterprise) |
| Google Agentic Commerce | Company | `vault/Companies/Google-Agentic-Commerce.md` | Pillars 1+3 (Project Mariner, Gemini 2.5 Pro, Vertex AI Agent Engine 9× cheaper than AgentCore, AP2/UCP) |
| Stripe Agent Payments | Company | `vault/Companies/Stripe-Agent-Payments.md` | **Pillar 3** (SPT token model, Payments Foundation Model, MPP, ACP co-author, Radar fraud detection) |
| Coinbase Agent Payments | Company | `vault/Companies/Coinbase-Agent-Payments.md` | **Pillar 3** (x402 protocol, USDC micropayments, Agentic Wallets, irreversibility risk, KYC gap flagged) |
| Amine Allouah | Person | `vault/People/Amine-Allouah.md` | **Pillar 2** (ACES paper lead author; RCT benchmark; 5× position bias + endorsement effect documented) |
| Omar Besbes | Person | `vault/People/Omar-Besbes.md` | **Pillar 2** (ACES senior author; Columbia professor; revenue management + market microstructure theory) |
| Yasser Mohammad | Person | `vault/People/Yasser-Mohammad.md` | Pillars 1+2 (NegMAS + SCML creator; official ANAC engine; BuyerBench `negmas` agent reference) |
| Kevin Frechette | Person | `vault/People/Kevin-Frechette.md` | **Pillar 1** (Fairmarkit CEO; 150K+ zero-touch sourcing events/year; enterprise practitioner reference) |
| Amir Sarhangi | Person | `vault/People/Amir-Sarhangi.md` | **Pillar 3** (Skyfire CEO; KYAPay open protocol architect; prior Ripple VP; identity-first payment design) |
| Rubail Birwadker | Person | `vault/People/Rubail-Birwadker.md` | **Pillar 3** (Visa SVP; VIC + TAP lead; 100+ partners; crypto/stablecoins; at Visa since 2011) |
| Jorn Lambert | Person | `vault/People/Jorn-Lambert.md` | **Pillar 3** (Mastercard CPO; Agent Pay + Verifiable Intent + Web Bot Auth; audit trail reference) |

### Research Notes

- **Research Complete — Phase 06 (2026-04-06).** All synthesis documents created: Global Competitive Landscape (4-layer market map, 22-event timeline, 8 white-space gaps), Pricing Registry (global + Brazil, 6 pricing observations), Brazil vs. Global Analysis (three-tier market-entry framework, 11 scenario archetypes), BuyerBench Scenario Recommendations (20 new scenarios across Pillars 1–3 + 5 Brazil-specific). Vault is now a fully interconnected, queryable knowledge base.
- **Phase 03 Complete (2026-04-06).** 12 Phase 03 entities profiled: 5 major platform company profiles (Amazon, OpenAI, Google, Stripe, Coinbase) + 7 key people profiles. Vault now at 37/37 (100%) coverage.
- **Phase 02 Complete (2026-04-05).** 10 Phase 02 entities profiled: 5 research papers + 5 security/compliance frameworks.
- **Companies category: COMPLETE.** All 10 companies fully profiled — 5 original (Procure AI, Omnea, Zycus, Fairmarkit, Skyfire) + 5 Phase 03 platform incumbents (Amazon, OpenAI, Google, Stripe, Coinbase).
- **People category: COMPLETE.** All 7 key people profiled: ACES authors (Allouah, Besbes), NegMAS creator (Mohammad), Fairmarkit CEO (Frechette), Skyfire CEO (Sarhangi), Visa SVP (Birwadker), Mastercard CPO (Lambert).
- **Protocols, Products, Research Papers, Security Frameworks: COMPLETE.** All fully profiled as of Phase 01/02 (2026-04-05).
- **0 entities remain.** Vault coverage is 100%.
- **Inter-page links:** All profiles use `[[Entity]]` wiki-link syntax. The Obsidian graph shows a dense cluster connecting all protocols (ACP ↔ AP2/UCP ↔ x402 ↔ Visa ↔ Mastercard), products cross-referencing each other (Amazon ↔ Perplexity ↔ ChatGPT), and all Pillar 3 entities linking to Skyfire and PCI-DSS-v4.
- **Pipeline note (Loop 00001):** The research pipeline ran 12 loops due to a recurring stall pattern (5_PROGRESS.md gate was firing before docs 1–4 executed in each cycle). Loops 7–12 used a stall-break pattern where the gate directly executed blocked pipeline steps.

---
*This vault was initialized by the Maestro Market Research Playbook*
*Full market analysis: [[LOOP_00001_MARKET_ANALYSIS]]*
