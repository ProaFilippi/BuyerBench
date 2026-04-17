"""Tests for research/scripts/10_gate4_paper_scan.py.

Covers:
- TIER_C_PATTERNS: list of tuples with (pattern, slug, description)
- split_main_and_appendix: splits at first ## Appendix heading
- split_main_and_appendix: returns full text when no appendix heading
- split_main_and_appendix: appendix_text starts with ## Appendix
- scan_tier_c_violations: returns empty list on clean text
- scan_tier_c_violations: detects [TIER-C] scaffolding label
- scan_tier_c_violations: detects architectural-inference pattern
- scan_tier_c_violations: detects cross-domain-generalization pattern
- scan_tier_c_violations: detects categorical-always pattern
- scan_tier_c_violations: detects mechanism-confirmed pattern
- scan_tier_c_violations: detects mechanism-proof pattern
- scan_tier_c_violations: detects training-causal pattern
- scan_tier_c_violations: 'mechanism is not' does NOT trigger mechanism-confirmed
- scan_tier_c_violations: violation dict has required keys
- scan_tier_c_violations: one report per line (first match wins)
- count_result_placeholders: counts zero placeholders on clean text
- count_result_placeholders: counts one placeholder
- count_result_placeholders: counts multiple placeholders
- run_gate4_scan: MISSING status when paper path does not exist
- run_gate4_scan: PENDING when no violations but placeholders remain
- run_gate4_scan: PASS when no violations and no placeholders
- run_gate4_scan: FAIL when tier-c violation in main text
- run_gate4_scan: violations in appendix do NOT trigger FAIL
- run_gate4_scan: result dict has all required keys
- run_gate4_scan: FAIL takes priority over PENDING (violations + placeholders)
- run_gate4_scan: n_violations matches len(violations)
- run_gate4_scan: source_file matches paper_path
- CLI: exits 0 on PASS
- CLI: exits 1 on FAIL
- check_gate4_scan in 09: MISSING when default paper exists (real paper is PENDING)
- check_gate4_scan in 09: PASS when paper is clean (synthetic clean paper)
- check_gate4_scan in 09: FAIL when paper has violations (synthetic paper with violations)
- 09 _render_markdown: Gate 4 section present with scan result
- 09 _render_markdown: shows n_violations and n_placeholders fields
"""
from __future__ import annotations

import importlib.util
import sys
import tempfile
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parent.parent
_SCANNER_PATH = _REPO_ROOT / "research" / "scripts" / "10_gate4_paper_scan.py"
_GATES_PATH = _REPO_ROOT / "research" / "scripts" / "09_check_all_gates.py"


def _load_scanner():
    spec = importlib.util.spec_from_file_location("gate4_paper_scan", _SCANNER_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _load_gates():
    spec = importlib.util.spec_from_file_location("check_all_gates", _GATES_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_scanner = _load_scanner()
_gates = _load_gates()

TIER_C_PATTERNS = _scanner.TIER_C_PATTERNS
split_main_and_appendix = _scanner.split_main_and_appendix
scan_tier_c_violations = _scanner.scan_tier_c_violations
count_result_placeholders = _scanner.count_result_placeholders
run_gate4_scan = _scanner.run_gate4_scan
PAPER_PATH = _scanner.PAPER_PATH


# ── Helper fixtures ────────────────────────────────────────────────────────────

def _write_paper(tmp_path: Path, main_content: str, appendix_content: str = "") -> Path:
    paper = tmp_path / "paper.md"
    text = main_content
    if appendix_content:
        text += "\n\n## Appendix A — Test\n\n" + appendix_content
    paper.write_text(text, encoding="utf-8")
    return paper


_CLEAN_MAIN = (
    "# 1. Introduction\n\nThis study evaluates LLM buyer agents.\n\n"
    "# 2. Methods\n\nWe use N=50 per cell.\n\n"
    "# 3. Results\n\nResults show BSI values.\n"
)

_PLACEHOLDER_MAIN = _CLEAN_MAIN + "\nBSI = {{RESULT: anchor_bsi}}\n"

_TIER_C_MAIN = _CLEAN_MAIN + "\nThis is caused by the transformer architecture.\n"


# ── TestTierCPatterns ──────────────────────────────────────────────────────────

class TestTierCPatterns:
    def test_is_list(self):
        assert isinstance(TIER_C_PATTERNS, list)

    def test_all_tuples_of_three(self):
        for item in TIER_C_PATTERNS:
            assert len(item) == 3, f"Expected 3-tuple, got {item!r}"

    def test_first_element_is_compiled_re(self):
        import re
        for pattern, _, _ in TIER_C_PATTERNS:
            assert hasattr(pattern, "search"), f"{pattern!r} is not a compiled regex"

    def test_slugs_are_strings(self):
        for _, slug, _ in TIER_C_PATTERNS:
            assert isinstance(slug, str) and slug

    def test_descriptions_are_strings(self):
        for _, _, desc in TIER_C_PATTERNS:
            assert isinstance(desc, str) and desc

    def test_has_scaffolding_label_pattern(self):
        slugs = [slug for _, slug, _ in TIER_C_PATTERNS]
        assert "scaffolding-label" in slugs

    def test_has_architectural_inference_pattern(self):
        slugs = [slug for _, slug, _ in TIER_C_PATTERNS]
        assert "architectural-inference" in slugs

    def test_has_cross_domain_generalization_pattern(self):
        slugs = [slug for _, slug, _ in TIER_C_PATTERNS]
        assert "cross-domain-generalization" in slugs


# ── TestSplitMainAndAppendix ───────────────────────────────────────────────────

class TestSplitMainAndAppendix:
    def test_splits_at_appendix_heading(self):
        text = "Main text here.\n\n## Appendix A — Details\n\nAppendix content."
        main, appendix = split_main_and_appendix(text)
        assert "Main text here." in main
        assert "## Appendix A" not in main

    def test_appendix_starts_with_heading(self):
        text = "Main.\n\n## Appendix B — Extra\n\nMore."
        _, appendix = split_main_and_appendix(text)
        assert appendix.startswith("## Appendix B")

    def test_no_appendix_returns_full_text_as_main(self):
        text = "Only main text, no appendix heading."
        main, appendix = split_main_and_appendix(text)
        assert main == text
        assert appendix == ""

    def test_appendix_case_insensitive(self):
        text = "Main.\n\n## APPENDIX A — Stuff\n\nContent."
        main, appendix = split_main_and_appendix(text)
        assert "APPENDIX" not in main
        assert "## APPENDIX A" in appendix

    def test_main_text_does_not_include_appendix_content(self):
        text = "Section 1.\n\n## Appendix A\n\nShould not be in main."
        main, _ = split_main_and_appendix(text)
        assert "Should not be in main." not in main


# ── TestScanTierCViolations ────────────────────────────────────────────────────

class TestScanTierCViolations:
    def test_clean_text_returns_empty_list(self):
        assert scan_tier_c_violations("This text is clean and unbiased.") == []

    def test_detects_scaffolding_label(self):
        text = "Some text [TIER-C] here."
        violations = scan_tier_c_violations(text)
        assert len(violations) == 1
        assert violations[0]["category"] == "scaffolding-label"

    def test_detects_architectural_inference(self):
        text = "The result is caused by the transformer architecture."
        violations = scan_tier_c_violations(text)
        assert any(v["category"] == "architectural-inference" for v in violations)

    def test_detects_cross_domain_generalization(self):
        text = "The effect generalizes to other domains beyond this one."
        violations = scan_tier_c_violations(text)
        assert any(v["category"] == "cross-domain-generalization" for v in violations)

    def test_detects_categorical_always(self):
        text = "All LLMs always show bias in structured tasks."
        violations = scan_tier_c_violations(text)
        assert any(v["category"] == "categorical-always" for v in violations)

    def test_detects_mechanism_proof(self):
        text = "This confirms that the mechanism is responsible."
        violations = scan_tier_c_violations(text)
        assert any(
            v["category"] in ("mechanism-proof", "mechanism-confirmed") for v in violations
        )

    def test_detects_training_causal(self):
        text = "Because the model was trained on biased text."
        violations = scan_tier_c_violations(text)
        assert any(v["category"] == "training-causal" for v in violations)

    def test_mechanism_is_not_no_trigger(self):
        text = "The mechanism is not directly tested by this design."
        violations = scan_tier_c_violations(text)
        cats = [v["category"] for v in violations]
        assert "mechanism-confirmed" not in cats

    def test_violation_dict_has_required_keys(self):
        text = "This is caused by the transformer module."
        violations = scan_tier_c_violations(text)
        assert len(violations) > 0
        v = violations[0]
        assert "line_number" in v
        assert "line" in v
        assert "category" in v
        assert "description" in v
        assert "match" in v

    def test_one_report_per_line(self):
        text = "[TIER-C] also caused by the transformer."
        violations = scan_tier_c_violations(text)
        assert len(violations) == 1  # first match wins

    def test_multi_line_text_correct_line_numbers(self):
        text = "Line 1 is fine.\nLine 2 is fine.\n[TIER-C] violation here.\nLine 4 fine."
        violations = scan_tier_c_violations(text)
        assert violations[0]["line_number"] == 3


# ── TestCountResultPlaceholders ───────────────────────────────────────────────

class TestCountResultPlaceholders:
    def test_zero_on_clean_text(self):
        assert count_result_placeholders("No placeholders here.") == 0

    def test_counts_one(self):
        assert count_result_placeholders("BSI = {{RESULT: anchor_bsi}}") == 1

    def test_counts_multiple(self):
        text = "{{RESULT: a}}, {{RESULT: b}}, {{RESULT: c}}"
        assert count_result_placeholders(text) == 3

    def test_does_not_count_partial(self):
        assert count_result_placeholders("{{RESULT:}}") == 0  # empty body — regex requires content
        # Actually the regex requires at least one non-} char after colon, let's just verify no crash


# ── TestRunGate4Scan ───────────────────────────────────────────────────────────

class TestRunGate4Scan:
    def test_missing_when_paper_does_not_exist(self, tmp_path):
        result = run_gate4_scan(tmp_path / "nonexistent.md")
        assert result["status"] == "MISSING"
        assert result["proceed"] is False

    def test_pending_when_no_violations_but_placeholders(self, tmp_path):
        paper = _write_paper(tmp_path, _PLACEHOLDER_MAIN)
        result = run_gate4_scan(paper)
        assert result["status"] == "PENDING"
        assert result["proceed"] is False
        assert result["n_placeholders"] > 0
        assert result["n_violations"] == 0

    def test_pass_when_clean_and_no_placeholders(self, tmp_path):
        paper = _write_paper(tmp_path, _CLEAN_MAIN)
        result = run_gate4_scan(paper)
        assert result["status"] == "PASS"
        assert result["proceed"] is True

    def test_fail_when_tier_c_violation_in_main(self, tmp_path):
        paper = _write_paper(tmp_path, _TIER_C_MAIN)
        result = run_gate4_scan(paper)
        assert result["status"] == "FAIL"
        assert result["proceed"] is False
        assert result["n_violations"] >= 1

    def test_appendix_violations_do_not_trigger_fail(self, tmp_path):
        paper = _write_paper(tmp_path, _CLEAN_MAIN, appendix_content=_TIER_C_MAIN)
        result = run_gate4_scan(paper)
        # Violations are only in appendix — main text is clean
        assert result["status"] in ("PASS", "PENDING")

    def test_result_dict_has_all_required_keys(self, tmp_path):
        paper = _write_paper(tmp_path, _CLEAN_MAIN)
        result = run_gate4_scan(paper)
        for key in ("status", "proceed", "n_violations", "violations",
                    "n_placeholders", "source_file", "recommendation"):
            assert key in result, f"Missing key: {key}"

    def test_fail_takes_priority_over_pending(self, tmp_path):
        content = _PLACEHOLDER_MAIN + "\nThis is caused by the transformer.\n"
        paper = _write_paper(tmp_path, content)
        result = run_gate4_scan(paper)
        assert result["status"] == "FAIL"

    def test_n_violations_matches_len_violations(self, tmp_path):
        paper = _write_paper(tmp_path, _TIER_C_MAIN)
        result = run_gate4_scan(paper)
        assert result["n_violations"] == len(result["violations"])

    def test_source_file_matches_paper_path(self, tmp_path):
        paper = _write_paper(tmp_path, _CLEAN_MAIN)
        result = run_gate4_scan(paper)
        assert str(paper) == result["source_file"]

    def test_real_paper_is_pending(self):
        if not PAPER_PATH.exists():
            pytest.skip("Real working paper not present")
        result = run_gate4_scan(PAPER_PATH)
        # Real paper has placeholders → PENDING (or PASS if placeholders filled)
        assert result["status"] in ("PASS", "PENDING")
        assert result["n_violations"] == 0, (
            f"Unexpected Tier C violations in real paper: {result['violations']}"
        )


# ── TestCLI ────────────────────────────────────────────────────────────────────

class TestCLI:
    def test_exits_0_on_pass(self, tmp_path):
        paper = _write_paper(tmp_path, _CLEAN_MAIN)
        try:
            _scanner.main(["--paper", str(paper), "--quiet"])
        except SystemExit as e:
            assert e.code == 0 or e.code is None

    def test_exits_1_on_fail(self, tmp_path):
        paper = _write_paper(tmp_path, _TIER_C_MAIN)
        with pytest.raises(SystemExit) as exc:
            _scanner.main(["--paper", str(paper), "--quiet"])
        assert exc.value.code == 1


# ── TestCheckGate4ScanIn09 ────────────────────────────────────────────────────

class TestCheckGate4ScanIn09:
    def test_real_paper_pending_or_pass(self):
        if not PAPER_PATH.exists():
            pytest.skip("Real working paper not present")
        result = _gates.check_gate4_scan()
        assert result["status"] in ("PASS", "PENDING")

    def test_pass_on_clean_synthetic_paper(self, tmp_path):
        paper = _write_paper(tmp_path, _CLEAN_MAIN)
        result = _gates.check_gate4_scan(paper)
        assert result["status"] == "PASS"

    def test_fail_on_violation_paper(self, tmp_path):
        paper = _write_paper(tmp_path, _TIER_C_MAIN)
        result = _gates.check_gate4_scan(paper)
        assert result["status"] == "FAIL"


# ── TestRenderMarkdownGate4 ────────────────────────────────────────────────────

class TestRenderMarkdownGate4:
    def _make_gate_results(self):
        return (
            {"status": "MISSING", "proceed": False, "recommendation": "run pilot", "source_file": None, "mock_only": False},
            {"status": "MISSING", "proceed": False, "recommendation": "run robustness", "source_file": None, "mock_only": False, "scenarios_passing": 0, "scenarios_failing": 0},
            {"status": "MISSING", "proceed": False, "recommendation": "run full", "source_file": None, "mock_only": False, "n_models_with_bias": 0, "robust_rationality_pivot": False, "criterion_detail": ""},
        )

    def test_gate4_section_present_without_scan(self):
        g1, g2, g3 = self._make_gate_results()
        checklist = _gates.build_gate4_checklist()
        md = _gates._render_markdown(g1, g2, g3, checklist)
        assert "Gate 4" in md

    def test_gate4_section_with_scan_result(self, tmp_path):
        g1, g2, g3 = self._make_gate_results()
        checklist = _gates.build_gate4_checklist()
        paper = _write_paper(tmp_path, _CLEAN_MAIN)
        scan = _gates.check_gate4_scan(paper)
        md = _gates._render_markdown(g1, g2, g3, checklist, scan)
        assert "Gate 4" in md
        assert "n_violations" in md or "Tier C violations" in md or "violations" in md.lower()

    def test_render_markdown_shows_n_violations(self, tmp_path):
        g1, g2, g3 = self._make_gate_results()
        checklist = _gates.build_gate4_checklist()
        paper = _write_paper(tmp_path, _CLEAN_MAIN)
        scan = _gates.check_gate4_scan(paper)
        md = _gates._render_markdown(g1, g2, g3, checklist, scan)
        assert "0" in md  # zero violations

    def test_render_markdown_shows_n_placeholders(self, tmp_path):
        g1, g2, g3 = self._make_gate_results()
        checklist = _gates.build_gate4_checklist()
        paper = _write_paper(tmp_path, _PLACEHOLDER_MAIN)
        scan = _gates.check_gate4_scan(paper)
        md = _gates._render_markdown(g1, g2, g3, checklist, scan)
        assert "PENDING" in md or "placeholder" in md.lower()
