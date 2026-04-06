# Phase 04: Brazil Market Research — Companies, Products & Players

This phase launches an entirely new research thread focused on the Brazilian market for AI buyer agents and autonomous procurement technology. Brazil represents a strategically important market: it has the largest B2B e-commerce volume in Latin America, a uniquely advanced instant payment infrastructure (Pix), an Open Finance mandate, and a growing domestic AI startup ecosystem. This phase discovers and profiles Brazilian-specific companies, B2B marketplace platforms, procurement fintechs, and ERP players — building a parallel Brazil vault alongside the global research.

## Tasks

- [x] Set up the Brazil research folder structure and initialize a Brazil INDEX:
  - Create folder `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/Brazil/`
  - Create subfolders: `Companies/`, `Products/`, `Regulatory/`, `Market-Context/`
  - Create `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/Brazil/INDEX.md` with YAML front matter (type: index, title: "Brazil AI Buyer Agent Market Index", created: 2026-04-05, tags: [brazil, market-research, index]) and sections: Overview, Entity Categories, Coverage Statistics (to be filled as phase progresses), Key Market Themes
  - **Completed 2026-04-06**: Created all 4 subfolders (Companies, Products, Regulatory, Market-Context) and INDEX.md with full front matter, 6 key market themes (Pix, Open Finance, TOTVS dominance, tax complexity, LGPD, agribusiness verticals), entity category tables, and coverage statistics scaffold.

- [x] Research Brazilian AI procurement startups and buyer agent companies:
  - Web search: "Brazil AI procurement startup agente comprador 2024 2025"
  - Web search: "inteligência artificial compras empresariais B2B Brazil startup 2025"
  - Web search: "Brazil AI agent procurement automation company funded 2024 2025"
  - Web search: "Latin America AI purchasing agent B2B platform Brazil 2025"
  - Web search: "Brazil B2B AI sourcing agent platform supplier discovery 2025"
  - For each significant company found (target 3-6), create a profile in `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/Brazil/Companies/[CompanyName].md` with YAML front matter (type: company, tags: [brazil, ai-procurement, startup]) and sections: Overview, Product, Funding, Target Market, Pricing (in BRL if available), BuyerBench Relevance
  - Create `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/Brazil/Market-Context/Brazil-AI-Procurement-Landscape.md` summarizing the discovery with wiki-links to each company found
  - **Completed 2026-04-06**: Ran all 5 web searches + targeted article fetches. Profiled 4 companies: **Freedom** (Brazilian AI agent platform, R$14.5M seed, 900% growth), **Zinit** (e-sourcing SaaS, US$8M/R$44M seed, Dubai HQ / Brazil expansion), **Linkana** (SRM platform, YC W20, Brazilian native), **Pipefy** (no-code workflow + AI agents, ~$150M raised, Curitiba). Created `Brazil-AI-Procurement-Landscape.md` with competitive matrix, stack diagram, macro market data, and BuyerBench scenario design recommendations (Pix flows, Nota Fiscal validation, CNPJ verification, TOTVS integration layer).

- [x] Research Brazilian B2B marketplaces and procurement platforms:
  - Web search: "Mercado Livre B2B empresas marketplace procurement Brazil 2025"
  - Web search: "TOTVS procurement AI automation Brazil ERP 2025"
  - Web search: "Boa Compra governo eletrônico compras empresariais Brazil"
  - Web search: "Brazil B2B e-commerce marketplace supplier discovery platform 2025 pricing"
  - Web search: "Nomos Linkana supplier management Brazil 2024 2025"
  - For each significant platform found (target 4-6), create a profile in `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/Brazil/Products/[PlatformName].md` with YAML front matter (type: product, tags: [brazil, b2b-marketplace, procurement]) and sections: Overview, Key Capabilities, Market Share (if available), Pricing in BRL, AI/Agent Features (if any), BuyerBench Scenario Relevance
  - **Completed 2026-04-06**: Ran all 5 web searches + 3 follow-up targeted searches. Profiled 5 platforms: **Mercado Livre Negócios** (B2B marketplace, Sep 2025 launch, 1.3M SKUs, up to 50% corporate discounts, CNPJ-gated, NF-e filter), **TOTVS ERP Procurement + Fluig Voyager 2.0** (~50% Brazil ERP market share, generative AI workflow builder, natural language procurement requisitions), **Compras.gov.br / PNCP** (Brazilian federal e-procurement portal, PNCP REST API for public bids, SICAF supplier registry, Law 14.133/2021), **B2Brazil** (largest Americas foreign trade B2B marketplace, 230K+ companies, free for buyers, B2B SafePay + Freight), **Nomos** (regulatory intelligence platform, 230+ regulatory events/day, LGPD/ANVISA monitoring). Created `Brazil-B2B-Marketplace-Landscape.md` with competitive matrix, stack architecture diagram, market sizing (R$ 234B e-commerce, 18.42% B2B CAGR), 6 key market themes (TOTVS dominance, Pix payment flow, NF-e compliance gate, PNCP API, SISCOMEX import complexity, compliance intelligence), and 10 BuyerBench scenario design recommendations spanning all 3 pillars.

- [x] Research Brazilian ERP systems and their AI agent capabilities:
  - Web search: "TOTVS inteligência artificial agente compras 2025 preço"
  - Web search: "SAP Brazil S4HANA procurement agent AI 2025"
  - Web search: "Senior Sistemas ERP procurement AI Brazil 2025"
  - Web search: "Sankhya ERP Brazil AI agent automation 2025"
  - Web search: "Oracle Brazil ERP procurement automation agent 2025"
  - Create `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/Brazil/Market-Context/Brazil-ERP-Landscape.md` with YAML front matter (type: market-context, tags: [brazil, erp, procurement, ai-integration]) and sections: Market Overview, Key Players (TOTVS ~50% share, SAP, Senior, Sankhya, Oracle), AI Agent Integration Status per ERP, Pricing Tiers (in BRL where available), Implications for BuyerBench Brazil Test Scenarios
  - **Completed 2026-04-06**: Ran all 5 web searches + 2 follow-up pricing searches. Created `Brazil-ERP-Landscape.md` profiling all 5 ERP players: **TOTVS** (Agente de Compras + TOTVS Copilot Agent Store, from R$1,800/mo cloud), **SAP** (Joule + Sourcing Agent 70% RFP time reduction, multi-agent Finance+Procurement+Production, BRF as key Brazil AI adopter), **Senior Sistemas** (AI-Centric ERP concept, 50+ specialized agents, 50% faster implementation), **Sankhya** (Deploy Agent reduces implementation 9–12mo → 30 days, Bia AI assistant for procurement), **Oracle** (Fusion Agentic Applications 22 agents, Quote-to-Requisition Agent, Agent Marketplace Oct 2025). Document includes: market share table, per-player AI agent feature matrix, pricing tiers in BRL, 6 structural market themes (fiscal compliance forcing function, TOTVS lock-in, domestic vendor AI race, pricing opacity, multi-agent gap, Pix+ERP), and 12 BuyerBench scenario recommendations across all 3 pillars. Updated Brazil INDEX.md with ERP entities and coverage statistics.

- [x] Research Brazilian fintech companies relevant to AI agent payments:
  - Web search: "Nubank B2B empresa conta empresarial pagamento automático agente IA 2025"
  - Web search: "Stone Cielo B2B payment AI automation agent Brazil 2025"
  - Web search: "PagSeguro PagBank empresa AI agent pagamento 2025"
  - Web search: "Celcoin Open Finance API agente pagamento Brazil 2025"
  - Web search: "Brazil fintech AI agent payment automation B2B procurement 2025"
  - For each significant fintech found (target 3-5), create a profile in `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/Brazil/Companies/[FintechName].md` with YAML front matter (type: company, tags: [brazil, fintech, payments, b2b]) and sections: Overview, Payment Products, AI/Agent Capabilities, Pricing (in BRL: transaction fees, monthly fees), Open Finance integration, Pix capabilities, BuyerBench Pillar 3 Relevance
  - **Completed 2026-04-06**: Ran all 5 web searches + 4 follow-up targeted searches/fetches. Profiled 5 fintechs: **Nubank Nu Empresas** (100M+ customers, Assistente de Pagamentos, Voice Pix Jun 2025, free PJ account), **Stone/StoneCo** (~14% acquiring market share, Conta PJ, Linx ERP integration, R$7B+ gross profit guidance 2025), **Celcoin** (ITP-licensed BaaS, R$30B+/month, 80-endpoint Open Finance API, Direct Pix Participant), **ASAAS** (R$820M Series C, free SMB REST API, PCI-DSS, SCD license, 100%+ annual growth), **Belvo** (YC W20, ITP-authorized Open Finance middleware, multi-bank data aggregation, Pix Biometria pioneer). Created `Brazil-Fintech-Payment-Landscape.md` with 3-layer stack architecture diagram, competitive matrix, 6 key market themes (Pix as universal B2B rail, ITP authorization gating, consent-before-payment model, CNPJ fraud prevention, NF-e compliance gate, SMB-first automation), and 10 BuyerBench scenario recommendations spanning Pillars 1 and 3. Updated Brazil INDEX.md with all 5 fintech entities and revised coverage statistics (19 entities profiled / ~79% coverage).

- [ ] Research global AI buyer agent platforms' Brazil presence and local pricing:
  - Web search: "Salesforce Agentforce Brazil preço Real BRL 2025"
  - Web search: "OpenAI API Brazil pricing BRL 2025 enterprise"
  - Web search: "Microsoft Copilot Brazil enterprise pricing 2025"
  - Web search: "SAP Ariba Brazil pricing BRL procurement 2025"
  - Web search: "Zycus Brazil Latin America presence 2024 2025"
  - Create `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/Brazil/Market-Context/Global-Players-Brazil-Presence.md` with YAML front matter (type: market-context, tags: [brazil, global-players, pricing-brl, market-entry]) and sections: Overview, Per-Player Coverage (local entity? pricing in BRL? Portuguese language support?), Localization Gaps, Market Opportunity Assessment, wiki-links to corresponding global profiles ([[Salesforce-Agentforce]], [[OpenAI-Agent-Platform]], etc.)

- [ ] Update Brazil INDEX.md with all discovered entities and create a market overview summary:
  - Read `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/Brazil/INDEX.md`
  - Update with all company, product, and market context files created in this phase
  - Add coverage statistics: total entities discovered, total profiled, categories covered
  - Update `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/INDEX.md` (global) to add a Brazil section pointing to the Brazil sub-vault
