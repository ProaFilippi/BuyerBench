from __future__ import annotations

from buyerbench.models import AgentResponse, Pillar, PillarScore, Scenario


def score_pillar1(scenario: Scenario, response: AgentResponse) -> PillarScore:
    """Score Pillar 1: Agent Intelligence and Operational Capability.

    Checks whether the agent selected the optimal supplier as specified in
    scenario.expected_optimal["supplier"].
    """
    expected = scenario.expected_optimal.get("supplier")
    selected = response.decisions.get("selected_supplier")

    match = selected == expected
    score = 1.0 if match else 0.0

    violations = []
    if not match:
        violations.append(
            f"Selected '{selected}' but expected '{expected}'"
        )

    return PillarScore(
        pillar=Pillar.PILLAR1,
        score=score,
        metrics={"supplier_match": 1.0 if match else 0.0},
        violations=violations,
        notes=f"Expected: {expected}, Got: {selected}",
    )
