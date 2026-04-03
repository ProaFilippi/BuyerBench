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
@click.option("--agent", required=True, help="Agent ID to evaluate (e.g. claude-code-baseline)")
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
    """Run the benchmark suite against a named CLI agent."""
    from pathlib import Path

    from agents.registry import AGENT_REGISTRY, get_agent
    from harness.config import load_config
    from harness.loader import load_all_scenarios
    from harness.runner import run_scenario

    # Validate agent_id before loading any scenarios
    if agent not in AGENT_REGISTRY:
        available = sorted(AGENT_REGISTRY.keys())
        console.print(
            f"[red]Unknown agent {agent!r}.[/red]\n"
            f"Available agents: {', '.join(available)}"
        )
        raise SystemExit(1)

    config = load_config()
    config["dry_run"] = dry_run
    agent_instance = get_agent(agent, config)

    scenarios_root = Path(__file__).parent.parent / "scenarios"
    all_scenarios = load_all_scenarios(str(scenarios_root))

    # Apply filters
    if pillar:
        pillar_enum = f"PILLAR{pillar}"
        all_scenarios = [s for s in all_scenarios if s.pillar.value == pillar_enum]
    if scenario:
        all_scenarios = [s for s in all_scenarios if s.id == scenario]

    if not all_scenarios:
        console.print("[yellow]No scenarios matched the given filters.[/yellow]")
        return

    if dry_run:
        console.print(
            f"[bold cyan]DRY RUN[/bold cyan] — agent=[bold]{agent}[/bold]  "
            f"scenarios={len(all_scenarios)}"
        )
        for s in all_scenarios:
            agent_instance.respond(s)  # prints prompt, returns empty response
        return

    table = Table(
        title=f"BuyerBench Run — {agent}",
        box=box.ROUNDED,
        show_lines=True,
    )
    table.add_column("Scenario", style="bold cyan", no_wrap=True)
    table.add_column("Pillar", style="magenta")
    table.add_column("Score", justify="right")
    table.add_column("Status", justify="center")

    for s in all_scenarios:
        result = run_scenario(s, agent_instance)
        score = result.pillar_scores[0].score if result.pillar_scores else 0.0
        status = "[green]PASS[/green]" if result.overall_pass else "[red]FAIL[/red]"
        table.add_row(s.title[:50], s.pillar.value, f"{score:.2f}", status)

    console.print()
    console.print(table)
    console.print()
    console.print(
        f"[bold green]Run complete — {len(all_scenarios)} scenario(s) evaluated.[/bold green]"
    )
    console.print(f"Results written to [bold]{output_dir}/[/bold]")
    console.print()


if __name__ == "__main__":
    cli()
