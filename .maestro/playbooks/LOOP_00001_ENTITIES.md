---
type: reference
title: "Entity Discovery Log — AI Buyer Agents Market Research"
created: 2026-04-04
tags:
  - market-research
  - entities
  - ai-agents
  - procurement
  - agentic-commerce
related:
  - '[[LOOP_00001_MARKET_ANALYSIS]]'
  - '[[INDEX]]'
---

# Entity Discovery Log — Loop 00001

This document tracks all entities discovered during market research for the AI Buyer Agents / Autonomous Procurement space. Entities progress through statuses: `PENDING → RESEARCHED` (or `SKIP` / `DUPLICATE`).

---

## Companies - Discovered 2026-04-04

### Procure AI
- **Type:** Company
- **Brief:** AI-native enterprise procurement platform deploying 50+ autonomous agents across the full source-to-pay lifecycle.
- **Why Notable:** One of the clearest pure-play "AI buyer agent" companies in enterprise procurement; raised $13M seed in Nov 2025 led by Headline (C4 Ventures, Futury Capital). Agents span three tiers: autonomous execution, human-collaborative, and ambient/proactive. Directly benchmarkable as an AI buyer agent system.
- **Discovery Source:** https://siliconangle.com/2025/11/27/procure-ai-lands-13m-funding-automate-business-procurement-tasks/
- **Status:** RESEARCHED
- **Research File:** `vault/Companies/Procure-AI.md`
- **Researched:** 2026-04-04

### Omnea
- **Type:** Company
- **Brief:** Enterprise procurement orchestration platform automating vendor onboarding, intake workflows, and cross-functional approvals.
- **Why Notable:** Raised $50M Series B (Sep 2025, led by Insight Partners + Khosla Ventures) with total funding >$75M; backed by Accel, First Round, Point Nine, Prosus. CFO-positioning ("make procurement every CFO's competitive advantage") suggests strong economic optimization angle — relevant to Pillar 2 decision quality evaluation.
- **Discovery Source:** https://www.omnea.co/blog/series-b-announcement
- **Status:** RESEARCHED
- **Research File:** `vault/Companies/Omnea.md`
- **Researched:** 2026-04-04

### Zycus
- **Type:** Company
- **Brief:** Global source-to-pay suite with agentic AI capabilities including Merlin Intake agent and Merlin Autonomous Negotiation Agent (ANA).
- **Why Notable:** One of the first established procurement vendors to deploy an *autonomous negotiation agent* (Merlin ANA) — directly relevant to Pillar 1 (negotiation task scenarios) and Pillar 2 (economic decision quality). The ANA represents a commercial reference implementation of agent-driven price negotiation worth profiling and comparing against NegMAS.
- **Discovery Source:** https://www.zycus.com/
- **Status:** RESEARCHED
- **Research File:** `vault/Companies/Zycus.md`
- **Researched:** 2026-04-04

### Fairmarkit
- **Type:** Company
- **Brief:** AI-powered sourcing platform automating tail-spend and low-value procurement through demand-to-award automation and supplier recommendation.
- **Why Notable:** Handles thousands of small sourcing events autonomously — a high-volume, repeatable buyer-agent workflow ideal for Pillar 1 capability benchmarking (supplier discovery, quote comparison, bid evaluation). Published a "2025 AI in Procurement Index" which may contain adoption/bias data relevant to benchmark design.
- **Discovery Source:** https://www.fairmarkit.com/resource/2025-ai-in-procurement
- **Status:** PENDING

### Skyfire
- **Type:** Company
- **Brief:** AI agent payment infrastructure providing KYA (Know Your Agent) identity verification and autonomous payment execution for AI agents.
- **Why Notable:** Raised $9.5–10M (Neuberger Berman, a16z CSX, Coinbase Ventures); partnered with Visa Intelligent Commerce. Skyfire enables AI agents to spend money without human intervention and is one of the few companies building the *financial rails* layer — critical context for Pillar 3 (payment security, authorization, fraud detection). Demonstrated a live end-to-end agent purchase (Consumer Reports agent buying Bose headphones).
- **Discovery Source:** https://techcrunch.com/2024/08/21/skyfire-lets-ai-agents-spend-your-money/
- **Status:** PENDING

### Discovery Summary
- **Category:** Companies
- **Entities Found:** 5
- **Search Queries Used:**
  - "AI buyer agent companies autonomous procurement startups 2026"
  - "Procure AI Omnea Rye agentic commerce companies funding 2025 2026"
  - "Zycus Fairmarkit Levelpath AI procurement agent company profile 2025"
  - "Skyfire Nekuda AI agent payments company funding 2025 2026"
- **Sources Checked:**
  - SiliconANGLE (Procure AI funding announcement)
  - Omnea blog / PR Newswire (Series B announcement)
  - Zycus.com product pages
  - Fairmarkit resource center
  - TechCrunch / Skyfire.xyz / Crunchbase (Skyfire profile)
  - Rye.com agentic commerce landscape 2026
  - Levelpath top 10 AI procurement solutions 2026

---

## Protocols & Standards - Discovered 2026-04-04

### ACP (Agents Commerce Protocol)
- **Type:** Protocol / Standard
- **Brief:** Open-source Apache 2.0 specification co-developed by OpenAI and Stripe that enables AI agents to discover, select, and pay for goods and services through a standardized checkout API.
- **Why Notable:** ACP is one of two leading contenders for the dominant agent commerce protocol standard. Integrated into ChatGPT as "Instant Checkout" (Sep 2025) with a 4% merchant fee; temporarily removed from ChatGPT in March 2026 following the OpenAI–Amazon strategic partnership, signaling active market dynamics. Critical to Pillar 3 (payment API protocols, authentication flows) and Pillar 1 (agent tool use patterns). OpenAI's $50B Amazon partnership (Feb 2026) may reshape ACP's trajectory.
- **Discovery Source:** https://orium.com/blog/agentic-payments-acp-ap2-x402
- **Status:** PENDING

### AP2 / UCP (Google Agentic Payment Protocol / Universal Commerce Protocol)
- **Type:** Protocol / Standard
- **Brief:** Google's dual-protocol suite for agent commerce: AP2 handles payment authorization and settlement (60+ partners including Mastercard, Adyen, PayPal, Coinbase), while UCP (developed with Shopify) standardizes the product discovery and checkout experience layer.
- **Why Notable:** AP2/UCP represents the most broadly adopted protocol suite by partner count (60+), competing directly with ACP. Google's backing gives it reach across Google Shopping AI, Vertex AI Agent Builder, and a major merchant ecosystem. The AP2 vs. ACP protocol war directly shapes what "correct" agent payment behavior looks like for Pillar 3 security and compliance testing.
- **Discovery Source:** https://www.griddynamics.com/blog/agentic-payments
- **Status:** PENDING

### x402
- **Type:** Protocol / Standard
- **Brief:** HTTP-native micropayment protocol built by Coinbase that repurposes the HTTP 402 "Payment Required" status code to enable instant, cryptographic machine-to-machine payments for AI agents, without OAuth flows or pre-authorization.
- **Why Notable:** x402 represents a fundamentally different payment security model — no traditional card-network authorization chain, instead using cryptographic payment proofs. This creates novel Pillar 3 test scenarios: fraud detection without CVV/3DS, authorization without traditional credential flows, and compliance gaps vs. PCI DSS. Skyfire's agent payment infrastructure is x402-adjacent.
- **Discovery Source:** https://orium.com/blog/agentic-payments-acp-ap2-x402
- **Status:** PENDING

### Visa Intelligent Commerce + Trusted Agent Protocol
- **Type:** Protocol / Standard
- **Brief:** Visa's two-pronged agentic commerce initiative: Visa Intelligent Commerce (launched Apr 2025 with Anthropic, Microsoft, OpenAI, Perplexity as partners) provides AI agents secure access to Visa's payment network; the Visa Trusted Agent Protocol (Oct 2025, 10+ partners, open spec) adds a KYA (Know Your Agent) identity layer for agent authorization and delegation.
- **Why Notable:** Visa launched on the same day as Mastercard (Oct 16, 2025), signaling that traditional card networks are actively building agent payment infrastructure. The Trusted Agent Protocol's KYA model (assigning verified identities to AI agents) is directly relevant to Pillar 3 authentication and authorization test scenarios. Partnered with Anthropic — relevant context for Claude-based agents.
- **Discovery Source:** https://corporate.visa.com/en/sites/visa-perspectives/newsroom/visa-partners-complete-secure-agentic-transactions.html
- **Status:** PENDING

### Mastercard Agent Pay
- **Type:** Protocol / Standard
- **Brief:** Mastercard's agentic payments infrastructure launched October 2025, enabling AI agents to transact through Mastercard's network with built-in identity verification, tokenization, and transaction monitoring designed for autonomous agent use cases.
- **Why Notable:** Co-launched with Visa's agent protocols on Oct 16, 2025, confirming that both major card networks view agentic payments as a near-term operational reality. Mastercard Agent Pay's tokenization and identity requirements map directly to Pillar 3 secure transaction flows and PCI DSS compliance scenarios. Provides a regulatory benchmark for what "compliant" agent payment behavior should look like.
- **Discovery Source:** https://www.mastercard.com/us/en/business/artificial-intelligence/mastercard-agent-pay.html
- **Status:** PENDING

### Discovery Summary
- **Category:** Protocols & Standards
- **Entities Found:** 5
- **Search Queries Used:**
  - "ACP AP2 x402 agentic payment protocol comparison 2025 2026"
  - "Visa Intelligent Commerce Trusted Agent Protocol 2025"
  - "Mastercard Agent Pay agentic payments 2025"
  - "OpenAI Stripe ACP protocol specification"
  - "Google AP2 UCP agentic commerce protocol partners"
- **Sources Checked:**
  - Orium blog: agentic payments ACP, AP2, x402 comparison
  - Grid Dynamics blog: AP2 vs. ACP and x402 analysis
  - Visa corporate newsroom: Intelligent Commerce and Trusted Agent Protocol
  - Mastercard: Agent Pay product page
  - FourWeekMBA: Protocol Wars — Standards Battle for AI Commerce
  - LOOP_00001_MARKET_ANALYSIS.md (primary synthesis source)

---

## Products & Platforms - Discovered 2026-04-04

### Amazon Alexa+ / "Buy for Me"
- **Type:** Product / Platform
- **Brief:** Amazon's consumer-facing AI buyer agent family: Alexa+ (March 2026 launch, $19.99/mo subscription) handles conversational purchasing and task orchestration, while "Buy for Me" (Feb 2025 beta) autonomously executes checkout on third-party sites without leaving the Amazon app.
- **Why Notable:** Amazon commands the dominant consumer buyer-agent position with 300M+ active Alexa users and $12B+ in AI-attributed incremental sales (2025). "Buy for Me" is the most widely-deployed autonomous checkout agent operating at production scale, and thus the primary real-world baseline for Pillar 1 (workflow execution) and Pillar 2 (pricing decision quality at scale). Amazon's court action against Perplexity Comet (March 2026) also establishes Amazon as the key platform gatekeeper for agentic commerce.
- **Discovery Source:** LOOP_00001_MARKET_ANALYSIS.md (Modern Retail / Digital Commerce 360 sourced)
- **Status:** PENDING

### OpenAI ChatGPT Instant Checkout (ACP)
- **Type:** Product / Platform
- **Brief:** OpenAI's consumer purchasing agent built on the Agents Commerce Protocol (ACP, co-developed with Stripe), deployed as "Instant Checkout" in ChatGPT in September 2025 and partially removed from ChatGPT in March 2026 following the OpenAI–Amazon strategic partnership ($50B investment, Feb 2026).
- **Why Notable:** First major LLM-native checkout agent deployed to 300M+ ChatGPT users, and the primary real-world implementation of the ACP protocol. Its partial rollback in March 2026 due to the Amazon deal is a significant market event showing how business partnerships can override protocol adoption. Directly relevant to Pillar 1 (agent commerce workflow execution) and Pillar 3 (ACP payment security and authorization flows).
- **Discovery Source:** LOOP_00001_MARKET_ANALYSIS.md (Orium / Grid Dynamics / Forrester sourced)
- **Status:** PENDING

### Perplexity Comet
- **Type:** Product / Platform
- **Brief:** Perplexity AI's autonomous shopping and web-browsing agent capable of executing multi-step research and purchase workflows on behalf of users. Subject to a March 2026 court injunction blocking its access to Amazon's marketplace.
- **Why Notable:** The most legally-tested buyer agent to date: Amazon's successful court order (March 2026) restricting Comet's marketplace access established the first major legal boundary for autonomous buyer agents. Comet's legal dimension creates unique Pillar 3 benchmarking context — compliance scenarios should include platform access restrictions, terms-of-service enforcement, and agent identity verification challenges. Also relevant to Pillar 1 multi-step sourcing across restricted environments.
- **Discovery Source:** LOOP_00001_MARKET_ANALYSIS.md (Decrypt / Forrester sourced)
- **Status:** PENDING

### Salesforce Agentforce
- **Type:** Product / Platform
- **Brief:** Salesforce's enterprise AI agent platform for building, deploying, and orchestrating autonomous agents across CRM, customer service, and procurement workflows. Positioned as the leading enterprise agentic AI platform (per MARKET_ANALYSIS.md competitive landscape).
- **Why Notable:** Agentforce is the enterprise-scale reference platform for agent orchestration with procurement and spend management use cases — defining what "enterprise-grade" autonomous buying looks like. Its built-in trust layer (guardrails, audit trails, permission controls) is directly relevant to Pillar 3 security and compliance scenario design. As a market leader, it sets the baseline against which BuyerBench Pillar 1 task complexity should be calibrated.
- **Discovery Source:** LOOP_00001_MARKET_ANALYSIS.md (Market Leaders section)
- **Status:** PENDING

### NegMAS (Negotiation Multi-Agent System)
- **Type:** Product / Platform (Open-Source Framework)
- **Brief:** Open-source Python framework (BSD 3-Clause, yasserfarouk/negmas on GitHub) for automated negotiation, multi-agent simulation, and tournament management. Serves as the backbone of the ANAC Automated Negotiation Leagues and is the primary open-source research platform for buyer-agent negotiation research.
- **Why Notable:** NegMAS is one of BuyerBench's explicitly named reference agents (`negmas` agent ID in CLAUDE.md). It provides a reference implementation of formal negotiation protocols (alternating offers, auction mechanisms, multilateral deal-making) directly applicable to Pillar 1 negotiation task scenarios. The ANAC 2025 tournament results provide empirical benchmarks for negotiation agent performance that BuyerBench can reference or replicate as ground truth.
- **Discovery Source:** LOOP_00001_MARKET_ANALYSIS.md (Open-Source / Research section; github.com/yasserfarouk/negmas)
- **Status:** PENDING

### Discovery Summary
- **Category:** Products & Platforms
- **Entities Found:** 5
- **Search Queries Used:**
  - "Amazon Alexa+ Buy for Me consumer buyer agent 2025 2026"
  - "OpenAI ChatGPT Instant Checkout ACP agent 2025 2026"
  - "Perplexity Comet shopping agent Amazon court ruling 2026"
  - "Salesforce Agentforce enterprise procurement orchestration"
  - "NegMAS negotiation MAS framework ANAC 2025"
- **Sources Checked:**
  - LOOP_00001_MARKET_ANALYSIS.md (primary synthesis source with linked external sources)
  - Modern Retail / Digital Commerce 360 (Amazon Rufus/Alexa+ / Buy for Me coverage)
  - Orium / Grid Dynamics blogs (ACP / ChatGPT Instant Checkout)
  - Decrypt / Forrester (Perplexity Comet legal case and Amazon partnership)
  - Salesforce corporate (Agentforce product pages — Market Leaders)
  - yasserfarouk/negmas GitHub (NegMAS documentation, licensing, ANAC integration)

---

## Research Papers - Discovered 2026-04-04

### ACES: What Is Your AI Agent Buying?
- **Type:** Research Paper
- **Brief:** Evaluation framework (Agentic e-CommercE Simulator) pairing a VLM shopping agent with a fully programmable mock e-commerce application to study AI agent purchasing biases in agentic commerce scenarios.
- **Why Notable:** The most directly relevant academic work to BuyerBench — systematically documents AI buyer agent biases including position bias, anchoring, decoy susceptibility, and choice homogeneity. Published arXiv 2508.02630 (Aug 2025). Provides empirical grounding for BuyerBench Pillar 2 bias test scenario design.
- **Discovery Source:** https://arxiv.org/abs/2508.02630
- **Status:** PENDING

### Evaluation and Benchmarking of LLM Agents: A Survey
- **Type:** Research Paper
- **Brief:** Comprehensive survey of evaluation methodologies for LLM-based agents, covering task design, metrics, environment types, and benchmark limitations across dozens of agent evaluation frameworks published through mid-2025.
- **Why Notable:** Provides the methodological foundation for BuyerBench's evaluation design. Directly applicable for validating the scoring approach across all three pillars. arXiv 2507.21504 (Jul 2025). Covers both capability benchmarks (Pillar 1) and behavioral evaluation designs (Pillar 2 bias testing).
- **Discovery Source:** https://arxiv.org/html/2507.21504v1
- **Status:** PENDING

### AgentBench: Evaluating LLMs as Agents
- **Type:** Research Paper
- **Brief:** Multi-dimensional LLM agent benchmark consisting of 8 distinct task environments (OS, DB, knowledge graphs, digital card games, lateral thinking puzzles, house-holding, web shopping, web browsing) to assess reasoning and decision-making ability. ICLR 2024.
- **Why Notable:** Established benchmark demonstrating that most LLMs perform significantly worse as agents than as pure text generators — with web shopping and web browsing tasks most relevant to BuyerBench Pillar 1 buyer workflow scenarios. arXiv 2308.03688. Provides baseline performance expectations for LLM-based buyer agents before fine-tuning.
- **Discovery Source:** https://arxiv.org/abs/2308.03688
- **Status:** PENDING

### WebArena: A Realistic Web Environment for Building Autonomous Agents
- **Type:** Research Paper
- **Brief:** Self-hosted realistic web benchmark comprising four simulated domains (e-commerce, social forums, collaborative code development, content management) with 812 templated tasks. Tests end-to-end web task completion including shopping and purchasing workflows.
- **Why Notable:** The e-commerce domain in WebArena provides a direct analog to BuyerBench Pillar 1 sourcing and purchasing scenarios. Establishes the standard methodology for realistic web-based agent evaluation: faithful simulation environments, templated task variants, and execution-grounded success criteria — all patterns BuyerBench adopts. arXiv 2307.13854 (2023).
- **Discovery Source:** https://webarena.dev/
- **Status:** PENDING

### WebShop: Towards Scalable Real-World Web Interaction with Grounded Language Agents
- **Type:** Research Paper
- **Brief:** Pioneering AI shopping agent benchmark (Princeton, NeurIPS 2022) with 1.18M real Amazon products and 12,087 crowd-sourced instructions. Agents must search, navigate, and purchase products matching user specifications. Established the first large-scale evaluation environment for language-grounded buyer agents.
- **Why Notable:** Foundational work establishing that web shopping is a valid and scalable evaluation environment for language agents. WebShop's reward structure (product attribute matching + pricing adherence) directly informs BuyerBench Pillar 1 scoring methodology. First paper to operationalize "buyer agent quality" as a measurable, reproducible metric. arXiv 2207.01206.
- **Discovery Source:** https://arxiv.org/abs/2207.01206
- **Status:** PENDING

### Discovery Summary
- **Category:** Research Papers
- **Entities Found:** 5
- **Search Queries Used:**
  - "AI buyer agent research papers evaluation benchmark 2024 2025 WebShop AgentBench"
  - "ACES agentic e-commerce simulator arXiv 2508.02630"
  - "LLM agent evaluation survey arXiv 2507.21504"
  - "WebArena WebShop AI agent web shopping benchmark NeurIPS"
- **Sources Checked:**
  - arXiv: 2508.02630 (ACES), 2507.21504 (LLM Agent Eval Survey), 2308.03688 (AgentBench), 2307.13854 (WebArena), 2207.01206 (WebShop)
  - LOOP_00001_MARKET_ANALYSIS.md (primary synthesis source citing ACES and LLM eval survey)
  - OpenReview: AgentBench ICLR 2024 paper page
  - WebArena project site (webarena.dev)
  - o-mega.ai: 2025 AI agent benchmarks guide
  - evidentlyai.com: 10 AI agent benchmarks overview

---

## Security & Compliance Frameworks - Discovered 2026-04-04

### PCI DSS v4.0
- **Type:** Security / Compliance Framework
- **Brief:** Payment Card Industry Data Security Standard version 4.0 (released March 2022, full enforcement April 2025) — the primary global standard governing secure handling of cardholder data, covering network security, access control, encryption, logging, and vulnerability management across all entities that store, process, or transmit card data.
- **Why Notable:** PCI DSS is the non-negotiable baseline for any AI buyer agent that executes card-based transactions. v4.0 introduces new authentication requirements (multi-factor authentication expanded to all CDE access), clarifies responsibilities for cloud and shared environments, and adds flexibility through customized implementations — all of which interact directly with agentic payment flows. Every Pillar 3 secure-transaction scenario in BuyerBench must be evaluated against PCI DSS compliance: correct sequencing of payment operations, secure credential handling, and network segmentation.
- **Discovery Source:** https://www.pcisecuritystandards.org/document_library/?category=pcidss&document=pci_dss
- **Status:** PENDING

### EMV 3-D Secure (3DS2)
- **Type:** Security / Compliance Framework (Authentication Protocol)
- **Brief:** EMV 3-D Secure version 2 (3DS2) is the industry-standard authentication protocol for card-not-present transactions, developed by EMVCo and adopted by all major card networks (Visa, Mastercard, Amex). It provides risk-based authentication, frictionless flows for low-risk transactions, and strong customer authentication (SCA) for high-risk ones — replacing the older 3DS1 / "Verified by Visa" redirect flow.
- **Why Notable:** AI buyer agents executing online card payments operate in the 3DS2 environment. Understanding when agents trigger friction (step-up challenges) vs. frictionless flows is critical for Pillar 3 authorization scenario design. The protocol also defines how merchants and issuers exchange data elements — agent identity, device fingerprint, behavioral signals — that are directly relevant to KYA (Know Your Agent) identity verification. Visa and Mastercard's agent payment protocols (Intelligent Commerce, Agent Pay) are built on top of EMV 3DS2 tokenization infrastructure.
- **Discovery Source:** https://www.emvco.com/emv-technologies/3-d-secure/
- **Status:** PENDING

### NIST AI Risk Management Framework (AI RMF 1.0)
- **Type:** Security / Compliance Framework (AI Governance)
- **Brief:** NIST AI Risk Management Framework version 1.0 (released January 2023) — a voluntary framework for organizations to identify, assess, and manage AI risks across the full AI lifecycle. Structured around four core functions: GOVERN, MAP, MEASURE, MANAGE. Widely adopted as the de facto AI governance reference for US federal agencies and increasingly referenced in private-sector AI procurement policies.
- **Why Notable:** NIST AI RMF is becoming the standard reference for enterprise AI compliance attestations — especially relevant to AI buyer agents operating in regulated procurement environments. The GOVERN function maps to Pillar 3 authorization and policy enforcement scenarios. The MEASURE function is directly applicable to BuyerBench's evaluation methodology: defining what "trustworthy AI buyer agent behavior" means and how to measure it quantitatively. Enterprise buyers (large companies evaluating AI procurement tools) will increasingly require AI RMF alignment.
- **Discovery Source:** https://airc.nist.gov/RMF
- **Status:** PENDING

### ISO/IEC 42001:2023 (AI Management System Standard)
- **Type:** Security / Compliance Framework (AI Governance)
- **Brief:** ISO/IEC 42001:2023 is the first international standard specifying requirements for establishing, implementing, maintaining, and continually improving an Artificial Intelligence Management System (AIMS) within an organization. Published December 2023, developed by ISO/IEC JTC 1/SC 42. Provides a certifiable framework (similar to ISO 27001 for information security) for responsible AI development and deployment.
- **Why Notable:** ISO 42001 provides organizations deploying AI buyer agents with a certifiable compliance pathway. Its requirements cover AI system objectives, risk treatment, data governance, and human oversight mechanisms — all of which map to BuyerBench Pillar 3 compliance scenarios. As enterprise procurement organizations face AI governance audits, ISO 42001 certification will increasingly be demanded of AI agent vendors (Procure AI, Omnea, Zycus). BuyerBench Pillar 3 should reference ISO 42001 controls when designing oversight and escalation scenarios.
- **Discovery Source:** https://www.iso.org/standard/77304.html
- **Status:** PENDING

### FATF Guidance on AML/CFT for Virtual Assets and AI Agents
- **Type:** Security / Compliance Framework (AML / Financial Crime)
- **Brief:** Financial Action Task Force (FATF) recommendations and guidance covering anti-money laundering (AML) and counter-financing of terrorism (CFT) obligations for virtual asset service providers (VASPs) and, increasingly, AI-driven financial agents. The "Travel Rule" (FATF Recommendation 16) requires VASPs to share originator/beneficiary information for transactions above $1,000/€1,000. FATF updated its guidance on virtual assets in 2021 and is actively developing guidance on AI's role in financial crime risk.
- **Why Notable:** AI buyer agents operating on crypto payment rails (x402 Coinbase protocol, digital currency checkouts) must comply with FATF's Travel Rule and AML/CFT obligations. This creates unique Pillar 3 scenarios: fraud detection for crypto-based agent transactions, AML screening within autonomous payment flows, and KYC/KYA verification requirements. The intersection of FATF obligations with agent autonomy (who is the "originator" when an AI agent sends crypto?) creates novel compliance challenges that BuyerBench can model as adversarial security scenarios.
- **Discovery Source:** https://www.fatf-gafi.org/en/topics/virtual-assets.html
- **Status:** PENDING

### Discovery Summary
- **Category:** Security & Compliance Frameworks
- **Entities Found:** 5
- **Search Queries Used:**
  - "PCI DSS v4.0 AI agent payment security compliance 2024 2025"
  - "EMV 3DS2 authentication protocol agentic payments card-not-present"
  - "NIST AI RMF 1.0 procurement AI governance risk management framework"
  - "ISO 42001 AI management system standard certification 2023 2024"
  - "FATF AML CFT virtual assets AI agents Travel Rule compliance"
- **Sources Checked:**
  - PCI Security Standards Council: pcisecuritystandards.org (PCI DSS v4.0 documentation)
  - EMVCo: emvco.com (EMV 3DS2 specification and overview)
  - NIST AI RMF: airc.nist.gov/RMF (framework documentation)
  - ISO: iso.org/standard/77304.html (ISO 42001:2023 standard page)
  - FATF: fatf-gafi.org (virtual assets guidance)
  - LOOP_00001_MARKET_ANALYSIS.md (Pillar 3 security context)

---

## ALL_CATEGORIES_COVERED

All five priority entity categories from `LOOP_00001_MARKET_ANALYSIS.md` have been discovered:

| Category | Target | Discovered | Status |
|----------|--------|------------|--------|
| Companies | 5–10 | 5 | ✓ COMPLETE |
| Protocols & Standards | 3–5 | 5 | ✓ COMPLETE |
| Products & Platforms | 5–10 | 5 | ✓ COMPLETE |
| Research Papers | 3–5 | 5 | ✓ COMPLETE |
| Security & Compliance Frameworks | 3–5 | 5 | ✓ COMPLETE |

**Total entities discovered: 25** (5 per category × 5 categories)
**Discovery completed: 2026-04-04 (Loop 10 — stall-break)**
