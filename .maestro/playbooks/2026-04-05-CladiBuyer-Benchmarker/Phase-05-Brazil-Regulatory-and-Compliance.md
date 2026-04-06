# Phase 05: Brazil Regulatory Context — LGPD, Pix, Open Finance & BACEN

This phase documents the Brazilian regulatory and compliance environment that any AI buyer agent operating in Brazil must navigate. Brazil has a distinctive stack: LGPD (data privacy, analogous to GDPR but with local nuances), Pix (instant payment rail operated by BACEN with unique API semantics), Open Finance (Open Banking expanded to all financial products, mandatory for large institutions), and BACEN's evolving AI governance posture. These frameworks directly inform BuyerBench Pillar 3 scenarios designed for Brazilian deployments and create a meaningful contrast with the global compliance layer (PCI DSS, EMV 3DS2) already profiled in Phase 02.

## Tasks

- [x] Read existing compliance profiles from Phase 02 before writing Brazil regulatory profiles:
  - Read `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/Security-Compliance/PCI-DSS-v4.md`
  - Read `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/Brazil/INDEX.md`
  - *Completed 2026-04-06: PCI DSS v4.0 profile ingested (NHI reqs, tokenization architecture, BuyerBench scenario hooks). Brazil INDEX read — vault has 25 entities across companies/products/ERP/fintechs; Regulatory section reserved for Phase 05.*

- [x] Research and profile LGPD (Lei Geral de Proteção de Dados):
  - Web search: "LGPD Lei Geral Proteção Dados requirements AI agents autonomous systems 2025"
  - Web search: "LGPD ANPD enforcement penalties AI automated decision making 2024 2025"
  - Web search: "LGPD vs GDPR key differences Brazil data protection agent systems"
  - Create `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/Brazil/Regulatory/LGPD.md` with YAML front matter (type: compliance-framework, tags: [brazil, lgpd, data-privacy, anpd, pillar-3]) and sections: Overview, Key Obligations (consent, data minimization, transparency), Automated Decision-Making Provisions (Art. 20 — agent-specific implications), ANPD Enforcement Status and Fines (in BRL), Comparison to GDPR, Implications for AI Buyer Agents Operating in Brazil, BuyerBench Pillar 3 Scenario Mapping, wiki-links to [[Pix]], [[Open-Finance-Brazil]], [[NIST-AI-RMF]]
  - *Completed 2026-04-06: Full LGPD profile created — 10 legal bases, Art. 20 automated decision analysis (lower threshold than GDPR), ANPD enforcement escalation (blocking orders > fines in 2024-2025), non-discrimination principle unique to LGPD, 7 Pillar 3 scenario mappings, LGPD vs GDPR comparison table.*

- [x] Research and profile Pix (BACEN instant payment rail):
  - Web search: "Pix BACEN API specification 2025 B2B enterprise payments"
  - Web search: "Pix automatic Pix Agendado programmatic payment AI agent 2025"
  - Web search: "Pix Cobrança API QR code payment B2B procurement Brazil"
  - Web search: "Pix fraud prevention BACEN limits rules 2025 agent transactions"
  - Create `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/Brazil/Regulatory/Pix.md` with YAML front matter (type: payment-infrastructure, tags: [brazil, pix, bacen, instant-payment, b2b, pillar-3]) and sections: Overview, Pix Architecture (keys, QR codes, API flows), B2B Capabilities (Pix Cobrança, Pix Automatic, scheduled Pix), Transaction Limits (per-person, B2B, nighttime), Fraud Prevention Rules (BACEN regulations), AI Agent Compatibility (programmatic Pix initiation), BuyerBench Pillar 3 Scenario Design Implications, wiki-links to [[Open-Finance-Brazil]], [[LGPD]], [[Stripe-Agent-Payments]] (global comparison)
  - *Completed 2026-04-06: Full Pix profile created — DICT key architecture, COB vs COBV B2B invoice distinction, Pix Automático (Jun 2025 launch) for recurring contracts, Pix Agendado for milestone payments, BCB Resolution 506 fraud rules (MED registry, device limits, R$200 new-device cap), mTLS+OAuth2.0 auth requirements, 8 Pillar 3 scenario mappings, comparison table vs Stripe/ACH/SEPA.*

- [x] Research and profile Open Finance Brazil (Open Banking expanded):
  - Web search: "Open Finance Brazil Phase 4 2024 2025 API agent payments"
  - Web search: "Open Finance BACEN mandatory institutions data sharing AI agent 2025"
  - Web search: "Open Finance Brazil payment initiation API Pix integration 2025"
  - Create `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/Brazil/Regulatory/Open-Finance-Brazil.md` with YAML front matter (type: compliance-framework, tags: [brazil, open-finance, open-banking, bacen, api, pillar-3]) and sections: Overview, Phase Timeline (Phases 1-4, current status), Mandatory Institutions, Data Sharing Scope, Payment Initiation API (how agents can trigger payments via Open Finance), Consent Model (user consent for agent-initiated transactions), AI Agent Implications, BuyerBench Pillar 3 Scenario Mapping, wiki-links to [[Pix]], [[LGPD]], [[EMV-3DS2]] (global comparison)
  - *Completed 2026-04-06: Full Open Finance Brazil profile created — all 4 phases documented (Phase 4 complete April 2024), Payment Initiation API V1-V4 flow diagram, Pix Automático (June 2025 recurring consent mechanism), Contactless Pix/Journey Without Redirection (Enrollments API + asymmetric device signing), FAPI 1.0 security profile with ICP-Brasil mTLS requirement, LGPD consent coupling analysis, 8 Pillar 3 scenario mappings (consent scope enforcement, mTLS certificate rotation, corporate multi-sig, redirectless payment security), comparison table vs EU PSD2 and US frameworks.*

- [x] Research BACEN's AI governance posture and Brazilian financial regulation for AI agents:
  - Web search: "BACEN Banco Central Brasil regulação inteligência artificial agentes autônomos 2024 2025"
  - Web search: "Brazil central bank AI agent autonomous financial transactions regulation 2025"
  - Web search: "BACEN resolução norma AI agente comprador 2024 2025"
  - Web search: "CMN BACEN financial agent regulation Brazil procurement automation compliance"
  - Create `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/Brazil/Regulatory/BACEN-AI-Governance.md` with YAML front matter (type: compliance-framework, tags: [brazil, bacen, ai-governance, financial-regulation, pillar-3]) and sections: Overview, Current Regulatory Position on AI Agents, Relevant Resolutions and Circulars, KYC/AML Requirements for Automated Transactions, Agent Identity and Authorization Requirements, Gap Analysis vs. Global Standards (FATF, NIST), BuyerBench Pillar 3 Brazil Scenario Mapping, wiki-links to [[Pix]], [[Open-Finance-Brazil]], [[LGPD]], [[FATF-AML-CFT]]
  - *Completed 2026-04-06: Full BACEN AI governance profile created — "monitor first, regulate later" posture confirmed (no AI rules before 2027); PL 2338/2023 strict liability framework (Senate-approved Dec 2024, House pending); BACEN Circular 3.978/2020 as live AML/KYC anchor; CMN 4.893 cybersecurity procurement requirements; COAF reporting thresholds (R$10K cash, R$50K Pix); FATF/NIST gap analysis (5 critical gaps identified); 7 Pillar 3 Brazil scenario mappings including AML structuring, MED reversal, sanction-list hit, and unlicensed payment initiation; compliance checklist (10 items) for immediate obligations.*

- [ ] Research Brazilian procurement regulation and nota fiscal (tax invoice) requirements for AI agents:
  - Web search: "nota fiscal eletrônica NF-e NFe AI agent automated procurement Brazil 2025"
  - Web search: "SEFAZ nota fiscal B2B procurement automation Brazil requirements"
  - Web search: "Brazil compras públicas licitação AI agent automation law 2025"
  - Web search: "Lei 14.133/2021 Nova Lei de Licitações AI procurement Brazil"
  - Create `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/Brazil/Regulatory/Brazil-Procurement-Regulation.md` with YAML front matter (type: compliance-framework, tags: [brazil, procurement-law, nota-fiscal, licitacao, compliance]) and sections: Overview, NF-e / NFS-e Requirements for Agent-Initiated Purchases, Nova Lei de Licitações (public procurement AI implications), SPED (digital tax bookkeeping) integration, Key Differences from US/EU Procurement Law, BuyerBench Scenario Implications, wiki-links to [[LGPD]], [[Open-Finance-Brazil]]

- [ ] Create a Brazil Compliance Summary cross-reference document:
  - Read all 5 regulatory profiles just created
  - Create `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/Brazil/Regulatory/Brazil-Compliance-Overview.md` with YAML front matter (type: report, tags: [brazil, compliance, summary, pillar-3, comparison]) and sections: Executive Summary, Compliance Stack for AI Buyer Agents in Brazil (table: Framework → Governing Body → Scope → Key AI Agent Implication → Enforcement Level), Comparison to Global Stack (PCI DSS vs. Pix, GDPR/NIST vs. LGPD, FATF vs. BACEN), Priority Compliance Actions for a BuyerBench Brazil Deployment, wiki-links to all 5 regulatory profiles + [[PCI-DSS-v4]], [[NIST-AI-RMF]], [[FATF-AML-CFT]]
  - Update `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/Brazil/INDEX.md` with all 6 new regulatory files
