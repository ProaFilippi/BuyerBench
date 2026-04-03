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

*Documents to be added in Phase 03 (BUYERBENCH-03).*

---

## Paper (`paper/`)

*Documents to be added in later phases.*
