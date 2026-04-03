"""JSON output schemas for BuyerBench evaluation results."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field


class PillarScoreJSON(BaseModel):
    pillar: str
    score: float
    metrics: dict[str, float] = Field(default_factory=dict)
    violations: list[str] = Field(default_factory=list)
    notes: str = ""


class EvaluationResultJSON(BaseModel):
    """JSON-serializable evaluation result for a single scenario."""
    scenario_id: str
    agent_id: str
    pillar_scores: list[PillarScoreJSON] = Field(default_factory=list)
    overall_pass: bool = False
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    variant_pair_id: str | None = None


class PillarStats(BaseModel):
    """Aggregate statistics for one pillar across all scenarios in a suite run."""
    mean_score: float
    std_score: float
    min_score: float
    max_score: float
    pass_rate: float
    per_metric: dict[str, dict[str, float]] = Field(default_factory=dict)


class BiasReport(BaseModel):
    """Aggregated bias susceptibility report across all variant pairs."""
    total_pairs: int
    pairs_with_decision_change: int
    mean_bsi: float
    per_variant_type: dict[str, Any] = Field(default_factory=dict)


class SummaryReport(BaseModel):
    """Top-level summary report for a full benchmark suite run."""
    agent_id: str
    total_scenarios: int
    overall_pass_rate: float
    per_pillar: dict[str, PillarStats] = Field(default_factory=dict)
    bias_report: BiasReport = Field(
        default_factory=lambda: BiasReport(
            total_pairs=0, pairs_with_decision_change=0, mean_bsi=0.0
        )
    )
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
