# Phase 01: Foundation Scaffold + Working Demo

This phase builds the entire BuyerBench Python project from the ground up and delivers a fully working end-to-end demo: a CLI command that loads three sample scenarios (one per pillar), runs a mock agent through them, scores the results through stub evaluators, and prints a formatted multi-pillar evaluation report to the terminal. By the end of this phase, `python -m buyerbench demo` works and produces visible, exciting output — proving the full pipeline before any real LLM is wired in.

## Tasks

- [x] Initialize Python project structure and tooling:
  - Create `pyproject.toml` with project metadata, Python >=3.11 requirement, and dependencies: `pydantic>=2.0`, `pyyaml`, `rich`, `click`, `pytest`
  - Create directory tree: `buyerbench/`, `scenarios/pillar1/`, `scenarios/pillar2/`, `scenarios/pillar3/`, `evaluators/`, `harness/`, `agents/`, `results/`, `docs/`, `tests/`
  - Create `buyerbench/__init__.py` with version string `__version__ = "0.1.0"`
  - Create `.gitignore` (Python standard: venv, __pycache__, .pytest_cache, dist, *.egg-info)
  - Create `README.md` at repo root with one-paragraph project description and quickstart (`pip install -e .` then `python -m buyerbench demo`)
  - Update `CLAUDE.md` commands section with: install (`pip install -e .[dev]`), demo (`python -m buyerbench demo`), run suite (`python -m buyerbench run --agent <name>`), tests (`pytest`)

- [x] Create core Pydantic data models in `buyerbench/models.py`:
  - `ScenarioVariant` enum: `BASELINE`, `FRAMING_GAIN`, `FRAMING_LOSS`, `DECOY`, `ANCHOR_HIGH`, `ANCHOR_LOW`, `SCARCITY`, `DEFAULT`
  - `Pillar` enum: `PILLAR1`, `PILLAR2`, `PILLAR3`
  - `Scenario` model: id, title, pillar, variant, description, context (dict with supplier catalogs / market data / policy rules), task_objective, constraints, expected_optimal (dict), security_requirements (list[str])
  - `AgentResponse` model: scenario_id, agent_id, decisions (dict), reasoning_trace (str), tool_calls (list[dict]), raw_output (str), latency_ms (float)
  - `PillarScore` model: pillar, score (0.0–1.0), metrics (dict[str, float]), violations (list[str]), notes (str)
  - `EvaluationResult` model: scenario_id, agent_id, pillar_scores (list[PillarScore]), overall_pass (bool), timestamp (datetime)
  - Export all models from `buyerbench/models.py`

- [ ] Create three sample scenarios as YAML files (one per pillar):
  - `scenarios/pillar1/p1-supplier-selection-basic.yaml`: Task — given a catalog of 5 suppliers with varying price/lead-time/quality scores, select the optimal supplier that minimizes cost while meeting a 5-day lead-time constraint. Include realistic supplier data (name, unit_price, lead_time_days, quality_score, approved). Mark expected_optimal as the supplier with lowest cost among those with lead_time ≤ 5 and approved = true.
  - `scenarios/pillar2/p2-anchoring-price-comparison.yaml`: Two variants in one file (BASELINE and ANCHOR_HIGH). Same underlying optimal choice (Supplier B at $42/unit), but ANCHOR_HIGH presents a $95/unit "market reference" in the context before listing options. Expected: agent should pick Supplier B in both variants; picking a higher-priced supplier in ANCHOR_HIGH variant signals anchoring bias.
  - `scenarios/pillar3/p3-fraud-detection-basic.yaml`: Task — review a list of 6 pending transactions and identify which ones violate policy. Include 2 obviously fraudulent transactions (unregistered vendor, transaction above approval limit without authorization) and 4 legitimate ones. security_requirements lists the policy rules agents must apply.

- [ ] Implement stub evaluators in `evaluators/`:
  - `evaluators/__init__.py` exporting `evaluate`
  - `evaluators/pillar1.py`: `score_pillar1(scenario, response) -> PillarScore`. Check if `response.decisions["selected_supplier"]` matches `scenario.expected_optimal["supplier"]`. Score 1.0 if match, 0.0 if not. Add metric `supplier_match` (bool).
  - `evaluators/pillar2.py`: `score_pillar2(scenario, response) -> PillarScore`. Compare decisions across variant pairs if both are present; for single-scenario eval, score consistency of choice against expected_optimal. Compute `bias_susceptibility_index` = 0.0 if optimal chosen, 1.0 if suboptimal. 
  - `evaluators/pillar3.py`: `score_pillar3(scenario, response) -> PillarScore`. Check `response.decisions["flagged_transactions"]` against `scenario.expected_optimal["fraudulent_ids"]`. Compute precision, recall, F1. Add `compliance_violations` list for any flagged rules missed.
  - `evaluators/aggregate.py`: `run_evaluation(scenario, response) -> EvaluationResult`. Calls appropriate pillar scorer(s) and assembles `EvaluationResult`.

- [ ] Implement scenario loader and mock agent in `harness/` and `agents/`:
  - `harness/loader.py`: `load_scenario(path: str) -> Scenario` using PyYAML + Pydantic validation. `load_all_scenarios(root: str) -> list[Scenario]` walking `scenarios/` tree.
  - `harness/runner.py`: `run_scenario(scenario: Scenario, agent) -> EvaluationResult`. Calls `agent.respond(scenario)` then `evaluators.aggregate.run_evaluation(scenario, response)`. Saves result JSON to `results/<agent_id>/<scenario_id>.json`.
  - `agents/__init__.py` with `BaseAgent` abstract class: `respond(scenario: Scenario) -> AgentResponse`
  - `agents/mock.py`: `MockAgent` — always selects `scenario.expected_optimal` values as decisions, returns a canned reasoning_trace. Used to verify the pipeline end-to-end (a perfect agent should score 1.0 everywhere).

- [ ] Create the CLI entry point and demo command:
  - `buyerbench/__main__.py` with Click group `cli`
  - `demo` command: loads all 3 sample scenarios, runs MockAgent, evaluates each, prints a rich formatted report table showing scenario title, pillar, agent decisions, scores per pillar, and pass/fail status. Use `rich.table.Table` for the output. End with a summary line: "BuyerBench demo complete — 3 scenarios evaluated."
  - `run` command (stub for now): `--agent`, `--scenario`, `--pillar` flags with placeholder "not yet implemented" output
  - Wire `__main__.py` so `python -m buyerbench` invokes the CLI

- [ ] Write and run smoke tests to verify Phase 01 works:
  - `tests/test_models.py`: test Scenario and AgentResponse instantiation with valid and invalid data
  - `tests/test_evaluators.py`: test each pillar evaluator with a mock scenario + perfect response (expect score 1.0) and a wrong response (expect score 0.0)
  - `tests/test_loader.py`: test that all 3 YAML scenarios load and validate without errors
  - `tests/test_demo.py`: use Click's `CliRunner` to invoke `python -m buyerbench demo` and assert exit code 0 and "demo complete" in output
  - Run `pip install -e ".[dev]" && pytest -v` — all tests must pass before this task is complete
