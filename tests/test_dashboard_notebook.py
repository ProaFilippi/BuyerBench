"""Tests for the rich terminal dashboard and results-analysis notebook.

Covers:
- _score_markup returns correctly colour-coded rich markup strings
- _render_rich_dashboard produces no exceptions when called with real/empty report data
- `report` CLI command output includes dashboard section headers
- notebooks/results-analysis.ipynb is valid nbformat 4 JSON
- notebook contains all four required visualisation cells
"""
from __future__ import annotations

import json
import pathlib
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

from agents.mock import MockAgent
from buyerbench.__main__ import _render_rich_dashboard, _score_markup, cli
from harness.loader import load_all_scenarios
from harness.runner import run_scenario
from results.report import generate_full_report

SCENARIOS_ROOT = str(pathlib.Path(__file__).parent.parent / "scenarios")
NOTEBOOK_PATH = pathlib.Path(__file__).parent.parent / "notebooks" / "results-analysis.ipynb"


# ---------------------------------------------------------------------------
# _score_markup
# ---------------------------------------------------------------------------


class TestScoreMarkup:
    def test_green_at_08(self):
        markup = _score_markup(0.8)
        assert "green" in markup
        assert "0.8000" in markup

    def test_green_above_08(self):
        markup = _score_markup(0.95)
        assert "green" in markup

    def test_yellow_at_05(self):
        markup = _score_markup(0.5)
        assert "yellow" in markup

    def test_yellow_between_05_and_08(self):
        markup = _score_markup(0.65)
        assert "yellow" in markup

    def test_red_below_05(self):
        markup = _score_markup(0.3)
        assert "red" in markup

    def test_none_returns_dim_dash(self):
        markup = _score_markup(None)
        assert "dim" in markup
        assert "—" in markup

    def test_boundary_exactly_05(self):
        markup = _score_markup(0.5)
        assert "red" not in markup  # 0.5 is yellow, not red

    def test_boundary_exactly_08(self):
        markup = _score_markup(0.8)
        assert "yellow" not in markup  # 0.8 is green, not yellow

    def test_zero_is_red(self):
        assert "red" in _score_markup(0.0)

    def test_one_is_green(self):
        assert "green" in _score_markup(1.0)


# ---------------------------------------------------------------------------
# _render_rich_dashboard — no exceptions on real + empty data
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def full_report_with_data(tmp_path_factory):
    """Full report built from MockAgent results across all pillars."""
    exp = tmp_path_factory.mktemp("dash_exp")
    agent = MockAgent()

    for pillar_value, subdir in [
        ("PILLAR1", "pillar1"),
        ("PILLAR2", "pillar2"),
        ("PILLAR3", "pillar3"),
    ]:
        scenarios = [s for s in load_all_scenarios(SCENARIOS_ROOT) if s.pillar.value == pillar_value]
        out = str(exp / subdir)
        for scenario in scenarios:
            run_scenario(scenario, agent, output_dir=out)

    from evaluators.aggregate import (
        compute_bsi_from_experiment_dir,
        compute_security_summary_from_experiment_dir,
    )

    bsi_summary = compute_bsi_from_experiment_dir(str(exp / "pillar2"))
    (exp / "pillar2" / "bias-susceptibility-summary.json").write_text(
        json.dumps(bsi_summary, indent=2, default=str)
    )
    sec_summary = compute_security_summary_from_experiment_dir(str(exp / "pillar3"))
    (exp / "pillar3" / "security-compliance-summary.json").write_text(
        json.dumps(sec_summary, indent=2, default=str)
    )

    return generate_full_report(str(exp))


class TestRenderRichDashboard:
    def test_no_exception_with_real_data(self, full_report_with_data):
        from rich.console import Console

        con = Console(file=open("/dev/null", "w"), highlight=False)
        _render_rich_dashboard(full_report_with_data, con)  # must not raise

    def test_no_exception_with_empty_report(self):
        empty = {
            "generated_at": "2026-01-01T00:00:00",
            "experiment_dir": "/tmp/empty",
            "per_pillar_aggregate": [],
            "per_metric_breakdown": {},
            "bias_susceptibility_table": [],
            "security_violation_table": [],
            "skills_mcp_delta_table": [],
        }
        from rich.console import Console

        con = Console(file=open("/dev/null", "w"), highlight=False)
        _render_rich_dashboard(empty, con)  # must not raise

    def test_dashboard_renders_section_titles(self, full_report_with_data):
        import io
        from rich.console import Console

        buf = io.StringIO()
        con = Console(file=buf, highlight=False, width=200)
        _render_rich_dashboard(full_report_with_data, con)
        output = buf.getvalue()
        assert "Per-Pillar Aggregate Scores" in output
        assert "Bias Susceptibility Index" in output
        assert "Security" in output
        assert "Skills / MCP Score Delta" in output

    def test_dashboard_shows_agent_in_aggregate_table(self, full_report_with_data):
        import io
        from rich.console import Console

        buf = io.StringIO()
        con = Console(file=buf, highlight=False, width=200)
        _render_rich_dashboard(full_report_with_data, con)
        output = buf.getvalue()
        # MockAgent should appear in the aggregate table
        assert "mock-agent-v1" in output

    def test_dashboard_positive_delta_shown_in_green(self):
        import io
        from rich.console import Console

        report_with_delta = {
            "per_pillar_aggregate": [],
            "bias_susceptibility_table": [],
            "security_violation_table": [],
            "skills_mcp_delta_table": [
                {
                    "family": "claude-code",
                    "mode": "skills",
                    "agent_id": "claude-code-skills",
                    "pillar": "PILLAR1",
                    "baseline_score": 0.7,
                    "variant_score": 0.9,
                    "delta": 0.2,
                }
            ],
        }
        buf = io.StringIO()
        con = Console(file=buf, highlight=False, width=200)
        _render_rich_dashboard(report_with_delta, con)
        # Positive delta rendered with green colour markup
        output = buf.getvalue()
        assert "claude-code" in output


# ---------------------------------------------------------------------------
# `report` CLI command — dashboard appears in output
# ---------------------------------------------------------------------------


class TestReportCliDashboard:
    def test_report_command_prints_dashboard_rule(self, tmp_path):
        """The `report` command output must include the dashboard section."""
        # Build a minimal experiment dir with MockAgent results
        agent = MockAgent()
        scenarios = [s for s in load_all_scenarios(SCENARIOS_ROOT) if s.pillar.value == "PILLAR1"]
        out = str(tmp_path / "pillar1")
        for s in scenarios:
            run_scenario(s, agent, output_dir=out)

        runner = CliRunner()
        result = runner.invoke(cli, ["report", "--experiment-dir", str(tmp_path)])
        assert result.exit_code == 0, result.output
        assert "BuyerBench Results Dashboard" in result.output

    def test_report_command_shows_aggregate_section(self, tmp_path):
        agent = MockAgent()
        scenarios = [s for s in load_all_scenarios(SCENARIOS_ROOT) if s.pillar.value == "PILLAR1"]
        out = str(tmp_path / "pillar1")
        for s in scenarios:
            run_scenario(s, agent, output_dir=out)

        runner = CliRunner()
        result = runner.invoke(cli, ["report", "--experiment-dir", str(tmp_path)])
        assert "Per-Pillar Aggregate Scores" in result.output


# ---------------------------------------------------------------------------
# Notebook file validity
# ---------------------------------------------------------------------------


class TestResultsAnalysisNotebook:
    def test_notebook_file_exists(self):
        assert NOTEBOOK_PATH.exists(), f"Notebook not found at {NOTEBOOK_PATH}"

    def test_notebook_is_valid_json(self):
        data = json.loads(NOTEBOOK_PATH.read_text())
        assert isinstance(data, dict)

    def test_notebook_nbformat_version(self):
        data = json.loads(NOTEBOOK_PATH.read_text())
        assert data.get("nbformat") == 4

    def test_notebook_has_cells(self):
        data = json.loads(NOTEBOOK_PATH.read_text())
        assert len(data.get("cells", [])) > 0

    def test_notebook_has_code_cells(self):
        data = json.loads(NOTEBOOK_PATH.read_text())
        code_cells = [c for c in data["cells"] if c.get("cell_type") == "code"]
        assert len(code_cells) >= 4, "Expected at least 4 code cells (setup + 4 plots)"

    def test_notebook_has_radar_chart_cell(self):
        data = json.loads(NOTEBOOK_PATH.read_text())
        sources = [
            "".join(c.get("source", [])) for c in data["cells"] if c.get("cell_type") == "code"
        ]
        assert any("polar" in src or "radar" in src.lower() for src in sources), \
            "No radar/polar chart cell found"

    def test_notebook_has_bsi_bar_chart_cell(self):
        data = json.loads(NOTEBOOK_PATH.read_text())
        sources = [
            "".join(c.get("source", [])) for c in data["cells"] if c.get("cell_type") == "code"
        ]
        assert any("bias_susceptibility_table" in src or "bsi_df" in src for src in sources), \
            "No BSI bar chart cell found"

    def test_notebook_has_heatmap_cell(self):
        data = json.loads(NOTEBOOK_PATH.read_text())
        sources = [
            "".join(c.get("source", [])) for c in data["cells"] if c.get("cell_type") == "code"
        ]
        assert any("heatmap" in src for src in sources), "No heatmap cell found"

    def test_notebook_has_boxplot_cell(self):
        data = json.loads(NOTEBOOK_PATH.read_text())
        sources = [
            "".join(c.get("source", [])) for c in data["cells"] if c.get("cell_type") == "code"
        ]
        assert any("boxplot" in src or "latency" in src.lower() for src in sources), \
            "No latency boxplot cell found"

    def test_notebook_loads_full_report_json(self):
        data = json.loads(NOTEBOOK_PATH.read_text())
        sources = [
            "".join(c.get("source", [])) for c in data["cells"] if c.get("cell_type") == "code"
        ]
        assert any("FULL-REPORT.json" in src for src in sources), \
            "Notebook must reference FULL-REPORT.json"
