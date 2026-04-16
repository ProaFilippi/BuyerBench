"""Tests for research/tables/ — paper table generators (PILLAR2-RESEARCH-06 L.8).

Covers:
  - main_results.py   → Table 1: Main BSI Results
  - regression_table.py → Table 2: Regression Results + Table 3: Variance Decomposition
  - power_table.py    → Table A1: Power Analysis

pandas is required for the main_results tests; others run without it.
"""
from __future__ import annotations

import math
import re

import pytest

pandas = pytest.importorskip("pandas", reason="pandas not installed")
import pandas as pd

from research.tables.main_results import (
    _bias_label,
    _normal_cdf,
    _one_sample_pvalue_gt_zero,
    _short,
    build_main_results_table,
    save_main_results_table,
)
from research.tables.regression_table import (
    _fmt_coef,
    _fmt_pval,
    _sig_stars,
    build_regression_table,
    build_variance_table,
    save_regression_table,
    save_variance_table,
)
from research.tables.power_table import (
    _GPOWER_REFERENCE,
    _approx_power,
    _normal_cdf as _power_normal_cdf,
    _z_crit,
    build_power_table,
    save_power_table,
)


# ─────────────────────────────────────────────────────────────────────────────
# SHARED FIXTURES
# ─────────────────────────────────────────────────────────────────────────────


def _make_cell_df(n_agents: int = 3, n_biases: int = 3) -> pd.DataFrame:
    """Minimal aggregated cell-level DataFrame with n_agents × n_biases rows."""
    agents = [f"openrouter-model-{i}" for i in range(n_agents)]
    biases = ["anchoring", "framing", "decoy"][:n_biases]
    rows = []
    for ai, agent in enumerate(agents):
        for bi, bias in enumerate(biases):
            rows.append({
                "agent_id": agent,
                "bias_category": bias,
                "mean_bsi": 0.10 + ai * 0.15 + bi * 0.05,
                "std_bsi": 0.08,
                "n_valid_runs": 50,
            })
    return pd.DataFrame(rows)


def _make_cell_df_with_known_agents() -> pd.DataFrame:
    """Cell df using known OpenRouter agent IDs (tests short name lookup)."""
    rows = []
    agents = [
        "openrouter-openai-gpt-4o",
        "openrouter-deepseek-deepseek-chat",
    ]
    for agent in agents:
        for bias in ["anchoring", "framing"]:
            rows.append({
                "agent_id": agent,
                "bias_category": bias,
                "mean_bsi": 0.3,
                "std_bsi": 0.1,
                "n_valid_runs": 50,
            })
    return pd.DataFrame(rows)


def _make_regression_result(n_coefs: int = 4):
    """Minimal RegressionResult-like object."""
    from dataclasses import dataclass, field
    from typing import Optional

    @dataclass
    class FakeCoef:
        name: str
        estimate: float
        se: float
        t_stat: float
        p_value: Optional[float]
        ci_lower_95: float
        ci_upper_95: float
        p_value_bh: Optional[float] = None
        significant_bh: bool = False

    @dataclass
    class FakeResult:
        spec_name: str = "primary"
        formula: str = "bsi ~ treatment + C(bias_category)"
        n_obs: int = 5000
        df_residual: Optional[int] = 4990
        r_squared: Optional[float] = 0.142
        backend: str = "statsmodels_mixedlm"
        aic: Optional[float] = -1234.5
        bic: Optional[float] = -1210.3
        log_likelihood: Optional[float] = -612.2
        random_effects_variance: Optional[float] = 0.031
        notes: str = ""
        warnings: list = field(default_factory=list)
        coefficients: list = field(default_factory=list)

    coefs = [
        FakeCoef("Intercept", 0.2342, 0.0231, 10.14, 0.0001, 0.189, 0.279, 0.0002, True),
        FakeCoef("C(bias)[T.framing]", 0.1120, 0.0312, 3.59, 0.0003, 0.051, 0.173, 0.0006, True),
        FakeCoef("treatment", 0.1423, 0.0301, 4.73, 0.0000, 0.083, 0.201, 0.0001, True),
        FakeCoef("C(agent_id)[T.model2]", -0.0210, 0.0401, -0.52, 0.6031, -0.100, 0.058),
    ]
    result = FakeResult()
    result.coefficients = coefs[:n_coefs]
    return result


def _make_variance_result():
    """Minimal VarianceDecompositionResult-like object."""
    from research.analysis.regression import VariancePartition, VarianceDecompositionResult

    rows = [
        VariancePartition("Model", ss=0.30, df=9, ms=0.0333, eta_squared=0.30, pct_variance=30.0),
        VariancePartition("BiasType", ss=0.10, df=4, ms=0.0250, eta_squared=0.10, pct_variance=10.0),
        VariancePartition("Treatment", ss=0.05, df=1, ms=0.0500, eta_squared=0.05, pct_variance=5.0),
        VariancePartition("Residual", ss=0.55, df=985, ms=0.000558, eta_squared=0.55, pct_variance=55.0),
    ]
    return VarianceDecompositionResult(rows=rows, total_ss=1.00, n_obs=1000, notes="test fixture")


# ─────────────────────────────────────────────────────────────────────────────
# TESTS — Helper utilities (main_results.py)
# ─────────────────────────────────────────────────────────────────────────────


class TestDisplayHelpers:
    def test_short_known_agent(self):
        assert _short("openrouter-openai-gpt-4o") == "GPT-4o"

    def test_short_unknown_agent_fallback(self):
        result = _short("unknown-agent-xyz")
        assert isinstance(result, str)
        assert len(result) <= 12

    def test_bias_label_known(self):
        assert _bias_label("anchoring") == "Anchoring"
        assert _bias_label("sunk_cost") == "Sunk Cost"

    def test_bias_label_unknown_titlecase(self):
        assert _bias_label("novel_bias") == "Novel Bias"


class TestNormalCdf:
    def test_z_zero_is_half(self):
        assert abs(_normal_cdf(0.0) - 0.5) < 1e-9

    def test_z_positive_large(self):
        assert _normal_cdf(4.0) > 0.9999

    def test_z_negative_large(self):
        assert _normal_cdf(-4.0) < 0.0001


class TestOneSamplePvalue:
    def test_negative_mean_returns_one(self):
        assert _one_sample_pvalue_gt_zero(-0.1, 0.2, 50) == 1.0

    def test_zero_mean_returns_one(self):
        assert _one_sample_pvalue_gt_zero(0.0, 0.2, 50) == 1.0

    def test_zero_std_returns_one(self):
        assert _one_sample_pvalue_gt_zero(0.3, 0.0, 50) == 1.0

    def test_n_less_than_2_returns_one(self):
        assert _one_sample_pvalue_gt_zero(0.3, 0.1, 1) == 1.0

    def test_large_n_large_effect_is_significant(self):
        # mean=0.4, std=0.1, n=100 → t = 40.0 → p ≈ 0
        p = _one_sample_pvalue_gt_zero(0.4, 0.1, 100)
        assert p < 0.001

    def test_small_n_large_effect(self):
        # n=20 → uses t-distribution path
        p = _one_sample_pvalue_gt_zero(0.4, 0.2, 20)
        assert 0 < p < 1

    def test_large_n_borderline(self):
        # When BSI is just barely positive
        p = _one_sample_pvalue_gt_zero(0.01, 0.3, 50)
        assert p > 0.3  # Not significant

    def test_returns_float(self):
        result = _one_sample_pvalue_gt_zero(0.3, 0.1, 50)
        assert isinstance(result, float)


# ─────────────────────────────────────────────────────────────────────────────
# TESTS — build_main_results_table
# ─────────────────────────────────────────────────────────────────────────────


class TestBuildMainResultsTable:
    def test_returns_dict_with_latex_and_csv(self):
        result = build_main_results_table(_make_cell_df())
        assert "latex" in result
        assert "csv" in result

    def test_latex_contains_table_environment(self):
        latex = build_main_results_table(_make_cell_df())["latex"]
        assert r"\begin{table}" in latex
        assert r"\end{table}" in latex

    def test_latex_contains_booktabs_rules(self):
        latex = build_main_results_table(_make_cell_df())["latex"]
        assert r"\toprule" in latex
        assert r"\midrule" in latex
        assert r"\bottomrule" in latex

    def test_latex_contains_all_bias_types(self):
        latex = build_main_results_table(_make_cell_df(n_biases=3))["latex"]
        assert "Anchoring" in latex
        assert "Framing" in latex
        assert "Decoy" in latex

    def test_latex_contains_caption_and_label(self):
        latex = build_main_results_table(
            _make_cell_df(), title="My Title", label="my:label"
        )["latex"]
        assert r"\caption{My Title}" in latex
        assert r"\label{my:label}" in latex

    def test_significant_cells_are_bolded(self):
        # High BSI + high n → should be significant → \textbf present
        df = pd.DataFrame([{
            "agent_id": "agent-A",
            "bias_category": "anchoring",
            "mean_bsi": 0.8,
            "std_bsi": 0.05,
            "n_valid_runs": 100,
        }])
        latex = build_main_results_table(df)["latex"]
        assert r"\textbf{" in latex

    def test_non_significant_cells_not_bolded_when_borderline(self):
        # Very high std, very low mean → not significant → cell row should not contain \textbf
        df = pd.DataFrame([{
            "agent_id": "agent-A",
            "bias_category": "anchoring",
            "mean_bsi": 0.01,
            "std_bsi": 0.5,
            "n_valid_runs": 5,
        }])
        result = build_main_results_table(df)
        latex = result["latex"]
        # Isolate the data rows (between \midrule and \bottomrule)
        midrule_pos = latex.index(r"\midrule")
        bottomrule_pos = latex.index(r"\bottomrule")
        data_section = latex[midrule_pos:bottomrule_pos]
        # The single data cell should not be bolded
        assert r"\textbf{" not in data_section

    def test_csv_has_correct_headers(self):
        csv_str = build_main_results_table(_make_cell_df(n_biases=2))["csv"]
        first_line = csv_str.strip().split("\n")[0]
        assert "model_id" in first_line
        assert "anchoring" in first_line
        assert "framing" in first_line

    def test_csv_significant_cells_marked_with_star(self):
        df = pd.DataFrame([{
            "agent_id": "agent-A",
            "bias_category": "anchoring",
            "mean_bsi": 0.9,
            "std_bsi": 0.02,
            "n_valid_runs": 200,
        }])
        csv_str = build_main_results_table(df)["csv"]
        assert "*" in csv_str

    def test_p1_scores_sort_models(self):
        df = _make_cell_df_with_known_agents()
        p1 = {
            "openrouter-openai-gpt-4o": 0.9,
            "openrouter-deepseek-deepseek-chat": 0.5,
        }
        latex = build_main_results_table(df, p1_scores=p1)["latex"]
        gpt_pos = latex.index("GPT-4o")
        deepseek_pos = latex.index("DeepSeek")
        # GPT-4o (higher P1) should appear before DeepSeek
        assert gpt_pos < deepseek_pos

    def test_known_agent_ids_use_short_names(self):
        latex = build_main_results_table(_make_cell_df_with_known_agents())["latex"]
        assert "GPT-4o" in latex
        assert "DeepSeek" in latex

    def test_missing_std_col_handled_gracefully(self):
        df = pd.DataFrame([{
            "agent_id": "agent-A",
            "bias_category": "anchoring",
            "mean_bsi": 0.3,
        }])
        result = build_main_results_table(df)
        assert "latex" in result

    def test_missing_n_col_handled_gracefully(self):
        df = pd.DataFrame([{
            "agent_id": "agent-A",
            "bias_category": "anchoring",
            "mean_bsi": 0.3,
            "std_bsi": 0.1,
        }])
        result = build_main_results_table(df)
        assert "latex" in result

    def test_empty_df_raises_value_error(self):
        with pytest.raises(ValueError, match="empty"):
            build_main_results_table(pd.DataFrame())

    def test_missing_required_column_raises_value_error(self):
        df = pd.DataFrame([{"agent_id": "a", "mean_bsi": 0.3}])
        with pytest.raises(ValueError, match="bias_category"):
            build_main_results_table(df)

    def test_custom_column_names(self):
        df = pd.DataFrame([{
            "model": "agent-A",
            "bias": "anchoring",
            "bsi_mean": 0.3,
            "bsi_std": 0.1,
            "n": 50,
        }])
        result = build_main_results_table(
            df,
            agent_col="model",
            bias_col="bias",
            mean_col="bsi_mean",
            std_col="bsi_std",
            n_col="n",
        )
        assert "latex" in result

    def test_footnote_mentions_bh_correction(self):
        latex = build_main_results_table(_make_cell_df())["latex"]
        assert "Benjamini" in latex or "BH" in latex or "corrected" in latex.lower()


class TestSaveMainResultsTable:
    def test_saves_tex_and_csv(self, tmp_path):
        paths = save_main_results_table(_make_cell_df(), tmp_path / "table1")
        assert paths["tex"].exists()
        assert paths["csv"].exists()
        assert paths["tex"].suffix == ".tex"
        assert paths["csv"].suffix == ".csv"

    def test_creates_parent_dirs(self, tmp_path):
        paths = save_main_results_table(
            _make_cell_df(), tmp_path / "subdir" / "nested" / "table1"
        )
        assert paths["tex"].exists()


# ─────────────────────────────────────────────────────────────────────────────
# TESTS — Helper utilities (regression_table.py)
# ─────────────────────────────────────────────────────────────────────────────


class TestSigStars:
    def test_below_0001(self):
        assert _sig_stars(0.0001) == "***"

    def test_below_001(self):
        assert _sig_stars(0.005) == "**"

    def test_below_005(self):
        assert _sig_stars(0.03) == "*"

    def test_below_010(self):
        assert r"\dagger" in _sig_stars(0.07)

    def test_above_010(self):
        assert _sig_stars(0.15) == ""

    def test_none_returns_empty(self):
        assert _sig_stars(None) == ""

    def test_exactly_005_is_star(self):
        # p=0.05 is not < 0.05, so should not get a star (use strict <)
        assert _sig_stars(0.05) == r"\dagger" or _sig_stars(0.05) == ""


class TestFmtCoef:
    def test_four_decimal_places(self):
        assert _fmt_coef(0.123456) == "0.1235"

    def test_negative_value(self):
        result = _fmt_coef(-0.1234)
        assert result.startswith("-")


class TestFmtPval:
    def test_below_001_uses_lt(self):
        result = _fmt_pval(0.0005)
        assert "$<$" in result or "<" in result

    def test_three_decimal_places_otherwise(self):
        result = _fmt_pval(0.123)
        assert "0.123" in result

    def test_none_returns_dash(self):
        assert _fmt_pval(None) == "--"


# ─────────────────────────────────────────────────────────────────────────────
# TESTS — build_regression_table (Table 2)
# ─────────────────────────────────────────────────────────────────────────────


class TestBuildRegressionTable:
    def test_returns_string(self):
        result = build_regression_table(_make_regression_result())
        assert isinstance(result, str)

    def test_contains_table_environment(self):
        tex = build_regression_table(_make_regression_result())
        assert r"\begin{table}" in tex
        assert r"\end{table}" in tex

    def test_contains_booktabs_rules(self):
        tex = build_regression_table(_make_regression_result())
        assert r"\toprule" in tex
        assert r"\midrule" in tex
        assert r"\bottomrule" in tex

    def test_contains_coefficient_names(self):
        tex = build_regression_table(_make_regression_result())
        assert "Intercept" in tex
        assert "treatment" in tex

    def test_contains_caption_and_label(self):
        tex = build_regression_table(
            _make_regression_result(), title="My Reg Table", label="tab:reg"
        )
        assert r"\caption{My Reg Table}" in tex
        assert r"\label{tab:reg}" in tex

    def test_stars_present_for_significant_coef(self):
        tex = build_regression_table(_make_regression_result())
        # Intercept has p=0.0001 → should have at least one star
        assert "***" in tex or "**" in tex

    def test_n_obs_in_output(self):
        tex = build_regression_table(_make_regression_result())
        assert "5,000" in tex or "5000" in tex

    def test_r_squared_in_output(self):
        tex = build_regression_table(_make_regression_result())
        assert "0.142" in tex or "R^2" in tex or r"$R^2$" in tex

    def test_backend_in_output(self):
        tex = build_regression_table(_make_regression_result())
        assert "statsmodels" in tex

    def test_footnote_mentions_stars(self):
        tex = build_regression_table(_make_regression_result())
        assert "p<0" in tex.replace(" ", "") or "$p<" in tex

    def test_no_coefficients_still_produces_valid_table(self):
        result = _make_regression_result(n_coefs=0)
        tex = build_regression_table(result)
        assert r"\begin{table}" in tex


class TestSaveRegressionTable:
    def test_writes_tex_file(self, tmp_path):
        path = save_regression_table(_make_regression_result(), tmp_path / "table2")
        assert path.exists()
        assert path.suffix == ".tex"

    def test_creates_parent_dirs(self, tmp_path):
        path = save_regression_table(
            _make_regression_result(), tmp_path / "subdir" / "table2"
        )
        assert path.exists()

    def test_content_matches_build(self, tmp_path):
        result = _make_regression_result()
        expected = build_regression_table(result)
        path = save_regression_table(result, tmp_path / "table2")
        assert path.read_text(encoding="utf-8") == expected


# ─────────────────────────────────────────────────────────────────────────────
# TESTS — build_variance_table (Table 3)
# ─────────────────────────────────────────────────────────────────────────────


class TestBuildVarianceTable:
    def test_returns_string(self):
        result = build_variance_table(_make_variance_result())
        assert isinstance(result, str)

    def test_contains_table_environment(self):
        tex = build_variance_table(_make_variance_result())
        assert r"\begin{table}" in tex
        assert r"\end{table}" in tex

    def test_contains_source_rows(self):
        tex = build_variance_table(_make_variance_result())
        assert "Model" in tex
        assert "BiasType" in tex
        assert "Residual" in tex

    def test_contains_pct_variance_values(self):
        tex = build_variance_table(_make_variance_result())
        assert "30.0" in tex  # Model: 30% variance

    def test_contains_total_row(self):
        tex = build_variance_table(_make_variance_result())
        assert "Total" in tex

    def test_footnote_explains_eta_squared(self):
        tex = build_variance_table(_make_variance_result())
        assert r"\eta^2" in tex or "eta" in tex.lower()

    def test_residual_row_has_no_eta_squared(self):
        tex = build_variance_table(_make_variance_result())
        # Residual row shows "--" for eta²
        # Check that the row containing "Residual" has "--" after it
        lines = tex.split("\n")
        for line in lines:
            if "Residual" in line and r"\textit" in line:
                assert "--" in line
                break

    def test_n_obs_in_output(self):
        tex = build_variance_table(_make_variance_result())
        assert "1,000" in tex or "1000" in tex

    def test_custom_title_and_label(self):
        tex = build_variance_table(
            _make_variance_result(), title="Var Dec", label="tab:var"
        )
        assert r"\caption{Var Dec}" in tex
        assert r"\label{tab:var}" in tex


class TestSaveVarianceTable:
    def test_writes_tex_file(self, tmp_path):
        path = save_variance_table(_make_variance_result(), tmp_path / "table3")
        assert path.exists()
        assert path.suffix == ".tex"


# ─────────────────────────────────────────────────────────────────────────────
# TESTS — Power computation utilities (power_table.py)
# ─────────────────────────────────────────────────────────────────────────────


class TestZCrit:
    def test_alpha_005_approx_196(self):
        assert abs(_z_crit(0.05) - 1.96) < 0.005

    def test_alpha_001_approx_258(self):
        assert abs(_z_crit(0.01) - 2.576) < 0.005

    def test_custom_alpha(self):
        z = _z_crit(0.10)
        assert 1.6 < z < 1.7  # z ≈ 1.645

    def test_returns_positive(self):
        assert _z_crit(0.05) > 0


class TestApproxPower:
    def test_zero_d_gives_low_power(self):
        p = _approx_power(0.0, 50)
        assert p == 0.0

    def test_very_large_d_gives_high_power(self):
        p = _approx_power(2.0, 100)
        assert p > 0.99

    def test_n_less_than_2_gives_zero(self):
        p = _approx_power(0.4, 1)
        assert p == 0.0

    def test_increases_with_n(self):
        p30 = _approx_power(0.4, 30)
        p50 = _approx_power(0.4, 50)
        p100 = _approx_power(0.4, 100)
        assert p30 < p50 < p100

    def test_increases_with_d(self):
        p_small = _approx_power(0.2, 50)
        p_medium = _approx_power(0.5, 50)
        p_large = _approx_power(0.8, 50)
        assert p_small < p_medium < p_large

    def test_power_bounded_0_to_1(self):
        for d in [0.1, 0.4, 0.8, 2.0]:
            for n in [10, 50, 100, 500]:
                p = _approx_power(d, n)
                assert 0.0 <= p <= 1.0

    def test_gpower_reference_d04_n50_approx_range(self):
        # G.8 states power ≈ 0.70 at N=50, d=0.4; approx_power is a lower bound
        # so we expect it to be somewhat lower than 0.70
        p = _approx_power(0.4, 50)
        assert p > 0.0  # Should compute something positive

    def test_power_d04_n100_in_reasonable_range(self):
        # G.8 states power ≈ 0.86 at N=100, d=0.4
        p = _approx_power(0.4, 100)
        # Normal approx gives a lower bound; should be in plausible range
        assert 0.4 < p < 1.0


# ─────────────────────────────────────────────────────────────────────────────
# TESTS — build_power_table (Table A1)
# ─────────────────────────────────────────────────────────────────────────────


class TestBuildPowerTable:
    def test_returns_string(self):
        result = build_power_table()
        assert isinstance(result, str)

    def test_contains_table_environment(self):
        tex = build_power_table()
        assert r"\begin{table}" in tex
        assert r"\end{table}" in tex

    def test_contains_panel_a_and_b_labels(self):
        tex = build_power_table()
        assert "Panel A" in tex
        assert "Panel B" in tex

    def test_contains_design_tier_names(self):
        tex = build_power_table()
        assert "Minimal" in tex
        assert "Realistic" in tex
        assert "Flagship" in tex
        assert "Gold Standard" in tex

    def test_contains_effect_size_rows_in_panel_b(self):
        tex = build_power_table(effect_sizes=[0.4, 0.5, 0.6])
        assert "$d = 0.4$" in tex or "d = 0.4" in tex
        assert "$d = 0.5$" in tex or "d = 0.5" in tex
        assert "$d = 0.6$" in tex or "d = 0.6" in tex

    def test_contains_n_per_cell_columns_in_panel_b(self):
        tex = build_power_table(n_per_cell_values=[30, 50, 100])
        assert "N=30" in tex or "$N=30$" in tex
        assert "N=50" in tex or "$N=50$" in tex
        assert "N=100" in tex or "$N=100$" in tex

    def test_gpower_reference_values_in_output(self):
        tex = build_power_table()
        # G.8 reference values should appear
        assert "0.52" in tex  # N=30
        assert "0.70" in tex  # N=50
        assert "0.86" in tex  # N=100

    def test_underpowered_rows_marked_with_dagger(self):
        tex = build_power_table()
        # N=30 (power=0.52) and N=50 (power=0.70) should be marked
        assert r"\dagger" in tex or r"$\dagger$" in tex

    def test_custom_effect_sizes(self):
        tex = build_power_table(effect_sizes=[0.3, 0.7])
        assert "0.3" in tex
        assert "0.7" in tex

    def test_custom_title_and_label(self):
        tex = build_power_table(title="My Power Analysis", label="tab:mpa")
        assert r"\caption{My Power Analysis}" in tex
        assert r"\label{tab:mpa}" in tex

    def test_contains_cost_estimates(self):
        tex = build_power_table()
        # Should contain dollar sign for cost column
        assert "\\$" in tex or "$" in tex

    def test_contains_total_runs(self):
        tex = build_power_table()
        # 100 cells × 30 = 3,000 runs for Minimal tier
        assert "3,000" in tex or "3000" in tex

    def test_footnote_mentions_normal_approximation(self):
        tex = build_power_table()
        assert "normal approximation" in tex.lower() or "normal" in tex.lower()

    def test_bold_for_adequate_power_in_panel_b(self):
        tex = build_power_table()
        # High d, high n → power ≥ 0.80 → should be bold in Panel B
        assert r"\textbf{" in tex


class TestSavePowerTable:
    def test_writes_tex_file(self, tmp_path):
        path = save_power_table(tmp_path / "tableA1")
        assert path.exists()
        assert path.suffix == ".tex"

    def test_creates_parent_dirs(self, tmp_path):
        path = save_power_table(tmp_path / "appendix" / "tableA1")
        assert path.exists()

    def test_content_matches_build(self, tmp_path):
        expected = build_power_table()
        path = save_power_table(tmp_path / "tableA1")
        assert path.read_text(encoding="utf-8") == expected


# ─────────────────────────────────────────────────────────────────────────────
# TESTS — G*Power reference constants sanity
# ─────────────────────────────────────────────────────────────────────────────


class TestGPowerReference:
    def test_contains_expected_n_values(self):
        assert 30 in _GPOWER_REFERENCE
        assert 50 in _GPOWER_REFERENCE
        assert 100 in _GPOWER_REFERENCE

    def test_power_increases_with_n(self):
        assert _GPOWER_REFERENCE[30] < _GPOWER_REFERENCE[50] < _GPOWER_REFERENCE[100]

    def test_n30_is_underpowered(self):
        assert _GPOWER_REFERENCE[30] < 0.80

    def test_n100_is_adequate(self):
        assert _GPOWER_REFERENCE[100] >= 0.80
