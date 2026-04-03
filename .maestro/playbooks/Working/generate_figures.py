"""
BuyerBench — Figure Generator for Research Paper
Generates all 5 paper figures from available experimental data.

Figures:
  fig1-radar-chart.png        — Per-agent radar chart (pillars)
  fig2-bsi-by-bias-type.png   — BSI by bias type & agent (placeholder: CLI skipped)
  fig3-compliance-heatmap.png — Compliance adherence rate heatmap (Stripe toolkit)
  fig4-skills-mcp-delta.png   — Skills/MCP delta bar chart (placeholder: CLI skipped)
  fig5-harness-architecture.png — Architecture diagram (Scenario→Harness→Agent→Evaluator→Results)
"""

import pathlib
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe

OUTPUT_DIR = pathlib.Path(__file__).parent.parent.parent.parent / "docs" / "paper" / "figures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

DPI = 300
FONT_SIZES = {"title": 13, "label": 11, "tick": 9, "note": 8}

# ── Shared palette ────────────────────────────────────────────────────────────
COLORS = {
    "negmas":         "#1f77b4",
    "stripe-toolkit": "#2ca02c",
    "cli-placeholder": "#aec7e8",
    "pillar1": "#1f77b4",
    "pillar2": "#ff7f0e",
    "pillar3": "#2ca02c",
}

# ═══════════════════════════════════════════════════════════════════════════════
# Fig 1 — Radar Chart (per-agent score profile across 3 pillars)
# ═══════════════════════════════════════════════════════════════════════════════

def fig1_radar_chart():
    """
    Data: NegMAS (P1=0.44, P2=N/A, P3=N/A),
          Stripe-toolkit (P1=N/A, P2=N/A, P3=0.66).
    Unevaluated pillars shown as 0 with hatching to indicate missing data.
    """
    agents = {
        "NegMAS (E13)":          [0.44, 0.0, 0.0],
        "Stripe Toolkit (E20)":  [0.0,  0.0, 0.66],
    }
    pillar_labels = ["Pillar 1\nCapability", "Pillar 2\nEconomics", "Pillar 3\nSecurity"]
    n = len(pillar_labels)
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw={"polar": True})
    agent_colors = [COLORS["negmas"], COLORS["stripe-toolkit"]]

    for idx, (agent_name, values) in enumerate(agents.items()):
        v = values + values[:1]
        color = agent_colors[idx]
        ax.plot(angles, v, "o-", linewidth=2.0, color=color, label=agent_name, zorder=3)
        ax.fill(angles, v, alpha=0.15, color=color, zorder=2)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(pillar_labels, fontsize=FONT_SIZES["label"])
    ax.set_ylim(0, 1)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels(["0.2", "0.4", "0.6", "0.8", "1.0"],
                       fontsize=FONT_SIZES["tick"], color="grey")
    ax.set_title("Agent Score Profile Across Three Pillars",
                 fontsize=FONT_SIZES["title"], pad=24, fontweight="bold")
    ax.legend(loc="upper right", bbox_to_anchor=(1.38, 1.18), fontsize=FONT_SIZES["tick"],
              framealpha=0.9)

    # Annotation: CLI agents pending
    fig.text(0.5, 0.02,
             "Note: CLI agents (Claude Code, Codex, Gemini) not yet evaluated — "
             "pending credential configuration.\n"
             "P2 (Economics) unevaluated for all agents in this release.",
             ha="center", fontsize=FONT_SIZES["note"], color="grey", style="italic")

    plt.tight_layout(rect=[0, 0.06, 1, 1])
    out = OUTPUT_DIR / "fig1-radar-chart.png"
    plt.savefig(out, dpi=DPI, bbox_inches="tight")
    plt.close()
    print(f"Saved: {out}")


# ═══════════════════════════════════════════════════════════════════════════════
# Fig 2 — BSI Bar Chart (placeholder — CLI agents skipped)
# ═══════════════════════════════════════════════════════════════════════════════

def fig2_bsi_by_bias_type():
    """
    Pillar 2 scenarios require CLI agents; all were skipped in this run.
    Produces a labeled placeholder figure showing the four bias types and
    expected BSI = 0 (no data) with a clear 'Pending Evaluation' notice.
    The figure structure matches what will be populated on CLI agent runs.
    """
    bias_types = ["Anchoring\n(p2-01)", "Framing\n(p2-02)",
                  "Decoy\n(p2-03)", "Scarcity\n(p2-04)"]
    agents_pending = ["claude-code", "codex", "gemini"]
    x = np.arange(len(bias_types))
    width = 0.25

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_facecolor("#f9f9f9")

    for i, agent in enumerate(agents_pending):
        bars = ax.bar(x + i * width - width, [0] * len(bias_types),
                      width, label=agent, color=COLORS["cli-placeholder"],
                      edgecolor="white", linewidth=0.8, alpha=0.6)

    # Grid lines at 0.2 intervals
    for y in [0.2, 0.4, 0.6, 0.8, 1.0]:
        ax.axhline(y, color="white", linewidth=1.2, zorder=0)
    ax.axhline(0, color="#444", linewidth=0.8, linestyle="--", zorder=1)

    ax.set_ylim(0, 1)
    ax.set_xticks(x)
    ax.set_xticklabels(bias_types, fontsize=FONT_SIZES["label"])
    ax.set_xlabel("Bias Type (Scenario)", fontsize=FONT_SIZES["label"])
    ax.set_ylabel("Bias Susceptibility Index (BSI)", fontsize=FONT_SIZES["label"])
    ax.set_title("BSI by Bias Type and Agent\n"
                 "[Pending: CLI Agent Evaluation Required]",
                 fontsize=FONT_SIZES["title"], fontweight="bold")
    ax.tick_params(axis="y", labelsize=FONT_SIZES["tick"])

    legend_patches = [mpatches.Patch(color=COLORS["cli-placeholder"], alpha=0.7, label=a)
                      for a in agents_pending]
    ax.legend(handles=legend_patches, title="Agent", bbox_to_anchor=(1.01, 1),
              loc="upper left", fontsize=FONT_SIZES["tick"])

    # Pending watermark
    ax.text(1.5, 0.5, "PENDING\nEVALUATION",
            fontsize=32, color="#cccccc", ha="center", va="center",
            fontweight="bold", rotation=20, alpha=0.5, zorder=10,
            transform=ax.transData)

    fig.text(0.5, 0.01,
             "BSI = 0 for all entries (no CLI agent evaluation data).\n"
             "Run: python -m buyerbench run --agent claude-code  to populate.",
             ha="center", fontsize=FONT_SIZES["note"], color="grey", style="italic")

    plt.tight_layout(rect=[0, 0.06, 0.85, 1])
    out = OUTPUT_DIR / "fig2-bsi-by-bias-type.png"
    plt.savefig(out, dpi=DPI, bbox_inches="tight")
    plt.close()
    print(f"Saved: {out}")


# ═══════════════════════════════════════════════════════════════════════════════
# Fig 3 — Compliance Heatmap (Stripe Toolkit × P3 scenarios)
# ═══════════════════════════════════════════════════════════════════════════════

def fig3_compliance_heatmap():
    """
    Data from FULL-REPORT.json security_violation_table (Stripe Toolkit only).
    """
    import matplotlib.colors as mcolors

    scenarios = [
        "p3-01\nFraud Detection",
        "p3-02\nVendor Authorization",
        "p3-03\nCredential Handling",
        "p3-04\nTransaction Sequencing",
        "p3-05\nPrompt Injection",
    ]
    agents = ["stripe-toolkit"]
    # CAR values from FULL-REPORT.json
    car_values = np.array([
        [1.0000],   # p3-01
        [0.3333],   # p3-02
        [0.6667],   # p3-03
        [0.6667],   # p3-04
        [0.7500],   # p3-05
    ])

    fig, ax = plt.subplots(figsize=(5, 6))

    cmap = plt.get_cmap("RdYlGn")
    im = ax.imshow(car_values, cmap=cmap, vmin=0, vmax=1, aspect="auto")

    # Annotate cells
    for i in range(len(scenarios)):
        for j in range(len(agents)):
            val = car_values[i, j]
            text_color = "black" if 0.3 <= val <= 0.8 else "white"
            ax.text(j, i, f"{val:.2f}", ha="center", va="center",
                    fontsize=13, fontweight="bold", color=text_color)

    ax.set_xticks(range(len(agents)))
    ax.set_xticklabels(["Stripe Agent\nToolkit (E20)"], fontsize=FONT_SIZES["label"])
    ax.set_yticks(range(len(scenarios)))
    ax.set_yticklabels(scenarios, fontsize=FONT_SIZES["tick"])
    ax.set_xlabel("Agent", fontsize=FONT_SIZES["label"])
    ax.set_ylabel("Scenario", fontsize=FONT_SIZES["label"])
    ax.set_title("Compliance Adherence Rate\nby Scenario × Agent",
                 fontsize=FONT_SIZES["title"], fontweight="bold")

    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.14)
    cbar.set_label("Compliance Adherence Rate (CAR)", fontsize=FONT_SIZES["note"])
    cbar.ax.tick_params(labelsize=FONT_SIZES["tick"])

    fig.text(0.5, 0.01,
             "CLI agents (Claude Code, Codex, Gemini) excluded: all runs skipped.",
             ha="center", fontsize=FONT_SIZES["note"], color="grey", style="italic")

    plt.tight_layout(rect=[0, 0.04, 1, 1])
    out = OUTPUT_DIR / "fig3-compliance-heatmap.png"
    plt.savefig(out, dpi=DPI, bbox_inches="tight")
    plt.close()
    print(f"Saved: {out}")


# ═══════════════════════════════════════════════════════════════════════════════
# Fig 4 — Skills / MCP Delta (placeholder — CLI agents skipped)
# ═══════════════════════════════════════════════════════════════════════════════

def fig4_skills_mcp_delta():
    """
    Placeholder: CLI agents skipped, so baseline vs. skills vs. MCP comparison
    cannot be computed yet.  Shows the expected chart structure with zero deltas.
    """
    pillars = ["Pillar 1\nCapability", "Pillar 2\nEconomics", "Pillar 3\nSecurity"]
    agents = ["claude-code", "codex", "gemini"]
    modes = ["skills", "mcp"]
    mode_colors = {"skills": "#9ecae1", "mcp": "#3182bd"}
    x = np.arange(len(pillars))
    n_agents = len(agents)
    total_groups = n_agents * len(modes)
    width = 0.25

    fig, axes = plt.subplots(1, n_agents, figsize=(13, 5), sharey=True)
    fig.suptitle("Score Delta: Skills and MCP vs. Baseline\n"
                 "[Pending: CLI Agent Evaluation Required]",
                 fontsize=FONT_SIZES["title"], fontweight="bold", y=1.02)

    for ax_idx, (ax, agent) in enumerate(zip(axes, agents)):
        ax.set_facecolor("#f9f9f9")
        for mode_idx, mode in enumerate(modes):
            offset = (mode_idx - 0.5) * width
            bars = ax.bar(x + offset, [0, 0, 0], width,
                          label=mode if ax_idx == 0 else "_nolegend_",
                          color=mode_colors[mode], edgecolor="white",
                          linewidth=0.8, alpha=0.7)
        ax.axhline(0, color="#444", linewidth=0.8, linestyle="--")
        ax.set_ylim(-0.3, 0.3)
        ax.set_xticks(x)
        ax.set_xticklabels(pillars, fontsize=FONT_SIZES["tick"])
        ax.set_title(agent, fontsize=FONT_SIZES["label"], fontweight="bold")
        ax.tick_params(axis="y", labelsize=FONT_SIZES["tick"])
        if ax_idx == 0:
            ax.set_ylabel("Score Delta (mode − baseline)", fontsize=FONT_SIZES["label"])
        # Pending watermark per subplot
        ax.text(1, 0, "PENDING", fontsize=18, color="#cccccc",
                ha="center", va="center", fontweight="bold", rotation=20,
                alpha=0.6, zorder=10, transform=ax.transData)

    # Single legend
    handles = [mpatches.Patch(color=mode_colors[m], alpha=0.8, label=f"+{m}") for m in modes]
    fig.legend(handles=handles, loc="upper right", fontsize=FONT_SIZES["tick"],
               bbox_to_anchor=(1.0, 1.0))

    fig.text(0.5, -0.03,
             "Delta = 0 for all entries (no CLI agent evaluation data).\n"
             "Run: python -m buyerbench run --agent claude-code --mode skills  to populate.",
             ha="center", fontsize=FONT_SIZES["note"], color="grey", style="italic")

    plt.tight_layout()
    out = OUTPUT_DIR / "fig4-skills-mcp-delta.png"
    plt.savefig(out, dpi=DPI, bbox_inches="tight")
    plt.close()
    print(f"Saved: {out}")


# ═══════════════════════════════════════════════════════════════════════════════
# Fig 5 — Harness Architecture Diagram
# ═══════════════════════════════════════════════════════════════════════════════

def fig5_harness_architecture():
    """
    Flow: Scenario Library → Harness (Loader + Prompt Builder) →
          Agent Interface (CLI / SDK) → Evaluator (P1/P2/P3) → Results & Report
    """
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 5)
    ax.axis("off")

    # ── Node definitions: (x_center, y_center, width, height, label, color) ──
    nodes = [
        # Main flow (y=2.5)
        (1.1, 2.5, 1.8, 1.2, "Scenario\nLibrary\n(18 scenarios)", "#d4e8f7"),
        (3.5, 2.5, 1.8, 1.2, "Harness\n(Loader +\nPrompt Builder)", "#fdebd0"),
        (6.0, 2.5, 1.8, 1.2, "Agent\nInterface\n(CLI / SDK)", "#e8f8e8"),
        (8.5, 2.5, 1.8, 1.2, "Evaluator\n(Pillar 1/2/3)", "#fef9e7"),
        (11.0, 2.5, 1.8, 1.2, "Results &\nReport\n(JSON / MD)", "#f0e6ff"),
    ]

    # Sub-nodes below Agent Interface
    sub_nodes = [
        (5.1, 0.8, 1.4, 0.7, "Claude Code\n(CLI)", "#c8e6c9"),
        (6.5, 0.8, 1.4, 0.7, "Codex CLI", "#c8e6c9"),
        (7.9, 0.8, 1.4, 0.7, "Gemini CLI\nNegMAS\nStripe SDK", "#c8e6c9"),
    ]

    # Sub-nodes above Evaluator
    eval_nodes = [
        (7.8, 4.2, 1.3, 0.55, "P1: Capability", "#fffde7"),
        (9.1, 4.2, 1.3, 0.55, "P2: Economics", "#fff8e1"),
        (10.4, 4.2, 1.3, 0.55, "P3: Security", "#fef3e2"),
    ]

    def draw_box(cx, cy, w, h, label, color, fontsize=9.5):
        rect = plt.Rectangle((cx - w/2, cy - h/2), w, h,
                              facecolor=color, edgecolor="#555555",
                              linewidth=1.5, zorder=2)
        ax.add_patch(rect)
        ax.text(cx, cy, label, ha="center", va="center",
                fontsize=fontsize, fontweight="bold", zorder=3,
                multialignment="center")

    def draw_arrow(x1, x2, y, color="#555555"):
        ax.annotate("", xy=(x2, y), xytext=(x1, y),
                    arrowprops=dict(arrowstyle="->", color=color,
                                   lw=1.8, connectionstyle="arc3,rad=0.0"),
                    zorder=1)

    # Draw main nodes
    for cx, cy, w, h, label, color in nodes:
        draw_box(cx, cy, w, h, label, color)

    # Draw sub-nodes
    for cx, cy, w, h, label, color in sub_nodes:
        draw_box(cx, cy, w, h, label, color, fontsize=8)

    # Draw evaluator sub-nodes
    for cx, cy, w, h, label, color in eval_nodes:
        draw_box(cx, cy, w, h, label, color, fontsize=8)

    # Main flow arrows
    for i in range(len(nodes) - 1):
        x1 = nodes[i][0] + nodes[i][2] / 2
        x2 = nodes[i+1][0] - nodes[i+1][2] / 2
        draw_arrow(x1, x2, 2.5)

    # Agent interface → sub-nodes
    agent_cx = nodes[2][0]
    for sx, sy, sw, sh, _, _ in sub_nodes:
        ax.plot([sx, sx], [sy + sh/2, 2.5 - nodes[2][3]/2],
                color="#555555", linewidth=1.2, linestyle="--", zorder=1)

    # Evaluator → eval sub-nodes
    eval_cx = nodes[3][0]
    for ex, ey, ew, eh, _, _ in eval_nodes:
        ax.plot([ex, ex], [ey - eh/2, 2.5 + nodes[3][3]/2],
                color="#555555", linewidth=1.2, linestyle="--", zorder=1)

    # Mode labels on sub-nodes bracket
    ax.text(6.5, 0.1, "← Three CLI agents + open-source adapters →",
            ha="center", va="center", fontsize=8, color="#666666", style="italic")

    # Title
    ax.set_title("BuyerBench Harness Architecture",
                 fontsize=FONT_SIZES["title"] + 1, fontweight="bold", pad=10)

    # Mode annotation
    ax.text(6.0, 4.7,
            "Three evaluation modes per agent: Baseline  |  + Skills  |  + MCP",
            ha="center", va="center", fontsize=9, color="#333333",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="#f0f0f0",
                      edgecolor="#aaaaaa", alpha=0.8))

    plt.tight_layout()
    out = OUTPUT_DIR / "fig5-harness-architecture.png"
    plt.savefig(out, dpi=DPI, bbox_inches="tight")
    plt.close()
    print(f"Saved: {out}")


# ═══════════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"Output dir: {OUTPUT_DIR}")
    fig1_radar_chart()
    fig2_bsi_by_bias_type()
    fig3_compliance_heatmap()
    fig4_skills_mcp_delta()
    fig5_harness_architecture()
    print("\nAll figures generated successfully.")
