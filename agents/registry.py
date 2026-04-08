"""Agent registry for BuyerBench.

Maps canonical agent_id strings to their adapter classes and provides
``get_agent()`` for instantiation from a config dict.

Canonical agent IDs
-------------------
  claude-code-baseline   Claude Code CLI, no tools
  claude-code-skills     Claude Code CLI, built-in tools enabled
  claude-code-mcp        Claude Code CLI, MCP server attached
  codex-baseline         OpenAI Codex CLI, no tools
  codex-skills           OpenAI Codex CLI, built-in tools enabled
  codex-mcp              OpenAI Codex CLI, MCP server attached
  gemini-baseline        Google Gemini CLI, no tools
  gemini-skills          Google Gemini CLI, built-in tools enabled
  gemini-mcp             Google Gemini CLI, MCP server attached
  mock-agent-v1          Perfect mock agent (test / pipeline verification)
  stripe-toolkit         Stripe Agent Toolkit adapter (Pillar 3 focus)
  negmas                 NegMAS negotiation agent adapter (Pillar 1 focus)
  openrouter-*           Direct HTTP agents via OpenRouter (10 models)
"""
from __future__ import annotations

from agents import BaseAgent
from agents.claude_code_agent import ClaudeCodeAgent
from agents.codex_agent import CodexAgent
from agents.gemini_agent import GeminiAgent
from agents.mock import MockAgent
from agents.negmas_agent import NegMASAgent
from agents.openrouter_agent import OpenRouterAgent
from agents.stripe_toolkit_agent import StripeToolkitAgent

# ------------------------------------------------------------------
# OpenRouter model map: agent_id slug -> OpenRouter model_id
# ------------------------------------------------------------------

OPENROUTER_MODEL_MAP: dict[str, str] = {
    "openrouter-openai-gpt-4o": "openai/gpt-4o",
    "openrouter-anthropic-claude-3.5-sonnet": "anthropic/claude-3.5-sonnet",
    "openrouter-google-gemini-pro-1.5": "google/gemini-pro-1.5",
    "openrouter-meta-llama-llama-3.1-405b-instruct": "meta-llama/llama-3.1-405b-instruct",
    "openrouter-mistralai-mistral-large": "mistralai/mistral-large",
    "openrouter-deepseek-deepseek-chat": "deepseek/deepseek-chat",
    "openrouter-qwen-qwen-2.5-72b-instruct": "qwen/qwen-2.5-72b-instruct",
    "openrouter-cohere-command-r-plus": "cohere/command-r-plus",
    "openrouter-mistralai-mixtral-8x22b-instruct": "mistralai/mixtral-8x22b-instruct",
    "openrouter-01-ai-yi-large": "01-ai/yi-large",
}

# ------------------------------------------------------------------
# Registry: agent_id -> adapter class
# ------------------------------------------------------------------

AGENT_REGISTRY: dict[str, type[BaseAgent]] = {
    # Claude Code
    "claude-code-baseline": ClaudeCodeAgent,
    "claude-code-skills": ClaudeCodeAgent,
    "claude-code-mcp": ClaudeCodeAgent,
    # Codex
    "codex-baseline": CodexAgent,
    "codex-skills": CodexAgent,
    "codex-mcp": CodexAgent,
    # Gemini
    "gemini-baseline": GeminiAgent,
    "gemini-skills": GeminiAgent,
    "gemini-mcp": GeminiAgent,
    # Mock (for testing)
    "mock-agent-v1": MockAgent,
    # Open-source agent adapters
    "stripe-toolkit": StripeToolkitAgent,
    "negmas": NegMASAgent,
    # OpenRouter HTTP agents (10 models)
    **{agent_id: OpenRouterAgent for agent_id in OPENROUTER_MODEL_MAP},
}


def get_agent(agent_id: str, config: dict | None = None) -> BaseAgent:
    """Return a configured agent instance for the given *agent_id*.

    Parameters
    ----------
    agent_id:
        A canonical id from ``AGENT_REGISTRY`` (e.g. ``"claude-code-baseline"``).
    config:
        Optional config dict (typically from ``harness.config.load_config()``).
        Per-agent keys are looked up under the agent family name
        (``"claude_code"``, ``"codex"``, ``"gemini"``).

    Raises
    ------
    KeyError
        If *agent_id* is not found in the registry.
    """
    if agent_id not in AGENT_REGISTRY:
        available = sorted(AGENT_REGISTRY.keys())
        raise KeyError(
            f"Unknown agent_id {agent_id!r}.  Available: {available}"
        )

    cls = AGENT_REGISTRY[agent_id]
    config = config or {}

    # Mock agent takes no constructor args
    if cls is MockAgent:
        return MockAgent()

    # Stripe toolkit and NegMAS agents take no mode/CLI args
    if cls is StripeToolkitAgent:
        return StripeToolkitAgent()
    if cls is NegMASAgent:
        return NegMASAgent()

    # OpenRouter agents: instantiate directly with model_id + config overrides
    if agent_id.startswith("openrouter-"):
        model_id = OPENROUTER_MODEL_MAP[agent_id]
        or_cfg = config.get("openrouter", {})
        return OpenRouterAgent(
            model_id=model_id,
            timeout=config.get("timeout", or_cfg.get("timeout", 120)),
            dry_run=config.get("dry_run", False),
        )

    # Extract mode from the agent_id suffix
    _, mode = agent_id.rsplit("-", 1)

    # Determine config key by family
    if "claude-code" in agent_id:
        family_cfg = config.get("claude_code", {})
    elif "codex" in agent_id:
        family_cfg = config.get("codex", {})
    else:
        family_cfg = config.get("gemini", {})

    kwargs: dict = {
        "mode": mode,
        "timeout": config.get("timeout", family_cfg.get("timeout", 120)),
        "dry_run": config.get("dry_run", False),
    }
    if cli_path := family_cfg.get("cli_path"):
        kwargs["cli_path"] = cli_path
    if mcp_cfg := family_cfg.get("mcp_config_path"):
        kwargs["mcp_config_path"] = mcp_cfg

    return cls(**kwargs)
