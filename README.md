# BuyerBench

**BuyerBench** is an open-source, multi-dimensional benchmark framework for evaluating AI buyer agents. It measures three independent properties of any buyer agent:

| Pillar | What it measures | Key metrics |
|--------|-----------------|-------------|
| **P1 — Capability** | Can the agent execute procurement workflows? (supplier discovery, quote comparison, multi-step sourcing, policy-constrained selection) | Task Completion Rate, Supplier Selection Accuracy, Policy Adherence |
| **P2 — Economic Rationality** | Does the agent make economically optimal decisions and resist cognitive biases? (anchoring, framing, decoy, scarcity) | Optimal Choice Rate, Optimality Gap, Bias Susceptibility Index (BSI) |
| **P3 — Security & Compliance** | Does the agent follow payment security standards and detect fraud? (PCI DSS, EMV 3DS, prompt injection, vendor authorization) | Compliance Adherence Rate, Fraud Detection F1, Security Degradation Score |

BuyerBench is the **first open-source benchmark** addressing all three dimensions simultaneously. A single aggregate benchmark score for a procurement agent is misleading; capability, rationality, and security compliance are empirically uncorrelated. BuyerBench produces a three-dimensional evaluation profile.

---

## Quickstart

```bash
# Install
pip install -e ".[dev]"

# Run preflight check (verify CLI tools and API keys)
python -m buyerbench check

# Run end-to-end demo (3 scenarios, MockAgent, rich formatted report)
python -m buyerbench demo

# Run full benchmark against an agent
python -m buyerbench run --agent claude-code-baseline

# Generate full report from experiment results
python -m buyerbench report --experiment-dir results/experiments
```

---

## Benchmark Results Preview

Initial evaluation of two open-source reference agents:

| Agent | P1 Capability | P2 Economics | P3 Security | Notes |
|-------|:-------------:|:------------:|:-----------:|-------|
| **NegMAS (E13)** | **0.44** | — | — | Perfect on structured optimization; zero on multi-step workflow |
| **Stripe Toolkit (E20)** | — | — | **0.66** | Perfect fraud detection (F1=1.0); fails transaction sequencing (CAR=0.30) |
| Claude Code | pending | pending | pending | CLI credential required |
| Codex CLI | pending | pending | pending | CLI credential required |
| Gemini CLI | pending | pending | pending | CLI credential required |

The NegMAS/Stripe results demonstrate the framework's core value: both agents achieve moderate aggregate scores, but the per-pillar breakdown reveals stark capability boundaries that an aggregate score would obscure.

See the [full paper](docs/paper/buyerbench-paper.md) and [FULL-REPORT.json](results/experiments/FULL-REPORT.json) for complete results.

---

## Features

- **18 evaluation scenarios** across three pillars, organized by difficulty (easy/medium/hard)
- **Controlled variant methodology** for bias measurement: A/B scenario pairs with identical economics but differing presentations; the Bias Susceptibility Index (BSI) quantifies susceptibility
- **Three evaluation modes** per CLI agent: baseline (prompt-only), skills (structured tool definitions), MCP (Model Context Protocol tool server)
- **Subprocess-based agent interface**: agents run as external CLI processes — no code modification required to evaluate new CLI tools
- **Open-source agent adapters**: NegMAS (negotiation), Stripe Agent Toolkit (payment), with stubs for 20+ commercial/consumer agents
- **Rich terminal dashboard**: real-time evaluation results via `rich` formatted tables
- **Research paper**: full methodology paper in `docs/paper/buyerbench-paper.md`

---

## Architecture

```
Scenario Library (18 scenarios)
        │
        ▼
Harness: Loader + Prompt Builder
        │
        ▼
Agent Interface (CLI subprocess / SDK adapter)
  ├── Baseline mode   (prompt only)
  ├── Skills mode     (+ BuyerBench skill catalog)
  └── MCP mode        (+ Model Context Protocol tool server)
        │
        ▼
Evaluator (Pillar 1 / Pillar 2 / Pillar 3)
        │
        ▼
Results: JSON per scenario → FULL-REPORT.json + FULL-REPORT.md
```

See [Figure 1 in the paper](docs/paper/figures/fig5-harness-architecture.png) for a visual diagram.

---

## Project Structure

```
buyerbench/          # Core package (CLI entry point, data models)
├── __main__.py      # CLI commands: demo, check, run, report
└── models.py        # Scenario, AgentResponse, EvaluationResult data models

scenarios/           # Scenario definitions (YAML/JSON, organized by pillar)
├── pillar1/         # 5 capability scenarios
├── pillar2/         # 8 behavioral bias scenarios (4 variant pairs)
└── pillar3/         # 5 security/compliance scenarios

evaluators/          # Per-pillar scoring logic
├── pillar1.py       # TCR, SSA, PA, TCE metrics
├── pillar2.py       # OCR, OG, EVR, BSI metrics
├── pillar3.py       # CAR, SVF, FD-F1, SDS metrics
└── aggregate.py     # BSI aggregation, skills/MCP delta, report generation

harness/             # Scenario execution infrastructure
├── loader.py        # Scenario discovery and loading
├── runner.py        # Agent invocation and result collection
├── prompt.py        # Prompt serialization (baseline/skills/MCP modes)
├── config.py        # Harness configuration
├── preflight.py     # CLI/API key availability checks
└── mock_mcp_server.py  # Mock MCP server for MCP-mode evaluation

agents/              # Agent implementations and adapters
├── mock.py          # MockAgent (deterministic, always available)
├── cli_base.py      # Base class for CLI subprocess agents
├── claude_code_agent.py  # Claude Code adapter
├── codex_agent.py   # OpenAI Codex CLI adapter
├── gemini_agent.py  # Google Gemini CLI adapter
├── negmas_agent.py  # NegMAS negotiation agent adapter
├── stripe_toolkit_agent.py  # Stripe Agent Toolkit adapter
└── registry.py      # Agent registry (maps agent IDs to classes)

results/             # Output schemas and experiment results
├── schemas.py       # EvaluationResult JSON schema
├── report.py        # Report generation (generate_full_report, render_markdown)
└── experiments/     # Experiment run outputs (auto-created by `run` command)

tests/               # Full test suite (pytest)
notebooks/           # Jupyter notebooks for results analysis
docs/
├── paper/           # Research paper (Markdown + BibTeX)
│   ├── buyerbench-paper.md  # Full paper
│   ├── figures/             # Publication figures (300 DPI PNG)
│   ├── references.bib       # BibTeX references
│   ├── PAPER-STATUS.md      # Section status tracker
│   └── SUBMISSION-CHECKLIST.md  # Venue checklist
└── agents/          # Agent catalog and evaluation stubs
```

---

## Running Tests

```bash
# Full test suite
pytest -v

# With coverage
pytest --cov=buyerbench --cov=evaluators --cov=harness --cov=agents

# Specific pillar
pytest tests/test_evaluator_pillar3.py -v
```

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to:
- Add new evaluation scenarios
- Add new agent adapters
- Run the test suite
- Submit pull requests

---

## Citation

If you use BuyerBench in your research, please cite:

```bibtex
@software{buyerbench2026,
  title     = {{BuyerBench}: A Multi-Dimensional Benchmark for Evaluating {AI} Buyer Agents},
  author    = {[Author list TBD]},
  year      = {2026},
  url       = {https://github.com/[org]/BuyerBench},
  note      = {Open-source Python benchmark framework, v1.0}
}
```

---

## License

BuyerBench is released under the Apache 2.0 License. See [LICENSE](LICENSE) for details.
