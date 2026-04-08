"""Tests for the OpenRouter HTTP agent adapter.

Covers:
- Agent ID slug formatting (slashes → dashes)
- Dry-run mode returns stub response without network calls
- All 10 model variants registered in AGENT_REGISTRY
- get_agent() instantiates OpenRouterAgent for openrouter-* IDs
- Happy-path HTTP POST body structure (requests.post mocked)
"""
from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import pytest

from buyerbench.models import Difficulty, Pillar, Scenario, ScenarioVariant
from agents.openrouter_agent import OpenRouterAgent
from agents.registry import AGENT_REGISTRY, OPENROUTER_MODEL_MAP, get_agent


# ---------------------------------------------------------------------------
# Shared scenario factory
# ---------------------------------------------------------------------------

def _make_scenario(**overrides) -> Scenario:
    defaults = dict(
        id="test-scenario",
        title="Test Supplier Selection",
        pillar=Pillar.PILLAR1,
        variant=ScenarioVariant.BASELINE,
        description="Select the best supplier.",
        task_objective="Choose the supplier with the lowest total cost.",
        constraints=["Budget must not exceed $10,000"],
        expected_optimal={"selected_supplier": "SupplierA", "unit_price": 90.0},
        security_requirements=[],
        tags=["pillar1"],
        difficulty=Difficulty.EASY,
        context={
            "suppliers": [
                {"name": "SupplierA", "unit_price": 90.0, "quality_score": 0.9,
                 "delivery_reliability": 0.85},
                {"name": "SupplierB", "unit_price": 80.0, "quality_score": 0.7,
                 "delivery_reliability": 0.70},
            ]
        },
        evaluation_weights={},
    )
    defaults.update(overrides)
    return Scenario(**defaults)


# ---------------------------------------------------------------------------
# OpenRouterAgent unit tests
# ---------------------------------------------------------------------------

class TestOpenRouterAgent:
    def test_openrouter_agent_id_format(self):
        """Slashes in model_id must be replaced by dashes in agent_id."""
        agent = OpenRouterAgent("openai/gpt-4o")
        assert agent.agent_id == "openrouter-openai-gpt-4o"

    def test_agent_id_multi_slash(self):
        """Multi-segment model IDs (e.g. org/model-name) collapse correctly."""
        agent = OpenRouterAgent("meta-llama/llama-3.1-405b-instruct")
        assert agent.agent_id == "openrouter-meta-llama-llama-3.1-405b-instruct"

    def test_openrouter_agent_dry_run(self):
        """Dry-run mode must return [dry-run] stub without any HTTP call."""
        agent = OpenRouterAgent("openai/gpt-4o", dry_run=True)
        scenario = _make_scenario()
        response = agent.respond(scenario)
        assert response.raw_output == "[dry-run]"
        assert response.decisions == {}
        assert response.scenario_id == "test-scenario"
        assert response.agent_id == "openrouter-openai-gpt-4o"

    def test_dry_run_no_network_call(self):
        """Confirm requests.post is never called in dry-run mode."""
        agent = OpenRouterAgent("openai/gpt-4o", dry_run=True)
        scenario = _make_scenario()
        with patch("requests.post") as mock_post:
            agent.respond(scenario)
            mock_post.assert_not_called()

    def test_openrouter_model_id_stored(self):
        agent = OpenRouterAgent("cohere/command-r-plus")
        assert agent.model_id == "cohere/command-r-plus"

    def test_default_timeout(self):
        agent = OpenRouterAgent("openai/gpt-4o")
        assert agent.timeout == 120

    def test_custom_timeout(self):
        agent = OpenRouterAgent("openai/gpt-4o", timeout=30)
        assert agent.timeout == 30


# ---------------------------------------------------------------------------
# Registry tests
# ---------------------------------------------------------------------------

class TestOpenRouterRegistry:
    def test_all_10_registered(self):
        """All 10 openrouter-* agent IDs must appear in AGENT_REGISTRY."""
        expected = [
            "openrouter-openai-gpt-4o",
            "openrouter-anthropic-claude-3.5-sonnet",
            "openrouter-google-gemini-pro-1.5",
            "openrouter-meta-llama-llama-3.1-405b-instruct",
            "openrouter-mistralai-mistral-large",
            "openrouter-deepseek-deepseek-chat",
            "openrouter-qwen-qwen-2.5-72b-instruct",
            "openrouter-cohere-command-r-plus",
            "openrouter-mistralai-mixtral-8x22b-instruct",
            "openrouter-01-ai-yi-large",
        ]
        for agent_id in expected:
            assert agent_id in AGENT_REGISTRY, f"{agent_id} missing from AGENT_REGISTRY"

    def test_openrouter_model_map_has_10_entries(self):
        assert len(OPENROUTER_MODEL_MAP) == 10

    def test_model_map_values_contain_slash(self):
        """All OpenRouter model IDs must use org/model format."""
        for agent_id, model_id in OPENROUTER_MODEL_MAP.items():
            assert "/" in model_id, f"{agent_id} maps to {model_id!r} — missing '/'"

    def test_get_agent_openrouter(self):
        """get_agent() must return an OpenRouterAgent for openrouter-* IDs."""
        agent = get_agent("openrouter-openai-gpt-4o", {"dry_run": True})
        assert isinstance(agent, OpenRouterAgent)
        assert agent.model_id == "openai/gpt-4o"
        assert agent.dry_run is True

    def test_get_agent_model_id_mapping(self):
        """get_agent() must pass the correct model_id from OPENROUTER_MODEL_MAP."""
        agent = get_agent("openrouter-cohere-command-r-plus", {})
        assert isinstance(agent, OpenRouterAgent)
        assert agent.model_id == "cohere/command-r-plus"

    def test_get_agent_unknown_raises(self):
        with pytest.raises(KeyError):
            get_agent("openrouter-nonexistent-model")


# ---------------------------------------------------------------------------
# HTTP POST integration (mocked)
# ---------------------------------------------------------------------------

class TestOpenRouterHTTP:
    def _make_mock_response(self, content: str) -> MagicMock:
        """Build a fake requests.Response with the given message content."""
        mock_resp = MagicMock()
        mock_resp.raise_for_status = MagicMock()
        mock_resp.json.return_value = {
            "choices": [
                {"message": {"content": content}}
            ]
        }
        return mock_resp

    def test_post_body_contains_model_and_messages(self, monkeypatch):
        """The POST body must include 'model' and 'messages' keys."""
        monkeypatch.setenv("OPENROUTER_API_KEY", "test-key-abc")
        agent = OpenRouterAgent("openai/gpt-4o")
        scenario = _make_scenario()

        json_content = json.dumps({"selected_supplier": "SupplierA", "unit_price": 90.0})
        mock_resp = self._make_mock_response(f"```json\n{json_content}\n```")

        with patch("requests.post", return_value=mock_resp) as mock_post:
            response = agent.respond(scenario)
            mock_post.assert_called_once()
            _, kwargs = mock_post.call_args
            body = kwargs.get("json") or mock_post.call_args[0][1] if len(mock_post.call_args[0]) > 1 else kwargs["json"]
            assert "model" in body
            assert "messages" in body
            assert body["model"] == "openai/gpt-4o"
            assert body["messages"][0]["role"] == "user"

    def test_post_uses_auth_header(self, monkeypatch):
        """Authorization header must include the API key."""
        monkeypatch.setenv("OPENROUTER_API_KEY", "sk-or-test-12345")
        agent = OpenRouterAgent("openai/gpt-4o")
        scenario = _make_scenario()

        json_content = json.dumps({"selected_supplier": "SupplierA", "unit_price": 90.0})
        mock_resp = self._make_mock_response(f"```json\n{json_content}\n```")

        with patch("requests.post", return_value=mock_resp) as mock_post:
            agent.respond(scenario)
            _, kwargs = mock_post.call_args
            headers = kwargs.get("headers", {})
            assert "Authorization" in headers
            assert "sk-or-test-12345" in headers["Authorization"]

    def test_http_error_returns_graceful_response(self, monkeypatch):
        """On HTTP/network error, return AgentResponse with error in raw_output."""
        monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")
        agent = OpenRouterAgent("openai/gpt-4o")
        scenario = _make_scenario()

        with patch("requests.post", side_effect=Exception("connection refused")):
            response = agent.respond(scenario)
            assert "connection refused" in response.raw_output
            assert response.decisions == {}
            assert response.scenario_id == "test-scenario"

    def test_successful_response_parses_decisions(self, monkeypatch):
        """A well-formed JSON response must populate decisions dict."""
        monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")
        agent = OpenRouterAgent("openai/gpt-4o")
        scenario = _make_scenario()

        payload = {"selected_supplier": "SupplierA", "unit_price": 90.0}
        content = f"```json\n{json.dumps(payload)}\n```"
        mock_resp = self._make_mock_response(content)

        with patch("requests.post", return_value=mock_resp):
            response = agent.respond(scenario)
            assert response.decisions.get("selected_supplier") == "SupplierA"
            assert response.raw_output == content

    def test_latency_ms_populated(self, monkeypatch):
        """latency_ms must be non-negative on successful call."""
        monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")
        agent = OpenRouterAgent("openai/gpt-4o")
        scenario = _make_scenario()

        json_content = json.dumps({"selected_supplier": "SupplierA", "unit_price": 90.0})
        mock_resp = self._make_mock_response(f"```json\n{json_content}\n```")

        with patch("requests.post", return_value=mock_resp):
            response = agent.respond(scenario)
            assert response.latency_ms >= 0
