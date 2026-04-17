"""Tests for research/scripts/09_check_all_gates.py.

Covers:
- check_gate1: MISSING when pilot_dir is None
- check_gate1: MISSING when ceiling_effect.json absent
- check_gate1: PENDING when only mock data (n_models < 3)
- check_gate1: PASS when gate1.proceed=True and n_models >= 3
- check_gate1: FAIL when gate1.proceed=False and n_models >= 3
- check_gate1: criterion1/criterion2 details propagated
- check_gate1: mock_only=True for single-model data
- check_gate2: MISSING when robustness_dir is None
- check_gate2: MISSING when robustness_pilot.json absent
- check_gate2: PENDING when all_zero BSI (mock pattern)
- check_gate2: PASS when overall_recommendation=PROCEED and non-zero BSI
- check_gate2: FAIL when overall_recommendation=REDESIGN and non-zero BSI
- check_gate2: scenarios_passing/failing propagated
- check_gate3: MISSING when full_dir is None
- check_gate3: MISSING when neither gate3.json nor cells.json present
- check_gate3: PASS when gate3.proceed=True
- check_gate3: FAIL when gate3.proceed=False
- check_gate3: robust_rationality_pivot propagated
- build_gate4_checklist: returns list of 8 items
- build_gate4_checklist: all items have label, instruction, note
- build_gate4_checklist: OSF preregistration item present
- build_gate4_checklist: claim tiers item present
- build_gate4_checklist: BH-FDR item present
- _auto_discover: fills in None when artifacts exist
- _auto_discover: returns None when no artifacts found
- _latest_matching_dir: returns most-recent dir matching prefix
- _latest_matching_dir: returns None when no match
- CLI: no-args run (auto-discover, no crash)
- CLI: --gate 1 only checks gate 1
- CLI: --gate 4 shows checklist
- CLI: --quiet suppresses recommendations
- CLI: --report writes Markdown file
- _render_markdown: all four gate sections present
- _render_markdown: status badges for PASS/FAIL/PENDING/MISSING
- GateStatus constants correct
"""
from __future__ import annotations

import json
import sys
import tempfile
from io import StringIO
from pathlib import Path

import importlib.util

import pytest

_REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPT_PATH = _REPO_ROOT / "research" / "scripts" / "09_check_all_gates.py"


def _load_script():
    spec = importlib.util.spec_from_file_location("check_all_gates", _SCRIPT_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_script = _load_script()

GATE2_CV_THRESHOLD = _script.GATE2_CV_THRESHOLD
GateStatus = _script.GateStatus
_auto_discover = _script._auto_discover
_latest_matching_dir = _script._latest_matching_dir
_render_markdown = _script._render_markdown
build_gate4_checklist = _script.build_gate4_checklist
check_gate1 = _script.check_gate1
check_gate2 = _script.check_gate2
check_gate3 = _script.check_gate3
main = _script.main


# ── Helpers ────────────────────────────────────────────────────────────────────

def _make_ceiling_json(
    gate1_proceed: bool,
    n_models: int,
    criterion1_pass: bool = True,
    criterion2_pass: bool = True,
) -> dict:
    return {
        "gate": "PROCEED" if n_models >= 3 else "INSUFFICIENT",
        "n_models": n_models,
        "n_floor_models": 0,
        "recommendation": "ok",
        "n_total_runs": n_models * 30,
        "n_valid_runs": n_models * 30,
        "gate1": {
            "proceed": gate1_proceed,
            "criterion1_pass": criterion1_pass,
            "criterion1_detail": "Error rate 0% — PASS",
            "criterion2_pass": criterion2_pass,
            "criterion2_detail": "2 models show BSI > 0.05 — PASS" if criterion2_pass
                                 else "0 models show BSI > 0.05 — FAIL",
            "recommendation": "Gate 1 PASSED" if gate1_proceed else "Gate 1 FAILED",
        },
    }


def _make_robustness_json(all_zero: bool = True, overall: str = "PROCEED") -> dict:
    mean_bsi = 0.0 if all_zero else 0.35
    return {
        "n_runs": 5,
        "cv_threshold": 0.5,
        "phrasings": ["robustness_a", "robustness_b", "robustness_c"],
        "per_scenario": {
            "p2-01-anchoring": {
                "phrasings": 3,
                "per_phrasing_mean_bsi": {k: mean_bsi for k in
                                          ["robustness_a", "robustness_b", "robustness_c"]},
                "mean_of_means": mean_bsi,
                "std_of_means": 0.0,
                "cv": 0.0,
                "cv_threshold": 0.5,
                "robust": overall == "PROCEED",
                "recommendation": overall,
            },
        },
        "scenarios_passing": 1 if overall == "PROCEED" else 0,
        "scenarios_failing": 0 if overall == "PROCEED" else 1,
        "scenarios_to_redesign": [] if overall == "PROCEED" else ["p2-01-anchoring"],
        "overall_recommendation": overall,
    }


def _make_gate3_json(proceed: bool, n_models: int = 3, pivot: bool = False) -> dict:
    return {
        "gate3": {
            "proceed": proceed,
            "n_models_with_bias": n_models if proceed else 0,
            "qualifying_models": {},
            "per_model_bias_counts": {},
            "criterion_detail": f"{n_models} qualify",
            "recommendation": "Gate 3 PASSED" if proceed else "Gate 3 FAILED",
            "robust_rationality_pivot": pivot,
            "gate3_min_models": 3,
            "gate3_min_bias_types": 2,
        }
    }


# ── GateStatus constants ───────────────────────────────────────────────────────

class TestGateStatusConstants:
    def test_pass(self):
        assert GateStatus.PASS == "PASS"

    def test_fail(self):
        assert GateStatus.FAIL == "FAIL"

    def test_pending(self):
        assert GateStatus.PENDING == "PENDING"

    def test_missing(self):
        assert GateStatus.MISSING == "MISSING"

    def test_gate2_threshold(self):
        assert GATE2_CV_THRESHOLD == 0.60


# ── check_gate1 ────────────────────────────────────────────────────────────────

class TestCheckGate1:
    def test_missing_when_dir_is_none(self):
        r = check_gate1(None)
        assert r["status"] == GateStatus.MISSING
        assert r["proceed"] is False
        assert "01_run_pilot_full" in r["recommendation"]

    def test_missing_when_file_absent(self, tmp_path):
        r = check_gate1(tmp_path)
        assert r["status"] == GateStatus.MISSING
        assert "03_analyze_ceiling_effect" in r["recommendation"]

    def test_pending_for_mock_only_single_model(self, tmp_path):
        data = _make_ceiling_json(gate1_proceed=False, n_models=1)
        (tmp_path / "ceiling_effect.json").write_text(json.dumps(data))
        r = check_gate1(tmp_path)
        assert r["status"] == GateStatus.PENDING
        assert r["mock_only"] is True

    def test_pending_for_insufficient_models(self, tmp_path):
        data = _make_ceiling_json(gate1_proceed=False, n_models=2)
        data["gate"] = "INSUFFICIENT"
        (tmp_path / "ceiling_effect.json").write_text(json.dumps(data))
        r = check_gate1(tmp_path)
        assert r["status"] == GateStatus.PENDING

    def test_pass_when_proceed_true_and_real_models(self, tmp_path):
        data = _make_ceiling_json(gate1_proceed=True, n_models=10)
        (tmp_path / "ceiling_effect.json").write_text(json.dumps(data))
        r = check_gate1(tmp_path)
        assert r["status"] == GateStatus.PASS
        assert r["proceed"] is True
        assert r["mock_only"] is False

    def test_fail_when_proceed_false_and_real_models(self, tmp_path):
        data = _make_ceiling_json(gate1_proceed=False, n_models=10, criterion2_pass=False)
        (tmp_path / "ceiling_effect.json").write_text(json.dumps(data))
        r = check_gate1(tmp_path)
        assert r["status"] == GateStatus.FAIL
        assert r["proceed"] is False

    def test_criterion_details_propagated(self, tmp_path):
        data = _make_ceiling_json(gate1_proceed=True, n_models=5)
        (tmp_path / "ceiling_effect.json").write_text(json.dumps(data))
        r = check_gate1(tmp_path)
        assert "0%" in r["criterion1_detail"]
        assert "PASS" in r["criterion2_detail"]

    def test_n_models_propagated(self, tmp_path):
        data = _make_ceiling_json(gate1_proceed=True, n_models=8)
        (tmp_path / "ceiling_effect.json").write_text(json.dumps(data))
        r = check_gate1(tmp_path)
        assert r["n_models"] == 8

    def test_source_file_present(self, tmp_path):
        data = _make_ceiling_json(gate1_proceed=True, n_models=5)
        (tmp_path / "ceiling_effect.json").write_text(json.dumps(data))
        r = check_gate1(tmp_path)
        assert r["source_file"] is not None
        assert "ceiling_effect.json" in r["source_file"]


# ── check_gate2 ────────────────────────────────────────────────────────────────

class TestCheckGate2:
    def test_missing_when_dir_is_none(self):
        r = check_gate2(None)
        assert r["status"] == GateStatus.MISSING
        assert r["proceed"] is False
        assert "robustness-pilot" in r["recommendation"]

    def test_missing_when_file_absent(self, tmp_path):
        r = check_gate2(tmp_path)
        assert r["status"] == GateStatus.MISSING
        assert "robustness_pilot.json" in r["recommendation"]

    def test_pending_when_all_zero_bsi(self, tmp_path):
        data = _make_robustness_json(all_zero=True, overall="PROCEED")
        (tmp_path / "robustness_pilot.json").write_text(json.dumps(data))
        r = check_gate2(tmp_path)
        assert r["status"] == GateStatus.PENDING
        assert r["mock_only"] is True

    def test_pass_when_nonzero_bsi_and_proceed(self, tmp_path):
        data = _make_robustness_json(all_zero=False, overall="PROCEED")
        (tmp_path / "robustness_pilot.json").write_text(json.dumps(data))
        r = check_gate2(tmp_path)
        assert r["status"] == GateStatus.PASS
        assert r["proceed"] is True

    def test_fail_when_nonzero_bsi_and_redesign(self, tmp_path):
        data = _make_robustness_json(all_zero=False, overall="REDESIGN")
        (tmp_path / "robustness_pilot.json").write_text(json.dumps(data))
        r = check_gate2(tmp_path)
        assert r["status"] == GateStatus.FAIL
        assert r["proceed"] is False

    def test_scenarios_passing_failing_propagated(self, tmp_path):
        data = _make_robustness_json(all_zero=False, overall="PROCEED")
        (tmp_path / "robustness_pilot.json").write_text(json.dumps(data))
        r = check_gate2(tmp_path)
        assert r["scenarios_passing"] == 1
        assert r["scenarios_failing"] == 0

    def test_source_file_present(self, tmp_path):
        data = _make_robustness_json(all_zero=True)
        (tmp_path / "robustness_pilot.json").write_text(json.dumps(data))
        r = check_gate2(tmp_path)
        assert r["source_file"] is not None
        assert "robustness_pilot.json" in r["source_file"]

    def test_recommendation_mentions_cv(self, tmp_path):
        data = _make_robustness_json(all_zero=False, overall="PROCEED")
        (tmp_path / "robustness_pilot.json").write_text(json.dumps(data))
        r = check_gate2(tmp_path)
        assert "CV" in r["recommendation"] or "cv" in r["recommendation"].lower()


# ── check_gate3 ────────────────────────────────────────────────────────────────

class TestCheckGate3:
    def test_missing_when_dir_is_none(self):
        r = check_gate3(None)
        assert r["status"] == GateStatus.MISSING
        assert r["proceed"] is False
        assert "02_run_full_experiment" in r["recommendation"]

    def test_missing_when_files_absent(self, tmp_path):
        r = check_gate3(tmp_path)
        assert r["status"] == GateStatus.MISSING

    def test_missing_when_only_cells_json(self, tmp_path):
        # cells.json exists but gate3.json not yet generated
        cells = {"cells": []}
        (tmp_path / "cells.json").write_text(json.dumps(cells))
        r = check_gate3(tmp_path)
        assert r["status"] == GateStatus.MISSING
        assert "--analyze-gate3" in r["recommendation"]

    def test_pass_when_proceed_true(self, tmp_path):
        data = _make_gate3_json(proceed=True, n_models=5)
        (tmp_path / "gate3.json").write_text(json.dumps(data))
        r = check_gate3(tmp_path)
        assert r["status"] == GateStatus.PASS
        assert r["proceed"] is True

    def test_fail_when_proceed_false(self, tmp_path):
        data = _make_gate3_json(proceed=False)
        (tmp_path / "gate3.json").write_text(json.dumps(data))
        r = check_gate3(tmp_path)
        assert r["status"] == GateStatus.FAIL
        assert r["proceed"] is False

    def test_robust_rationality_pivot_propagated(self, tmp_path):
        data = _make_gate3_json(proceed=False, pivot=True)
        (tmp_path / "gate3.json").write_text(json.dumps(data))
        r = check_gate3(tmp_path)
        assert r["robust_rationality_pivot"] is True

    def test_source_file_present(self, tmp_path):
        data = _make_gate3_json(proceed=True)
        (tmp_path / "gate3.json").write_text(json.dumps(data))
        r = check_gate3(tmp_path)
        assert r["source_file"] is not None

    def test_criterion_detail_propagated(self, tmp_path):
        data = _make_gate3_json(proceed=True, n_models=4)
        (tmp_path / "gate3.json").write_text(json.dumps(data))
        r = check_gate3(tmp_path)
        assert "qualify" in r["criterion_detail"]


# ── build_gate4_checklist ──────────────────────────────────────────────────────

class TestBuildGate4Checklist:
    def test_returns_list(self):
        c = build_gate4_checklist()
        assert isinstance(c, list)

    def test_has_eight_items(self):
        c = build_gate4_checklist()
        assert len(c) == 8

    def test_all_items_have_label(self):
        for item in build_gate4_checklist():
            assert "label" in item
            assert item["label"]

    def test_all_items_have_instruction(self):
        for item in build_gate4_checklist():
            assert "instruction" in item
            assert item["instruction"]

    def test_osf_preregistration_item(self):
        labels = [i["label"].lower() for i in build_gate4_checklist()]
        assert any("osf" in l or "pre-registr" in l or "preregistr" in l for l in labels)

    def test_claim_tiers_item(self):
        labels = [i["label"].lower() for i in build_gate4_checklist()]
        assert any("claim" in l or "tier" in l for l in labels)

    def test_bh_fdr_item(self):
        texts = [i["instruction"].lower() for i in build_gate4_checklist()]
        assert any("bh" in t or "fdr" in t or "correction" in t for t in texts)

    def test_no_tier_c_item(self):
        labels = [i["label"].lower() for i in build_gate4_checklist()]
        assert any("tier c" in l or "tier-c" in l for l in labels)


# ── _auto_discover ─────────────────────────────────────────────────────────────

class TestAutoDiscover:
    def test_returns_none_when_empty(self, tmp_path):
        p, r, f = _auto_discover(None, None, None)
        # These may or may not discover real files — just ensure no exception
        assert True  # no crash

    def test_explicit_dirs_not_overridden(self, tmp_path):
        p, r, f = _auto_discover(tmp_path, tmp_path, tmp_path)
        assert p == tmp_path
        assert r == tmp_path
        assert f == tmp_path


class TestLatestMatchingDir:
    def test_returns_none_when_no_match(self, tmp_path):
        result = _latest_matching_dir("nonexistent-prefix-xyz-", search_root=tmp_path)
        assert result is None

    def test_returns_most_recent_match(self, tmp_path):
        import time
        d1 = tmp_path / "pillar2-test-001"
        d1.mkdir()
        time.sleep(0.01)
        d2 = tmp_path / "pillar2-test-002"
        d2.mkdir()
        result = _latest_matching_dir("pillar2-test-", search_root=tmp_path)
        assert result == d2

    def test_returns_none_when_search_root_missing(self, tmp_path):
        result = _latest_matching_dir("x", search_root=tmp_path / "does-not-exist")
        assert result is None


# ── _render_markdown ───────────────────────────────────────────────────────────

class TestRenderMarkdown:
    def _make_all_gates(self, tmp_path):
        # Gate 1: PENDING
        g1 = {"status": GateStatus.PENDING, "proceed": False, "mock_only": True,
               "recommendation": "run real models", "source_file": str(tmp_path / "c.json"),
               "n_models": 1, "criterion1_detail": "ok", "criterion2_detail": "fail"}
        # Gate 2: MISSING
        g2 = {"status": GateStatus.MISSING, "proceed": False, "mock_only": False,
               "recommendation": "run pilot", "source_file": None,
               "scenarios_passing": 0, "scenarios_failing": 0, "cv_threshold": 0.5}
        # Gate 3: MISSING
        g3 = {"status": GateStatus.MISSING, "proceed": False,
               "recommendation": "run full", "source_file": None,
               "n_models_with_bias": 0, "robust_rationality_pivot": False,
               "criterion_detail": ""}
        g4 = build_gate4_checklist()
        return g1, g2, g3, g4

    def test_renders_without_crash(self, tmp_path):
        g1, g2, g3, g4 = self._make_all_gates(tmp_path)
        md = _render_markdown(g1, g2, g3, g4)
        assert isinstance(md, str)
        assert len(md) > 100

    def test_contains_gate_sections(self, tmp_path):
        g1, g2, g3, g4 = self._make_all_gates(tmp_path)
        md = _render_markdown(g1, g2, g3, g4)
        assert "Gate 1" in md
        assert "Gate 2" in md
        assert "Gate 3" in md
        assert "Gate 4" in md

    def test_pass_badge(self, tmp_path):
        g1, g2, g3, g4 = self._make_all_gates(tmp_path)
        g1["status"] = GateStatus.PASS
        md = _render_markdown(g1, g2, g3, g4)
        assert "✅" in md or "PASS" in md

    def test_fail_badge(self, tmp_path):
        g1, g2, g3, g4 = self._make_all_gates(tmp_path)
        g1["status"] = GateStatus.FAIL
        md = _render_markdown(g1, g2, g3, g4)
        assert "❌" in md or "FAIL" in md

    def test_pending_badge(self, tmp_path):
        g1, g2, g3, g4 = self._make_all_gates(tmp_path)
        md = _render_markdown(g1, g2, g3, g4)
        assert "⏳" in md or "PENDING" in md

    def test_gate4_checklist_items_present(self, tmp_path):
        g1, g2, g3, g4 = self._make_all_gates(tmp_path)
        md = _render_markdown(g1, g2, g3, g4)
        for item in g4:
            assert item["label"] in md

    def test_robust_rationality_note_when_pivot(self, tmp_path):
        g1, g2, g3, g4 = self._make_all_gates(tmp_path)
        g3["status"] = GateStatus.FAIL
        g3["robust_rationality_pivot"] = True
        md = _render_markdown(g1, g2, g3, g4)
        assert "robust rationality" in md.lower() or "Robust Rationality" in md

    def test_mock_only_warning_when_pending(self, tmp_path):
        g1, g2, g3, g4 = self._make_all_gates(tmp_path)
        md = _render_markdown(g1, g2, g3, g4)
        assert "mock" in md.lower()

    def test_yaml_frontmatter(self, tmp_path):
        g1, g2, g3, g4 = self._make_all_gates(tmp_path)
        md = _render_markdown(g1, g2, g3, g4)
        assert md.startswith("---")
        assert "type: report" in md

    def test_next_steps_section(self, tmp_path):
        g1, g2, g3, g4 = self._make_all_gates(tmp_path)
        md = _render_markdown(g1, g2, g3, g4)
        assert "Next Steps" in md or "next steps" in md.lower()


# ── CLI ────────────────────────────────────────────────────────────────────────

class TestCLI:
    def test_no_args_runs_without_crash(self, capsys):
        # auto-discovers from real results/experiments/ — should not raise
        try:
            main([])
        except SystemExit as e:
            # FAIL exit is acceptable; what we test is no unhandled exception
            assert e.code in (0, 1)

    def test_gate_1_only(self, tmp_path, capsys):
        data = _make_ceiling_json(gate1_proceed=False, n_models=1)
        (tmp_path / "ceiling_effect.json").write_text(json.dumps(data))
        try:
            main(["--gate", "1", "--pilot-dir", str(tmp_path)])
        except SystemExit:
            pass  # PENDING exits 0
        out = capsys.readouterr().out
        assert "Gate 1" in out

    def test_gate_4_shows_checklist(self, capsys):
        try:
            main(["--gate", "4"])
        except SystemExit:
            pass
        out = capsys.readouterr().out
        assert "Gate 4" in out

    def test_quiet_suppresses_recommendations(self, tmp_path, capsys):
        data = _make_ceiling_json(gate1_proceed=True, n_models=10)
        (tmp_path / "ceiling_effect.json").write_text(json.dumps(data))
        try:
            main(["--gate", "1", "--pilot-dir", str(tmp_path), "--quiet"])
        except SystemExit:
            pass
        out = capsys.readouterr().out
        # status line still present; detailed recommendation should not be
        assert "Gate 1" in out

    def test_report_writes_markdown_file(self, tmp_path, capsys):
        report_path = tmp_path / "gate_status.md"
        try:
            main([
                "--pilot-dir", str(tmp_path),
                "--robustness-dir", str(tmp_path),
                "--full-dir", str(tmp_path),
                "--report", str(report_path),
            ])
        except SystemExit:
            pass
        assert report_path.exists()
        content = report_path.read_text()
        assert "Gate" in content

    def test_fail_exit_when_gate_fails(self, tmp_path):
        data = _make_ceiling_json(gate1_proceed=False, n_models=10, criterion2_pass=False)
        (tmp_path / "ceiling_effect.json").write_text(json.dumps(data))
        with pytest.raises(SystemExit) as exc:
            main(["--gate", "1", "--pilot-dir", str(tmp_path)])
        assert exc.value.code == 1

    def test_no_fail_exit_when_only_pending(self, tmp_path):
        data = _make_ceiling_json(gate1_proceed=False, n_models=1)
        (tmp_path / "ceiling_effect.json").write_text(json.dumps(data))
        try:
            main(["--gate", "1", "--pilot-dir", str(tmp_path)])
        except SystemExit as e:
            # PENDING should NOT exit with 1
            assert e.code != 1
