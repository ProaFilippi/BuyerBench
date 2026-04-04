---
type: index
title: Literature Index
created: 2026-04-03
tags:
  - index
---

# Literature Index

Top-level index of all literature review documents. Updated as each phase adds new documents.

---

## Evaluation Methodology (`eval-methodology/`)

- [[agent-evaluation-overview]] — Survey of key agent benchmarks (AgentBench, GAIA, WebArena, SWE-bench, HELM, BIG-Bench); properties of good benchmarks; gaps addressed by BuyerBench
- [[llm-as-judge]] — LLM-as-judge methods, positional/verbosity/self-enhancement biases, and how BuyerBench uses judges for Pillar 2 reasoning quality
- [[multi-agent-eval]] — Evaluation of tool-using and multi-agent systems; agent traces as evaluation artifacts; trace-based metrics for BuyerBench
- [[reproducibility-in-benchmarks]] — Benchmark contamination, train-test leakage, static vs. dynamic benchmarks; how BuyerBench's variant design addresses these
- [[evaluation-metrics-taxonomy]] — Catalogue of capability, efficiency, robustness, and safety/alignment metrics mapped to BuyerBench's three pillars

---

## Pillar 1 — Agent Capability (`pillar1-capability/`)

- [[procurement-ai-survey]] — Survey of SAP/Joule/Ariba, Coupa, Ivalua IVA, and Zip; capability claims, evaluation gaps, and why no third-party benchmark currently exists
- [[workflow-completion-metrics]] — Multi-step task decomposition, partial credit scoring, tool call accuracy, and action economy for procurement workflows
- [[supplier-selection-literature]] — AHP, TOPSIS, VIKOR, DEA; how MCDM methods define the ground-truth optimal supplier choice in BuyerBench scenarios
- [[cli-agents-landscape]] — Profile of Claude Code CLI, Codex CLI, and Gemini CLI as BuyerBench evaluation targets; comparison table of tool use, MCP, skills, and procurement relevance
- [[PILLAR1-SUMMARY]] — Synthesis: 5 key findings and their scenario design implications; gaps BuyerBench fills; recommended next steps

---

## Pillar 2 — Economic Decision Quality (`pillar2-economics/`)

- [[behavioral-economics-foundations]] — Prospect theory, loss aversion, anchoring, framing, status quo bias, sunk cost fallacy, decoy effect; BuyerBench scenario designs for each
- [[bias-in-llm-agents]] — Survey (2023–2025) of empirically documented vs. theoretical cognitive biases in LLMs; evidence classification per bias category
- [[economic-rationality-metrics]] — Optimality gap, EV regret, WARP, bias susceptibility index (BSI), controlled variant methodology
- [[negotiation-agent-economics]] — NegMAS, GeniusWeb/Genius, ANAC competition results; Nash Bargaining Solution; LLM negotiation rationality findings; procurement-specific rationality requirements
- [[PILLAR2-SUMMARY]] — Synthesis: 4 key findings; eight-bias taxonomy with primary sources and LLM evidence; controlled variant design methodology

---

## Pillar 3 — Security, Compliance, and Market Readiness (`pillar3-security/`)

- [[payment-security-standards]] — PCI DSS 4.0.1, EMV 3DS v2.3.1 (incl. 3RI for agent flows), EMV Payment Tokenisation, PCI 3DS SDK Standard; testable agent behaviors per standard
- [[ai-governance-standards]] — ISO/IEC 42001:2023 (AI management system), ISO/IEC 23894:2023 (AI risk management), NIST AI RMF 1.0; mapped to BuyerBench audit and governance requirements
- [[agentic-commerce-protocols]] — AP2, UCP, and ACP in depth; governance models, spec maturity, security profiles, interoperability positioning; testable behaviors per protocol
- [[network-initiatives]] — Visa Intelligent Commerce + Trusted Agent Protocol (TAP), Mastercard Agent Pay; authentication patterns, tokenization flows, trust boundary requirements
- [[network-rules-amex-unionpay-jcb]] — American Express (DSOP, SafeKey, closed-loop model, dispute lifecycle), UnionPay International (PBOC, PIPL, Discover partnership, IFR co-badging), JCB (DSP, J/Secure, Discover access, APPI); cross-network comparison table
- [[fraud-patterns-and-attacks]] — Catalogue of six attack categories (prompt injection, economic manipulation, refund/chargeback, credential theft, protocol abuse, authorization bypass); BuyerBench scenario mappings
- [[regulatory-frameworks-usa]] — GLBA Safeguards Rule (2023), EFTA/Regulation E, Regulation Z, Durbin Amendment, BSA/AML/OFAC, FedNow, 21-state privacy law table; testable agent behaviors per law
- [[regulatory-frameworks-eu]] — GDPR (incl. extraterritorial scope, breach notification, international transfers), UK GDPR, NIS2, IFR interchange caps, AMLD6/AMLA, SEPA Instant (mandatory Oct 2024, VoP), eIDAS 2.0/EUDI Wallet
- [[regulatory-frameworks-brazil]] — LGPD (10 lawful bases, ANPD, cross-border transfers), PIX (DICT key resolution, nighttime limits, Pix Garantido), Open Finance Brazil (4 phases, FAPI), Brazilian AML (COAF, BACEN Circular 3.978, PEP screening)
- [[regulatory-cross-jurisdiction-matrix]] — Master compliance matrix: 65+ regulations × scenario category × test type × scoring × existing scenario ID; gap analysis; priority new scenarios; jurisdiction clustering for variant design
- [[PILLAR3-SUMMARY]] — Synthesis: 5 key findings; scenario category taxonomy; compliance gap analysis; Security Degradation Score methodology

---

## Cross-Pillar Synthesis

- [[RESEARCH-GAPS]] — Top 7 research gaps across all three pillars that BuyerBench addresses; cross-gap summary table mapping gaps to metrics; direct source material for paper Introduction and Related Work

---

## Paper (`paper/`)

- [[buyerbench-paper]] — Main research paper (IMRaD structure): Abstract, Introduction, Related Work, Methodology, Results (TBD), Discussion, Conclusion
- [[PAPER-STATUS]] — Section-by-section writing status tracker (Draft/Review/Done)
- [[FIGURE-PLAN]] — Planned figures with descriptions, source notebook cells, and placement
- `references.bib` — BibTeX references for all cited papers (Kahneman & Tversky, AgentBench, GAIA, HELM, PCI DSS, EMV 3DS, ISO 42001, AP2/UCP/ACP, etc.)
