"""Figure 1 — BSI Heatmap.

Renders a model × bias_type heatmap where cell color encodes mean BSI.
  - X-axis: model names, sorted by capability tier (Pillar 1 score)
  - Y-axis: bias types
  - Color scale: 0 (blue) → 1 (red)
  - Cell annotations: mean ± SD
  - Optional human benchmark row

Public API
----------
- ``plot_bsi_heatmap(cell_df, p1_scores=None, human_bsi=None, ...)``
  Returns a ``matplotlib.figure.Figure``.
"""
from __future__ import annotations

from typing import Any, Optional

try:
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors
    import numpy as np
    _MATPLOTLIB_AVAILABLE = True
except ImportError:
    _MATPLOTLIB_AVAILABLE = False


# ── Short display names for known agent IDs ───────────────────────────────────

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
    "mock-agent-v1": "Mock Agent",
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


def _short(agent_id: str) -> str:
    return _SHORT_NAMES.get(agent_id, agent_id.split("-")[-1][:12])


def _bias_label(bias: str) -> str:
    return _BIAS_DISPLAY.get(bias, bias.replace("_", " ").title())


def plot_bsi_heatmap(
    cell_df: Any,
    *,
    p1_scores: Optional[dict[str, float]] = None,
    human_bsi: Optional[dict[str, float]] = None,
    figsize: tuple[float, float] = (12.0, 5.5),
    annotate: bool = True,
    title: str = "Bias Susceptibility Index (BSI) — Model × Bias Type",
    agent_col: str = "agent_id",
    bias_col: str = "bias_category",
    mean_col: str = "mean_bsi",
    std_col: str = "std_bsi",
) -> "plt.Figure":
    """Render a model × bias-type BSI heatmap.

    Parameters
    ----------
    cell_df:
        Aggregated cell-level DataFrame.  Required columns: *agent_col*,
        *bias_col*, *mean_col*, and (when *annotate* is True) *std_col*.
    p1_scores:
        ``{agent_id: P1_score}`` mapping used to sort models along the X-axis
        from most to least capable.  When absent, models are sorted
        alphabetically.
    human_bsi:
        ``{bias_category: bsi_value}`` for a human-benchmark row appended at
        the bottom of the heatmap.
    figsize:
        Matplotlib figure size (width, height) in inches.
    annotate:
        If True, each cell is annotated with ``"mean ± SD"``.
    title:
        Figure title.
    agent_col, bias_col, mean_col, std_col:
        Column name overrides.

    Returns
    -------
    matplotlib.figure.Figure

    Raises
    ------
    ImportError
        When ``matplotlib`` or ``numpy`` are not installed.
    ValueError
        When *cell_df* is missing required columns.
    """
    if not _MATPLOTLIB_AVAILABLE:
        raise ImportError(
            "matplotlib and numpy are required for figure generation.  "
            "Install with: pip install matplotlib numpy"
        )

    import pandas as pd

    # ── Validate columns ──────────────────────────────────────────────────────
    required = {agent_col, bias_col, mean_col}
    missing = required - set(cell_df.columns)
    if missing:
        raise ValueError(f"cell_df is missing columns: {missing}")
    if annotate and std_col not in cell_df.columns:
        annotate = False  # silently degrade — std unavailable

    # ── Pivot to matrix (models × biases) ────────────────────────────────────
    pivot_mean = cell_df.pivot_table(
        index=agent_col, columns=bias_col, values=mean_col, aggfunc="mean"
    )
    pivot_std = None
    if annotate and std_col in cell_df.columns:
        pivot_std = cell_df.pivot_table(
            index=agent_col, columns=bias_col, values=std_col, aggfunc="mean"
        )

    # ── Sort models by P1 capability score (descending) ──────────────────────
    if p1_scores:
        all_agents = list(pivot_mean.index)
        sorted_agents = sorted(
            all_agents,
            key=lambda a: p1_scores.get(a, 0.0),
            reverse=True,
        )
        pivot_mean = pivot_mean.loc[sorted_agents]
        if pivot_std is not None:
            pivot_std = pivot_std.loc[sorted_agents]
    else:
        pivot_mean = pivot_mean.sort_index()
        if pivot_std is not None:
            pivot_std = pivot_std.sort_index()

    # ── Append human benchmark row ────────────────────────────────────────────
    if human_bsi:
        bias_cols = list(pivot_mean.columns)
        human_row = pd.DataFrame(
            [[human_bsi.get(b, float("nan")) for b in bias_cols]],
            columns=bias_cols,
            index=["Human Benchmark"],
        )
        pivot_mean = pd.concat([pivot_mean, human_row])
        if pivot_std is not None:
            human_std_row = pd.DataFrame(
                [[float("nan")] * len(bias_cols)],
                columns=bias_cols,
                index=["Human Benchmark"],
            )
            pivot_std = pd.concat([pivot_std, human_std_row])

    # ── Display labels ────────────────────────────────────────────────────────
    row_labels = [
        "Human Benchmark" if r == "Human Benchmark" else _short(r)
        for r in pivot_mean.index
    ]
    col_labels = [_bias_label(c) for c in pivot_mean.columns]

    matrix = pivot_mean.values.astype(float)
    n_rows, n_cols = matrix.shape

    # ── Build figure ──────────────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=figsize)

    cmap = plt.cm.RdYlBu_r  # blue (low BSI) → red (high BSI)
    im = ax.imshow(matrix, cmap=cmap, vmin=0.0, vmax=1.0, aspect="auto")

    # Colour bar
    cbar = fig.colorbar(im, ax=ax, fraction=0.025, pad=0.02)
    cbar.set_label("Mean BSI", fontsize=10)
    cbar.set_ticks([0.0, 0.25, 0.5, 0.75, 1.0])

    # Tick labels
    ax.set_xticks(range(n_cols))
    ax.set_xticklabels(col_labels, rotation=30, ha="right", fontsize=9)
    ax.set_yticks(range(n_rows))
    ax.set_yticklabels(row_labels, fontsize=9)

    # Separate human benchmark row with a horizontal line
    if human_bsi and n_rows > 1:
        ax.axhline(n_rows - 1.5, color="white", linewidth=2.5, linestyle="--")

    # Cell annotations
    if annotate:
        std_matrix = pivot_std.values.astype(float) if pivot_std is not None else None
        for r in range(n_rows):
            for c in range(n_cols):
                val = matrix[r, c]
                if np.isnan(val):
                    continue
                text = f"{val:.2f}"
                if std_matrix is not None and not np.isnan(std_matrix[r, c]):
                    text = f"{val:.2f}\n±{std_matrix[r, c]:.2f}"
                # choose white or black text based on cell brightness
                bg = cmap((val - 0.0) / 1.0)
                brightness = 0.299 * bg[0] + 0.587 * bg[1] + 0.114 * bg[2]
                color = "white" if brightness < 0.5 else "black"
                ax.text(c, r, text, ha="center", va="center", fontsize=7, color=color)

    ax.set_title(title, fontsize=12, fontweight="bold", pad=10)
    ax.set_xlabel("Bias Type", fontsize=10)
    ax.set_ylabel("Model (sorted by P1 capability ↓)" if p1_scores else "Model", fontsize=10)

    fig.tight_layout()
    return fig
