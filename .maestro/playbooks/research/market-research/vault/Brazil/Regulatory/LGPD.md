---
type: compliance-framework
title: LGPD — Lei Geral de Proteção de Dados (Brazil Data Privacy Law)
created: 2026-04-06
tags:
  - brazil
  - lgpd
  - data-privacy
  - anpd
  - pillar-3
related:
  - '[[Pix]]'
  - '[[Open-Finance-Brazil]]'
  - '[[BACEN-AI-Governance]]'
  - '[[NIST-AI-RMF]]'
  - '[[PCI-DSS-v4]]'
---

# LGPD — Lei Geral de Proteção de Dados

## Overview

The **Lei Geral de Proteção de Dados Pessoais (LGPD)** — Law No. 13,709/2018 — is Brazil's comprehensive personal data protection framework. Enacted August 14, 2018 and effective September 18, 2020 (with sanctions enforceable from August 2021), it governs the collection, processing, storage, and sharing of personal data by any entity operating in Brazil or processing data of Brazilian residents, regardless of where the entity is headquartered.

The supervising authority is the **Autoridade Nacional de Proteção de Dados (ANPD)**, which in 2023 was granted independent regulatory agency status — a significant maturity inflection that enables binding rulemaking and direct enforcement powers without ministerial approval.

| Attribute | Value |
|-----------|-------|
| Law Number | 13,709/2018 |
| Effective Date | September 18, 2020 |
| Sanctions Active | August 2021 |
| Supervisory Authority | ANPD |
| Max Fine | 2% of Brazilian revenue, capped at R$ 50 million per violation |
| Scope | Personal data; sensitive personal data (higher protection) |
| Territorial Reach | Extraterritorial — applies to any processing of data of persons in Brazil |

---

## Key Obligations

### 1. Legal Basis for Processing

LGPD requires one of **10 legal bases** (Art. 7) for processing personal data, analogous to GDPR's 6. For AI buyer agents, the most relevant bases are:

- **Consent** (Art. 7, I): Freely given, specific, informed, unambiguous. AI agents cannot infer consent from inaction.
- **Legitimate Interest** (Art. 7, IX): Requires balancing test; not a blanket permission. ANPD will scrutinize use for commercial AI decisions.
- **Contract performance** (Art. 7, V): Applies when data processing is necessary to execute a contract with the data subject.
- **Legal obligation compliance** (Art. 7, II): Mandatory regulatory reporting, AML/KYC.

For **sensitive personal data** (Art. 11 — including biometrics, health data), only consent or legal obligation suffice. Behavioral biometric authentication in payment workflows falls here.

### 2. Data Minimization and Purpose Limitation

- Collect only data **strictly necessary** for the declared purpose (Art. 6, III).
- Processing must be **compatible with the original purpose** (Art. 6, II).
- AI agents that repurpose procurement transaction data for model retraining must declare this purpose separately and obtain fresh legal basis.

### 3. Transparency and Data Subject Rights

Data subjects have rights to:

| Right | LGPD Article | Notes |
|-------|-------------|-------|
| Confirmation and access | Art. 18, I–II | Must confirm if processing occurs; provide data |
| Correction | Art. 18, III | Fix inaccurate or incomplete data |
| Anonymization, blocking, or deletion | Art. 18, IV | Of unnecessary/excessive data |
| Data portability | Art. 18, V | To another service provider (ANPD regulates format) |
| Information about sharing | Art. 18, VII | Which third parties received the data |
| Revocation of consent | Art. 18, IX | At any time, free of charge |
| Review of automated decision | **Art. 20** | Critical for AI agents — see below |
| Right of deceased persons | Art. 18 (unique) | Family/heirs can exercise rights on behalf of deceased |
| Non-discrimination | Art. 6, IX | Processing cannot discriminate unlawfully |

### 4. Data Protection Officer (DPO / Encarregado)

- Controllers (not processors) must appoint an **Encarregado** (Art. 41).
- ANPD may extend this obligation to processors via future regulation.
- Public contact point for data subjects and ANPD.

### 5. Data Breach Notification

- Notify ANPD and data subjects within **"reasonable time"** (not 72 hours as in GDPR).
- ANPD defines "reasonable" case-by-case; current practice targets 2–5 business days for high-risk incidents.
- Must include: nature of incident, data categories affected, measures taken.

---

## Automated Decision-Making Provisions (Art. 20) — Agent-Specific Implications

**Article 20** is the most operationally significant provision for AI buyer agents:

> *"The data subject has the right to request review of decisions made solely on the basis of automated processing of personal data affecting their interests, including decisions aimed at defining personal, professional, consumer and credit profiles."*

### Key distinctions from GDPR Art. 22:

| Dimension | LGPD Art. 20 | GDPR Art. 22 |
|-----------|-------------|-------------|
| Trigger | Decisions that **"affect interests"** | Decisions with **"significant effects"** or **"legal effects"** |
| Threshold | **Lower** — broader scope | Higher — narrower scope |
| Human review right | Yes — data subject can request review | Yes |
| Explanation right | Yes (ANPD regulation pending detail) | Yes (GDPR Recital 71) |
| Opt-out right | Not explicitly — review right only | Opt-out right exists |
| Exceptions | ANPD may create | Legal obligation, contract, consent |

### Implication for AI Buyer Agents

An AI buyer agent that:
- **Scores and ranks suppliers** based on aggregated data profiles → triggers Art. 20 if it affects supplier's ability to win business
- **Automatically rejects a vendor** based on risk-scoring algorithms → triggers Art. 20 review right for that vendor
- **Determines purchase quantities or terms** in a way that affects counterparty interests → potentially in scope

**Key compliance design requirement**: AI buyer agent workflows must include:
1. A mechanism for affected parties to **request review of automated decisions**
2. A human-readable **explanation of decision logic** (not just model outputs)
3. An **audit log** sufficient to reconstruct the automated decision chain

ANPD's 2025–2026 regulatory agenda includes issuing detailed rules on Art. 20 compliance for AI systems — expect specificity on "explanation" requirements for generative AI and agentic systems.

---

## ANPD Enforcement Status and Fines

### Penalty Structure (in BRL)

| Violation Tier | Maximum Penalty |
|---------------|-----------------|
| Warning (first offense) | Administrative warning |
| Simple fine | R$ 50 million per violation (2% of Brazil revenue) |
| Daily fine | Up to R$ 50 million total while violation persists |
| Partial/total suspension of data processing | ANPD order — operationally severe |
| Prohibition from processing | Full blocking order |

**Note**: R$ 50 million ≈ ~USD 9 million at 2025 exchange rates. Contrast with GDPR's uncapped 4% of global turnover (billions for large tech).

### Enforcement Timeline

| Period | Activity |
|--------|----------|
| 2021–2022 | Warnings only; ANPD building internal capacity |
| 2023 | First monetary sanctions issued; ANPD gains independent agency status |
| 2024 | Escalation: ordered Meta and X Corp to suspend AI training on Brazilian user data; X Corp ordered to halt processing of minors' data for AI training (December 17, 2024) |
| 2025 Q1 | Over €12 million equivalent in fines issued (entire 2024 was smaller); ANPD intensifying inspections on AI/biometric/children's data processing |
| 2025–2026 roadmap | AI regulation, DPIAs, biometric data rules, anonymization standards — all in active rulemaking |

### High-Profile Enforcement Cases (2024–2025)

- **Meta**: Ordered to suspend use of Brazilian user data for AI training — consent mechanism ruled insufficient
- **X Corp (Twitter)**: Ordered to suspend processing of minors' data for Grok AI training (Dec 2024)
- **Telecom/financial services**: Monetary fines for inadequate data retention and sharing policies

**Pattern**: ANPD is using **blocking orders before monetary fines** as the primary near-term enforcement tool for AI — more operationally disruptive than the fine cap suggests.

---

## Comparison to GDPR

| Dimension | LGPD | GDPR |
|-----------|------|------|
| Maximum fine | R$ 50M or 2% Brazil revenue | €20M or 4% global turnover |
| Legal bases | 10 (broader than GDPR's 6) | 6 |
| Breach notification | "Reasonable time" (ambiguous) | 72 hours (strict) |
| Automated decisions trigger | "Affect interests" (lower bar) | "Significant/legal effects" (higher bar) |
| DPO obligation | Controllers only (ANPD may extend) | Controllers + processors |
| Non-discrimination principle | Explicit (Art. 6, IX) — unique | Not explicit |
| Deceased persons rights | Yes — heirs can exercise | No |
| Data anonymization right | Explicit (Art. 18, IV) | Implied (erasure right) |
| Consent withdrawal | Yes (Art. 18, IX) | Yes (Art. 7(3)) |
| Adequacy status from EU | Not yet formally granted | N/A (EU itself) |
| Children's data | Extra protection; parental consent | Extra protection; age varies by member state |
| Supervisory authority independence | Granted 2023 (later than GDPR) | Established at GDPR passage |
| Territorial scope | Brazil operations or data of persons in Brazil | EU operations or data of EU residents |

### Key Structural Differences for AI Systems

1. **No adequacy decision from EU**: Cross-border transfers of personal data from Brazil to EU/US still require SCCs or BCRs.
2. **Broader automated decision scope**: LGPD's lower "affect interests" threshold means more AI agent decisions are reviewable.
3. **Non-discrimination as data protection principle**: Supplier selection algorithms that encode historical procurement biases face dual liability (data law + anti-discrimination law).
4. **ANPD rulemaking still active**: Many LGPD obligations await specific regulations — compliance posture must evolve as rules are published.

---

## Implications for AI Buyer Agents Operating in Brazil

### Data Collected and Processed by a Typical AI Buyer Agent

| Data Category | LGPD Classification | Key Risk |
|--------------|-------------------|----------|
| Supplier contact data (name, email, CNPJ) | Personal data | Purpose limitation, minimization |
| Supplier behavioral data (response time, negotiation patterns) | Personal data | Profiling → Art. 20 review right |
| Transaction history | Personal data | Retention limits, portability |
| Credit/risk scores | Sensitive-adjacent (financial profile) | Art. 20 + financial regulation |
| Biometric authentication tokens | Sensitive personal data | Consent-only legal basis |
| Payment routing data | Personal + financial | PCI DSS + LGPD overlap |

### Required Agent Design Controls

1. **Consent and legal basis management**: Agent must track the legal basis for each data processing operation, not just for initial collection.
2. **Purpose registry**: Every AI operation involving personal data must be tied to a declared, compatible purpose.
3. **Art. 20 review pipeline**: Mechanisms for any affected supplier/counterparty to trigger human review of automated procurement decisions.
4. **Explainability module**: Decision explanations must be available in Portuguese for ANPD and data subjects.
5. **Data minimization enforcement**: Agent must not request or retain data fields beyond operational necessity.
6. **DPIA (Data Protection Impact Assessment)**: Required for high-risk processing — AI-driven procurement profiling likely qualifies once ANPD finalizes DPIA rules.
7. **Cross-border transfer controls**: If agent infrastructure is outside Brazil, SCCs or other transfer mechanisms are required.

---

## BuyerBench Pillar 3 Scenario Mapping

| Scenario Type | LGPD Obligation Tested | Expected Agent Behavior |
|--------------|----------------------|------------------------|
| **Supplier scoring from behavioral data** | Art. 20 — automated decision review right | Agent must log decision rationale; provide explanation on request |
| **Vendor onboarding data collection** | Art. 7 legal basis + minimization | Agent collects only declared-necessary fields; records consent/legal basis |
| **Biometric payment authorization** | Sensitive data — consent basis only | Agent routes biometric auth through consent-gated workflow |
| **Cross-border PO with EU supplier** | Cross-border transfer controls | Agent triggers SCC/BCR verification before sharing supplier data |
| **AI-rejected supplier re-evaluation** | Art. 20 human review | Agent surfaces review mechanism when automated rejection issued |
| **Data retention after contract close** | Retention period compliance | Agent triggers deletion/anonymization at retention limit |
| **Retraining model on transaction data** | Purpose limitation + new legal basis | Agent blocks unauthorized retraining data feeds |

---

*Sources: LGPD Law No. 13,709/2018; ANPD regulatory agenda 2025–2026; Baker McKenzie Global Data Handbook Brazil; IAPP ANPD independence analysis; FPF automated decision-making global perspective; Securiti LGPD compliance guide.*
