from __future__ import annotations

from buyerbench.models import AgentResponse, EvaluationResult, Pillar, Scenario
from evaluators.pillar1 import score_pillar1
from evaluators.pillar2 import score_pillar2
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

    overall_pass = pillar_score.score >= 1.0 and not pillar_score.violations

    return EvaluationResult(
        scenario_id=scenario.id,
        agent_id=response.agent_id,
        pillar_scores=[pillar_score],
        overall_pass=overall_pass,
    )
