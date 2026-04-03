---
type: research
title: CLI Agent Landscape — Evaluation Targets for BuyerBench
created: 2026-04-03
tags:
  - pillar1
  - cli-agents
  - claude
  - codex
  - gemini
  - evaluation-targets
related:
  - '[[procurement-ai-survey]]'
  - '[[workflow-completion-metrics]]'
  - '[[PILLAR1-SUMMARY]]'
---

# CLI Agent Landscape — Evaluation Targets for BuyerBench

## Overview

BuyerBench's primary evaluation targets are **general-purpose CLI-based AI coding and task agents** that can be adapted for procurement workflows. These agents are publicly available, widely used, and represent the frontier of agentic AI capability accessible to enterprise developers and research teams. This document profiles the three primary candidates.

---

## Primary Evaluation Targets

### Claude Code CLI (Anthropic)
**Model family**: Claude Sonnet / Opus / Haiku (configurable)  
**Interface**: CLI (`claude`) + VS Code / JetBrains extension + Web app  
**Primary use case**: Software engineering — code generation, editing, debugging, test writing, codebase navigation  

**Tool-use capabilities**:
- Read, Write, Edit files
- Bash execution (shell commands)
- Glob (file search), Grep (content search)
- Web search and web fetch
- Agent spawning (sub-agent delegation)
- Task and todo management

**MCP support**: Full MCP (Model Context Protocol) support — can connect to external servers (databases, APIs, internal systems) via MCP, enabling custom tool integration without code changes. BuyerBench can expose procurement APIs as MCP servers.

**Skills support**: Yes — slash commands (skills) can package multi-step workflows as reusable commands. Relevant for packaging procurement workflows as evaluatable units.

**Procurement-relevant capabilities**:
- Can read supplier catalogs (CSV, JSON, structured files)
- Can execute bash scripts (e.g., calling procurement APIs)
- Can reason across multi-step workflows
- Strong instruction-following for complex constraint satisfaction
- MCP integration allows connecting to ERP/procurement system stubs

**Publicly documented strengths**:
- Excellent at complex software engineering tasks
- Strong code understanding and modification
- Context window allows handling large supplier catalogs
- Multi-agent capabilities for orchestrating sub-tasks

**Publicly documented weaknesses/limitations**:
- Primarily optimized for software tasks; procurement domain requires scenario scaffolding
- Tool approval prompts may interrupt automated benchmark runs (requires `--dangerously-skip-permissions` or headless mode)

**Notes for BuyerBench**: The Claude Code CLI is the native environment for CladiBuyer Benchmarker (the benchmark orchestrator itself). Claude Code's MCP support and sub-agent delegation make it the most natural fit for BuyerBench's layered evaluation architecture.

---

### Codex CLI (OpenAI)
**Model family**: Codex / GPT-4o (configurable)  
**Interface**: CLI (`codex`)  
**Primary use case**: Software engineering — code generation, editing, shell execution with AI oversight  
**Release context**: Released by OpenAI as an open-source CLI agent in 2025, positioned as a terminal-first counterpart to ChatGPT

**Tool-use capabilities**:
- File read and write
- Shell command execution (with configurable approval modes: suggest, auto-edit, full-auto)
- Code search and navigation
- Multi-file project manipulation

**MCP support**: Limited at time of writing — MCP integration is not a core feature of the initial Codex CLI design. Tool calls are primarily file and shell operations.

**Skills support**: No native skills/slash-command packaging equivalent to Claude Code.

**Procurement-relevant capabilities**:
- Can read and manipulate structured files (supplier catalogs)
- Shell execution enables calling procurement API stubs
- GPT-4o's strong instruction following enables constraint satisfaction tasks
- "Full auto" mode enables uninterrupted benchmark execution

**Publicly documented strengths**:
- Clean CLI interface; approval modes simplify automated evaluation
- Strong coding capability inherited from GPT-4o
- Open-source agent code enables inspection of agent behavior

**Publicly documented weaknesses/limitations**:
- Less extensive tool ecosystem than Claude Code (no MCP, no sub-agent spawning)
- Procurement domain knowledge may require more scaffolding in the system prompt

**Notes for BuyerBench**: Codex CLI is the most direct OpenAI counterpart to Claude Code for CLI-based agentic evaluation. Its "full auto" mode is useful for uninterrupted benchmark runs.

---

### Gemini CLI (Google)
**Model family**: Gemini 2.0 Flash / Pro (configurable)  
**Interface**: CLI (`gemini`)  
**Primary use case**: Software engineering — code generation, editing, multi-file reasoning  
**Release context**: Released by Google in 2025 as an open-source terminal-based agent, explicitly positioned to compete with Claude Code and Codex CLI

**Tool-use capabilities**:
- File read and write
- Shell command execution
- Web search (leveraging Google Search integration)
- Large context window (1M tokens) for ingesting large codebases or supplier catalogs

**MCP support**: Yes — Gemini CLI supports MCP server integration, enabling external tool connections.

**Skills support**: No native skills/slash-command system equivalent to Claude Code.

**Procurement-relevant capabilities**:
- Very large context window enables processing large supplier catalogs without chunking
- Web search integration enables live supplier research scenarios (if network access is permitted)
- MCP support allows connecting to procurement API stubs
- Gemini 2.0's multimodal capabilities could support document-based procurement (invoices, RFx PDFs)

**Publicly documented strengths**:
- Industry-leading context window (1M tokens) for large-catalog scenarios
- Web search integration for research-heavy tasks
- MCP support for extensibility

**Publicly documented weaknesses/limitations**:
- Newer to the CLI agent market; less community-documented agentic behavior
- Tool approval and safety guardrails may require configuration for automated benchmark runs

**Notes for BuyerBench**: Gemini CLI's large context window is a potential advantage for scenarios requiring full catalog ingestion. Its MCP support aligns it architecturally with Claude Code for BuyerBench integration.

---

## Comparison Table

| Dimension | Claude Code CLI | Codex CLI | Gemini CLI |
|-----------|----------------|-----------|------------|
| **Tool use** | Read, Write, Edit, Bash, Glob, Grep, Web | Read, Write, Bash, Shell | Read, Write, Bash, Web Search |
| **MCP support** | Full | Limited / None | Yes |
| **Skills / slash commands** | Yes (extensible) | No | No |
| **Sub-agent delegation** | Yes (Agent tool) | No | No |
| **Context window** | ~200K tokens | ~128K tokens | ~1M tokens |
| **Approval/auto mode** | Configurable (permission modes) | Yes (suggest/auto-edit/full-auto) | Configurable |
| **Open-source agent code** | Partial (closed model) | Yes | Yes |
| **Procurement-relevant: catalog ingestion** | Good | Good | Excellent (large context) |
| **Procurement-relevant: API integration** | Excellent (MCP) | Good (Bash) | Good (MCP + Bash) |
| **Procurement-relevant: multi-step workflows** | Excellent (skills + sub-agents) | Good | Good |
| **Procurement-relevant: constraint enforcement** | Strong | Strong | Strong |
| **BuyerBench integration complexity** | Low (native environment) | Medium | Medium |

---

## BuyerBench Adapter Architecture

Each CLI agent requires a thin adapter layer that:
1. **Translates** BuyerBench scenario inputs into the agent's expected interface (system prompt, tool definitions, initial context)
2. **Captures** the agent's trajectory (tool calls, reasoning, final decision)
3. **Enforces** evaluation constraints (e.g., which tools are available for a given scenario)

The adapter pattern insulates BuyerBench scenarios from agent-specific interface changes — if Gemini CLI changes its tool format, only the Gemini adapter needs updating.

---

## See Also

- [[procurement-ai-survey]] — commercial procurement AI systems (different target population)
- [[workflow-completion-metrics]] — how CLI agent workflows are evaluated
- [[PILLAR1-SUMMARY]] — synthesis and scenario design implications
