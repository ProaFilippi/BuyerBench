# Phase 01: Unified Researcher Home Screen

This phase delivers the core experience: a Rich-powered home screen that launches when `python -m buyerbench` is run with no subcommand. The screen presents three clearly numbered paths (keyboard navigation only, no mouse, no Textual), routes to existing commands for sessions and dashboard, and gives the researcher an immediate sense of professional-grade tooling. By the end of this phase, running `python -m buyerbench` shows a branded, navigable home screen that works end-to-end.

## Tasks

- [x] Create `buyerbench/home.py` with a `home_tui()` function. The function should:
  - Print a Rich `Panel` header with the BuyerBench title ("BuyerBench — AI Buyer Agent Benchmark") and a one-line tagline ("Researcher-grade evaluation framework")
  - Scan `results/` for any `.json` result files and display a status line: "X experiments on record" (or "No experiments yet" if empty)
  - Display a numbered menu using Rich `Table` or styled `Text`:
    ```
    [1]  New Session          Configure and launch a new benchmark run
    [2]  Rerun / Continue     Pick and re-run an existing session
    [3]  Reports & Papers     Browse results, dashboards, and academic outputs
    [q]  Quit
    ```
  - Read a single keypress from the user using `Prompt.ask("Select", choices=["1","2","3","q"], show_choices=False)`
  - On [1]: call `run_session_tui()` from `buyerbench.selector`, then offer to immediately run with `python -m buyerbench run --from-session <saved-path>` (print the command and ask yes/no)
  - On [2]: print "Rerun browser coming in Phase 03 — launching session picker for now" and call `run_session_tui()` as a fallback
  - On [3]: print "Reports browser coming in Phase 04 — launching dashboard for now" and call the dashboard entry point from `buyerbench.dashboard` (`ResultsDashboard(results_dir).run()` or equivalent)
  - On [q]: print "Goodbye." and return
  - Wrap everything in a `try/except KeyboardInterrupt` that exits cleanly with a goodbye message

- [x] Modify `buyerbench/__main__.py` so that the top-level Click group's `invoke_without_command=True` path calls `home_tui()` when no subcommand is given. Read the current `__main__.py` to find the existing Click group definition (look for `@click.group` or `@cli.result_callback`) and add the no-subcommand guard. The pattern is:
  ```python
  @cli.result_callback()
  def process_result(result, **kwargs):
      pass

  # OR at the group level:
  @click.group(invoke_without_command=True)
  @click.pass_context
  def cli(ctx):
      if ctx.invoked_subcommand is None:
          from buyerbench.home import home_tui
          home_tui()
  ```
  Read `__main__.py` first to understand the exact current group structure before editing.

- [x] Verify the home screen works end-to-end:
  - Run `python -m buyerbench` with no args and confirm the home screen renders (use `--help` to also confirm existing subcommands still work)
  - Run `python -m buyerbench session` to confirm the existing session command still functions
  - Run `python -m buyerbench dashboard` to confirm dashboard still works
  - Fix any import errors or missing dependencies that surface during testing
