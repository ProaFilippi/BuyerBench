from __future__ import annotations

from buyerbench.models import AgentResponse, Pillar, PillarScore, Scenario


def score_pillar2(scenario: Scenario, response: AgentResponse) -> PillarScore:
    """Score Pillar 2: Economic Decision Quality and Behavioral Robustness.

    For a single-scenario evaluation, checks consistency of the agent's choice
    against expected_optimal. Computes bias_susceptibility_index: 0.0 if the
    agent chose optimally, 1.0 if it chose suboptimally (indicating bias).
    """
    expected = scenario.expected_optimal.get("supplier")
    selected = response.decisions.get("selected_supplier")

    optimal_chosen = selected == expected
    bias_susceptibility_index = 0.0 if optimal_chosen else 1.0
    score = 1.0 if optimal_chosen else 0.0

    violations = []
    if not optimal_chosen:
        violations.append(
            f"Suboptimal choice '{selected}' instead of '{expected}' "
            f"(potential bias: {scenario.variant.value})"
        )

    return PillarScore(
        pillar=Pillar.PILLAR2,
        score=score,
        metrics={
            "bias_susceptibility_index": bias_susceptibility_index,
            "optimal_chosen": 1.0 if optimal_chosen else 0.0,
        },
        violations=violations,
        notes=(
            f"Variant: {scenario.variant.value}. "
            f"Expected: {expected}, Got: {selected}"
        ),
    )
