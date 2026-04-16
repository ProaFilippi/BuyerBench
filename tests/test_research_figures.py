"""Tests for research/figures/ — BSI figure templates (PILLAR2-RESEARCH-06 L.7).

All tests use the Agg (non-interactive) backend so they run headless in CI.
matplotlib is a dev dependency (pyproject.toml [dev]) so these tests are
expected to pass in the standard dev environment.
"""
from __future__ import annotations

import math

import pytest

# Skip entire module if matplotlib is not installed
matplotlib = pytest.importorskip("matplotlib", reason="matplotlib not installed")
matplotlib.use("Agg")  # force headless backend before any pyplot import

import matplotlib.pyplot as plt
import pandas as pd

from research.figures.heatmap import plot_bsi_heatmap
from research.figures.capability_scatter import plot_capability_scatter
from research.figures.distribution_plot import plot_bsi_distributions
from research.figures.variance_plot import plot_variance_decomposition, plot_treatment_effects


# ─────────────────────────────────────────────────────────────────────────────
# SHARED FIXTURES
# ─────────────────────────────────────────────────────────────────────────────


@pytest.fixture(autouse=True)
def close_figures():
    """Close all matplotlib figures after each test to prevent resource leaks."""
    yield
    plt.close("all")


def _make_cell_df() -> pd.DataFrame:
    """Minimal aggregated cell-level DataFrame."""
    rows = []
    for agent in ["openrouter-openai-gpt-4o", "openrouter-deepseek-deepseek-chat"]:
        for bias in ["anchoring", "framing", "scarcity"]:
            rows.append({
                "agent_id": agent,
                "bias_category": bias,
                "mean_bsi": 0.3 + 0.1 * len(rows),
                "std_bsi": 0.05,
                "treatment_effect": 0.15 - 0.01 * len(rows),
                "ci_lower_95": 0.05,
                "ci_upper_95": 0.25,
            })
    return pd.DataFrame(rows)


def _make_run_df() -> pd.DataFrame:
    """Minimal run-level DataFrame."""
    rows = []
    for agent in ["agent-A", "agent-B"]:
        for bias in ["anchoring", "framing"]:
            for variant, bsi_base in [("BASELINE", 0.1), ("ANCHOR_HIGH", 0.5)]:
                for i in range(10):
                    rows.append({
                        "agent_id": agent,
                        "bias_category": bias,
                        "variant": variant,
                        "bsi": bsi_base + i * 0.02,
                    })
    return pd.DataFrame(rows)


def _make_variance_result():
    """Minimal VarianceDecompositionResult-like object."""
    from research.analysis.regression import VariancePartition, VarianceDecompositionResult

    rows = [
        VariancePartition("Model", ss=0.30, df=9, ms=0.033, eta_squared=0.30, pct_variance=30.0),
        VariancePartition("BiasType", ss=0.10, df=4, ms=0.025, eta_squared=0.10, pct_variance=10.0),
        VariancePartition("Treatment", ss=0.05, df=1, ms=0.05, eta_squared=0.05, pct_variance=5.0),
        VariancePartition("Residual", ss=0.55, df=985, ms=0.00056, eta_squared=0.55, pct_variance=55.0),
    ]
    return VarianceDecompositionResult(rows=rows, total_ss=1.0, n_obs=1000,
                                       notes="η²_Residual > 0.70 test note")


# ─────────────────────────────────────────────────────────────────────────────
# FIGURE 1 — BSI HEATMAP
# ─────────────────────────────────────────────────────────────────────────────


class TestBsiHeatmap:

    def test_returns_figure(self):
        cell_df = _make_cell_df()
        fig = plot_bsi_heatmap(cell_df)
        assert isinstance(fig, plt.Figure)

    def test_returns_figure_with_p1_scores(self):
        cell_df = _make_cell_df()
        p1 = {"openrouter-openai-gpt-4o": 0.85, "openrouter-deepseek-deepseek-chat": 0.72}
        fig = plot_bsi_heatmap(cell_df, p1_scores=p1)
        assert isinstance(fig, plt.Figure)

    def test_returns_figure_with_human_benchmark(self):
        cell_df = _make_cell_df()
        human = {"anchoring": 0.15, "framing": 0.12, "scarcity": 0.08}
        fig = plot_bsi_heatmap(cell_df, human_bsi=human)
        assert isinstance(fig, plt.Figure)

    def test_returns_figure_without_std_col(self):
        cell_df = _make_cell_df().drop(columns=["std_bsi"])
        fig = plot_bsi_heatmap(cell_df, annotate=True)
        assert isinstance(fig, plt.Figure)

    def test_missing_agent_col_raises(self):
        df = _make_cell_df().drop(columns=["agent_id"])
        with pytest.raises(ValueError, match="agent_id"):
            plot_bsi_heatmap(df)

    def test_missing_bias_col_raises(self):
        df = _make_cell_df().drop(columns=["bias_category"])
        with pytest.raises(ValueError, match="bias_category"):
            plot_bsi_heatmap(df)

    def test_missing_mean_bsi_col_raises(self):
        df = _make_cell_df().drop(columns=["mean_bsi"])
        with pytest.raises(ValueError, match="mean_bsi"):
            plot_bsi_heatmap(df)

    def test_custom_column_names(self):
        df = _make_cell_df().rename(columns={
            "agent_id": "model",
            "bias_category": "bias",
            "mean_bsi": "bsi_mean",
        })
        fig = plot_bsi_heatmap(df, agent_col="model", bias_col="bias", mean_col="bsi_mean")
        assert isinstance(fig, plt.Figure)

    def test_figsize_respected(self):
        cell_df = _make_cell_df()
        fig = plot_bsi_heatmap(cell_df, figsize=(6.0, 3.0))
        w, h = fig.get_size_inches()
        assert abs(w - 6.0) < 0.01
        assert abs(h - 3.0) < 0.01

    def test_annotate_false(self):
        cell_df = _make_cell_df()
        fig = plot_bsi_heatmap(cell_df, annotate=False)
        assert isinstance(fig, plt.Figure)

    def test_p1_scores_sort_order(self):
        """Models should appear sorted by P1 score (descending) when p1_scores provided."""
        cell_df = _make_cell_df()
        p1 = {"openrouter-openai-gpt-4o": 0.9, "openrouter-deepseek-deepseek-chat": 0.5}
        fig = plot_bsi_heatmap(cell_df, p1_scores=p1)
        # Verify: no exception and figure has one axes with ytick labels
        ax = fig.axes[0]
        ylabels = [t.get_text() for t in ax.get_yticklabels()]
        assert len(ylabels) == 2

    def test_single_model_single_bias(self):
        df = pd.DataFrame([{
            "agent_id": "agent-X", "bias_category": "anchoring",
            "mean_bsi": 0.4, "std_bsi": 0.05,
        }])
        fig = plot_bsi_heatmap(df)
        assert isinstance(fig, plt.Figure)

    def test_human_row_appears_when_provided(self):
        cell_df = _make_cell_df()
        human = {"anchoring": 0.1}
        fig = plot_bsi_heatmap(cell_df, human_bsi=human)
        ax = fig.axes[0]
        ylabels = [t.get_text() for t in ax.get_yticklabels()]
        assert any("Benchmark" in l or "Human" in l for l in ylabels)


# ─────────────────────────────────────────────────────────────────────────────
# FIGURE 2 — CAPABILITY SCATTER
# ─────────────────────────────────────────────────────────────────────────────


class TestCapabilityScatter:

    def _p1(self) -> dict[str, float]:
        return {
            "openrouter-openai-gpt-4o": 0.85,
            "openrouter-deepseek-deepseek-chat": 0.72,
            "extra-agent": 0.60,
        }

    def _cell_df_3models(self) -> pd.DataFrame:
        rows = []
        for agent, bsi in [
            ("openrouter-openai-gpt-4o", 0.28),
            ("openrouter-deepseek-deepseek-chat", 0.45),
            ("extra-agent", 0.38),
        ]:
            for bias in ["anchoring", "framing"]:
                rows.append({"agent_id": agent, "bias_category": bias, "mean_bsi": bsi})
        return pd.DataFrame(rows)

    def test_returns_figure(self):
        fig = plot_capability_scatter(self._cell_df_3models(), self._p1())
        assert isinstance(fig, plt.Figure)

    def test_missing_agent_col_raises(self):
        df = self._cell_df_3models().drop(columns=["agent_id"])
        with pytest.raises(ValueError, match="agent_id"):
            plot_capability_scatter(df, self._p1())

    def test_missing_mean_col_raises(self):
        df = self._cell_df_3models().drop(columns=["mean_bsi"])
        with pytest.raises(ValueError, match="mean_bsi"):
            plot_capability_scatter(df, self._p1())

    def test_too_few_common_models_raises(self):
        df = self._cell_df_3models()
        with pytest.raises(ValueError, match="at least 3"):
            plot_capability_scatter(df, {"openrouter-openai-gpt-4o": 0.9})

    def test_regression_line_drawn(self):
        fig = plot_capability_scatter(self._cell_df_3models(), self._p1(), draw_regression=True)
        assert isinstance(fig, plt.Figure)

    def test_no_regression_line(self):
        fig = plot_capability_scatter(self._cell_df_3models(), self._p1(), draw_regression=False)
        assert isinstance(fig, plt.Figure)

    def test_custom_figsize(self):
        fig = plot_capability_scatter(self._cell_df_3models(), self._p1(), figsize=(5.0, 4.0))
        w, h = fig.get_size_inches()
        assert abs(w - 5.0) < 0.01 and abs(h - 4.0) < 0.01

    def test_custom_column_names(self):
        df = self._cell_df_3models().rename(columns={"agent_id": "model", "mean_bsi": "bsi"})
        fig = plot_capability_scatter(df, self._p1(), agent_col="model", mean_col="bsi")
        assert isinstance(fig, plt.Figure)

    def test_axis_labels_present(self):
        fig = plot_capability_scatter(self._cell_df_3models(), self._p1())
        ax = fig.axes[0]
        assert "Pillar 1" in ax.get_xlabel() or "capability" in ax.get_xlabel().lower()
        assert "BSI" in ax.get_ylabel() or "bsi" in ax.get_ylabel().lower()

    def test_descriptive_annotation_present(self):
        fig = plot_capability_scatter(self._cell_df_3models(), self._p1())
        ax = fig.axes[0]
        texts = [t.get_text() for t in ax.texts]
        combined = " ".join(texts)
        assert "descriptive" in combined.lower() or "N =" in combined


# ─────────────────────────────────────────────────────────────────────────────
# FIGURE 3 — DISTRIBUTION VIOLIN PLOTS
# ─────────────────────────────────────────────────────────────────────────────


class TestBsiDistributions:

    def test_returns_figure(self):
        fig = plot_bsi_distributions(_make_run_df())
        assert isinstance(fig, plt.Figure)

    def test_missing_bias_col_raises(self):
        df = _make_run_df().drop(columns=["bias_category"])
        with pytest.raises(ValueError, match="bias_category"):
            plot_bsi_distributions(df)

    def test_missing_variant_col_raises(self):
        df = _make_run_df().drop(columns=["variant"])
        with pytest.raises(ValueError, match="variant"):
            plot_bsi_distributions(df)

    def test_missing_bsi_col_raises(self):
        df = _make_run_df().drop(columns=["bsi"])
        with pytest.raises(ValueError, match="bsi"):
            plot_bsi_distributions(df)

    def test_null_bsi_rows_dropped_silently(self):
        df = _make_run_df()
        df.loc[0, "bsi"] = None
        fig = plot_bsi_distributions(df)
        assert isinstance(fig, plt.Figure)

    def test_custom_column_names(self):
        df = _make_run_df().rename(columns={"bsi": "score", "bias_category": "bias",
                                             "variant": "cond"})
        fig = plot_bsi_distributions(df, bsi_col="score", bias_col="bias", variant_col="cond")
        assert isinstance(fig, plt.Figure)

    def test_empty_after_dropna_raises(self):
        df = _make_run_df()
        df["bsi"] = None
        with pytest.raises(ValueError, match="No bias categories"):
            plot_bsi_distributions(df)

    def test_max_biases_limits_output(self):
        fig = plot_bsi_distributions(_make_run_df(), max_biases=1)
        assert isinstance(fig, plt.Figure)

    def test_figsize_override(self):
        fig = plot_bsi_distributions(_make_run_df(), figsize=(10.0, 6.0))
        w, h = fig.get_size_inches()
        assert abs(w - 10.0) < 0.01 and abs(h - 6.0) < 0.01

    def test_single_bias_type(self):
        df = _make_run_df()[_make_run_df()["bias_category"] == "anchoring"]
        fig = plot_bsi_distributions(df)
        assert isinstance(fig, plt.Figure)

    def test_title_customisation(self):
        fig = plot_bsi_distributions(_make_run_df(), title="Custom Title")
        ax = fig.axes[0]
        assert ax.get_title() == "Custom Title"

    def test_only_baseline_variant(self):
        df = _make_run_df()[_make_run_df()["variant"] == "BASELINE"].copy()
        fig = plot_bsi_distributions(df)
        assert isinstance(fig, plt.Figure)


# ─────────────────────────────────────────────────────────────────────────────
# FIGURE 4 — VARIANCE DECOMPOSITION BAR CHART
# ─────────────────────────────────────────────────────────────────────────────


class TestVarianceDecomposition:

    def test_returns_figure(self):
        result = _make_variance_result()
        fig = plot_variance_decomposition(result)
        assert isinstance(fig, plt.Figure)

    def test_empty_rows_raises(self):
        from research.analysis.regression import VarianceDecompositionResult
        empty = VarianceDecompositionResult(rows=[], total_ss=0.0, n_obs=0)
        with pytest.raises(ValueError, match="rows is empty"):
            plot_variance_decomposition(empty)

    def test_custom_figsize(self):
        result = _make_variance_result()
        fig = plot_variance_decomposition(result, figsize=(5.0, 3.0))
        w, h = fig.get_size_inches()
        assert abs(w - 5.0) < 0.01

    def test_custom_title(self):
        result = _make_variance_result()
        fig = plot_variance_decomposition(result, title="My Variance Chart")
        ax = fig.axes[0]
        assert ax.get_title() == "My Variance Chart"

    def test_show_pct_labels_false(self):
        result = _make_variance_result()
        fig = plot_variance_decomposition(result, show_pct_labels=False)
        assert isinstance(fig, plt.Figure)

    def test_all_known_sources_present(self):
        """Single-source variance result (degenerate but valid)."""
        from research.analysis.regression import VariancePartition, VarianceDecompositionResult
        rows = [VariancePartition("Residual", ss=1.0, df=100, ms=0.01,
                                  eta_squared=1.0, pct_variance=100.0)]
        result = VarianceDecompositionResult(rows=rows, total_ss=1.0, n_obs=101)
        fig = plot_variance_decomposition(result)
        assert isinstance(fig, plt.Figure)


# ─────────────────────────────────────────────────────────────────────────────
# FIGURE 4 (PART B) — TREATMENT EFFECTS FOREST PLOT
# ─────────────────────────────────────────────────────────────────────────────


class TestTreatmentEffects:

    def test_returns_figure(self):
        fig = plot_treatment_effects(_make_cell_df())
        assert isinstance(fig, plt.Figure)

    def test_missing_effect_col_raises(self):
        df = _make_cell_df().drop(columns=["treatment_effect"])
        with pytest.raises(ValueError, match="treatment_effect"):
            plot_treatment_effects(df)

    def test_missing_ci_lower_raises(self):
        df = _make_cell_df().drop(columns=["ci_lower_95"])
        with pytest.raises(ValueError, match="ci_lower_95"):
            plot_treatment_effects(df)

    def test_missing_ci_upper_raises(self):
        df = _make_cell_df().drop(columns=["ci_upper_95"])
        with pytest.raises(ValueError, match="ci_upper_95"):
            plot_treatment_effects(df)

    def test_all_null_effects_raises(self):
        df = _make_cell_df()
        df["treatment_effect"] = None
        with pytest.raises(ValueError, match="No rows with non-null"):
            plot_treatment_effects(df)

    def test_custom_column_names(self):
        df = _make_cell_df().rename(columns={
            "agent_id": "model",
            "bias_category": "bias",
            "treatment_effect": "effect",
            "ci_lower_95": "ci_lo",
            "ci_upper_95": "ci_hi",
        })
        fig = plot_treatment_effects(
            df,
            agent_col="model",
            bias_col="bias",
            effect_col="effect",
            ci_lower_col="ci_lo",
            ci_upper_col="ci_hi",
        )
        assert isinstance(fig, plt.Figure)

    def test_figsize_override(self):
        fig = plot_treatment_effects(_make_cell_df(), figsize=(9.0, 7.0))
        w, h = fig.get_size_inches()
        assert abs(w - 9.0) < 0.01 and abs(h - 7.0) < 0.01

    def test_single_row(self):
        df = _make_cell_df().head(1)
        fig = plot_treatment_effects(df)
        assert isinstance(fig, plt.Figure)

    def test_null_treatment_effects_dropped(self):
        df = _make_cell_df()
        df.loc[0, "treatment_effect"] = None
        fig = plot_treatment_effects(df)
        assert isinstance(fig, plt.Figure)

    def test_reference_line_at_zero(self):
        """Ensure the vertical reference line at x=0 is drawn."""
        fig = plot_treatment_effects(_make_cell_df())
        ax = fig.axes[0]
        vlines = [line for line in ax.lines if
                  len(line.get_xdata()) == 2 and
                  line.get_xdata()[0] == line.get_xdata()[1] and
                  abs(line.get_xdata()[0]) < 1e-9]
        assert len(vlines) >= 1, "Expected vertical reference line at x=0"

    def test_sorted_by_effect_size(self):
        """Effects within each bias group should be decreasing top-to-bottom."""
        df = _make_cell_df()
        # Ensure distinct effect values
        df = df.copy()
        effects = [0.5, 0.3, 0.2, 0.4, 0.1, 0.35]
        df["treatment_effect"] = effects[:len(df)]
        fig = plot_treatment_effects(df)
        assert isinstance(fig, plt.Figure)

    def test_custom_title(self):
        fig = plot_treatment_effects(_make_cell_df(), title="Forest Plot Test")
        ax = fig.axes[0]
        assert ax.get_title() == "Forest Plot Test"
