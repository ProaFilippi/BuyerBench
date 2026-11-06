# Phase 08: Commercial Agent Research + Evaluation Planning

This phase catalogs and profiles the commercial and open-source buyer agents identified in the deep research report, determines which ones are accessible for direct evaluation, implements adapters where possible, and creates structured research profiles for all agents. For inaccessible commercial systems (SAP, Coupa, Ivalua, Zip), we design documented evaluation stubs that describe the methodology for future evaluation. The result is a comprehensive agent catalog that significantly strengthens the paper's breadth.

## Tasks

- [x] Create structured agent profiles for all 23 catalogued agents from deep-research-report.md:
  - Create `docs/agents/` folder and one markdown file per agent category
  - `docs/agents/enterprise-procurement.md`: profiles for SAP Joule/Ariba (E04), Coupa (E05), Ivalua IVA (E06), Zip (E07) — each with front matter `type: reference, tags: [agent-profile, enterprise, procurement]`; include: what BuyerBench scenarios they'd be evaluated on, accessibility for research evaluation, expected strengths/weaknesses based on vendor documentation, evaluation blockers (access, cost, enterprise-only)
  - `docs/agents/consumer-shopping.md`: profiles for Amazon Rufus (E01), Klarna (E02), Google Agentic Checkout (E03) — same structure; note: these are consumer-facing products with no direct evaluation API; describe the methodology gap
  - `docs/agents/trading-and-simulation.md`: profiles for Freqtrade (E08), Hummingbot (E09), LEAN (E10), FinRL (E11), ABIDES (E12) — note: these are open-source and evaluable; assess relevance to BuyerBench pillars (primarily Pillar 1 + 2 for trading agents)
  - `docs/agents/negotiation-and-economics.md`: profiles for NegMAS (E13), GeniusWeb/Genius (E14), ANAC (E15), AI Economist (E16)
  - `docs/agents/payment-protocols.md`: profiles for AP2 (E17), UCP (E18), ACP (E19), Stripe Agent Toolkit (E20), Visa Intelligent Commerce (E21), Visa TAP (E22), Mastercard Agent Pay (E23)
  - Create `docs/agents/INDEX.md` linking all profiles

- [x] Implement adapters for accessible open-source agents:
  - `agents/stripe_toolkit_agent.py`: implement adapter using Stripe Agent Toolkit SDK; create a minimal Pillar 3-focused evaluation mode where the agent is given a payment task and evaluated on credential handling, tool permission scoping, and correct API call sequencing; requires `STRIPE_SECRET_KEY` (test mode) in config
  - `agents/negmas_agent.py`: implement adapter wrapping a NegMAS negotiation agent for Pillar 1 multi-criteria scenarios where supplier selection can be framed as a bilateral negotiation; map NegMAS utility functions to BuyerBench scenario economics
  - Add both to `agents/registry.py`

- [x] Design evaluation stubs for inaccessible commercial agents:
  - Create `docs/agents/evaluation-stubs/enterprise-procurement-evaluation-plan.md`: for each inaccessible enterprise system (SAP, Coupa, Ivalua, Zip), document: the exact scenarios from BuyerBench that would apply, the evaluation methodology (what prompts to send, what outputs to capture), what institutional access or API credentials would be required, and what alternative evaluation approaches exist (e.g., public demo environments, published case studies as proxy data); front matter `type: analysis, tags: [evaluation-plan, enterprise, future-work]`
  - Create `docs/agents/evaluation-stubs/consumer-agents-evaluation-plan.md`: same for Amazon Rufus, Klarna, Google Agentic Checkout; propose browser automation + Playwright as a methodology for evaluating consumer-facing agents via their web interfaces

- [x] Run BuyerBench against accessible open-source agents and integrate results:
  - Run `python -m buyerbench run --agent stripe-toolkit --pillar 3 --output-dir results/experiments/pillar3-stripe/`
  - Run `python -m buyerbench run --agent negmas --pillar 1 --output-dir results/experiments/pillar1-negmas/`
  - Integrate these results into `results/experiments/FULL-REPORT.json` by re-running the report generator

- [x] Compile the agent landscape summary document:
  - Create `docs/agents/AGENT-LANDSCAPE-SUMMARY.md`: synthesize findings across all 23+ agents; organize by category; produce a comparison table adapted from `deep-research-report.md` with BuyerBench evaluation status column (Evaluated / Stub Designed / Not Applicable); front matter `type: analysis, tags: [agent-landscape, summary, research-paper]`; this document maps directly to the paper's "Evaluated Systems" section
  - Include `related: ['[[FULL-REPORT]]', '[[enterprise-procurement-evaluation-plan]]']` wiki-links
