"""Tests for CLI agent adapters using subprocess mocking.

Covers:
- ClaudeCodeAgent, CodexAgent, GeminiAgent — correct command construction,
  output parsing, timeout propagation
- CLIAgent dry-run mode (prints prompt, returns empty AgentResponse)
- Agent registry: get_agent() returns the right class with correct agent_id
- harness.config: load_config() applies env var overrides
"""
from __future__ import annotations

import subprocess
from unittest.mock import MagicMock, patch

import pytest

from buyerbench.models import Difficulty, Pillar, Scenario, ScenarioVariant


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_scenario(**overrides) -> Scenario:
    defaults = dict(
        id="test-p1-cli",
        title="CLI Adapter Test Scenario",
        pillar=Pillar.PILLAR1,
        variant=ScenarioVariant.BASELINE,
        description="Test scenario for CLI adapter validation.",
        task_objective="Select the supplier with the lowest unit price.",
        constraints=[],
        expected_optimal={"selected_supplier": "SupplierB", "unit_price": 38.5},
        security_requirements=[],
        tags=["pillar1"],
        difficulty=Difficulty.EASY,
        context={},
        evaluation_weights={},
    )
    defaults.update(overrides)
    return Scenario(**defaults)


FAKE_CLI_OUTPUT = (
    'Based on my analysis:\n'
    '```json\n'
    '{"selected_supplier": "SupplierB", "unit_price": 38.5}\n'
    '```\n'
)

_MOCK_RUN_RESULT = MagicMock(
    stdout=FAKE_CLI_OUTPUT,
    stderr="",
    returncode=0,
)


# ---------------------------------------------------------------------------
# ClaudeCodeAgent
# ---------------------------------------------------------------------------

class TestClaudeCodeAgent:
    def test_baseline_invocation(self):
        from agents.claude_code_agent import ClaudeCodeAgent
        agent = ClaudeCodeAgent(mode="baseline", cli_path="claude")
        assert agent.agent_id == "claude-code-baseline"

        with patch("subprocess.run", return_value=_MOCK_RUN_RESULT) as mock_sub:
            response = agent.respond(_make_scenario())

        cmd = mock_sub.call_args[0][0]
        assert cmd[0] == "claude"
        assert "--print" in cmd
        assert "--message" in cmd

    def test_skills_mode_includes_allowed_tools(self):
        from agents.claude_code_agent import ClaudeCodeAgent
        agent = ClaudeCodeAgent(mode="skills", cli_path="claude")

        with patch("subprocess.run", return_value=_MOCK_RUN_RESULT) as mock_sub:
            agent.respond(_make_scenario())

        cmd = mock_sub.call_args[0][0]
        assert "--allowedTools" in cmd

    def test_mcp_mode_includes_mcp_config(self, tmp_path):
        from agents.claude_code_agent import ClaudeCodeAgent
        cfg = tmp_path / "mcp.json"
        cfg.write_text('{"mcpServers": {}}')
        agent = ClaudeCodeAgent(mode="mcp", mcp_config_path=str(cfg))

        with patch("subprocess.run", return_value=_MOCK_RUN_RESULT) as mock_sub:
            agent.respond(_make_scenario())

        cmd = mock_sub.call_args[0][0]
        assert "--mcp-config" in cmd

    def test_parses_json_from_output(self):
        from agents.claude_code_agent import ClaudeCodeAgent
        agent = ClaudeCodeAgent(mode="baseline")

        with patch("subprocess.run", return_value=_MOCK_RUN_RESULT):
            response = agent.respond(_make_scenario())

        assert response.decisions == {"selected_supplier": "SupplierB", "unit_price": 38.5}

    def test_latency_recorded(self):
        from agents.claude_code_agent import ClaudeCodeAgent
        agent = ClaudeCodeAgent(mode="baseline")

        with patch("subprocess.run", return_value=_MOCK_RUN_RESULT):
            response = agent.respond(_make_scenario())

        assert response.latency_ms >= 0.0

    def test_raw_output_stored(self):
        from agents.claude_code_agent import ClaudeCodeAgent
        agent = ClaudeCodeAgent(mode="baseline")

        with patch("subprocess.run", return_value=_MOCK_RUN_RESULT):
            response = agent.respond(_make_scenario())

        assert response.raw_output == FAKE_CLI_OUTPUT

    def test_invalid_mode_raises(self):
        from agents.claude_code_agent import ClaudeCodeAgent
        with pytest.raises(ValueError, match="mode must be one of"):
            ClaudeCodeAgent(mode="invalid")

    def test_timeout_propagated_to_subprocess(self):
        from agents.claude_code_agent import ClaudeCodeAgent
        agent = ClaudeCodeAgent(mode="baseline", timeout=30)

        with patch("subprocess.run", return_value=_MOCK_RUN_RESULT) as mock_sub:
            agent.respond(_make_scenario())

        assert mock_sub.call_args.kwargs["timeout"] == 30

    def test_timeout_exception_propagates(self):
        from agents.claude_code_agent import ClaudeCodeAgent
        agent = ClaudeCodeAgent(mode="baseline", timeout=1)

        with patch("subprocess.run", side_effect=subprocess.TimeoutExpired("claude", 1)):
            with pytest.raises(subprocess.TimeoutExpired):
                agent.respond(_make_scenario())


# ---------------------------------------------------------------------------
# CodexAgent
# ---------------------------------------------------------------------------

class TestCodexAgent:
    def test_baseline_invocation(self):
        from agents.codex_agent import CodexAgent
        agent = CodexAgent(mode="baseline", cli_path="codex")
        assert agent.agent_id == "codex-baseline"

        with patch("subprocess.run", return_value=_MOCK_RUN_RESULT) as mock_sub:
            agent.respond(_make_scenario())

        cmd = mock_sub.call_args[0][0]
        assert cmd[0] == "codex"
        # Prompt should be last positional arg
        assert "Select the supplier" in cmd[-1]

    def test_skills_mode_includes_tools_flag(self):
        from agents.codex_agent import CodexAgent
        agent = CodexAgent(mode="skills")

        with patch("subprocess.run", return_value=_MOCK_RUN_RESULT) as mock_sub:
            agent.respond(_make_scenario())

        cmd = mock_sub.call_args[0][0]
        assert "--tools" in cmd

    def test_mcp_mode_includes_config(self, tmp_path):
        from agents.codex_agent import CodexAgent
        cfg = tmp_path / "mcp.json"
        cfg.write_text('{"mcpServers": {}}')
        agent = CodexAgent(mode="mcp", mcp_config_path=str(cfg))

        with patch("subprocess.run", return_value=_MOCK_RUN_RESULT) as mock_sub:
            agent.respond(_make_scenario())

        cmd = mock_sub.call_args[0][0]
        assert "--mcp-config" in cmd

    def test_invalid_mode_raises(self):
        from agents.codex_agent import CodexAgent
        with pytest.raises(ValueError):
            CodexAgent(mode="turbo")


# ---------------------------------------------------------------------------
# GeminiAgent
# ---------------------------------------------------------------------------

class TestGeminiAgent:
    def test_baseline_invocation(self):
        from agents.gemini_agent import GeminiAgent
        agent = GeminiAgent(mode="baseline", cli_path="gemini")
        assert agent.agent_id == "gemini-baseline"

        with patch("subprocess.run", return_value=_MOCK_RUN_RESULT) as mock_sub:
            agent.respond(_make_scenario())

        cmd = mock_sub.call_args[0][0]
        assert cmd[0] == "gemini"
        assert "--prompt" in cmd

    def test_skills_mode_includes_tools_flag(self):
        from agents.gemini_agent import GeminiAgent
        agent = GeminiAgent(mode="skills")

        with patch("subprocess.run", return_value=_MOCK_RUN_RESULT) as mock_sub:
            agent.respond(_make_scenario())

        cmd = mock_sub.call_args[0][0]
        assert "--tools" in cmd

    def test_model_flag_included_when_set(self):
        from agents.gemini_agent import GeminiAgent
        agent = GeminiAgent(mode="baseline", model="gemini-2.0-flash")

        with patch("subprocess.run", return_value=_MOCK_RUN_RESULT) as mock_sub:
            agent.respond(_make_scenario())

        cmd = mock_sub.call_args[0][0]
        assert "--model" in cmd
        assert "gemini-2.0-flash" in cmd

    def test_invalid_mode_raises(self):
        from agents.gemini_agent import GeminiAgent
        with pytest.raises(ValueError):
            GeminiAgent(mode="ultra")


# ---------------------------------------------------------------------------
# Dry-run mode
# ---------------------------------------------------------------------------

class TestDryRunMode:
    def test_dry_run_does_not_invoke_subprocess(self, capsys):
        from agents.claude_code_agent import ClaudeCodeAgent
        agent = ClaudeCodeAgent(mode="baseline", dry_run=True)

        with patch("subprocess.run") as mock_sub:
            response = agent.respond(_make_scenario())

        mock_sub.assert_not_called()

    def test_dry_run_prints_prompt(self, capsys):
        from agents.claude_code_agent import ClaudeCodeAgent
        agent = ClaudeCodeAgent(mode="baseline", dry_run=True)
        scenario = _make_scenario()
        agent.respond(scenario)
        captured = capsys.readouterr()
        assert scenario.task_objective in captured.out

    def test_dry_run_returns_empty_response(self):
        from agents.claude_code_agent import ClaudeCodeAgent
        agent = ClaudeCodeAgent(mode="baseline", dry_run=True)
        response = agent.respond(_make_scenario())
        assert response.decisions == {}
        assert response.latency_ms == 0.0
        assert "dry-run" in response.reasoning_trace

    def test_dry_run_works_for_codex(self, capsys):
        from agents.codex_agent import CodexAgent
        agent = CodexAgent(mode="baseline", dry_run=True)
        scenario = _make_scenario()

        with patch("subprocess.run") as mock_sub:
            response = agent.respond(scenario)

        mock_sub.assert_not_called()
        assert response.decisions == {}

    def test_dry_run_works_for_gemini(self, capsys):
        from agents.gemini_agent import GeminiAgent
        agent = GeminiAgent(mode="baseline", dry_run=True)
        scenario = _make_scenario()

        with patch("subprocess.run") as mock_sub:
            response = agent.respond(scenario)

        mock_sub.assert_not_called()
        assert response.decisions == {}


# ---------------------------------------------------------------------------
# Agent registry
# ---------------------------------------------------------------------------

class TestAgentRegistry:
    def test_all_nine_cli_ids_registered(self):
        from agents.registry import AGENT_REGISTRY
        expected_ids = {
            "claude-code-baseline", "claude-code-skills", "claude-code-mcp",
            "codex-baseline", "codex-skills", "codex-mcp",
            "gemini-baseline", "gemini-skills", "gemini-mcp",
        }
        assert expected_ids.issubset(set(AGENT_REGISTRY.keys()))

    def test_mock_agent_registered(self):
        from agents.registry import AGENT_REGISTRY
        assert "mock-agent-v1" in AGENT_REGISTRY

    def test_get_agent_returns_correct_type(self):
        from agents.claude_code_agent import ClaudeCodeAgent
        from agents.registry import get_agent
        agent = get_agent("claude-code-baseline", {})
        assert isinstance(agent, ClaudeCodeAgent)
        assert agent.agent_id == "claude-code-baseline"

    def test_get_agent_respects_mode(self):
        from agents.claude_code_agent import ClaudeCodeAgent
        from agents.registry import get_agent
        agent = get_agent("claude-code-mcp", {})
        assert isinstance(agent, ClaudeCodeAgent)
        assert agent.mode == "mcp"

    def test_get_agent_unknown_id_raises(self):
        from agents.registry import get_agent
        with pytest.raises(KeyError, match="Unknown agent_id"):
            get_agent("nonexistent-agent", {})

    def test_get_agent_dry_run_from_config(self):
        from agents.registry import get_agent
        agent = get_agent("codex-baseline", {"dry_run": True})
        assert agent.dry_run is True

    def test_get_mock_agent(self):
        from agents.mock import MockAgent
        from agents.registry import get_agent
        agent = get_agent("mock-agent-v1", {})
        assert isinstance(agent, MockAgent)


# ---------------------------------------------------------------------------
# Config loading
# ---------------------------------------------------------------------------

class TestLoadConfig:
    def test_returns_dict_with_required_keys(self):
        from harness.config import load_config
        config = load_config(path="/nonexistent/path.yaml")
        for key in ("claude_code", "codex", "gemini", "timeout", "dry_run"):
            assert key in config

    def test_anthropic_api_key_env_override(self, monkeypatch):
        from harness.config import load_config
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key-claude")
        config = load_config(path="/nonexistent/path.yaml")
        assert config["claude_code"]["api_key"] == "test-key-claude"

    def test_openai_api_key_env_override(self, monkeypatch):
        from harness.config import load_config
        monkeypatch.setenv("OPENAI_API_KEY", "test-key-openai")
        config = load_config(path="/nonexistent/path.yaml")
        assert config["codex"]["api_key"] == "test-key-openai"

    def test_google_api_key_env_override(self, monkeypatch):
        from harness.config import load_config
        monkeypatch.setenv("GOOGLE_API_KEY", "test-key-google")
        config = load_config(path="/nonexistent/path.yaml")
        assert config["gemini"]["api_key"] == "test-key-google"

    def test_timeout_env_override(self, monkeypatch):
        from harness.config import load_config
        monkeypatch.setenv("BUYERBENCH_TIMEOUT", "60")
        config = load_config(path="/nonexistent/path.yaml")
        assert config["timeout"] == 60

    def test_dry_run_env_override_true(self, monkeypatch):
        from harness.config import load_config
        monkeypatch.setenv("BUYERBENCH_DRY_RUN", "1")
        config = load_config(path="/nonexistent/path.yaml")
        assert config["dry_run"] is True

    def test_dry_run_env_override_false(self, monkeypatch):
        from harness.config import load_config
        monkeypatch.setenv("BUYERBENCH_DRY_RUN", "0")
        config = load_config(path="/nonexistent/path.yaml")
        assert config["dry_run"] is False

    def test_loads_yaml_file(self, tmp_path):
        from harness.config import load_config
        cfg_file = tmp_path / "test.yaml"
        cfg_file.write_text("timeout: 45\nclaude_code:\n  cli_path: /usr/local/bin/claude\n")
        config = load_config(path=str(cfg_file))
        assert config["timeout"] == 45
        assert config["claude_code"]["cli_path"] == "/usr/local/bin/claude"


# ---------------------------------------------------------------------------
# Mock MCP Server
# ---------------------------------------------------------------------------

class TestMockMCPServer:
    def test_server_starts_and_stops(self):
        import socket
        import time
        from harness.mock_mcp_server import MOCK_MCP_PORT, MockMCPServer

        # Use a random port to avoid conflicts
        with MockMCPServer(port=0) as server:
            # Server should be running (thread alive)
            assert server._thread is not None
            assert server._thread.is_alive()

    def test_health_check_endpoint(self):
        import json
        import urllib.request
        from harness.mock_mcp_server import MockMCPServer

        with MockMCPServer(port=17777) as server:
            resp = urllib.request.urlopen("http://127.0.0.1:17777/")
            data = json.loads(resp.read())
            assert data["status"] == "ok"

    def test_tool_call_returns_deterministic_response(self):
        import json
        import urllib.request
        from harness.mock_mcp_server import MockMCPServer

        payload = json.dumps({"id": 1, "name": "list_suppliers"}).encode()
        req = urllib.request.Request(
            "http://127.0.0.1:17778/",
            data=payload,
            method="POST",
            headers={"Content-Type": "application/json"},
        )
        with MockMCPServer(port=17778) as server:
            resp = urllib.request.urlopen(req)
            data = json.loads(resp.read())
            content_text = data["result"]["content"][0]["text"]
            tool_result = json.loads(content_text)
            assert "suppliers" in tool_result
            assert len(tool_result["suppliers"]) > 0

    def test_context_manager_cleans_up(self):
        from harness.mock_mcp_server import MockMCPServer
        server = MockMCPServer(port=17779)
        with server:
            pass
        # After __exit__, server should be stopped
        assert server._server is None
