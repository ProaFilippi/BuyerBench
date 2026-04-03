from __future__ import annotations

import json
from pathlib import Path

from buyerbench.models import EvaluationResult, Scenario
from evaluators.aggregate import run_evaluation


def run_scenario(scenario: Scenario, agent) -> EvaluationResult:
    """Run a single scenario through an agent and evaluate the result.

    Saves the JSON result to results/<agent_id>/<scenario_id>.json.
    """
    response = agent.respond(scenario)
    result = run_evaluation(scenario, response)

    output_dir = Path("results") / response.agent_id
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{scenario.id}.json"
    output_path.write_text(result.model_dump_json(indent=2))

    return result
