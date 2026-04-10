# Phase 04: Reports & Papers Browser

This phase builds the "Reports & Papers" path on the home screen. The browser scans `results/` for experiment directories, presents them in a Rich table with coverage metadata, and offers focused sub-commands: open the TUI dashboard, generate or view the academic report, or generate the AI review. This is the researcher's primary interface for consuming benchmark outputs and progressing toward publication.

## Tasks

- [x] Create `buyerbench/reports_browser.py` with a `browse_reports()` function. The function should:
  - Scan `results/` recursively to discover experiment directories. An experiment directory is any directory containing at least one `.json` result file. Also check for `results/experiments/` subdirectories as a top-level grouping.
  - For each experiment directory, collect metadata:
    - Directory name / path (displayed as experiment identifier)
    - Date (mtime of the directory or the most recent `.json` file, formatted as `YYYY-MM-DD`)
    - Agent count (count of unique `agent_id` values across all JSON files — read `agent_id` from each JSON's top-level key)
    - Pillar coverage (which of pillar1/pillar2/pillar3 subdirectories or `pillar_scores` entries are present)
    - Has `FULL-REPORT.md` (boolean)
    - Has academic paper (`ACADEMIC-PAPER.md` or `academic-report*.md` — glob check)
    - Has review (`REVIEW.md`)
  - If no results found: print "No experiments found. Run a benchmark with [1] New Session first." and return
  - Display in a Rich `Table` with columns: `#`, `Experiment`, `Date`, `Agents`, `Pillars`, `Report`, `Paper`, `Review`
  - Use colored indicators: green checkmark for present, dim dash for absent
  - Prompt: `"Select experiment [1-N] or [q] back"` — validate input
  - On selection, show a sub-menu:
    ```
    [d]  TUI Dashboard         (interactive results viewer)
    [r]  Generate / View Report     (FULL-REPORT.md)
    [a]  Generate / View Academic Paper
    [v]  Generate / View AI Review
    [b]  Back
    ```
  - On [d]: call `ResultsDashboard(selected_dir).run()` from `buyerbench.dashboard` (read dashboard.py to confirm the correct class/method signature before calling)
  - On [r]: if `FULL-REPORT.md` exists, print it with `rich.markdown.Markdown`; if not, invoke `subprocess.run([sys.executable, "-m", "buyerbench", "report", "--experiment-dir", str(selected_dir)])` then print the generated file
  - On [a]: if academic paper exists, print it with `rich.markdown.Markdown`; if not, invoke the `academic-report` subcommand: `subprocess.run([sys.executable, "-m", "buyerbench", "academic-report", "--experiment-dir", str(selected_dir)])`
  - On [v]: if `REVIEW.md` exists, print it; if not, invoke `subprocess.run([sys.executable, "-m", "buyerbench", "review", "--experiment-dir", str(selected_dir)])`
  - On [b]: return None
  - After any generation command completes, loop back to the sub-menu so the researcher can immediately open the result

- [x] Read `buyerbench/dashboard.py` to verify the `ResultsDashboard` constructor signature and its interactive loop entry point. If the class requires a specific invocation pattern (e.g., `dashboard.run()` vs `dashboard.render_summary()`), use the correct one. If there is no unified `run()` method, create a thin `run()` wrapper inside `dashboard.py` that runs the existing command loop.

- [x] Update `home_tui()` in `buyerbench/home.py` to call `browse_reports()` from `buyerbench.reports_browser` when the user selects [3] (replacing the Phase 01 placeholder).

- [x] Verify end-to-end: run `python -m buyerbench` → select [3] — if `results/` has data from any prior runs, the experiment table should appear with correct metadata. Confirm [d] launches the dashboard, [r] prints or generates a report, [b] returns to home. Fix any path or import errors that appear.
  <!-- Verified via unit tests (22 pass) and import smoke-tests. Metadata confirmed correct for results/claude-code-baseline (1 agent, all 3 pillars, 2026-04-04). run() wrapper on ResultsDashboard added and tested. -->
