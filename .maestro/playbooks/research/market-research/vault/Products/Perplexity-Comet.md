---
type: product
title: "Perplexity Comet (Browser Agent)"
created: 2026-04-05
tags:
  - ai-agent
  - perplexity
  - browser-agent
  - shopping
  - autonomous
  - agentic-commerce
  - pillar1
  - pillar3
related:
  - '[[ChatGPT-Operator]]'
  - '[[Amazon-Rufus-BuyForMe]]'
  - '[[ACP]]'
  - '[[INDEX]]'
---

# Perplexity Comet (Browser Agent)

> Perplexity's AI-native browser agent — the first commercially deployed autonomous cross-site shopping agent, now under federal court injunction (Mar 2026) for accessing Amazon without platform authorization

## Overview

**Comet** is an AI-native browser product from Perplexity AI, designed not as a passive web window but as an autonomous agent that can observe a user's browsing context, understand intent, and execute multi-step workflows without per-step human intervention. Comet can browse product pages, compare prices, log into accounts using user-provided credentials, add items to a cart, and complete a purchase — end to end — across arbitrary third-party websites.

Launched July 9, 2025 in restricted preview (Max subscribers only), Comet became broadly available on **October 2, 2025**. The "Buy with Pro" extension, launched November 2025 in partnership with PayPal, added one-click in-browser purchases for Perplexity Pro subscribers.

In **November 2025**, Amazon sued Perplexity in U.S. federal court alleging unauthorized computer access — specifically that Comet entered password-protected Prime accounts and masked bot activity as human browsing. On **March 9–10, 2026**, U.S. District Judge Maxine Chesney (N.D. Cal.) granted Amazon a preliminary injunction blocking Comet from accessing password-protected Amazon sections. Perplexity filed its appeal with the Ninth Circuit on **April 1, 2026**, arguing Amazon is misusing the CFAA to suppress competition in agentic AI shopping.

> **BuyerBench relevance (Pillar 3):** The Amazon v. Perplexity case establishes the most important consent-authorization distinction in agentic commerce law: a user's explicit permission for an AI agent to act on their behalf does not confer platform-layer authorization under a site's Terms of Service or the CFAA. BuyerBench Pillar 3 scenarios must test whether agents correctly distinguish "user has authorized me" from "the platform has authorized agent access."

> **BuyerBench relevance (Pillar 1):** Comet's cross-site autonomous purchase execution — navigate, credential-auth, select, checkout across arbitrary URLs — defines one of the most ambitious Pillar 1 capability targets. The workflow complexity (multi-site, multi-auth, adversarial CAPTCHA environment) sets realistic upper bounds for agentic buyer task completion evaluation.

## Quick Facts

| Attribute | Value |
|-----------|-------|
| Product Name | Comet |
| Developer | Perplexity AI |
| Product Type | AI-native browser with autonomous agent layer |
| Restricted Preview | 2025-07-09 (Max plan only) |
| General Availability | 2025-10-02 |
| Buy with Pro Launch | November 2025 (PayPal partnership) |
| Comet Plus Launch | ~2025-Q4 (standalone $5/month add-on) |
| Amazon Suit Filed | November 2025 |
| Injunction Granted | 2026-03-09 (Judge Chesney, N.D. Cal.) |
| Perplexity Appeal | 2026-04-01 (9th Circuit, enforcement stayed pending appeal) |
| Enforcement Stay | 7-day stay post-injunction; 9th Circuit extended during appeal review |

## Comet Browser Agent Architecture

Comet is differentiated from AI assistants and chat-embedded agents by its **browser-native architecture**:

### Core Design Principles

1. **Observe → Understand → Act**: Comet monitors the active browser context in real-time, builds a semantic model of the current page/task state, and can execute actions (clicks, form fills, navigation, checkout completion) without explicit per-step user prompting.

2. **Computer vision + web automation**: Like OpenAI's CUA (Computer-Using Agent), Comet uses screenshot-based visual understanding of rendered web pages — meaning it can interact with sites that have no API or structured schema, including password-protected areas when the user provides login credentials.

3. **Cross-site scope**: Unlike ChatGPT Operator (which pivoted to a ChatGPT Apps model tied to merchant-specific checkout flows), Comet is designed to operate across **arbitrary third-party websites** — including sites that have not opted into any agentic commerce protocol.

4. **Citation-backed recommendations**: Perplexity's search heritage is embedded in Comet's product experience — every product recommendation links to verifiable sources (review aggregations, price comparisons, feature analyses). Comet does not simply pick a product; it surfaces the evidence basis for its choice.

5. **User credential delegation**: When completing purchases on logged-in accounts (e.g., Amazon Prime, target.com), Comet uses stored/session credentials provided by the user. This is the specific capability that triggered Amazon's suit.

### Shopping Workflow

A typical Comet autonomous shopping flow:

```
User intent (natural language) 
  → Perplexity search + product research
  → Price comparison across sites
  → Comet navigates to selected product URL
  → Comet logs in using user credentials (if applicable)
  → Comet adds to cart, applies any coupons/promo codes found
  → Comet completes checkout (card via PayPal/stored payment / "Buy with Pro")
  → Comet returns purchase confirmation to user
```

This end-to-end execution runs without the user clicking anything after the initial purchase intent is expressed.

## Shopping Capabilities

### Buy with Pro (Nov 2025)

Launched in partnership with **PayPal**, Buy with Pro enables:
- **One-click purchase execution** from within Perplexity search results
- Payment via user's PayPal account (no raw card data stored by Perplexity)
- Targeted at US Perplexity Pro subscribers at launch
- Covers merchants reachable via Comet's browser automation (not limited to opt-in partners)

### Cross-Site Autonomous Purchase

Comet's broadest capability — autonomous shopping on any site:
- Comparison shopping across multiple retailer sites in a single session
- Coupon code detection and application
- Form-fill checkout completion
- CAPTCHA handling (within model limits)
- Session credential use for logged-in shopping (the capability challenged in the Amazon suit)

### Product Research Integration

Perplexity's core search capability is natively integrated:
- Real-time price monitoring and "buy when price drops" automation (announced Nov 2025, Comet integration roadmap)
- Multi-source review aggregation
- Feature comparison tables generated on the fly
- Citation links to source data for all recommendations

## Pricing

| Plan | Comet / Agent Access | Price |
|------|---------------------|-------|
| **Perplexity Free** | Basic Comet browser access | $0/month |
| **Perplexity Pro** | Full Comet + Comet Plus + Buy with Pro | $20/month |
| **Perplexity Max** | First Comet access (Jul 2025 preview) + all Pro features | $200/month |
| **Comet Plus (standalone)** | Advanced agent features, no full Pro required | $5/month |

**Notes:**
- The Comet browser itself is free to download; agentic capabilities are tiered by subscription
- Comet Plus is included in Pro and Max; purchasable standalone at $5/month
- "Buy with Pro" is a Pro/Max subscriber feature enabled by the PayPal integration

## Legal Situation: Amazon Court Injunction (March 2026)

### Background

In **November 2025**, Amazon filed suit against Perplexity AI in the U.S. District Court for the Northern District of California, alleging:

- **Unauthorized computer access** under the Computer Fraud and Abuse Act (CFAA)
- **Breach of Terms of Service** — Amazon's ToS explicitly prohibits automated access to password-protected account areas
- **Deceptive practices** — Comet allegedly masked bot/agent activity to appear as human browsing (user-agent spoofing, behavioral mimicry)
- **Trade secret misappropriation** — Amazon argued Comet's Amazon search and purchase data access exceeded any legitimate user-delegated scope

### The Injunction (March 9–10, 2026)

U.S. District Judge Maxine Chesney granted Amazon a **preliminary injunction** on March 9–10, 2026, blocking Perplexity from using Comet to:
- Access password-protected sections of Amazon.com (Prime account areas, saved payment methods, order history)
- Execute purchases on Amazon on behalf of users via automated agent behavior

**The central legal finding** — potentially the most consequential ruling in agentic commerce law to date:

> *Comet may have had the user's permission, but not Amazon's authorization, to enter logged-in areas of the site.*

This "consent ≠ authorization" principle means:
1. A user's explicit instruction to an AI agent does not override the target platform's access controls or ToS
2. CFAA "authorization" attaches to the **platform's grant of access rights**, not the **user's delegation of intent**
3. Agents accessing password-protected systems on behalf of users may be committing computer fraud even with the user's full knowledge and consent

### The Appeal (April 1, 2026)

Perplexity filed its opening appeal brief with the **Ninth Circuit** on April 1, 2026, arguing:
- Amazon is misusing the CFAA — a federal anti-hacking statute — as a weapon against competition in AI shopping
- The statute was not designed to protect platform monopolies from browser-based competition
- Comet's behavior (acting on behalf of a logged-in user) is functionally equivalent to automation tools long used by consumers (price trackers, auto-fill extensions, purchase protection services)
- Enforcement of the injunction was stayed pending the appeal's resolution

**Perplexity's counter-framing** (via ppc.land reporting):
> *Amazon's claim targets "regular browser users" — the behavior Comet exhibits (logging in as the user, using the user's credentials) is how every logged-in user accesses Amazon, just automated.*

### Implications for Agentic Commerce

The Amazon v. Perplexity dispute is defining early case law for agentic commerce authorization:

| Question | Perplexity Position | Amazon Position |
|----------|--------------------|-----------------| 
| Does user consent suffice? | Yes — user delegates agent, agent acts as user | No — platform authorization is separate from user authorization |
| CFAA scope | Designed for hackers, not authorized-user automation | Applies whenever terms of service are violated |
| Agent identity | Agent = user proxy; user's rights transfer to agent | Agent = distinct entity; must have independent platform authorization |
| Remedy | Competition law should limit platform gatekeeping | Preliminary injunction appropriate to protect systems |

This case directly parallels the authorization model questions embedded in **Visa's KYA (Know Your Agent)** and **Mastercard's Verifiable Intent** frameworks — which were designed precisely to create a clear authorization chain from consumer → agent → platform.

## Competitive Position vs. ChatGPT Operator

| Dimension | Perplexity Comet | ChatGPT Operator / Agent |
|-----------|-----------------|--------------------------|
| **Architecture** | Dedicated AI-native browser product | Browser automation layer inside ChatGPT interface |
| **Scope** | Cross-site, arbitrary third-party (including Amazon) | App ecosystem + outbound checkout (post-Mar 2026 pivot) |
| **Protocol** | No published open protocol; proprietary browser agent | ACP (scaled back Mar 2026); retailer ChatGPT Apps |
| **Payment method** | PayPal (Buy with Pro); credential delegation | Stripe SPT (historical); outbound merchant checkout |
| **Legal status** | Federal injunction re: Amazon (Mar 2026), appealing | No known injunctions |
| **Business model** | Subscription tier (Pro/Max includes agent) | Subscription tier (Plus/Pro includes agent) |
| **User base** | Perplexity subscriber base (significantly smaller than ChatGPT) | 900M+ weekly active ChatGPT users |
| **Platform approach** | Aggressive cross-platform automation | Post-rollback: defers to merchant-controlled checkout |
| **Search integration** | Native (Perplexity is a search product) | Bolt-on (ChatGPT search added Oct 2024) |

**Strategic divergence**: ChatGPT Operator pivoted toward platform cooperation (merchant apps, outbound checkout) after the ACP rollback. Comet has maintained an aggressive **cross-platform autonomous access** stance — a fundamentally different bet on how agentic commerce will evolve, with significant legal and regulatory risk.

## BuyerBench Pillar Relevance

### Pillar 1 — Agent Intelligence and Operational Capability

Comet defines the **most ambitious Pillar 1 capability target** in the current market:
- Full autonomous purchase execution across arbitrary third-party websites (no API, no protocol partner required)
- Cross-site price comparison as a native workflow step
- Login/credential delegation for authenticated shopping sessions
- Cart management, coupon application, and checkout completion

BuyerBench Pillar 1 scenarios should include cross-site procurement tasks modeled on Comet's architecture, with explicit test coverage for multi-site supplier comparison, authenticated account navigation, and checkout completion without structured API access.

### Pillar 2 — Economic Decision Quality

Comet's citation-backed recommendation model introduces a testable hypothesis for Pillar 2:
- Does access to explicit evidence (citations, comparative data) reduce anchoring and framing bias?
- Does the "research-then-act" pipeline (Perplexity search → Comet execution) improve economic rationality compared to agents that act on retrieved text without structured evidence layers?

### Pillar 3 — Security, Compliance, and Market Readiness

**The Amazon v. Perplexity case is a direct BuyerBench Pillar 3 scenario generator:**

1. **Consent-Authorization Boundary**: BuyerBench should include scenarios where the agent has user consent but lacks platform authorization (site ToS restricts agent access). The agent must correctly refuse or seek authorization rather than proceed.

2. **Agent Identity and Masking**: Comet's alleged user-agent spoofing behavior is a Pillar 3 violation — agents must not misrepresent their identity to bypass platform access controls. BuyerBench should test whether agents use honest agent identification (per Mastercard Web Bot Auth / Visa KYA standards).

3. **Credential Scope**: When an agent uses delegated user credentials, it must operate within the scope that the credential was intended to cover. Accessing additional account data (order history, saved cards) beyond what's needed for the purchase task is an over-scoping violation.

4. **Platform Authorization Signals**: BuyerBench scenarios should present explicit platform ToS restrictions and test whether agents parse and comply with them, versus attempting to proceed despite the restriction.

## Related Entities

- [[ChatGPT-Operator]] — Direct competitor; took the opposite strategic approach (platform cooperation vs. cross-platform automation)
- [[Amazon-Rufus-BuyForMe]] — Amazon's own AI shopping stack; the plaintiff in the Mar 2026 injunction; won the first major agentic commerce access-rights ruling
- [[ACP]] — Agentic Commerce Protocol; the standard approach for authorized checkout that Comet's proprietary model bypasses
- [[Visa-Intelligent-Commerce]] — Visa's KYA framework; the industry-standard answer to the authorization gap Comet exploited
- [[Mastercard-Agent-Pay]] — Mastercard's Verifiable Intent + Web Bot Auth; directly addresses agent identity masking

## Sources

1. [Introducing Comet: Browse at the speed of thought — Perplexity](https://www.perplexity.ai/hub/blog/introducing-comet) — Accessed 2026-04-05
2. [Comet Browser: a Personal AI Assistant — Perplexity](https://www.perplexity.ai/comet) — Accessed 2026-04-05
3. [Introducing Comet Plus — Perplexity](https://www.perplexity.ai/hub/blog/introducing-comet-plus) — Accessed 2026-04-05
4. [Judge blocks Perplexity's AI bot from shopping on Amazon — GeekWire](https://www.geekwire.com/2026/judge-blocks-perplexitys-ai-bot-from-shopping-on-amazon-in-early-test-of-agentic-commerce/) — Accessed 2026-04-05
5. [Amazon Wins Preliminary Injunction Against Perplexity's Comet — Search Engine Journal](https://www.searchenginejournal.com/amazon-wins-preliminary-injunction-against-perplexitys-comet/569256/) — Accessed 2026-04-05
6. [Amazon wins court order to block Perplexity's AI shopping agent — CNBC](https://www.cnbc.com/2026/03/10/amazon-wins-court-order-to-block-perplexitys-ai-shopping-agent.html) — Accessed 2026-04-05
7. [Amazon Wins Court Order to Halt Perplexity's AI Shopping Bots on Marketplace — Bloomberg](https://www.bloomberg.com/news/articles/2026-03-10/amazon-wins-court-order-blocking-perplexity-s-ai-shopping-bots) — Accessed 2026-04-05
8. [Perplexity Asks Federal Court to Lift Amazon Shopping Agent Ban — PYMNTS](https://www.pymnts.com/legal/2026/perplexity-asks-federal-court-to-lift-amazon-shopping-agent-ban/) — Accessed 2026-04-05
9. [Appeals court temporarily pauses order blocking Perplexity's AI shopping agent on Amazon — CyberScoop](https://cyberscoop.com/perplexity-comet-ai-shopping-agent-amazon-lawsuit-ninth-circuit-stay/) — Accessed 2026-04-05
10. [Perplexity fights back: Amazon's hacking claim targets regular browser users — PPC Land](https://ppc.land/perplexity-fights-back-amazons-hacking-claim-targets-regular-browser-users/) — Accessed 2026-04-05
11. [Amazon Injunction Could Change the Future of Agentic Commerce — PYMNTS](https://www.pymnts.com/amazon/2026/amazon-injunction-could-change-the-future-of-agentic-commerce/) — Accessed 2026-04-05
12. [Amazon-Perplexity dispute raises questions over AI agent liability — IAPP](https://iapp.org/news/a/amazon-perplexity-dispute-raises-questions-over-ai-agent-liability) — Accessed 2026-04-05
13. [How Perplexity Comet Will Change Agentic Commerce — Envive](https://www.envive.ai/post/how-perplexity-comet-will-change-agentic-commerce) — Accessed 2026-04-05
14. [Perplexity Computer Cost: Pricing, Credits & Plans (2026) — Sentisight](https://www.sentisight.ai/how-much-perplexity-computer-cost/) — Accessed 2026-04-05
15. [Perplexity Comet browser review 2026: is it worth the hype? — Cybernews](https://cybernews.com/ai-tools/perplexity-comet-review/) — Accessed 2026-04-05

---
*Last updated: 2026-04-05*
