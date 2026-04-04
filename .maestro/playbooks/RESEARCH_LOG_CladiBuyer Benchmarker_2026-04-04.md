# Research Log — CladiBuyer Benchmarker — 2026-04-04

---

## [2026-04-04 Loop 9] - Researched: Omnea

**Loop:** 00001 (Loop 9 — stall-break direct execution)
**Entity Type:** Company
**Importance:** HIGH
**File Created:** `vault/Companies/Omnea.md`

### Research Summary
Omnea is an AI SRM (Supplier Relationship Management) platform founded in 2022 by Ben Freeman (CEO), with ex-Tessian executives Abhirukt Sapru (CCO) and Sabrina Castiglione (CFO). Raised $50M Series B (Sep 2025, Insight Partners + Khosla Ventures lead; total >$75M). Key insight: Omnea's "orchestration-first" architecture contrasts sharply with Procure AI's "execution-first" approach — Omnea routes and recommends rather than autonomously executing, which is a foundational design dimension for BuyerBench Pillar 1 scenario breadth.

### Key Facts Discovered
- Founded 2022, London; team from Tessian (acquired by Proofpoint)
- 5× revenue growth and 3× headcount growth in the year before Series B
- Enterprise customers: Spotify, Adecco Group, Entrust, Wise, MongoDB, Monzo
- Product = single front door for procurement requests + two-way finance tech stack orchestration
- CFO positioning: procurement as strategic financial intelligence tool, not just operational automation
- "AI SRM" category framing — positions Omnea above point solutions in vendor relationship lifecycle

### Links Created
- [[Procure-AI]] — direct competitor; execution-first vs. orchestration-first architecture
- [[Zycus]] — incumbent contrast; Omnea as modern overlay vs. legacy suite
- [[Fairmarkit]] — peer; different workflow layer focus (sourcing events vs. intake/approval)
- [[Insight Partners]] — lead Series B investor
- [[Khosla Ventures]] — co-lead Series B investor

### Sources Used
1. [Omnea Series B Blog](https://www.omnea.co/blog/series-b-announcement)
2. [PR Newswire — Omnea $50M](https://www.prnewswire.com/news-releases/omnea-raises-50m-to-make-procurement-every-cfos-competitive-advantage-302559153.html)
3. [Procurement Magazine — Omnea Series B](https://procurementmag.com/news/omnea-series-b-funding)
4. [TechStartups — Omnea $50M](https://techstartups.com/2025/09/17/omnea-raises-50m-from-insight-and-khosla-to-transform-enterprise-procurement-with-ai/)

### Research Notes
- No public API documentation, agent architecture internals, or technical specs found
- Specific ARR or revenue figures not disclosed; "5× growth" is the only financial performance metric
- Founder Ben Freeman's prior background before Omnea not confirmed from public sources
- Follow-up recommended: research Zycus (PENDING HIGH in PLAN.md); then Fairmarkit, Skyfire

---

## [2026-04-04 00:00] - Researched: Procure AI

**Loop:** 00001
**Entity Type:** Company
**Importance:** CRITICAL
**File Created:** `vault/Companies/Procure-AI.md`

### Research Summary
Procure AI is a European AI-native procurement automation platform founded in 2020 by Konstantin von Büren and Yves Bauer. It deploys 50+ AI agents across a three-tier architecture (autonomous/collaborative/ambient) covering the full source-to-pay lifecycle, and raised a $13M seed round led by Headline in November 2025. Enterprise clients managing €50B+ in spend report 37–47% time savings and ~5% cost reductions from the platform.

### Key Facts Discovered
- **Three-tier agent architecture** directly analogous to BuyerBench evaluation spectrum: autonomous execution (Pillar 1), collaborative decision support (Pillar 2 quality), ambient proactive agents (Pillar 3 compliance triggers)
- **Performance baselines for BuyerBench**: 4.9% average tactical spend savings, 47% faster award decisions, 60% of intake requests handled fully autonomously — usable as Pillar 1 benchmark targets
- **Founded 2020**, seed-stage as of 2025 — earlier than the "AI agent" hype wave, suggesting real enterprise traction rather than narrative-driven funding
- **Sovereign data positioning**: dedicated hosting, built in Europe — Pillar 3 data residency and audit trail requirements have real-world precedent here
- **Konstantin von Büren** previously worked at C4 Ventures, one of Procure AI's own seed investors — founder-investor connection worth noting
- **Fairmarkit listed as direct competitor** by CB Insights; Omnea overlaps on intake/vendor workflows; Zycus is the incumbent contrast
- No publicly disclosed API documentation, technical architecture papers, or security certification details (ISO 27001, SOC 2 unconfirmed)

### Links Created
- [[Headline-VC]] — lead seed investor
- [[C4-Ventures]] — co-investor; founder Konstantin von Büren previously worked there
- [[Futury-Capital]] — co-investor
- [[Omnea]] — competitor: AI-native intake and vendor workflow automation
- [[Zycus]] — competitor: established S2P incumbent with agentic AI features
- [[Fairmarkit]] — competitor: tail-spend sourcing automation (CB Insights peer listing)
- [[Skyfire]] — potential future integration: payment execution rails for autonomous agents
- [[Konstantin-von-Büren]] — Co-CEO and Co-Founder
- [[Yves-Bauer]] — Co-CEO and Co-Founder

### Sources Used
1. [Procure AI Blog — Seed Funding Announcement](https://www.procure.ai/blog/seed-funding-announcement)
2. [SiliconANGLE — Procure AI lands $13M](https://siliconangle.com/2025/11/27/procure-ai-lands-13m-funding-automate-business-procurement-tasks/)
3. [Tech.eu — Procure AI nets $13M](https://tech.eu/2025/11/26/procure-ai-nets-13m-to-scale-autonomous-ai-for-procurement/)
4. [Procure AI website](https://www.procure.ai/)
5. [EU-Startups — Procure AI €11M](https://www.eu-startups.com/2025/11/amid-new-tariffs-and-volatile-delivery-timelines-procure-ai-lands-e11-million-to-help-enterprises-stabilise-procurement-and-supply-chains/)
6. [Crunchbase — Konstantin von Bueren](https://www.crunchbase.com/person/konstantin-von-bueren)

### Research Notes
- Technical documentation (agent architecture internals, ML stack, API specs) is not publicly available — Procure AI is seed-stage and protective of IP
- Security certifications (ISO 27001, SOC 2) referenced via trust.procure.ai but specific certification status not confirmed from public sources
- Founding year stated as "spring 2020" in one source but not consistently confirmed across all coverage
- Follow-up recommended: research Omnea, Fairmarkit, Zycus for competitive landscape depth; research Headline VC thesis for market context
