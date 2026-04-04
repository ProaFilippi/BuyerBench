# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

BuyerBench is an open-source benchmark framework for evaluating AI buyer agents across three pillars:

1. **Pillar 1 — Agent Intelligence and Operational Capability**: Can the agent execute buyer workflows (supplier discovery, quote comparison, multi-step procurement tasks)?
2. **Pillar 2 — Economic Decision Quality and Behavioral Robustness**: Does the agent make economically rational decisions and resist behavioral biases (anchoring, framing, decoy effects, sunk cost, etc.)?
3. **Pillar 3 — Security, Compliance, and Market Readiness**: Does the agent follow payment security practices, fraud detection, and regulatory compliance?

## Commands

```bash
# Install package and dev dependencies
pip install -e ".[dev]"

# Preflight check — verify CLI tools, API keys, and MCP server availability
python -m buyerbench check

# Run the end-to-end demo (loads 3 scenarios, runs MockAgent, prints rich report)
python -m buyerbench demo

# Run the full benchmark suite against a named agent (all 18 scenarios)
python -m buyerbench run --agent <name>

# Run against a specific agent in a specific pillar only
python -m buyerbench run --agent claude-code-baseline --pillar 1

# Run against all configured agents (preflight-checks each before running)
python -m buyerbench run --agent all

# Dry-run: print serialized prompts without invoking the CLI agent
python -m buyerbench run --agent claude-code-baseline --dry-run

# Generate FULL-REPORT.json + FULL-REPORT.md from experiment result directory
python -m buyerbench report --experiment-dir results/experiments

# Generate all paper figures from the report (requires matplotlib + numpy)
python3 .maestro/playbooks/Working/generate_figures.py

# Run tests
pytest

# Run tests with coverage
pytest --cov=buyerbench --cov=evaluators --cov=harness --cov=agents

# Run a specific test module
pytest tests/test_evaluator_pillar3.py -v

# Available agent IDs for --agent flag:
#   mock-agent-v1            MockAgent (always available; no credentials required)
#   claude-code-baseline     Claude Code CLI, prompt-only mode
#   claude-code-skills       Claude Code CLI + BuyerBench skill definitions
#   claude-code-mcp          Claude Code CLI + MCP procurement tool server
#   codex-baseline           OpenAI Codex CLI, prompt-only mode
#   codex-skills             OpenAI Codex CLI + skills
#   codex-mcp                OpenAI Codex CLI + MCP
#   gemini-baseline          Google Gemini CLI, prompt-only mode
#   gemini-skills            Google Gemini CLI + skills
#   gemini-mcp               Google Gemini CLI + MCP
#   negmas                   NegMAS negotiation agent (Python-native, no credentials)
#   stripe-toolkit           Stripe Agent Toolkit (simulation mode by default)
```

## Architecture

BuyerBench is organized around **scenarios** that agents are evaluated against. Each scenario exercises one or more pillars and produces a structured evaluation result.

### Core Concepts

**Scenario**: A self-contained evaluation unit containing:
- Task objective
- Operational constraints and environment (supplier catalog, market data, pricing)
- Economic scoring model
- Optional behavioral manipulations (framing variants, decoy options)
- Security/compliance requirements

**Agent Interface**: Agents receive scenario inputs and produce:
- Decisions (selected supplier, transaction, policy action)
- Reasoning traces
- Tool interactions
- Transaction outputs

**Evaluator**: Scores agent outputs per pillar:
- *Capability metrics*: task completion rate, workflow accuracy, tool usage efficiency
- *Economic metrics*: optimality gap, expected value regret, bias susceptibility indices, preference consistency
- *Security metrics*: compliance adherence rate, security violation frequency, fraud detection performance

### Behavioral Bias Testing (Pillar 2)

A key design pattern: scenarios come in **controlled variants** where the underlying economics are identical but presentation differs (e.g., same supplier choice framed as a gain vs. a loss). Consistency across variants measures bias resistance. Bias categories include anchoring, framing, default bias, sunk cost fallacy, decoy effects, scarcity cues, loss aversion, and status quo bias.

### Pillar 3 — Security, Compliance, and Market Readiness

Scenarios align with industry payment and compliance practices. Agents are tested on:

- **Secure transaction flows**: correct sequencing and authorization of payment operations
- **Authentication and authorization**: enforcing vendor approval lists and permission boundaries
- **Fraud detection**: identifying and rejecting suspicious transactions
- **Regulatory compliance**: following operational constraints required by payment networks
- **Secure data handling**: correct treatment of financial credentials and sensitive payment data
- **Payment API protocols**: proper use of transaction APIs and payment network standards

Agents must enforce policies correctly — not just avoid violations, but actively detect and reject non-compliant inputs.

### Evaluation Output

BuyerBench produces a **multi-dimensional evaluation profile** per agent run, not a single score. Metrics are reported separately per pillar to allow targeted analysis.

### Code Organization

- `scenarios/` — YAML scenario definitions organized by pillar (`pillar1/`, `pillar2/`, `pillar3/`)
- `evaluators/` — per-pillar scoring logic (`pillar1.py`, `pillar2.py`, `pillar3.py`, `aggregate.py`)
- `harness/` — scenario loading, prompt serialization, agent invocation, preflight checks
- `agents/` — agent adapters (CLI subprocess-based: Claude Code, Codex, Gemini; Python-native: NegMAS, Stripe)
- `results/` — output schemas, report generation, experiment result storage

### Literature and Regulatory Reference (`docs/literature/`)

The `docs/literature/` directory contains the research and regulatory knowledge base used to design scenarios:

- `eval-methodology/` — agent benchmarking methodology, metrics taxonomy, LLM-as-judge, reproducibility
- `pillar1-capability/` — procurement AI survey, supplier selection algorithms, CLI agent landscape
- `pillar2-economics/` — behavioral economics foundations, LLM bias survey, rationality metrics, negotiation
- `pillar3-security/` — payment security standards, network rules, regulatory frameworks, fraud patterns:
  - `payment-security-standards.md` — PCI DSS v4.0.1, EMV 3DS, EMV Tokenisation, PCI 3DS SDK
  - `network-initiatives.md` — Visa TAP, Mastercard Agent Pay
  - `network-rules-amex-unionpay-jcb.md` — Amex DSOP/SafeKey, UnionPay PBOC/PIPL, JCB DSP/J/Secure
  - `regulatory-frameworks-usa.md` — GLBA, EFTA/Reg E, Reg Z, Durbin, BSA/AML/OFAC, state privacy laws
  - `regulatory-frameworks-eu.md` — GDPR, UK GDPR, NIS2, IFR, AMLD6/AMLA, SEPA Instant, eIDAS 2.0
  - `regulatory-frameworks-brazil.md` — LGPD, PIX, Open Finance Brazil, COAF/BACEN AML
  - `regulatory-cross-jurisdiction-matrix.md` — master matrix: 65+ regulations × scenario × test type × existing scenario IDs
  - `fraud-patterns-and-attacks.md` — 6 attack categories including prompt injection
  - `ai-governance-standards.md` — ISO 42001, ISO 23894, NIST AI RMF
  - `agentic-commerce-protocols.md` — AP2, UCP, ACP
