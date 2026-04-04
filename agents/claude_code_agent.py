"""Claude Code CLI adapter for BuyerBench.

Invokes the ``claude`` CLI in one of three modes:
- **baseline**: plain ``claude --print --message "..."`` with no extra tools
- **skills**:   same invocation but with built-in tool access enabled via
                ``--allowedTools``
- **mcp**:      attaches a local MCP server config so the agent can call
                mock procurement tools via the Model Context Protocol

Requirements
------------
- Claude Code CLI >= 1.0  (``claude --version`` to verify)
- ``ANTHROPIC_API_KEY`` environment variable must be set

CLI reference: https://docs.anthropic.com/en/docs/claude-code/cli-usage
"""
from __future__ import annotations

import json
import subprocess
import tempfile

from agents.cli_base import CLIAgent

# Skills exposed to the agent in "skills" mode.  These map to built-in Claude
# Code tools relevant to procurement research tasks.
_SKILLS_MODE_TOOLS = "WebSearch,WebFetch"

# Port used by the mock MCP server (kept in sync with mock_mcp_server.py).
_MOCK_MCP_PORT = 7777


class ClaudeCodeAgent(CLIAgent):
    """Agent adapter that drives the Claude Code CLI (``claude`` command).

    Parameters
    ----------
    mode:
        One of ``"baseline"``, ``"skills"``, or ``"mcp"``.
    cli_path:
        Path to the ``claude`` binary.  Defaults to ``"claude"`` (PATH lookup).
    timeout:
        Subprocess timeout in seconds.
    dry_run:
        Print prompt without invoking the CLI.
    mcp_config_path:
        Path to a custom MCP config JSON file.  When *None* in ``"mcp"`` mode
        a temporary config pointing to the local mock server is generated.
    """

    MODES = ("baseline", "skills", "mcp")

    def __init__(
        self,
        mode: str = "baseline",
        cli_path: str = "claude",
        timeout: int = 120,
        dry_run: bool = False,
        mcp_config_path: str | None = None,
    ) -> None:
        if mode not in self.MODES:
            raise ValueError(f"mode must be one of {self.MODES!r}, got {mode!r}")
        super().__init__(timeout=timeout, dry_run=dry_run)
        self.mode = mode
        self.cli_path = cli_path
        self.mcp_config_path = mcp_config_path
        self.agent_id = f"claude-code-{mode}"

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
        """Construct the ``claude`` invocation for the current mode."""
        # --print  → non-interactive; output goes to stdout
        # --message → the user turn content
        cmd = [self.cli_path, "--print", prompt]

        if self.mode == "baseline":
            # No tools; keep the invocation as clean as possible
            pass
        elif self.mode == "skills":
            cmd += ["--allowedTools", _SKILLS_MODE_TOOLS]
        elif self.mode == "mcp":
            config_path = self.mcp_config_path or self._write_mock_mcp_config()
            cmd += ["--mcp-config", config_path]

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
            prefix="buyerbench_mcp_",
        )
        json.dump(config, tmp)
        tmp.close()
        return tmp.name
