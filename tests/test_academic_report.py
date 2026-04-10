"""Tests for buyerbench.academic_report."""
from __future__ import annotations

import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import yaml
from click.testing import CliRunner

from buyerbench.academic_report import build_academic_prompt, generate_academic_report
from buyerbench.__main__ import cli


# ── Fixtures ──────────────────────────────────────────────────────────────────

SAMPLE_RESULTS = [
    {
        "scenario_id": "p1-01",
        "agent_id": "mock-agent-v1",
        "status": "completed",
        "overall_pass": True,
        "pillar_scores": [
            {"pillar": "PILLAR1", "score": 0.85, "metrics": {}, "violations": [], "notes": ""}
        ],
    },
    {
        "scenario_id": "p2-01",
        "agent_id": "mock-agent-v1",
        "status": "completed",
        "overall_pass": False,
        "pillar_scores": [
            {"pillar": "PILLAR2", "score": 0.60, "metrics": {}, "violations": [], "notes": ""}
        ],
        "variant_pair_id": "framing-a",
    },
]

SAMPLE_SESSION_META = {
    "agents": ["mock-agent-v1"],
    "session_id": "session-20260408-120000",
}

SAMPLE_BIB = """\
@article{kahneman1979prospect,
  title = {Prospect Theory},
  author = {Kahneman, Daniel and Tversky, Amos},
  journal = {Econometrica},
  year = {1979},
}

@article{liu2023agentbench,
  title = {AgentBench},
  author = {Liu, Xiao and others},
  journal = {arXiv preprint},
  year = {2023},
}
"""

TEST_CONTEXT = "Experiment run on 2026-04-08 using BuyerBench v1.0 with mock agent."


# ── build_academic_prompt tests ───────────────────────────────────────────────

class TestBuildAcademicPrompt:
    def test_returns_string(self):
        prompt = build_academic_prompt(SAMPLE_RESULTS, SAMPLE_SESSION_META, TEST_CONTEXT, SAMPLE_BIB)
        assert isinstance(prompt, str)

    def test_contains_required_sections(self):
        prompt = build_academic_prompt(SAMPLE_RESULTS, SAMPLE_SESSION_META, TEST_CONTEXT, SAMPLE_BIB)
        for section in ["Abstract", "Related Work", "References"]:
            assert section in prompt, f"Missing section: {section}"

    def test_contains_citation_syntax(self):
        prompt = build_academic_prompt(SAMPLE_RESULTS, SAMPLE_SESSION_META, TEST_CONTEXT, SAMPLE_BIB)
        assert "[@" in prompt, "Prompt must include [@key] citation syntax instruction"

    def test_test_context_injected_verbatim(self):
        prompt = build_academic_prompt(SAMPLE_RESULTS, SAMPLE_SESSION_META, TEST_CONTEXT, SAMPLE_BIB)
        assert TEST_CONTEXT in prompt

    def test_references_bib_content_in_prompt(self):
        prompt = build_academic_prompt(SAMPLE_RESULTS, SAMPLE_SESSION_META, TEST_CONTEXT, SAMPLE_BIB)
        assert "kahneman1979prospect" in prompt
        assert "liu2023agentbench" in prompt

    def test_benchmark_results_embedded(self):
        prompt = build_academic_prompt(SAMPLE_RESULTS, SAMPLE_SESSION_META, TEST_CONTEXT, SAMPLE_BIB)
        assert "BENCHMARK RESULTS" in prompt
        assert "p1-01" in prompt

    def test_bibliography_source_label_present(self):
        prompt = build_academic_prompt(SAMPLE_RESULTS, SAMPLE_SESSION_META, TEST_CONTEXT, SAMPLE_BIB)
        assert "BIBLIOGRAPHY SOURCE" in prompt

    def test_prompt_under_token_budget(self):
        # Rough token estimate: 4 chars per token
        prompt = build_academic_prompt(SAMPLE_RESULTS, SAMPLE_SESSION_META, TEST_CONTEXT, SAMPLE_BIB)
        estimated_tokens = len(prompt) / 4
        assert estimated_tokens < 8000, f"Prompt too long: ~{estimated_tokens:.0f} tokens"

    def test_methodology_pillar_descriptions(self):
        prompt = build_academic_prompt(SAMPLE_RESULTS, SAMPLE_SESSION_META, TEST_CONTEXT, SAMPLE_BIB)
        for keyword in ["Pillar 1", "Pillar 2", "Pillar 3"]:
            assert keyword in prompt


# ── generate_academic_report tests ───────────────────────────────────────────

class TestGenerateAcademicReport:
    def _write_results(self, tmp_dir: Path, results: list[dict]) -> None:
        for r in results:
            (tmp_dir / f"{r['scenario_id']}.json").write_text(json.dumps(r))

    def _write_bib(self, tmp_dir: Path) -> Path:
        bib_path = tmp_dir / "references.bib"
        bib_path.write_text(SAMPLE_BIB)
        return bib_path

    def test_returns_error_for_missing_results_dir(self):
        result = generate_academic_report(
            results_dir="/nonexistent/path",
            test_context=TEST_CONTEXT,
        )
        assert result.startswith("ERROR:")
        assert "not found" in result.lower()

    def test_returns_error_for_missing_bib(self, tmp_path):
        self._write_results(tmp_path, SAMPLE_RESULTS)
        result = generate_academic_report(
            results_dir=str(tmp_path),
            test_context=TEST_CONTEXT,
            bib_path="/nonexistent/references.bib",
        )
        assert result.startswith("ERROR:")

    def test_returns_error_for_empty_results_dir(self, tmp_path):
        bib_path = self._write_bib(tmp_path)
        result = generate_academic_report(
            results_dir=str(tmp_path),
            test_context=TEST_CONTEXT,
            bib_path=str(bib_path),
        )
        assert result.startswith("ERROR:")

    def test_skips_skipped_results(self, tmp_path):
        """Skipped result files should not count toward the result set."""
        (tmp_path / "p1-01.json").write_text(json.dumps({"status": "skipped", "agent_id": "x"}))
        bib_path = self._write_bib(tmp_path)
        result = generate_academic_report(
            results_dir=str(tmp_path),
            test_context=TEST_CONTEXT,
            bib_path=str(bib_path),
        )
        assert result.startswith("ERROR:")
        assert "no valid" in result.lower()

    def test_writes_front_matter_and_content(self, tmp_path):
        self._write_results(tmp_path, SAMPLE_RESULTS)
        bib_path = self._write_bib(tmp_path)
        output_path = tmp_path / "ACADEMIC-REPORT.md"

        fake_paper = "## Abstract\n\nThis is a test paper about BuyerBench.\n\n## References\n\n1. Kahneman 1979."

        mock_proc = MagicMock()
        mock_proc.stdout = fake_paper
        mock_proc.returncode = 0

        with patch("subprocess.run", return_value=mock_proc):
            result = generate_academic_report(
                results_dir=str(tmp_path),
                test_context=TEST_CONTEXT,
                output_path=str(output_path),
                bib_path=str(bib_path),
            )

        assert output_path.exists()
        written = output_path.read_text(encoding="utf-8")

        # Front matter present
        assert "---" in written
        assert "type: report" in written
        assert "title: BuyerBench Academic Report" in written
        assert "tags: [benchmark, academic, buyer-agent, evaluation]" in written

        # Paper content present
        assert fake_paper in written

        # Return value matches written content
        assert result == written

    def test_handles_cli_timeout(self, tmp_path):
        import subprocess as _subprocess

        self._write_results(tmp_path, SAMPLE_RESULTS)
        bib_path = self._write_bib(tmp_path)

        with patch("subprocess.run", side_effect=_subprocess.TimeoutExpired("claude", 600)):
            result = generate_academic_report(
                results_dir=str(tmp_path),
                test_context=TEST_CONTEXT,
                bib_path=str(bib_path),
            )

        assert result.startswith("ERROR:")
        assert "timed out" in result.lower()

    def test_handles_cli_not_found(self, tmp_path):
        self._write_results(tmp_path, SAMPLE_RESULTS)
        bib_path = self._write_bib(tmp_path)

        with patch("subprocess.run", side_effect=FileNotFoundError):
            result = generate_academic_report(
                results_dir=str(tmp_path),
                test_context=TEST_CONTEXT,
                bib_path=str(bib_path),
                cli_path="nonexistent-claude",
            )

        assert result.startswith("ERROR:")
        assert "not found" in result.lower()

    def test_handles_empty_cli_output(self, tmp_path):
        self._write_results(tmp_path, SAMPLE_RESULTS)
        bib_path = self._write_bib(tmp_path)

        mock_proc = MagicMock()
        mock_proc.stdout = ""
        mock_proc.stderr = ""
        mock_proc.returncode = 0

        with patch("subprocess.run", return_value=mock_proc):
            result = generate_academic_report(
                results_dir=str(tmp_path),
                test_context=TEST_CONTEXT,
                bib_path=str(bib_path),
            )

        assert result.startswith("ERROR:")


# ── CLI academic-report --from-session / --research-notes tests ───────────────

class TestAcademicReportCLISessionNotes:
    """Tests for --from-session and --research-notes flags on the academic-report command."""

    def _write_results(self, tmp_dir: Path) -> None:
        for r in SAMPLE_RESULTS:
            (tmp_dir / f"{r['scenario_id']}.json").write_text(json.dumps(r))

    def _write_bib(self, tmp_dir: Path) -> Path:
        bib_path = tmp_dir / "references.bib"
        bib_path.write_text(SAMPLE_BIB)
        return bib_path

    def _write_session_yaml(self, tmp_dir: Path, research_notes: str) -> Path:
        session_path = tmp_dir / "session-config.yaml"
        payload = {
            "experiment_name": "test-experiment",
            "research_objective": "test objective",
            "research_notes": research_notes,
            "recurrence": None,
            "output_dir": "results",
            "agents": [{"agent_id": "mock-agent-v1", "skill_mode": "none"}],
            "scenario_ids": ["p1-01"],
            "created_at": "2026-04-09T00:00:00+00:00",
        }
        session_path.write_text(yaml.safe_dump(payload))
        return session_path

    def _mock_proc(self, text: str) -> MagicMock:
        mock = MagicMock()
        mock.stdout = text
        mock.returncode = 0
        return mock

    def test_from_session_loads_notes_into_context(self, tmp_path):
        self._write_results(tmp_path)
        bib_path = self._write_bib(tmp_path)
        session_path = self._write_session_yaml(tmp_path, "Notes from session YAML.")
        output_path = tmp_path / "out.md"

        captured_prompt: list[str] = []

        def fake_run(cmd, **kwargs):
            captured_prompt.append(cmd[2])  # claude --print <prompt>
            return self._mock_proc("## Abstract\n\nTest paper.")

        with patch("subprocess.run", side_effect=fake_run):
            runner = CliRunner()
            result = runner.invoke(cli, [
                "academic-report",
                "--results-dir", str(tmp_path),
                "--from-session", str(session_path),
                "--output", str(output_path),
                "--bib-path", str(bib_path),
            ])

        assert result.exit_code == 0, result.output
        assert captured_prompt, "subprocess.run was not called"
        assert "Researcher Notes:" in captured_prompt[0]
        assert "Notes from session YAML." in captured_prompt[0]

    def test_research_notes_flag_prepended(self, tmp_path):
        self._write_results(tmp_path)
        bib_path = self._write_bib(tmp_path)
        output_path = tmp_path / "out.md"

        captured_prompt: list[str] = []

        def fake_run(cmd, **kwargs):
            captured_prompt.append(cmd[2])
            return self._mock_proc("## Abstract\n\nTest paper.")

        with patch("subprocess.run", side_effect=fake_run):
            runner = CliRunner()
            result = runner.invoke(cli, [
                "academic-report",
                "--results-dir", str(tmp_path),
                "--research-notes", "Inline flag notes.",
                "--output", str(output_path),
                "--bib-path", str(bib_path),
            ])

        assert result.exit_code == 0, result.output
        assert "Researcher Notes:" in captured_prompt[0]
        assert "Inline flag notes." in captured_prompt[0]

    def test_from_session_and_research_notes_merged(self, tmp_path):
        """Session notes appear first; flag notes appended after."""
        self._write_results(tmp_path)
        bib_path = self._write_bib(tmp_path)
        session_path = self._write_session_yaml(tmp_path, "Session note.")
        output_path = tmp_path / "out.md"

        captured_prompt: list[str] = []

        def fake_run(cmd, **kwargs):
            captured_prompt.append(cmd[2])
            return self._mock_proc("## Abstract\n\nTest paper.")

        with patch("subprocess.run", side_effect=fake_run):
            runner = CliRunner()
            result = runner.invoke(cli, [
                "academic-report",
                "--results-dir", str(tmp_path),
                "--from-session", str(session_path),
                "--research-notes", "Flag note.",
                "--output", str(output_path),
                "--bib-path", str(bib_path),
            ])

        assert result.exit_code == 0, result.output
        prompt = captured_prompt[0]
        assert "Researcher Notes:" in prompt
        session_pos = prompt.index("Session note.")
        flag_pos = prompt.index("Flag note.")
        assert session_pos < flag_pos, "Session notes must precede flag notes"

    def test_from_session_with_empty_notes_does_not_prepend(self, tmp_path):
        """No 'Researcher Notes:' block if session has no notes and no --research-notes flag."""
        self._write_results(tmp_path)
        bib_path = self._write_bib(tmp_path)
        session_path = self._write_session_yaml(tmp_path, "")
        output_path = tmp_path / "out.md"

        captured_prompt: list[str] = []

        def fake_run(cmd, **kwargs):
            captured_prompt.append(cmd[2])
            return self._mock_proc("## Abstract\n\nTest paper.")

        with patch("subprocess.run", side_effect=fake_run):
            runner = CliRunner()
            result = runner.invoke(cli, [
                "academic-report",
                "--results-dir", str(tmp_path),
                "--from-session", str(session_path),
                "--output", str(output_path),
                "--bib-path", str(bib_path),
            ])

        assert result.exit_code == 0, result.output
        assert "Researcher Notes:" not in captured_prompt[0]
