# Phase 06: Synthesis — Competitive Landscape & Cross-Market Analysis

This phase synthesizes all research from Phases 01–05 into high-value analytical documents: a global competitive landscape map, a Brazil vs. global comparison, an updated pricing registry, and a master entity relationship graph. These synthesis documents are the deliverables that make the research vault actionable — they answer questions like "which players compete directly?", "what does the Brazil opportunity look like vs. the global market?", and "what does it actually cost to deploy an AI buyer agent?". The vault will end this phase as a fully interconnected, queryable knowledge base.

## Tasks

- [x] Read all vault indexes and key profiles before starting synthesis:
  - Read `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/INDEX.md`
  - Read `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/Brazil/INDEX.md`
  - Read `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/Brazil/Regulatory/Brazil-Compliance-Overview.md`
  - Skim headings of all Companies/ profiles (global + Brazil) to prepare for competitive mapping
  <!-- Completed 2026-04-06: Read global INDEX (37 entities, 100% coverage), Brazil INDEX (25 entities, ~83% coverage), Brazil-Compliance-Overview (four-plane architecture: data/authorization/settlement/audit), and confirmed all Companies/ and Products/ profile files exist (10 global companies, 5 global products, 9 Brazil companies, 5 Brazil products). Ready for synthesis. -->

- [x] Build the Global Competitive Landscape document:
  - Read all profiles in `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/Companies/` and `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/Products/`
  - Create `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/Competitive-Landscape.md` with YAML front matter (type: analysis, tags: [competitive-analysis, global, market-map, synthesis]) and sections:
    - Market Map (Layer 1: Procurement Platforms; Layer 2: AI Agent Runtimes; Layer 3: Payment Infrastructure; Layer 4: Standards/Protocols)
    - Competitive Clusters (procurement orchestration cluster, agent runtime cluster, payment rail cluster)
    - Head-to-Head Comparisons (table: Player A vs. Player B — differentiator, pricing, pillar relevance)
    - Notable Competitive Events Timeline (2025–2026: ACP rollback, Perplexity injunction, Visa+Mastercard same-day launch, OpenAI-Amazon partnership)
    - White Space / Gaps Identified
    - wiki-links to every profiled company and product
  <!-- Completed 2026-04-06: Read all 10 company profiles (Procure AI, Omnea, Zycus, Fairmarkit, Skyfire, Amazon, OpenAI, Google, Stripe, Coinbase) and 5 product profiles (Amazon Rufus/BuyForMe, ChatGPT Operator, Perplexity Comet, Salesforce Agentforce, NegMAS). Created Competitive-Landscape.md with 4-layer market map, 4 competitive clusters, 12 head-to-head comparison tables, 22-event timeline (Apr 2025–Apr 2026), 8 white space gaps, and wiki-links to all 37 vault entities. -->

- [ ] Build the Global Pricing Registry:
  - Read all profiles that contain pricing information (Companies/ and Products/ folders — look for BRL, USD, per-seat, per-transaction pricing)
  - Create `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/Pricing-Registry.md` with YAML front matter (type: reference, tags: [pricing, registry, global, brazil, comparison]) and sections:
    - Global Pricing Table (columns: Entity | Model | Price | Currency | Notes | Source Date)
    - Brazil Pricing Table (same columns, BRL-denominated where available)
    - Pricing Observations (enterprise SaaS opacity, open-source free tier patterns, per-transaction models in payment protocols)
    - wiki-links to all entities listed

- [ ] Build the Brazil vs. Global Comparison document:
  - Read `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/Brazil/Market-Context/Brazil-AI-Procurement-Landscape.md`
  - Read `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/Brazil/Market-Context/Global-Players-Brazil-Presence.md`
  - Read `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/Brazil/Regulatory/Brazil-Compliance-Overview.md`
  - Create `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/Brazil/Brazil-vs-Global-Analysis.md` with YAML front matter (type: analysis, tags: [brazil, global, comparison, market-analysis, synthesis]) and sections:
    - Market Size Comparison (Brazil B2B e-commerce vs. global agentic commerce)
    - Infrastructure Contrast (Pix vs. card rails, TOTVS ERP dominance vs. SAP/Oracle global)
    - Regulatory Contrast (LGPD vs. GDPR, Pix/Open Finance vs. PCI DSS/EMV 3DS2)
    - Localization Gaps for Global Players
    - Brazil-Native Players Competitive Advantage
    - Priority Market Entry Considerations for AI Buyer Agent Vendors
    - wiki-links to key Brazil profiles and corresponding global profiles

- [ ] Create BuyerBench Scenario Design Recommendations document:
  - Read `/home/superiora/Documents/CODE/BuyerBench/CLAUDE.md` (project context)
  - Read `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/LOOP_00001_MARKET_ANALYSIS.md`
  - Read `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/Research-Papers/ACES-AI-Agent-Buying.md`
  - Create `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/BuyerBench-Scenario-Recommendations.md` with YAML front matter (type: report, tags: [buyerbench, scenarios, recommendations, pillar-1, pillar-2, pillar-3]) and sections:
    - Pillar 1 New Scenarios Suggested (from research: Amazon Business catalog navigation, multi-supplier Brazilian marketplace sourcing, ERP-integrated procurement flows)
    - Pillar 2 New Scenarios Suggested (from ACES paper: specific bias types to implement with variant designs, AI-vs-AI negotiation scenario using NegMAS)
    - Pillar 3 New Scenarios Suggested (from protocols + compliance: Pix-based payment flow for Brazil scenarios, Open Finance consent model, x402 micropayment authorization)
    - Brazil-Specific Scenario Set (LGPD-compliant data handling, Pix payment sequencing, nota fiscal validation)
    - wiki-links to [[ACES-AI-Agent-Buying]], [[NegMAS]], [[Pix]], [[LGPD]], [[PCI-DSS-v4]]

- [ ] Update the master vault INDEX.md with all synthesis documents and finalize statistics:
  - Read `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/INDEX.md`
  - Add entries for: Competitive-Landscape.md, Pricing-Registry.md, BuyerBench-Scenario-Recommendations.md
  - Add pointer to Brazil sub-vault: Brazil/INDEX.md and Brazil/Brazil-vs-Global-Analysis.md
  - Update final entity counts (global + Brazil separately)
  - Add "Research Complete — Phase 06" note with date 2026-04-05
  - Add a "Start Here" navigation guide at the top of the INDEX pointing readers to the most useful entry points: Competitive-Landscape, Pricing-Registry, Brazil-vs-Global-Analysis, BuyerBench-Scenario-Recommendations
