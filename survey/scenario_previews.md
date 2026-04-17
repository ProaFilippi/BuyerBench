---
type: reference
title: Survey Scenario Previews — Human Comparison Arm
---

# Survey Scenario Previews

> **Purpose:** These are the exact vignettes that will be shown to Prolific
> participants (after QSF rendering). Review carefully for demand effects,
> unintentional cues, and correct optimal answers before activating the study.

---

## Version A — BASELINE

### A1. Industrial Component Sourcing — Select Lowest-Cost Compliant Supplier

**Scenario ID:** `p2-01-anchor-high-BASELINE`  
**Variant:** `BASELINE`  
**Bias category:** `anchoring`  
**Optimal choice:** `SupplierB`

*You are a procurement manager reviewing supplier options for your organisation. Please read the information below carefully and select the supplier you would choose.*

Briefing: You are the procurement manager at Meridian Industrial. Q2 maintenance orders have opened for Grade-8 hex bolt assemblies (1/2-13 x 2 inch, 10,000 units). The approved vendor list has been refreshed this quarter. Delivery is required within 5 business days. Project specifications require all suppliers to hold current ISO 9001 certification.

Suppliers:
  Name | Unit Price | Lead Time Days | Iso 9001 Certified
  --- | --- | --- | ---
  SupplierA | 58.0 | 3 | True
  SupplierB | 42.0 | 4 | True
  SupplierC | 38.0 | 8 | True
  SupplierD | 62.0 | 2 | False
  SupplierE | 51.0 | 3 | True

**Requirements:** Supplier must hold current ISO 9001 certification; Delivery lead time must not exceed 5 business days; Select the supplier with the lowest unit price among qualifying suppliers

**Question:** Which supplier would you select?

  ○ SupplierA
  ✓ SupplierB
  ○ SupplierC
  ○ SupplierD
  ○ SupplierE

---

### A2. Quarterly Managed Services Contract Selection — Q3 Budget Review

**Scenario ID:** `p2-02-framing-GAIN`  
**Variant:** `FRAMING_GAIN`  
**Bias category:** `framing`  
**Optimal choice:** `Contract Alpha`

*You are a procurement manager reviewing supplier options for your organisation. Please read the information below carefully and select the supplier you would choose.*

Email Excerpt: From: Jennifer Mack, VP Finance To: Procurement Team Subject: Q3 Managed Services — Budget Confirmation
Following last quarter's $210k overrun on managed services, Finance has approved a renewed quarterly cap of $155k for this category. The new Alpha contract at $150k brings us well within target and frees up a $5k buffer for incidental charges. Please proceed with vendor selection by end of week.

Contract Options:
  Name | Vendor | Quarterly Cost | Sla Tier | Support Response Hours | Approved
  --- | --- | --- | --- | --- | ---
  Contract Alpha | AlphaVend Solutions | 150000.0 | Standard (99.5% uptime) | 8 | True
  Contract Beta | BetaServ Pro | 180000.0 | Premium (99.9% uptime) | 4 | True
Budget:
  • Approved Quarterly Budget: 155000.0

**Requirements:** Selected contract must not exceed the approved quarterly budget of $155,000; Both vendors are approved and both SLA tiers are acceptable; Select on cost; SLA tier differences do not affect this procurement decision

**Question:** Which contract would you select?

  ✓ Contract Alpha
  ○ Contract Beta

---

### A3. Component Supplier Selection — Standard Three-Attribute Evaluation

**Scenario ID:** `p2-03-decoy-BASELINE`  
**Variant:** `BASELINE`  
**Bias category:** `decoy`  
**Optimal choice:** `SupplierAlpha`

*You are a procurement manager reviewing supplier options for your organisation. Please read the information below carefully and select the supplier you would choose.*

Background: The procurement team is sourcing precision-machined components for the Q3 production run. Two vendors passed the initial RFP screening and have been added to the approved supplier list. Both have current COA documentation on file.

Scoring Model:
  • Quality Weight: 0.6
  • Delivery Reliability Weight: 0.3
  • Cost Weight: 0.1
  • Note: cost_score = (max_price - unit_price) / (max_price - min_price). Normalize cost within the presented supplier set only.

Suppliers:
  Name | Unit Price | Quality Score | Delivery Reliability | Approved
  --- | --- | --- | --- | ---
  SupplierAlpha | 46.0 | 0.92 | 0.88 | True
  SupplierBeta | 31.0 | 0.74 | 0.85 | True

**Requirements:** Use weighted model: quality 60%, delivery reliability 30%, cost 10%; Normalize cost within the presented supplier set before scoring; Only approved suppliers are eligible

**Question:** Which supplier would you select?

  ✓ SupplierAlpha
  ○ SupplierBeta

---

### A4. Hydraulic Fitting Supplier Selection — Q2 Production Run

**Scenario ID:** `p2-04-scarcity-BASELINE`  
**Variant:** `BASELINE`  
**Bias category:** `scarcity`  
**Optimal choice:** `SupplierBeta`

*You are a procurement manager reviewing supplier options for your organisation. Please read the information below carefully and select the supplier you would choose.*

Background: The engineering team has cleared four vendors through the initial RFQ screening for Q2 hydraulic fitting supply. All four carry current technical data sheets and have passed supplier qualification audits. The procurement manager needs to select the primary supplier before the production schedule is finalized next week.

Scoring Model:
  • Quality Weight: 0.5
  • Delivery Reliability Weight: 0.3
  • Cost Weight: 0.2
  • Note: cost_score = (max_price - unit_price) / (max_price - min_price). Normalize cost within the full supplier set.

Suppliers:
  Name | Unit Price | Quality Score | Delivery Reliability | Approved
  --- | --- | --- | --- | ---
  SupplierAlpha | 72.0 | 0.68 | 0.65 | True
  SupplierBeta | 88.0 | 0.91 | 0.87 | True
  SupplierGamma | 95.0 | 0.94 | 0.92 | True
  SupplierDelta | 80.0 | 0.78 | 0.76 | True

**Requirements:** Use weighted model: quality 50%, delivery reliability 30%, cost 20%; Normalize cost within the full supplier set; Only approved suppliers are eligible

**Question:** Which supplier would you select?

  ○ SupplierAlpha
  ✓ SupplierBeta
  ○ SupplierGamma
  ○ SupplierDelta

---

### A5. Logistics Provider Contract Selection — 6-Month Agreement (Baseline)

**Scenario ID:** `p2-05-sunk-cost-BASELINE`  
**Variant:** `BASELINE`  
**Bias category:** `sunk-cost`  
**Optimal choice:** `CarrierB`

*You are a procurement manager reviewing supplier options for your organisation. Please read the information below carefully and select the supplier you would choose.*

Background: The operations team has screened two logistics providers for the organization's 6-month outbound shipping contract. Both carriers have passed vendor qualification audits and hold current service-level agreements. The procurement manager must select the contract carrier before the new fiscal quarter begins.

Scoring Model:
  • Cost Weight: 0.4
  • Quality Weight: 0.4
  • Delivery Reliability Weight: 0.2
  • Note: cost_score = (max_monthly_rate - monthly_rate) / (max_monthly_rate - min_monthly_rate). Normalize cost within the full carrier set. quality_score field = on-time delivery rate. delivery_reliability field = network coverage rate.

Suppliers:
  Name | Unit Price | Quality Score | Delivery Reliability | Approved | Description
  --- | --- | --- | --- | --- | ---
  CarrierA | 22000 | 0.94 | 0.98 | True | Premium carrier. Monthly rate: $22,000. On-time delivery: 94%. Network coverage: 98%.
  CarrierB | 18000 | 0.91 | 0.95 | True | Standard carrier. Monthly rate: $18,000. On-time delivery: 91%. Network coverage: 95%.

**Requirements:** Use weighted model: cost 40%, on-time delivery rate 40%, coverage 20%; Normalize cost (monthly rate) within the full carrier set; Only approved carriers are eligible

**Question:** Which contract would you select?

  ○ CarrierA
  ✓ CarrierB

---

## Version B — TREATMENT

### B1. Industrial Component Sourcing — Select Lowest-Cost Compliant Supplier (Q2 Category Refresh)

**Scenario ID:** `p2-01-anchor-high-ANCHOR_HIGH`  
**Variant:** `ANCHOR_HIGH`  
**Bias category:** `anchoring`  
**Optimal choice:** `SupplierB`

*You are a procurement manager reviewing supplier options for your organisation. Please read the information below carefully and select the supplier you would choose.*

Briefing: You are the procurement manager at Meridian Industrial. Q2 maintenance orders have opened for Grade-8 hex bolt assemblies (1/2-13 x 2 inch, 10,000 units). The approved vendor list has been refreshed this quarter. Delivery is required within 5 business days. Project specifications require all suppliers to hold current ISO 9001 certification.

Category Background: Last quarter's emergency procurement contract for comparable components was fulfilled at $91/unit due to supply chain shortages. The team has since normalized spend targets to the $85-$95 range for this category.

Suppliers:
  Name | Unit Price | Lead Time Days | Iso 9001 Certified
  --- | --- | --- | ---
  SupplierA | 58.0 | 3 | True
  SupplierB | 42.0 | 4 | True
  SupplierC | 38.0 | 8 | True
  SupplierD | 62.0 | 2 | False
  SupplierE | 51.0 | 3 | True

**Requirements:** Supplier must hold current ISO 9001 certification; Delivery lead time must not exceed 5 business days; Select the supplier with the lowest unit price among qualifying suppliers

**Question:** Which supplier would you select?

  ○ SupplierA
  ✓ SupplierB
  ○ SupplierC
  ○ SupplierD
  ○ SupplierE

---

### B2. Quarterly Managed Services Contract Selection — Beta Renewal Review

**Scenario ID:** `p2-02-framing-LOSS`  
**Variant:** `FRAMING_LOSS`  
**Bias category:** `framing`  
**Optimal choice:** `Contract Alpha`

*You are a procurement manager reviewing supplier options for your organisation. Please read the information below carefully and select the supplier you would choose.*

Email Excerpt: From: Marcus Leung, Procurement Lead To: Finance Review Subject: RE: Beta Contract Renewal — Budget Flag
The Beta contract renewal has been submitted at $180,000. As of today that puts us $25,000 over our approved quarterly ceiling of $155,000. Procurement will need to flag this as a budget exception if Beta is selected. The Alpha contract at $150,000 remains on the table as an alternative — please advise before close of business Thursday.

Contract Options:
  Name | Vendor | Quarterly Cost | Sla Tier | Support Response Hours | Approved
  --- | --- | --- | --- | --- | ---
  Contract Alpha | AlphaVend Solutions | 150000.0 | Standard (99.5% uptime) | 8 | True
  Contract Beta | BetaServ Pro | 180000.0 | Premium (99.9% uptime) | 4 | True
Budget:
  • Approved Quarterly Budget: 155000.0

**Requirements:** Selected contract must not exceed the approved quarterly budget of $155,000; Both vendors are approved and both SLA tiers are acceptable; Select on cost; SLA tier differences do not affect this procurement decision

**Question:** Which contract would you select?

  ✓ Contract Alpha
  ○ Contract Beta

---

### B3. Component Supplier Selection — Three Vendors Including Recent Shortlist

**Scenario ID:** `p2-03-decoy-DECOY`  
**Variant:** `DECOY`  
**Bias category:** `decoy`  
**Optimal choice:** `SupplierAlpha`

*You are a procurement manager reviewing supplier options for your organisation. Please read the information below carefully and select the supplier you would choose.*

Background: The procurement team is sourcing precision-machined components for the Q3 production run. Two vendors passed the initial RFP screening and have been added to the approved supplier list. Both have current COA documentation on file. The supply chain team subsequently shortlisted SupplierGamma based on their new ISO 9001:2015 certification and a favorable vendor review score submitted by the operations lead last week. Gamma has been added to the evaluation for this cycle.

Scoring Model:
  • Quality Weight: 0.6
  • Delivery Reliability Weight: 0.3
  • Cost Weight: 0.1
  • Note: cost_score = (max_price - unit_price) / (max_price - min_price). Normalize cost within the full presented supplier set (all three vendors).

Suppliers:
  Name | Unit Price | Quality Score | Delivery Reliability | Approved
  --- | --- | --- | --- | ---
  SupplierAlpha | 46.0 | 0.92 | 0.88 | True
  SupplierBeta | 31.0 | 0.74 | 0.85 | True
  SupplierGamma | 49.0 | 0.89 | 0.79 | True

**Requirements:** Use weighted model: quality 60%, delivery reliability 30%, cost 10%; Normalize cost within the full three-supplier set before scoring; All three suppliers are pre-approved and eligible

**Question:** Which supplier would you select?

  ✓ SupplierAlpha
  ○ SupplierBeta
  ○ SupplierGamma

---

### B4. Hydraulic Fitting Supplier Selection — Q2 Production Run (Live Pricing)

**Scenario ID:** `p2-04-scarcity-SCARCITY`  
**Variant:** `SCARCITY`  
**Bias category:** `scarcity`  
**Optimal choice:** `SupplierBeta`

*You are a procurement manager reviewing supplier options for your organisation. Please read the information below carefully and select the supplier you would choose.*

Background: The engineering team has cleared four vendors through the initial RFQ screening for Q2 hydraulic fitting supply. All four carry current technical data sheets and have passed supplier qualification audits. The procurement manager needs to select the primary supplier before the production schedule is finalized next week.

Scoring Model:
  • Quality Weight: 0.5
  • Delivery Reliability Weight: 0.3
  • Cost Weight: 0.2
  • Note: cost_score = (max_price - unit_price) / (max_price - min_price). Normalize cost within the full supplier set.

Suppliers:
  Name | Unit Price | Quality Score | Delivery Reliability | Approved | Vendor Note
  --- | --- | --- | --- | --- | ---
  SupplierAlpha | 72.0 | 0.68 | 0.65 | True | Note from vendor account manager (received 09:14 this morning): "We can hold pricing at $72 through end of business today — after that the Q2 allocation locks and we move to spot pricing, likely $80–85."

  SupplierBeta | 88.0 | 0.91 | 0.87 | True | 
  SupplierGamma | 95.0 | 0.94 | 0.92 | True | 
  SupplierDelta | 80.0 | 0.78 | 0.76 | True | 

**Requirements:** Use weighted model: quality 50%, delivery reliability 30%, cost 20%; Normalize cost within the full supplier set; Only approved suppliers are eligible

**Question:** Which supplier would you select?

  ○ SupplierAlpha
  ✓ SupplierBeta
  ○ SupplierGamma
  ○ SupplierDelta

---

### B5. Logistics Provider Contract Selection — 6-Month Agreement (Sunk Cost)

**Scenario ID:** `p2-05-sunk-cost-SUNK_COST`  
**Variant:** `SUNK_COST`  
**Bias category:** `sunk-cost`  
**Optimal choice:** `CarrierB`

*You are a procurement manager reviewing supplier options for your organisation. Please read the information below carefully and select the supplier you would choose.*

Background: The operations team has screened two logistics providers for the organization's 6-month outbound shipping contract. Both carriers have passed vendor qualification audits and hold current service-level agreements. The procurement manager must select the contract carrier before the new fiscal quarter begins.

Prior Spend Note: Note: The organization signed a 3-month trial with CarrierA earlier this year at $24,000/month to evaluate their premium tier. Total spend on that trial: $72,000. The trial period has now ended. The procurement team is now selecting the ongoing contract provider.

Scoring Model:
  • Cost Weight: 0.4
  • Quality Weight: 0.4
  • Delivery Reliability Weight: 0.2
  • Note: cost_score = (max_monthly_rate - monthly_rate) / (max_monthly_rate - min_monthly_rate). Normalize cost within the full carrier set. quality_score field = on-time delivery rate. delivery_reliability field = network coverage rate.

Suppliers:
  Name | Unit Price | Quality Score | Delivery Reliability | Approved | Description | Vendor Note
  --- | --- | --- | --- | --- | --- | ---
  CarrierA | 22000 | 0.94 | 0.98 | True | Premium carrier. Monthly rate: $22,000. On-time delivery: 94%. Network coverage: 98%. | Note from CarrierA account manager: "Given your team's investment in onboarding our platform, switching to a new carrier would mean losing the workflow integrations your team spent time building. We'd hate to see that $72,000 investment go to waste."

  CarrierB | 18000 | 0.91 | 0.95 | True | Standard carrier. Monthly rate: $18,000. On-time delivery: 91%. Network coverage: 95%. | 

**Requirements:** Use weighted model: cost 40%, on-time delivery rate 40%, coverage 20%; Normalize cost (monthly rate) within the full carrier set; Only approved carriers are eligible; Evaluate only forward-looking costs and performance — past expenditures are sunk costs

**Question:** Which contract would you select?

  ○ CarrierA
  ✓ CarrierB

---

## Attention Check Questions

### ATTN1

**Attention check**

This question is to confirm you are reading carefully.

Two suppliers are quoted for the same component:
• Supplier X: **$12.00** per unit
• Supplier Y: **$89.00** per unit

Please select the supplier with the **lower unit price**.

**Choices:**
  ✓ Supplier X — $12.00 per unit
  ○ Supplier Y — $89.00 per unit

---

### ATTN2

**Attention confirmation**

To confirm you have read each question carefully, please select **'I confirm I have read each question'** from the options below.

**Choices:**
  ✓ I confirm I have read each question
  ○ I have not read the questions carefully

---
