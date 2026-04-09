# Phase 01: Unified TUI Session Config

This phase extends the existing `buyerbench/selector.py` model picker into a full three-pane session-configuration TUI: (1) model selection, (2) per-model skill toggle, (3) scenario multi-select. The result is a working `python -m buyerbench session` command that guides the user through the entire pre-run configuration and saves a unified `session-config.yaml`. By the end of this phase, a user can launch the TUI, configure their experiment, and see a rich summary panel — everything needed to feed the runner in Phase 02.

## Tasks

- [x] Read `buyerbench/selector.py` (full file) and `buyerbench/__main__.py` (full file) to understand the existing `interactive_select()` TUI, `save_selection()`, `SessionMetadata`, and the `select` CLI command before writing anything new.
  <!-- Completed 2026-04-08: Read both files in full. selector.py provides display_catalog_table(), interactive_select(), save_selection(), load_selection() with a module-level Rich Console. __main__.py has click CLI group with check/demo/select/run/report/review/session-report commands. harness/loader.py load_all_scenarios() discovered for Step 3. -->

- [x] Add a `SessionConfig` dataclass and session persistence helpers to `buyerbench/selector.py`:
  - `@dataclass class AgentSlot: agent_id: str; skill_mode: str  # "baseline" | "skills" | "mcp"`
  - `@dataclass class SessionConfig: agents: list[AgentSlot]; scenario_ids: list[str]; created_at: str`
  - `save_session_config(config: SessionConfig, path: str = "session-config.yaml") -> None` — serialize to YAML with top-level keys `agents` (list of `{agent_id, skill_mode}`), `scenario_ids`, `created_at`
  - `load_session_config(path: str) -> SessionConfig` — deserialize and return `SessionConfig`
  <!-- Completed 2026-04-08: Added AgentSlot and SessionConfig dataclasses plus save_session_config/load_session_config helpers to selector.py. Added tests/test_session_tui.py with 8 tests covering round-trip, YAML structure, edge cases (empty agents/scenarios, default paths). All 534 tests pass. -->

- [x] Add `interactive_skill_select(agent_ids: list[str]) -> dict[str, str]` to `buyerbench/selector.py`. This function shows a Rich table listing each selected agent with its current skill mode. Commands: type an agent number + mode abbreviation (e.g. `1 s` for skills, `1 b` for baseline, `1 m` for mcp), `a b` to set all to baseline, `done` to confirm. Display the table after each change. Return a dict mapping `agent_id → skill_mode`. Default all agents to `"baseline"`.
  <!-- Completed 2026-04-08: Added interactive_skill_select() to selector.py with full command grammar (N b/s/m, a b/s/m, done, q). Added _display_skill_table() helper and _SKILL_LABELS/_SKILL_ABBREVS constants. Added TestInteractiveSkillSelect class with 11 tests covering defaults, per-agent set, batch-set, override, unknown input, out-of-range, quit, empty input. All 545 tests pass. -->

- [ ] Add `interactive_scenario_select(scenarios: list) -> list[str]` to `buyerbench/selector.py`. Each scenario has `.id`, `.title`, `.pillar`, `.difficulty`, `.tags`. Show a Rich table with columns: #, ID, Title, Pillar, Difficulty, Selected (✓/·). Support commands: `1,3,5` (toggle), `a` (all), `c` (clear), `p1`/`p2`/`p3` (select all in pillar), `done` (confirm), `q` (quit). Return list of selected scenario IDs.

- [ ] Add `run_session_tui() -> SessionConfig` to `buyerbench/selector.py` that chains the three steps:
  1. Print a Rich header panel: "BuyerBench — Session Configuration"
  2. Step 1: Call `interactive_select()` for model selection; print step header "Step 1/3 — Select Models"
  3. Step 2: Call `interactive_skill_select(selected_agent_ids)` for per-model skill modes; print "Step 2/3 — Configure Skills"
  4. Step 3: Load all scenarios via `harness.loader.load_all_scenarios("scenarios/")`, call `interactive_scenario_select(scenarios)`; print "Step 3/3 — Select Scenarios"
  5. Build and return `SessionConfig` with `created_at=datetime.utcnow().isoformat()`
  6. Print a Rich summary Panel showing: selected agents (with skill mode), scenario count, pillars covered

- [ ] Register a new `session` CLI command in `buyerbench/__main__.py`:
  ```
  python -m buyerbench session [--output session-config.yaml]
  ```
  The command calls `run_session_tui()`, saves the result via `save_session_config()`, and prints a confirmation message with the output path and a hint: "Run `python -m buyerbench run --from-session <path>` to execute."

- [ ] Verify the new command works end-to-end:
  - Run `python -m buyerbench session --output /tmp/test-session.yaml` in dry-run/smoke fashion by importing and calling `save_session_config` + `load_session_config` round-trip in a quick `pytest` test: `tests/test_session_tui.py`
  - Test that `load_session_config(save_session_config(...))` round-trips correctly for a 2-agent, 3-scenario config
  - Run `pytest tests/test_session_tui.py -v` and confirm all tests pass
