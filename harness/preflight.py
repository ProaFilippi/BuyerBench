"""Pre-flight environment validation for BuyerBench.

Verifies that all CLI agent dependencies, API keys, and infrastructure
(mock MCP server) are available before running experiments.  Reports
results in a rich table and returns a structured dict so callers can
programmatically skip unavailable agents.

Usage
-----
Programmatic::

    from harness.preflight import check_environment
    env = check_environment()
    if not env["overall"]:
        print("Some checks failed — see report above")

CLI::

    python -m buyerbench check
"""
from __future__ import annotations

import os
import subprocess
from typing import Any

from rich.console import Console
from rich.table import Table
from rich import box

console = Console(highlight=False)

# ---------------------------------------------------------------------------
# CLI tools to probe — maps agent family → (cli_name, version_flag)
# ---------------------------------------------------------------------------
_CLI_TOOLS: dict[str, tuple[str, str]] = {
    "claude": ("claude", "--version"),
    "codex": ("codex", "--version"),
    "gemini": ("gemini", "--version"),
}

# ---------------------------------------------------------------------------
# API key environment variables — maps agent family → env var name(s)
# ---------------------------------------------------------------------------
_API_KEYS: dict[str, list[str]] = {
    "Claude (ANTHROPIC_API_KEY)": ["ANTHROPIC_API_KEY"],
    "Codex (OPENAI_API_KEY)": ["OPENAI_API_KEY"],
    "Gemini (GOOGLE_API_KEY / GEMINI_API_KEY)": ["GOOGLE_API_KEY", "GEMINI_API_KEY"],
}


def _probe_cli(cli_name: str, version_flag: str) -> dict[str, Any]:
    """Run ``cli_name version_flag`` and capture the outcome."""
    try:
        result = subprocess.run(
            [cli_name, version_flag],
            capture_output=True,
            text=True,
            timeout=10,
        )
        version_line = (result.stdout or result.stderr or "").strip().splitlines()
        version = version_line[0] if version_line else "(no version output)"
        return {"installed": True, "version": version, "error": None}
    except FileNotFoundError:
        return {"installed": False, "version": None, "error": "not found in PATH"}
    except subprocess.TimeoutExpired:
        return {"installed": False, "version": None, "error": "timed out"}
    except Exception as exc:  # noqa: BLE001
        return {"installed": False, "version": None, "error": str(exc)}


def _probe_api_keys(key_names: list[str]) -> dict[str, Any]:
    """Return whether *any* of the listed env vars is non-empty."""
    for name in key_names:
        if os.environ.get(name):
            return {"set": True, "key_name": name}
    return {"set": False, "key_name": None}


def _probe_mcp_server() -> dict[str, Any]:
    """Try to start the mock MCP server and immediately stop it."""
    try:
        from harness.mock_mcp_server import MockMCPServer

        # Use port 0 so the OS picks a free ephemeral port
        with MockMCPServer(port=0):
            pass
        return {"started": True, "error": None}
    except Exception as exc:  # noqa: BLE001
        return {"started": False, "error": str(exc)}


def check_environment(print_report: bool = True) -> dict[str, Any]:
    """Run all pre-flight checks and optionally print a rich report.

    Parameters
    ----------
    print_report:
        When *True* (default) a formatted table is printed to stdout.

    Returns
    -------
    dict
        Structure::

            {
                "clis": {
                    "claude": {"installed": bool, "version": str|None, "error": str|None},
                    "codex":  {...},
                    "gemini": {...},
                },
                "api_keys": {
                    "Claude (ANTHROPIC_API_KEY)": {"set": bool, "key_name": str|None},
                    ...
                },
                "mcp_server": {"started": bool, "error": str|None},
                "overall": bool,
                "available_agents": list[str],  # agent_ids whose CLI + key are present
            }
    """
    results: dict[str, Any] = {"clis": {}, "api_keys": {}, "mcp_server": {}}

    # --- CLI probes ---
    for family, (cli_name, version_flag) in _CLI_TOOLS.items():
        results["clis"][family] = _probe_cli(cli_name, version_flag)

    # --- API key probes ---
    for label, key_names in _API_KEYS.items():
        results["api_keys"][label] = _probe_api_keys(key_names)

    # --- Mock MCP server probe ---
    results["mcp_server"] = _probe_mcp_server()

    # --- Derive available agent families ---
    _family_ok = {
        "claude": (
            results["clis"]["claude"]["installed"]
            and results["api_keys"]["Claude (ANTHROPIC_API_KEY)"]["set"]
        ),
        "codex": (
            results["clis"]["codex"]["installed"]
            and results["api_keys"]["Codex (OPENAI_API_KEY)"]["set"]
        ),
        "gemini": (
            results["clis"]["gemini"]["installed"]
            and results["api_keys"]["Gemini (GOOGLE_API_KEY / GEMINI_API_KEY)"]["set"]
        ),
    }
    available_agents: list[str] = []
    for family, ok in _family_ok.items():
        if ok:
            available_agents.extend(
                [f"{family}-baseline", f"{family}-skills", f"{family}-mcp"]
                if family != "claude"
                else [
                    "claude-code-baseline",
                    "claude-code-skills",
                    "claude-code-mcp",
                ]
            )
    results["available_agents"] = available_agents

    all_keys_set = all(v["set"] for v in results["api_keys"].values())
    any_cli_installed = any(v["installed"] for v in results["clis"].values())
    results["overall"] = (
        any_cli_installed and all_keys_set and results["mcp_server"]["started"]
    )

    if print_report:
        _print_report(results)

    return results


def _print_report(results: dict[str, Any]) -> None:
    """Render the pre-flight report to the console."""
    console.print()
    console.rule("[bold cyan]BuyerBench Pre-Flight Check[/bold cyan]")
    console.print()

    # --- CLI table ---
    cli_table = Table(
        title="CLI Tools",
        box=box.ROUNDED,
        show_lines=True,
    )
    cli_table.add_column("CLI", style="bold cyan", no_wrap=True)
    cli_table.add_column("Status", justify="center")
    cli_table.add_column("Version / Error")

    for family, info in results["clis"].items():
        if info["installed"]:
            status = "[green]OK[/green]"
            detail = info["version"] or "—"
        else:
            status = "[yellow]MISSING[/yellow]"
            detail = info["error"] or "not found"
        cli_table.add_row(family, status, detail)

    console.print(cli_table)
    console.print()

    # --- API key table ---
    key_table = Table(
        title="API Keys",
        box=box.ROUNDED,
        show_lines=True,
    )
    key_table.add_column("Variable", style="bold cyan", no_wrap=True)
    key_table.add_column("Status", justify="center")
    key_table.add_column("Active Key Name")

    for label, info in results["api_keys"].items():
        if info["set"]:
            status = "[green]SET[/green]"
            detail = info["key_name"] or "—"
        else:
            status = "[yellow]NOT SET[/yellow]"
            detail = "—"
        key_table.add_row(label, status, detail)

    console.print(key_table)
    console.print()

    # --- MCP server ---
    mcp = results["mcp_server"]
    if mcp["started"]:
        mcp_status = "[green]OK[/green]"
        mcp_detail = "Mock MCP server starts cleanly"
    else:
        mcp_status = "[red]FAIL[/red]"
        mcp_detail = mcp["error"] or "unknown error"

    mcp_table = Table(title="Infrastructure", box=box.ROUNDED, show_lines=True)
    mcp_table.add_column("Component", style="bold cyan", no_wrap=True)
    mcp_table.add_column("Status", justify="center")
    mcp_table.add_column("Detail")
    mcp_table.add_row("Mock MCP Server", mcp_status, mcp_detail)
    console.print(mcp_table)
    console.print()

    # --- Summary ---
    available = results["available_agents"]
    if available:
        console.print(
            f"[bold green]Available agents ({len(available)}):[/bold green] "
            + ", ".join(available)
        )
    else:
        console.print(
            "[bold yellow]No fully configured agents found.[/bold yellow] "
            "Install CLI tools and set API keys to enable real agent runs."
        )
    console.print()

    if results["overall"]:
        console.print("[bold green]Pre-flight PASSED — all checks OK.[/bold green]")
    else:
        console.print(
            "[bold yellow]Pre-flight INCOMPLETE — some dependencies missing. "
            "Missing agents will be skipped during experiments.[/bold yellow]"
        )
    console.print()
