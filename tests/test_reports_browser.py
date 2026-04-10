"""Tests for buyerbench.reports_browser."""
from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from buyerbench.reports_browser import (
    _collect_metadata,
    _find_experiment_dirs,
    _indicator,
    browse_reports,
)


# ── _indicator ────────────────────────────────────────────────────────────────

class TestIndicator:
    def test_true_returns_check(self):
        result = _indicator(True)
        assert "✓" in result.plain

    def test_false_returns_dash(self):
        result = _indicator(False)
        assert "—" in result.plain


# ── _find_experiment_dirs ─────────────────────────────────────────────────────

class TestFindExperimentDirs:
    def test_returns_empty_when_no_results(self, tmp_path):
        results = tmp_path / "results"
        results.mkdir()
        assert _find_experiment_dirs(results) == []

    def test_returns_empty_when_results_missing(self, tmp_path):
        assert _find_experiment_dirs(tmp_path / "nonexistent") == []

    def test_finds_direct_children_with_json(self, tmp_path):
        results = tmp_path / "results"
        exp = results / "my-experiment"
        exp.mkdir(parents=True)
        (exp / "result.json").write_text(json.dumps({"agent_id": "a1"}))
        found = _find_experiment_dirs(results)
        assert exp in found

    def test_ignores_children_without_json(self, tmp_path):
        results = tmp_path / "results"
        empty = results / "empty"
        empty.mkdir(parents=True)
        found = _find_experiment_dirs(results)
        assert empty not in found

    def test_also_scans_experiments_subdirectories(self, tmp_path):
        results = tmp_path / "results"
        grouped = results / "experiments" / "sub-exp"
        grouped.mkdir(parents=True)
        (grouped / "result.json").write_text(json.dumps({"agent_id": "a2"}))
        found = _find_experiment_dirs(results)
        assert grouped in found

    def test_excludes_experiments_grouping_dir_itself(self, tmp_path):
        results = tmp_path / "results"
        experiments = results / "experiments"
        experiments.mkdir(parents=True)
        # Put a json at the grouping level — it should be excluded
        (experiments / "summary.json").write_text(json.dumps({}))
        sub = experiments / "real-exp"
        sub.mkdir()
        (sub / "result.json").write_text(json.dumps({"agent_id": "a3"}))
        found = _find_experiment_dirs(results)
        assert experiments not in found
        assert sub in found

    def test_no_duplicates(self, tmp_path):
        results = tmp_path / "results"
        exp = results / "exp1"
        exp.mkdir(parents=True)
        (exp / "r.json").write_text(json.dumps({"agent_id": "a"}))
        found = _find_experiment_dirs(results)
        assert len(found) == len(set(found))


# ── _collect_metadata ─────────────────────────────────────────────────────────

class TestCollectMetadata:
    def _make_exp(self, tmp_path, results: list[dict]) -> Path:
        exp = tmp_path / "exp"
        exp.mkdir()
        for i, r in enumerate(results):
            (exp / f"result-{i}.json").write_text(json.dumps(r))
        return exp

    def test_collects_agent_ids(self, tmp_path):
        exp = self._make_exp(tmp_path, [
            {"agent_id": "agent-a", "pillar_scores": []},
            {"agent_id": "agent-b", "pillar_scores": []},
        ])
        meta = _collect_metadata(exp)
        assert meta["agent_ids"] == {"agent-a", "agent-b"}

    def test_skips_skipped_results(self, tmp_path):
        exp = self._make_exp(tmp_path, [
            {"agent_id": "agent-a", "status": "skipped", "pillar_scores": []},
        ])
        meta = _collect_metadata(exp)
        assert "agent-a" not in meta["agent_ids"]

    def test_detects_pillar_scores(self, tmp_path):
        exp = self._make_exp(tmp_path, [
            {"agent_id": "a", "pillar_scores": [{"pillar": "PILLAR1", "score": 0.8}]},
        ])
        meta = _collect_metadata(exp)
        assert "p1" in meta["pillar_display"]

    def test_report_absent_when_missing(self, tmp_path):
        exp = self._make_exp(tmp_path, [{"agent_id": "a", "pillar_scores": []}])
        meta = _collect_metadata(exp)
        assert meta["has_report"] is False

    def test_report_present_when_exists(self, tmp_path):
        exp = self._make_exp(tmp_path, [{"agent_id": "a", "pillar_scores": []}])
        (exp / "FULL-REPORT.md").write_text("# Report")
        meta = _collect_metadata(exp)
        assert meta["has_report"] is True

    def test_paper_detected_by_glob(self, tmp_path):
        exp = self._make_exp(tmp_path, [{"agent_id": "a", "pillar_scores": []}])
        (exp / "academic-report-2026.md").write_text("# Paper")
        meta = _collect_metadata(exp)
        assert meta["has_paper"] is True

    def test_review_detected(self, tmp_path):
        exp = self._make_exp(tmp_path, [{"agent_id": "a", "pillar_scores": []}])
        (exp / "REVIEW.md").write_text("# Review")
        meta = _collect_metadata(exp)
        assert meta["has_review"] is True

    def test_date_format(self, tmp_path):
        exp = self._make_exp(tmp_path, [{"agent_id": "a", "pillar_scores": []}])
        meta = _collect_metadata(exp)
        # Should be YYYY-MM-DD
        parts = meta["date"].split("-")
        assert len(parts) == 3


# ── browse_reports ────────────────────────────────────────────────────────────

class TestBrowseReports:
    def test_prints_no_experiments_when_none(self, tmp_path, capsys):
        with patch("buyerbench.reports_browser._RESULTS_ROOT", tmp_path / "results"):
            browse_reports()
        captured = capsys.readouterr()
        assert "No experiments found" in captured.out

    def test_shows_table_and_back_returns(self, tmp_path, capsys):
        results = tmp_path / "results"
        exp = results / "my-exp"
        exp.mkdir(parents=True)
        (exp / "r.json").write_text(json.dumps({"agent_id": "agent-x", "pillar_scores": []}))

        with (
            patch("buyerbench.reports_browser._RESULTS_ROOT", results),
            patch("buyerbench.reports_browser.Prompt.ask", side_effect=["q"]),
        ):
            browse_reports()

        captured = capsys.readouterr()
        assert "my-exp" in captured.out

    def test_submenu_back_returns(self, tmp_path, capsys):
        results = tmp_path / "results"
        exp = results / "exp1"
        exp.mkdir(parents=True)
        (exp / "r.json").write_text(json.dumps({"agent_id": "a", "pillar_scores": []}))

        with (
            patch("buyerbench.reports_browser._RESULTS_ROOT", results),
            patch("buyerbench.reports_browser.Prompt.ask", side_effect=["1", "b"]),
        ):
            browse_reports()  # should not raise

    def test_submenu_report_prints_existing(self, tmp_path, capsys):
        results = tmp_path / "results"
        exp = results / "exp1"
        exp.mkdir(parents=True)
        (exp / "r.json").write_text(json.dumps({"agent_id": "a", "pillar_scores": []}))
        (exp / "FULL-REPORT.md").write_text("# Full Report Content")

        with (
            patch("buyerbench.reports_browser._RESULTS_ROOT", results),
            patch("buyerbench.reports_browser.Prompt.ask", side_effect=["1", "r", "b"]),
        ):
            browse_reports()

        captured = capsys.readouterr()
        assert "Full Report Content" in captured.out

    def test_submenu_dashboard_invokes_run(self, tmp_path, capsys):
        results = tmp_path / "results"
        exp = results / "exp1"
        exp.mkdir(parents=True)
        (exp / "r.json").write_text(json.dumps({"agent_id": "a", "pillar_scores": []}))

        mock_dashboard = MagicMock()

        with (
            patch("buyerbench.reports_browser._RESULTS_ROOT", results),
            patch("buyerbench.reports_browser.Prompt.ask", side_effect=["1", "d", "b"]),
            patch("buyerbench.dashboard.ResultsDashboard", return_value=mock_dashboard),
        ):
            browse_reports()

        mock_dashboard.run.assert_called_once()
