"""Rich table renderers styled after academic paper result tables."""
from __future__ import annotations

import math
from collections import defaultdict
from typing import TYPE_CHECKING

import rich.box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

if TYPE_CHECKING:
    from buyerbench.models import EvaluationResult
    from results.session_export import SessionMetadata


def _pillar_name(ps) -> str:
    return ps.pillar.value if hasattr(ps.pillar, "value") else str(ps.pillar)


def _score_cell(score: float | None, *, bold: bool = False) -> str:
    """Return a Rich markup string coloured by score threshold."""
    if score is None:
        return "[dim]—[/dim]"
    formatted = f"{score:.2f}"
    if bold:
        formatted = f"[bold]{formatted}[/bold]"
    if score >= 0.8:
        return f"[bold green]{formatted}[/bold green]"
    if score >= 0.5:
        return f"[yellow]{formatted}[/yellow]"
    return f"[bold red]{formatted}[/bold red]"


def _mean_std(scores: list[float]) -> tuple[float, float]:
    if not scores:
        return 0.0, 0.0
    mean = sum(scores) / len(scores)
    variance = sum((s - mean) ** 2 for s in scores) / len(scores) if len(scores) > 1 else 0.0
    return mean, math.sqrt(variance)


def render_model_comparison_table(
    results: list[EvaluationResult],
    console: Console,
) -> None:
    """Print academic-style model comparison table.

    Rows = agents, Columns = P1 Score, P2 Score, P3 Score, Overall, Δ vs. Baseline, N.
    - Top performer per numeric column marked with ★
    - Scores >0.05 above baseline marked with †
    """
    # Build: agent_id → pillar → list[float]
    agent_pillar: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))
    for r in results:
        for ps in r.pillar_scores:
            agent_pillar[r.agent_id][_pillar_name(ps)].append(ps.score)

    if not agent_pillar:
        console.print("[dim]No results to display.[/dim]")
        return

    # Compute per-agent means per pillar + overall
    PILLARS = ["PILLAR1", "PILLAR2", "PILLAR3"]
    agent_means: dict[str, dict[str, float | None]] = {}
    agent_stds: dict[str, dict[str, float]] = {}
    agent_n: dict[str, int] = {}

    for agent_id in sorted(agent_pillar):
        means: dict[str, float | None] = {}
        stds: dict[str, float] = {}
        all_scores: list[float] = []
        for p in PILLARS:
            scores = agent_pillar[agent_id].get(p, [])
            if scores:
                m, s = _mean_std(scores)
                means[p] = m
                stds[p] = s
                all_scores.extend(scores)
            else:
                means[p] = None
                stds[p] = 0.0
        overall_scores = all_scores
        means["OVERALL"] = sum(overall_scores) / len(overall_scores) if overall_scores else None
        agent_means[agent_id] = means
        agent_stds[agent_id] = stds
        agent_n[agent_id] = len(overall_scores)

    # Find top performer per column
    def _top(col: str) -> str | None:
        best_agent, best_val = None, -1.0
        for agent_id, means in agent_means.items():
            v = means.get(col)
            if v is not None and v > best_val:
                best_val = v
                best_agent = agent_id
        return best_agent

    top_by_col = {col: _top(col) for col in PILLARS + ["OVERALL"]}

    # Find baseline agent for Δ column
    baseline_agent = next(
        (a for a in sorted(agent_means) if "baseline" in a.lower()), None
    )
    baseline_overall = (
        agent_means[baseline_agent]["OVERALL"] if baseline_agent else None
    )

    t = Table(
        title="[bold]Model Comparison (Academic Format)[/bold]",
        box=rich.box.HEAVY_HEAD,
        show_lines=True,
        caption="★ = top performer in column   † = >0.05 above baseline",
    )
    t.add_column("Agent", style="bold cyan", no_wrap=True)
    t.add_column("P1 Score", justify="right")
    t.add_column("P2 Score", justify="right")
    t.add_column("P3 Score", justify="right")
    t.add_column("Overall", justify="right")
    t.add_column("Δ Baseline", justify="right")
    t.add_column("N", justify="right", style="dim")

    for agent_id in sorted(agent_means):
        means = agent_means[agent_id]
        cells: list[str] = []
        for col in PILLARS + ["OVERALL"]:
            v = means.get(col)
            is_top = top_by_col.get(col) == agent_id
            cell = _score_cell(v)
            if v is not None:
                std = agent_stds[agent_id].get(col, 0.0)
                cell = _score_cell(v)
                if std > 0:
                    cell = cell.rstrip() + f" [dim]± {std:.2f}[/dim]"
            if is_top and v is not None:
                cell = "★ " + cell
            cells.append(cell)

        # Δ vs. baseline
        overall_val = means.get("OVERALL")
        if baseline_overall is not None and overall_val is not None and baseline_agent != agent_id:
            delta = overall_val - baseline_overall
            sig_marker = "†" if delta > 0.05 else ""
            if delta > 0:
                delta_cell = f"[bold green]+{delta:.2f}[/bold green]{sig_marker}"
            elif delta < 0:
                delta_cell = f"[bold red]{delta:.2f}[/bold red]"
            else:
                delta_cell = f"[dim]{delta:.2f}[/dim]"
        elif agent_id == baseline_agent:
            delta_cell = "[dim]baseline[/dim]"
        else:
            delta_cell = "[dim]—[/dim]"

        t.add_row(agent_id, *cells, delta_cell, str(agent_n[agent_id]))

    console.print()
    console.print(t)
    console.print()


def render_pillar_breakdown_table(
    results: list[EvaluationResult],
    pillar: int,
    console: Console,
) -> None:
    """Print per-scenario breakdown for one pillar.

    Rows = scenarios (sorted by id), Columns = one per agent.
    Green ≥0.8, Yellow 0.5–0.8, Red <0.5.
    Includes a "Best" row at the bottom.
    """
    pillar_name = f"PILLAR{pillar}"

    # scenario_id → agent_id → score
    scenario_agent: dict[str, dict[str, float]] = defaultdict(dict)
    for r in results:
        for ps in r.pillar_scores:
            if _pillar_name(ps) == pillar_name:
                scenario_agent[r.scenario_id][r.agent_id] = ps.score

    if not scenario_agent:
        console.print(f"[dim]No {pillar_name} results to display.[/dim]")
        return

    agents = sorted({a for scores in scenario_agent.values() for a in scores})
    scenarios = sorted(scenario_agent)

    t = Table(
        title=f"[bold]{pillar_name} — Per-Scenario Breakdown[/bold]",
        box=rich.box.HEAVY_HEAD,
        show_lines=True,
    )
    t.add_column("Scenario", style="bold cyan", no_wrap=True)
    for a in agents:
        t.add_column(a[:20], justify="right")

    for scenario_id in scenarios:
        row_cells = [scenario_id[:40]]
        for agent_id in agents:
            score = scenario_agent[scenario_id].get(agent_id)
            row_cells.append(_score_cell(score))
        t.add_row(*row_cells)

    # "Best" row
    best_cells = ["[bold]Best[/bold]"]
    for agent_id in agents:
        agent_scores = [
            scenario_agent[sid][agent_id]
            for sid in scenarios
            if agent_id in scenario_agent[sid]
        ]
        if agent_scores:
            best_cells.append(_score_cell(max(agent_scores), bold=True))
        else:
            best_cells.append("[dim]—[/dim]")
    t.add_row(*best_cells)

    console.print()
    console.print(t)
    console.print()


def render_bias_table(
    results: list[EvaluationResult],
    console: Console,
) -> None:
    """Print Pillar 2 bias consistency table.

    For each variant pair, shows BASELINE vs. FRAMING/ANCHOR/DECOY/etc.
    Highlights inconsistencies (decision changed) in red.
    """
    # Group by variant_pair_id → list[EvaluationResult]
    pairs: dict[str, list[EvaluationResult]] = defaultdict(list)
    baseline_results: list[EvaluationResult] = []

    for r in results:
        has_p2 = any(
            _pillar_name(ps) == "PILLAR2" for ps in r.pillar_scores
        )
        if not has_p2:
            continue
        if r.variant_pair_id:
            pairs[r.variant_pair_id].append(r)
        else:
            baseline_results.append(r)

    t = Table(
        title="[bold]Pillar 2 — Bias Consistency[/bold]",
        box=rich.box.HEAVY_HEAD,
        show_lines=True,
        caption="[bold red]RED[/bold red] = decision changed vs. baseline",
    )
    t.add_column("Pair ID / Variant", style="bold cyan", no_wrap=True)
    t.add_column("Agent", style="cyan")
    t.add_column("Baseline Score", justify="right")
    t.add_column("Variant Score", justify="right")
    t.add_column("Consistent?", justify="center")

    # Baseline score lookup: scenario_id → agent_id → score
    baseline_lookup: dict[str, dict[str, float]] = defaultdict(dict)
    for r in baseline_results:
        for ps in r.pillar_scores:
            if _pillar_name(ps) == "PILLAR2":
                baseline_lookup[r.scenario_id][r.agent_id] = ps.score

    added_any = False
    for pair_id in sorted(pairs):
        for r in pairs[pair_id]:
            for ps in r.pillar_scores:
                if _pillar_name(ps) != "PILLAR2":
                    continue
                variant_score = ps.score
                baseline_score = baseline_lookup.get(r.scenario_id, {}).get(r.agent_id)
                if baseline_score is None:
                    consistent = "[dim]unknown[/dim]"
                elif abs(variant_score - baseline_score) < 0.05:
                    consistent = "[green]YES[/green]"
                else:
                    consistent = "[bold red]NO[/bold red]"
                t.add_row(
                    pair_id[:35],
                    r.agent_id[:20],
                    _score_cell(baseline_score),
                    _score_cell(variant_score),
                    consistent,
                )
                added_any = True

    if not added_any:
        t.add_row("[dim]—[/dim]", "[dim]—[/dim]", "[dim]—[/dim]", "[dim]—[/dim]", "[dim]—[/dim]")

    console.print()
    console.print(t)
    console.print()


def render_session_summary_panel(
    meta: SessionMetadata,
    results: list[EvaluationResult],
    console: Console,
) -> None:
    """Print a Rich Panel summarising the session at a glance."""
    total = len(results)
    passes = sum(1 for r in results if r.overall_pass)
    pass_rate = passes / total if total else 0.0

    # Best performer by mean overall score
    agent_scores: dict[str, list[float]] = defaultdict(list)
    for r in results:
        for ps in r.pillar_scores:
            agent_scores[r.agent_id].append(ps.score)

    best_agent = "—"
    best_score = -1.0
    for agent_id, scores in agent_scores.items():
        mean = sum(scores) / len(scores)
        if mean > best_score:
            best_score = mean
            best_agent = agent_id

    lines = [
        f"[bold]Session:[/bold]  {meta.session_id}",
        f"[bold]Agents:[/bold]   {', '.join(meta.agents)}",
        f"[bold]Scenarios:[/bold] {meta.scenarios_run}",
        f"[bold]Pillars:[/bold]  {', '.join(str(p) for p in meta.pillars)}",
        f"[bold]Pass rate:[/bold] {pass_rate:.1%}  ({passes}/{total})",
        f"[bold]Best:[/bold]     {best_agent} ({best_score:.2f})",
        f"[bold]Duration:[/bold] {meta.duration_seconds:.1f}s",
        "",
    ]
    if meta.md_path:
        lines.append(f"[dim]Report → {meta.md_path}[/dim]")
    if meta.csv_path:
        lines.append(f"[dim]CSV    → {meta.csv_path}[/dim]")

    console.print()
    console.print(
        Panel(
            "\n".join(lines),
            title="[bold green]BuyerBench Session Complete[/bold green]",
            border_style="green",
        )
    )
    console.print()
