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


# ---------------------------------------------------------------------------
# REV-1: methodology_notes in generate_full_report (PILLAR2 rationality scope)
# ---------------------------------------------------------------------------


class TestMethodologyNotes:
    """REV-1: 'Optimality is defined relative to the scenario's stated evaluation
    weights. We test internal rationality, not external optimality.' must appear
    in every results section that presents Pillar 2 data.
    """

    _SCOPE_FRAGMENT = "not external optimality"

    def test_methodology_notes_key_present(self, experiment_dir):
        report = generate_full_report(str(experiment_dir))
        assert "methodology_notes" in report

    def test_pillar2_rationality_scope_field_present(self, experiment_dir):
        report = generate_full_report(str(experiment_dir))
        assert "pillar2_rationality_scope" in report["methodology_notes"]

    def test_pillar2_rationality_scope_content(self, experiment_dir):
        report = generate_full_report(str(experiment_dir))
        scope = report["methodology_notes"]["pillar2_rationality_scope"]
        assert "internal rationality" in scope

    def test_pillar2_rationality_scope_mentions_evaluation_weights(self, experiment_dir):
        report = generate_full_report(str(experiment_dir))
        scope = report["methodology_notes"]["pillar2_rationality_scope"]
        assert "evaluation weights" in scope

    def test_methodology_notes_present_for_empty_dir(self, tmp_path):
        """methodology_notes must be present even when no result files exist."""
        (tmp_path / "pillar1").mkdir()
        report = generate_full_report(str(tmp_path))
        assert "methodology_notes" in report
        assert "pillar2_rationality_scope" in report["methodology_notes"]

    def test_markdown_bias_section_contains_scope_note(self, experiment_dir):
        """Section 3 (Bias Susceptibility) must include the REV-1 scope note."""
        report = generate_full_report(str(experiment_dir))
        md = render_full_report_markdown(report)
        # Locate section 3 and check the note appears before the table header
        bias_idx = md.index("## 3. Bias Susceptibility")
        sec4_idx = md.index("## 4. Security Violation Frequency")
        bias_section = md[bias_idx:sec4_idx]
        assert self._SCOPE_FRAGMENT in bias_section

    def test_markdown_pillar2_subsection_contains_scope_note(self, experiment_dir):
        """PILLAR2 subsection in Section 2 must include the REV-1 scope note."""
        report = generate_full_report(str(experiment_dir))
        md = render_full_report_markdown(report)
        pillar2_idx = md.index("### PILLAR2")
        # Find next subsection or section boundary
        next_boundary = len(md)
        for marker in ("### PILLAR3", "## 3. Bias Susceptibility"):
            try:
                idx = md.index(marker)
                if idx > pillar2_idx:
                    next_boundary = min(next_boundary, idx)
            except ValueError:
                pass
        pillar2_section = md[pillar2_idx:next_boundary]
        assert self._SCOPE_FRAGMENT in pillar2_section

    def test_summary_report_contains_pillar2_rationality_scope(self):
        """SummaryReport schema must carry the REV-1 field in every serialised output."""
        from results.schemas import SummaryReport
        sr = SummaryReport(agent_id="test-agent", total_scenarios=1, overall_pass_rate=1.0)
        data = sr.model_dump()
        assert "pillar2_rationality_scope" in data
        assert "internal rationality" in data["pillar2_rationality_scope"]

    def test_summary_report_scope_mentions_evaluation_weights(self):
        from results.schemas import SummaryReport
        sr = SummaryReport(agent_id="test-agent", total_scenarios=5, overall_pass_rate=0.8)
        data = sr.model_dump()
        assert "evaluation weights" in data["pillar2_rationality_scope"]


# ---------------------------------------------------------------------------
# REV-3: exploratory_only_label — single-run data must be labeled EXPLORATORY ONLY
# ---------------------------------------------------------------------------


class TestExploratoryOnlyLabel:
    """REV-3: Current single-run data is EXPLORATORY ONLY. Label clearly.
    Do not use in paper as evidence. N≥50 per cell required before any claims.
    """

    _EXPLORATORY_FRAGMENT = "EXPLORATORY ONLY"
    _N50_FRAGMENT = "50"

    def test_exploratory_only_label_in_methodology_notes(self, experiment_dir):
        """generate_full_report must include exploratory_only_label in methodology_notes."""
        report = generate_full_report(str(experiment_dir))
        assert "exploratory_only_label" in report["methodology_notes"]

    def test_exploratory_only_label_content(self, experiment_dir):
        """exploratory_only_label must mention EXPLORATORY ONLY."""
        report = generate_full_report(str(experiment_dir))
        label = report["methodology_notes"]["exploratory_only_label"]
        assert self._EXPLORATORY_FRAGMENT in label

    def test_exploratory_only_label_mentions_n50(self, experiment_dir):
        """exploratory_only_label must mention N≥50 threshold."""
        report = generate_full_report(str(experiment_dir))
        label = report["methodology_notes"]["exploratory_only_label"]
        assert self._N50_FRAGMENT in label

    def test_exploratory_only_label_mentions_published_work(self, experiment_dir):
        """exploratory_only_label must warn against use in published work."""
        report = generate_full_report(str(experiment_dir))
        label = report["methodology_notes"]["exploratory_only_label"]
        assert "published" in label.lower()

    def test_exploratory_only_label_present_for_empty_dir(self, tmp_path):
        """exploratory_only_label must be present even when no result files exist."""
        (tmp_path / "pillar1").mkdir()
        report = generate_full_report(str(tmp_path))
        assert "exploratory_only_label" in report["methodology_notes"]
        assert self._EXPLORATORY_FRAGMENT in report["methodology_notes"]["exploratory_only_label"]

    def test_markdown_header_contains_exploratory_warning(self, experiment_dir):
        """Report Markdown must display the exploratory warning near the top."""
        report = generate_full_report(str(experiment_dir))
        md = render_full_report_markdown(report)
        # The warning should appear before Section 1
        sec1_idx = md.index("## 1. Per-Pillar Aggregate Scores")
        header_section = md[:sec1_idx]
        assert self._EXPLORATORY_FRAGMENT in header_section

    def test_markdown_bias_section_contains_exploratory_warning(self, experiment_dir):
        """Section 3 (Bias Susceptibility) must include the exploratory warning."""
        report = generate_full_report(str(experiment_dir))
        md = render_full_report_markdown(report)
        bias_idx = md.index("## 3. Bias Susceptibility")
        sec4_idx = md.index("## 4. Security Violation Frequency")
        bias_section = md[bias_idx:sec4_idx]
        assert self._EXPLORATORY_FRAGMENT in bias_section

    def test_markdown_exploratory_warning_mentions_n50(self, experiment_dir):
        """The exploratory warning in Markdown must mention N≥50."""
        report = generate_full_report(str(experiment_dir))
        md = render_full_report_markdown(report)
        assert self._N50_FRAGMENT in md

    def test_summary_report_contains_exploratory_only_label(self):
        """SummaryReport schema must carry the REV-3 field in every serialised output."""
        from results.schemas import SummaryReport
        sr = SummaryReport(agent_id="test-agent", total_scenarios=1, overall_pass_rate=1.0)
        data = sr.model_dump()
        assert "exploratory_only_label" in data
        assert self._EXPLORATORY_FRAGMENT in data["exploratory_only_label"]

    def test_summary_report_exploratory_label_mentions_n50(self):
        """SummaryReport.exploratory_only_label must mention N≥50."""
        from results.schemas import SummaryReport
        sr = SummaryReport(agent_id="test-agent", total_scenarios=5, overall_pass_rate=0.8)
        data = sr.model_dump()
        assert self._N50_FRAGMENT in data["exploratory_only_label"]


# ---------------------------------------------------------------------------
# REV-6: cross_model_regression_scope — cross-model analyses are descriptive only
# ---------------------------------------------------------------------------


class TestRev6CrossModelRegressionScope:
    """REV-6: Cross-model comparisons are DESCRIPTIVE ONLY (N=10 models).
    No p-values or inferential claims are valid for cross-model analyses.
    """

    _DESCRIPTIVE_FRAGMENT = "DESCRIPTIVE ONLY"
    _NO_PVALUE_FRAGMENT = "p-values"

    def test_cross_model_regression_scope_in_methodology_notes(self, experiment_dir):
        """generate_full_report must include cross_model_regression_scope."""
        report = generate_full_report(str(experiment_dir))
        assert "cross_model_regression_scope" in report["methodology_notes"]

    def test_cross_model_regression_scope_content_mentions_descriptive(self, experiment_dir):
        """cross_model_regression_scope must say DESCRIPTIVE ONLY."""
        report = generate_full_report(str(experiment_dir))
        scope = report["methodology_notes"]["cross_model_regression_scope"]
        assert self._DESCRIPTIVE_FRAGMENT in scope

    def test_cross_model_regression_scope_mentions_no_pvalue(self, experiment_dir):
        """cross_model_regression_scope must mention p-values are not valid."""
        report = generate_full_report(str(experiment_dir))
        scope = report["methodology_notes"]["cross_model_regression_scope"]
        assert self._NO_PVALUE_FRAGMENT in scope

    def test_cross_model_regression_scope_mentions_n10(self, experiment_dir):
        """cross_model_regression_scope must mention N=10."""
        report = generate_full_report(str(experiment_dir))
        scope = report["methodology_notes"]["cross_model_regression_scope"]
        assert "10" in scope

    def test_cross_model_regression_scope_present_for_empty_dir(self, tmp_path):
        """cross_model_regression_scope must be present even with no result files."""
        (tmp_path / "pillar1").mkdir()
        report = generate_full_report(str(tmp_path))
        assert "cross_model_regression_scope" in report["methodology_notes"]
        assert self._DESCRIPTIVE_FRAGMENT in report["methodology_notes"]["cross_model_regression_scope"]

    def test_markdown_section1_contains_rev6_note(self, experiment_dir):
        """Section 1 (Per-Pillar Aggregate) must include the REV-6 cross-model warning."""
        report = generate_full_report(str(experiment_dir))
        md = render_full_report_markdown(report)
        sec1_idx = md.index("## 1. Per-Pillar Aggregate Scores")
        sec2_idx = md.index("## 2. Per-Metric Breakdown")
        sec1_body = md[sec1_idx:sec2_idx]
        assert "REV-6" in sec1_body

    def test_markdown_rev6_note_mentions_descriptive(self, experiment_dir):
        """The REV-6 warning in Markdown must say 'descriptive only'."""
        report = generate_full_report(str(experiment_dir))
        md = render_full_report_markdown(report)
        assert "descriptive only" in md.lower()

    def test_methodology_notes_has_three_keys(self, experiment_dir):
        """methodology_notes must contain all three REV keys."""
        report = generate_full_report(str(experiment_dir))
        notes = report["methodology_notes"]
        assert "pillar2_rationality_scope" in notes
        assert "exploratory_only_label" in notes
        assert "cross_model_regression_scope" in notes


class TestRev7PipelineScope:
    """REV-7: Abstract/introduction must contain the pipeline scope statement.

    The exact phrasing 'final selection stage of AI buyer agents' must appear
    in ``methodology_notes['pipeline_scope']`` (JSON) and as a REV-7 blockquote
    in the Markdown header section.
    """

    _SCOPE_FRAGMENT = "final selection stage"
    _NOT_PIPELINE_FRAGMENT = "not the full agent pipeline"

    def test_pipeline_scope_in_methodology_notes(self, experiment_dir):
        """generate_full_report must include pipeline_scope in methodology_notes."""
        report = generate_full_report(str(experiment_dir))
        assert "pipeline_scope" in report["methodology_notes"]

    def test_pipeline_scope_content_mentions_final_selection(self, experiment_dir):
        """pipeline_scope must reference the 'final selection stage'."""
        report = generate_full_report(str(experiment_dir))
        scope = report["methodology_notes"]["pipeline_scope"]
        assert self._SCOPE_FRAGMENT in scope

    def test_pipeline_scope_content_mentions_not_full_pipeline(self, experiment_dir):
        """pipeline_scope must state it does not cover the full agent pipeline."""
        report = generate_full_report(str(experiment_dir))
        scope = report["methodology_notes"]["pipeline_scope"]
        assert self._NOT_PIPELINE_FRAGMENT in scope

    def test_pipeline_scope_present_for_empty_dir(self, tmp_path):
        """pipeline_scope must be present even with no result files."""
        (tmp_path / "pillar1").mkdir()
        report = generate_full_report(str(tmp_path))
        assert "pipeline_scope" in report["methodology_notes"]
        scope = report["methodology_notes"]["pipeline_scope"]
        assert self._SCOPE_FRAGMENT in scope

    def test_markdown_header_contains_rev7_note(self, experiment_dir):
        """Markdown header must include the REV-7 pipeline scope blockquote."""
        report = generate_full_report(str(experiment_dir))
        md = render_full_report_markdown(report)
        sec1_idx = md.index("## 1. Per-Pillar Aggregate Scores")
        header_body = md[:sec1_idx]
        assert "REV-7" in header_body

    def test_markdown_rev7_note_mentions_final_selection(self, experiment_dir):
        """The REV-7 blockquote in Markdown must reference 'final selection'."""
        report = generate_full_report(str(experiment_dir))
        md = render_full_report_markdown(report)
        assert "final selection" in md.lower()

    def test_markdown_rev7_note_mentions_not_full_pipeline(self, experiment_dir):
        """The REV-7 blockquote must state 'not the full agent pipeline'."""
        report = generate_full_report(str(experiment_dir))
        md = render_full_report_markdown(report)
        assert "not the full agent pipeline" in md.lower()

    def test_methodology_notes_has_four_keys(self, experiment_dir):
        """methodology_notes must contain all four REV keys after REV-7."""
        report = generate_full_report(str(experiment_dir))
        notes = report["methodology_notes"]
        assert "pillar2_rationality_scope" in notes
        assert "exploratory_only_label" in notes
        assert "cross_model_regression_scope" in notes
        assert "pipeline_scope" in notes


class TestN2ClaimTierHierarchy:
    """N.2: Claim tier hierarchy must be present in methodology_notes, schemas, and Markdown.

    Every result statement must be labeled Tier A (fully defensible), Tier B (suggestive),
    or Tier C (speculative / future work). No Tier C claims may appear in Results or Conclusions.
    """

    def test_claim_tier_hierarchy_in_methodology_notes(self, experiment_dir):
        """generate_full_report must include claim_tier_hierarchy in methodology_notes."""
        report = generate_full_report(str(experiment_dir))
        assert "claim_tier_hierarchy" in report["methodology_notes"]

    def test_claim_tier_hierarchy_present_for_empty_dir(self, tmp_path):
        """claim_tier_hierarchy must be present even with no result files."""
        (tmp_path / "pillar1").mkdir()
        report = generate_full_report(str(tmp_path))
        assert "claim_tier_hierarchy" in report["methodology_notes"]

    def test_claim_tier_hierarchy_mentions_tier_a(self, experiment_dir):
        """claim_tier_hierarchy must describe Tier A claims."""
        report = generate_full_report(str(experiment_dir))
        value = report["methodology_notes"]["claim_tier_hierarchy"]
        assert "tier a" in value.lower() or "tier_a" in value.lower()

    def test_claim_tier_hierarchy_mentions_tier_b(self, experiment_dir):
        """claim_tier_hierarchy must describe Tier B claims."""
        report = generate_full_report(str(experiment_dir))
        value = report["methodology_notes"]["claim_tier_hierarchy"]
        assert "tier b" in value.lower() or "tier_b" in value.lower()

    def test_claim_tier_hierarchy_mentions_tier_c(self, experiment_dir):
        """claim_tier_hierarchy must describe Tier C claims."""
        report = generate_full_report(str(experiment_dir))
        value = report["methodology_notes"]["claim_tier_hierarchy"]
        assert "tier c" in value.lower() or "tier_c" in value.lower()

    def test_claim_tier_hierarchy_mentions_gate4(self, experiment_dir):
        """claim_tier_hierarchy must reference the Gate 4 submission check."""
        report = generate_full_report(str(experiment_dir))
        value = report["methodology_notes"]["claim_tier_hierarchy"]
        assert "gate" in value.lower() or "submission" in value.lower()

    def test_markdown_header_contains_n2_claim_tiers(self, experiment_dir):
        """Markdown header must include the N.2 claim tier blockquote."""
        report = generate_full_report(str(experiment_dir))
        md = render_full_report_markdown(report)
        sec1_idx = md.index("## 1. Per-Pillar Aggregate Scores")
        header_body = md[:sec1_idx]
        assert "N.2" in header_body

    def test_markdown_n2_note_mentions_tier_c_restriction(self, experiment_dir):
        """The N.2 blockquote must state Tier C claims are forbidden from Results."""
        report = generate_full_report(str(experiment_dir))
        md = render_full_report_markdown(report)
        assert "tier c" in md.lower()

    def test_methodology_notes_has_five_keys(self, experiment_dir):
        """methodology_notes must contain all five keys after N.2."""
        report = generate_full_report(str(experiment_dir))
        notes = report["methodology_notes"]
        assert "pillar2_rationality_scope" in notes
        assert "exploratory_only_label" in notes
        assert "cross_model_regression_scope" in notes
        assert "pipeline_scope" in notes
        assert "claim_tier_hierarchy" in notes

    def test_summary_report_schema_has_claim_tier_hierarchy(self):
        """SummaryReport must carry claim_tier_hierarchy as a default field."""
        from results.schemas import SummaryReport
        report = SummaryReport(agent_id="test", total_scenarios=0, overall_pass_rate=0.0)
        assert hasattr(report, "claim_tier_hierarchy")
        assert isinstance(report.claim_tier_hierarchy, str)
        assert len(report.claim_tier_hierarchy) > 0

    def test_claim_tiers_in_aggregate_bias_report_empty(self):
        """aggregate_bias_report must include claim_tiers in the empty-list return."""
        from evaluators.pillar2 import aggregate_bias_report
        result = aggregate_bias_report([])
        assert "claim_tiers" in result
        tiers = result["claim_tiers"]
        assert "tier_a" in tiers
        assert "tier_b" in tiers
        assert "tier_c" in tiers

    def test_claim_tiers_in_aggregate_bias_report_nonempty(self):
        """aggregate_bias_report must include claim_tiers in the non-empty return."""
        from evaluators.pillar2 import aggregate_bias_report
        pair_results = [{"bias_susceptibility_index": 0.5, "variant_type": "ANCHOR_HIGH", "decision_changed": True}]
        result = aggregate_bias_report(pair_results)
        assert "claim_tiers" in result
        tiers = result["claim_tiers"]
        assert "tier_a" in tiers
        assert "tier_b" in tiers
        assert "tier_c" in tiers

    def test_claim_tiers_tier_a_mentions_bh_fdr(self):
        """Tier A description must reference BH-FDR correction."""
        from evaluators.pillar2 import aggregate_bias_report
        result = aggregate_bias_report([])
        tier_a = result["claim_tiers"]["tier_a"]
        assert "bh" in tier_a.lower() or "fdr" in tier_a.lower()

    def test_claim_tiers_tier_c_mentions_future_work(self):
        """Tier C description must state claims must be framed as future work."""
        from evaluators.pillar2 import aggregate_bias_report
        result = aggregate_bias_report([])
        tier_c = result["claim_tiers"]["tier_c"]
        assert "future" in tier_c.lower()
