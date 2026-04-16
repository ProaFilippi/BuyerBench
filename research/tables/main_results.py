"""Table 1 — Main BSI Results.

Renders the primary results table: mean BSI for each (model × bias_type) cell.
Cells with BSI significantly > 0 (BH-corrected) are bolded in LaTeX output.
Exports both .tex and .csv formats.

Public API
----------
- ``build_main_results_table(cell_df, ...)``
  Returns a dict with 'latex' (str) and 'csv' (str) keys.
- ``save_main_results_table(cell_df, output_path, ...)``
  Writes <output_path>.tex and <output_path>.csv; returns dict of Path objects.
"""
from __future__ import annotations

import csv
import io
import math
from pathlib import Path
from typing import Any, Optional

try:
    import pandas as pd
    _PANDAS_AVAILABLE = True
except ImportError:
    _PANDAS_AVAILABLE = False


# ── Display name helpers ──────────────────────────────────────────────────────

_SHORT_NAMES: dict[str, str] = {
    "openrouter-openai-gpt-4o": "GPT-4o",
    "openrouter-anthropic-claude-3.5-sonnet": "Claude 3.5",
    "openrouter-google-gemini-pro-1.5": "Gemini 1.5",
    "openrouter-meta-llama-llama-3.1-405b-instruct": "LLaMA 405B",
    "openrouter-mistralai-mistral-large": "Mistral Lg",
    "openrouter-deepseek-deepseek-chat": "DeepSeek",
    "openrouter-qwen-qwen-2.5-72b-instruct": "Qwen 2.5",
    "openrouter-cohere-command-r-plus": "Command R+",
    "openrouter-mistralai-mixtral-8x22b-instruct": "Mixtral 8x22B",
    "openrouter-01-ai-yi-large": "Yi Large",
    "mock-agent-v1": "Mock Agent",
}

_BIAS_DISPLAY: dict[str, str] = {
    "anchoring": "Anchoring",
    "framing": "Framing",
    "decoy": "Decoy",
    "scarcity": "Scarcity",
    "sunk_cost": "Sunk Cost",
    "default_bias": "Default",
    "loss_aversion": "Loss Aversion",
    "status_quo": "Status Quo",
}


def _short(agent_id: str) -> str:
    return _SHORT_NAMES.get(agent_id, agent_id.split("-")[-1][:12])


def _bias_label(bias: str) -> str:
    return _BIAS_DISPLAY.get(bias, bias.replace("_", " ").title())


# ── Statistics helpers ────────────────────────────────────────────────────────

def _normal_cdf(x: float) -> float:
    """Standard normal CDF using math.erfc (pure Python, no scipy required)."""
    return 0.5 * math.erfc(-x / math.sqrt(2))


def _one_sample_pvalue_gt_zero(mean: float, std: float, n: int) -> float:
    """One-tailed p-value: H0 — BSI = 0, H1 — BSI > 0 (one-sample t-test).

    Returns 1.0 if mean ≤ 0, std is non-positive, or n < 2.
    Uses a normal approximation for df ≥ 30; falls back to importing
    ``_t_pvalue`` from ``research.analysis.regression`` for small samples.
    """
    if mean <= 0 or std <= 0 or n < 2:
        return 1.0
    t_stat = mean / (std / math.sqrt(n))
    df = n - 1
    if df >= 30:
        # Normal approximation is adequate for df ≥ 30
        return 1.0 - _normal_cdf(t_stat)
    # For small df, convert two-tailed t-pvalue to one-tailed
    try:
        from research.analysis.regression import _t_pvalue  # type: ignore[attr-defined]
        two_tailed = _t_pvalue(float(t_stat), int(df))
        return two_tailed / 2 if t_stat > 0 else 1.0 - two_tailed / 2
    except (ImportError, AttributeError):
        return 1.0 - _normal_cdf(t_stat)


# ── Core table builder ────────────────────────────────────────────────────────

def build_main_results_table(
    cell_df: Any,
    *,
    alpha: float = 0.05,
    agent_col: str = "agent_id",
    bias_col: str = "bias_category",
    mean_col: str = "mean_bsi",
    std_col: str = "std_bsi",
    n_col: str = "n_valid_runs",
    p1_scores: Optional[dict[str, float]] = None,
    title: str = "Mean BSI by Model and Bias Type",
    label: str = "tab:main_results",
) -> dict[str, str]:
    """Build the main BSI results table (Table 1).

    Parameters
    ----------
    cell_df:
        One row per (agent_id, bias_category) combination — typically the
        treatment-variant cells from ``CellAggregate``. Must contain at least
        ``agent_col``, ``bias_col``, and ``mean_col``.
    alpha:
        BH-corrected significance threshold. Default 0.05.
    agent_col, bias_col, mean_col, std_col, n_col:
        Column name overrides.
    p1_scores:
        Optional mapping from agent_id → Pillar 1 score. When provided, model
        rows are sorted in descending capability order.
    title, label:
        LaTeX \\caption and \\label strings.

    Returns
    -------
    dict
        ``'latex'`` — booktabs LaTeX table string ready for paper inclusion.
        ``'csv'``   — CSV string with numeric values; ``*`` suffix marks
                      significant cells (BH-corrected).

    Raises
    ------
    ImportError
        If pandas is not installed.
    ValueError
        If ``cell_df`` is empty or required columns are missing.
    """
    if not _PANDAS_AVAILABLE:
        raise ImportError(
            "pandas is required for build_main_results_table. "
            "Install it with: pip install pandas"
        )

    df = pd.DataFrame(cell_df) if not isinstance(cell_df, pd.DataFrame) else cell_df.copy()

    if df.empty:
        raise ValueError("cell_df is empty — cannot build table.")
    for col in (agent_col, bias_col, mean_col):
        if col not in df.columns:
            raise ValueError(f"Required column '{col}' not found in cell_df.")

    # Ensure optional columns exist with sensible defaults
    if std_col not in df.columns:
        df[std_col] = float("nan")
    if n_col not in df.columns:
        df[n_col] = 1

    # ── Compute raw p-values for each row ─────────────────────────────────────
    pvalues: list[float] = []
    for _, row in df.iterrows():
        n_val = int(row[n_col]) if pd.notna(row[n_col]) else 1
        std_val = float(row[std_col]) if pd.notna(row[std_col]) else 0.0
        p = _one_sample_pvalue_gt_zero(float(row[mean_col]), std_val, n_val)
        pvalues.append(p)
    df = df.copy()
    df["_p_raw"] = pvalues

    # ── BH multiple comparison correction ─────────────────────────────────────
    try:
        from research.analysis.regression import apply_bh_correction
        _, sig_flags = apply_bh_correction(list(pvalues), alpha=alpha)
    except ImportError:
        sig_flags = [p < alpha for p in pvalues]
    df["_significant"] = sig_flags

    # ── Sort model rows by P1 score (descending) or display name ──────────────
    agents = list(df[agent_col].unique())
    if p1_scores:
        agents = sorted(agents, key=lambda a: p1_scores.get(a, 0.0), reverse=True)
    else:
        agents = sorted(agents, key=_short)
    bias_types = sorted(df[bias_col].unique().tolist())

    # ── Cell formatting helpers ───────────────────────────────────────────────
    def _latex_cell(mean: float, std: float, sig: bool) -> str:
        if not math.isnan(std) and std > 0:
            core = f"{mean:.2f} {{\\scriptsize $\\pm$ {std:.2f}}}"
        else:
            core = f"{mean:.2f}"
        return f"\\textbf{{{core}}}" if sig else core

    def _csv_cell(mean: float, sig: bool) -> str:
        return f"{mean:.4f}{'*' if sig else ''}"

    # Index df for fast lookup
    idx: dict[tuple[str, str], tuple[float, float, bool]] = {}
    for _, row in df.iterrows():
        key = (str(row[agent_col]), str(row[bias_col]))
        idx[key] = (
            float(row[mean_col]),
            float(row[std_col]) if pd.notna(row[std_col]) else float("nan"),
            bool(row["_significant"]),
        )

    # ── Build LaTeX table ─────────────────────────────────────────────────────
    col_headers_tex = [f"\\textbf{{{_bias_label(b)}}}" for b in bias_types]
    n_cols = len(bias_types)
    col_spec = "l" + "c" * n_cols

    lines: list[str] = [
        r"\begin{table}[htbp]",
        r"  \centering",
        f"  \\caption{{{title}}}",
        f"  \\label{{{label}}}",
        f"  \\begin{{tabular}}{{{col_spec}}}",
        r"  \toprule",
        "  \\textbf{Model} & " + " & ".join(col_headers_tex) + r" \\",
        r"  \midrule",
    ]
    for agent in agents:
        cells = []
        for bias in bias_types:
            if (agent, bias) in idx:
                mean_v, std_v, sig = idx[(agent, bias)]
                cells.append(_latex_cell(mean_v, std_v, sig))
            else:
                cells.append("--")
        lines.append(f"  {_short(agent)} & " + " & ".join(cells) + r" \\")
    lines += [
        r"  \bottomrule",
        r"  \end{tabular}",
        (
            r"  \smallskip\par\noindent{\footnotesize "
            r"\textbf{Bold}: BSI significantly $>$ 0 (one-sample $t$-test, "
            r"Benjamini--Hochberg corrected, $\alpha = 0.05$). "
            r"Values: mean $\pm$ SD.}"
        ),
        r"\end{table}",
    ]
    latex_str = "\n".join(lines)

    # ── Build CSV output ──────────────────────────────────────────────────────
    csv_buf = io.StringIO()
    writer = csv.writer(csv_buf)
    writer.writerow(["model_id", "model_short"] + bias_types)
    for agent in agents:
        row_data: list[str] = [agent, _short(agent)]
        for bias in bias_types:
            if (agent, bias) in idx:
                mean_v, _, sig = idx[(agent, bias)]
                row_data.append(_csv_cell(mean_v, sig))
            else:
                row_data.append("")
        writer.writerow(row_data)
    csv_str = csv_buf.getvalue()

    return {"latex": latex_str, "csv": csv_str}


def save_main_results_table(
    cell_df: Any,
    output_path: str | Path,
    **kwargs: Any,
) -> dict[str, Path]:
    """Build and save Table 1 to ``<output_path>.tex`` and ``<output_path>.csv``.

    Parameters
    ----------
    cell_df:
        Same as ``build_main_results_table``.
    output_path:
        Destination path without extension (e.g. ``results/experiments/e1/tables/table1``).
    **kwargs:
        Forwarded to ``build_main_results_table``.

    Returns
    -------
    dict with ``'tex'`` and ``'csv'`` Path objects.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    tables = build_main_results_table(cell_df, **kwargs)
    tex_path = output_path.with_suffix(".tex")
    csv_path = output_path.with_suffix(".csv")
    tex_path.write_text(tables["latex"], encoding="utf-8")
    csv_path.write_text(tables["csv"], encoding="utf-8")
    return {"tex": tex_path, "csv": csv_path}
