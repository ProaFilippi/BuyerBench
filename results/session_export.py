"""Session export engine for BuyerBench — generates .md and .csv artifacts per run."""
from __future__ import annotations

import csv
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from buyerbench.models import EvaluationResult


def generate_session_id() -> str:
    """Return a session ID of the form ``session-YYYYMMDD-HHMMSS``."""
    return f"session-{datetime.now().strftime('%Y%m%d-%H%M%S')}"


@dataclass
class SessionMetadata:
    session_id: str
    agents: list[str]
    scenarios_run: int
    pillars: list[int]
    started_at: datetime
    completed_at: datetime
    output_dir: str
    md_path: str = ""
    csv_path: str = ""

    @property
    def duration_seconds(self) -> float:
        return (self.completed_at - self.started_at).total_seconds()


def export_session_markdown(
    results: list[EvaluationResult],
    meta: SessionMetadata,
    output_path: str,
) -> None:
    """Write a structured Markdown session report with YAML front matter.

    Args:
        results: All EvaluationResult objects from the session.
        meta:    SessionMetadata describing the run.
        output_path: File path where the .md should be written.
    """
    iso_date = meta.started_at.strftime("%Y-%m-%d")
    lines: list[str] = [
        "---",
        "type: report",
        f"title: BuyerBench Session {meta.session_id}",
        f"created: {iso_date}",
        "tags:",
        "  - benchmark",
        "  - buyerbench",
        "  - openrouter",
        "related:",
        "  - '[[FULL-REPORT]]'",
        "---",
        "",
    ]

    # ── Summary ──────────────────────────────────────────────────────────────
    lines += [
        "## Summary",
        "",
        f"- **Session ID:** {meta.session_id}",
        f"- **Agents:** {', '.join(meta.agents)}",
        f"- **Scenarios run:** {meta.scenarios_run}",
        f"- **Pillars:** {', '.join(str(p) for p in meta.pillars)}",
        f"- **Started:** {meta.started_at.isoformat()}",
        f"- **Completed:** {meta.completed_at.isoformat()}",
        f"- **Duration:** {meta.duration_seconds:.1f}s",
        "",
    ]

    # ── Results by Pillar ─────────────────────────────────────────────────────
    lines += ["## Results by Pillar", ""]

    from collections import defaultdict
    pillar_agent_scores: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    for r in results:
        for ps in r.pillar_scores:
            pname = ps.pillar.value if hasattr(ps.pillar, "value") else str(ps.pillar)
            pillar_agent_scores[pname][r.agent_id].append(ps.score)

    for pname in sorted(pillar_agent_scores):
        lines += [f"### {pname}", "", "| Agent | Mean Score | N |", "|-------|-----------|---|"]
        for agent_id in sorted(pillar_agent_scores[pname]):
            scores = pillar_agent_scores[pname][agent_id]
            mean = sum(scores) / len(scores)
            lines.append(f"| {agent_id} | {mean:.4f} | {len(scores)} |")
        lines.append("")

    # ── Per-Scenario Breakdown ────────────────────────────────────────────────
    lines += [
        "## Per-Scenario Breakdown",
        "",
        "| Scenario | Pillar | Variant | Agent | Score | Pass |",
        "|----------|--------|---------|-------|-------|------|",
    ]
    for r in results:
        score = r.pillar_scores[0].score if r.pillar_scores else 0.0
        pillar = (
            r.pillar_scores[0].pillar.value
            if r.pillar_scores and hasattr(r.pillar_scores[0].pillar, "value")
            else (r.pillar_scores[0].pillar if r.pillar_scores else "—")
        )
        variant = r.variant_pair_id or "BASELINE"
        pass_str = "✓" if r.overall_pass else "✗"
        lines.append(
            f"| {r.scenario_id} | {pillar} | {variant} | {r.agent_id} | {score:.4f} | {pass_str} |"
        )
    lines.append("")

    # ── Notes ─────────────────────────────────────────────────────────────────
    lines += ["## Notes", ""]
    error_agents = [r.agent_id for r in results if not r.pillar_scores]
    if error_agents:
        unique_errors = sorted(set(error_agents))
        lines += [
            "The following agents returned no pillar scores (possible error or timeout):",
            "",
        ]
        for a in unique_errors:
            lines.append(f"- {a}")
    else:
        lines.append("No errors or timeouts detected.")
    lines.append("")

    with open(output_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))


def export_session_csv(
    results: list[EvaluationResult],
    meta: SessionMetadata,
    output_path: str,
) -> None:
    """Write a flat CSV with one row per (agent, scenario) pair.

    Columns: session_id, agent_id, scenario_id, pillar, variant, score,
             overall_pass, latency_ms, timestamp.
    """
    fieldnames = [
        "session_id",
        "agent_id",
        "scenario_id",
        "run_index",
        "run_id",
        "supplier_order_seed",
        "pillar",
        "variant",
        "variant_pair_id",
        "bias_category",
        "score",
        "overall_pass",
        "temperature",
        "prompt_version",
        "token_count_input",
        "token_count_output",
        "api_cost_usd",
        "error_flag",
        "model_version",
        "latency_ms",
        "timestamp",
    ]

    with open(output_path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for r in results:
            score = r.pillar_scores[0].score if r.pillar_scores else 0.0
            pillar = (
                r.pillar_scores[0].pillar.value
                if r.pillar_scores and hasattr(r.pillar_scores[0].pillar, "value")
                else (str(r.pillar_scores[0].pillar) if r.pillar_scores else "")
            )
            writer.writerow({
                "session_id": meta.session_id,
                "agent_id": r.agent_id,
                "scenario_id": r.scenario_id,
                "run_index": r.run_index,
                "run_id": r.run_id,
                "supplier_order_seed": r.supplier_order_seed,
                "pillar": pillar,
                "variant": r.variant or "",
                "variant_pair_id": r.variant_pair_id or "",
                "bias_category": r.bias_category or "",
                "score": round(score, 6),
                "overall_pass": r.overall_pass,
                "temperature": r.temperature if r.temperature is not None else "",
                "prompt_version": r.prompt_version,
                "token_count_input": r.token_count_input,
                "token_count_output": r.token_count_output,
                "api_cost_usd": r.api_cost_usd if r.api_cost_usd is not None else "",
                "error_flag": r.error_flag,
                "model_version": r.model_version or "",
                "latency_ms": r.latency_ms,
                "timestamp": r.timestamp.isoformat() if r.timestamp else "",
            })
