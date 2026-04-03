---
type: reference
title: Consumer Shopping Agent Profiles
created: 2026-04-03
tags:
  - agent-profile
  - consumer
  - shopping
related:
  - '[[INDEX]]'
  - '[[AGENT-LANDSCAPE-SUMMARY]]'
  - '[[consumer-agents-evaluation-plan]]'
---

# Consumer Shopping Agent Profiles

Profiles for E01–E03: Amazon Rufus, Klarna AI, and Google Agentic Checkout.
These are consumer-facing products embedded in large platforms.  None provide
a direct evaluation API; all three require indirect evaluation methodology
(browser automation, researcher accounts, or published behavioural studies as
proxy data).

---

## E01 — Amazon Rufus

**Category:** Consumer shopping  
**Ownership:** Amazon (commercial)  
**Licence:** Proprietary / bundled  
**Pricing:** Consumer-facing (free to Amazon customers)  
**Maturity:** Production

### What it is
Amazon Rufus is a conversational shopping assistant embedded in the Amazon app
and website.  It supports product discovery, comparison, and purchase guidance.
Published features include price history tracking, personalised recommendations,
and user-invoked auto-buy capabilities that require explicit authorisation.

### BuyerBench scenarios applicable

| Scenario | Pillar | Rationale |
|---|---|---|
| p1-01 Supplier/Product Selection | P1 | Core discovery and recommendation use case |
| p2-03 Decoy Effect | P2 | Sponsored/featured products act as decoys |
| p2-04 Scarcity | P2 | "Only 3 left in stock" messaging |
| p2-02 Framing | P2 | "Save $X" vs. "X% off" framing variants |
| p3-03 Credential Handling | P3 | Delegated purchase authorization |

### Methodology gap: no direct evaluation API
Rufus is accessible only through:
1. Amazon mobile app (iOS/Android)
2. Amazon.com web interface

There is no public API, SDK, or programmatic interface.  **BuyerBench cannot
evaluate Rufus directly.** Indirect evaluation options:
- **Browser automation (Playwright):** Scripted interactions via the web UI;
  limited by anti-automation measures and account requirements
- **Published case studies:** Amazon's own public announcements describe
  feature behaviour but cannot be used for systematic scenario scoring
- **Human-in-the-loop evaluation:** Research participants replicate
  BuyerBench scenarios manually via the UI; requires IRB approval for studies
  involving real purchases

### Expected strengths
- Rich product catalogue integration → strong discovery performance
- Personalisation signals → may improve selection quality vs. generic agents

### Expected weaknesses
- **Conflict of interest:** Amazon surfaces sponsored products; objective
  recommendation quality conflated with commercial incentives
- **Prompt injection surface:** Seller-controlled product descriptions are
  a natural injection vector (analogous to p3-05 scenario)
- **Preference leakage:** Purchase history used for recommendations creates
  privacy and bias risks not measurable without account-level access

---

## E02 — Klarna AI Shopping Assistant

**Category:** Consumer shopping  
**Ownership:** Klarna (commercial fintech)  
**Licence:** Proprietary / bundled  
**Pricing:** Consumer-facing (free within Klarna app)  
**Maturity:** Production

### What it is
Klarna's AI assistant is embedded in the Klarna shopping and payments app.  It
supports chat-based product search, comparison, and purchase recommendations
integrated with Klarna's buy-now-pay-later (BNPL) payment products.

### BuyerBench scenarios applicable

| Scenario | Pillar | Rationale |
|---|---|---|
| p1-01 Product Selection | P1 | Core recommendation use case |
| p2-02 Framing | P2 | BNPL framing ("pay later") vs. upfront cost |
| p2-04 Scarcity | P2 | Time-limited deals in shopping feed |
| p3-03 Credential Handling | P3 | Integrated payment credential management |

### Methodology gap
Like Rufus, Klarna's AI assistant has no evaluation API.  Additional concerns:
- **Conflicts of interest:** Klarna monetises through merchant affiliate fees;
  recommendations may systematically favour higher-margin products
- **BNPL framing bias:** The agent's native payment product (BNPL) may
  introduce systematic framing effects not present in other agents
  (paying "later" makes total cost feel lower — directly relevant to Pillar 2)

Indirect evaluation via Playwright browser automation is the most tractable
approach, but requires a Klarna account and navigating rate limiting.

---

## E03 — Google AI Mode Shopping and Agentic Checkout

**Category:** Consumer shopping  
**Ownership:** Google (commercial)  
**Licence:** Proprietary / bundled  
**Pricing:** Consumer-facing (bundled with Google Search and Shopping)  
**Maturity:** Production / Emerging (features evolving rapidly in 2025–2026)

### What it is
Google's AI-assisted shopping experience spans AI Mode in Google Search,
Google Shopping surfaces, and "agentic checkout" — a flow where the agent
tracks prices, notifies users of deals, and can execute purchases with user
confirmation.  The UCP (Universal Commerce Protocol) is integrated into
Google's merchant surfaces.

### BuyerBench scenarios applicable

| Scenario | Pillar | Rationale |
|---|---|---|
| p1-01 Supplier/Product Selection | P1 | AI Mode product recommendations |
| p1-03 Quote Comparison Workflow | P1 | Price tracking across merchants |
| p2-01 Anchoring | P2 | Google Shopping price history shown |
| p2-02 Framing | P2 | "X% off" vs. savings amount framing |
| p3-04 Transaction Sequencing | P3 | Agentic checkout flow: track→notify→confirm→buy |
| p3-03 Credential Handling | P3 | Google Pay credential delegation |

### Methodology gap
Google's agentic checkout requires:
1. Google account with Google Pay configured
2. Merchant acceptance of agentic checkout
3. No public API; browser automation required

**Unique advantage vs other consumer agents:** Google's UCP integration and
developer documentation offer more insight into the technical architecture than
Rufus or Klarna, making it a candidate for Playwright-based scenario testing.

See `[[consumer-agents-evaluation-plan]]` for the Playwright methodology.
