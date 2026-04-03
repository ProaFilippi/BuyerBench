from __future__ import annotations

import time

from agents import BaseAgent
from buyerbench.models import AgentResponse, Scenario


class MockAgent(BaseAgent):
    """A perfect mock agent that always returns the expected optimal decisions.

    Used to verify the full evaluation pipeline end-to-end. A MockAgent should
    score 1.0 on every scenario since it always selects the known optimal answer.
    """

    agent_id = "mock-agent-v1"

    def respond(self, scenario: Scenario) -> AgentResponse:
        start = time.monotonic()

        # The mock agent "cheats" by reading expected_optimal directly.
        # Real agents must infer decisions from scenario context alone.
        decisions = dict(scenario.expected_optimal)

        # Normalize decisions to the keys each evaluator expects.
        # Pillar 1 & 2: selected_supplier
        if "supplier" in decisions and "selected_supplier" not in decisions:
            decisions["selected_supplier"] = decisions["supplier"]

        # Pillar 3: flagged_transactions
        if "fraudulent_ids" in decisions and "flagged_transactions" not in decisions:
            decisions["flagged_transactions"] = decisions["fraudulent_ids"]

        latency_ms = (time.monotonic() - start) * 1000

        return AgentResponse(
            scenario_id=scenario.id,
            agent_id=self.agent_id,
            decisions=decisions,
            reasoning_trace=(
                f"[MockAgent] Returning expected_optimal for scenario "
                f"'{scenario.id}' (pillar: {scenario.pillar.value})."
            ),
            tool_calls=[],
            raw_output=str(decisions),
            latency_ms=latency_ms,
        )
