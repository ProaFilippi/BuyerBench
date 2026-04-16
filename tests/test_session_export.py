"""Tests for results.session_export and results.academic_tables."""
from __future__ import annotations

import csv
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import pytest
from rich.console import Console

from buyerbench.models import EvaluationResult, Pillar, PillarScore, ScenarioVariant
from results.academic_tables import render_model_comparison_table
from results.session_export import (
    SessionMetadata,
    export_session_csv,
    export_session_markdown,
    generate_session_id,
)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _make_result(
    scenario_id: str,
    agent_id: str,
    pillar: Pillar = Pillar.PILLAR1,
    score: float = 0.8,
    overall_pass: bool = True,
) -> EvaluationResult:
    return EvaluationResult(
        scenario_id=scenario_id,
        agent_id=agent_id,
        pillar_scores=[
            PillarScore(pillar=pillar, score=score, metrics={}, violations=[], notes="")
        ],
        overall_pass=overall_pass,
        timestamp=datetime.now(timezone.utc),
        variant_pair_id=None,
    )


def _make_meta(session_id: str = "session-20260408-120000", output_dir: str = "/tmp") -> SessionMetadata:
    now = datetime.now(timezone.utc)
    return SessionMetadata(
        session_id=session_id,
        agents=["mock-agent-v1"],
        scenarios_run=3,
        pillars=[1],
        started_at=now,
        completed_at=now,
        output_dir=output_dir,
    )


def _make_mock_results(
    agents: list[str] | None = None,
    n_scenarios: int = 3,
) -> list[EvaluationResult]:
    agents = agents or ["agent-a", "agent-b"]
    results = []
    for agent_id in agents:
        for i in range(1, n_scenarios + 1):
            results.append(
                _make_result(
                    scenario_id=f"p1-0{i}",
                    agent_id=agent_id,
                    score=0.6 + 0.1 * i,
                )
            )
    return results


# ── Tests ──────────────────────────────────────────────────────────────────────

def test_generate_session_id_format():
    sid = generate_session_id()
    assert re.match(r"session-\d{8}-\d{6}", sid), f"Unexpected format: {sid}"


def test_export_session_csv_columns():
    results = _make_mock_results(agents=["agent-a", "agent-b"], n_scenarios=3)
    assert len(results) == 6

    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False, mode="w") as f:
        csv_path = f.name

    meta = _make_meta(output_dir="/tmp")
    export_session_csv(results, meta, csv_path)

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    expected_columns = {
        "session_id",
        "agent_id",
        "scenario_id",
        "run_index",
        "run_id",
        "supplier_order_seed",
        "pillar",
        "variant",
        "variant_pair_id",
        "bias_category",
        "score",
        "overall_pass",
        "temperature",
        "token_count_input",
        "token_count_output",
        "api_cost_usd",
        "error_flag",
        "model_version",
        "latency_ms",
        "timestamp",
    }
    assert expected_columns == set(reader.fieldnames or []), (
        f"Missing columns: {expected_columns - set(reader.fieldnames or [])}"
    )
    assert len(rows) == 6, f"Expected 6 rows, got {len(rows)}"


def test_export_session_markdown_front_matter():
    results = _make_mock_results(n_scenarios=2)
    with tempfile.NamedTemporaryFile(suffix=".md", delete=False, mode="w") as f:
        md_path = f.name

    meta = _make_meta()
    export_session_markdown(results, meta, md_path)

    content = Path(md_path).read_text(encoding="utf-8")

    assert content.startswith("---"), "Front matter must begin with ---"
    assert "type: report" in content
    assert "[[FULL-REPORT]]" in content


def test_export_session_markdown_sections():
    results = _make_mock_results(n_scenarios=2)
    with tempfile.NamedTemporaryFile(suffix=".md", delete=False, mode="w") as f:
        md_path = f.name

    meta = _make_meta()
    export_session_markdown(results, meta, md_path)

    content = Path(md_path).read_text(encoding="utf-8")

    assert "## Summary" in content
    assert "## Results by Pillar" in content
    assert "## Per-Scenario Breakdown" in content


def test_academic_table_smoke():
    results = _make_mock_results(agents=["mock-agent-v1", "claude-code-baseline"], n_scenarios=3)
    con = Console(record=True)
    render_model_comparison_table(results, con)
    output = con.export_text()
    assert "★" in output, "Expected ★ top-performer marker in table output"


def test_session_report_command():
    from click.testing import CliRunner
    from buyerbench.__main__ import cli

    runner = CliRunner()
    result = runner.invoke(cli, ["session-report", "--help"])
    assert result.exit_code == 0, f"Expected exit 0, got {result.exit_code}\n{result.output}"
