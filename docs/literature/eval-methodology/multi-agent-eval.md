---
type: research
title: Evaluation of Multi-Agent and Tool-Using Agents
created: 2026-04-03
tags:
  - evaluation
  - multi-agent
  - tool-use
related:
  - '[[agent-evaluation-overview]]'
  - '[[llm-as-judge]]'
  - '[[evaluation-metrics-taxonomy]]'
---

# Evaluation of Multi-Agent and Tool-Using Agents

## The Shift from Static to Agentic Evaluation

Traditional LLM benchmarks evaluate single-turn input–output mappings. Agentic evaluation must handle:
- **Trajectories**: sequences of steps, tool calls, and observations
- **Environment state**: the agent's actions modify the world, creating new observations
- **Non-determinism**: same agent, same task, different execution paths
- **Tool composition**: the agent's capability depends on which tools are available and how it uses them

These differences require purpose-built evaluation frameworks that can replay, inspect, and score agent traces.

---

## Tool-Using Agent Evaluation

### ToolBench / ToolLLM (Qin et al., 2023)
A benchmark of 16,000+ real-world APIs and instruction-following tasks. Evaluates agents on whether they can select the correct tool, form valid tool calls, and compose multi-tool pipelines.
- **Key metric**: Pass Rate (task succeeded end-to-end), Win Rate (quality comparison)
- **Relevance to BuyerBench**: directly analogous — BuyerBench agents must invoke supplier discovery, quote comparison, and purchase execution tools in the correct order

### ReAct (Yao et al., 2022)
Interleaves reasoning traces with action calls. Evaluation is primarily task-outcome based, but the trace structure enables inspection of *why* the agent took each action.
- **Relevance to BuyerBench**: reasoning traces are first-class evaluation artifacts in BuyerBench (bias detection requires inspecting *why* a biased choice was made, not just that it was made)

### API-Bank (Li et al., 2023)
Tests LLM tool-calling in a controlled API sandbox. Distinguishes between retrieving, using, and chaining APIs.

---

## Agent Traces as Evaluation Artifacts

A crucial insight from recent work: **the trajectory is as important as the outcome** for evaluating agent quality. Two agents that reach the same final answer but via different paths may have very different reliability, cost, and bias profiles.

BuyerBench captures the following trace elements:
- **Tool calls**: which tools were invoked, in what order, with what arguments
- **Decision points**: at each choice moment, what alternatives were considered and why
- **Reasoning excerpts**: the agent's stated justification for key decisions
- **Violation events**: any moment the agent considered or executed a policy-violating action

### Trace-Based Metrics
| Metric | What It Measures | BuyerBench Pillar |
|--------|-----------------|-------------------|
| Tool call accuracy | Correct tool selected for each sub-task | Pillar 1 |
| Tool call order correctness | Steps executed in the valid workflow sequence | Pillar 1 |
| Reasoning consistency | Same choice made across equivalent framing variants | Pillar 2 |
| Bias-implication trace | Whether the agent's stated reasoning references a biased cue | Pillar 2 |
| Policy check invocation | Whether the agent queried compliance rules before acting | Pillar 3 |
| Violation attempt rate | How often the agent attempted a policy-violating action | Pillar 3 |

---

## Multi-Agent System Evaluation

### Challenges
Multi-agent settings (orchestrator + sub-agents) introduce attribution problems: when a task fails, which agent is responsible? Evaluation must handle:
- **Coordination overhead**: inter-agent communication failures
- **Cascading errors**: sub-agent mistakes propagating to orchestrator
- **Role clarity**: whether each agent respects its designated scope

### Relevant Work
- **AutoGen** (Microsoft, 2023): framework for multi-agent conversation; evaluation done via task success, but agent-specific attribution is manual
- **MetaGPT** (Hong et al., 2023): software engineering multi-agent system; evaluation tracks role adherence and code quality
- **AgentVerse** (Chen et al., 2023): simulates multi-agent task completion; includes inter-agent communication quality metrics

### BuyerBench Stance
BuyerBench Phase 1 focuses on **single-agent evaluation** — one agent receives a scenario and is evaluated on its response. This avoids multi-agent attribution complexity. Future phases may test orchestrator agents that delegate to specialized sub-agents (e.g., a procurement orchestrator calling supplier-search and policy-check sub-agents), at which point the trace attribution framework will need to be extended.

---

## Key Evaluation Design Principles for Agentic Settings

1. **Deterministic environments**: sandbox or replay environments should produce identical states for the same agent action, enabling fair comparison
2. **Partial credit**: long-horizon tasks rarely succeed or fail completely; partial credit for correct sub-task completion is essential
3. **Trace replay**: the ability to replay an agent's trajectory for post-hoc inspection
4. **Counterfactual variants**: same task, manipulated environment — the core technique for bias and robustness testing in BuyerBench
5. **Separation of capability and behavior**: an agent can complete a task (high capability) while violating policy (poor compliance); these dimensions should not be conflated

---

## See Also

- [[agent-evaluation-overview]] — broader benchmark taxonomy
- [[evaluation-metrics-taxonomy]] — metric catalogue across all pillars
- [[workflow-completion-metrics]] — Pillar 1-specific metrics for procurement workflow execution
