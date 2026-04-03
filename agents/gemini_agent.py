"""Google Gemini CLI adapter for BuyerBench.

Invokes the ``gemini`` CLI in one of three modes: baseline, skills, and mcp.

Invocation reference
--------------------
The Gemini CLI (Google's ``gemini`` command-line tool) accepts prompts via
``--prompt`` or stdin:

    gemini --prompt "your prompt here"                 # baseline
    gemini --tools google_search --prompt "..."        # skills
    gemini --mcp-config path/to/config.json --prompt "..."  # mcp

Gemini-specific prompt formatting notes
----------------------------------------
- Gemini performs well with structured markdown sections
- Explicitly labelling the JSON output requirement ("Output ONLY valid JSON")
  improves parse reliability compared to other CLIs
- The ``--model`` flag can pin a specific Gemini model version; defaults to
  the CLI's configured default (typically gemini-2.0-flash or later)

Requirements
------------
- Gemini CLI installed: ``npm install -g @google/gemini-cli``
  (check ``gemini --version``)
- ``GOOGLE_API_KEY`` or ``GEMINI_API_KEY`` environment variable must be set

Differences from Claude Code
-----------------------------
- Prompt is passed via ``--prompt`` flag (not ``--message``)
- Tool enablement uses ``--tools`` (same flag pattern as Codex)
- No ``--print`` flag needed — non-interactive by default when ``--prompt`` is given
"""
from __future__ import annotations

import json
import tempfile

from agents.cli_base import CLIAgent

_SKILLS_MODE_TOOLS = "google_search"
_MOCK_MCP_PORT = 7777


class GeminiAgent(CLIAgent):
    """Agent adapter that drives the Google Gemini CLI (``gemini`` command).

    Parameters
    ----------
    mode:
        One of ``"baseline"``, ``"skills"``, or ``"mcp"``.
    cli_path:
        Path to the ``gemini`` binary.  Defaults to ``"gemini"`` (PATH lookup).
    timeout:
        Subprocess timeout in seconds.
    dry_run:
        Print prompt without invoking the CLI.
    mcp_config_path:
        Path to a custom MCP config JSON file used in ``"mcp"`` mode.
    model:
        Override the Gemini model version.  ``None`` uses the CLI default.
    """

    MODES = ("baseline", "skills", "mcp")

    def __init__(
        self,
        mode: str = "baseline",
        cli_path: str = "gemini",
        timeout: int = 120,
        dry_run: bool = False,
        mcp_config_path: str | None = None,
        model: str | None = None,
    ) -> None:
        if mode not in self.MODES:
            raise ValueError(f"mode must be one of {self.MODES!r}, got {mode!r}")
        super().__init__(timeout=timeout, dry_run=dry_run)
        self.mode = mode
        self.cli_path = cli_path
        self.mcp_config_path = mcp_config_path
        self.model = model
        self.agent_id = f"gemini-{mode}"

    # ------------------------------------------------------------------
    # CLIAgent interface
    # ------------------------------------------------------------------

    def run_cli(self, prompt: str) -> str:
        cmd = self._build_command(prompt)
        return self._invoke_subprocess(cmd)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _build_command(self, prompt: str) -> list[str]:
        """Construct the ``gemini`` invocation for the current mode."""
        cmd = [self.cli_path]

        if self.model:
            cmd += ["--model", self.model]

        if self.mode == "baseline":
            pass  # No extra flags
        elif self.mode == "skills":
            cmd += ["--tools", _SKILLS_MODE_TOOLS]
        elif self.mode == "mcp":
            config_path = self.mcp_config_path or self._write_mock_mcp_config()
            cmd += ["--mcp-config", config_path]

        # Gemini uses --prompt flag for non-interactive prompts
        cmd += ["--prompt", prompt]
        return cmd

    def _write_mock_mcp_config(self) -> str:
        """Write a temp JSON file pointing at the local mock MCP server."""
        config = {
            "mcpServers": {
                "buyerbench-mock": {
                    "url": f"http://localhost:{_MOCK_MCP_PORT}",
                    "transport": "http",
                }
            }
        }
        tmp = tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".json",
            delete=False,
            prefix="buyerbench_gemini_mcp_",
        )
        json.dump(config, tmp)
        tmp.close()
        return tmp.name
