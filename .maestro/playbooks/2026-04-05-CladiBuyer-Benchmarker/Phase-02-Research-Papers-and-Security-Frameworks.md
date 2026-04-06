# Phase 02: Profile Research Papers & Security Frameworks

This phase completes the academic and standards layer of the research vault by profiling all 5 pending research papers and all 5 pending security/compliance frameworks. These entities form the theoretical and regulatory backbone of BuyerBench — the papers provide empirical evidence for bias testing (Pillar 2) and benchmark methodology, while the security frameworks define compliance ground truth for Pillar 3 scenario design. By the end of this phase, every discovered entity will have a full profile, bringing vault coverage to 100% of the original 25 discovered entities.

## Tasks

- [x] Read profile format references and paper/framework entity details before writing any profiles:
  - Read `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/Technologies/ACP.md` (format reference — longest existing profile)
  - Read `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/LOOP_00001_ENTITIES.md` lines covering Research Papers and Security/Compliance sections (scan for entity metadata already captured)
  <!-- Completed 2026-04-05: ACP.md establishes the profile format — YAML front matter (type/title/created/tags/related), Quick Facts table, deep protocol sections, BuyerBench relevance blockquotes, wiki-links, and numbered Sources. ENTITIES.md confirmed arXiv IDs, Why Notable context, and discovery sources for all 5 research papers (ACES 2508.02630, LLM Agent Survey 2507.21504, AgentBench 2308.03688, WebArena 2307.13854, WebShop 2207.01206) and all 5 security frameworks (PCI DSS v4.0, EMV 3DS2, NIST AI RMF 1.0, ISO 42001:2023, FATF AML/CFT). All 10 entities have Status: PENDING — ready for profiling in subsequent tasks. -->

- [x] Research and profile the ACES paper (AI buyer agent bias evaluation):
  - Web search: "ACES What Is Your AI Agent Buying arXiv 2508.02630"
  - Web search: "ACES benchmark buyer agent position bias anchoring decoy evaluation"
  - Create `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/Research-Papers/ACES-AI-Agent-Buying.md` with YAML front matter (type: research-paper, tags: [benchmark, buyer-agent, behavioral-bias, evaluation, pillar-2]) and sections: Citation, Abstract Summary, Key Findings (position bias, anchoring, decoy susceptibility metrics), Methodology (controlled variants, scenario design), Datasets Used, Implications for BuyerBench Pillar 2 Design, wiki-links to [[AgentBench]], [[WebShop]], [[Fairmarkit]]
  <!-- Completed 2026-04-05: Profile created at Research-Papers/ACES-AI-Agent-Buying.md. ACES = Agentic e-CommercE Simulator (arXiv 2508.02630, Columbia University, Aug 2025, v3 Dec 2025). Key findings: 5× position bias, −0.135–−0.371 sponsored tag penalty, +1.06–+1.90 Overall Pick endorsement effect, price elasticity −1.6 to −2.2, seller description manipulation yielding +3.66–80.4pp market share. RCT+conditional logit methodology directly validates BuyerBench Pillar 2 controlled-variant design. Six BuyerBench design implications documented. -->

- [x] Research and profile the LLM Agent Benchmarking Survey (arXiv 2507.21504):
  - Web search: "Evaluation Benchmarking LLM Agents Survey arXiv 2507.21504 2025"
  - Web search: "LLM agent evaluation survey taxonomy methodology 2025"
  - Create `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/Research-Papers/LLM-Agent-Benchmarking-Survey.md` with YAML front matter (type: research-paper, tags: [survey, benchmark, methodology, llm-agents, evaluation]) and sections: Citation, Scope, Taxonomy of Evaluation Dimensions, Key Gaps Identified, Methodological Recommendations, Implications for BuyerBench Framework Design, wiki-links to [[AgentBench]], [[ACES-AI-Agent-Buying]]
  <!-- Completed 2026-04-05: Profile created at Research-Papers/LLM-Agent-Benchmarking-Survey.md. Authors: Mohammadi, Li, Lo, Yip (SAP). Published KDD '25 (ACM DOI 10.1145/3711896.3736570). Two-dimensional taxonomy: (1) objectives — behavior, capabilities, reliability, safety; (2) process — interaction modes, datasets, metrics, tooling, environments. Key gaps: enterprise compliance/reliability, safety coverage, fine-grained scoring, cost-efficiency metrics. BuyerBench three pillars map exactly to three taxonomy objectives (capability → Pillar 1, reliability/robustness → Pillar 2, safety/compliance → Pillar 3). Survey provides academic grounding for multi-pillar, non-aggregated evaluation design. Six BuyerBench design implications documented. -->

- [x] Research and profile AgentBench (ICLR 2024):
  - Web search: "AgentBench Evaluating LLMs as Agents ICLR 2024 paper results"
  - Web search: "AgentBench benchmark tasks environments leaderboard"
  - Create `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/Research-Papers/AgentBench.md` with YAML front matter (type: research-paper, tags: [benchmark, multi-task, llm-agents, iclr-2024]) and sections: Citation, Task Environments (8 environments), Scoring Methodology, Key Results (model comparisons), Lessons for Multi-Pillar Benchmark Design, BuyerBench Alignment, wiki-links to [[WebArena]], [[WebShop]], [[LLM-Agent-Benchmarking-Survey]]
  <!-- Completed 2026-04-05: Profile created at Research-Papers/AgentBench.md. Authors: Liu et al. (Tsinghua THUDM group), ICLR 2024, arXiv 2308.03688. 8 task environments: OS, DB, KG (code-grounded); DCG, LTP, HH/ALFWorld (game-grounded); Web Shopping, Web Browsing (web-grounded). Key result: GPT-4 scored ~4.01 vs. <1.00 for best open-source 70B models — ~4× commercial/OSS gap. Three root-cause obstacles: poor long-term reasoning, weak decision-making under uncertainty, instruction-following failures. Five lessons for multi-pillar benchmark design documented (per-environment metrics, multi-turn evaluation, I/O interface standardization, baseline environment, commercial+OSS testing). Full BuyerBench alignment table mapping all 8 AgentBench environments to BuyerBench pillars and components. -->

- [ ] Research and profile WebArena (arXiv 2307.13854):
  - Web search: "WebArena realistic web environment evaluation autonomous agents 2307.13854"
  - Web search: "WebArena e-commerce domain shopping tasks benchmark"
  - Create `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/Research-Papers/WebArena.md` with YAML front matter (type: research-paper, tags: [benchmark, web-agent, e-commerce, realistic-environment]) and sections: Citation, Environment Design (5 websites including e-commerce), Task Categories, Success Rate Metrics, Key Limitations, BuyerBench Pillar 1 Alignment (web-based procurement tasks), wiki-links to [[WebShop]], [[AgentBench]]

- [ ] Research and profile WebShop (NeurIPS 2022, arXiv 2207.01206):
  - Web search: "WebShop NeurIPS 2022 AI shopping benchmark 1.18 million Amazon products"
  - Web search: "WebShop environment reward function agent evaluation results 2207.01206"
  - Create `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/Research-Papers/WebShop.md` with YAML front matter (type: research-paper, tags: [benchmark, shopping, e-commerce, neurips-2022, foundational]) and sections: Citation, Dataset (1.18M Amazon products), Task Design (instruction-following product search + purchase), Reward Function, Human vs. Agent Performance, Foundational Influence on Later Benchmarks, BuyerBench Pillar 1 Alignment, wiki-links to [[WebArena]], [[ACES-AI-Agent-Buying]]

- [ ] Research and profile PCI DSS v4.0:
  - Web search: "PCI DSS v4.0 requirements full enforcement April 2025 AI agents"
  - Web search: "PCI DSS 4.0 payment security requirements card-not-present agent transactions"
  - Create `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/Security-Compliance/PCI-DSS-v4.md` with YAML front matter (type: compliance-framework, tags: [payment-security, compliance, PCI-DSS, standards, pillar-3]) and sections: Overview, v4.0 Key Changes (vs. v3.2.1), Full Enforcement Date (Apr 2025), Requirements Most Relevant to AI Agent Transactions (Req 3, 6, 8, 10, 12), Applicability to Agentic Commerce, BuyerBench Pillar 3 Scenario Mapping, wiki-links to [[EMV-3DS2]], [[ACP]], [[Visa-Intelligent-Commerce]]

- [ ] Research and profile EMV 3-D Secure (3DS2):
  - Web search: "EMV 3D Secure 3DS2 card-not-present authentication AI agent transactions 2025"
  - Web search: "3DS2 friction-less flow challenge flow authentication protocol specification"
  - Create `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/Security-Compliance/EMV-3DS2.md` with YAML front matter (type: compliance-framework, tags: [payment-security, authentication, 3ds2, emv, fraud-prevention, pillar-3]) and sections: Overview, Protocol Flow (frictionless vs. challenge), Role in AI Agent Checkout (who initiates authentication?), Integration with Visa/Mastercard Agent Pay, Fraud Prevention Efficacy, BuyerBench Pillar 3 Scenario Mapping, wiki-links to [[PCI-DSS-v4]], [[Visa-Intelligent-Commerce]], [[Mastercard-Agent-Pay]]

- [ ] Research and profile NIST AI Risk Management Framework (AI RMF 1.0):
  - Web search: "NIST AI RMF 1.0 AI Risk Management Framework January 2023 requirements"
  - Web search: "NIST AI RMF governance trustworthy AI buyer agent compliance"
  - Create `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/Security-Compliance/NIST-AI-RMF.md` with YAML front matter (type: compliance-framework, tags: [ai-governance, risk-management, nist, voluntary, pillar-3]) and sections: Overview, Core Functions (GOVERN, MAP, MEASURE, MANAGE), Voluntary vs. Mandatory Status, Applicability to Autonomous Procurement Agents, Key Controls Relevant to BuyerBench, Cross-reference to ISO 42001, wiki-links to [[ISO-42001]], [[FATF-AML-CFT]]

- [ ] Research and profile ISO/IEC 42001:2023:
  - Web search: "ISO IEC 42001 2023 AI Management System standard certification requirements"
  - Web search: "ISO 42001 AI governance procurement enterprise certification 2024 2025"
  - Create `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/Security-Compliance/ISO-42001.md` with YAML front matter (type: compliance-framework, tags: [ai-governance, iso, management-system, certification, pillar-3]) and sections: Overview, Scope and Requirements, Certification Process, First Certifications (who has certified?), Relation to NIST AI RMF, Applicability to AI Buyer Agent Deployments, BuyerBench Pillar 3 Scenario Mapping, wiki-links to [[NIST-AI-RMF]], [[PCI-DSS-v4]]

- [ ] Research and profile FATF AML/CFT Guidance for AI and Virtual Assets:
  - Web search: "FATF AML CFT Travel Rule guidance AI agents virtual assets 2025"
  - Web search: "FATF recommendations autonomous agents financial transactions compliance"
  - Create `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/Security-Compliance/FATF-AML-CFT.md` with YAML front matter (type: compliance-framework, tags: [aml, cft, fatf, travel-rule, virtual-assets, pillar-3]) and sections: Overview, Travel Rule (who must comply, thresholds), Virtual Asset Guidance Relevant to AI Agents, Risk-Based Approach, Regulatory Gaps for Autonomous Agents, BuyerBench Pillar 3 Scenario Mapping, wiki-links to [[PCI-DSS-v4]], [[NIST-AI-RMF]], [[x402]]

- [ ] Update the vault INDEX.md to reflect all 10 new profiles and full 25/25 entity coverage:
  - Read `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/research/market-research/vault/INDEX.md`
  - Add all 10 new entries under Research-Papers and Security-Compliance sections
  - Update statistics: 25/25 entities researched (100% coverage)
  - Add "Phase 02 Complete" note with date 2026-04-05
