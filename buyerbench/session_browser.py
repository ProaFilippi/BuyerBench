"""Session browser — scan sessions/ for past configs and allow rerun or modify.

Public API
----------
browse_sessions()   — Rich table of past sessions; sub-menu for rerun / modify / view
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text
from rich import box

from buyerbench.selector import SessionConfig, load_session_config

console = Console(highlight=False)

_SESSIONS_ROOT = Path("sessions")
_RESULTS_ROOT = Path("results")


def _find_session_configs() -> list[Path]:
    """Recursively find all session-config.yaml files.

    Scans ``sessions/`` first; falls back to ``results/`` for legacy layouts.
    """
    if _SESSIONS_ROOT.exists():
        found = sorted(_SESSIONS_ROOT.rglob("session-config.yaml"))
        if found:
            return found
    if _RESULTS_ROOT.exists():
        return sorted(_RESULTS_ROOT.rglob("session-config.yaml"))
    return []


def _has_results(config: SessionConfig) -> bool:
    """Return True if a results directory matching the experiment name exists."""
    results_dir = Path(config.output_dir) if config.output_dir else _RESULTS_ROOT
    if not results_dir.exists() or not config.experiment_name:
        return False
    return any(
        d for d in results_dir.iterdir()
        if d.is_dir() and config.experiment_name in d.name
    )


def _format_created_at(created_at: str) -> str:
    """Trim an ISO-8601 timestamp down to a YYYY-MM-DD date string."""
    if not created_at:
        return "—"
    return created_at[:10]


def browse_sessions() -> None:
    """Scan the sessions directory and present an interactive session browser.

    Displays a Rich table of past sessions with key metadata, then lets the
    researcher pick one to re-run as-is, modify via the wizard, or inspect.

    Returns
    -------
    None
        Always returns None; side-effects are sub-process launches or wizard
        invocations.
    """
    console.print()

    config_paths = _find_session_configs()

    if not config_paths:
        console.print(
            "[dim]No sessions found. Create one with [bold cyan][1] New Session[/bold cyan].[/dim]"
        )
        return None

    # Load each config, skip malformed ones silently
    rows: list[tuple[Path, SessionConfig, bool]] = []
    for path in config_paths:
        try:
            config = load_session_config(str(path))
            rows.append((path, config, _has_results(config)))
        except Exception:
            continue

    if not rows:
        console.print(
            "[dim]No valid sessions found. Create one with [bold cyan][1] New Session[/bold cyan].[/dim]"
        )
        return None

    # ── Build table ───────────────────────────────────────────────────────────
    t = Table(
        title="[bold cyan]BuyerBench — Session Browser[/bold cyan]",
        box=box.ROUNDED,
        show_lines=True,
        highlight=True,
    )
    t.add_column("#", style="dim", justify="right", no_wrap=True)
    t.add_column("Experiment", style="bold", no_wrap=True)
    t.add_column("Created", style="cyan", no_wrap=True)
    t.add_column("Models", justify="right")
    t.add_column("Scenarios", justify="right")
    t.add_column("Recurrence")
    t.add_column("Has Results", justify="center")

    for idx, (path, config, has_results) in enumerate(rows, start=1):
        exp_name = config.experiment_name or path.parent.name
        created = _format_created_at(config.created_at)
        model_count = str(len(config.agents))
        scenario_count = str(len(config.scenario_ids)) if config.scenario_ids else "all"
        recurrence = config.recurrence or "one-shot"
        results_cell = Text("✓", style="bold green") if has_results else Text("—", style="dim")

        t.add_row(
            str(idx),
            exp_name,
            created,
            model_count,
            scenario_count,
            recurrence,
            results_cell,
        )

    console.print(t)
    console.print()

    # ── Selection prompt ──────────────────────────────────────────────────────
    valid_choices = [str(i) for i in range(1, len(rows) + 1)] + ["q"]
    raw = Prompt.ask(
        f"Select session [1-{len(rows)}] or [q] back",
        choices=valid_choices,
        show_choices=False,
    )

    if raw.lower() == "q":
        return None

    selected_idx = int(raw) - 1
    selected_path, selected_config, _ = rows[selected_idx]

    # ── Sub-menu loop ─────────────────────────────────────────────────────────
    while True:
        exp_label = selected_config.experiment_name or selected_path.parent.name
        console.print()
        console.print(
            Panel(
                f"[bold]Experiment:[/bold] {exp_label}\n"
                f"[bold]Config:[/bold]     {selected_path}\n\n"
                "  [bold cyan]\\[1][/bold cyan]  Re-run as-is\n"
                "  [bold cyan]\\[2][/bold cyan]  Modify (edit in wizard)\n"
                "  [bold cyan]\\[3][/bold cyan]  View config (YAML)\n"
                "  [bold cyan]\\[4][/bold cyan]  Back",
                title="[bold white]Session Actions[/bold white]",
                border_style="cyan",
            )
        )

        action = Prompt.ask("Action", choices=["1", "2", "3", "4"], show_choices=False)
        action = {"1": "r", "2": "m", "3": "v", "4": "b"}[action]

        if action == "r":
            console.print(f"\n[dim]Re-running session: {selected_path}[/dim]\n")
            subprocess.run(
                [sys.executable, "-m", "buyerbench", "run", "--from-session", str(selected_path)]
            )
            return

        if action == "m":
            from buyerbench.selector import wizard_new_session
            wizard_new_session(prefill=selected_config)
            return

        if action == "v":
            raw_yaml = selected_path.read_text(encoding="utf-8")
            syntax = Syntax(raw_yaml, "yaml", theme="monokai", line_numbers=True)
            console.print(
                Panel(
                    syntax,
                    title=f"[bold white]{selected_path.name}[/bold white]",
                    border_style="cyan",
                )
            )
            # Loop back to sub-menu automatically

        if action == "b":
            return None
