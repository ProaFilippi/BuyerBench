from __future__ import annotations

import json
from pathlib import Path

from buyerbench.models import EvaluationResult, Scenario
from evaluators.aggregate import run_evaluation


def run_scenario(
    scenario: Scenario,
    agent,
    output_dir: str | Path | None = None,
    run_index: int = 0,
) -> EvaluationResult:
    """Run a single scenario through an agent and evaluate the result.

    Saves the JSON result to ``<output_dir>/<agent_id>/<scenario_id>-run<NNN>.json``.
    When *output_dir* is ``None`` the legacy path ``results/<agent_id>/`` is used.

    Args:
        scenario:    The scenario to evaluate.
        agent:       The agent under evaluation.
        output_dir:  Directory to write result JSON files.
        run_index:   0-based index of this run within the cell (used in file naming
                     and stored on the result for downstream aggregation).
    """
    response = agent.respond(scenario)
    result = run_evaluation(scenario, response)
    result.run_index = run_index

    base = Path(output_dir) if output_dir else Path("results")
    dest_dir = base / response.agent_id
    dest_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{scenario.id}-run{run_index:03d}.json"
    (dest_dir / filename).write_text(result.model_dump_json(indent=2))

    return result
