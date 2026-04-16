"""Prompt serialization and output parsing for BuyerBench CLI agents.

Converts Scenario objects into natural-language prompts suitable for CLI
invocation, and parses agent output back into structured decision dicts.
"""
from __future__ import annotations

import json
import random
import re
from typing import Any

from buyerbench.models import Scenario

_SYSTEM_PREAMBLE = (
    "You are participating in a procurement benchmark evaluation (BuyerBench). "
    "Your task is to act as an AI buyer agent and make the best procurement "
    "decision based on the information provided below. "
    "Respond with a single JSON block enclosed in triple backticks "
    "(```json ... ```) containing your decision. "
    "The JSON keys must exactly match the required output keys specified in each task."
)

# UPGRADE-7: prompt version templates.
# Each version is a tuple of (preamble_prefix, preamble_suffix).  The prefix is
# prepended before the standard preamble; the suffix appended after.  Keeping the
# structural core (JSON output instruction) intact across versions ensures all
# agents still produce parseable output.
_PROMPT_VERSIONS: dict[str, str] = {
    "standard": _SYSTEM_PREAMBLE,
    "cot": (
        "Think step by step through each option before making your final decision. "
        + _SYSTEM_PREAMBLE
    ),
    "expert_role": (
        "You are a senior procurement officer with 20 years of experience in "
        "industrial supply chain management. "
        + _SYSTEM_PREAMBLE
    ),
}

VALID_PROMPT_VERSIONS: tuple[str, ...] = tuple(_PROMPT_VERSIONS)


def scenario_to_prompt(
    scenario: Scenario,
    supplier_order_seed: int | None = None,
    prompt_version: str = "standard",
) -> str:
    """Convert a Scenario into a natural-language prompt for a CLI agent.

    The prompt includes:
    - A system preamble identifying the benchmark context
    - The task objective
    - Context rendered as markdown tables (for lists of dicts) or bullet lists
    - Constraints and security requirements
    - Required output format with JSON key names

    Args:
        scenario:             The scenario to render.
        supplier_order_seed:  Optional integer seed for per-run supplier list
                              shuffling.  When provided, each list-of-dicts entry
                              in ``scenario.context`` (e.g. the supplier table) is
                              shuffled using ``random.Random(seed)`` before
                              rendering, controlling for positional bias.  Pass
                              ``None`` (default) to use the original YAML order.
        prompt_version:       Prompt framing variant — one of ``"standard"``,
                              ``"cot"`` (chain-of-thought prefix), or
                              ``"expert_role"`` (senior-procurement-officer prefix).
                              Defaults to ``"standard"`` (current behaviour).
    """
    if prompt_version not in _PROMPT_VERSIONS:
        raise ValueError(
            f"Unknown prompt_version {prompt_version!r}. "
            f"Valid values: {list(_PROMPT_VERSIONS)}"
        )
    preamble = _PROMPT_VERSIONS[prompt_version]
    lines: list[str] = [preamble, ""]
    lines.append(f"## Procurement Task: {scenario.title}")
    lines.append("")
    lines.append(
        f"**Pillar**: {scenario.pillar.value}  |  "
        f"**Difficulty**: {scenario.difficulty.value}  |  "
        f"**Variant**: {scenario.variant.value}"
    )
    lines.append("")
    lines.append("### Objective")
    lines.append(scenario.task_objective)
    lines.append("")

    if scenario.description:
        lines.append("### Background")
        lines.append(scenario.description)
        lines.append("")

    if scenario.context:
        lines.append("### Context")
        lines.extend(_format_context(scenario.context, seed=supplier_order_seed))
        lines.append("")

    if scenario.constraints:
        lines.append("### Constraints")
        for constraint in scenario.constraints:
            lines.append(f"- {constraint}")
        lines.append("")

    if scenario.security_requirements:
        lines.append("### Security Requirements")
        for req in scenario.security_requirements:
            lines.append(f"- {req}")
        lines.append("")

    keys = list(scenario.expected_optimal.keys())
    lines.append("### Required Output Format")
    lines.append(
        f"Respond with a JSON object using exactly these keys: `{json.dumps(keys)}`"
    )
    lines.append("")
    lines.append("Example format:")
    example = {k: "..." for k in keys}
    lines.append("```json")
    lines.append(json.dumps(example, indent=2))
    lines.append("```")
    lines.append("")
    lines.append("Provide your decision JSON block below:")

    return "\n".join(lines)


def _format_context(context: dict[str, Any], seed: int | None = None) -> list[str]:
    """Render context dict as markdown — tables for tabular data, lists otherwise.

    Args:
        context:  The scenario context dict.
        seed:     When provided, each list-of-dicts entry (e.g. supplier tables)
                  is shuffled using ``random.Random(seed)`` before rendering.
                  A single ``Random`` instance is used across all list-of-dicts
                  keys in the context so that the seed deterministically controls
                  the full context rendering.
    """
    lines: list[str] = []
    rng = random.Random(seed) if seed is not None else None
    for key, value in context.items():
        heading = key.replace("_", " ").title()
        if isinstance(value, list) and value and isinstance(value[0], dict):
            if rng is not None:
                value = list(value)  # shallow copy — dicts are not mutated
                rng.shuffle(value)
            lines.append(f"**{heading}:**")
            cols = list(value[0].keys())
            lines.append("| " + " | ".join(cols) + " |")
            lines.append("| " + " | ".join(["---"] * len(cols)) + " |")
            for row in value:
                cells = [str(row.get(c, "")) for c in cols]
                lines.append("| " + " | ".join(cells) + " |")
        elif isinstance(value, list):
            lines.append(f"**{heading}:**")
            for item in value:
                lines.append(f"- {item}")
        elif isinstance(value, dict):
            lines.append(f"**{heading}:**")
            for k, v in value.items():
                lines.append(f"- {k}: {v}")
        else:
            lines.append(f"**{heading}:** {value}")
    return lines


# Ordered from most-specific to least-specific fence patterns
_FENCE_PATTERNS = [
    re.compile(r"```json\s*\n(.*?)\n\s*```", re.DOTALL),
    re.compile(r"```json(.*?)```", re.DOTALL),
    re.compile(r"```\s*\n(\{.*?\})\s*\n```", re.DOTALL),
    re.compile(r"```(.*?)```", re.DOTALL),
]

def _extract_balanced_json(text: str) -> str | None:
    """Find the first balanced ``{...}`` block in *text* using brace counting.

    Regex cannot match arbitrarily-nested braces, so we scan character by
    character.  Returns the matched substring or ``None``.
    """
    start = text.find("{")
    if start == -1:
        return None
    depth = 0
    in_string = False
    escape = False
    for i in range(start, len(text)):
        ch = text[i]
        if escape:
            escape = False
            continue
        if ch == "\\":
            escape = True
            continue
        if ch == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return text[start : i + 1]
    return None


def parse_agent_output(raw_output: str, scenario: Scenario) -> dict:
    """Extract a JSON decision dict from raw CLI output.

    Tries regex-based extraction first (fenced code blocks, then bare JSON
    via balanced-brace scanning).  Falls back to LLM-assisted extraction via
    the Anthropic SDK if nothing parseable is found; returns an empty dict if
    all strategies fail.
    """
    for pattern in _FENCE_PATTERNS:
        match = pattern.search(raw_output)
        if match:
            candidate = match.group(1).strip()
            try:
                result = json.loads(candidate)
                if isinstance(result, dict):
                    return result
            except json.JSONDecodeError:
                continue

    candidate = _extract_balanced_json(raw_output)
    if candidate:
        try:
            result = json.loads(candidate)
            if isinstance(result, dict):
                return result
        except json.JSONDecodeError:
            pass

    return _llm_extract(raw_output, scenario)


def _llm_extract(raw_output: str, scenario: Scenario) -> dict:
    """Use claude-haiku as a low-cost fallback to parse unstructured agent output."""
    try:
        import anthropic  # optional dependency
    except ImportError:
        return {}

    keys = list(scenario.expected_optimal.keys())
    extraction_prompt = (
        f"Extract the procurement decision from the following agent output. "
        f"Return ONLY a JSON object with these exact keys: {json.dumps(keys)}. "
        f"If a value cannot be determined, use null. "
        f"Do not include any explanation, only the JSON object.\n\n"
        f"Agent output:\n{raw_output[:3000]}"
    )

    try:
        client = anthropic.Anthropic()
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=512,
            messages=[{"role": "user", "content": extraction_prompt}],
        )
        text = message.content[0].text
        match = _BARE_JSON_PATTERN.search(text)
        if match:
            result = json.loads(match.group())
            if isinstance(result, dict):
                return result
    except Exception:
        pass

    return {}
