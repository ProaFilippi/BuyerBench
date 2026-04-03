---
type: research
title: Evaluation Metrics Taxonomy for AI Agent Benchmarks
created: 2026-04-03
tags:
  - metrics
  - evaluation
  - taxonomy
related:
  - '[[agent-evaluation-overview]]'
  - '[[BuyerBench-Pillar-Mapping]]'
  - '[[reproducibility-in-benchmarks]]'
  - '[[llm-as-judge]]'
---

# Evaluation Metrics Taxonomy for AI Agent Benchmarks

## Overview

AI agent evaluation metrics fall into four families: **capability**, **efficiency**, **robustness**, and **safety/alignment**. Each family measures a different aspect of agent behavior. BuyerBench's three pillars map cleanly onto this taxonomy, with each pillar drawing primarily from one or two families.

---

## 1. Capability Metrics

Capability metrics measure whether the agent can correctly complete the intended task.

### Task Completion Rate (TCR)
The fraction of scenarios where the agent fully achieves the stated objective.
- Binary per scenario: did the agent produce a valid final decision?
- Averaged across a scenario suite for an overall TCR

### Workflow Accuracy
In multi-step tasks, were the individual steps (tool calls, sub-decisions) correct, even if the final outcome succeeded?
- Useful for distinguishing agents that "got lucky" from agents that followed the correct procedure

### Partial Credit Score
For long-horizon tasks, a fraction-of-steps-correct score rather than binary success/failure.
- Essential for BuyerBench Pillar 1: an agent that correctly identifies the top-3 suppliers but fails to execute the purchase order deserves partial credit

### Tool Call Accuracy
Correct tool invoked with correct arguments, in the correct sequence. See [[multi-agent-eval]] for trace-based measurement.

### Constraint Satisfaction Rate
Fraction of scenarios where all operational constraints (budget ceiling, approved vendor list, delivery deadline) were respected.

---

## 2. Efficiency Metrics

Efficiency metrics measure the cost of achieving the task — time, compute, and money.

### Step Count / Action Economy
How many tool calls or reasoning steps did the agent require to reach the correct answer? Fewer steps (with equal accuracy) is better.

### Latency
Wall-clock time from scenario input to final decision. Relevant for deployment contexts where procurement decisions are time-sensitive.

### Token Cost
Total input + output tokens consumed across the trajectory. Directly maps to API cost in deployed systems.

### Tool Redundancy Rate
How often did the agent call the same tool with the same arguments more than once (wasted steps)?

---

## 3. Robustness Metrics

Robustness metrics measure consistency and resistance to perturbation.

### Variant Consistency Rate
The core BuyerBench Pillar 2 metric: across economically-equivalent scenario variants with different framings, does the agent make the same decision?
- Inconsistency = susceptibility to the tested bias (anchoring, framing, decoy, etc.)

### Expected Value Regret
The gap between the agent's chosen option's economic value and the optimal option's value.
- EV Regret = EV(optimal) − EV(agent_choice)
- Normalized regret = (EV_regret) / EV(optimal), expressed as a percentage

### Optimality Gap
Similar to EV regret but measured against a known optimal decision (e.g., from a linear program solution or domain expert).

### Bias Susceptibility Index (BSI)
For each bias category (anchoring, framing, decoy, sunk cost, etc.), the fraction of variant pairs where the agent's decision changed due to the manipulated cue.
- BSI = 0: fully consistent (bias-resistant)
- BSI = 1: always susceptible

### Preference Consistency (Transitivity)
If the agent prefers A > B and B > C, does it also prefer A > C? Violations indicate irrational preference ordering — a classical economic rationality test.

---

## 4. Safety and Alignment Metrics

Safety metrics measure whether the agent respects policy, avoids harm, and behaves as authorized.

### Compliance Adherence Rate
Fraction of scenarios where the agent followed all specified compliance rules (payment sequencing, vendor approval, spending limits).

### Security Violation Rate
Frequency of attempted or completed security violations (bypassing auth, using unauthorized payment methods, accessing forbidden suppliers).

### Fraud Detection Rate
In scenarios containing embedded fraud signals (anomalous pricing, identity spoofing, unauthorized transaction patterns), what fraction did the agent correctly identify and reject?

### False Positive Rate (Fraud)
How often did the agent flag legitimate transactions as fraudulent? The trade-off between fraud detection recall and false positive rate is a key operating characteristic.

### Escalation Appropriate Rate
When a scenario is beyond the agent's authorized scope, does it correctly escalate rather than proceed autonomously?

---

## BuyerBench Pillar Mapping

| Metric Family | Primary Pillar | Specific Metrics |
|---------------|---------------|-----------------|
| Capability | Pillar 1 | TCR, workflow accuracy, partial credit, tool call accuracy, constraint satisfaction |
| Efficiency | Pillar 1 (secondary) | Step count, token cost, latency |
| Robustness | Pillar 2 | Variant consistency rate, EV regret, optimality gap, bias susceptibility index, preference transitivity |
| Safety/Alignment | Pillar 3 | Compliance adherence, security violation rate, fraud detection rate, false positive rate, escalation rate |

Note: some metrics span pillars. For example, constraint satisfaction (capability family) is also relevant to Pillar 3 compliance.

---

## Reporting Guidance

BuyerBench produces a **multi-dimensional evaluation profile** — metrics are not collapsed into a single score. The recommended reporting structure is:

```
Agent: <name>
Scenario suite: <version>

Pillar 1 — Capability:
  Task Completion Rate: X%
  Workflow Accuracy: Y%
  Constraint Satisfaction: Z%

Pillar 2 — Economic Decision Quality:
  Variant Consistency Rate: X%
  Mean EV Regret: Y%
  Bias Susceptibility by Category:
    Anchoring: X%
    Framing: Y%
    Decoy: Z%
    ...

Pillar 3 — Security/Compliance:
  Compliance Adherence Rate: X%
  Security Violation Rate: Y%
  Fraud Detection Recall: Z%
  Fraud False Positive Rate: W%
```

---

## See Also

- [[agent-evaluation-overview]] — benchmark design principles
- [[llm-as-judge]] — scoring approaches for open-ended outputs
- [[multi-agent-eval]] — trace-based metrics
- [[reproducibility-in-benchmarks]] — how robustness metrics support contamination resistance
