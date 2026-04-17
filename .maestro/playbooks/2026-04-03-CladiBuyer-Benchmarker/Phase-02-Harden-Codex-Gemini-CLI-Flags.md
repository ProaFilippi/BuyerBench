# Phase 02: Audit and Harden Codex & Gemini CLI Adapter Flags

The Codex and Gemini CLI adapters were built from assumed flag names, but those CLIs evolve independently and a wrong flag silently degrades to no-tools mode — the agent runs but without the capabilities under test. This phase verifies the actual CLI interfaces by running `--help` on each, corrects any discrepancies in the adapter command builders, and tightens the corresponding unit tests so flag regressions are caught automatically.

## Tasks

- [ ] Audit the actual Codex CLI interface and compare to `agents/codex_agent.py`:
  - Run `codex --help 2>&1 || true` and `codex --version 2>&1 || true` to capture actual flags
  - Read `agents/codex_agent.py` lines ~81-95 (command construction) and note every flag currently used (`--tools`, `--mcp-config`, positional prompt, etc.)
  - Cross-check each flag against the `--help` output:
    - Is `--tools` the correct flag name or is it `--enable-tools`, `--tool`, or something else?
    - Is the tools value a comma-separated string, space-separated, or repeated flags?
    - Is the prompt passed as a bare positional arg or via a named flag?
    - Is `--mcp-config` supported, or is it `--mcp`, `--mcp-server`, or a different shape?
  - If Codex is not installed, note that and record the expected interface from the latest public docs for the `openai/codex-cli` repository
  - Document findings inline as a comment block at the top of `agents/codex_agent.py`

- [ ] Audit the actual Gemini CLI interface and compare to `agents/gemini_agent.py`:
  - Run `gemini --help 2>&1 || true` and `gemini --version 2>&1 || true`
  - Read `agents/gemini_agent.py` lines ~96-113 and note every flag used (`--model`, `--tools`, `--mcp-config`, `--prompt`, etc.)
  - Cross-check: Is `--prompt` correct or is it `-p` / positional? Is `--tools` the right name? Is `--mcp-config` supported?
  - If Gemini CLI is not installed, note that and record expected interface from `google-gemini/gemini-cli` repository docs
  - Document findings inline as a comment block at the top of `agents/gemini_agent.py`

- [ ] Apply corrections to `agents/codex_agent.py` based on audit findings:
  - Update the command list in the `_build_command()` method (or equivalent) to use verified flag names and argument formats
  - If the prompt must be passed differently (e.g., via stdin or a different flag), update the subprocess call accordingly
  - Preserve all existing functional behavior — only change flag names/shapes where the audit found them wrong

- [ ] Apply corrections to `agents/gemini_agent.py` based on audit findings:
  - Same approach as the Codex fix above
  - Pay special attention to the `--tools` argument format, which differs between Gemini CLI versions

- [ ] Update `tests/test_cli_adapters.py` to assert the corrected flag shapes:
  - Read the existing tests for `CodexAgent` and `GeminiAgent` — find assertions that check command list construction
  - Update expected command lists to match the verified flag names from the audit
  - Add a test case for each agent that asserts an invalid/legacy flag name does NOT appear in the built command (negative assertion as a regression guard)
  - Do NOT change Claude Code agent tests

- [ ] Run the adapter tests and confirm they pass:
  - Run: `pytest tests/test_cli_adapters.py -v 2>&1`
  - If tests fail due to the flag corrections, re-read the adapter and test code carefully and resolve the mismatch before marking done
