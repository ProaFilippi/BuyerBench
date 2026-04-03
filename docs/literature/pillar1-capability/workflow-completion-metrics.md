---
type: research
title: Workflow Completion Metrics for Agent Systems
created: 2026-04-03
tags:
  - pillar1
  - metrics
  - workflow
  - tool-use
related:
  - '[[evaluation-metrics-taxonomy]]'
  - '[[multi-agent-eval]]'
  - '[[procurement-ai-survey]]'
  - '[[PILLAR1-SUMMARY]]'
---

# Workflow Completion Metrics for Agent Systems

## Motivation

Procurement workflows are inherently multi-step: a buyer agent must (1) interpret requirements, (2) search and filter suppliers, (3) compare quotes against criteria, (4) select a supplier, and (5) generate or execute a purchase order. Evaluating only the final outcome (did the PO get created?) misses critical information about *how* the agent arrived there and *where* it would fail under slightly different inputs.

---

## Workflow Completion Rate (WCR)

The fraction of scenarios where the agent completes all required workflow steps in the correct order, producing a valid final output.

```
WCR = (scenarios fully completed) / (total scenarios)
```

**Binary WCR** treats success/failure as all-or-nothing — strict but easy to game by shallow last-step shortcuts.

**Weighted WCR** weights each scenario by difficulty (number of steps, number of constraints) so that harder workflows contribute more to the aggregate score.

---

## Multi-Step Task Decomposition

Long-horizon tasks must be decomposed into atomic steps for evaluation. BuyerBench defines a canonical procurement workflow:

```
Step 1: Requirements interpretation
  → Correctly extract: item category, quantity, budget ceiling, delivery deadline, approved vendor constraints

Step 2: Supplier search and filtering
  → Return at least K relevant suppliers; filter out non-compliant or out-of-budget suppliers

Step 3: Quote evaluation
  → Score each supplier on all relevant attributes (price, delivery, quality tier, compliance status)

Step 4: Optimal selection
  → Select the supplier that maximizes the objective function subject to constraints

Step 5: Decision documentation
  → Produce a rationale that references the comparison criteria and the selected supplier's advantages
```

Each step is independently evaluable. An agent that fails at Step 4 (wrong selection) but correctly completes Steps 1–3 deserves partial credit.

---

## Partial Credit Scoring

Partial credit is essential for long-horizon procurement tasks. The recommended approach:

### Step-Weighted Partial Credit
Assign weights to each workflow step based on difficulty and importance:

| Step | Weight | Rationale |
|------|--------|-----------|
| Requirements interpretation | 0.15 | Foundational; errors cascade |
| Supplier search & filtering | 0.20 | Determines candidate set quality |
| Quote evaluation | 0.30 | Core analytical task |
| Optimal selection | 0.25 | The decision that counts |
| Decision documentation | 0.10 | Audit and transparency |

Final score = Σ(step_weight × step_score) for completed steps.

### Threshold-Based Partial Credit
Give full credit for a step if it meets a defined quality threshold (e.g., "top supplier in the correct category was included in shortlist"), partial credit if partially correct, zero otherwise.

---

## Tool Call Accuracy

Measures whether the agent uses the correct tools (API calls, data lookups, calculators) with valid arguments at each step.

**Exact match**: the agent's tool call matches the expected tool and arguments exactly.  
**Functional match**: the agent's tool call is syntactically different but semantically equivalent (e.g., different query phrasing that retrieves the same supplier set).

For BuyerBench, **functional match is preferred** — procurement queries often have multiple valid formulations.

### Tool Call Sequence Accuracy
Evaluates the *ordering* of tool calls, not just individual calls. In procurement workflows, correct sequencing matters:
- A constraint check (is this vendor approved?) should precede a purchase execution call
- A budget validation should precede a PO submission

Sequence violations are flagged as potential compliance risks even if the final outcome is correct.

---

## Efficiency as a Secondary Capability Dimension

Beyond correctness, efficiency metrics measure how *well* the agent completes workflows:

### Action Economy Score
```
AES = (minimum_steps_required) / (steps_taken_by_agent)
AES ∈ (0, 1]; 1.0 = perfectly efficient
```

An agent that correctly finds the optimal supplier in 3 tool calls scores higher than one that reaches the same conclusion in 12 tool calls — especially relevant for deployed systems where token cost is real.

### Redundant Tool Call Rate
```
RTR = (duplicate_tool_calls) / (total_tool_calls)
```

High RTR suggests the agent is "thrashing" — re-querying data it already has — indicating poor state tracking.

---

## Relevance to Existing Benchmark Literature

| Benchmark | Task Type | Multi-Step | Partial Credit | Tool Trace |
|-----------|-----------|------------|----------------|------------|
| SWE-bench | Code repair | Yes | No (pass/fail via tests) | No |
| WebArena | Web navigation | Yes | No | Partial (action log) |
| ToolBench | API composition | Yes | Partial | Yes |
| BuyerBench | Procurement | Yes | Yes (step-weighted) | Yes |

BuyerBench extends the ToolBench model into the procurement domain, adding economic optimality assessment (Pillar 2) and compliance-aware tool sequencing (Pillar 3) as dimensions that ToolBench does not cover.

---

## See Also

- [[evaluation-metrics-taxonomy]] — full metrics catalogue
- [[multi-agent-eval]] — trace-based evaluation and step attribution
- [[procurement-ai-survey]] — how commercial systems currently claim capability
- [[PILLAR1-SUMMARY]] — synthesis of Pillar 1 findings
