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
@click.option("--agent", required=True, help="Agent name to evaluate")
@click.option("--scenario", default=None, help="Specific scenario ID to run")
@click.option("--pillar", default=None, type=click.Choice(["1", "2", "3"]), help="Pillar filter")
def run(agent: str, scenario: str | None, pillar: str | None) -> None:
    """Run the full benchmark suite against a named agent. (Not yet implemented.)"""
    console.print(
        f"[yellow]run --agent {agent!r} is not yet implemented.[/yellow]\n"
        "Use [bold]python -m buyerbench demo[/bold] to test the pipeline."
    )


if __name__ == "__main__":
    cli()
