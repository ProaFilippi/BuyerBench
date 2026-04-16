"""Cell-level aggregate output for multi-run Pillar 2 experiments (UPGRADE-5).

Groups N repeated EvaluationResult runs by ``(agent_id, variant_pair_id, variant,
temperature)`` and computes ``mean_bsi``, ``std_bsi``, 95 % CI, ``choice_rate_correct``,
``mean_optimality_gap``, and ``treatment_effect_vs_baseline``.

Typical usage::

    from results.aggregate_cells import aggregate_cells, write_cell_aggregates

    # After all runs complete (all_results is list[EvaluationResult]):
    report = aggregate_cells(all_results)
    write_cell_aggregates(report, output_dir)

    # Or load from an experiment directory of JSON files:
    report = aggregate_cells_from_dir("results/my-experiment")
"""
from __future__ import annotations

import json
import math
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from pydantic import BaseModel, Field

from buyerbench.models import EvaluationResult, Pillar


# ── t-distribution critical values for 95 % two-tailed CI ────────────────────
# Source: standard t-table; df = n - 1.

_T95_TABLE: dict[int, float] = {
    1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571,
    6: 2.447, 7: 2.365, 8: 2.306, 9: 2.262, 10: 2.228,
    11: 2.201, 12: 2.179, 13: 2.160, 14: 2.145, 15: 2.131,
    16: 2.120, 17: 2.110, 18: 2.101, 19: 2.093, 20: 2.086,
    21: 2.080, 22: 2.074, 23: 2.069, 24: 2.064, 25: 2.060,
    26: 2.056, 27: 2.052, 28: 2.048, 29: 2.045,
}


def _t_critical_95(n: int) -> float:
    """Two-tailed t critical value for 95 % CI with df = n - 1.

    Uses the lookup table for df < 30 and the normal approximation (z = 1.960)
    for df >= 30, where the t-distribution converges to the standard normal.
    """
    df = max(1, n - 1)
    if df >= 30:
        return 1.960
    return _T95_TABLE.get(df, 2.000)


def _confidence_interval_95(values: list[float]) -> tuple[float, float]:
    """Compute a 95 % confidence interval for *values* using the t-distribution.

    Returns ``(lower, upper)`` clamped to ``[0.0, 1.0]``.  For n=1, the CI
    degenerates to the point estimate.  For n=0, returns ``(0.0, 0.0)``.
    """
    n = len(values)
    if n == 0:
        return (0.0, 0.0)
    mean = sum(values) / n
    if n == 1:
        return (mean, mean)
    variance = sum((x - mean) ** 2 for x in values) / (n - 1)
    std_err = math.sqrt(variance / n)
    margin = _t_critical_95(n) * std_err
    return (max(0.0, mean - margin), min(1.0, mean + margin))


# ── Output schema ─────────────────────────────────────────────────────────────


class CellAggregate(BaseModel):
    """Aggregated statistics for a single (agent, scenario_variant, temperature) cell.

    A *cell* contains all N repeated runs of the same scenario variant by the same
    agent at the same temperature setting.  Cell-level statistics (mean_bsi, std_bsi,
    CI, treatment_effect) are only meaningful when N >= 2 — with N=1 the CI
    degenerates to the point estimate and the std is 0.
    """

    cell_id: str
    """Unique string key: ``{agent_id}__{variant_pair_id or scenario_id}__{variant}__{temperature}``."""

    agent_id: str
    scenario_id: str
    """Representative scenario_id from the first run in this cell."""

    variant_pair_id: str | None = None
    variant: str | None = None
    bias_category: str | None = None
    temperature: float | None = None

    n_runs: int
    """Total number of runs in this cell (including error runs)."""

    n_valid_runs: int
    """Runs where error_flag == False; used as the denominator for all metrics."""

    mean_bsi: float
    """Mean per-run bias susceptibility index (0.0 = always optimal, 1.0 = never optimal)."""

    std_bsi: float
    """Sample standard deviation of BSI across valid runs (0.0 if n_valid_runs <= 1)."""

    ci_lower_95: float
    """Lower bound of the 95 % t-distribution CI for mean_bsi."""

    ci_upper_95: float
    """Upper bound of the 95 % t-distribution CI for mean_bsi."""

    choice_rate_correct: float
    """Fraction of valid runs in which the agent selected the optimal choice."""

    choice_rate_distribution: dict[str, int] = Field(default_factory=dict)
    """Supplier name → number of runs in which that supplier was selected."""

    mean_optimality_gap: float
    """Mean optimality_gap across valid runs (0.0 = always optimal; 1.0 = maximum gap)."""

    treatment_effect_vs_baseline: float | None = None
    """For non-BASELINE cells: ``mean_bsi(treatment) - mean_bsi(baseline)``; null if no paired baseline cell exists or this IS the baseline."""


class CellAggregateReport(BaseModel):
    """Full cell-level aggregate report for a multi-run experiment."""

    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    n_agents: int
    n_cells: int
    n_total_runs: int
    cells: list[CellAggregate] = Field(default_factory=list)


# ── Core aggregation logic ────────────────────────────────────────────────────


def _cell_key(result: EvaluationResult) -> tuple:
    """Compute the hashable grouping key for *result*.

    Groups by ``(agent_id, pair_group, variant, temperature)`` where
    *pair_group* is ``variant_pair_id`` when available (groups BASELINE +
    TREATMENT from the same scenario pair) and falls back to ``scenario_id``
    for results without a pair.
    """
    return (
        result.agent_id,
        result.variant_pair_id or result.scenario_id,
        result.variant or "",
        result.temperature,
    )


def _make_cell_id(
    agent_id: str,
    pair_group: str,
    variant: str,
    temperature: float | None,
) -> str:
    """Build the human-readable cell ID string."""
    temp_str = f"{temperature}" if temperature is not None else "None"
    return f"{agent_id}__{pair_group}__{variant}__{temp_str}"


def _compute_cell_aggregate(results: list[EvaluationResult]) -> CellAggregate:
    """Aggregate statistics for *results* that all belong to the same cell.

    Extracts per-run metrics from ``PillarScore.metrics`` for Pillar 2 results.
    Skips runs with ``error_flag == True`` when computing statistical metrics.
    """
    first = results[0]
    pair_group = first.variant_pair_id or first.scenario_id

    bsi_values: list[float] = []
    opt_gap_values: list[float] = []
    supplier_counts: dict[str, int] = {}
    valid_count = 0

    for r in results:
        if r.error_flag:
            continue
        valid_count += 1

        p2_score = next(
            (ps for ps in r.pillar_scores if ps.pillar == Pillar.PILLAR2), None
        )
        if p2_score is not None:
            bsi_values.append(p2_score.metrics.get("bias_susceptibility_index", 0.0))
            opt_gap_values.append(p2_score.metrics.get("optimality_gap", 0.0))

        # Tally supplier choice distribution
        supplier = (
            r.decisions.get("selected_supplier")
            or r.decisions.get("supplier")
        )
        if supplier is not None:
            key = str(supplier)
            supplier_counts[key] = supplier_counts.get(key, 0) + 1

    n = len(bsi_values)
    mean_bsi = sum(bsi_values) / n if n > 0 else 0.0

    if n >= 2:
        std_bsi = math.sqrt(sum((x - mean_bsi) ** 2 for x in bsi_values) / (n - 1))
    else:
        std_bsi = 0.0

    ci_lower, ci_upper = _confidence_interval_95(bsi_values)

    # choice_rate_correct = fraction of runs where BSI == 0 (i.e., optimal chosen)
    choice_rate_correct = sum(1 for v in bsi_values if v == 0.0) / n if n > 0 else 0.0
    mean_opt_gap = sum(opt_gap_values) / len(opt_gap_values) if opt_gap_values else 0.0

    cell_id = _make_cell_id(
        first.agent_id,
        pair_group,
        first.variant or "",
        first.temperature,
    )

    return CellAggregate(
        cell_id=cell_id,
        agent_id=first.agent_id,
        scenario_id=first.scenario_id,
        variant_pair_id=first.variant_pair_id,
        variant=first.variant,
        bias_category=first.bias_category,
        temperature=first.temperature,
        n_runs=len(results),
        n_valid_runs=valid_count,
        mean_bsi=mean_bsi,
        std_bsi=std_bsi,
        ci_lower_95=ci_lower,
        ci_upper_95=ci_upper,
        choice_rate_correct=choice_rate_correct,
        choice_rate_distribution=supplier_counts,
        mean_optimality_gap=mean_opt_gap,
        # treatment_effect computed in a second pass after all cells are known
        treatment_effect_vs_baseline=None,
    )


def _add_treatment_effects(cells: list[CellAggregate]) -> None:
    """In-place: fill ``treatment_effect_vs_baseline`` for non-BASELINE cells.

    Pairs cells by ``(agent_id, variant_pair_id, temperature)``.  The BASELINE
    cell in each pair sets the reference; all other cells in the pair receive
    ``treatment_effect = mean_bsi(treatment) - mean_bsi(baseline)``.

    Cells without a matching baseline (or without a ``variant_pair_id``) are
    left with ``treatment_effect_vs_baseline = None``.
    """
    # Index baseline cells by their pairing key
    baseline_index: dict[tuple, CellAggregate] = {}
    for cell in cells:
        if cell.variant == "BASELINE" and cell.variant_pair_id:
            key = (cell.agent_id, cell.variant_pair_id, cell.temperature)
            baseline_index[key] = cell

    for cell in cells:
        if cell.variant == "BASELINE" or not cell.variant_pair_id:
            continue
        key = (cell.agent_id, cell.variant_pair_id, cell.temperature)
        baseline = baseline_index.get(key)
        if baseline is not None:
            cell.treatment_effect_vs_baseline = round(
                cell.mean_bsi - baseline.mean_bsi, 6
            )


# ── Public API ────────────────────────────────────────────────────────────────


def aggregate_cells(results: list[EvaluationResult]) -> CellAggregateReport:
    """Aggregate *results* into cell-level statistics.

    Groups results by ``(agent_id, variant_pair_id or scenario_id, variant,
    temperature)`` and computes mean_bsi, std_bsi, 95 % CI,
    choice_rate_correct, mean_optimality_gap, and treatment_effect for each
    cell.  Treatment effects are computed in a second pass after all cells
    are assembled.

    Args:
        results: Flat list of :class:`EvaluationResult` from one or more
            agents across one or more runs.  May contain results from any
            pillar; non-Pillar-2 results still produce cells but will have
            zero BSI metrics.

    Returns:
        :class:`CellAggregateReport` with ``cells`` sorted by
        ``(agent_id, variant_pair_id, variant, temperature)``.
    """
    grouped: dict[tuple, list[EvaluationResult]] = defaultdict(list)
    for r in results:
        grouped[_cell_key(r)].append(r)

    cells: list[CellAggregate] = []
    for key in sorted(grouped.keys()):
        cell = _compute_cell_aggregate(grouped[key])
        cells.append(cell)

    _add_treatment_effects(cells)

    agent_ids = {r.agent_id for r in results}
    return CellAggregateReport(
        n_agents=len(agent_ids),
        n_cells=len(cells),
        n_total_runs=len(results),
        cells=cells,
    )


def aggregate_cells_from_dir(
    experiment_dir: str | Path,
) -> CellAggregateReport:
    """Load result JSONs from *experiment_dir* and produce a :class:`CellAggregateReport`.

    Walks one sub-directory per agent under *experiment_dir*, loads all
    non-skipped result JSON files, and passes them through
    :func:`aggregate_cells`.

    Args:
        experiment_dir: Path produced by ``buyerbench run --output-dir``.
            Expects one sub-directory per agent, each containing
            ``<scenario_id>[-run<NNN>].json`` files.

    Returns:
        :class:`CellAggregateReport` for the full experiment.
    """
    experiment_dir = Path(experiment_dir)
    results: list[EvaluationResult] = []

    for agent_dir in sorted(experiment_dir.iterdir()):
        if not agent_dir.is_dir():
            continue
        for json_file in sorted(agent_dir.glob("*.json")):
            try:
                raw = json.loads(json_file.read_text())
            except Exception:
                continue
            if raw.get("status") == "skipped":
                continue
            try:
                result = EvaluationResult.model_validate(raw)
                results.append(result)
            except Exception:
                continue

    return aggregate_cells(results)


def write_cell_aggregates(
    report: CellAggregateReport,
    output_dir: str | Path,
    filename: str = "cell_aggregates.json",
) -> Path:
    """Serialise *report* to ``{output_dir}/{filename}`` and return the path.

    Args:
        report: The :class:`CellAggregateReport` to write.
        output_dir: Directory in which to place the output file.
        filename: Output filename (default: ``cell_aggregates.json``).

    Returns:
        :class:`~pathlib.Path` of the written file.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / filename
    out_path.write_text(
        report.model_dump_json(indent=2, exclude_none=False)
    )
    return out_path
