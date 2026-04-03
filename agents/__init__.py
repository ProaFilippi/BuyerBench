from __future__ import annotations

from abc import ABC, abstractmethod

from buyerbench.models import AgentResponse, Scenario


class BaseAgent(ABC):
    """Abstract base class for all BuyerBench agents."""

    @abstractmethod
    def respond(self, scenario: Scenario) -> AgentResponse:
        """Process a scenario and return the agent's response."""
        ...
