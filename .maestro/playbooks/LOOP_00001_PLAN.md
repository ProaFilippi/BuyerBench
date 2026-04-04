---
type: research
title: "Research Plan — AI Buyer Agents Market Research — Loop 00001"
created: 2026-04-04
tags:
  - market-research
  - research-plan
  - ai-agents
  - procurement
  - agentic-commerce
related:
  - '[[LOOP_00001_ENTITIES]]'
  - '[[LOOP_00001_MARKET_ANALYSIS]]'
  - '[[INDEX]]'
---

# Research Plan — Loop 00001

This document contains evaluated entities and their prioritized research plans. Entities are sourced from `LOOP_00001_ENTITIES.md` and evaluated one at a time for research importance and effort.

---

## Procure AI - Evaluated 2026-04-04

**Source:** LOOP_00001_ENTITIES.md — Companies category
**Type:** Company
**Category:** AI-Native Procurement Platforms

### Quick Profile
Procure AI is an enterprise procurement SaaS company that deploys 50+ autonomous AI agents across the full source-to-pay lifecycle. Its multi-tier agent architecture supports autonomous execution, human-collaborative, and ambient/proactive operating modes. The company raised a $13M seed round in November 2025 led by Headline (with C4 Ventures and Futury Capital).

### Importance Assessment
- **Rating:** CRITICAL
- **Justification:** Procure AI is one of the clearest pure-play "AI buyer agent" companies in existence — their core product is essentially an operational deployment of the exact agent types BuyerBench is designed to evaluate. Their three-tier agent model (autonomous, collaborative, ambient) maps closely to the behavioral and capability pillars in BuyerBench. As a funded, production-deployed system, it provides a direct competitive reference point and potential benchmarking subject. Understanding how Procure AI defines "autonomous buyer agent" success sets the semantic baseline for the benchmark itself.
- **Key Questions to Answer:**
  1. What specific procurement tasks do Procure AI's autonomous agents perform end-to-end, and how do these map to BuyerBench Pillar 1 scenarios?
  2. How does Procure AI handle economic decision-making (price negotiation, quote comparison, supplier scoring) — does it expose any decision quality metrics relevant to Pillar 2?
  3. What guardrails, audit trails, or compliance controls are built into the platform — and how do these relate to Pillar 3 security/compliance scenarios?

### Research Effort Assessment
- **Rating:** MEDIUM
- **Justification:** Procure AI has meaningful press coverage from its November 2025 funding round (SiliconANGLE, Crunchbase), a company website with product descriptions, and investor-facing materials. However, it is a seed-stage startup, so detailed technical documentation, agent architecture papers, and performance benchmarks are unlikely to be publicly available. Synthesis from multiple secondary sources (press, website, LinkedIn) will be required.
- **Primary Sources Available:**
  - Company website: procure.ai (product pages, agent descriptions, use cases)
  - SiliconANGLE funding announcement (Nov 2025): https://siliconangle.com/2025/11/27/procure-ai-lands-13m-funding-automate-business-procurement-tasks/
  - Crunchbase profile (funding history, investor details, founding team)
  - LinkedIn company page (team size, job postings — signals of product focus areas)
  - Headline VC portfolio page (investor thesis, positioning language)

### Expected Connections
Entities this will likely link to:
- [[Omnea]] — both target enterprise procurement automation; may compete or integrate
- [[Zycus]] — established incumbent whose agent capabilities Procure AI likely positions against
- [[Fairmarkit]] — overlapping tail-spend and sourcing automation use cases
- [[Skyfire]] — Procure AI autonomous agents will eventually need payment execution rails that Skyfire provides
- [[Headline VC]] — lead investor; may have portfolio companies that interact with Procure AI

### Status: RESEARCHED
### Research File: `vault/Companies/Procure-AI.md`
### Researched: 2026-04-04

---

## Omnea - Evaluated 2026-04-04

**Source:** LOOP_00001_ENTITIES.md — Companies category
**Type:** Company
**Category:** AI-Native Procurement Platforms

### Quick Profile
Omnea is an enterprise procurement orchestration platform that automates vendor onboarding, intake workflows, and cross-functional approvals. The company raised a $50M Series B in September 2025 led by Insight Partners and Khosla Ventures, bringing total funding above $75M. Omnea positions itself as a CFO-facing tool ("make procurement every CFO's competitive advantage"), emphasizing economic outcomes over operational automation.

### Importance Assessment
- **Rating:** HIGH
- **Justification:** Omnea's CFO positioning and $75M+ funding make it a significant commercial reference for BuyerBench Pillar 2 (economic decision quality). Its focus on cross-functional approval workflows and vendor onboarding maps directly to Pillar 1 capability scenarios. As a peer competitor to Procure AI, it represents a different product philosophy — orchestration-first vs. agent-execution-first — that informs BuyerBench's scenario diversity. Insight Partners + Khosla backing signals strong market validation.
- **Key Questions to Answer:**
  1. What specific economic optimization signals does Omnea surface to users (cost savings, cycle time, supplier substitution recommendations)?
  2. How autonomous is Omnea's decision-making — does it execute or only recommend? What human-in-the-loop controls exist?
  3. How does Omnea's intake and approval workflow map to BuyerBench Pillar 1 multi-step procurement task scenarios?

### Research Effort Assessment
- **Rating:** MEDIUM
- **Justification:** Omnea has good press coverage from its Series B announcement (Sep 2025) with multiple investor and founder quotes. The company website details product functionality. However, granular performance metrics and technical decision architecture may require synthesis from secondary sources.
- **Primary Sources Available:**
  - Company website: omnea.co (product pages, use cases, ROI claims)
  - Series B announcement: omnea.co/blog/series-b-announcement
  - Insight Partners and Khosla Ventures portfolio pages (investor thesis framing)
  - LinkedIn company page (team size, job postings)
  - Product Hunt / G2 reviews (customer-reported capabilities)

### Expected Connections
Entities this will likely link to:
- [[Procure AI]] — direct competitor in enterprise procurement automation; different product philosophy
- [[Zycus]] — established incumbent; Omnea positions against legacy suites
- [[Fairmarkit]] — complementary in sourcing; potential integration partner
- [[Insight Partners]] — lead Series B investor
- [[Khosla Ventures]] — co-lead Series B investor

### Status: PENDING
