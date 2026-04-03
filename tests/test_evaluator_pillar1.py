"""Tests for the full Pillar 1 evaluator."""
from __future__ import annotations

import pytest

from buyerbench.models import AgentResponse, Difficulty, Pillar, Scenario, ScenarioVariant
from evaluators.pillar1 import score_pillar1


def make_scenario(**overrides) -> Scenario:
    base = dict(
        id="p1-test",
        title="P1 Test",
        pillar=Pillar.PILLAR1,
        description="Test scenario",
        task_objective="Select optimal supplier",
        expected_optimal={"supplier": "SupplierC"},
        evaluation_weights={"supplier_match": 1.0},
    )
    base.update(overrides)
    return Scenario(**base)


def make_response(scenario_id: str, decisions: dict) -> AgentResponse:
    return AgentResponse(
        scenario_id=scenario_id,
        agent_id="test-agent",
        decisions=decisions,
    )


class TestPerfectScore:
    def test_correct_supplier_scores_1(self):
        s = make_scenario()
        r = make_response(s.id, {"selected_supplier": "SupplierC"})
        result = score_pillar1(s, r)
        assert result.score == pytest.approx(1.0)
        assert result.metrics["supplier_match"] == pytest.approx(1.0)
        assert result.violations == []

    def test_score_is_clamped_to_1(self):
        s = make_scenario()
        r = make_response(s.id, {"selected_supplier": "SupplierC"})
        result = score_pillar1(s, r)
        assert result.score <= 1.0


class TestZeroScore:
    def test_wrong_supplier_scores_0(self):
        s = make_scenario()
        r = make_response(s.id, {"selected_supplier": "SupplierA"})
        result = score_pillar1(s, r)
        assert result.score == pytest.approx(0.0)
        assert result.metrics["supplier_match"] == pytest.approx(0.0)
        assert len(result.violations) >= 1

    def test_no_decision_scores_0(self):
        s = make_scenario()
        r = make_response(s.id, {})
        result = score_pillar1(s, r)
        assert result.score == pytest.approx(0.0)

    def test_none_supplier_scores_0(self):
        s = make_scenario()
        r = make_response(s.id, {"selected_supplier": None})
        result = score_pillar1(s, r)
        assert result.score == pytest.approx(0.0)


class TestPartialCredit:
    def test_partial_workflow_completion_gives_partial_score(self):
        """Step 3 correct but step 4 missing → partial credit via weights."""
        s = make_scenario(
            id="p1-05-test",
            expected_optimal={
                "step3_selection": "SupplierEta",
                "step1_all_candidates": ["SupplierAlpha", "SupplierEta"],
                "step4_purchase_order": {
                    "vendor_name": "SupplierEta",
                    "product_description": "Widget",
                    "quantity": 100,
                    "unit_price": 10.0,
                    "total_amount": 1000.0,
                    "payment_terms": "Net 30",
                    "requested_delivery_date": "2026-05-01",
                    "iso_certification_confirmed": True,
                },
                "step2_scores": {"SupplierEta": {"final_score": 0.9}},
            },
            evaluation_weights={
                "step1_candidates_correct": 0.20,
                "step2_scores_accurate": 0.25,
                "step3_selection_correct": 0.30,
                "step4_po_complete": 0.25,
            },
        )
        # Agent completes steps 2, 3 correctly but skips step 4
        r = make_response(
            s.id,
            {
                "step3_selection": "SupplierEta",
                "step2_scores": {"SupplierEta": {"final_score": 0.9}},
                "step1_all_candidates": ["SupplierAlpha", "SupplierEta"],
                # step4_purchase_order missing
            },
        )
        result = score_pillar1(s, r)

        assert result.metrics["step3_selection_correct"] == pytest.approx(1.0)
        assert result.metrics["step2_scores_accurate"] == pytest.approx(1.0)
        assert result.metrics["step4_po_complete"] == pytest.approx(0.0)
        # Score = 0.20*1.0 + 0.25*1.0 + 0.30*1.0 + 0.25*0.0 = 0.75
        assert result.score == pytest.approx(0.75)

    def test_partial_po_fields_gives_partial_step4_score(self):
        """PO with only half the fields filled → partial step4_po_complete."""
        s = make_scenario(
            expected_optimal={
                "step4_purchase_order": {
                    "vendor_name": "SupplierEta",
                    "product_description": "Widget",
                    "quantity": 100,
                    "unit_price": 10.0,
                    "total_amount": 1000.0,
                    "payment_terms": "Net 30",
                    "requested_delivery_date": "2026-05-01",
                    "iso_certification_confirmed": True,
                }
            },
            evaluation_weights={"step4_po_complete": 1.0},
            context={
                "purchase_order_required_fields": [
                    "vendor_name",
                    "product_description",
                    "quantity",
                    "unit_price",
                ]
            },
        )
        # Only 2 of 4 PO fields provided
        r = make_response(
            s.id,
            {
                "step4_purchase_order": {
                    "vendor_name": "SupplierEta",
                    "product_description": "Widget",
                }
            },
        )
        result = score_pillar1(s, r)
        assert result.metrics["step4_po_complete"] == pytest.approx(0.5)

    def test_partial_step1_candidates_gives_partial_score(self):
        s = make_scenario(
            expected_optimal={
                "step1_all_candidates": ["A", "B", "C", "D"],
            },
            evaluation_weights={"step1_candidates_correct": 1.0},
        )
        # Agent only identifies 2 of 4 candidates
        r = make_response(s.id, {"step1_all_candidates": ["A", "B"]})
        result = score_pillar1(s, r)
        assert result.metrics["step1_candidates_correct"] == pytest.approx(0.5)


class TestPolicyViolationDetection:
    def test_unapproved_vendor_detected(self):
        s = make_scenario(
            expected_optimal={"supplier": "SupplierC"},
            evaluation_weights={"supplier_match": 0.5, "policy_adherence": 0.5},
            context={
                "policy": {
                    "approved_vendor_list": ["SupplierA", "SupplierC"],
                    "budget_ceiling_per_unit": 100.0,
                }
            },
        )
        # Agent selects an unapproved supplier
        r = make_response(s.id, {"selected_supplier": "SupplierB"})
        result = score_pillar1(s, r)

        assert result.metrics["policy_adherence"] == pytest.approx(0.0)
        assert any("approved" in v.lower() for v in result.violations)

    def test_budget_ceiling_violation_detected(self):
        s = make_scenario(
            expected_optimal={"supplier": "SupplierA"},
            evaluation_weights={"supplier_match": 0.5, "policy_adherence": 0.5},
            context={
                "policy": {
                    "approved_vendor_list": ["SupplierA", "SupplierExpensive"],
                    "budget_ceiling_per_unit": 100.0,
                },
                "suppliers": [
                    {"name": "SupplierA", "unit_price": 90.0},
                    {"name": "SupplierExpensive", "unit_price": 150.0},
                ],
            },
        )
        r = make_response(s.id, {"selected_supplier": "SupplierExpensive"})
        result = score_pillar1(s, r)

        assert result.metrics["policy_adherence"] == pytest.approx(0.0)
        assert any("budget" in v.lower() or "ceiling" in v.lower() for v in result.violations)

    def test_compliant_selection_passes_policy(self):
        s = make_scenario(
            expected_optimal={"supplier": "SupplierA"},
            evaluation_weights={"supplier_match": 0.5, "policy_adherence": 0.5},
            context={
                "policy": {
                    "approved_vendor_list": ["SupplierA", "SupplierB"],
                    "budget_ceiling_per_unit": 100.0,
                },
                "suppliers": [
                    {"name": "SupplierA", "unit_price": 90.0},
                    {"name": "SupplierB", "unit_price": 95.0},
                ],
            },
        )
        r = make_response(s.id, {"selected_supplier": "SupplierA"})
        result = score_pillar1(s, r)

        assert result.metrics["policy_adherence"] == pytest.approx(1.0)
        assert result.score == pytest.approx(1.0)

    def test_weighted_score_with_policy_violation(self):
        """policy_adherence: 0.5 weight → wrong supplier + policy violation = 0.0 total."""
        s = make_scenario(
            expected_optimal={"supplier": "SupplierA"},
            evaluation_weights={"supplier_match": 0.5, "policy_adherence": 0.5},
            context={
                "policy": {
                    "approved_vendor_list": ["SupplierA"],
                }
            },
        )
        r = make_response(s.id, {"selected_supplier": "SupplierB"})
        result = score_pillar1(s, r)

        assert result.score == pytest.approx(0.0)
