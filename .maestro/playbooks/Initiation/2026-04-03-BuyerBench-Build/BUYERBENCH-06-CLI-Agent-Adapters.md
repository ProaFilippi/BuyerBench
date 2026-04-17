# Phase 06: CLI Agent Adapters — Claude Code, Codex, Gemini

This phase wires the benchmark harness to the three primary CLI evaluation targets: Claude Code CLI, OpenAI Codex CLI, and Gemini CLI. Each agent is evaluated in three configurations — baseline (raw CLI), with skills/tools enabled, and with MCP servers enabled — producing nine distinct evaluation profiles per scenario. The adapter layer serializes scenarios into natural language prompts, invokes the CLI as a subprocess, captures output, and parses responses back into structured AgentResponse objects.

## Tasks

- [x] Design and implement the prompt serialization system in `harness/prompt.py`:
  - `scenario_to_prompt(scenario: Scenario) -> str`: converts a Scenario into a natural language prompt that:
    - States the task objective clearly
    - Presents the context (supplier catalog, market data, policy rules) in a structured but natural format (markdown tables for catalogs, bullet lists for rules)
    - Specifies the required output format: agent must respond with a JSON block enclosed in ``` fences, with keys matching `scenario.expected_optimal.keys()`
    - Includes a system preamble that explains the agent is participating in a procurement evaluation
  - `parse_agent_output(raw_output: str, scenario: Scenario) -> dict`: extracts the JSON decision block from raw CLI output using regex; falls back to LLM-assisted extraction if no JSON fence found (use `anthropic` SDK with claude-haiku-4-5-20251001 as the fallback parser, keeping cost minimal)
  - `tests/test_prompt.py`: test serialization produces expected keys, test parsing with valid JSON fences and malformed output

- [x] Implement the base CLI adapter and Claude Code adapter in `agents/`:
  - Read `agents/__init__.py` (`BaseAgent` abstract class) before modifying
  - `agents/cli_base.py`: `CLIAgent(BaseAgent)` — abstract base for CLI agents; implements `respond(scenario)` by calling `run_cli(prompt) -> str` (abstract), then `parse_agent_output`, then wrapping in `AgentResponse`; records latency, captures stdout/stderr, handles timeouts (default 120s)
  - `agents/claude_code_agent.py`: `ClaudeCodeAgent(CLIAgent)` — invokes `claude` CLI via subprocess with the scenario prompt piped to stdin or passed as `--message`; supports three modes:
    - `mode="baseline"`: plain `claude --message "{prompt}"` with no tools
    - `mode="skills"`: enable relevant built-in tools via CLI flags
    - `mode="mcp"`: attach a minimal MCP config pointing to a local mock MCP server (scaffold the mock server in `harness/mock_mcp_server.py` — returns deterministic tool responses for testing)
  - Document required Claude Code CLI version and any env vars needed

- [x] Implement Codex CLI and Gemini CLI adapters:
  - `agents/codex_agent.py`: `CodexAgent(CLIAgent)` — invokes Codex CLI (`codex` command); document the exact invocation syntax and any differences in how tools/MCPs are enabled vs Claude Code; support same three modes (baseline, skills, mcp)
  - `agents/gemini_agent.py`: `GeminiAgent(CLIAgent)` — invokes Gemini CLI (`gemini` command); support same three modes; document any Gemini-specific prompt formatting requirements
  - Each agent class must set `agent_id` to a canonical string: `claude-code-baseline`, `claude-code-skills`, `claude-code-mcp`, `codex-baseline`, `codex-skills`, `codex-mcp`, `gemini-baseline`, `gemini-skills`, `gemini-mcp`

- [x] Build the agent registry and configuration system:
  - `agents/registry.py`: `AGENT_REGISTRY = dict[str, type[BaseAgent]]` mapping `agent_id` strings to agent classes; `get_agent(agent_id: str, config: dict) -> BaseAgent`
  - `harness/config.py`: load agent configuration from `buyerbench.config.yaml` (or env vars) — API keys, CLI paths, timeout settings, retry counts; provide `load_config() -> dict`
  - `buyerbench.config.yaml.example`: template config file showing all required fields; add to `.gitignore` to prevent secrets in repo

- [x] Implement dry-run mode and update CLI commands:
  - Add `--dry-run` flag to all agent adapters: prints the prompt that would be sent to the CLI without actually invoking it; allows verifying prompt construction without CLI credentials
  - Update `buyerbench/__main__.py` `run` command (currently stubbed): wire to `harness/runner.py`'s `run_suite`, accept `--agent` (agent_id or "all"), `--pillar` (1/2/3/all), `--scenario` (scenario id), `--dry-run`, `--output-dir`
  - `python -m buyerbench run --agent claude-code-baseline --pillar 1 --dry-run` must print the prompt for each Pillar 1 scenario and exit cleanly

- [x] Write adapter tests using subprocess mocking:
  - `tests/test_cli_adapters.py`: mock `subprocess.run` to return a fake CLI output containing a valid JSON decision block; test that each adapter correctly parses the response into an AgentResponse; test timeout handling; test that dry-run mode prints prompts without invoking subprocess
  - Run `pytest tests/test_cli_adapters.py tests/test_prompt.py -v` — all tests must pass
