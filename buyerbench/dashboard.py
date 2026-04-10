"""Interactive terminal dashboard for browsing BuyerBench benchmark results."""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

import rich.box
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table


class ResultsDashboard:
    """Load results from a directory and render navigable Rich TUI panels."""

    def __init__(self, results_dir: str) -> None:
        self.results_dir = Path(results_dir)
        self.results: list[dict] = self._load_results(self.results_dir)
        self._agg: dict = self._aggregate()
        self.agents: list[str] = sorted(self._agg.keys())
        self.pillars: list[int] = [1, 2, 3]

    def _load_results(self, results_dir: Path) -> list[dict]:
        """Load all non-skipped scenario result JSONs from results_dir."""
        results = []
        for path in sorted(results_dir.rglob("*.json")):
            try:
                data = json.loads(path.read_text())
            except (json.JSONDecodeError, OSError):
                continue
            if data.get("status") == "skipped":
                continue
            results.append(data)
        return results

    def _aggregate(self) -> dict:
        """Group results by agent_id; compute mean score per pillar, overall mean, pass rate."""
        agent_pillar_scores: dict[str, dict[str, list[float]]] = defaultdict(
            lambda: defaultdict(list)
        )
        agent_pass: dict[str, list[bool]] = defaultdict(list)

        for r in self.results:
            agent_id = r.get("agent_id", "unknown")
            for ps in r.get("pillar_scores", []):
                pillar = ps.get("pillar", "")
                score = ps.get("score")
                if score is not None:
                    agent_pillar_scores[agent_id][pillar].append(float(score))
            agent_pass[agent_id].append(bool(r.get("overall_pass", False)))

        result: dict[str, dict] = {}
        for agent_id in agent_pillar_scores:
            all_scores: list[float] = []
            pillar_means: dict[str, float | None] = {}
            for pillar_name, scores in agent_pillar_scores[agent_id].items():
                pillar_means[pillar_name] = sum(scores) / len(scores) if scores else None
                all_scores.extend(scores)
            passes = agent_pass[agent_id]
            result[agent_id] = {
                "pillar_means": pillar_means,
                "overall_mean": sum(all_scores) / len(all_scores) if all_scores else None,
                "pass_rate": sum(passes) / len(passes) if passes else 0.0,
                "n": len(passes),
            }
        return result

    def _to_eval_results(self) -> list:
        """Convert raw result dicts to EvaluationResult objects for academic_tables renderers."""
        from buyerbench.models import EvaluationResult

        out = []
        for raw in self.results:
            try:
                out.append(EvaluationResult.model_validate(raw))
            except Exception:
                continue
        return out

    def render_summary(self, console: Console) -> None:
        """Print a Rich Panel with session overview."""
        session_id = self.results_dir.name
        agent_count = len(self.agents)
        scenario_count = len(self.results)

        best_agent = "—"
        best_score = -1.0
        for agent_id, data in self._agg.items():
            score = data.get("overall_mean") or 0.0
            if score > best_score:
                best_score = score
                best_agent = agent_id

        total_passes = sum(int(r.get("overall_pass", False)) for r in self.results)
        overall_pass_rate = total_passes / scenario_count if scenario_count else 0.0

        lines = [
            f"[bold]Session:[/bold]   {session_id}",
            f"[bold]Agents:[/bold]    {agent_count}  ({', '.join(self.agents) or '—'})",
            f"[bold]Scenarios:[/bold] {scenario_count}",
            f"[bold]Pass rate:[/bold] {overall_pass_rate:.1%}  ({total_passes}/{scenario_count})",
            f"[bold]Best agent:[/bold] {best_agent} ({best_score:.2f})",
        ]
        console.print()
        console.print(
            Panel(
                "\n".join(lines),
                title="[bold green]BuyerBench Session Summary[/bold green]",
                border_style="green",
            )
        )
        console.print()

    def render_comparison(self, console: Console) -> None:
        """Print academic-style model comparison table (agent × pillar)."""
        from results.academic_tables import render_model_comparison_table

        render_model_comparison_table(self._to_eval_results(), console)

    def render_scenarios(self, console: Console, pillar_filter: int | None = None) -> None:
        """Print per-scenario breakdown. Pass pillar_filter=1/2/3 to narrow to one pillar."""
        from results.academic_tables import render_pillar_breakdown_table

        eval_results = self._to_eval_results()
        pillars = [pillar_filter] if pillar_filter else [1, 2, 3]
        for p in pillars:
            render_pillar_breakdown_table(eval_results, p, console)

    def run(self) -> None:
        """Launch the interactive dashboard loop for this results directory."""
        run_dashboard(str(self.results_dir))

    def render_bias_security(self, console: Console) -> None:
        """Print Pillar 2 bias table followed by a compact Pillar 3 security summary."""
        from results.academic_tables import render_bias_table

        render_bias_table(self._to_eval_results(), console)

        # Compact security summary: agent → compliance_rate, violation_count
        agent_compliance: dict[str, list[float]] = defaultdict(list)
        agent_violations: dict[str, int] = defaultdict(int)
        for r in self.results:
            agent_id = r.get("agent_id", "unknown")
            for ps in r.get("pillar_scores", []):
                if ps.get("pillar") == "PILLAR3":
                    metrics = ps.get("metrics", {})
                    compliance = metrics.get("compliance_adherence_rate")
                    if compliance is not None:
                        agent_compliance[agent_id].append(float(compliance))
                    agent_violations[agent_id] += len(ps.get("violations", []))

        t = Table(
            title="[bold]Pillar 3 — Security / Compliance Summary[/bold]",
            box=rich.box.HEAVY_HEAD,
            show_lines=True,
        )
        t.add_column("Agent", style="bold cyan", no_wrap=True)
        t.add_column("Compliance Rate", justify="right")
        t.add_column("Violation Count", justify="right")

        all_p3_agents = sorted(
            set(list(agent_compliance.keys()) + list(agent_violations.keys()))
        )
        if all_p3_agents:
            for agent_id in all_p3_agents:
                rates = agent_compliance.get(agent_id, [])
                mean_rate: float | None = sum(rates) / len(rates) if rates else None
                vcount = agent_violations.get(agent_id, 0)

                if mean_rate is None:
                    rate_cell = "[dim]—[/dim]"
                elif mean_rate >= 0.8:
                    rate_cell = f"[bold green]{mean_rate:.2f}[/bold green]"
                elif mean_rate >= 0.5:
                    rate_cell = f"[yellow]{mean_rate:.2f}[/yellow]"
                else:
                    rate_cell = f"[bold red]{mean_rate:.2f}[/bold red]"

                vcount_cell = (
                    f"[bold red]{vcount}[/bold red]" if vcount > 0 else f"[green]{vcount}[/green]"
                )
                t.add_row(agent_id, rate_cell, vcount_cell)
        else:
            t.add_row("[dim]—[/dim]", "[dim]—[/dim]", "[dim]—[/dim]")

        console.print()
        console.print(t)
        console.print()


_HELP_BAR = (
    "[bold cyan][1][/bold cyan] Summary  "
    "[bold cyan][2][/bold cyan] Comparison  "
    "[bold cyan][3][/bold cyan] Scenarios  "
    "[bold cyan][4][/bold cyan] Bias/Security  "
    "[bold cyan][p1/p2/p3][/bold cyan] Filter  "
    "[bold cyan][q][/bold cyan] Quit"
)


def run_dashboard(results_dir: str) -> None:
    """Launch the interactive BuyerBench results dashboard."""
    console = Console()
    dashboard = ResultsDashboard(results_dir)

    console.print()
    console.print(_HELP_BAR)
    console.print()

    dashboard.render_summary(console)

    while True:
        try:
            cmd = Prompt.ask("[bold cyan]>[/bold cyan]", default="").strip().lower()
        except (EOFError, KeyboardInterrupt):
            break

        console.clear()
        if cmd == "1":
            dashboard.render_summary(console)
        elif cmd == "2":
            dashboard.render_comparison(console)
        elif cmd == "3":
            dashboard.render_scenarios(console)
        elif cmd in ("p1", "p2", "p3"):
            dashboard.render_scenarios(console, pillar_filter=int(cmd[1]))
        elif cmd == "4":
            dashboard.render_bias_security(console)
        elif cmd in ("q", "quit"):
            break
        else:
            console.print(_HELP_BAR)
