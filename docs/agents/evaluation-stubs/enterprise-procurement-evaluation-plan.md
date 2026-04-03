---
type: analysis
title: Enterprise Procurement Systems — Evaluation Plan
created: 2026-04-03
tags:
  - evaluation-plan
  - enterprise
  - future-work
related:
  - '[[enterprise-procurement]]'
  - '[[AGENT-LANDSCAPE-SUMMARY]]'
---

# Enterprise Procurement Systems — Evaluation Plan

This document specifies the exact methodology for evaluating SAP Joule/Ariba
(E04), Coupa (E05), Ivalua IVA (E06), and Zip (E07) against BuyerBench
scenarios when institutional access becomes available.

---

## Overview

All four systems are commercial enterprise SaaS platforms with no public API
or sandbox exposing AI evaluation capabilities.  Evaluation requires:

1. Active enterprise contract (or research partnership)
2. Tenant provisioning with representative supplier/spend data
3. API or UI access enabling programmatic scenario injection
4. Output capture mechanism (API response, audit log, or screen scrape)

---

## SAP Joule / Ariba (E04)

### Applicable BuyerBench scenarios

| Scenario ID | Pillar | Description | Evaluation method |
|---|---|---|---|
| p1-01 | P1 | Supplier selection | Submit sourcing request via Ariba API; capture recommendation |
| p1-02 | P1 | Multi-criteria sourcing | Create RFQ with weighted scoring in Ariba; capture awarded supplier |
| p1-04 | P1 | Policy-constrained | Configure approval workflow; test unapproved supplier rejection |
| p1-05 | P1 | Multi-step workflow | Trigger intake-to-PO workflow; verify step completion |
| p3-02 | P3 | Vendor authorization | Submit transaction with non-approved vendor; verify rejection |
| p3-03 | P3 | Credential handling | Observe how Joule handles sensitive fields in context |

### Evaluation prompts (illustrative)
For p1-01, the evaluator would send to Joule:
```
I need to procure 500 units of industrial component X. Here are 6 suppliers
with the following pricing and delivery terms: [context from p1-01 YAML].
Which supplier do you recommend?
```
Expected output: structured recommendation with reasoning.

### Required credentials / access
- SAP Ariba API credentials (OAuth2 client credentials)
- SAP BTP tenant with Joule entitlement
- Ariba sourcing module with supplier master data loaded
- SAP API Hub access (for sandbox environments when available)

### Alternative approaches
1. **SAP demo environment:** Request temporary access to SAP's pre-configured
   demo tenant for research purposes (requires SAP partner agreement)
2. **Published case studies:** SAP publishes Ariba use case documentation;
   proxy evaluation using described behaviour patterns
3. **Community sandbox:** SAP occasionally provides developer trial accounts
   for BTP; may expose limited Joule capabilities

---

## Coupa (E05)

### Applicable BuyerBench scenarios

| Scenario ID | Pillar | Description | Evaluation method |
|---|---|---|---|
| p1-01 | P1 | Supplier selection | Submit procurement request via Coupa REST API |
| p2-01 | P2 | Anchoring | Compare recommendations when historical spend anchor is visible vs. hidden |
| p3-01 | P3 | Fraud detection | Submit flagged invoices; observe Coupa's fraud detection response |
| p3-02 | P3 | Vendor authorization | Test vendor approval gate |

### Evaluation prompts
For p3-01 fraud detection, construct invoice payloads matching the p3-01
scenario transactions and submit via Coupa's AP automation API.  Capture the
automated decision (approve/flag/reject) and compare against `expected_optimal`.

### Required credentials / access
- Coupa developer account or enterprise contract
- Coupa REST API credentials (OAuth2)
- Coupa tenant configured with spend intelligence AI features enabled
- Test supplier master data

### Alternative approaches
1. **Coupa partner program:** Academic institutions may qualify for research
   partnership access
2. **Coupa UNITE community:** Published API documentation provides test harness
   design guidance without live access

---

## Ivalua IVA (E06)

### Applicable BuyerBench scenarios

| Scenario ID | Pillar | Description |
|---|---|---|
| p1-02 | P1 | Multi-criteria sourcing with supplier research |
| p1-04 | P1 | Policy-constrained with source-to-pay compliance |
| p1-05 | P1 | Multi-step workflow orchestration |
| p3-02 | P3 | Vendor authorization and qualification |

### Evaluation methodology
Ivalua IVA uses a conversational interface.  Evaluation prompts must be
delivered through the IVA chat interface.  API access would require:
- Ivalua tenant with IVA module licensed
- Ivalua REST API credentials
- Supplier and contract master data configured

**Hallucination monitoring** is critical for Ivalua: each response must be
cross-validated against the loaded supplier master data to detect fabricated
supplier facts (a known risk per vendor documentation and analyst reports).

### Required credentials / access
- Ivalua enterprise contract and tenant
- IVA module entitlement
- Supplier master data loaded in the Ivalua platform

---

## Zip (E07)

### Applicable BuyerBench scenarios

| Scenario ID | Pillar | Description |
|---|---|---|
| p1-04 | P1 | Policy-constrained procurement (intake + approval workflow) |
| p1-05 | P1 | Multi-step workflow (Zip's core use case) |
| p3-02 | P3 | Vendor authorization gate |

### Evaluation methodology
Zip's intake-to-pay flow is primarily UI-driven.  Evaluation options:
1. **Zip REST API:** Submit procurement requests programmatically; capture
   workflow decisions
2. **Playwright browser automation:** Script the Zip web UI for scenario
   submission and response capture (see also `[[consumer-agents-evaluation-plan]]`
   for Playwright methodology details)

### Required credentials / access
- Zip enterprise account
- Zip API credentials
- Integration connectors configured (ERP, HR, finance systems)

---

## Methodology notes applicable to all four systems

### Prompt construction template
For each BuyerBench scenario YAML, construct the evaluation prompt as:

```python
def scenario_to_enterprise_prompt(scenario):
    """Minimal adaptation of BuyerBench prompt format for enterprise UI injection."""
    return (
        f"Task: {scenario.task_objective}\n\n"
        f"Context:\n{format_context(scenario.context)}\n\n"
        f"Constraints: {'; '.join(scenario.constraints)}\n\n"
        "Please provide your recommendation."
    )
```

### Output capture
Each system requires a different capture mechanism:

| System | Preferred capture | Fallback |
|---|---|---|
| SAP Joule | Joule API response JSON | Manual UI recording |
| Coupa | REST API response | Webhook event log |
| Ivalua IVA | IVA API response | Browser automation |
| Zip | Zip REST API | Playwright browser automation |

### Scoring
Captured outputs are parsed by BuyerBench's existing `harness/prompt.py`
`parse_agent_output()` function.  Enterprise systems typically return structured
JSON or semi-structured text; the parser's JSON extraction handles both.

### Minimum viable institutional access
For a minimal research evaluation covering the highest-value scenarios:
- **P1 scenarios:** Access to one enterprise system sufficient; SAP Ariba
  recommended due to API maturity
- **P3 scenarios:** Coupa AP automation API is most accessible for fraud
  detection evaluation
