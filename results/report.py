"""Summary report generation for BuyerBench evaluation results."""
from __future__ import annotations

import json
import math
from collections import defaultdict
from datetime import datetime, timezone
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
            generated_at=datetime.now(timezone.utc),
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
        generated_at=datetime.now(timezone.utc),
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

    # ── collect all result JSONs ─────────────────────────────────────────────
    # Supports two directory layouts:
    #   Structured: <exp_dir>/pillar1/<agent_id>/<scenario>.json
    #   Flat:       <exp_dir>/<agent_id>/<scenario>.json
    all_results: list[EvaluationResult] = []
    error_result_keys: set[tuple[str, str]] = set()  # (agent_id, scenario_id) pairs with API errors
    agent_pillar_scores: dict[str, dict[str, list]] = defaultdict(lambda: defaultdict(list))

    # Error patterns that indicate a failed API call rather than a real eval
    _ERROR_PATTERNS = (
        "Client Error:",
        "Server Error:",
        "Connection Error:",
        "Timeout Error:",
        "Rate limit",
        "ECONNREFUSED",
        "getaddrinfo",
    )

    def _is_error_result(result: EvaluationResult) -> bool:
        raw = (result.raw_output or "").lower()
        return any(pat.lower() in raw for pat in _ERROR_PATTERNS)

    def _ingest_agent_dir(agent_dir: Path, agent_id: str) -> None:
        for json_file in sorted(agent_dir.glob("*.json")):
            if json_file.name in ("summary.json", "FULL-REPORT.json"):
                continue
            try:
                raw = json.loads(json_file.read_text())
            except Exception:
                continue
            if raw.get("status") == "skipped":
                continue
            try:
                result = EvaluationResult.model_validate(raw)
            except Exception:
                continue
            all_results.append(result)
            if _is_error_result(result):
                error_result_keys.add((result.agent_id, result.scenario_id))
                continue  # exclude from aggregate scoring
            for ps in result.pillar_scores:
                pname = ps.pillar.value if isinstance(ps.pillar, Pillar) else str(ps.pillar)
                agent_pillar_scores[agent_id][pname].append(ps)

    # Try structured layout first (pillar1/, pillar2/, pillar3/)
    pillar_dirs = sorted(d for d in exp_dir.iterdir() if d.is_dir() and d.name.startswith("pillar"))
    if pillar_dirs:
        for pillar_dir in pillar_dirs:
            for agent_dir in sorted(d for d in pillar_dir.iterdir() if d.is_dir()):
                _ingest_agent_dir(agent_dir, agent_dir.name)
    else:
        # Flat layout: <exp_dir>/<agent_id>/<scenario>.json
        for agent_dir in sorted(d for d in exp_dir.iterdir() if d.is_dir()):
            # Skip non-agent directories (experiments, __pycache__, etc.)
            if agent_dir.name.startswith(("__", ".")) or agent_dir.name == "experiments":
                continue
            if any(agent_dir.glob("*.json")):
                _ingest_agent_dir(agent_dir, agent_dir.name)

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

    # ── 6. Per-scenario results (with raw_output and decisions) ────────────────
    scenario_results: list[dict] = []
    for result in all_results:
        raw = result.raw_output[:5000] if result.raw_output else ""
        is_error = (result.agent_id, result.scenario_id) in error_result_keys
        ts = result.timestamp.isoformat() if result.timestamp else None
        for ps in result.pillar_scores:
            pname = ps.pillar.value if isinstance(ps.pillar, Pillar) else str(ps.pillar)
            scenario_results.append({
                "agent_id": result.agent_id,
                "scenario_id": result.scenario_id,
                "pillar": pname,
                "score": round(ps.score, 4),
                "overall_pass": result.overall_pass,
                "violations": ps.violations,
                "notes": ps.notes,
                "metrics": {k: round(v, 4) for k, v in ps.metrics.items()},
                "raw_output": raw,
                "decisions": result.decisions,
                "timestamp": ts,
                "is_error": is_error,
            })

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "experiment_dir": str(exp_dir),
        # REV-1: explicit rationality-scope statement in every results section.
        # REV-3: single-run data must be labeled EXPLORATORY ONLY.
        "methodology_notes": {
            "pillar2_rationality_scope": (
                "Optimality is defined relative to the scenario's stated evaluation weights. "
                "We test internal rationality, not external optimality."
            ),
            "exploratory_only_label": (
                "Current data is based on single-run sessions (N=1 per cell). "
                "This data is EXPLORATORY ONLY and must not be used as evidence in published work. "
                "N\u226550 runs per cell are required before any statistical claims can be made."
            ),
            # REV-6: cross-model regression must never be used for inference.
            "cross_model_regression_scope": (
                "Cross-model comparisons (H2 capability scatter, inter-model BSI) are "
                "DESCRIPTIVE ONLY (N=10 models). "
                "No p-values, regression coefficients, or inferential claims are valid "
                "for cross-model analyses at N=10. "
                "Present capability scatter as a descriptive figure only; "
                "all within-model analyses (H1, H3, H5, H7) remain inferential at N\u226550 runs per cell."
            ),
            # REV-7: abstract/introduction pipeline scope statement.
            "pipeline_scope": (
                "We evaluate the final selection stage of AI buyer agents \u2014 specifically, "
                "the economic judgment call when structured options are presented \u2014 "
                "not the full agent pipeline."
            ),
        },
        "per_pillar_aggregate": per_pillar_aggregate,
        "per_metric_breakdown": dict(per_metric_breakdown),
        "bias_susceptibility_table": bsi_table,
        "security_violation_table": security_table,
        "skills_mcp_delta_table": delta_table,
        "scenario_results": scenario_results,
    }


def render_full_report_markdown(report: dict) -> str:
    """Render a full report dict as human-readable GitHub-flavoured Markdown.

    Args:
        report: Dict produced by :func:`generate_full_report`.

    Returns:
        A Markdown string with five labelled sections, each containing a table.
    """
    _P2_SCOPE = (
        "> **Pillar 2 scope note (REV-1):** "
        "Optimality is defined relative to the scenario's stated evaluation weights. "
        "We test *internal* rationality, not external optimality."
    )

    _EXPLORATORY_WARN = (
        "> **⚠ REV-3 — EXPLORATORY DATA WARNING:** "
        "Current data is based on single-run sessions (N=1 per cell). "
        "This data is **EXPLORATORY ONLY** and must not be used as evidence in published work. "
        "N≥50 runs per cell are required before any statistical claims can be made."
    )

    _REV6_CROSS_MODEL_WARN = (
        "> **REV-6 — CROSS-MODEL ANALYSIS SCOPE:** "
        "All cross-model comparisons (capability scatter, inter-model BSI) are "
        "**descriptive only** (N=10 models). "
        "No p-values or inferential claims are valid for cross-model analyses. "
        "Within-model analyses (H1, H3, H5, H7) remain inferential at N≥50 runs per cell."
    )

    _REV7_PIPELINE_SCOPE = (
        "> **REV-7 — PIPELINE SCOPE (use verbatim in abstract/introduction):** "
        "We evaluate the **final selection stage** of AI buyer agents — specifically, "
        "the economic judgment call when structured options are presented — "
        "not the full agent pipeline."
    )

    lines = [
        "# BuyerBench Full Experiment Report",
        "",
        f"**Generated:** {report.get('generated_at', 'N/A')}  ",
        f"**Experiment dir:** `{report.get('experiment_dir', 'N/A')}`",
        "",
        _EXPLORATORY_WARN,
        "",
        _REV7_PIPELINE_SCOPE,
        "",
    ]

    # ── 1. Per-pillar aggregate ───────────────────────────────────────────────
    lines += [
        "## 1. Per-Pillar Aggregate Scores",
        "",
        _REV6_CROSS_MODEL_WARN,
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
        lines += [f"### {pillar_name}", ""]
        if pillar_name == "PILLAR2":
            lines += [_P2_SCOPE, ""]
        lines += [
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
        _P2_SCOPE,
        "",
        _EXPLORATORY_WARN,
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
