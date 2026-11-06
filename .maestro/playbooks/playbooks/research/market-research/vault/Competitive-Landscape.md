---
type: analysis
title: "Global Competitive Landscape — AI Buyer Agents and Autonomous Procurement"
created: 2026-04-06
tags:
  - competitive-analysis
  - global
  - market-map
  - synthesis
related:
  - '[[INDEX]]'
  - '[[Brazil/INDEX]]'
  - '[[Pricing-Registry]]'
  - '[[Brazil/Brazil-vs-Global-Analysis]]'
  - '[[BuyerBench-Scenario-Recommendations]]'
---

# Global Competitive Landscape — AI Buyer Agents and Autonomous Procurement

> Synthesis document covering all 37 entities in the vault. Last updated: 2026-04-06. See [[INDEX]] for full entity list.

---

## Market Map

The global market for AI buyer agents and autonomous procurement spans four distinct structural layers. Players frequently operate at multiple layers simultaneously, creating vertical integration advantages (Amazon, Google) and enabling ecosystem lock-in (OpenAI, Salesforce).

---

### Layer 1 — Procurement Platforms

AI-native or AI-augmented software that automates buyer workflows: intake, sourcing, negotiation, supplier management, and P2P execution.

| Player | Type | Scope | Pillar Relevance |
|--------|------|-------|-----------------|
| [[Companies/Procure-AI\|Procure AI]] | AI-native startup | Full source-to-pay; 50+ autonomous agents | Pillar 1 (execution depth) |
| [[Companies/Omnea\|Omnea]] | AI-native startup | Orchestration-first; intake + vendor onboarding | Pillar 1, 2 (CFO economics) |
| [[Companies/Zycus\|Zycus]] | Incumbent S2P suite | End-to-end suite + Merlin ANA negotiation agent | Pillar 1, 2 (ANA bias-test target) |
| [[Companies/Fairmarkit\|Fairmarkit]] | Specialist autonomous sourcing | Demand-to-award; 150K+ zero-touch events/yr | Pillar 1 (throughput baseline) |
| [[Products/Salesforce-Agentforce\|Salesforce Agentforce]] | Enterprise CRM + agent platform | B2B procurement + supply chain agents | Pillar 1, 2, 3 (governance reference) |
| **SAP Ariba / Coupa** | Legacy S2P incumbents | Broad enterprise; AI being retrofitted | Not yet profiled |
| **Pactum AI** | Specialist autonomous negotiation | Supplier price negotiation at scale (Walmart, Maersk) | Not yet profiled |

**Architecture divergence note**: Procure AI deploys 50+ autonomous execution agents; Omnea orchestrates workflows + humans; Zycus embeds agents in a mature suite; Fairmarkit targets full hands-off event execution. These represent four distinct design philosophies for the same procurement AI problem — each testable in BuyerBench Pillar 1.

---

### Layer 2 — AI Agent Runtimes and Foundation Models

Cloud platforms and model APIs that procurement agent builders use to construct buyer agents. This layer is where per-token and per-compute pricing is set.

| Player | Key Products | Pricing Anchor | Pillar Relevance |
|--------|-------------|----------------|-----------------|
| [[Companies/Amazon-Agentic-Commerce\|Amazon]] | Nova models + AgentCore + Bedrock Agents | Nova Pro: $0.80/M in; AgentCore: $0.0895/vCPU-hr | Pillars 1+2+3 |
| [[Companies/OpenAI-Agent-Platform\|OpenAI]] | GPT-5 family + Agents SDK + Operator | gpt-5.2: $1.75/M in; ChatGPT Pro: $200/mo | Pillars 1+2+3 |
| [[Companies/Google-Agentic-Commerce\|Google]] | Gemini 2.5 Pro + Project Mariner + Vertex AI Agent Engine | Gemini Pro: $1.25/M in; Vertex Agent Engine: $0.00994/vCPU-hr | Pillars 1+3 |
| [[Companies/Skyfire\|Skyfire]] | KYA identity + multi-rail wallets | Infrastructure layer; no model pricing | Pillar 3 (payment rails) |

**Critical pricing insight**: Google's Vertex AI Agent Engine at $0.00994/vCPU-hr is **~9× cheaper** than Amazon's AgentCore at $0.0895/vCPU-hr — a dramatic runtime cost difference for high-throughput procurement agent workloads. This creates a structural economic incentive for procurement platform builders to prefer Google's infrastructure.

**Agent cost multiplier warning**: Across all three major platforms (Amazon, OpenAI, Google), multi-step agentic workflows consume **5–10× more tokens** per user intent than single-turn LLM calls, due to reasoning traces, tool calls, and synthesis steps. This non-linear cost scaling is a key constraint for BuyerBench scenario design and enterprise deployment economics.

---

### Layer 3 — Payment Infrastructure

The financial rails, authorization protocols, and fraud detection systems that enable AI agents to execute transactions autonomously.

| Player | Core Offering | Authorization Model | Compliance Layer |
|--------|--------------|--------------------|-----------------| 
| [[Companies/Stripe-Agent-Payments\|Stripe]] | ACP co-author; Shared Payment Tokens (SPT); Radar fraud | Delegated token (buyer-issued SPT with governance rules) | PCI DSS, EMV 3DS, full KYC |
| [[Companies/Coinbase-Agent-Payments\|Coinbase]] | x402 protocol; Agentic Wallets; USDC on Base | Wallet signature (cryptographic) | GENIUS Act, FinCEN MSB; no PCI DSS |
| [[Companies/Skyfire\|Skyfire]] | KYAPay open protocol; multi-rail agent wallets | KYA identity + just-in-time decisioning | PCI DSS (card rail); FATF (USDC rail) |

**Complementary positioning**: Stripe and Coinbase publicly positioned as complementary rather than competitive: Stripe integrated x402 in Feb 2026 and co-founded the x402 Foundation with Coinbase in Apr 2026. The emerging consensus is a **dual-rail model** — Stripe/ACP for $10+ regulated fiat transactions; Coinbase/x402 for sub-$10 micropayments where Stripe's 2.9%+$0.30 flat fee is economically prohibitive.

---

### Layer 4 — Standards and Protocols

Open specifications governing how AI agents identify themselves, obtain payment authorization, and execute commerce transactions.

| Protocol | Maintainer | Scope | Status (Apr 2026) |
|----------|-----------|-------|-------------------|
| [[Technologies/ACP\|ACP (Agentic Commerce Protocol)]] | OpenAI + Stripe | Agent checkout API; SPT credential model | Narrowed to 7 retailers + Shopify after Mar 2026 rollback |
| [[Protocols/AP2-UCP\|AP2 / UCP]] | Google (60+ partners incl. all 5 card networks) | Full lifecycle: discovery → mandate → payment → fulfillment | Expanding; NRF Jan 2026 launch; UCP in Google Search AI Mode |
| [[Protocols/x402\|x402]] | Coinbase (x402 Foundation with Cloudflare, Stripe) | HTTP-native USDC micropayments | Active; 160M+ transactions; ~$28K/day real commerce volume |
| [[Protocols/Visa-Intelligent-Commerce\|Visa Intelligent Commerce + TAP]] | Visa (100+ partners) | KYA identity; Trusted Agent Protocol; open framework | Fully live; 10+ TAP partners |
| [[Protocols/Mastercard-Agent-Pay\|Mastercard Agent Pay]] | Mastercard | Agent registration; Agentic Tokens; Verifiable Intent | Live (US cardholders, Nov 2025); Web Bot Auth via Cloudflare |

**Protocol momentum shift**: ACP launched in September 2025 and controlled the narrative briefly — but Google's AP2/UCP (NRF, Jan 2026) landed with 60+ partners including all 5 card networks, while ACP rolled back Instant Checkout in March 2026. AP2/UCP enters Q2 2026 with stronger institutional backing and broader retailer adoption.

---

## Competitive Clusters

### Cluster 1 — Procurement Orchestration

**Core battleground**: Source-to-pay automation for enterprise buyers. The fundamental question is the architectural approach: autonomous execution agents (Procure AI), orchestration + human-in-the-loop (Omnea), AI-augmented incumbent suite (Zycus), or specialist sourcing automation (Fairmarkit).

**Key dynamics**:
- **AI-native vs. suite-embedded**: Procure AI and Omnea can move faster but lack the breadth of Zycus; Zycus has enterprise relationships but slower innovation cycles
- **Execution depth vs. orchestration breadth**: Fairmarkit excels at zero-touch sourcing events; Omnea excels at cross-functional approval orchestration — different value propositions for different workflow stages
- **Platform attachment**: Salesforce Agentforce competes here via CRM-native Buyer Agent + Supply Chain Agent, but requires existing Salesforce org — high adoption cost for greenfield buyers
- **Merlin ANA as the negotiation differentiator**: Zycus's Merlin ANA (autonomous supplier negotiation) is the most directly competitive capability against startups' negotiation automation claims; Pactum AI (Walmart, Maersk) is the specialized leader not yet profiled

**Cluster players**: [[Companies/Procure-AI]], [[Companies/Omnea]], [[Companies/Zycus]], [[Companies/Fairmarkit]], [[Products/Salesforce-Agentforce]], [[Products/NegMAS]]

---

### Cluster 2 — Consumer Browser Agent

**Core battleground**: Autonomous cross-site purchasing on behalf of individual users. The battleground is whether agents should operate via open protocols (ACP, AP2/UCP) on merchant-controlled checkout flows, or directly navigate any site autonomously.

**Key dynamics**:
- **Protocol cooperation vs. aggressive automation**: ChatGPT Operator/Agent pivoted post-ACP-rollback toward merchant-controlled checkout apps. Perplexity Comet maintained aggressive cross-site autonomy — and received a federal injunction for accessing Amazon without platform authorization
- **Legal precedent (consent ≠ authorization)**: The Amazon v. Perplexity ruling (Mar 2026) defines that user consent does not equal platform authorization under CFAA. This reshapes all browser agents' risk calculus
- **Amazon's dual role**: Amazon is both a platform operator (blocking Perplexity) and an agent deployer (Rufus, Buy for Me) — it is simultaneously a competitor and a gatekeeper for the category

**Cluster players**: [[Products/Amazon-Rufus-BuyForMe]], [[Products/ChatGPT-Operator]], [[Products/Perplexity-Comet]]

---

### Cluster 3 — Platform Agent Infrastructure

**Core battleground**: Who provides the foundation models, agent runtimes, and commerce protocols that procurement platforms and shopping agents are built on?

**Key dynamics**:
- **Amazon's vertical integration advantage**: Controls model (Nova) + orchestration (Bedrock Agents) + runtime (AgentCore) + marketplace (Amazon.com/Business) + consumer agent (Rufus/Buy for Me) — no other player spans this full stack
- **OpenAI's infrastructure dependency risk**: Most procurement AI startups (Procure AI, Fairmarkit, Omnea) build on OpenAI APIs — OpenAI can reprice or compete directly with any capability it exposes
- **Google's protocol + compute leadership**: AP2/UCP has more institutional support than ACP; Vertex AI Agent Engine is 9× cheaper than AgentCore; Project Mariner holds the browser agent capability benchmark (83.5% WebVoyager vs. no published OpenAI Operator benchmark)
- **AWS as neutral ground**: OpenAI's $50B AWS partnership positions AWS as the preferred cloud for OpenAI models — a strategic tension given Amazon's own Nova/AgentCore competition with OpenAI

**Cluster players**: [[Companies/Amazon-Agentic-Commerce]], [[Companies/OpenAI-Agent-Platform]], [[Companies/Google-Agentic-Commerce]]

---

### Cluster 4 — Agent Payment Rail

**Core battleground**: Which infrastructure layer handles the financial settlement when AI agents execute transactions?

**Key dynamics**:
- **Stripe owns the regulated fiat lane**: ACP co-authorship + SPT + Radar fraud detection + existing $1.4T volume gives Stripe a durable position in enterprise and consumer agent payments requiring chargebacks and PCI DSS compliance
- **Coinbase owns the micropayment / permissionless lane**: x402 is the only economically viable payment method for sub-$10 agent-to-API transactions; the x402 Foundation (Stripe + Coinbase + Cloudflare) formalizes the industry split
- **Skyfire is the identity-first infrastructure layer**: KYA + KYAPay + multi-rail wallets serve as the abstraction above both Stripe and Coinbase rails — connecting agent identity to transaction authorization
- **Visa and Mastercard are the authorization standards layer**: VIC/TAP and Agent Pay define how agents are credentialed and how transactions are authorized at the card network level — orthogonal to, and supporting, the Stripe/Coinbase settlement layer

**Cluster players**: [[Companies/Stripe-Agent-Payments]], [[Companies/Coinbase-Agent-Payments]], [[Companies/Skyfire]], [[Protocols/Visa-Intelligent-Commerce]], [[Protocols/Mastercard-Agent-Pay]]

---

## Head-to-Head Comparisons

### Procurement Platform Comparisons

| Player A | Player B | Key Differentiator (A vs. B) | Pricing (A) | Pricing (B) | Primary Pillar |
|----------|----------|------------------------------|-------------|-------------|----------------|
| [[Companies/Procure-AI\|Procure AI]] | [[Companies/Omnea\|Omnea]] | Procure AI: full autonomous execution (50+ agents, end-to-end S2P). Omnea: orchestration + human-in-the-loop; CFO-facing intelligence layer | Custom enterprise; no public pricing | Custom enterprise; no public pricing | Pillar 1 |
| [[Companies/Zycus\|Zycus]] | [[Companies/Fairmarkit\|Fairmarkit]] | Zycus: full S2P suite + Merlin ANA autonomous negotiation. Fairmarkit: specialist autonomous sourcing (demand-to-award); 5× ProcureTech100 | Custom; estimated $100–200M ARR | $78M raised; no public per-seat pricing | Pillar 1 + 2 |
| [[Companies/Procure-AI\|Procure AI]] | [[Companies/Zycus\|Zycus]] | Procure AI: AI-native from scratch; ROI in months. Zycus: 25+ yr incumbent; ANA is production-deployed; SAP Ariba displacement | $13M seed; early-stage | Bootstrapped; mature; 2,500 employees | Pillar 1 |
| [[Products/Salesforce-Agentforce\|Agentforce]] | [[Companies/Procure-AI\|Procure AI]] | Agentforce: CRM-native; best-in-class governance (audit trail, Agent Script, least-privilege). Procure AI: standalone; no Salesforce dependency | $2/conv or $0.10/action or $125+/user/mo | $13M seed; custom pricing | Pillar 1, 3 |

### Consumer Browser Agent Comparisons

| Player A | Player B | Key Differentiator | Pillar 3 Risk | Legal Status |
|----------|----------|-------------------|--------------|--------------|
| [[Products/ChatGPT-Operator\|ChatGPT Operator/Agent]] | [[Products/Perplexity-Comet\|Perplexity Comet]] | ChatGPT: merchant-app cooperation model; outbound checkout post-Mar 2026. Comet: aggressive cross-site autonomous access | ChatGPT: ACP rollback = protocol-available-but-disabled risk. Comet: CFAA injection risk | ChatGPT: clean. Comet: federal injunction (Amazon, Mar 2026) |
| [[Products/Amazon-Rufus-BuyForMe\|Amazon Rufus/Buy for Me]] | [[Products/ChatGPT-Operator\|ChatGPT Operator/Agent]] | Amazon: 250M+ users; ecosystem-native; price-triggered auto-buy. ChatGPT: 900M+ WAU but limited to merchant apps post-rollback | Both test user consent vs. platform authorization | Amazon: injunction plaintiff (Perplexity). ChatGPT: no injunction |
| [[Products/Perplexity-Comet\|Perplexity Comet]] | [[Products/Amazon-Rufus-BuyForMe\|Amazon Buy for Me]] | Comet: cross-site autonomy via credential delegation. Buy for Me: Amazon-controlled; no credential exposure to third-party sites | Comet: CFAA; agent masking allegations. Buy for Me: encryption credential injection at external sites | Comet: enjoined from Amazon. Buy for Me: no restrictions |

### Agent Runtime Platform Comparisons

| Player A | Player B | Differentiator | A Runtime Pricing | B Runtime Pricing |
|----------|----------|---------------|-------------------|-------------------|
| [[Companies/Amazon-Agentic-Commerce\|Amazon AgentCore]] | [[Companies/Google-Agentic-Commerce\|Google Vertex Agent Engine]] | Amazon: tightest vertical integration (model + runtime + marketplace). Google: 9× cheaper compute; broader protocol network (AP2/UCP with 60+ partners) | $0.0895/vCPU-hr | $0.00994/vCPU-hr |
| [[Companies/OpenAI-Agent-Platform\|OpenAI Agents SDK]] | [[Companies/Google-Agentic-Commerce\|Google Vertex AI]] | OpenAI: largest developer ecosystem; Traces dashboard; provider-agnostic SDK. Google: cheaper compute; Project Mariner has published 83.5% WebVoyager benchmark (OpenAI Operator has no published benchmark) | Operator: $200/mo (Pro) | Mariner: $249.99/mo (AI Ultra) |
| [[Companies/Amazon-Agentic-Commerce\|Amazon Nova Pro]] | [[Companies/OpenAI-Agent-Platform\|OpenAI GPT-5.2]] | Amazon: 10.5× cheaper per input token vs. GPT-5.2; tighter AWS ecosystem integration. OpenAI: frontier reasoning quality; largest API ecosystem | $0.80/M tokens in | $1.75/M tokens in |

### Payment Rail Comparisons

| Player A | Player B | Differentiator | Best Use Case |
|----------|----------|---------------|--------------|
| [[Companies/Stripe-Agent-Payments\|Stripe ACP + SPT]] | [[Companies/Coinbase-Agent-Payments\|Coinbase x402]] | Stripe: regulated fiat; chargebacks; Radar fraud; PCI DSS compliance. Coinbase: permissionless; sub-$10 micropayments; ~$0 gas on Base | Stripe wins for $10+ regulated transactions. Coinbase wins for sub-$10 micropayments |
| [[Companies/Skyfire\|Skyfire KYAPay]] | [[Protocols/Visa-Intelligent-Commerce\|Visa TAP]] | Skyfire: infrastructure-agnostic KYA identity + multi-rail wallets (cards+ACH+USDC). Visa: card-network-native; 10+ TAP partners; directly extends existing Visa token ecosystem | Skyfire: greenfield agent payment infrastructure. Visa TAP: extending existing Visa merchant base |
| [[Protocols/ACP\|ACP]] | [[Protocols/AP2-UCP\|AP2 / UCP]] | ACP: Stripe-centric; narrowed to 7 retailers post-rollback; Apache 2.0. AP2/UCP: 60+ partners, all 5 card networks; full lifecycle (discovery→fulfillment); crypto native via x402 | ACP: existing Stripe merchants wanting agent checkout. AP2/UCP: retailers wanting broadest agent buyer coverage |

---

## Notable Competitive Events Timeline (2025–2026)

| Date | Event | Players | Significance |
|------|-------|---------|-------------|
| **2025-04-30** | Visa Intelligent Commerce launches | [[Protocols/Visa-Intelligent-Commerce\|Visa]], Anthropic, Microsoft, OpenAI, Perplexity | First major card network agent identity framework; 100+ partners in first cohort |
| **2025-05-07** | Stripe Payments Foundation Model announced | [[Companies/Stripe-Agent-Payments\|Stripe]], Nvidia | AI fraud detection trained on $1.4T+ transactions; GPU infrastructure partnership |
| **2025-06-26** | Skyfire launches open KYAPay protocol | [[Companies/Skyfire\|Skyfire]] | First open specification for AI agent identity + payment; Apache-licensed |
| **2025-08** | ANAC 2025 (16th edition) at IJCAI, Montreal | [[Products/NegMAS\|NegMAS]] | Milestone for autonomous negotiation benchmarking; NegMAS officially named the engine |
| **2025-09-25** | OpenAI ACP Instant Checkout goes live | [[Companies/OpenAI-Agent-Platform\|OpenAI]], [[Companies/Stripe-Agent-Payments\|Stripe]] | First production agentic commerce checkout; 4% merchant fee; Etsy + Shopify |
| **2025-10-14** | **Visa TAP + Mastercard Agent Pay both launch on the same day** | [[Protocols/Visa-Intelligent-Commerce\|Visa]], [[Protocols/Mastercard-Agent-Pay\|Mastercard]] | Both major card networks launch agent payment frameworks simultaneously; direct competitive signal to Stripe/Coinbase |
| **2025-11** | Amazon sues Perplexity over Comet bot access | [[Companies/Amazon-Agentic-Commerce\|Amazon]], [[Products/Perplexity-Comet\|Perplexity]] | First major legal challenge to autonomous shopping agents; CFAA theory |
| **2025-11-13** | Amazon Business unveils AI procurement tools | [[Companies/Amazon-Agentic-Commerce\|Amazon]] | AI Assistant + Savings Insights + Anomaly Monitoring for B2B buyers |
| **2025-12-11** | Omnea raises $50M Series B | [[Companies/Omnea\|Omnea]] | Signals continued investor conviction in procurement orchestration despite uncertain macro |
| **2025-12-18** | Skyfire × Visa live KYAPay purchase demo | [[Companies/Skyfire\|Skyfire]], [[Protocols/Visa-Intelligent-Commerce\|Visa]] | First publicly demonstrated full-stack agentic commerce purchase: identity + payment + execution |
| **2026-01-06** | Amazon launches Alexa.com at CES | [[Companies/Amazon-Agentic-Commerce\|Amazon]] | Alexa+ extends to web; voice-native agentic commerce reaches web surface |
| **2026-01-11** | Google launches AP2 + UCP at NRF | [[Companies/Google-Agentic-Commerce\|Google]] | Sundar Pichai keynote; 60+ partners, all 5 card networks; positioned as industry-consensus alternative to ACP |
| **2026-02-04** | Alexa+ broadly available in US | [[Companies/Amazon-Agentic-Commerce\|Amazon]] | 70+ LLMs; Expedia, Yelp, Angi, Square integrations; agentic household commerce |
| **2026-02-05** | OpenAI Frontier enterprise platform launches | [[Companies/OpenAI-Agent-Platform\|OpenAI]] | Enterprise agent operations for HP, Oracle, State Farm, Uber; enterprise pivot post-ACP |
| **2026-02-11** | Coinbase Agentic Wallets GA | [[Companies/Coinbase-Agent-Payments\|Coinbase]] | First wallet infrastructure purpose-built for AI agents; CDP Portal + gasless on Base |
| **2026-02-27** | **OpenAI + Amazon $50B strategic partnership** | [[Companies/OpenAI-Agent-Platform\|OpenAI]], [[Companies/Amazon-Agentic-Commerce\|Amazon]] | OpenAI models in Amazon Bedrock; AWS as preferred OpenAI cloud; signals co-opetition at infrastructure layer |
| **2026-03-04** | **OpenAI removes ACP Instant Checkout from ChatGPT** | [[Companies/OpenAI-Agent-Platform\|OpenAI]], [[Products/ChatGPT-Operator\|ChatGPT Operator]] | ACP narrowed to 7 retailers; merchant apps replace in-chat checkout; AP2/UCP gains momentum |
| **2026-03-10** | **Amazon wins preliminary injunction blocking Perplexity Comet from Amazon.com** | [[Companies/Amazon-Agentic-Commerce\|Amazon]], [[Products/Perplexity-Comet\|Perplexity Comet]] | Landmark ruling: user consent ≠ platform authorization under CFAA; defines dual-authorization requirement for all browser agents |
| **2026-03-18** | Stripe + Tempo launch Machine Payments Protocol (MPP) | [[Companies/Stripe-Agent-Payments\|Stripe]] | Pre-authorized budgets + streamed micropayments; A2A payment pattern |
| **2026-04-01** | Perplexity appeals Amazon injunction (9th Circuit) | [[Products/Perplexity-Comet\|Perplexity]] | Enforcement stayed pending appeal; CFAA-as-competition-suppressor argument |
| **2026-04-02** | Coinbase + Stripe + Cloudflare co-found x402 Foundation | [[Companies/Coinbase-Agent-Payments\|Coinbase]], [[Companies/Stripe-Agent-Payments\|Stripe]] | Formalizes complementary positioning; micropayment layer becomes community-governed open standard |

---

## White Space and Gaps Identified

### Gap 1 — Brazil-Specific Procurement Infrastructure
No global procurement platform (Procure AI, Omnea, Zycus, Fairmarkit, Agentforce) has documented Pix payment integration, NF-e fiscal validation, or LGPD compliance as a native capability. Brazil represents a $234B+ B2B e-commerce market ($18.42% CAGR) with ERP dominance by TOTVS (not SAP) — creating a structural opportunity for Brazil-native players (Freedom, Zinit, Linkana) that global players have not yet addressed. See [[Brazil/Brazil-vs-Global-Analysis]] for detailed analysis.

### Gap 2 — Formal Negotiation in Production
NegMAS's SAOMechanism implements theoretically optimal bilateral negotiation protocols (Nash bargaining, Pareto-frontier discovery), but no production enterprise procurement platform uses formal mechanism-design negotiation. Zycus Merlin ANA and Pactum AI both use LLM-driven negotiation rather than formal protocols. The academic precision of NegMAS does not yet translate into production deployment — leaving the "best possible negotiation outcome" question unanswered at enterprise scale.

### Gap 3 — Crypto Payment Rails in Enterprise Procurement
No enterprise procurement platform (Procure AI, Omnea, Zycus, Fairmarkit, Agentforce) has integrated x402 or Coinbase Agentic Wallets. The micropayment use case (API-per-call billing, sub-$1 data access) is not yet addressed in enterprise source-to-pay tooling. Skyfire's multi-rail wallet is the only bridge between enterprise procurement identity (KYA) and crypto payment rails.

### Gap 4 — Open Agent Identity Standard
Despite Skyfire's KYAPay, Visa's TAP, and Mastercard's Verifiable Intent all addressing agent identity, there is no single universally adopted "Know Your Agent" standard. The market is fragmented across three competing identity frameworks with different cryptographic architectures. This creates compliance uncertainty for enterprises deploying buyer agents across multiple platforms.

### Gap 5 — AI-vs-AI Procurement Scenarios
Fairmarkit's 2025 AI in Procurement Index found 94% of procurement leaders report that their suppliers now use AI in negotiations. No public benchmark (including BuyerBench) yet measures buyer agent performance in adversarial AI-vs-AI negotiation scenarios — where the seller's AI actively attempts anchoring, framing, and manipulation tactics against the buyer's AI.

### Gap 6 — Behavioral Bias Testing in Production
ACES (arXiv:2508.02630) documented 5× position bias and +1.0–+1.9 endorsement effects in AI buyer agents, but no commercial procurement platform publicly measures or reports bias susceptibility as a product metric. BuyerBench Pillar 2 would be the first standardized benchmark to generate comparable bias-susceptibility data across agents.

### Gap 7 — Audit Trail Portability
Salesforce Agentforce compiles agent decisions into JSON audit artifacts. Zycus Merlin ANA logs full negotiation transcripts. But these audit trails are platform-proprietary — there is no common audit trail format that can be compared across platforms, verified by third parties, or used as evidence in a procurement dispute across vendor relationships. A standardized agent decision audit format remains an unaddressed white space.

### Gap 8 — Agent Authorization for Government Procurement
Brazil's Compras.gov.br/PNCP and public sector procurement globally require specific authorization chains (NF-e validation, contract registration) that no current AI agent payment protocol (ACP, AP2/UCP, x402) addresses. Government procurement remains outside the coverage scope of all Layer 3 payment infrastructure players.

---

## Wiki-Links to All Profiled Entities

### Companies
- [[Companies/Procure-AI]] · [[Companies/Omnea]] · [[Companies/Zycus]] · [[Companies/Fairmarkit]] · [[Companies/Skyfire]]
- [[Companies/Amazon-Agentic-Commerce]] · [[Companies/OpenAI-Agent-Platform]] · [[Companies/Google-Agentic-Commerce]]
- [[Companies/Stripe-Agent-Payments]] · [[Companies/Coinbase-Agent-Payments]]

### Products
- [[Products/Amazon-Rufus-BuyForMe]] · [[Products/ChatGPT-Operator]] · [[Products/Perplexity-Comet]]
- [[Products/Salesforce-Agentforce]] · [[Products/NegMAS]]

### Protocols and Standards
- [[Technologies/ACP]] · [[Protocols/AP2-UCP]] · [[Protocols/x402]]
- [[Protocols/Visa-Intelligent-Commerce]] · [[Protocols/Mastercard-Agent-Pay]]

### Security and Compliance Frameworks
- [[Security-Compliance/PCI-DSS-v4]] · [[Security-Compliance/EMV-3DS2]] · [[Security-Compliance/NIST-AI-RMF]]
- [[Security-Compliance/ISO-42001]] · [[Security-Compliance/FATF-AML-CFT]]

### Research Papers
- [[Research-Papers/ACES-AI-Agent-Buying]] · [[Research-Papers/LLM-Agent-Benchmarking-Survey]]
- [[Research-Papers/AgentBench]] · [[Research-Papers/WebArena]] · [[Research-Papers/WebShop]]

### Key People
- [[People/Amine-Allouah]] · [[People/Omar-Besbes]] · [[People/Yasser-Mohammad]]
- [[People/Kevin-Frechette]] · [[People/Amir-Sarhangi]] · [[People/Rubail-Birwadker]] · [[People/Jorn-Lambert]]

### Brazil Market (Sub-Vault)
- [[Brazil/INDEX]] · [[Brazil/Brazil-vs-Global-Analysis]] · [[Brazil/Regulatory/Brazil-Compliance-Overview]]
- [[Brazil/Market-Context/Brazil-AI-Procurement-Landscape]] · [[Brazil/Market-Context/Brazil-Fintech-Payment-Landscape]]
- [[Brazil/Market-Context/Brazil-ERP-Landscape]] · [[Brazil/Market-Context/Global-Players-Brazil-Presence]]

---

## Cross-Reference Navigation

| If you want to understand... | Start here |
|------------------------------|-----------|
| Global pricing across all entities | [[Pricing-Registry]] |
| Brazil vs. global market comparison | [[Brazil/Brazil-vs-Global-Analysis]] |
| BuyerBench scenario design recommendations | [[BuyerBench-Scenario-Recommendations]] |
| Full entity list and vault statistics | [[INDEX]] |
| Brazil entity coverage | [[Brazil/INDEX]] |

---
*Synthesis document created: 2026-04-06 | Phase 06 Task 2 — CladiBuyer Benchmarker*
