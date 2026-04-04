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

### Status: RESEARCHED
### Research File: `vault/Companies/Omnea.md`
### Researched: 2026-04-04

---

## Zycus - Evaluated 2026-04-04

**Source:** LOOP_00001_ENTITIES.md — Companies category
**Type:** Company
**Category:** AI-Native Procurement Platforms

### Quick Profile
Zycus is a global source-to-pay suite that has embedded agentic AI across its Merlin platform. Key components include Merlin Intake (AI-powered procurement intake orchestration), Merlin Autonomous Negotiation Agent (ANA — a production-deployed system that conducts price negotiations with suppliers autonomously without constant human intervention), and Merlin Copilot (user-facing assistant). Zycus serves enterprise customers in manufacturing, retail, and financial services globally, with approximately 2,500 employees.

### Importance Assessment
- **Rating:** HIGH
- **Justification:** Zycus is among the first established procurement vendors to publicly deploy an *autonomous negotiation agent* (Merlin ANA) in production. This is a direct commercial reference implementation of agent-driven price negotiation — precisely the scenario type BuyerBench Pillar 1 is designed to evaluate. Merlin ANA's existence allows BuyerBench to calibrate negotiation task scenarios against real-world deployed capabilities. Zycus also provides a useful contrast to pure-play startups (Procure AI, Omnea): it illustrates how incumbents add agentic AI to existing source-to-pay suites rather than building agent-native from scratch, which informs scenario design breadth.
- **Key Questions to Answer:**
  1. What negotiation protocol does Merlin ANA use — formal alternating-offer mechanisms, LLM-prompt-driven negotiation, or a hybrid? How does its approach compare to NegMAS?
  2. What economic performance metrics does Zycus publish for Merlin ANA (savings rate, deal closure time, supplier win/concession rates)? How do these compare to human buyer baselines?
  3. What human oversight and fallback controls govern Merlin ANA — under what conditions does it escalate to a human buyer, and what authorization boundaries exist?

### Research Effort Assessment
- **Rating:** MEDIUM
- **Justification:** Zycus is a large, established private company with a mature website, product documentation, and meaningful press coverage from its Merlin ANA launch. Procurement trade press (Spend Matters, CPO Rising) and analyst platforms (Gartner Peer Insights, G2) cover Zycus. Technical architecture details and independent performance benchmarks will require synthesis from product pages, press releases, and analyst commentary.
- **Primary Sources Available:**
  - Company website: zycus.com (Merlin product pages, ANA feature descriptions)
  - Spend Matters / CPO Rising analyst coverage (Merlin ANA launch)
  - G2 / Gartner Peer Insights (customer reviews citing Merlin capabilities)
  - Zycus press releases (Merlin ANA GA announcement)
  - LinkedIn company page (team size, AI team hiring signals)

### Expected Connections
Entities this will likely link to:
- [[Procure AI]] — startup competitor; agent-native architecture vs. Zycus suite add-on
- [[Omnea]] — competitor in procurement orchestration; Omnea positions against legacy suites like Zycus
- [[Fairmarkit]] — overlapping sourcing automation for tail-spend workflows
- [[NegMAS]] — open-source negotiation framework Merlin ANA may be architecturally comparable to

### Status: PENDING

---

## Fairmarkit - Evaluated 2026-04-04

**Source:** LOOP_00001_ENTITIES.md — Companies category
**Type:** Company
**Category:** AI-Native Procurement Platforms (Tail-Spend Automation)

### Quick Profile
Fairmarkit is an AI-powered sourcing platform that automates tail-spend and low-value procurement through demand-to-award automation and supplier recommendation. The platform handles thousands of small sourcing events autonomously — automating RFQ creation, supplier matching, bid collection, and award decisions. Fairmarkit published a "2025 AI in Procurement Index" documenting AI adoption trends and buyer behavior patterns in procurement organizations.

### Importance Assessment
- **Rating:** HIGH
- **Justification:** Tail-spend automation represents the highest-frequency, most repetitive segment of buyer-agent workflows — exactly the scenario type where BuyerBench Pillar 1 capability benchmarks are most meaningful (supplier discovery, quote comparison, bid evaluation at scale). Fairmarkit's autonomous demand-to-award workflow makes it a direct commercial reference implementation for "sourcing cycle" scenarios in BuyerBench. The 2025 AI in Procurement Index may also contain adoption/bias data relevant to Pillar 2 scenario design. As a direct competitor to Procure AI and peer of Omnea/Zycus, it completes the competitive landscape mapping for this benchmark domain.
- **Key Questions to Answer:**
  1. How autonomous is Fairmarkit's award decision — does it fully auto-award, or does it surface a ranked recommendation requiring human approval?
  2. What supplier selection and bid evaluation criteria does the AI use (price alone, quality scores, delivery terms, risk ratings)? How do these map to BuyerBench Pillar 1 multi-criteria scoring scenarios?
  3. What does the 2025 AI in Procurement Index report about bias or consistency patterns in how AI-assisted procurement teams make sourcing decisions?

### Research Effort Assessment
- **Rating:** MEDIUM
- **Justification:** Fairmarkit is a Boston-based, VC-backed startup with solid press coverage, published thought leadership (the 2025 Index), and an active website with product documentation and customer case studies. Procurement trade press (Spend Matters, CPO Rising) covers Fairmarkit. Independent financial data (funding rounds, ARR) may require synthesis from multiple sources.
- **Primary Sources Available:**
  - Company website: fairmarkit.com (product pages, use case descriptions, customer stories)
  - 2025 AI in Procurement Index: fairmarkit.com/resource/2025-ai-in-procurement
  - Spend Matters / CPO Rising analyst coverage (product reviews, competitive quadrant placements)
  - Crunchbase profile (funding history, founding team, investor details)
  - G2 / Gartner Peer Insights (customer reviews and feature ratings)

### Expected Connections
Entities this will likely link to:
- [[Procure AI]] — direct competitor; both target autonomous sourcing execution
- [[Omnea]] — complementary in intake orchestration; Fairmarkit focuses downstream on sourcing events
- [[Zycus]] — overlapping tail-spend sourcing use case; Fairmarkit positions against legacy suite limitations
- [[NegMAS]] — theoretical comparison for multi-supplier bidding optimization mechanisms
- [[SAP Ariba]] — incumbent tail-spend platform Fairmarkit displaces

### Status: PENDING
