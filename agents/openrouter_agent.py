"""OpenRouter HTTP adapter for BuyerBench.

Makes direct HTTP calls to OpenRouter's OpenAI-compatible chat completions API,
enabling evaluation of any model available on OpenRouter without needing a
separate CLI tool installed.

Requires:
    OPENROUTER_API_KEY environment variable (or pass via harness config)
    pip install requests

Usage::

    from agents.openrouter_agent import OpenRouterAgent
    agent = OpenRouterAgent("openai/gpt-4o")
    response = agent.respond(scenario)
"""
from __future__ import annotations

import json
import os
import time
from typing import Any

from agents import BaseAgent
from buyerbench.models import AgentResponse, Scenario

_OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
_HTTP_REFERER = "https://github.com/BuyerBench"
_X_TITLE = "BuyerBench"


class OpenRouterAgent(BaseAgent):
    """BuyerBench agent adapter that calls OpenRouter's chat completions API.

    Parameters
    ----------
    model_id:
        OpenRouter model identifier (e.g. ``"openai/gpt-4o"``).
    timeout:
        HTTP request timeout in seconds.
    dry_run:
        When True, print the prompt and return a stub response without
        making any API calls.
    """

    def __init__(
        self,
        model_id: str,
        timeout: int = 120,
        dry_run: bool = False,
        system_prompt: str = "",
        temperature: float | None = None,
    ) -> None:
        self.model_id = model_id
        self.agent_id = f"openrouter-{model_id.replace('/', '-')}"
        self.timeout = timeout
        self.dry_run = dry_run
        self.system_prompt = system_prompt
        self.temperature = temperature

    # ------------------------------------------------------------------
    # BaseAgent interface
    # ------------------------------------------------------------------

    def respond(self, scenario: Scenario) -> AgentResponse:
        from harness.prompt import scenario_to_prompt, parse_agent_output

        prompt = scenario_to_prompt(scenario)

        if self.dry_run:
            print(f"\n[dry-run] OpenRouterAgent({self.model_id})\n")
            print(prompt)
            return AgentResponse(
                scenario_id=scenario.id,
                agent_id=self.agent_id,
                decisions={},
                raw_output="[dry-run]",
                latency_ms=0.0,
                temperature=self.temperature,
                prompt_text=prompt,
            )

        return self._call_openrouter(prompt, scenario)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _call_openrouter(self, prompt: str, scenario: Scenario) -> AgentResponse:
        """POST to OpenRouter and return a structured AgentResponse."""
        import requests  # runtime import — optional dependency

        from harness.prompt import parse_agent_output

        api_key = os.environ.get("OPENROUTER_API_KEY", "")

        headers: dict[str, str] = {
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": _HTTP_REFERER,
            "X-Title": _X_TITLE,
            "Content-Type": "application/json",
        }
        messages: list[dict[str, str]] = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        messages.append({"role": "user", "content": prompt})

        body: dict[str, Any] = {
            "model": self.model_id,
            "messages": messages,
        }
        if self.temperature is not None:
            body["temperature"] = self.temperature

        start = time.monotonic()
        try:
            resp = requests.post(
                _OPENROUTER_URL,
                headers=headers,
                json=body,
                timeout=self.timeout,
            )
            resp.raise_for_status()
            data = resp.json()
            content: str = data["choices"][0]["message"]["content"]
        except Exception as exc:
            elapsed_ms = (time.monotonic() - start) * 1000
            return AgentResponse(
                scenario_id=scenario.id,
                agent_id=self.agent_id,
                decisions={},
                raw_output=str(exc),
                latency_ms=elapsed_ms,
                temperature=self.temperature,
                prompt_text=prompt,
                error_flag=True,
                error_message=str(exc),
            )

        elapsed_ms = (time.monotonic() - start) * 1000
        parsed = parse_agent_output(content, scenario)

        usage = data.get("usage") or {}
        return AgentResponse(
            scenario_id=scenario.id,
            agent_id=self.agent_id,
            decisions=parsed,
            raw_output=content,
            latency_ms=elapsed_ms,
            temperature=self.temperature,
            prompt_text=prompt,
            model_version=data.get("model"),
            token_count_input=usage.get("prompt_tokens", 0) or 0,
            token_count_output=usage.get("completion_tokens", 0) or 0,
            api_cost_usd=usage.get("cost"),
            api_response_raw=json.dumps(data),
        )
