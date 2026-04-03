from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from buyerbench.models import AgentResponse, EvaluationResult, Pillar, Scenario
from evaluators.pillar1 import score_pillar1
from evaluators.pillar2 import score_pillar2, compute_bias_susceptibility, aggregate_bias_report
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


def compute_bsi_from_experiment_dir(
    experiment_dir: str | Path,
    scenarios_root: str | Path | None = None,
) -> dict:
    """Compute Bias Susceptibility Index by reading result JSONs from an experiment directory.

    Walks ``experiment_dir`` for per-agent subdirectories, loads all non-skipped result
    JSONs, groups Pillar 2 results by variant pair, and computes BSI for each agent.
    Skipped results (status=skipped sentinel files) are counted but excluded from BSI
    computation.

    Args:
        experiment_dir: Directory produced by ``run --output-dir``.  Contains one
            sub-directory per agent, each holding ``<scenario_id>.json`` files.
        scenarios_root: Path to the ``scenarios/`` directory for variant metadata.
            Defaults to the package-relative ``scenarios/`` directory.

    Returns:
        A structured dict with per-agent BSI results and a cross-agent summary, suitable
        for serialisation to ``bias-susceptibility-summary.json``.
    """
    experiment_dir = Path(experiment_dir)

    # ── load scenario metadata for variant classification ─────────────────────
    if scenarios_root is None:
        scenarios_root = Path(__file__).parent.parent / "scenarios"
    from harness.loader import load_all_scenarios

    all_scenarios = load_all_scenarios(str(scenarios_root))
    scenario_by_id: dict[str, Scenario] = {s.id: s for s in all_scenarios}

    # ── walk per-agent subdirectories ─────────────────────────────────────────
    total_files = 0
    skipped_files = 0
    valid_files = 0

    # agent_id → pair_id → list[EvaluationResult]
    per_agent_pairs: dict[str, dict[str, list[EvaluationResult]]] = {}

    for agent_dir in sorted(experiment_dir.iterdir()):
        if not agent_dir.is_dir():
            continue
        agent_id = agent_dir.name

        for json_file in sorted(agent_dir.glob("*.json")):
            total_files += 1
            raw = json.loads(json_file.read_text())

            if raw.get("status") == "skipped":
                skipped_files += 1
                continue

            # Deserialize as EvaluationResult
            try:
                result = EvaluationResult.model_validate(raw)
            except Exception:
                skipped_files += 1
                continue

            # Only care about Pillar 2 results with a variant_pair_id
            if not result.variant_pair_id:
                continue
            has_p2 = any(ps.pillar == Pillar.PILLAR2 for ps in result.pillar_scores)
            if not has_p2:
                continue

            valid_files += 1
            per_agent_pairs.setdefault(agent_id, {}).setdefault(
                result.variant_pair_id, []
            ).append(result)

    # ── compute BSI per agent per pair ────────────────────────────────────────
    per_agent_bsi: dict[str, dict] = {}
    all_pair_bsi: list[dict] = []

    for agent_id, pair_map in per_agent_pairs.items():
        agent_pair_bsi: list[dict] = []

        for pair_id, members in pair_map.items():
            if len(members) != 2:
                continue

            r0, r1 = members
            s0 = scenario_by_id.get(r0.scenario_id)
            s1 = scenario_by_id.get(r1.scenario_id)

            # Identify baseline by Scenario.variant == BASELINE; fall back to first
            if s0 is not None and s0.variant.value == "BASELINE":
                baseline_result, variant_result = r0, r1
            elif s1 is not None and s1.variant.value == "BASELINE":
                baseline_result, variant_result = r1, r0
            else:
                baseline_result, variant_result = r0, r1

            bsi = compute_bias_susceptibility(baseline_result, variant_result)
            bsi["agent_id"] = agent_id
            agent_pair_bsi.append(bsi)
            all_pair_bsi.append(bsi)

        per_agent_bsi[agent_id] = {
            "pair_bsi_results": agent_pair_bsi,
            "bias_report": aggregate_bias_report(agent_pair_bsi),
        }

    # ── cross-agent summary ───────────────────────────────────────────────────
    cross_agent_summary = aggregate_bias_report(all_pair_bsi)

    return {
        "experiment_dir": str(experiment_dir),
        "generated_at": datetime.utcnow().isoformat(),
        "total_result_files": total_files,
        "skipped_result_files": skipped_files,
        "valid_result_files": valid_files,
        "agents_evaluated": sorted(per_agent_bsi.keys()),
        "agents_skipped": sorted(
            agent_dir.name
            for agent_dir in experiment_dir.iterdir()
            if agent_dir.is_dir() and agent_dir.name not in per_agent_bsi
        ),
        "per_agent_bsi": per_agent_bsi,
        "cross_agent_summary": cross_agent_summary,
    }
