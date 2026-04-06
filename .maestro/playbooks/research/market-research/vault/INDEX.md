# AI Buyer Agents and Autonomous Procurement Research Vault

> Research initiated: 2026-04-04
> Last updated: 2026-04-05 (Phase 01 — 9 new protocol + product profiles; vault now 15 entities fully profiled)
> Agent: CladiBuyer Benchmarker

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
_No people researched yet._

### Technologies
_No technologies researched yet._

### Market Trends
_No trends researched yet._

### Research Papers
_Discovered — research profiles pending._
- arXiv 2508.02630 — ACES: What Is Your AI Agent Buying? (buyer agent biases, VLM shopping agent evaluation)
- arXiv 2507.21504 — Evaluation and Benchmarking of LLM Agents: A Survey (methodology for all pillars)
- arXiv 2308.03688 — AgentBench: Evaluating LLMs as Agents (ICLR 2024; web shopping + web browsing tasks)
- arXiv 2307.13854 — WebArena: Realistic Web Environment for Autonomous Agents (e-commerce domain)
- arXiv 2207.01206 — WebShop: AI Shopping Agent Benchmark (NeurIPS 2022; 1.18M Amazon products)

### Security & Compliance Frameworks
_Discovered — research profiles pending._
- **PCI DSS v4.0** — Payment Card Industry Data Security Standard; full enforcement from April 2025; primary baseline for any AI buyer agent executing card transactions
- **EMV 3-D Secure (3DS2)** — Card-not-present authentication protocol; governs online card payment authorization flows for agent-initiated transactions
- **NIST AI Risk Management Framework (AI RMF 1.0)** — Voluntary AI governance framework (Jan 2023); GOVERN/MAP/MEASURE/MANAGE functions applicable to enterprise AI procurement compliance
- **ISO/IEC 42001:2023 AI Management System** — First international certifiable AI management standard (Dec 2023); enterprise AI governance certification pathway
- **FATF Guidance on AML/CFT for Virtual Assets** — Anti-money laundering framework for crypto rails; Travel Rule obligations for x402/Coinbase-based agent payments

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

| Category | Discovered | Researched |
|----------|------------|------------|
| Companies | 5 | 5 (100%) |
| Protocols & Standards | 5 | 5 (100%) |
| Products & Platforms | 5 | 5 (100%) |
| People | 0 | 0 |
| Technologies | 0 | 0 |
| Trends | 0 | 0 |
| Research Papers | 5 | 0 |
| Security & Compliance Frameworks | 5 | 0 |
| **Total Entities** | **25** | **15 (60%)** |

## Research Summary

**Research Period:** 2026-04-04 — 2026-04-05
**Total Loops:** 12 (Loop 00001, iterations 1–12) + Phase 01 (2026-04-05)
**Agent:** CladiBuyer Benchmarker

### Coverage Statistics

| Category | Discovered | Researched | Gap |
|----------|------------|------------|-----|
| Companies | 5 | 5 (100%) | 0 — all 5 companies fully profiled |
| Protocols & Standards | 5 | 5 (100%) | 0 — ACP, AP2/UCP, x402, Visa, Mastercard all profiled |
| Products & Platforms | 5 | 5 (100%) | 0 — Amazon, ChatGPT Operator, Perplexity Comet, Agentforce, NegMAS all profiled |
| Research Papers | 5 | 0 | ACES, LLM Eval Survey, AgentBench, WebArena, WebShop — pending |
| Security & Compliance Frameworks | 5 | 0 | PCI DSS, 3DS2, NIST AI RMF, ISO 42001, FATF — pending |
| **Total** | **25** | **15 (60%)** | 10 entities discovered but not yet deeply profiled |

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

### Research Notes

- **Companies, Protocols, and Products categories: COMPLETE.** All 15 entities across these three categories fully profiled as of 2026-04-05.
- **10 entities remain unresearched.** 5 research papers (ACES, LLM Eval Survey, AgentBench, WebArena, WebShop) and 5 security frameworks (PCI DSS, 3DS2, NIST AI RMF, ISO 42001, FATF) are discovered but pending deep-dive profiles.
- **Inter-page links:** All profiles use `[[Entity]]` wiki-link syntax. The Obsidian graph now shows a dense cluster connecting all protocols (ACP ↔ AP2/UCP ↔ x402 ↔ Visa ↔ Mastercard), products cross-referencing each other (Amazon ↔ Perplexity ↔ ChatGPT), and all Pillar 3 entities linking to Skyfire.
- **Recommended next phase:** Research Papers + Security Frameworks (10 remaining entities). The ACES paper (arXiv 2508.02630) and PCI DSS v4.0 are highest-priority for BuyerBench scenario design.
- **Pipeline note (Loop 00001):** The research pipeline ran 12 loops due to a recurring stall pattern (5_PROGRESS.md gate was firing before docs 1–4 executed in each cycle). Loops 7–12 used a stall-break pattern where the gate directly executed blocked pipeline steps.

---
*This vault was initialized by the Maestro Market Research Playbook*
*Full market analysis: [[LOOP_00001_MARKET_ANALYSIS]]*
