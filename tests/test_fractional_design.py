"""Tests for UPGRADE-12: fractional factorial design orchestrator."""
from __future__ import annotations

import csv
from pathlib import Path

import pytest
from click.testing import CliRunner

from results.fractional_design import (
    BUYERBENCH_PRESET,
    CSV_FIELDNAMES,
    RunPlanRow,
    RunPlanSummary,
    _cell_id,
    _infer_bias_category,
    _treatment_label,
    generate_run_plan,
    select_treatment_combinations,
    write_run_plan_csv,
)


# ── _infer_bias_category ──────────────────────────────────────────────────────


class TestInferBiasCategory:
    def test_anchoring_baseline(self):
        # Variant suffix "BASELINE" is all-uppercase → stops at "BASELINE"
        # "anchor" is not a compound slug → returns primary "anchor"
        assert _infer_bias_category("p2-01-anchor-high-BASELINE") == "anchor"

    def test_anchoring_high_variant(self):
        assert _infer_bias_category("p2-01-anchor-high-ANCHOR_HIGH") == "anchor"

    def test_framing(self):
        # "FRAMING_LOSS" is all-uppercase → parts[3] is uppercase → returns "framing"
        assert _infer_bias_category("p2-02-framing-FRAMING_LOSS") == "framing"

    def test_framing_gain(self):
        assert _infer_bias_category("p2-02-framing-FRAMING_GAIN") == "framing"

    def test_sunk_cost_compound(self):
        # "sunk" in COMPOUND, parts[3]="cost" is lowercase → "sunk_cost"
        assert _infer_bias_category("p2-05-sunk-cost-BASELINE") == "sunk_cost"

    def test_sunk_cost_treatment(self):
        assert _infer_bias_category("p2-05-sunk-cost-SUNK_COST") == "sunk_cost"

    def test_decoy(self):
        assert _infer_bias_category("p2-03-decoy-DECOY") == "decoy"

    def test_decoy_baseline(self):
        assert _infer_bias_category("p2-03-decoy-BASELINE") == "decoy"

    def test_scarcity(self):
        assert _infer_bias_category("p2-04-scarcity-BASELINE") == "scarcity"

    def test_default_bias(self):
        assert _infer_bias_category("p2-06-default-DEFAULT") == "default"

    def test_loss_aversion_compound(self):
        # "loss" in COMPOUND, parts[3]="aversion" (lowercase) → "loss_aversion"
        assert _infer_bias_category("p2-07-loss-aversion-LOSS_AVERSION") == "loss_aversion"

    def test_loss_aversion_baseline(self):
        assert _infer_bias_category("p2-07-loss-aversion-BASELINE") == "loss_aversion"

    def test_warp_triplet_ab(self):
        assert _infer_bias_category("p2-08-warp-WARP_AB") == "warp"

    def test_warp_triplet_bc(self):
        assert _infer_bias_category("p2-08-warp-WARP_BC") == "warp"

    def test_warp_triplet_ac(self):
        assert _infer_bias_category("p2-08-warp-WARP_AC") == "warp"

    def test_non_pillar2_returns_empty(self):
        assert _infer_bias_category("p1-01-supplier-discovery") == ""

    def test_empty_string_returns_empty(self):
        assert _infer_bias_category("") == ""

    def test_short_id_returns_empty(self):
        assert _infer_bias_category("p2-01") == ""


# ── _cell_id and _treatment_label ─────────────────────────────────────────────


class TestHelpers:
    def test_cell_id_basic(self):
        cid = _cell_id("agent-a", "p2-01", "standard", 0.7)
        assert cid == "agent-a__p2-01__standard__0.7"

    def test_cell_id_none_temperature(self):
        cid = _cell_id("agent-a", "p2-01", "cot", None)
        assert cid == "agent-a__p2-01__cot__"

    def test_treatment_label_basic(self):
        assert _treatment_label("standard", 0.7) == "standard×T=0.7"

    def test_treatment_label_none(self):
        assert _treatment_label("expert_role", None) == "expert_role×default"


# ── select_treatment_combinations ────────────────────────────────────────────


class TestSelectTreatmentCombinations:
    """Tests for the core fractional factorial selection algorithm."""

    PROMPTS = ["standard", "cot", "expert_role"]
    TEMPS = [0.0, 0.3, 0.7, 1.0]

    # ── full mode ────────────────────────────────────────────────────────────

    def test_full_returns_all_combinations(self):
        combos = select_treatment_combinations(self.PROMPTS, self.TEMPS, mode="full")
        assert len(combos) == 3 * 4  # 12

    def test_full_covers_all_prompts(self):
        combos = select_treatment_combinations(self.PROMPTS, self.TEMPS, mode="full")
        seen_prompts = {p for p, _ in combos}
        assert seen_prompts == set(self.PROMPTS)

    def test_full_covers_all_temps(self):
        combos = select_treatment_combinations(self.PROMPTS, self.TEMPS, mode="full")
        seen_temps = {t for _, t in combos}
        assert seen_temps == set(self.TEMPS)

    def test_full_no_duplicates(self):
        combos = select_treatment_combinations(self.PROMPTS, self.TEMPS, mode="full")
        assert len(combos) == len(set(combos))

    # ── preset mode ──────────────────────────────────────────────────────────

    def test_preset_returns_exact_preset(self):
        combos = select_treatment_combinations(self.PROMPTS, self.TEMPS, mode="preset")
        assert combos == BUYERBENCH_PRESET

    def test_preset_has_4_combinations(self):
        combos = select_treatment_combinations(self.PROMPTS, self.TEMPS, mode="preset")
        assert len(combos) == 4

    def test_preset_wrong_prompts_raises(self):
        with pytest.raises(ValueError, match="Preset mode requires"):
            select_treatment_combinations(["standard", "cot"], self.TEMPS, mode="preset")

    def test_preset_wrong_temps_raises(self):
        with pytest.raises(ValueError, match="Preset mode requires"):
            select_treatment_combinations(self.PROMPTS, [0.0, 0.7], mode="preset")

    def test_preset_covers_all_prompts(self):
        combos = select_treatment_combinations(self.PROMPTS, self.TEMPS, mode="preset")
        seen_prompts = {p for p, _ in combos}
        assert seen_prompts == set(self.PROMPTS)

    def test_preset_covers_all_temps(self):
        combos = select_treatment_combinations(self.PROMPTS, self.TEMPS, mode="preset")
        seen_temps = {t for _, t in combos}
        assert seen_temps == set(self.TEMPS)

    # ── auto mode ────────────────────────────────────────────────────────────

    def test_auto_minimum_cells_3prompts_4temps(self):
        """auto mode: 3 prompts × 4 temps → max(3,4) = 4 combinations."""
        combos = select_treatment_combinations(self.PROMPTS, self.TEMPS, mode="auto")
        assert len(combos) == 4

    def test_auto_covers_all_prompts(self):
        combos = select_treatment_combinations(self.PROMPTS, self.TEMPS, mode="auto")
        seen_prompts = {p for p, _ in combos}
        assert seen_prompts == set(self.PROMPTS)

    def test_auto_covers_all_temps(self):
        combos = select_treatment_combinations(self.PROMPTS, self.TEMPS, mode="auto")
        seen_temps = {t for _, t in combos}
        assert seen_temps == set(self.TEMPS)

    def test_auto_no_duplicates(self):
        combos = select_treatment_combinations(self.PROMPTS, self.TEMPS, mode="auto")
        assert len(combos) == len(set(combos))

    def test_auto_single_prompt_single_temp(self):
        combos = select_treatment_combinations(["standard"], [0.7], mode="auto")
        assert combos == [("standard", 0.7)]

    def test_auto_more_prompts_than_temps(self):
        """When k > m: min covering size is max(k, m) = k."""
        prompts = ["standard", "cot", "expert_role"]
        temps = [0.7]
        combos = select_treatment_combinations(prompts, temps, mode="auto")
        # Can't cover all 3 prompts with 1 temp without repeating — round-robin gives 1 combo
        # (each temp assigned to one prompt, only 1 temp so only 1 combo)
        assert len(combos) == 1
        # Only 1 temperature, so only 1 combination is possible without repetition
        seen_temps = {t for _, t in combos}
        assert seen_temps == {0.7}

    def test_auto_equal_k_m(self):
        """k == m: exactly k combinations, all levels covered."""
        prompts = ["standard", "cot", "expert_role"]
        temps = [0.0, 0.5, 1.0]
        combos = select_treatment_combinations(prompts, temps, mode="auto")
        assert len(combos) == 3
        assert {p for p, _ in combos} == set(prompts)
        assert {t for _, t in combos} == set(temps)

    def test_auto_none_temperature_included(self):
        """None temperature (provider default) is sorted last and covered."""
        combos = select_treatment_combinations(["standard"], [None], mode="auto")
        assert combos == [("standard", None)]

    def test_auto_deterministic(self):
        """Same inputs always produce the same output."""
        combos1 = select_treatment_combinations(self.PROMPTS, self.TEMPS, mode="auto")
        combos2 = select_treatment_combinations(self.PROMPTS, self.TEMPS, mode="auto")
        assert combos1 == combos2

    # ── invalid mode ─────────────────────────────────────────────────────────

    def test_invalid_mode_raises(self):
        with pytest.raises(ValueError, match="Unknown design mode"):
            select_treatment_combinations(self.PROMPTS, self.TEMPS, mode="invalid")  # type: ignore[arg-type]

    def test_empty_prompts_raises(self):
        with pytest.raises(ValueError, match="prompt_versions must be non-empty"):
            select_treatment_combinations([], self.TEMPS)

    def test_empty_temps_raises(self):
        with pytest.raises(ValueError, match="temperatures must be non-empty"):
            select_treatment_combinations(self.PROMPTS, [])


# ── generate_run_plan ─────────────────────────────────────────────────────────


class TestGenerateRunPlan:
    AGENTS = ["openrouter-openai-gpt-4o", "openrouter-anthropic-claude-3.5-sonnet"]
    SCENARIOS = ["p2-01-anchor-high-BASELINE", "p2-01-anchor-high-ANCHOR_HIGH"]
    PROMPTS = ["standard", "cot", "expert_role"]
    TEMPS = [0.0, 0.3, 0.7, 1.0]

    def test_auto_mode_total_rows(self):
        """auto: 2 agents × 2 scenarios × 4 combos × 1 run = 16 rows."""
        rows, summary = generate_run_plan(
            agent_ids=self.AGENTS,
            scenario_ids=self.SCENARIOS,
            prompt_versions=self.PROMPTS,
            temperatures=self.TEMPS,
            n_runs=1,
            mode="auto",
        )
        assert len(rows) == 2 * 2 * 4 * 1

    def test_full_mode_total_rows(self):
        """full: 2 agents × 2 scenarios × 12 combos × 1 run = 48 rows."""
        rows, summary = generate_run_plan(
            agent_ids=self.AGENTS,
            scenario_ids=self.SCENARIOS,
            prompt_versions=self.PROMPTS,
            temperatures=self.TEMPS,
            n_runs=1,
            mode="full",
        )
        assert len(rows) == 2 * 2 * 12 * 1

    def test_n_runs_multiplies_rows(self):
        rows, _ = generate_run_plan(
            agent_ids=self.AGENTS,
            scenario_ids=self.SCENARIOS,
            prompt_versions=self.PROMPTS,
            temperatures=self.TEMPS,
            n_runs=3,
            mode="auto",
        )
        assert len(rows) == 2 * 2 * 4 * 3

    def test_run_plan_id_sequential(self):
        rows, _ = generate_run_plan(
            agent_ids=self.AGENTS,
            scenario_ids=self.SCENARIOS,
            prompt_versions=self.PROMPTS,
            temperatures=self.TEMPS,
            n_runs=1,
        )
        ids = [r.run_plan_id for r in rows]
        assert ids == list(range(1, len(rows) + 1))

    def test_run_index_sequential_within_cell(self):
        rows, _ = generate_run_plan(
            agent_ids=["agent-a"],
            scenario_ids=["p2-01-BASELINE"],
            prompt_versions=["standard"],
            temperatures=[0.7],
            n_runs=5,
        )
        assert [r.run_index for r in rows] == [1, 2, 3, 4, 5]

    def test_all_agents_covered(self):
        rows, _ = generate_run_plan(
            agent_ids=self.AGENTS,
            scenario_ids=self.SCENARIOS,
            prompt_versions=["standard"],
            temperatures=[0.7],
            n_runs=1,
        )
        seen_agents = {r.agent_id for r in rows}
        assert seen_agents == set(self.AGENTS)

    def test_all_scenarios_covered(self):
        rows, _ = generate_run_plan(
            agent_ids=["agent-a"],
            scenario_ids=self.SCENARIOS,
            prompt_versions=["standard"],
            temperatures=[0.7],
            n_runs=1,
        )
        seen = {r.scenario_id for r in rows}
        assert seen == set(self.SCENARIOS)

    def test_row_is_runplanrow(self):
        rows, _ = generate_run_plan(
            agent_ids=["agent-a"],
            scenario_ids=["p2-01-BASELINE"],
            prompt_versions=["standard"],
            temperatures=[0.7],
            n_runs=1,
        )
        assert isinstance(rows[0], RunPlanRow)

    def test_summary_is_runplansummary(self):
        _, summary = generate_run_plan(
            agent_ids=["agent-a"],
            scenario_ids=["p2-01-BASELINE"],
            prompt_versions=["standard"],
            temperatures=[0.7],
            n_runs=1,
        )
        assert isinstance(summary, RunPlanSummary)

    def test_summary_mode_stored(self):
        _, summary = generate_run_plan(
            agent_ids=["agent-a"],
            scenario_ids=["p2-01"],
            prompt_versions=["standard"],
            temperatures=[0.7],
            n_runs=1,
            mode="full",
        )
        assert summary.mode == "full"

    def test_summary_reduction_auto_less_than_full(self):
        _, summary = generate_run_plan(
            agent_ids=self.AGENTS,
            scenario_ids=self.SCENARIOS,
            prompt_versions=self.PROMPTS,
            temperatures=self.TEMPS,
            n_runs=1,
            mode="auto",
        )
        assert summary.reduction_pct > 0.0

    def test_summary_full_factorial_zero_reduction(self):
        _, summary = generate_run_plan(
            agent_ids=self.AGENTS,
            scenario_ids=self.SCENARIOS,
            prompt_versions=self.PROMPTS,
            temperatures=self.TEMPS,
            n_runs=1,
            mode="full",
        )
        assert summary.reduction_pct == 0.0

    def test_bias_category_inferred(self):
        rows, _ = generate_run_plan(
            agent_ids=["agent-a"],
            scenario_ids=["p2-05-sunk-cost-BASELINE"],
            prompt_versions=["standard"],
            temperatures=[0.7],
            n_runs=1,
        )
        assert rows[0].bias_category == "sunk_cost"

    def test_cell_id_format(self):
        rows, _ = generate_run_plan(
            agent_ids=["agent-a"],
            scenario_ids=["p2-01-BASELINE"],
            prompt_versions=["standard"],
            temperatures=[0.7],
            n_runs=1,
        )
        assert rows[0].cell_id == "agent-a__p2-01-BASELINE__standard__0.7"

    def test_treatment_combination_format(self):
        rows, _ = generate_run_plan(
            agent_ids=["agent-a"],
            scenario_ids=["p2-01-BASELINE"],
            prompt_versions=["cot"],
            temperatures=[1.0],
            n_runs=1,
        )
        assert rows[0].treatment_combination == "cot×T=1.0"

    def test_empty_agents_raises(self):
        with pytest.raises(ValueError, match="agent_ids must be non-empty"):
            generate_run_plan(
                agent_ids=[],
                scenario_ids=["p2-01"],
                prompt_versions=["standard"],
                temperatures=[0.7],
            )

    def test_empty_scenarios_raises(self):
        with pytest.raises(ValueError, match="scenario_ids must be non-empty"):
            generate_run_plan(
                agent_ids=["agent-a"],
                scenario_ids=[],
                prompt_versions=["standard"],
                temperatures=[0.7],
            )

    def test_n_runs_zero_raises(self):
        with pytest.raises((ValueError, Exception)):
            generate_run_plan(
                agent_ids=["agent-a"],
                scenario_ids=["p2-01"],
                prompt_versions=["standard"],
                temperatures=[0.7],
                n_runs=0,
            )

    def test_flagship_scale_auto(self):
        """Smoke test for flagship-scale experiment: 10 agents × 17 scenarios × 50 runs."""
        agents = [f"openrouter-model-{i}" for i in range(10)]
        scenarios = [f"p2-0{i}-bias-BASELINE" for i in range(1, 8)] + [
            f"p2-0{i}-bias-TREATMENT" for i in range(1, 8)
        ] + ["p2-08-warp-WARP_AB", "p2-08-warp-WARP_BC", "p2-08-warp-WARP_AC"]
        rows, summary = generate_run_plan(
            agent_ids=agents,
            scenario_ids=scenarios,
            prompt_versions=["standard", "cot", "expert_role"],
            temperatures=[0.0, 0.3, 0.7, 1.0],
            n_runs=50,
            mode="auto",
        )
        # auto: max(3, 4)=4 treatment combos
        # 10 agents × 17 scenarios × 4 combos × 50 runs = 34,000
        assert summary.total_planned_runs == 10 * 17 * 4 * 50
        # Full factorial would be 10 × 17 × 12 × 50 = 102,000
        assert summary.full_factorial_runs == 10 * 17 * 12 * 50
        assert summary.reduction_pct > 50.0


# ── write_run_plan_csv ────────────────────────────────────────────────────────


class TestWriteRunPlanCsv:
    def _make_rows(self, n: int = 3) -> list[RunPlanRow]:
        return [
            RunPlanRow(
                run_plan_id=i,
                agent_id=f"agent-{i}",
                scenario_id="p2-01-BASELINE",
                prompt_version="standard",
                temperature=0.7,
                run_index=1,
                cell_id=f"agent-{i}__p2-01-BASELINE__standard__0.7",
                treatment_combination="standard×T=0.7",
                bias_category="anchoring",
            )
            for i in range(1, n + 1)
        ]

    def test_file_created(self, tmp_path):
        rows = self._make_rows()
        out = write_run_plan_csv(rows, tmp_path / "plan.csv")
        assert out.exists()

    def test_header_matches_fieldnames(self, tmp_path):
        rows = self._make_rows()
        out = write_run_plan_csv(rows, tmp_path / "plan.csv")
        with out.open(newline="") as fh:
            reader = csv.DictReader(fh)
            assert tuple(reader.fieldnames or []) == CSV_FIELDNAMES

    def test_row_count(self, tmp_path):
        rows = self._make_rows(5)
        out = write_run_plan_csv(rows, tmp_path / "plan.csv")
        with out.open(newline="") as fh:
            content = list(csv.DictReader(fh))
        assert len(content) == 5

    def test_temperature_none_written_as_empty(self, tmp_path):
        rows = [
            RunPlanRow(
                run_plan_id=1,
                agent_id="agent-a",
                scenario_id="p2-01-BASELINE",
                prompt_version="standard",
                temperature=None,
                run_index=1,
                cell_id="agent-a__p2-01-BASELINE__standard__",
                treatment_combination="standard×default",
            )
        ]
        out = write_run_plan_csv(rows, tmp_path / "plan.csv")
        with out.open(newline="") as fh:
            row = next(csv.DictReader(fh))
        assert row["temperature"] == ""

    def test_temperature_value_written_correctly(self, tmp_path):
        rows = self._make_rows(1)
        out = write_run_plan_csv(rows, tmp_path / "plan.csv")
        with out.open(newline="") as fh:
            row = next(csv.DictReader(fh))
        assert row["temperature"] == "0.7"

    def test_parent_directories_created(self, tmp_path):
        deep_path = tmp_path / "nested" / "dir" / "plan.csv"
        rows = self._make_rows(1)
        out = write_run_plan_csv(rows, deep_path)
        assert out.exists()

    def test_returns_resolved_path(self, tmp_path):
        rows = self._make_rows(1)
        out = write_run_plan_csv(rows, tmp_path / "plan.csv")
        assert out.is_absolute()

    def test_empty_rows_writes_header_only(self, tmp_path):
        out = write_run_plan_csv([], tmp_path / "empty.csv")
        with out.open(newline="") as fh:
            reader = csv.DictReader(fh)
            rows = list(reader)
        assert rows == []

    def test_roundtrip_values(self, tmp_path):
        rows, _ = generate_run_plan(
            agent_ids=["agent-a"],
            scenario_ids=["p2-05-sunk-cost-BASELINE"],
            prompt_versions=["cot"],
            temperatures=[0.3],
            n_runs=2,
        )
        out = write_run_plan_csv(rows, tmp_path / "plan.csv")
        with out.open(newline="") as fh:
            csv_rows = list(csv.DictReader(fh))
        assert len(csv_rows) == 2
        assert csv_rows[0]["agent_id"] == "agent-a"
        assert csv_rows[0]["prompt_version"] == "cot"
        assert csv_rows[0]["temperature"] == "0.3"
        assert csv_rows[0]["run_index"] == "1"
        assert csv_rows[1]["run_index"] == "2"
        assert csv_rows[0]["bias_category"] == "sunk_cost"


# ── CLI integration ───────────────────────────────────────────────────────────


class TestPlanCLI:
    """Integration tests for the 'buyerbench plan' subcommand."""

    def test_plan_command_help(self):
        from buyerbench.__main__ import cli
        runner = CliRunner()
        result = runner.invoke(cli, ["plan", "--help"])
        assert result.exit_code == 0
        assert "fractional factorial" in result.output.lower()

    def test_plan_command_exits_zero(self, tmp_path):
        from buyerbench.__main__ import cli
        runner = CliRunner()
        out_csv = tmp_path / "plan.csv"
        result = runner.invoke(cli, [
            "plan",
            "--pillar", "2",
            "--agent", "openrouter-openai-gpt-4o",
            "--prompt-versions", "standard",
            "--temperatures", "0.7",
            "--n-runs", "1",
            "--mode", "full",
            "--output", str(out_csv),
        ])
        assert result.exit_code == 0, result.output

    def test_plan_creates_csv_file(self, tmp_path):
        from buyerbench.__main__ import cli
        runner = CliRunner()
        out_csv = tmp_path / "plan.csv"
        runner.invoke(cli, [
            "plan",
            "--pillar", "2",
            "--agent", "openrouter-openai-gpt-4o",
            "--prompt-versions", "standard",
            "--temperatures", "0.7",
            "--n-runs", "1",
            "--mode", "full",
            "--output", str(out_csv),
        ])
        assert out_csv.exists()

    def test_plan_output_has_correct_header(self, tmp_path):
        from buyerbench.__main__ import cli
        runner = CliRunner()
        out_csv = tmp_path / "plan.csv"
        runner.invoke(cli, [
            "plan",
            "--pillar", "2",
            "--agent", "openrouter-openai-gpt-4o",
            "--prompt-versions", "standard",
            "--temperatures", "0.7",
            "--n-runs", "1",
            "--mode", "full",
            "--output", str(out_csv),
        ])
        with out_csv.open(newline="") as fh:
            reader = csv.DictReader(fh)
            assert tuple(reader.fieldnames or []) == CSV_FIELDNAMES

    def test_plan_auto_mode_default(self, tmp_path):
        """Default mode ('auto') should produce fewer rows than full factorial."""
        from buyerbench.__main__ import cli
        runner = CliRunner()

        out_full = tmp_path / "full.csv"
        out_auto = tmp_path / "auto.csv"

        runner.invoke(cli, [
            "plan", "--pillar", "2",
            "--agent", "openrouter-openai-gpt-4o",
            "--prompt-versions", "standard",
            "--prompt-versions", "cot",
            "--prompt-versions", "expert_role",
            "--temperatures", "0.0",
            "--temperatures", "0.3",
            "--temperatures", "0.7",
            "--temperatures", "1.0",
            "--n-runs", "1", "--mode", "full",
            "--output", str(out_full),
        ])
        runner.invoke(cli, [
            "plan", "--pillar", "2",
            "--agent", "openrouter-openai-gpt-4o",
            "--prompt-versions", "standard",
            "--prompt-versions", "cot",
            "--prompt-versions", "expert_role",
            "--temperatures", "0.0",
            "--temperatures", "0.3",
            "--temperatures", "0.7",
            "--temperatures", "1.0",
            "--n-runs", "1", "--mode", "auto",
            "--output", str(out_auto),
        ])
        with out_full.open(newline="") as fh:
            full_rows = list(csv.DictReader(fh))
        with out_auto.open(newline="") as fh:
            auto_rows = list(csv.DictReader(fh))
        assert len(auto_rows) < len(full_rows)

    def test_plan_invalid_mode_error(self, tmp_path):
        from buyerbench.__main__ import cli
        runner = CliRunner()
        result = runner.invoke(cli, [
            "plan", "--mode", "bogus",
            "--output", str(tmp_path / "plan.csv"),
        ])
        assert result.exit_code != 0

    def test_plan_summary_printed(self, tmp_path):
        from buyerbench.__main__ import cli
        runner = CliRunner()
        out_csv = tmp_path / "plan.csv"
        result = runner.invoke(cli, [
            "plan",
            "--pillar", "2",
            "--agent", "openrouter-openai-gpt-4o",
            "--prompt-versions", "standard",
            "--temperatures", "0.7",
            "--n-runs", "1",
            "--mode", "full",
            "--output", str(out_csv),
        ])
        assert "Treatment Combinations" in result.output or "Total planned" in result.output.lower() or "Run Plan" in result.output
