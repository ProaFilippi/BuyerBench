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
    from buyerbench.selector import run_session_tui

    saved_path = run_session_tui()

    if saved_path:
        console.print()
        cmd = f"python -m buyerbench run --from-session {saved_path}"
        console.print(f"[bold]Ready to run:[/bold] [cyan]{cmd}[/cyan]")
        launch = Prompt.ask("Launch now?", choices=["y", "n"], default="y")
        if launch == "y":
            import subprocess
            import sys

            subprocess.run([sys.executable, "-m", "buyerbench", "run", "--from-session", saved_path])


def _rerun_session() -> None:
    console.print()
    console.print(
        "[yellow]Rerun browser coming in Phase 03 — launching session picker for now[/yellow]"
    )
    from buyerbench.selector import run_session_tui

    run_session_tui()


def _reports() -> None:
    console.print()
    console.print(
        "[yellow]Reports browser coming in Phase 04 — launching dashboard for now[/yellow]"
    )
    from buyerbench.dashboard import run_dashboard

    results_dir = str(_RESULTS_ROOT)
    run_dashboard(results_dir)
