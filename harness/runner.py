from __future__ import annotations

import json
from pathlib import Path

from buyerbench.models import EvaluationResult, Scenario
from evaluators.aggregate import run_evaluation


def run_scenario(
    scenario: Scenario,
    agent,
    output_dir: str | Path | None = None,
) -> EvaluationResult:
    """Run a single scenario through an agent and evaluate the result.

    Saves the JSON result to ``<output_dir>/<agent_id>/<scenario_id>.json``.
    When *output_dir* is ``None`` the legacy path ``results/<agent_id>/`` is used.
    """
    response = agent.respond(scenario)
    result = run_evaluation(scenario, response)

    base = Path(output_dir) if output_dir else Path("results")
    dest_dir = base / response.agent_id
    dest_dir.mkdir(parents=True, exist_ok=True)
    (dest_dir / f"{scenario.id}.json").write_text(result.model_dump_json(indent=2))

    return result
