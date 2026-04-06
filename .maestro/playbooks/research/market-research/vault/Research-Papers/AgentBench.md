---
type: research-paper
title: "AgentBench: Evaluating LLMs as Agents — Multi-Environment Agent Benchmark (ICLR 2024)"
created: 2026-04-05
tags:
  - benchmark
  - multi-task
  - llm-agents
  - iclr-2024
  - evaluation
  - operating-system
  - web-agent
  - decision-making
related:
  - '[[WebArena]]'
  - '[[WebShop]]'
  - '[[LLM-Agent-Benchmarking-Survey]]'
  - '[[ACES-AI-Agent-Buying]]'
  - '[[INDEX]]'
---

# AgentBench

> The first comprehensive multi-environment benchmark for evaluating LLMs as interactive agents — testing 29 models across 8 distinct task environments with interactive multi-turn evaluation, revealing a dramatic performance gap between commercial and open-source models

## Citation

**Full title:** "AgentBench: Evaluating LLMs as Agents"

| Field | Value |
|-------|-------|
| Authors | Xiao Liu, Hao Yu, Hanchen Zhang, Yifan Xu, Xuanyu Lei, Hanyu Lai, Yu Gu, Hangliang Ding, Kaiwen Men, Kejuan Yang, Shudan Zhang, Xiang Deng, Aohan Zeng, Zhengxiao Du, Chenhui Zhang, Sheng Shen, Tianjun Zhang, Yu Su, Huimin Chen, Guanyu Feng, Yuxiao Dong, Jie Tang |
| arXiv ID | [2308.03688](https://arxiv.org/abs/2308.03688) |
| Submitted | August 7, 2023 |
| Venue | **ICLR 2024** (International Conference on Learning Representations) |
| Subject areas | cs.AI, cs.CL |
| Institutional affiliation | Tsinghua University (THUDM group), with collaborators at Ohio State University |
| GitHub | [THUDM/AgentBench](https://github.com/THUDM/AgentBench) |

## Abstract Summary

AgentBench addresses a gap in LLM evaluation: while standard benchmarks test knowledge or single-step reasoning, they do not measure whether models can act as *agents* — i.e., engage in multi-turn, interactive decision-making under real-world constraints. The paper introduces 8 task environments spanning code-grounded, game-grounded, and web-grounded scenarios, and evaluates 29 commercial and open-source LLMs under identical conditions. Its core finding: frontier commercial models (GPT-4 at the time) outperform the best open-source 70B models by a factor of ~4× on the composite Overall score, and most open-source models score near zero — revealing that "agentification" is not a free capability improvement but a qualitatively distinct capability frontier.

> **BuyerBench relevance (Pillar 1):** AgentBench is the primary architectural precedent for BuyerBench's multi-task harness design. Its pattern of wrapping diverse environments under a unified evaluation interface — with standardized agent I/O, multi-turn interaction, and per-environment metrics — is the direct template for BuyerBench's three-pillar scenario runner. The web-grounded environments (Web Shopping, Web Browsing) are the precursors of BuyerBench's Pillar 1 supplier-discovery and quote-comparison tasks.

> **BuyerBench relevance (Framework Design):** AgentBench's overall weighted scoring methodology — aggregating sub-environment scores into a composite ranking — provides a worked example of the aggregation trade-off BuyerBench must resolve. BuyerBench intentionally rejects single-score aggregation in favor of per-pillar profiles, but AgentBench's leaderboard design shows what is gained (comparability) and lost (masking weakness in individual environments) by aggregation.

## Task Environments

AgentBench defines 8 environments, grouped into three categories:

### Code-Grounded Environments

| Environment | Abbreviation | Task Description | Metric |
|-------------|-------------|------------------|--------|
| Operating System | OS | Execute bash commands to complete file system and process management tasks in an interactive shell | Task success rate |
| Database | DB | Query and manipulate a SQL database to answer questions or produce requested data | Task success rate |
| Knowledge Graph | KG | Navigate a Freebase-style knowledge graph to answer multi-hop factual questions via SPARQL-like queries | F1 / exact match |

### Game-Grounded Environments

| Environment | Abbreviation | Task Description | Metric |
|-------------|-------------|------------------|--------|
| Digital Card Game | DCG | Play a Pokemon-style collectible card game against a rule-based opponent, requiring strategic decision-making across turns | Win rate |
| Lateral Thinking Puzzles | LTP | Solve "situation puzzles" via yes/no Q&A — requires hypothesis generation and convergent reasoning | Scoring rubric |
| ALFWorld (House-Holding) | HH | Navigate and manipulate objects in a simulated household environment (text-based) to complete specified tasks | Task success rate |

### Web-Grounded Environments

| Environment | Abbreviation | Task Description | Metric |
|-------------|-------------|------------------|--------|
| Web Shopping | WS | Browse a product catalog, interpret a user's shopping instruction, and purchase the best-matching product | Score (0–1) combining attribute matching and purchase action |
| Web Browsing | WB | Complete open-domain web navigation tasks on a real (sandboxed) browser interface — search, click, form-fill | Task success rate |

> **BuyerBench relevance (Pillar 1):** The Web Shopping (WS) environment is the direct predecessor of BuyerBench Pillar 1 scenarios. Its scoring approach — rewarding both product-attribute match quality *and* correct purchase action — directly maps to BuyerBench's capability metrics: task completion rate × workflow accuracy. The Web Browsing (WB) environment validates the feasibility of testing agents on realistic browser interfaces, which BuyerBench can adopt for supplier portal simulation.

## Scoring Methodology

### Per-Environment Metrics

Each environment uses the most appropriate task-completion metric:
- **Binary success rate** (OS, DB, WB, HH): Did the agent complete the terminal goal?
- **Graded reward** (WS): Score in [0, 1] based on attribute match quality and purchase correctness
- **Win rate** (DCG): Head-to-head performance against a rule-based bot
- **F1 / partial match** (KG): Information-retrieval quality for multi-hop answers

### Overall Score

The composite **Overall** score is a weighted average across all 8 environments — weights approximate relative task difficulty and scope. This enables leaderboard ranking across diverse models.

### Evaluation Protocol

- **Multi-turn interactive sessions**: Each task involves a dialogue between the LLM agent and the task environment, not a single-prompt query
- **Standardized I/O format**: Environments return observations; agents return actions (bash commands, SQL queries, click/navigate instructions, etc.)
- **Instruction following test**: Agents receive task descriptions in natural language and must translate these into correct action sequences
- **No fine-tuning required**: All models evaluated in prompt-only mode (few-shot or zero-shot with system prompt)

## Key Results

### Overall Score Comparison (29 Models)

| Model | Overall Score | Category |
|-------|--------------|----------|
| GPT-4 (OpenAI) | ~4.01 | Commercial API |
| GPT-3.5-Turbo | ~1.41 | Commercial API |
| Claude-1 (Anthropic) | ~0.97 | Commercial API |
| Best open-source ≤70B | < 1.00 | Open-source |
| Typical open-source | ~0.00–0.50 | Open-source |

**Key finding:** GPT-4 scores ~4× higher than the best open-source 70B models tested, and the vast majority of open-source models tested score close to zero — despite many of them performing competitively on single-turn benchmarks (MMLU, GSM8K, etc.).

### Performance by Environment Type

- **Code-grounded tasks** (OS, DB, KG): Highest absolute scores and sharpest commercial/OSS gap — instruction following and multi-turn reasoning on structured tasks heavily favors large commercial models
- **Game-grounded tasks** (DCG, LTP, HH): All models score lower; GPT-4's margin narrows slightly but remains dominant
- **Web-grounded tasks** (WS, WB): Moderate scores for top models; these tasks resemble the real-world web browsing use case closest to agentic commerce

### Root-Cause Analysis

The paper identifies three primary obstacles for LLM agents:
1. **Poor long-term reasoning**: Models lose coherence across many turns; context management degrades performance on tasks requiring 10+ steps
2. **Weak decision-making under uncertainty**: Models exhibit overconfidence, fail to backtrack after errors, and do not explore alternatives
3. **Instruction following failures**: Especially for structured-output requirements (JSON, specific command syntax) — models generate plausible but syntactically incorrect actions

## Lessons for Multi-Pillar Benchmark Design

### 1. Separate Environment-Level Metrics from Aggregate Scores

AgentBench's decision to report per-environment scores *alongside* an Overall score allows diagnosis of model strengths and weaknesses. A model that scores 3.0 on OS but 0.1 on Web Browsing has a fundamentally different capability profile than one that scores 1.5 across the board. BuyerBench's three-pillar structure extends this principle: agents should be reported as a vector of pillar scores, not a single number.

### 2. Multi-Turn Interaction Is the Right Unit of Evaluation

Single-prompt benchmarks systematically overestimate agent capability. AgentBench validates that multi-turn, stateful interaction is necessary to expose the failure modes that matter for agentic deployment (context loss, error recovery, backtracking). All BuyerBench scenarios should be multi-turn tasks, not single-shot queries.

### 3. Standardize the Agent I/O Interface Early

AgentBench's hardest engineering challenge was defining a clean I/O interface that worked across 8 heterogeneous environments. BuyerBench faces the same challenge across 3 pillars and ~18 scenarios. AgentBench's solution — a thin JSON wrapper with `observation` and `action` fields — provides a viable template for BuyerBench's harness abstraction.

### 4. Include a Simple Baseline Environment

AgentBench's OS environment (bash commands in a sandboxed shell) is the simplest and highest-scoring environment, giving evaluators a "sanity check" floor. BuyerBench should include at least one straightforward Pillar 1 scenario that strong agents should score near-perfect on — to detect degenerate failure modes (connectivity issues, prompt format errors) vs. genuine reasoning failures.

### 5. Evaluate Both Commercial and Open-Source Models

The commercial/OSS gap in AgentBench was not predicted and was highly informative. BuyerBench should test at least one open-source model alongside commercial models to expose whether Pillar 2 and Pillar 3 behaviors generalize or are model-family-specific.

## BuyerBench Alignment

| BuyerBench Component | AgentBench Precedent |
|----------------------|---------------------|
| Pillar 1 — Supplier discovery tasks | Web Shopping (WS) + Web Browsing (WB) environments |
| Pillar 1 — Quote comparison workflow | Database (DB) environment — structured data querying |
| Pillar 2 — Multi-step reasoning under bias | Digital Card Game (DCG) — strategic multi-turn decisions |
| Pillar 3 — Policy enforcement tasks | Operating System (OS) — constraint-following in sandboxed environment |
| Harness architecture | AgentBench's unified multi-environment runner with per-environment metric modules |
| Leaderboard design | AgentBench Overall score + per-environment breakdown → BuyerBench per-pillar profile |
| Agent I/O interface | AgentBench's observation/action schema → BuyerBench's scenario input/output schema |

## Related Entities

- [[WebArena]] — Extends AgentBench's web-grounded approach to a full multi-website realistic web environment; WebArena's e-commerce domain (OneStopShop) builds directly on AgentBench's WS/WB task design
- [[WebShop]] — Foundational shopping benchmark that AgentBench's WS environment adapts; the original instruction-following product search + purchase task
- [[LLM-Agent-Benchmarking-Survey]] — 2025 KDD survey that taxonomizes AgentBench as the canonical multi-domain LLM agent benchmark and cites it as methodological foundation for evaluation dimension design
- [[ACES-AI-Agent-Buying]] — ACES's e-commerce focus narrows AgentBench's WS scope while adding causal RCT methodology AgentBench lacks; both assess buying capability but at different granularities
- [[WebShop]] — AgentBench's WS environment directly incorporates the WebShop task design; WebShop is thus a component of AgentBench rather than a successor

## Sources

1. [AgentBench arXiv abstract (2308.03688)](https://arxiv.org/abs/2308.03688) — Accessed 2026-04-05
2. [ICLR 2024 proceedings page](https://proceedings.iclr.cc/paper_files/paper/2024/hash/e9df36b21ff4ee211a8b71ee8b7e9f57-Abstract-Conference.html) — Accessed 2026-04-05
3. [THUDM/AgentBench GitHub repository](https://github.com/THUDM/AgentBench) — Accessed 2026-04-05
4. [OpenReview discussion thread (ICLR 2024)](https://openreview.net/forum?id=zAdUB0aCTQ) — Accessed 2026-04-05
5. [Emergent Mind summary](https://www.emergentmind.com/papers/2308.03688) — Accessed 2026-04-05

---
*Last updated: 2026-04-05*
