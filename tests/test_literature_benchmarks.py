"""Tests for UPGRADE-16: literature benchmark calibration (results/literature_benchmarks.py)."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from results.literature_benchmarks import (
    LITERATURE_BENCHMARKS,
    BenchmarkCalibrationResult,
    BenchmarkOverlayData,
    LiteratureBenchmark,
    compute_benchmark_calibration,
    get_all_human_benchmarks,
    get_all_llm_benchmarks,
    get_benchmark_overlay_data,
    get_benchmarks_by_bias,
    get_bias_categories,
    render_benchmark_calibration_markdown,
)


# ─────────────────────────────────────────────────────────────────────────────
# §1  DATABASE INTEGRITY
# ─────────────────────────────────────────────────────────────────────────────


class TestLiteratureBenchmarkDatabase:
    """Validate the hardcoded LITERATURE_BENCHMARKS list."""

    def test_database_is_non_empty(self):
        assert len(LITERATURE_BENCHMARKS) >= 1

    def test_all_have_required_fields(self):
        for b in LITERATURE_BENCHMARKS:
            assert b.id, f"Missing id on {b}"
            assert b.bias_category, f"Missing bias_category on {b.id}"
            assert b.citation, f"Missing citation on {b.id}"
            assert b.sample_type in ("human", "llm"), (
                f"sample_type must be 'human' or 'llm', got {b.sample_type!r} on {b.id}"
            )
            assert b.effect_description, f"Missing effect_description on {b.id}"

    def test_effect_sizes_in_range(self):
        for b in LITERATURE_BENCHMARKS:
            assert 0.0 <= b.effect_size <= 1.0, (
                f"effect_size {b.effect_size} out of [0,1] on {b.id}"
            )

    def test_ci_bounds_ordered(self):
        for b in LITERATURE_BENCHMARKS:
            if b.ci_lower_95 is not None and b.ci_upper_95 is not None:
                assert b.ci_lower_95 <= b.effect_size <= b.ci_upper_95, (
                    f"CI does not bracket effect_size on {b.id}"
                )

    def test_ids_are_unique(self):
        ids = [b.id for b in LITERATURE_BENCHMARKS]
        assert len(ids) == len(set(ids)), "Duplicate IDs in LITERATURE_BENCHMARKS"

    def test_human_benchmarks_present(self):
        human = get_all_human_benchmarks()
        assert len(human) >= 1

    def test_llm_benchmarks_present(self):
        llm = get_all_llm_benchmarks()
        assert len(llm) >= 1

    def test_all_five_core_bias_types_covered_by_human_benchmarks(self):
        core_types = {"anchoring", "framing", "decoy", "scarcity", "sunk_cost"}
        human_cats = {b.bias_category for b in get_all_human_benchmarks()}
        missing = core_types - human_cats
        assert not missing, f"Human benchmarks missing for: {missing}"

    def test_framing_has_both_human_and_llm_benchmarks(self):
        human = get_benchmarks_by_bias("framing", "human")
        llm = get_benchmarks_by_bias("framing", "llm")
        assert human
        assert llm

    def test_n_subjects_positive_when_present(self):
        for b in LITERATURE_BENCHMARKS:
            if b.n_subjects is not None:
                assert b.n_subjects > 0, f"n_subjects must be positive on {b.id}"


# ─────────────────────────────────────────────────────────────────────────────
# §2  LOOKUP FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────


class TestLookupFunctions:
    def test_get_benchmarks_by_bias_returns_matching_category(self):
        bms = get_benchmarks_by_bias("anchoring")
        assert all(b.bias_category == "anchoring" for b in bms)
        assert bms  # at least one

    def test_get_benchmarks_by_bias_unknown_returns_empty(self):
        assert get_benchmarks_by_bias("unknown-bias") == []

    def test_get_benchmarks_by_bias_filters_sample_type_human(self):
        bms = get_benchmarks_by_bias("framing", "human")
        assert all(b.sample_type == "human" for b in bms)

    def test_get_benchmarks_by_bias_filters_sample_type_llm(self):
        bms = get_benchmarks_by_bias("framing", "llm")
        assert all(b.sample_type == "llm" for b in bms)

    def test_get_benchmarks_by_bias_none_returns_all_types(self):
        all_bms = get_benchmarks_by_bias("framing", None)
        human = get_benchmarks_by_bias("framing", "human")
        llm = get_benchmarks_by_bias("framing", "llm")
        assert len(all_bms) == len(human) + len(llm)

    def test_get_all_human_benchmarks_returns_only_human(self):
        bms = get_all_human_benchmarks()
        assert all(b.sample_type == "human" for b in bms)

    def test_get_all_llm_benchmarks_returns_only_llm(self):
        bms = get_all_llm_benchmarks()
        assert all(b.sample_type == "llm" for b in bms)

    def test_get_bias_categories_is_sorted(self):
        cats = get_bias_categories()
        assert cats == sorted(cats)

    def test_get_bias_categories_contains_core_types(self):
        cats = set(get_bias_categories())
        assert {"anchoring", "framing", "decoy", "scarcity", "sunk_cost"}.issubset(cats)

    def test_human_plus_llm_equals_all(self):
        all_count = len(LITERATURE_BENCHMARKS)
        human_count = len(get_all_human_benchmarks())
        llm_count = len(get_all_llm_benchmarks())
        assert human_count + llm_count == all_count


# ─────────────────────────────────────────────────────────────────────────────
# §3  COMPUTE_BENCHMARK_CALIBRATION
# ─────────────────────────────────────────────────────────────────────────────


class TestComputeBenchmarkCalibration:
    def test_returns_one_result_per_bias_category(self):
        results = compute_benchmark_calibration()
        cats = get_bias_categories()
        assert len(results) == len(cats)
        result_cats = [r.bias_category for r in results]
        assert result_cats == cats  # sorted

    def test_no_experiment_data_llm_mean_bsi_is_none(self):
        results = compute_benchmark_calibration(None)
        for r in results:
            assert r.llm_mean_bsi is None

    def test_no_experiment_data_within_human_range_is_none(self):
        results = compute_benchmark_calibration(None)
        for r in results:
            assert r.within_human_range is None

    def test_within_range_when_bsi_inside_human_bounds(self):
        # Find a bias type and use a BSI in the middle of its human range
        cats = get_bias_categories()
        bias_cat = cats[0]
        human_bms = get_benchmarks_by_bias(bias_cat, "human")
        human_effects = [b.effect_size for b in human_bms]
        mid = (min(human_effects) + max(human_effects)) / 2
        results = compute_benchmark_calibration({bias_cat: mid})
        r = next(x for x in results if x.bias_category == bias_cat)
        assert r.within_human_range is True
        assert r.llm_mean_bsi == pytest.approx(mid)

    def test_below_human_range(self):
        cats = get_bias_categories()
        bias_cat = cats[0]
        human_bms = get_benchmarks_by_bias(bias_cat, "human")
        human_min = min(b.effect_size for b in human_bms)
        results = compute_benchmark_calibration({bias_cat: max(0.0, human_min - 0.10)})
        r = next(x for x in results if x.bias_category == bias_cat)
        assert r.within_human_range is False
        assert "below" in r.calibration_note.lower() or r.within_human_range is False

    def test_above_human_range(self):
        cats = get_bias_categories()
        bias_cat = cats[0]
        human_bms = get_benchmarks_by_bias(bias_cat, "human")
        human_max = max(b.effect_size for b in human_bms)
        results = compute_benchmark_calibration({bias_cat: min(1.0, human_max + 0.10)})
        r = next(x for x in results if x.bias_category == bias_cat)
        assert r.within_human_range is False

    def test_human_range_values_correct(self):
        results = compute_benchmark_calibration()
        for r in results:
            human_bms = get_benchmarks_by_bias(r.bias_category, "human")
            effects = [b.effect_size for b in human_bms]
            if effects:
                assert r.human_benchmark_min == pytest.approx(min(effects))
                assert r.human_benchmark_max == pytest.approx(max(effects))
                assert r.human_benchmark_mean == pytest.approx(
                    sum(effects) / len(effects)
                )

    def test_llm_prior_range_values_correct(self):
        results = compute_benchmark_calibration()
        for r in results:
            llm_bms = get_benchmarks_by_bias(r.bias_category, "llm")
            effects = [b.effect_size for b in llm_bms]
            if effects:
                assert r.llm_prior_min == pytest.approx(min(effects))
                assert r.llm_prior_max == pytest.approx(max(effects))
                assert r.llm_prior_mean == pytest.approx(
                    sum(effects) / len(effects)
                )
            else:
                assert r.llm_prior_min is None
                assert r.llm_prior_max is None
                assert r.llm_prior_mean is None

    def test_human_benchmarks_list_populated(self):
        results = compute_benchmark_calibration()
        for r in results:
            expected = get_benchmarks_by_bias(r.bias_category, "human")
            assert len(r.human_benchmarks) == len(expected)

    def test_llm_prior_benchmarks_list_populated(self):
        results = compute_benchmark_calibration()
        for r in results:
            expected = get_benchmarks_by_bias(r.bias_category, "llm")
            assert len(r.llm_prior_benchmarks) == len(expected)

    def test_calibration_note_is_non_empty(self):
        results = compute_benchmark_calibration()
        for r in results:
            assert r.calibration_note

    def test_empty_experiment_dict_same_as_none(self):
        results_none = compute_benchmark_calibration(None)
        results_empty = compute_benchmark_calibration({})
        for a, b in zip(results_none, results_empty):
            assert a.llm_mean_bsi == b.llm_mean_bsi
            assert a.within_human_range == b.within_human_range

    def test_partial_experiment_data_leaves_others_as_none(self):
        cats = get_bias_categories()
        first_cat = cats[0]
        experiment_bsi = {first_cat: 0.30}
        results = compute_benchmark_calibration(experiment_bsi)
        first = next(r for r in results if r.bias_category == first_cat)
        others = [r for r in results if r.bias_category != first_cat]
        assert first.llm_mean_bsi is not None
        for r in others:
            assert r.llm_mean_bsi is None


# ─────────────────────────────────────────────────────────────────────────────
# §4  GET_BENCHMARK_OVERLAY_DATA
# ─────────────────────────────────────────────────────────────────────────────


class TestGetBenchmarkOverlayData:
    def test_returns_all_categories_when_none_specified(self):
        overlays = get_benchmark_overlay_data()
        expected_cats = get_bias_categories()
        assert len(overlays) == len(expected_cats)
        assert [o.bias_category for o in overlays] == expected_cats

    def test_returns_requested_categories_in_order(self):
        cats = ["decoy", "anchoring"]
        overlays = get_benchmark_overlay_data(cats)
        assert len(overlays) == 2
        assert overlays[0].bias_category == "decoy"
        assert overlays[1].bias_category == "anchoring"

    def test_unknown_category_returns_empty_reference_lines(self):
        overlays = get_benchmark_overlay_data(["unknown-bias"])
        assert len(overlays) == 1
        ov = overlays[0]
        assert ov.human_reference_lines == []
        assert ov.llm_reference_lines == []
        assert ov.human_range_min == 0.0
        assert ov.human_range_max == 0.0

    def test_human_reference_lines_have_required_keys(self):
        overlays = get_benchmark_overlay_data()
        for ov in overlays:
            for line in ov.human_reference_lines:
                assert "citation" in line
                assert "effect_size" in line
                assert "ci_lower_95" in line
                assert "ci_upper_95" in line
                assert "n_subjects" in line

    def test_llm_reference_lines_have_required_keys(self):
        overlays = get_benchmark_overlay_data()
        for ov in overlays:
            for line in ov.llm_reference_lines:
                assert "citation" in line
                assert "effect_size" in line

    def test_human_range_min_leq_mean_leq_max(self):
        overlays = get_benchmark_overlay_data()
        for ov in overlays:
            if ov.human_reference_lines:
                assert ov.human_range_min <= ov.human_range_mean <= ov.human_range_max

    def test_human_range_values_match_benchmarks(self):
        overlays = get_benchmark_overlay_data()
        for ov in overlays:
            human_bms = get_benchmarks_by_bias(ov.bias_category, "human")
            effects = [b.effect_size for b in human_bms]
            if effects:
                assert ov.human_range_min == pytest.approx(min(effects))
                assert ov.human_range_max == pytest.approx(max(effects))

    def test_human_line_count_matches_benchmarks(self):
        overlays = get_benchmark_overlay_data()
        for ov in overlays:
            expected = len(get_benchmarks_by_bias(ov.bias_category, "human"))
            assert len(ov.human_reference_lines) == expected

    def test_llm_line_count_matches_benchmarks(self):
        overlays = get_benchmark_overlay_data()
        for ov in overlays:
            expected = len(get_benchmarks_by_bias(ov.bias_category, "llm"))
            assert len(ov.llm_reference_lines) == expected


# ─────────────────────────────────────────────────────────────────────────────
# §5  RENDER_BENCHMARK_CALIBRATION_MARKDOWN
# ─────────────────────────────────────────────────────────────────────────────


class TestRenderBenchmarkCalibrationMarkdown:
    def _calibration_with_data(self) -> list[BenchmarkCalibrationResult]:
        cats = get_bias_categories()
        experiment_bsi = {c: 0.30 for c in cats}
        return compute_benchmark_calibration(experiment_bsi)

    def test_returns_string(self):
        md = render_benchmark_calibration_markdown(compute_benchmark_calibration())
        assert isinstance(md, str)

    def test_contains_header(self):
        md = render_benchmark_calibration_markdown(compute_benchmark_calibration())
        assert "Literature Benchmark Calibration" in md

    def test_contains_table_header_row(self):
        md = render_benchmark_calibration_markdown(compute_benchmark_calibration())
        assert "Bias Type" in md
        assert "BuyerBench BSI" in md
        assert "Human Range" in md
        assert "Human Mean" in md
        assert "Prior LLM Range" in md
        assert "Status" in md

    def test_contains_one_row_per_bias_category(self):
        cal = compute_benchmark_calibration()
        md = render_benchmark_calibration_markdown(cal)
        for r in cal:
            assert r.bias_category in md

    def test_shows_dash_when_no_experiment_data(self):
        cal = compute_benchmark_calibration(None)
        md = render_benchmark_calibration_markdown(cal)
        # All BuyerBench BSI cells should show "—" (em dash or regular dash)
        assert "—" in md

    def test_shows_bsi_value_when_data_present(self):
        cal = self._calibration_with_data()
        md = render_benchmark_calibration_markdown(cal)
        assert "0.300" in md

    def test_shows_within_range_status(self):
        cats = get_bias_categories()
        # Pick a BSI in the human range
        first_cat = cats[0]
        human_bms = get_benchmarks_by_bias(first_cat, "human")
        mid = (
            min(b.effect_size for b in human_bms) + max(b.effect_size for b in human_bms)
        ) / 2
        cal = compute_benchmark_calibration({first_cat: mid})
        md = render_benchmark_calibration_markdown(cal)
        assert "within range" in md

    def test_shows_below_human_status(self):
        cats = get_bias_categories()
        first_cat = cats[0]
        cal = compute_benchmark_calibration({first_cat: 0.001})
        md = render_benchmark_calibration_markdown(cal)
        assert "below human" in md

    def test_empty_calibration_list_returns_header_only(self):
        md = render_benchmark_calibration_markdown([])
        assert "Literature Benchmark Calibration" in md


# ─────────────────────────────────────────────────────────────────────────────
# §6  STATS_PIPELINE INTEGRATION
# ─────────────────────────────────────────────────────────────────────────────


class TestStatsPipelineIntegration:
    """Verify that run_stats_pipeline() populates literature_calibration."""

    def _make_cell(
        self,
        agent_id: str = "agent-A",
        scenario_id: str = "p2-01-anchoring-BASELINE",
        variant_pair_id: str = "p2-01-anchoring",
        variant: str = "BASELINE",
        bias_category: str = "anchoring",
        mean_bsi: float = 0.0,
        n_valid_runs: int = 10,
    ):
        from results.aggregate_cells import CellAggregate

        return CellAggregate(
            cell_id=f"{agent_id}__{variant_pair_id}__{variant}__0.7",
            agent_id=agent_id,
            scenario_id=scenario_id,
            variant_pair_id=variant_pair_id,
            variant=variant,
            bias_category=bias_category,
            temperature=0.7,
            n_runs=n_valid_runs,
            n_valid_runs=n_valid_runs,
            mean_bsi=mean_bsi,
            std_bsi=0.0,
            ci_lower_95=0.0,
            ci_upper_95=0.0,
            choice_rate_correct=1.0 - mean_bsi,
            mean_optimality_gap=mean_bsi,
        )

    def test_literature_calibration_present_in_report(self):
        from results.aggregate_cells import CellAggregateReport
        from results.stats_pipeline import run_stats_pipeline

        cells = [
            self._make_cell("A", variant="BASELINE", bias_category="anchoring"),
            self._make_cell("A", variant="ANCHOR_HIGH", bias_category="anchoring",
                            mean_bsi=0.35),
        ]
        report_data = CellAggregateReport(
            n_agents=1, n_cells=len(cells), n_total_runs=20, cells=cells
        )
        stats_report = run_stats_pipeline(report_data)
        assert stats_report.literature_calibration is not None
        assert len(stats_report.literature_calibration) > 0

    def test_literature_calibration_contains_anchoring_with_bsi(self):
        from results.aggregate_cells import CellAggregateReport
        from results.stats_pipeline import run_stats_pipeline

        cells = [
            self._make_cell("A", variant="BASELINE", bias_category="anchoring",
                            mean_bsi=0.0),
            self._make_cell("A", variant="ANCHOR_HIGH", bias_category="anchoring",
                            mean_bsi=0.40),
        ]
        report_data = CellAggregateReport(
            n_agents=1, n_cells=len(cells), n_total_runs=20, cells=cells
        )
        stats_report = run_stats_pipeline(report_data)
        cal = stats_report.literature_calibration
        anchoring_entry = next(
            (r for r in cal if r.bias_category == "anchoring"), None
        )
        assert anchoring_entry is not None
        # mean_bsi = mean(0.0, 0.40) = 0.20
        assert anchoring_entry.llm_mean_bsi == pytest.approx(0.20)

    def test_literature_calibration_all_bias_types_included(self):
        from results.aggregate_cells import CellAggregateReport
        from results.stats_pipeline import run_stats_pipeline

        report_data = CellAggregateReport(
            n_agents=0, n_cells=0, n_total_runs=0, cells=[]
        )
        stats_report = run_stats_pipeline(report_data)
        # Even with no cells, calibration is populated (just with llm_mean_bsi=None)
        assert stats_report.literature_calibration is not None
        cal_cats = {r.bias_category for r in stats_report.literature_calibration}
        expected = set(get_bias_categories())
        assert expected.issubset(cal_cats)

    def test_stats_pipeline_report_json_serialisable(self):
        from results.aggregate_cells import CellAggregateReport
        from results.stats_pipeline import run_stats_pipeline

        report_data = CellAggregateReport(
            n_agents=0, n_cells=0, n_total_runs=0, cells=[]
        )
        stats_report = run_stats_pipeline(report_data)
        serialized = stats_report.model_dump_json()
        data = json.loads(serialized)
        assert "literature_calibration" in data
        assert isinstance(data["literature_calibration"], list)
