# Phase 04: Interactive Results Dashboard

This phase adds a post-run `dashboard` command that loads a results directory and presents a navigable Rich TUI for reviewing benchmark outcomes. The dashboard has four panels: session summary, model × skill comparison table, per-scenario breakdown (filterable by pillar), and a bias/security side-by-side view. The user can cycle through panels with keyboard shortcuts and filter by agent or pillar without leaving the terminal.

## Tasks

- [x] Read `results/academic_tables.py` (full file) and `buyerbench/__main__.py` (the `report` and `session-report` commands and the `_render_rich_dashboard` helper if it exists) before writing anything. Identify which table-rendering functions already exist and can be reused directly. Also read `results/session_export.py` for the `SessionMetadata` shape.

- [x] Create `buyerbench/dashboard.py` with a `ResultsDashboard` class:
  - Constructor: `__init__(results_dir: str)` — loads all `*.json` result files from the directory (skip `status=skipped`), computes aggregate scores per agent per pillar, stores as `self.results`, `self.agents`, `self.pillars`
  - `_load_results(results_dir) -> list[dict]` — reuse the same pattern as `review.py`'s `_load_results`
  - `_aggregate() -> dict` — group results by `agent_id`, compute mean score per pillar, overall mean, pass rate
  - Four render methods (each returns `None`, writes to a passed `Console`):
    - `render_summary(console)` — Rich Panel with session_id (from directory name), agent count, scenario count, best-performing agent, overall pass rate
    - `render_comparison(console)` — reuse `render_model_comparison_table()` from `results/academic_tables.py`
    - `render_scenarios(console, pillar_filter: int | None = None)` — reuse `render_pillar_breakdown_table()`, default shows all pillars; if `pillar_filter` is set, show only that pillar
    - `render_bias_security(console)` — side-by-side: left half calls `render_bias_table()`, right half calls a compact security summary table (agent → compliance_rate, violation_count)

- [x] Add `run_dashboard(results_dir: str) -> None` to `buyerbench/dashboard.py`:
  - Create `Console()` instance
  - Print navigation help bar: `[1] Summary  [2] Comparison  [3] Scenarios  [4] Bias/Security  [p1/p2/p3] Filter  [q] Quit`
  - Enter a `while True` input loop (use `input()` or `Prompt.ask()` from Rich):
    - `"1"` → clear + `render_summary(console)`
    - `"2"` → clear + `render_comparison(console)`
    - `"3"` → clear + `render_scenarios(console)`
    - `"p1"`, `"p2"`, `"p3"` → clear + `render_scenarios(console, pillar_filter=1/2/3)`
    - `"4"` → clear + `render_bias_security(console)`
    - `"q"` or `"quit"` → break
    - Any other input → reprint the help bar
  - On startup, automatically call `render_summary(console)` so the user immediately sees something

- [x] Add a `dashboard` command to `buyerbench/__main__.py`:
  - Usage: `python -m buyerbench dashboard --results-dir <dir>`
  - Import and call `run_dashboard(results_dir)` from `buyerbench.dashboard`
  - If `results_dir` does not exist or contains zero JSON files, print a helpful error and exit with code 1
  - Add `--results-dir` as a required argument (no default, to avoid confusion with stale results)

- [x] Wire a post-run dashboard launch option into the `run` command in `buyerbench/__main__.py`:
  - Add `--dashboard / --no-dashboard` flag (default: `--no-dashboard`)
  - After all results are written and session export is done, if `--dashboard` is set, print "Launching results dashboard..." and call `run_dashboard(output_dir)`
  - This makes the full end-to-end flow: `python -m buyerbench run --from-session session-config.yaml --dashboard`

- [x] Write tests in `tests/test_dashboard.py` using sample fixture data:
  - Create a `@pytest.fixture` that writes 3 fake result JSON files to a `tmp_path` dir (one per pillar)
  - Test `ResultsDashboard(tmp_path)._load_results()` returns 3 items
  - Test `ResultsDashboard(tmp_path)._aggregate()` returns a dict keyed by agent_id with pillar scores
  - Test `render_summary(Console(file=io.StringIO()))` does not raise and produces output containing "Session"
  - Run `pytest tests/test_dashboard.py -v` and confirm all pass
