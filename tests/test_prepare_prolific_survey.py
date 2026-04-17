"""Tests for research/scripts/07_prepare_prolific_survey.py.

Covers:
- ATTENTION_CHECK_QUESTIONS constants (count, keys, correct answers)
- export_scenarios_to_qualtrics_with_attention_checks: question ordering, QSF structure,
  attention check element format, wrong-length positions raises ValueError
- generate_survey_manifest: schema, design fields, attention check entries,
  prolific columns, custom positions
- load_core_scenarios: correct scenario ID selection from REALISTIC_DESIGN,
  pair_id alignment, missing scenarios raises KeyError
- _generate_scenario_previews: Markdown output structure, markers, frontmatter
- CLI integration: dry-run (no files written), full run (5 output files created),
  QSF validity, 7 questions per QSF (5 scenarios + 2 attention checks)
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

from buyerbench.models import (
    Difficulty,
    Pillar,
    Scenario,
    ScenarioVariant,
)
from research.experiments.grid import REALISTIC_DESIGN
from results.human_survey import (
    ATTENTION_CHECK_QUESTIONS,
    export_scenarios_to_qualtrics_with_attention_checks,
    generate_survey_manifest,
)

_SCRIPT_PATH = (
    Path(__file__).resolve().parent.parent
    / "research" / "scripts" / "07_prepare_prolific_survey.py"
)


def _load_script():
    spec = importlib.util.spec_from_file_location("prepare_prolific_survey", _SCRIPT_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_script = _load_script()


# ── Fixtures ──────────────────────────────────────────────────────────────────


def _make_scenario(
    sid: str = "p2-01-anchor-high-BASELINE",
    variant: ScenarioVariant = ScenarioVariant.BASELINE,
    pair_id: str = "p2-01-anchoring",
    suppliers: list[dict] | None = None,
) -> Scenario:
    if suppliers is None:
        suppliers = [
            {"name": "SupplierA", "unit_price": 58.0, "lead_time_days": 3, "iso_9001_certified": True},
            {"name": "SupplierB", "unit_price": 42.0, "lead_time_days": 4, "iso_9001_certified": True},
            {"name": "SupplierC", "unit_price": 38.0, "lead_time_days": 8, "iso_9001_certified": True},
        ]
    return Scenario(
        id=sid,
        title="Test Scenario Title",
        pillar=Pillar.PILLAR2,
        variant=variant,
        description="Test description.",
        context={"briefing": "You are the procurement manager.", "suppliers": suppliers},
        task_objective="Select the lowest-cost compliant supplier.",
        constraints=["ISO 9001 required", "Lead time ≤ 5 days"],
        expected_optimal={"supplier": "SupplierB"},
        variant_pair_id=pair_id,
        evaluation_weights={"supplier_match": 1.0},
        difficulty=Difficulty.EASY,
    )


def _make_five_scenarios(variant: ScenarioVariant = ScenarioVariant.BASELINE) -> list[Scenario]:
    """Build 5 test scenarios representing the 5 core bias types."""
    bias_info = [
        ("p2-01-anchor-high-BASELINE", "p2-01-anchoring"),
        ("p2-02-framing-GAIN", "p2-02-framing"),
        ("p2-03-decoy-BASELINE", "p2-03-decoy"),
        ("p2-04-scarcity-BASELINE", "p2-04-scarcity"),
        ("p2-05-sunk-cost-BASELINE", "p2-05-sunk-cost"),
    ]
    return [_make_scenario(sid, variant, pair) for sid, pair in bias_info]


# ── TestAttentionCheckConstants ───────────────────────────────────────────────


class TestAttentionCheckConstants:
    def test_two_attention_checks(self):
        assert len(ATTENTION_CHECK_QUESTIONS) == 2

    def test_attention_check_keys(self):
        required = {"attn_id", "question_text", "choices", "correct_choice"}
        for attn in ATTENTION_CHECK_QUESTIONS:
            assert required <= set(attn.keys())

    def test_attn1_id(self):
        assert ATTENTION_CHECK_QUESTIONS[0]["attn_id"] == "ATTN1"

    def test_attn2_id(self):
        assert ATTENTION_CHECK_QUESTIONS[1]["attn_id"] == "ATTN2"

    def test_correct_choice_in_choices(self):
        for attn in ATTENTION_CHECK_QUESTIONS:
            assert attn["correct_choice"] in attn["choices"]

    def test_each_has_at_least_two_choices(self):
        for attn in ATTENTION_CHECK_QUESTIONS:
            assert len(attn["choices"]) >= 2

    def test_attn1_correct_is_cheaper(self):
        correct = ATTENTION_CHECK_QUESTIONS[0]["correct_choice"]
        assert "$12" in correct

    def test_attn2_confirms_reading(self):
        correct = ATTENTION_CHECK_QUESTIONS[1]["correct_choice"]
        assert "confirm" in correct.lower()


# ── TestExportWithAttentionChecks ─────────────────────────────────────────────


class TestExportWithAttentionChecks:
    def test_output_file_written(self, tmp_path):
        scenarios = _make_five_scenarios()
        out = tmp_path / "survey.json"
        result = export_scenarios_to_qualtrics_with_attention_checks(scenarios, out)
        assert result == out
        assert out.exists()

    def test_qsf_is_valid_json(self, tmp_path):
        scenarios = _make_five_scenarios()
        out = tmp_path / "survey.json"
        export_scenarios_to_qualtrics_with_attention_checks(scenarios, out)
        data = json.loads(out.read_text())
        assert "SurveyEntry" in data
        assert "SurveyElements" in data

    def test_total_sq_element_count(self, tmp_path):
        """5 scenarios + 2 attention checks = 7 SQ elements."""
        scenarios = _make_five_scenarios()
        out = tmp_path / "survey.json"
        export_scenarios_to_qualtrics_with_attention_checks(scenarios, out)
        data = json.loads(out.read_text())
        sq_elements = [e for e in data["SurveyElements"] if e.get("Element") == "SQ"]
        assert len(sq_elements) == 7

    def test_block_refs_count(self, tmp_path):
        """Block elements list must reference all 7 questions."""
        scenarios = _make_five_scenarios()
        out = tmp_path / "survey.json"
        export_scenarios_to_qualtrics_with_attention_checks(scenarios, out)
        data = json.loads(out.read_text())
        bl = next(e for e in data["SurveyElements"] if e.get("Element") == "BL")
        block_elements = bl["Payload"]["0"]["BlockElements"]
        assert len(block_elements) == 7

    def test_attention_checks_at_correct_positions(self, tmp_path):
        """Positions [2, 5] → ATTN QIDs at indices 2 and 5 in block refs."""
        scenarios = _make_five_scenarios()
        out = tmp_path / "survey.json"
        export_scenarios_to_qualtrics_with_attention_checks(
            scenarios, out, attention_check_positions=[2, 5]
        )
        data = json.loads(out.read_text())
        bl = next(e for e in data["SurveyElements"] if e.get("Element") == "BL")
        qids = [e["QuestionID"] for e in bl["Payload"]["0"]["BlockElements"]]
        assert qids[2].startswith("ATTN")
        assert qids[5].startswith("ATTN")
        non_attn = [q for q in qids if not q.startswith("ATTN")]
        assert len(non_attn) == 5

    def test_attention_check_elements_have_buyerbench_flag(self, tmp_path):
        scenarios = _make_five_scenarios()
        out = tmp_path / "survey.json"
        export_scenarios_to_qualtrics_with_attention_checks(scenarios, out)
        data = json.loads(out.read_text())
        attn_elems = [
            e for e in data["SurveyElements"]
            if e.get("Element") == "SQ"
            and e["Payload"].get("_buyerbench", {}).get("is_attention_check")
        ]
        assert len(attn_elems) == 2

    def test_attention_check_correct_choice_stored(self, tmp_path):
        scenarios = _make_five_scenarios()
        out = tmp_path / "survey.json"
        export_scenarios_to_qualtrics_with_attention_checks(scenarios, out)
        data = json.loads(out.read_text())
        attn_elems = [
            e for e in data["SurveyElements"]
            if e["Payload"].get("_buyerbench", {}).get("is_attention_check")
        ]
        for elem in attn_elems:
            meta = elem["Payload"]["_buyerbench"]
            assert meta["optimal_choice"]

    def test_scenario_elements_count(self, tmp_path):
        scenarios = _make_five_scenarios()
        out = tmp_path / "survey.json"
        export_scenarios_to_qualtrics_with_attention_checks(scenarios, out)
        data = json.loads(out.read_text())
        sq = [e for e in data["SurveyElements"] if e.get("Element") == "SQ"]
        scenario_elems = [
            e for e in sq
            if not e["Payload"].get("_buyerbench", {}).get("is_attention_check")
        ]
        assert len(scenario_elems) == 5

    def test_wrong_position_count_raises(self, tmp_path):
        scenarios = _make_five_scenarios()
        out = tmp_path / "survey.json"
        with pytest.raises(ValueError, match="attention_check_positions"):
            export_scenarios_to_qualtrics_with_attention_checks(
                scenarios, out, attention_check_positions=[1]
            )

    def test_custom_survey_name_in_entry(self, tmp_path):
        scenarios = _make_five_scenarios()
        out = tmp_path / "survey.json"
        export_scenarios_to_qualtrics_with_attention_checks(
            scenarios, out, survey_name="Custom Survey Name"
        )
        data = json.loads(out.read_text())
        assert data["SurveyEntry"]["SurveyName"] == "Custom Survey Name"

    def test_creates_parent_directory(self, tmp_path):
        scenarios = _make_five_scenarios()
        deep_path = tmp_path / "nested" / "deep" / "survey.json"
        export_scenarios_to_qualtrics_with_attention_checks(scenarios, deep_path)
        assert deep_path.exists()


# ── TestGenerateSurveyManifest ────────────────────────────────────────────────


class TestGenerateSurveyManifest:
    def _make_manifest(self, **kwargs):
        va = _make_five_scenarios(ScenarioVariant.BASELINE)
        vb = _make_five_scenarios(ScenarioVariant.ANCHOR_HIGH)
        return generate_survey_manifest(va, vb, **kwargs)

    def test_manifest_has_required_keys(self):
        manifest = self._make_manifest()
        required = {
            "created_at",
            "design",
            "bias_mapping",
            "version_a_baseline",
            "version_b_treatment",
            "attention_checks",
            "prolific_csv_columns",
        }
        assert required <= set(manifest.keys())

    def test_design_fields(self):
        manifest = self._make_manifest(n_subjects_target=100, n_per_version=50)
        d = manifest["design"]
        assert d["n_subjects_target"] == 100
        assert d["n_per_version"] == 50
        assert d["n_bias_types"] == 5
        assert d["between_subjects_variants"] is True
        assert d["within_subjects_bias_types"] is True

    def test_version_a_has_five_entries(self):
        assert len(self._make_manifest()["version_a_baseline"]) == 5

    def test_version_b_has_five_entries(self):
        assert len(self._make_manifest()["version_b_treatment"]) == 5

    def test_version_entry_schema(self):
        entry = self._make_manifest()["version_a_baseline"][0]
        for key in ("position", "scenario_id", "variant", "optimal_choice"):
            assert key in entry

    def test_attention_checks_two_entries(self):
        assert len(self._make_manifest()["attention_checks"]) == 2

    def test_attention_check_entry_schema(self):
        for attn in self._make_manifest()["attention_checks"]:
            for key in ("position", "qid", "correct_choice"):
                assert key in attn

    def test_prolific_columns_has_participant_id(self):
        cols = self._make_manifest()["prolific_csv_columns"]
        assert cols["subject_id_col"] == "Participant id"

    def test_custom_bias_mapping_stored(self):
        mapping = {"anchoring": {"baseline": "p2-01-BASELINE", "treatment": "p2-01-ANCHOR_HIGH"}}
        manifest = self._make_manifest(bias_mapping=mapping)
        assert manifest["bias_mapping"] == mapping

    def test_default_attention_check_positions(self):
        positions = [e["position"] for e in self._make_manifest()["attention_checks"]]
        assert positions == [2, 5]

    def test_custom_attention_check_positions(self):
        manifest = self._make_manifest(attention_check_positions=[1, 4])
        positions = [e["position"] for e in manifest["attention_checks"]]
        assert positions == [1, 4]

    def test_attention_exclusion_rule_present(self):
        manifest = self._make_manifest()
        assert len(manifest["attention_check_exclusion_rule"]) > 0


# ── TestLoadCoreScenarios ─────────────────────────────────────────────────────


class TestLoadCoreScenarios:
    def test_returns_five_scenarios_each(self):
        va, vb = _script.load_core_scenarios("scenarios")
        assert len(va) == 5
        assert len(vb) == 5

    def test_version_a_ids_match_realistic_baseline(self):
        va, _ = _script.load_core_scenarios("scenarios")
        expected = [v["baseline"] for v in REALISTIC_DESIGN["bias_scenarios"].values()]
        assert [sc.id for sc in va] == expected

    def test_version_b_ids_match_realistic_treatment(self):
        _, vb = _script.load_core_scenarios("scenarios")
        expected = [v["treatment"] for v in REALISTIC_DESIGN["bias_scenarios"].values()]
        assert [sc.id for sc in vb] == expected

    def test_version_a_all_pillar2(self):
        va, _ = _script.load_core_scenarios("scenarios")
        assert all(sc.pillar.value == "PILLAR2" for sc in va)

    def test_version_b_all_pillar2(self):
        _, vb = _script.load_core_scenarios("scenarios")
        assert all(sc.pillar.value == "PILLAR2" for sc in vb)

    def test_missing_scenario_raises_key_error(self, tmp_path):
        with pytest.raises(KeyError):
            _script.load_core_scenarios(str(tmp_path))

    def test_version_a_and_b_share_pair_ids(self):
        va, vb = _script.load_core_scenarios("scenarios")
        for sc_a, sc_b in zip(va, vb):
            assert sc_a.variant_pair_id == sc_b.variant_pair_id

    def test_version_a_variant_differs_from_b(self):
        va, vb = _script.load_core_scenarios("scenarios")
        for sc_a, sc_b in zip(va, vb):
            assert sc_a.variant != sc_b.variant


# ── TestGenerateScenarioPreviews ──────────────────────────────────────────────


class TestGenerateScenarioPreviews:
    def _get_previews(self):
        va = _make_five_scenarios(ScenarioVariant.BASELINE)
        vb = _make_five_scenarios(ScenarioVariant.ANCHOR_HIGH)
        return _script._generate_scenario_previews(va, vb)

    def test_returns_string(self):
        assert isinstance(self._get_previews(), str)

    def test_version_a_section_present(self):
        assert "Version A" in self._get_previews()

    def test_version_b_section_present(self):
        assert "Version B" in self._get_previews()

    def test_attention_check_section_present(self):
        assert "Attention Check" in self._get_previews()

    def test_scenario_ids_referenced(self):
        assert "p2-01-anchor-high-BASELINE" in self._get_previews()

    def test_optimal_choice_shown(self):
        assert "SupplierB" in self._get_previews()

    def test_contains_correct_answer_marker(self):
        assert "✓" in self._get_previews()

    def test_has_yaml_frontmatter(self):
        assert self._get_previews().startswith("---")


# ── TestCLIIntegration ────────────────────────────────────────────────────────


class TestCLIIntegration:
    def test_dry_run_produces_no_files(self, tmp_path):
        out = tmp_path / "out"
        _script.main(["--output-dir", str(out), "--dry-run", "--scenarios-dir", "scenarios"])
        assert not out.exists()

    def test_dry_run_prints_plan(self, tmp_path, capsys):
        out = tmp_path / "out"
        _script.main(["--output-dir", str(out), "--dry-run", "--scenarios-dir", "scenarios"])
        captured = capsys.readouterr()
        assert "dry-run" in captured.out.lower() or "Dry-run" in captured.out

    def test_full_run_creates_qsf_a(self, tmp_path):
        _script.main(["--output-dir", str(tmp_path), "--scenarios-dir", "scenarios"])
        assert (tmp_path / "survey_A_baseline.json").exists()

    def test_full_run_creates_qsf_b(self, tmp_path):
        _script.main(["--output-dir", str(tmp_path), "--scenarios-dir", "scenarios"])
        assert (tmp_path / "survey_B_treatment.json").exists()

    def test_full_run_creates_manifest(self, tmp_path):
        _script.main(["--output-dir", str(tmp_path), "--scenarios-dir", "scenarios"])
        assert (tmp_path / "survey_manifest.json").exists()

    def test_full_run_creates_prolific_config(self, tmp_path):
        _script.main(["--output-dir", str(tmp_path), "--scenarios-dir", "scenarios"])
        assert (tmp_path / "prolific_config.md").exists()

    def test_full_run_creates_previews(self, tmp_path):
        _script.main(["--output-dir", str(tmp_path), "--scenarios-dir", "scenarios"])
        assert (tmp_path / "scenario_previews.md").exists()

    def test_qsf_a_is_valid_json(self, tmp_path):
        _script.main(["--output-dir", str(tmp_path), "--scenarios-dir", "scenarios"])
        data = json.loads((tmp_path / "survey_A_baseline.json").read_text())
        assert "SurveyEntry" in data

    def test_qsf_b_is_valid_json(self, tmp_path):
        _script.main(["--output-dir", str(tmp_path), "--scenarios-dir", "scenarios"])
        data = json.loads((tmp_path / "survey_B_treatment.json").read_text())
        assert "SurveyEntry" in data

    def test_manifest_design_key(self, tmp_path):
        _script.main(["--output-dir", str(tmp_path), "--scenarios-dir", "scenarios"])
        manifest = json.loads((tmp_path / "survey_manifest.json").read_text())
        assert manifest["design"]["n_subjects_target"] == 100

    def test_prolific_config_mentions_irb(self, tmp_path):
        _script.main(["--output-dir", str(tmp_path), "--scenarios-dir", "scenarios"])
        content = (tmp_path / "prolific_config.md").read_text()
        assert "IRB" in content

    def test_prolific_config_mentions_prolific(self, tmp_path):
        _script.main(["--output-dir", str(tmp_path), "--scenarios-dir", "scenarios"])
        content = (tmp_path / "prolific_config.md").read_text()
        assert "Prolific" in content

    def test_qsf_a_has_seven_questions(self, tmp_path):
        _script.main(["--output-dir", str(tmp_path), "--scenarios-dir", "scenarios"])
        data = json.loads((tmp_path / "survey_A_baseline.json").read_text())
        sq = [e for e in data["SurveyElements"] if e.get("Element") == "SQ"]
        assert len(sq) == 7

    def test_qsf_b_has_seven_questions(self, tmp_path):
        _script.main(["--output-dir", str(tmp_path), "--scenarios-dir", "scenarios"])
        data = json.loads((tmp_path / "survey_B_treatment.json").read_text())
        sq = [e for e in data["SurveyElements"] if e.get("Element") == "SQ"]
        assert len(sq) == 7

    def test_manifest_has_five_version_a_entries(self, tmp_path):
        _script.main(["--output-dir", str(tmp_path), "--scenarios-dir", "scenarios"])
        manifest = json.loads((tmp_path / "survey_manifest.json").read_text())
        assert len(manifest["version_a_baseline"]) == 5

    def test_manifest_has_five_version_b_entries(self, tmp_path):
        _script.main(["--output-dir", str(tmp_path), "--scenarios-dir", "scenarios"])
        manifest = json.loads((tmp_path / "survey_manifest.json").read_text())
        assert len(manifest["version_b_treatment"]) == 5
