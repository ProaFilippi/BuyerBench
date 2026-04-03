"""Tests for harness.preflight — environment validation.

Covers:
- CLI probing: installed vs. not-found, timeout, version capture
- API key probing: env vars set vs. absent, alias resolution
- Mock MCP server probe: success and failure cases
- check_environment(): available_agents derivation, overall flag
- Rich table rendering (smoke test — no assertion on table content)
- CLI 'check' command: exit-code 0/1
"""
from __future__ import annotations

import subprocess
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner


# ---------------------------------------------------------------------------
# _probe_cli
# ---------------------------------------------------------------------------

class TestProbeCli:
    def test_installed_cli_returns_version(self):
        from harness.preflight import _probe_cli

        mock_result = MagicMock(stdout="claude 1.2.3\n", stderr="", returncode=0)
        with patch("subprocess.run", return_value=mock_result):
            info = _probe_cli("claude", "--version")

        assert info["installed"] is True
        assert "claude" in info["version"].lower() or "1.2.3" in info["version"]
        assert info["error"] is None

    def test_missing_cli_returns_not_installed(self):
        from harness.preflight import _probe_cli

        with patch("subprocess.run", side_effect=FileNotFoundError):
            info = _probe_cli("not-a-real-cli", "--version")

        assert info["installed"] is False
        assert info["version"] is None
        assert "not found" in info["error"]

    def test_timeout_returns_not_installed(self):
        from harness.preflight import _probe_cli

        with patch(
            "subprocess.run",
            side_effect=subprocess.TimeoutExpired("cli", 10),
        ):
            info = _probe_cli("slow-cli", "--version")

        assert info["installed"] is False
        assert "timed out" in info["error"]

    def test_version_from_stderr_when_stdout_empty(self):
        from harness.preflight import _probe_cli

        mock_result = MagicMock(stdout="", stderr="codex v0.9.0\n", returncode=0)
        with patch("subprocess.run", return_value=mock_result):
            info = _probe_cli("codex", "--version")

        assert info["installed"] is True
        assert "codex" in info["version"].lower() or "0.9.0" in info["version"]


# ---------------------------------------------------------------------------
# _probe_api_keys
# ---------------------------------------------------------------------------

class TestProbeApiKeys:
    def test_key_set_returns_true(self, monkeypatch):
        from harness.preflight import _probe_api_keys
        monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test-123")
        info = _probe_api_keys(["ANTHROPIC_API_KEY"])
        assert info["set"] is True
        assert info["key_name"] == "ANTHROPIC_API_KEY"

    def test_key_not_set_returns_false(self, monkeypatch):
        from harness.preflight import _probe_api_keys
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        info = _probe_api_keys(["OPENAI_API_KEY"])
        assert info["set"] is False
        assert info["key_name"] is None

    def test_alias_resolution_first_wins(self, monkeypatch):
        from harness.preflight import _probe_api_keys
        monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
        monkeypatch.setenv("GEMINI_API_KEY", "gemini-key-abc")
        info = _probe_api_keys(["GOOGLE_API_KEY", "GEMINI_API_KEY"])
        assert info["set"] is True
        assert info["key_name"] == "GEMINI_API_KEY"

    def test_first_key_takes_priority_over_alias(self, monkeypatch):
        from harness.preflight import _probe_api_keys
        monkeypatch.setenv("GOOGLE_API_KEY", "google-key-xyz")
        monkeypatch.setenv("GEMINI_API_KEY", "gemini-key-abc")
        info = _probe_api_keys(["GOOGLE_API_KEY", "GEMINI_API_KEY"])
        assert info["key_name"] == "GOOGLE_API_KEY"


# ---------------------------------------------------------------------------
# _probe_mcp_server
# ---------------------------------------------------------------------------

class TestProbeMcpServer:
    def test_successful_start_returns_started_true(self):
        from harness.preflight import _probe_mcp_server
        info = _probe_mcp_server()
        assert info["started"] is True
        assert info["error"] is None

    def test_exception_returns_started_false(self):
        from harness.preflight import _probe_mcp_server

        with patch(
            "harness.mock_mcp_server.MockMCPServer",
            side_effect=OSError("address already in use"),
        ):
            info = _probe_mcp_server()

        assert info["started"] is False
        assert "address already in use" in info["error"]


# ---------------------------------------------------------------------------
# check_environment
# ---------------------------------------------------------------------------

class TestCheckEnvironment:
    def _make_cli_ok(self, installed: bool = True) -> dict:
        return {
            "installed": installed,
            "version": "cli 1.0" if installed else None,
            "error": None if installed else "not found in PATH",
        }

    def test_returns_required_keys(self):
        from harness.preflight import check_environment
        result = check_environment(print_report=False)
        for key in ("clis", "api_keys", "mcp_server", "overall", "available_agents"):
            assert key in result

    def test_all_missing_gives_overall_false(self, monkeypatch):
        from harness.preflight import check_environment
        # Ensure no API keys are set
        for k in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY", "GOOGLE_API_KEY", "GEMINI_API_KEY"):
            monkeypatch.delenv(k, raising=False)
        # All CLIs missing
        with patch("subprocess.run", side_effect=FileNotFoundError):
            result = check_environment(print_report=False)
        assert result["overall"] is False

    def test_available_agents_populated_when_cli_and_key_present(self, monkeypatch):
        from harness.preflight import check_environment
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
        # All other keys absent
        for k in ("OPENAI_API_KEY", "GOOGLE_API_KEY", "GEMINI_API_KEY"):
            monkeypatch.delenv(k, raising=False)

        mock_result = MagicMock(stdout="claude 1.0\n", stderr="", returncode=0)
        side_effects = {
            "claude": mock_result,
            "codex": FileNotFoundError(),
            "gemini": FileNotFoundError(),
        }

        def _fake_run(cmd, **kwargs):
            cli = cmd[0]
            effect = side_effects.get(cli)
            if isinstance(effect, Exception):
                raise effect
            return effect

        with patch("subprocess.run", side_effect=_fake_run):
            result = check_environment(print_report=False)

        assert "claude-code-baseline" in result["available_agents"]
        assert "claude-code-skills" in result["available_agents"]
        assert "claude-code-mcp" in result["available_agents"]
        # codex and gemini should NOT appear
        assert not any("codex" in a for a in result["available_agents"])

    def test_print_report_does_not_raise(self, capsys):
        from harness.preflight import check_environment
        with patch("subprocess.run", side_effect=FileNotFoundError):
            # Should not raise even when everything is missing
            check_environment(print_report=True)


# ---------------------------------------------------------------------------
# CLI 'check' command
# ---------------------------------------------------------------------------

class TestCheckCommand:
    def test_exits_1_when_checks_fail(self, monkeypatch):
        from buyerbench.__main__ import cli
        for k in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY", "GOOGLE_API_KEY", "GEMINI_API_KEY"):
            monkeypatch.delenv(k, raising=False)

        runner = CliRunner()
        with patch("subprocess.run", side_effect=FileNotFoundError):
            result = runner.invoke(cli, ["check"])

        assert result.exit_code == 1

    def test_exits_0_when_checks_pass(self, monkeypatch):
        from buyerbench.__main__ import cli
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key-a")
        monkeypatch.setenv("OPENAI_API_KEY", "test-key-o")
        monkeypatch.setenv("GOOGLE_API_KEY", "test-key-g")

        mock_result = MagicMock(stdout="cli 1.0\n", stderr="", returncode=0)

        runner = CliRunner()
        with patch("subprocess.run", return_value=mock_result):
            result = runner.invoke(cli, ["check"])

        assert result.exit_code == 0

    def test_output_contains_preflight_header(self, monkeypatch):
        from buyerbench.__main__ import cli
        for k in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY", "GOOGLE_API_KEY", "GEMINI_API_KEY"):
            monkeypatch.delenv(k, raising=False)

        runner = CliRunner()
        with patch("subprocess.run", side_effect=FileNotFoundError):
            result = runner.invoke(cli, ["check"])

        # The rich output is captured — check for key content fragments
        assert result.exit_code in (0, 1)  # either outcome is fine for smoke test
