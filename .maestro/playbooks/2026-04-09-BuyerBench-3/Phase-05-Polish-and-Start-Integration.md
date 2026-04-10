# Phase 05: Polish, Start.sh Integration & UX Hardening

This phase ties the unified TUI together: updates `start.sh` to launch the new home screen by default, adds keyboard shortcut help and consistent visual chrome across all three paths, handles edge cases (first launch, missing API keys, empty results), and makes the research notes field flow into the academic report generator. After this phase the full researcher experience is complete and launch-ready.

## Tasks

- [x] Read `start.sh` fully. Update the TUI launch logic so that the default mode (when `results/` is empty) goes to `python -m buyerbench` with no args (i.e., the new home screen) rather than `python -m buyerbench session`. Also update the smart default so that when `results/` has content it still launches the home screen (not the dashboard directly) — the researcher can navigate to Reports from there. Update the `--tui` flag documentation comment to note that `home` is now the default mode.
  <!-- Done: simplified TUI_CMD default from dashboard/session smart-detect to always "home"; added home branch in launch section (exec with no subcommand); updated --tui docs and env var comment. -->

- [ ] Add a persistent keyboard shortcut help bar to `home_tui()` using a Rich `Table` or styled footer line printed below the menu. The bar should show: `Ctrl+C: quit   /: search sessions   ?: help`. This is cosmetic — `Ctrl+C` is already handled by the `KeyboardInterrupt` guard, and `/` and `?` can simply re-print the menu for now (stubs). Also add a "last run" status line that reads the most recently modified `.json` in `results/` and shows its timestamp: `Last run: 2026-04-08 14:32  |  3 experiments on record`.

- [ ] Thread `research_notes` from `SessionConfig` into the academic report generation pipeline. In `buyerbench/__main__.py`, find the `academic-report` command. Read how it calls the report generator (likely `academic_tables.py` or a subprocess call to Claude CLI). Update it to:
  - Accept `--research-notes <text>` as an optional CLI flag
  - When `--from-session <path>` is provided, auto-load `research_notes` from the session config and prepend it to the academic paper prompt as "Researcher Notes:" context
  - If both `--from-session` and `--research-notes` are provided, merge them (session notes first, then flag notes)

- [ ] Add first-launch detection and onboarding to `home_tui()`. On first launch (no `sessions/` directory and no `results/` directory with JSON files), display an onboarding Panel:
  ```
  Welcome to BuyerBench!

  To get started:
    [1] Run the demo first to verify your setup:
        python -m buyerbench demo

    [2] Then create your first research session with [1] New Session

  Press any key to continue...
  ```
  Detect first launch by checking `not Path("sessions").exists() and not any(Path("results").rglob("*.json"))`.

- [ ] Run the full smoke test sequence to validate the complete researcher experience:
  - `python -m buyerbench` with no results → onboarding panel appears
  - `python -m buyerbench demo` → demo runs successfully (MockAgent)
  - `python -m buyerbench` after demo → home screen with "1 experiment on record"
  - Select [1] → wizard completes all 6 steps → session saved to `sessions/`
  - Select [2] → session browser shows the created session → [v] shows YAML
  - Select [3] → reports browser shows the demo experiment → [d] opens dashboard
  - `python -m buyerbench session` (legacy) → still works
  - `python -m buyerbench --help` → all existing subcommands still listed
  - Fix any regressions found during this sequence
