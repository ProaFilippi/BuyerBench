"""Rich-powered home screen for BuyerBench — shown when no subcommand is given."""
from __future__ import annotations

from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich import box

console = Console(highlight=False)

_RESULTS_ROOT = Path(__file__).parent.parent / "results"


def _count_experiments(results_dir: Path) -> int:
    """Count non-skipped JSON result files under results_dir."""
    import json

    count = 0
    for path in results_dir.rglob("*.json"):
        try:
            data = json.loads(path.read_text())
        except (json.JSONDecodeError, OSError):
            continue
        if data.get("status") != "skipped":
            count += 1
    return count


def home_tui() -> None:
    """Display the BuyerBench home screen and route to sub-TUIs."""
    try:
        _show_home()
    except KeyboardInterrupt:
        console.print()
        console.print("[dim]Goodbye.[/dim]")


def _show_home() -> None:
    console.print()
    console.print(
        Panel(
            "[bold cyan]BuyerBench — AI Buyer Agent Benchmark[/bold cyan]\n"
            "[dim]Researcher-grade evaluation framework[/dim]",
            border_style="cyan",
            padding=(1, 4),
        )
    )

    # Experiment status line
    if _RESULTS_ROOT.exists():
        n = _count_experiments(_RESULTS_ROOT)
        if n:
            console.print(f"[dim]  {n} experiment{'s' if n != 1 else ''} on record[/dim]")
        else:
            console.print("[dim]  No experiments yet[/dim]")
    else:
        console.print("[dim]  No experiments yet[/dim]")

    console.print()

    # Menu table
    menu = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
    menu.add_column("Key", style="bold cyan", no_wrap=True)
    menu.add_column("Action", style="bold white", no_wrap=True)
    menu.add_column("Description", style="dim")
    menu.add_row("[1]", "New Session", "Configure and launch a new benchmark run")
    menu.add_row("[2]", "Rerun / Continue", "Pick and re-run an existing session")
    menu.add_row("[3]", "Reports & Papers", "Browse results, dashboards, and academic outputs")
    menu.add_row("[q]", "Quit", "")
    console.print(menu)

    choice = Prompt.ask("Select", choices=["1", "2", "3", "q"], show_choices=False)

    if choice == "1":
        _new_session()
    elif choice == "2":
        _rerun_session()
    elif choice == "3":
        _reports()
    else:
        console.print("[dim]Goodbye.[/dim]")


def _new_session() -> None:
    import subprocess
    import sys
    from buyerbench.selector import wizard_new_session, _make_session_path

    config = wizard_new_session()

    session_dir = _make_session_path(config.experiment_name, config.created_at)
    config_path = session_dir / "session-config.yaml"

    if config.recurrence:
        console.print()
        console.print(
            Panel(
                f"To activate recurring runs, register this session with the scheduler:\n\n"
                f"  [bold cyan]claude /schedule[/bold cyan] "
                f"[cyan]\"BuyerBench: {config.experiment_name}\"[/cyan] \\\\\n"
                f"    [cyan]--cron \"{config.recurrence}\"[/cyan] \\\\\n"
                f"    [cyan]--command \"python -m buyerbench run "
                f"--from-session {config_path}\"[/cyan]",
                title="[bold yellow]Scheduler Setup[/bold yellow]",
                border_style="yellow",
            )
        )
    else:
        console.print()
        launch = Prompt.ask("Run now?", choices=["y", "n"], default="n")
        if launch == "y":
            subprocess.run(
                [sys.executable, "-m", "buyerbench", "run", "--from-session", str(config_path)]
            )


def _rerun_session() -> None:
    from buyerbench.session_browser import browse_sessions

    browse_sessions()


def _reports() -> None:
    console.print()
    console.print(
        "[yellow]Reports browser coming in Phase 04 — launching dashboard for now[/yellow]"
    )
    from buyerbench.dashboard import run_dashboard

    results_dir = str(_RESULTS_ROOT)
    run_dashboard(results_dir)
