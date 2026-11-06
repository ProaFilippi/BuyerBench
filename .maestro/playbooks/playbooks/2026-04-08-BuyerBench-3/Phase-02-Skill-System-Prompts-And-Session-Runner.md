# Phase 02: Skill System Prompts and Session-Aware Runner

This phase wires the session config from Phase 01 into the run engine. It introduces a `buyerbench/skills.py` module defining system prompts for each skill mode, extends the agent classes to accept and inject those prompts, and adds a `--from-session` flag to the `run` command. After this phase, running `python -m buyerbench run --from-session session-config.yaml` executes the full benchmark with per-agent skill customization.

## Tasks

- [x] Read `agents/cli_base.py`, `agents/claude_code_agent.py`, `agents/openrouter_agent.py`, and `agents/registry.py` in full before writing any agent changes. Understand how `respond()`, `run_cli()`, and `get_agent()` interact, and where to inject a system prompt without breaking existing behavior.

- [x] Create `buyerbench/skills.py` with a `SKILL_PROMPTS` dict and helper:
  - `SKILL_PROMPTS: dict[str, str]` — three keys: `"baseline"` (empty string, no injection), `"skills"` (a procurement-focused system prompt that instructs the agent to use available tools for web search, price lookup, and supplier verification), `"mcp"` (a system prompt focused on invoking MCP procurement tools for quote retrieval, PO issuance, and payment authorization)
  - Write the `"skills"` prompt as 3–5 sentences covering: act as a procurement specialist, use provided tools to verify supplier data, compare prices, and justify decisions with evidence
  - Write the `"mcp"` prompt similarly but emphasizing MCP tool calls for structured data retrieval
  - `get_skill_prompt(mode: str) -> str` — returns the prompt string or raises `ValueError` for unknown modes

- [x] Extend `agents/cli_base.py` to support system prompt injection:
  - Add optional `system_prompt: str = ""` parameter to `__init__`
  - In `respond()` (or `run_cli()`), if `system_prompt` is non-empty, prepend it to the scenario prompt using a `[SYSTEM]\n{system_prompt}\n[/SYSTEM]\n\n` delimiter before the task prompt
  - Ensure this is backwards-compatible (default empty string means no change to existing behavior)

- [x] Extend `agents/openrouter_agent.py` to support system prompt injection:
  - Add optional `system_prompt: str = ""` to `__init__`
  - If non-empty, add a `{"role": "system", "content": system_prompt}` message at the front of the messages list in the HTTP request body
  - Default empty means single user message (existing behavior)

- [x] Extend `agents/registry.py` `get_agent()` to accept and pass through `skill_prompt`:
  - Add optional `skill_prompt: str = ""` parameter to `get_agent(agent_id, config, skill_prompt="")`
  - When constructing any agent (CLI or OpenRouter), pass `system_prompt=skill_prompt`
  - Existing callers with no `skill_prompt` continue to work unchanged

- [x] Add `--from-session` flag to the `run` command in `buyerbench/__main__.py`:
  - `--from-session PATH` — load `SessionConfig` via `load_session_config(path)` from `buyerbench/selector.py`
  - Extract `agent_ids` and per-agent `skill_mode` from `config.agents`
  - Load skill prompts via `get_skill_prompt(mode)` from `buyerbench/skills.py`
  - Filter scenarios to only those in `config.scenario_ids` (if the list is non-empty)
  - Pass `skill_prompt` per agent into `get_agent(agent_id, config, skill_prompt=...)`
  - `--from-session` and `--agent` should be mutually exclusive; raise a `UsageError` if both are given
  - Copy the session-config.yaml into the output directory alongside results for provenance

- [x] Write tests in `tests/test_skills.py`:
  - Test `get_skill_prompt("baseline")` returns an empty string
  - Test `get_skill_prompt("skills")` returns a non-empty string containing relevant procurement terms
  - Test `get_skill_prompt("invalid")` raises `ValueError`
  - Test that `CLIAgent` with a non-empty `system_prompt` prepends it correctly (mock `_invoke_subprocess`)
  - Run `pytest tests/test_skills.py -v` and confirm all pass
