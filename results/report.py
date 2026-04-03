"""Summary report generation for BuyerBench evaluation results."""
from __future__ import annotations

import math
from collections import defaultdict
from datetime import datetime

from buyerbench.models import EvaluationResult, Pillar
from results.schemas import BiasReport, PillarStats, SummaryReport


def generate_summary_report(results: list[EvaluationResult]) -> dict:
    """Produce per-pillar aggregate statistics and overall summary.

    Returns a dict (JSON-serializable) with:
        - agent_id, total_scenarios, overall_pass_rate
        - per_pillar: {pillar_name: PillarStats}
        - bias_report: BiasReport (populated if bias_susceptibility_pairs provided separately)
        - generated_at
    """
    if not results:
        return SummaryReport(
            agent_id="unknown",
            total_scenarios=0,
            overall_pass_rate=0.0,
            generated_at=datetime.utcnow(),
        ).model_dump()

    agent_id = results[0].agent_id
    total = len(results)
    overall_passes = sum(1 for r in results if r.overall_pass)

    # Group scores by pillar
    pillar_scores: dict[str, list[float]] = defaultdict(list)
    pillar_metrics: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))

    for result in results:
        for ps in result.pillar_scores:
            pname = ps.pillar.value if isinstance(ps.pillar, Pillar) else str(ps.pillar)
            pillar_scores[pname].append(ps.score)
            for metric_name, metric_val in ps.metrics.items():
                pillar_metrics[pname][metric_name].append(metric_val)

    # Build per-pillar stats
    per_pillar: dict[str, PillarStats] = {}
    for pname, scores in pillar_scores.items():
        n = len(scores)
        mean = sum(scores) / n
        variance = sum((s - mean) ** 2 for s in scores) / n if n > 1 else 0.0
        std = math.sqrt(variance)

        per_metric_stats: dict[str, dict[str, float]] = {}
        for metric_name, vals in pillar_metrics[pname].items():
            mv = sum(vals) / len(vals)
            per_metric_stats[metric_name] = {
                "mean": mv,
                "min": min(vals),
                "max": max(vals),
            }

        per_pillar[pname] = PillarStats(
            mean_score=mean,
            std_score=std,
            min_score=min(scores),
            max_score=max(scores),
            pass_rate=sum(1 for r in results if any(
                ps.pillar.value == pname and ps.score >= 0.95
                for ps in r.pillar_scores
            )) / n,
            per_metric=per_metric_stats,
        )

    report = SummaryReport(
        agent_id=agent_id,
        total_scenarios=total,
        overall_pass_rate=overall_passes / total,
        per_pillar={k: v for k, v in per_pillar.items()},
        generated_at=datetime.utcnow(),
    )

    return report.model_dump()
