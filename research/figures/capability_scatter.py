"""Figure 2 — Capability vs. Bias Susceptibility Scatter.

One point per model: X = Pillar 1 capability score, Y = mean BSI across all
bias types.  Includes an OLS regression line with a 95% confidence band.
Annotated with "N=10 models; interpret as descriptive only."

Public API
----------
- ``plot_capability_scatter(cell_df, p1_scores, ...)``
  Returns a ``matplotlib.figure.Figure``.
"""
from __future__ import annotations

import math
from typing import Any, Optional

try:
    import matplotlib.pyplot as plt
    import numpy as np
    _MATPLOTLIB_AVAILABLE = True
except ImportError:
    _MATPLOTLIB_AVAILABLE = False


_SHORT_NAMES: dict[str, str] = {
    "openrouter-openai-gpt-4o": "GPT-4o",
    "openrouter-anthropic-claude-3.5-sonnet": "Claude 3.5",
    "openrouter-google-gemini-pro-1.5": "Gemini 1.5",
    "openrouter-meta-llama-llama-3.1-405b-instruct": "LLaMA 405B",
    "openrouter-mistralai-mistral-large": "Mistral Lg",
    "openrouter-deepseek-deepseek-chat": "DeepSeek",
    "openrouter-qwen-qwen-2.5-72b-instruct": "Qwen 2.5",
    "openrouter-cohere-command-r-plus": "Command R+",
    "openrouter-mistralai-mixtral-8x22b-instruct": "Mixtral 8×22B",
    "openrouter-01-ai-yi-large": "Yi Large",
}


def _short(agent_id: str) -> str:
    return _SHORT_NAMES.get(agent_id, agent_id.split("-")[-1][:12])


def _ols_with_ci(
    x: list[float], y: list[float], alpha: float = 0.05
) -> tuple[float, float, float, float, float]:
    """Return (intercept, slope, x_lo, x_hi, se_beta1).

    Pure-Python OLS for two variables; used to draw the CI band without scipy.
    """
    n = len(x)
    if n < 3:
        raise ValueError("Need at least 3 observations for OLS CI.")

    x_bar = sum(x) / n
    y_bar = sum(y) / n
    sxx = sum((xi - x_bar) ** 2 for xi in x)
    sxy = sum((xi - x_bar) * (yi - y_bar) for xi, yi in zip(x, y))

    if abs(sxx) < 1e-12:
        raise ValueError("All P1 scores are identical — cannot fit OLS.")

    beta1 = sxy / sxx
    beta0 = y_bar - beta1 * x_bar

    residuals = [yi - (beta0 + beta1 * xi) for xi, yi in zip(x, y)]
    s2 = sum(r ** 2 for r in residuals) / (n - 2)
    se_beta1 = math.sqrt(s2 / sxx)

    return beta0, beta1, min(x), max(x), se_beta1


def plot_capability_scatter(
    cell_df: Any,
    p1_scores: dict[str, float],
    *,
    figsize: tuple[float, float] = (7.0, 5.5),
    title: str = "Pillar 1 Capability vs. Mean BSI",
    agent_col: str = "agent_id",
    mean_col: str = "mean_bsi",
    draw_regression: bool = True,
    ci_level: float = 0.95,
) -> "plt.Figure":
    """Scatter plot: capability score (X) vs. mean BSI (Y), one point per model.

    Parameters
    ----------
    cell_df:
        Aggregated cell-level DataFrame.  Required columns: *agent_col*,
        *mean_col*.  The mean BSI per model is computed by averaging across
        all bias categories present in the DataFrame.
    p1_scores:
        ``{agent_id: P1_score}`` from a Pillar 1 experiment run.
    figsize:
        Matplotlib figure size in inches.
    title:
        Axis title.
    agent_col, mean_col:
        Column name overrides.
    draw_regression:
        If True, fit and draw an OLS regression line with a *ci_level* CI band.
    ci_level:
        Confidence level for the regression CI band (default 0.95).

    Returns
    -------
    matplotlib.figure.Figure

    Raises
    ------
    ImportError
        When ``matplotlib`` is not installed.
    ValueError
        When *cell_df* is missing required columns or fewer than 3 models have
        both P2 data and P1 scores.
    """
    if not _MATPLOTLIB_AVAILABLE:
        raise ImportError(
            "matplotlib is required for figure generation.  "
            "Install with: pip install matplotlib"
        )

    # ── Validate columns ──────────────────────────────────────────────────────
    for col in (agent_col, mean_col):
        if col not in cell_df.columns:
            raise ValueError(f"cell_df is missing column '{col}'.")

    # ── Aggregate: per-model mean BSI ─────────────────────────────────────────
    model_mean_bsi = (
        cell_df.groupby(agent_col)[mean_col].mean().to_dict()
    )

    common = sorted(a for a in model_mean_bsi if a in p1_scores)
    if len(common) < 3:
        raise ValueError(
            f"Only {len(common)} model(s) have both P2 data and P1 scores; "
            "need at least 3."
        )

    x_vals = [p1_scores[a] for a in common]
    y_vals = [model_mean_bsi[a] for a in common]

    # ── Build figure ──────────────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=figsize)

    ax.scatter(x_vals, y_vals, s=80, color="steelblue", zorder=5, edgecolors="white", linewidths=0.8)

    # Model labels (offset to avoid overlap)
    for agent, x, y in zip(common, x_vals, y_vals):
        ax.annotate(
            _short(agent),
            xy=(x, y),
            xytext=(5, 4),
            textcoords="offset points",
            fontsize=8,
            color="#333333",
        )

    # ── OLS regression line + CI band ────────────────────────────────────────
    if draw_regression and len(common) >= 3:
        try:
            beta0, beta1, x_lo, x_hi, se_beta1 = _ols_with_ci(x_vals, y_vals)
            x_range = np.linspace(x_lo - 0.02 * (x_hi - x_lo), x_hi + 0.02 * (x_hi - x_lo), 200)
            y_hat = beta0 + beta1 * x_range

            n = len(common)
            x_bar = sum(x_vals) / n
            sxx = sum((xi - x_bar) ** 2 for xi in x_vals)

            # Pure-Python t critical value for CI
            df = n - 2
            t_crit_map = {1: 12.71, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571,
                          6: 2.447, 7: 2.365, 8: 2.306, 9: 2.262, 10: 2.228}
            t_crit = t_crit_map.get(df, 1.96)

            # SE of fitted line at each x_range point
            residuals = [y - (beta0 + beta1 * xv) for xv, y in zip(x_vals, y_vals)]
            s2 = sum(r ** 2 for r in residuals) / max(1, n - 2)
            se_line = np.sqrt(s2 * (1.0 / n + (x_range - x_bar) ** 2 / max(sxx, 1e-12)))
            ci_upper = y_hat + t_crit * se_line
            ci_lower = y_hat - t_crit * se_line

            ax.plot(x_range, y_hat, color="tomato", linewidth=1.5, label=f"OLS fit (β₁={beta1:.2f})")
            ax.fill_between(x_range, ci_lower, ci_upper, alpha=0.15, color="tomato",
                            label=f"{int(ci_level * 100)}% CI band")
            ax.legend(fontsize=9, framealpha=0.8)
        except ValueError:
            pass  # skip regression line if degenerate

    ax.set_xlabel("Pillar 1 Score (capability)", fontsize=11)
    ax.set_ylabel("Mean BSI (across bias types)", fontsize=11)
    ax.set_title(title, fontsize=12, fontweight="bold")
    ax.set_ylim(-0.05, 1.05)
    ax.grid(axis="both", alpha=0.3, linestyle="--")

    # Descriptive-only caveat
    n_models = len(common)
    ax.text(
        0.97, 0.04,
        f"N = {n_models} models\nInterpret as descriptive only",
        transform=ax.transAxes,
        ha="right", va="bottom",
        fontsize=8, color="#666666",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow", alpha=0.7),
    )

    fig.tight_layout()
    return fig
