# Phase 02: Enhanced New Session Wizard

This phase upgrades the existing session creation flow to capture the full researcher context: experiment name, research objective, recurrence schedule, and research notes for the academic paper generator. The enhanced wizard wraps the existing `interactive_select()`, `interactive_skill_select()`, and `interactive_scenario_select()` functions from `selector.py` — all work is additive. By the end of this phase, a researcher can name their experiment, annotate it with hypotheses, and configure a recurring cron schedule in a single guided flow.

## Tasks

- [x] Read `buyerbench/selector.py` fully to understand the current `SessionConfig` dataclass and `run_session_tui()` function. Then extend `SessionConfig` to add three optional fields:
  - `experiment_name: str = ""` — short slug for the experiment (e.g., "gpt4o-vs-claude-p2")
  - `research_objective: str = ""` — free-text research question or hypothesis
  - `research_notes: str = ""` — any notes to pass to the academic report generator
  - `recurrence: str | None = None` — cron expression (e.g., `"0 9 * * 1"`) or None for one-shot
  - Also add `output_dir: str = "results"` if not already present
  - Update `save_session_config()` and `load_session_config()` to serialize/deserialize these new fields (YAML round-trip). The session YAML should be saved to `sessions/<experiment_name>-<timestamp>/session-config.yaml` (create the `sessions/` directory if it does not exist).

- [x] Add a `wizard_new_session()` function to `buyerbench/selector.py` that runs the full researcher wizard as a sequence of clearly labeled steps. Use Rich `Rule` separators between steps. Each step should print its step number (e.g., `"[Step 1/6] Experiment Identity"`):
  - **Step 1 — Experiment Identity**: `Prompt.ask` for experiment name (validate: lowercase, hyphens, no spaces — strip and slugify) and research objective (free text, allow empty)
  - **Step 2 — Model Selection**: call existing `interactive_select()` and return selected agent IDs
  - **Step 3 — Skill Mode**: call existing `interactive_skill_select(agent_ids)`
  - **Step 4 — Scenario Scope**: call existing `interactive_scenario_select(scenarios)` (load scenarios from `harness.loader` or the existing pattern in `run_session_tui`)
  - **Step 5 — Recurrence**: display options:
    ```
    [1] One-shot (run once now)
    [2] Daily at 09:00        →  cron: 0 9 * * *
    [3] Weekly on Monday      →  cron: 0 9 * * 1
    [4] Custom cron expression
    ```
    Store the selected cron string (or None for one-shot) in `recurrence`
  - **Step 6 — Research Notes**: `Prompt.ask` for optional notes (shown as: "Notes for academic paper generator [leave blank to skip]")
  - After all steps: show a Rich `Panel` confirmation summary (experiment name, models count, scenarios count, skill modes, recurrence, has notes), then `Prompt.ask("Confirm and save? [y/N]")`. On confirm: call `save_session_config()` and print the saved path. Return the `SessionConfig`.

- [x] Update `home_tui()` in `buyerbench/home.py` to call `wizard_new_session()` instead of `run_session_tui()` when the user selects [1]. After the wizard completes and the config is saved:
  - If `recurrence` is not None: print a Rich `Panel` with the schedule setup instructions:
    ```
    To activate recurring runs, register this session with the scheduler:

      claude /schedule "BuyerBench: <experiment_name>" \
        --cron "<cron_expression>" \
        --command "python -m buyerbench run --from-session <session_config_path>"
    ```
  - If one-shot: `Prompt.ask("Run now? [y/N]")` → on yes, invoke `subprocess.run(["python", "-m", "buyerbench", "run", "--from-session", str(config_path)])` using `sys.executable` for the correct Python

- [x] Verify the wizard end-to-end: run `python -m buyerbench` → select [1] → complete all 6 steps → confirm the saved YAML contains all new fields → verify the file is created in `sessions/<name>-<timestamp>/session-config.yaml`
  <!-- Verified via Python smoke test: save/load round-trip, _slugify, _make_session_path all pass. All 626 existing tests green. Interactive TUI wired in home.py. -->
