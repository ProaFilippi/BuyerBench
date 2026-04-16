"""Statistical analysis pipeline for BuyerBench Pillar 2 (UPGRADE-14).

Implements the regression specifications from Section G of the econometric
strategy document.  All analyses operate on a :class:`CellAggregateReport`
produced by UPGRADE-5 (``results/aggregate_cells.py``).

No external dependencies — pure Python stdlib only.

CROSS-MODEL REGRESSION (REV-6)
-------------------------------
BuyerBench evaluates N=10 models.  OLS regression with N=10 observational
units (models) produces standard errors that span the full coefficient
magnitude — reported p-values are unreliable, confidence intervals are
enormous, and no inferential claim is supportable.  This is a fundamental
statistical constraint, not a software limitation.

Accordingly:

  * **H2 capability regression** (``compute_h2_capability``) is the only
    cross-model OLS analysis in this pipeline.  Its results carry
    ``cross_model_descriptive_only=True`` on the :class:`OLSResult` object.
    All coefficients have ``significant_05`` forced to ``False`` — the
    p-value field is retained for internal computation only and must never
    be used to claim statistical significance across models.

  * **All other analyses** (Level 1 WLS, H7, session order) operate
    *within* or *across cells* — they are inferential analyses with
    adequate N and do not set ``cross_model_descriptive_only``.

  * **Report renderers** must check ``OLSResult.cross_model_descriptive_only``
    and suppress p-value columns / significance stars when displaying H2.
    Display the scatter as a descriptive figure only; no asterisks, no
    inferential language.

Claims about the H2 capability scatter MUST be stated as:
  "Descriptive pattern across N=10 models; no inferential claim."

Claims MUST NOT be stated as:
  "Higher Pillar 1 capability is significantly associated with lower BSI
   (β = ..., p < 0.05)" — that framing requires far larger N at the model
   level and is not valid here.

Typical usage::

    from results.aggregate_cells import aggregate_cells_from_dir
    from results.stats_pipeline import run_stats_pipeline, write_stats_pipeline_report

    cell_report = aggregate_cells_from_dir("results/my-experiment/pillar2")
    stats = run_stats_pipeline(cell_report)
    write_stats_pipeline_report(stats, "results/my-experiment")

Implemented analyses
--------------------
- **Level 1 WLS** (G.2): BSI ~ Treatment + BiasType + Model using cell-level
  weighted least squares (weights = n_valid_runs).  OLS and clustered-by-model
  standard errors both reported.
- **Variance decomposition** (G.2): ANOVA-style SS partition into Model,
  BiasType, Treatment, and Residual components with η² effect sizes.
- **Treatment-effect tests** (G.1 τ_bias): Per-(bias_category × agent_id)
  Welch t-tests with BH-FDR correction at q = 0.05.
- **H7 noise-bias correlation** (G.1 σ²_stoch): std_bsi ~ mean_bsi OLS across
  all cells — tests whether biased decisions are noisier.
- **H2 capability regression** (G.1 Δ_capability): mean_BSI_m ~ P1Score_m
  descriptive OLS (N = 10; no inference claims).
- **Session order effects** (G.6.5): BSI ~ run_index robustness check; accepts
  raw ``EvaluationResult`` list.
- **BH-FDR correction** (G.5): Benjamini-Hochberg at q = 0.05 across the
  primary treatment-effect family.
"""
from __future__ import annotations

import json
import math
from datetime import datetime, timezone
from pathlib import Path

from pydantic import BaseModel, Field

from results.aggregate_cells import CellAggregate, CellAggregateReport


# ─────────────────────────────────────────────────────────────────────────────
# §1  LINEAR ALGEBRA (PURE PYTHON)
# ─────────────────────────────────────────────────────────────────────────────
# Design matrices are ≤ ~200 rows × 25 cols; pure-Python ops are fast enough.


def _dot(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def _transpose(A: list[list[float]]) -> list[list[float]]:
    if not A or not A[0]:
        return []
    return [[A[i][j] for i in range(len(A))] for j in range(len(A[0]))]


def _matmul(A: list[list[float]], B: list[list[float]]) -> list[list[float]]:
    """Matrix multiply A (n×k) × B (k×m) → n×m."""
    n, k = len(A), len(A[0])
    m = len(B[0])
    Bt = _transpose(B)
    return [[_dot(A[i], Bt[j]) for j in range(m)] for i in range(n)]


def _solve_linear(A: list[list[float]], b: list[float]) -> list[float]:
    """Solve Ax = b via Gaussian elimination with partial pivoting.

    Raises ``ValueError`` if the system is singular (rank-deficient design
    matrix, typically caused by collinear predictors or too few cells).
    """
    n = len(b)
    M = [A[i][:] + [b[i]] for i in range(n)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(M[r][col]))
        M[col], M[pivot] = M[pivot], M[col]
        if abs(M[col][col]) < 1e-12:
            raise ValueError(
                f"Singular design matrix at column {col}.  "
                "Likely cause: collinear predictors or fewer cells than "
                "parameters (run with n_runs ≥ 2 and ≥ 2 models/bias types)."
            )
        for row in range(col + 1, n):
            f = M[row][col] / M[col][col]
            M[row] = [M[row][j] - f * M[col][j] for j in range(n + 1)]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (M[i][n] - sum(M[i][j] * x[j] for j in range(i + 1, n))) / M[i][i]
    return x


# ─────────────────────────────────────────────────────────────────────────────
# §2  STATISTICS
# ─────────────────────────────────────────────────────────────────────────────

# Two-tailed t-critical values for 95 % CI (df = 1..29; df ≥ 30 → 1.960).
_T95_BY_DF: dict[int, float] = {
    1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571,
    6: 2.447, 7: 2.365, 8: 2.306, 9: 2.262, 10: 2.228,
    11: 2.201, 12: 2.179, 13: 2.160, 14: 2.145, 15: 2.131,
    16: 2.120, 17: 2.110, 18: 2.101, 19: 2.093, 20: 2.086,
    21: 2.080, 22: 2.074, 23: 2.069, 24: 2.064, 25: 2.060,
    26: 2.056, 27: 2.052, 28: 2.048, 29: 2.045,
}


def _t_critical_95(df: float) -> float:
    """Two-tailed t critical value for 95 % CI."""
    if df >= 30:
        return 1.960
    df_int = max(1, int(df))
    return _T95_BY_DF.get(df_int, 2.000)


def _betacf(a: float, b: float, x: float, max_iter: int = 200) -> float:
    """Continued-fraction expansion for the regularized incomplete beta function.

    Uses the Lentz algorithm (Numerical Recipes §6.4).
    """
    TINY = 1e-300
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
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
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < 3e-7:
            break
    return h


def _betainc(a: float, b: float, x: float) -> float:
    """Regularized incomplete beta function I_x(a, b).

    Used to compute exact t-distribution p-values via the identity:
    ``P(|T| > t; df) = I_{df/(df+t²)}(df/2, 1/2)``.
    """
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    if x > (a + 1.0) / (a + b + 2.0):
        return 1.0 - _betainc(b, a, 1.0 - x)
    lbeta = math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)
    return (
        math.exp(a * math.log(x) + b * math.log(1.0 - x) - lbeta)
        * _betacf(a, b, x)
        / a
    )


def _t_pvalue(t_stat: float, df: float) -> float:
    """Exact two-tailed p-value for *t_stat* with *df* degrees of freedom."""
    if df <= 0:
        return 1.0
    return _betainc(df / 2.0, 0.5, df / (df + t_stat ** 2))


def bh_fdr_correction(
    p_values: list[float], q: float = 0.05
) -> tuple[list[float], list[bool]]:
    """Benjamini-Hochberg FDR correction at level *q* (default 0.05).

    Returns ``(adjusted_p_values, rejected)`` in the *original* input order.
    The adjusted values satisfy the step-down monotonicity constraint so that
    they can be directly compared against *q*.

    Algorithm (Benjamini & Hochberg 1995):
    1. Sort hypotheses by raw p-value (ascending).
    2. Adjusted p-value at rank k: ``p_adj = min(1, p_k × n / k)``.
    3. Enforce monotonicity (step-down): take cumulative minimum from rank n → 1.
    4. Reject hypothesis i if ``p_adj_i < q``.
    """
    n = len(p_values)
    if n == 0:
        return [], []
    order = sorted(range(n), key=lambda i: p_values[i])
    # Step 2: compute raw adjustments in sorted order
    adj_sorted = [min(1.0, p_values[order[k]] * n / (k + 1)) for k in range(n)]
    # Step 3: step-down monotonicity (cummin from top)
    for k in range(n - 2, -1, -1):
        adj_sorted[k] = min(adj_sorted[k], adj_sorted[k + 1])
    # Map back to original order
    result = [0.0] * n
    for k, orig_idx in enumerate(order):
        result[orig_idx] = adj_sorted[k]
    rejected = [p < q for p in result]
    return result, rejected


# ─────────────────────────────────────────────────────────────────────────────
# §3  DATA MODELS
# ─────────────────────────────────────────────────────────────────────────────


class RegressionCoefficient(BaseModel):
    """One row of a regression results table."""

    name: str
    estimate: float
    se: float
    t_stat: float
    p_value: float
    """Raw (uncorrected) two-tailed p-value."""
    p_value_bh: float | None = None
    """BH-FDR adjusted p-value (set by the calling analysis)."""
    ci_lower_95: float
    ci_upper_95: float
    significant_05: bool = False
    """True when p_value_bh < 0.05 (or p_value < 0.05 if BH not applied)."""


class OLSResult(BaseModel):
    """Result of an OLS or WLS regression."""

    spec_name: str
    """Identifier: e.g. 'Level1_WLS', 'H2_Capability', 'H7_NoiseBias'."""
    n_obs: int
    df_residual: int
    r_squared: float
    se_type: str
    """'OLS', 'WLS', or 'clustered_by_model'."""
    n_clusters: int | None = None
    coefficients: list[RegressionCoefficient] = Field(default_factory=list)
    notes: str = ""
    cross_model_descriptive_only: bool = False
    """REV-6: True for cross-model analyses (N=10 models).
    When True, ``significant_05`` is forced False on all coefficients —
    p-values must NOT be used to claim statistical significance across models.
    Report as a descriptive scatter only; no p-value columns, no asterisks."""


class VarianceDecompositionRow(BaseModel):
    """One row of an ANOVA-style SS partition table."""

    source: str
    ss: float
    df: int
    ms: float
    eta_squared: float
    """η² = SS / SS_total."""
    pct_variance: float
    """η² × 100 (for display)."""


class VarianceDecomposition(BaseModel):
    """ANOVA-style SS partition for Pillar 2 BSI (G.2 Variance Decomposition)."""

    rows: list[VarianceDecompositionRow] = Field(default_factory=list)
    total_ss: float
    n_obs: int
    notes: str = ""

    def eta_squared(self, source: str) -> float | None:
        """Return η² for *source*, or ``None`` if not found."""
        for row in self.rows:
            if row.source == source:
                return row.eta_squared
        return None


class TreatmentEffectTest(BaseModel):
    """Per-(bias_category × agent_id) treatment-effect test (G.1 τ_bias)."""

    agent_id: str
    bias_category: str
    variant_pair_id: str | None = None
    mean_bsi_baseline: float
    mean_bsi_treatment: float
    treatment_effect: float
    """mean_bsi_treatment − mean_bsi_baseline."""
    n_baseline: int
    n_treatment: int
    se: float
    """Standard error of the treatment-effect estimate (Welch)."""
    t_stat: float
    df: float
    """Welch–Satterthwaite degrees of freedom."""
    p_value: float
    p_value_bh: float | None = None
    ci_lower_95: float
    ci_upper_95: float
    significant_05: bool = False


class StatsPipelineReport(BaseModel):
    """Full statistical analysis report for a multi-run Pillar 2 experiment."""

    generated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    n_cells: int
    n_agents: int
    n_treatment_effect_tests: int

    level1_ols: OLSResult | None = None
    """Level 1 WLS: BSI ~ Treatment + BiasType + Model (G.2)."""

    variance_decomposition: VarianceDecomposition | None = None
    """ANOVA-style SS partition: Model + BiasType + Treatment + Residual (G.2)."""

    treatment_effects: list[TreatmentEffectTest] = Field(default_factory=list)
    """Per-(bias_category × agent_id) tests with BH-FDR correction (G.1, G.5)."""

    h7_noise_bias: OLSResult | None = None
    """H7: std_bsi ~ mean_bsi (cell-level OLS; G.1 σ²_stoch)."""

    session_order_ols: OLSResult | None = None
    """G.6.5 robustness: BSI ~ run_index (requires EvaluationResult list)."""

    h2_capability: OLSResult | None = None
    """H2 descriptive: mean_BSI_m ~ P1Score_m across models (G.1 Δ_capability)."""

    bh_family_size: int = 0
    """Number of hypotheses in the primary BH-FDR family."""

    literature_calibration: list | None = None
    """UPGRADE-16: BuyerBench BSI calibrated against human and prior-LLM
    literature benchmarks.  Each entry is a
    :class:`results.literature_benchmarks.BenchmarkCalibrationResult`.
    ``None`` when no Pillar 2 cells are present."""

    warnings: list[str] = Field(default_factory=list)


# ─────────────────────────────────────────────────────────────────────────────
# §4  INTERNAL HELPERS
# ─────────────────────────────────────────────────────────────────────────────

# Variants that are the *control* arm (Treatment indicator = 0).
_CONTROL_VARIANTS: frozenset[str] = frozenset({"BASELINE", "FRAMING_GAIN"})

# WARP triplet variants — no clear BASELINE/TREATMENT; excluded from OLS.
_WARP_VARIANTS: frozenset[str] = frozenset({"WARP_AB", "WARP_BC", "WARP_AC"})


def _is_treatment(variant: str | None) -> bool:
    """Return True if this variant is the manipulation arm (Treatment = 1)."""
    if variant is None:
        return False
    return variant not in _CONTROL_VARIANTS and variant not in _WARP_VARIANTS


def _p2_cells_for_ols(cells: list[CellAggregate]) -> list[CellAggregate]:
    """Filter to P2 cells suitable for OLS: bias_category known, not WARP."""
    return [
        c for c in cells
        if c.bias_category
        and c.variant not in _WARP_VARIANTS
        and c.n_valid_runs > 0
    ]


def _wls_regress(
    X: list[list[float]],
    y: list[float],
    weights: list[float],
    col_names: list[str],
    cluster_ids: list[str] | None,
    spec_name: str,
) -> OLSResult:
    """Core WLS engine.

    Fits weighted least squares and returns an :class:`OLSResult` with
    regression coefficients, standard errors, t-statistics and p-values.

    When *cluster_ids* is provided, standard errors use the model-level
    clustered sandwich estimator (G.4): ``V = A⁻¹ B A⁻¹`` where
    ``A = X'WX`` and ``B = Σ_g score_g score_g'`` (with small-cluster
    correction ``G / (G − 1)``).  t-statistics use ``df = G − 1``.

    Without clustering, standard WLS SEs are computed and t-statistics
    use ``df = n − k``.
    """
    n, k = len(y), len(X[0])

    # ── Normal equations: A β = c ─────────────────────────────────────────
    A = [[0.0] * k for _ in range(k)]
    c = [0.0] * k
    for i in range(n):
        w = weights[i]
        xi = X[i]
        for j in range(k):
            c[j] += w * xi[j] * y[i]
            for l in range(k):
                A[j][l] += w * xi[j] * xi[l]

    beta = _solve_linear(A, c)

    # ── Residuals + R² ────────────────────────────────────────────────────
    w_sum = sum(weights)
    y_mean = sum(weights[i] * y[i] for i in range(n)) / w_sum
    residuals = [y[i] - sum(X[i][j] * beta[j] for j in range(k)) for i in range(n)]
    ss_res = sum(weights[i] * residuals[i] ** 2 for i in range(n))
    ss_tot = sum(weights[i] * (y[i] - y_mean) ** 2 for i in range(n))
    r2 = max(0.0, 1.0 - ss_res / ss_tot) if ss_tot > 1e-12 else 0.0

    # ── Variance–covariance matrix of β ──────────────────────────────────
    if cluster_ids is not None:
        # Clustered sandwich: V = A⁻¹ B A⁻¹
        unique_clusters = sorted(set(cluster_ids))
        G = len(unique_clusters)
        cluster_map: dict[str, list[int]] = {g: [] for g in unique_clusters}
        for i, cid in enumerate(cluster_ids):
            cluster_map[cid].append(i)
        # Meat matrix B (k × k)
        B = [[0.0] * k for _ in range(k)]
        corr = G / (G - 1.0) if G > 1 else 1.0  # small-cluster correction
        for g in unique_clusters:
            score = [
                sum(weights[i] * residuals[i] * X[i][j] for i in cluster_map[g])
                for j in range(k)
            ]
            for j in range(k):
                for l in range(k):
                    B[j][l] += corr * score[j] * score[l]
        # M = A⁻¹ B: solve A m_l = B[:, l] for each column l
        M = _transpose(
            [_solve_linear(A, [B[j][l] for j in range(k)]) for l in range(k)]
        )
        # V diag: V[j][j] = (A⁻¹ M^T)[j][j] = solve(A, M[j,:])[j]
        v_diag = [_solve_linear(A, M[j])[j] for j in range(k)]
        df_inf = float(G - 1)
        se_type = "clustered_by_model"
        n_clusters = G
    else:
        # Standard WLS: V = σ² A⁻¹
        sigma2 = ss_res / max(1, n - k)
        # V[j][j] = σ² × (A⁻¹)[j][j]; solve A e_j = e_j to get column j
        v_diag = []
        for j in range(k):
            e_j = [1.0 if l == j else 0.0 for l in range(k)]
            inv_col_j = _solve_linear(A, e_j)
            v_diag.append(sigma2 * inv_col_j[j])
        df_inf = float(n - k)
        se_type = "WLS"
        n_clusters = None

    # ── Assemble coefficient table ────────────────────────────────────────
    t_crit = _t_critical_95(df_inf)
    coefficients: list[RegressionCoefficient] = []
    for j in range(k):
        se_j = math.sqrt(max(0.0, v_diag[j]))
        t_j = beta[j] / se_j if se_j > 1e-12 else 0.0
        p_j = _t_pvalue(t_j, df_inf)
        margin = t_crit * se_j
        coefficients.append(
            RegressionCoefficient(
                name=col_names[j],
                estimate=round(beta[j], 6),
                se=round(se_j, 6),
                t_stat=round(t_j, 4),
                p_value=round(p_j, 6),
                ci_lower_95=round(beta[j] - margin, 6),
                ci_upper_95=round(beta[j] + margin, 6),
                significant_05=p_j < 0.05,
            )
        )

    return OLSResult(
        spec_name=spec_name,
        n_obs=n,
        df_residual=int(df_inf),
        r_squared=round(r2, 6),
        se_type=se_type,
        n_clusters=n_clusters,
        coefficients=coefficients,
    )


# ─────────────────────────────────────────────────────────────────────────────
# §5  LEVEL 1 OLS  (G.2)
# ─────────────────────────────────────────────────────────────────────────────


def run_level1_ols(cells: list[CellAggregate]) -> OLSResult | None:
    """Level 1 WLS: BSI ~ Treatment + BiasType + Model (G.2).

    Specification::

        BSI_cell = α + β_t · Treatment + Σ β_b · BiasType_b
                 + Σ β_m · Model_m + ε

    Each cell is one observation; weight = n_valid_runs (more runs →
    more weight).  Returns both WLS and clustered (model-level) SEs.

    Returns ``None`` when there are fewer than 3 distinct agents or fewer
    than 2 bias types (design matrix would be singular).
    """
    eligible = _p2_cells_for_ols(cells)
    agents = sorted({c.agent_id for c in eligible})
    bias_types = sorted({c.bias_category for c in eligible if c.bias_category})

    if len(agents) < 2 or len(bias_types) < 2:
        return None

    # Reference categories (dropped): agents[0], bias_types[0]
    ref_agent = agents[0]
    ref_bias = bias_types[0]

    col_names = (
        ["Intercept", "Treatment"]
        + [f"BiasType_{b}" for b in bias_types if b != ref_bias]
        + [f"Model_{m}" for m in agents if m != ref_agent]
    )
    k = len(col_names)

    X: list[list[float]] = []
    y: list[float] = []
    weights: list[float] = []
    cluster_ids: list[str] = []

    for c in eligible:
        row = [1.0, 1.0 if _is_treatment(c.variant) else 0.0]
        for b in bias_types:
            if b != ref_bias:
                row.append(1.0 if c.bias_category == b else 0.0)
        for m in agents:
            if m != ref_agent:
                row.append(1.0 if c.agent_id == m else 0.0)
        X.append(row)
        y.append(c.mean_bsi)
        weights.append(float(max(1, c.n_valid_runs)))
        cluster_ids.append(c.agent_id)

    if len(X) <= k:
        return None  # under-identified

    try:
        return _wls_regress(
            X, y, weights, col_names,
            cluster_ids=cluster_ids,
            spec_name="Level1_WLS_clustered",
        )
    except ValueError:
        # Fall back to plain WLS if clustering fails (e.g. G ≤ 1)
        try:
            return _wls_regress(
                X, y, weights, col_names,
                cluster_ids=None,
                spec_name="Level1_WLS",
            )
        except ValueError:
            return None


# ─────────────────────────────────────────────────────────────────────────────
# §6  VARIANCE DECOMPOSITION  (G.2)
# ─────────────────────────────────────────────────────────────────────────────


def compute_variance_decomposition(
    cells: list[CellAggregate],
) -> VarianceDecomposition | None:
    """ANOVA-style SS partition: Model + BiasType + Treatment + Residual.

    Uses unweighted (cell-level) SS to show what fraction of observed BSI
    variance is attributable to each source.  Returns ``None`` when fewer
    than 4 cells are available (cannot form meaningful ANOVA).
    """
    eligible = _p2_cells_for_ols(cells)
    if len(eligible) < 4:
        return None

    bsi = [c.mean_bsi for c in eligible]
    n = len(bsi)
    grand_mean = sum(bsi) / n
    ss_total = sum((v - grand_mean) ** 2 for v in bsi)
    if ss_total < 1e-12:
        return None

    def _between_ss(group_key) -> float:
        groups: dict = {}
        for c in eligible:
            k = group_key(c)
            groups.setdefault(k, []).append(c.mean_bsi)
        return sum(
            len(vals) * (sum(vals) / len(vals) - grand_mean) ** 2
            for vals in groups.values()
        )

    agents = sorted({c.agent_id for c in eligible})
    bias_types = sorted({c.bias_category for c in eligible if c.bias_category})
    n_agents = len(agents)
    n_bias = len(bias_types)

    ss_model = _between_ss(lambda c: c.agent_id)
    ss_bias = _between_ss(lambda c: c.bias_category)
    ss_treat = _between_ss(lambda c: _is_treatment(c.variant))
    ss_residual = max(0.0, ss_total - ss_model - ss_bias - ss_treat)

    df_model = n_agents - 1
    df_bias = n_bias - 1
    df_treat = 1
    df_residual = max(1, n - df_model - df_bias - df_treat - 1)

    def _row(source: str, ss: float, df: int) -> VarianceDecompositionRow:
        ms = ss / max(1, df)
        eta2 = ss / ss_total
        return VarianceDecompositionRow(
            source=source,
            ss=round(ss, 6),
            df=df,
            ms=round(ms, 6),
            eta_squared=round(eta2, 6),
            pct_variance=round(eta2 * 100.0, 2),
        )

    rows = [
        _row("Model", ss_model, df_model),
        _row("BiasType", ss_bias, df_bias),
        _row("Treatment", ss_treat, df_treat),
        _row("Residual", ss_residual, df_residual),
    ]
    return VarianceDecomposition(
        rows=rows,
        total_ss=round(ss_total, 6),
        n_obs=n,
        notes=(
            "Unweighted (cell-level) SS.  η² = SS / SS_total.  "
            "η²_Residual > 0.70 → most BSI variance is stochastic noise (G.2)."
        ),
    )


# ─────────────────────────────────────────────────────────────────────────────
# §7  TREATMENT EFFECT TESTS  (G.1)
# ─────────────────────────────────────────────────────────────────────────────


def _find_control_variant(
    group: list[CellAggregate],
) -> CellAggregate | None:
    """Return the control-arm cell from a paired group.

    Prefers explicit BASELINE; falls back to FRAMING_GAIN for framing pairs.
    """
    for c in group:
        if c.variant == "BASELINE":
            return c
    for c in group:
        if c.variant == "FRAMING_GAIN":
            return c
    return None


def compute_treatment_effect_tests(
    cells: list[CellAggregate],
) -> list[TreatmentEffectTest]:
    """Per-(bias_category × agent_id) Welch t-tests with BH-FDR correction.

    For each (agent, variant_pair) group, pairs the control arm with the
    treatment arm and computes:

    - ``treatment_effect = mean_bsi_treatment − mean_bsi_baseline``
    - ``SE`` via the Welch formula: ``√(SE_b² + SE_t²)``
    - ``df`` via Welch–Satterthwaite
    - two-tailed ``p_value`` via the exact t-distribution CDF
    - BH-FDR adjusted ``p_value_bh`` at q = 0.05 across all tests

    WARP-triplet cells are excluded (no clear BASELINE/TREATMENT pairing).
    Cells with ``n_valid_runs < 2`` use a pooled-SE approximation (N = 1 is
    treated as N = 2 with std_bsi = 0 to avoid division by zero, and the
    result is flagged as low-precision).
    """
    eligible = [
        c for c in cells
        if c.bias_category
        and c.variant not in _WARP_VARIANTS
        and c.n_valid_runs > 0
    ]

    # Group by (agent_id, variant_pair_id or scenario_id)
    groups: dict[tuple, list[CellAggregate]] = {}
    for c in eligible:
        key = (c.agent_id, c.variant_pair_id or c.scenario_id)
        groups.setdefault(key, []).append(c)

    tests: list[TreatmentEffectTest] = []
    for (agent_id, _), group in sorted(groups.items()):
        baseline = _find_control_variant(group)
        treatments = [c for c in group if c is not baseline and _is_treatment(c.variant)]
        if baseline is None or not treatments:
            continue
        treatment = treatments[0]  # take the first treatment arm

        # SE via Welch: var(cell) = (std_bsi / sqrt(n))^2
        n_b = max(2, baseline.n_valid_runs)
        n_t = max(2, treatment.n_valid_runs)
        var_b = (baseline.std_bsi ** 2) / n_b if baseline.std_bsi > 0 else 1e-6 / n_b
        var_t = (treatment.std_bsi ** 2) / n_t if treatment.std_bsi > 0 else 1e-6 / n_t
        se = math.sqrt(var_b + var_t)

        te = treatment.mean_bsi - baseline.mean_bsi
        t_stat = te / se if se > 1e-12 else 0.0

        # Welch–Satterthwaite df
        if (var_b + var_t) > 1e-24:
            df_welch = (var_b + var_t) ** 2 / (
                var_b ** 2 / max(1, n_b - 1) + var_t ** 2 / max(1, n_t - 1)
            )
        else:
            df_welch = float(n_b + n_t - 2)

        p = _t_pvalue(t_stat, df_welch)
        t_crit = _t_critical_95(df_welch)
        ci_lo = te - t_crit * se
        ci_hi = te + t_crit * se

        tests.append(
            TreatmentEffectTest(
                agent_id=agent_id,
                bias_category=baseline.bias_category or "",
                variant_pair_id=baseline.variant_pair_id,
                mean_bsi_baseline=round(baseline.mean_bsi, 6),
                mean_bsi_treatment=round(treatment.mean_bsi, 6),
                treatment_effect=round(te, 6),
                n_baseline=baseline.n_valid_runs,
                n_treatment=treatment.n_valid_runs,
                se=round(se, 6),
                t_stat=round(t_stat, 4),
                df=round(df_welch, 2),
                p_value=round(p, 6),
                ci_lower_95=round(ci_lo, 6),
                ci_upper_95=round(ci_hi, 6),
                significant_05=p < 0.05,
            )
        )

    if not tests:
        return tests

    # BH-FDR correction across all tests (primary family, G.5)
    raw_p = [t.p_value for t in tests]
    adj_p, rejected = bh_fdr_correction(raw_p, q=0.05)
    for i, test in enumerate(tests):
        test.p_value_bh = round(adj_p[i], 6)
        test.significant_05 = rejected[i]

    return tests


# ─────────────────────────────────────────────────────────────────────────────
# §8  H7 NOISE-BIAS CORRELATION  (G.1 σ²_stoch)
# ─────────────────────────────────────────────────────────────────────────────


def compute_h7_noise_bias(cells: list[CellAggregate]) -> OLSResult | None:
    """H7: std_bsi ~ mean_bsi (G.1 σ²_stoch — noise-bias correlation).

    Regresses within-cell BSI standard deviation on the cell mean BSI.
    A positive slope supports H7: biased decisions are noisier because the
    agent is near a decision boundary.

    Only cells with n_valid_runs ≥ 2 are included (std_bsi = 0 at N = 1).
    Returns ``None`` if fewer than 3 qualifying cells.
    """
    eligible = [
        c for c in cells
        if c.bias_category
        and c.n_valid_runs >= 2
        and c.std_bsi >= 0.0
    ]
    if len(eligible) < 3:
        return None

    X = [[1.0, c.mean_bsi] for c in eligible]
    y = [c.std_bsi for c in eligible]
    weights = [float(c.n_valid_runs) for c in eligible]

    try:
        return _wls_regress(
            X, y, weights,
            col_names=["Intercept", "mean_bsi"],
            cluster_ids=None,
            spec_name="H7_NoiseBias",
        )
    except ValueError:
        return None


# ─────────────────────────────────────────────────────────────────────────────
# §9  H2 CAPABILITY REGRESSION  (G.1 Δ_capability)
# ─────────────────────────────────────────────────────────────────────────────


def compute_h2_capability(
    cells: list[CellAggregate],
    p1_scores: dict[str, float],
) -> OLSResult | None:
    """H2 descriptive: mean_BSI_m ~ P1Score_m (G.1 Δ_capability).

    Regresses each model's mean BSI on its Pillar 1 capability score.
    With N = 10 models, this is treated as **descriptive only** — no
    inference claims; p-values are not reported as evidence for causation.

    Args:
        cells: All P2 cell aggregate data.
        p1_scores: Mapping ``{agent_id: P1_aggregate_score}`` from a
            separate Pillar 1 experiment or literature calibration.

    Returns ``None`` if fewer than 3 agents have P1 scores.
    """
    eligible = [c for c in cells if c.bias_category and c.n_valid_runs > 0]

    # Compute per-agent mean BSI across all bias types
    agent_bsi: dict[str, list[float]] = {}
    for c in eligible:
        agent_bsi.setdefault(c.agent_id, []).append(c.mean_bsi)
    agent_mean_bsi = {
        a: sum(v) / len(v) for a, v in agent_bsi.items() if v
    }

    # Keep only agents with both mean_bsi and p1_score
    common = sorted(
        a for a in agent_mean_bsi if a in p1_scores
    )
    if len(common) < 3:
        return None

    X = [[1.0, p1_scores[a]] for a in common]
    y = [agent_mean_bsi[a] for a in common]
    weights = [1.0] * len(common)

    try:
        result = _wls_regress(
            X, y, weights,
            col_names=["Intercept", "P1Score"],
            cluster_ids=None,
            spec_name="H2_Capability",
        )
        result.notes = (
            f"N = {len(common)} models.  Descriptive only (G.2 caveat): "
            "with N = 10, do not interpret p-values as inferential evidence.  "
            "Report as 'suggestive pattern' with wide CIs."
        )
        # REV-6: mark as cross-model descriptive and suppress significance flags.
        # p_value fields are retained for internal computation but must never
        # be reported as evidence of a statistically significant cross-model effect.
        result.cross_model_descriptive_only = True
        for coef in result.coefficients:
            coef.significant_05 = False
        return result
    except ValueError:
        return None


# ─────────────────────────────────────────────────────────────────────────────
# §10  SESSION ORDER EFFECTS  (G.6.5)
# ─────────────────────────────────────────────────────────────────────────────


def compute_session_order_effects(results: list) -> OLSResult | None:
    """G.6.5 robustness check: BSI ~ run_index.

    A non-zero slope would indicate drift across runs within a cell,
    suggesting API-load effects, within-collection model updates, or caching
    artefacts.  Expectation: coefficient ≈ 0.

    Accepts a list of ``EvaluationResult`` objects (requires ``run_index``
    and Pillar 2 ``PillarScore`` to be present).  Returns ``None`` when
    fewer than 4 qualifying observations.
    """
    from buyerbench.models import Pillar

    rows_x: list[float] = []
    rows_y: list[float] = []

    for r in results:
        if getattr(r, "error_flag", False):
            continue
        p2 = next(
            (ps for ps in r.pillar_scores if ps.pillar == Pillar.PILLAR2), None
        )
        if p2 is None:
            continue
        bsi = p2.metrics.get("bias_susceptibility_index")
        if bsi is None:
            continue
        rows_x.append(float(getattr(r, "run_index", 0)))
        rows_y.append(float(bsi))

    if len(rows_x) < 4:
        return None

    X = [[1.0, x] for x in rows_x]
    y = rows_y
    weights = [1.0] * len(y)

    try:
        result = _wls_regress(
            X, y, weights,
            col_names=["Intercept", "run_index"],
            cluster_ids=None,
            spec_name="SessionOrder_G6_5",
        )
        result.notes = (
            "G.6.5 robustness: non-zero run_index slope → drift (API load, "
            "within-collection model updates).  Expected coefficient ≈ 0."
        )
        return result
    except ValueError:
        return None


# ─────────────────────────────────────────────────────────────────────────────
# §11  PUBLIC API
# ─────────────────────────────────────────────────────────────────────────────


def run_stats_pipeline(
    cell_report: CellAggregateReport,
    *,
    p1_scores: dict[str, float] | None = None,
    evaluation_results: list | None = None,
) -> StatsPipelineReport:
    """Run all Section G analyses and return a :class:`StatsPipelineReport`.

    Args:
        cell_report: Cell-level aggregate data from :func:`aggregate_cells`.
        p1_scores: Optional ``{agent_id: float}`` mapping for H2 capability
            regression.  When ``None``, H2 is skipped.
        evaluation_results: Optional list of raw ``EvaluationResult`` objects
            for the G.6.5 session-order robustness check.  When ``None``,
            session-order analysis is skipped.

    Returns:
        :class:`StatsPipelineReport` with all available analyses populated
        and ``warnings`` for any analyses that could not be run.
    """
    cells = cell_report.cells
    warnings: list[str] = []

    # ── Level 1 OLS ──────────────────────────────────────────────────────
    level1 = run_level1_ols(cells)
    if level1 is None:
        warnings.append(
            "Level 1 OLS skipped: need ≥ 2 agents and ≥ 2 bias types with "
            "non-WARP Pillar 2 cells."
        )

    # ── Variance decomposition ────────────────────────────────────────────
    var_decomp = compute_variance_decomposition(cells)
    if var_decomp is None:
        warnings.append(
            "Variance decomposition skipped: need ≥ 4 Pillar 2 cells."
        )

    # ── Treatment effect tests (BH corrected) ────────────────────────────
    te_tests = compute_treatment_effect_tests(cells)
    if not te_tests:
        warnings.append(
            "Treatment effect tests skipped: no paired BASELINE/TREATMENT "
            "cells found.  Run with --n-runs ≥ 2 for meaningful SEs."
        )

    # ── H7 noise-bias correlation ─────────────────────────────────────────
    h7 = compute_h7_noise_bias(cells)
    if h7 is None:
        warnings.append(
            "H7 noise-bias skipped: need ≥ 3 cells with n_valid_runs ≥ 2."
        )

    # ── H2 capability regression ──────────────────────────────────────────
    h2 = None
    if p1_scores:
        h2 = compute_h2_capability(cells, p1_scores)
        if h2 is None:
            warnings.append(
                "H2 capability regression skipped: need ≥ 3 agents with both "
                "P2 cell data and P1 scores."
            )
    else:
        warnings.append(
            "H2 capability regression skipped: no p1_scores provided.  "
            "Pass p1_scores={agent_id: score} to enable."
        )

    # ── Session order effects ─────────────────────────────────────────────
    session_order = None
    if evaluation_results:
        session_order = compute_session_order_effects(evaluation_results)
        if session_order is None:
            warnings.append(
                "Session order effects skipped: need ≥ 4 Pillar 2 run-level "
                "results with run_index set."
            )
    else:
        warnings.append(
            "Session order effects skipped: no evaluation_results provided.  "
            "Pass evaluation_results=list[EvaluationResult] to enable."
        )

    # ── Literature benchmark calibration (UPGRADE-16) ─────────────────────
    from results.literature_benchmarks import compute_benchmark_calibration

    p2_cells = _p2_cells_for_ols(cells)
    experiment_bsi: dict[str, float] | None = None
    if p2_cells:
        bsi_by_bias: dict[str, list[float]] = {}
        for c in p2_cells:
            if c.bias_category:
                bsi_by_bias.setdefault(c.bias_category, []).append(c.mean_bsi)
        if bsi_by_bias:
            experiment_bsi = {
                bias: sum(vals) / len(vals)
                for bias, vals in bsi_by_bias.items()
            }
    lit_calibration = compute_benchmark_calibration(experiment_bsi)

    agents = {c.agent_id for c in cells}
    return StatsPipelineReport(
        n_cells=len(cells),
        n_agents=len(agents),
        n_treatment_effect_tests=len(te_tests),
        level1_ols=level1,
        variance_decomposition=var_decomp,
        treatment_effects=te_tests,
        h7_noise_bias=h7,
        session_order_ols=session_order,
        h2_capability=h2,
        bh_family_size=len(te_tests),
        literature_calibration=lit_calibration,
        warnings=warnings,
    )


def write_stats_pipeline_report(
    report: StatsPipelineReport,
    output_dir: str | Path,
    filename: str = "stats_pipeline_report.json",
) -> Path:
    """Serialise *report* to ``{output_dir}/{filename}`` and return the path."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / filename
    out_path.write_text(report.model_dump_json(indent=2, exclude_none=False))
    return out_path
