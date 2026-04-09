"""Tests for buyerbench/skills.py and system-prompt injection in agent adapters."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from buyerbench.models import Difficulty, Pillar, Scenario, ScenarioVariant


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_scenario(**overrides) -> Scenario:
    defaults = dict(
        id="test-skills-scenario",
        title="Skills Test Scenario",
        pillar=Pillar.PILLAR1,
        variant=ScenarioVariant.BASELINE,
        description="Scenario for skill prompt injection tests.",
        task_objective="Select the cheapest supplier.",
        constraints=[],
        expected_optimal={"selected_supplier": "SupplierA", "unit_price": 10.0},
        security_requirements=[],
        tags=["pillar1"],
        difficulty=Difficulty.EASY,
        context={},
        evaluation_weights={},
    )
    defaults.update(overrides)
    return Scenario(**defaults)


_MOCK_RUN_RESULT = MagicMock(
    stdout='```json\n{"selected_supplier": "SupplierA", "unit_price": 10.0}\n```',
    stderr="",
    returncode=0,
)


# ---------------------------------------------------------------------------
# get_skill_prompt tests
# ---------------------------------------------------------------------------

class TestGetSkillPrompt:
    def test_baseline_returns_empty_string(self):
        from buyerbench.skills import get_skill_prompt
        assert get_skill_prompt("baseline") == ""

    def test_skills_returns_non_empty_string(self):
        from buyerbench.skills import get_skill_prompt
        prompt = get_skill_prompt("skills")
        assert isinstance(prompt, str)
        assert len(prompt) > 0

    def test_skills_prompt_contains_procurement_terms(self):
        from buyerbench.skills import get_skill_prompt
        prompt = get_skill_prompt("skills").lower()
        # Must reference procurement-related concepts
        assert any(term in prompt for term in ["procurement", "supplier", "price"])

    def test_mcp_returns_non_empty_string(self):
        from buyerbench.skills import get_skill_prompt
        prompt = get_skill_prompt("mcp")
        assert isinstance(prompt, str)
        assert len(prompt) > 0

    def test_mcp_prompt_references_mcp_tools(self):
        from buyerbench.skills import get_skill_prompt
        prompt = get_skill_prompt("mcp").lower()
        assert "mcp" in prompt

    def test_invalid_mode_raises_value_error(self):
        from buyerbench.skills import get_skill_prompt
        with pytest.raises(ValueError, match="Unknown skill mode"):
            get_skill_prompt("invalid")

    def test_invalid_mode_error_lists_valid_modes(self):
        from buyerbench.skills import get_skill_prompt
        with pytest.raises(ValueError) as exc_info:
            get_skill_prompt("turbo")
        assert "baseline" in str(exc_info.value)

    def test_skill_prompts_dict_has_three_keys(self):
        from buyerbench.skills import SKILL_PROMPTS
        assert set(SKILL_PROMPTS.keys()) == {"baseline", "skills", "mcp"}


# ---------------------------------------------------------------------------
# CLIAgent system_prompt injection tests
# ---------------------------------------------------------------------------

class TestCLIAgentSystemPrompt:
    def test_system_prompt_prepended_to_prompt(self):
        """When system_prompt is set, it appears in the text sent to run_cli."""
        from agents.claude_code_agent import ClaudeCodeAgent

        agent = ClaudeCodeAgent(
            mode="baseline",
            system_prompt="You are a procurement specialist.",
        )
        assert agent.system_prompt == "You are a procurement specialist."

        captured_prompts: list[str] = []

        def fake_run_cli(prompt: str) -> str:
            captured_prompts.append(prompt)
            return _MOCK_RUN_RESULT.stdout

        agent.run_cli = fake_run_cli  # type: ignore[method-assign]
        agent.respond(_make_scenario())

        assert len(captured_prompts) == 1
        full_prompt = captured_prompts[0]
        assert "[SYSTEM]" in full_prompt
        assert "You are a procurement specialist." in full_prompt
        assert "[/SYSTEM]" in full_prompt

    def test_system_prompt_appears_before_task(self):
        """The [SYSTEM] block must come before the task content."""
        from agents.claude_code_agent import ClaudeCodeAgent

        agent = ClaudeCodeAgent(mode="baseline", system_prompt="SYS_CONTENT")
        captured: list[str] = []
        agent.run_cli = lambda p: (captured.append(p), _MOCK_RUN_RESULT.stdout)[1]  # type: ignore[method-assign]
        agent.respond(_make_scenario())

        prompt = captured[0]
        sys_pos = prompt.index("[SYSTEM]")
        task_pos = prompt.index("Select the cheapest supplier")
        assert sys_pos < task_pos

    def test_empty_system_prompt_does_not_inject(self):
        """Default empty system_prompt → prompt is unchanged (no [SYSTEM] block)."""
        from agents.claude_code_agent import ClaudeCodeAgent

        agent = ClaudeCodeAgent(mode="baseline")  # system_prompt=""
        captured: list[str] = []
        agent.run_cli = lambda p: (captured.append(p), _MOCK_RUN_RESULT.stdout)[1]  # type: ignore[method-assign]
        agent.respond(_make_scenario())

        assert "[SYSTEM]" not in captured[0]

    def test_system_prompt_via_subprocess_mock(self):
        """Verify injection works end-to-end through _invoke_subprocess path."""
        from agents.claude_code_agent import ClaudeCodeAgent

        agent = ClaudeCodeAgent(mode="baseline", system_prompt="INJECT_ME")

        with patch("subprocess.run", return_value=_MOCK_RUN_RESULT) as mock_sub:
            agent.respond(_make_scenario())

        # The prompt passed to the CLI should contain the injection
        cmd = mock_sub.call_args[0][0]
        # --message is followed by the full prompt string
        msg_idx = cmd.index("--message")
        full_prompt = cmd[msg_idx + 1]
        assert "INJECT_ME" in full_prompt
        assert "[SYSTEM]" in full_prompt


# ---------------------------------------------------------------------------
# OpenRouterAgent system_prompt injection tests
# ---------------------------------------------------------------------------

class TestOpenRouterAgentSystemPrompt:
    def test_system_prompt_adds_system_message(self):
        """Non-empty system_prompt inserts {"role": "system"} at front of messages."""
        from agents.openrouter_agent import OpenRouterAgent

        agent = OpenRouterAgent("openai/gpt-4o", system_prompt="Be a buyer.")

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": '{"selected_supplier": "A"}'}}]
        }
        mock_response.raise_for_status = MagicMock()

        with patch("requests.post", return_value=mock_response) as mock_post:
            agent.respond(_make_scenario())

        body = mock_post.call_args.kwargs["json"]
        messages = body["messages"]
        assert messages[0]["role"] == "system"
        assert messages[0]["content"] == "Be a buyer."
        assert messages[1]["role"] == "user"

    def test_empty_system_prompt_sends_single_user_message(self):
        """Empty system_prompt → only a user message (existing behavior)."""
        from agents.openrouter_agent import OpenRouterAgent

        agent = OpenRouterAgent("openai/gpt-4o")

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": '{"selected_supplier": "A"}'}}]
        }
        mock_response.raise_for_status = MagicMock()

        with patch("requests.post", return_value=mock_response) as mock_post:
            agent.respond(_make_scenario())

        body = mock_post.call_args.kwargs["json"]
        messages = body["messages"]
        assert len(messages) == 1
        assert messages[0]["role"] == "user"


# ---------------------------------------------------------------------------
# Registry skill_prompt pass-through tests
# ---------------------------------------------------------------------------

class TestRegistrySkillPrompt:
    def test_get_agent_passes_skill_prompt_to_cli_agent(self):
        from agents.registry import get_agent
        from agents.claude_code_agent import ClaudeCodeAgent

        agent = get_agent("claude-code-baseline", {}, skill_prompt="SKILL_TEXT")
        assert isinstance(agent, ClaudeCodeAgent)
        assert agent.system_prompt == "SKILL_TEXT"

    def test_get_agent_passes_skill_prompt_to_openrouter(self):
        from agents.registry import get_agent
        from agents.openrouter_agent import OpenRouterAgent

        agent = get_agent(
            "openrouter-openai-gpt-4o", {}, skill_prompt="OR_SKILL"
        )
        assert isinstance(agent, OpenRouterAgent)
        assert agent.system_prompt == "OR_SKILL"

    def test_get_agent_default_skill_prompt_is_empty(self):
        from agents.registry import get_agent
        from agents.claude_code_agent import ClaudeCodeAgent

        agent = get_agent("claude-code-baseline", {})
        assert isinstance(agent, ClaudeCodeAgent)
        assert agent.system_prompt == ""
