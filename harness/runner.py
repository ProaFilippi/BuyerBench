from __future__ import annotations

import hashlib
import hmac
import json
import random
from pathlib import Path

from buyerbench.models import AgentResponse, EvaluationResult, Scenario
from evaluators.aggregate import run_evaluation


def derive_seed(base_seed: int, scenario_id: str, variant: str | None, run_index: int) -> int:
    """Derive a deterministic per-run seed from a base seed + cell identifier.

    Uses HMAC-SHA256 so every (base_seed, scenario_id, variant, run_index)
    combination maps to a unique seed, while the entire experiment remains
    reproducible from *base_seed* alone.  The digest is folded into [0, 2**31)
    to stay compatible with Python's ``random.Random`` seed range.

    Args:
        base_seed:   Experiment-level seed provided by the caller.
        scenario_id: Scenario identifier (e.g. ``"p2-01-anchoring"``).
        variant:     Scenario variant string, or ``None`` for the baseline.
        run_index:   0-based run index within the cell.

    Returns:
        An integer in [0, 2**31).
    """
    key = str(base_seed).encode()
    msg = f"{scenario_id}|{variant or ''}|{run_index}".encode()
    digest = hmac.new(key, msg, hashlib.sha256).digest()
    return int.from_bytes(digest[:4], "big") % (2**31)


def run_scenario(
    scenario: Scenario,
    agent,
    output_dir: str | Path | None = None,
    run_index: int = 0,
    supplier_order_seed: int | None = None,
    supplier_order_static: bool = False,
) -> EvaluationResult:
    """Run a single scenario through an agent and evaluate the result.

    Saves the JSON result to ``<output_dir>/<agent_id>/<scenario_id>-run<NNN>.json``.
    When *output_dir* is ``None`` the legacy path ``results/<agent_id>/`` is used.

    Args:
        scenario:               The scenario to evaluate.
        agent:                  The agent under evaluation.
        output_dir:             Directory to write result JSON files.
        run_index:              0-based index of this run within the cell (used in
                                file naming and stored on the result for downstream
                                aggregation).
        supplier_order_seed:    Seed controlling supplier list ordering in the
                                rendered prompt.  When ``None`` (default) a fresh
                                random seed is generated per run, ensuring each
                                independent repeat sees a different supplier order.
                                Pass an explicit integer to reproduce a specific run.
                                Ignored when *supplier_order_static* is ``True``.
        supplier_order_static:  When ``True``, suppliers are presented in their
                                original YAML order — no shuffling is performed.
                                ``supplier_order_seed`` is stored as ``None`` on
                                the result to signal the static mode.
    """
    if supplier_order_static:
        # No shuffling: present suppliers in original YAML order.
        seed_value: int | None = None
        scenario_for_agent = scenario
        run_id_seed_component = "static"
    else:
        # Always generate a concrete seed so every run is independently replayable.
        seed_value = supplier_order_seed if supplier_order_seed is not None else random.randrange(2**31)
        # Pass a scenario copy with shuffled context to the agent; the original is
        # kept intact so run_evaluation() compares against the unmodified ground truth.
        scenario_for_agent = _shuffle_context(scenario, seed_value)
        run_id_seed_component = str(seed_value)

    if scenario_for_agent.workflow:
        response = run_multi_step_scenario(scenario_for_agent, agent)
    else:
        response = agent.respond(scenario_for_agent)
    result = run_evaluation(scenario, response)
    result.run_index = run_index
    result.supplier_order_seed = seed_value

    # Compute content-addressable run_id once all key dimensions are known.
    result.run_id = hashlib.sha256(
        f"{result.agent_id}|{result.scenario_id}|{result.variant or ''}|{run_index}|{run_id_seed_component}".encode()
    ).hexdigest()[:16]

    base = Path(output_dir) if output_dir else Path("results")
    dest_dir = base / response.agent_id
    dest_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{scenario.id}-run{run_index:03d}.json"
    (dest_dir / filename).write_text(result.model_dump_json(indent=2))

    return result


def run_multi_step_scenario(scenario: Scenario, agent) -> AgentResponse:
    """Execute a multi-step workflow scenario, collecting per-step agent outputs.

    Iterates through ``scenario.workflow`` in order.  Each step receives the
    main scenario context merged with its own step context.  The prior step's
    decisions are injected as ``previous_step_output`` so later steps can
    condition on earlier results.

    The returned ``AgentResponse`` carries the final step's decisions merged
    with a ``steps_output`` list (one dict per step) to support cross-step
    analysis such as ``compute_anchor_propagation_index``.
    """
    steps_output: list[dict] = []
    prior_output: dict = {}
    last_response: AgentResponse | None = None

    for step in scenario.workflow:
        step_context = {**scenario.context, **step.context}
        if prior_output:
            step_context["previous_step_output"] = prior_output

        step_scenario = scenario.model_copy(update={
            "task_objective": step.task_objective,
            "context": step_context,
            "expected_optimal": step.expected_output,
        })

        last_response = agent.respond(step_scenario)
        prior_output = dict(last_response.decisions)
        steps_output.append(prior_output)

    if last_response is None:
        raise ValueError(f"Scenario {scenario.id!r} has an empty workflow.")

    final_decisions = {**steps_output[-1], "steps_output": steps_output}

    return AgentResponse(
        scenario_id=scenario.id,
        agent_id=last_response.agent_id,
        decisions=final_decisions,
        reasoning_trace=last_response.reasoning_trace,
        tool_calls=last_response.tool_calls,
        raw_output=last_response.raw_output,
        latency_ms=last_response.latency_ms,
        prompt_version=last_response.prompt_version,
    )


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
