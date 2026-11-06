# Phase 03: Rerun / Continue Session Browser

This phase builds the "Rerun / Continue" path on the home screen. The browser scans the `sessions/` directory (and falls back to scanning `results/` for legacy session configs) for all `session-config.yaml` files, displays them in a Rich table with key metadata, and lets the researcher pick one to re-run as-is or modify before running. This gives researchers a clean audit trail of past experiments and a friction-free way to reproduce or iterate on runs.

## Tasks

- [x] Create `buyerbench/session_browser.py` with a `browse_sessions()` function. The function should:
  - Scan `sessions/` (and `results/` as fallback) recursively for all `session-config.yaml` files using `pathlib.Path.rglob("session-config.yaml")`
  - For each found config: call `load_session_config(path)` to load it, extract: experiment name (from `experiment_name` field or parent directory name), created_at, model count, scenario count (or "all" if empty), recurrence (or "one-shot")
  - If no sessions found: print a styled message "No sessions found. Create one with [1] New Session." and return None
  - Display the sessions in a Rich `Table` with columns: `#`, `Experiment`, `Created`, `Models`, `Scenarios`, `Recurrence`, `Has Results` (check for a matching results directory)
  - Color the `Has Results` column: green checkmark if results exist, dim dash if not
  - Prompt: `"Select session [1-N] or [q] back"` — validate input
  - On selection, show a sub-menu for the chosen session:
    ```
    [r]  Re-run as-is
    [m]  Modify (edit in wizard)
    [v]  View config (print YAML summary)
    [b]  Back
    ```
  - On [r]: invoke `subprocess.run([sys.executable, "-m", "buyerbench", "run", "--from-session", str(selected_path)])` and return
  - On [m]: call `wizard_new_session()` from `buyerbench.selector` pre-filled with the loaded config values (pass a `prefill: SessionConfig` parameter to the wizard — add this parameter in selector.py, defaulting to None; when provided, use the existing values as Prompt defaults via `Prompt.ask("...", default=value)`)
  - On [v]: print the raw YAML using `rich.syntax.Syntax` with `yaml` lexer inside a Panel, then loop back to the sub-menu
  - On [b]: return None

- [x] Update `wizard_new_session()` in `buyerbench/selector.py` to accept an optional `prefill: SessionConfig | None = None` parameter. When prefill is provided, use `Prompt.ask("Experiment name", default=prefill.experiment_name)` pattern for all Step 1 and Step 6 fields. For Steps 2-4 (model/skill/scenario selection), display a note "Pre-filled from existing session — press Enter to keep, or re-select" and skip re-entry if the user types nothing (keep existing selections). This enables the modify flow from the session browser.

- [x] Update `home_tui()` in `buyerbench/home.py` to call `browse_sessions()` from `buyerbench.session_browser` when the user selects [2] (replacing the Phase 01 placeholder).

- [x] Verify the browser end-to-end:
  - Create a dummy session config manually in `sessions/test-experiment-2026-04-09/session-config.yaml` with minimal valid content, then run `python -m buyerbench` → select [2] and confirm the session appears in the table
  - Confirm [v] shows styled YAML, [b] returns to home, [r] prints a run attempt (even if it fails due to missing API keys — the invocation itself should be correct)
  - Remove the test session after verification
