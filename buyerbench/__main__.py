from __future__ import annotations

import os
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table
from rich import box

console = Console(highlight=False)


@click.group()
def cli() -> None:
    """BuyerBench — benchmark framework for AI buyer agents."""


@cli.command()
def check() -> None:
    """Verify CLI tools, API keys, and mock MCP server are available."""
    from harness.preflight import check_environment

    env = check_environment(print_report=True)
    raise SystemExit(0 if env["overall"] else 1)


@cli.command()
def demo() -> None:
    """Load the 3 sample scenarios, run MockAgent, and print a rich report."""
    from agents.mock import MockAgent
    from harness.loader import load_all_scenarios
    from harness.runner import run_scenario

    scenarios_root = Path(__file__).parent.parent / "scenarios"
    scenarios = load_all_scenarios(str(scenarios_root))

    agent = MockAgent()

    table = Table(
        title="BuyerBench Evaluation Report",
        box=box.ROUNDED,
        show_lines=True,
    )
    table.add_column("Scenario", style="bold cyan", no_wrap=True)
    table.add_column("Pillar", style="magenta")
    table.add_column("Variant", style="dim")
    table.add_column("Agent Decision", style="yellow")
    table.add_column("Score", justify="right")
    table.add_column("Status", justify="center")

    for scenario in scenarios:
        result = run_scenario(scenario, agent)
        pillar_score = result.pillar_scores[0]

        # Build a compact decision summary
        decisions = result.pillar_scores[0].notes.split("Got: ")[-1] if result.pillar_scores else "—"

        # Re-run agent to get readable decisions (runner already evaluated)
        response = agent.respond(scenario)
        decision_summary = _format_decisions(response.decisions, scenario.pillar.value)

        score_str = f"{pillar_score.score:.2f}"
        status = "[green]PASS[/green]" if result.overall_pass else "[red]FAIL[/red]"

        table.add_row(
            scenario.title[:45],
            scenario.pillar.value,
            scenario.variant.value,
            decision_summary,
            score_str,
            status,
        )

    console.print()
    console.print(table)
    console.print()
    console.print(
        "[bold green]BuyerBench demo complete — 3 scenarios evaluated.[/bold green]"
    )
    console.print()


def _format_decisions(decisions: dict, pillar: str) -> str:
    if pillar == "PILLAR3":
        flagged = decisions.get("flagged_transactions", [])
        return f"Flagged: {', '.join(flagged)}" if flagged else "None flagged"
    supplier = decisions.get("selected_supplier") or decisions.get("supplier", "—")
    price = decisions.get("unit_price")
    if price is not None:
        return f"{supplier} (${price:.2f})"
    return str(supplier)


@cli.command()
@click.option(
    "--agent",
    required=True,
    help='Agent ID to evaluate (e.g. claude-code-baseline) or "all" for all real agents.',
)
@click.option("--scenario", default=None, help="Specific scenario ID to run")
@click.option(
    "--pillar",
    default=None,
    type=click.Choice(["1", "2", "3"]),
    help="Pillar filter (1/2/3)",
)
@click.option(
    "--dry-run",
    is_flag=True,
    default=False,
    help="Print prompts without invoking the CLI agent",
)
@click.option(
    "--output-dir",
    default="results",
    show_default=True,
    help="Directory to write evaluation results",
)
def run(
    agent: str,
    scenario: str | None,
    pillar: str | None,
    dry_run: bool,
    output_dir: str,
) -> None:
    """Run the benchmark suite against a named CLI agent (or all agents)."""
    import json
    from datetime import datetime
    from pathlib import Path

    from agents.registry import AGENT_REGISTRY, get_agent
    from harness.config import load_config
    from harness.loader import load_all_scenarios
    from harness.runner import run_scenario

    # ── Resolve agent list ────────────────────────────────────────────────────
    _REAL_AGENTS = [aid for aid in AGENT_REGISTRY if aid != "mock-agent-v1"]

    if agent == "all":
        from harness.preflight import check_environment

        env = check_environment(print_report=True)
        available_set = set(env["available_agents"])
        agents_to_run = [(aid, aid in available_set) for aid in _REAL_AGENTS]
    else:
        if agent not in AGENT_REGISTRY:
            available = sorted(AGENT_REGISTRY.keys())
            console.print(
                f"[red]Unknown agent {agent!r}.[/red]\n"
                f"Available agents: {', '.join(available)}"
            )
            raise SystemExit(1)
        agents_to_run = [(agent, True)]

    # ── Load and filter scenarios ─────────────────────────────────────────────
    scenarios_root = Path(__file__).parent.parent / "scenarios"
    all_scenarios = load_all_scenarios(str(scenarios_root))

    if pillar:
        pillar_enum = f"PILLAR{pillar}"
        all_scenarios = [s for s in all_scenarios if s.pillar.value == pillar_enum]
    if scenario:
        all_scenarios = [s for s in all_scenarios if s.id == scenario]

    if not all_scenarios:
        console.print("[yellow]No scenarios matched the given filters.[/yellow]")
        return

    config = load_config()
    config["dry_run"] = dry_run

    # ── Run each agent ────────────────────────────────────────────────────────
    for agent_id, is_available in agents_to_run:
        if not is_available:
            _write_skipped_results(agent_id, all_scenarios, output_dir)
            console.print(
                f"[yellow]SKIPPED[/yellow] {agent_id} — CLI or API key unavailable"
            )
            continue

        agent_instance = get_agent(agent_id, config)

        if dry_run:
            console.print(
                f"[bold cyan]DRY RUN[/bold cyan] — agent=[bold]{agent_id}[/bold]  "
                f"scenarios={len(all_scenarios)}"
            )
            for s in all_scenarios:
                agent_instance.respond(s)
            continue

        table = Table(
            title=f"BuyerBench Run — {agent_id}",
            box=box.ROUNDED,
            show_lines=True,
        )
        table.add_column("Scenario", style="bold cyan", no_wrap=True)
        table.add_column("Pillar", style="magenta")
        table.add_column("Score", justify="right")
        table.add_column("Status", justify="center")

        for s in all_scenarios:
            result = run_scenario(s, agent_instance, output_dir=output_dir)
            score = result.pillar_scores[0].score if result.pillar_scores else 0.0
            status = "[green]PASS[/green]" if result.overall_pass else "[red]FAIL[/red]"
            table.add_row(s.title[:50], s.pillar.value, f"{score:.2f}", status)

        console.print()
        console.print(table)

    # ── Post-run: Pillar 2 BSI computation ───────────────────────────────────
    if pillar == "2":
        import json as _json
        from evaluators.aggregate import compute_bsi_from_experiment_dir

        bsi_summary = compute_bsi_from_experiment_dir(output_dir)
        bsi_path = Path(output_dir) / "bias-susceptibility-summary.json"
        bsi_path.write_text(_json.dumps(bsi_summary, indent=2, default=str))
        console.print(
            f"[bold cyan]BSI summary saved to[/bold cyan] "
            f"[bold]{bsi_path}[/bold]"
        )

    # ── Post-run: Pillar 3 security/compliance summary ────────────────────────
    if pillar == "3":
        import json as _json
        from evaluators.aggregate import compute_security_summary_from_experiment_dir

        sec_summary = compute_security_summary_from_experiment_dir(output_dir)
        sec_path = Path(output_dir) / "security-compliance-summary.json"
        sec_path.write_text(_json.dumps(sec_summary, indent=2, default=str))
        console.print(
            f"[bold cyan]Security/compliance summary saved to[/bold cyan] "
            f"[bold]{sec_path}[/bold]"
        )
        # Log injection resistance table explicitly — task requirement
        inj_table = sec_summary.get("injection_resistance_table", [])
        if inj_table:
            from rich.table import Table as RichTable
            from rich import box as rbox

            inj_t = RichTable(
                title="Prompt Injection Resistance (p3-05)",
                box=rbox.SIMPLE,
            )
            inj_t.add_column("Agent", style="bold cyan")
            inj_t.add_column("Injection Resisted", justify="center")
            inj_t.add_column("Flagged in Reasoning", justify="center")
            inj_t.add_column("Correct Supplier", justify="center")
            for row in inj_table:
                resisted = "[green]YES[/green]" if row["injected_instruction_not_followed"] else "[red]NO[/red]"
                flagged = "[green]YES[/green]" if row["injection_flagged_in_reasoning"] else "[yellow]NO[/yellow]"
                correct = "[green]YES[/green]" if row["correct_supplier_selected"] else "[red]NO[/red]"
                inj_t.add_row(row["agent_id"], resisted, flagged, correct)
            console.print()
            console.print(inj_t)
        else:
            console.print(
                "[dim]No prompt injection results to display "
                "(all agents skipped or no p3-05 results)[/dim]"
            )

    console.print()
    console.print(
        f"[bold green]Run complete — {len(all_scenarios)} scenario(s) × "
        f"{len(agents_to_run)} agent(s).[/bold green]"
    )
    console.print(f"Results written to [bold]{output_dir}/[/bold]")
    console.print()


@cli.command()
@click.option(
    "--experiment-dir",
    default="results/experiments",
    show_default=True,
    help="Root experiment directory with pillar1/, pillar2/, pillar3/ subdirs",
)
def report(experiment_dir: str) -> None:
    """Generate FULL-REPORT.json and FULL-REPORT.md from all experiment result JSONs."""
    import json
    from pathlib import Path

    from results.report import generate_full_report, render_full_report_markdown

    exp_dir = Path(experiment_dir)
    if not exp_dir.exists():
        console.print(f"[red]Experiment directory not found: {exp_dir}[/red]")
        raise SystemExit(1)

    console.print(
        f"[bold cyan]Generating full report from[/bold cyan] [bold]{exp_dir}[/bold] ..."
    )

    full_report = generate_full_report(str(exp_dir))

    json_path = exp_dir / "FULL-REPORT.json"
    md_path = exp_dir / "FULL-REPORT.md"

    json_path.write_text(json.dumps(full_report, indent=2, default=str))
    md_path.write_text(render_full_report_markdown(full_report))

    console.print("[bold green]Full report saved:[/bold green]")
    console.print(f"  JSON     → [bold]{json_path}[/bold]")
    console.print(f"  Markdown → [bold]{md_path}[/bold]")
    console.print()

    n_agg = len(full_report.get("per_pillar_aggregate", []))
    n_bsi = len(full_report.get("bias_susceptibility_table", []))
    n_sec = len(full_report.get("security_violation_table", []))
    n_delta = len(full_report.get("skills_mcp_delta_table", []))
    console.print(
        f"[dim]Per-pillar rows: {n_agg}  |  BSI rows: {n_bsi}  |  "
        f"Security rows: {n_sec}  |  Delta rows: {n_delta}[/dim]"
    )
    console.print()

    _render_rich_dashboard(full_report, console)


def _score_markup(score: float | None) -> str:
    """Return rich markup for a 0-1 score: green ≥ 0.8, yellow 0.5–0.8, red < 0.5."""
    if score is None:
        return "[dim]—[/dim]"
    if score >= 0.8:
        return f"[bold green]{score:.4f}[/bold green]"
    if score >= 0.5:
        return f"[yellow]{score:.4f}[/yellow]"
    return f"[bold red]{score:.4f}[/bold red]"


def _render_rich_dashboard(report: dict, con: "Console") -> None:
    """Render a multi-panel rich terminal dashboard from a FULL-REPORT dict."""
    con.rule("[bold cyan]BuyerBench Results Dashboard[/bold cyan]")
    con.print()

    # ── 1. Per-pillar aggregate ───────────────────────────────────────────────
    agg_rows = report.get("per_pillar_aggregate", [])
    agg_t = Table(
        title="[bold]1. Per-Pillar Aggregate Scores[/bold]",
        box=box.ROUNDED,
        show_lines=True,
    )
    agg_t.add_column("Agent", style="bold cyan", no_wrap=True)
    agg_t.add_column("Pillar", style="magenta")
    agg_t.add_column("Mean Score", justify="right")
    agg_t.add_column("Std", justify="right", style="dim")
    agg_t.add_column("Min", justify="right")
    agg_t.add_column("Max", justify="right")
    agg_t.add_column("N", justify="right", style="dim")
    if agg_rows:
        for row in agg_rows:
            agg_t.add_row(
                row["agent_id"],
                row["pillar"],
                _score_markup(row["mean_score"]),
                f"{row['std']:.4f}",
                _score_markup(row["min"]),
                _score_markup(row["max"]),
                str(row["n_scenarios"]),
            )
    else:
        agg_t.add_row("[dim]—[/dim]", "[dim]—[/dim]", "[dim]—[/dim]",
                      "[dim]—[/dim]", "[dim]—[/dim]", "[dim]—[/dim]", "[dim]—[/dim]")
    con.print(agg_t)
    con.print()

    # ── 2. Bias Susceptibility Index ─────────────────────────────────────────
    bsi_rows = report.get("bias_susceptibility_table", [])
    bsi_t = Table(
        title="[bold]2. Bias Susceptibility Index[/bold]",
        box=box.ROUNDED,
        show_lines=True,
    )
    bsi_t.add_column("Bias Type", style="bold cyan", no_wrap=True)
    bsi_t.add_column("Agent", style="cyan")
    bsi_t.add_column("Mode", style="magenta")
    bsi_t.add_column("BSI", justify="right")
    bsi_t.add_column("Decision Changed", justify="center")
    if bsi_rows:
        for row in bsi_rows:
            changed = "[bold red]YES[/bold red]" if row["decision_changed"] else "[green]no[/green]"
            bsi_t.add_row(
                row["bias_type"],
                row["agent_id"],
                row["mode"],
                _score_markup(row["bsi"]),
                changed,
            )
    else:
        bsi_t.add_row("[dim]—[/dim]", "[dim]—[/dim]", "[dim]—[/dim]",
                      "[dim]—[/dim]", "[dim]—[/dim]")
    con.print(bsi_t)
    con.print()

    # ── 3. Security compliance ────────────────────────────────────────────────
    sec_rows = report.get("security_violation_table", [])
    sec_t = Table(
        title="[bold]3. Security / Compliance[/bold]",
        box=box.ROUNDED,
        show_lines=True,
    )
    sec_t.add_column("Scenario", style="bold cyan", no_wrap=True)
    sec_t.add_column("Agent", style="cyan")
    sec_t.add_column("Compliance Rate", justify="right")
    sec_t.add_column("Violation Freq", justify="right")
    sec_t.add_column("Score", justify="right")
    if sec_rows:
        for row in sec_rows:
            sec_t.add_row(
                row["scenario_id"],
                row["agent_id"],
                _score_markup(row["compliance_adherence_rate"]),
                _score_markup(1.0 - row["security_violation_frequency"]),
                _score_markup(row["score"]),
            )
    else:
        sec_t.add_row("[dim]—[/dim]", "[dim]—[/dim]", "[dim]—[/dim]",
                      "[dim]—[/dim]", "[dim]—[/dim]")
    con.print(sec_t)
    con.print()

    # ── 4. Skills vs MCP delta ────────────────────────────────────────────────
    delta_rows = report.get("skills_mcp_delta_table", [])
    delta_t = Table(
        title="[bold]4. Skills / MCP Score Delta vs. Baseline[/bold]",
        box=box.ROUNDED,
        show_lines=True,
    )
    delta_t.add_column("Family", style="bold cyan", no_wrap=True)
    delta_t.add_column("Mode", style="magenta")
    delta_t.add_column("Pillar", style="dim")
    delta_t.add_column("Baseline", justify="right")
    delta_t.add_column("Variant", justify="right")
    delta_t.add_column("Δ Delta", justify="right")
    if delta_rows:
        for row in delta_rows:
            delta_val = row.get("delta")
            if delta_val is None:
                delta_markup = "[dim]—[/dim]"
            elif delta_val > 0:
                delta_markup = f"[bold green]+{delta_val:.4f}[/bold green]"
            elif delta_val < 0:
                delta_markup = f"[bold red]{delta_val:.4f}[/bold red]"
            else:
                delta_markup = f"[dim]{delta_val:.4f}[/dim]"
            delta_t.add_row(
                row["family"],
                row["mode"],
                row["pillar"],
                _score_markup(row.get("baseline_score")),
                _score_markup(row.get("variant_score")),
                delta_markup,
            )
    else:
        delta_t.add_row("[dim]—[/dim]", "[dim]—[/dim]", "[dim]—[/dim]",
                        "[dim]—[/dim]", "[dim]—[/dim]", "[dim]—[/dim]")
    con.print(delta_t)
    con.print()

    con.rule("[dim]End of Dashboard[/dim]")
    con.print()


def _write_skipped_results(
    agent_id: str,
    scenarios,
    output_dir: str,
) -> None:
    """Write status=skipped JSON files for each scenario for an unavailable agent."""
    import json
    from datetime import datetime
    from pathlib import Path

    base = Path(output_dir) / agent_id
    base.mkdir(parents=True, exist_ok=True)
    for s in scenarios:
        payload = {
            "status": "skipped",
            "agent_id": agent_id,
            "scenario_id": s.id,
            "reason": "CLI or API key unavailable (see preflight check)",
            "timestamp": datetime.utcnow().isoformat(),
        }
        (base / f"{s.id}.json").write_text(json.dumps(payload, indent=2))


if __name__ == "__main__":
    cli()
