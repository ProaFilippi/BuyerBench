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

- [x] Build the Global Pricing Registry:
  - Read all profiles that contain pricing information (Companies/ and Products/ folders — look for BRL, USD, per-seat, per-transaction pricing)
  - Create `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/Pricing-Registry.md` with YAML front matter (type: reference, tags: [pricing, registry, global, brazil, comparison]) and sections:
    - Global Pricing Table (columns: Entity | Model | Price | Currency | Notes | Source Date)
    - Brazil Pricing Table (same columns, BRL-denominated where available)
    - Pricing Observations (enterprise SaaS opacity, open-source free tier patterns, per-transaction models in payment protocols)
    - wiki-links to all entities listed
  <!-- Completed 2026-04-06: Read all 10 global company profiles and 5 global product profiles, plus 9 Brazil company profiles and 5 Brazil product profiles. Created Pricing-Registry.md with: (1) global model API pricing table (Amazon Nova, OpenAI GPT-5 family, Gemini 2.5 family), (2) agent runtime pricing (AgentCore vs Vertex AI Agent Engine — 9× cost gap), (3) consumer subscription tiers ($0–$249.99/month across ChatGPT/Perplexity/Google), (4) Salesforce Agentforce all 3 pricing models ($2/conv, $0.10/action, $125+/user), (5) full Stripe + Coinbase x402 per-transaction fee schedules with break-even analysis, (6) Brazil BRL table (Nubank, Stone, ASAAS, Celcoin, Belvo, TOTVS, Mercado Livre Negócios, Pipefy), (7) 6 pricing observations including Brazil cost competitiveness vs. global and $200/month consumer agent tier convergence. Wiki-links to all 37 vault entities. -->

- [x] Build the Brazil vs. Global Comparison document:
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
  <!-- Completed 2026-04-06: Read all three source documents (Brazil-AI-Procurement-Landscape, Global-Players-Brazil-Presence, Brazil-Compliance-Overview). Created Brazil-vs-Global-Analysis.md with: (1) market size comparison table (Brazil $1.4–1.65B TAM vs. global $9.5B procurement software market), (2) infrastructure contrast across three dimensions (Pix vs. card rails, TOTVS vs. SAP/Oracle, Open Finance vs. PSD2), (3) full regulatory contrast — four-plane Brazil architecture vs. two-plane global, LGPD vs. GDPR automated-decision trigger comparison, Pix vs. PCI DSS non-overlap analysis, (4) localization gap table for all 6 global players across 5 dimensions, (5) Brazil-native competitive advantage across 5 structural factors with segment-by-segment positioning matrix, (6) three-tier market entry priority framework (legal prerequisites → compliance operations → differentiation), (7) 11 recommended Brazil-specific BuyerBench scenario archetypes with framework activation mapping, (8) wiki-links to all relevant Brazil and global vault profiles. -->

- [x] Create BuyerBench Scenario Design Recommendations document:
  - Read `/home/superiora/Documents/CODE/BuyerBench/CLAUDE.md` (project context)
  - Read `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/LOOP_00001_MARKET_ANALYSIS.md`
  - Read `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/Research-Papers/ACES-AI-Agent-Buying.md`
  - Create `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/BuyerBench-Scenario-Recommendations.md` with YAML front matter (type: report, tags: [buyerbench, scenarios, recommendations, pillar-1, pillar-2, pillar-3]) and sections:
    - Pillar 1 New Scenarios Suggested (from research: Amazon Business catalog navigation, multi-supplier Brazilian marketplace sourcing, ERP-integrated procurement flows)
    - Pillar 2 New Scenarios Suggested (from ACES paper: specific bias types to implement with variant designs, AI-vs-AI negotiation scenario using NegMAS)
    - Pillar 3 New Scenarios Suggested (from protocols + compliance: Pix-based payment flow for Brazil scenarios, Open Finance consent model, x402 micropayment authorization)
    - Brazil-Specific Scenario Set (LGPD-compliant data handling, Pix payment sequencing, nota fiscal validation)
    - wiki-links to [[ACES-AI-Agent-Buying]], [[NegMAS]], [[Pix]], [[LGPD]], [[PCI-DSS-v4]]
  <!-- Completed 2026-04-06: Read CLAUDE.md, LOOP_00001_MARKET_ANALYSIS.md, ACES-AI-Agent-Buying.md, NegMAS.md, Pix.md, LGPD.md, Open-Finance-Brazil.md, PCI-DSS-v4.md, and x402.md. Created BuyerBench-Scenario-Recommendations.md with: (1) 4 Pillar 1 new scenarios (Amazon Business catalog P1-19, Brazilian B2B marketplace P1-20, TOTVS ERP-integrated P1-21, NegMAS SCML tournament P1-22), (2) 6 Pillar 2 new scenarios with ACES-calibrated bias coefficients as evaluation benchmarks (position bias RCT P2-10, endorsement badge P2-11, seller manipulation resistance P2-12, model-version drift P2-13, AI-vs-AI NegMAS negotiation P2-14, sunk cost x402 P2-15), (3) 5 Pillar 3 new scenarios (PCI DSS NHI credential lifecycle P3-07, PAN tokenization enforcement P3-08, x402 replay attack prevention P3-09, Open Finance consent scope P3-10, audit trail completeness P3-11), (4) 5 Brazil-specific scenarios (BR-01 through BR-05: Pix COBV/NF-e, LGPD Art.20, Open Finance multi-sig, nota fiscal validation, Pix Automático mandate lifecycle), (5) 20-scenario priority roadmap table with complexity ratings and quick-win identification, (6) wiki-links to all 37 vault entities plus new document. -->  

- [ ] Update the master vault INDEX.md with all synthesis documents and finalize statistics:
  - Read `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/INDEX.md`
  - Add entries for: Competitive-Landscape.md, Pricing-Registry.md, BuyerBench-Scenario-Recommendations.md
  - Add pointer to Brazil sub-vault: Brazil/INDEX.md and Brazil/Brazil-vs-Global-Analysis.md
  - Update final entity counts (global + Brazil separately)
  - Add "Research Complete — Phase 06" note with date 2026-04-05
  - Add a "Start Here" navigation guide at the top of the INDEX pointing readers to the most useful entry points: Competitive-Landscape, Pricing-Registry, Brazil-vs-Global-Analysis, BuyerBench-Scenario-Recommendations
