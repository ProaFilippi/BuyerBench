# Phase 03: Academic-Style Terminal Reports + Session Exports

This phase adds publication-quality reporting to every benchmark run: a Rich terminal table styled after academic paper result tables (with significance markers, alignment, and score deltas), and automatic per-session exports to `.md` and `.csv` files. The session Markdown uses structured front matter for DocGraph navigation, while the CSV is clean and flat for downstream analysis. Both are generated automatically at the end of every `buyerbench run` invocation.

## Tasks

- [x] Create `results/session_export.py` — the session export engine. This file owns both the `.md` and `.csv` generation. Implement:
  - `SessionMetadata` dataclass: `session_id: str` (format: `session-YYYYMMDD-HHMMSS`), `agents: list[str]`, `scenarios_run: int`, `pillars: list[int]`, `started_at: datetime`, `completed_at: datetime`, `output_dir: str`.
  - `export_session_markdown(results: list[EvaluationResult], meta: SessionMetadata, output_path: str) -> None`: writes a `.md` file with YAML front matter (`type: report`, `title: BuyerBench Session <session_id>`, `created: <ISO date>`, `tags: [benchmark, buyerbench, openrouter]`, `related: ['[[FULL-REPORT]]']`) followed by sections: ## Summary (agent list, scenario count, date range), ## Results by Pillar (one sub-table per pillar with agent rows and score columns), ## Per-Scenario Breakdown (markdown table: Scenario | Pillar | Variant | Agent | Score | Pass), ## Notes (any agents with errors or timeouts).
  - `export_session_csv(results: list[EvaluationResult], meta: SessionMetadata, output_path: str) -> None`: writes a flat CSV using Python's stdlib `csv` module. Columns: `session_id, agent_id, scenario_id, pillar, variant, score, overall_pass, latency_ms, timestamp`. One row per (agent, scenario) pair.
  - `generate_session_id() -> str`: returns `f"session-{datetime.now().strftime('%Y%m%d-%H%M%S')}"`.

- [x] Create `results/academic_tables.py` — Rich table renderers styled after academic paper formatting. Implement:
  - `render_model_comparison_table(results: list[EvaluationResult], console: Console) -> None`: the main academic table. Rows = models/agents, Columns = P1 Score, P2 Score, P3 Score, Overall, Δ vs. Baseline, N. Use Rich `Table` with `box=rich.box.HEAVY_HEAD` for the header separator. Format scores as `0.XX ± 0.XX` if multiple scenarios. Mark top performer per column with `★`. Mark scores significantly above baseline (>0.05 gap) with `†`. Render a legend below the table explaining markers.
  - `render_pillar_breakdown_table(results: list[EvaluationResult], pillar: int, console: Console) -> None`: detailed per-scenario breakdown for one pillar. Rows = scenarios (sorted by difficulty), Columns = one column per agent. Shade cells: green ≥0.8, yellow 0.5–0.8, red <0.5 using Rich markup. Include a "Best" row at the bottom showing the top agent per scenario.
  - `render_bias_table(results: list[EvaluationResult], console: Console) -> None`: Pillar 2 focused. For each variant pair, show BASELINE vs. FRAMING/ANCHOR/DECOY/etc. columns with decision consistency rate. Highlight inconsistencies in red.
  - `render_session_summary_panel(meta: SessionMetadata, results: list[EvaluationResult], console: Console) -> None`: a Rich Panel with a brief summary — total scenarios, agents tested, overall pass rate, best performer, session duration, and file paths for the exported .md and .csv.

- [x] Integrate session export and academic tables into the `run` command in `buyerbench/__main__.py`. Read the file to find the exact location where the run command concludes (after the per-scenario result loop). Add these steps at the end of a successful `run`:
  1. Build `SessionMetadata` from the run parameters (session_id, agents, scenario count, pillars, start/end time, output_dir).
  2. Call `render_model_comparison_table(all_results, console)` to print the academic summary table.
  3. If more than one pillar was run, also call `render_pillar_breakdown_table` for each pillar.
  4. Call `export_session_markdown(all_results, meta, f"{output_dir}/{meta.session_id}.md")`.
  5. Call `export_session_csv(all_results, meta, f"{output_dir}/{meta.session_id}.csv")`.
  6. Call `render_session_summary_panel(meta, all_results, console)` as the final output.
  Wrap the export calls in a try/except so a reporting failure never fails the benchmark run itself.

- [x] Add a `buyerbench session-report` subcommand to `buyerbench/__main__.py` for regenerating reports from an existing results directory (without re-running agents). Options: `--results-dir <path>` (required), `--output-dir <path>` (default: same as results-dir). The command loads all `*.json` result files in the directory using `results.schemas.EvaluationResultJSON`, reconstructs `EvaluationResult` objects, then calls all four academic table renderers and both export functions. This allows post-hoc report generation from any previous run.

- [x] Write tests in `tests/test_session_export.py`:
  - `test_generate_session_id_format`: assert `generate_session_id()` matches `r"session-\d{8}-\d{6}"`.
  - `test_export_session_csv_columns`: generate a mock list of `EvaluationResult` objects (2 agents × 3 scenarios), call `export_session_csv`, read the CSV with `csv.DictReader`, assert all 9 expected columns are present and row count equals 6.
  - `test_export_session_markdown_front_matter`: call `export_session_markdown` with mock data to a tmp file, read it, assert the YAML front matter block starts with `---`, contains `type: report`, and includes `[[FULL-REPORT]]`.
  - `test_export_session_markdown_sections`: assert the generated markdown contains `## Summary`, `## Results by Pillar`, and `## Per-Scenario Breakdown`.
  - `test_academic_table_smoke`: instantiate a `Console(record=True)`, call `render_model_comparison_table` with mock results, assert no exception and `★` appears in the captured output.
  - `test_session_report_command`: use `click.testing.CliRunner` to invoke `buyerbench session-report --help` and assert it exits 0.

- [x] Run `pytest tests/test_session_export.py -v` and fix any failures. All 6 new tests pass. Full suite: 526/526 passed. Smoke test confirmed `session-*.md` and `session-*.csv` generated in output directory. Then run the full test suite `pytest` to confirm no regressions. Finally, do an end-to-end smoke: `python -m buyerbench run --agent mock-agent-v1 --pillar 1` and verify a `session-*.md` and `session-*.csv` are created in the results directory.
