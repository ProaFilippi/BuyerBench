"""Prompt serialization and output parsing for BuyerBench CLI agents.

Converts Scenario objects into natural-language prompts suitable for CLI
invocation, and parses agent output back into structured decision dicts.
"""
from __future__ import annotations

import json
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


def scenario_to_prompt(scenario: Scenario) -> str:
    """Convert a Scenario into a natural-language prompt for a CLI agent.

    The prompt includes:
    - A system preamble identifying the benchmark context
    - The task objective
    - Context rendered as markdown tables (for lists of dicts) or bullet lists
    - Constraints and security requirements
    - Required output format with JSON key names
    """
    lines: list[str] = [_SYSTEM_PREAMBLE, ""]
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
        lines.extend(_format_context(scenario.context))
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


def _format_context(context: dict[str, Any]) -> list[str]:
    """Render context dict as markdown — tables for tabular data, lists otherwise."""
    lines: list[str] = []
    for key, value in context.items():
        heading = key.replace("_", " ").title()
        if isinstance(value, list) and value and isinstance(value[0], dict):
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

_BARE_JSON_PATTERN = re.compile(r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)?\}", re.DOTALL)


def parse_agent_output(raw_output: str, scenario: Scenario) -> dict:
    """Extract a JSON decision dict from raw CLI output.

    Tries regex-based extraction first (fenced code blocks, then bare JSON).
    Falls back to LLM-assisted extraction via the Anthropic SDK if nothing
    parseable is found; returns an empty dict if all strategies fail.
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

    match = _BARE_JSON_PATTERN.search(raw_output)
    if match:
        try:
            result = json.loads(match.group())
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
