from __future__ import annotations

from buyerbench.models import AgentResponse, Pillar, PillarScore, Scenario

_PO_REQUIRED_FIELDS = [
    "vendor_name",
    "product_description",
    "quantity",
    "unit_price",
    "total_amount",
    "payment_terms",
    "requested_delivery_date",
    "iso_certification_confirmed",
]

# Maps evaluation_weight keys for workflow steps to their decision dict keys
_STEP_DECISION_KEYS = {
    "step1_candidates_correct": "step1_all_candidates",
    "step2_scores_accurate": "step2_scores",
    "step3_selection_correct": "step3_selection",
    "step4_po_complete": "step4_purchase_order",
}


def score_pillar1(scenario: Scenario, response: AgentResponse) -> PillarScore:
    """Score Pillar 1: Agent Intelligence and Operational Capability."""
    metrics: dict[str, float] = {}
    violations: list[str] = []

    weights = scenario.evaluation_weights if scenario.evaluation_weights else {"supplier_match": 1.0}

    # ── task_completion_rate ──────────────────────────────────────────────────
    required = _required_decision_fields(weights)
    if required:
        present = sum(1 for f in required if response.decisions.get(f) is not None)
        metrics["task_completion_rate"] = present / len(required)
    else:
        metrics["task_completion_rate"] = 1.0 if response.decisions else 0.0

    # ── supplier_match ────────────────────────────────────────────────────────
    if "supplier_match" in weights:
        metrics["supplier_match"] = _compute_supplier_match(scenario, response, violations)

    # ── score_within_threshold ────────────────────────────────────────────────
    if "score_within_threshold" in weights:
        metrics["score_within_threshold"] = _compute_score_within_threshold(scenario, response)

    # ── policy_adherence ──────────────────────────────────────────────────────
    if "policy_adherence" in weights:
        metrics["policy_adherence"] = _compute_policy_adherence(scenario, response, violations)

    # ── extraction_accuracy ───────────────────────────────────────────────────
    if "extraction_accuracy" in weights:
        metrics["extraction_accuracy"] = _compute_extraction_accuracy(scenario, response)

    # ── constraint_adherence ──────────────────────────────────────────────────
    if "constraint_adherence" in weights:
        metrics["constraint_adherence"] = _compute_constraint_adherence(scenario, response, violations)

    # ── workflow step metrics ─────────────────────────────────────────────────
    for weight_key, decision_key in _STEP_DECISION_KEYS.items():
        if weight_key in weights:
            metrics[weight_key] = _compute_step_metric(
                scenario, response, weight_key, decision_key, violations
            )

    # ── tool_call_efficiency ──────────────────────────────────────────────────
    if response.tool_calls:
        relevant = [t for t in response.tool_calls if t.get("relevant", True)]
        metrics["tool_call_efficiency"] = len(relevant) / len(response.tool_calls)
    else:
        metrics["tool_call_efficiency"] = 1.0

    # ── weighted score ────────────────────────────────────────────────────────
    total_weight = sum(weights.values())
    if total_weight > 0:
        score = sum(weights.get(k, 0.0) * metrics.get(k, 0.0) for k in weights) / total_weight
    else:
        score = metrics.get("supplier_match", 0.0)

    selected = (
        response.decisions.get("selected_supplier")
        or response.decisions.get("supplier", "N/A")
    )
    return PillarScore(
        pillar=Pillar.PILLAR1,
        score=min(1.0, max(0.0, score)),
        metrics=metrics,
        violations=violations,
        notes=f"Weights: {weights}. Selected: {selected}",
    )


# ── helpers ───────────────────────────────────────────────────────────────────


def _required_decision_fields(weights: dict[str, float]) -> list[str]:
    """Derive the required decision keys from evaluation weight keys."""
    fields = []
    if "supplier_match" in weights:
        fields.append("selected_supplier")
    for weight_key, decision_key in _STEP_DECISION_KEYS.items():
        if weight_key in weights:
            fields.append(decision_key)
    return fields


def _compute_supplier_match(
    scenario: Scenario, response: AgentResponse, violations: list[str]
) -> float:
    expected = scenario.expected_optimal.get("supplier") or scenario.expected_optimal.get(
        "step3_selection"
    )
    selected = response.decisions.get("selected_supplier") or response.decisions.get("supplier")

    if expected is None:
        return 1.0

    if selected == expected:
        return 1.0

    violations.append(f"Selected '{selected}' but expected '{expected}'")

    # Partial credit: ratio of chosen utility to optimal utility via scoring model
    optimal_utility = _compute_supplier_utility(scenario, expected)
    chosen_utility = _compute_supplier_utility(scenario, selected) if selected else None

    if optimal_utility is not None and chosen_utility is not None and optimal_utility > 0:
        return max(0.0, chosen_utility / optimal_utility)

    return 0.0


def _compute_supplier_utility(scenario: Scenario, supplier_name: str | None) -> float | None:
    """Compute the weighted utility score for a named supplier using context.scoring_model."""
    if not supplier_name:
        return None

    scoring_model = scenario.context.get("scoring_model")
    if not scoring_model:
        return None

    suppliers = scenario.context.get("suppliers") or scenario.context.get("supplier_catalog", [])
    supplier = next((s for s in suppliers if s.get("name") == supplier_name), None)
    if not supplier:
        return None

    prices = [s["unit_price"] for s in suppliers if "unit_price" in s]
    if not prices or max(prices) == min(prices):
        cost_score = 1.0
    else:
        cost_score = (max(prices) - supplier["unit_price"]) / (max(prices) - min(prices))

    cost_w = scoring_model.get("cost_weight", 0.0)
    quality_w = scoring_model.get("quality_weight", 0.0)
    delivery_w = scoring_model.get("delivery_reliability_weight", 0.0)

    return (
        cost_w * cost_score
        + quality_w * supplier.get("quality_score", 0.0)
        + delivery_w * supplier.get("delivery_reliability", 0.0)
    )


def _compute_score_within_threshold(scenario: Scenario, response: AgentResponse) -> float:
    """1.0 if agent's reported weighted score is within 5% of expected optimal."""
    optimal_ws = scenario.expected_optimal.get("weighted_score")
    chosen_ws = response.decisions.get("weighted_score")

    if optimal_ws is not None and chosen_ws is not None:
        diff = abs(chosen_ws - optimal_ws) / (optimal_ws + 1e-9)
        return 1.0 if diff <= 0.05 else max(0.0, 1.0 - diff * 10)

    # Fallback: credit full weight if the correct supplier was chosen
    if response.decisions.get("selected_supplier") == scenario.expected_optimal.get("supplier"):
        return 1.0
    if response.decisions.get("supplier") == scenario.expected_optimal.get("supplier"):
        return 1.0

    return 0.0


def _compute_policy_adherence(
    scenario: Scenario, response: AgentResponse, violations: list[str]
) -> float:
    policy = scenario.context.get("policy", {})
    if not policy:
        return 1.0

    selected = response.decisions.get("selected_supplier") or response.decisions.get("supplier")
    if not selected:
        violations.append("No supplier selected — policy adherence cannot be verified")
        return 0.0

    ok = True

    vendor_list = policy.get("approved_vendor_list", [])
    if vendor_list and selected not in vendor_list:
        violations.append(
            f"Selected vendor '{selected}' is not on the approved vendor list"
        )
        ok = False

    budget_ceiling = policy.get("budget_ceiling_per_unit")
    if budget_ceiling:
        suppliers = scenario.context.get("suppliers", [])
        supplier_data = next((s for s in suppliers if s.get("name") == selected), None)
        if supplier_data:
            price = supplier_data.get("unit_price", 0)
            if price > budget_ceiling:
                violations.append(
                    f"Selected vendor '{selected}' price ${price} exceeds "
                    f"budget ceiling ${budget_ceiling}"
                )
                ok = False

    return 1.0 if ok else 0.0


def _compute_extraction_accuracy(scenario: Scenario, response: AgentResponse) -> float:
    """Fraction of expected procurement data fields correctly extracted."""
    extraction_fields = ["supplier", "unit_price", "lead_time_days", "iso_9001_certified"]
    expected = scenario.expected_optimal

    checkable = [f for f in extraction_fields if expected.get(f) is not None]
    if not checkable:
        return 1.0

    correct = sum(
        1 for f in checkable if response.decisions.get(f) == expected[f]
    )
    return correct / len(checkable)


def _compute_constraint_adherence(
    scenario: Scenario, response: AgentResponse, violations: list[str]
) -> float:
    """1.0 if selected supplier satisfies scenario constraints; partial credit otherwise."""
    expected = scenario.expected_optimal.get("supplier")
    selected = response.decisions.get("selected_supplier") or response.decisions.get("supplier")

    # If optimal supplier chosen, constraints are satisfied by definition
    if selected == expected:
        return 1.0

    # Check if the selected supplier violates any detectable constraints
    product_req = scenario.context.get("product_request", {})
    req_lead = product_req.get("required_lead_time_days")
    req_cert = product_req.get("required_certification")

    ok = True
    selected_lead = response.decisions.get("lead_time_days")
    selected_cert = response.decisions.get("iso_9001_certified")

    if req_lead is not None and selected_lead is not None and selected_lead > req_lead:
        violations.append(
            f"Selected supplier lead time {selected_lead}d exceeds maximum {req_lead}d"
        )
        ok = False

    if req_cert == "ISO 9001" and selected_cert is not None and not selected_cert:
        violations.append("Selected supplier lacks required ISO 9001 certification")
        ok = False

    return 1.0 if ok else 0.0


def _compute_step_metric(
    scenario: Scenario,
    response: AgentResponse,
    weight_key: str,
    decision_key: str,
    violations: list[str],
) -> float:
    expected_val = scenario.expected_optimal.get(decision_key)
    chosen_val = response.decisions.get(decision_key)

    if expected_val is None:
        return 1.0

    if weight_key == "step1_candidates_correct":
        expected_set = set(expected_val) if isinstance(expected_val, list) else {expected_val}
        if isinstance(chosen_val, list):
            chosen_set = set(
                item.get("name", str(item)) if isinstance(item, dict) else item
                for item in chosen_val
            )
        elif chosen_val:
            chosen_set = {chosen_val}
        else:
            chosen_set = set()
        if not expected_set:
            return 1.0
        correct = len(expected_set & chosen_set)
        score = correct / len(expected_set)
        if score < 1.0:
            missing = sorted(expected_set - chosen_set)
            violations.append(f"Step 1: Missing expected candidates {missing}")
        return score

    elif weight_key == "step2_scores_accurate":
        # Credit for providing scores (presence check)
        return 1.0 if chosen_val is not None else 0.0

    elif weight_key == "step3_selection_correct":
        if isinstance(chosen_val, dict):
            chosen_val = chosen_val.get("selected_supplier") or chosen_val.get("name")
        match = chosen_val == expected_val
        if not match:
            violations.append(
                f"Step 3: Selected '{chosen_val}' but expected '{expected_val}'"
            )
        return 1.0 if match else 0.0

    elif weight_key == "step4_po_complete":
        if not isinstance(chosen_val, dict):
            violations.append("Step 4: No purchase order draft produced")
            return 0.0
        required = scenario.context.get("purchase_order_required_fields", _PO_REQUIRED_FIELDS)
        present = sum(1 for f in required if chosen_val.get(f) is not None)
        score = present / len(required) if required else 1.0
        if score < 1.0:
            missing = [f for f in required if chosen_val.get(f) is None]
            violations.append(f"Step 4: PO missing fields: {missing}")
        return score

    return 1.0 if chosen_val == expected_val else 0.0
