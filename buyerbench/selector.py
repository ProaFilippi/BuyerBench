"""Interactive Rich-powered terminal UI for selecting OpenRouter models to benchmark.

Public API
----------
display_catalog_table(catalog, selected_ids) — render a Rich table
interactive_select(catalog)                   — main TUI loop
save_selection(agent_ids, path)               — persist to YAML
load_selection(path)                          — load from YAML

Session config API
------------------
AgentSlot                                     — dataclass: agent_id + skill_mode
SessionConfig                                 — dataclass: agents + scenario_ids + created_at
save_session_config(config, path)             — serialize SessionConfig to YAML
load_session_config(path)                     — deserialize SessionConfig from YAML
"""
from __future__ import annotations

import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional

import yaml
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.text import Text
from rich import box

from buyerbench.model_catalog import MODEL_CATALOG, ModelEntry, filter_catalog

console = Console()


# ── Session Config dataclasses ─────────────────────────────────────────────────

@dataclass
class AgentSlot:
    """One agent selected for a benchmark session, with its configured skill mode."""
    agent_id: str
    skill_mode: str  # "baseline" | "skills" | "mcp"


@dataclass
class SessionConfig:
    """Complete pre-run session configuration produced by the TUI."""
    agents: list[AgentSlot]
    scenario_ids: list[str]
    created_at: str


def save_session_config(
    config: SessionConfig,
    path: str = "session-config.yaml",
) -> None:
    """Serialize a SessionConfig to a YAML file.

    The YAML structure uses plain dicts so it remains human-editable:

    .. code-block:: yaml

        agents:
          - agent_id: openrouter-openai-gpt-4o
            skill_mode: baseline
        scenario_ids:
          - p1-01-supplier-discovery
        created_at: '2026-04-08T12:00:00+00:00'
    """
    payload = {
        "agents": [
            {"agent_id": slot.agent_id, "skill_mode": slot.skill_mode}
            for slot in config.agents
        ],
        "scenario_ids": config.scenario_ids,
        "created_at": config.created_at,
    }
    with open(path, "w", encoding="utf-8") as fh:
        yaml.safe_dump(payload, fh, default_flow_style=False, allow_unicode=True)


def load_session_config(path: str = "session-config.yaml") -> SessionConfig:
    """Deserialize a SessionConfig from a YAML file produced by save_session_config.

    Parameters
    ----------
    path:
        Source file path.

    Returns
    -------
    SessionConfig
        Populated dataclass instance.
    """
    with open(path, "r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}

    agents = [
        AgentSlot(agent_id=a["agent_id"], skill_mode=a["skill_mode"])
        for a in data.get("agents", [])
    ]
    return SessionConfig(
        agents=agents,
        scenario_ids=data.get("scenario_ids", []),
        created_at=data.get("created_at", ""),
    )

_SKILL_LABELS = {
    "baseline": ("baseline", "dim"),
    "skills": ("skills", "green"),
    "mcp": ("mcp", "cyan"),
}
_SKILL_ABBREVS = {"b": "baseline", "s": "skills", "m": "mcp"}


def _display_skill_table(agent_ids: list[str], modes: dict[str, str]) -> None:
    """Render the per-agent skill-mode table."""
    t = Table(
        title="[bold cyan]BuyerBench — Per-Agent Skill Configuration[/bold cyan]",
        box=box.ROUNDED,
        show_lines=True,
        highlight=True,
    )
    t.add_column("#", style="dim", justify="right", no_wrap=True)
    t.add_column("Agent ID", style="bold", no_wrap=True)
    t.add_column("Skill Mode", justify="center")

    for idx, aid in enumerate(agent_ids, start=1):
        mode = modes.get(aid, "baseline")
        label, color = _SKILL_LABELS.get(mode, (mode, "white"))
        t.add_row(str(idx), aid, Text(label, style=f"bold {color}"))

    console.print()
    console.print(t)


def interactive_skill_select(agent_ids: list[str]) -> dict[str, str]:
    """Interactively assign a skill mode to each selected agent.

    Shows a Rich table listing every agent with its current skill mode.
    The user can change modes one agent at a time or batch-set all agents.

    Commands
    --------
    1 b / 1 s / 1 m    Set agent #1 to baseline / skills / mcp
    a b / a s / a m    Set ALL agents to the given mode
    done               Confirm and return
    q / quit           Abort (raises SystemExit(0))

    Parameters
    ----------
    agent_ids:
        Ordered list of agent IDs selected in Step 1.

    Returns
    -------
    dict[str, str]
        Maps each ``agent_id`` to its chosen ``skill_mode``.
    """
    modes: dict[str, str] = {aid: "baseline" for aid in agent_ids}

    console.print(
        Panel(
            "[bold]Commands:[/bold]  "
            "[cyan]<N> b[/cyan] baseline  "
            "[cyan]<N> s[/cyan] skills  "
            "[cyan]<N> m[/cyan] mcp  "
            "[cyan]a b/s/m[/cyan] set-all  "
            "[cyan]done[/cyan] confirm  "
            "[cyan]q[/cyan] quit",
            title="Skill Mode Selector",
            border_style="cyan",
        )
    )

    while True:
        _display_skill_table(agent_ids, modes)
        console.print()

        raw = Prompt.ask("[bold cyan]>[/bold cyan]").strip()
        if not raw:
            continue

        tokens = raw.lower().split()

        # Quit
        if tokens[0] in ("q", "quit"):
            console.print("[yellow]Selection aborted.[/yellow]")
            raise SystemExit(0)

        # Confirm
        if tokens[0] == "done":
            break

        # Batch set: "a b" / "a s" / "a m"
        if tokens[0] == "a" and len(tokens) == 2:
            abbrev = tokens[1]
            if abbrev not in _SKILL_ABBREVS:
                console.print(
                    f"[yellow]Unknown mode '{abbrev}'. Use b (baseline), s (skills), or m (mcp).[/yellow]"
                )
                continue
            new_mode = _SKILL_ABBREVS[abbrev]
            for aid in agent_ids:
                modes[aid] = new_mode
            console.print(f"[dim]All agents set to [bold]{new_mode}[/bold].[/dim]")
            continue

        # Per-agent: "<N> b/s/m"
        if len(tokens) == 2 and tokens[0].isdigit():
            idx = int(tokens[0]) - 1
            abbrev = tokens[1]
            if idx < 0 or idx >= len(agent_ids):
                console.print(
                    f"[yellow]Index {tokens[0]} out of range (1–{len(agent_ids)})[/yellow]"
                )
                continue
            if abbrev not in _SKILL_ABBREVS:
                console.print(
                    f"[yellow]Unknown mode '{abbrev}'. Use b (baseline), s (skills), or m (mcp).[/yellow]"
                )
                continue
            aid = agent_ids[idx]
            modes[aid] = _SKILL_ABBREVS[abbrev]
            console.print(
                f"[dim]Agent [bold]{aid}[/bold] → [bold]{modes[aid]}[/bold][/dim]"
            )
            continue

        console.print(
            f"[yellow]Unknown command: '{raw}'. "
            "Use '<N> b/s/m', 'a b/s/m', 'done', or 'q'.[/yellow]"
        )

    return modes


_COST_COLORS = {
    "free": "bright_green",
    "low": "green",
    "mid": "yellow",
    "high": "red",
}


def display_catalog_table(
    catalog: list[ModelEntry],
    selected_ids: set[str],
) -> None:
    """Render the model catalog as a Rich Table.

    Color-codes cost tiers (green=low, yellow=mid, red=high) and highlights
    currently selected rows.

    Parameters
    ----------
    catalog:
        Ordered list of entries to display (may be a filtered sub-list).
    selected_ids:
        Set of ``agent_id`` strings that are currently selected; these rows
        receive a checkmark and row highlight.
    """
    t = Table(
        title="[bold cyan]BuyerBench — OpenRouter Model Catalog[/bold cyan]",
        box=box.ROUNDED,
        show_lines=True,
        highlight=True,
    )
    t.add_column("#", style="dim", justify="right", no_wrap=True)
    t.add_column("Model Name", style="bold", no_wrap=True)
    t.add_column("Provider", style="cyan")
    t.add_column("Context", justify="right")
    t.add_column("Cost", justify="center")
    t.add_column("Tags")
    t.add_column("Selected", justify="center")

    for idx, entry in enumerate(catalog, start=1):
        is_selected = entry.agent_id in selected_ids
        row_style = "bold on dark_blue" if is_selected else ""

        cost_color = _COST_COLORS.get(entry.cost_tier, "white")
        cost_cell = Text(entry.cost_tier.upper(), style=cost_color)

        selected_cell = Text("✓", style="bold green") if is_selected else Text("·", style="dim")
        tags_cell = ", ".join(entry.capability_tags)
        context_cell = f"{entry.context_k}K"

        t.add_row(
            str(idx),
            entry.display_name,
            entry.provider,
            context_cell,
            cost_cell,
            tags_cell,
            selected_cell,
            style=row_style,
        )

    console.print()
    console.print(t)


def interactive_select(
    catalog: list[ModelEntry] | None = None,
) -> list[str]:
    """Run the interactive model-selection TUI loop.

    Prompts the user to toggle model selections with comma-separated numbers,
    filter commands, and navigation keywords.

    Commands accepted at the prompt
    --------------------------------
    1,3,5       Toggle items by 1-based index (comma-separated or space-separated)
    a           Select all visible entries
    c           Clear all selections
    f <tag>     Filter visible entries by capability tag
    p <prov>    Filter visible entries by provider name
    reset       Remove current filter (show full catalog)
    done        Confirm selection (requires ≥ 1 entry selected)
    q / quit    Abort without saving (raises SystemExit(0))

    Parameters
    ----------
    catalog:
        Starting catalog to display.  Defaults to the full ``MODEL_CATALOG``.

    Returns
    -------
    list[str]
        Ordered list of selected ``agent_id`` strings.
    """
    if catalog is None:
        catalog = MODEL_CATALOG[:]

    full_catalog = catalog[:]
    visible_catalog = catalog[:]
    selected_ids: set[str] = set()

    console.print(
        Panel(
            "[bold]Commands:[/bold]  "
            "[cyan]1,3,5[/cyan] toggle  "
            "[cyan]a[/cyan] select-all  "
            "[cyan]c[/cyan] clear  "
            "[cyan]f <tag>[/cyan] filter-tag  "
            "[cyan]p <provider>[/cyan] filter-provider  "
            "[cyan]reset[/cyan] show-all  "
            "[cyan]done[/cyan] confirm  "
            "[cyan]q[/cyan] quit",
            title="Model Selector",
            border_style="cyan",
        )
    )

    while True:
        display_catalog_table(visible_catalog, selected_ids)
        console.print(
            f"[dim]Selected: {len(selected_ids)} / {len(full_catalog)}[/dim]  "
            f"[dim]Visible: {len(visible_catalog)}[/dim]"
        )
        console.print()

        raw = Prompt.ask("[bold cyan]>[/bold cyan]").strip()
        if not raw:
            continue

        cmd = raw.lower()

        # Quit
        if cmd in ("q", "quit"):
            console.print("[yellow]Selection aborted.[/yellow]")
            raise SystemExit(0)

        # Confirm
        if cmd == "done":
            if not selected_ids:
                console.print(
                    "[red]Please select at least one model before confirming.[/red]"
                )
                continue
            break

        # Select all visible
        if cmd == "a":
            for entry in visible_catalog:
                selected_ids.add(entry.agent_id)
            continue

        # Clear all
        if cmd == "c":
            selected_ids.clear()
            continue

        # Reset filter
        if cmd == "reset":
            visible_catalog = full_catalog[:]
            console.print("[dim]Filter cleared — showing all models.[/dim]")
            continue

        # Filter by tag: "f <tag>"
        if cmd.startswith("f "):
            tag = raw[2:].strip()
            if not tag:
                console.print("[yellow]Usage: f <tag>   e.g. f coding[/yellow]")
                continue
            visible_catalog = filter_catalog(tags=[tag])
            if not visible_catalog:
                console.print(f"[yellow]No models found with tag '{tag}'. Type reset to show all.[/yellow]")
                visible_catalog = full_catalog[:]
            else:
                console.print(f"[dim]Filtered by tag '[bold]{tag}[/bold]' — {len(visible_catalog)} result(s)[/dim]")
            continue

        # Filter by provider: "p <provider>"
        if cmd.startswith("p "):
            prov = raw[2:].strip()
            if not prov:
                console.print("[yellow]Usage: p <provider>   e.g. p Mistral[/yellow]")
                continue
            visible_catalog = filter_catalog(providers=[prov])
            if not visible_catalog:
                console.print(f"[yellow]No models found for provider '{prov}'. Type reset to show all.[/yellow]")
                visible_catalog = full_catalog[:]
            else:
                console.print(f"[dim]Filtered by provider '[bold]{prov}[/bold]' — {len(visible_catalog)} result(s)[/dim]")
            continue

        # Toggle by number(s): "1", "1,3", "1 3 5"
        tokens = raw.replace(",", " ").split()
        if all(t.isdigit() for t in tokens):
            for tok in tokens:
                idx = int(tok) - 1
                if 0 <= idx < len(visible_catalog):
                    entry = visible_catalog[idx]
                    if entry.agent_id in selected_ids:
                        selected_ids.discard(entry.agent_id)
                    else:
                        selected_ids.add(entry.agent_id)
                else:
                    console.print(
                        f"[yellow]Index {tok} out of range (1–{len(visible_catalog)})[/yellow]"
                    )
            continue

        console.print(
            f"[yellow]Unknown command: '{raw}'. Type 'done' to confirm or 'q' to quit.[/yellow]"
        )

    # Return selected agent_ids preserving MODEL_CATALOG order
    order_map = {e.agent_id: i for i, e in enumerate(MODEL_CATALOG)}
    return sorted(selected_ids, key=lambda aid: order_map.get(aid, 9999))


def save_selection(
    agent_ids: list[str],
    path: str = "session-selection.yaml",
) -> None:
    """Persist a model selection to a YAML file.

    Parameters
    ----------
    agent_ids:
        Ordered list of ``agent_id`` strings to save.
    path:
        Destination file path (default: ``session-selection.yaml`` in the CWD).
    """
    payload = {
        "selected_agents": agent_ids,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    with open(path, "w", encoding="utf-8") as fh:
        yaml.safe_dump(payload, fh, default_flow_style=False, allow_unicode=True)


def load_selection(path: str = "session-selection.yaml") -> list[str]:
    """Load a previously saved model selection from a YAML file.

    Parameters
    ----------
    path:
        Source file path.

    Returns
    -------
    list[str]
        The ``selected_agents`` list from the YAML, or an empty list if the
        key is absent.
    """
    with open(path, "r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    return data.get("selected_agents", [])
