from __future__ import annotations

import json
import random
from pathlib import Path

from buyerbench.models import EvaluationResult, Scenario
from evaluators.aggregate import run_evaluation


def run_scenario(
    scenario: Scenario,
    agent,
    output_dir: str | Path | None = None,
    run_index: int = 0,
    supplier_order_seed: int | None = None,
) -> EvaluationResult:
    """Run a single scenario through an agent and evaluate the result.

    Saves the JSON result to ``<output_dir>/<agent_id>/<scenario_id>-run<NNN>.json``.
    When *output_dir* is ``None`` the legacy path ``results/<agent_id>/`` is used.

    Args:
        scenario:             The scenario to evaluate.
        agent:                The agent under evaluation.
        output_dir:           Directory to write result JSON files.
        run_index:            0-based index of this run within the cell (used in
                              file naming and stored on the result for downstream
                              aggregation).
        supplier_order_seed:  Seed controlling supplier list ordering in the
                              rendered prompt.  When ``None`` (default) a fresh
                              random seed is generated per run, ensuring each
                              independent repeat sees a different supplier order.
                              Pass an explicit integer to reproduce a specific run.
    """
    # Always generate a concrete seed so every run is independently replayable.
    seed = supplier_order_seed if supplier_order_seed is not None else random.randrange(2**31)

    # Pass a scenario copy with shuffled context to the agent; the original is
    # kept intact so run_evaluation() compares against the unmodified ground truth.
    shuffled_scenario = _shuffle_context(scenario, seed)

    response = agent.respond(shuffled_scenario)
    result = run_evaluation(scenario, response)
    result.run_index = run_index
    result.supplier_order_seed = seed

    base = Path(output_dir) if output_dir else Path("results")
    dest_dir = base / response.agent_id
    dest_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{scenario.id}-run{run_index:03d}.json"
    (dest_dir / filename).write_text(result.model_dump_json(indent=2))

    return result


def _shuffle_context(scenario: Scenario, seed: int) -> Scenario:
    """Return a shallow copy of *scenario* with list-of-dicts context entries shuffled.

    Only the list ordering is changed; dict contents and all other scenario fields
    are shared with the original (no deep copy needed since nothing is mutated).
    """
    rng = random.Random(seed)
    shuffled: dict = {}
    for key, value in scenario.context.items():
        if isinstance(value, list) and value and isinstance(value[0], dict):
            lst = list(value)  # copy the list; dict items are read-only in the prompt
            rng.shuffle(lst)
            shuffled[key] = lst
        else:
            shuffled[key] = value
    return scenario.model_copy(update={"context": shuffled})
