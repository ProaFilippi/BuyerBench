"""Prompt robustness pilot for REV-5 (PILLAR2-RESEARCH-07 N.1).

Runs a small N=5 pilot across 3 minor prompt-phrasing variants of the same
scenarios and computes the coefficient of variation (CV) of mean BSI across
phrasings.  If CV > cv_threshold (default 0.50) the scenario wording is
unstable and must be redesigned before the main experiment proceeds.

Usage example::

    from harness.robustness_pilot import run_robustness_pilot
    from harness.prompt import REV5_PHRASINGS
    from agents.openrouter_agent import OpenRouterAgent

    phrasings = [
        (label, OpenRouterAgent(..., prompt_version=label))
        for label in REV5_PHRASINGS
    ]
    results = run_robustness_pilot(
        scenario_pairs=pairs,   # list of (baseline_scenario, variant_scenario)
        phrasings=phrasings,
        n_runs=5,
    )
    print(results["overall_recommendation"])  # "PROCEED" or "REDESIGN"

The returned dict is also written to ``<output_dir>/robustness_pilot.json`` when
*output_dir* is provided.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING

from evaluators.pillar2 import compute_bias_susceptibility, compute_prompt_sensitivity
from evaluators.aggregate import run_evaluation

if TYPE_CHECKING:
    from buyerbench.models import Scenario
    from agents import BaseAgent


def run_robustness_pilot(
    scenario_pairs: list[tuple["Scenario", "Scenario"]],
    phrasings: list[tuple[str, "BaseAgent"]],
    n_runs: int = 5,
    cv_threshold: float = 0.50,
    output_dir: str | Path | None = None,
) -> dict:
    """Run the REV-5 prompt robustness pilot across phrasing variants.

    For each scenario pair (baseline, variant) and each prompt phrasing
    (label, agent), runs *n_runs* independent trials.  For each trial, scores
    both the baseline and variant scenarios via the phrasing agent, computes
    BSI from the paired results, and accumulates per-phrasing BSI lists.
    After all runs, calls ``compute_prompt_sensitivity`` to check whether the
    CV of mean-BSI across phrasings exceeds *cv_threshold*.

    Args:
        scenario_pairs:
            List of (baseline_scenario, variant_scenario) tuples.  Each pair
            should share the same ``variant_pair_id`` and represent a matched
            economic-equivalence comparison (e.g. BASELINE vs ANCHOR_HIGH).
        phrasings:
            List of (label, agent) tuples.  Each agent must be pre-configured
            with the corresponding prompt_version so that
            ``agent.respond(scenario)`` uses the intended phrasing.  Typically
            built from ``harness.prompt.REV5_PHRASINGS`` with agents that have
            ``prompt_version`` set accordingly.
        n_runs:
            Number of independent runs per (phrasing × scenario_pair) cell.
            Per REV-5: pilot uses N=5; main experiment uses N=50.
        cv_threshold:
            CV above which a scenario is flagged as wording-sensitive.
            Default 0.50 (per REV-5 go/no-go gate).
        output_dir:
            Optional path.  When provided, ``robustness_pilot.json`` is
            written here with the full result dict.

    Returns:
        dict with:
            ``n_runs``: int — runs per cell.
            ``cv_threshold``: float — threshold used.
            ``phrasings``: list[str] — phrasing labels evaluated.
            ``per_scenario``: dict mapping pair_id → sensitivity report dict
                (output of ``compute_prompt_sensitivity``).
            ``scenarios_passing``: int — pairs with CV ≤ cv_threshold.
            ``scenarios_failing``: int — pairs with CV > cv_threshold.
            ``scenarios_to_redesign``: list[str] — pair_ids that failed.
            ``overall_recommendation``: ``"PROCEED"`` or ``"REDESIGN"``.
    """
    if len(phrasings) < 2:
        raise ValueError(
            "run_robustness_pilot requires at least 2 prompt phrasings; "
            f"got {len(phrasings)}."
        )

    phrasing_labels = [label for label, _ in phrasings]

    per_scenario: dict[str, dict] = {}

    for baseline_scenario, variant_scenario in scenario_pairs:
        pair_id = (
            baseline_scenario.variant_pair_id
            or f"{baseline_scenario.id}__{variant_scenario.id}"
        )

        # Accumulate per-phrasing BSI lists for this scenario pair.
        bsi_by_phrasing: dict[str, list[float]] = {
            label: [] for label in phrasing_labels
        }

        for label, agent in phrasings:
            for _ in range(n_runs):
                baseline_response = agent.respond(baseline_scenario)
                variant_response = agent.respond(variant_scenario)

                baseline_result = run_evaluation(baseline_scenario, baseline_response)
                variant_result = run_evaluation(variant_scenario, variant_response)

                bsi_record = compute_bias_susceptibility(baseline_result, variant_result)
                bsi_by_phrasing[label].append(bsi_record["bias_susceptibility_index"])

        sensitivity = compute_prompt_sensitivity(bsi_by_phrasing, cv_threshold=cv_threshold)
        per_scenario[pair_id] = sensitivity

    scenarios_to_redesign = [
        pair_id
        for pair_id, report in per_scenario.items()
        if not report["robust"]
    ]
    scenarios_passing = len(per_scenario) - len(scenarios_to_redesign)
    overall_recommendation = "PROCEED" if not scenarios_to_redesign else "REDESIGN"

    result = {
        "n_runs": n_runs,
        "cv_threshold": cv_threshold,
        "phrasings": phrasing_labels,
        "per_scenario": per_scenario,
        "scenarios_passing": scenarios_passing,
        "scenarios_failing": len(scenarios_to_redesign),
        "scenarios_to_redesign": scenarios_to_redesign,
        "overall_recommendation": overall_recommendation,
    }

    if output_dir is not None:
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)
        (out / "robustness_pilot.json").write_text(
            json.dumps(result, indent=2, default=str)
        )

    return result
