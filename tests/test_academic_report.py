"""Tests for buyerbench.academic_report."""
from __future__ import annotations

import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from buyerbench.academic_report import build_academic_prompt, generate_academic_report


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
