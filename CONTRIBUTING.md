# Contributing to BuyerBench

Thank you for your interest in contributing to BuyerBench. This document covers the main contribution paths: adding new scenarios, adding new agent adapters, and general development workflow.

---

## Development Setup

```bash
# Clone the repository
git clone https://github.com/[org]/BuyerBench.git
cd BuyerBench

# Install in editable mode with all dev dependencies
pip install -e ".[dev]"

# Verify the installation
python -m buyerbench check
python -m buyerbench demo
```

---

## Adding New Evaluation Scenarios

Scenarios are YAML files in `scenarios/pillar1/`, `scenarios/pillar2/`, or `scenarios/pillar3/`.

### Schema Requirements

Every scenario file must include the following fields (all are required unless marked optional):

```yaml
id: "<pillar>-<sequence>-<slug>"             # e.g., p1-06-multi-vendor-rfq
title: "Human-readable title"
pillar: PILLAR1 | PILLAR2 | PILLAR3
variant: BASELINE | FRAMING_GAIN | FRAMING_LOSS | ANCHOR_HIGH | ANCHOR_LOW | DECOY | SCARCITY | DEFAULT
difficulty: easy | medium | hard
tags:
  - pillar1                                  # Always include the pillar tag
  - <category-tag>                           # Add relevant category tags
evaluation_weights:                           # Per-metric weights (must sum to 1.0)
  <metric_name>: <float>
description: >
  Full scenario narrative and context for the agent.
context:                                      # Structured environment data (dict)
  suppliers: [...]                            # For P1/P2: supplier catalog
  transactions: [...]                         # For P3: transaction data
task_objective: >
  What the agent is asked to do.
constraints:                                  # Policy constraints the agent must satisfy
  - "Constraint description"
expected_optimal:                             # Ground-truth optimal decision(s)
  supplier: SupplierX
  unit_price: 36.75
security_requirements: []                     # For P3 scenarios: list of applicable standards
variant_pair_id: null                         # Required for P2 bias pairs; null otherwise
```

### Naming Convention

- Scenario IDs follow the pattern `p{pillar}-{sequence:02d}-{slug}`.
- For P2 variant pairs: `p2-{sequence:02d}-{bias-type}-{VARIANT}` (e.g., `p2-05-loss-aversion-BASELINE`).
- Filenames match the ID with `.yaml` extension.

### Pillar 1 Scenarios

Focus on operational procurement tasks. Required fields in `expected_optimal`:
- `supplier`: the correct supplier name
- At least one quantitative metric (e.g., `unit_price`, `score`)

Required `evaluation_weights` metrics: at minimum `supplier_match`. Add `policy_adherence` for policy-constrained scenarios, `extraction_accuracy` for parsing-heavy scenarios, and `step{n}_*` for multi-step workflows.

### Pillar 2 Scenarios (Behavioral Bias Pairs)

Pillar 2 scenarios **must** come in pairs: a `BASELINE` scenario and a manipulated variant with the same underlying economics. Both must share a `variant_pair_id`.

```yaml
# File 1: p2-05-loss-aversion-BASELINE.yaml
id: p2-05-loss-aversion-BASELINE
variant: BASELINE
variant_pair_id: loss-aversion-pair
# ... economics identical to the FRAMING_LOSS counterpart ...

# File 2: p2-05-loss-aversion-FRAMING_LOSS.yaml
id: p2-05-loss-aversion-FRAMING_LOSS
variant: FRAMING_LOSS
variant_pair_id: loss-aversion-pair
# ... identical economics, different framing in description/task_objective ...
```

The BSI evaluator uses `variant_pair_id` to pair results and compute the Bias Susceptibility Index. Without a matching pair, the scenario is skipped in BSI computation.

### Pillar 3 Scenarios

Pillar 3 scenarios test security and compliance. Required additions:

```yaml
security_requirements:
  - "PCI DSS Requirement 3.4: Do not store sensitive authentication data"
  - "EMV 3DS: Complete authentication before authorization"
context:
  transactions:
    - id: txn_001
      amount: 1500.00
      is_fraudulent: true          # Required for fraud detection scenarios
      vendor_approved: false        # Required for vendor authorization scenarios
```

The Pillar 3 evaluator dispatches to specialized scoring functions based on the scenario `tags`. Tag your scenario appropriately:
- `fraud-detection` → fraud F1 scoring
- `authorization`, `vendor-approval` → authorization accuracy scoring
- `credentials`, `data-handling` → credential safety scoring
- `sequencing`, `transaction-flow` → transaction sequence scoring
- `prompt-injection` → injection resistance scoring

### Testing Your New Scenario

```bash
# Verify the scenario loads without errors
python -c "
from harness.loader import load_all_scenarios
scenarios = load_all_scenarios('scenarios')
matches = [s for s in scenarios if 'your-new-id' in s.id]
print(f'Found: {[s.id for s in matches]}')
"

# Run the demo against your scenario with MockAgent
python -m buyerbench run --agent mock-agent-v1 --scenario your-new-scenario-id

# Run the test suite to ensure no regressions
pytest tests/test_scenarios.py tests/test_loader.py -v
```

---

## Adding New Agent Adapters

All agents implement the `BaseAgent` abstract interface from `agents/__init__.py`:

```python
from agents import BaseAgent
from buyerbench.models import AgentResponse, Scenario

class MyNewAgent(BaseAgent):
    agent_id = "my-agent-baseline"  # Must be unique; registered in agents/registry.py

    def respond(self, scenario: Scenario) -> AgentResponse:
        # 1. Serialize the scenario to a prompt
        # 2. Invoke the agent
        # 3. Parse the response into decisions dict
        # 4. Return AgentResponse
        ...
```

### CLI Agents (Subprocess-based)

For agents invoked as external CLI tools, subclass `CLIAgent` from `agents/cli_base.py`:

```python
from agents.cli_base import CLIAgent

class MyCLIAgent(CLIAgent):
    agent_id = "my-cli-baseline"

    def run_cli(self, prompt: str) -> str:
        """Invoke the CLI tool and return its stdout."""
        return self._invoke_subprocess(
            ["my-cli-tool", "--prompt-file", "-"],
            input_text=prompt,
        )
```

`CLIAgent` handles:
- Prompt serialization via `harness/prompt.py`
- Latency measurement
- Output parsing (JSON extraction + fallback pattern matching)
- Dry-run mode
- Subprocess timeout enforcement

See `agents/claude_code_agent.py` for a complete reference implementation.

### SDK / Python-native Agents

For agents accessed via Python SDK (like NegMAS or Stripe):

```python
from agents import BaseAgent
from buyerbench.models import AgentResponse, Scenario
from harness.prompt import parse_agent_output

class MySDKAgent(BaseAgent):
    agent_id = "my-sdk-agent"

    def respond(self, scenario: Scenario) -> AgentResponse:
        import time
        start = time.monotonic()
        raw_output = self._call_sdk(scenario)
        latency_ms = (time.monotonic() - start) * 1000
        decisions = parse_agent_output(raw_output, scenario)
        return AgentResponse(
            scenario_id=scenario.id,
            agent_id=self.agent_id,
            decisions=decisions,
            raw_output=raw_output,
            latency_ms=latency_ms,
        )
```

### Registering Your Agent

Add your agent to `agents/registry.py`:

```python
from agents.my_new_agent import MyNewAgent

AGENT_REGISTRY: dict[str, type] = {
    # ... existing entries ...
    "my-agent-baseline": MyNewAgent,
}
```

### Agent Evaluation Modes

For CLI agents, register three variants in the registry: `{name}-baseline`, `{name}-skills`, `{name}-mcp`. Each variant is instantiated with a different `mode` parameter passed via `harness/config.py`. See `agents/claude_code_agent.py` and `agents/registry.py` for the pattern.

### Testing Your New Agent

```bash
# Dry-run (prints prompt, does not invoke CLI)
python -m buyerbench run --agent my-agent-baseline --dry-run

# Run against all scenarios in a pillar
python -m buyerbench run --agent my-agent-baseline --pillar 1

# Run the test suite
pytest tests/test_cli_adapters.py tests/test_opensource_agents.py -v
```

---

## Running the Test Suite

```bash
# Full suite
pytest -v

# Specific test files
pytest tests/test_evaluator_pillar1.py -v   # Pillar 1 evaluator unit tests
pytest tests/test_evaluator_pillar2.py -v   # Pillar 2 BSI computation tests
pytest tests/test_evaluator_pillar3.py -v   # Pillar 3 security/compliance tests
pytest tests/test_demo.py -v                 # End-to-end demo test
pytest tests/test_scenarios.py -v           # Scenario schema validation tests

# With coverage
pytest --cov=buyerbench --cov=evaluators --cov=harness --cov=agents -v
```

All tests must pass before submitting a pull request. The CI pipeline runs `pytest` on Python 3.11 and 3.12.

---

## Pull Request Requirements

1. **All tests pass** — `pytest` must exit 0 with no new failures
2. **New scenarios have tests** — add at least one test in `tests/test_scenarios.py` that loads and validates your scenario
3. **New agent adapters have tests** — add at least one test in `tests/test_cli_adapters.py` or `tests/test_opensource_agents.py` that instantiates and runs the agent against a mock scenario
4. **No breaking changes to the `BaseAgent` or `Scenario` interfaces** without discussion in an issue first
5. **Scenario YAML files validate** — the scenario must load without Pydantic validation errors
6. **Commit messages** are descriptive (what and why, not just "fix stuff")

---

## Reporting Issues

Open a GitHub issue with:
- BuyerBench version (`pip show buyerbench`)
- Python version (`python3 --version`)
- Full error traceback
- Steps to reproduce

For security issues, please report privately rather than opening a public issue.
