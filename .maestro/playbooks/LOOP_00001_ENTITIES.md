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
- **Status:** PENDING

### Zycus
- **Type:** Company
- **Brief:** Global source-to-pay suite with agentic AI capabilities including Merlin Intake agent and Merlin Autonomous Negotiation Agent (ANA).
- **Why Notable:** One of the first established procurement vendors to deploy an *autonomous negotiation agent* (Merlin ANA) — directly relevant to Pillar 1 (negotiation task scenarios) and Pillar 2 (economic decision quality). The ANA represents a commercial reference implementation of agent-driven price negotiation worth profiling and comparing against NegMAS.
- **Discovery Source:** https://www.zycus.com/
- **Status:** PENDING

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
