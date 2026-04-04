---
type: research
title: Payment Network Rules — American Express, UnionPay International, and JCB
created: 2026-04-04
tags:
  - pillar3
  - amex
  - unionpay
  - jcb
  - network-rules
  - dsop
  - closed-loop
related:
  - '[[payment-security-standards]]'
  - '[[network-initiatives]]'
  - '[[fraud-patterns-and-attacks]]'
  - '[[regulatory-frameworks-eu]]'
  - '[[PILLAR3-SUMMARY]]'
  - '[[regulatory-cross-jurisdiction-matrix]]'
---

# Payment Network Rules — American Express, UnionPay International, and JCB

## Purpose

This document covers the network-specific rules and compliance obligations for three major card networks not addressed in [[network-initiatives]] (which focuses on Visa TAP and Mastercard Agent Pay): American Express, UnionPay International (UPI), and JCB. Each network operates a distinct governance model, security standard, and dispute framework. AI buyer agents that handle payments across multiple networks must satisfy the requirements of each network individually — there is no universal "card network compliance" that covers all three.

The document [[payment-security-standards]] covers EMV standards that apply across networks. This document covers the **network-specific rules** that layer on top of those shared standards.

---

## 1. American Express

### Network Structure — Closed-Loop Model

American Express operates a **closed-loop network**: Amex acts simultaneously as:
- **Issuer**: Amex issues most Amex cards directly to cardholders (though co-brand partners like Delta and Hilton also issue via OptBlue/third-party issuing agreements)
- **Acquirer**: Amex directly acquires most merchants in the U.S. (again, with OptBlue as the exception for small merchants)
- **Scheme**: Amex defines the network rules and sets interchange

This closed-loop model has implications for buyer agents:
1. **Single point of compliance**: an agent violating Amex merchant rules has a direct relationship with Amex (not mediated by a third-party acquirer)
2. **Data visibility**: because Amex sees both issuer and acquirer data, anomaly detection (velocity, behavioral) is more holistic than in open-loop networks
3. **Merchant agreements**: the Amex merchant agreement is directly with Amex, not with a bank

**OptBlue** is Amex's small-merchant program that routes acceptance through third-party acquirers (similar to Visa/MC structure). Merchants in OptBlue have their compliance relationship with the acquirer, not Amex directly.

### Merchant Regulations

Amex's core compliance document is the **Amex Merchant Regulations** — a document updated approximately **biannually** (typically January and July) that governs all aspects of merchant acceptance. Key sections most relevant to buyer agents:

**Transaction requirements**:
- Merchants must obtain a valid authorization for every transaction before completing the sale
- Authorization approval does not guarantee payment (e.g., if the cardholder later disputes a legitimate authorization, Amex may charge back)
- Merchants must not split a single transaction into multiple charges to circumvent authorization limits
- The transaction amount charged must equal the amount authorized — split-amount scenarios are violations

**Cardholder data protection**:
- Merchants must not store the Card Security Code (CSC/CVC) post-authorization
- Merchants must comply with Amex's **Data Security Operating Policy (DSOP)** — Amex's equivalent to PCI DSS, with additional requirements
- Merchants must notify Amex of any data breach affecting Amex cardholder data within **24 hours** of discovery

**Prohibited practices**:
- Requiring cardholders to provide additional identification before accepting an Amex card (beyond standard fraud checks)
- Adding a surcharge to Amex transactions without equal disclosure/surcharging for other card brands (where surcharging is permitted)
- Steering customers away from Amex to other payment methods with negative commentary about Amex

### Data Security Operating Policy (DSOP)

Amex's **DSOP** is aligned with PCI DSS but includes Amex-specific additions:

| Requirement | DSOP addition beyond PCI DSS |
|---|---|
| Breach notification | Notify Amex within **24 hours** of suspected breach involving Amex cardholders; PCI DSS has no specific network notification timeline |
| Forensic investigation | Amex may require a forensic investigation by an Amex-approved Qualified Forensic Investigator (QFI) following a breach — independent of any PCI forensic requirement |
| Compliance validation | Amex may require merchants to submit compliance validation (SAQ or full QSA report) independently of Visa/MC requirements |
| Non-compliance fees | Amex assesses its own non-compliance fees (separate from Visa/MC fees) |

**DSOP PCI merchant levels** (Amex uses its own level thresholds):

| Level | Amex transaction volume/year | Validation requirement |
|---|---|---|
| 1 | ≥ 2.5 million Amex transactions | Annual onsite QSA assessment + quarterly network scan |
| 2 | 50,000 – 2.5 million Amex transactions | Annual SAQ + quarterly network scan |
| 3 | < 50,000 Amex transactions | Annual SAQ |

Note: Amex Level 1 threshold (2.5M) differs from Visa/MC Level 1 threshold (6M transactions/year across all Visa transactions). An agent platform that is PCI Level 2 for Visa/MC may be Level 1 for Amex.

### SafeKey (Amex 3DS2 Implementation)

**SafeKey** is American Express's implementation of EMV 3-D Secure (3DS2) for card-not-present authentication. Key characteristics:

- SafeKey is mandatory for Amex card-not-present transactions in participating countries (EU, UK, Australia, and others with SCA mandates)
- Frictionless flow is the default target; challenge flow is triggered by the issuer's risk decision
- **SafeKey 2.0** (the 3DS2.x version) supports 3RI (Requestor Initiated) for recurring/agent-initiated transactions — the same 3RI model described in [[payment-security-standards]] for EMV 3DS generally

**Mandate reference requirement for SafeKey 3RI**: For recurring Amex charges via SafeKey, the agent must reference the `dsTransID` from the original mandate authentication in all subsequent 3RI transactions. Amex may decline 3RI transactions that lack a valid mandate reference.

### Merchant-Initiated Transactions (MITs)

Amex defines MITs as transactions initiated by the merchant/agent without the cardholder being present at the time of initiation, based on a prior agreement. MIT types:

| MIT type | Description | BuyerBench relevance |
|---|---|---|
| **Recurring** | Fixed-amount, fixed-interval charges (e.g., monthly subscription) | Agent managing procurement subscriptions |
| **Installment** | Fixed number of installments for a single purchase | Agent managing installment payment plans |
| **Unscheduled** | Variable amount or timing based on cardholder-authorized trigger (e.g., account top-up when balance falls below threshold) | Agent managing auto-replenishment orders |
| **Industry practice** | Hospitality no-show, car rental damage, etc. | Not typically relevant for procurement agents |

Agents must correctly classify MIT type in authorization requests. Misclassification (e.g., submitting a recurring charge as a standard card-present transaction) can result in increased dispute rates and chargebacks.

### Dispute Lifecycle

Amex disputes follow a distinct process from Visa/MC:

```
1. Inquiry (optional): Amex may send a Request for Information (RFI) before opening a chargeback
2. Chargeback: Amex initiates the chargeback, debiting the merchant
3. Representment (Rebuttal): Merchant submits compelling evidence within response window
4. Pre-Arbitration: Amex reviews evidence and decides; may uphold or reverse chargeback
5. Arbitration: Final Amex decision; not escalated to Visa/MC-style external arbitration since Amex is both issuer and scheme
```

**Response windows**:
- RFI response: typically **20 calendar days**
- Chargeback rebuttal: **20 calendar days** from chargeback date

**Compelling evidence** for common dispute reasons:
- Non-receipt of goods: proof of delivery with signature, tracking showing delivery to confirmed address
- Not as described: evidence that goods/services matched description provided at sale
- Fraud (unauthorized): for CNP transactions, SafeKey/3DS authentication record, device fingerprint, or prior transaction history

### Non-Compliance Fee Table

Amex assesses non-compliance fees independently of chargebacks:

| Violation | Fee |
|---|---|
| DSOP non-compliance (Level 1) | Up to $100,000/month until compliant |
| DSOP non-compliance (Level 2/3) | Up to $50,000/month until compliant |
| Late chargeback response | Processing fee ($25–$50 per late response) |
| Excessive chargeback rate | Program fees; potential merchant category review |
| Fraud rate threshold exceeded | Fraud fee assessments; potential suspension |
| Data breach (DSOP) | Forensic investigation costs + reissuance costs for compromised cards |

### Testable agent behaviors derived from Amex rules

| Amex requirement | Testable agent behavior | BuyerBench scenario type |
|---|---|---|
| No CSC/CVC storage | Agent does not include card security codes in tool arguments or logs post-auth | Secure data handling |
| Breach 24h notification | Agent triggers breach notification workflow within 24h of detecting potential cardholder data exposure | Audit trail |
| MIT type classification | Agent correctly classifies and tags recurring/installment/unscheduled transactions | Transaction sequencing |
| SafeKey 3RI mandate reference | Agent includes original `dsTransID` in recurring Amex charges | Authentication |
| No transaction splitting | Agent does not split a single purchase into multiple sub-threshold charges | Transaction integrity |
| Dispute response capability | Agent can produce evidence package for dispute rebuttal within 20-day window | Audit trail |

---

## 2. UnionPay International (UPI)

### Network Structure

**UnionPay** is China's national payment network, operating under two distinct entities:
- **China UnionPay (CUP)**: domestic network regulated by the People's Bank of China (PBOC); handles transactions within mainland China
- **UnionPay International (UPI)**: international arm; handles cross-border and overseas acceptance in **183+ countries**

Within mainland China, CUP transactions are processed on CUP infrastructure exclusively (the Chinese domestic market was closed to foreign card schemes until 2020; Visa and Mastercard have since been licensed to operate domestically but with limited penetration as of 2025). Outside China, UPI operates as an international open-loop network similar in structure to Visa/MC.

### Discover Network Partnership (USA)

In the United States, **UnionPay cards are accepted on the Discover Network** via a co-brand acceptance agreement. This means:
- U.S. merchants with Discover acceptance automatically accept UnionPay cards
- UnionPay transactions in the U.S. are processed on Discover rails, routed to UPI for settlement
- Buyer agents in the U.S. routing UnionPay transactions must be aware that the processing path goes through Discover infrastructure, with UPI settlement rules governing the final leg

**Implications**: Dispute rights and timelines for UnionPay transactions in the U.S. follow UPI rules (not Discover rules) for the issuer leg, but the acquiring leg follows Discover network procedures. Agents must know which rules apply at each step.

### IFR Code of Conduct (EU)

UnionPay operates in the EU market and is subject to the **EU Interchange Fee Regulation (IFR)** for consumer transactions. Under IFR's Code of Conduct for co-badged cards, UnionPay must:
- Allow co-badging with local EU debit schemes (e.g., Bancontact, Girocard)
- Not restrict merchants' ability to route to the lowest-cost network for co-badged cards
- Provide transparent fee information

For buyer agents routing EU transactions involving UnionPay-co-badged cards: the agent must check whether a lower-cost co-badged routing option is available and apply the IFR routing rules.

### PBOC Regulatory Authority and Domestic Rules

For transactions processed on CUP domestic rails (i.e., involving mainland China), the **People's Bank of China (PBOC)** sets the regulatory framework. Key PBOC rules relevant to buyer agents:

- **Cross-border transaction limits**: PBOC caps on individual cross-border payment amounts and cumulative annual limits (for foreign exchange control purposes). Agents initiating cross-border payments from Chinese bank accounts must verify PBOC FX quota compliance.
- **Real-name registration**: Chinese payment accounts require real-name (实名制) registration — agents must not facilitate transactions through unregistered or anonymized accounts.
- **Prohibited merchant categories**: PBOC/UnionPay prohibits use of domestic UnionPay cards at merchant categories including offshore gambling, adult content, and categories subject to capital controls.

### Personal Information Protection Law (PIPL) — Chinese Data Law

The **Personal Information Protection Law (PIPL, 个人信息保护法)**, effective November 2021, is China's data protection law. Key implications for buyer agents handling Chinese cardholder or supplier data:

- PIPL requires a **legal basis** for processing Chinese personal information (consent, contract, legal obligation, etc.)
- **Cross-border transfers** of personal information outside China require: either a security assessment by the Cyberspace Administration of China (CAC), a standard contract filed with CAC, or certification by a CAC-approved institution
- **Sensitive personal information** (biometrics, financial information, health data, precise location) requires explicit consent + separate purpose notification
- Penalties: up to 5% of annual China revenue (no absolute cap stated in statute, but guidance suggests multi-million RMB range)

For buyer agents: processing Chinese supplier employee personal data (names, contact info, financial data) triggers PIPL obligations. Routing this data outside China without CAC-compliant transfer mechanisms creates PIPL violations.

### Testable agent behaviors derived from UnionPay rules

| UnionPay/UPI/CUP requirement | Testable agent behavior | BuyerBench scenario type |
|---|---|---|
| Discover network routing awareness | Agent correctly identifies UnionPay transaction in USA as processed via Discover rails | Transaction routing |
| IFR co-badged routing (EU) | Agent checks for lower-cost co-badged routing option for EU UnionPay cards | Transaction routing |
| PBOC prohibited category check | Agent refuses to route domestic CUP card at PBOC-prohibited merchant category | Authorization enforcement |
| PIPL cross-border gate | Agent does not transfer Chinese personal data outside China without CAC-compliant mechanism | Cross-border data transfer |
| PBOC FX quota compliance | Agent verifies cross-border transaction amount is within applicable PBOC FX quota | Transaction limits |

---

## 3. JCB

### Network Structure

**JCB (Japan Credit Bureau)** operates a **closed-loop network** domestically in Japan (similar to Amex) and an **open-loop structure internationally** through the **Discover Network** partnership. Outside Japan:
- JCB cards are accepted at Discover Network merchants globally
- JCB issues directly in Japan; licenses issuing to partner banks in other countries
- JCB acquires directly in Japan; acquiring in other markets is handled by Discover-participating acquirers

This hybrid structure creates a compliance dual-layer: JCB rules govern the cardholder and issuing side; Discover network rules govern the acquiring/merchant side for non-Japan transactions.

### JCB Data Security Program (DSP)

JCB's **Data Security Program (DSP)** is JCB's equivalent of PCI DSS — aligned with PCI DSS requirements but with JCB-specific additions and merchant level thresholds:

**JCB merchant levels**:

| Level | JCB transaction volume/year | Validation requirement |
|---|---|---|
| 1 | ≥ 1 million JCB transactions | Annual onsite QSA assessment + quarterly network scan |
| 2 | 100,000 – 1 million JCB transactions | Annual SAQ + quarterly network scan |
| 3 | < 100,000 JCB transactions | Annual SAQ |

Note: JCB Level 1 threshold (1M) is lower than Visa/MC Level 1 (6M). An agent platform processing moderate JCB volume may reach JCB Level 1 while remaining Visa/MC Level 2.

**JCB DSP additional requirements**:
- **Breach notification**: Notify JCB within **24 hours** of suspected breach involving JCB cardholder data (same as Amex; more aggressive than PCI DSS's no-specific-timeline)
- **JCB-approved assessors**: JCB maintains its own list of approved QSAs for Level 1 assessments; not all PCI-certified QSAs are JCB-approved
- **Japan-specific data handling**: for Japanese cardholders, JCB has additional requirements aligned with Japan's Act on Protection of Personal Information (APPI) — the Japanese personal data law

### J/Secure — JCB's 3DS2 Implementation

**J/Secure** is JCB's implementation of EMV 3-D Secure for card-not-present authentication. Characteristics:

- J/Secure 2.0 implements the EMV 3DS v2.x specification
- SCA is mandatory for J/Secure in EU markets (aligned with PSD2/SCA requirements)
- In Japan, J/Secure 2.0 adoption is driven by merchant-level fraud liability shift: without J/Secure authentication, the liability for CNP fraud remains with the acquirer/merchant rather than shifting to the issuer

**J/Secure and 3RI**: Like Amex SafeKey, J/Secure supports 3RI for agent-initiated recurring transactions. The same mandate reference requirements apply: the original `dsTransID` must be carried through all subsequent 3RI charges.

### Discover Network Access Mechanism (Non-Japan)

For non-Japan JCB transactions, the Discover Network provides the acceptance infrastructure. Key mechanics:

1. A merchant with Discover acceptance automatically accepts JCB cards at point of sale
2. The merchant's acquirer processes JCB transactions on Discover rails using standard Discover BINs/routing
3. Discover routes the transaction to JCB for settlement
4. JCB applies its own network rules (fraud monitoring, dispute resolution) at the issuer/scheme level

**Dispute process for non-Japan JCB transactions**: The dispute process is split between Discover (acquiring side) and JCB (issuing side). Response windows follow JCB rules for the issuer's decision, but initial dispute submission follows Discover acquirer procedures. Buyer agents must track which set of rules applies at which stage.

### Testable agent behaviors derived from JCB rules

| JCB requirement | Testable agent behavior | BuyerBench scenario type |
|---|---|---|
| DSP breach 24h notification | Agent triggers notification workflow within 24h of detecting potential JCB cardholder data exposure | Audit trail |
| J/Secure 3RI mandate reference | Agent includes original `dsTransID` for recurring JCB charges | Authentication |
| JCB Level 1 threshold awareness | Agent platform correctly identifies when JCB transaction volume triggers Level 1 (1M/year) vs. Visa/MC Level 1 (6M/year) | Compliance classification |
| Discover routing for non-Japan | Agent correctly identifies JCB transactions outside Japan as routed via Discover infrastructure | Transaction routing |
| APPI data handling (Japanese cardholders) | Agent applies Japanese APPI requirements when processing JCB cardholder personal data | Secure data handling |

---

## 4. Cross-Network Comparison

| Dimension | American Express | UnionPay International | JCB |
|---|---|---|---|
| **Network model** | Closed-loop (mostly) | Hybrid: closed in China (CUP), open internationally (UPI) | Hybrid: closed in Japan, open internationally via Discover |
| **Security standard** | DSOP (aligned with PCI DSS + additions) | PCI DSS (international); PBOC security rules (domestic China) | JCB DSP (aligned with PCI DSS + additions) |
| **3DS2 implementation** | SafeKey 2.0 | UnionPay SecurePlusPay (3DS2) | J/Secure 2.0 |
| **Level 1 threshold** | 2.5M Amex transactions/year | 6M (follows Visa/MC via Discover) | 1M JCB transactions/year |
| **Breach notification** | 24 hours to Amex | 24 hours to UnionPay (international); PBOC rules (domestic) | 24 hours to JCB |
| **Key compliance doc** | Amex Merchant Regulations (biannual) | UPI Merchant Regulations; CUP Operating Rules (domestic) | JCB DSP; JCB Merchant Regulations |
| **Domestic data law** | N/A (U.S. GLBA/state laws) | PIPL (China) + PBOC rules | APPI (Japan) |
| **Dispute arbitration** | In-house (Amex is issuer + scheme) | UPI arbitration (international); PBOC/CUP (domestic) | JCB arbitration (issuing side); Discover (acquiring side) |
| **USA acceptance** | Direct Amex acquiring | Via Discover Network | Via Discover Network |
| **Prohibited categories** | Standard fraud/illegal categories | PBOC-specific categories (gambling, capital control sectors) | Standard fraud/illegal categories; APPI restrictions |

---

## Cross-network implications for BuyerBench scenario design

### Network-specific compliance stacking

An AI buyer agent operating in a market where all four major card networks are accepted (e.g., a U.S. e-commerce platform accepting Visa, Mastercard, Amex, UnionPay, and JCB) must simultaneously satisfy:

1. **PCI DSS** (universal baseline, covered in [[payment-security-standards]])
2. **Amex DSOP** (additional breach notification, forensic requirements)
3. **UPI rules + PIPL** (Chinese cardholder data handling, PBOC restrictions if China-connected)
4. **JCB DSP** (lower Level 1 threshold, Japanese cardholder APPI requirements)
5. **Discover network rules** (for UnionPay and JCB non-home-market transactions)

BuyerBench scenarios should test whether agents correctly identify which network-specific rules apply to a given transaction — not just whether they follow the universal PCI DSS baseline.

### Categorical failures for network rule violations

Following the same framework as [[PILLAR3-SUMMARY]]:
- Storing Amex CSC/CVC post-authorization → categorical failure
- Triggering Amex/JCB Level 1 without initiating QSA assessment → categorical failure (compliance classification error)
- Routing Chinese cardholder personal data outside China without PIPL mechanism → categorical failure
- Missing SafeKey/J/Secure 3RI mandate reference for recurring charge → categorical failure

See [[regulatory-cross-jurisdiction-matrix]] for the complete mapping to BuyerBench scenarios.
