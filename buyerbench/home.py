"""Rich-powered home screen for BuyerBench — shown when no subcommand is given."""
from __future__ import annotations

from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.text import Text
from rich import box

console = Console(highlight=False)

_RESULTS_ROOT = Path(__file__).parent.parent / "results"
_SESSIONS_ROOT = Path(__file__).parent.parent / "sessions"


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


def _last_run_info(results_dir: Path) -> str | None:
    """Return a formatted 'Last run: <timestamp>' string, or None if no results exist."""
    from datetime import datetime

    json_files = list(results_dir.rglob("*.json")) if results_dir.exists() else []
    if not json_files:
        return None
    latest = max(json_files, key=lambda p: p.stat().st_mtime)
    ts = datetime.fromtimestamp(latest.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
    n = len(json_files)
    return f"Last run: {ts}  |  {n} experiment{'s' if n != 1 else ''} on record"


def _is_first_launch(results_dir: Path, sessions_dir: Path) -> bool:
    """Return True when neither a sessions directory nor any result JSON files exist."""
    no_sessions = not sessions_dir.exists()
    no_results = not results_dir.exists() or not any(results_dir.rglob("*.json"))
    return no_sessions and no_results


def _show_onboarding() -> None:
    """Display a first-launch welcome panel and wait for the user to continue."""
    console.print()
    console.print(
        Panel(
            "[bold cyan]Welcome to BuyerBench![/bold cyan]\n\n"
            "To get started:\n\n"
            "  [bold][1][/bold] Run the demo first to verify your setup:\n"
            "      [cyan]python -m buyerbench demo[/cyan]\n\n"
            "  [bold][2][/bold] Then create your first research session with "
            "[bold cyan][1] New Session[/bold cyan]",
            border_style="cyan",
            padding=(1, 4),
        )
    )
    Prompt.ask("[dim]Press Enter to continue[/dim]", default="")


def home_tui() -> None:
    """Display the BuyerBench home screen and route to sub-TUIs."""
    try:
        _show_home()
    except KeyboardInterrupt:
        console.print()
        console.print("[dim]Goodbye.[/dim]")


def _show_home() -> None:
    if _is_first_launch(_RESULTS_ROOT, _SESSIONS_ROOT):
        _show_onboarding()

    console.print()
    console.print(
        Panel(
            "[bold cyan]BuyerBench — AI Buyer Agent Benchmark[/bold cyan]\n"
            "[dim]Researcher-grade evaluation framework[/dim]",
            border_style="cyan",
            padding=(1, 4),
        )
    )

    # Last-run status line (timestamp + experiment count)
    last_run = _last_run_info(_RESULTS_ROOT)
    if last_run:
        console.print(f"[dim]  {last_run}[/dim]")
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

    # Keyboard shortcut help bar
    help_bar = Text(justify="left")
    help_bar.append("  Ctrl+C", style="bold cyan")
    help_bar.append(": quit   ", style="dim")
    help_bar.append("/", style="bold cyan")
    help_bar.append(": search sessions   ", style="dim")
    help_bar.append("?", style="bold cyan")
    help_bar.append(": help", style="dim")
    console.print(help_bar)
    console.print()

    choice = Prompt.ask("Select", choices=["1", "2", "3", "q", "/", "?"], show_choices=False)

    if choice == "1":
        _new_session()
    elif choice == "2":
        _rerun_session()
    elif choice == "3":
        _reports()
    elif choice in ("/", "?"):
        # Stubs: re-display the home screen (search/help not yet implemented)
        _show_home()
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
    from buyerbench.reports_browser import browse_reports

    browse_reports()
