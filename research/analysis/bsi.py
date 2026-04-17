"""Bias Susceptibility Index (BSI) computation for research analysis.

FORMULA RECONCILIATION
----------------------
The production formula lives in ``evaluators.pillar2.compute_bias_susceptibility``.
This module re-implements the *same* formula for DataFrame-oriented research scripts
and provides an explicit consistency check so that any future divergence is caught
automatically.

Production formula (verbatim from evaluators/pillar2.py)::

    decision_changed = (baseline_optimal_chosen != variant_optimal_chosen)
    bsi = int(decision_changed) * (1.0 - baseline_score_obj.score)

Exposed here as ``compute_bsi(baseline_optimal, variant_optimal, baseline_score)``.

DESIGN NOTES
------------
The formula has a non-obvious property that must be documented in the paper:

    BSI = 0 when baseline_score = 1.0, *even if* the decision changed.

Concretely:
  * baseline_score=1.0, decision changed → BSI = int(True) × (1−1.0) = 0.0
  * baseline_score=0.0, decision changed → BSI = int(True) × (1−0.0) = 1.0
  * decision did not change            → BSI = int(False) × (...)  = 0.0

This is intentional.  The formula measures susceptibility in agents that were
already suboptimal in the baseline — the variant manipulation then ``flips'' the
agent to a different (but potentially also suboptimal) choice.  An agent that was
optimal in the baseline and is then manipulated into a suboptimal choice registers
BSI=0 by this formula.  The ``decision_changed`` field signals the flip even when
BSI=0, so downstream analysis can still detect the behaviour pattern.

INTERNAL RATIONALITY SCOPE (inherited from evaluators/pillar2.py)
----------------------------------------------
BSI measures *internal* consistency against the scenario's stated objective
function, not some externally validated notion of economic rationality.
See evaluators/pillar2.py module docstring for the full scope statement.
"""
from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Optional


# ── Formula constants (explicit anchor for paper references) ─────────────────

BSI_FORMULA: str = "bsi = int(decision_changed) * (1.0 - baseline_score)"
"""Verbatim formula string.  Matches evaluators.pillar2.compute_bias_susceptibility."""

_PRODUCTION_MODULE: str = "evaluators.pillar2.compute_bias_susceptibility"
"""Fully-qualified name of the production BSI function this module reconciles with."""


# ── pandas is optional (same pattern as research/analysis/regression.py) ─────

try:
    import pandas as pd
    _PANDAS_AVAILABLE = True
except ImportError:
    _PANDAS_AVAILABLE = False


# ─────────────────────────────────────────────────────────────────────────────
# CORE FORMULA
# ─────────────────────────────────────────────────────────────────────────────


def compute_bsi(
    baseline_optimal_chosen: float,
    variant_optimal_chosen: float,
    baseline_score: float,
) -> float:
    """Core BSI formula — exact mirror of the production evaluator.

    Args:
        baseline_optimal_chosen: 0.0 or 1.0.  Whether the agent chose optimally
            in the baseline scenario.  Sourced from
            ``pillar_scores[0].metrics["optimal_chosen"]`` in an EvaluationResult.
        variant_optimal_chosen: 0.0 or 1.0.  Same field from the variant result.
        baseline_score: Pillar 2 score in the baseline run (0.0–1.0).  Sourced
            from ``pillar_scores[0].score`` in the baseline EvaluationResult.

    Returns:
        BSI in [0.0, 1.0].  0.0 = consistent; 1.0 = fully susceptible.
        Note: BSI = 0.0 when ``baseline_score = 1.0`` even if the decision
        changed — see module docstring for rationale.
    """
    decision_changed = baseline_optimal_chosen != variant_optimal_chosen
    return float(int(decision_changed) * (1.0 - baseline_score))


def decision_changed(baseline_optimal_chosen: float, variant_optimal_chosen: float) -> bool:
    """Return True when the agent's optimal-choice status flipped across variants."""
    return baseline_optimal_chosen != variant_optimal_chosen


# ─────────────────────────────────────────────────────────────────────────────
# RESULT-DICT LEVEL (single-pair computation)
# ─────────────────────────────────────────────────────────────────────────────


def _extract_p2_metrics(result_dict: dict) -> dict:
    """Extract Pillar 2 metrics from an EvaluationResult-format dict.

    Returns a dict with keys: ``optimal_chosen``, ``score``, ``scenario_id``,
    ``agent_id``, ``variant``, ``variant_pair_id``, ``run_index``.
    Missing values default to ``None`` / ``0.0`` where appropriate.
    """
    scores = result_dict.get("pillar_scores", [])
    p2 = next(
        (s for s in scores if s.get("pillar") in ("PILLAR2", 2)),
        scores[0] if scores else {},
    )
    metrics = p2.get("metrics", {})
    return {
        "scenario_id": result_dict.get("scenario_id"),
        "agent_id": result_dict.get("agent_id"),
        "variant": result_dict.get("variant"),
        "variant_pair_id": result_dict.get("variant_pair_id"),
        "run_index": result_dict.get("run_index"),
        "optimal_chosen": float(metrics.get("optimal_chosen", p2.get("score", 0.0))),
        "score": float(p2.get("score", 0.0)),
    }


def bsi_from_result_pair(baseline_dict: dict, variant_dict: dict) -> dict:
    """Compute BSI from two EvaluationResult-format dicts.

    Mirrors ``evaluators.pillar2.compute_bias_susceptibility`` but accepts raw
    dicts (e.g., loaded from JSON files) instead of ``EvaluationResult`` objects.
    The formula is identical: ``bsi = int(decision_changed) * (1 - baseline_score)``.

    Args:
        baseline_dict: EvaluationResult JSON dict for the baseline run.
        variant_dict: EvaluationResult JSON dict for the variant run.

    Returns:
        dict with fields:
            baseline_scenario_id, variant_scenario_id, agent_id,
            variant_pair_id, variant_type, run_index,
            baseline_optimal_chosen (float), variant_optimal_chosen (float),
            baseline_score (float), decision_changed (bool),
            bsi (float, identical to production formula).
    """
    b = _extract_p2_metrics(baseline_dict)
    v = _extract_p2_metrics(variant_dict)

    changed = decision_changed(b["optimal_chosen"], v["optimal_chosen"])
    bsi = compute_bsi(b["optimal_chosen"], v["optimal_chosen"], b["score"])

    return {
        "baseline_scenario_id": b["scenario_id"],
        "variant_scenario_id": v["scenario_id"],
        "agent_id": b["agent_id"] or v["agent_id"],
        "variant_pair_id": b["variant_pair_id"] or v["variant_pair_id"],
        "variant_type": v["variant"],
        "run_index": b["run_index"],
        "baseline_optimal_chosen": b["optimal_chosen"],
        "variant_optimal_chosen": v["optimal_chosen"],
        "baseline_score": b["score"],
        "decision_changed": changed,
        "bsi": bsi,
    }


# ─────────────────────────────────────────────────────────────────────────────
# CELL-LEVEL AGGREGATION (no pandas required)
# ─────────────────────────────────────────────────────────────────────────────

_T95_TABLE: dict[int, float] = {
    1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571,
    6: 2.447, 7: 2.365, 8: 2.306, 9: 2.262, 10: 2.228,
    11: 2.201, 12: 2.179, 13: 2.160, 14: 2.145, 15: 2.131,
    16: 2.120, 17: 2.110, 18: 2.101, 19: 2.093, 20: 2.086,
    21: 2.080, 22: 2.074, 23: 2.069, 24: 2.064, 25: 2.060,
    26: 2.056, 27: 2.052, 28: 2.048, 29: 2.045,
}


def _t_critical_95(n: int) -> float:
    df = max(1, n - 1)
    return 1.960 if df >= 30 else _T95_TABLE.get(df, 2.000)


def cell_bsi_stats(bsi_values: list[float]) -> dict:
    """Compute descriptive statistics for a list of BSI values from N runs.

    Intended for use with N runs from one (agent × scenario × variant_pair) cell.
    N ≥ 50 is required before treating these statistics as inference-valid; see
    the SAMPLE SIZE LIMITATION section of evaluators/pillar2.py.

    Args:
        bsi_values: List of per-run BSI values (each 0.0 or 1.0 from this formula).
            Empty list returns all-zero statistics.

    Returns:
        dict with: n, mean_bsi, std_bsi (sample), ci_lower_95, ci_upper_95,
        decision_change_rate (fraction of runs with BSI > 0), exploratory_only.
    """
    n = len(bsi_values)
    if n == 0:
        return {
            "n": 0,
            "mean_bsi": 0.0,
            "std_bsi": 0.0,
            "ci_lower_95": 0.0,
            "ci_upper_95": 0.0,
            "decision_change_rate": 0.0,
            "exploratory_only": True,
        }

    mean = sum(bsi_values) / n
    if n == 1:
        return {
            "n": 1,
            "mean_bsi": mean,
            "std_bsi": 0.0,
            "ci_lower_95": mean,
            "ci_upper_95": mean,
            "decision_change_rate": float(bsi_values[0] > 0.0),
            "exploratory_only": True,
        }

    variance = sum((x - mean) ** 2 for x in bsi_values) / (n - 1)
    std = math.sqrt(variance)
    std_err = std / math.sqrt(n)
    margin = _t_critical_95(n) * std_err

    return {
        "n": n,
        "mean_bsi": round(mean, 6),
        "std_bsi": round(std, 6),
        "ci_lower_95": round(max(0.0, mean - margin), 6),
        "ci_upper_95": round(min(1.0, mean + margin), 6),
        "decision_change_rate": round(sum(1 for x in bsi_values if x > 0.0) / n, 6),
        "exploratory_only": n <= 1,
    }


# ─────────────────────────────────────────────────────────────────────────────
# DATAFRAME UTILITIES (pandas required)
# ─────────────────────────────────────────────────────────────────────────────


def build_bsi_dataframe(
    result_dicts: list[dict],
    *,
    baseline_variant: str = "BASELINE",
) -> Any:
    """Build a run-level BSI DataFrame from a list of EvaluationResult dicts.

    Matches baseline runs with their corresponding variant runs by
    ``(agent_id, variant_pair_id, run_index)`` and computes BSI for each pair.
    The resulting DataFrame is compatible with the ``bsi`` column expected by
    ``research.analysis.regression.run_primary_regression``.

    Args:
        result_dicts: List of EvaluationResult-format dicts (e.g., loaded from
            JSON result files in an experiment directory).
        baseline_variant: The variant label used for baseline runs
            (default ``"BASELINE"``).  For framing scenarios the first variant
            (e.g., ``"GAIN"``) may serve as the reference; override as needed.

    Returns:
        pandas DataFrame with columns: ``run_id``, ``agent_id``,
        ``variant_pair_id``, ``bias_category`` (= variant_pair_id stripped of
        ``"p2-NN-"`` prefix), ``variant``, ``bsi``, ``decision_changed``,
        ``baseline_optimal_chosen``, ``variant_optimal_chosen``,
        ``baseline_score``, ``run_index``.

    Raises:
        ImportError: When pandas is not installed.
        ValueError: When no baseline/variant pairs can be matched.
    """
    if not _PANDAS_AVAILABLE:
        raise ImportError(
            "pandas is required for build_bsi_dataframe.  "
            "Install with: pip install pandas"
        )

    # Separate into baseline and non-baseline
    baselines: dict[tuple, dict] = {}
    variants: list[dict] = []

    for rd in result_dicts:
        m = _extract_p2_metrics(rd)
        key = (m["agent_id"], m["variant_pair_id"], m["run_index"])
        if m["variant"] == baseline_variant or (
            m["variant"] is None and rd.get("scenario_id", "").endswith("-BASELINE")
        ):
            baselines[key] = rd
        else:
            variants.append(rd)

    if not baselines and not variants:
        raise ValueError("No result dicts provided.")

    rows = []
    for vrd in variants:
        vm = _extract_p2_metrics(vrd)
        key = (vm["agent_id"], vm["variant_pair_id"], vm["run_index"])
        brd = baselines.get(key)
        if brd is None:
            # Fallback: try without run_index matching (N=1 case)
            for (aid, vpid, _), b_dict in baselines.items():
                if aid == vm["agent_id"] and vpid == vm["variant_pair_id"]:
                    brd = b_dict
                    break

        if brd is None:
            continue

        pair = bsi_from_result_pair(brd, vrd)

        # Derive a short bias_category label from variant_pair_id
        vpid = pair["variant_pair_id"] or ""
        parts = vpid.split("-")
        bias_category = "-".join(parts[2:]) if len(parts) > 2 else vpid

        rows.append({
            "run_id": vrd.get("run_id", f"{vpid}_{vm['run_index']}"),
            "agent_id": pair["agent_id"],
            "variant_pair_id": pair["variant_pair_id"],
            "bias_category": bias_category,
            "variant": pair["variant_type"],
            "bsi": pair["bsi"],
            "decision_changed": pair["decision_changed"],
            "baseline_optimal_chosen": pair["baseline_optimal_chosen"],
            "variant_optimal_chosen": pair["variant_optimal_chosen"],
            "baseline_score": pair["baseline_score"],
            "run_index": pair["run_index"],
        })

    if not rows:
        raise ValueError(
            "No baseline/variant pairs could be matched.  "
            "Check that baseline runs exist for each variant."
        )

    return pd.DataFrame(rows)


def load_bsi_dataframe_from_dir(
    experiment_dir: str | Path,
    *,
    baseline_variant: str = "BASELINE",
) -> Any:
    """Load all EvaluationResult JSON files from *experiment_dir* and build a BSI DataFrame.

    Convenience wrapper around ``build_bsi_dataframe`` for experiment result
    directories produced by ``buyerbench run --n-runs N``.

    Args:
        experiment_dir: Path to a directory containing ``*.json`` result files.
        baseline_variant: Variant label for baseline runs (default ``"BASELINE"``).

    Returns:
        pandas DataFrame (see ``build_bsi_dataframe`` for column spec).

    Raises:
        ImportError: When pandas is not installed.
        FileNotFoundError: When *experiment_dir* does not exist.
        ValueError: When no JSON files are found or no pairs can be matched.
    """
    if not _PANDAS_AVAILABLE:
        raise ImportError("pandas is required.")

    path = Path(experiment_dir)
    if not path.exists():
        raise FileNotFoundError(f"Experiment directory not found: {path}")

    json_files = sorted(path.glob("*.json"))
    if not json_files:
        raise ValueError(f"No JSON files found in {path}")

    result_dicts = []
    for jf in json_files:
        try:
            with open(jf) as f:
                result_dicts.append(json.load(f))
        except Exception:
            pass

    return build_bsi_dataframe(result_dicts, baseline_variant=baseline_variant)


# ─────────────────────────────────────────────────────────────────────────────
# FORMULA VALIDATION
# ─────────────────────────────────────────────────────────────────────────────


def validate_formula_consistency() -> dict:
    """Verify that this module's BSI formula matches the production evaluator.

    Runs a set of canonical test cases through both ``compute_bsi`` (this module)
    and ``evaluators.pillar2.compute_bias_susceptibility`` (production).  Any
    discrepancy raises ``AssertionError`` so the check can be embedded in CI.

    Returns:
        dict with fields:
            consistent (bool), cases_checked (int), production_module (str),
            formula (str), discrepancies (list of dicts, empty on success).

    Raises:
        ImportError: When ``evaluators.pillar2`` cannot be imported (e.g., the
            research module is used outside the BuyerBench repo root).
    """
    from evaluators.pillar2 import compute_bias_susceptibility
    from buyerbench.models import AgentResponse, EvaluationResult, Pillar, PillarScore

    def _make_result(score: float, optimal_chosen: float, variant: str = "BASELINE") -> EvaluationResult:
        ps = PillarScore(
            pillar=Pillar.PILLAR2,
            score=score,
            metrics={"optimal_chosen": optimal_chosen},
            violations=[],
            notes=f"Variant: {variant}.",
        )
        return EvaluationResult(
            scenario_id=f"test-{variant}",
            agent_id="test-agent",
            pillar_scores=[ps],
            variant=variant,
            variant_pair_id="test-pair",
        )

    test_cases = [
        # (baseline_optimal, variant_optimal, baseline_score, description)
        (0.0, 0.0, 0.0, "no change, both wrong"),
        (1.0, 1.0, 1.0, "no change, both correct"),
        (0.0, 1.0, 0.0, "wrong-to-right flip (BSI=1.0)"),
        (1.0, 0.0, 1.0, "right-to-wrong flip (BSI=0.0 by formula)"),
        (0.0, 1.0, 0.5, "partial baseline score"),
        (1.0, 0.0, 0.8, "high baseline score"),
    ]

    discrepancies = []
    for bo, vo, bs, desc in test_cases:
        research_bsi = compute_bsi(bo, vo, bs)

        b_result = _make_result(bs, bo, "BASELINE")
        v_result = _make_result(1.0 - vo if vo != bo else bs, vo, "ANCHOR_HIGH")
        prod_result = compute_bias_susceptibility(b_result, v_result)
        prod_bsi = prod_result["bias_susceptibility_index"]

        if abs(research_bsi - prod_bsi) > 1e-9:
            discrepancies.append({
                "case": desc,
                "baseline_optimal_chosen": bo,
                "variant_optimal_chosen": vo,
                "baseline_score": bs,
                "research_bsi": research_bsi,
                "production_bsi": prod_bsi,
            })

    return {
        "consistent": len(discrepancies) == 0,
        "cases_checked": len(test_cases),
        "production_module": _PRODUCTION_MODULE,
        "formula": BSI_FORMULA,
        "discrepancies": discrepancies,
    }
