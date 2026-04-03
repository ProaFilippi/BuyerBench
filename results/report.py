"""Summary report generation for BuyerBench evaluation results."""
from __future__ import annotations

import json
import math
from collections import defaultdict
from datetime import datetime
from pathlib import Path

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


def generate_full_report(experiment_dir: str) -> dict:
    """Generate a comprehensive multi-table report from all experiment result JSONs.

    Reads all per-agent result JSONs from pillar subdirs (``pillar1/``, ``pillar2/``,
    ``pillar3/``) inside *experiment_dir*, then aggregates five analysis tables:

    - **per_pillar_aggregate**: mean/std/min/max score per agent × pillar
    - **per_metric_breakdown**: per-metric stats per agent grouped by pillar
    - **bias_susceptibility_table**: BSI per variant pair (from saved summary JSON)
    - **security_violation_table**: compliance & violation rates per scenario × agent
    - **skills_mcp_delta_table**: score delta when adding skills/MCP vs. baseline mode

    Args:
        experiment_dir: Root directory holding ``pillar1/``, ``pillar2/``,
            ``pillar3/`` subdirs produced by ``run --output-dir``.

    Returns:
        A JSON-serialisable dict with all five tables plus ``generated_at`` and
        ``experiment_dir`` metadata fields.
    """
    exp_dir = Path(experiment_dir)

    # ── collect pillar scores across all pillar subdirs ───────────────────────
    # agent_id → pillar_name → list[PillarScore]
    agent_pillar_scores: dict[str, dict[str, list]] = defaultdict(lambda: defaultdict(list))

    for pillar_dir in sorted(d for d in exp_dir.iterdir() if d.is_dir() and d.name.startswith("pillar")):
        for agent_dir in sorted(d for d in pillar_dir.iterdir() if d.is_dir()):
            agent_id = agent_dir.name
            for json_file in sorted(agent_dir.glob("*.json")):
                raw = json.loads(json_file.read_text())
                if raw.get("status") == "skipped":
                    continue
                try:
                    result = EvaluationResult.model_validate(raw)
                except Exception:
                    continue
                for ps in result.pillar_scores:
                    pname = ps.pillar.value if isinstance(ps.pillar, Pillar) else str(ps.pillar)
                    agent_pillar_scores[agent_id][pname].append(ps)

    # ── 1. Per-pillar aggregate table ─────────────────────────────────────────
    per_pillar_aggregate: list[dict] = []
    for agent_id in sorted(agent_pillar_scores):
        for pillar_name in sorted(agent_pillar_scores[agent_id]):
            scores = [ps.score for ps in agent_pillar_scores[agent_id][pillar_name]]
            n = len(scores)
            mean = sum(scores) / n
            variance = sum((s - mean) ** 2 for s in scores) / n if n > 1 else 0.0
            per_pillar_aggregate.append({
                "agent_id": agent_id,
                "pillar": pillar_name,
                "mean_score": round(mean, 4),
                "std": round(math.sqrt(variance), 4),
                "min": round(min(scores), 4),
                "max": round(max(scores), 4),
                "n_scenarios": n,
            })

    # ── 2. Per-metric breakdown ────────────────────────────────────────────────
    per_metric_breakdown: dict[str, list[dict]] = defaultdict(list)
    for agent_id in sorted(agent_pillar_scores):
        for pillar_name in sorted(agent_pillar_scores[agent_id]):
            metric_vals: dict[str, list[float]] = defaultdict(list)
            for ps in agent_pillar_scores[agent_id][pillar_name]:
                for m, v in ps.metrics.items():
                    metric_vals[m].append(float(v))
            for metric in sorted(metric_vals):
                vals = metric_vals[metric]
                per_metric_breakdown[pillar_name].append({
                    "agent_id": agent_id,
                    "metric": metric,
                    "mean": round(sum(vals) / len(vals), 4),
                    "min": round(min(vals), 4),
                    "max": round(max(vals), 4),
                })

    # ── 3. Bias susceptibility table (from saved summary JSON) ────────────────
    bsi_table: list[dict] = []
    bsi_summary_path = exp_dir / "pillar2" / "bias-susceptibility-summary.json"
    if bsi_summary_path.exists():
        bsi_summary = json.loads(bsi_summary_path.read_text())
        for agent_id, agent_data in bsi_summary.get("per_agent_bsi", {}).items():
            mode = agent_id.rsplit("-", 1)[-1] if "-" in agent_id else agent_id
            for pair in agent_data.get("pair_bsi_results", []):
                bsi_table.append({
                    "bias_type": pair.get("variant_type") or "UNKNOWN",
                    "agent_id": agent_id,
                    "mode": mode,
                    "bsi": round(pair.get("bias_susceptibility_index", 0.0), 4),
                    "decision_changed": bool(pair.get("decision_changed", False)),
                    "pair_id": pair.get("pair_id"),
                })

    # ── 4. Security violation frequency table ─────────────────────────────────
    security_table: list[dict] = []
    sec_summary_path = exp_dir / "pillar3" / "security-compliance-summary.json"
    if sec_summary_path.exists():
        sec_summary = json.loads(sec_summary_path.read_text())
        for agent_id, agent_sec in sec_summary.get("per_agent_security", {}).items():
            for scenario_id, metrics in agent_sec.get("results_by_scenario", {}).items():
                security_table.append({
                    "scenario_id": scenario_id,
                    "agent_id": agent_id,
                    "compliance_adherence_rate": metrics.get("compliance_adherence_rate", 0.0),
                    "security_violation_frequency": metrics.get("security_violation_frequency", 0.0),
                    "score": metrics.get("score", 0.0),
                })

    # ── 5. Skills vs MCP delta table ──────────────────────────────────────────
    # Per-agent mean score across all scenarios for each pillar
    agent_means: dict[str, dict[str, float]] = {
        agent_id: {
            pname: sum(ps.score for ps in plist) / len(plist)
            for pname, plist in pillar_map.items()
        }
        for agent_id, pillar_map in agent_pillar_scores.items()
    }

    # Group by agent family (everything before the last "-" segment)
    families: dict[str, dict[str, str]] = {}  # family → mode → agent_id
    for agent_id in agent_means:
        if "-" in agent_id:
            *family_parts, mode = agent_id.split("-")
            family = "-".join(family_parts)
            families.setdefault(family, {})[mode] = agent_id

    delta_table: list[dict] = []
    for family in sorted(families):
        mode_map = families[family]
        baseline_id = mode_map.get("baseline")
        if not baseline_id:
            continue
        baseline_means = agent_means.get(baseline_id, {})
        for mode in ("skills", "mcp"):
            variant_id = mode_map.get(mode)
            if not variant_id:
                continue
            variant_means = agent_means.get(variant_id, {})
            for pillar_name in sorted(set(baseline_means) | set(variant_means)):
                b = baseline_means.get(pillar_name)
                v = variant_means.get(pillar_name)
                delta_table.append({
                    "family": family,
                    "mode": mode,
                    "agent_id": variant_id,
                    "pillar": pillar_name,
                    "baseline_score": round(b, 4) if b is not None else None,
                    "variant_score": round(v, 4) if v is not None else None,
                    "delta": round(v - b, 4) if (b is not None and v is not None) else None,
                })

    return {
        "generated_at": datetime.utcnow().isoformat(),
        "experiment_dir": str(exp_dir),
        "per_pillar_aggregate": per_pillar_aggregate,
        "per_metric_breakdown": dict(per_metric_breakdown),
        "bias_susceptibility_table": bsi_table,
        "security_violation_table": security_table,
        "skills_mcp_delta_table": delta_table,
    }


def render_full_report_markdown(report: dict) -> str:
    """Render a full report dict as human-readable GitHub-flavoured Markdown.

    Args:
        report: Dict produced by :func:`generate_full_report`.

    Returns:
        A Markdown string with five labelled sections, each containing a table.
    """
    lines = [
        "# BuyerBench Full Experiment Report",
        "",
        f"**Generated:** {report.get('generated_at', 'N/A')}  ",
        f"**Experiment dir:** `{report.get('experiment_dir', 'N/A')}`",
        "",
    ]

    # ── 1. Per-pillar aggregate ───────────────────────────────────────────────
    lines += [
        "## 1. Per-Pillar Aggregate Scores",
        "",
        "| Agent | Pillar | Mean Score | Std | Min | Max | N Scenarios |",
        "|-------|--------|-----------|-----|-----|-----|-------------|",
    ]
    for row in report.get("per_pillar_aggregate", []):
        lines.append(
            f"| {row['agent_id']} | {row['pillar']} | {row['mean_score']:.4f} | "
            f"{row['std']:.4f} | {row['min']:.4f} | {row['max']:.4f} | {row['n_scenarios']} |"
        )
    lines.append("")

    # ── 2. Per-metric breakdown ───────────────────────────────────────────────
    lines.append("## 2. Per-Metric Breakdown")
    lines.append("")
    for pillar_name in sorted(report.get("per_metric_breakdown", {})):
        lines += [
            f"### {pillar_name}",
            "",
            "| Agent | Metric | Mean | Min | Max |",
            "|-------|--------|------|-----|-----|",
        ]
        for row in report["per_metric_breakdown"][pillar_name]:
            lines.append(
                f"| {row['agent_id']} | {row['metric']} | {row['mean']:.4f} | "
                f"{row['min']:.4f} | {row['max']:.4f} |"
            )
        lines.append("")

    # ── 3. Bias susceptibility ────────────────────────────────────────────────
    lines += [
        "## 3. Bias Susceptibility",
        "",
        "| Bias Type | Agent | Mode | BSI | Decision Changed |",
        "|-----------|-------|------|-----|-----------------|",
    ]
    bsi_rows = report.get("bias_susceptibility_table", [])
    if bsi_rows:
        for row in bsi_rows:
            changed = "Yes" if row.get("decision_changed") else "No"
            lines.append(
                f"| {row['bias_type']} | {row['agent_id']} | {row['mode']} | "
                f"{row['bsi']:.4f} | {changed} |"
            )
    else:
        lines.append("| — | — | — | — | — |")
    lines.append("")

    # ── 4. Security violation frequency ──────────────────────────────────────
    lines += [
        "## 4. Security Violation Frequency",
        "",
        "| Scenario | Agent | Compliance Rate | Violation Frequency | Score |",
        "|----------|-------|----------------|---------------------|-------|",
    ]
    sec_rows = report.get("security_violation_table", [])
    if sec_rows:
        for row in sec_rows:
            lines.append(
                f"| {row['scenario_id']} | {row['agent_id']} | "
                f"{row['compliance_adherence_rate']:.4f} | "
                f"{row['security_violation_frequency']:.4f} | "
                f"{row['score']:.4f} |"
            )
    else:
        lines.append("| — | — | — | — | — |")
    lines.append("")

    # ── 5. Skills vs MCP delta ────────────────────────────────────────────────
    lines += [
        "## 5. Skills vs. MCP Score Delta (vs. Baseline)",
        "",
        "| Family | Mode | Pillar | Baseline Score | Variant Score | Delta |",
        "|--------|------|--------|---------------|--------------|-------|",
    ]
    delta_rows = report.get("skills_mcp_delta_table", [])
    if delta_rows:
        for row in delta_rows:
            b = f"{row['baseline_score']:.4f}" if row["baseline_score"] is not None else "—"
            v = f"{row['variant_score']:.4f}" if row["variant_score"] is not None else "—"
            d = f"{row['delta']:+.4f}" if row["delta"] is not None else "—"
            lines.append(
                f"| {row['family']} | {row['mode']} | {row['pillar']} | {b} | {v} | {d} |"
            )
    else:
        lines.append("| — | — | — | — | — | — |")
    lines.append("")

    return "\n".join(lines)
