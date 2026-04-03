from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class ScenarioVariant(str, Enum):
    BASELINE = "BASELINE"
    FRAMING_GAIN = "FRAMING_GAIN"
    FRAMING_LOSS = "FRAMING_LOSS"
    DECOY = "DECOY"
    ANCHOR_HIGH = "ANCHOR_HIGH"
    ANCHOR_LOW = "ANCHOR_LOW"
    SCARCITY = "SCARCITY"
    DEFAULT = "DEFAULT"


class Pillar(str, Enum):
    PILLAR1 = "PILLAR1"
    PILLAR2 = "PILLAR2"
    PILLAR3 = "PILLAR3"


class Difficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class Scenario(BaseModel):
    id: str
    title: str
    pillar: Pillar
    variant: ScenarioVariant = ScenarioVariant.BASELINE
    description: str
    context: dict[str, Any] = Field(default_factory=dict)
    task_objective: str
    constraints: list[str] = Field(default_factory=list)
    expected_optimal: dict[str, Any] = Field(default_factory=dict)
    security_requirements: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    difficulty: Difficulty = Difficulty.EASY
    variant_pair_id: str | None = None
    evaluation_weights: dict[str, float] = Field(default_factory=dict)


class AgentResponse(BaseModel):
    scenario_id: str
    agent_id: str
    decisions: dict[str, Any] = Field(default_factory=dict)
    reasoning_trace: str = ""
    tool_calls: list[dict[str, Any]] = Field(default_factory=list)
    raw_output: str = ""
    latency_ms: float = 0.0


class PillarScore(BaseModel):
    pillar: Pillar
    score: float = Field(ge=0.0, le=1.0)
    metrics: dict[str, float] = Field(default_factory=dict)
    violations: list[str] = Field(default_factory=list)
    notes: str = ""


class EvaluationResult(BaseModel):
    scenario_id: str
    agent_id: str
    pillar_scores: list[PillarScore] = Field(default_factory=list)
    overall_pass: bool = False
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    variant_pair_id: str | None = None
