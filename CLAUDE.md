# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

BuyerBench is an open-source benchmark framework for evaluating AI buyer agents across three pillars:

1. **Pillar 1 — Agent Intelligence and Operational Capability**: Can the agent execute buyer workflows (supplier discovery, quote comparison, multi-step procurement tasks)?
2. **Pillar 2 — Economic Decision Quality and Behavioral Robustness**: Does the agent make economically rational decisions and resist behavioral biases (anchoring, framing, decoy effects, sunk cost, etc.)?
3. **Pillar 3 — Security, Compliance, and Market Readiness**: Does the agent follow payment security practices, fraud detection, and regulatory compliance?

## Commands

_This repository is in early initialization. Commands will be added here once a tech stack and build system are established._

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

### Evaluation Output

BuyerBench produces a **multi-dimensional evaluation profile** per agent run, not a single score. Metrics are reported separately per pillar to allow targeted analysis.
