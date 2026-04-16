"""Pillar 2 evaluator — Economic Decision Quality and Behavioral Robustness.

INTERNAL RATIONALITY SCOPE
--------------------------
This evaluator tests *internal* rationality: whether an agent optimizes the
objective function *as stated* in each scenario's ``evaluation_weights`` YAML
field.  We do NOT claim that those weights represent the uniquely correct or
universally rational preference ordering.  The ground truth here is
algorithmic — derived deterministically from the scenario definition — not an
externally validated economic optimum.

Concretely:
  * ``expected_optimal`` in each scenario YAML is computed from the scenario's
    own evaluation weights.
  * ``optimal_choice_rate`` == 1.0 means the agent matched that scenario-defined
    best choice, nothing more.
  * ``bias_susceptibility_index`` (BSI) measures whether the agent's choice
    changes across economically-equivalent presentation variants (baseline vs.
    framing/anchor/decoy).  A BSI > 0 means the agent's choice is *inconsistent
    with its own stated objective* across variants — not that the agent is irrational
    in some absolute sense.

This framing is the correct response to the "no ground truth" critique: we
measure deviation from the stated objective, making the claim falsifiable and
scope-limited.  Any cross-scenario generalization must restrict claims to
"procurement decision-making" and label them accordingly.

DOMAIN SCOPE
------------
All results produced by this evaluator are scoped to **LLM-based procurement
decision-making** — specifically, the final supplier/contract selection step
when structured options are presented to an agent.

Domain specificity is a deliberate feature, not a flaw:
  * Applied relevance: procurement automation is an active deployment context
    for LLM agents, making bias effects here practically significant.
  * Ecological validity: scenarios mirror real procurement inputs (supplier
    catalogs, unit prices, quality scores, delivery terms) rather than abstract
    lotteries, increasing applicability to deployed systems.
  * Scope control: restricting to one domain enables tighter experimental
    control and avoids conflating context effects across dissimilar tasks.

Claims about anchoring, framing, decoy, or scarcity effects from this
evaluator MUST be stated as:
  "Bias susceptibility in LLM-based procurement decision-making."

Claims MUST NOT be stated as:
  "LLMs exhibit anchoring bias [in general]" — that requires replication
  across additional domains (contract negotiation, investment decisions,
  hiring, etc.) and is explicitly out of scope for this study.

Future work: extending these scenarios to contract negotiation and capital
allocation domains would test whether procurement-observed effects generalize.

PROMPT SENSITIVITY
------------------
A genuine threat to validity: BSI values may be a property of the *specific
prompt wording* chosen by researchers rather than a stable model property.
Slight rephrasing (e.g., "Please select the best supplier" vs. "Which supplier
would you recommend?") can shift BSI by >0.1, making results non-replicable.

This threat cannot be eliminated by design — it must be measured and reported.

Mandatory robustness check (REV-5 from the red-team plan): before the main
experiment, run a 5-run pilot at 3 prompt phrasings per scenario.  Compute
the coefficient of variation (CV = population_std / mean) of mean-BSI across
phrasings.  If CV > 0.50, the scenario wording is unstable and must be
redesigned before data collection proceeds.  This is an explicit go/no-go gate.

The ``compute_prompt_sensitivity`` function in this module implements the check.
All CV values — whether robust or not — must be reported in the paper's
Appendix D (robustness checks).  Do not selectively report only passing checks.

Interpretation of CV:
  * CV ≤ 0.20 — low sensitivity; wording has negligible effect
  * 0.20 < CV ≤ 0.50 — moderate; report but may proceed
  * CV > 0.50 — high sensitivity; result is wording-dependent → redesign

Edge case: if mean BSI across all phrasings is 0.0 (model always chooses
optimally regardless of prompt wording), CV is defined as 0.0 — this is
actually the most robust finding possible.

HYPOTHETICAL CHOICE FRAMING
---------------------------
LLMs do not receive monetary payoffs.  Classic behavioral economics results
(Kahneman, Thaler, Tversky) were established with real financial stakes.
This raises the objection that our measured "biases" may be superficial text
pattern reproduction rather than genuine decision-theoretic failures.

This limitation is unavoidable given current technology.  The appropriate
response is to frame results explicitly:

  "We test *behavioral consistency* — whether an agent's choice changes
   across economically equivalent presentation variants — not incentivized
   decision-making.  The agent operates in a context where it has been told
   its procurement decision is consequential.  This is analogous to
   hypothetical-choice studies in behavioral economics (Camerer & Hogarth,
   1999), which show bias effects comparable to incentivized designs."

This framing does not eliminate the objection, but it accurately characterizes
the study scope and situates it within established methodological practice.

Claims from this evaluator MUST be stated as:
  "Behavioral consistency under [bias type] presentation manipulations,
   in hypothetical-choice procurement tasks."

Claims MUST NOT be stated as:
  "LLMs exhibit [bias] in the same way that humans with real financial stakes
   do" — that requires incentivized replication and is out of scope.

The ``incentive_framing`` field in ``aggregate_bias_report`` output is a
machine-readable anchor for this limitation so that all downstream JSON/CSV
consumers carry this framing alongside the BSI values.

SAMPLE SIZE LIMITATION
----------------------
With N=1 run per (model × scenario) cell, BSI values are single-realization
observations, not distributions.  A model that exhibits a bias with probability
p=0.4 will score BSI=0 roughly 60% of the time from a single run — making
single-run data entirely uninformative about true bias rates.

Critical implications:
  * Single-run BSI == 0 does NOT mean the model is unbiased.
  * Single-run BSI == 1 does NOT mean the model is reliably biased.
  * No statistical test (t-test, BH correction, mixed-effects model) is valid
    on N=1 per cell data.  A "significant" result from a single run is
    meaningless.

The mandatory minimum is **N=50 independent runs per (model × scenario)
cell** before any inferential claim.  N=5 is adequate for pilot feasibility
checks (Gate 1) but not for paper evidence.

Use protocol:
  * Current single-run session data is EXPLORATORY ONLY — use it to verify
    infrastructure, check schema correctness, and estimate costs.
  * Do not report single-run BSI values as evidence in the paper.
  * Gate 1 (pilot at N=5): verify error rate < 5% and at least 2/10 models
    show mean_BSI > 0.05 on at least 1 bias type.

The ``exploratory_only`` field in ``aggregate_bias_report`` is True whenever
``n_runs_per_cell`` is None or ≤ 1, providing a machine-readable flag that
downstream consumers can check before treating BSI values as inference-valid.
The ``sample_size_warning`` field carries the limitation text for JSON/CSV
consumers that log metadata alongside results.
"""
from __future__ import annotations

from buyerbench.models import AgentResponse, EvaluationResult, Pillar, PillarScore, Scenario


def score_pillar2(scenario: Scenario, response: AgentResponse) -> PillarScore:
    """Score Pillar 2: Economic Decision Quality and Behavioral Robustness.

    Computes optimal_choice_rate, optimality_gap, expected_value_regret, and
    bias_susceptibility_index for a single scenario evaluation.

    "Optimal" is defined relative to the scenario's own ``evaluation_weights``
    and ``expected_optimal`` fields — this is an *internal* rationality test,
    not a claim about external or universal economic optimality.
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

    The BSI measures *decision inconsistency* across economically equivalent
    presentation variants.  A baseline and variant share identical underlying
    economics (same suppliers, same evaluation weights, same expected_optimal)
    but differ in how the choice set is framed (anchor values, gain/loss
    framing, decoy options, scarcity cues, etc.).

    A rational agent — one that optimizes the scenario's stated objective
    regardless of irrelevant contextual cues — should make the same choice in
    both variants, yielding BSI == 0.0.  BSI > 0 indicates susceptibility to
    presentation effects that are economically irrelevant according to the
    scenario's own objective function.

    Note: BSI captures *behavioral inconsistency*, not incentivized decision
    failure.  LLMs do not receive monetary payoffs; results should be framed
    as hypothetical-choice consistency tests (analogous to Camerer & Hogarth
    1999), not incentivized economic experiments.

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


def compute_warp_transitivity(
    ab_result: EvaluationResult,
    bc_result: EvaluationResult,
    ac_result: EvaluationResult,
    supplier_a: str,
    supplier_b: str,
    supplier_c: str,
) -> dict:
    """Check for WARP (Weak Axiom of Revealed Preference) violations across
    three binary pairwise choice tasks.

    Given three binary choice tasks — AB (choose between A and B), BC (choose
    between B and C), and AC (choose between A and C) — a rational agent must
    exhibit transitive preferences.  A WARP violation occurs when the three
    choices form a cyclic preference: A>B, B>C but C>A (or the reverse cycle
    B>A, C>B but A>C).

    Args:
        ab_result: EvaluationResult for the AB pairwise task.
        bc_result: EvaluationResult for the BC pairwise task.
        ac_result: EvaluationResult for the AC pairwise task.
        supplier_a: Name of supplier A (appears in AB and AC tasks).
        supplier_b: Name of supplier B (appears in AB and BC tasks).
        supplier_c: Name of supplier C (appears in BC and AC tasks).

    Returns:
        dict with fields:
            warp_violated: bool — True if choices form a cycle.
            transitivity_preserved: bool — inverse of warp_violated.
            choice_ab: str or None — agent's choice in the AB task.
            choice_bc: str or None — agent's choice in the BC task.
            choice_ac: str or None — agent's choice in the AC task.
            a_over_b: bool — True if agent chose supplier_a in the AB task.
            b_over_c: bool — True if agent chose supplier_b in the BC task.
            a_over_c: bool — True if agent chose supplier_a in the AC task.
            warp_cycle_type: str or None — cycle description if violated.
            pair_id: str or None — variant_pair_id shared by all three tasks.
    """
    choice_ab = ab_result.decisions.get("selected_supplier") or ab_result.decisions.get(
        "supplier"
    )
    choice_bc = bc_result.decisions.get("selected_supplier") or bc_result.decisions.get(
        "supplier"
    )
    choice_ac = ac_result.decisions.get("selected_supplier") or ac_result.decisions.get(
        "supplier"
    )

    a_over_b = choice_ab == supplier_a
    b_over_c = choice_bc == supplier_b
    a_over_c = choice_ac == supplier_a

    # Cycle 1: A>B AND B>C BUT C>A (transitivity requires A>C, but agent chose C)
    warp_cycle_fwd = a_over_b and b_over_c and not a_over_c
    # Cycle 2: B>A AND C>B BUT A>C (transitivity requires C>A, but agent chose A)
    warp_cycle_rev = not a_over_b and not b_over_c and a_over_c

    warp_violated = warp_cycle_fwd or warp_cycle_rev

    return {
        "warp_violated": warp_violated,
        "transitivity_preserved": not warp_violated,
        "choice_ab": choice_ab,
        "choice_bc": choice_bc,
        "choice_ac": choice_ac,
        "a_over_b": a_over_b,
        "b_over_c": b_over_c,
        "a_over_c": a_over_c,
        "warp_cycle_type": (
            f"{supplier_a}>{supplier_b}>{supplier_c}>{supplier_a}"
            if warp_cycle_fwd
            else (
                f"{supplier_b}>{supplier_a}>{supplier_c}>{supplier_b}"
                if warp_cycle_rev
                else None
            )
        ),
        "pair_id": ab_result.variant_pair_id,
    }


def aggregate_bias_report(
    pair_results: list[dict],
    n_runs_per_cell: int | None = None,
) -> dict:
    """Summarize BSI across all variant pairs.

    Returns per-variant-type mean BSI, overall mean BSI, and count of
    pairs where decision_changed == True.

    The ``domain_scope`` field in the returned dict is a machine-readable
    anchor for the single-domain limitation (CRITIQUE 2): all BSI values
    here are valid *only* for LLM-based procurement decision-making and
    must not be generalized to other decision domains without replication.

    The ``incentive_framing`` field is a machine-readable anchor for the
    no-incentives limitation (CRITIQUE 4): results characterize behavioral
    consistency in hypothetical-choice tasks, not incentivized decision-making.

    The ``exploratory_only`` field is True when ``n_runs_per_cell`` is None
    or ≤ 1 (CRITIQUE 5): single-run BSI values are individual realizations,
    not distributions, and no statistical inference is valid on them.  Pass
    the actual run count per cell so downstream consumers can gate on this flag
    before treating BSI values as inference-valid.

    The ``sample_size_warning`` field carries the same limitation as a
    human-readable string for JSON/CSV logging alongside BSI values.

    Args:
        pair_results: list of dicts from ``compute_bias_susceptibility``.
        n_runs_per_cell: number of independent runs per (model × scenario)
            cell.  None or ≤ 1 triggers ``exploratory_only=True``.
            N ≥ 50 is required for inferential claims; N ≥ 5 for pilot gates.
    """
    _INCENTIVE_FRAMING = (
        "hypothetical-choice consistency; no monetary payoffs (cf. Camerer & Hogarth 1999)"
    )
    _SAMPLE_SIZE_WARNING = (
        "N=1 per cell: single-realization data; exploratory only — "
        "N≥50 required for inference (N≥5 for pilot gates)"
    )

    exploratory_only = n_runs_per_cell is None or n_runs_per_cell <= 1

    if not pair_results:
        return {
            "total_pairs": 0,
            "pairs_with_decision_change": 0,
            "mean_bsi": 0.0,
            "per_variant_type": {},
            "domain_scope": "LLM-based procurement decision-making",
            "incentive_framing": _INCENTIVE_FRAMING,
            "n_runs_per_cell": n_runs_per_cell,
            "exploratory_only": exploratory_only,
            "sample_size_warning": _SAMPLE_SIZE_WARNING,
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
        "domain_scope": "LLM-based procurement decision-making",
        "incentive_framing": _INCENTIVE_FRAMING,
        "n_runs_per_cell": n_runs_per_cell,
        "exploratory_only": exploratory_only,
        "sample_size_warning": _SAMPLE_SIZE_WARNING,
    }


def compute_prompt_sensitivity(
    bsi_by_phrasing: dict[str, list[float]],
    cv_threshold: float = 0.50,
) -> dict:
    """Compute a prompt-sensitivity report across multiple prompt phrasings.

    Takes BSI values from pilot runs for each of 2+ prompt phrasings of the
    *same* scenario.  Computes the coefficient of variation (CV = population
    std / mean) across per-phrasing mean BSI values to test whether the
    measured bias is a stable model property or an artifact of the specific
    wording.

    Per REV-5: if CV > cv_threshold (default 0.50), the scenario is wording-
    sensitive and must be redesigned before any main experiment data is
    collected.  If mean BSI is 0.0 across all phrasings, CV is set to 0.0
    (the model is robustly optimal regardless of wording — the strongest
    possible robustness finding).

    Args:
        bsi_by_phrasing: dict mapping phrasing label → list of BSI floats
            from pilot runs (e.g. ``{"phrasing_a": [0.2, 0.0, 0.4], ...}``).
            At least 2 phrasings required; each list should contain ≥2 runs.
        cv_threshold: coefficient of variation above which the result is
            considered wording-sensitive.  Per REV-5, the go/no-go gate is
            0.50.

    Returns:
        dict with fields:
            phrasings: int — number of prompt phrasings evaluated.
            per_phrasing_mean_bsi: dict — mean BSI per phrasing label.
            mean_of_means: float — grand mean of per-phrasing mean BSI values.
            std_of_means: float — population std-dev across phrasing means.
            cv: float — coefficient of variation; 0.0 when mean_of_means == 0.
            cv_threshold: float — the threshold value used for the go/no-go.
            robust: bool — True when CV ≤ cv_threshold (safe to proceed).
            recommendation: str — ``"PROCEED"`` or ``"REDESIGN"``.

    Raises:
        ValueError: if fewer than 2 phrasings are provided.
    """
    if len(bsi_by_phrasing) < 2:
        raise ValueError(
            "compute_prompt_sensitivity requires at least 2 prompt phrasings; "
            f"got {len(bsi_by_phrasing)}."
        )

    per_phrasing_mean: dict[str, float] = {
        label: (sum(vals) / len(vals)) if vals else 0.0
        for label, vals in bsi_by_phrasing.items()
    }

    means = list(per_phrasing_mean.values())
    mean_of_means = sum(means) / len(means)

    # Population std-dev (we're characterising these specific phrasings, not a sample)
    variance = sum((m - mean_of_means) ** 2 for m in means) / len(means)
    std_of_means = variance ** 0.5

    # CV is undefined when the mean is zero; treat as 0.0 — perfect robustness
    cv = std_of_means / mean_of_means if mean_of_means > 0.0 else 0.0

    robust = cv <= cv_threshold

    return {
        "phrasings": len(bsi_by_phrasing),
        "per_phrasing_mean_bsi": per_phrasing_mean,
        "mean_of_means": mean_of_means,
        "std_of_means": std_of_means,
        "cv": cv,
        "cv_threshold": cv_threshold,
        "robust": robust,
        "recommendation": "PROCEED" if robust else "REDESIGN",
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
