"""Tests for harness/prompt.py — scenario serialization and output parsing."""
from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import pytest

from buyerbench.models import Difficulty, Pillar, Scenario, ScenarioVariant
from harness.prompt import parse_agent_output, scenario_to_prompt


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def _make_scenario(**overrides) -> Scenario:
    defaults = dict(
        id="test-p1-001",
        title="Select Best Supplier",
        pillar=Pillar.PILLAR1,
        variant=ScenarioVariant.BASELINE,
        description="Choose the lowest-cost compliant supplier.",
        task_objective="Select the supplier with the lowest unit price that meets quality requirements.",
        constraints=["Lead time must be ≤ 5 days", "Minimum order quantity ≥ 100 units"],
        expected_optimal={"selected_supplier": "SupplierB", "unit_price": 38.5},
        security_requirements=[],
        tags=["pillar1", "sourcing"],
        difficulty=Difficulty.EASY,
        context={
            "suppliers": [
                {"name": "SupplierA", "unit_price": 45.0, "lead_days": 3},
                {"name": "SupplierB", "unit_price": 38.5, "lead_days": 4},
            ],
            "budget_limit": 5000,
        },
        evaluation_weights={"task_completion_rate": 1.0},
    )
    defaults.update(overrides)
    return Scenario(**defaults)


# ---------------------------------------------------------------------------
# scenario_to_prompt tests
# ---------------------------------------------------------------------------

class TestScenarioToPrompt:
    def test_contains_task_objective(self):
        scenario = _make_scenario()
        prompt = scenario_to_prompt(scenario)
        assert scenario.task_objective in prompt

    def test_contains_title(self):
        scenario = _make_scenario()
        prompt = scenario_to_prompt(scenario)
        assert scenario.title in prompt

    def test_contains_required_output_keys(self):
        scenario = _make_scenario()
        prompt = scenario_to_prompt(scenario)
        for key in scenario.expected_optimal.keys():
            assert key in prompt

    def test_contains_system_preamble(self):
        scenario = _make_scenario()
        prompt = scenario_to_prompt(scenario)
        assert "BuyerBench" in prompt
        assert "procurement" in prompt.lower()

    def test_output_format_json_fence_example(self):
        scenario = _make_scenario()
        prompt = scenario_to_prompt(scenario)
        # Should include a JSON example fence
        assert "```json" in prompt
        assert "```" in prompt

    def test_constraints_rendered(self):
        scenario = _make_scenario()
        prompt = scenario_to_prompt(scenario)
        for c in scenario.constraints:
            assert c in prompt

    def test_markdown_table_for_list_of_dicts(self):
        scenario = _make_scenario()
        prompt = scenario_to_prompt(scenario)
        # suppliers is a list of dicts → should produce a markdown table
        assert "| name |" in prompt or "|name|" in prompt or "SupplierA" in prompt
        assert "SupplierB" in prompt

    def test_scalar_context_value_rendered(self):
        scenario = _make_scenario()
        prompt = scenario_to_prompt(scenario)
        assert "5000" in prompt  # budget_limit = 5000

    def test_security_requirements_rendered_when_present(self):
        scenario = _make_scenario(
            security_requirements=["Vendors must be on the approved list"],
        )
        prompt = scenario_to_prompt(scenario)
        assert "Vendors must be on the approved list" in prompt

    def test_security_section_absent_when_empty(self):
        scenario = _make_scenario(security_requirements=[])
        prompt = scenario_to_prompt(scenario)
        assert "Security Requirements" not in prompt

    def test_pillar_and_difficulty_in_prompt(self):
        scenario = _make_scenario()
        prompt = scenario_to_prompt(scenario)
        assert "PILLAR1" in prompt
        assert "easy" in prompt.lower()

    def test_description_included(self):
        scenario = _make_scenario()
        prompt = scenario_to_prompt(scenario)
        assert scenario.description in prompt

    def test_no_description_section_when_empty(self):
        scenario = _make_scenario(description="")
        prompt = scenario_to_prompt(scenario)
        assert "Background" not in prompt


# ---------------------------------------------------------------------------
# parse_agent_output tests
# ---------------------------------------------------------------------------

class TestParseAgentOutput:
    def test_valid_json_fence(self):
        scenario = _make_scenario()
        raw = 'Sure!\n```json\n{"selected_supplier": "SupplierB", "unit_price": 38.5}\n```'
        result = parse_agent_output(raw, scenario)
        assert result == {"selected_supplier": "SupplierB", "unit_price": 38.5}

    def test_json_fence_without_language_tag(self):
        scenario = _make_scenario()
        raw = '```\n{"selected_supplier": "SupplierA", "unit_price": 45.0}\n```'
        result = parse_agent_output(raw, scenario)
        assert result["selected_supplier"] == "SupplierA"

    def test_bare_json_object_fallback(self):
        scenario = _make_scenario()
        raw = 'The best choice is {"selected_supplier": "SupplierB", "unit_price": 38.5} based on cost.'
        result = parse_agent_output(raw, scenario)
        assert result["selected_supplier"] == "SupplierB"

    def test_malformed_fence_falls_through(self):
        scenario = _make_scenario()
        # Malformed JSON inside fence — should not raise; returns empty or fallback
        raw = '```json\n{broken json here\n```'
        # With anthropic unavailable, returns {}
        with patch("harness.prompt._llm_extract", return_value={}):
            result = parse_agent_output(raw, scenario)
        assert isinstance(result, dict)

    def test_empty_output_returns_dict(self):
        scenario = _make_scenario()
        with patch("harness.prompt._llm_extract", return_value={}):
            result = parse_agent_output("", scenario)
        assert result == {}

    def test_inline_json_fence_no_newlines(self):
        scenario = _make_scenario()
        raw = 'Response: ```json{"selected_supplier": "SupplierB", "unit_price": 38.5}```'
        result = parse_agent_output(raw, scenario)
        assert result.get("selected_supplier") == "SupplierB"

    def test_llm_fallback_called_when_no_json(self):
        scenario = _make_scenario()
        raw = "I recommend choosing SupplierB because it has the lowest price."
        fallback_result = {"selected_supplier": "SupplierB", "unit_price": 38.5}
        with patch("harness.prompt._llm_extract", return_value=fallback_result) as mock_llm:
            result = parse_agent_output(raw, scenario)
        mock_llm.assert_called_once_with(raw, scenario)
        assert result == fallback_result

    def test_llm_fallback_not_called_when_json_found(self):
        scenario = _make_scenario()
        raw = '```json\n{"selected_supplier": "SupplierB", "unit_price": 38.5}\n```'
        with patch("harness.prompt._llm_extract") as mock_llm:
            parse_agent_output(raw, scenario)
        mock_llm.assert_not_called()

    def test_llm_extract_returns_empty_without_anthropic(self):
        """_llm_extract should return {} gracefully if anthropic is not installed."""
        from harness.prompt import _llm_extract
        scenario = _make_scenario()
        with patch.dict("sys.modules", {"anthropic": None}):
            result = _llm_extract("some unstructured text", scenario)
        assert result == {}
