---
type: reference
title: "Global Pricing Registry — AI Buyer Agent Ecosystem"
created: 2026-04-06
tags:
  - pricing
  - registry
  - global
  - brazil
  - comparison
related:
  - '[[INDEX]]'
  - '[[Brazil/INDEX]]'
  - '[[Competitive-Landscape]]'
  - '[[Brazil-vs-Global-Analysis]]'
---

# Global Pricing Registry — AI Buyer Agent Ecosystem

> A consolidated reference of publicly available pricing across all 37 vault entities — global and Brazil. Enterprise SaaS procurement platforms universally withhold public pricing; infrastructure and consumer platforms publish granular rates. This asymmetry is itself a market observation.

---

## Navigation

- [Global Pricing Table](#global-pricing-table)
- [Brazil Pricing Table](#brazil-pricing-table)
- [Pricing Observations](#pricing-observations)
- [Entity Quick-Reference Index](#entity-quick-reference-index)

---

## Global Pricing Table

### AI Model APIs — Per-Token Inference Costs

| Entity | Model / Tier | Input ($/M tokens) | Output ($/M tokens) | Cached Input | Source Date |
|--------|-------------|-------------------|---------------------|-------------|-------------|
| [[OpenAI-Agent-Platform]] | gpt-5.2 (flagship) | $1.75 | $14.00 | $0.175 | 2026-04 |
| [[OpenAI-Agent-Platform]] | gpt-5.1 | $1.25 | $10.00 | $0.125 | 2026-04 |
| [[OpenAI-Agent-Platform]] | gpt-5-mini | $0.25 | $2.00 | $0.025 | 2026-04 |
| [[OpenAI-Agent-Platform]] | gpt-5-nano (lightest) | $0.05 | $0.40 | $0.005 | 2026-04 |
| [[OpenAI-Agent-Platform]] | GPT-4.1 | $2.00 | $8.00 | — | 2026-04 |
| [[OpenAI-Agent-Platform]] | GPT-4o (post-Dec 2025 cut) | $2.50 | $10.00 | — | 2026-04 |
| [[OpenAI-Agent-Platform]] | o3 (reasoning) | $2.00 | $8.00 | — | 2026-04 |
| [[Google-Agentic-Commerce]] | Gemini 2.5 Pro (≤200K ctx) | $1.25 | $10.00 | — | 2026-04 |
| [[Google-Agentic-Commerce]] | Gemini 2.5 Pro (>200K ctx) | $2.50 | $10.00 | — | 2026-04 |
| [[Google-Agentic-Commerce]] | Gemini 2.5 Flash | $0.15 | $0.60 | — | 2026-04 |
| [[Google-Agentic-Commerce]] | Gemini 2.0 Flash | $0.10 | $0.40 | — | 2026-04 |
| [[Google-Agentic-Commerce]] | Gemini 2.0 Flash-Lite | $0.075 | $0.30 | — | 2026-04 |
| [[Google-Agentic-Commerce]] | Gemini 1.5 Pro (≤200K ctx) | $1.25 | $5.00 | — | 2026-04 |
| [[Amazon-Agentic-Commerce]] | Nova Micro (text) | $0.035 | $0.14 | — | 2026-04 |
| [[Amazon-Agentic-Commerce]] | Nova Lite (multimodal) | $0.060 | $0.24 | — | 2026-04 |
| [[Amazon-Agentic-Commerce]] | Nova Pro (complex reasoning) | $0.80 | $3.20 | — | 2026-04 |
| [[Amazon-Agentic-Commerce]] | Nova Premier (highest capability) | Contact AWS | Contact AWS | — | 2026-04 |
| [[Amazon-Agentic-Commerce]] | Claude 3.5 Haiku (via Bedrock) | ~$0.80 | ~$4.00 | — | 2026-04 |
| [[Amazon-Agentic-Commerce]] | Claude 3.5 Sonnet (via Bedrock) | ~$3.00 | ~$15.00 | — | 2026-04 |

> **Agent cost multiplier warning:** Multi-step agentic workflows consume 5–10× the raw token volume of a single-turn completion, due to reasoning traces, tool calls, and synthesis steps. Budget accordingly when evaluating API costs for BuyerBench runs.

---

### AI Model APIs — Batch & Caching Discounts

| Entity | Discount Type | Rate | Notes |
|--------|--------------|------|-------|
| [[OpenAI-Agent-Platform]] | Batch API | 50% off input + output | All models; for offline evaluation pipelines |
| [[OpenAI-Agent-Platform]] | Priority API surcharge | 2× standard | Guaranteed low-latency SLA |
| [[Google-Agentic-Commerce]] | Context caching (cached reads) | $0.25/M tokens | Fixed prefix caching on Gemini models |
| [[Google-Agentic-Commerce]] | Free tier (AI Studio) | 0 | Up to 15 req/min, 1M tokens/min, 1,500 req/day on Gemini 2.0 Flash |
| [[Amazon-Agentic-Commerce]] | Provisioned Throughput | Negotiated | Reserved capacity; eliminates per-token cost for predictable workloads |

---

### Agent Runtime / Orchestration Infrastructure

| Entity | Service | Fee | Unit | Notes |
|--------|---------|-----|------|-------|
| [[Amazon-Agentic-Commerce]] | AgentCore Runtime | $0.0895 | /vCPU-hour | Active use only; idle = free |
| [[Amazon-Agentic-Commerce]] | AgentCore Gateway | Per call | /1,000 API calls | — |
| [[Amazon-Agentic-Commerce]] | Knowledge Bases (OpenSearch) | $345+ | /month (min) | Fixed storage cost regardless of usage |
| [[Amazon-Agentic-Commerce]] | Bedrock Flows | $0.035 | /1,000 node transitions | Billed from Feb 2025 |
| [[Amazon-Agentic-Commerce]] | Amazon Business AI tools | $0 | Bundled | No additional charge with Amazon Business |
| [[Amazon-Agentic-Commerce]] | New AWS customer credits | $200 | One-time | Free-tier credit for new accounts |
| [[Google-Agentic-Commerce]] | Vertex AI Agent Engine vCPU | $0.00994 | /vCPU-hour | Active runtime only; 9× cheaper than AgentCore |
| [[Google-Agentic-Commerce]] | Vertex AI Agent Engine memory | $0.0105 | /GiB-hour | Active runtime only |
| [[Google-Agentic-Commerce]] | Vertex AI Sessions | Billed per session-second | — | Paid since Feb 11, 2026 |
| [[Google-Agentic-Commerce]] | Vertex AI Data Store queries | $2.00 | /1,000 queries | Enterprise search |
| [[Google-Agentic-Commerce]] | Grounding with Google Search | $35.00 | /1,000 queries | For RAG-based agents |
| [[Google-Agentic-Commerce]] | Gemini API free tier | $0 | — | Google AI Studio only; not on Vertex AI |

---

### API Tool Usage Costs (OpenAI Responses API)

| Entity | Tool | Cost | Notes |
|--------|------|------|-------|
| [[OpenAI-Agent-Platform]] | Web Search (gpt-4o) | $30 | /1,000 queries | — |
| [[OpenAI-Agent-Platform]] | Web Search (gpt-4o-mini / 4.1-mini) | Fixed 8,000 input tokens | /call | Billed as token consumption |
| [[OpenAI-Agent-Platform]] | Code Interpreter | $0.03 | /container session | — |
| [[OpenAI-Agent-Platform]] | File Search storage | $0.10 | /GB/day | First GB free |
| [[OpenAI-Agent-Platform]] | File Search queries | $2.50 | /1,000 calls | — |
| [[OpenAI-Agent-Platform]] | Remote MCP | Output tokens only | /call | No tool call fee |
| [[ChatGPT-Operator]] | Computer Use tool (CUA) | $3.00/$12.00 | /1M input/output | Research preview; tier 3–5 only |

---

### Consumer Subscription Tiers — Global Agents

| Entity | Plan | Price (USD) | Agent / Agentic Access | Notes |
|--------|------|-------------|------------------------|-------|
| [[ChatGPT-Operator]] / [[OpenAI-Agent-Platform]] | Free | $0/month | None | Basic ChatGPT only |
| [[ChatGPT-Operator]] / [[OpenAI-Agent-Platform]] | Plus | $20/month | Operator (waitlist post Feb 2026) | Limited usage |
| [[ChatGPT-Operator]] / [[OpenAI-Agent-Platform]] | Pro | $200/month | Operator + full agent; immediate access | Same price as Google AI Ultra |
| [[ChatGPT-Operator]] / [[OpenAI-Agent-Platform]] | Team | $30/user/month | Agent mode | Team/collaborative workspace |
| [[ChatGPT-Operator]] / [[OpenAI-Agent-Platform]] | Enterprise | Custom (≥$30/user/month) | Operator + Frontier; custom rate limits | — |
| [[OpenAI-Agent-Platform]] | Frontier (enterprise agent platform) | Custom only | Enterprise autonomous agent management | HP, Oracle, State Farm, Uber |
| [[Google-Agentic-Commerce]] | Google One (AI Basic) | $19.99/month | Standard Gemini | No Project Mariner |
| [[Google-Agentic-Commerce]] | Google AI Pro | $19.99/month | Gemini 2.5 Pro access | No Project Mariner |
| [[Google-Agentic-Commerce]] | Google AI Ultra | $249.99/month | Project Mariner + full Gemini suite + 1TB storage | Highest-capability consumer tier |
| [[Google-Agentic-Commerce]] | Gemini Enterprise | $30/user/month | All Google AI tools; retail CX agents | Business subscription |
| [[Perplexity-Comet]] | Free | $0/month | Basic Comet browser | Limited agentic features |
| [[Perplexity-Comet]] | Pro | $20/month | Full Comet + Comet Plus + Buy with Pro (PayPal) | — |
| [[Perplexity-Comet]] | Max | $200/month | First Comet access (Jul 2025 preview) + all Pro | Same price as ChatGPT Pro |
| [[Perplexity-Comet]] | Comet Plus (standalone) | $5/month | Advanced agent features | Available without full Pro |
| [[Amazon-Rufus-BuyForMe]] | Rufus | $0 | AI product discovery + auto-buy | Bundled in Amazon app |
| [[Amazon-Rufus-BuyForMe]] | Buy for Me | $0 (beta) | Cross-site autonomous checkout | No separate subscription |
| [[Amazon-Rufus-BuyForMe]] | Alexa+ | Amazon Prime / Echo device pricing | Multi-domain voice commerce | No per-transaction fee |

---

### Enterprise Procurement SaaS — Global

| Entity | Model | Price | Unit | Notes | Source Date |
|--------|-------|-------|------|-------|-------------|
| [[Salesforce-Agentforce]] | Conversations | $2.00 | /conversation (24h) | Being phased out in favor of Flex Credits | 2026-04 |
| [[Salesforce-Agentforce]] | Flex Credits | $0.10 | /agent action | $500 per 100,000 credits; 1 action = 20 credits | 2026-04 |
| [[Salesforce-Agentforce]] | AELA (Agentic Enterprise License) | $125+ | /user/month | Bundled digital workforce; enterprise-wide | 2026-04 |
| [[Procure-AI]] | Enterprise SaaS | Not disclosed | Custom | European enterprise; €50B+ managed spend; ROI in months | 2026-04 |
| [[Omnea]] | Enterprise SaaS | Not disclosed | Custom | London; Spotify, MongoDB, Monzo as customers | 2026-04 |
| [[Zycus]] | S2P Suite (Merlin AI) | Not disclosed | Custom | Self-funded/PE; ~$100–200M ARR est. | 2026-04 |
| [[Fairmarkit]] | Autonomous sourcing | Not disclosed | Custom | Series C; $78M raised; enterprise contracts | 2026-04 |
| [[Skyfire]] | Agent payment infrastructure | Not disclosed | Custom | Enterprise tier launched Mar 2025; startup pricing | 2026-04 |
| [[NegMAS]] | Open source | $0 | Free (MIT) | pip install negmas; no commercial license required | 2026-04 |

---

### Payment Infrastructure — Global (Per-Transaction Rates)

| Entity | Transaction Type | Fee | Currency | Notes |
|--------|-----------------|-----|----------|-------|
| [[Stripe-Agent-Payments]] | US card (standard) | 2.9% + $0.30 | USD | Per successful charge |
| [[Stripe-Agent-Payments]] | UK card | 1.5% + £0.20 | GBP | Per successful charge |
| [[Stripe-Agent-Payments]] | EU card | 1.5% + €0.25 | EUR | Per successful charge |
| [[Stripe-Agent-Payments]] | International card | +1.5% | USD | Cross-border surcharge on top of standard rate |
| [[Stripe-Agent-Payments]] | Currency conversion | +1.0% | — | Additional surcharge |
| [[Stripe-Agent-Payments]] | ACH Direct Debit | 0.8%, cap $5.00 | USD | — |
| [[Stripe-Agent-Payments]] | USDC/crypto (x402) | Gas fees only (~$0) | USD | Via Base network integration |
| [[Stripe-Agent-Payments]] | Chargeback Protection | +$0.04 | USD | /transaction; Stripe absorbs dispute cost |
| [[Stripe-Agent-Payments]] | Radar for Fraud Teams | +$0.02 | USD | /screened transaction; basic Radar included in std. fee |
| [[Stripe-Agent-Payments]] | Connect Express | $2.00/month + 0.25%+$0.25/payout | USD | /active connected account |
| [[Stripe-Agent-Payments]] | Dispute fee | $15.00 | USD | Refunded if merchant wins |
| [[Stripe-Agent-Payments]] | Checkout Optimization revenue lift | +11.9% avg | — | Statistical uplift, not a fee |
| [[Coinbase-Agent-Payments]] | x402 facilitator fee (USDC on Base) | $0 | USD | Coinbase subsidizes; Base L2 gas only |
| [[Coinbase-Agent-Payments]] | Base L2 gas (USDC transfer) | ~$0.001–$0.01 | USD | Per transaction |
| [[Coinbase-Agent-Payments]] | CDP wallet operations (create/sign/broadcast/policy) | $0.005 | USD | /operation |
| [[Coinbase-Agent-Payments]] | CDP free tier | 0 | — | First 5,000 operations/month |
| [[Coinbase-Agent-Payments]] | CDP Prime trading (maker) | 0.00%–0.20% | — | Volume tiers |
| [[Coinbase-Agent-Payments]] | CDP Prime trading (taker) | 0.05%–0.60% | — | Volume tiers |
| [[ChatGPT-Operator]] | ACP merchant fee (historical, Sep 2025–Mar 2026) | 4% | USD | On completed Instant Checkout transactions; discontinued Mar 2026 |

---

### Payment Rail Economics: x402 vs. Stripe Break-Even Analysis

| Transaction Size | Stripe Fee (USD) | x402/Base Fee (USD) | Optimal Rail |
|-----------------|-----------------|---------------------|-------------|
| $0.01 (per-token API call) | $0.31 (3,100%) | ~$0.00001 | [[Coinbase-Agent-Payments]] x402 |
| $0.10 | $0.33 (330%) | ~$0.00001 | [[Coinbase-Agent-Payments]] x402 |
| $1.00 | $0.32 (32%) | ~$0.001 | [[Coinbase-Agent-Payments]] x402 |
| $10.00 | $0.59 (5.9%) | ~$0.001 | Comparable |
| $100.00 | $3.20 (3.2%) | ~$0.005 | [[Stripe-Agent-Payments]] (chargeback protection value) |
| $1,000+ | Negotiated | ~$0.01 | [[Stripe-Agent-Payments]] (enterprise compliance) |

**Rule of thumb:** x402 is economically dominant for sub-$10 agent micropayments; Stripe/ACP is preferred for $10+ transactions requiring compliance, chargeback protection, or enterprise purchasing controls.

---

## Brazil Pricing Table

### Brazilian Fintech / Payment Platforms (BRL-Denominated)

| Entity | Service | Fee | Currency | Notes | Source Date |
|--------|---------|-----|----------|-------|-------------|
| [[Nubank-Nu-Empresas]] | Conta PJ monthly fee | R$ 0 | BRL | Free digital business account | 2026-04 |
| [[Nubank-Nu-Empresas]] | Pix (send/receive) | R$ 0 | BRL | Unlimited free |  2026-04 |
| [[Nubank-Nu-Empresas]] | TED / DOC transfers | R$ 0 | BRL | Free | 2026-04 |
| [[Nubank-Nu-Empresas]] | Boleto issuing (per paid boleto) | R$ 3,00 | BRL | Per paid boleto | 2026-04 |
| [[Nubank-Nu-Empresas]] | ATM withdrawal | R$ 6,50 | BRL | Banco24Horas / Saque e Pague network | 2026-04 |
| [[Nubank-Nu-Empresas]] | Card acquiring — débito | 0,89% | BRL | Tap to Pay | 2026-04 |
| [[Nubank-Nu-Empresas]] | Card acquiring — crédito à vista | 3,15% | BRL | Single installment | 2026-04 |
| [[Nubank-Nu-Empresas]] | Card acquiring — crédito 2x parcelado | 5,39% | BRL | 2-installment credit | 2026-04 |
| [[Nubank-Nu-Empresas]] | Card acquiring — crédito 12x parcelado | 12,40% | BRL | 12-installment credit | 2026-04 |
| [[Stone-StoneCo]] | Conta Stone PJ monthly fee | R$ 0 | BRL | Free digital business account | 2026-04 |
| [[Stone-StoneCo]] | Pix (send/receive) | R$ 0 | BRL | — | 2026-04 |
| [[Stone-StoneCo]] | Boleto issuing | R$ 1–4 | BRL | Varies; typically R$1–4 per paid boleto | 2026-04 |
| [[Stone-StoneCo]] | Card acquiring — débito | ~0,99–1,49% | BRL | Varies by volume; not publicly posted | 2026-04 |
| [[Stone-StoneCo]] | Card acquiring — crédito à vista | ~2,69–3,49% | BRL | Varies by volume | 2026-04 |
| [[Stone-StoneCo]] | Card acquiring — crédito parcelado (2–12x) | ~3,99–5,99% | BRL | Varies by installments | 2026-04 |
| [[ASAAS]] | Conta ASAAS PJ monthly fee | R$ 0 | BRL | Free SMB account; SCD+PI licensed | 2026-04 |
| [[ASAAS]] | Pix receive | R$ 0 | BRL | — | 2026-04 |
| [[ASAAS]] | Boleto receive (per paid boleto) | ~R$ 1,99 | BRL | Typical rate; subject to change | 2026-04 |
| [[ASAAS]] | Credit card receive (à vista) | ~2,99% | BRL | — | 2026-04 |
| [[ASAAS]] | Credit card receive (parcelado) | ~4,99–9,99% | BRL | 2–12 installments | 2026-04 |
| [[ASAAS]] | Receivables anticipation | ~1,5–2,5%/month | BRL | FIDC credit facility; varies by profile | 2026-04 |
| [[ASAAS]] | API access | R$ 0 | BRL | Free with account; ~80+ REST endpoints | 2026-04 |
| [[Celcoin]] | BaaS / Pix transactions | ~R$ 0,05–0,50 | BRL | Per Pix transaction; negotiated B2B; no public rack rate | 2026-04 |
| [[Celcoin]] | Open Finance / ITP / BaaS platform | Custom / Negotiated | BRL | Monthly minimums apply for regulated license access | 2026-04 |
| [[Belvo]] | Data API calls (aggregation) | ~US$ 0,01–0,05 | USD | Per API call; industry benchmark, not confirmed rate | 2026-04 |
| [[Belvo]] | Payment initiation (Pix via Open Finance) | ~US$ 0,10–0,50 | USD | Per Pix initiated; enterprise contracts for volume | 2026-04 |
| [[Belvo]] | Free developer tier | $0 | USD | Limited calls/month for testing | 2026-04 |

---

### Brazilian Enterprise Software (BRL-Denominated Estimates)

| Entity | Tier | Typical Monthly Est. | Currency | Notes | Source Date |
|--------|------|---------------------|----------|-------|-------------|
| [[TOTVS-ERP-Procurement]] | TOTVS Start (SMB, ≤20 users, 1 entity) | R$ 800–2.000 | BRL | Reseller estimates; TOTVS does not publish prices | 2026-04 |
| [[TOTVS-ERP-Procurement]] | TOTVS Midsizê (20–100 users, multi-entity) | R$ 3.000–12.000 | BRL | Reseller estimates | 2026-04 |
| [[TOTVS-ERP-Procurement]] | TOTVS Enterprise (100+ users, full P2P + Fluig) | R$ 15.000–60.000+ | BRL | Reseller estimates; implementation adds 1–3× annual license | 2026-04 |
| [[TOTVS-ERP-Procurement]] | Fluig Voyager 2.0 add-on (GenAI layer) | R$ 80–300 | BRL | /user/month; per-process or per-user licensing | 2026-04 |
| [[Pipefy]] | Starter | Free | USD | Limited workflows; no AI Agents | 2026-04 |
| [[Pipefy]] | Business | ~$20 | USD | /user/month; core workflow automation | 2026-04 |
| [[Pipefy]] | Enterprise | Custom | USD | AI Agents, advanced integrations, SLA | 2026-04 |
| [[Freedom]] | Custom AI agents (enterprise) | Not disclosed | BRL | Project-based or per-seat; Seed-stage startup | 2026-04 |

---

### Brazilian B2B Marketplaces

| Entity | Access Model | Buyer Fee | Seller Fee | Currency | Notes | Source Date |
|--------|-------------|-----------|-----------|----------|-------|-------------|
| [[Mercado-Livre-Negocios]] | CNPJ-gated registration | Free | 10–16% commission (category-dependent) | BRL | B2B wholesale; up to 50% discount vs. consumer | 2026-04 |
| [[Compras-gov-br]] | Government registration required | Free for suppliers | Not disclosed | BRL | Federal procurement portal; mandatory for gov. contracts | 2026-04 |
| [[B2Brazil]] | B2B marketplace | Free basic / premium tiers | Not disclosed | BRL/USD | International B2B trade platform | 2026-04 |

---

## Pricing Observations

### 1. Enterprise Procurement SaaS: Systematic Opacity

The **six core enterprise procurement vendors** — [[Procure-AI]], [[Omnea]], [[Zycus]], [[Fairmarkit]], [[Salesforce-Agentforce]] (Frontier tier), and [[Skyfire]] — do not publish pricing. This is a deliberate enterprise SaaS convention: complex multi-module deployments with implementation costs, custom integrations, and negotiated volume discounts resist standardized pricing. The implication for BuyerBench:

- **Benchmark cost** is not a differentiator among enterprise SaaS procurement platforms — capability and economic outcome quality are.
- **Salesforce Agentforce** is the exception: three concurrent pricing models ($2/conversation, $0.10/action, $125+/user/month AELA) are published, creating the most granular enterprise procurement agent cost model in the vault.
- **Zycus** is bootstrapped/PE-backed (no VC rounds), meaning its pricing is under more profit-discipline pressure than VC-funded competitors — yet still not public.

### 2. Open-Source Free Tier Pattern

[[NegMAS]] is the only vault entity priced at zero with full capability access (MIT license, pip-installable, no API keys). This makes it uniquely valuable for BuyerBench development and scenario validation:

- **No API cost for large-scale testing**: 1,000 NegMAS negotiation runs cost $0 in API fees (only compute).
- **Algorithmic floor**: NegMAS provides the theoretically optimal bilateral negotiation baseline against which commercial agents can be measured.
- Open-source procurement tools (Compras.gov.br, B2Brazil free tier) follow the same zero-marginal-cost model for initial access.

### 3. Per-Transaction Models in Payment Infrastructure

Payment infrastructure shows a clear per-transaction pricing structure across all providers:

| Rail | Cost Model | Best For |
|------|-----------|---------|
| Stripe card (standard) | 2.9% + $0.30 flat | $10+ transactions needing compliance |
| Stripe ACH | 0.8%, capped $5.00 | High-value bank transfers |
| x402/Base USDC | ~$0.001–$0.01 (gas only) | Sub-$10 micropayments, A2A |
| Brazil Pix | R$0 (consumer/SMB) | All transaction sizes within Brazil |
| Brazil boleto | R$1.99–3.00/paid boleto | Invoiced B2B payments |
| Brazil card acquiring (débito) | 0.89–1.49% | Point-of-sale debit |
| Brazil card acquiring (crédito parcelado) | 3.15–12.40% | Installment credit — rates rise with installment count |

**Key asymmetry**: Brazil's Pix is free at zero cost for any amount, while US/EU card rails charge 2.9%+$0.30 minimum. For a $1 transaction, Pix costs $0 while Stripe costs $0.33 — a 33% fee ratio. This creates a structural cost advantage for Brazilian B2B procurement scenarios.

### 4. Consumer Agent Tier Convergence

Three consumer agent products independently converged on the same $200/month "full agentic access" price point:

| Product | Tier | Price | What's Included |
|---------|------|-------|-----------------|
| [[ChatGPT-Operator]] Pro | ChatGPT Pro | $200/month | Operator (immediate), higher rate limits |
| [[Perplexity-Comet]] Max | Perplexity Max | $200/month | Full Comet + Buy with Pro (PayPal) |
| [[Google-Agentic-Commerce]] AI Ultra | Google AI Ultra | $249.99/month | Project Mariner + full Gemini + 1TB |

This price alignment ($200–$250/month) appears to represent the emerging market consensus for **"full agentic consumer capability"** — the level at which browser agents, autonomous purchase execution, and advanced reasoning are bundled. BuyerBench agent cost modeling should use $200/month as the baseline consumer-tier agentic spending threshold.

### 5. Model API Cost Compression Trend

Between 2024 and 2026, API pricing across all three major providers fell by 40–80% for equivalent capability:

- **OpenAI** cut GPT-4o pricing 50% in December 2025 (from $5.00/$15.00 to $2.50/$10.00 per M tokens), simultaneous with GPT-5 launch — classic penetration pricing to prevent migration.
- **Google** launched Gemini 2.5 Flash at $0.15/$0.60 (input/output per M tokens), vs. Gemini 1.5 Pro at $1.25/$5.00 — 8× cheaper for equivalent tasks in Google's own benchmark.
- **Amazon** launched Nova Micro at $0.035/$0.14 — among the lowest published rates for a frontier-grade model, available at a discount in Bedrock on-demand pricing.

**BuyerBench implication:** Cost-per-evaluation is falling rapidly. BuyerBench runs that cost $10/agent in 2024 may cost $1–3 in 2026. Build evaluation pipelines to exploit Batch API discounts (50% off for all OpenAI models) and Gemini context caching.

### 6. Brazil Pricing Competitiveness vs. Global

Comparing Brazil-native infrastructure to global equivalents:

| Dimension | Global (Stripe/AWS) | Brazil (Pix/ASAAS) | Advantage |
|-----------|--------------------|--------------------|-----------|
| Payment rail cost | 2.9%+$0.30 (Stripe) | R$0 (Pix) | Brazil: ~33× cheaper on $1 txn |
| ERP monthly cost | SAP Ariba: $100K+/year enterprise | TOTVS Start: R$800–2,000/month | Brazil: 5–10× cheaper entry |
| SMB payment API | Stripe: 2.9%+$0.30 | ASAAS: R$0 API, R$1.99/boleto | Brazil: cheaper for B2B invoicing |
| Agent runtime compute | AWS AgentCore: $0.0895/vCPU-hr | Google Vertex AI: $0.00994/vCPU-hr | Google: 9× cheaper |
| Open Finance consent | PCI DSS / Stripe only | Free via BCB Open Finance framework | Brazil: regulated free access |

Brazilian procurement infrastructure is **cost-competitive** — in some dimensions dramatically cheaper — than global equivalents. This supports a business case for AI buyer agent deployment in Brazil even at lower average order values.

---

## Entity Quick-Reference Index

### Global — Companies
- [[Procure-AI]] — Enterprise procurement SaaS; pricing not disclosed
- [[Omnea]] — AI SRM platform; pricing not disclosed
- [[Zycus]] — S2P suite with Merlin ANA; pricing not disclosed
- [[Fairmarkit]] — Autonomous sourcing; pricing not disclosed
- [[Skyfire]] — Agent payment infrastructure; pricing not disclosed
- [[Amazon-Agentic-Commerce]] — Nova models, Bedrock, AgentCore (rates above)
- [[OpenAI-Agent-Platform]] — GPT-5 family, Agents SDK, Frontier (rates above)
- [[Google-Agentic-Commerce]] — Gemini 2.5, Project Mariner, Vertex AI (rates above)
- [[Stripe-Agent-Payments]] — ACP, SPT, Radar (rates above)
- [[Coinbase-Agent-Payments]] — x402, CDP wallets, Base USDC (rates above)

### Global — Products
- [[Amazon-Rufus-BuyForMe]] — Free (Rufus, Buy for Me, Alexa+)
- [[ChatGPT-Operator]] — $0–$200/month (Free/Plus/Pro); ACP historical 4% merchant fee
- [[Perplexity-Comet]] — $0–$200/month (Free/Pro/Max); $5/month Comet Plus
- [[Salesforce-Agentforce]] — $2/conversation or $0.10/action or $125+/user/month
- [[NegMAS]] — Free (MIT open source)

### Brazil — Companies
- [[Nubank-Nu-Empresas]] — Free account; R$3/boleto; 0.89–12.40% card acquiring
- [[Stone-StoneCo]] — Free account; ~0.99–5.99% card; R$1–4/boleto
- [[Celcoin]] — B2B negotiated; ~R$0.05–0.50/Pix (estimated)
- [[ASAAS]] — Free account + API; R$1.99/boleto; ~2.99–9.99% card
- [[Belvo]] — Custom; ~US$0.01–0.50 per call/payment
- [[Freedom]] — Not disclosed (enterprise custom)

### Brazil — Products
- [[TOTVS-ERP-Procurement]] — R$800–60,000+/month depending on tier; +R$80–300/user for Fluig Voyager 2.0
- [[Mercado-Livre-Negocios]] — Buyer: free; Seller: 10–16% commission
- [[Pipefy]] — Free starter; ~$20/user/month Business; Enterprise custom
- [[Compras-gov-br]] — Free for registered suppliers
- [[B2Brazil]] — Free basic / premium tiers

---

*Last updated: 2026-04-06 — Vault synthesis document created during Phase 06, Loop 00001*
