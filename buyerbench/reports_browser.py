"""Reports & Papers browser — scan results/ for experiment directories.

Public API
----------
browse_reports()   — Rich table of experiments; sub-menu for dashboard / report / paper / review
"""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.text import Text
from rich import box

console = Console(highlight=False)

_RESULTS_ROOT = Path(__file__).parent.parent / "results"

# ── Indicators ───────────────────────────────────────────────────────────────

_CHECK = Text("✓", style="bold green")
_DASH = Text("—", style="dim")


def _indicator(present: bool) -> Text:
    return _CHECK if present else _DASH


# ── Metadata helpers ──────────────────────────────────────────────────────────


def _find_experiment_dirs(results_root: Path) -> list[Path]:
    """Return directories that directly contain at least one .json result file.

    Scans immediate children of results_root, plus immediate children of
    results_root/experiments/ to cover the grouped layout.
    """
    candidates: list[Path] = []

    if not results_root.exists():
        return candidates

    grouped = results_root / "experiments"
    # Directories treated as grouping containers — excluded from experiment list
    grouping_dirs: set[Path] = set()
    if grouped.is_dir():
        grouping_dirs.add(grouped)

    search_roots = [results_root]
    if grouped.is_dir():
        search_roots.append(grouped)

    for root in search_roots:
        for child in sorted(root.iterdir()):
            if not child.is_dir():
                continue
            if child in grouping_dirs:
                continue
            if any(child.glob("*.json")):
                candidates.append(child)

    # Deduplicate while preserving order
    seen: set[Path] = set()
    deduped: list[Path] = []
    for p in candidates:
        if p not in seen:
            seen.add(p)
            deduped.append(p)

    return deduped


def _collect_metadata(exp_dir: Path) -> dict:
    """Read all JSON files in exp_dir and extract experiment metadata."""
    json_files = sorted(exp_dir.glob("*.json"))

    agent_ids: set[str] = set()
    pillars_present: set[str] = set()
    latest_mtime: float = exp_dir.stat().st_mtime

    for jf in json_files:
        mtime = jf.stat().st_mtime
        if mtime > latest_mtime:
            latest_mtime = mtime
        try:
            data = json.loads(jf.read_text())
        except (json.JSONDecodeError, OSError):
            continue
        if data.get("status") == "skipped":
            continue
        agent_id = data.get("agent_id")
        if agent_id:
            agent_ids.add(agent_id)
        for ps in data.get("pillar_scores", []):
            pillar = ps.get("pillar", "")
            if pillar:
                pillars_present.add(pillar)

    date_str = datetime.fromtimestamp(latest_mtime).strftime("%Y-%m-%d")

    # Normalise pillar labels to p1/p2/p3 for display
    pillar_display_parts = []
    for label in ("PILLAR1", "PILLAR2", "PILLAR3"):
        short = label.replace("PILLAR", "p")
        if label in pillars_present:
            pillar_display_parts.append(f"[green]{short}[/green]")
        else:
            pillar_display_parts.append(f"[dim]{short}[/dim]")
    pillar_display = " ".join(pillar_display_parts)

    # Report / paper / review presence
    has_report = (exp_dir / "FULL-REPORT.md").exists()
    has_paper = bool(
        list(exp_dir.glob("ACADEMIC-PAPER.md"))
        + list(exp_dir.glob("academic-report*.md"))
    )
    has_review = (exp_dir / "REVIEW.md").exists()

    return {
        "date": date_str,
        "agent_ids": agent_ids,
        "pillar_display": pillar_display,
        "has_report": has_report,
        "has_paper": has_paper,
        "has_review": has_review,
    }


# ── Sub-menu helpers ──────────────────────────────────────────────────────────


def _open_markdown(path: Path) -> None:
    """Print a Markdown file with Rich rendering."""
    console.print(Markdown(path.read_text(encoding="utf-8")))


def _find_academic_paper(exp_dir: Path) -> Optional[Path]:
    candidates = list(exp_dir.glob("ACADEMIC-PAPER.md")) + list(
        exp_dir.glob("academic-report*.md")
    )
    return candidates[0] if candidates else None


def _run_submenu(exp_dir: Path) -> None:
    """Interactive sub-menu for a selected experiment directory."""
    while True:
        console.print()
        console.print(
            Panel(
                f"[bold]Experiment:[/bold] {exp_dir.name}\n"
                f"[bold]Path:[/bold]       {exp_dir}\n\n"
                f"  [bold cyan][d][/bold cyan]  TUI Dashboard         (interactive results viewer)\n"
                f"  [bold cyan][r][/bold cyan]  Generate / View Report     (FULL-REPORT.md)\n"
                f"  [bold cyan][a][/bold cyan]  Generate / View Academic Paper\n"
                f"  [bold cyan][v][/bold cyan]  Generate / View AI Review\n"
                f"  [bold cyan][b][/bold cyan]  Back",
                title="[bold white]Experiment Actions[/bold white]",
                border_style="cyan",
            )
        )

        action = Prompt.ask("Action", choices=["d", "r", "a", "v", "b"], show_choices=False)

        if action == "d":
            from buyerbench.dashboard import ResultsDashboard

            dashboard = ResultsDashboard(str(exp_dir))
            dashboard.run()

        elif action == "r":
            report_path = exp_dir / "FULL-REPORT.md"
            if report_path.exists():
                _open_markdown(report_path)
            else:
                console.print("[dim]Generating report…[/dim]")
                subprocess.run(
                    [sys.executable, "-m", "buyerbench", "report", "--experiment-dir", str(exp_dir)]
                )
                if report_path.exists():
                    _open_markdown(report_path)

        elif action == "a":
            paper_path = _find_academic_paper(exp_dir)
            if paper_path:
                _open_markdown(paper_path)
            else:
                console.print("[dim]Generating academic paper…[/dim]")
                subprocess.run(
                    [
                        sys.executable,
                        "-m",
                        "buyerbench",
                        "academic-report",
                        "--experiment-dir",
                        str(exp_dir),
                    ]
                )
                paper_path = _find_academic_paper(exp_dir)
                if paper_path:
                    _open_markdown(paper_path)

        elif action == "v":
            review_path = exp_dir / "REVIEW.md"
            if review_path.exists():
                _open_markdown(review_path)
            else:
                console.print("[dim]Generating AI review…[/dim]")
                subprocess.run(
                    [sys.executable, "-m", "buyerbench", "review", "--experiment-dir", str(exp_dir)]
                )
                if review_path.exists():
                    _open_markdown(review_path)

        elif action == "b":
            return


# ── Main entry point ──────────────────────────────────────────────────────────


def browse_reports() -> None:
    """Scan results/ for experiment directories and present an interactive browser.

    Displays a Rich table with coverage metadata, then routes the researcher to
    a sub-menu for launching the TUI dashboard, generating/viewing reports, the
    academic paper, or the AI review.
    """
    console.print()

    exp_dirs = _find_experiment_dirs(_RESULTS_ROOT)

    if not exp_dirs:
        console.print(
            "[dim]No experiments found. Run a benchmark with "
            "[bold cyan][1] New Session[/bold cyan] first.[/dim]"
        )
        return

    # Collect metadata for each experiment directory
    rows: list[tuple[Path, dict]] = []
    for exp_dir in exp_dirs:
        meta = _collect_metadata(exp_dir)
        rows.append((exp_dir, meta))

    # ── Build table ───────────────────────────────────────────────────────────
    t = Table(
        title="[bold cyan]BuyerBench — Reports & Papers[/bold cyan]",
        box=box.ROUNDED,
        show_lines=True,
        highlight=False,
    )
    t.add_column("#", style="dim", justify="right", no_wrap=True)
    t.add_column("Experiment", style="bold", no_wrap=True)
    t.add_column("Date", style="cyan", no_wrap=True)
    t.add_column("Agents", justify="right")
    t.add_column("Pillars", no_wrap=True)
    t.add_column("Report", justify="center")
    t.add_column("Paper", justify="center")
    t.add_column("Review", justify="center")

    for idx, (exp_dir, meta) in enumerate(rows, start=1):
        t.add_row(
            str(idx),
            exp_dir.name,
            meta["date"],
            str(len(meta["agent_ids"])),
            meta["pillar_display"],
            _indicator(meta["has_report"]),
            _indicator(meta["has_paper"]),
            _indicator(meta["has_review"]),
        )

    console.print(t)
    console.print()

    # ── Selection prompt ──────────────────────────────────────────────────────
    valid_choices = [str(i) for i in range(1, len(rows) + 1)] + ["q"]
    raw = Prompt.ask(
        f"Select experiment [1-{len(rows)}] or [q] back",
        choices=valid_choices,
        show_choices=False,
    )

    if raw.lower() == "q":
        return

    selected_idx = int(raw) - 1
    selected_dir, _ = rows[selected_idx]

    _run_submenu(selected_dir)
