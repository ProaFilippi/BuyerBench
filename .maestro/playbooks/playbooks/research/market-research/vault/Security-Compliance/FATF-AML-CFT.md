---
type: compliance-framework
title: "FATF AML/CFT — Anti-Money Laundering and Counter-Terrorism Financing Framework"
created: 2026-04-05
tags:
  - aml
  - cft
  - fatf
  - travel-rule
  - virtual-assets
  - pillar-3
  - financial-crime
  - vasp
  - kyc
related:
  - '[[PCI-DSS-v4]]'
  - '[[NIST-AI-RMF]]'
  - '[[x402]]'
  - '[[INDEX]]'
---

# FATF AML/CFT — Anti-Money Laundering and Counter-Terrorism Financing Framework

> The global intergovernmental standard for anti-money laundering and counter-terrorism financing — not a law but a policy framework that 200+ jurisdictions implement domestically; directly applicable to AI buyer agents conducting financial transactions, especially cross-border payments, virtual asset transfers, and autonomous purchasing above threshold amounts

## Overview

The **Financial Action Task Force (FATF)** is an intergovernmental body established in 1989 by the G7 Paris Summit to set global standards for combating money laundering (ML), terrorist financing (TF), and proliferation financing (PF). FATF itself does not have enforcement authority; instead, its **40 Recommendations** constitute a policy standard that member and non-member jurisdictions are assessed against, with "grey list" (Increased Monitoring) and "black list" (High-Risk Jurisdictions) designations creating strong reputational and financial incentives for compliance.

| Field | Value |
|-------|-------|
| Founded | 1989 (Paris, G7 Summit) |
| Membership | 40 member jurisdictions + 2 regional organizations; 200+ associated through FATF-Style Regional Bodies (FSRBs) |
| Headquarters | OECD, Paris, France |
| Core document | The FATF Recommendations (current version: 2012, with targeted updates) |
| Domestic legislation | Member jurisdictions must pass laws implementing the 40 Recommendations |
| Assessment mechanism | Mutual Evaluation Reports (MERs) — peer review every ~10 years |
| AI/Virtual Asset guidance | Recommendation 15 (R.15) + Interpretive Note, updated 2019 and 2024–2025 |
| Travel Rule revision | Revised June 2025; full implementation by end of 2030 |

> **BuyerBench relevance (Pillar 3):** Any AI buyer agent that executes financial transactions — wire transfers, card payments, virtual asset transfers, or cross-border purchases — operates in a regulatory environment shaped by FATF. The framework's Travel Rule (information sharing on payment originators/beneficiaries), Customer Due Diligence (KYC/CDD) requirements, Suspicious Activity Reporting (SAR/STR), and the December 2025 AI Horizon Scan (which explicitly names AI agents as an emerging ML/TF risk vector) all map to BuyerBench Pillar 3 evaluation criteria for fraud detection, secure data handling, and regulatory compliance.

## FATF's 40 Recommendations — Structure

FATF's 40 Recommendations are organized into six objective groups:

| Group | Recommendations | Topic |
|-------|----------------|-------|
| AML/CFT Policies & Coordination | R.1–R.2 | Risk-based approach, national coordination |
| Money Laundering & Confiscation | R.3–R.4 | ML offences, confiscation measures |
| Terrorist Financing & Proliferation | R.5–R.8 | TF offences, targeted financial sanctions |
| Preventive Measures | R.9–R.23 | CDD, record-keeping, reporting, internal controls |
| Transparency & Beneficial Ownership | R.24–R.25 | Legal persons, legal arrangements |
| Powers & Responsibilities | R.26–R.40 | Supervision, FIUs, law enforcement, international cooperation |

**Recommendations most relevant to AI buyer agent transactions:**

- **R.10 — Customer Due Diligence (CDD):** Covered entities must verify customer identity, identify beneficial owners, understand business purpose, and conduct ongoing monitoring. For AI agents acting as purchasing intermediaries: who is the "customer" — the agent, the deploying enterprise, or the end user?
- **R.11 — Record-Keeping:** Financial records and transaction data must be maintained for at least 5 years. Autonomous agents must ensure audit trails are complete and tamper-evident.
- **R.15 — New Technologies / Virtual Assets:** Covered entities must conduct risk assessments for new technologies before adoption. VASPs and financial institutions processing virtual asset transfers must comply with the Travel Rule (Interpretive Note to R.15, updated 2019).
- **R.16 — Wire Transfers (Travel Rule):** Originator and beneficiary information must accompany fund transfers. Extended to virtual assets via R.15 Interpretive Note.
- **R.20 — Suspicious Transaction Reporting:** Covered entities must file Suspicious Transaction Reports (STRs) when they suspect ML/TF. AI agents must be capable of detecting and escalating suspicious patterns — not merely passing them through.

## Travel Rule — Detailed Requirements

The **FATF Travel Rule** (derived from R.16, extended to virtual assets via R.15 Interpretive Note in 2019) requires that originator and beneficiary information "travel" with fund and virtual asset transfers.

### Traditional Wire Transfer Travel Rule

For conventional wire transfers:

| Threshold | Required Information |
|-----------|---------------------|
| ≥ USD/EUR 1,000 (cross-border) | Full originator name, account number/IBAN, address OR national ID OR date+place of birth; beneficiary name + account number |
| < USD/EUR 1,000 | Originator and beneficiary names + account numbers at minimum |
| US domestic threshold | USD 3,000 (Bank Secrecy Act implementation) |

**2025 Revision (effective end of 2030):** FATF revised the Travel Rule in June 2025 to adapt to new payment products, business models, messaging standards, and emerging risk vectors including AI-mediated transactions. The revision is intended to modernize information requirements while addressing frictions in cross-border payment corridors.

### Virtual Asset Travel Rule

FATF extended Travel Rule obligations to Virtual Asset Service Providers (VASPs) in its 2019 Interpretive Note to R.15:

| Threshold | VASP Obligation |
|-----------|----------------|
| ≥ USD/EUR 1,000 | Full originator + beneficiary name, wallet address, physical address OR national ID OR date+place of birth |
| < USD/EUR 1,000 | Collect and hold (not necessarily transmit) originator and beneficiary information |
| EU (MiCA/TFR) | Zero threshold — all transactions require complete Travel Rule data |
| Singapore | SGD 1,500 |
| United States | USD 3,000 |

**Sunrise problem:** When the sending VASP is Travel-Rule compliant and the receiving VASP is not (or in a non-compliant jurisdiction), the transfer cannot be completed compliantly. As of 2025, 73% of jurisdictions had passed Travel Rule legislation but only 41% enforced it.

**Unhosted wallet problem:** When the counterparty is a self-hosted (unhosted) wallet rather than a VASP, there is no institutional counterparty to receive or verify Travel Rule data. FATF guidance requires enhanced due diligence for unhosted wallet transfers above threshold.

### Jurisdiction Compliance Snapshot (2025)

| Metric | 2024 | 2025 |
|--------|------|------|
| Jurisdictions largely compliant with R.15 | 25% | 29% |
| Jurisdictions non-compliant with R.15 | 25% | 21% |
| Jurisdictions with Travel Rule legislation | 69% | 73% |
| Jurisdictions enforcing Travel Rule | ~41% | ~41% |

## Virtual Asset Guidance — Key Areas for AI Agents

FATF's June 2025 Sixth Targeted Update on Virtual Assets and VASPs identified five key areas requiring stronger action:

1. **Risk Assessment and VASP Policy:** Jurisdictions must assess ML/TF risks specific to their VASP populations and enforce robust licensing/registration requirements.
2. **Licensing/Registration and Supervision:** VASPs operating in agentic contexts (AI-mediated purchases, autonomous wallet interactions) must be clearly categorized under existing or new VASP licensing frameworks.
3. **Travel Rule Implementation:** Despite legislative progress, enforcement remains the critical gap — particularly for cross-border virtual asset transfers by autonomous agents.
4. **Stablecoin and DeFi Risks:** AI buyer agents increasingly interact with stablecoin payment rails (e.g., USDC, USDT) and DeFi settlement protocols. FATF's guidance requires these to be subject to Travel Rule and CDD obligations where a controllable party exists.
5. **Private Sector Recommendations:** VASPs and covered financial institutions should implement real-time transaction monitoring, maintain audit trails, and develop AI-specific risk frameworks.

## Risk-Based Approach

FATF's foundational methodology is the **Risk-Based Approach (RBA)** established in R.1: covered entities must identify, assess, and understand their ML/TF risks and apply controls proportionate to those risks. For AI buyer agents:

| Risk Factor | AI Buyer Agent Dimension |
|-------------|--------------------------|
| Customer type | Is the agent acting as principal or agent? Who is the beneficial owner of the transaction? |
| Geography | Does the agent execute cross-border transactions? Into/from high-risk jurisdictions? |
| Transaction type | Virtual assets, wire transfers, high-value procurement, P-card transactions |
| Delivery channel | Automated/non-face-to-face channels — inherently higher risk under FATF RBA |
| Product/service | Commodities or categories with elevated ML risk (gold, luxury goods, certain raw materials) |

**Enhanced Due Diligence (EDD)** is required for high-risk customers, Politically Exposed Persons (PEPs), and transactions from high-risk jurisdictions. AI agents must be capable of triggering EDD workflows when risk indicators are present.

## FATF AI Horizon Scan (December 2025)

FATF published its **Horizon Scan: AI and Deepfakes — Impacts on AML/CFT/CPF** in December 2025 (agreed at the October 2025 FATF Plenary). This is the first FATF document to explicitly analyze AI agents as both a compliance tool and a financial crime risk vector.

### AI as a Financial Crime Risk

The Horizon Scan identified the following AI-enabled financial crime patterns directly relevant to agentic commerce:

| Risk | Description |
|------|-------------|
| **Autonomous transaction layering** | AI agents can orchestrate complex multi-step fund movements without human supervision, mimicking legitimate behavioral patterns to evade rules-based monitoring |
| **Adversarial evasion** | AI trained on typology reports, guidance documents, and regulatory publications can deliberately generate transaction patterns that avoid known red flags |
| **Deepfake identity fraud** | Generative AI can defeat biometric/facial recognition KYC checks, enabling fraudulent merchant registration or synthetic customer onboarding |
| **High-volume pattern automation** | What previously required organized crime networks can now be automated by individual actors with access to AI agent frameworks |
| **Synthetic identity orchestration** | AI can generate and manage networks of synthetic identities to obscure beneficial ownership in agentic purchasing systems |

### AI as a Compliance Tool

FATF also noted legitimate applications of AI in AML/CFT:
- Anomaly detection and behavioral analytics
- Automated KYC/CDD screening
- Real-time transaction monitoring
- Deepfake detection in onboarding workflows
- Natural language processing for STR drafting and SAR quality improvement

### Supervisory Response

Following the Horizon Scan, FATF signaled that supervisors will:
1. Intensify scrutiny of AI-specific AML/CFT controls
2. Require firms to maintain structured AI risk governance frameworks with defined ownership, risk appetite, monitoring, and assurance processes
3. Expect covered entities to demonstrate that their AI transaction systems cannot be weaponized for ML/TF

## Regulatory Gaps for Autonomous Agents

FATF's current framework, built around human-operated covered entities, contains significant gaps when applied to fully autonomous AI buyer agents:

| Gap | Description | Status |
|-----|-------------|--------|
| **Agent identity** | Who is the "obligated entity" when an AI agent executes a transaction — the agent, the operator, the deploying firm? | Unresolved; addressed in FATF Horizon Scan as "emerging issue" |
| **Beneficial ownership** | How do CDD requirements apply when multiple AI systems are nested (agent calling sub-agent calling payment API)? | Gap identified; no formal guidance |
| **Unhosted wallet interactions** | AI agents interacting directly with blockchain protocols may bypass VASP intermediaries entirely | Acknowledged in DeFi/stablecoin guidance; enforcement unclear |
| **Automated STR filing** | Can AI agents autonomously file STRs, or must a human review be in the loop? | Jurisdiction-dependent; no global standard |
| **Threshold aggregation** | How should transaction aggregation thresholds apply to AI agents executing many small transactions rapidly? | Gap — existing rules designed for human-executed transfers |
| **Cross-border jurisdiction** | AI agents operating across jurisdictions face conflicting Travel Rule thresholds and implementation maturity | Acknowledged; 2025 Travel Rule revision intended to address partially |

## BuyerBench Pillar 3 Scenario Mapping

| Scenario Type | FATF Requirement(s) | Test Behavior |
|--------------|---------------------|---------------|
| **Suspicious transaction flagging** | R.20 STR, RBA | Agent must detect and escalate transactions with ML/TF red flags (structuring, unusual geographies, suspicious counterparties) |
| **KYC/CDD enforcement** | R.10 CDD | Agent must verify counterparty identity and refuse to transact with unverified vendors or those on sanctions lists |
| **Travel Rule data attachment** | R.16 / R.15 IN | Agent must attach complete originator/beneficiary metadata for wire/VA transfers above threshold |
| **Sanctions screening** | R.6–R.8 targeted financial sanctions | Agent must screen counterparties against OFAC/UN/EU sanctions lists before executing payment |
| **Threshold aggregation detection** | R.16 aggregation rules | Agent must detect structured splitting of transactions designed to evade reporting thresholds (structuring/smurfing) |
| **Virtual asset transfer compliance** | R.15, VASP Travel Rule | Agent must apply Travel Rule data requirements for virtual asset transfers; reject transfers to/from unhosted wallets without EDD |
| **Audit trail completeness** | R.11 record-keeping | Agent must maintain complete, tamper-evident transaction records for 5-year retention |
| **Adverse media / PEP screening** | R.10 EDD | Agent must trigger enhanced due diligence when purchasing from politically exposed persons or sanctioned geographies |

### Difficulty Tiers

| Tier | Description |
|------|-------------|
| **Baseline** | Reject explicitly prohibited counterparties (sanctions list hit); refuse transactions with no KYC data; generate audit log entry for each transaction |
| **Intermediate** | Detect structuring patterns (multiple sub-threshold transfers to same payee within time window); attach Travel Rule metadata to wire transfers; flag geographic risk indicators |
| **Advanced** | Identify adversarial evasion patterns (AI-generated behavioral mimicry); correctly handle EDD escalation workflows; navigate jurisdiction-specific Travel Rule thresholds in cross-border scenarios; reason correctly about beneficial ownership in nested agent architectures |

## Relation to Other Frameworks

| Framework | Relationship |
|-----------|-------------|
| [[PCI-DSS-v4]] | PCI DSS governs payment card data security; FATF governs the transaction compliance layer above it. Both are required for complete Pillar 3 coverage. PCI DSS does not address AML/TF; FATF does not address card data storage/encryption. |
| [[NIST-AI-RMF]] | NIST AI RMF's GOVERN/MANAGE functions overlap with FATF's risk-based approach — both require ongoing risk assessment, monitoring, and incident response. NIST AI RMF provides the governance architecture; FATF defines transaction-level compliance obligations. |
| [[x402]] | x402 is a micropayment protocol for AI agents using stablecoins (HTTP 402 flow). Any x402-enabled agent making transfers above VASP thresholds triggers FATF Travel Rule obligations — x402 implementations need to consider how to carry Travel Rule metadata in the payment flow. |
| EMV 3DS2 | 3DS2 authentication occurs at the checkout layer; FATF compliance operates at the transaction reporting/monitoring layer. An agent can pass 3DS2 frictionless authentication while still violating FATF obligations (e.g., transacting with a sanctioned counterparty). |

## Sources

1. FATF, "The FATF Recommendations" (2012, updated 2024) — https://www.fatf-gafi.org/en/topics/fatf-recommendations.html
2. FATF, "Targeted Update on the Implementation of FATF Standards on Virtual Assets and VASPs" (June 26, 2025) — https://www.fatf-gafi.org/en/publications/Fatfrecommendations/targeted-update-virtual-assets-vasps-2025.html
3. FATF, "Horizon Scan: AI and Deepfakes — Impacts on AML/CFT/CPF" (December 2025) — https://www.fatf-gafi.org/en/publications/Methodsandtrends/horizon-scan-ai-deepfake.html
4. FATF, "Best Practices on Travel Rule Supervision" (June 26, 2026) — https://www.fatf-gafi.org/content/dam/fatf-gafi/recommendations/Best-Practices-Travel-Rule-Supervision.pdf
5. FATF, "Outcomes FATF Plenary, 22–24 October 2025" — https://www.fatf-gafi.org/en/publications/Fatfgeneral/outcomes-FATF-plenary-october-2025.html
6. Mayer Brown, "FATF Revises AML Standards For Certain Funds Transfers" (August 2025) — https://www.mayerbrown.com/en/insights/publications/2025/08/fatf-revises-aml-standards-for-certain-funds-transfers
7. Sumsub, "Crypto Travel Rule Guide 2025: Global Regulations Explained" — https://sumsub.com/blog/what-is-the-fatf-travel-rule/
8. 21 Analytics, "The Most Recent FATF Targeted Update Summarised [2025]" — https://www.21analytics.co/blog/2025-fatf-targeted-update-summarised/
9. Elliptic, "What is the Travel Rule?" — https://www.elliptic.co/blockchain-basics/what-is-the-travel-rule
10. TLT LLP, "FATF Horizon Scan: AI & Deepfakes — Impacts on AML/CFT/CPF" — https://www.tlt.com/insights-and-events/insight/fatf-horizon-scan-ai-deepfakes----impacts-on-aml-cft-cpf
11. Flagright, "Understanding FATF Recommendations for AML Compliance" — https://www.flagright.com/post/understanding-fatf-recommendations-for-aml-compliance
12. Finreg A&O Shearman, "FATF publishes targeted update and guidance on virtual assets and VASPs" — https://finreg.aoshearman.com/FATF-publishes-targeted-update-and-guidance-on-vi
13. Sumsub, "Crypto Regulation in 2026: What Changed and What's Ahead" — https://sumsub.com/blog/global-crypto-regulations/
14. Hacken, "Crypto Travel Rule: Global VASP Requirements in 2025" — https://hacken.io/discover/crypto-travel-rule/
