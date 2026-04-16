"""Tests for UPGRADE-5: cell-level aggregate output (results/aggregate_cells.py)."""
from __future__ import annotations

import json
import math
from datetime import datetime, timezone
from pathlib import Path

import pytest

from buyerbench.models import EvaluationResult, Pillar, PillarScore, ScenarioVariant
from results.aggregate_cells import (
    CellAggregate,
    CellAggregateReport,
    _confidence_interval_95,
    _t_critical_95,
    aggregate_cells,
    aggregate_cells_from_dir,
    write_cell_aggregates,
)


# ── Helpers ───────────────────────────────────────────────────────────────────


def _make_result(
    agent_id: str = "agent-A",
    scenario_id: str = "p2-01-anchoring-baseline",
    variant_pair_id: str | None = "p2-01-anchoring",
    variant: str | None = "BASELINE",
    bias_category: str | None = "anchoring",
    optimal_chosen: float = 1.0,
    optimality_gap: float = 0.0,
    supplier_choice: str | None = "SupplierA",
    temperature: float | None = None,
    error_flag: bool = False,
    run_index: int = 0,
) -> EvaluationResult:
    """Build a minimal EvaluationResult for testing."""
    bsi = 0.0 if optimal_chosen == 1.0 else 1.0
    return EvaluationResult(
        scenario_id=scenario_id,
        agent_id=agent_id,
        pillar_scores=[
            PillarScore(
                pillar=Pillar.PILLAR2,
                score=optimal_chosen,
                metrics={
                    "optimal_choice_rate": optimal_chosen,
                    "optimal_chosen": optimal_chosen,
                    "optimality_gap": optimality_gap,
                    "expected_value_regret": optimality_gap,
                    "bias_susceptibility_index": bsi,
                },
            )
        ],
        overall_pass=optimal_chosen >= 0.6,
        variant_pair_id=variant_pair_id,
        variant=variant,
        bias_category=bias_category,
        temperature=temperature,
        error_flag=error_flag,
        error_message="mock error" if error_flag else None,
        run_index=run_index,
        decisions={"selected_supplier": supplier_choice} if supplier_choice else {},
    )


# ── t-distribution helpers ────────────────────────────────────────────────────


class TestTCritical95:
    def test_normal_approximation_for_large_n(self):
        assert _t_critical_95(100) == 1.960
        assert _t_critical_95(31) == 1.960

    def test_known_values_from_table(self):
        # n=3 → df=2 → t=4.303; n=7 → df=6 → t=2.447; n=30 → df=29 → t=2.045
        assert _t_critical_95(3) == pytest.approx(4.303, abs=1e-3)
        assert _t_critical_95(7) == pytest.approx(2.447, abs=1e-3)
        assert _t_critical_95(30) == pytest.approx(2.045, abs=1e-3)

    def test_n1_returns_max_table_value(self):
        # n=1 → df=0, clamped to df=1
        val = _t_critical_95(1)
        assert val == pytest.approx(12.706, abs=1e-3)


class TestConfidenceInterval95:
    def test_empty_list(self):
        assert _confidence_interval_95([]) == (0.0, 0.0)

    def test_single_value_returns_point_estimate(self):
        lo, hi = _confidence_interval_95([0.4])
        assert lo == pytest.approx(0.4)
        assert hi == pytest.approx(0.4)

    def test_two_identical_values_zero_variance(self):
        lo, hi = _confidence_interval_95([0.5, 0.5])
        assert lo == pytest.approx(0.5)
        assert hi == pytest.approx(0.5)

    def test_symmetric_around_mean(self):
        values = [0.2, 0.4, 0.6, 0.8]
        lo, hi = _confidence_interval_95(values)
        mean = 0.5
        assert lo < mean < hi
        # CI should be symmetric around the mean
        assert abs((hi - mean) - (mean - lo)) < 1e-9

    def test_bounds_clamped_to_zero_one(self):
        # High variance sample that could push bounds outside [0,1]
        lo, hi = _confidence_interval_95([0.0, 0.0, 1.0, 1.0])
        assert lo >= 0.0
        assert hi <= 1.0

    def test_wider_ci_for_smaller_n(self):
        values_small = [0.0, 1.0, 0.0, 1.0, 0.0]      # N=5
        values_large = [0.0, 1.0] * 25                 # N=50
        lo_s, hi_s = _confidence_interval_95(values_small)
        lo_l, hi_l = _confidence_interval_95(values_large)
        # Smaller sample → wider CI
        assert (hi_s - lo_s) > (hi_l - lo_l)

    def test_large_n_uses_z_1_96(self):
        # 50 identical values: std_err = 0 → CI collapses to point
        lo, hi = _confidence_interval_95([0.3] * 50)
        assert lo == pytest.approx(0.3)
        assert hi == pytest.approx(0.3)


# ── Cell grouping and aggregate computation ───────────────────────────────────


class TestAggregateCellsGrouping:
    def test_single_result_one_cell(self):
        results = [_make_result()]
        report = aggregate_cells(results)
        assert report.n_cells == 1
        assert len(report.cells) == 1

    def test_multiple_runs_same_cell(self):
        results = [
            _make_result(run_index=i, optimal_chosen=1.0 if i < 3 else 0.0)
            for i in range(5)
        ]
        report = aggregate_cells(results)
        assert report.n_cells == 1
        cell = report.cells[0]
        assert cell.n_runs == 5
        assert cell.n_valid_runs == 5

    def test_different_agents_produce_different_cells(self):
        results = [
            _make_result(agent_id="agent-A"),
            _make_result(agent_id="agent-B"),
        ]
        report = aggregate_cells(results)
        assert report.n_cells == 2
        agent_ids = {c.agent_id for c in report.cells}
        assert agent_ids == {"agent-A", "agent-B"}

    def test_different_variants_produce_different_cells(self):
        results = [
            _make_result(scenario_id="p2-01-baseline", variant="BASELINE"),
            _make_result(scenario_id="p2-01-anchor-high", variant="ANCHOR_HIGH"),
        ]
        report = aggregate_cells(results)
        assert report.n_cells == 2

    def test_different_temperatures_produce_different_cells(self):
        results = [
            _make_result(temperature=0.0),
            _make_result(temperature=0.7),
            _make_result(temperature=1.0),
        ]
        report = aggregate_cells(results)
        assert report.n_cells == 3

    def test_n_total_runs_matches_input(self):
        results = [_make_result(run_index=i) for i in range(10)]
        report = aggregate_cells(results)
        assert report.n_total_runs == 10

    def test_n_agents_counts_unique_agents(self):
        results = [
            _make_result(agent_id="agent-A"),
            _make_result(agent_id="agent-A"),
            _make_result(agent_id="agent-B"),
        ]
        report = aggregate_cells(results)
        assert report.n_agents == 2


class TestCellAggregateMetrics:
    def test_all_optimal_gives_zero_bsi(self):
        results = [_make_result(optimal_chosen=1.0) for _ in range(5)]
        report = aggregate_cells(results)
        cell = report.cells[0]
        assert cell.mean_bsi == pytest.approx(0.0)
        assert cell.std_bsi == pytest.approx(0.0)
        assert cell.choice_rate_correct == pytest.approx(1.0)
        assert cell.mean_optimality_gap == pytest.approx(0.0)

    def test_all_suboptimal_gives_unit_bsi(self):
        results = [
            _make_result(optimal_chosen=0.0, optimality_gap=0.5) for _ in range(4)
        ]
        report = aggregate_cells(results)
        cell = report.cells[0]
        assert cell.mean_bsi == pytest.approx(1.0)
        assert cell.choice_rate_correct == pytest.approx(0.0)
        assert cell.mean_optimality_gap == pytest.approx(0.5)

    def test_mixed_optimality(self):
        # 2 optimal, 3 suboptimal → mean_bsi = 3/5 = 0.6
        results = (
            [_make_result(optimal_chosen=1.0)] * 2
            + [_make_result(optimal_chosen=0.0)] * 3
        )
        report = aggregate_cells(results)
        cell = report.cells[0]
        assert cell.mean_bsi == pytest.approx(0.6)
        assert cell.choice_rate_correct == pytest.approx(0.4)
        assert cell.n_valid_runs == 5

    def test_std_bsi_correct(self):
        # Values: [0, 0, 1, 1] → mean=0.5, sample std = sqrt(sum((x-0.5)^2)/3)
        results = (
            [_make_result(optimal_chosen=1.0)] * 2
            + [_make_result(optimal_chosen=0.0)] * 2
        )
        report = aggregate_cells(results)
        cell = report.cells[0]
        expected_std = math.sqrt(sum((x - 0.5) ** 2 for x in [0, 0, 1, 1]) / 3)
        assert cell.std_bsi == pytest.approx(expected_std, abs=1e-6)

    def test_ci_contains_mean(self):
        results = [
            _make_result(optimal_chosen=1.0),
            _make_result(optimal_chosen=0.0),
            _make_result(optimal_chosen=1.0),
            _make_result(optimal_chosen=0.0),
        ]
        report = aggregate_cells(results)
        cell = report.cells[0]
        assert cell.ci_lower_95 <= cell.mean_bsi <= cell.ci_upper_95

    def test_ci_wider_with_higher_variance(self):
        results_certain = [_make_result(optimal_chosen=1.0)] * 10
        results_uncertain = (
            [_make_result(optimal_chosen=1.0)] * 5
            + [_make_result(optimal_chosen=0.0)] * 5
        )
        r_certain = aggregate_cells(results_certain)
        r_uncertain = aggregate_cells(results_uncertain)
        ci_width_certain = (
            r_certain.cells[0].ci_upper_95 - r_certain.cells[0].ci_lower_95
        )
        ci_width_uncertain = (
            r_uncertain.cells[0].ci_upper_95 - r_uncertain.cells[0].ci_lower_95
        )
        assert ci_width_uncertain > ci_width_certain

    def test_single_run_ci_equals_point_estimate(self):
        results = [_make_result(optimal_chosen=0.0)]
        report = aggregate_cells(results)
        cell = report.cells[0]
        assert cell.ci_lower_95 == pytest.approx(cell.mean_bsi)
        assert cell.ci_upper_95 == pytest.approx(cell.mean_bsi)


class TestErrorFlagExclusion:
    def test_error_runs_excluded_from_valid_count(self):
        results = [
            _make_result(error_flag=False),
            _make_result(error_flag=True),
            _make_result(error_flag=False),
        ]
        report = aggregate_cells(results)
        cell = report.cells[0]
        assert cell.n_runs == 3
        assert cell.n_valid_runs == 2

    def test_error_run_not_counted_in_bsi(self):
        # 1 optimal + 1 error (suboptimal body but error_flag=True) = only 1 valid
        results = [
            _make_result(optimal_chosen=1.0, error_flag=False),
            _make_result(optimal_chosen=0.0, error_flag=True),
        ]
        report = aggregate_cells(results)
        cell = report.cells[0]
        # Only the non-error run counts → BSI = 0.0 (optimal)
        assert cell.mean_bsi == pytest.approx(0.0)
        assert cell.n_valid_runs == 1

    def test_all_error_runs_gives_zero_metrics(self):
        results = [_make_result(error_flag=True) for _ in range(3)]
        report = aggregate_cells(results)
        cell = report.cells[0]
        assert cell.n_valid_runs == 0
        assert cell.mean_bsi == pytest.approx(0.0)
        assert cell.n_runs == 3


class TestChoiceRateDistribution:
    def test_single_supplier_all_runs(self):
        results = [_make_result(supplier_choice="SupplierA") for _ in range(5)]
        report = aggregate_cells(results)
        dist = report.cells[0].choice_rate_distribution
        assert dist == {"SupplierA": 5}

    def test_mixed_supplier_choices(self):
        results = (
            [_make_result(supplier_choice="SupplierA")] * 3
            + [_make_result(supplier_choice="SupplierB")] * 2
        )
        report = aggregate_cells(results)
        dist = report.cells[0].choice_rate_distribution
        assert dist["SupplierA"] == 3
        assert dist["SupplierB"] == 2

    def test_none_supplier_not_counted(self):
        results = [_make_result(supplier_choice=None) for _ in range(3)]
        report = aggregate_cells(results)
        assert report.cells[0].choice_rate_distribution == {}


# ── Treatment effect computation ─────────────────────────────────────────────


class TestTreatmentEffect:
    def _make_pair_results(
        self,
        baseline_optimal_rate: float = 1.0,
        treatment_optimal_rate: float = 0.6,
        n_runs: int = 5,
    ) -> list[EvaluationResult]:
        """Build N baseline + N treatment results sharing a variant_pair_id."""
        n_baseline_optimal = int(round(baseline_optimal_rate * n_runs))
        n_treatment_optimal = int(round(treatment_optimal_rate * n_runs))

        baseline = [
            _make_result(
                scenario_id="p2-01-baseline",
                variant="BASELINE",
                optimal_chosen=1.0 if i < n_baseline_optimal else 0.0,
            )
            for i in range(n_runs)
        ]
        treatment = [
            _make_result(
                scenario_id="p2-01-anchor-high",
                variant="ANCHOR_HIGH",
                optimal_chosen=1.0 if i < n_treatment_optimal else 0.0,
            )
            for i in range(n_runs)
        ]
        return baseline + treatment

    def test_treatment_effect_is_none_for_baseline_cell(self):
        results = self._make_pair_results()
        report = aggregate_cells(results)
        baseline_cell = next(c for c in report.cells if c.variant == "BASELINE")
        assert baseline_cell.treatment_effect_vs_baseline is None

    def test_treatment_effect_computed_for_treatment_cell(self):
        results = self._make_pair_results(
            baseline_optimal_rate=1.0,  # mean_bsi_baseline = 0.0
            treatment_optimal_rate=0.6,  # mean_bsi_treatment = 0.4
        )
        report = aggregate_cells(results)
        treatment_cell = next(c for c in report.cells if c.variant != "BASELINE")
        # treatment_effect = mean_bsi(treatment) - mean_bsi(baseline) = 0.4 - 0.0
        assert treatment_cell.treatment_effect_vs_baseline is not None
        assert treatment_cell.treatment_effect_vs_baseline == pytest.approx(
            treatment_cell.mean_bsi - 0.0, abs=1e-6
        )

    def test_no_treatment_effect_when_no_baseline_cell(self):
        # Treatment cell with no matching baseline in the results set
        results = [
            _make_result(scenario_id="p2-01-anchor-high", variant="ANCHOR_HIGH")
        ]
        report = aggregate_cells(results)
        assert report.cells[0].treatment_effect_vs_baseline is None

    def test_treatment_effect_positive_when_treatment_more_biased(self):
        results = self._make_pair_results(
            baseline_optimal_rate=1.0,   # mean_bsi_baseline = 0.0
            treatment_optimal_rate=0.0,  # mean_bsi_treatment = 1.0
        )
        report = aggregate_cells(results)
        treatment_cell = next(c for c in report.cells if c.variant != "BASELINE")
        assert treatment_cell.treatment_effect_vs_baseline == pytest.approx(1.0, abs=1e-6)

    def test_treatment_effect_zero_when_no_bias(self):
        results = self._make_pair_results(
            baseline_optimal_rate=1.0,
            treatment_optimal_rate=1.0,
        )
        report = aggregate_cells(results)
        treatment_cell = next(c for c in report.cells if c.variant != "BASELINE")
        assert treatment_cell.treatment_effect_vs_baseline == pytest.approx(0.0, abs=1e-6)

    def test_treatment_effect_matches_baseline_when_only_one_pair(self):
        """treatment_effect = mean_bsi(T) - mean_bsi(B) for a single pair."""
        # 5 baseline runs (all optimal) + 5 treatment runs (3 optimal, 2 not)
        n = 5
        baseline = [
            _make_result(scenario_id="p2-01-baseline", variant="BASELINE", optimal_chosen=1.0)
            for _ in range(n)
        ]
        treatment = [
            _make_result(
                scenario_id="p2-01-anchor-high",
                variant="ANCHOR_HIGH",
                optimal_chosen=1.0 if i < 3 else 0.0,
            )
            for i in range(n)
        ]
        report = aggregate_cells(baseline + treatment)
        baseline_cell = next(c for c in report.cells if c.variant == "BASELINE")
        treatment_cell = next(c for c in report.cells if c.variant != "BASELINE")
        expected_effect = treatment_cell.mean_bsi - baseline_cell.mean_bsi
        assert treatment_cell.treatment_effect_vs_baseline == pytest.approx(
            expected_effect, abs=1e-6
        )

    def test_multiple_agents_treatment_effects_independent(self):
        """Agents are not cross-paired; each agent's baseline is its own reference."""
        results_a = [
            _make_result(agent_id="agent-A", scenario_id="p2-01-baseline", variant="BASELINE"),
            _make_result(agent_id="agent-A", scenario_id="p2-01-high", variant="ANCHOR_HIGH", optimal_chosen=0.0),
        ]
        results_b = [
            _make_result(agent_id="agent-B", scenario_id="p2-01-baseline", variant="BASELINE"),
            _make_result(agent_id="agent-B", scenario_id="p2-01-high", variant="ANCHOR_HIGH", optimal_chosen=0.0),
        ]
        report = aggregate_cells(results_a + results_b)
        for cell in report.cells:
            if cell.variant == "BASELINE":
                assert cell.treatment_effect_vs_baseline is None
            else:
                assert cell.treatment_effect_vs_baseline is not None


# ── Cell ID format ────────────────────────────────────────────────────────────


class TestCellId:
    def test_cell_id_contains_all_dimensions(self):
        results = [
            _make_result(
                agent_id="agent-X",
                variant_pair_id="p2-01-anchoring",
                variant="BASELINE",
                temperature=0.7,
            )
        ]
        report = aggregate_cells(results)
        cell_id = report.cells[0].cell_id
        assert "agent-X" in cell_id
        assert "p2-01-anchoring" in cell_id
        assert "BASELINE" in cell_id
        assert "0.7" in cell_id

    def test_cell_id_unique_across_cells(self):
        results = [
            _make_result(agent_id="A", variant="BASELINE"),
            _make_result(agent_id="A", variant="ANCHOR_HIGH"),
            _make_result(agent_id="B", variant="BASELINE"),
        ]
        report = aggregate_cells(results)
        cell_ids = [c.cell_id for c in report.cells]
        assert len(cell_ids) == len(set(cell_ids)), "Cell IDs must be unique"


# ── Report metadata ───────────────────────────────────────────────────────────


class TestReportMetadata:
    def test_generated_at_is_recent(self):
        report = aggregate_cells([_make_result()])
        now = datetime.now(timezone.utc)
        delta = abs((now - report.generated_at).total_seconds())
        assert delta < 5

    def test_empty_results_produces_empty_report(self):
        report = aggregate_cells([])
        assert report.n_cells == 0
        assert report.n_total_runs == 0
        assert report.n_agents == 0
        assert report.cells == []


# ── File I/O ──────────────────────────────────────────────────────────────────


class TestWriteCellAggregates:
    def test_writes_json_file(self, tmp_path):
        results = [_make_result(run_index=i) for i in range(3)]
        report = aggregate_cells(results)
        out_path = write_cell_aggregates(report, tmp_path)
        assert out_path.exists()
        assert out_path.name == "cell_aggregates.json"

    def test_written_file_is_valid_json(self, tmp_path):
        results = [_make_result(run_index=i) for i in range(3)]
        report = aggregate_cells(results)
        out_path = write_cell_aggregates(report, tmp_path)
        data = json.loads(out_path.read_text())
        assert "cells" in data
        assert "n_cells" in data

    def test_custom_filename(self, tmp_path):
        results = [_make_result()]
        report = aggregate_cells(results)
        out_path = write_cell_aggregates(report, tmp_path, filename="my_cells.json")
        assert out_path.name == "my_cells.json"

    def test_creates_output_dir_if_missing(self, tmp_path):
        new_dir = tmp_path / "new" / "subdir"
        assert not new_dir.exists()
        results = [_make_result()]
        report = aggregate_cells(results)
        write_cell_aggregates(report, new_dir)
        assert new_dir.exists()

    def test_round_trip_serialization(self, tmp_path):
        """Values written and re-read must match."""
        results = [_make_result(optimal_chosen=1.0 if i % 2 == 0 else 0.0) for i in range(6)]
        report = aggregate_cells(results)
        out_path = write_cell_aggregates(report, tmp_path)
        loaded = json.loads(out_path.read_text())
        cell = loaded["cells"][0]
        assert cell["n_runs"] == 6
        assert cell["n_valid_runs"] == 6
        assert abs(cell["mean_bsi"] - report.cells[0].mean_bsi) < 1e-9


# ── aggregate_cells_from_dir ──────────────────────────────────────────────────


class TestAggregateCellsFromDir:
    def test_loads_results_from_json_files(self, tmp_path):
        # Write two result JSONs to agent subdirectory
        agent_dir = tmp_path / "agent-A"
        agent_dir.mkdir()
        for i in range(3):
            result = _make_result(run_index=i)
            (agent_dir / f"p2-01-anchoring-baseline-run{i:03d}.json").write_text(
                result.model_dump_json()
            )
        report = aggregate_cells_from_dir(tmp_path)
        assert report.n_total_runs == 3
        assert report.n_agents == 1

    def test_skips_sentinel_files(self, tmp_path):
        agent_dir = tmp_path / "agent-A"
        agent_dir.mkdir()
        # Write a valid result
        result = _make_result()
        (agent_dir / "p2-01.json").write_text(result.model_dump_json())
        # Write a skipped sentinel
        (agent_dir / "p2-02-skipped.json").write_text('{"status": "skipped"}')
        report = aggregate_cells_from_dir(tmp_path)
        assert report.n_total_runs == 1

    def test_skips_invalid_json(self, tmp_path):
        agent_dir = tmp_path / "agent-A"
        agent_dir.mkdir()
        (agent_dir / "bad.json").write_text("not valid json or schema")
        report = aggregate_cells_from_dir(tmp_path)
        assert report.n_total_runs == 0

    def test_empty_directory_produces_empty_report(self, tmp_path):
        report = aggregate_cells_from_dir(tmp_path)
        assert report.n_cells == 0

    def test_multiple_agents_in_subdirectories(self, tmp_path):
        for agent_id in ("agent-A", "agent-B"):
            d = tmp_path / agent_id
            d.mkdir()
            result = _make_result(agent_id=agent_id)
            (d / "p2-01.json").write_text(result.model_dump_json())
        report = aggregate_cells_from_dir(tmp_path)
        assert report.n_agents == 2
        assert report.n_cells == 2
