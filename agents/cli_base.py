"""Abstract base class for CLI-invoked agent adapters.

Each concrete subclass wraps a specific CLI tool (Claude Code, Codex, Gemini)
by implementing run_cli(prompt) -> str.  The base class handles prompt
construction, latency measurement, output parsing, dry-run mode, and
timeout enforcement.
"""
from __future__ import annotations

import subprocess
import time
from abc import abstractmethod

from agents import BaseAgent
from buyerbench.models import AgentResponse, Scenario
from harness.prompt import parse_agent_output, scenario_to_prompt


class CLIAgent(BaseAgent):
    """Abstract base for agents invoked as external CLI subprocesses.

    Subclasses must set ``agent_id`` as a class attribute and implement
    ``run_cli(prompt) -> str``.

    Parameters
    ----------
    timeout:
        Maximum seconds to wait for the CLI process.  Defaults to 120.
    dry_run:
        If True, print the prompt that *would* be sent without invoking the
        CLI, then return an empty AgentResponse.
    """

    agent_id: str = ""
    timeout: int = 120
    dry_run: bool = False

    def __init__(self, timeout: int = 120, dry_run: bool = False) -> None:
        self.timeout = timeout
        self.dry_run = dry_run

    @abstractmethod
    def run_cli(self, prompt: str) -> str:
        """Invoke the CLI tool with *prompt* and return its stdout."""
        ...

    def respond(self, scenario: Scenario) -> AgentResponse:
        """Serialize *scenario* to a prompt, invoke the CLI, parse the output."""
        prompt = scenario_to_prompt(scenario)

        if self.dry_run:
            _print_dry_run(self.agent_id, scenario.id, prompt)
            return AgentResponse(
                scenario_id=scenario.id,
                agent_id=self.agent_id,
                decisions={},
                reasoning_trace="[dry-run: CLI not invoked]",
                raw_output="",
                latency_ms=0.0,
            )

        start = time.monotonic()
        raw_output = self.run_cli(prompt)
        latency_ms = (time.monotonic() - start) * 1000

        decisions = parse_agent_output(raw_output, scenario)

        return AgentResponse(
            scenario_id=scenario.id,
            agent_id=self.agent_id,
            decisions=decisions,
            reasoning_trace="",
            raw_output=raw_output,
            latency_ms=latency_ms,
        )

    def _invoke_subprocess(self, cmd: list[str], input_text: str | None = None) -> str:
        """Run *cmd* as a subprocess and return stdout.

        Raises ``subprocess.TimeoutExpired`` (re-raised) if the process
        exceeds ``self.timeout`` seconds.  Returns stderr merged into output
        when the process exits with a non-zero code but produces no stdout.
        """
        result = subprocess.run(
            cmd,
            input=input_text,
            capture_output=True,
            text=True,
            timeout=self.timeout,
        )
        output = result.stdout
        if result.returncode != 0 and not output.strip():
            output = result.stderr
        return output


def _print_dry_run(agent_id: str, scenario_id: str, prompt: str) -> None:
    separator = "=" * 60
    print(f"\n{separator}")
    print(f"DRY RUN  |  agent={agent_id}  |  scenario={scenario_id}")
    print(separator)
    print(prompt)
    print(f"{separator}\n")
