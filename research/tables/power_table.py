"""Table A1 — Power Analysis.

Paper-ready version of the pre-experiment power analysis (Section G.8).
Reproduces the minimum viable sample table showing required N per cell,
expected minimum detectable effect sizes, and achieved power at key
design tiers.

The table is structured as two panels:
  Panel A — Design Tiers: N/cell, min-detectable d, total runs, cost, power.
  Panel B — Power Grid: achieved power at d ∈ {0.4, 0.5, 0.6} for N ∈ {30, 50, 100}.

Power values in Panel A use the G*Power reference values from G.8.
Panel B values are computed with a normal approximation to the non-central
t-distribution (see ``_approx_power``).

Public API
----------
- ``_approx_power(d, n_per_group, alpha=0.05)``
  Approximate power for a two-sample t-test using the normal distribution.
- ``build_power_table(...)``   — LaTeX str (Table A1, both panels).
- ``save_power_table(output_path, ...)`` — writes .tex file, returns Path.
"""
from __future__ import annotations

import math
from pathlib import Path
from typing import Any, Optional


# ── G.8 Reference constants ───────────────────────────────────────────────────
#
# These are the canonical G*Power values cited in Section G.8 of the research
# design playbook (PILLAR2-RESEARCH-03).  They were computed for a two-sample
# t-test at α = 0.05 (two-tailed), target effect size d = 0.4.
#
#   N = 30/cell → power ≈ 0.52  (exploratory; underpowered for d=0.4)
#   N = 50/cell → power ≈ 0.70  (marginal)
#   N = 100/cell → power ≈ 0.86 (adequate)
#
_GPOWER_REFERENCE: dict[int, float] = {
    30: 0.52,
    50: 0.70,
    100: 0.86,
}

# Experiment grid constants (5 bias × 2 variants × 10 models)
_CELLS_PER_DESIGN: int = 5 * 2 * 10  # = 100

# Approximate cost per LLM run (USD)
_COST_PER_RUN_USD: float = 0.15

# Design tier definitions: (label, N_per_cell, min_d_80pct, G*Power reference at d=0.4)
_DESIGN_TIERS: list[tuple[str, int, str, Optional[float]]] = [
    ("Minimal",       30,  "$\\geq 0.6$",  0.52),
    ("Realistic",     50,  "$\\geq 0.5$",  0.70),
    ("Flagship",      100, "0.4",           0.86),
    ("Gold Standard", 100, "0.4",           0.86),   # + 3 prompts × 3 temps; N kept same
]

# Gold Standard has more cells due to prompt/temperature variations
_GOLD_STANDARD_MULTIPLIER: int = 3 * 3  # 3 prompt_versions × 3 temperatures


# ── Power computation ─────────────────────────────────────────────────────────

def _normal_cdf(x: float) -> float:
    """Standard normal CDF using math.erfc (pure Python, no scipy)."""
    return 0.5 * math.erfc(-x / math.sqrt(2))


def _approx_power(d: float, n_per_group: int, alpha: float = 0.05) -> float:
    """Approximate power for an independent two-sample t-test.

    Uses the normal approximation to the non-central t-distribution:
        power ≈ Φ(λ − z_{α/2})
    where λ = d · √(n/2) is the non-centrality parameter and
    z_{α/2} is the critical value (1.96 for α=0.05 two-tailed).

    This approximation is asymptotically exact as df → ∞ and provides
    a lower bound on power for finite df (the true non-central t gives
    slightly higher power than the normal approx for small df).

    Parameters
    ----------
    d:
        Cohen's d effect size (standardized mean difference).
    n_per_group:
        Number of observations per group (same in each group).
    alpha:
        Two-tailed significance level.

    Returns
    -------
    float
        Approximate power in [0, 1].
    """
    if n_per_group < 2 or d <= 0:
        return 0.0
    z_alpha_2 = _z_crit(alpha)
    noncentrality = d * math.sqrt(n_per_group / 2)
    power = _normal_cdf(noncentrality - z_alpha_2)
    # Add the tiny left-tail contribution (effectively 0 when λ > 0)
    power += _normal_cdf(-noncentrality - z_alpha_2)
    return min(power, 1.0)


def _z_crit(alpha: float = 0.05) -> float:
    """Return the z critical value for a two-tailed test at level alpha.

    Hardcoded for common alpha values; uses Newton–Raphson inverse-CDF
    otherwise.
    """
    known = {0.05: 1.95996, 0.01: 2.57583, 0.001: 3.29053, 0.10: 1.64485}
    if alpha in known:
        return known[alpha]
    # Newton–Raphson on the standard normal CDF for other alpha values
    target = 1.0 - alpha / 2
    z = 1.96  # initial guess
    for _ in range(30):
        fz = _normal_cdf(z) - target
        # PDF of standard normal at z
        pdf_z = math.exp(-z * z / 2) / math.sqrt(2 * math.pi)
        if pdf_z == 0:
            break
        z -= fz / pdf_z
    return z


# ── Table builder ─────────────────────────────────────────────────────────────

def build_power_table(
    *,
    alpha: float = 0.05,
    target_d: float = 0.4,
    effect_sizes: Optional[list[float]] = None,
    n_per_cell_values: Optional[list[int]] = None,
    title: str = (
        "Pre-Experiment Power Analysis (Section G.8): "
        "Required Runs per Cell at $\\alpha = 0.05$"
    ),
    label: str = "tab:power",
) -> str:
    """Build Table A1: pre-experiment power analysis in paper-ready LaTeX.

    Produces two panels:
      **Panel A** — Design tier summary (N/cell, min detectable d, total runs,
      estimated cost, and G*Power reference power at d=0.4).

      **Panel B** — Achieved power grid: rows = effect sizes, columns = N/cell.
      Panel B values are computed with ``_approx_power``.

    Parameters
    ----------
    alpha:
        Significance level for power computations.
    target_d:
        The "target" effect size for the G*Power reference column in Panel A.
        Default 0.4 (as in G.8).
    effect_sizes:
        Effect sizes for the Panel B grid rows.
        Default ``[0.4, 0.5, 0.6]``.
    n_per_cell_values:
        N per cell values for the Panel B grid columns.
        Default ``[30, 50, 100]``.
    title, label:
        LaTeX \\caption and \\label strings.

    Returns
    -------
    str
        Complete LaTeX table environment string (both panels).
    """
    if effect_sizes is None:
        effect_sizes = [0.4, 0.5, 0.6]
    if n_per_cell_values is None:
        n_per_cell_values = [30, 50, 100]

    lines: list[str] = [
        r"\begin{table}[htbp]",
        r"  \centering",
        f"  \\caption{{{title}}}",
        f"  \\label{{{label}}}",
    ]

    # ── Panel A — Design tier summary ─────────────────────────────────────────
    lines += [
        r"  \textbf{Panel A: Design Tiers} \\[4pt]",
        r"  \begin{tabular}{llcccc}",
        r"  \toprule",
        (
            r"  \textbf{Tier} & "
            r"\textbf{Min-det.\ $d$} & "
            r"\textbf{$N$/cell} & "
            r"\textbf{Total runs} & "
            r"\textbf{Est.\ cost} & "
            r"\textbf{Power at $d=0.4$} \\"
        ),
        r"  \midrule",
    ]

    for label_tier, n_cell, min_d_str, gpower_ref in _DESIGN_TIERS:
        if label_tier == "Gold Standard":
            total_runs = _CELLS_PER_DESIGN * n_cell * _GOLD_STANDARD_MULTIPLIER
            tier_note = r"$^\S$"
        else:
            total_runs = _CELLS_PER_DESIGN * n_cell
            tier_note = ""

        cost = total_runs * _COST_PER_RUN_USD
        power_str = (
            f"{gpower_ref:.2f}"
            if gpower_ref is not None
            else "--"
        )
        # Mark underpowered rows
        if gpower_ref is not None and gpower_ref < 0.80:
            power_str += r"$^\dagger$"

        lines.append(
            f"  {label_tier}{tier_note} & {min_d_str} & {n_cell} & "
            f"{total_runs:,} & \\${cost:,.0f} & {power_str} \\\\"
        )

    lines += [
        r"  \bottomrule",
        r"  \end{tabular}",
        r"  \vspace{8pt}",
    ]

    # ── Panel B — Power grid ───────────────────────────────────────────────────
    n_cols_b = len(n_per_cell_values)
    col_headers_b = " & ".join(f"$N={n}$" for n in n_per_cell_values)

    lines += [
        r"  \textbf{Panel B: Achieved Power (normal approximation)} \\[4pt]",
        f"  \\begin{{tabular}}{{l{'c' * n_cols_b}}}",
        r"  \toprule",
        f"  \\textbf{{Effect size ($d$)}} & {col_headers_b} \\\\",
        r"  \midrule",
    ]

    for d_val in effect_sizes:
        powers = [_approx_power(d_val, n) for n in n_per_cell_values]
        power_strs = []
        for p in powers:
            if p >= 0.80:
                power_strs.append(f"\\textbf{{{p:.2f}}}")
            else:
                power_strs.append(f"{p:.2f}")
        lines.append(
            f"  $d = {d_val}$ & " + " & ".join(power_strs) + r" \\"
        )

    lines += [
        r"  \bottomrule",
        r"  \end{tabular}",
    ]

    # ── Footnotes ─────────────────────────────────────────────────────────────
    lines += [
        r"  \smallskip\par\noindent{\footnotesize",
        (
            r"  \textbf{Panel A}: G*Power reference values (two-sample $t$-test,"
            r" $\alpha = 0.05$ two-tailed). "
            r"Total runs = 5 bias types $\times$ 2 variants $\times$ 10 models $\times$ $N$/cell. "
            r"Cost estimate at \$0.15/run. "
            r"$^\dagger$Exploratory: power $<$ 0.80; use confidence intervals rather than $p$-values. "
            r"$^\S$Gold Standard includes 3 prompt versions $\times$ 3 temperature levels."
        ),
        (
            r"  \textbf{Panel B}: Computed using the normal approximation "
            r"$\Phi(\delta\sqrt{n/2} - z_{\alpha/2})$ where $\delta$ is Cohen's $d$ "
            r"and $n$ is the number of observations per group. "
            r"\textbf{Bold} = power $\geq 0.80$."
        ),
        r"  }",
        r"\end{table}",
    ]

    return "\n".join(lines)


def save_power_table(
    output_path: str | Path,
    **kwargs: Any,
) -> Path:
    """Build and write Table A1 to ``<output_path>.tex``.

    Parameters
    ----------
    output_path:
        Destination path without extension.
    **kwargs:
        Forwarded to ``build_power_table``.

    Returns
    -------
    Path
        The written ``.tex`` file path.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    tex_path = output_path.with_suffix(".tex")
    tex_path.write_text(build_power_table(**kwargs), encoding="utf-8")
    return tex_path


