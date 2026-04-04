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
