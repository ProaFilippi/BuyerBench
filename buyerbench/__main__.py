from __future__ import annotations

import os
import sys
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table
from rich import box

console = Console(highlight=False)


def _stdin_is_tty() -> bool:
    """Return True when stdin is an interactive terminal. Extracted for testability."""
    return sys.stdin.isatty()


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx: click.Context) -> None:
    """BuyerBench — benchmark framework for AI buyer agents."""
    if ctx.invoked_subcommand is None:
        from buyerbench.home import home_tui

        home_tui()


@cli.command()
def check() -> None:
    """Verify CLI tools, API keys, and mock MCP server are available."""
    from harness.preflight import check_environment

    env = check_environment(print_report=True)
    raise SystemExit(0 if env["overall"] else 1)


@cli.command()
def demo() -> None:
    """Load the 3 sample scenarios, run MockAgent, and print a rich report."""
    from agents.mock import MockAgent
    from evaluators.aggregate import run_evaluation
    from harness.loader import load_all_scenarios

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
        response = agent.respond(scenario)
        result = run_evaluation(scenario, response)
        pillar_score = result.pillar_scores[0]

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
        f"[bold green]BuyerBench demo complete — {len(scenarios)} scenarios evaluated.[/bold green]"
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
@click.option("--output", default="session-selection.yaml", show_default=True, help="Path to save the selection YAML")
@click.option("--filter-tag", default=None, help="Pre-filter catalog by capability tag")
@click.option("--filter-provider", default=None, help="Pre-filter catalog by provider name")
def select(output: str, filter_tag: str | None, filter_provider: str | None) -> None:
    """Interactively choose which OpenRouter models to benchmark and save the selection."""
    from rich.panel import Panel

    from buyerbench.model_catalog import filter_catalog, MODEL_CATALOG
    from buyerbench.selector import interactive_select, save_selection

    if not _stdin_is_tty():
        console.print("[red]Error: 'select' requires an interactive terminal (TTY).[/red]")
        raise SystemExit(1)

    catalog = MODEL_CATALOG[:]
    if filter_tag or filter_provider:
        catalog = filter_catalog(
            tags=[filter_tag] if filter_tag else None,
            providers=[filter_provider] if filter_provider else None,
        )
        if not catalog:
            console.print("[yellow]No models matched the supplied filters.[/yellow]")
            raise SystemExit(1)

    selected = interactive_select(catalog)
    save_selection(selected, output)

    names = []
    from buyerbench.model_catalog import MODEL_CATALOG as _MC
    id_to_name = {e.agent_id: e.display_name for e in _MC}
    for aid in selected:
        names.append(f"  • {id_to_name.get(aid, aid)}")

    console.print()
    console.print(
        Panel(
            "\n".join(names) + f"\n\n[dim]Saved to: [bold]{output}[/bold][/dim]",
            title=f"[bold green]Selection saved — {len(selected)} model(s)[/bold green]",
            border_style="green",
        )
    )
    console.print()


@cli.command()
@click.option(
    "--agent",
    default=None,
    help='Agent ID to evaluate (e.g. claude-code-baseline) or "all" for all real agents.',
)
@click.option("--from-selection", "from_selection", default=None, metavar="PATH",
              help="Path to a session-selection.yaml produced by 'buyerbench select'")
@click.option("--from-session", "from_session", default=None, metavar="PATH",
              help="Path to a session-config.yaml produced by 'buyerbench session'")
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
@click.option(
    "--academic-report/--no-academic-report",
    default=False,
    show_default=True,
    help="Generate an academic paper after the run via Claude CLI",
)
@click.option(
    "--test-context",
    "test_context",
    default=None,
    help="Experiment description injected into the academic report §4 (used with --academic-report)",
)
@click.option(
    "--dashboard/--no-dashboard",
    default=False,
    show_default=True,
    help="Launch interactive results dashboard after the run",
)
@click.option(
    "--n-runs",
    "n_runs",
    default=1,
    show_default=True,
    type=click.IntRange(min=1),
    help="Number of independent runs per (agent, scenario) cell for statistical analysis.",
)
@click.option(
    "--temperature",
    "temperature",
    default=None,
    type=float,
    help="Sampling temperature passed to the model (0.0–1.0). Omit to use provider default.",
)
@click.option(
    "--research-mode",
    "research_mode",
    is_flag=True,
    default=False,
    help=(
        "Add a mandatory temperature=0.0 robustness pass saved to "
        "<output-dir>/robustness-t0/. "
        "Flags if BSI collapses at T=0.0 (stochastic artifact warning, per G.6)."
    ),
)
@click.option(
    "--prompt-version",
    "prompt_version",
    default="standard",
    show_default=True,
    type=click.Choice(["standard", "cot", "expert_role"]),
    help=(
        "Prompt framing variant: 'standard' (default), 'cot' (chain-of-thought prefix), "
        "or 'expert_role' (senior-procurement-officer identity prefix)."
    ),
)
@click.option(
    "--supplier-order-seed",
    "supplier_order_seed",
    default=None,
    type=int,
    help=(
        "Base seed for supplier ordering across all runs. "
        "Per-run seeds are derived via HMAC-SHA256(base_seed, scenario_id|variant|run_index), "
        "making the full experiment reproducible from this single integer. "
        "Omit to use a fresh random seed per run (default, recommended for production experiments)."
    ),
)
@click.option(
    "--supplier-order-static",
    "supplier_order_static",
    is_flag=True,
    default=False,
    help=(
        "Present suppliers in their original YAML order — no randomisation. "
        "Useful for debugging or comparing runs that must see identical supplier ordering. "
        "Overrides --supplier-order-seed when both are supplied."
    ),
)
def run(
    agent: str | None,
    from_selection: str | None,
    from_session: str | None,
    scenario: str | None,
    pillar: str | None,
    dry_run: bool,
    output_dir: str,
    academic_report: bool,
    test_context: str | None,
    dashboard: bool,
    n_runs: int,
    temperature: float | None,
    research_mode: bool,
    prompt_version: str,
    supplier_order_seed: int | None,
    supplier_order_static: bool,
) -> None:
    """Run the benchmark suite against a named CLI agent (or all agents)."""
    import json
    from datetime import datetime, timezone
    from pathlib import Path

    from agents.registry import AGENT_REGISTRY, get_agent
    from harness.config import load_config
    from harness.loader import load_all_scenarios
    from harness.runner import run_scenario

    # ── Validate mutually exclusive options ───────────────────────────────────
    exclusive_count = sum(bool(x) for x in [agent, from_selection, from_session])
    if exclusive_count > 1:
        console.print(
            "[red]--agent, --from-selection, and --from-session are mutually exclusive.[/red]\n"
            "Use exactly one."
        )
        raise SystemExit(1)

    if exclusive_count == 0:
        console.print(
            "[red]Provide one of --agent <id>, --from-selection <path>, or --from-session <path>.[/red]"
        )
        raise SystemExit(1)

    # ── Resolve agent list ────────────────────────────────────────────────────
    _REAL_AGENTS = [aid for aid in AGENT_REGISTRY if aid != "mock-agent-v1"]

    # Maps agent_id -> skill system prompt (empty = no injection)
    skill_prompts_by_agent: dict[str, str] = {}
    # Scenario IDs from session config (empty = no extra filter)
    session_scenario_ids: list[str] = []

    if from_session:
        import shutil
        from buyerbench.selector import load_session_config
        from buyerbench.skills import get_skill_prompt

        sess_cfg = load_session_config(from_session)
        if not sess_cfg.agents:
            console.print(f"[red]No agents found in session config: {from_session}[/red]")
            raise SystemExit(1)

        selected_ids = [slot.agent_id for slot in sess_cfg.agents]
        unknown = [aid for aid in selected_ids if aid not in AGENT_REGISTRY]
        if unknown:
            console.print(f"[red]Unknown agent IDs in session config: {', '.join(unknown)}[/red]")
            raise SystemExit(1)

        for slot in sess_cfg.agents:
            skill_prompts_by_agent[slot.agent_id] = get_skill_prompt(slot.skill_mode)

        session_scenario_ids = sess_cfg.scenario_ids

        lines = "\n".join(
            f"  • [bold]{slot.agent_id}[/bold] ([cyan]{slot.skill_mode}[/cyan])"
            for slot in sess_cfg.agents
        )
        from rich.panel import Panel as _Panel
        console.print(
            _Panel(
                lines + f"\n\n[dim]Session file: [bold]{from_session}[/bold][/dim]",
                title=f"[bold cyan]Running {len(selected_ids)} agent(s) from session config[/bold cyan]",
                border_style="cyan",
            )
        )
        console.print()
        agents_to_run = [(aid, True) for aid in selected_ids]

    elif from_selection:
        from buyerbench.selector import load_selection
        from buyerbench.model_catalog import MODEL_CATALOG as _MC

        selected_ids = load_selection(from_selection)
        if not selected_ids:
            console.print(f"[red]No agents found in selection file: {from_selection}[/red]")
            raise SystemExit(1)

        unknown = [aid for aid in selected_ids if aid not in AGENT_REGISTRY]
        if unknown:
            console.print(f"[red]Unknown agent IDs in selection file: {', '.join(unknown)}[/red]")
            raise SystemExit(1)

        id_to_name = {e.agent_id: e.display_name for e in _MC}
        names_list = "\n".join(f"  • {id_to_name.get(a, a)}" for a in selected_ids)
        from rich.panel import Panel as _Panel
        console.print(
            _Panel(
                names_list + f"\n\n[dim]Selection file: [bold]{from_selection}[/bold][/dim]",
                title=f"[bold cyan]Running {len(selected_ids)} model(s) from saved selection[/bold cyan]",
                border_style="cyan",
            )
        )
        console.print()
        agents_to_run = [(aid, True) for aid in selected_ids]

    elif agent == "all":
        from harness.preflight import check_environment

        env = check_environment(print_report=True)
        available_set = set(env["available_agents"])
        agents_to_run = [(aid, aid in available_set) for aid in _REAL_AGENTS]
    else:
        if agent not in AGENT_REGISTRY:
            available = sorted(AGENT_REGISTRY.keys())
            console.print(
                f"[red]Unknown agent {agent!r}.[/red]\n"
                f"Available agents: {', '.join(available)}"
            )
            raise SystemExit(1)
        agents_to_run = [(agent, True)]

    # ── Load and filter scenarios ─────────────────────────────────────────────
    scenarios_root = Path(__file__).parent.parent / "scenarios"
    all_scenarios = load_all_scenarios(str(scenarios_root))

    # Apply session scenario filter first (if --from-session specified a list)
    if session_scenario_ids:
        session_set = set(session_scenario_ids)
        all_scenarios = [s for s in all_scenarios if s.id in session_set]

    if pillar:
        pillar_enum = f"PILLAR{pillar}"
        all_scenarios = [s for s in all_scenarios if s.pillar.value == pillar_enum]
    if scenario:
        all_scenarios = [s for s in all_scenarios if s.id == scenario]

    if not all_scenarios:
        console.print("[yellow]No scenarios matched the given filters.[/yellow]")
        return

    config = load_config()
    config["dry_run"] = dry_run
    if temperature is not None:
        config["temperature"] = temperature
    if prompt_version != "standard":
        config["prompt_version"] = prompt_version

    # Copy session config into output dir for provenance
    if from_session:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        import shutil as _shutil
        _shutil.copy2(from_session, Path(output_dir) / Path(from_session).name)

    started_at = datetime.now(timezone.utc)
    from results.session_export import generate_session_id
    session_id = generate_session_id()
    pillar_ints = [int(pillar)] if pillar else [1, 2, 3]

    # ── UPGRADE-11: Write frozen experiment manifest before execution ─────────
    _manifest = None
    if not dry_run:
        try:
            from results.experiment_manifest import create_manifest, write_manifest as _write_manifest
            Path(output_dir).mkdir(parents=True, exist_ok=True)
            _manifest = create_manifest(
                session_id=session_id,
                agents=[aid for aid, _ in agents_to_run],
                scenarios=all_scenarios,
                n_runs=n_runs,
                temperature=temperature,
                prompt_version=prompt_version,
                pillars=pillar_ints,
                research_mode=research_mode,
                output_dir=output_dir,
                started_at=started_at,
            )
            _write_manifest(_manifest, output_dir)
            console.print(
                f"[dim]Experiment manifest → "
                f"[bold]{output_dir}/experiment_manifest.json[/bold][/dim]"
            )
        except Exception as _e:
            console.print(f"[dim yellow]Manifest creation failed: {_e}[/dim yellow]")

    all_results: list = []

    # ── Run each agent ────────────────────────────────────────────────────────
    for agent_id, is_available in agents_to_run:
        if not is_available:
            _write_skipped_results(agent_id, all_scenarios, output_dir)
            console.print(
                f"[yellow]SKIPPED[/yellow] {agent_id} — CLI or API key unavailable"
            )
            continue

        agent_instance = get_agent(
            agent_id, config, skill_prompt=skill_prompts_by_agent.get(agent_id, "")
        )

        if dry_run:
            console.print(
                f"[bold cyan]DRY RUN[/bold cyan] — agent=[bold]{agent_id}[/bold]  "
                f"scenarios={len(all_scenarios)}"
            )
            for s in all_scenarios:
                agent_instance.respond(s)
            continue

        table = Table(
            title=f"BuyerBench Run — {agent_id}",
            box=box.ROUNDED,
            show_lines=True,
        )
        table.add_column("Scenario", style="bold cyan", no_wrap=True)
        table.add_column("Pillar", style="magenta")
        table.add_column("Score", justify="right")
        table.add_column("Status", justify="center")

        for s in all_scenarios:
            for run_idx in range(n_runs):
                # Derive a per-run seed from the base seed when one is provided,
                # so the full experiment is reproducible from a single integer while
                # each (scenario, run_index) cell still receives a distinct seed.
                from harness.runner import derive_seed as _derive_seed
                per_run_seed: int | None = (
                    _derive_seed(supplier_order_seed, s.id, s.variant, run_idx)
                    if supplier_order_seed is not None and not supplier_order_static
                    else None
                )
                result = run_scenario(
                    s, agent_instance, output_dir=output_dir, run_index=run_idx,
                    supplier_order_seed=per_run_seed,
                    supplier_order_static=supplier_order_static,
                )
                all_results.append(result)
                score = result.pillar_scores[0].score if result.pillar_scores else 0.0
                status = "[green]PASS[/green]" if result.overall_pass else "[red]FAIL[/red]"
                run_label = f"{s.title[:44]} [{run_idx+1}/{n_runs}]" if n_runs > 1 else s.title[:50]
                table.add_row(run_label, s.pillar.value, f"{score:.2f}", status)

        console.print()
        console.print(table)

    # ── Post-run: Pillar 2 BSI computation ───────────────────────────────────
    if pillar == "2":
        import json as _json
        from evaluators.aggregate import compute_bsi_from_experiment_dir

        bsi_summary = compute_bsi_from_experiment_dir(output_dir)
        bsi_path = Path(output_dir) / "bias-susceptibility-summary.json"
        bsi_path.write_text(_json.dumps(bsi_summary, indent=2, default=str))
        console.print(
            f"[bold cyan]BSI summary saved to[/bold cyan] "
            f"[bold]{bsi_path}[/bold]"
        )

        # UPGRADE-5: generate cell-level aggregates when N runs > 1
        if all_results and n_runs > 1:
            from results.aggregate_cells import aggregate_cells, write_cell_aggregates

            cell_report = aggregate_cells(all_results)
            cell_path = write_cell_aggregates(cell_report, output_dir)
            console.print(
                f"[bold cyan]Cell aggregates saved to[/bold cyan] "
                f"[bold]{cell_path}[/bold] "
                f"({cell_report.n_cells} cells, {cell_report.n_total_runs} runs)"
            )

    # ── Post-run: Pillar 3 security/compliance summary ────────────────────────
    if pillar == "3":
        import json as _json
        from evaluators.aggregate import compute_security_summary_from_experiment_dir

        sec_summary = compute_security_summary_from_experiment_dir(output_dir)
        sec_path = Path(output_dir) / "security-compliance-summary.json"
        sec_path.write_text(_json.dumps(sec_summary, indent=2, default=str))
        console.print(
            f"[bold cyan]Security/compliance summary saved to[/bold cyan] "
            f"[bold]{sec_path}[/bold]"
        )
        # Log injection resistance table explicitly — task requirement
        inj_table = sec_summary.get("injection_resistance_table", [])
        if inj_table:
            from rich.table import Table as RichTable
            from rich import box as rbox

            inj_t = RichTable(
                title="Prompt Injection Resistance (p3-05)",
                box=rbox.SIMPLE,
            )
            inj_t.add_column("Agent", style="bold cyan")
            inj_t.add_column("Injection Resisted", justify="center")
            inj_t.add_column("Flagged in Reasoning", justify="center")
            inj_t.add_column("Correct Supplier", justify="center")
            for row in inj_table:
                resisted = "[green]YES[/green]" if row["injected_instruction_not_followed"] else "[red]NO[/red]"
                flagged = "[green]YES[/green]" if row["injection_flagged_in_reasoning"] else "[yellow]NO[/yellow]"
                correct = "[green]YES[/green]" if row["correct_supplier_selected"] else "[red]NO[/red]"
                inj_t.add_row(row["agent_id"], resisted, flagged, correct)
            console.print()
            console.print(inj_t)
        else:
            console.print(
                "[dim]No prompt injection results to display "
                "(all agents skipped or no p3-05 results)[/dim]"
            )

    # ── Research mode: temperature=0.0 robustness pass (UPGRADE-6) ───────────
    robustness_results: list = []
    if research_mode and not dry_run and all_results:
        robustness_dir = str(Path(output_dir) / "robustness-t0")
        robustness_config = dict(config)
        robustness_config["temperature"] = 0.0

        console.print()
        console.print(
            "[bold yellow]Research Mode — Robustness Check (temperature=0.0)[/bold yellow]"
        )
        console.print(
            "[dim]Re-running all scenarios at T=0.0 to verify findings are not "
            "stochastic sampling artifacts (G.6 pre-specified check).[/dim]"
        )

        for agent_id, is_available in agents_to_run:
            if not is_available:
                continue

            rob_agent = get_agent(
                agent_id, robustness_config,
                skill_prompt=skill_prompts_by_agent.get(agent_id, "")
            )

            rob_table = Table(
                title=f"Robustness Check (T=0.0) — {agent_id}",
                box=box.ROUNDED,
                show_lines=True,
            )
            rob_table.add_column("Scenario", style="bold cyan", no_wrap=True)
            rob_table.add_column("Pillar", style="magenta")
            rob_table.add_column("Score", justify="right")
            rob_table.add_column("Status", justify="center")

            for s in all_scenarios:
                for run_idx in range(n_runs):
                    result = run_scenario(
                        s, rob_agent, output_dir=robustness_dir, run_index=run_idx
                    )
                    robustness_results.append(result)
                    score = result.pillar_scores[0].score if result.pillar_scores else 0.0
                    status = "[green]PASS[/green]" if result.overall_pass else "[red]FAIL[/red]"
                    run_label = (
                        f"{s.title[:44]} [{run_idx+1}/{n_runs}]" if n_runs > 1 else s.title[:50]
                    )
                    rob_table.add_row(run_label, s.pillar.value, f"{score:.2f}", status)

            console.print()
            console.print(rob_table)

        # Pillar 2 post-processing for robustness pass
        if pillar == "2" and robustness_results:
            import json as _json2
            from evaluators.aggregate import compute_bsi_from_experiment_dir

            rob_bsi = compute_bsi_from_experiment_dir(robustness_dir)
            rob_bsi_path = Path(robustness_dir) / "bias-susceptibility-summary.json"
            rob_bsi_path.write_text(_json2.dumps(rob_bsi, indent=2, default=str))
            console.print(
                f"[bold cyan]Robustness BSI summary →[/bold cyan] [bold]{rob_bsi_path}[/bold]"
            )

            if n_runs > 1:
                from results.aggregate_cells import aggregate_cells, write_cell_aggregates

                rob_cell_report = aggregate_cells(robustness_results)
                rob_cell_path = write_cell_aggregates(rob_cell_report, robustness_dir)
                console.print(
                    f"[bold cyan]Robustness cell aggregates →[/bold cyan] "
                    f"[bold]{rob_cell_path}[/bold] "
                    f"({rob_cell_report.n_cells} cells, {rob_cell_report.n_total_runs} runs)"
                )

        # BSI collapse detection (G.6 warning)
        if pillar == "2":
            _print_robustness_bsi_comparison(all_results, robustness_results, console)

    # ── Post-run: Academic tables + session export ────────────────────────────
    if all_results and not dry_run:
        from results.academic_tables import (
            render_model_comparison_table,
            render_pillar_breakdown_table,
            render_session_summary_panel,
        )
        from results.session_export import (
            SessionMetadata,
            export_session_csv,
            export_session_markdown,
        )

        completed_at = datetime.now(timezone.utc)
        agent_ids = [aid for aid, _ in agents_to_run]

        # ── UPGRADE-11: Finalize experiment manifest with completion data ─────
        if _manifest is not None:
            try:
                from results.experiment_manifest import (
                    finalize_manifest,
                    write_manifest as _write_manifest_final,
                )
                _manifest = finalize_manifest(_manifest, all_results, completed_at)
                _write_manifest_final(_manifest, output_dir)
            except Exception as _e:
                console.print(f"[dim yellow]Manifest finalization failed: {_e}[/dim yellow]")

        md_path = str(Path(output_dir) / f"{session_id}.md")
        csv_path = str(Path(output_dir) / f"{session_id}.csv")

        meta = SessionMetadata(
            session_id=session_id,
            agents=agent_ids,
            scenarios_run=len(all_scenarios) * len(agents_to_run) * n_runs,
            pillars=pillar_ints,
            started_at=started_at,
            completed_at=completed_at,
            output_dir=output_dir,
            md_path=md_path,
            csv_path=csv_path,
        )

        try:
            render_model_comparison_table(all_results, console)
            if not pillar or pillar_ints != [pillar_ints[0]]:
                for p in pillar_ints:
                    render_pillar_breakdown_table(all_results, p, console)
        except Exception as _e:
            console.print(f"[dim yellow]Academic table rendering failed: {_e}[/dim yellow]")

        try:
            Path(output_dir).mkdir(parents=True, exist_ok=True)
            export_session_markdown(all_results, meta, md_path)
            export_session_csv(all_results, meta, csv_path)
        except Exception as _e:
            console.print(f"[dim yellow]Session export failed: {_e}[/dim yellow]")

        try:
            render_session_summary_panel(meta, all_results, console)
        except Exception as _e:
            console.print(f"[dim yellow]Summary panel failed: {_e}[/dim yellow]")

        # ── Post-run: Academic report generation ──────────────────────────────
        if academic_report and not dry_run:
            from buyerbench.academic_report import generate_academic_report

            resolved_context = test_context or (
                "Evaluation conducted on BuyerBench v1.0. "
                "See session-config.yaml for agent and scenario configuration."
            )
            ar_output = str(Path(output_dir) / "ACADEMIC-REPORT.md")
            console.print(
                "[bold cyan]Generating academic report via Claude CLI...[/bold cyan]"
            )
            ar_text = generate_academic_report(
                results_dir=output_dir,
                test_context=resolved_context,
                output_path=ar_output,
            )
            if ar_text.startswith("ERROR:"):
                console.print(f"[dim yellow]Academic report failed: {ar_text}[/dim yellow]")
            else:
                console.print(
                    f"[bold green]Academic report saved →[/bold green] [bold]{ar_output}[/bold]"
                )

    console.print()
    console.print(
        f"[bold green]Run complete — {len(all_scenarios)} scenario(s) × "
        f"{len(agents_to_run)} agent(s).[/bold green]"
    )
    console.print(f"Results written to [bold]{output_dir}/[/bold]")
    console.print()

    # ── Publish to web dashboard prompt ──────────────────────────────────────
    if not dry_run and all_results and sys.stdin.isatty():
        from rich.prompt import Confirm

        if Confirm.ask(
            "[bold cyan]Publish results to web dashboard?[/bold cyan]",
            default=True,
        ):
            try:
                import json as _json
                from results.report import generate_full_report

                exp_dir = Path(output_dir)
                console.print(
                    f"[dim]Generating FULL-REPORT.json from {exp_dir} ...[/dim]"
                )
                full_report = generate_full_report(str(exp_dir))
                report_path = exp_dir / "FULL-REPORT.json"
                report_path.write_text(_json.dumps(full_report, indent=2, default=str))
                console.print(
                    f"[bold green]Published![/bold green] "
                    f"Report → [bold]{report_path}[/bold]"
                )
                n_scenarios = len(full_report.get("scenario_results", []))
                console.print(
                    f"[dim]{n_scenarios} scenario results with logs included.[/dim]"
                )
                console.print(
                    "[dim]Web dashboard will pick up changes automatically in dev mode "
                    "(npm run dev). For production, rebuild with: cd web && npm run build[/dim]"
                )
            except Exception as _pub_err:
                console.print(
                    f"[dim yellow]Publish failed: {_pub_err}[/dim yellow]"
                )
        console.print()

    if dashboard and not dry_run:
        from buyerbench.dashboard import run_dashboard

        console.print("[bold cyan]Launching results dashboard...[/bold cyan]")
        run_dashboard(output_dir)


@cli.command("dashboard")
@click.option(
    "--results-dir",
    default="results",
    show_default=True,
    help="Directory containing per-scenario result JSON files",
)
def dashboard_cmd(results_dir: str) -> None:
    """Browse benchmark results in an interactive terminal dashboard."""
    from pathlib import Path as _Path

    results_path = _Path(results_dir)
    if not results_path.exists():
        console.print(f"[red]Results directory not found: {results_path}[/red]")
        raise SystemExit(1)

    json_files = list(results_path.rglob("*.json"))
    if not json_files:
        console.print(
            f"[red]No JSON result files found in {results_path}[/red]\n"
            "[dim]Run [bold cyan]python -m buyerbench run[/bold cyan] first to generate results.[/dim]"
        )
        raise SystemExit(1)

    from buyerbench.dashboard import run_dashboard

    run_dashboard(results_dir)


@cli.command()
@click.option(
    "--experiment-dir",
    default="results/experiments",
    show_default=True,
    help="Root experiment directory with pillar1/, pillar2/, pillar3/ subdirs",
)
def report(experiment_dir: str) -> None:
    """Generate FULL-REPORT.json and FULL-REPORT.md from all experiment result JSONs."""
    import json
    from pathlib import Path

    from results.report import generate_full_report, render_full_report_markdown

    exp_dir = Path(experiment_dir)
    if not exp_dir.exists():
        console.print(f"[red]Experiment directory not found: {exp_dir}[/red]")
        raise SystemExit(1)

    console.print(
        f"[bold cyan]Generating full report from[/bold cyan] [bold]{exp_dir}[/bold] ..."
    )

    full_report = generate_full_report(str(exp_dir))

    json_path = exp_dir / "FULL-REPORT.json"
    md_path = exp_dir / "FULL-REPORT.md"

    json_path.write_text(json.dumps(full_report, indent=2, default=str))
    md_path.write_text(render_full_report_markdown(full_report))

    console.print("[bold green]Full report saved:[/bold green]")
    console.print(f"  JSON     → [bold]{json_path}[/bold]")
    console.print(f"  Markdown → [bold]{md_path}[/bold]")
    console.print()

    n_agg = len(full_report.get("per_pillar_aggregate", []))
    n_bsi = len(full_report.get("bias_susceptibility_table", []))
    n_sec = len(full_report.get("security_violation_table", []))
    n_delta = len(full_report.get("skills_mcp_delta_table", []))
    console.print(
        f"[dim]Per-pillar rows: {n_agg}  |  BSI rows: {n_bsi}  |  "
        f"Security rows: {n_sec}  |  Delta rows: {n_delta}[/dim]"
    )
    console.print()

    _render_rich_dashboard(full_report, console)


@cli.command()
@click.option(
    "--agent",
    "agent_ids",
    multiple=True,
    default=None,
    help=(
        "Agent ID(s) to include (repeat for multiple). "
        "Pass 'all' as the sole value to include every model in the catalog."
    ),
)
@click.option(
    "--pillar",
    default=None,
    type=click.Choice(["1", "2", "3"]),
    help="Filter scenarios by pillar (1/2/3). When omitted, all scenarios are included.",
)
@click.option(
    "--prompt-versions",
    "prompt_versions",
    multiple=True,
    default=["standard", "cot", "expert_role"],
    show_default=True,
    type=click.Choice(["standard", "cot", "expert_role"]),
    help="Prompt version(s) to include in the design space (repeat for multiple).",
)
@click.option(
    "--temperatures",
    "temperatures",
    multiple=True,
    default=[0.0, 0.3, 0.7, 1.0],
    show_default=True,
    type=float,
    help="Temperature value(s) to include in the design space (repeat for multiple).",
)
@click.option(
    "--n-runs",
    "n_runs",
    default=50,
    show_default=True,
    type=click.IntRange(min=1),
    help="Number of independent repeat runs per cell.",
)
@click.option(
    "--mode",
    default="auto",
    show_default=True,
    type=click.Choice(["full", "preset", "auto"]),
    help=(
        "Design mode. "
        "'auto' (default): greedy covering design — max(k, m) combinations. "
        "'preset': hardcoded BuyerBench 4-cell L4-analogous design. "
        "'full': all prompt × temperature combinations."
    ),
)
@click.option(
    "--output",
    "output_path",
    default="run-plan.csv",
    show_default=True,
    help="Destination path for the run plan CSV.",
)
def plan(
    agent_ids: tuple[str, ...],
    pillar: str | None,
    prompt_versions: tuple[str, ...],
    temperatures: tuple[float, ...],
    n_runs: int,
    mode: str,
    output_path: str,
) -> None:
    """Generate a fractional factorial run plan CSV for a flagship experiment.

    Auto-selects treatment combinations (prompt_version × temperature) to maximise
    statistical coverage while minimising total API calls. Outputs a row-per-run CSV
    with columns: run_plan_id, agent_id, scenario_id, prompt_version, temperature,
    run_index, cell_id, treatment_combination, bias_category.

    Examples:

    \b
      # Flagship 20K-run plan (auto fractional, all agents, Pillar 2):
      buyerbench plan --pillar 2 --n-runs 50 --output flagship-plan.csv

    \b
      # Full factorial (12 treatment cells per scenario):
      buyerbench plan --pillar 2 --n-runs 30 --mode full --output full-plan.csv

    \b
      # Preset BuyerBench 4-cell design:
      buyerbench plan --pillar 2 --n-runs 50 --mode preset --output preset-plan.csv
    """
    from pathlib import Path as _Path

    from buyerbench.model_catalog import MODEL_CATALOG
    from harness.loader import load_all_scenarios
    from results.fractional_design import CSV_FIELDNAMES, generate_run_plan, write_run_plan_csv

    # ── Resolve agent IDs ─────────────────────────────────────────────────────
    all_catalog_ids = [m.agent_id for m in MODEL_CATALOG]
    if not agent_ids or (len(agent_ids) == 1 and agent_ids[0] == "all"):
        resolved_agents = all_catalog_ids
    else:
        resolved_agents = list(agent_ids)

    # ── Load & filter scenarios ───────────────────────────────────────────────
    scenarios_root = _Path(__file__).parent.parent / "scenarios"
    all_scenarios = load_all_scenarios(str(scenarios_root))
    if pillar:
        pillar_int = int(pillar)
        from buyerbench.models import Pillar
        pillar_map = {1: Pillar.PILLAR1, 2: Pillar.PILLAR2, 3: Pillar.PILLAR3}
        target_pillar = pillar_map[pillar_int]
        all_scenarios = [s for s in all_scenarios if s.pillar == target_pillar]

    if not all_scenarios:
        console.print("[red]No scenarios matched the filter. Aborting.[/red]")
        raise SystemExit(1)

    scenario_ids = [s.id for s in all_scenarios]

    # ── Generate run plan ─────────────────────────────────────────────────────
    prompt_ver_list = list(prompt_versions) or ["standard"]
    temp_list: list[float | None] = list(temperatures) if temperatures else [None]

    try:
        rows, summary = generate_run_plan(
            agent_ids=resolved_agents,
            scenario_ids=scenario_ids,
            prompt_versions=prompt_ver_list,
            temperatures=temp_list,
            n_runs=n_runs,
            mode=mode,  # type: ignore[arg-type]
        )
    except ValueError as exc:
        console.print(f"[red]Design generation failed: {exc}[/red]")
        raise SystemExit(1)

    # ── Write CSV ─────────────────────────────────────────────────────────────
    out_path = write_run_plan_csv(rows, output_path)

    # ── Print summary ─────────────────────────────────────────────────────────
    console.print()
    console.rule("[bold cyan]BuyerBench Run Plan[/bold cyan]")
    console.print()

    summary_table = Table(box=box.ROUNDED, show_header=False, padding=(0, 2))
    summary_table.add_column("Field", style="bold cyan", no_wrap=True)
    summary_table.add_column("Value", style="white")

    summary_table.add_row("Design mode", summary.mode)
    summary_table.add_row("Agents", str(summary.n_agents))
    summary_table.add_row("Scenarios", str(summary.n_scenarios))
    summary_table.add_row("Treatment combinations", str(summary.n_treatment_combinations))
    summary_table.add_row("Runs per cell", str(summary.n_runs_per_cell))
    summary_table.add_row(
        "Total planned runs",
        f"[bold green]{summary.total_planned_runs:,}[/bold green]",
    )
    summary_table.add_row(
        "Full factorial runs",
        f"{summary.full_factorial_runs:,}",
    )
    summary_table.add_row(
        "Reduction vs full",
        f"[bold yellow]{summary.reduction_pct:.1f}%[/bold yellow]",
    )

    console.print(summary_table)
    console.print()

    combo_table = Table(
        title="[bold]Selected Treatment Combinations[/bold]",
        box=box.SIMPLE_HEAVY,
        show_lines=False,
    )
    combo_table.add_column("#", style="dim", justify="right")
    combo_table.add_column("Prompt Version", style="cyan")
    combo_table.add_column("Temperature", style="magenta", justify="right")
    for i, (pv, temp) in enumerate(summary.treatment_combinations, 1):
        temp_str = "default" if temp is None else str(temp)
        combo_table.add_row(str(i), pv, temp_str)
    console.print(combo_table)
    console.print()
    console.print(
        f"[bold green]Run plan saved →[/bold green] [bold]{out_path}[/bold]"
    )
    console.print(f"[dim]{len(rows):,} rows × {len(CSV_FIELDNAMES)} columns[/dim]")
    console.print()


def _score_markup(score: float | None) -> str:
    """Return rich markup for a 0-1 score: green ≥ 0.8, yellow 0.5–0.8, red < 0.5."""
    if score is None:
        return "[dim]—[/dim]"
    if score >= 0.8:
        return f"[bold green]{score:.4f}[/bold green]"
    if score >= 0.5:
        return f"[yellow]{score:.4f}[/yellow]"
    return f"[bold red]{score:.4f}[/bold red]"


def _render_rich_dashboard(report: dict, con: "Console") -> None:
    """Render a multi-panel rich terminal dashboard from a FULL-REPORT dict."""
    con.rule("[bold cyan]BuyerBench Results Dashboard[/bold cyan]")
    con.print()

    # ── 1. Per-pillar aggregate ───────────────────────────────────────────────
    agg_rows = report.get("per_pillar_aggregate", [])
    agg_t = Table(
        title="[bold]1. Per-Pillar Aggregate Scores[/bold]",
        box=box.ROUNDED,
        show_lines=True,
    )
    agg_t.add_column("Agent", style="bold cyan", no_wrap=True)
    agg_t.add_column("Pillar", style="magenta")
    agg_t.add_column("Mean Score", justify="right")
    agg_t.add_column("Std", justify="right", style="dim")
    agg_t.add_column("Min", justify="right")
    agg_t.add_column("Max", justify="right")
    agg_t.add_column("N", justify="right", style="dim")
    if agg_rows:
        for row in agg_rows:
            agg_t.add_row(
                row["agent_id"],
                row["pillar"],
                _score_markup(row["mean_score"]),
                f"{row['std']:.4f}",
                _score_markup(row["min"]),
                _score_markup(row["max"]),
                str(row["n_scenarios"]),
            )
    else:
        agg_t.add_row("[dim]—[/dim]", "[dim]—[/dim]", "[dim]—[/dim]",
                      "[dim]—[/dim]", "[dim]—[/dim]", "[dim]—[/dim]", "[dim]—[/dim]")
    con.print(agg_t)
    con.print()

    # ── 2. Bias Susceptibility Index ─────────────────────────────────────────
    bsi_rows = report.get("bias_susceptibility_table", [])
    bsi_t = Table(
        title="[bold]2. Bias Susceptibility Index[/bold]",
        box=box.ROUNDED,
        show_lines=True,
    )
    bsi_t.add_column("Bias Type", style="bold cyan", no_wrap=True)
    bsi_t.add_column("Agent", style="cyan")
    bsi_t.add_column("Mode", style="magenta")
    bsi_t.add_column("BSI", justify="right")
    bsi_t.add_column("Decision Changed", justify="center")
    if bsi_rows:
        for row in bsi_rows:
            changed = "[bold red]YES[/bold red]" if row["decision_changed"] else "[green]no[/green]"
            bsi_t.add_row(
                row["bias_type"],
                row["agent_id"],
                row["mode"],
                _score_markup(row["bsi"]),
                changed,
            )
    else:
        bsi_t.add_row("[dim]—[/dim]", "[dim]—[/dim]", "[dim]—[/dim]",
                      "[dim]—[/dim]", "[dim]—[/dim]")
    con.print(bsi_t)
    con.print()

    # ── 3. Security compliance ────────────────────────────────────────────────
    sec_rows = report.get("security_violation_table", [])
    sec_t = Table(
        title="[bold]3. Security / Compliance[/bold]",
        box=box.ROUNDED,
        show_lines=True,
    )
    sec_t.add_column("Scenario", style="bold cyan", no_wrap=True)
    sec_t.add_column("Agent", style="cyan")
    sec_t.add_column("Compliance Rate", justify="right")
    sec_t.add_column("Violation Freq", justify="right")
    sec_t.add_column("Score", justify="right")
    if sec_rows:
        for row in sec_rows:
            sec_t.add_row(
                row["scenario_id"],
                row["agent_id"],
                _score_markup(row["compliance_adherence_rate"]),
                _score_markup(1.0 - row["security_violation_frequency"]),
                _score_markup(row["score"]),
            )
    else:
        sec_t.add_row("[dim]—[/dim]", "[dim]—[/dim]", "[dim]—[/dim]",
                      "[dim]—[/dim]", "[dim]—[/dim]")
    con.print(sec_t)
    con.print()

    # ── 4. Skills vs MCP delta ────────────────────────────────────────────────
    delta_rows = report.get("skills_mcp_delta_table", [])
    delta_t = Table(
        title="[bold]4. Skills / MCP Score Delta vs. Baseline[/bold]",
        box=box.ROUNDED,
        show_lines=True,
    )
    delta_t.add_column("Family", style="bold cyan", no_wrap=True)
    delta_t.add_column("Mode", style="magenta")
    delta_t.add_column("Pillar", style="dim")
    delta_t.add_column("Baseline", justify="right")
    delta_t.add_column("Variant", justify="right")
    delta_t.add_column("Δ Delta", justify="right")
    if delta_rows:
        for row in delta_rows:
            delta_val = row.get("delta")
            if delta_val is None:
                delta_markup = "[dim]—[/dim]"
            elif delta_val > 0:
                delta_markup = f"[bold green]+{delta_val:.4f}[/bold green]"
            elif delta_val < 0:
                delta_markup = f"[bold red]{delta_val:.4f}[/bold red]"
            else:
                delta_markup = f"[dim]{delta_val:.4f}[/dim]"
            delta_t.add_row(
                row["family"],
                row["mode"],
                row["pillar"],
                _score_markup(row.get("baseline_score")),
                _score_markup(row.get("variant_score")),
                delta_markup,
            )
    else:
        delta_t.add_row("[dim]—[/dim]", "[dim]—[/dim]", "[dim]—[/dim]",
                        "[dim]—[/dim]", "[dim]—[/dim]", "[dim]—[/dim]")
    con.print(delta_t)
    con.print()

    con.rule("[dim]End of Dashboard[/dim]")
    con.print()


def _print_robustness_bsi_comparison(
    primary_results: list,
    robustness_results: list,
    console,  # rich.console.Console
) -> None:
    """Print a G.6 BSI collapse check: primary pass vs temperature=0.0 pass.

    Warns prominently if BSI collapses at T=0.0 (stochastic artifact indicator).
    """
    if not primary_results or not robustness_results:
        return

    def _mean_bsi(results: list) -> float:
        bsi_values: list[float] = []
        for r in results:
            for ps in r.pillar_scores:
                bsi = ps.metrics.get("bias_susceptibility_index")
                if bsi is not None:
                    try:
                        bsi_values.append(float(bsi))
                    except (TypeError, ValueError):
                        pass
        return sum(bsi_values) / len(bsi_values) if bsi_values else 0.0

    primary_bsi = _mean_bsi(primary_results)
    robust_bsi = _mean_bsi(robustness_results)

    console.print()
    console.print("[bold yellow]G.6 Robustness Check — BSI Comparison[/bold yellow]")
    console.print(f"  Primary run mean BSI :  [bold]{primary_bsi:.4f}[/bold]")
    console.print(f"  T=0.0 run mean BSI   :  [bold]{robust_bsi:.4f}[/bold]")

    COLLAPSE_THRESHOLD = 0.05
    if primary_bsi > 0.10 and robust_bsi <= COLLAPSE_THRESHOLD:
        console.print(
            "\n  [bold red]⚠  BSI COLLAPSE DETECTED[/bold red]\n"
            "  BSI dropped to near-zero at temperature=0.0 while the primary run "
            "showed non-trivial susceptibility.\n"
            "  [bold]Interpretation:[/bold] The observed bias susceptibility is likely a "
            "stochastic sampling artifact, NOT a stable encoded preference structure.\n"
            "  This must be prominently flagged in any published results (G.6 criterion)."
        )
    elif robust_bsi > COLLAPSE_THRESHOLD:
        console.print(
            "\n  [bold green]✓  BSI stable at T=0.0[/bold green]\n"
            "  Bias susceptibility persists under near-deterministic decoding — "
            "findings are not explained by sampling stochasticity."
        )
    else:
        console.print(
            "\n  [dim]Primary BSI is below detection threshold; robustness check "
            "is inconclusive (no strong bias signal to collapse).[/dim]"
        )
    console.print()


def _write_skipped_results(
    agent_id: str,
    scenarios,
    output_dir: str,
) -> None:
    """Write status=skipped JSON files for each scenario for an unavailable agent."""
    import json
    from datetime import datetime, timezone
    from pathlib import Path

    base = Path(output_dir) / agent_id
    base.mkdir(parents=True, exist_ok=True)
    for s in scenarios:
        payload = {
            "status": "skipped",
            "agent_id": agent_id,
            "scenario_id": s.id,
            "reason": "CLI or API key unavailable (see preflight check)",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        (base / f"{s.id}.json").write_text(json.dumps(payload, indent=2))


@cli.command()
@click.option(
    "--output",
    default="session-config.yaml",
    show_default=True,
    help="Path to save the session configuration YAML",
)
def session(output: str) -> None:
    """Interactively configure a full benchmark session (models + skills + scenarios)."""
    from rich.panel import Panel

    from buyerbench.selector import run_session_tui, save_session_config

    if not _stdin_is_tty():
        console.print("[red]Error: 'session' requires an interactive terminal (TTY).[/red]")
        raise SystemExit(1)

    config = run_session_tui()
    save_session_config(config, output)

    console.print()
    console.print(
        Panel(
            f"[bold]{output}[/bold]\n\n"
            f"[dim]Run [bold cyan]python -m buyerbench run --from-session {output}[/bold cyan] to execute.[/dim]",
            title=f"[bold green]Session config saved — {len(config.agents)} agent(s), {len(config.scenario_ids)} scenario(s)[/bold green]",
            border_style="green",
        )
    )
    console.print()


@cli.command("academic-report")
@click.option(
    "--results-dir",
    required=True,
    help="Directory containing per-scenario result JSON files",
)
@click.option(
    "--test-context",
    "test_context",
    default=None,
    help="Short description of the experiment (injected verbatim into §4)",
)
@click.option(
    "--test-context-file",
    "test_context_file",
    default=None,
    type=click.Path(exists=True, readable=True),
    help="Path to a file whose contents are used as the test context",
)
@click.option(
    "--from-session",
    "from_session",
    default=None,
    type=click.Path(exists=True, readable=True),
    help="Path to a session-config YAML; auto-loads research_notes as 'Researcher Notes:' context",
)
@click.option(
    "--research-notes",
    "research_notes",
    default=None,
    help="Researcher notes to prepend as context (merged after session notes when --from-session is also given)",
)
@click.option(
    "--output",
    default="ACADEMIC-REPORT.md",
    show_default=True,
    help="Output path for the generated academic report",
)
@click.option(
    "--bib-path",
    default="docs/paper/references.bib",
    show_default=True,
    help="Path to the BibTeX references file",
)
@click.option(
    "--cli-path",
    default="claude",
    show_default=True,
    help="Path to the Claude CLI binary",
)
def academic_report(
    results_dir: str,
    test_context: str | None,
    test_context_file: str | None,
    from_session: str | None,
    research_notes: str | None,
    output: str,
    bib_path: str,
    cli_path: str,
) -> None:
    """Generate a full academic paper from benchmark results via Claude CLI."""
    from buyerbench.academic_report import generate_academic_report

    if test_context and test_context_file:
        console.print("[red]--test-context and --test-context-file are mutually exclusive.[/red]")
        raise SystemExit(1)

    if test_context_file:
        resolved_context = Path(test_context_file).read_text(encoding="utf-8").strip()
    elif test_context:
        resolved_context = test_context
    else:
        resolved_context = (
            "Evaluation conducted on BuyerBench v1.0. "
            "See session-config.yaml for agent and scenario configuration."
        )

    # ── Researcher notes: load from session YAML and/or inline flag ───────────
    notes_parts: list[str] = []
    if from_session:
        from buyerbench.selector import load_session_config
        session_cfg = load_session_config(from_session)
        if session_cfg.research_notes:
            notes_parts.append(session_cfg.research_notes.strip())
    if research_notes:
        notes_parts.append(research_notes.strip())
    if notes_parts:
        combined_notes = "\n\n".join(notes_parts)
        resolved_context = f"Researcher Notes:\n{combined_notes}\n\n{resolved_context}"

    console.print("[bold cyan]Generating academic report via Claude CLI...[/bold cyan]")
    console.print("[dim]This may take several minutes — writing a full paper.[/dim]")
    console.print()

    result_text = generate_academic_report(
        results_dir=results_dir,
        test_context=resolved_context,
        output_path=output,
        cli_path=cli_path,
        bib_path=bib_path,
    )

    if result_text.startswith("ERROR:"):
        console.print(f"[red]{result_text}[/red]")
        raise SystemExit(1)

    console.print(f"[bold green]Academic report saved →[/bold green] [bold]{output}[/bold]")
    console.print()

    # Print the first 3 lines of the abstract (skip front matter)
    lines = [ln for ln in result_text.splitlines() if ln.strip() and not ln.startswith("---") and not ln.startswith("type:") and not ln.startswith("title:") and not ln.startswith("created:") and not ln.startswith("tags:")]
    abstract_lines = lines[:3]
    if abstract_lines:
        console.print("[bold]Abstract preview:[/bold]")
        for ln in abstract_lines:
            console.print(f"  {ln}")
    console.print()


@cli.command()
@click.option(
    "--results-dir",
    default="results/claude-code-baseline",
    show_default=True,
    help="Directory containing per-scenario result JSON files",
)
@click.option(
    "--output",
    default=None,
    help="Path to write the review Markdown (default: REVIEW.md inside --results-dir)",
)
def review(results_dir: str, output: str | None) -> None:
    """Generate a deep AI-written analytical review of benchmark results."""
    from pathlib import Path
    from buyerbench.review import generate_review

    results_path = Path(results_dir)
    if not results_path.exists():
        console.print(f"[red]Results directory not found: {results_path}[/red]")
        raise SystemExit(1)

    out_path = Path(output) if output else results_path / "REVIEW.md"

    console.print(
        f"[bold cyan]Generating deep review from[/bold cyan] [bold]{results_path}[/bold] ..."
    )
    console.print("[dim]Invoking Claude CLI — this may take 30–90 seconds.[/dim]")
    console.print()

    review_text = generate_review(str(results_path))

    if review_text.startswith("ERROR:"):
        console.print(f"[red]{review_text}[/red]")
        raise SystemExit(1)

    out_path.write_text(review_text)
    console.print(f"[bold green]Review saved →[/bold green] [bold]{out_path}[/bold]")
    console.print()
    console.print(review_text)


@cli.command("session-report")
@click.option(
    "--results-dir",
    required=True,
    help="Directory containing per-scenario result JSON files",
)
@click.option(
    "--output-dir",
    default=None,
    help="Directory to write .md and .csv exports (default: same as --results-dir)",
)
def session_report(results_dir: str, output_dir: str | None) -> None:
    """Regenerate academic reports and session exports from an existing results directory."""
    import json
    from datetime import datetime, timezone
    from pathlib import Path

    from buyerbench.models import EvaluationResult
    from results.academic_tables import (
        render_bias_table,
        render_model_comparison_table,
        render_pillar_breakdown_table,
        render_session_summary_panel,
    )
    from results.session_export import (
        SessionMetadata,
        export_session_csv,
        export_session_markdown,
        generate_session_id,
    )

    results_path = Path(results_dir)
    if not results_path.exists():
        console.print(f"[red]Results directory not found: {results_path}[/red]")
        raise SystemExit(1)

    out_dir = Path(output_dir) if output_dir else results_path
    out_dir.mkdir(parents=True, exist_ok=True)

    # Load all *.json result files
    results: list[EvaluationResult] = []
    for json_file in sorted(results_path.rglob("*.json")):
        try:
            raw = json.loads(json_file.read_text())
            if raw.get("status") == "skipped":
                continue
            results.append(EvaluationResult.model_validate(raw))
        except Exception:
            continue

    if not results:
        console.print("[yellow]No valid result JSON files found.[/yellow]")
        raise SystemExit(1)

    console.print(
        f"[bold cyan]Loaded {len(results)} result(s) from[/bold cyan] "
        f"[bold]{results_path}[/bold]"
    )

    session_id = generate_session_id()
    agent_ids = sorted({r.agent_id for r in results})
    pillar_set = sorted({
        int(ps.pillar.value.replace("PILLAR", ""))
        for r in results
        for ps in r.pillar_scores
        if hasattr(ps.pillar, "value")
    })
    now = datetime.now(timezone.utc)
    md_path = str(out_dir / f"{session_id}.md")
    csv_path = str(out_dir / f"{session_id}.csv")

    meta = SessionMetadata(
        session_id=session_id,
        agents=agent_ids,
        scenarios_run=len(results),
        pillars=pillar_set or [1],
        started_at=now,
        completed_at=now,
        output_dir=str(out_dir),
        md_path=md_path,
        csv_path=csv_path,
    )

    render_model_comparison_table(results, console)
    for p in (meta.pillars or [1, 2, 3]):
        render_pillar_breakdown_table(results, p, console)
    render_bias_table(results, console)

    export_session_markdown(results, meta, md_path)
    export_session_csv(results, meta, csv_path)

    render_session_summary_panel(meta, results, console)

    console.print(f"[bold green]Session report saved → {md_path}[/bold green]")
    console.print(f"[bold green]CSV export saved    → {csv_path}[/bold green]")
    console.print()


@cli.command()
@click.option(
    "--experiment-dir",
    required=True,
    help="Directory with agent sub-directories containing per-scenario result JSON files.",
)
@click.option(
    "--output-dir",
    default=None,
    help="Directory for stats_pipeline_report.json (default: --experiment-dir).",
)
@click.option(
    "--p1-scores",
    "p1_scores_str",
    default=None,
    help=(
        'Optional JSON mapping of agent_id → P1 score for H2 capability regression. '
        'Example: \'{"agent-A": 0.80, "agent-B": 0.65}\''
    ),
)
def stats(experiment_dir: str, output_dir: str | None, p1_scores_str: str | None) -> None:
    """Run Section G statistical analysis pipeline on a Pillar 2 experiment directory.

    Produces ``stats_pipeline_report.json`` containing:

    \b
    - Level 1 WLS: BSI ~ Treatment + BiasType + Model
    - ANOVA-style variance decomposition (η² per source)
    - Per-(bias_category × model) treatment-effect tests with BH-FDR correction
    - H7 noise-bias correlation (std_bsi ~ mean_bsi)
    - H2 capability regression (mean_BSI ~ P1Score; descriptive only)
    """
    import json as _json
    from pathlib import Path

    from results.aggregate_cells import aggregate_cells_from_dir
    from results.stats_pipeline import run_stats_pipeline, write_stats_pipeline_report

    exp_path = Path(experiment_dir)
    if not exp_path.exists():
        console.print(f"[red]Experiment directory not found: {exp_path}[/red]")
        raise SystemExit(1)

    out_path = Path(output_dir) if output_dir else exp_path

    # Parse optional P1 scores
    p1_scores: dict[str, float] | None = None
    if p1_scores_str:
        try:
            p1_scores = _json.loads(p1_scores_str)
        except Exception as exc:
            console.print(f"[red]--p1-scores is not valid JSON: {exc}[/red]")
            raise SystemExit(1)

    console.print(f"\n[bold cyan]Loading cell aggregates from:[/bold cyan] {exp_path}")
    try:
        cell_report = aggregate_cells_from_dir(exp_path)
    except Exception as exc:
        console.print(f"[red]Failed to load results: {exc}[/red]")
        raise SystemExit(1)

    console.print(
        f"[dim]  {cell_report.n_agents} agents · "
        f"{cell_report.n_cells} cells · "
        f"{cell_report.n_total_runs} total runs[/dim]"
    )

    console.print("\n[bold cyan]Running statistical analysis pipeline…[/bold cyan]")
    stats_report = run_stats_pipeline(cell_report, p1_scores=p1_scores)

    out_file = write_stats_pipeline_report(stats_report, out_path)
    console.print(f"\n[bold green]Stats report saved →[/bold green] [bold]{out_file}[/bold]")

    # ── Summary display ────────────────────────────────────────────────────────
    from rich.table import Table as RichTable
    from rich import box as rich_box

    if stats_report.variance_decomposition:
        vd = stats_report.variance_decomposition
        t = RichTable(
            title="[bold]Variance Decomposition (η²)[/bold]",
            box=rich_box.SIMPLE,
        )
        t.add_column("Source", style="bold cyan")
        t.add_column("SS", justify="right")
        t.add_column("η²", justify="right")
        t.add_column("% Variance", justify="right")
        for row in vd.rows:
            t.add_row(
                row.source,
                f"{row.ss:.4f}",
                f"{row.eta_squared:.4f}",
                f"{row.pct_variance:.1f}%",
            )
        console.print()
        console.print(t)

    if stats_report.treatment_effects:
        n_sig = sum(1 for te in stats_report.treatment_effects if te.significant_05)
        console.print(
            f"\n[bold]Treatment effects:[/bold] "
            f"{len(stats_report.treatment_effects)} tests · "
            f"{n_sig} significant at BH-FDR q=0.05"
        )

    if stats_report.level1_ols:
        ols = stats_report.level1_ols
        treat_coef = next(
            (c for c in ols.coefficients if c.name == "Treatment"), None
        )
        if treat_coef:
            sig_str = "[bold green]✓[/bold green]" if treat_coef.significant_05 else "[dim]ns[/dim]"
            console.print(
                f"[bold]Level 1 OLS Treatment β:[/bold] "
                f"{treat_coef.estimate:+.4f} "
                f"(SE={treat_coef.se:.4f}, p={treat_coef.p_value:.4f}) {sig_str}"
            )

    # ── Literature benchmark calibration table (UPGRADE-16) ───────────────
    if stats_report.literature_calibration:
        cal_table = RichTable(
            title="[bold]Literature Benchmark Calibration (UPGRADE-16)[/bold]",
            box=rich_box.SIMPLE,
        )
        cal_table.add_column("Bias Type", style="bold cyan")
        cal_table.add_column("BuyerBench BSI", justify="right")
        cal_table.add_column("Human Range", justify="right")
        cal_table.add_column("Human Mean", justify="right")
        cal_table.add_column("Prior LLM Range", justify="right")
        cal_table.add_column("Status")
        for r in stats_report.literature_calibration:
            bb_bsi = f"{r.llm_mean_bsi:.3f}" if r.llm_mean_bsi is not None else "—"
            h_range = f"[{r.human_benchmark_min:.2f}, {r.human_benchmark_max:.2f}]"
            h_mean = f"{r.human_benchmark_mean:.2f}"
            if r.llm_prior_min is not None and r.llm_prior_max is not None:
                llm_range = f"[{r.llm_prior_min:.2f}, {r.llm_prior_max:.2f}]"
            else:
                llm_range = "—"
            if r.within_human_range is None:
                status = "[dim]—[/dim]"
            elif r.within_human_range:
                status = "[green]within range[/green]"
            elif r.llm_mean_bsi is not None and r.llm_mean_bsi < r.human_benchmark_min:
                status = "[yellow]below human[/yellow]"
            else:
                status = "[red]above human[/red]"
            cal_table.add_row(r.bias_category, bb_bsi, h_range, h_mean, llm_range, status)
        console.print()
        console.print(cal_table)

    if stats_report.warnings:
        console.print("\n[bold yellow]Warnings:[/bold yellow]")
        for w in stats_report.warnings:
            console.print(f"  [dim]·[/dim] {w}")

    console.print()


@cli.command()
@click.option(
    "--manifest",
    default=None,
    help=(
        "Path to experiment_manifest.json produced by `buyerbench run`. "
        "Mutually exclusive with --standalone."
    ),
)
@click.option(
    "--standalone",
    is_flag=True,
    default=False,
    help=(
        "Generate a pre-registration document without a manifest, using the "
        "Realistic Design defaults (N=50, 10 models).  Use this to register on "
        "OSF BEFORE running experiments."
    ),
)
@click.option(
    "--output-dir",
    default=None,
    help="Directory for prereg_osf.md and prereg_metadata.json (default: manifest directory or cwd).",
)
@click.option(
    "--title",
    default=None,
    help="Custom document title.  Defaults to the standard BuyerBench pre-registration title.",
)
@click.option(
    "--authors",
    default="BuyerBench Research Team",
    show_default=True,
    help="Author attribution string for the pre-registration document.",
)
def prereg(
    manifest: str | None,
    standalone: bool,
    output_dir: str | None,
    title: str | None,
    authors: str,
) -> None:
    """Generate an OSF-compatible pre-registration document.

    Two modes:

    \b
    --manifest PATH   Read from an existing experiment_manifest.json (post-run).
    --standalone      Build from Realistic Design defaults; no manifest needed.
                      Use this to register on OSF BEFORE data collection begins.

    Outputs:

    \b
    - prereg_osf.md        — Structured Markdown for OSF/AsPredicted upload
    - prereg_metadata.json — Machine-readable document model

    The document includes all pre-specified hypotheses (H1–H10), the registered
    model set, bias type battery, statistical analysis plan, and null-result
    pre-specification.  It should be submitted to OSF before data collection begins.
    """
    from pathlib import Path as _Path

    from results.experiment_manifest import ExperimentManifest
    from results.prereg_export import (
        build_planned_manifest,
        generate_prereg_document,
        write_prereg_document,
    )

    if standalone and manifest:
        console.print("[red]--standalone and --manifest are mutually exclusive.[/red]")
        raise SystemExit(1)
    if not standalone and not manifest:
        console.print("[red]Provide either --manifest PATH or --standalone.[/red]")
        raise SystemExit(1)

    if standalone:
        manifest_data = build_planned_manifest()
        out_path = _Path(output_dir) if output_dir else _Path("docs/preregistration")
        console.print(
            f"\n[bold cyan]Generating standalone pre-registration document…[/bold cyan]\n"
            f"  [dim]Mode:[/dim]      standalone (planned defaults, N=50)\n"
            f"  [dim]Output:[/dim]    {out_path}"
        )
    else:
        manifest_path = _Path(manifest)  # type: ignore[arg-type]
        if not manifest_path.exists():
            console.print(f"[red]Manifest file not found: {manifest_path}[/red]")
            raise SystemExit(1)
        try:
            manifest_data = ExperimentManifest.model_validate_json(manifest_path.read_text())
        except Exception as exc:
            console.print(f"[red]Failed to parse manifest: {exc}[/red]")
            raise SystemExit(1)
        out_path = _Path(output_dir) if output_dir else manifest_path.parent
        console.print(
            f"\n[bold cyan]Generating pre-registration document…[/bold cyan]\n"
            f"  [dim]Manifest:[/dim]  {manifest_path}\n"
            f"  [dim]Output:[/dim]    {out_path}"
        )

    kwargs: dict = {}
    if title:
        kwargs["title"] = title
    kwargs["authors"] = authors

    doc, markdown = generate_prereg_document(manifest_data, **kwargs)
    md_file = write_prereg_document(doc, markdown, out_path)

    console.print(
        f"\n[bold green]Pre-registration document written →[/bold green] "
        f"[bold]{md_file}[/bold]"
    )
    console.print(
        f"[bold green]Metadata JSON written →[/bold green] "
        f"[bold]{out_path / 'prereg_metadata.json'}[/bold]"
    )

    # ── Summary ────────────────────────────────────────────────────────────────
    from rich.table import Table as RichTable
    from rich import box as rich_box

    t = RichTable(
        title="[bold]Pre-Registration Summary[/bold]",
        box=rich_box.SIMPLE,
    )
    t.add_column("Field", style="bold cyan")
    t.add_column("Value")

    t.add_row("Experiment ID", doc.manifest_experiment_id)
    t.add_row("Design tier", doc.manifest_design_tier)
    t.add_row("Models", str(doc.manifest_n_models))
    t.add_row("Scenarios", str(doc.manifest_n_scenarios))
    t.add_row("Runs per cell", str(doc.manifest_n_runs_per_cell))
    t.add_row("Planned runs", f"{doc.manifest_total_planned_runs:,}")
    t.add_row("Hypotheses", str(len(doc.hypotheses)))
    t.add_row("Bias types", ", ".join(doc.bias_types_tested))
    t.add_row(
        "Git commit",
        doc.manifest_git_hash or "[dim]unknown[/dim]",
    )
    if doc.manifest_pre_registration_url:
        t.add_row("Pre-reg URL", doc.manifest_pre_registration_url)

    console.print()
    console.print(t)
    console.print()


@cli.command("robustness-pilot")
@click.option(
    "--agent",
    "agent_id",
    required=True,
    help="Agent ID to use for the robustness pilot (e.g. openrouter-openai-gpt-4o).",
)
@click.option(
    "--pair-id",
    "pair_ids",
    multiple=True,
    help=(
        "Scenario pair ID(s) to test (e.g. p2-01-anchoring).  "
        "Repeat for multiple pairs.  Omits all other Pillar 2 pairs if unset."
    ),
)
@click.option(
    "--n-runs",
    "n_runs",
    default=5,
    show_default=True,
    type=int,
    help="Independent runs per (phrasing × scenario_pair) cell.",
)
@click.option(
    "--cv-threshold",
    "cv_threshold",
    default=0.50,
    show_default=True,
    type=float,
    help="CV above which a scenario is flagged wording-sensitive (REV-5 gate: 0.50).",
)
@click.option(
    "--output-dir",
    "output_dir",
    default="results/robustness-pilot",
    show_default=True,
    help="Directory to write robustness_pilot.json output.",
)
def robustness_pilot_cmd(
    agent_id: str,
    pair_ids: tuple[str, ...],
    n_runs: int,
    cv_threshold: float,
    output_dir: str,
) -> None:
    """Run the REV-5 prompt robustness pilot (3 phrasings × N runs per scenario pair).

    Evaluates whether BSI values are stable across 3 minor prompt-phrasing
    variants of the same scenario.  If the coefficient of variation (CV) of
    mean-BSI across phrasings exceeds --cv-threshold, the scenario is flagged
    as wording-sensitive and must be redesigned before the main experiment.

    \b
    Outputs:
      results/robustness-pilot/robustness_pilot.json
        Per-scenario CV, per-phrasing mean-BSI, and overall PROCEED/REDESIGN.

    \b
    Example:
      buyerbench robustness-pilot \\
        --agent openrouter-openai-gpt-4o \\
        --pair-id p2-01-anchoring --pair-id p2-02-framing \\
        --n-runs 5
    """
    from pathlib import Path as _Path

    from agents.registry import get_agent
    from harness.config import load_config
    from harness.loader import load_all_scenarios
    from harness.prompt import REV5_PHRASINGS
    from harness.robustness_pilot import run_robustness_pilot

    config = load_config()

    # Build 3 agents — one per robustness phrasing.
    phrasings: list = []
    for label in REV5_PHRASINGS:
        phrasing_config = dict(config)
        phrasing_config["prompt_version"] = label
        agent = get_agent(agent_id, phrasing_config)
        phrasings.append((label, agent))

    # Load Pillar 2 scenario pairs.
    scenarios_root = _Path(__file__).parent.parent / "scenarios"
    all_scenarios = load_all_scenarios(str(scenarios_root))
    p2_scenarios = [s for s in all_scenarios if s.pillar.value == "PILLAR2"]

    # Group into (baseline, variant) pairs by variant_pair_id.
    from collections import defaultdict
    by_pair: dict = defaultdict(list)
    for s in p2_scenarios:
        if s.variant_pair_id:
            by_pair[s.variant_pair_id].append(s)

    # Filter to requested pair_ids (or all Pillar 2 pairs).
    selected_pairs: list = []
    for pid, scenarios in by_pair.items():
        if pair_ids and pid not in pair_ids:
            continue
        # Separate baseline from variant(s); use first non-baseline as the variant.
        baselines = [s for s in scenarios if s.variant.value == "BASELINE"]
        variants = [s for s in scenarios if s.variant.value != "BASELINE"]
        if baselines and variants:
            selected_pairs.append((baselines[0], variants[0]))

    if not selected_pairs:
        console.print(
            "[red]No matching Pillar 2 scenario pairs found.  "
            "Check --pair-id values or ensure scenarios/ is populated.[/red]"
        )
        raise SystemExit(1)

    console.print(
        f"\n[bold cyan]REV-5 Prompt Robustness Pilot[/bold cyan]\n"
        f"  [dim]Agent:[/dim]       {agent_id}\n"
        f"  [dim]Phrasings:[/dim]   {', '.join(REV5_PHRASINGS)}\n"
        f"  [dim]Pairs:[/dim]       {len(selected_pairs)}\n"
        f"  [dim]Runs/cell:[/dim]   {n_runs}\n"
        f"  [dim]CV gate:[/dim]     {cv_threshold}\n"
        f"  [dim]Output:[/dim]      {output_dir}\n"
    )

    result = run_robustness_pilot(
        scenario_pairs=selected_pairs,
        phrasings=phrasings,
        n_runs=n_runs,
        cv_threshold=cv_threshold,
        output_dir=output_dir,
    )

    # ── Rich summary table ─────────────────────────────────────────────────────
    from rich.table import Table as RichTable
    from rich import box as rich_box

    t = RichTable(
        title="[bold]Prompt Robustness Pilot Results (REV-5)[/bold]",
        box=rich_box.SIMPLE,
    )
    t.add_column("Scenario Pair", style="bold cyan")
    t.add_column("CV", justify="right")
    t.add_column("Mean BSI", justify="right")
    t.add_column("Recommendation", justify="center")

    for pair_id, report in result["per_scenario"].items():
        cv_str = f"{report['cv']:.3f}"
        mean_bsi_str = f"{report['mean_of_means']:.3f}"
        rec = report["recommendation"]
        rec_markup = (
            "[green]PROCEED[/green]" if rec == "PROCEED" else "[red]REDESIGN[/red]"
        )
        t.add_row(pair_id, cv_str, mean_bsi_str, rec_markup)

    console.print()
    console.print(t)
    console.print()

    overall = result["overall_recommendation"]
    if overall == "PROCEED":
        console.print(
            f"[bold green]Overall: PROCEED[/bold green] — "
            f"all {result['scenarios_passing']} scenario pair(s) are wording-stable "
            f"(CV ≤ {cv_threshold})."
        )
    else:
        console.print(
            f"[bold red]Overall: REDESIGN[/bold red] — "
            f"{result['scenarios_failing']} scenario pair(s) are wording-sensitive "
            f"(CV > {cv_threshold}).  Redesign before main experiment:"
        )
        for pid in result["scenarios_to_redesign"]:
            console.print(f"  [red]•[/red] {pid}")

    console.print(
        f"\n[bold]Results written →[/bold] {_Path(output_dir) / 'robustness_pilot.json'}\n"
    )

    raise SystemExit(0 if overall == "PROCEED" else 2)


if __name__ == "__main__":
    cli()
