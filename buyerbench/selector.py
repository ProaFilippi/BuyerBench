"""Interactive Rich-powered terminal UI for selecting OpenRouter models to benchmark.

Public API
----------
display_catalog_table(catalog, selected_ids) — render a Rich table
interactive_select(catalog)                   — main TUI loop (model selection)
interactive_skill_select(agent_ids)           — per-agent skill-mode TUI loop
interactive_scenario_select(scenarios)        — scenario multi-select TUI loop
run_session_tui()                             — full three-pane session config TUI
wizard_new_session()                          — enhanced 6-step researcher wizard
save_selection(agent_ids, path)               — persist to YAML
load_selection(path)                          — load from YAML

Session config API
------------------
AgentSlot                                     — dataclass: agent_id + skill_mode
SessionConfig                                 — dataclass: full session configuration
save_session_config(config, path)             — serialize SessionConfig to YAML
load_session_config(path)                     — deserialize SessionConfig from YAML
"""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
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
    experiment_name: str = ""
    research_objective: str = ""
    research_notes: str = ""
    recurrence: Optional[str] = None
    output_dir: str = "results"


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
        "experiment_name": config.experiment_name,
        "research_objective": config.research_objective,
        "research_notes": config.research_notes,
        "recurrence": config.recurrence,
        "output_dir": config.output_dir,
        "agents": [
            {"agent_id": slot.agent_id, "skill_mode": slot.skill_mode}
            for slot in config.agents
        ],
        "scenario_ids": config.scenario_ids,
        "created_at": config.created_at,
    }
    Path(path).parent.mkdir(parents=True, exist_ok=True)
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
        experiment_name=data.get("experiment_name", ""),
        research_objective=data.get("research_objective", ""),
        research_notes=data.get("research_notes", ""),
        recurrence=data.get("recurrence"),
        output_dir=data.get("output_dir", "results"),
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


_PILLAR_COLORS = {
    "PILLAR1": "blue",
    "PILLAR2": "yellow",
    "PILLAR3": "red",
}

_DIFFICULTY_COLORS = {
    "easy": "green",
    "medium": "yellow",
    "hard": "red",
}

# Maps "p1"/"p2"/"p3" command prefix → canonical pillar value string
_PILLAR_CMD_MAP = {
    "p1": "PILLAR1",
    "p2": "PILLAR2",
    "p3": "PILLAR3",
}


def _display_scenario_table(scenarios: list, selected_ids: set[str]) -> None:
    """Render the scenario selection table."""
    t = Table(
        title="[bold cyan]BuyerBench — Scenario Selection[/bold cyan]",
        box=box.ROUNDED,
        show_lines=True,
        highlight=True,
    )
    t.add_column("#", style="dim", justify="right", no_wrap=True)
    t.add_column("ID", style="bold", no_wrap=True)
    t.add_column("Title")
    t.add_column("Pillar", justify="center")
    t.add_column("Difficulty", justify="center")
    t.add_column("Selected", justify="center")

    for idx, scenario in enumerate(scenarios, start=1):
        is_selected = scenario.id in selected_ids
        row_style = "bold on dark_blue" if is_selected else ""

        pillar_val = scenario.pillar.value if hasattr(scenario.pillar, "value") else str(scenario.pillar)
        pillar_color = _PILLAR_COLORS.get(pillar_val, "white")
        pillar_label = pillar_val.replace("PILLAR", "P")

        diff_val = scenario.difficulty.value if hasattr(scenario.difficulty, "value") else str(scenario.difficulty)
        diff_color = _DIFFICULTY_COLORS.get(diff_val, "white")

        selected_cell = Text("✓", style="bold green") if is_selected else Text("·", style="dim")

        t.add_row(
            str(idx),
            scenario.id,
            scenario.title,
            Text(pillar_label, style=f"bold {pillar_color}"),
            Text(diff_val, style=diff_color),
            selected_cell,
            style=row_style,
        )

    console.print()
    console.print(t)


def interactive_scenario_select(scenarios: list) -> list[str]:
    """Interactively select scenarios for the benchmark session.

    Shows a Rich table with columns: #, ID, Title, Pillar, Difficulty, Selected.

    Commands
    --------
    1,3,5       Toggle by comma-separated or space-separated 1-based indices
    a           Select all scenarios
    c           Clear all selections
    p1/p2/p3    Select all scenarios in the given pillar
    done        Confirm selection
    q / quit    Abort (raises SystemExit(0))

    Parameters
    ----------
    scenarios:
        List of Scenario objects; each must have ``.id``, ``.title``,
        ``.pillar``, and ``.difficulty`` attributes.

    Returns
    -------
    list[str]
        Ordered list of selected scenario IDs (preserving input order).
    """
    selected_ids: set[str] = set()

    console.print(
        Panel(
            "[bold]Commands:[/bold]  "
            "[cyan]1,3,5[/cyan] toggle  "
            "[cyan]a[/cyan] select-all  "
            "[cyan]c[/cyan] clear  "
            "[cyan]p1/p2/p3[/cyan] select-pillar  "
            "[cyan]done[/cyan] confirm  "
            "[cyan]q[/cyan] quit",
            title="Scenario Selector",
            border_style="cyan",
        )
    )

    while True:
        _display_scenario_table(scenarios, selected_ids)
        console.print(
            f"[dim]Selected: {len(selected_ids)} / {len(scenarios)}[/dim]"
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
            break

        # Select all
        if cmd == "a":
            for s in scenarios:
                selected_ids.add(s.id)
            continue

        # Clear all
        if cmd == "c":
            selected_ids.clear()
            continue

        # Pillar filter: "p1", "p2", "p3"
        if cmd in _PILLAR_CMD_MAP:
            target_pillar = _PILLAR_CMD_MAP[cmd]
            added = 0
            for s in scenarios:
                pillar_val = s.pillar.value if hasattr(s.pillar, "value") else str(s.pillar)
                if pillar_val == target_pillar:
                    selected_ids.add(s.id)
                    added += 1
            console.print(
                f"[dim]Added {added} scenario(s) from pillar [bold]{target_pillar}[/bold].[/dim]"
            )
            continue

        # Toggle by number(s): "1", "1,3", "1 3 5"
        tokens = raw.replace(",", " ").split()
        if tokens and all(t.isdigit() for t in tokens):
            for tok in tokens:
                idx = int(tok) - 1
                if 0 <= idx < len(scenarios):
                    s = scenarios[idx]
                    if s.id in selected_ids:
                        selected_ids.discard(s.id)
                    else:
                        selected_ids.add(s.id)
                else:
                    console.print(
                        f"[yellow]Index {tok} out of range (1–{len(scenarios)})[/yellow]"
                    )
            continue

        console.print(
            f"[yellow]Unknown command: '{raw}'. "
            "Use '1,3', 'a', 'c', 'p1/p2/p3', 'done', or 'q'.[/yellow]"
        )

    # Return IDs in original scenario order
    order_map = {s.id: i for i, s in enumerate(scenarios)}
    return sorted(selected_ids, key=lambda sid: order_map.get(sid, 9999))


def run_session_tui() -> "SessionConfig":
    """Run the full three-pane session configuration TUI.

    Chains model selection, per-agent skill configuration, and scenario
    selection into a single guided workflow, then returns a complete
    :class:`SessionConfig` ready to be persisted with
    :func:`save_session_config`.

    Steps
    -----
    1. Print a welcome header panel.
    2. Call :func:`interactive_select` — the user picks models.
    3. Call :func:`interactive_skill_select` — per-model skill modes.
    4. Load all scenarios and call :func:`interactive_scenario_select`.
    5. Build and return :class:`SessionConfig`.
    6. Print a rich summary panel.

    Returns
    -------
    SessionConfig
        Fully populated session configuration.
    """
    from datetime import datetime, timezone
    from harness.loader import load_all_scenarios

    # ── Welcome header ────────────────────────────────────────────────────────
    console.print()
    console.print(
        Panel(
            "[bold cyan]Configure your BuyerBench experiment in three steps:[/bold cyan]\n"
            "  [dim]1.[/dim] Select models to evaluate\n"
            "  [dim]2.[/dim] Choose skill mode per model\n"
            "  [dim]3.[/dim] Pick benchmark scenarios",
            title="[bold white]BuyerBench — Session Configuration[/bold white]",
            border_style="cyan",
        )
    )
    console.print()

    # ── Step 1: Model selection ───────────────────────────────────────────────
    console.rule("[bold cyan]Step 1/3 — Select Models[/bold cyan]")
    console.print()
    selected_agent_ids = interactive_select()

    # ── Step 2: Skill modes ───────────────────────────────────────────────────
    console.print()
    console.rule("[bold cyan]Step 2/3 — Configure Skills[/bold cyan]")
    console.print()
    skill_modes = interactive_skill_select(selected_agent_ids)

    # ── Step 3: Scenario selection ────────────────────────────────────────────
    console.print()
    console.rule("[bold cyan]Step 3/3 — Select Scenarios[/bold cyan]")
    console.print()
    scenarios = load_all_scenarios("scenarios/")
    selected_scenario_ids = interactive_scenario_select(scenarios)

    # ── Build SessionConfig ───────────────────────────────────────────────────
    agents = [
        AgentSlot(agent_id=aid, skill_mode=skill_modes[aid])
        for aid in selected_agent_ids
    ]
    config = SessionConfig(
        agents=agents,
        scenario_ids=selected_scenario_ids,
        created_at=datetime.now(timezone.utc).isoformat(),
    )

    # ── Summary panel ─────────────────────────────────────────────────────────
    agent_lines = "\n".join(
        f"  • [bold]{slot.agent_id}[/bold] ([cyan]{slot.skill_mode}[/cyan])"
        for slot in config.agents
    )
    selected_set = set(selected_scenario_ids)
    pillar_vals: set[str] = set()
    for s in scenarios:
        if s.id in selected_set:
            pv = s.pillar.value if hasattr(s.pillar, "value") else str(s.pillar)
            pillar_vals.add(pv.replace("PILLAR", "P"))
    pillars_str = ", ".join(sorted(pillar_vals)) if pillar_vals else "none"

    summary = (
        f"{agent_lines}\n\n"
        f"[dim]Scenarios: [bold]{len(selected_scenario_ids)}[/bold]  "
        f"Pillars covered: [bold]{pillars_str}[/bold][/dim]"
    )
    console.print()
    console.print(
        Panel(
            summary,
            title="[bold green]Session Configuration Complete[/bold green]",
            border_style="green",
        )
    )
    console.print()

    return config


def _slugify(text: str) -> str:
    """Convert arbitrary text to a lowercase hyphen-slug (no spaces or special chars)."""
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9\-]", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-") or "session"


def _make_session_path(experiment_name: str, created_at: str) -> Path:
    """Compute the canonical session directory: sessions/<name>-<YYYYMMDD-HHMMSS>."""
    slug = experiment_name or "session"
    # created_at is ISO-8601 e.g. "2026-04-09T12:00:00+00:00"
    ts = created_at[:19].replace("-", "").replace("T", "-").replace(":", "")
    return Path("sessions") / f"{slug}-{ts}"


_RECURRENCE_OPTIONS = [
    ("One-shot (run once now)", None),
    ("Daily at 09:00        →  cron: 0 9 * * *", "0 9 * * *"),
    ("Weekly on Monday      →  cron: 0 9 * * 1", "0 9 * * 1"),
    ("Custom cron expression", "__custom__"),
]


def wizard_new_session(prefill: "Optional[SessionConfig]" = None) -> "SessionConfig":
    """Run the full 6-step researcher wizard for configuring a new BuyerBench session.

    Steps
    -----
    1. Experiment Identity  — experiment name (slugified) + research objective
    2. Model Selection      — call :func:`interactive_select`
    3. Skill Mode           — call :func:`interactive_skill_select`
    4. Scenario Scope       — call :func:`interactive_scenario_select`
    5. Recurrence           — one-shot or cron schedule
    6. Research Notes       — free-text notes for the academic report generator

    After all steps a confirmation Panel is shown. On confirm the config is saved to
    ``sessions/<experiment_name>-<timestamp>/session-config.yaml`` and returned.

    Parameters
    ----------
    prefill:
        Optional existing :class:`SessionConfig` to pre-populate wizard defaults.
        When provided, Step 1 and Step 6 prompts use values from this config as
        defaults, and Steps 2–4 offer a "keep existing" shortcut.

    Returns
    -------
    SessionConfig
        Fully populated session configuration.
    """
    from harness.loader import load_all_scenarios

    console.print()
    console.print(
        Panel(
            "[bold cyan]Enhanced Researcher Wizard — 6 guided steps[/bold cyan]\n"
            "[dim]Name your experiment, select models & scenarios, set a schedule, "
            "and annotate hypotheses for the academic report.[/dim]",
            title="[bold white]BuyerBench — New Session Wizard[/bold white]",
            border_style="cyan",
        )
    )
    console.print()

    # ── Step 1: Experiment Identity ───────────────────────────────────────────
    console.rule("[bold cyan][Step 1/6] Experiment Identity[/bold cyan]")
    console.print()
    raw_name = Prompt.ask(
        "[bold]Experiment name[/bold] [dim](e.g. gpt4o-vs-claude-p2)[/dim]",
        default=prefill.experiment_name if prefill else "my-experiment",
    )
    experiment_name = _slugify(raw_name)
    if experiment_name != raw_name.strip():
        console.print(f"[dim]Slugified to: [bold]{experiment_name}[/bold][/dim]")
    research_objective = Prompt.ask(
        "[bold]Research objective[/bold] [dim](free text, leave blank to skip)[/dim]",
        default=prefill.research_objective if prefill else "",
    )

    # ── Step 2: Model Selection ───────────────────────────────────────────────
    console.print()
    console.rule("[bold cyan][Step 2/6] Model Selection[/bold cyan]")
    console.print()
    if prefill and prefill.agents:
        console.print(
            "[dim]Pre-filled from existing session — press Enter to keep, or re-select[/dim]"
        )
        keep_models = Prompt.ask(
            "Keep existing model selections?", choices=["y", "n"], default="y"
        )
        if keep_models == "y":
            selected_agent_ids = [slot.agent_id for slot in prefill.agents]
        else:
            selected_agent_ids = interactive_select()
    else:
        selected_agent_ids = interactive_select()

    # ── Step 3: Skill Mode ────────────────────────────────────────────────────
    console.print()
    console.rule("[bold cyan][Step 3/6] Skill Mode[/bold cyan]")
    console.print()
    if prefill and prefill.agents:
        console.print(
            "[dim]Pre-filled from existing session — press Enter to keep, or re-select[/dim]"
        )
        keep_skills = Prompt.ask(
            "Keep existing skill modes?", choices=["y", "n"], default="y"
        )
        if keep_skills == "y":
            skill_modes = {slot.agent_id: slot.skill_mode for slot in prefill.agents}
            # Ensure all selected agents have a mode (may differ from prefill if re-selected)
            for aid in selected_agent_ids:
                if aid not in skill_modes:
                    skill_modes[aid] = "baseline"
        else:
            skill_modes = interactive_skill_select(selected_agent_ids)
    else:
        skill_modes = interactive_skill_select(selected_agent_ids)

    # ── Step 4: Scenario Scope ────────────────────────────────────────────────
    console.print()
    console.rule("[bold cyan][Step 4/6] Scenario Scope[/bold cyan]")
    console.print()
    scenarios = load_all_scenarios("scenarios/")
    if prefill and prefill.scenario_ids:
        console.print(
            "[dim]Pre-filled from existing session — press Enter to keep, or re-select[/dim]"
        )
        keep_scenarios = Prompt.ask(
            "Keep existing scenario selections?", choices=["y", "n"], default="y"
        )
        if keep_scenarios == "y":
            selected_scenario_ids = list(prefill.scenario_ids)
        else:
            selected_scenario_ids = interactive_scenario_select(scenarios)
    else:
        selected_scenario_ids = interactive_scenario_select(scenarios)

    # ── Step 5: Recurrence ────────────────────────────────────────────────────
    console.print()
    console.rule("[bold cyan][Step 5/6] Recurrence[/bold cyan]")
    console.print()
    for i, (label, _) in enumerate(_RECURRENCE_OPTIONS, start=1):
        console.print(f"  [dim][{i}][/dim] {label}")
    console.print()
    rec_choice = Prompt.ask(
        "[bold]Schedule[/bold]", choices=["1", "2", "3", "4"], default="1"
    )
    if rec_choice == "4":
        recurrence: Optional[str] = Prompt.ask(
            "[bold]Enter cron expression[/bold]"
        ).strip() or None
    else:
        recurrence = _RECURRENCE_OPTIONS[int(rec_choice) - 1][1]

    # ── Step 6: Research Notes ────────────────────────────────────────────────
    console.print()
    console.rule("[bold cyan][Step 6/6] Research Notes[/bold cyan]")
    console.print()
    research_notes = Prompt.ask(
        "[bold]Notes for academic paper generator[/bold] [dim][leave blank to skip][/dim]",
        default=prefill.research_notes if prefill else "",
    )

    # ── Build config ──────────────────────────────────────────────────────────
    created_at = datetime.now(timezone.utc).isoformat()
    agents = [
        AgentSlot(agent_id=aid, skill_mode=skill_modes[aid])
        for aid in selected_agent_ids
    ]
    config = SessionConfig(
        agents=agents,
        scenario_ids=selected_scenario_ids,
        created_at=created_at,
        experiment_name=experiment_name,
        research_objective=research_objective,
        research_notes=research_notes,
        recurrence=recurrence,
    )

    # ── Confirmation summary ──────────────────────────────────────────────────
    rec_display = recurrence if recurrence else "one-shot"
    summary_lines = [
        f"[bold]Experiment:[/bold]  {experiment_name}",
        f"[bold]Models:[/bold]      {len(agents)} agent(s)",
        f"[bold]Scenarios:[/bold]   {len(selected_scenario_ids)} selected",
        f"[bold]Skill modes:[/bold] "
        + ", ".join(f"{slot.agent_id}={slot.skill_mode}" for slot in agents),
        f"[bold]Recurrence:[/bold] {rec_display}",
        f"[bold]Has notes:[/bold]  {'yes' if research_notes else 'no'}",
    ]
    if research_objective:
        summary_lines.insert(1, f"[bold]Objective:[/bold]   {research_objective}")

    console.print()
    console.print(
        Panel(
            "\n".join(summary_lines),
            title="[bold yellow]Session Summary[/bold yellow]",
            border_style="yellow",
        )
    )
    console.print()

    confirm = Prompt.ask(
        "Confirm and save?", choices=["y", "n"], default="n"
    ).strip().lower()
    if confirm != "y":
        console.print("[yellow]Session not saved.[/yellow]")
        raise SystemExit(0)

    # ── Save ──────────────────────────────────────────────────────────────────
    session_dir = _make_session_path(experiment_name, created_at)
    config_path = session_dir / "session-config.yaml"
    save_session_config(config, str(config_path))
    console.print(f"\n[bold green]Session saved:[/bold green] [cyan]{config_path}[/cyan]")

    return config


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
