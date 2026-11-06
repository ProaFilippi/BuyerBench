---
type: analysis
title: "Market Analysis: AI Buyer Agents and Autonomous Procurement"
created: 2026-04-04
tags:
  - market-research
  - ai-agents
  - procurement
  - agentic-commerce
  - autonomous-buying
related:
  - '[[INDEX]]'
  - '[[Agent-Prompt]]'
---

# Market Analysis: AI Buyer Agents and Autonomous Procurement

## Market Overview

- **Market Size:** Global AI Agents market ~$7.63B (2025), ~$10.91B (2026); Agentic Commerce segment ~$1.90B (2025), ~$2.66B (2026); broader agentic AI enterprise platform market ~$9.89B (2025)
- **Growth Rate:** AI agents CAGR ~42% through 2034 (projected $182.6B); agentic commerce growing toward $135B (2025 total TAM across all agentic channels) and $1.7T by 2030
- **Key Drivers:**
  - LLM capability step-change enabling multi-step autonomous task execution
  - New payment protocols (ACP, AP2/UCP, x402, Visa Intelligent Commerce, Mastercard Agent Pay) enabling agents to actually transact
  - Enterprise cost-reduction pressure: Gartner projects 90% of B2B purchases ($15T+) handled by AI agents by 2028
  - Consumer familiarity with AI assistants lowering trust barriers (520%+ YoY growth in AI ecommerce traffic into Black Friday 2025)
  - Network effects from OpenAI–Amazon strategic partnership (Feb 2026, $50B investment)
- **Key Challenges:**
  - Security & compliance: agents must satisfy PCI DSS, EMV 3DS, tokenization requirements with no direct human in the loop
  - Behavioral vulnerability: agents exhibit position bias, anchoring, decoy susceptibility, and choice homogeneity (studied in ACES framework, arXiv 2508.02630)
  - Legal/competitive friction: Amazon obtained court injunction blocking Perplexity's Comet agent from accessing Amazon marketplace (March 2026)
  - Protocol fragmentation: ACP (OpenAI/Stripe), AP2/UCP (Google/Shopify), x402 (Coinbase), Visa Trusted Agent Protocol all competing for standard adoption
  - Model instability: agent purchasing preferences can shift drastically across model version updates

## Market Segments

1. **Enterprise Procurement Agents (Source-to-Pay AI)** — AI embedded in spend management suites (Coupa, SAP Ariba, Jaggaer, Ivalua) and point solutions (Procure AI, Omnea) that automate supplier discovery, RFQ, bid evaluation, contract negotiation, and PO approval workflows
2. **Consumer Shopping Agents (Delegated Checkout)** — Agents that research, compare, and execute purchases on behalf of consumers: Amazon Rufus/Alexa+/Buy for Me, OpenAI ACP (Instant Checkout, partially rolled back March 2026), Perplexity Comet, Google Shopping AI, Shopify Sidekick
3. **Trading & Investment Buyer Agents** — Algorithmic trading bots (market execution in equities, FX, crypto), DeFi automated market makers, and crypto purchasing agents (x402/Coinbase ecosystem)
4. **Negotiation Buyer Agents** — Formal automated negotiation systems using protocols like alternating offers, auction mechanisms, and multi-lateral deal-making (NegMAS/ANAC ecosystem, commercial variants in B2B SaaS pricing)
5. **Payment-Capable Agents & Commerce Protocols** — The infrastructure layer: ACP (OpenAI + Stripe, Apache 2.0), AP2 (Google, 60+ partners), UCP (Google + Shopify), x402 (Coinbase HTTP payment protocol), Visa Intelligent Commerce + Trusted Agent Protocol, Mastercard Agent Pay

## Competitive Landscape

- **Market Leaders:**
  - **Salesforce** (Agentforce — enterprise agent platform with procurement orchestration)
  - **Microsoft** (Copilot Studio — enterprise agent builder, deep SAP/ERP integration)
  - **Amazon** (Rufus, Alexa+, Buy for Me — dominant consumer agentic commerce; 300M users, $12B incremental sales 2025)
  - **Google** (AP2/UCP protocol author, Vertex AI Agent Builder, Google Shopping AI)
  - **OpenAI** (ACP protocol + ChatGPT Instant Checkout; strategic Amazon partnership Feb 2026)

- **Emerging Players:**
  - **Perplexity** (Comet shopping agent — legal battles with Amazon over marketplace access)
  - **Procure AI** (raised $13M Series A, enterprise source-to-pay AI agents)
  - **Omnea** (enterprise procurement orchestration startup)
  - **Rye** (agentic commerce API infrastructure for merchants)
  - **Stripe** (ACP co-developer + payment backbone for agent transactions)
  - **Coinbase** (x402 protocol — HTTP-native micropayments for agents)

- **Open-Source / Research:**
  - **NegMAS** (yasserfarouk/negmas on GitHub — Python negotiation MAS framework, BSD 3-Clause; backbone of ANAC Automated Negotiation Leagues)
  - **ACES** (Agentic e-CommercE Simulator — research framework for studying agent purchasing biases, arXiv 2508.02630)

- **Recent M&A / Partnerships:**
  - OpenAI ↔ Amazon: $50B strategic investment + commerce partnership (Feb 2026)
  - Visa: partnerships with Anthropic, Microsoft, OpenAI, Perplexity for Intelligent Commerce (Apr 2025)
  - Google AP2: 60+ partners including Mastercard, Adyen, PayPal, Coinbase

## Entity Categories for Research

### Priority Categories (research first)

| Category | Relevance | Target Count |
|----------|-----------|--------------|
| Companies | Core commercial players building buyer agents or enabling infrastructure | 10 |
| Protocols & Standards | Technical specs governing how agents pay and transact — defines the ecosystem's plumbing | 8 |
| Products & Platforms | Specific buyer-agent products to profile and benchmark | 10 |
| Research Papers | Academic foundations for bias testing and evaluation methodology | 8 |
| Security & Compliance Frameworks | PCI DSS, EMV 3DS, tokenization standards — defines Pillar 3 test cases | 6 |

### Secondary Categories (if time permits)

| Category | Relevance | Target Count |
|----------|-----------|--------------|
| Key People | Founders, researchers, and protocol authors shaping the space | 6 |
| Technologies | Underlying tech (LLMs, MCP, function calling, RAG) enabling buyer agents | 5 |
| Trends | Regulatory, behavioral, and market-structure trends for contextual framing | 5 |
| Legal Cases | Emerging case law (e.g., Amazon vs. Perplexity) defining platform boundaries | 3 |

## Entity Templates

### Company Template
- **Name**, Founded, Headquarters, Employees
- **What they do** (1–2 sentences describing their buyer-agent or procurement-AI play)
- **Key products/services** (with links to product profiles)
- **Funding / financials** (latest round, revenue if known)
- **Key people** (CEO, CTO, relevant researchers)
- **Payment/protocol stance** (which protocols they support: ACP, AP2, x402, proprietary)
- **Behavioral/security posture** (any published bias testing, compliance certifications)
- **Recent news** (last 3–6 months)
- **Related entities** (wiki-links to protocols, products, people)
- **Sources** (URLs)

### Protocol / Standard Template
- **Name**, Governing Body, License, Status (draft/live/deprecated)
- **What it does** (1–2 sentences)
- **Scope** (discovery, checkout, payment authorization, full commerce stack)
- **Key participants / adopters**
- **Technical spec** (link to spec/GitHub)
- **Comparison to alternatives** (wiki-links to competing protocols)
- **Compliance alignment** (PCI DSS, EMV, ISO 20022 relevance)
- **Recent developments**
- **Sources**

### Product / Platform Template
- **Name**, Company, Launch Date, Status (GA/beta/discontinued)
- **What it does**
- **Agent capabilities** (can it autonomously transact? Under what conditions?)
- **Pricing model** (transaction fee, subscription, usage-based)
- **Target customers** (consumer, SMB, enterprise)
- **Protocols supported**
- **Known behavioral vulnerabilities** (any documented bias susceptibility)
- **Competitors** (wiki-links)
- **Sources**

### Research Paper Template
- **Title**, Authors, Year, Venue (arXiv/journal/conference)
- **Core finding** (1–2 sentences)
- **Methodology** (simulation, human study, LLM eval)
- **Relevance to BuyerBench** (which pillar(s) this informs)
- **Key metrics / benchmarks introduced**
- **Caveats / limitations**
- **Citation** (BibTeX snippet)
- **Sources**

### Security / Compliance Framework Template
- **Name**, Governing Body, Version, Scope
- **What it governs**
- **Key requirements relevant to AI agents** (specific controls)
- **Gaps in current AI agent implementations**
- **Relevant BuyerBench Pillar 3 test scenarios**
- **Sources**

## Research Priorities

1. **Protocol landscape deep-dive**: Profile ACP, AP2/UCP, x402, Visa Intelligent Commerce, Mastercard Agent Pay, and Visa Trusted Agent Protocol — these define the rules of the game for any agent that can actually pay
2. **Commercial buyer-agent products**: Profile Amazon Rufus/Alexa+, OpenAI ChatGPT ACP, Perplexity Comet, Salesforce Agentforce, Microsoft Copilot Studio, Procure AI, Omnea — understand capability baselines
3. **Bias & evaluation research**: Deep-read arXiv 2508.02630 (ACES framework) and arXiv 2507.21504 (LLM agent eval survey) to ground Pillar 2 test design in published evidence
4. **Pillar 3 compliance mapping**: Map PCI DSS v4.0 controls, EMV 3DS, and PCI SSC AI guidance documents to specific security test scenarios
5. **NegMAS ecosystem**: Profile NegMAS + ANAC league as the reference implementation for Pillar 1 negotiation task scenarios

## Sources Consulted

- [Gartner: AI agents will command $15T in B2B purchases by 2028](https://www.digitalcommerce360.com/2025/11/28/gartner-ai-agents-15-trillion-in-b2b-purchases-by-2028/)
- [Agentic Commerce Market — NextMSC](https://www.nextmsc.com/report/agentic-commerce-market-ic4296)
- [AI Agents Market Size & Share — Grand View Research](https://www.grandviewresearch.com/industry-analysis/ai-agents-market-report)
- [Procure AI Raises $13M — JustAI News](https://justainews.com/industries/b2b-tech/why-every-enterprise-is-betting-big-on-ai-agents-in-2026/)
- [Visa and Mastercard launch agentic AI payments tools](https://www.digitalcommerce360.com/2025/10/16/visa-mastercard-both-launch-agentic-ai-payments-tools/)
- [Mastercard Agent Pay](https://www.mastercard.com/us/en/business/artificial-intelligence/mastercard-agent-pay.html)
- [Agentic Payments: AP2 vs. ACP & x402 — Grid Dynamics](https://www.griddynamics.com/blog/agentic-payments)
- [Agentic Payments Explained: ACP, AP2, x402 — Orium](https://orium.com/blog/agentic-payments-acp-ap2-x402)
- [Visa Intelligent Commerce secure AI transactions](https://corporate.visa.com/en/sites/visa-perspectives/newsroom/visa-partners-complete-secure-agentic-transactions.html)
- [Protocol Wars: Standards Battle for AI Commerce — FourWeekMBA](https://fourweekmba.com/the-protocol-wars-standards-battle-for-ai-commerce/)
- [AI Shopping Agent Wars 2026 — Modern Retail](https://www.modernretail.co/technology/why-the-ai-shopping-agent-wars-will-heat-up-in-2026/)
- [Amazon vs. Perplexity Comet court ruling](https://decrypt.co/360629/amazon-perplexity-comet-court-order-agentic-commerce)
- [OpenAI + Amazon partnership — Forrester](https://www.forrester.com/blogs/power-couple-openai-amazon-may-have-just-won-consumer-agentic-commerce/)
- [What Is Your AI Agent Buying? (ACES, arXiv 2508.02630)](https://arxiv.org/abs/2508.02630)
- [Evaluation and Benchmarking of LLM Agents survey (arXiv 2507.21504)](https://arxiv.org/html/2507.21504v1)
- [PCI SSC: AI and Payments — Pitfalls and Security Risks](https://blog.pcisecuritystandards.org/ai-and-payments-exploring-pitfalls-and-potential-security-risks)
- [Agentic AI for PCI DSS & PSD2 — FluxForce](https://www.fluxforce.ai/blog/agentic-ai-for-pci-dss-psd2)
- [Agentic AI Security Threats — Stellar Cyber](https://stellarcyber.ai/learn/agentic-ai-securiry-threats/)
- [NegMAS GitHub](https://github.com/yasserfarouk/negmas)
- [ANL 2025 — Automated Negotiation League](https://autoneg.github.io/anl2025/)
- [State of AI in Procurement 2026 — Art of Procurement](https://artofprocurement.com/blog/state-of-ai-in-procurement)
- [McKinsey: Redefining procurement in era of agentic AI](https://www.mckinsey.com/capabilities/operations/our-insights/redefining-procurement-performance-in-the-era-of-agentic-ai)
- [Agentic Commerce Landscape 2026 — Rye](https://rye.com/blog/agentic-commerce-startups)
- [AI Shopping Agents Guide 2026 — Opascope](https://opascope.com/insights/ai-shopping-assistant-guide-2026-agentic-commerce-protocols/)
