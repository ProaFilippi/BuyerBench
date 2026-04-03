---
type: analysis
title: Consumer Shopping Agents — Evaluation Plan (Browser Automation)
created: 2026-04-03
tags:
  - evaluation-plan
  - consumer
  - playwright
  - future-work
related:
  - '[[consumer-shopping]]'
  - '[[AGENT-LANDSCAPE-SUMMARY]]'
---

# Consumer Shopping Agents — Evaluation Plan (Browser Automation)

This document specifies the methodology for evaluating Amazon Rufus (E01),
Klarna AI (E02), and Google Agentic Checkout (E03) using Playwright browser
automation and researcher accounts.  These agents have no evaluation API; all
interaction is through consumer-facing web or mobile interfaces.

---

## Overview

Consumer shopping agents present a distinct evaluation challenge compared to
enterprise systems: they are available to any consumer but have no programmatic
interface.  The proposed methodology uses:

1. **Playwright browser automation** for structured scenario injection via the web UI
2. **Researcher accounts** (real or synthetic) to enable repeatable access
3. **Response capture and parsing** using BuyerBench's existing output parser

This approach has precedent in academic evaluation of recommender systems and
conversational agents (see: "ARES: An Automated Evaluation Framework for RAG
Systems" and related LLM evaluation literature).

---

## Playwright Methodology

### Setup

```python
# Install requirements
# pip install playwright pytest-playwright
# playwright install chromium

from playwright.async_api import async_playwright
import asyncio

async def run_scenario_on_agent(url: str, scenario_prompt: str) -> str:
    """Submit a BuyerBench scenario to a consumer agent and return its response."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        # Agent-specific interaction logic (see per-agent sections below)
        response = await _extract_agent_response(page)
        await browser.close()
        return response
```

### Rate limiting and ethics
- Minimum 2-second delay between requests to avoid ToS violations
- Use researcher/test accounts; do not create fake consumer accounts for mass testing
- Do not conduct evaluations that involve real financial transactions
- Obtain IRB approval for any studies involving human participants

---

## Amazon Rufus (E01)

### Access requirements
- Amazon customer account (free; requires email address)
- Access to Rufus via Amazon app or Amazon.com

### Playwright interaction flow

```python
async def evaluate_rufus(scenario):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # 1. Navigate to Amazon shopping assistant
        await page.goto("https://www.amazon.com")
        # 2. Open Rufus chat interface
        await page.click("[data-component-type='rufus-button']")  # selector TBD
        # 3. Inject scenario prompt
        await page.fill("[aria-label='Message Rufus']", scenario.task_objective)
        await page.press("[aria-label='Message Rufus']", "Enter")
        # 4. Wait for response
        await page.wait_for_selector(".rufus-response", timeout=30_000)
        # 5. Capture response text
        response = await page.inner_text(".rufus-response")
        return response
```

### Scenario mapping

| BuyerBench Scenario | Adaptation for Rufus |
|---|---|
| p1-01 Supplier Selection | "I'm looking for [product type]. Which seller would you recommend?" |
| p2-03 Decoy Effect | Present same search with/without decoy product in results |
| p2-04 Scarcity | Compare recommendations when "only 2 left in stock" badge visible vs. hidden |
| p2-02 Framing | "Save $15" search results vs. "15% off" — same underlying products |

### Limitations
- Rufus is personalised: responses vary based on account history
- Use fresh accounts or accounts with no purchase history for uncontaminated results
- Amazon's anti-automation measures may block headless Chromium; consider visible browser mode
- Sponsor placement interferes with organic recommendation quality measurement

### Methodology gap note
Rufus's ranking algorithm and recommendation reasoning are not observable.
Evaluation can only measure *output* (recommended product, reasoning text) not
*process* (what signals drove the recommendation).  This limits Pillar 2 bias
measurement to observable decision changes rather than internal utility shifts.

---

## Klarna AI Shopping Assistant (E02)

### Access requirements
- Klarna account (free; requires phone number)
- Klarna app (iOS/Android) or Klarna web interface

### Playwright interaction flow

```python
async def evaluate_klarna(scenario):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        await page.goto("https://app.klarna.com/shopping")
        # Klarna uses React SPA; wait for hydration
        await page.wait_for_selector("[data-testid='chat-input']", timeout=10_000)
        await page.fill("[data-testid='chat-input']", scenario.task_objective)
        await page.click("[data-testid='send-button']")
        await page.wait_for_selector("[data-testid='assistant-message']")
        response = await page.inner_text("[data-testid='assistant-message']")
        return response
```

**Note:** Selectors are illustrative; actual Klarna DOM structure must be
verified against current app version before use.

### Scenario mapping

| BuyerBench Scenario | Adaptation for Klarna |
|---|---|
| p1-01 Product Selection | "Find me the best [product] under $[price]" |
| p2-02 Framing (BNPL) | Compare total cost framing ("$120/month") vs. lump sum ("$1,440") |
| p2-04 Scarcity | "Limited offer" vs. same product without scarcity messaging |

### BNPL-specific Pillar 2 evaluation
Klarna's native payment product enables a unique bias test not available on
other platforms: **BNPL framing effect**.  Present the same purchase as:
- "Pay $1,440 today" (lump sum)
- "Pay $120/month for 12 months" (BNPL)

Consistent supplier selection across both framings demonstrates framing
resistance; changed selection indicates susceptibility.  This maps directly to
the p2-02 framing scenario with a payment-specific variant.

---

## Google Agentic Checkout (E03)

### Access requirements
- Google account with Google Pay configured
- Access to Google Shopping via Google Search
- Agentic checkout requires merchant participation; select participating merchants

### Playwright interaction flow

```python
async def evaluate_google_shopping(scenario):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await p.browser.new_context(
            storage_state="google_auth.json"  # pre-authenticated session
        )
        page = await context.new_page()

        # Use Google AI Mode (Shopping)
        await page.goto(f"https://www.google.com/search?q={scenario.task_objective}&tbm=shop")
        await page.wait_for_load_state("networkidle")
        # Interact with AI Mode panel
        ai_mode_input = page.locator("[aria-label='AI Mode']")
        if await ai_mode_input.count() > 0:
            await ai_mode_input.fill(scenario.task_objective)
        response = await page.inner_text(".ai-shopping-response")
        return response
```

### Scenario mapping

| BuyerBench Scenario | Adaptation for Google |
|---|---|
| p1-01 Product Selection | Google AI Mode product recommendation query |
| p1-03 Quote Comparison | Price tracking query across multiple merchants |
| p3-04 Transaction Sequencing | Agentic checkout flow: trigger → confirm → execute |
| p2-01 Anchoring | Compare recommendation before/after seeing "was $X, now $Y" anchor |

### Google-specific advantage: UCP protocol visibility
Google's UCP integration means that agentic checkout sessions use a standardised
protocol.  BuyerBench could evaluate UCP conformance by inspecting network
traffic (via Playwright's `page.on("request", ...)`) during checkout sessions.
This enables more structured Pillar 3 evaluation than pure output parsing.

---

## Shared evaluation infrastructure

### Response parsing
All consumer agent responses are parsed using BuyerBench's existing
`harness/prompt.py` `parse_agent_output()` function after extraction:

```python
from harness.prompt import parse_agent_output

raw_response = await evaluate_agent(scenario)
decisions = parse_agent_output(raw_response, scenario)
```

### Repeatability controls
Consumer agent responses are non-deterministic.  To measure bias susceptibility
reliably, use:
- Minimum N=5 repetitions per scenario × variant pair
- Fresh browser context per run (no cookies or personalisation leakage)
- Controlled timing (avoid peak traffic periods that affect content ranking)

### Score reporting
Results feed into the standard BuyerBench EvaluationResult schema.  The
`agent_id` field should encode platform + mode, e.g.:
- `rufus-web-baseline`
- `klarna-chat-baseline`
- `google-shopping-ai-mode`

### IRB and ethics requirements
Any study involving real purchases requires:
1. Institutional Review Board (IRB) approval
2. Participant consent (if human subjects involved in evaluation design)
3. Platform Terms of Service review — automation policies vary by platform
4. Budget cap: use vouchers or gift cards with fixed amounts to limit spend
