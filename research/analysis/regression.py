"""Mixed-effects regression wrappers for Pillar 2 research analysis (L.6).

Operates on **pandas DataFrames** of raw run records (``runs.jsonl`` loaded via
``pd.read_json``), rather than the pre-aggregated ``CellAggregate`` objects used
by the production ``results/stats_pipeline.py`` layer.

Function signatures
-------------------
- ``run_primary_regression(df)``          — BSI ~ BiasType + Model + Treatment +
                                             BiasType×Model + (1|run) via statsmodels
- ``run_capability_regression(df, p1)``   — OLS: mean_BSI ~ P1Score (descriptive)
- ``run_variance_decomposition(df)``       — ANOVA-style SS partition
- ``apply_bh_correction(pvalues, alpha)`` — Benjamini-Hochberg FDR

Optional dependencies
---------------------
- ``statsmodels`` — required for ``run_primary_regression``; install with
  ``pip install statsmodels``.  When absent the function raises ``ImportError``
  with an actionable message.
- ``rpy2`` — required for the ``lme4`` robustness check in
  ``run_primary_regression(use_r=True)``; gracefully skipped when absent.

Both packages are listed as optional extras in ``pyproject.toml`` under
``[project.optional-dependencies] research = [...]``.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Optional

# ── pandas is a hard requirement for this module (data format is DataFrame) ──

try:
    import pandas as pd
    _PANDAS_AVAILABLE = True
except ImportError:  # pragma: no cover
    _PANDAS_AVAILABLE = False

# ── statsmodels is optional ──────────────────────────────────────────────────

try:
    import statsmodels.formula.api as smf
    import statsmodels.api as sm
    _STATSMODELS_AVAILABLE = True
except ImportError:
    _STATSMODELS_AVAILABLE = False

# ── rpy2 is optional ─────────────────────────────────────────────────────────

try:
    import rpy2.robjects as ro
    import rpy2.robjects.packages as rpackages
    from rpy2.robjects import pandas2ri
    _RPY2_AVAILABLE = True
except Exception:
    _RPY2_AVAILABLE = False


# ─────────────────────────────────────────────────────────────────────────────
# DATA CLASSES
# ─────────────────────────────────────────────────────────────────────────────


@dataclass
class RegressionCoefficient:
    """One row of a regression table."""

    name: str
    estimate: float
    se: float
    t_stat: float
    p_value: float
    ci_lower_95: float
    ci_upper_95: float
    p_value_bh: Optional[float] = None
    significant_bh: bool = False


@dataclass
class RegressionResult:
    """Result of one regression analysis."""

    spec_name: str
    """Human-readable specification name, e.g. 'PrimaryMixedLM'."""

    formula: str
    """R-style formula string (informational)."""

    n_obs: int
    df_residual: Optional[int]
    r_squared: Optional[float]
    """Pseudo R² (marginal) for mixed models; standard R² for OLS."""

    backend: str
    """'statsmodels_mixedlm', 'statsmodels_ols', 'rpy2_lme4', or 'fallback_wls'."""

    coefficients: list[RegressionCoefficient] = field(default_factory=list)
    aic: Optional[float] = None
    bic: Optional[float] = None
    log_likelihood: Optional[float] = None
    random_effects_variance: Optional[float] = None
    """Estimated variance of the random intercept (1|run_id)."""

    notes: str = ""
    warnings: list[str] = field(default_factory=list)


@dataclass
class VariancePartition:
    """ANOVA-style SS partition for BSI variance."""

    source: str
    ss: float
    df: int
    ms: float
    eta_squared: float
    pct_variance: float


@dataclass
class VarianceDecompositionResult:
    """Full variance decomposition output."""

    rows: list[VariancePartition] = field(default_factory=list)
    total_ss: float = 0.0
    n_obs: int = 0
    notes: str = ""

    def eta_squared(self, source: str) -> Optional[float]:
        for row in self.rows:
            if row.source == source:
                return row.eta_squared
        return None


# ─────────────────────────────────────────────────────────────────────────────
# INTERNAL HELPERS
# ─────────────────────────────────────────────────────────────────────────────

_CONTROL_VARIANTS: frozenset[str] = frozenset({"BASELINE", "FRAMING_GAIN"})
_WARP_VARIANTS: frozenset[str] = frozenset({"WARP_AB", "WARP_BC", "WARP_AC"})


def _is_treatment(variant: Optional[str]) -> bool:
    """Return True if *variant* is the manipulation arm."""
    if variant is None:
        return False
    return variant not in _CONTROL_VARIANTS and variant not in _WARP_VARIANTS


# ── Pure-Python t-distribution statistics (no scipy needed) ──────────────────

_T95_BY_DF: dict[int, float] = {
    1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571,
    6: 2.447, 7: 2.365, 8: 2.306, 9: 2.262, 10: 2.228,
    11: 2.201, 12: 2.179, 13: 2.160, 14: 2.145, 15: 2.131,
    16: 2.120, 17: 2.110, 18: 2.101, 19: 2.093, 20: 2.086,
    21: 2.080, 22: 2.074, 23: 2.069, 24: 2.064, 25: 2.060,
    26: 2.056, 27: 2.052, 28: 2.048, 29: 2.045,
}


def _t_critical_95(df: float) -> float:
    if df >= 30:
        return 1.960
    return _T95_BY_DF.get(max(1, int(df)), 2.000)


def _betacf(a: float, b: float, x: float, max_iter: int = 200) -> float:
    TINY = 1e-300
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c, d = 1.0, 1.0 - qab * x / qap
    if abs(d) < TINY:
        d = TINY
    d = 1.0 / d
    h = d
    for m in range(1, max_iter + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        c = 1.0 + aa / c
        if abs(c) < TINY:
            c = TINY
        d = 1.0 + aa * d
        if abs(d) < TINY:
            d = TINY
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        c = 1.0 + aa / c
        if abs(c) < TINY:
            c = TINY
        d = 1.0 + aa * d
        if abs(d) < TINY:
            d = TINY
        d = 1.0 / d
        h *= d * c
        if abs(d * c - 1.0) < 3e-7:
            break
    return h


def _betainc(a: float, b: float, x: float) -> float:
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    if x > (a + 1.0) / (a + b + 2.0):
        return 1.0 - _betainc(b, a, 1.0 - x)
    lbeta = math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)
    return (
        math.exp(a * math.log(x) + b * math.log(1.0 - x) - lbeta)
        * _betacf(a, b, x) / a
    )


def _t_pvalue(t: float, df: float) -> float:
    if df <= 0:
        return 1.0
    return _betainc(df / 2.0, 0.5, df / (df + t ** 2))


# ── Fallback WLS (no external deps) ──────────────────────────────────────────

def _dot(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def _transpose(A: list[list[float]]) -> list[list[float]]:
    if not A or not A[0]:
        return []
    return [[A[i][j] for i in range(len(A))] for j in range(len(A[0]))]


def _solve_linear(A: list[list[float]], b: list[float]) -> list[float]:
    n = len(b)
    M = [A[i][:] + [b[i]] for i in range(n)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(M[r][col]))
        M[col], M[pivot] = M[pivot], M[col]
        if abs(M[col][col]) < 1e-12:
            raise ValueError(
                f"Singular design matrix at column {col} (collinear predictors "
                "or under-identified model)."
            )
        for row in range(col + 1, n):
            f = M[row][col] / M[col][col]
            M[row] = [M[row][j] - f * M[col][j] for j in range(n + 1)]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (M[i][n] - sum(M[i][j] * x[j] for j in range(i + 1, n))) / M[i][i]
    return x


def _wls_fallback(
    X: list[list[float]],
    y: list[float],
    weights: list[float],
    col_names: list[str],
    spec_name: str,
) -> RegressionResult:
    """Pure-Python WLS engine used when statsmodels is unavailable."""
    n, k = len(y), len(X[0])
    A = [[0.0] * k for _ in range(k)]
    c = [0.0] * k
    for i in range(n):
        w = weights[i]
        for j in range(k):
            c[j] += w * X[i][j] * y[i]
            for l in range(k):
                A[j][l] += w * X[i][j] * X[i][l]
    beta = _solve_linear(A, c)
    w_sum = sum(weights)
    y_mean = sum(weights[i] * y[i] for i in range(n)) / w_sum
    residuals = [y[i] - sum(X[i][j] * beta[j] for j in range(k)) for i in range(n)]
    ss_res = sum(weights[i] * residuals[i] ** 2 for i in range(n))
    ss_tot = sum(weights[i] * (y[i] - y_mean) ** 2 for i in range(n))
    r2 = max(0.0, 1.0 - ss_res / ss_tot) if ss_tot > 1e-12 else 0.0
    sigma2 = ss_res / max(1, n - k)
    df_resid = n - k
    t_crit = _t_critical_95(df_resid)
    coefficients = []
    for j in range(k):
        e_j = [1.0 if l == j else 0.0 for l in range(k)]
        inv_col = _solve_linear(A, e_j)
        se = math.sqrt(max(0.0, sigma2 * inv_col[j]))
        t = beta[j] / se if se > 1e-12 else 0.0
        p = _t_pvalue(t, df_resid)
        margin = t_crit * se
        coefficients.append(
            RegressionCoefficient(
                name=col_names[j],
                estimate=round(beta[j], 6),
                se=round(se, 6),
                t_stat=round(t, 4),
                p_value=round(p, 6),
                ci_lower_95=round(beta[j] - margin, 6),
                ci_upper_95=round(beta[j] + margin, 6),
            )
        )
    return RegressionResult(
        spec_name=spec_name,
        formula="fallback WLS (no statsmodels)",
        n_obs=n,
        df_residual=df_resid,
        r_squared=round(r2, 6),
        backend="fallback_wls",
        coefficients=coefficients,
        warnings=["statsmodels not installed; used pure-Python WLS fallback."],
    )


# ─────────────────────────────────────────────────────────────────────────────
# PUBLIC API
# ─────────────────────────────────────────────────────────────────────────────


def run_primary_regression(
    df: Any,
    *,
    bsi_col: str = "bsi",
    bias_col: str = "bias_category",
    model_col: str = "agent_id",
    variant_col: str = "variant",
    run_id_col: str = "run_id",
    use_r: bool = False,
) -> RegressionResult:
    """Primary mixed-effects regression: BSI ~ BiasType + Model + Treatment +
    BiasType×Model + (1|run_id).

    Specification (G.2 extended)::

        BSI_ij = α + β_t·Treatment + Σ β_b·BiasType_b + Σ β_m·Model_m
                   + Σ β_bm·BiasType_b×Model_m + u_i + ε_ij

    where ``u_i ~ N(0, σ²_u)`` is a random intercept per ``run_id``,
    absorbing within-cell repetition variance.

    Args:
        df: pandas DataFrame of run-level records (``runs.jsonl`` rows).
            Must contain columns named by *bsi_col*, *bias_col*, *model_col*,
            *variant_col*, and *run_id_col*.
        bsi_col: Column name for the BSI outcome (0–1).
        bias_col: Column name for the bias category (categorical).
        model_col: Column name for the model / agent ID (categorical).
        variant_col: Column name for the variant name (determines Treatment flag).
        run_id_col: Column name used as the grouping variable for random effects.
        use_r: If ``True`` and ``rpy2`` is available, re-fit using ``lme4::lmer``
            as a robustness check.  When ``rpy2`` is absent, a warning is added
            and the statsmodels result is returned.

    Returns:
        :class:`RegressionResult` with coefficients and metadata.

    Raises:
        ImportError: When neither ``statsmodels`` nor the fallback WLS can fit
            the model (e.g., singular matrix).

    Notes:
        - WARP variants (``WARP_AB``, ``WARP_BC``, ``WARP_AC``) are dropped
          before fitting.
        - Reference categories: the alphabetically first bias type and model.
        - With ``n_models × n_biases`` interaction terms the design matrix can
          become large; the statsmodels path handles this via pandas Categoricals
          and formula strings.
    """
    if not _PANDAS_AVAILABLE:
        raise ImportError(
            "pandas is required for research/analysis/regression.py.  "
            "Install with: pip install pandas"
        )

    # ── Validate input ────────────────────────────────────────────────────────
    for col in (bsi_col, bias_col, model_col, variant_col, run_id_col):
        if col not in df.columns:
            raise ValueError(f"Column '{col}' not found in DataFrame.")

    # Drop WARP variants and rows with missing values
    mask = (
        df[variant_col].notna()
        & ~df[variant_col].isin(_WARP_VARIANTS)
        & df[bsi_col].notna()
        & df[bias_col].notna()
        & df[model_col].notna()
    )
    clean = df[mask].copy()

    if len(clean) == 0:
        raise ValueError("No rows remaining after filtering WARP variants and NA values.")

    # ── Add Treatment dummy ───────────────────────────────────────────────────
    clean["_treatment"] = clean[variant_col].apply(_is_treatment).astype(float)

    n_models = clean[model_col].nunique()
    n_biases = clean[bias_col].nunique()

    # ── Fit via statsmodels if available ─────────────────────────────────────
    if _STATSMODELS_AVAILABLE:
        formula = (
            f"{bsi_col} ~ _treatment + C({bias_col}) + C({model_col}) "
            f"+ C({bias_col}):C({model_col})"
        )
        try:
            model = smf.mixedlm(
                formula,
                clean,
                groups=clean[run_id_col],
            )
            fit = model.fit(reml=True, method="lbfgs")

            coefficients: list[RegressionCoefficient] = []
            for name in fit.params.index:
                est = float(fit.params[name])
                se = float(fit.bse[name]) if name in fit.bse.index else 0.0
                t = float(fit.tvalues[name]) if name in fit.tvalues.index else 0.0
                p = float(fit.pvalues[name]) if name in fit.pvalues.index else 1.0
                ci = fit.conf_int()
                lo = float(ci.loc[name, 0]) if name in ci.index else est
                hi = float(ci.loc[name, 1]) if name in ci.index else est
                coefficients.append(
                    RegressionCoefficient(
                        name=name,
                        estimate=round(est, 6),
                        se=round(se, 6),
                        t_stat=round(t, 4),
                        p_value=round(p, 6),
                        ci_lower_95=round(lo, 6),
                        ci_upper_95=round(hi, 6),
                    )
                )

            re_var = float(fit.cov_re.iloc[0, 0]) if hasattr(fit, "cov_re") and fit.cov_re is not None else None

            result = RegressionResult(
                spec_name="PrimaryMixedLM",
                formula=formula,
                n_obs=int(fit.nobs),
                df_residual=None,  # mixed models don't have a single df_residual
                r_squared=None,    # marginal R² requires pingouin/statsmodels extension
                backend="statsmodels_mixedlm",
                coefficients=coefficients,
                aic=round(float(fit.aic), 4) if hasattr(fit, "aic") else None,
                bic=round(float(fit.bic), 4) if hasattr(fit, "bic") else None,
                log_likelihood=round(float(fit.llf), 4) if hasattr(fit, "llf") else None,
                random_effects_variance=round(re_var, 6) if re_var is not None else None,
                notes=(
                    f"Mixed-effects: BSI ~ Treatment + BiasType + Model + "
                    f"BiasType×Model + (1|run_id).  N={len(clean)} runs, "
                    f"{n_models} models, {n_biases} bias types.  "
                    "REML fit via L-BFGS (statsmodels MixedLM)."
                ),
            )

            # ── Optional R/lme4 robustness check ─────────────────────────────
            if use_r:
                result = _run_lme4_robustness(clean, result, bsi_col, bias_col, model_col, run_id_col)

            return result

        except Exception as exc:
            # Fall through to fallback WLS
            warn = f"statsmodels MixedLM failed ({exc}); falling back to WLS."
            return _primary_fallback_wls(clean, bsi_col, bias_col, model_col, warn)

    # ── Fallback WLS (no statsmodels) ─────────────────────────────────────────
    return _primary_fallback_wls(
        clean, bsi_col, bias_col, model_col,
        "statsmodels not installed; interaction terms omitted in WLS fallback.",
    )


def _primary_fallback_wls(
    clean: Any,
    bsi_col: str,
    bias_col: str,
    model_col: str,
    extra_warning: str,
) -> RegressionResult:
    """Build a WLS design matrix (no interactions) and fit via pure Python."""
    biases = sorted(clean[bias_col].unique())
    models = sorted(clean[model_col].unique())
    ref_bias, ref_model = biases[0], models[0]

    col_names = (
        ["Intercept", "Treatment"]
        + [f"BiasType_{b}" for b in biases if b != ref_bias]
        + [f"Model_{m}" for m in models if m != ref_model]
    )

    X: list[list[float]] = []
    y: list[float] = []
    weights: list[float] = []

    for _, row in clean.iterrows():
        xrow = [1.0, float(row["_treatment"])]
        for b in biases:
            if b != ref_bias:
                xrow.append(1.0 if row[bias_col] == b else 0.0)
        for m in models:
            if m != ref_model:
                xrow.append(1.0 if row[model_col] == m else 0.0)
        X.append(xrow)
        y.append(float(row[bsi_col]))
        weights.append(1.0)

    if len(X) <= len(col_names):
        raise ValueError("Under-identified: more parameters than observations.")

    result = _wls_fallback(X, y, weights, col_names, "PrimaryMixedLM_WLS")
    result.warnings.append(extra_warning)
    return result


def _run_lme4_robustness(
    clean: Any,
    statsmodels_result: RegressionResult,
    bsi_col: str,
    bias_col: str,
    model_col: str,
    run_id_col: str,
) -> RegressionResult:
    """Re-fit the primary model using R's ``lme4::lmer`` and annotate the result.

    When ``rpy2`` is unavailable or the R fit fails, the original
    *statsmodels_result* is returned with a warning appended.
    """
    if not _RPY2_AVAILABLE:
        statsmodels_result.warnings.append(
            "rpy2 not installed; lme4 robustness check skipped.  "
            "Install with: pip install rpy2"
        )
        return statsmodels_result

    try:
        pandas2ri.activate()
        lme4 = rpackages.importr("lme4")
        lmerTest = rpackages.importr("lmerTest")  # noqa: F841 — loads to get p-values

        r_df = pandas2ri.py2rpy(clean)
        formula_r = (
            f"{bsi_col} ~ _treatment + {bias_col} * {model_col} "
            f"+ (1 | {run_id_col})"
        )
        fit_r = lmerTest.lmer(formula_r, data=r_df, REML=True)
        summary_r = ro.r["summary"](fit_r)
        coef_table = summary_r.rx2("coefficients")
        # Annotate statsmodels result with R AIC/BIC for comparison
        aic_r = float(ro.r["AIC"](fit_r)[0])
        bic_r = float(ro.r["BIC"](fit_r)[0])
        statsmodels_result.notes += (
            f"  lme4 robustness: AIC={aic_r:.2f}, BIC={bic_r:.2f} "
            f"(statsmodels AIC={statsmodels_result.aic})."
        )
        statsmodels_result.warnings.append(
            f"lme4 robustness check completed.  "
            f"AIC difference (lme4 − statsmodels): {aic_r - (statsmodels_result.aic or 0):.2f}."
        )
    except Exception as exc:
        statsmodels_result.warnings.append(
            f"lme4 robustness check failed ({exc}); statsmodels result unchanged."
        )
    finally:
        try:
            pandas2ri.deactivate()
        except Exception:
            pass

    return statsmodels_result


def run_capability_regression(
    df: Any,
    p1_scores: dict[str, float],
    *,
    bsi_col: str = "bsi",
    model_col: str = "agent_id",
    bias_col: str = "bias_category",
) -> Optional[RegressionResult]:
    """OLS: mean_BSI_m ~ P1Score_m (H2 capability hypothesis, G.1 Δ_capability).

    Computes each model's mean BSI across all bias types, then regresses
    on the provided Pillar 1 capability scores.  With N = 10 models this is
    treated as **descriptive only** — p-values are shown but should not be
    interpreted as inferential evidence.

    Args:
        df: pandas DataFrame of run-level records.
        p1_scores: Mapping ``{agent_id: P1_score}`` from a Pillar 1 experiment.
        bsi_col: Column name for BSI outcome.
        model_col: Column name for the model / agent ID.
        bias_col: Column name for bias category (used to filter P2 rows only).

    Returns:
        :class:`RegressionResult`, or ``None`` if fewer than 3 models have
        both P2 data and P1 scores.
    """
    if not _PANDAS_AVAILABLE:
        raise ImportError("pandas is required.")

    clean = df[df[bsi_col].notna() & df[bias_col].notna()].copy()

    # Compute per-model mean BSI
    model_means = clean.groupby(model_col)[bsi_col].mean().to_dict()
    common = sorted(a for a in model_means if a in p1_scores)

    if len(common) < 3:
        return None

    x_vals = [p1_scores[a] for a in common]
    y_vals = [model_means[a] for a in common]

    if _STATSMODELS_AVAILABLE:
        try:
            ols_df = pd.DataFrame({"mean_bsi": y_vals, "P1Score": x_vals})
            fit = smf.ols("mean_bsi ~ P1Score", data=ols_df).fit()
            coefficients = []
            for name in fit.params.index:
                est = float(fit.params[name])
                se = float(fit.bse[name])
                t = float(fit.tvalues[name])
                p = float(fit.pvalues[name])
                lo, hi = fit.conf_int().loc[name]
                coefficients.append(
                    RegressionCoefficient(
                        name=name,
                        estimate=round(est, 6),
                        se=round(se, 6),
                        t_stat=round(t, 4),
                        p_value=round(p, 6),
                        ci_lower_95=round(float(lo), 6),
                        ci_upper_95=round(float(hi), 6),
                    )
                )
            return RegressionResult(
                spec_name="H2_Capability",
                formula="mean_bsi ~ P1Score",
                n_obs=len(common),
                df_residual=int(fit.df_resid),
                r_squared=round(float(fit.rsquared), 6),
                backend="statsmodels_ols",
                coefficients=coefficients,
                notes=(
                    f"N = {len(common)} models.  Descriptive only (G.2 caveat): "
                    "do not interpret p-values as inferential evidence.  "
                    "Report as 'suggestive pattern' with wide CIs."
                ),
            )
        except Exception as exc:
            # Fall through to pure-Python fallback
            pass

    # Fallback pure-Python OLS
    X = [[1.0, x] for x in x_vals]
    result = _wls_fallback(X, y_vals, [1.0] * len(common), ["Intercept", "P1Score"], "H2_Capability")
    result.formula = "mean_bsi ~ P1Score"
    result.notes = (
        f"N = {len(common)} models.  Descriptive only (G.2 caveat).  "
        "statsmodels not available; used pure-Python OLS."
    )
    return result


def run_variance_decomposition(
    df: Any,
    *,
    bsi_col: str = "bsi",
    bias_col: str = "bias_category",
    model_col: str = "agent_id",
    variant_col: str = "variant",
    temperature_col: Optional[str] = "temperature",
) -> Optional[VarianceDecompositionResult]:
    """ANOVA-style SS partition: Model + BiasType + Treatment + Temperature + Residual.

    Extends the production ``results/stats_pipeline.py`` implementation by
    optionally partitioning variance attributable to the sampling *temperature*
    factor (G.2 — robustness check).

    Args:
        df: pandas DataFrame of run-level records.
        bsi_col: Column name for BSI outcome.
        bias_col: Column name for bias category.
        model_col: Column name for the model / agent ID.
        variant_col: Column name for the variant name.
        temperature_col: Column name for sampling temperature, or ``None`` to
            skip temperature partitioning.

    Returns:
        :class:`VarianceDecompositionResult`, or ``None`` if fewer than 4
        eligible rows remain after filtering.
    """
    if not _PANDAS_AVAILABLE:
        raise ImportError("pandas is required.")

    mask = (
        df[bsi_col].notna()
        & df[bias_col].notna()
        & df[model_col].notna()
        & ~df[variant_col].isin(_WARP_VARIANTS)
    )
    clean = df[mask].copy()
    n = len(clean)
    if n < 4:
        return None

    bsi = clean[bsi_col].astype(float).values
    grand_mean = float(bsi.mean())
    ss_total = float(((bsi - grand_mean) ** 2).sum())
    if ss_total < 1e-12:
        return None

    def _between_ss(group_key: str) -> float:
        return float(
            clean.groupby(group_key)[bsi_col].apply(
                lambda g: len(g) * (float(g.mean()) - grand_mean) ** 2
            ).sum()
        )

    n_models = clean[model_col].nunique()
    n_biases = clean[bias_col].nunique()
    clean["_treatment"] = clean[variant_col].apply(_is_treatment)

    ss_model = _between_ss(model_col)
    ss_bias = _between_ss(bias_col)
    ss_treat = float(
        clean.groupby("_treatment")[bsi_col].apply(
            lambda g: len(g) * (float(g.mean()) - grand_mean) ** 2
        ).sum()
    )

    ss_temp = 0.0
    df_temp = 0
    if temperature_col and temperature_col in clean.columns:
        n_temps = clean[temperature_col].nunique()
        if n_temps > 1:
            ss_temp = _between_ss(temperature_col)
            df_temp = n_temps - 1

    ss_residual = max(0.0, ss_total - ss_model - ss_bias - ss_treat - ss_temp)

    df_model = n_models - 1
    df_bias = n_biases - 1
    df_treat = 1
    df_residual = max(1, n - df_model - df_bias - df_treat - df_temp - 1)

    def _row(source: str, ss: float, df_: int) -> VariancePartition:
        ms = ss / max(1, df_)
        eta2 = ss / ss_total
        return VariancePartition(
            source=source,
            ss=round(ss, 6),
            df=df_,
            ms=round(ms, 6),
            eta_squared=round(eta2, 6),
            pct_variance=round(eta2 * 100.0, 2),
        )

    rows: list[VariancePartition] = [
        _row("Model", ss_model, df_model),
        _row("BiasType", ss_bias, df_bias),
        _row("Treatment", ss_treat, df_treat),
    ]
    if df_temp > 0:
        rows.append(_row("Temperature", ss_temp, df_temp))
    rows.append(_row("Residual", ss_residual, df_residual))

    return VarianceDecompositionResult(
        rows=rows,
        total_ss=round(ss_total, 6),
        n_obs=n,
        notes=(
            "Run-level (unweighted) SS.  η² = SS / SS_total.  "
            "η²_Residual > 0.70 → most BSI variance is within-cell stochastic noise (G.2).  "
            "Temperature factor included when ≥ 2 temperature levels present."
        ),
    )


def apply_bh_correction(
    pvalues: list[float],
    alpha: float = 0.05,
) -> tuple[list[float], list[bool]]:
    """Benjamini-Hochberg FDR correction.

    A thin wrapper around the same algorithm used in ``results/stats_pipeline.py``,
    exposed here for direct use in research scripts.

    Args:
        pvalues: List of raw p-values in any order.
        alpha: FDR threshold (default 0.05).

    Returns:
        ``(adjusted_pvalues, rejected)`` in the *original* input order.
        ``adjusted_pvalues[i] < alpha`` iff ``rejected[i]`` is ``True``.

    Algorithm
    ---------
    Benjamini & Hochberg (1995) step-up procedure with step-down monotonicity
    enforcement so adjusted values can be directly compared against *alpha*::

        p_adj[k] = min(1, p[k] × n / k)   (sorted ascending, rank k from 1)
        p_adj = cummin(p_adj)              (step-down: enforce monotone decrease)
    """
    n = len(pvalues)
    if n == 0:
        return [], []

    order = sorted(range(n), key=lambda i: pvalues[i])
    adj_sorted = [min(1.0, pvalues[order[k]] * n / (k + 1)) for k in range(n)]
    for k in range(n - 2, -1, -1):
        adj_sorted[k] = min(adj_sorted[k], adj_sorted[k + 1])

    result = [0.0] * n
    for k, orig_idx in enumerate(order):
        result[orig_idx] = adj_sorted[k]

    rejected = [p < alpha for p in result]
    return result, rejected
