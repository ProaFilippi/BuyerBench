---
type: product
title: "ChatGPT Operator / Shopping (OpenAI)"
created: 2026-04-05
tags:
  - ai-agent
  - openai
  - operator
  - shopping
  - autonomous
  - agentic-commerce
  - pillar1
  - pillar3
related:
  - '[[ACP]]'
  - '[[Perplexity-Comet]]'
  - '[[AP2-UCP]]'
  - '[[INDEX]]'
---

# ChatGPT Operator / Shopping (OpenAI)

> OpenAI's autonomous browser agent and in-chat shopping infrastructure — from the first commercially deployed agentic shopping protocol (ACP Instant Checkout, Sep 2025) to the strategic pivot away from checkout (Mar 2026)

## Overview

OpenAI's **Operator** was the first commercially deployed autonomous browser agent from a major AI lab, launching January 23, 2025. Built on the **Computer-Using Agent (CUA)** model (a fine-tuned GPT-4o variant), Operator could navigate websites, fill forms, complete purchases, and execute multi-step workflows in a real browser session — entirely without human intervention per step.

In September 2025, OpenAI extended this capability into **ChatGPT Instant Checkout**, the first large-scale production deployment of the **Agentic Commerce Protocol (ACP)** — a checkout standard co-developed with Stripe. This gave ChatGPT's 900M+ weekly active users the ability to buy from Shopify merchants and Etsy sellers without leaving the chat interface.

By March 2026, OpenAI had **rolled back Instant Checkout** due to poor consumer adoption, pivoting to an **app-based model** where retailers operate their own dedicated ChatGPT apps with outbound links to their native checkout flows. The ACP specification itself was not deprecated and remains active under Apache 2.0 licensing.

In February 2026, Operator was merged into the broader **ChatGPT Agent** mode — a unified agentic capability accessible via dropdown in the ChatGPT composer interface.

> **BuyerBench relevance (Pillar 1):** Operator's task execution model (CUA + browser) is a direct reference architecture for Pillar 1 capability scenarios: supplier discovery via unstructured web navigation, form-based RFQ submission, and multi-step procurement workflows. The capability ceiling and failure modes of Operator define realistic bounds for agentic buyer task completion benchmarks.

> **BuyerBench relevance (Pillar 3):** The ACP Instant Checkout rollback is a canonical example of a **platform-layer authorization change**: technically functional payment flows disabled by business-layer policy rather than security failure. Pillar 3 scenarios should test whether agents correctly interpret and respect platform authorization signals that are not purely technical (e.g., protocol version changes, feature deprecation notices, merchant app availability as a signal of permitted checkout path).

## Quick Facts

| Attribute | Value |
|-----------|-------|
| Product Name | ChatGPT Operator (→ ChatGPT Agent, Feb 2026) |
| Developer | OpenAI |
| Underlying Model | GPT-4o (Computer-Using Agent / CUA fine-tune) |
| Initial Launch | 2025-01-23 (Operator) |
| Shopping Launch | 2025-09-29 (ACP Instant Checkout) |
| Shopping Rollback | 2026-03-04 (Instant Checkout removed) |
| Current Form | ChatGPT Agent mode (Feb 2026+) + retailer apps |
| Monthly Active Users | 900M+ weekly active ChatGPT users (context for reach) |
| Merchant Transaction Fee | 4% (Instant Checkout era, Sep 2025 – Mar 2026) |
| Checkout Protocol | ACP (Agentic Commerce Protocol, Apache 2.0, still active) |

## Operator Product

### What It Is

Operator is a **task-executing AI agent** embedded in ChatGPT that uses a live Chromium browser instance to act on behalf of users. Unlike pure LLM agents operating via tool calls, Operator observes and interacts with actual web interfaces through screenshot-based computer vision — the same interaction model a human uses.

Key capabilities at launch (Jan 2025):
- Filling out forms and submitting data
- Completing purchases across arbitrary e-commerce sites
- Booking travel, restaurants, and services
- Navigating multi-step web workflows (account creation, preference selection, checkout)
- Handling CAPTCHA challenges (within limits)

### Architecture

Operator is built on the **Computer-Using Agent (CUA)** model architecture:
- A GPT-4o fine-tune trained on GUI navigation and computer-use tasks
- Receives screenshots of browser state as input
- Produces structured actions (click, type, scroll, navigate) as output
- Each action → screenshot → next action loop runs until task completion or user intervention

OpenAI designed deliberate **human-in-the-loop checkpoints** for sensitive actions:
- Payment execution requires explicit user confirmation
- Logins and credential entry pause for human approval
- Irreversible actions (e.g., confirming purchases) trigger confirmation dialogs

### Evolution to ChatGPT Agent (Feb 2026)

In February 2026, OpenAI unified Operator into **ChatGPT Agent** — a mode selectable from the composer dropdown. The update:
- Consolidated computer-use, tool-use, and search under a single "agent" entry point
- Expanded access from Pro-only to Plus and Team subscribers
- Retained Operator's browser automation core with better task orchestration
- Framed the product as a general work assistant rather than a shopping-specific feature

## Shopping Feature History

### Phase 1: ACP Instant Checkout Launch (Sep 2025)

On **September 29, 2025**, OpenAI launched **ChatGPT Instant Checkout** — the first large-scale production deployment of the Agentic Commerce Protocol (ACP). This allowed US ChatGPT users to purchase products directly inside the chat conversation.

**Launch mechanics:**
- ChatGPT displays shoppable product cards in search results
- User clicks "Buy" → in-chat checkout flow powered by ACP
- Payment processed via Stripe SharedPaymentToken (SPT) — no raw card data exposed to ChatGPT
- Transaction routed to merchant via ACP's four-step sequence (Create → Update → Complete → Cancel)
- Merchant charged **4% transaction fee** by OpenAI (in addition to standard Stripe processing fees)

**Launch partners:** Etsy, Shopify merchants (1M+), Glossier, Vuori, Spanx, SKIMS

**January 2026:** Shopify merchant onboarding scaled up; 4% fee model confirmed publicly.

### Phase 2: Strategic Tensions (Jan – Feb 2026)

Several friction points became apparent during the Instant Checkout scale-up:

| Issue | Detail |
|-------|--------|
| **Conversion rate gap** | Walmart data: 3× lower conversion for in-chat checkout vs. redirecting users to merchant website |
| **Missing retail functionality** | No real-time inventory, no coupon/promotion support, no loyalty points integration, no store pickup option |
| **Tax collection gap** | As of February 2026, OpenAI had not implemented US state sales tax collection |
| **Merchant control loss** | Retailers resisted ceding the checkout experience and post-purchase customer relationship |
| **Amazon partnership** | OpenAI's $50B strategic partnership with Amazon (Feb 27, 2026) aligned incentives toward "send users to Amazon" rather than "buy in ChatGPT" |

### Phase 3: ACP Rollback (Mar 2026)

On **March 4, 2026**, OpenAI removed the Instant Checkout feature from ChatGPT. Official explanation:

> *"The initial version of Instant Checkout did not offer the level of flexibility that we aspire to provide, so we're allowing merchants to use their own checkout experiences."*

Key facts about the rollback:
- **ACP specification was NOT deprecated** — the Apache 2.0 open standard remained live and under active development
- **Merchant apps replaced in-chat checkout**: Walmart, Etsy, Sephora, DoorDash, Instacart, CarMax, Lowe's, Expedia, and others now operate dedicated ChatGPT Apps that link back to their own checkout flows
- **ACP's role narrowed**: from universal in-chat checkout rail to an optional protocol for ChatGPT App developers
- Retailers that had integrated ACP for product **discovery** (Target, Sephora, Nordstrom, Lowe's, Best Buy, Home Depot, Wayfair) retained those integrations

## Current State (2026)

As of April 2026, OpenAI's agentic commerce strategy is:

1. **ChatGPT as discovery hub** — product search and comparison within ChatGPT, with outbound links to merchant checkout
2. **ChatGPT Apps ecosystem** — retailers build branded apps within ChatGPT that control the checkout experience
3. **ACP as optional infrastructure** — available for App developers wanting standardized cart-to-checkout signaling; not the primary product
4. **Amazon as preferred destination** — the $50B partnership effectively positions Amazon as the default purchase destination from ChatGPT shopping intent

Strategic summary from OpenAI's post-rollback communications:
> *"prioritizing making ChatGPT search and product discovery great, with ACP serving as the infrastructure that connects users to merchants across the full shopping journey"*

The **ChatGPT Agent** (evolved from Operator) continues to support autonomous web-based purchases for users who instruct it to complete transactions on arbitrary third-party sites — this capability was never removed, only the structured in-chat checkout rail.

## Pricing

### Consumer (ChatGPT Plans)

| Plan | Operator / Agent Access | Price |
|------|------------------------|-------|
| ChatGPT Free | No agent mode | $0/month |
| ChatGPT Plus | Agent mode (post Feb 2026) | $20/month |
| ChatGPT Pro | Agent mode (first access Nov 2025) | $200/month |
| ChatGPT Team | Agent mode (post Feb 2026) | $30/user/month |

### API / Developer (Responses API)

The **Responses API** provides developer access to the same underlying models with built-in tool support. Pricing is token-based (no API surcharge), with tool-specific fees:

| Tool | Pricing |
|------|---------|
| **Base model (gpt-4o)** | ~$2.50/1M input tokens, ~$10/1M output tokens |
| **Computer Use tool** | $3/1M input + $12/1M output (research preview, tier 3–5 only) |
| **Web Search tool** | Per-call fee (varies by model) + search content tokens |
| **File Search tool** | $2.50/thousand queries + $0.10/GB/day storage (first GB free) |

### Merchant (ACP Era, Historical)

During Instant Checkout (Sep 2025 – Mar 2026):
- **4% transaction fee** charged to merchants on completed Instant Checkout purchases
- Standard Stripe payment processing fees applied in addition
- Fee model confirmed publicly in January 2026 when Shopify merchant onboarding scaled

## Lessons from the ACP Rollback

The ACP Instant Checkout failure is a rich case study in agentic commerce product design:

| Lesson | Implication |
|--------|-------------|
| **Conversion requires context** | Buyers want price comparison, reviews, loyalty points, and promotions before committing — an AI that strips this context loses conversion |
| **Merchant relationship > transaction efficiency** | Retailers value owning the post-purchase experience (returns, loyalty, upsell) more than reducing checkout friction for the buyer |
| **Tax and compliance can't be deferred** | Missing sales tax was a fundamental operational gap that undermined enterprise merchant trust |
| **Protocol ≠ Product** | ACP's technical soundness didn't prevent product failure — the UX layer and business model failed independently |
| **Platform partnerships constrain agent autonomy** | The Amazon partnership effectively overrides technical protocol capability with a business-layer constraint |
| **Open standards survive product failures** | Because ACP was Apache 2.0 from day one, the spec outlived the feature — an important governance design principle |

## BuyerBench Pillar Relevance

### Pillar 1 — Agent Intelligence and Operational Capability

Operator / ChatGPT Agent is a **direct real-world benchmark target** for BuyerBench Pillar 1:
- Multi-step workflow execution (navigate → compare → select → purchase)
- Unstructured web navigation (no API — pure browser automation)
- Form completion and credential management
- Human-in-the-loop checkpoint handling
- Task completion under ambiguous instructions

Operator's published failure rates (high error rate on complex multi-step tasks) and the CUA architecture's screenshot-based action loop define realistic capability bounds for Pillar 1 evaluation rubrics.

### Pillar 2 — Economic Decision Quality

The Instant Checkout product design revealed a key behavioral pattern: **users research in ChatGPT but buy elsewhere**. This suggests AI shopping agents may exhibit a "discovery-completion gap" — task completion (buy) and task initiation (discover) are decoupled. BuyerBench Pillar 2 scenarios should test whether agents correctly identify when to complete vs. when to hand off purchasing intent.

### Pillar 3 — Security, Compliance, and Market Readiness

The rollback creates a critical **authorization boundary scenario** for Pillar 3:
- The ACP spec is technically available but the in-chat checkout feature was removed
- An agent operating in 2026 that attempts to use ACP Instant Checkout is violating platform authorization — not a protocol error, but a **policy enforcement failure**
- BuyerBench should include scenarios where a historically valid protocol endpoint becomes unavailable by platform-layer decision, and test whether agents correctly detect and handle this state
- The merchant app model (outbound checkout) represents the **currently authorized payment path** — agents must route to it rather than attempting direct ACP checkout calls

## Comparison: ChatGPT Operator vs. Perplexity Comet

| Dimension | ChatGPT Operator / Agent | Perplexity Comet |
|-----------|--------------------------|-----------------|
| **Architecture** | Browser automation (CUA) + ChatGPT chat interface | Dedicated browser agent (Comet product) |
| **Shopping approach** | App ecosystem + outbound checkout (post-Mar 2026) | Autonomous cross-site purchase execution |
| **Protocol** | ACP (scaled back) | Unknown / proprietary |
| **Legal status** | No known injunctions (2026) | Amazon court injunction (Mar 10, 2026) |
| **User base** | 900M+ weekly ChatGPT users | Perplexity subscriber base |
| **Merchant model** | ChatGPT Apps (retailer-controlled checkout) | Direct site navigation |

See also: [[Perplexity-Comet]] for the competing approach and its legal challenges.

## Related Entities

- [[ACP]] — The Agentic Commerce Protocol that powered Instant Checkout; the technical substrate of ChatGPT's shopping infrastructure
- [[Perplexity-Comet]] — Direct competitor autonomous shopping agent; faced Amazon court injunction (Mar 2026)
- [[AP2-UCP]] — Google's competing agentic commerce protocol stack; benefited from ACP rollback reducing OpenAI's protocol momentum
- [[Amazon-Rufus-BuyForMe]] — Amazon's AI shopping stack; the $50B OpenAI-Amazon partnership aligns both companies against Perplexity/Google in consumer agentic commerce

## Sources

1. [Introducing Operator — OpenAI](https://openai.com/index/introducing-operator/) — Accessed 2026-04-05
2. [OpenAI launches Operator, an AI agent that performs tasks autonomously — TechCrunch](https://techcrunch.com/2025/01/23/openai-launches-operator-an-ai-agent-that-performs-tasks-autonomously/) — Accessed 2026-04-05
3. [Buy it in ChatGPT: Instant Checkout and the Agentic Commerce Protocol — OpenAI](https://openai.com/index/buy-it-in-chatgpt/) — Accessed 2026-04-05
4. [OpenAI's plans to make ChatGPT more like Amazon aren't going so well — TechCrunch](https://techcrunch.com/2026/03/24/openais-plans-to-make-chatgpt-more-like-amazon-arent-going-so-well/) — Accessed 2026-04-05
5. [OpenAI shifts checkout plans in its agentic commerce strategy — Digital Commerce 360](https://www.digitalcommerce360.com/2026/03/06/openai-shifts-checkout-plans-agentic-commerce-strategy/) — Accessed 2026-04-05
6. [OpenAI reveals updates to its agentic commerce experience for ChatGPT — Digital Commerce 360](https://www.digitalcommerce360.com/2026/03/24/openai-agentic-commerce-updates-chatgpt-walmart/) — Accessed 2026-04-05
7. [OpenAI Scales Back Shopping Plans for ChatGPT — The Information](https://www.theinformation.com/articles/openai-scales-back-shopping-plans-chatgpt) — Accessed 2026-04-05
8. [OpenAI Scales Back ChatGPT Checkout: Why Agentic Commerce Needs Universal Checkout Infrastructure — Rye](https://rye.com/blog/openai-chatgpt-checkout-agentic-commerce) — Accessed 2026-04-05
9. [ChatGPT Bails on Transactions — Good News for Expedia and Booking — Skift](https://skift.com/2026/03/05/openai-chatgpt-checkout-walkback/) — Accessed 2026-04-05
10. [OpenAI Pulls Plug on ChatGPT Checkout Plans — Hello Partner](https://hellopartner.com/2026/03/09/openai-pulls-plug-on-chatgpt-checkout-plans/) — Accessed 2026-04-05
11. [New tools for building agents — OpenAI](https://openai.com/index/new-tools-for-building-agents/) — Accessed 2026-04-05
12. [OpenAI API Pricing — OpenAI](https://openai.com/api/pricing/) — Accessed 2026-04-05
13. [ChatGPT February 2026 Updates: What Marketers Need to Know — ADSX](https://www.adsx.com/blog/chatgpt-updates-february-2026) — Accessed 2026-04-05

---
*Last updated: 2026-04-05*
