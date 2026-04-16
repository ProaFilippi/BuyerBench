"""Figure 3 — Within-Cell BSI Distribution (violin plots).

One violin per (bias_type × variant) showing the distribution of per-run BSI
values.  Motivates n = 50 per cell by demonstrating that single-run results
are unreliable (high within-cell variance).

Public API
----------
- ``plot_bsi_distributions(run_df, ...)``
  Returns a ``matplotlib.figure.Figure``.
"""
from __future__ import annotations

from typing import Any, Optional

try:
    import matplotlib.pyplot as plt
    import numpy as np
    _MATPLOTLIB_AVAILABLE = True
except ImportError:
    _MATPLOTLIB_AVAILABLE = False

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

_CONTROL_VARIANTS = frozenset({"BASELINE", "FRAMING_GAIN"})


def _bias_label(bias: str) -> str:
    return _BIAS_DISPLAY.get(bias, bias.replace("_", " ").title())


def _variant_label(variant: str) -> str:
    return "Baseline" if variant in _CONTROL_VARIANTS else "Treatment"


def _violin_parts(
    ax: "plt.Axes",
    data: list[float],
    pos: float,
    color: str,
    width: float = 0.35,
) -> None:
    """Draw a minimal violin using matplotlib's violinplot, overlaid with median line."""
    if len(data) < 2:
        # Too few points: just draw a scatter dot
        ax.scatter([pos], data, color=color, zorder=5, s=40)
        return
    parts = ax.violinplot([data], positions=[pos], widths=width, showmedians=True,
                          showextrema=True)
    for pc in parts.get("bodies", []):
        pc.set_facecolor(color)
        pc.set_alpha(0.65)
        pc.set_edgecolor("none")
    for line_key in ("cmedians", "cmins", "cmaxes", "cbars"):
        if line_key in parts:
            parts[line_key].set_color(color)
            parts[line_key].set_linewidth(1.2)


def plot_bsi_distributions(
    run_df: Any,
    *,
    figsize: Optional[tuple[float, float]] = None,
    title: str = "Within-Cell BSI Distribution by Bias Type × Variant",
    bias_col: str = "bias_category",
    variant_col: str = "variant",
    bsi_col: str = "bsi",
    baseline_color: str = "#5b9bd5",
    treatment_color: str = "#ed7d31",
    max_biases: int = 8,
) -> "plt.Figure":
    """Violin plots: BSI distribution per (bias_type × variant).

    Demonstrates that single-run BSI values are highly variable, motivating
    the n = 50 per cell design.  Violins are drawn side-by-side (baseline in
    blue, treatment in orange) for each bias category.

    Parameters
    ----------
    run_df:
        Run-level DataFrame with columns *bias_col*, *variant_col*, *bsi_col*.
        All rows with null BSI are dropped silently.
    figsize:
        Override figure size.  Defaults to ``(2.5 * n_biases + 2, 5.5)``.
    title:
        Figure title.
    bias_col, variant_col, bsi_col:
        Column name overrides.
    baseline_color, treatment_color:
        Matplotlib colour strings for baseline / treatment violins.
    max_biases:
        Cap on number of bias types plotted (useful for quick previews).

    Returns
    -------
    matplotlib.figure.Figure

    Raises
    ------
    ImportError
        When ``matplotlib`` or ``numpy`` are not installed.
    ValueError
        When *run_df* is missing required columns.
    """
    if not _MATPLOTLIB_AVAILABLE:
        raise ImportError(
            "matplotlib and numpy are required for figure generation.  "
            "Install with: pip install matplotlib numpy"
        )

    for col in (bias_col, variant_col, bsi_col):
        if col not in run_df.columns:
            raise ValueError(f"run_df is missing column '{col}'.")

    clean = run_df[run_df[bsi_col].notna()].copy()
    clean[bsi_col] = clean[bsi_col].astype(float)

    biases = sorted(clean[bias_col].dropna().unique())[:max_biases]
    n_biases = len(biases)

    if n_biases == 0:
        raise ValueError("No bias categories found in run_df.")

    auto_figsize = (max(8.0, 2.5 * n_biases + 2), 5.5)
    fig, ax = plt.subplots(figsize=figsize or auto_figsize)

    tick_positions: list[float] = []
    tick_labels: list[str] = []
    legend_handles: list[Any] = []

    spacing = 1.0  # space between bias groups
    offset = 0.22  # half-gap between paired violins

    for i, bias in enumerate(biases):
        bias_df = clean[clean[bias_col] == bias]
        center = i * spacing

        baseline_data = bias_df[bias_df[variant_col].isin(_CONTROL_VARIANTS)][bsi_col].tolist()
        treatment_data = bias_df[~bias_df[variant_col].isin(_CONTROL_VARIANTS)][bsi_col].tolist()

        if baseline_data:
            _violin_parts(ax, baseline_data, center - offset, baseline_color)
        if treatment_data:
            _violin_parts(ax, treatment_data, center + offset, treatment_color)

        tick_positions.append(center)
        tick_labels.append(_bias_label(bias))

    # Legend proxies
    from matplotlib.patches import Patch
    legend_handles = [
        Patch(facecolor=baseline_color, alpha=0.65, label="Baseline"),
        Patch(facecolor=treatment_color, alpha=0.65, label="Treatment"),
    ]
    ax.legend(handles=legend_handles, fontsize=9, framealpha=0.8, loc="upper right")

    ax.set_xticks(tick_positions)
    ax.set_xticklabels(tick_labels, rotation=20, ha="right", fontsize=9)
    ax.set_ylabel("BSI (per run)", fontsize=11)
    ax.set_ylim(-0.05, 1.1)
    ax.axhline(0.5, linestyle="--", linewidth=0.8, color="#999999", alpha=0.6,
               label="BSI = 0.5")
    ax.set_title(title, fontsize=12, fontweight="bold")
    ax.grid(axis="y", alpha=0.3, linestyle="--")

    # Annotation: motivate n=50
    ax.text(
        0.02, 0.97,
        "Wide within-cell distributions motivate n = 50 runs per cell",
        transform=ax.transAxes,
        va="top", ha="left",
        fontsize=8, color="#555555",
        style="italic",
    )

    fig.tight_layout()
    return fig
