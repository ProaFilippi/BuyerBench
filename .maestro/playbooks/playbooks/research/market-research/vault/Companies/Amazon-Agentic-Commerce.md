---
type: company
title: "Amazon Agentic Commerce"
created: 2026-04-06
tags:
  - amazon
  - platform
  - ai-agents
  - cloud
  - e-commerce
  - pricing
  - bedrock
  - nova
  - supply-chain
  - b2b
  - pillar1
  - pillar2
  - pillar3
related:
  - '[[Amazon-Rufus-BuyForMe]]'
  - '[[ACP]]'
  - '[[OpenAI-Agent-Platform]]'
  - '[[INDEX]]'
---

# Amazon Agentic Commerce

> Amazon's end-to-end agentic commerce stack: Nova foundation models → Bedrock Agents orchestration → AgentCore managed runtime → Amazon Business procurement tools → Rufus/Buy for Me/Alexa+ consumer layer — the most vertically integrated AI buyer ecosystem in the world as of 2026

## Overview

Amazon has assembled the broadest agentic commerce stack of any single company: it operates on both sides of the transaction (as marketplace operator **and** as AI agent platform provider), controls the cloud infrastructure (AWS/Bedrock), ships its own foundation models (Nova family), provides the agent runtime (AgentCore), and deploys consumer-facing buyer agents (Rufus, Buy for Me, Alexa+) that transact on its own marketplace. No other company simultaneously builds the AI model, the agent orchestration layer, the payment infrastructure, **and** owns the inventory and marketplace being transacted against.

Amazon's agentic commerce strategy bifurcates into two tracks:

1. **B2B / Enterprise Track (AWS)**: Amazon Bedrock, Nova models, AgentCore, and Amazon Business AI tools — enabling enterprises and developers to build procurement agents, supply chain automation, and buyer workflows on AWS infrastructure.
2. **Consumer Track (Retail)**: Rufus (product discovery), Buy for Me (cross-site autonomous checkout), and Alexa+ (voice-native agentic assistant) — deployed to 300M+ users against Amazon's own marketplace and external retailers.

The Feb 2026 strategic partnership with OpenAI ($50B framing) and the Mar 2026 injunction against Perplexity Comet confirm Amazon's intent to control which AI agents are permitted to transact against its marketplace — making the company simultaneously the largest agentic commerce enabler and the most consequential platform gatekeeper.

> **BuyerBench relevance (Pillar 1):** Amazon Business AI tools (Assistant, Savings Insights, Anomaly Monitoring) and AWS Supply Chain AI agents are direct reference implementations for Pillar 1 capability scenarios — autonomous supplier filtering, catalog search, spend optimization, and multi-step procurement workflows at enterprise scale.

> **BuyerBench relevance (Pillar 2):** Amazon Business Savings Insights and Spend Anomaly Monitoring test economically rational agent behavior under volume discounts, Subscribe & Save substitutions, and pattern-based spend optimization — each a Pillar 2 scenario type.

> **BuyerBench relevance (Pillar 3):** The Mar 2026 injunction establishes the legal precedent that **platform authorization ≠ user consent** — Perplexity's agent had user authorization but not Amazon's platform authorization. This is the defining Pillar 3 scenario: does a buyer agent enforce the distinction between "the user approved this action" and "the destination platform permits this agent to transact"?

## Quick Facts

| Attribute | Value |
|-----------|-------|
| Parent Company | Amazon.com, Inc. |
| Agentic AI Platform | Amazon Bedrock + AgentCore |
| Foundation Models | Amazon Nova family (Micro, Lite, Pro, Premier, Act) |
| Consumer Agents | Rufus (discovery), Buy for Me (checkout), Alexa+ (voice) |
| Enterprise Procurement | Amazon Business AI Assistant, Savings Insights, Anomaly Monitoring |
| B2B Marketplace GMV | $35B+ (Amazon Business, 2024) |
| Consumer Agent Users | 300M+ (Rufus) |
| Key Strategic Move | OpenAI partnership (Feb 2026, $50B); Perplexity injunction (Mar 2026) |
| Agent Runtime | AgentCore — CPU-based billing, no idle charges |
| AWS Marketplace | AI Agents & Tools solution page launched 2025 |

## Key Products

### 1. Amazon Nova Model Family

Amazon Nova is Amazon's proprietary foundation model family, launched at AWS re:Invent 2024. Nova models are the inference backbone for all Amazon agentic commerce products and are the only models available at a discount in Amazon Bedrock's on-demand tier.

| Model | Best For | Input ($/M tokens) | Output ($/M tokens) |
|-------|----------|-------------------|-------------------|
| Nova Micro | Fastest text tasks, lowest cost | $0.035 | $0.14 |
| Nova Lite | Multimodal (text + image + video) | $0.060 | $0.24 |
| Nova Pro | Complex reasoning, agentic tasks | $0.800 | $3.20 |
| Nova Premier | Highest capability, long context | Contact AWS | Contact AWS |
| Nova Act | Browser UI automation (agent-specific) | See AgentCore pricing | — |

Nova Act specifically targets agentic UI workflows — browser-based task automation with reported 90%+ reliability on production enterprise workflows (e.g., CRM record updates, order status checks). Nova Act underpins **Buy for Me** and is available as a managed service via AgentCore.

### 2. Amazon Bedrock Agents

Amazon Bedrock Agents is the orchestration layer that enables developers to build multi-step AI workflows using Nova or third-party models (Anthropic Claude, Meta Llama, Mistral, etc.). Key architectural properties:

- **Reasoning traces**: Agents expose intermediate thoughts; each thought step incurs inference charges
- **Cost multiplier effect**: A single user query may trigger 5–10× the raw token consumption of a direct model call, because the agent reasons, plans, calls tools, and synthesizes — paying for each step
- **Knowledge Bases**: RAG integration adds OpenSearch Serverless costs ($345/month minimum for storage alone)
- **Bedrock Flows**: Workflow orchestration at $0.035 per 1,000 node transitions (billed from Feb 2025)
- **Guardrails**: Safety filtering layer with its own per-invocation charge

### 3. Amazon Bedrock AgentCore

Launched 2025, AgentCore is Amazon's managed runtime for production agent deployment — analogous to Lambda for agentic workloads. It decouples agent **execution infrastructure** from model inference pricing:

**AgentCore Components:**
| Component | Pricing Model |
|-----------|--------------|
| Runtime | $0.0895/vCPU-hour (billed on actual CPU use; idle = free) |
| Gateway | Per 1,000 API calls |
| Memory | Per memory record creation + retrieval |
| Identity | No charge via AgentCore Runtime |
| Browser | Per browser-session hour |
| Code Interpreter | Per execution |

New AWS customers receive $200 free-tier credits.

### 4. Amazon Business AI Tools (B2B Procurement)

Amazon Business is Amazon's B2B marketplace ($35B+ GMV), and as of late 2025, it deploys three AI agent capabilities for enterprise procurement:

**Amazon Business Assistant**
- Conversational procurement guidance (powered by Amazon Bedrock)
- Account configuration optimization, category compliance flagging
- Analyzes purchase patterns; recommends efficiency improvements
- "Always-on procurement assistant" with deep Amazon Business knowledge

**Savings Insights**
- AI analysis of order histories, negotiated terms, supplier catalogs, and order frequency
- Identifies missed savings: quantity discounts, Subscribe & Save substitutions, lower-cost alternates
- No additional charge (bundled with Amazon Business account)

**Spend Anomaly Monitoring**
- Detects irregular spend: unusual categories, repeated orders, transactions structured to bypass approval thresholds
- Provides alerts without locking purchasing controls (compliance + flexibility balance)
- Enterprise governance layer for autonomous procurement agents

**Industrial Manufacturing Agent (Early 2026, Select Manufacturers)**
- AI agents for: order management, supplier quality oversight, demand forecasting
- Predicts inventory disruptions; recommends parts reallocation or expedited shipments
- Powered by Amazon Bedrock, released to select manufacturers Q1 2026

### 5. AWS Supply Chain AI

Amazon Web Services ships dedicated supply chain AI capabilities for enterprises building on AWS infrastructure:

- **Agentic AI for logistics**: Real-time data aggregation from ERP, TMS, WMS, and customer portals
- **Instant inquiry response**: Agents answer supply chain status questions without human routing
- **Expedite cost reduction**: Reported 3–5% reduction in total logistics spend via AI-assisted exception management
- **Demand forecasting model**: AWS's proprietary supply chain foundation model integrates time-bound variables (weather, local events, holiday schedules) for last-mile demand prediction

### 6. Consumer Agentic Commerce Layer

The consumer track of Amazon's agentic commerce strategy is documented in detail in [[Amazon-Rufus-BuyForMe]]:

- **Rufus**: AI shopping assistant, 300M+ users, embedded in Amazon app — product discovery, comparison, recommendation
- **Buy for Me**: Cross-site autonomous purchase agent — uses Nova+Claude models to buy from external retailers via Amazon's mobile app; does NOT share user credentials with third-party retailers
- **Alexa+**: Voice-native agentic assistant with GA in Feb 2026 — ambient procurement, household restocking, subscription management

## Agentic Commerce Strategy

### Vertical Integration

Amazon's strategy is uniquely vertical: it controls the model (Nova), the orchestration (Bedrock Agents), the runtime (AgentCore), the marketplace (Amazon.com + Amazon Business), and the consumer agent layer (Rufus / Buy for Me / Alexa+). This creates:

- **Data flywheel advantage**: Consumer transaction data feeds Nova model training, which improves agent quality, which drives more transactions
- **Platform leverage**: As marketplace operator, Amazon can define which third-party agents are permitted to transact — as demonstrated by the Perplexity injunction

### Partnership Strategy

- **OpenAI Partnership (Feb 2026)**: $50B strategic framing; OpenAI models available in Amazon Bedrock; signals co-opetition — Amazon and OpenAI compete in consumer agents but cooperate on cloud infrastructure
- **AWS Marketplace AI Agents & Tools page**: Enables third-party procurement agent vendors (Procure AI, Fairmarkit, etc.) to distribute via AWS — keeping the ecosystem on Amazon's infrastructure

### Platform Gatekeeper Position

The Mar 2026 injunction against Perplexity Comet (blocked from accessing Amazon.com for autonomous purchasing on behalf of users) is the most consequential agentic commerce legal event of 2026. Amazon's legal theory: even if a user explicitly authorizes an AI agent to purchase on their behalf, the agent must also have Amazon's platform authorization to access Amazon's systems — user consent alone is insufficient. This directly challenges the general consumer agent model (where agent authorization derives from user delegation).

## Pricing Summary

### Amazon Bedrock On-Demand (Most Relevant for Agent Workflows)

| Model | Input ($/M tokens) | Output ($/M tokens) | Recommended Use |
|-------|--------------------|--------------------|-|
| Nova Micro | $0.035 | $0.14 | High-volume text classification, routing |
| Nova Lite | $0.060 | $0.24 | Multimodal product search, catalog processing |
| Nova Pro | $0.80 | $3.20 | Complex procurement reasoning, multi-step planning |
| Claude 3.5 Haiku (via Bedrock) | ~$0.80 | ~$4.00 | Anthropic-class reasoning via AWS |
| Claude 3.5 Sonnet (via Bedrock) | ~$3.00 | ~$15.00 | Highest-quality agent reasoning via AWS |

> **Agent cost multiplier warning**: A "1 token" user query to a Bedrock Agent typically results in 5–10× that in actual inference consumption across reasoning traces, tool calls, and synthesis steps. Budget accordingly.

### Bedrock Infrastructure

| Service | Pricing |
|---------|---------|
| Bedrock Flows | $0.035 per 1,000 node transitions |
| AgentCore Runtime | $0.0895/vCPU-hour (actual usage only) |
| AgentCore Gateway | Per 1,000 API calls |
| Knowledge Bases (OpenSearch) | $345/month minimum storage |
| Amazon Business AI tools | Bundled (no additional charge) |

### Provisioned Throughput

For production workloads, Provisioned Throughput offers reserved model capacity at negotiated rates, eliminating per-token costs in exchange for committed monthly usage — preferred by enterprises with predictable agent workload volumes.

## Strategic Moves

### OpenAI + Amazon Strategic Partnership (Feb 2026)
OpenAI and Amazon announced a $50B strategic partnership framing OpenAI models as first-class citizens in Amazon Bedrock and Amazon's infrastructure as a preferred cloud for OpenAI workloads. For agentic commerce, this means:
- OpenAI's GPT-4o / o3 models available via Bedrock on-demand
- OpenAI's Operator and Responses API accessible within AWS-governed infrastructure
- Potential for Amazon marketplace data to improve OpenAI agent capabilities

### Perplexity Comet Injunction (Mar 2026)
Amazon won a preliminary injunction blocking Perplexity Comet from autonomously accessing Amazon.com on behalf of users. Legal theory: CFAA (Computer Fraud and Abuse Act) violation — accessing Amazon's systems without Amazon's authorization, even with user consent. The case is on appeal as of Apr 2026.

**BuyerBench Pillar 3 Implication**: This injunction defines the **dual-authorization requirement** for agentic commerce — buyer agents must obtain BOTH user authorization AND destination-platform authorization before executing transactions. Scenarios testing whether buyer agents enforce this distinction are direct Pillar 3 content.

## Limitations

| Limitation | Detail |
|------------|--------|
| **Platform gatekeeper risk** | Amazon may use the Perplexity precedent to block competitor AI agents from transacting on Amazon.com, concentrating agentic commerce on Amazon-endorsed agents only |
| **Cost multiplier opacity** | Bedrock Agent pricing is non-intuitive — the multiplier effect from reasoning traces and tool calls is difficult to predict, creating budget risk for enterprise deployments |
| **Vendor lock-in** | AgentCore, Knowledge Bases, and Bedrock Flows create deep AWS dependency; migrating an agent workflow to Azure/GCP is non-trivial |
| **No native payment rail** | Amazon Bedrock and AgentCore have no payment execution layer — enterprise procurement agents must integrate external payment systems (Stripe, Skyfire, AP2) for settlement |
| **Consumer / Enterprise gap** | Amazon Business AI tools are comparatively basic (assistant + savings insights) relative to the sophistication of Nova Act — the advanced agentic capabilities are primarily developer/cloud-facing, not enterprise-procurement-facing |
| **OpenSearch cost trap** | Knowledge Bases deployments incur $345+/month OpenSearch storage cost regardless of usage — a hidden fixed cost that surprises developers building RAG-based procurement agents |

## BuyerBench Pillar Relevance

### Pillar 1 — Agent Intelligence and Operational Capability

Amazon's agentic commerce stack provides multiple reference benchmarks for Pillar 1:

- **Supplier discovery**: Amazon Business catalog search via AI Assistant mirrors BuyerBench supplier discovery tasks at scale (300M+ product SKUs)
- **Multi-step procurement workflows**: Bedrock Agents' orchestration loop (reason → plan → tool call → synthesize) is structurally identical to BuyerBench's scenario execution model
- **Supply chain exception handling**: AWS Supply Chain AI agents (ERP/TMS/WMS aggregation, expedite cost reduction) are real-world reference implementations for Pillar 1 exception-handling tasks
- **Industrial Manufacturing Agent**: Order management + supplier quality oversight + demand forecasting represents a complete Pillar 1 workflow in production

### Pillar 2 — Economic Decision Quality and Behavioral Robustness

- **Savings Insights scenarios**: Can a buyer agent correctly identify Subscribe & Save substitutions, quantity discount thresholds, and lower-cost alternates? These are structurally identical to BuyerBench price-optimization scenarios
- **Spend Anomaly detection**: Can a buyer agent detect when it is being used to structure transactions that circumvent approval thresholds? This is a Pillar 2 behavioral integrity scenario
- **Nova model selection**: Choosing the right Nova model tier (Micro vs. Lite vs. Pro) for a procurement task is itself an economic optimization scenario — over-specifying (using Pro where Micro suffices) wastes budget; under-specifying produces lower-quality decisions

### Pillar 3 — Security, Compliance, and Market Readiness

Amazon's agentic commerce posture generates several Pillar 3 scenario types:

- **Dual-authorization requirement (critical)**: The Perplexity injunction establishes that user authorization ≠ platform authorization. BuyerBench scenarios should test whether buyer agents check destination-platform permission before executing cross-site purchases
- **Agent identity on Amazon marketplace**: Does an agent correctly identify itself as an AI agent (vs. masquerading as a human browser) when transacting on Amazon Business?
- **Spend anomaly self-detection**: Amazon's Anomaly Monitoring detects transactions structured to bypass approval thresholds — BuyerBench Pillar 3 tests whether buyer agents enforce their own approval-limit rules
- **No payment rail = PO-only scope**: Since Bedrock/AgentCore have no payment execution layer, Pillar 3 scenarios testing full payment completion cannot use native Amazon infrastructure — agents must correctly identify the boundary between PO issuance and payment settlement

## Related Entities

- [[Amazon-Rufus-BuyForMe]] — Consumer agent layer (Rufus, Buy for Me, Alexa+); 300M users; Perplexity injunction details
- [[ACP]] — OpenAI's Agentic Commerce Protocol; Amazon is a strategic partner (Feb 2026) and one of the key platforms ACP-enabled agents would transact against
- [[OpenAI-Agent-Platform]] — Strategic partner (Feb 2026); OpenAI models available via Amazon Bedrock; joint agentic commerce ecosystem
- [[AP2-UCP]] — Google's competing payment protocol; Amazon Business and AWS are notably absent from AP2's 60+ partner list — competitive gap
- [[Skyfire]] — Provides the payment rail layer that Amazon Bedrock/AgentCore lacks; Skyfire + Bedrock = complete procurement-to-payment stack
- [[Perplexity-Comet]] — Enjoined competitor; the Mar 2026 injunction defines Pillar 3 dual-authorization requirements

## Sources

1. [Amazon Bedrock Pricing — AWS](https://aws.amazon.com/bedrock/pricing/) — Accessed 2026-04-06
2. [Amazon Bedrock AgentCore Pricing — AWS](https://aws.amazon.com/bedrock/agentcore/pricing/) — Accessed 2026-04-06
3. [Amazon Nova Pricing — AWS](https://aws.amazon.com/nova/pricing/) — Accessed 2026-04-06
4. [Amazon introduces Nova models and Nova Act — About Amazon](https://www.aboutamazon.com/news/aws/aws-agentic-ai-amazon-bedrock-nova-models) — Accessed 2026-04-06
5. [Build reliable AI agents with Amazon Nova Act — AWS Blog](https://aws.amazon.com/blogs/aws/build-reliable-ai-agents-for-ui-workflow-automation-with-amazon-nova-act-now-generally-available/) — Accessed 2026-04-06
6. [Amazon Business Unveils Next Generation AI Solutions — BusinessWire](https://www.businesswire.com/news/home/20251112781484/en/Amazon-Business-Unveils-Next-Generation-AI-Solutions-to-Help-Organizations-and-Small-Businesses-Save-Time-and-Money) — Nov 12, 2025
7. [Amazon Business pushes AI deeper into procurement at Reshape 2025 — Digital Commerce 360](https://www.digitalcommerce360.com/2025/11/13/amazon-business-ai-procurement-reshape-2025-conference/) — Nov 13, 2025
8. [Amazon's AI vision points to a new front door for B2B buying: Agents — Digital Commerce 360](https://www.digitalcommerce360.com/2026/02/06/amazons-ai-b2b-buying-agents-q4-2025/) — Feb 6, 2026
9. [Transform Supply Chain Logistics with Agentic AI — AWS Blog](https://aws.amazon.com/blogs/industries/transform-supply-chain-logistics-with-agentic-ai/) — Accessed 2026-04-06
10. [AgentCore Pricing and When Self-Hosting Wins — Scalevise](https://scalevise.com/resources/agentcore-bedrock-pricing-self-hosting/) — Accessed 2026-04-06
11. [Amazon Bedrock Pricing: Token Rates Hide a $350/Month Trap — Cloud Burn](https://cloudburn.io/blog/amazon-bedrock-pricing) — Accessed 2026-04-06
12. [Amazon, Tech Platforms Push Agentic Commerce — Distribution Strategy Group](https://distributionstrategy.com/2026/03/amazon-tech-platforms-push-agentic-commerce-raising-new-questions-for-distributors/) — Accessed 2026-04-06

---
*Last updated: 2026-04-06*
