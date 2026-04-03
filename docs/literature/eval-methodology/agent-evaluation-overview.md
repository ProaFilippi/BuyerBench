---
type: research
title: AI Agent Evaluation — Overview and Taxonomy
created: 2026-04-03
tags:
  - evaluation
  - benchmarking
  - agents
  - methodology
related:
  - '[[llm-as-judge]]'
  - '[[multi-agent-eval]]'
  - '[[reproducibility-in-benchmarks]]'
  - '[[evaluation-metrics-taxonomy]]'
---

# AI Agent Evaluation — Overview and Taxonomy

## What Makes a Good Agent Benchmark

Evaluating AI agents is substantially harder than evaluating language model outputs in isolation. Agents act across multi-step trajectories, use tools, modify environment state, and must be assessed both on *outcome quality* and *process quality*. The key properties of a well-designed agent benchmark are:

### 1. Coverage
A benchmark should span the realistic distribution of tasks an agent will face in deployment. Coverage includes:
- **Task type diversity**: instruction following, multi-step planning, tool use, constraint satisfaction
- **Difficulty gradient**: easy (single-step) through complex (long-horizon, multi-tool, adversarial)
- **Domain breadth**: general-purpose benchmarks (GAIA, BIG-Bench) vs. domain-specific (SWE-bench for software, BuyerBench for procurement)

### 2. Reproducibility
Scenarios must be deterministic enough to allow controlled comparisons across agents and over time. Key challenges include benchmark contamination (training data overlap), LLM non-determinism, and environment state drift. See [[reproducibility-in-benchmarks]].

### 3. Adversarial Robustness
Benchmarks that test only the "happy path" underestimate failure modes. Robust benchmarks include:
- Adversarial inputs (manipulated prompts, misleading context)
- Controlled perturbation variants (same economics, different framing)
- Edge cases and constraint violations

### 4. Multi-Dimensional Scoring
A single aggregate score obscures critical tradeoffs. Well-designed benchmarks report:
- Capability metrics (task completion rate, accuracy)
- Efficiency metrics (steps, latency, cost)
- Robustness metrics (variance across variants)
- Safety/alignment metrics (policy violation rate)

BuyerBench follows this principle explicitly: results are reported per pillar (capability, economic decision quality, security/compliance), not as a single score.

---

## Key Benchmarks and Their Approaches

### AgentBench (Liu et al., 2023)
Evaluates LLMs as agents across 8 diverse environments: web browsing, database query, operating system tasks, knowledge graph traversal, card games, lateral thinking puzzles, and more.
- **Approach**: Environment-specific reward functions; agent traces captured; reproducible environments via Docker
- **Strength**: breadth and task realism
- **Gap**: limited domain-specific evaluation (e.g., procurement, economics)

### GAIA (Mialon et al., 2023)
General AI Assistant benchmark requiring real-world tool use (web search, file reading, arithmetic). Questions require multi-step reasoning and factual grounding.
- **Approach**: Factual correctness grading; human performance baseline (96%); GPT-4 baselines (~15%)
- **Strength**: real-world task grounding; reveals capability gaps
- **Gap**: primarily factual/retrieval tasks; no behavioral bias or compliance evaluation

### WebArena (Zhou et al., 2023)
Realistic web browser agent evaluation across e-commerce, social forums, project management, and mapping sites. Agents operate in sandboxed replicas of real sites.
- **Approach**: Functional correctness (did the agent complete the task in the web environment?); diverse site types
- **Strength**: ecological validity for web-based workflows
- **Gap**: static website snapshots; limited to UI-level interactions

### SWE-bench (Jimenez et al., 2023)
Software engineering tasks derived from real GitHub issues. Agents must locate the bug, write a patch, and pass test suites.
- **Approach**: Unit test pass rate as proxy for correctness; real codebases
- **Strength**: objectively gradable via automated testing; real-world relevance
- **Gap**: single-domain (code); no multi-stakeholder or constraint-satisfaction evaluation

### HELM (Liang et al., 2022)
Holistic Evaluation of Language Models: standardized evaluation across 42 scenarios and 7 metric classes (accuracy, calibration, robustness, fairness, bias, toxicity, efficiency).
- **Approach**: Multi-metric profiling; scenario-level and aggregate reporting
- **Strength**: most comprehensive multi-metric framework pre-2024
- **Gap**: primarily static LM evaluation; not designed for agentic/tool-using settings

### BIG-Bench (Srivastava et al., 2022)
A collaborative benchmark of 204 tasks covering language, reasoning, coding, mathematics, and social understanding.
- **Approach**: Community-contributed tasks; human rater calibration; BIG-Bench Hard subset for chain-of-thought analysis
- **Strength**: diversity; global community contribution
- **Gap**: tasks are mostly single-turn; agentic settings not covered

---

## Gaps BuyerBench Is Positioned to Fill

| Gap | BuyerBench Response |
|-----|---------------------|
| No procurement/buyer-specific benchmark exists | Explicit buyer-agent task scenarios (supplier discovery, quote comparison, purchase execution) |
| Existing benchmarks do not test behavioral biases | Pillar 2: controlled framing variants measuring anchoring, decoy effects, loss aversion, etc. |
| Security and compliance are absent from agent benchmarks | Pillar 3: explicit fraud detection, PCI DSS alignment, payment protocol scenarios |
| Single-score aggregation obscures tradeoffs | Multi-pillar reporting (capability, economic rationality, security) |
| Static benchmarks are contaminated by training data | Controlled variant design allows fresh scenario generation; economic structure is parameterizable |
| Capability benchmarks ignore economic optimality | Pillar 2 measures optimality gap and expected value regret alongside task completion |

---

## See Also

- [[llm-as-judge]] — scoring approaches for subjective agent outputs
- [[multi-agent-eval]] — evaluation in tool-using and multi-agent settings
- [[reproducibility-in-benchmarks]] — contamination, leakage, and dynamic benchmarks
- [[evaluation-metrics-taxonomy]] — catalogue of metric types mapped to BuyerBench pillars
