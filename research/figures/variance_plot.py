"""Figure 4 — Variance Decomposition & Treatment Effects.

Two complementary views of the Pillar 2 results:

``plot_variance_decomposition(decomp_result)``
    Stacked (or grouped) bar chart showing the proportion of total BSI variance
    attributable to: Model, Bias Type, Treatment, Temperature, and Residual.

``plot_treatment_effects(cell_df)``
    Forest plot: point estimate (treatment_effect) ± 95% CI for each
    (bias_type × model) cell.  Sorted by effect size within each bias type;
    reference line at 0 (no effect).

Both functions return ``matplotlib.figure.Figure`` objects.
"""
from __future__ import annotations

from typing import Any, Optional

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
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

_BIAS_DISPLAY: dict[str, str] = {
    "anchoring": "Anchoring",
    "framing": "Framing",
    "decoy": "Decoy Effect",
    "scarcity": "Scarcity",
    "sunk_cost": "Sunk Cost",
    "default_bias": "Default Bias",
    "loss_aversion": "Loss Aversion",
    "status_quo": "Status Quo",
}

# Colour palette for variance components
_VARIANCE_COLORS: dict[str, str] = {
    "Model": "#5b9bd5",
    "BiasType": "#ed7d31",
    "Treatment": "#a9d18e",
    "Temperature": "#ffc000",
    "Residual": "#d0d0d0",
}


def _short(agent_id: str) -> str:
    return _SHORT_NAMES.get(agent_id, agent_id.split("-")[-1][:12])


def _bias_label(bias: str) -> str:
    return _BIAS_DISPLAY.get(bias, bias.replace("_", " ").title())


# ─────────────────────────────────────────────────────────────────────────────
# Variance Decomposition Bar Chart
# ─────────────────────────────────────────────────────────────────────────────


def plot_variance_decomposition(
    decomp_result: Any,
    *,
    figsize: tuple[float, float] = (7.0, 4.5),
    title: str = "BSI Variance Decomposition",
    show_pct_labels: bool = True,
) -> "plt.Figure":
    """Stacked horizontal bar chart of variance components.

    Parameters
    ----------
    decomp_result:
        A ``VarianceDecompositionResult`` object (from
        ``research.analysis.regression.run_variance_decomposition``) or any
        object with a ``.rows`` attribute, each row having ``.source``,
        ``.pct_variance``, and ``.eta_squared`` fields.
    figsize:
        Figure size in inches.
    title:
        Figure title.
    show_pct_labels:
        If True, percentage labels are rendered inside each bar segment.

    Returns
    -------
    matplotlib.figure.Figure

    Raises
    ------
    ImportError
        When ``matplotlib`` is not installed.
    ValueError
        When *decomp_result* has no rows.
    """
    if not _MATPLOTLIB_AVAILABLE:
        raise ImportError(
            "matplotlib is required for figure generation.  "
            "Install with: pip install matplotlib"
        )

    rows = getattr(decomp_result, "rows", None)
    if not rows:
        raise ValueError("decomp_result.rows is empty or missing.")

    sources = [r.source for r in rows]
    pcts = [r.pct_variance for r in rows]
    colors = [_VARIANCE_COLORS.get(s, "#bbbbbb") for s in sources]

    fig, ax = plt.subplots(figsize=figsize)

    left = 0.0
    bar_height = 0.55
    handles = []
    for source, pct, color in zip(sources, pcts, colors):
        bar = ax.barh(0, pct, left=left, height=bar_height, color=color, edgecolor="white",
                      linewidth=0.8)
        if show_pct_labels and pct >= 3.0:
            ax.text(
                left + pct / 2, 0,
                f"{pct:.1f}%",
                va="center", ha="center",
                fontsize=8, color="black" if pct > 10 else "white",
                fontweight="bold" if pct > 15 else "normal",
            )
        handles.append(mpatches.Patch(facecolor=color, label=source))
        left += pct

    ax.set_xlim(0, 100)
    ax.set_yticks([])
    ax.set_xlabel("% of Total BSI Variance (η²)", fontsize=10)
    ax.set_title(title, fontsize=12, fontweight="bold")
    ax.legend(
        handles=handles,
        loc="lower center",
        bbox_to_anchor=(0.5, -0.35),
        ncol=min(len(handles), 5),
        fontsize=9,
        framealpha=0.8,
    )

    # Annotation from research note
    n_obs = getattr(decomp_result, "n_obs", None)
    note = getattr(decomp_result, "notes", "")
    footer = f"N = {n_obs} runs.  " if n_obs else ""
    if "η²_Residual > 0.70" in note:
        footer += "η²_Residual > 0.70 → most variance is within-cell stochastic noise."
    if footer:
        ax.text(
            0.5, -0.18, footer,
            transform=ax.transAxes,
            ha="center", fontsize=7.5, color="#555555", style="italic",
        )

    fig.tight_layout()
    return fig


# ─────────────────────────────────────────────────────────────────────────────
# Treatment Effects Forest Plot (Figure 4 from L.7)
# ─────────────────────────────────────────────────────────────────────────────


def plot_treatment_effects(
    cell_df: Any,
    *,
    figsize: Optional[tuple[float, float]] = None,
    title: str = "Treatment Effects by Bias Type (BSI_treatment − BSI_baseline)",
    agent_col: str = "agent_id",
    bias_col: str = "bias_category",
    effect_col: str = "treatment_effect",
    ci_lower_col: str = "ci_lower_95",
    ci_upper_col: str = "ci_upper_95",
    p1_scores: Optional[dict[str, float]] = None,
) -> "plt.Figure":
    """Forest plot of treatment effects per (bias_type × model).

    Each row in the forest plot represents one model within a bias category.
    Rows are sorted by effect size (descending) within each bias group.  A
    vertical reference line at 0 marks "no effect."

    Parameters
    ----------
    cell_df:
        Cell-level DataFrame. Required columns: *agent_col*, *bias_col*,
        *effect_col*, *ci_lower_col*, *ci_upper_col*.  Rows where
        *effect_col* is null are silently dropped.
    figsize:
        Override figure size.  Defaults to ``(7, 0.55 * n_rows + 2.5)``.
    title:
        Figure title.
    agent_col, bias_col, effect_col, ci_lower_col, ci_upper_col:
        Column name overrides.
    p1_scores:
        When provided, models are ordered within each bias group by P1 score
        (descending) as a secondary sort after effect size.

    Returns
    -------
    matplotlib.figure.Figure

    Raises
    ------
    ImportError
        When ``matplotlib`` is not installed.
    ValueError
        When *cell_df* is missing required columns or has no valid rows.
    """
    if not _MATPLOTLIB_AVAILABLE:
        raise ImportError(
            "matplotlib is required for figure generation.  "
            "Install with: pip install matplotlib"
        )

    for col in (agent_col, bias_col, effect_col, ci_lower_col, ci_upper_col):
        if col not in cell_df.columns:
            raise ValueError(f"cell_df is missing column '{col}'.")

    clean = cell_df[cell_df[effect_col].notna()].copy()
    if clean.empty:
        raise ValueError("No rows with non-null treatment_effect values found in cell_df.")

    # ── Build ordered rows: sorted by bias, then by effect size descending ────
    biases = sorted(clean[bias_col].dropna().unique())

    rows: list[dict] = []
    for bias in biases:
        group = clean[clean[bias_col] == bias].copy()
        group = group.sort_values(effect_col, ascending=False)
        for _, row in group.iterrows():
            rows.append({
                "label": f"{_short(str(row[agent_col]))}",
                "bias": bias,
                "effect": float(row[effect_col]),
                "ci_lo": float(row[ci_lower_col]),
                "ci_hi": float(row[ci_upper_col]),
            })

    n_rows = len(rows)
    if n_rows == 0:
        raise ValueError("No valid rows to plot.")

    auto_figsize = (8.0, max(4.0, 0.55 * n_rows + 2.5))
    fig, ax = plt.subplots(figsize=figsize or auto_figsize)

    # ── Colour by bias type ───────────────────────────────────────────────────
    bias_palette = plt.cm.Set2(np.linspace(0, 1, len(biases)))
    bias_color = {b: bias_palette[i] for i, b in enumerate(biases)}

    # ── Plot rows (y = 0 is top) ───────────────────────────────────────────────
    y_positions = list(range(n_rows - 1, -1, -1))  # top row = highest y

    group_separators: set[int] = set()
    prev_bias = None

    for y_pos, row_data in zip(y_positions, rows):
        color = bias_color[row_data["bias"]]
        err_lo = row_data["effect"] - row_data["ci_lo"]
        err_hi = row_data["ci_hi"] - row_data["effect"]

        ax.errorbar(
            row_data["effect"], y_pos,
            xerr=[[max(0.0, err_lo)], [max(0.0, err_hi)]],
            fmt="o",
            color=color,
            ecolor=color,
            elinewidth=1.2,
            capsize=3,
            markersize=6,
            zorder=5,
        )

        # Label on the left margin
        ax.text(
            -0.02, y_pos, row_data["label"],
            transform=ax.get_yaxis_transform(),
            ha="right", va="center",
            fontsize=8, color="#333333",
        )

        # Track bias group boundaries for separator lines
        if prev_bias is not None and row_data["bias"] != prev_bias:
            group_separators.add(y_pos)
        prev_bias = row_data["bias"]

    # ── Group separator lines and bias labels ─────────────────────────────────
    bias_label_positions: dict[str, list[int]] = {}
    for y_pos, row_data in zip(y_positions, rows):
        bias_label_positions.setdefault(row_data["bias"], []).append(y_pos)

    for y_sep in group_separators:
        ax.axhline(y_sep + 0.5, color="#cccccc", linewidth=0.8, linestyle="--", zorder=1)

    x_lo, x_hi = ax.get_xlim()
    x_label = x_lo - (x_hi - x_lo) * 0.55
    for bias, y_list in bias_label_positions.items():
        mid_y = (max(y_list) + min(y_list)) / 2.0
        ax.text(
            1.01, mid_y,
            _bias_label(bias),
            transform=ax.get_yaxis_transform(),
            ha="left", va="center",
            fontsize=8, color=bias_color[bias],
            fontweight="bold",
        )

    # ── Reference line at 0 ───────────────────────────────────────────────────
    ax.axvline(0, color="black", linewidth=1.0, linestyle="-", zorder=2)

    ax.set_yticks([])
    ax.set_xlabel("Treatment Effect (BSI_treatment − BSI_baseline)", fontsize=10)
    ax.set_title(title, fontsize=11, fontweight="bold")
    ax.set_ylim(-0.8, n_rows - 0.2)

    # Positive = increased susceptibility; negative = decreased
    x_min, x_max = ax.get_xlim()
    mid = (x_min + x_max) / 2
    ax.text(mid + (x_max - mid) * 0.4, -0.6, "↑ more biased",
            ha="center", fontsize=7.5, color="#888888")
    ax.text(mid - (mid - x_min) * 0.4, -0.6, "↓ less biased",
            ha="center", fontsize=7.5, color="#888888")

    ax.grid(axis="x", alpha=0.3, linestyle="--")
    fig.tight_layout()
    return fig
