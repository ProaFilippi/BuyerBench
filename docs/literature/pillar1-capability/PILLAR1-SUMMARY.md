---
type: analysis
title: Pillar 1 Capability — Literature Synthesis and Scenario Design Implications
created: 2026-04-03
tags:
  - pillar1
  - summary
related:
  - '[[procurement-ai-survey]]'
  - '[[workflow-completion-metrics]]'
  - '[[supplier-selection-literature]]'
  - '[[cli-agents-landscape]]'
  - '[[evaluation-metrics-taxonomy]]'
  - '[[PILLAR2-SUMMARY]]'
  - '[[PILLAR3-SUMMARY]]'
---

# Pillar 1 Capability — Literature Synthesis and Scenario Design Implications

## Purpose

This document synthesizes the most important findings from the Pillar 1 literature review and translates them into concrete implications for BuyerBench scenario design, evaluation methodology, and positioning.

---

## Finding 1: No Third-Party Procurement AI Benchmark Exists

The four major enterprise procurement AI systems (SAP/Joule/Ariba, Coupa, Ivalua IVA, Zip) all make capability claims in marketing materials with no publicly available third-party evaluation. See [[procurement-ai-survey]].

**Gap BuyerBench fills**: BuyerBench is, to our knowledge, the first open-source benchmark specifically designed to evaluate AI buyer agents on procurement tasks. The absence of existing benchmarks is a direct market opportunity and a research contribution in its own right.

**Scenario design implication**: BuyerBench scenarios should map to the canonical procurement workflow tasks that vendors claim capability for — supplier discovery, RFx evaluation, quote comparison, purchase order generation — so that results are directly interpretable against vendor claims.

---

## Finding 2: MCDM Literature Provides a Defensible Ground-Truth Oracle

The supplier selection literature (AHP, TOPSIS, VIKOR) provides well-validated mathematical frameworks for defining "optimal" supplier choice given a set of criteria and weights. See [[supplier-selection-literature]].

**Gap BuyerBench fills**: By grounding "correct answer" in TOPSIS-ranked supplier evaluation matrices, BuyerBench avoids the "who decides what's correct?" problem that plagues many open-ended agent benchmarks. The optimal choice is computable, auditable, and not dependent on human judgment.

**Scenario design implication**: Each Pillar 1 scenario should include a normalized supplier attribute matrix with declared criterion weights. The TOPSIS-ranked result defines the ground truth. Agents are scored by their selection's rank position in the TOPSIS ordering (not just exact match, which would be too strict for multi-attribute problems with near-ties).

---

## Finding 3: Multi-Step Workflow Completion Requires Partial Credit Scoring

Long procurement workflows (5+ steps) almost never succeed or fail completely. Binary success/failure scoring wastes signal and penalizes agents for single-step failures even when 80% of the workflow was correct. See [[workflow-completion-metrics]].

**Gap BuyerBench fills**: BuyerBench's step-weighted partial credit scoring provides finer-grained capability assessment than binary benchmarks like SWE-bench or WebArena.

**Scenario design implication**: Define explicit step decompositions for every Pillar 1 scenario. Assign step weights reflecting both difficulty and downstream impact (errors in requirements interpretation cascade; errors in documentation do not). Tool call sequence accuracy should be scored separately from outcome accuracy.

---

## Finding 4: CLI Agent Tool-Use Capabilities Are Sufficient for Procurement Workflows

Claude Code CLI, Codex CLI, and Gemini CLI all have the fundamental capabilities needed for procurement workflow execution: file I/O, shell execution, and (for Claude Code and Gemini CLI) MCP support for external API integration. See [[cli-agents-landscape]].

**Gap BuyerBench fills**: No existing benchmark exposes these CLI agents to procurement domain tasks. BuyerBench provides the evaluation harness that translates "can this agent edit code?" into "can this agent evaluate supplier quotes and enforce budget constraints?"

**Scenario design implication**: BuyerBench scenarios should be deliverable as structured context files (JSON or Markdown) plus tool stubs (Python functions or MCP servers), making them accessible to all three CLI agents without requiring agent-specific customization beyond the adapter layer.

---

## Finding 5: The Agent Trace Is as Informative as the Outcome

Multi-agent evaluation literature (ReAct, ToolBench) demonstrates that *how* an agent reaches a decision is evaluation-relevant — not just *what* decision it reaches. An agent that selects the correct supplier by reasoning correctly is more reliable than one that selects correctly by coincidence. See [[multi-agent-eval]].

**Gap BuyerBench fills**: BuyerBench captures full agent trajectories (tool calls, reasoning excerpts, constraint checks) enabling trace-level evaluation. This is particularly important for Pillar 2 (behavioral bias detection requires inspecting whether biased cues appeared in the reasoning trace) and Pillar 3 (compliance evaluation requires detecting policy violations in the action trace, not just the final output).

**Scenario design implication**: The BuyerBench harness must capture and store the full agent trace for every evaluation run. Evaluators should have access to both the final decision and the trace when computing scores.

---

## Key Gaps That BuyerBench Is Positioned to Fill

| Gap | Evidence | BuyerBench Response |
|-----|----------|---------------------|
| No open-source procurement agent benchmark | [[procurement-ai-survey]]: zero public benchmarks found | BuyerBench is the first |
| No adversarial or bias testing for procurement AI | [[procurement-ai-survey]]: vendors don't test this | Pillar 2 behavioral bias scenarios |
| Binary outcome scoring misses partial workflows | [[workflow-completion-metrics]]: ToolBench partial credit | Step-weighted partial credit scoring |
| No formal "correct answer" definition for supplier selection | [[supplier-selection-literature]]: MCDM methods available | TOPSIS-grounded ground truth |
| CLI agents not evaluated on procurement tasks | [[cli-agents-landscape]]: capability exists but untested | BuyerBench provides the missing harness |

---

## Recommended Next Steps (for Phase 03 and Beyond)

1. **Build scenario suite**: Implement TOPSIS scoring oracle as a Python utility in BuyerBench; use it to define ground-truth answers for all Pillar 1 scenarios
2. **Implement step decompositions**: Define canonical procurement workflow step sequences; implement step-level scoring in the Pillar 1 evaluator
3. **Build CLI agent adapters**: Implement thin adapter classes for Claude Code, Codex CLI, and Gemini CLI that translate scenario inputs and capture traces
4. **Run pilot evaluation**: Run 3–5 scenarios against all three CLI agents; validate scoring methodology; identify systematic capability gaps

---

## See Also

- [[procurement-ai-survey]] — enterprise procurement AI landscape
- [[workflow-completion-metrics]] — step decomposition and partial credit methodology
- [[supplier-selection-literature]] — MCDM ground-truth oracle
- [[cli-agents-landscape]] — CLI agent capabilities and comparison
- [[evaluation-metrics-taxonomy]] — full metrics catalogue
