# Phase 01: Profile Pending Protocols & Products

This phase profiles the 9 highest-priority entities that were discovered but never researched: the 4 agentic payment protocols (AP2/UCP, x402, Visa Intelligent Commerce, Mastercard Agent Pay) and the 5 major product/platform entries (Amazon Rufus/Buy for Me, ChatGPT Operator/Shopping, Perplexity Comet, Salesforce Agentforce, NegMAS). These are the market-facing, commercially deployed entities most directly relevant to BuyerBench's three pillars. By the end of this phase, the vault will have 15 fully populated entity profiles (up from 6) and the INDEX will be updated to reflect the new coverage.

## Tasks

- [x] Read the existing vault INDEX and entity discovery log to understand profile conventions, then read one existing company profile and the ACP protocol profile to match format exactly:
  - Read `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/INDEX.md`
  - Read `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/LOOP_00001_ENTITIES.md` (scan for all Protocol and Product entries)
  - Read `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/Technologies/ACP.md` (use as profile format reference)
  - Read `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/Companies/Skyfire.md` (use as company profile format reference)

- [x] Research and profile the AP2/UCP protocol (Google):
  - Web search: "AP2 UCP Google agentic payment protocol 2025 2026"
  - Web search: "Google AP2 autonomous purchase protocol partners specification"
  - Create `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/Protocols/AP2-UCP.md` with YAML front matter (type: protocol, tags: [payment-protocol, google, authorization, agentic-commerce]) and sections: Overview, How It Works, Key Partners (60+), Coverage (payment authorization + checkout layer), Comparison to ACP, BuyerBench Pillar Relevance, wiki-links to [[ACP]], [[Visa-Intelligent-Commerce]], [[Skyfire]]
  <!-- Completed 2026-04-05: Created Protocols/AP2-UCP.md. Key findings: AP2 = payment authorization via cryptographic Intent+Cart mandates (VC-signed); UCP = full commerce orchestration (discovery→fulfillment); co-launched NRF Jan 11, 2026 with 60+ partners including all 5 major card networks. AP2 has native x402 crypto extension. Both protocols REST/MCP/A2A compatible. -->

- [x] Research and profile the x402 protocol (Coinbase/HTTP-native micropayments):
  - Web search: "x402 Coinbase HTTP 402 micropayment protocol AI agents 2025"
  - Web search: "x402 payment required protocol specification cryptographic"
  - Create `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/Protocols/x402.md` with YAML front matter (type: protocol, tags: [payment-protocol, coinbase, micropayments, http, crypto]) and sections: Overview, HTTP 402 Mechanism, Cryptographic Payment Model, Use Cases for AI Agents, Adoption Status, Comparison to ACP and AP2, BuyerBench Pillar Relevance, wiki-links to [[ACP]], [[AP2-UCP]]
  <!-- Completed 2026-04-05: Created Protocols/x402.md. Key findings: launched Sep 2025 by Coinbase+Cloudflare; revives HTTP 402 status code for pay-per-request USDC micropayments; uses EIP-712/EIP-3009 gasless signing; ~2s settlement on Base; x402 Foundation (Coinbase, Cloudflare, AWS, Anthropic, Circle); native AP2 crypto extension; early adoption — ~$28K/day volume with ~50% artificial activity per CoinDesk Mar 2026; complementary to ACP/AP2 (different layers). -->

- [x] Research and profile Visa Intelligent Commerce + Trusted Agent Protocol:
  - Web search: "Visa Intelligent Commerce agentic payment 2025 KYA identity"
  - Web search: "Visa Trusted Agent Protocol October 2025 tokenization"
  - Web search: "Visa AI agent payment launch April 2025 partners"
  - Create `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/Protocols/Visa-Intelligent-Commerce.md` with YAML front matter (type: protocol, tags: [payment-protocol, visa, tokenization, identity, KYA]) and sections: Overview, KYA (Know Your Agent) Identity Layer, Launch Timeline (Apr 2025 initial + Oct 2025 Trusted Agent Protocol), Partner Ecosystem, Token Model, Comparison to Mastercard Agent Pay, BuyerBench Pillar Relevance, wiki-links to [[Mastercard-Agent-Pay]], [[ACP]], [[Skyfire]]
  <!-- Completed 2026-04-05: Created Protocols/Visa-Intelligent-Commerce.md. Key findings: VIC launched Apr 30 2025 with 100+ partners incl. Anthropic, OpenAI, Microsoft, Stripe, Samsung; TAP launched Oct 14 2025 — open framework (HTTP Message Signatures + WebAuthn) with 3-element payload (Agent Intent + Consumer Recognition + Payment Info); KYA = cryptographic root-of-trust linking principal→agent→credential→scope; tens of billions of existing Visa tokens extended to agent use cases; Skyfire KYAPay integration demonstrated Dec 2025; AWS Bedrock AgentCore integration Dec 2025; TAP is direct Pillar 3 reference standard for BuyerBench authentication/authorization scenarios. -->

- [ ] Research and profile Mastercard Agent Pay:
  - Web search: "Mastercard Agent Pay October 2025 tokenization AI agents"
  - Web search: "Mastercard agentic payments identity verification 2025 2026"
  - Create `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/Protocols/Mastercard-Agent-Pay.md` with YAML front matter (type: protocol, tags: [payment-protocol, mastercard, tokenization, identity]) and sections: Overview, Launch (Oct 2025 — same day as Visa), Identity and Tokenization Model, Partner Network, Compliance Hooks, Comparison to Visa Intelligent Commerce, BuyerBench Pillar Relevance, wiki-links to [[Visa-Intelligent-Commerce]], [[ACP]], [[Skyfire]]

- [ ] Research and profile Amazon Rufus / Alexa+ / Buy for Me:
  - Web search: "Amazon Rufus AI shopping agent 2025 2026 features pricing"
  - Web search: "Amazon Buy for Me agent autonomous purchase 2025"
  - Web search: "Alexa Plus AI agent commerce capabilities 2025 2026"
  - Create `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/Products/Amazon-Rufus-BuyForMe.md` with YAML front matter (type: product, tags: [ai-shopping-agent, amazon, consumer, e-commerce]) and sections: Overview, Product Suite (Rufus / Alexa+ / Buy for Me — distinctions), Scale ($12B incremental sales, 300M users), Autonomous Purchase Capabilities, Pricing (consumer pricing if any), Limitations and Restrictions (Perplexity court injunction context), BuyerBench Pillar Relevance, wiki-links to [[Perplexity-Comet]], [[ACP]]

- [ ] Research and profile ChatGPT Operator / Shopping features (post-ACP rollback):
  - Web search: "ChatGPT Operator autonomous agent shopping 2025 2026"
  - Web search: "OpenAI ChatGPT shopping rollback March 2026 future plans"
  - Web search: "OpenAI Responses API agent tools pricing 2026"
  - Create `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/Products/ChatGPT-Operator.md` with YAML front matter (type: product, tags: [ai-agent, openai, operator, shopping, autonomous]) and sections: Overview, Operator Product (what it is, launch date, capabilities), Shopping Feature History (ACP Instant Checkout Sep 2025 → removed Mar 2026), Current State (2026), Pricing (API pricing tiers if applicable), Lessons from ACP Rollback, BuyerBench Pillar Relevance, wiki-links to [[ACP]], [[Perplexity-Comet]]

- [ ] Research and profile Perplexity Comet:
  - Web search: "Perplexity Comet AI shopping agent browser 2025 2026"
  - Web search: "Perplexity Amazon injunction March 2026 Comet"
  - Web search: "Perplexity Comet pricing features autonomous purchase"
  - Create `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/Products/Perplexity-Comet.md` with YAML front matter (type: product, tags: [ai-agent, perplexity, browser-agent, shopping, autonomous]) and sections: Overview, Comet Browser Agent Architecture, Shopping Capabilities, Pricing, Legal Situation (Amazon court injunction Mar 2026), Competitive Position vs. ChatGPT Operator, BuyerBench Pillar Relevance, wiki-links to [[ChatGPT-Operator]], [[Amazon-Rufus-BuyForMe]]

- [ ] Research and profile Salesforce Agentforce with pricing:
  - Web search: "Salesforce Agentforce pricing 2025 2026 per conversation"
  - Web search: "Salesforce Agentforce procurement purchasing agent capabilities"
  - Web search: "Salesforce Agentforce enterprise tier features agent studio"
  - Create `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/Products/Salesforce-Agentforce.md` with YAML front matter (type: product, tags: [ai-agent-platform, salesforce, enterprise, crm, procurement]) and sections: Overview, Agent Types (pre-built + custom), Procurement/Purchasing Use Cases, Pricing (per conversation model — include specific prices found), Integration Ecosystem (Slack, MuleSoft, Data Cloud), Limitations, BuyerBench Pillar Relevance, wiki-links to [[Procure-AI]], [[Omnea]]

- [ ] Research and profile NegMAS (open-source negotiation framework):
  - Web search: "NegMAS negotiation multi-agent system Python framework documentation"
  - Web search: "NegMAS ANAC automated negotiation competition 2025"
  - Web search: "NegMAS benchmark scenarios buyer seller negotiation"
  - Create `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/Products/NegMAS.md` with YAML front matter (type: product, tags: [open-source, negotiation, multi-agent, benchmark, python]) and sections: Overview, Architecture (agents, mechanisms, world), ANAC Competition Integration, Key Algorithms Supported, Installation and Quickstart, Relevance as BuyerBench Test Harness Component, BuyerBench Pillar Relevance, wiki-links to [[Zycus]] (Merlin ANA comparison)

- [ ] Update the vault INDEX.md to reflect all 9 new profiles:
  - Read `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/INDEX.md`
  - Add entries for all 9 new files under their respective sections (Protocols: AP2-UCP, x402, Visa-Intelligent-Commerce, Mastercard-Agent-Pay; Products: Amazon-Rufus-BuyForMe, ChatGPT-Operator, Perplexity-Comet, Salesforce-Agentforce, NegMAS)
  - Update statistics: researched count, category coverage percentages
  - Update "Last Updated" date to 2026-04-05
