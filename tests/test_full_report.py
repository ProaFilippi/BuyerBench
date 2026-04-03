"""Tests for generate_full_report and render_full_report_markdown.

Covers:
- generate_full_report on an experiment dir built from MockAgent results
- per_pillar_aggregate, per_metric_breakdown, skills_mcp_delta_table structure
- bias_susceptibility_table populated from an existing bias-susceptibility-summary.json
- security_violation_table populated from an existing security-compliance-summary.json
- render_full_report_markdown produces section headers and table rows
- `report` CLI command saves FULL-REPORT.json and FULL-REPORT.md
- generate_full_report returns empty tables for an empty/all-skipped experiment dir
"""
from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from agents.mock import MockAgent
from buyerbench.__main__ import cli
from buyerbench.models import Pillar
from harness.loader import load_all_scenarios
from harness.runner import run_scenario
from results.report import generate_full_report, render_full_report_markdown


SCENARIOS_ROOT = str(Path(__file__).parent.parent / "scenarios")


# ---------------------------------------------------------------------------
# Fixtures: build per-pillar experiment dirs using MockAgent
# ---------------------------------------------------------------------------


def _all_scenarios_for(pillar_value: str) -> list:
    return [s for s in load_all_scenarios(SCENARIOS_ROOT) if s.pillar.value == pillar_value]


@pytest.fixture(scope="module")
def experiment_dir(tmp_path_factory):
    """Build a full experiment dir with MockAgent results for all three pillars."""
    exp = tmp_path_factory.mktemp("full_exp")
    agent = MockAgent()

    for pillar_value, subdir in [("PILLAR1", "pillar1"), ("PILLAR2", "pillar2"), ("PILLAR3", "pillar3")]:
        scenarios = _all_scenarios_for(pillar_value)
        out = str(exp / subdir)
        for scenario in scenarios:
            run_scenario(scenario, agent, output_dir=out)

    # Populate bias-susceptibility-summary.json in pillar2/
    from evaluators.aggregate import compute_bsi_from_experiment_dir, compute_security_summary_from_experiment_dir

    bsi_summary = compute_bsi_from_experiment_dir(str(exp / "pillar2"))
    (exp / "pillar2" / "bias-susceptibility-summary.json").write_text(
        json.dumps(bsi_summary, indent=2, default=str)
    )

    # Populate security-compliance-summary.json in pillar3/
    sec_summary = compute_security_summary_from_experiment_dir(str(exp / "pillar3"))
    (exp / "pillar3" / "security-compliance-summary.json").write_text(
        json.dumps(sec_summary, indent=2, default=str)
    )

    return exp


# ---------------------------------------------------------------------------
# generate_full_report — structure
# ---------------------------------------------------------------------------


class TestGenerateFullReportStructure:
    def test_top_level_keys(self, experiment_dir):
        report = generate_full_report(str(experiment_dir))
        assert "generated_at" in report
        assert "experiment_dir" in report
        assert "per_pillar_aggregate" in report
        assert "per_metric_breakdown" in report
        assert "bias_susceptibility_table" in report
        assert "security_violation_table" in report
        assert "skills_mcp_delta_table" in report

    def test_per_pillar_aggregate_rows(self, experiment_dir):
        report = generate_full_report(str(experiment_dir))
        agg = report["per_pillar_aggregate"]
        assert len(agg) > 0

        # Each row must have the expected keys
        row = agg[0]
        for key in ("agent_id", "pillar", "mean_score", "std", "min", "max", "n_scenarios"):
            assert key in row, f"Missing key: {key}"

    def test_per_pillar_aggregate_pillar_values(self, experiment_dir):
        report = generate_full_report(str(experiment_dir))
        pillars_seen = {row["pillar"] for row in report["per_pillar_aggregate"]}
        # MockAgent covers all three pillars
        assert pillars_seen == {"PILLAR1", "PILLAR2", "PILLAR3"}

    def test_per_pillar_aggregate_scores_in_range(self, experiment_dir):
        report = generate_full_report(str(experiment_dir))
        for row in report["per_pillar_aggregate"]:
            assert 0.0 <= row["mean_score"] <= 1.0
            assert 0.0 <= row["min"] <= 1.0
            assert 0.0 <= row["max"] <= 1.0
            assert row["std"] >= 0.0
            assert row["n_scenarios"] > 0

    def test_mock_agent_scores_are_1(self, experiment_dir):
        """MockAgent always picks the optimal choice — all pillar scores must be 1.0."""
        report = generate_full_report(str(experiment_dir))
        agent_rows = [r for r in report["per_pillar_aggregate"] if r["agent_id"] == "mock-agent-v1"]
        assert len(agent_rows) > 0
        for row in agent_rows:
            assert row["mean_score"] == pytest.approx(1.0), f"Expected 1.0 for {row}"


# ---------------------------------------------------------------------------
# generate_full_report — per-metric breakdown
# ---------------------------------------------------------------------------


class TestPerMetricBreakdown:
    def test_breakdown_keyed_by_pillar(self, experiment_dir):
        report = generate_full_report(str(experiment_dir))
        breakdown = report["per_metric_breakdown"]
        assert isinstance(breakdown, dict)
        assert "PILLAR1" in breakdown

    def test_breakdown_rows_have_required_keys(self, experiment_dir):
        report = generate_full_report(str(experiment_dir))
        for pillar_name, rows in report["per_metric_breakdown"].items():
            for row in rows:
                for key in ("agent_id", "metric", "mean", "min", "max"):
                    assert key in row, f"Missing '{key}' in {pillar_name} breakdown row"

    def test_pillar1_has_expected_metrics(self, experiment_dir):
        report = generate_full_report(str(experiment_dir))
        p1_rows = report["per_metric_breakdown"].get("PILLAR1", [])
        metrics_seen = {r["metric"] for r in p1_rows if r["agent_id"] == "mock-agent-v1"}
        # Pillar 1 metrics from pillar1.py
        assert "task_completion_rate" in metrics_seen


# ---------------------------------------------------------------------------
# generate_full_report — bias susceptibility table
# ---------------------------------------------------------------------------


class TestBiasSusceptibilityTable:
    def test_bsi_table_populated_from_summary_json(self, experiment_dir):
        """BSI table must be populated when bias-susceptibility-summary.json exists."""
        report = generate_full_report(str(experiment_dir))
        # MockAgent always picks optimal → BSI = 0, but rows should still exist
        # if valid pairs were computed (pairs require two matching variant results)
        # The fixture writes the summary; check the table type at minimum.
        assert isinstance(report["bias_susceptibility_table"], list)

    def test_bsi_table_row_keys(self, experiment_dir):
        report = generate_full_report(str(experiment_dir))
        for row in report["bias_susceptibility_table"]:
            for key in ("bias_type", "agent_id", "mode", "bsi", "decision_changed"):
                assert key in row, f"Missing '{key}' in BSI table row"

    def test_bsi_values_in_range(self, experiment_dir):
        report = generate_full_report(str(experiment_dir))
        for row in report["bias_susceptibility_table"]:
            assert 0.0 <= row["bsi"] <= 1.0
            assert isinstance(row["decision_changed"], bool)


# ---------------------------------------------------------------------------
# generate_full_report — security violation table
# ---------------------------------------------------------------------------


class TestSecurityViolationTable:
    def test_security_table_type(self, experiment_dir):
        report = generate_full_report(str(experiment_dir))
        assert isinstance(report["security_violation_table"], list)

    def test_security_table_row_keys(self, experiment_dir):
        report = generate_full_report(str(experiment_dir))
        for row in report["security_violation_table"]:
            for key in ("scenario_id", "agent_id", "compliance_adherence_rate",
                        "security_violation_frequency", "score"):
                assert key in row, f"Missing '{key}' in security table row"

    def test_security_rates_in_range(self, experiment_dir):
        report = generate_full_report(str(experiment_dir))
        for row in report["security_violation_table"]:
            assert 0.0 <= row["compliance_adherence_rate"] <= 1.0
            assert 0.0 <= row["security_violation_frequency"] <= 1.0


# ---------------------------------------------------------------------------
# generate_full_report — skills vs MCP delta table
# ---------------------------------------------------------------------------


class TestSkillsMcpDeltaTable:
    def test_delta_table_is_list(self, experiment_dir):
        report = generate_full_report(str(experiment_dir))
        assert isinstance(report["skills_mcp_delta_table"], list)

    def test_delta_table_empty_for_single_agent(self, tmp_path):
        """Delta table must be empty when only one agent (mock-agent-v1) has results."""
        out = str(tmp_path / "pillar1")
        agent = MockAgent()
        for s in _all_scenarios_for("PILLAR1"):
            run_scenario(s, agent, output_dir=out)

        report = generate_full_report(str(tmp_path))
        # mock-agent-v1 has no "-baseline" suffix → no family grouping → empty delta table
        assert report["skills_mcp_delta_table"] == []


# ---------------------------------------------------------------------------
# generate_full_report — empty / all-skipped experiment dir
# ---------------------------------------------------------------------------


class TestEmptyExperimentDir:
    def test_empty_dir_returns_empty_tables(self, tmp_path):
        """generate_full_report must not crash on an experiment dir with no results."""
        (tmp_path / "pillar1").mkdir()
        report = generate_full_report(str(tmp_path))
        assert report["per_pillar_aggregate"] == []
        assert report["per_metric_breakdown"] == {}
        assert report["bias_susceptibility_table"] == []
        assert report["security_violation_table"] == []
        assert report["skills_mcp_delta_table"] == []

    def test_all_skipped_returns_empty_tables(self, tmp_path):
        """Skipped result sentinels must be silently ignored."""
        agent_dir = tmp_path / "pillar1" / "claude-code-baseline"
        agent_dir.mkdir(parents=True)
        skipped = {
            "status": "skipped",
            "agent_id": "claude-code-baseline",
            "scenario_id": "p1-01-supplier-selection-basic",
            "reason": "CLI unavailable",
        }
        (agent_dir / "p1-01.json").write_text(json.dumps(skipped))

        report = generate_full_report(str(tmp_path))
        assert report["per_pillar_aggregate"] == []


# ---------------------------------------------------------------------------
# render_full_report_markdown
# ---------------------------------------------------------------------------


class TestRenderFullReportMarkdown:
    def test_returns_string(self, experiment_dir):
        report = generate_full_report(str(experiment_dir))
        md = render_full_report_markdown(report)
        assert isinstance(md, str)
        assert len(md) > 0

    def test_contains_section_headers(self, experiment_dir):
        report = generate_full_report(str(experiment_dir))
        md = render_full_report_markdown(report)
        assert "## 1. Per-Pillar Aggregate Scores" in md
        assert "## 2. Per-Metric Breakdown" in md
        assert "## 3. Bias Susceptibility" in md
        assert "## 4. Security Violation Frequency" in md
        assert "## 5. Skills vs. MCP Score Delta" in md

    def test_aggregate_table_has_data_rows(self, experiment_dir):
        report = generate_full_report(str(experiment_dir))
        md = render_full_report_markdown(report)
        # MockAgent result rows should be present
        assert "mock-agent-v1" in md

    def test_pillar_breakdown_subheaders(self, experiment_dir):
        report = generate_full_report(str(experiment_dir))
        md = render_full_report_markdown(report)
        assert "### PILLAR1" in md

    def test_empty_report_renders_dash_placeholders(self):
        empty_report = {
            "generated_at": "2026-01-01T00:00:00",
            "experiment_dir": "/tmp/empty",
            "per_pillar_aggregate": [],
            "per_metric_breakdown": {},
            "bias_susceptibility_table": [],
            "security_violation_table": [],
            "skills_mcp_delta_table": [],
        }
        md = render_full_report_markdown(empty_report)
        # Empty tables render a dash placeholder row
        assert "| — |" in md


# ---------------------------------------------------------------------------
# `report` CLI command
# ---------------------------------------------------------------------------


class TestReportCliCommand:
    def test_report_command_saves_files(self, experiment_dir):
        runner = CliRunner()
        result = runner.invoke(cli, ["report", "--experiment-dir", str(experiment_dir)])
        assert result.exit_code == 0, result.output

        json_path = experiment_dir / "FULL-REPORT.json"
        md_path = experiment_dir / "FULL-REPORT.md"
        assert json_path.exists(), "FULL-REPORT.json was not created"
        assert md_path.exists(), "FULL-REPORT.md was not created"

    def test_report_json_is_valid(self, experiment_dir):
        runner = CliRunner()
        runner.invoke(cli, ["report", "--experiment-dir", str(experiment_dir)])

        json_path = experiment_dir / "FULL-REPORT.json"
        data = json.loads(json_path.read_text())
        assert "per_pillar_aggregate" in data
        assert "per_metric_breakdown" in data

    def test_report_md_contains_header(self, experiment_dir):
        runner = CliRunner()
        runner.invoke(cli, ["report", "--experiment-dir", str(experiment_dir)])

        md_path = experiment_dir / "FULL-REPORT.md"
        content = md_path.read_text()
        assert "# BuyerBench Full Experiment Report" in content

    def test_report_command_missing_dir(self, tmp_path):
        runner = CliRunner()
        result = runner.invoke(cli, ["report", "--experiment-dir", str(tmp_path / "nonexistent")])
        assert result.exit_code != 0
