"""Tests for buyerbench.dashboard — ResultsDashboard and run_dashboard."""
from __future__ import annotations

import io
import json
from datetime import datetime, timezone
from pathlib import Path

import pytest
from rich.console import Console

from buyerbench.dashboard import ResultsDashboard


# ── Fixture helpers ───────────────────────────────────────────────────────────

def _make_result_json(
    scenario_id: str,
    agent_id: str,
    pillar: str = "PILLAR1",
    score: float = 0.8,
    overall_pass: bool = True,
    *,
    skipped: bool = False,
) -> dict:
    if skipped:
        return {
            "status": "skipped",
            "agent_id": agent_id,
            "scenario_id": scenario_id,
        }
    return {
        "scenario_id": scenario_id,
        "agent_id": agent_id,
        "pillar_scores": [
            {
                "pillar": pillar,
                "score": score,
                "metrics": {"compliance_adherence_rate": score},
                "violations": [] if overall_pass else ["test-violation"],
                "notes": "",
            }
        ],
        "overall_pass": overall_pass,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "variant_pair_id": None,
    }


@pytest.fixture()
def results_dir(tmp_path: Path) -> Path:
    """Write 3 fake result JSON files (one per pillar) plus one skipped file."""
    (tmp_path / "p1.json").write_text(
        json.dumps(_make_result_json("p1-01", "agent-alpha", "PILLAR1", 0.9, True))
    )
    (tmp_path / "p2.json").write_text(
        json.dumps(_make_result_json("p2-01", "agent-alpha", "PILLAR2", 0.6, True))
    )
    (tmp_path / "p3.json").write_text(
        json.dumps(_make_result_json("p3-01", "agent-beta", "PILLAR3", 0.4, False))
    )
    (tmp_path / "skipped.json").write_text(
        json.dumps(_make_result_json("p1-02", "agent-gamma", skipped=True))
    )
    return tmp_path


# ── Unit tests ────────────────────────────────────────────────────────────────

class TestLoadResults:
    def test_returns_three_non_skipped_items(self, results_dir: Path) -> None:
        db = ResultsDashboard(str(results_dir))
        loaded = db._load_results(results_dir)
        assert len(loaded) == 3

    def test_excludes_skipped_status(self, results_dir: Path) -> None:
        db = ResultsDashboard(str(results_dir))
        for r in db.results:
            assert r.get("status") != "skipped"

    def test_empty_dir_returns_empty_list(self, tmp_path: Path) -> None:
        db = ResultsDashboard(str(tmp_path))
        assert db.results == []


class TestAggregate:
    def test_returns_dict_keyed_by_agent_id(self, results_dir: Path) -> None:
        db = ResultsDashboard(str(results_dir))
        agg = db._aggregate()
        assert isinstance(agg, dict)
        assert "agent-alpha" in agg
        assert "agent-beta" in agg

    def test_pillar_means_present(self, results_dir: Path) -> None:
        db = ResultsDashboard(str(results_dir))
        agg = db._aggregate()
        alpha = agg["agent-alpha"]
        assert "PILLAR1" in alpha["pillar_means"]
        assert "PILLAR2" in alpha["pillar_means"]
        assert alpha["pillar_means"]["PILLAR1"] == pytest.approx(0.9)

    def test_overall_mean_computed(self, results_dir: Path) -> None:
        db = ResultsDashboard(str(results_dir))
        agg = db._aggregate()
        # agent-alpha has PILLAR1=0.9, PILLAR2=0.6 → mean=0.75
        assert agg["agent-alpha"]["overall_mean"] == pytest.approx(0.75)

    def test_pass_rate(self, results_dir: Path) -> None:
        db = ResultsDashboard(str(results_dir))
        agg = db._aggregate()
        # agent-alpha: 2 results, both pass → 1.0
        assert agg["agent-alpha"]["pass_rate"] == pytest.approx(1.0)
        # agent-beta: 1 result, fail → 0.0
        assert agg["agent-beta"]["pass_rate"] == pytest.approx(0.0)

    def test_agents_attribute_sorted(self, results_dir: Path) -> None:
        db = ResultsDashboard(str(results_dir))
        assert db.agents == sorted(db.agents)


class TestRenderSummary:
    def test_does_not_raise(self, results_dir: Path) -> None:
        db = ResultsDashboard(str(results_dir))
        buf = io.StringIO()
        con = Console(file=buf, width=120, highlight=False)
        db.render_summary(con)

    def test_output_contains_session(self, results_dir: Path) -> None:
        db = ResultsDashboard(str(results_dir))
        buf = io.StringIO()
        con = Console(file=buf, width=120, highlight=False)
        db.render_summary(con)
        output = buf.getvalue()
        assert "Session" in output

    def test_output_contains_agent_count(self, results_dir: Path) -> None:
        db = ResultsDashboard(str(results_dir))
        buf = io.StringIO()
        con = Console(file=buf, width=120, highlight=False)
        db.render_summary(con)
        output = buf.getvalue()
        # 2 distinct non-skipped agents
        assert "2" in output


class TestRenderComparison:
    def test_does_not_raise(self, results_dir: Path) -> None:
        db = ResultsDashboard(str(results_dir))
        buf = io.StringIO()
        con = Console(file=buf, width=160, highlight=False)
        db.render_comparison(con)

    def test_output_contains_agent_name(self, results_dir: Path) -> None:
        db = ResultsDashboard(str(results_dir))
        buf = io.StringIO()
        con = Console(file=buf, width=160, highlight=False)
        db.render_comparison(con)
        assert "agent-alpha" in buf.getvalue()


class TestRenderScenarios:
    def test_all_pillars_no_filter(self, results_dir: Path) -> None:
        db = ResultsDashboard(str(results_dir))
        buf = io.StringIO()
        con = Console(file=buf, width=160, highlight=False)
        db.render_scenarios(con)

    def test_pillar_filter(self, results_dir: Path) -> None:
        db = ResultsDashboard(str(results_dir))
        buf = io.StringIO()
        con = Console(file=buf, width=160, highlight=False)
        db.render_scenarios(con, pillar_filter=1)
        output = buf.getvalue()
        assert "PILLAR1" in output

    def test_pillar_filter_excludes_others(self, results_dir: Path) -> None:
        db = ResultsDashboard(str(results_dir))
        buf = io.StringIO()
        con = Console(file=buf, width=160, highlight=False)
        db.render_scenarios(con, pillar_filter=1)
        output = buf.getvalue()
        # PILLAR2 and PILLAR3 tables should not appear
        assert "PILLAR2" not in output
        assert "PILLAR3" not in output


class TestRenderBiasSecurity:
    def test_does_not_raise(self, results_dir: Path) -> None:
        db = ResultsDashboard(str(results_dir))
        buf = io.StringIO()
        con = Console(file=buf, width=160, highlight=False)
        db.render_bias_security(con)

    def test_output_contains_security_summary(self, results_dir: Path) -> None:
        db = ResultsDashboard(str(results_dir))
        buf = io.StringIO()
        con = Console(file=buf, width=160, highlight=False)
        db.render_bias_security(con)
        output = buf.getvalue()
        assert "Security" in output or "Compliance" in output


class TestEmptyDirectory:
    def test_render_summary_empty(self, tmp_path: Path) -> None:
        db = ResultsDashboard(str(tmp_path))
        buf = io.StringIO()
        con = Console(file=buf, width=120, highlight=False)
        db.render_summary(con)
        assert "Session" in buf.getvalue()

    def test_render_comparison_empty(self, tmp_path: Path) -> None:
        db = ResultsDashboard(str(tmp_path))
        buf = io.StringIO()
        con = Console(file=buf, width=160, highlight=False)
        db.render_comparison(con)  # Should not raise
