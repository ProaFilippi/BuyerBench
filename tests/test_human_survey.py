"""Tests for UPGRADE-13: human comparison survey harness (results/human_survey.py)."""
from __future__ import annotations

import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path

import pytest

from buyerbench.models import (
    Difficulty,
    Pillar,
    Scenario,
    ScenarioVariant,
)
from results.aggregate_cells import CellAggregate
from results.human_survey import (
    HumanCellAggregate,
    HumanCellReport,
    HumanComparisonResult,
    HumanObservation,
    _wilson_score_ci_95,
    aggregate_human_cells,
    compare_human_llm_bsi,
    compute_human_bsi_from_survey,
    export_scenario_to_survey,
    export_scenarios_to_qualtrics,
    observations_to_csv,
    parse_prolific_csv,
    write_human_cell_report,
    write_human_comparisons,
)


# ── Fixtures / Helpers ────────────────────────────────────────────────────────


def _make_scenario(
    scenario_id: str = "p2-01-anchor-high-BASELINE",
    variant: ScenarioVariant = ScenarioVariant.BASELINE,
    variant_pair_id: str = "p2-01-anchoring",
    suppliers: list[dict] | None = None,
) -> Scenario:
    """Build a minimal Scenario fixture for testing."""
    if suppliers is None:
        suppliers = [
            {"name": "SupplierA", "unit_price": 58.00, "lead_time_days": 3, "iso_9001_certified": True},
            {"name": "SupplierB", "unit_price": 42.00, "lead_time_days": 4, "iso_9001_certified": True},
            {"name": "SupplierC", "unit_price": 38.00, "lead_time_days": 8, "iso_9001_certified": True},
        ]
    return Scenario(
        id=scenario_id,
        title="Industrial Component Sourcing",
        pillar=Pillar.PILLAR2,
        variant=variant,
        description="Test scenario for procurement benchmark.",
        context={
            "briefing": "You are the procurement manager. Select the best supplier.",
            "suppliers": suppliers,
        },
        task_objective="Select the lowest-cost compliant supplier.",
        constraints=["ISO 9001 required", "Lead time ≤ 5 days"],
        expected_optimal={"supplier": "SupplierB", "unit_price": 42.00},
        variant_pair_id=variant_pair_id,
        evaluation_weights={"supplier_match": 1.0},
        difficulty=Difficulty.EASY,
    )


def _make_observation(
    subject_id: str = "S001",
    scenario_id: str = "p2-01-anchor-high-BASELINE",
    selected_choice: str = "SupplierB",
    optimal_choice: str = "SupplierB",
    variant: str = "BASELINE",
    variant_pair_id: str = "p2-01-anchoring",
    bias_category: str = "anchoring",
    attention_check_passed: bool | None = True,
) -> HumanObservation:
    return HumanObservation.from_row(
        subject_id=subject_id,
        scenario_id=scenario_id,
        selected_choice=selected_choice,
        optimal_choice=optimal_choice,
        variant=variant,
        variant_pair_id=variant_pair_id,
        bias_category=bias_category,
        attention_check_passed=attention_check_passed,
    )


def _make_llm_cell(
    agent_id: str = "openrouter-gpt-4o",
    variant_pair_id: str = "p2-01-anchoring",
    variant: str = "ANCHOR_HIGH",
    bias_category: str = "anchoring",
    mean_bsi: float = 0.3,
    std_bsi: float = 0.1,
    n_valid_runs: int = 50,
) -> CellAggregate:
    return CellAggregate(
        cell_id=f"{agent_id}__{variant_pair_id}__{variant}__None",
        agent_id=agent_id,
        scenario_id=f"p2-01-anchor-high-{variant}",
        variant_pair_id=variant_pair_id,
        variant=variant,
        bias_category=bias_category,
        temperature=None,
        n_runs=n_valid_runs,
        n_valid_runs=n_valid_runs,
        mean_bsi=mean_bsi,
        std_bsi=std_bsi,
        ci_lower_95=mean_bsi - 0.05,
        ci_upper_95=mean_bsi + 0.05,
        choice_rate_correct=1.0 - mean_bsi,
        choice_rate_distribution={"SupplierB": 35, "SupplierA": 15},
        mean_optimality_gap=mean_bsi * 0.5,
        treatment_effect_vs_baseline=None,
    )


# ── Wilson Score CI ───────────────────────────────────────────────────────────


class TestWilsonScoreCI:
    def test_all_correct_gives_ci_near_one(self):
        lo, hi = _wilson_score_ci_95(50, 50)
        assert lo > 0.9
        assert hi == pytest.approx(1.0, abs=0.01)

    def test_none_correct_gives_ci_near_zero(self):
        lo, hi = _wilson_score_ci_95(0, 50)
        assert lo == pytest.approx(0.0, abs=0.01)
        assert hi < 0.1

    def test_half_correct(self):
        lo, hi = _wilson_score_ci_95(25, 50)
        assert lo < 0.5 < hi
        # CI should be roughly (0.36, 0.64) for 50 subjects
        assert lo > 0.3
        assert hi < 0.7

    def test_zero_subjects_returns_zeros(self):
        lo, hi = _wilson_score_ci_95(0, 0)
        assert lo == 0.0 and hi == 0.0

    def test_single_subject_all_correct(self):
        lo, hi = _wilson_score_ci_95(1, 1)
        assert 0.0 <= lo <= hi <= 1.0

    def test_ci_bounds_are_valid_probabilities(self):
        for k, n in [(0, 10), (5, 10), (10, 10), (1, 100), (99, 100)]:
            lo, hi = _wilson_score_ci_95(k, n)
            assert 0.0 <= lo <= hi <= 1.0


# ── HumanObservation ─────────────────────────────────────────────────────────


class TestHumanObservation:
    def test_correct_choice_sets_flag(self):
        obs = _make_observation(selected_choice="SupplierB", optimal_choice="SupplierB")
        assert obs.choice_is_correct is True

    def test_incorrect_choice_clears_flag(self):
        obs = _make_observation(selected_choice="SupplierA", optimal_choice="SupplierB")
        assert obs.choice_is_correct is False

    def test_case_insensitive_matching(self):
        obs = HumanObservation.from_row(
            subject_id="S001",
            scenario_id="p2-01",
            selected_choice="supplierb",
            optimal_choice="SupplierB",
            variant="BASELINE",
        )
        assert obs.choice_is_correct is True

    def test_optional_fields_default_to_none(self):
        obs = HumanObservation.from_row(
            subject_id="S001",
            scenario_id="p2-01",
            selected_choice="SupplierB",
            optimal_choice="SupplierB",
            variant="BASELINE",
        )
        assert obs.response_time_ms is None
        assert obs.attention_check_passed is None
        assert obs.variant_pair_id is None

    def test_timestamp_defaults_to_utc(self):
        obs = _make_observation()
        assert obs.timestamp.tzinfo is not None

    def test_model_has_all_required_fields(self):
        obs = _make_observation()
        assert obs.subject_id == "S001"
        assert obs.scenario_id == "p2-01-anchor-high-BASELINE"
        assert obs.variant == "BASELINE"
        assert obs.optimal_choice == "SupplierB"


# ── export_scenario_to_survey ─────────────────────────────────────────────────


class TestExportScenarioToSurvey:
    def test_returns_dict_with_required_keys(self):
        scenario = _make_scenario()
        vignette = export_scenario_to_survey(scenario)
        required_keys = {
            "scenario_id", "variant", "variant_pair_id", "bias_category",
            "title", "preamble", "context_text", "question", "choices",
            "optimal_choice", "constraints_text",
        }
        assert required_keys.issubset(vignette.keys())

    def test_scenario_id_matches(self):
        scenario = _make_scenario(scenario_id="p2-01-anchor-high-BASELINE")
        vignette = export_scenario_to_survey(scenario)
        assert vignette["scenario_id"] == "p2-01-anchor-high-BASELINE"

    def test_variant_matches(self):
        scenario = _make_scenario(variant=ScenarioVariant.ANCHOR_HIGH)
        vignette = export_scenario_to_survey(scenario)
        assert vignette["variant"] == "ANCHOR_HIGH"

    def test_no_benchmark_language_in_preamble(self):
        scenario = _make_scenario()
        vignette = export_scenario_to_survey(scenario)
        preamble = vignette["preamble"].lower()
        assert "buyerbench" not in preamble
        assert "benchmark" not in preamble
        assert "ai evaluation" not in preamble

    def test_choices_extracted_from_suppliers(self):
        scenario = _make_scenario()
        vignette = export_scenario_to_survey(scenario)
        assert "SupplierA" in vignette["choices"]
        assert "SupplierB" in vignette["choices"]
        assert "SupplierC" in vignette["choices"]

    def test_optimal_choice_is_correct(self):
        scenario = _make_scenario()
        vignette = export_scenario_to_survey(scenario)
        assert vignette["optimal_choice"] == "SupplierB"

    def test_bias_category_inferred_from_pair_id(self):
        scenario = _make_scenario(variant_pair_id="p2-01-anchoring")
        vignette = export_scenario_to_survey(scenario)
        assert vignette["bias_category"] == "anchoring"

    def test_context_text_includes_supplier_names(self):
        scenario = _make_scenario()
        vignette = export_scenario_to_survey(scenario)
        assert "SupplierA" in vignette["context_text"]
        assert "SupplierB" in vignette["context_text"]

    def test_constraints_included_in_text(self):
        scenario = _make_scenario()
        vignette = export_scenario_to_survey(scenario)
        assert "ISO 9001" in vignette["constraints_text"]

    def test_scenario_without_suppliers_falls_back_gracefully(self):
        scenario = Scenario(
            id="p2-no-suppliers",
            title="Simple Choice",
            pillar=Pillar.PILLAR2,
            variant=ScenarioVariant.BASELINE,
            description="No supplier list.",
            context={"briefing": "Choose a vendor."},
            task_objective="Choose the best vendor.",
            expected_optimal={"contract": "ContractAlpha"},
            variant_pair_id="p2-no-suppliers-pair",
        )
        vignette = export_scenario_to_survey(scenario)
        assert vignette["optimal_choice"] == "ContractAlpha"
        # choices fallback: optimal value as single option
        assert "ContractAlpha" in vignette["choices"]


# ── export_scenarios_to_qualtrics ─────────────────────────────────────────────


class TestExportScenariosToQualtrics:
    def test_creates_file(self, tmp_path):
        scenario = _make_scenario()
        out = export_scenarios_to_qualtrics([scenario], tmp_path / "survey.json")
        assert out.exists()

    def test_output_is_valid_json(self, tmp_path):
        scenario = _make_scenario()
        out = export_scenarios_to_qualtrics([scenario], tmp_path / "survey.json")
        data = json.loads(out.read_text())
        assert isinstance(data, dict)

    def test_qsf_has_survey_entry(self, tmp_path):
        scenario = _make_scenario()
        out = export_scenarios_to_qualtrics([scenario], tmp_path / "survey.json")
        data = json.loads(out.read_text())
        assert "SurveyEntry" in data
        assert "SurveyElements" in data

    def test_one_question_element_per_scenario(self, tmp_path):
        scenarios = [
            _make_scenario("p2-01-anchor-high-BASELINE"),
            _make_scenario("p2-01-anchor-high-ANCHOR_HIGH", variant=ScenarioVariant.ANCHOR_HIGH),
        ]
        out = export_scenarios_to_qualtrics(scenarios, tmp_path / "survey.json")
        data = json.loads(out.read_text())
        # Elements = 1 block element + N question elements
        question_elements = [e for e in data["SurveyElements"] if e.get("Element") == "SQ"]
        assert len(question_elements) == 2

    def test_question_has_multiple_choice_type(self, tmp_path):
        scenario = _make_scenario()
        out = export_scenarios_to_qualtrics([scenario], tmp_path / "survey.json")
        data = json.loads(out.read_text())
        sq = next(e for e in data["SurveyElements"] if e.get("Element") == "SQ")
        assert sq["Payload"]["QuestionType"] == "MC"

    def test_choices_match_supplier_names(self, tmp_path):
        scenario = _make_scenario()
        out = export_scenarios_to_qualtrics([scenario], tmp_path / "survey.json")
        data = json.loads(out.read_text())
        sq = next(e for e in data["SurveyElements"] if e.get("Element") == "SQ")
        choices = {v["Display"] for v in sq["Payload"]["Choices"].values()}
        assert "SupplierA" in choices
        assert "SupplierB" in choices

    def test_buyerbench_metadata_attached(self, tmp_path):
        scenario = _make_scenario()
        out = export_scenarios_to_qualtrics([scenario], tmp_path / "survey.json")
        data = json.loads(out.read_text())
        sq = next(e for e in data["SurveyElements"] if e.get("Element") == "SQ")
        meta = sq["Payload"]["_buyerbench"]
        assert meta["scenario_id"] == scenario.id
        assert meta["optimal_choice"] == "SupplierB"

    def test_secondary_attribute_is_scenario_id(self, tmp_path):
        scenario = _make_scenario("p2-01-anchor-high-BASELINE")
        out = export_scenarios_to_qualtrics([scenario], tmp_path / "survey.json")
        data = json.loads(out.read_text())
        sq = next(e for e in data["SurveyElements"] if e.get("Element") == "SQ")
        assert sq["SecondaryAttribute"] == "p2-01-anchor-high-BASELINE"

    def test_custom_survey_name_used(self, tmp_path):
        scenario = _make_scenario()
        out = export_scenarios_to_qualtrics(
            [scenario], tmp_path / "survey.json", survey_name="My Custom Survey"
        )
        data = json.loads(out.read_text())
        assert data["SurveyEntry"]["SurveyName"] == "My Custom Survey"

    def test_no_benchmark_language_in_survey_name(self, tmp_path):
        scenario = _make_scenario()
        out = export_scenarios_to_qualtrics([scenario], tmp_path / "survey.json")
        data = json.loads(out.read_text())
        name = data["SurveyEntry"]["SurveyName"].lower()
        assert "buyerbench" not in name
        assert "benchmark" not in name


# ── parse_prolific_csv ────────────────────────────────────────────────────────


def _write_test_csv(tmp_path: Path, rows: list[dict], filename: str = "responses.csv") -> Path:
    """Write a test CSV and return its path."""
    path = tmp_path / filename
    if not rows:
        path.write_text("")
        return path
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return path


class TestParseProlificCsv:
    def test_basic_parsing(self, tmp_path):
        rows = [
            {
                "Participant id": "S001",
                "scenario_id": "p2-01-anchor-high-BASELINE",
                "selected_choice": "SupplierB",
                "variant": "BASELINE",
                "variant_pair_id": "p2-01-anchoring",
                "bias_category": "anchoring",
                "optimal_choice": "SupplierB",
            }
        ]
        path = _write_test_csv(tmp_path, rows)
        observations = parse_prolific_csv(path)
        assert len(observations) == 1
        obs = observations[0]
        assert obs.subject_id == "S001"
        assert obs.selected_choice == "SupplierB"
        assert obs.choice_is_correct is True

    def test_multiple_rows(self, tmp_path):
        rows = [
            {
                "Participant id": f"S{i:03d}",
                "scenario_id": "p2-01-anchor-high-BASELINE",
                "selected_choice": "SupplierB" if i % 2 == 0 else "SupplierA",
                "variant": "BASELINE",
                "variant_pair_id": "p2-01-anchoring",
                "bias_category": "anchoring",
                "optimal_choice": "SupplierB",
            }
            for i in range(10)
        ]
        path = _write_test_csv(tmp_path, rows)
        observations = parse_prolific_csv(path)
        assert len(observations) == 10

    def test_skips_rows_with_missing_required_fields(self, tmp_path):
        rows = [
            {"Participant id": "", "scenario_id": "p2-01", "selected_choice": "SupplierB",
             "variant": "BASELINE", "variant_pair_id": "", "bias_category": "", "optimal_choice": "SupplierB"},
            {"Participant id": "S002", "scenario_id": "p2-01", "selected_choice": "",
             "variant": "BASELINE", "variant_pair_id": "", "bias_category": "", "optimal_choice": "SupplierB"},
        ]
        path = _write_test_csv(tmp_path, rows)
        observations = parse_prolific_csv(path)
        assert len(observations) == 0

    def test_attention_check_parsing(self, tmp_path):
        rows = [
            {"Participant id": "S001", "scenario_id": "p2-01", "selected_choice": "SupplierB",
             "variant": "BASELINE", "variant_pair_id": "", "bias_category": "", "optimal_choice": "SupplierB",
             "attention_check": "true"},
            {"Participant id": "S002", "scenario_id": "p2-01", "selected_choice": "SupplierA",
             "variant": "BASELINE", "variant_pair_id": "", "bias_category": "", "optimal_choice": "SupplierB",
             "attention_check": "false"},
        ]
        path = _write_test_csv(tmp_path, rows)
        observations = parse_prolific_csv(path, attention_check_col="attention_check")
        assert observations[0].attention_check_passed is True
        assert observations[1].attention_check_passed is False

    def test_response_time_parsing(self, tmp_path):
        rows = [
            {"Participant id": "S001", "scenario_id": "p2-01", "selected_choice": "SupplierB",
             "variant": "BASELINE", "variant_pair_id": "", "bias_category": "", "optimal_choice": "SupplierB",
             "rt_ms": "3200.5"},
        ]
        path = _write_test_csv(tmp_path, rows)
        observations = parse_prolific_csv(path, response_time_col="rt_ms")
        assert observations[0].response_time_ms == pytest.approx(3200.5)

    def test_scenario_map_lookup_fallback(self, tmp_path):
        """optimal_choice and variant looked up from scenario_map when cols absent."""
        scenario = _make_scenario("p2-01-anchor-high-BASELINE")
        scenario_map = {scenario.id: scenario}
        rows = [
            {"Participant id": "S001", "scenario_id": "p2-01-anchor-high-BASELINE",
             "selected_choice": "SupplierB"},
        ]
        path = _write_test_csv(tmp_path, rows)
        observations = parse_prolific_csv(
            path,
            scenario_col="scenario_id",
            choice_col="selected_choice",
            variant_col=None,
            variant_pair_id_col=None,
            bias_category_col=None,
            optimal_choice_col=None,
            scenario_map=scenario_map,
        )
        assert len(observations) == 1
        obs = observations[0]
        assert obs.optimal_choice == "SupplierB"
        assert obs.variant == "BASELINE"
        assert obs.variant_pair_id == "p2-01-anchoring"


# ── observations_to_csv (round-trip) ─────────────────────────────────────────


class TestObservationsToCsv:
    def test_round_trip(self, tmp_path):
        obs1 = _make_observation("S001", selected_choice="SupplierB")
        obs2 = _make_observation("S002", selected_choice="SupplierA")
        out = observations_to_csv([obs1, obs2], tmp_path / "out.csv")
        assert out.exists()
        scenario = _make_scenario()
        scenario_map = {scenario.id: scenario}
        loaded = parse_prolific_csv(out, scenario_map=scenario_map)
        assert len(loaded) == 2
        assert loaded[0].subject_id == "S001"
        assert loaded[1].subject_id == "S002"

    def test_creates_parent_dirs(self, tmp_path):
        obs = _make_observation()
        out = observations_to_csv([obs], tmp_path / "deep" / "dir" / "out.csv")
        assert out.exists()


# ── aggregate_human_cells ─────────────────────────────────────────────────────


class TestAggregateHumanCells:
    def _make_cell_observations(
        self,
        n_correct: int,
        n_total: int,
        variant: str = "BASELINE",
        pair_id: str = "p2-01-anchoring",
        include_failed: bool = False,
    ) -> list[HumanObservation]:
        obs = []
        for i in range(n_total):
            att = True if not include_failed or i < n_total - 1 else False
            obs.append(_make_observation(
                subject_id=f"S{i:03d}",
                selected_choice="SupplierB" if i < n_correct else "SupplierA",
                variant=variant,
                variant_pair_id=pair_id,
                attention_check_passed=att,
            ))
        return obs

    def test_basic_aggregation(self):
        obs = self._make_cell_observations(n_correct=8, n_total=10)
        report = aggregate_human_cells(obs)
        assert report.n_cells == 1
        cell = report.cells[0]
        assert cell.n_subjects == 10
        assert cell.n_valid_subjects == 10
        assert cell.choice_rate_optimal == pytest.approx(0.8)
        assert cell.mean_bsi == pytest.approx(0.2)

    def test_bsi_zero_when_all_correct(self):
        obs = self._make_cell_observations(n_correct=20, n_total=20)
        report = aggregate_human_cells(obs)
        assert report.cells[0].mean_bsi == pytest.approx(0.0)

    def test_bsi_one_when_none_correct(self):
        obs = self._make_cell_observations(n_correct=0, n_total=20)
        report = aggregate_human_cells(obs)
        assert report.cells[0].mean_bsi == pytest.approx(1.0)

    def test_excludes_failed_attention_checks(self):
        # 10 subjects, 1 fails attention check, 7 of remaining 9 correct
        obs = self._make_cell_observations(
            n_correct=7, n_total=10, include_failed=True
        )
        report = aggregate_human_cells(obs, exclude_failed_attention=True)
        cell = report.cells[0]
        assert cell.n_subjects == 10
        assert cell.n_valid_subjects == 9  # 1 excluded

    def test_include_all_when_flag_false(self):
        obs = self._make_cell_observations(
            n_correct=7, n_total=10, include_failed=True
        )
        report = aggregate_human_cells(obs, exclude_failed_attention=False)
        assert report.cells[0].n_valid_subjects == 10

    def test_multiple_cells(self):
        baseline_obs = self._make_cell_observations(
            n_correct=8, n_total=10, variant="BASELINE"
        )
        treatment_obs = self._make_cell_observations(
            n_correct=3, n_total=10, variant="ANCHOR_HIGH"
        )
        report = aggregate_human_cells(baseline_obs + treatment_obs)
        assert report.n_cells == 2

    def test_treatment_effect_computed(self):
        baseline_obs = [
            _make_observation(f"S{i:03d}", selected_choice="SupplierB",
                              variant="BASELINE", variant_pair_id="p2-01-anchoring")
            for i in range(10)
        ]
        treatment_obs = [
            _make_observation(f"T{i:03d}", selected_choice="SupplierA" if i < 5 else "SupplierB",
                              variant="ANCHOR_HIGH", variant_pair_id="p2-01-anchoring")
            for i in range(10)
        ]
        report = aggregate_human_cells(baseline_obs + treatment_obs)
        treatment_cell = next(c for c in report.cells if c.variant == "ANCHOR_HIGH")
        assert treatment_cell.treatment_effect_vs_baseline is not None
        # baseline BSI=0.0 (all correct), treatment BSI=0.5 (5 wrong), effect = +0.5
        assert treatment_cell.treatment_effect_vs_baseline == pytest.approx(0.5)

    def test_ci_bounds_are_valid(self):
        obs = self._make_cell_observations(n_correct=5, n_total=10)
        report = aggregate_human_cells(obs)
        cell = report.cells[0]
        assert 0.0 <= cell.ci_lower_95 <= cell.mean_bsi <= cell.ci_upper_95 <= 1.0

    def test_choice_distribution_recorded(self):
        obs = [
            _make_observation("S001", selected_choice="SupplierA"),
            _make_observation("S002", selected_choice="SupplierB"),
            _make_observation("S003", selected_choice="SupplierB"),
        ]
        report = aggregate_human_cells(obs)
        dist = report.cells[0].choice_rate_distribution
        assert dist.get("SupplierB") == 2
        assert dist.get("SupplierA") == 1

    def test_n_observations_in_report(self):
        obs = self._make_cell_observations(n_correct=5, n_total=20)
        report = aggregate_human_cells(obs)
        assert report.n_observations == 20


# ── compute_human_bsi_from_survey ─────────────────────────────────────────────


def _make_human_cell(
    scenario_id: str = "p2-01-anchor-high-BASELINE",
    variant: str = "BASELINE",
    pair_id: str = "p2-01-anchoring",
    choice_rate_optimal: float = 0.8,
    n_subjects: int = 50,
) -> HumanCellAggregate:
    mean_bsi = 1.0 - choice_rate_optimal
    n_correct = round(choice_rate_optimal * n_subjects)
    ci_lo, ci_hi = _wilson_score_ci_95(n_correct, n_subjects)
    return HumanCellAggregate(
        cell_id=f"{pair_id}__{variant}",
        scenario_id=scenario_id,
        variant_pair_id=pair_id,
        variant=variant,
        bias_category="anchoring",
        n_subjects=n_subjects,
        n_valid_subjects=n_subjects,
        choice_rate_optimal=choice_rate_optimal,
        choice_rate_distribution={"SupplierB": n_correct, "SupplierA": n_subjects - n_correct},
        mean_bsi=mean_bsi,
        ci_lower_95=1.0 - ci_hi,
        ci_upper_95=1.0 - ci_lo,
    )


class TestComputeHumanBsiFromSurvey:
    def test_bsi_zero_when_no_choice_change(self):
        baseline = _make_human_cell(variant="BASELINE", choice_rate_optimal=0.8)
        variant = _make_human_cell(
            scenario_id="p2-01-anchor-high-ANCHOR_HIGH",
            variant="ANCHOR_HIGH",
            choice_rate_optimal=0.8,
        )
        result = compute_human_bsi_from_survey(baseline, variant)
        assert result["bias_susceptibility_index"] == pytest.approx(0.0, abs=1e-6)

    def test_bsi_positive_when_variant_reduces_optimal(self):
        baseline = _make_human_cell(variant="BASELINE", choice_rate_optimal=0.9)
        variant = _make_human_cell(
            scenario_id="p2-01-anchor-high-ANCHOR_HIGH",
            variant="ANCHOR_HIGH",
            choice_rate_optimal=0.5,
        )
        result = compute_human_bsi_from_survey(baseline, variant)
        assert result["bias_susceptibility_index"] == pytest.approx(0.4, abs=1e-5)
        assert result["bsi_signed"] == pytest.approx(0.4, abs=1e-5)

    def test_bsi_is_absolute_value(self):
        baseline = _make_human_cell(variant="BASELINE", choice_rate_optimal=0.4)
        variant = _make_human_cell(
            scenario_id="p2-01-anchor-high-ANCHOR_HIGH",
            variant="ANCHOR_HIGH",
            choice_rate_optimal=0.7,
        )
        result = compute_human_bsi_from_survey(baseline, variant)
        assert result["bias_susceptibility_index"] == pytest.approx(0.3, abs=1e-5)
        assert result["bsi_signed"] == pytest.approx(-0.3, abs=1e-5)  # counter-bias

    def test_result_contains_required_keys(self):
        baseline = _make_human_cell(variant="BASELINE")
        variant = _make_human_cell(variant="ANCHOR_HIGH")
        result = compute_human_bsi_from_survey(baseline, variant)
        required = {
            "baseline_scenario_id", "variant_scenario_id",
            "choice_rate_optimal_baseline", "choice_rate_optimal_variant",
            "bsi_signed", "bias_susceptibility_index", "variant_type", "pair_id",
        }
        assert required.issubset(result.keys())

    def test_pair_id_propagated(self):
        baseline = _make_human_cell(variant="BASELINE", pair_id="p2-03-decoy")
        variant = _make_human_cell(variant="DECOY", pair_id="p2-03-decoy")
        result = compute_human_bsi_from_survey(baseline, variant)
        assert result["pair_id"] == "p2-03-decoy"


# ── compare_human_llm_bsi ─────────────────────────────────────────────────────


class TestCompareHumanLlmBsi:
    def test_returns_comparison_result(self):
        human_cell = _make_human_cell(variant="ANCHOR_HIGH", choice_rate_optimal=0.5)
        llm_cell = _make_llm_cell(mean_bsi=0.3)
        result = compare_human_llm_bsi(human_cell, llm_cell)
        assert isinstance(result, HumanComparisonResult)

    def test_bsi_difference_correct(self):
        human_cell = _make_human_cell(variant="ANCHOR_HIGH", choice_rate_optimal=0.5)
        # human BSI = 0.5; llm BSI = 0.3 → diff = 0.2
        llm_cell = _make_llm_cell(mean_bsi=0.3)
        result = compare_human_llm_bsi(human_cell, llm_cell)
        assert result.bsi_difference == pytest.approx(0.2, abs=1e-5)

    def test_ci_contains_difference(self):
        human_cell = _make_human_cell(variant="ANCHOR_HIGH", choice_rate_optimal=0.5)
        llm_cell = _make_llm_cell(mean_bsi=0.3)
        result = compare_human_llm_bsi(human_cell, llm_cell)
        assert result.ci_lower_95 <= result.bsi_difference <= result.ci_upper_95

    def test_cohens_d_zero_when_equal_bsi(self):
        human_cell = _make_human_cell(variant="ANCHOR_HIGH", choice_rate_optimal=0.7)
        # human BSI = 0.3; llm BSI = 0.3
        llm_cell = _make_llm_cell(mean_bsi=0.3, std_bsi=0.1)
        result = compare_human_llm_bsi(human_cell, llm_cell)
        assert result.bsi_difference == pytest.approx(0.0, abs=1e-5)

    def test_n_counts_propagated(self):
        human_cell = _make_human_cell(n_subjects=100)
        llm_cell = _make_llm_cell(n_valid_runs=50)
        result = compare_human_llm_bsi(human_cell, llm_cell)
        assert result.n_human == 100
        assert result.n_llm == 50

    def test_bias_category_propagated(self):
        human_cell = _make_human_cell(variant="ANCHOR_HIGH")
        llm_cell = _make_llm_cell()
        result = compare_human_llm_bsi(human_cell, llm_cell)
        assert result.bias_category == "anchoring"

    def test_cell_id_format(self):
        human_cell = _make_human_cell(variant="ANCHOR_HIGH", pair_id="p2-01-anchoring")
        llm_cell = _make_llm_cell()
        result = compare_human_llm_bsi(human_cell, llm_cell)
        assert "p2-01-anchoring" in result.cell_id
        assert "ANCHOR_HIGH" in result.cell_id


# ── I/O helpers ───────────────────────────────────────────────────────────────


class TestIOHelpers:
    def test_write_human_cell_report(self, tmp_path):
        obs = [_make_observation(f"S{i:03d}") for i in range(5)]
        report = aggregate_human_cells(obs)
        out = write_human_cell_report(report, tmp_path)
        assert out.exists()
        data = json.loads(out.read_text())
        assert "cells" in data
        assert "n_observations" in data

    def test_write_human_cell_report_creates_dirs(self, tmp_path):
        obs = [_make_observation()]
        report = aggregate_human_cells(obs)
        out = write_human_cell_report(report, tmp_path / "deep" / "dir")
        assert out.exists()

    def test_write_human_comparisons(self, tmp_path):
        human_cell = _make_human_cell(variant="ANCHOR_HIGH")
        llm_cell = _make_llm_cell()
        comparison = compare_human_llm_bsi(human_cell, llm_cell)
        out = write_human_comparisons([comparison], tmp_path)
        assert out.exists()
        data = json.loads(out.read_text())
        assert isinstance(data, list)
        assert len(data) == 1
        assert "bsi_difference" in data[0]

    def test_write_comparisons_empty_list(self, tmp_path):
        out = write_human_comparisons([], tmp_path)
        assert out.exists()
        data = json.loads(out.read_text())
        assert data == []
