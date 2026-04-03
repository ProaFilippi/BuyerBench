"""OpenAI Codex CLI adapter for BuyerBench.

Invokes the ``codex`` CLI (OpenAI Codex CLI, formerly "openai-codex") in one
of three modes: baseline, skills, and mcp.

Invocation reference
--------------------
Codex CLI accepts the prompt as a positional argument or via ``--input``:

    codex "your prompt here"           # baseline
    codex --tools web_search "prompt"  # skills
    codex --mcp-config path "prompt"   # mcp

Requirements
------------
- Codex CLI installed: ``npm install -g @openai/codex`` (check ``codex --version``)
- ``OPENAI_API_KEY`` environment variable must be set

Differences from Claude Code
-----------------------------
- Prompt is passed as a positional argument (not ``--message``)
- Tool enablement uses ``--tools`` flag with comma-separated tool names
- MCP config path uses ``--mcp-config`` (same flag as Claude Code)
- No ``--print`` flag needed — Codex always writes to stdout in non-interactive mode
"""
from __future__ import annotations

from agents.cli_base import CLIAgent

_SKILLS_MODE_TOOLS = "web_search,file_read"
_MOCK_MCP_PORT = 7777


class CodexAgent(CLIAgent):
    """Agent adapter that drives the OpenAI Codex CLI (``codex`` command).

    Parameters
    ----------
    mode:
        One of ``"baseline"``, ``"skills"``, or ``"mcp"``.
    cli_path:
        Path to the ``codex`` binary.  Defaults to ``"codex"`` (PATH lookup).
    timeout:
        Subprocess timeout in seconds.
    dry_run:
        Print prompt without invoking the CLI.
    mcp_config_path:
        Path to a custom MCP config JSON file used in ``"mcp"`` mode.
    """

    MODES = ("baseline", "skills", "mcp")

    def __init__(
        self,
        mode: str = "baseline",
        cli_path: str = "codex",
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
        self.agent_id = f"codex-{mode}"

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
        """Construct the ``codex`` invocation for the current mode."""
        cmd = [self.cli_path]

        if self.mode == "baseline":
            pass  # No extra flags
        elif self.mode == "skills":
            cmd += ["--tools", _SKILLS_MODE_TOOLS]
        elif self.mode == "mcp":
            config_path = self.mcp_config_path or self._default_mcp_config_path()
            cmd += ["--mcp-config", config_path]

        # Prompt as positional argument (Codex convention)
        cmd.append(prompt)
        return cmd

    def _default_mcp_config_path(self) -> str:
        """Return path to a generated mock MCP config for Codex."""
        import json
        import tempfile

        config = {
            "mcpServers": {
                "buyerbench-mock": {
                    "url": f"http://localhost:{_MOCK_MCP_PORT}",
                    "transport": "http",
                }
            }
        }
        tmp = tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False, prefix="buyerbench_codex_mcp_"
        )
        json.dump(config, tmp)
        tmp.close()
        return tmp.name
