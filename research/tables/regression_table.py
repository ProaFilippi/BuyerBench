"""Table 2 — Regression Results  &  Table 3 — Variance Decomposition.

Table 2 renders the mixed-effects regression output in stargazer-style format:
  coefficient, SE, t-statistic, p-value, significance stars.
Table 3 renders the ANOVA-style variance decomposition:
  source, SS, df, η², % variance explained.
Both functions export LaTeX strings; optional ``save_*`` helpers write .tex files.

Public API
----------
- ``build_regression_table(result, ...)``       — LaTeX str (Table 2).
- ``build_variance_table(decomp, ...)``         — LaTeX str (Table 3).
- ``save_regression_table(result, output_path, ...)`` — writes .tex, returns Path.
- ``save_variance_table(decomp, output_path, ...)``   — writes .tex, returns Path.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Optional


# ── Significance star helpers ─────────────────────────────────────────────────

def _sig_stars(p_value: Optional[float]) -> str:
    """Return significance star string for a p-value.

    Thresholds: ``***`` p<0.001, ``**`` p<0.01, ``*`` p<0.05, ``†`` p<0.10.
    Returns empty string for p ≥ 0.10 or None.
    """
    if p_value is None:
        return ""
    if p_value < 0.001:
        return "***"
    if p_value < 0.01:
        return "**"
    if p_value < 0.05:
        return "*"
    if p_value < 0.10:
        return "\\dagger"
    return ""


def _fmt_coef(value: float) -> str:
    """Format a regression coefficient with consistent decimal places."""
    return f"{value:.4f}"


def _fmt_pval(p: Optional[float]) -> str:
    """Format a p-value for tabular display."""
    if p is None:
        return "--"
    if p < 0.001:
        return "$<$0.001"
    return f"{p:.3f}"


# ── Table 2 — Regression results ─────────────────────────────────────────────

def build_regression_table(
    result: Any,
    *,
    title: str = "Mixed-Effects Regression Results: Bias Susceptibility Index (BSI)",
    label: str = "tab:regression",
    dep_var_label: str = "BSI",
    use_bh_stars: bool = True,
) -> str:
    """Build Table 2: stargazer-style mixed-effects regression output.

    Parameters
    ----------
    result:
        A ``RegressionResult`` dataclass instance from
        ``research.analysis.regression.run_primary_regression``.
        Expected attributes: ``spec_name``, ``formula``, ``n_obs``,
        ``df_residual``, ``r_squared``, ``backend``, ``aic``, ``bic``,
        ``log_likelihood``, ``random_effects_variance``, ``notes``,
        ``warnings``, ``coefficients`` (list of ``RegressionCoefficient``).
    title, label:
        LaTeX \\caption and \\label strings.
    dep_var_label:
        Column header label for the dependent variable.
    use_bh_stars:
        If True, use BH-corrected p-values (``p_value_bh``) for stars when
        available; otherwise fall back to raw ``p_value``.

    Returns
    -------
    str
        Complete LaTeX table environment string.
    """
    coefs = getattr(result, "coefficients", [])
    n_obs = getattr(result, "n_obs", None)
    df_res = getattr(result, "df_residual", None)
    r_sq = getattr(result, "r_squared", None)
    aic = getattr(result, "aic", None)
    bic = getattr(result, "bic", None)
    log_lik = getattr(result, "log_likelihood", None)
    re_var = getattr(result, "random_effects_variance", None)
    backend = getattr(result, "backend", "unknown")
    formula = getattr(result, "formula", "")
    notes_txt = getattr(result, "notes", "")
    warnings_list = getattr(result, "warnings", [])

    lines: list[str] = [
        r"\begin{table}[htbp]",
        r"  \centering",
        f"  \\caption{{{title}}}",
        f"  \\label{{{label}}}",
        r"  \begin{tabular}{lcccc}",
        r"  \toprule",
        (
            f"  \\textbf{{Coefficient}} & "
            f"\\textbf{{Estimate}} & "
            f"\\textbf{{SE}} & "
            f"\\textbf{{$t$-stat}} & "
            f"\\textbf{{$p$-value}} \\\\"
        ),
        r"  \midrule",
    ]

    for coef in coefs:
        name = getattr(coef, "name", "?")
        est = getattr(coef, "estimate", float("nan"))
        se = getattr(coef, "se", float("nan"))
        t_stat = getattr(coef, "t_stat", float("nan"))

        # Choose p-value for stars: BH-corrected if available and requested
        raw_p = getattr(coef, "p_value", None)
        bh_p = getattr(coef, "p_value_bh", None)
        star_p = (bh_p if (use_bh_stars and bh_p is not None) else raw_p)
        display_p = raw_p  # Always show raw p-value in the column

        stars = _sig_stars(star_p)
        bh_flag = (
            "$^{\\dagger}$"
            if (use_bh_stars and bh_p is not None and getattr(coef, "significant_bh", False))
            else ""
        )

        # Format coefficient name: remove C() statsmodels notation
        clean_name = name.replace("C(", "").replace(")", "").replace("[T.", " = ")
        clean_name = clean_name.replace("_", "\\_")

        est_str = _fmt_coef(est)
        if stars:
            est_str += f"$^{{{stars}}}${bh_flag}"

        lines.append(
            f"  {clean_name} & {est_str} & {_fmt_coef(se)} & "
            f"{_fmt_coef(t_stat)} & {_fmt_pval(display_p)} \\\\"
        )

    lines.append(r"  \midrule")

    # ── Model-level statistics ─────────────────────────────────────────────────
    if n_obs is not None:
        lines.append(f"  Observations & \\multicolumn{{4}}{{c}}{{{n_obs:,}}} \\\\")
    if df_res is not None:
        lines.append(f"  Residual df & \\multicolumn{{4}}{{c}}{{{df_res}}} \\\\")
    if r_sq is not None:
        lines.append(f"  $R^2$ & \\multicolumn{{4}}{{c}}{{{r_sq:.4f}}} \\\\")
    if log_lik is not None:
        lines.append(f"  Log likelihood & \\multicolumn{{4}}{{c}}{{{log_lik:.2f}}} \\\\")
    if aic is not None:
        lines.append(f"  AIC & \\multicolumn{{4}}{{c}}{{{aic:.2f}}} \\\\")
    if bic is not None:
        lines.append(f"  BIC & \\multicolumn{{4}}{{c}}{{{bic:.2f}}} \\\\")
    if re_var is not None:
        lines.append(
            f"  Random effects $\\sigma^2$ & \\multicolumn{{4}}{{c}}{{{re_var:.4f}}} \\\\"
        )
    lines.append(
        f"  Backend & \\multicolumn{{4}}{{c}}{{\\texttt{{{backend.replace('_', r'\_')}}}}} \\\\"
    )

    lines.append(r"  \bottomrule")
    lines.append(r"  \end{tabular}")

    # ── Footnote ──────────────────────────────────────────────────────────────
    star_note = (
        r"$^{*}p<0.05$; $^{**}p<0.01$; $^{***}p<0.001$; $^{\dagger}p<0.10$. "
    )
    if use_bh_stars:
        star_note += (
            r"Stars based on BH-corrected $p$-values when available. "
        )
    if formula:
        safe_formula = formula.replace("_", r"\_").replace("~", r"$\sim$")
        star_note += f"Formula: \\texttt{{{safe_formula}}}. "
    if notes_txt:
        star_note += notes_txt
    if warnings_list:
        star_note += " Warnings: " + "; ".join(str(w) for w in warnings_list) + "."

    lines.append(
        f"  \\smallskip\\par\\noindent{{\\footnotesize {star_note}}}"
    )
    lines.append(r"\end{table}")

    return "\n".join(lines)


def save_regression_table(
    result: Any,
    output_path: str | Path,
    **kwargs: Any,
) -> Path:
    """Build and write Table 2 to ``<output_path>.tex``.

    Parameters
    ----------
    result:
        ``RegressionResult`` instance (see ``build_regression_table``).
    output_path:
        Destination path without extension.
    **kwargs:
        Forwarded to ``build_regression_table``.

    Returns
    -------
    Path
        The written ``.tex`` file path.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    tex_path = output_path.with_suffix(".tex")
    tex_path.write_text(build_regression_table(result, **kwargs), encoding="utf-8")
    return tex_path


# ── Table 3 — Variance decomposition ─────────────────────────────────────────

def build_variance_table(
    decomp: Any,
    *,
    title: str = "Variance Decomposition: BSI by Source",
    label: str = "tab:variance",
) -> str:
    """Build Table 3: ANOVA-style variance decomposition table.

    Parameters
    ----------
    decomp:
        A ``VarianceDecompositionResult`` dataclass instance from
        ``research.analysis.regression.run_variance_decomposition``.
        Expected attributes: ``rows`` (list of ``VariancePartition``),
        ``total_ss``, ``n_obs``, ``notes``.
        Each ``VariancePartition`` row has: ``source``, ``ss``, ``df``,
        ``ms``, ``eta_squared``, ``pct_variance``.
    title, label:
        LaTeX \\caption and \\label strings.

    Returns
    -------
    str
        Complete LaTeX table environment string.
    """
    rows = getattr(decomp, "rows", [])
    total_ss = getattr(decomp, "total_ss", None)
    n_obs = getattr(decomp, "n_obs", None)
    notes_txt = getattr(decomp, "notes", "")

    lines: list[str] = [
        r"\begin{table}[htbp]",
        r"  \centering",
        f"  \\caption{{{title}}}",
        f"  \\label{{{label}}}",
        r"  \begin{tabular}{lrrrrc}",
        r"  \toprule",
        (
            r"  \textbf{Source} & "
            r"\textbf{SS} & "
            r"\textbf{df} & "
            r"\textbf{MS} & "
            r"\textbf{$\eta^2$} & "
            r"\textbf{\% Variance} \\"
        ),
        r"  \midrule",
    ]

    for row in rows:
        source = getattr(row, "source", "?")
        ss = getattr(row, "ss", 0.0)
        df_val = getattr(row, "df", 0)
        ms = getattr(row, "ms", 0.0)
        eta_sq = getattr(row, "eta_squared", 0.0)
        pct = getattr(row, "pct_variance", 0.0)
        # Residual row gets a lighter style (no eta² — it's the unexplained variance)
        if source.lower() == "residual":
            lines.append(
                f"  \\textit{{Residual}} & {ss:.4f} & {df_val:,} & "
                f"{ms:.6f} & -- & {pct:.1f}\\% \\\\"
            )
        else:
            lines.append(
                f"  {source} & {ss:.4f} & {df_val} & "
                f"{ms:.6f} & {eta_sq:.4f} & {pct:.1f}\\% \\\\"
            )

    lines.append(r"  \midrule")

    # Totals row
    if rows:
        total_pct = sum(getattr(r, "pct_variance", 0.0) for r in rows)
        total_ss_display = (
            f"{total_ss:.4f}" if total_ss is not None
            else f"{sum(getattr(r, 'ss', 0.0) for r in rows):.4f}"
        )
        lines.append(
            f"  \\textbf{{Total}} & \\textbf{{{total_ss_display}}} & "
            f"-- & -- & -- & {total_pct:.1f}\\% \\\\"
        )

    lines.append(r"  \bottomrule")
    lines.append(r"  \end{tabular}")

    footnote_parts: list[str] = [
        r"SS = sum of squares; df = degrees of freedom; "
        r"MS = mean squares; $\eta^2$ = eta-squared (proportion of explained variance)."
    ]
    if n_obs is not None:
        footnote_parts.append(f"$N = {n_obs:,}$ total observations.")
    if notes_txt:
        footnote_parts.append(notes_txt)

    lines.append(
        f"  \\smallskip\\par\\noindent{{\\footnotesize {' '.join(footnote_parts)}}}"
    )
    lines.append(r"\end{table}")

    return "\n".join(lines)


def save_variance_table(
    decomp: Any,
    output_path: str | Path,
    **kwargs: Any,
) -> Path:
    """Build and write Table 3 to ``<output_path>.tex``.

    Parameters
    ----------
    decomp:
        ``VarianceDecompositionResult`` instance (see ``build_variance_table``).
    output_path:
        Destination path without extension.
    **kwargs:
        Forwarded to ``build_variance_table``.

    Returns
    -------
    Path
        The written ``.tex`` file path.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    tex_path = output_path.with_suffix(".tex")
    tex_path.write_text(build_variance_table(decomp, **kwargs), encoding="utf-8")
    return tex_path
