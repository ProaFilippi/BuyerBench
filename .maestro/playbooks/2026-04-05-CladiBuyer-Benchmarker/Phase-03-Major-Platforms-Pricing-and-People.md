# Phase 03: Major Platforms, Pricing & Key People

This phase expands coverage beyond the original 25 discovered entities to profile the large platform players — Amazon, OpenAI, Google, Salesforce, Stripe, and Coinbase — that were flagged in the entity discovery log but never fully profiled. These are the incumbents building agentic commerce infrastructure, and their pricing models, API economics, and strategic positioning are critical context for understanding the competitive landscape. This phase also builds out the People section of the vault with key founders, executives, and researchers shaping this space.

## Tasks

- [x] Read existing vault structure and product profiles from Phase 01 before creating any new files:
  - Read `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/INDEX.md`
  - Read `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/Products/Salesforce-Agentforce.md` (pricing format reference from Phase 01)
  - Scan `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/LOOP_00001_ENTITIES.md` for any notes on major platform entities already captured
  - **Completed 2026-04-06**: Vault has 25/25 entities (100%). Companies dir has Procure-AI, Omnea, Zycus, Fairmarkit, Skyfire. No Amazon/OpenAI/Google/Stripe/Coinbase company-level profiles exist yet. LOOP_00001_ENTITIES.md confirms Amazon Alexa+/Buy for Me, OpenAI ChatGPT ACP, and Perplexity Comet are noted as Products (researched in Phase 01) — but no standalone company-level profiles for Amazon, OpenAI, Google, Stripe, or Coinbase. Profile format confirmed from Salesforce-Agentforce.md: YAML front matter → Overview → Quick Facts table → Feature sections → Pricing (tabular) → Limitations → BuyerBench Pillar Relevance → Related Entities → Sources.

- [ ] Research and profile Amazon's agentic commerce platform:
  - Web search: "Amazon Bedrock Agents pricing 2025 2026 per token"
  - Web search: "Amazon Nova agentic capabilities procurement enterprise 2025"
  - Web search: "Amazon Supply Chain AI agent capabilities pricing 2025"
  - Web search: "Amazon B2B procurement AI agent capabilities 2025 Business"
  - Create `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/Companies/Amazon-Agentic-Commerce.md` with YAML front matter (type: company, tags: [amazon, platform, ai-agents, cloud, e-commerce, pricing]) and sections: Overview, Key Products (Bedrock Agents, Nova, Supply Chain, Amazon Business), Agentic Commerce Strategy (Buy for Me, Rufus, Alexa+ as consumer layer), Pricing (Bedrock per-token rates, agent invocation costs), Strategic Moves (OpenAI partnership Feb 2026, Perplexity injunction Mar 2026), BuyerBench Pillar Relevance, wiki-links to [[Amazon-Rufus-BuyForMe]], [[ACP]]

- [ ] Research and profile OpenAI's agent platform and pricing:
  - Web search: "OpenAI Responses API Agents SDK pricing 2025 2026"
  - Web search: "OpenAI Operator agent tool use GPT-4o pricing per call"
  - Web search: "OpenAI enterprise agent deployment procurement capabilities 2026"
  - Create `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/Companies/OpenAI-Agent-Platform.md` with YAML front matter (type: company, tags: [openai, platform, ai-agents, api, operator, pricing]) and sections: Overview, Agent Products (Operator, Responses API, Agents SDK), Pricing Tiers (GPT-4o / GPT-4o mini per-token; Operator subscription if any), ACP History and Rollback (Sep 2025 → Mar 2026), Current Agentic Commerce Strategy, BuyerBench Pillar Relevance (as agent under test + as platform), wiki-links to [[ChatGPT-Operator]], [[ACP]], [[Amazon-Agentic-Commerce]]

- [ ] Research and profile Google's agentic commerce capabilities and pricing:
  - Web search: "Google Gemini 2.0 agent capabilities agentic commerce 2025 2026"
  - Web search: "Google AI Studio Vertex AI agent pricing 2025 2026"
  - Web search: "Google AP2 UCP agentic payment protocol partners 2025"
  - Web search: "Google Project Mariner agent browser shopping 2025"
  - Create `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/Companies/Google-Agentic-Commerce.md` with YAML front matter (type: company, tags: [google, platform, ai-agents, gemini, vertex-ai, pricing]) and sections: Overview, Key Products (Project Mariner, Gemini 2.0 agents, Vertex AI Agent Builder), AP2/UCP Payment Protocol, Pricing (Gemini API per-token; Vertex AI agent costs), Shopping Integration (Google Shopping agent capabilities), BuyerBench Pillar Relevance, wiki-links to [[AP2-UCP]], [[OpenAI-Agent-Platform]]

- [ ] Research and profile Stripe's agent payment infrastructure and pricing:
  - Web search: "Stripe agent payment infrastructure AI agents pricing 2025 2026"
  - Web search: "Stripe Connect fees transaction pricing 2025"
  - Web search: "Stripe ACP partnership OpenAI Radar fraud detection agent transactions"
  - Create `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/Companies/Stripe-Agent-Payments.md` with YAML front matter (type: company, tags: [stripe, payment-infrastructure, pricing, fraud-detection, pillar-3]) and sections: Overview, Agent Payment Products (ACP integration, Stripe Radar, Connect), Pricing (processing fees: 2.9%+30¢ standard; custom enterprise; per-transaction fraud tools), ACP Partnership History, Comparison to Coinbase/x402, BuyerBench Pillar 3 Relevance, wiki-links to [[ACP]], [[x402]], [[Skyfire]]

- [ ] Research and profile Coinbase's agent payment infrastructure and pricing:
  - Web search: "Coinbase x402 AI agent payments infrastructure pricing 2025 2026"
  - Web search: "Coinbase Developer Platform agent wallet pricing fees"
  - Web search: "Coinbase Base network agent micropayments USDC 2025"
  - Create `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/Companies/Coinbase-Agent-Payments.md` with YAML front matter (type: company, tags: [coinbase, crypto, payment-infrastructure, x402, micropayments, pricing]) and sections: Overview, x402 Protocol Origin, Agent Wallet Products, Base Network for Micropayments, Pricing (gas fees, USDC transaction costs), Regulatory Position, Comparison to Stripe, BuyerBench Pillar 3 Relevance, wiki-links to [[x402]], [[Stripe-Agent-Payments]], [[Skyfire]]

- [ ] Research and profile key people in the AI buyer agent space (founders, executives, researchers):
  - Web search: each of the following: founders of Procure AI, CEO of Fairmarkit, founder of Skyfire, lead author of ACES paper, NegMAS creator (Yasser Mohammad), key Visa/Mastercard agentic commerce leads
  - Web search: "who is building AI buyer agent benchmark research 2025 key researchers"
  - Create individual profile files in `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/People/` — one file per person found, each with YAML front matter (type: person, tags: [role, company/institution]) and sections: Role, Background, Key Contributions to Agentic Commerce, Public Statements / Papers, LinkedIn/X if found, wiki-links to their company/paper profiles
  - Target at least 6 people profiles; skip anyone where minimal public info is found

- [ ] Update the vault INDEX.md with all new company and people profiles:
  - Read `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/INDEX.md`
  - Add Companies section entries: Amazon-Agentic-Commerce, OpenAI-Agent-Platform, Google-Agentic-Commerce, Stripe-Agent-Payments, Coinbase-Agent-Payments
  - Add People section with all created person profiles
  - Update total entity count and coverage statistics
