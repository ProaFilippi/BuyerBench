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

    console.print()
    console.print(
        f"[bold green]Run complete — {len(all_scenarios)} scenario(s) × "
        f"{len(agents_to_run)} agent(s).[/bold green]"
    )
    console.print(f"Results written to [bold]{output_dir}/[/bold]")
    console.print()


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
