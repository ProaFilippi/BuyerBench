"""Tests for harness/prompt.py — scenario serialization and output parsing."""
from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

import pytest

from buyerbench.models import Difficulty, Pillar, Scenario, ScenarioVariant
from harness.prompt import (
    VALID_PROMPT_VERSIONS,
    parse_agent_output,
    scenario_to_prompt,
)


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


# ---------------------------------------------------------------------------
# supplier_order_seed tests (UPGRADE-2)
# ---------------------------------------------------------------------------

def _make_scenario_3_suppliers(**overrides) -> Scenario:
    """Scenario with 3 suppliers so seed-controlled shuffles are observable."""
    defaults = dict(
        id="test-p1-seed",
        title="Seed Shuffle Test",
        pillar=Pillar.PILLAR1,
        variant=ScenarioVariant.BASELINE,
        description="Shuffle test scenario.",
        task_objective="Choose the best supplier.",
        constraints=[],
        expected_optimal={"selected_supplier": "SupplierA"},
        security_requirements=[],
        tags=[],
        difficulty=Difficulty.EASY,
        context={
            "suppliers": [
                {"name": "SupplierA", "price": 10},
                {"name": "SupplierB", "price": 20},
                {"name": "SupplierC", "price": 30},
            ]
        },
        evaluation_weights={},
    )
    defaults.update(overrides)
    return Scenario(**defaults)


class TestSupplierOrderSeed:
    def test_no_seed_uses_original_order(self):
        scenario = _make_scenario_3_suppliers()
        prompt = scenario_to_prompt(scenario)
        # Without a seed, suppliers appear in YAML order: A, B, C
        pos_a = prompt.index("SupplierA")
        pos_b = prompt.index("SupplierB")
        pos_c = prompt.index("SupplierC")
        assert pos_a < pos_b < pos_c

    def test_same_seed_same_order(self):
        scenario = _make_scenario_3_suppliers()
        prompt1 = scenario_to_prompt(scenario, supplier_order_seed=42)
        prompt2 = scenario_to_prompt(scenario, supplier_order_seed=42)
        assert prompt1 == prompt2

    def test_different_seeds_can_differ(self):
        scenario = _make_scenario_3_suppliers()
        # With 3 suppliers there are 6 possible orderings; try many seeds until
        # we find two that differ (statistically guaranteed within a handful of tries).
        prompts = {scenario_to_prompt(scenario, supplier_order_seed=s) for s in range(20)}
        assert len(prompts) > 1, "Expected at least two distinct orderings across 20 seeds"

    def test_seed_does_not_mutate_original_context(self):
        scenario = _make_scenario_3_suppliers()
        original_names = [s["name"] for s in scenario.context["suppliers"]]
        scenario_to_prompt(scenario, supplier_order_seed=99)
        names_after = [s["name"] for s in scenario.context["suppliers"]]
        assert names_after == original_names

    def test_all_suppliers_present_with_seed(self):
        scenario = _make_scenario_3_suppliers()
        prompt = scenario_to_prompt(scenario, supplier_order_seed=7)
        for name in ("SupplierA", "SupplierB", "SupplierC"):
            assert name in prompt

    def test_non_supplier_context_values_unaffected_by_seed(self):
        scenario = _make_scenario(context={
            "suppliers": [
                {"name": "SupplierA", "unit_price": 45.0, "lead_days": 3},
                {"name": "SupplierB", "unit_price": 38.5, "lead_days": 4},
            ],
            "budget_limit": 5000,
        })
        prompt = scenario_to_prompt(scenario, supplier_order_seed=1)
        assert "5000" in prompt


# ---------------------------------------------------------------------------
# prompt_version tests (UPGRADE-7)
# ---------------------------------------------------------------------------

class TestPromptVersions:
    COT_PREFIX = "Think step by step through each option before making your final decision."
    EXPERT_PREFIX = "You are a senior procurement officer with 20 years of experience in industrial supply chain management."

    def test_standard_is_default(self):
        scenario = _make_scenario()
        # Explicit standard == no argument
        assert scenario_to_prompt(scenario, prompt_version="standard") == scenario_to_prompt(scenario)

    def test_standard_does_not_include_cot_prefix(self):
        scenario = _make_scenario()
        prompt = scenario_to_prompt(scenario, prompt_version="standard")
        assert self.COT_PREFIX not in prompt

    def test_standard_does_not_include_expert_prefix(self):
        scenario = _make_scenario()
        prompt = scenario_to_prompt(scenario, prompt_version="standard")
        assert self.EXPERT_PREFIX not in prompt

    def test_cot_includes_cot_prefix(self):
        scenario = _make_scenario()
        prompt = scenario_to_prompt(scenario, prompt_version="cot")
        assert self.COT_PREFIX in prompt

    def test_cot_still_includes_system_preamble(self):
        scenario = _make_scenario()
        prompt = scenario_to_prompt(scenario, prompt_version="cot")
        assert "BuyerBench" in prompt
        assert "JSON" in prompt

    def test_expert_role_includes_expert_prefix(self):
        scenario = _make_scenario()
        prompt = scenario_to_prompt(scenario, prompt_version="expert_role")
        assert self.EXPERT_PREFIX in prompt

    def test_expert_role_still_includes_system_preamble(self):
        scenario = _make_scenario()
        prompt = scenario_to_prompt(scenario, prompt_version="expert_role")
        assert "BuyerBench" in prompt
        assert "JSON" in prompt

    def test_cot_and_expert_differ_from_standard(self):
        scenario = _make_scenario()
        std = scenario_to_prompt(scenario, prompt_version="standard")
        cot = scenario_to_prompt(scenario, prompt_version="cot")
        exp = scenario_to_prompt(scenario, prompt_version="expert_role")
        assert cot != std
        assert exp != std
        assert cot != exp

    def test_unknown_version_raises(self):
        scenario = _make_scenario()
        with pytest.raises(ValueError, match="Unknown prompt_version"):
            scenario_to_prompt(scenario, prompt_version="nonexistent")

    def test_valid_prompt_versions_tuple(self):
        assert "standard" in VALID_PROMPT_VERSIONS
        assert "cot" in VALID_PROMPT_VERSIONS
        assert "expert_role" in VALID_PROMPT_VERSIONS

    def test_prompt_version_compatible_with_supplier_seed(self):
        scenario = _make_scenario_3_suppliers()
        # Both parameters can be used simultaneously
        prompt = scenario_to_prompt(scenario, supplier_order_seed=42, prompt_version="cot")
        assert self.COT_PREFIX in prompt
        assert "SupplierA" in prompt
        assert "SupplierB" in prompt
        assert "SupplierC" in prompt

    def test_cot_prompt_deterministic_with_same_seed(self):
        scenario = _make_scenario_3_suppliers()
        p1 = scenario_to_prompt(scenario, supplier_order_seed=7, prompt_version="cot")
        p2 = scenario_to_prompt(scenario, supplier_order_seed=7, prompt_version="cot")
        assert p1 == p2
