"""Static metadata registry for the 10 OpenRouter models available in BuyerBench.

Each ``ModelEntry`` carries human-readable display fields alongside the
canonical ``agent_id`` used throughout the agent registry and run harness.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ModelEntry:
    agent_id: str
    model_id: str
    display_name: str
    provider: str
    context_k: int
    cost_tier: str  # "free" | "low" | "mid" | "high"
    capability_tags: list[str] = field(default_factory=list)
    description: str = ""


MODEL_CATALOG: list[ModelEntry] = [
    ModelEntry(
        agent_id="openrouter-openai-gpt-4o",
        model_id="openai/gpt-4o",
        display_name="GPT-4o",
        provider="OpenAI",
        context_k=128,
        cost_tier="high",
        capability_tags=["reasoning", "coding", "multimodal"],
        description="OpenAI's flagship multimodal model with strong reasoning and coding ability.",
    ),
    ModelEntry(
        agent_id="openrouter-anthropic-claude-3.5-sonnet",
        model_id="anthropic/claude-3.5-sonnet",
        display_name="Claude 3.5 Sonnet",
        provider="Anthropic",
        context_k=200,
        cost_tier="high",
        capability_tags=["reasoning", "coding", "long-context"],
        description="Anthropic's high-intelligence model with 200K context and excellent instruction following.",
    ),
    ModelEntry(
        agent_id="openrouter-google-gemini-pro-1.5",
        model_id="google/gemini-pro-1.5",
        display_name="Gemini Pro 1.5",
        provider="Google",
        context_k=1000,
        cost_tier="mid",
        capability_tags=["long-context", "multimodal"],
        description="Google's multimodal model with an industry-leading 1M-token context window.",
    ),
    ModelEntry(
        agent_id="openrouter-meta-llama-llama-3.1-405b-instruct",
        model_id="meta-llama/llama-3.1-405b-instruct",
        display_name="Llama 3.1 405B Instruct",
        provider="Meta",
        context_k=128,
        cost_tier="low",
        capability_tags=["open-source", "reasoning"],
        description="Meta's largest open-source model with strong general reasoning capabilities.",
    ),
    ModelEntry(
        agent_id="openrouter-mistralai-mistral-large",
        model_id="mistralai/mistral-large",
        display_name="Mistral Large",
        provider="Mistral",
        context_k=32,
        cost_tier="mid",
        capability_tags=["reasoning", "european"],
        description="Mistral's flagship dense model designed for complex reasoning and EU data residency.",
    ),
    ModelEntry(
        agent_id="openrouter-deepseek-deepseek-chat",
        model_id="deepseek/deepseek-chat",
        display_name="DeepSeek V3",
        provider="DeepSeek",
        context_k=64,
        cost_tier="low",
        capability_tags=["coding", "open-source"],
        description="DeepSeek's open-source coding-focused model with strong benchmark performance.",
    ),
    ModelEntry(
        agent_id="openrouter-qwen-qwen-2.5-72b-instruct",
        model_id="qwen/qwen-2.5-72b-instruct",
        display_name="Qwen 2.5 72B Instruct",
        provider="Alibaba",
        context_k=128,
        cost_tier="low",
        capability_tags=["multilingual", "open-source"],
        description="Alibaba's multilingual open-source model excelling across Asian and Western languages.",
    ),
    ModelEntry(
        agent_id="openrouter-cohere-command-r-plus",
        model_id="cohere/command-r-plus",
        display_name="Command R+",
        provider="Cohere",
        context_k=128,
        cost_tier="mid",
        capability_tags=["rag", "enterprise"],
        description="Cohere's enterprise-grade retrieval-augmented generation model built for production RAG.",
    ),
    ModelEntry(
        agent_id="openrouter-mistralai-mixtral-8x22b-instruct",
        model_id="mistralai/mixtral-8x22b-instruct",
        display_name="Mixtral 8x22B Instruct",
        provider="Mistral",
        context_k=64,
        cost_tier="low",
        capability_tags=["moe", "open-source"],
        description="Mistral's open Mixture-of-Experts model offering high throughput at low cost.",
    ),
    ModelEntry(
        agent_id="openrouter-01-ai-yi-large",
        model_id="01-ai/yi-large",
        display_name="Yi Large 34B",
        provider="01.AI",
        context_k=32,
        cost_tier="low",
        capability_tags=["multilingual", "open-source"],
        description="01.AI's multilingual open-source model with competitive performance in Chinese and English.",
    ),
]


def filter_catalog(
    providers: list[str] | None = None,
    tags: list[str] | None = None,
    cost_tiers: list[str] | None = None,
) -> list[ModelEntry]:
    """Return catalog entries matching ALL supplied filter criteria.

    Parameters
    ----------
    providers:
        If given, only entries whose ``provider`` is in this list are returned
        (case-insensitive comparison).
    tags:
        If given, only entries that have at least one matching ``capability_tag``
        are returned.
    cost_tiers:
        If given, only entries whose ``cost_tier`` is in this list are returned.
    """
    results = MODEL_CATALOG[:]

    if providers:
        lower_providers = {p.lower() for p in providers}
        results = [e for e in results if e.provider.lower() in lower_providers]

    if tags:
        lower_tags = {t.lower() for t in tags}
        results = [
            e for e in results if any(ct.lower() in lower_tags for ct in e.capability_tags)
        ]

    if cost_tiers:
        lower_tiers = {t.lower() for t in cost_tiers}
        results = [e for e in results if e.cost_tier.lower() in lower_tiers]

    return results
