# BuyerBench

BuyerBench is an open-source benchmark framework for evaluating AI buyer agents across three dimensions: operational capability (can the agent execute procurement workflows?), economic decision quality (does it make rational choices and resist behavioral biases?), and security/compliance readiness (does it enforce payment policies and detect fraud?).

## Quickstart

```bash
pip install -e ".[dev]"
python -m buyerbench demo
```

## What the demo does

The `demo` command loads one scenario per pillar, runs a mock agent through each, scores the results, and prints a formatted multi-pillar evaluation report. It proves the full pipeline before any real LLM is wired in.

## Project Structure

```
buyerbench/       # Core package (CLI, models)
scenarios/        # YAML scenario definitions (pillar1/, pillar2/, pillar3/)
evaluators/       # Per-pillar scoring logic
harness/          # Scenario loader and runner
agents/           # Base agent interface and reference implementations
results/          # Runtime output (JSON evaluation results)
tests/            # Test suite
docs/             # Documentation
```

## Running tests

```bash
pytest -v
```
