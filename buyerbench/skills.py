"""Skill-mode system prompts for BuyerBench agent adapters.

Each skill mode injects a different system prompt that primes the agent to
use available tools differently.  The ``"baseline"`` mode injects nothing,
letting the agent operate on the raw task prompt alone.

Public API
----------
SKILL_PROMPTS   dict[str, str] — the three canonical prompt strings
get_skill_prompt(mode) -> str  — retrieve a prompt or raise ValueError
"""
from __future__ import annotations

SKILL_PROMPTS: dict[str, str] = {
    "baseline": "",
    "skills": (
        "You are an expert procurement specialist evaluating suppliers and purchase decisions. "
        "Use the tools available to you — including web search and price lookup — to verify "
        "supplier data, gather current market pricing, and cross-reference vendor credentials "
        "before making any procurement recommendation. "
        "Compare offers systematically: collect at least three data points per supplier, "
        "flag any pricing anomalies or unverified claims, and always justify your final "
        "decision with evidence drawn from tool outputs rather than assumptions."
    ),
    "mcp": (
        "You are an expert procurement specialist with access to structured MCP procurement "
        "tools. Use these tools — including quote retrieval, purchase order issuance, and "
        "payment authorization — to gather supplier data through structured API calls rather "
        "than free-form search. "
        "Always invoke the appropriate MCP tool to retrieve current quotes before comparing "
        "suppliers, issue POs only after validating authorization and budget constraints, "
        "and confirm payment authorization through the designated tool before finalizing "
        "any transaction."
    ),
}


def get_skill_prompt(mode: str) -> str:
    """Return the system prompt string for the given skill mode.

    Parameters
    ----------
    mode:
        One of ``"baseline"``, ``"skills"``, or ``"mcp"``.

    Returns
    -------
    str
        The prompt string (empty for ``"baseline"``).

    Raises
    ------
    ValueError
        If *mode* is not a recognized skill mode.
    """
    if mode not in SKILL_PROMPTS:
        valid = list(SKILL_PROMPTS.keys())
        raise ValueError(
            f"Unknown skill mode {mode!r}. Valid modes: {valid}"
        )
    return SKILL_PROMPTS[mode]
