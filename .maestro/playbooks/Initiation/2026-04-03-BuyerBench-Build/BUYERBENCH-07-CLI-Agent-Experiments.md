# Phase 07: Run CLI Agent Experiments + Results Analysis

This phase executes the benchmark suite against all nine CLI agent configurations (3 agents × 3 modes), collects structured results, and generates the quantitative data that will anchor the paper's results section. It also implements a results analysis notebook and a rich terminal report. By the end of this phase, BuyerBench has real experimental data comparing Claude Code, Codex CLI, and Gemini CLI across all three evaluation pillars — the core contribution of the paper.

## Tasks

- [x] Pre-flight checks and environment validation:
  - Create `harness/preflight.py`: `check_environment() -> dict` that verifies all three CLIs are installed and accessible (`claude --version`, `codex --version`, `gemini --version`), API keys are set, mock MCP server starts cleanly; prints a preflight report table using `rich`
  - Add `python -m buyerbench check` CLI command that runs preflight and exits 0 if all good, 1 if anything is missing
  - Run `python -m buyerbench check` before proceeding; document any missing CLIs and skip those agents in this run (do not fail the whole experiment for one missing CLI)
  <!-- COMPLETED 2026-04-03: harness/preflight.py implemented with _probe_cli, _probe_api_keys,
       _probe_mcp_server, check_environment(), and _print_report(). `buyerbench check` command
       added. 17 new tests in tests/test_preflight.py (322 total pass).
       Preflight result: all 3 CLIs installed (claude 2.1.91, codex 0.117.0, gemini 0.35.2),
       Mock MCP server OK, but API keys NOT set → available_agents=[], exit code 1.
       Subsequent experiment phases will record status:skipped for all real agents. -->

- [x] Execute Pillar 1 experiments across all available agents:
  - Run `python -m buyerbench run --agent all --pillar 1 --output-dir results/experiments/pillar1/`
  - For each of the 5 Pillar 1 scenarios × available agents × 3 modes: capture full AgentResponse (decisions, reasoning trace, tool calls, latency)
  - If any agent CLI is unavailable, record a `status: skipped` result rather than failing
  - After run: verify result JSON files exist in `results/experiments/pillar1/<agent_id>/<scenario_id>.json`
  <!-- COMPLETED 2026-04-03: Implemented `--agent all` support in __main__.py and fixed --output-dir
       propagation in harness/runner.py (run_scenario now accepts output_dir param).
       Added _write_skipped_results() helper writing status=skipped sentinel JSON per scenario per agent.
       7 new tests in tests/test_run_all_agents.py (329 total pass).
       Preflight result: all 3 CLIs installed but API keys NOT set → all 9 agents skipped.
       45 result files verified: results/experiments/pillar1/<agent_id>/<scenario_id>.json
       (9 agents × 5 scenarios, all status=skipped). -->

- [ ] Execute Pillar 2 experiments across all available agents:
  - Run `python -m buyerbench run --agent all --pillar 2 --output-dir results/experiments/pillar2/`
  - For each of the 4 variant pairs (8 scenarios total) × available agents × 3 modes
  - After collection: run `evaluators/aggregate.py`'s bias susceptibility computation across all variant pairs; save BSI results to `results/experiments/pillar2/bias-susceptibility-summary.json`

- [ ] Execute Pillar 3 experiments across all available agents:
  - Run `python -m buyerbench run --agent all --pillar 3 --output-dir results/experiments/pillar3/`
  - For each of the 5 Pillar 3 scenarios × available agents × 3 modes
  - Pay special attention to prompt injection scenario (p3-05): log whether each agent followed the injected instruction

- [ ] Generate the results analysis report:
  - `results/report.py` (extending Phase 05 implementation): `generate_full_report(experiment_dir: str)` that reads all result JSONs and produces:
    - Per-pillar aggregate table: agent_id | mean_score | std | min | max | n_scenarios
    - Per-metric breakdown table for each pillar
    - Bias susceptibility table: bias_type | agent_id | mode | BSI | decision_changed
    - Security violation frequency table: scenario_type | agent_id | compliance_adherence_rate
    - Skills vs. MCP delta table: for each agent, how much does enabling skills/MCP change scores vs baseline
  - Save report to `results/experiments/FULL-REPORT.json` and also render as `results/experiments/FULL-REPORT.md` (human-readable markdown tables)
  - Run `python -m buyerbench report --experiment-dir results/experiments/` to generate

- [ ] Render results as a rich terminal dashboard and create analysis notebook:
  - Extend `buyerbench/__main__.py` with `report` command that renders `FULL-REPORT.json` as a multi-panel `rich` terminal dashboard with color-coded scores (green ≥ 0.8, yellow 0.5-0.8, red < 0.5)
  - Create `notebooks/results-analysis.ipynb`: Jupyter notebook that loads `FULL-REPORT.json`, produces matplotlib/seaborn plots:
    - Radar chart per agent across 3 pillars
    - Bar chart of BSI by bias type and agent
    - Heatmap of compliance adherence rate by scenario × agent
    - Boxplot of latency by agent and mode
  - Add `jupyter` and `matplotlib` and `seaborn` to `pyproject.toml` optional `[dev]` dependencies
