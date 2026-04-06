---
type: product
title: "Salesforce Agentforce"
created: 2026-04-05
tags:
  - ai-agent-platform
  - salesforce
  - enterprise
  - crm
  - procurement
  - agentic-commerce
  - pillar1
  - pillar2
  - pillar3
related:
  - '[[Procure-AI]]'
  - '[[Omnea]]'
  - '[[Zycus]]'
  - '[[INDEX]]'
---

# Salesforce Agentforce

> Salesforce's enterprise autonomous AI agent platform — from $2/conversation in 2024 to a full Agentic Enterprise License Agreement in 2026, with purpose-built buyer, supply chain, and import specialist agents for procurement workflows

## Overview

**Agentforce** is Salesforce's enterprise-grade autonomous AI agent platform, launched in September 2024 at Dreamforce. It enables organizations to build, deploy, and manage AI agents that execute multi-step business workflows autonomously — operating across Salesforce's full product suite (Sales Cloud, Service Cloud, Commerce Cloud, Marketing Cloud) and integrating with external systems via MuleSoft.

Unlike point-solution AI copilots, Agentforce agents are **goal-driven**: they receive a task objective, access relevant data via Salesforce Data Cloud, determine the appropriate sequence of actions, and execute — including handoff to a human when ambiguity or policy thresholds require it. Agents are persistent, can run asynchronously, and can initiate work proactively (not just respond to user prompts).

As of April 2026, the platform has shipped three distinct pricing models (Conversations → Flex Credits → AELA per-user), reflecting rapid evolution in how Salesforce and its customers understand where AI agent value accrues in enterprise workflows. Agentforce 360 — the current GA iteration — adds Agent Script (deterministic control language), Agentforce Voice, and Intelligent Context for unstructured data grounding.

> **BuyerBench relevance (Pillar 1):** Agentforce Buyer Agent and Supply Chain agents are direct reference implementations for Pillar 1 capability scenarios — B2B supplier discovery, purchase order automation, supplier onboarding, and multi-step procurement workflows. Agentforce's published agent taxonomy (goal → action plan → tool call → human escalation) maps directly onto BuyerBench's task completion and workflow accuracy metrics.

> **BuyerBench relevance (Pillar 2):** Agentforce's "Import Specialist Agent" (tariff impact modeling) is a real-world example of economically rational agent decision-making under uncertainty. BuyerBench Pillar 2 scenarios should test whether agents correctly propagate cost changes (tariffs, freight) through margin calculations — exactly what this agent claims to do.

> **BuyerBench relevance (Pillar 3):** Agentforce's least-privilege access model, Agent Script determinism controls, and compiled JSON audit trail are the enterprise baseline for Pillar 3 compliance. Scenarios should test whether agents enforce Salesforce-defined permission scopes when executing financial transactions, and whether they generate auditable trails of agent decisions.

## Quick Facts

| Attribute | Value |
|-----------|-------|
| Product Name | Agentforce (→ Agentforce 360, 2026) |
| Developer | Salesforce |
| Initial Launch | September 2024 (Dreamforce) |
| Current Version | Agentforce 360 (Spring '26 Release) |
| Underlying Models | Einstein AI (Salesforce-trained LLMs + external model support) |
| Pricing Models | $2/conversation OR Flex Credits ($0.10/action) OR AELA ($125+/user/month) |
| Key Procurement Agent | Buyer Agent (B2B purchasing), Import Specialist Agent (tariff analysis) |
| Integration Foundation | Salesforce Data Cloud + MuleSoft + Slack |
| Governance Standard | Compiled JSON agents, least-privilege access, Agent Script determinism |
| NVIDIA Partnership | GTC 2026 — NVIDIA enterprise AI agent platform, Salesforce among 17 adopters |

## Agent Types

### Pre-Built Agents

Salesforce ships a library of purpose-built agents for common enterprise functions:

| Agent | Domain | Capability |
|-------|--------|------------|
| **Buyer Agent** | B2B procurement | Helps buyers find products, make purchases, and track orders via chat or within sales portals |
| **Import Specialist Agent** | Trade compliance | Calculates duties and freight costs; models margin impact of tariff changes in real time |
| **Merchant Agent** | Commerce | Manages e-commerce catalog operations, promotions, and buyer interactions |
| **Customer Service Agent** | Support | Resolves tier-1 support cases, escalates with context |
| **Campaign Optimizer Agent** | Marketing | Manages campaign performance and audience adjustments |
| **Supply Chain Agent** | Operations | Orchestrates mid- and back-office processes: procurement, supplier onboarding, warranty claims |
| **Sales Development Agent** | CRM | Qualifies leads, books meetings, drafts personalized outreach |

### Custom Agents via Agentforce Builder

Organizations can build proprietary agents using **Agentforce Builder** — a unified development environment with three authoring modes:
1. **Conversational workspace** — describe the agent in natural language; AI generates the initial configuration
2. **Document-like editor** — refine instructions, topics, and actions with autocomplete and structured templates
3. **Agent Script (pro-code)** — write deterministic control flows using Agentforce's scripting language

Every agent compiles into a **portable JSON artifact** for version control, deployment, and audit — enabling governance workflows identical to software releases.

## Procurement and Purchasing Use Cases

### Buyer Agent (B2B Purchasing)

The **Buyer Agent** is Salesforce's direct answer to the AI buyer agent category. Deployed within B2B Commerce Cloud portals or via chat interface, it enables business buyers to:
- Search and compare products across a supplier catalog using natural language
- Initiate and track purchase orders autonomously
- Escalate to a human procurement manager when approval thresholds are exceeded
- Surface order history, delivery status, and re-order recommendations

The Buyer Agent operates within the buyer's Salesforce-defined permission scope — it cannot initiate purchases above the user's approval authority without triggering a human-in-the-loop escalation.

### Agentforce Supply Chain

**Agentforce Supply Chain** targets the operational layer of procurement:
- Automates supplier onboarding (document collection, vendor verification, contract routing)
- Manages warranty claims and returns workflows
- Orchestrates cross-functional approval processes (finance, legal, operations) for large-ticket purchases
- Generates procurement analytics and spend reports

### Import Specialist Agent (Tariff and Trade Compliance)

Launched in response to 2025–2026 global tariff volatility, the **Import Specialist Agent**:
- Ingests tariff schedules and freight data in real time
- Calculates landed cost (duties + freight + insurance) for specific product categories
- Models margin sensitivity: *"if tariffs increase by 15%, what happens to gross margin on this product line?"*
- Generates scenario comparisons for sourcing decisions (domestic vs. international supplier)

This agent directly targets procurement decisions that would otherwise require specialist trade consultant engagement.

### Scope 3 and Emissions Procurement

Agentforce integrates with **Salesforce Net Zero Cloud** to surface emissions data alongside procurement decisions, enabling buyers to factor supplier carbon footprint into sourcing choices — a Pillar 2 multi-criteria optimization scenario.

## Pricing

Salesforce has shipped **three distinct pricing models** for Agentforce since launch — an unusually rapid pricing evolution that reflects ongoing calibration of enterprise AI agent value.

### Model 1: Conversations ($2/conversation) — Original Launch Model

- Flat fee per 24-hour conversation session between agent and user
- Simple to budget; well-suited for customer-facing bot deployments
- Poorly fits internal workflow automation where a "conversation" may span days of async execution
- Still available as of April 2026 but being phased out in favor of Flex Credits

### Model 2: Flex Credits ($0.10/action) — Introduced May 2025

- Launched May 15, 2025 as Salesforce's recommended model for new deployments
- **1 standard action = 20 credits; credits purchased at $500 per 100,000**
- Effective cost: $0.10 per agent action (e.g., query a record, send an email, call an external API)
- Aligns cost to value: organizations pay for work done, not for time elapsed
- **Constraint**: Flex Credits and Conversations pricing cannot coexist in the same Salesforce org — organizations must choose one model

### Model 3: Agentic Enterprise License Agreement (AELA) — Late 2025

- Per-user license starting at **$125/user/month**, scaling by tier and edition
- "Digital workforce" is included in the seat price — agents become a bundled capability rather than a consumption add-on
- Designed for enterprises deploying Agentforce broadly across multiple departments
- Simplified procurement: one contract, predictable cost, no per-action metering

### Pricing Summary

| Model | Unit | Effective Cost | Best For |
|-------|------|----------------|----------|
| Conversations | Per 24-hr session | $2/conversation | Customer-facing chat bots |
| Flex Credits | Per agent action | $0.10/action | Workflow automation, internal use |
| AELA | Per user/month | $125+/user | Enterprise-wide deployment |

> **Note for BuyerBench:** The existence of three concurrent pricing models is itself a Pillar 2 economic scenario — procurement agents evaluating Salesforce must select the optimal pricing model for their use case, and the decision is non-trivial (a high-volume internal agent is dramatically cheaper under AELA than Flex Credits at scale).

## Integration Ecosystem

### Core Salesforce Platform

Agentforce is **native to Salesforce** — agents have zero-integration access to:
- **Sales Cloud** — CRM data: accounts, contacts, opportunities, purchase history
- **Service Cloud** — Case management, knowledge bases, SLA policies
- **Commerce Cloud** — B2B and B2C product catalogs, pricing, order management
- **Marketing Cloud** — Campaign data, customer segments, channel preferences
- **Net Zero Cloud** — Emissions data for ESG-aware procurement

### Data Cloud (Unified Data Layer)

**Data Cloud** provides agents with a real-time, unified customer and supplier data layer:
- Harmonizes data from Salesforce + external systems into a single semantic layer
- Enables "Intelligent Context" — grounding agents in unstructured documents (contracts, emails, PDFs) alongside structured CRM data
- Powers relevance ranking for product discovery and supplier recommendations

### MuleSoft (External Integration)

**MuleSoft** is Agentforce's bridge to non-Salesforce systems:
- Connects agents to ERP systems (SAP, Oracle), financial platforms, logistics APIs
- Enables agents to execute procurement workflows that span Salesforce + external systems
- Exposes external APIs as Agentforce actions without custom code

### Slack

Salesforce-owned **Slack** serves as the primary asynchronous interface for Agentforce in enterprise deployments:
- Agents surface in Slack channels and DMs as conversational participants
- Procurement approvals, status updates, and escalations flow through Slack
- Human-in-the-loop checkpoints are implemented as Slack approval messages

### NVIDIA (GTC 2026 Partnership)

At GTC 2026, NVIDIA launched an enterprise AI agent platform with Salesforce as one of 17 launch adopters — integrating Agentforce with NVIDIA's accelerated compute infrastructure for latency-sensitive agentic workflows.

### AppExchange Procurement Extensions

The Salesforce AppExchange hosts native procurement software packages (e.g., Coupa, Jaggaer, Ivalua connectors) that extend Agentforce's source-to-pay reach to specialized procurement suite capabilities.

## Limitations

| Limitation | Detail |
|------------|--------|
| **Salesforce-org dependency** | Agentforce requires an existing Salesforce org — it is not a standalone procurement platform. Organizations not already on Salesforce face significant adoption cost. |
| **Pricing model lock-in** | Flex Credits and Conversations cannot coexist in the same org. Switching models requires a contract change. |
| **Per-user AELA cost** | $125+/user/month is steep for small teams. At 100 users, AELA = $150K/year before base Salesforce licensing. |
| **No native payment rail** | Agentforce does not include a payment execution layer — it can initiate purchase orders but relies on external payment systems for settlement. Contrast with Skyfire (KYAPay) or ACP (Stripe-native). |
| **Customization complexity** | While Agentforce Builder lowers the floor, production-grade custom agents with Agent Script and complex MuleSoft flows still require Salesforce-certified developers. |
| **Ecosystem monoculture risk** | Deep integration across Sales/Service/Commerce Cloud creates lock-in — Agentforce agents are not portable to non-Salesforce environments. |
| **Agent action cost accumulates** | Under Flex Credits, high-volume internal workflows (e.g., 10,000 daily supplier catalog queries) can exceed AELA cost quickly, requiring careful capacity planning. |

## BuyerBench Pillar Relevance

### Pillar 1 — Agent Intelligence and Operational Capability

Agentforce's **Buyer Agent** and **Supply Chain Agent** are the most direct enterprise reference implementations for BuyerBench Pillar 1 scenarios:

- **Supplier discovery**: Buyer Agent's natural language product search across a B2B catalog mirrors BuyerBench supplier discovery tasks
- **Multi-step workflow execution**: Agentforce's goal → action plan → tool call loop is structurally identical to BuyerBench's scenario execution model
- **Human-in-the-loop escalation**: Agentforce's approval authority thresholds are a real-world reference for Pillar 1 workflow handoff scenarios
- **Supplier onboarding automation**: Supply Chain Agent's vendor verification workflow maps to BuyerBench's supplier qualification tasks

The **Import Specialist Agent** is particularly relevant as a Pillar 1 + 2 hybrid — it executes a multi-step calculation workflow (Pillar 1) and produces an economically rational sourcing recommendation under changing cost conditions (Pillar 2).

### Pillar 2 — Economic Decision Quality and Behavioral Robustness

Agentforce exposes several economically rich scenarios for Pillar 2 testing:

- **Pricing model selection**: Three concurrent pricing models for the same platform — agents must correctly identify the optimal model for a given workload volume (framing and anchoring bias test)
- **Tariff scenario modeling**: Import Specialist Agent's margin sensitivity analysis is a reference for multi-variable economic optimization under uncertainty
- **Scope 3 vs. cost tradeoff**: Net Zero Cloud integration creates a multi-criteria optimization scenario where agents balance supplier cost against emissions — a real-world instance of competing economic and non-economic objectives
- **Approval authority thresholds**: Buyer Agent's escalation logic is a policy compliance scenario — does an agent correctly respect spending limits even when a lower-cost option requires exceeding authority?

### Pillar 3 — Security, Compliance, and Market Readiness

Agentforce's enterprise governance architecture is a **positive reference implementation** for Pillar 3:

- **Least-privilege access**: Agents operate within the permission scope of the initiating user — a direct implementation of the principle BuyerBench Pillar 3 scenarios test
- **Compiled JSON audit trail**: Every agent invocation produces an auditable, versioned artifact — the target behavior for BuyerBench's "does the agent maintain an audit trail?" scenarios
- **Agent Script determinism**: Ability to define deterministic control flows for financially sensitive operations (e.g., "always require human approval for orders >$10K") models the policy enforcement layer BuyerBench Pillar 3 tests
- **Shared responsibility model**: Salesforce's "we provide the platform controls; you configure the governance" model is the enterprise baseline for Pillar 3 compliance scenarios

**Gap**: Agentforce has **no native payment rail**. For BuyerBench scenarios requiring end-to-end payment execution (not just PO issuance), Agentforce would need to integrate with an external payment layer (Stripe, Skyfire, AP2, etc.) — making it relevant for testing whether procurement agents correctly detect and handle the boundary between purchase authorization and payment settlement.

## Related Entities

- [[Procure-AI]] — AI-native procurement automation competitor; 50+ autonomous agents vs. Agentforce's CRM-native approach; no Salesforce org dependency
- [[Omnea]] — AI SRM/procurement orchestration competitor focused on vendor onboarding and cross-functional approval workflows — overlapping with Agentforce Supply Chain
- [[Zycus]] — Established source-to-pay suite with Merlin ANA autonomous negotiation agent; enterprise procurement incumbent that Agentforce competes with in large enterprise accounts
- [[Skyfire]] — Provides the payment rail layer (KYAPay) that Agentforce lacks; an Agentforce + Skyfire integration would create a full procurement-to-payment agentic stack

## Sources

1. [Agentforce Pricing — Salesforce](https://www.salesforce.com/agentforce/pricing/) — Accessed 2026-04-05
2. [Salesforce Introduces Flexible Agentforce Pricing — Salesforce Press Release](https://www.salesforce.com/news/press-releases/2025/05/15/agentforce-flexible-pricing-news/) — May 15, 2025
3. [Salesforce Agentforce Credits & Cost Model: Complete Guide 2026 — jitendrazaa.com](https://www.jitendrazaa.com/blog/salesforce/salesforce-agentforce-credits-cost-model-complete-guide-2026/) — Accessed 2026-04-05
4. [Agentforce Pricing Update Q3 2025: Flex Credits — Aquiva Labs](https://aquivalabs.com/blog/agentforce-pricing-gets-a-long-overdue-fix-flex-credits-are-now-live/) — Accessed 2026-04-05
5. [The Doomed Evolution of Salesforce's Agentforce Pricing — Monetizely](https://www.getmonetizely.com/blogs/the-doomed-evolution-of-salesforces-agentforce-pricing) — Accessed 2026-04-05
6. [Agentforce Supply Chain — Salesforce](https://www.salesforce.com/agentforce/agentforce-supply-chain/) — Accessed 2026-04-05
7. [Amid Global Trade Turmoil, an AI Agent Can Help Businesses Respond — Salesforce](https://www.salesforce.com/news/stories/agentic-ai-for-tariffs/) — Accessed 2026-04-05
8. [Spring '26 Release: 10 Tools to Help Build an Agentic Enterprise — Salesforce](https://www.salesforce.com/news/stories/spring-2026-product-release-announcement/) — Accessed 2026-04-05
9. [4 Critical Features for Agentforce Architecture in 2026 — Salesforce Ben](https://www.salesforceben.com/4-critical-features-for-agentforce-architecture-in-2026/) — Accessed 2026-04-05
10. [Agentforce in 2026: What's New — Salesforce Monday](https://salesforcemonday.com/2026/01/29/agentforce-january-2026-updates-features/) — Accessed 2026-04-05
11. [NVIDIA Launches Enterprise AI Agent Platform — VentureBeat](https://venturebeat.com/technology/nvidia-launches-enterprise-ai-agent-platform-with-adobe-salesforce-sap-among) — Accessed 2026-04-05
12. [Explore Agentforce: Your Guide to Autonomous Agents — Salesforce Trailhead](https://trailhead.salesforce.com/content/learn/modules/agentforce-agents-quick-look/discover-agentforce-agents) — Accessed 2026-04-05
13. [10 High-Impact Use Cases for Salesforce Agentforce in 2026 — Focus on Force](https://focusonforce.com/blog/10-high-impact-use-cases-for-salesforce-agentforce-in-2026/) — Accessed 2026-04-05

---
*Last updated: 2026-04-05*
