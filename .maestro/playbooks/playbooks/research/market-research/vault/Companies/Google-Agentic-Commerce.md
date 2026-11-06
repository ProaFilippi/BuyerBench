---
type: company
title: "Google Agentic Commerce"
created: 2026-04-06
tags:
  - google
  - platform
  - ai-agents
  - gemini
  - vertex-ai
  - pricing
  - agentic-commerce
  - project-mariner
  - ap2
  - ucp
  - pillar1
  - pillar2
  - pillar3
related:
  - '[[AP2-UCP]]'
  - '[[OpenAI-Agent-Platform]]'
  - '[[ACP]]'
  - '[[x402]]'
  - '[[INDEX]]'
---

# Google Agentic Commerce

> Google's agentic commerce stack spans five layers: Project Mariner (DeepMind browser agent, 83.5% WebVoyager, 10 parallel tasks), Gemini 2.5 Pro model APIs ($1.25/$10.00 per 1M tokens), Vertex AI Agent Engine (compute-billed, $0.00994/vCPU-hour), Gemini Enterprise for CX (retail agents, deployed at Kroger/Lowe's/Home Depot), and the AP2/UCP open protocol stack (60+ partners, NRF Jan 11 2026). Google AI Ultra consumer tier ($249.99/month) includes Mariner access; Gemini Enterprise subscription is $30/user/month.

## Overview

Google occupies a uniquely comprehensive position in the agentic commerce landscape: it is simultaneously a **consumer agent provider** (Project Mariner browser agent), a **model and infrastructure platform** (Gemini API, Vertex AI), a **protocol standard-setter** (AP2, UCP), and an **enterprise CX agent vendor** (Gemini Enterprise for Customer Experience). No other company holds all four positions at once.

The agentic commerce strategy crystallized in three phases:

1. **Model Foundations (late 2024):** Gemini 2.0 was released as Google's first model explicitly built for the "agentic era" — featuring native tool use, multimodal I/O (text, image, audio), compositional function-calling, and the low latency required for real-time agent loops. Gemini 2.0 is the model underlying Project Mariner.

2. **Product Deployment (2025):** Project Mariner (DeepMind's browser agent) demonstrated autonomous multi-step purchase workflows with state-of-the-art benchmark performance. Gemini Enterprise for CX was deployed at major retailers (Kroger, Lowe's, Papa John's, Woolworths, Home Depot). Google expanded AI Shopping tools — conversational search, agentic checkout, and AI phone call-to-store — in November 2025.

3. **Protocol Leadership (January 2026):** At NRF Retail's Big Show (January 11, 2026), Google CEO Sundar Pichai personally presented the **Universal Commerce Protocol (UCP)** and the **Agent Payments Protocol (AP2)** — Google's open-standard answer to OpenAI/Stripe's ACP. The NRF launch landed as ACP was quietly underperforming, and Google's 60+ partners including all five major card networks positioned it as the industry-consensus alternative. The UCP will power checkout directly in Google Search AI Mode and the Gemini app for eligible US retailers.

> **BuyerBench relevance (Pillar 1):** Project Mariner's Observe–Plan–Act loop and "Teach & Repeat" workflow learning are reference implementations for how capable buyer agents should navigate supplier catalogs and execute procurement tasks. BuyerBench Pillar 1 scenarios should test agents operating in Mariner-like environments and use Mariner's 83.5% WebVoyager score as a capability ceiling benchmark.

> **BuyerBench relevance (Pillar 2):** Gemini Enterprise for CX's "proactive digital concierge" framing — where the agent builds carts on behalf of shoppers — creates measurable exposure to decoy effects and anchoring: the agent's cart suggestions become the default from which users must actively deviate. This is a documented Pillar 2 behavioral risk pattern (status quo bias + default anchoring).

> **BuyerBench relevance (Pillar 3):** AP2's two-phase mandate model (Intent Mandate → Cart Mandate with verifiable credentials) is the most rigorous real-world authorization protocol for buyer agents. See [[AP2-UCP]] for the full Pillar 3 authorization analysis. BuyerBench should use AP2's mandate architecture as the reference standard for authorization chain integrity scenarios.

## Quick Facts

| Attribute | Value |
|-----------|-------|
| Company | Alphabet / Google (founded 1998; ~$350B revenue 2025) |
| AI Model Brand | Gemini (2.0, 2.5 Pro, 2.5 Flash family) |
| Browser Agent | Project Mariner (DeepMind; Gemini 2.0 powered) |
| Commerce Protocol | AP2 (Agent Payments Protocol) + UCP (Universal Commerce Protocol) |
| Enterprise CX Product | Gemini Enterprise for Customer Experience |
| Developer Platform | Google AI Studio (free/dev), Vertex AI (enterprise) |
| AP2/UCP Launch Date | January 11, 2026 (NRF, New York) |
| Protocol Partners | 60+ orgs incl. all 5 major card networks |
| Enterprise Subscription | Gemini Enterprise — $30/user/month (launched Oct 2025) |
| Consumer Agent Tier | Google AI Ultra — $249.99/month (includes Project Mariner) |
| Key Enterprise Customers | Kroger, Lowe's, Papa John's, Woolworths, Home Depot, Best Buy, Macy's |
| CapEx Commitment | $185B capital investment pledge (2026, Alphabet) |

## Key Products

### Project Mariner (Google DeepMind)

Project Mariner is Google DeepMind's autonomous web browsing agent, built on Gemini 2.0, capable of navigating Chrome independently to complete complex multi-step tasks — including product research, cart building, form-filling, and purchase execution — on behalf of users.

**Key technical capabilities:**
- **Observe–Plan–Act loop**: perceives the current browser state, plans the next action, executes it — repeated iteratively until task completion
- **Teach & Repeat**: user demonstrates a workflow once; Mariner learns the pattern and applies it to similar future tasks (generalized from the demonstration, not just replayed)
- **Parallel task streams**: up to 10 independent tasks run simultaneously in cloud-hosted browser sessions
- **Multimodal understanding**: processes text, images, and page layouts to understand non-textual UI elements
- **Cloud-native execution**: tasks run in cloud-hosted browsers, not the user's local session — preserving user context and enabling parallelism

**Performance benchmarks:**
- **83.5% on WebVoyager** — state-of-the-art for browser agents as of mid-2025 (compare: OpenAI Operator has no published benchmark)
- Demonstrated use cases: job hunting from resume, furniture delivery booking, grocery list population from recipes

**Access:**
| Tier | Price | Mariner Access |
|------|-------|----------------|
| Google One (standard) | $2.99–$9.99/month | No |
| Google AI Pro | $19.99/month | No (standard Gemini agent) |
| **Google AI Ultra** | **$249.99/month** | **Yes — Mariner + full Gemini suite** |
| Vertex AI (developer API) | Pay-per-use (see Pricing) | Mariner API integration in progress (as of mid-2025) |
| Mariner Studio | Planned Q2 2026 | Visual task builder (announced) |

**Roadmap (announced):**
- **Q2 2026**: Mariner Studio — visual task building interface
- **Q3 2026**: Cross-device sync — continue tasks across desktop and Android
- **Q4 2026**: Agent Marketplace — third-party autonomous workflow distribution

---

### Gemini 2.0 / 2.5 Model Family

Gemini 2.0 (released Dec 2024) was Google's first model explicitly positioned for the agentic era. Key properties:

- **Native tool use** — function-calling, grounding, and web search are first-class primitives, not add-ons
- **Compositional function-calling** — chains multiple tool calls in a single reasoning pass
- **Long context** — up to 1M token context window in Pro variants (relevant for large supplier catalogs)
- **Native multimodal I/O** — text, image, audio input; image and audio output natively supported
- **Improved instruction following and planning** — benchmarked improvements over Gemini 1.5 on multi-step agent tasks

Gemini 2.5 Pro (successor, released Q1 2026) is Google's current flagship, with enhanced reasoning, coding, and instruction-following capabilities.

---

### Vertex AI Agent Engine (formerly Agent Builder)

Vertex AI Agent Engine is Google Cloud's managed runtime for deploying production-scale AI agents. Distinct from the model itself — it handles orchestration, memory, session management, and compute scaling.

**Key capabilities:**
- Horizontal auto-scaling for agent compute
- Memory Bank (persistent agent memory across sessions)
- Code Execution (sandboxed code running within agent workflows)
- Integration with Vertex AI Search and Data Store for retrieval-augmented agents
- Sessions-as-a-service (managed conversation state)

> Note: Sessions, Memory Bank, and Code Execution all entered paid billing as of February 11, 2026 (previously free during preview).

---

### Gemini Enterprise for Customer Experience (CX)

Announced at NRF January 11, 2026. A purpose-built agentic platform for retail and commerce, combining shopping intelligence with customer service automation.

**Core agents (pre-built, configurable):**
- **Shopping Agent**: processes text, voice, and image queries; acts as a "proactive digital concierge"; autonomously builds carts and executes consented checkout actions; handles the full customer lifecycle
- **Customer Service Agent**: manages post-purchase support, returns, inquiries — with handoff to human agents on escalation
- **Product Discovery Agent**: conversational product recommendation with multimodal input support (e.g., photo-based search)

**Live enterprise deployments (as of April 2026):**
- **Kroger** — AI-powered personalized grocery shopping
- **Lowe's** — Home improvement project planning agent
- **Papa John's** — Order customization and loyalty agent
- **Woolworths** — Grocery assistant (AU/NZ)
- **Home Depot** — Magic Apron agent with store-level aisle navigation and project planning
- **Best Buy**, **Macy's**, **Flipkart** — Additional UCP/Gemini CX partners

---

### Google Shopping Integration (AI Mode + Gemini App)

Google is integrating agentic checkout directly into its search and Gemini surfaces:

- **AI Mode in Search**: UCP-powered checkout will allow users to purchase from eligible US retailers directly within Google Search results — no redirect required
- **Gemini App**: same UCP checkout integration; agent can search for, compare, and purchase products within the conversational interface
- **Conversational Search**: launched Nov 2025 — users can ask shopping questions in multi-turn conversational format within Google Shopping
- **AI Calls-to-Store**: Google agent can autonomously call a physical store to check inventory, ask product questions, or place orders — bridging digital and physical retail
- **Direct Offers**: merchants can surface special offers directly to agents via the UCP/A2A interface

---

## AP2/UCP Payment Protocol

For the complete technical profile of AP2 and UCP, see [[AP2-UCP]]. Key summary for the company-level view:

| Protocol | Role | Launch |
|----------|------|--------|
| **AP2** (Agent Payments Protocol) | Payment authorization via cryptographic mandates (Intent + Cart) | January 11, 2026 (NRF) |
| **UCP** (Universal Commerce Protocol) | Full commerce orchestration (discovery → fulfillment); uses AP2 for payments | January 11, 2026 (NRF) |

**Strategic significance:**
- Launched 4 months after ACP went live — explicitly positioned as the **retail-industry-consensus** alternative to OpenAI/Stripe's checkout-centric ACP
- 60+ partners including **all five major card networks** (Visa, Mastercard, Amex, JCB, UnionPay) — vs. ACP's Stripe-centric model
- AP2 natively extends to crypto payments via [[x402]] (Coinbase integration)
- UCP will power checkout in Google Search AI Mode and Gemini app for eligible US retailers

**NRF CEO keynote:** Sundar Pichai personally presented UCP at NRF 2026 — a signal of CEO-level priority, not a developer product launch.

---

## Pricing

### Gemini API Pricing (per 1M tokens, April 2026)

| Model | Input (≤200K ctx) | Input (>200K ctx) | Output | Notes |
|-------|-------------------|-------------------|--------|-------|
| **Gemini 2.5 Pro** | $1.25 | $2.50 | $10.00 | Flagship; long context surcharge |
| **Gemini 2.5 Flash** | $0.15 | $0.15 | $0.60 | Cost-optimized; same context window |
| **Gemini 2.0 Flash** | $0.10 | $0.10 | $0.40 | Previous generation; widely deployed |
| **Gemini 2.0 Flash-Lite** | $0.075 | $0.075 | $0.30 | Lowest-cost Gemini model |
| **Gemini 1.5 Pro** | $1.25 | $2.50 | $5.00 | Legacy flagship |

> **Context pricing note:** Gemini charges a 2× surcharge on input tokens for prompts exceeding the 200K token threshold. This is relevant for Pillar 1 supplier catalog scenarios where agents must process large product datasets in a single context.

> **Batch discount:** Context caching available — prompts with repeating prefixes (e.g., fixed system instructions + large catalog) billed at 25¢/1M tokens for cached token reads. Relevant for bulk BuyerBench evaluation pipelines.

> **Free tier:** Google AI Studio offers Gemini 2.0 Flash free up to rate limits (15 requests/minute, 1M tokens/minute, 1,500 requests/day). No free tier on Vertex AI.

### Vertex AI Agent Engine Pricing

| Resource | Price | Notes |
|----------|-------|-------|
| **vCPU** | $0.00994 / vCPU-hour | Active runtime only; idle = no charge |
| **Memory** | $0.0105 / GiB-hour | Active runtime only |
| **Sessions** | Billed per session-second | Paid since Feb 11, 2026 |
| **Memory Bank** | Billed per GB stored | Paid since Feb 11, 2026 |
| **Code Execution** | Billed per execution | Paid since Feb 11, 2026 |

> **vs. Amazon AgentCore**: Amazon AgentCore Runtime is $0.0895/vCPU-hour — roughly **9× more expensive** than Vertex AI Agent Engine's $0.00994/vCPU-hour. Google's compute pricing is markedly more competitive for high-throughput agent workloads.

### Consumer Subscription Tiers

| Plan | Price | Agentic Capability |
|------|-------|--------------------|
| Google One (AI Basic) | $19.99/month | Gemini 1.5 Pro access, basic AI |
| Google AI Pro | $19.99/month | Gemini 2.5 Pro access, standard Gemini agent |
| **Google AI Ultra** | **$249.99/month** | **Project Mariner + full Gemini suite + 1 TB storage** |
| Gemini Enterprise | $30/user/month | Business subscription; all Google AI tools; predictable per-seat billing |

> **Note:** Google AI Ultra is priced at $249.99/month — comparable to OpenAI's ChatGPT Pro at $200/month, which is the tier that includes Operator access.

### Vertex AI Agent Builder Pricing

| Component | Cost |
|-----------|------|
| Data Store (enterprise search queries) | $2.00 per 1,000 queries |
| Grounding with Google Search | $35 per 1,000 queries |
| Agent Engine compute | See vCPU/memory rates above |
| Model tokens | Standard Gemini API rates |

---

## Strategic Positioning

### Google as the Infrastructure + Protocol Leader

Unlike OpenAI (which controls the model layer and is expanding into commerce) or Amazon (which controls the retail layer and is expanding into agents), Google's advantage is **simultaneous presence at every layer of the commerce stack**: search discovery, shopping comparison, checkout via UCP, payment authorization via AP2, and enterprise CX agent deployment.

This breadth creates a structural advantage: a UCP-enabled merchant gets a single integration that immediately reaches Google Search AI Mode, the Gemini app, and any third-party agent using the AP2/UCP protocol.

### AP2/UCP vs. ACP: Momentum Shift

The NRF January 2026 launch (timed 4 months after ACP's September 2025 live date, and just weeks before ACP's March 2026 rollback) proved prescient:

| Dimension | ACP (OpenAI + Stripe) | AP2 / UCP (Google) |
|-----------|----------------------|--------------------|
| Post-2026 status | Narrowed to 7 retailers + Shopify | Expanding in production |
| Card network coverage | Stripe-centric | All 5 major card networks |
| Protocol scope | Checkout API (merchant-facing) | Full lifecycle: discovery → payment → fulfillment |
| Crypto support | Not native | Native x402 extension |
| Consumer surface | ChatGPT (subscription gated) | Google Search + Gemini app (massive organic reach) |
| CEO visibility | Product/API-level announcement | Sundar Pichai NRF keynote |

### The $185B Infrastructure Bet

Alphabet announced a $185B capital expenditure commitment in 2026, with AI infrastructure (data centers, TPU compute, Gemini training) as the primary destination. This dwarfs Amazon's $50B OpenAI partnership and signals a multi-year price-to-win strategy on model inference costs.

---

## Limitations

- **Project Mariner API not fully public**: As of April 2026, Mariner is available to consumers via Google AI Ultra ($249.99/month); Vertex AI API integration was announced but not fully GA for enterprise developers
- **No published Mariner procurement benchmark**: The 83.5% WebVoyager score measures general browser task completion, not procurement-specific workflows — BuyerBench would be the first to measure Mariner's procurement performance
- **UCP checkout surface limited at launch**: UCP powers checkout in Google Search AI Mode and Gemini app, but only for "eligible US retailers" — full merchant coverage requires time for UCP integrations to propagate
- **Gemini Enterprise pricing opacity**: The $30/user/month enterprise subscription gives "unlimited access to all Google AI tools" but does not break out per-agent-call costs — actual unit economics in agentic workloads are not publicly modeled
- **Agent-to-token cost multiplier**: Like all LLM-based agents, multi-step agentic workflows consume significantly more tokens than single-turn queries — context pricing surcharges (>200K tokens) can amplify costs for catalog-heavy supplier research tasks

---

## BuyerBench Pillar Relevance

### Pillar 1 — Agent Intelligence and Operational Capability
- **Project Mariner** is the primary Google agent to benchmark for multi-step supplier research and procurement workflow execution; 83.5% WebVoyager establishes the capability ceiling
- **Teach & Repeat** is directly relevant to Pillar 1 workflow automation scenarios: can an agent learn a procurement workflow from demonstration?
- **Vertex AI Agent Engine** memory and session primitives model the stateful execution required for multi-stage source-to-award workflows
- **UCP's catalog/pricing/fulfillment APIs** define the ideal Pillar 1 tool interface — BuyerBench should test whether agents correctly use structured discovery before making selections

### Pillar 2 — Economic Decision Quality and Behavioral Robustness
- **Gemini Enterprise for CX's proactive cart-building** creates default-anchoring exposure: agent cart suggestions become the status quo from which users must actively deviate — a measurable susceptibility to **default bias** and **status quo bias**
- **Long-context pricing surcharge** creates a real economic cost-complexity tradeoff: agents must decide how much supplier data to include in context vs. making decisions with partial information — analogous to satisficing under information cost constraints
- **AI Mode Search checkout** creates a **framing** scenario: the same product purchased through Google's native checkout vs. clicking through to a merchant site may trigger different willingness-to-complete behavior

### Pillar 3 — Security, Compliance, and Market Readiness
- **AP2 mandate architecture** (Intent Mandate → Cart Mandate with verifiable credentials) is the primary Pillar 3 authorization reference — see [[AP2-UCP]] for full analysis
- **UCP's structured commerce flow** enforces mandatory consent checkpoints (intent capture + cart approval) that map directly to Pillar 3 authorization-chain integrity scenarios
- **AP2's native x402 crypto extension** means Google's protocol governs FATF Travel Rule compliance for crypto-based agent payments — Pillar 3 regulatory compliance scenarios should test agents operating under AP2 constraints with crypto payment rails

---

## Related Entities

- [[AP2-UCP]] — Full technical profile of AP2 and UCP protocol stack
- [[OpenAI-Agent-Platform]] — Primary competitor; ACP vs. AP2/UCP protocol comparison
- [[ACP]] — OpenAI/Stripe's competing checkout protocol; narrowed scope post-Mar 2026
- [[x402]] — Coinbase's HTTP micropayment protocol; AP2 native extension
- [[Amazon-Agentic-Commerce]] — Competitor with parallel agentic commerce infrastructure; AP2 partner via Amazon Business
- [[Skyfire]] — Crypto-native agent payment infrastructure; architecturally compatible with AP2's verifiable credential model; Coinbase Ventures-backed

---

## Sources

- [A new era of agentic commerce is here — Google Cloud Blog](https://cloud.google.com/transform/a-new-era-agentic-commerce-retail-ai)
- [Google Gemini Update Jan 2026: Agentic Commerce Goes Real — Beam AI](https://beam.ai/agentic-insights/geminis-january-2026-update-just-changed-how-people-buy-online)
- [Sundar Pichai's NRF 2026 remarks — Google Blog](https://blog.google/company-news/inside-google/message-ceo/nrf-2026-remarks/)
- [Google launches agentic commerce tools, Universal Commerce Protocol — Constellation Research](https://www.constellationr.com/insights/news/google-launches-agentic-commerce-tools-universal-commerce-protocol-gemini-enterprise)
- [Google Cloud Brings Shopping and Customer Service Together — Google Cloud Press Corner](https://www.googlecloudpresscorner.com/2026-01-11-Google-Cloud-Brings-Shopping-and-Customer-Service-Together-with-Gemini-Enterprise-for-Customer-Experience)
- [New tech and tools for retailers in the agentic shopping era — Google Blog](https://blog.google/products/ads-commerce/agentic-commerce-ai-tools-protocol-retailers-platforms/)
- [Google augments AI shopping with conversational search, agentic checkout — TechCrunch](https://techcrunch.com/2025/11/13/google-expands-ai-shopping-with-conversational-search-agentic-checkout-and-an-ai-that-calls-stores-for-you/)
- [Alphabet Bets $185B on Gemini, Agentic Commerce and Enterprise AI — PYMNTS](https://www.pymnts.com/google/2026/alphabet-bets-185b-on-gemini-agentic-commerce-and-enterprise-ai/)
- [Project Mariner — Google DeepMind](https://deepmind.google/models/project-mariner/)
- [Google Expands AI Web-Browsing Agent Project Mariner to More Users and Devs — CDO Magazine](https://www.cdomagazine.tech/aiml/google-expands-ai-web-browsing-agent-project-mariner-to-more-users-and-devs)
- [Google Project Mariner AI Agent 2026: Features, Price & How It Works — AllAboutAI](https://www.allaboutai.com/ai-agents/project-mariner/)
- [Vertex AI Pricing — Google Cloud](https://cloud.google.com/vertex-ai/generative-ai/pricing)
- [Gemini Pricing Jan 2026: Gemini API vs Vertex AI Costs — rahulkolekar.com](https://rahulkolekar.com/gemini-pricing-in-2026-gemini-api-vs-vertex-ai-tokens-batch-caching-imagen-veo/)
- [Vertex AI Agent Builder: What is the pricing structure? — Linkgo.dev](https://linkgo.dev/faq/the-pricing-structure-for-vertex-ai-agent-builder)
- [Google announces a new protocol to facilitate commerce using AI agents — TechCrunch](https://techcrunch.com/2026/01/11/google-announces-a-new-protocol-to-facilitate-commerce-using-ai-agents/)
- [Google Debuts 'Universal' Protocol for Agentic Commerce — PYMNTS](https://www.pymnts.com/google/2026/google-debuts-universal-protocol-for-agentic-commerce/)
- [UCP vs ACP: Which Agentic Commerce Protocol Should Retailers Choose? — paz.ai](https://www.paz.ai/blog/ucp-vs-acp-which-agentic-commerce-protocol-should-retailers-choose)
- [Google introduces Gemini 2.0: A new AI model for the agentic era — Google DeepMind Blog](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/google-gemini-ai-update-december-2024/)

---
*Last updated: 2026-04-06*
