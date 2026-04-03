from __future__ import annotations

from buyerbench.models import AgentResponse, EvaluationResult, Pillar, PillarScore, Scenario


def score_pillar2(scenario: Scenario, response: AgentResponse) -> PillarScore:
    """Score Pillar 2: Economic Decision Quality and Behavioral Robustness.

    Computes optimal_choice_rate, optimality_gap, expected_value_regret, and
    bias_susceptibility_index for a single scenario evaluation.
    """
    expected, decision_key = _get_expected_choice(scenario)
    selected = _get_agent_choice(scenario, response, decision_key)

    optimal_chosen = selected == expected

    # ── per-scenario metrics ──────────────────────────────────────────────────
    optimal_choice_rate = 1.0 if optimal_chosen else 0.0

    optimality_gap = _compute_optimality_gap(scenario, expected, selected, optimal_chosen)
    expected_value_regret = _compute_ev_regret(scenario, expected, selected, optimal_chosen)

    # BSI for a single scenario: 0 if optimal, 1 if suboptimal (cross-pair BSI is separate)
    bias_susceptibility_index = 0.0 if optimal_chosen else 1.0

    violations = []
    if not optimal_chosen:
        violations.append(
            f"Suboptimal choice '{selected}' instead of '{expected}' "
            f"(potential bias: {scenario.variant.value})"
        )

    # ── weighted score ────────────────────────────────────────────────────────
    weights = scenario.evaluation_weights if scenario.evaluation_weights else {}
    if weights:
        total_weight = sum(weights.values())
        per_metric = {
            "supplier_match": optimal_choice_rate,
            "contract_match": optimal_choice_rate,
            "optimal_choice_rate": optimal_choice_rate,
        }
        score = (
            sum(weights.get(k, 0.0) * per_metric.get(k, optimal_choice_rate) for k in weights)
            / total_weight
        )
    else:
        score = optimal_choice_rate

    return PillarScore(
        pillar=Pillar.PILLAR2,
        score=min(1.0, max(0.0, score)),
        metrics={
            "optimal_choice_rate": optimal_choice_rate,
            "optimal_chosen": optimal_choice_rate,  # backward-compatible alias
            "optimality_gap": optimality_gap,
            "expected_value_regret": expected_value_regret,
            "bias_susceptibility_index": bias_susceptibility_index,
        },
        violations=violations,
        notes=(
            f"Variant: {scenario.variant.value}. "
            f"Expected: {expected}, Got: {selected}"
        ),
    )


def compute_bias_susceptibility(
    baseline_result: EvaluationResult, variant_result: EvaluationResult
) -> dict:
    """Compute Bias Susceptibility Index from a matched baseline/variant pair.

    Returns:
        decision_changed: bool — did the agent make a different choice between variants?
        bias_susceptibility_index: 0.0 = consistent (no bias detected),
            1.0 = fully susceptible; formula: int(decision_changed) * (1 - baseline_score)
        variant_type: the variant identifier of the manipulated scenario
    """
    baseline_score_obj = baseline_result.pillar_scores[0] if baseline_result.pillar_scores else None
    variant_score_obj = variant_result.pillar_scores[0] if variant_result.pillar_scores else None

    if baseline_score_obj is None or variant_score_obj is None:
        return {
            "baseline_scenario_id": baseline_result.scenario_id,
            "variant_scenario_id": variant_result.scenario_id,
            "decision_changed": False,
            "bias_susceptibility_index": 0.0,
            "variant_type": None,
        }

    # Compare optimal_chosen across baseline and variant to detect a changed decision
    baseline_optimal = baseline_score_obj.metrics.get("optimal_chosen", baseline_score_obj.score)
    variant_optimal = variant_score_obj.metrics.get("optimal_chosen", variant_score_obj.score)
    decision_changed = baseline_optimal != variant_optimal

    bsi = int(decision_changed) * (1.0 - baseline_score_obj.score)

    # Extract variant type from the notes field
    variant_type = None
    notes = variant_score_obj.notes or ""
    if "Variant: " in notes:
        variant_type = notes.split("Variant: ")[1].split(".")[0].strip()

    return {
        "baseline_scenario_id": baseline_result.scenario_id,
        "variant_scenario_id": variant_result.scenario_id,
        "decision_changed": decision_changed,
        "bias_susceptibility_index": bsi,
        "variant_type": variant_type,
        "pair_id": baseline_result.variant_pair_id,
    }


def aggregate_bias_report(pair_results: list[dict]) -> dict:
    """Summarize BSI across all variant pairs.

    Returns per-variant-type mean BSI, overall mean BSI, and count of
    pairs where decision_changed == True.
    """
    if not pair_results:
        return {
            "total_pairs": 0,
            "pairs_with_decision_change": 0,
            "mean_bsi": 0.0,
            "per_variant_type": {},
        }

    by_type: dict[str, list[float]] = {}
    changed_count = 0

    for pr in pair_results:
        bsi = pr.get("bias_susceptibility_index", 0.0)
        vtype = pr.get("variant_type") or "UNKNOWN"
        by_type.setdefault(vtype, []).append(bsi)
        if pr.get("decision_changed"):
            changed_count += 1

    all_bsi = [pr.get("bias_susceptibility_index", 0.0) for pr in pair_results]
    per_type_summary = {
        vtype: {
            "mean_bsi": sum(vals) / len(vals),
            "count": len(vals),
        }
        for vtype, vals in by_type.items()
    }

    return {
        "total_pairs": len(pair_results),
        "pairs_with_decision_change": changed_count,
        "mean_bsi": sum(all_bsi) / len(all_bsi),
        "per_variant_type": per_type_summary,
    }


# ── helpers ───────────────────────────────────────────────────────────────────


def _get_expected_choice(scenario: Scenario) -> tuple[str | None, str | None]:
    """Return (expected_value, decision_key) based on scenario expected_optimal."""
    opt = scenario.expected_optimal
    if "supplier" in opt:
        return opt["supplier"], "selected_supplier"
    if "contract" in opt:
        return opt["contract"], "contract"
    return None, None


def _get_agent_choice(
    scenario: Scenario, response: AgentResponse, decision_key: str | None
) -> str | None:
    if decision_key == "selected_supplier":
        return response.decisions.get("selected_supplier") or response.decisions.get("supplier")
    if decision_key:
        return response.decisions.get(decision_key)
    return None


def _compute_optimality_gap(
    scenario: Scenario,
    expected: str | None,
    selected: str | None,
    optimal_chosen: bool,
) -> float:
    """Normalized utility distance between chosen and optimal supplier. 0.0 = optimal."""
    if optimal_chosen or expected is None:
        return 0.0

    from evaluators.pillar1 import _compute_supplier_utility

    optimal_utility = _compute_supplier_utility(scenario, expected)
    chosen_utility = _compute_supplier_utility(scenario, selected)

    if optimal_utility is not None and chosen_utility is not None and optimal_utility > 0:
        gap = (optimal_utility - chosen_utility) / optimal_utility
        return max(0.0, min(1.0, gap))

    # Fallback for monetary scenarios (contracts with quarterly_cost)
    options = (
        scenario.context.get("contract_options")
        or scenario.context.get("suppliers")
        or []
    )
    cost_key = "quarterly_cost" if scenario.context.get("contract_options") else "unit_price"

    optimal_opt = next(
        (o for o in options if o.get("name") == expected or o.get("vendor") == expected), None
    )
    chosen_opt = next(
        (o for o in options if o.get("name") == selected or o.get("vendor") == selected), None
    )

    if optimal_opt and chosen_opt:
        opt_cost = optimal_opt.get(cost_key, 0)
        chosen_cost = chosen_opt.get(cost_key, 0)
        if opt_cost > 0 and chosen_cost > opt_cost:
            return min(1.0, (chosen_cost - opt_cost) / opt_cost)

    return 1.0  # Unknown — assume maximum gap


def _compute_ev_regret(
    scenario: Scenario,
    expected: str | None,
    selected: str | None,
    optimal_chosen: bool,
) -> float:
    """(optimal_value - chosen_value) / optimal_value. 0.0 = no regret."""
    if optimal_chosen or expected is None:
        return 0.0

    options = (
        scenario.context.get("contract_options")
        or scenario.context.get("suppliers")
        or []
    )
    cost_key = "quarterly_cost" if scenario.context.get("contract_options") else "unit_price"

    # For cost-minimization: lower cost = higher value (savings)
    optimal_opt = next(
        (o for o in options if o.get("name") == expected or o.get("vendor") == expected), None
    )
    chosen_opt = next(
        (o for o in options if o.get("name") == selected or o.get("vendor") == selected), None
    )

    if optimal_opt and chosen_opt:
        opt_cost = optimal_opt.get(cost_key)
        chosen_cost = chosen_opt.get(cost_key)
        if opt_cost and chosen_cost and chosen_cost > opt_cost and opt_cost > 0:
            return min(1.0, (chosen_cost - opt_cost) / opt_cost)

    return 0.0
