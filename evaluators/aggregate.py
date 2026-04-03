from __future__ import annotations

import json
from pathlib import Path

from buyerbench.models import AgentResponse, EvaluationResult, Pillar, Scenario
from evaluators.pillar1 import score_pillar1
from evaluators.pillar2 import score_pillar2, compute_bias_susceptibility
from evaluators.pillar3 import score_pillar3

_SCORERS = {
    Pillar.PILLAR1: score_pillar1,
    Pillar.PILLAR2: score_pillar2,
    Pillar.PILLAR3: score_pillar3,
}


def run_evaluation(scenario: Scenario, response: AgentResponse) -> EvaluationResult:
    """Run the appropriate pillar scorer(s) and assemble an EvaluationResult."""
    scorer = _SCORERS[scenario.pillar]
    pillar_score = scorer(scenario, response)

    overall_pass = pillar_score.score >= 0.95 and not pillar_score.violations

    return EvaluationResult(
        scenario_id=scenario.id,
        agent_id=response.agent_id,
        pillar_scores=[pillar_score],
        overall_pass=overall_pass,
        variant_pair_id=scenario.variant_pair_id,
    )


def run_suite(scenarios: list[Scenario], agent) -> list[EvaluationResult]:
    """Run all scenarios through the agent, compute BSI for variant pairs, and save results.

    Individual results are saved to results/<agent_id>/<scenario_id>.json.
    A summary.json is written to results/<agent_id>/summary.json after all runs.
    """
    results: list[EvaluationResult] = []
    scenario_by_id: dict[str, Scenario] = {s.id: s for s in scenarios}

    for scenario in scenarios:
        response = agent.respond(scenario)
        result = run_evaluation(scenario, response)

        output_dir = Path("results") / response.agent_id
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / f"{scenario.id}.json").write_text(result.model_dump_json(indent=2))

        results.append(result)

    # ── compute BSI for variant pairs ─────────────────────────────────────────
    pair_groups: dict[str, list[tuple[EvaluationResult, Scenario]]] = {}
    for r in results:
        if r.variant_pair_id:
            scen = scenario_by_id.get(r.scenario_id)
            if scen is not None:
                pair_groups.setdefault(r.variant_pair_id, []).append((r, scen))

    pair_bsi_results: list[dict] = []
    for pair_id, members in pair_groups.items():
        if len(members) != 2:
            continue
        (r0, s0), (r1, s1) = members
        # Prefer the BASELINE scenario as baseline; fall back to first member
        if s0.variant.value == "BASELINE":
            baseline_result, variant_result = r0, r1
        elif s1.variant.value == "BASELINE":
            baseline_result, variant_result = r1, r0
        else:
            baseline_result, variant_result = r0, r1

        bsi = compute_bias_susceptibility(baseline_result, variant_result)
        pair_bsi_results.append(bsi)

    # ── generate and save summary ─────────────────────────────────────────────
    if results:
        from results.report import generate_summary_report

        summary = generate_summary_report(results)
        summary["bias_susceptibility_pairs"] = pair_bsi_results

        from evaluators.pillar2 import aggregate_bias_report

        if pair_bsi_results:
            summary["bias_report"] = aggregate_bias_report(pair_bsi_results)

        agent_id = results[0].agent_id
        summary_path = Path("results") / agent_id / "summary.json"
        summary_path.write_text(json.dumps(summary, indent=2, default=str))

    return results
