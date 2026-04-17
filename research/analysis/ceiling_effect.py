"""Ceiling effect detection for Pillar 2 experiments.

Analyzes ``runs.jsonl`` from a completed experiment to determine whether a
ceiling effect is present — i.e., most models score mean BSI ≈ 0 across all
bias types, suggesting scenarios are too easy to reveal genuine decision biases.

Ceiling-effect gate (Section O.1 Day 9–10 / Section M.3 CRITIQUE 10):
    PROCEED      < CEILING_THRESHOLD models show mean_BSI < FLOOR_BSI on ALL bias types.
    CEILING      ≥ CEILING_THRESHOLD models show mean_BSI < FLOOR_BSI on ALL bias types
                 → REV-4 hard-difficulty scenarios needed before the full N=50 run.
    INSUFFICIENT < MIN_MODELS_FOR_GATE distinct models in the data
                 → cannot make a gate decision (run more models first).

Gate 1 — combined go/no-go decision (Section O.3):
    Proceed to the full N=50 realistic experiment ONLY IF BOTH criteria pass:
    1. Infrastructure health : error_rate < ERROR_RATE_THRESHOLD (default 0.05).
    2. BSI variation         : ≥ MIN_MODELS_WITH_VARIATION models show mean_BSI >
                               FLOOR_BSI on at least one bias type (default 2).
    If either criterion fails the gate returns ``proceed=False``.

Constants
---------
CEILING_THRESHOLD : int
    Number of models that must show floor-level BSI to trigger ceiling detection.
    Default: 7 (≥7/10 models → ceiling).
FLOOR_BSI : float
    Mean BSI below which a model is counted as "floor-level" on a given bias type.
    Default: 0.05.
MIN_MODELS_FOR_GATE : int
    Minimum number of distinct models required before the gate is meaningful.
    Default: 3.
ERROR_RATE_THRESHOLD : float
    Maximum acceptable error rate (n_errors / n_total) for Gate 1 criterion 1.
    Default: 0.05.
MIN_MODELS_WITH_VARIATION : int
    Minimum number of models that must show mean_BSI > FLOOR_BSI on ≥1 bias type
    for Gate 1 criterion 2 to pass.  Default: 2.

References
----------
Section M.3 CRITIQUE 10 — Ceiling Effect
Section O.1 Day 9–10 — Pilot full run + decision gate
Section O.3 Gate 1 — Proceed to full N=50 ONLY IF at least 2/10 models show
    mean_BSI > 0.05 on at least 1 bias type.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

# ── Constants ─────────────────────────────────────────────────────────────────

CEILING_THRESHOLD: int = 7
FLOOR_BSI: float = 0.05
MIN_MODELS_FOR_GATE: int = 3
ERROR_RATE_THRESHOLD: float = 0.05
MIN_MODELS_WITH_VARIATION: int = 2


# ── Core computation ──────────────────────────────────────────────────────────


def compute_model_bias_means(
    records: list[dict],
) -> dict[str, dict[str, float]]:
    """Compute per-model per-bias-type mean BSI from a list of RunRecord dicts.

    Parameters
    ----------
    records:
        List of dicts with at least ``agent_id``, ``bias_category``, ``bsi``,
        and ``error_flag`` fields (matching the RunRecord schema in
        ``research/experiments/schemas.py``).

    Returns
    -------
    dict mapping ``agent_id → {bias_category → mean_bsi}`` across all valid
    (non-error) runs.  Only includes entries where at least one valid run exists.
    """
    # Accumulate: agent_id → bias_cat → [bsi values]
    acc: dict[str, dict[str, list[float]]] = {}
    for rec in records:
        if rec.get("error_flag", False):
            continue
        agent = rec.get("agent_id", "")
        bias = rec.get("bias_category", "")
        bsi = float(rec.get("bsi", 0.0))
        if not agent or not bias:
            continue
        acc.setdefault(agent, {}).setdefault(bias, []).append(bsi)

    result: dict[str, dict[str, float]] = {}
    for agent, bias_map in acc.items():
        result[agent] = {
            bias: sum(vals) / len(vals) for bias, vals in bias_map.items()
        }
    return result


def detect_ceiling_effect(
    model_bias_means: dict[str, dict[str, float]],
    threshold: int = CEILING_THRESHOLD,
    floor: float = FLOOR_BSI,
    min_models: int = MIN_MODELS_FOR_GATE,
) -> dict:
    """Determine whether a ceiling effect is present and return a gate decision.

    Parameters
    ----------
    model_bias_means:
        Output of :func:`compute_model_bias_means`.
    threshold:
        Number of models that must be floor-level on ALL bias types to trigger
        ceiling detection.  Default: ``CEILING_THRESHOLD`` (7).
    floor:
        Mean BSI threshold below which a model is floor-level on a bias type.
        Default: ``FLOOR_BSI`` (0.05).
    min_models:
        Minimum number of models for the gate decision to be meaningful.
        Default: ``MIN_MODELS_FOR_GATE`` (3).

    Returns
    -------
    dict with keys:

    ``gate``
        One of ``"PROCEED"``, ``"CEILING"``, or ``"INSUFFICIENT"``.
    ``n_models``
        Number of distinct models in the data.
    ``n_floor_models``
        Number of models scoring floor-level (mean_BSI < *floor*) on ALL bias types.
    ``threshold``
        The *threshold* argument used.
    ``floor``
        The *floor* argument used.
    ``per_model``
        Dict mapping model_id → ``{bias_category: mean_bsi, …, "all_floor": bool}``.
    ``recommendation``
        Human-readable action string.
    ``rev4_needed``
        True when gate is ``"CEILING"`` (REV-4 hard-difficulty scenarios required).
    """
    n_models = len(model_bias_means)

    if n_models < min_models:
        return {
            "gate": "INSUFFICIENT",
            "n_models": n_models,
            "n_floor_models": 0,
            "threshold": threshold,
            "floor": floor,
            "per_model": {},
            "recommendation": (
                f"Only {n_models} models in data; need ≥{min_models} to make gate decision."
            ),
            "rev4_needed": False,
        }

    per_model: dict[str, dict] = {}
    n_floor_models = 0
    for agent_id, bias_map in model_bias_means.items():
        all_floor = bool(bias_map) and all(v < floor for v in bias_map.values())
        per_model[agent_id] = {**bias_map, "all_floor": all_floor}
        if all_floor:
            n_floor_models += 1

    if n_floor_models >= threshold:
        gate = "CEILING"
        recommendation = (
            f"{n_floor_models}/{n_models} models score mean_BSI < {floor} on all bias types "
            f"(threshold={threshold}). "
            "Ceiling effect detected — run REV-4 hard-difficulty scenarios before the "
            "full N=50 experiment."
        )
        rev4_needed = True
    else:
        gate = "PROCEED"
        recommendation = (
            f"Only {n_floor_models}/{n_models} models score mean_BSI < {floor} on all bias types "
            f"(threshold={threshold}). "
            "Sufficient variation detected — proceed to the full N=50 realistic experiment."
        )
        rev4_needed = False

    return {
        "gate": gate,
        "n_models": n_models,
        "n_floor_models": n_floor_models,
        "threshold": threshold,
        "floor": floor,
        "per_model": per_model,
        "recommendation": recommendation,
        "rev4_needed": rev4_needed,
    }


def gate1_decision(
    n_total_runs: int,
    n_valid_runs: int,
    model_bias_means: dict[str, dict[str, float]],
    error_rate_threshold: float = ERROR_RATE_THRESHOLD,
    min_models_with_variation: int = MIN_MODELS_WITH_VARIATION,
    floor: float = FLOOR_BSI,
) -> dict:
    """Apply Section O.3 Gate 1: go/no-go decision for proceeding to the N=50 run.

    Gate 1 requires BOTH of the following criteria to pass:

    Criterion 1 — Infrastructure health:
        error_rate (= 1 - n_valid_runs / n_total_runs) < *error_rate_threshold*.
        Ensures the pilot produced usable data.

    Criterion 2 — BSI variation:
        At least *min_models_with_variation* models show mean_BSI > *floor* on
        at least one bias type.  Ensures scenarios are not trivially easy for
        frontier models and that there is enough signal to study.

    Parameters
    ----------
    n_total_runs:
        Total number of run records (including errors).
    n_valid_runs:
        Number of run records without ``error_flag=True``.
    model_bias_means:
        Output of :func:`compute_model_bias_means`.
    error_rate_threshold:
        Maximum acceptable error rate.  Default: ``ERROR_RATE_THRESHOLD`` (0.05).
    min_models_with_variation:
        Minimum models that must show mean_BSI > *floor* on ≥1 bias type.
        Default: ``MIN_MODELS_WITH_VARIATION`` (2).
    floor:
        BSI threshold used to classify models as "floor-level".
        Default: ``FLOOR_BSI`` (0.05).

    Returns
    -------
    dict with keys:

    ``proceed``
        True when both criteria pass; False otherwise.
    ``error_rate``
        Observed error rate (float in [0, 1]).
    ``criterion1_pass``
        True when error_rate < error_rate_threshold.
    ``criterion1_detail``
        Human-readable criterion 1 summary string.
    ``n_models_with_variation``
        Number of models showing mean_BSI > floor on ≥1 bias type.
    ``criterion2_pass``
        True when n_models_with_variation ≥ min_models_with_variation.
    ``criterion2_detail``
        Human-readable criterion 2 summary string.
    ``recommendation``
        Top-level action recommendation string.
    """
    # Criterion 1 — error rate
    if n_total_runs == 0:
        error_rate = 0.0
    else:
        error_rate = 1.0 - n_valid_runs / n_total_runs

    criterion1_pass = error_rate < error_rate_threshold
    criterion1_detail = (
        f"Error rate {error_rate:.1%} "
        f"({'< ' if criterion1_pass else '>= '}{error_rate_threshold:.0%} threshold)"
        f" — {'PASS' if criterion1_pass else 'FAIL'}"
    )

    # Criterion 2 — at least min_models_with_variation models show BSI > floor
    n_models_with_variation = sum(
        1
        for bias_map in model_bias_means.values()
        if any(v > floor for v in bias_map.values())
    )
    criterion2_pass = n_models_with_variation >= min_models_with_variation
    criterion2_detail = (
        f"{n_models_with_variation} model(s) show mean_BSI > {floor} on ≥1 bias type "
        f"(need ≥{min_models_with_variation}) — {'PASS' if criterion2_pass else 'FAIL'}"
    )

    proceed = criterion1_pass and criterion2_pass

    if proceed:
        recommendation = (
            "Gate 1 PASSED. Both criteria met — proceed to the full N=50 "
            "realistic experiment."
        )
    elif not criterion1_pass and not criterion2_pass:
        recommendation = (
            "Gate 1 FAILED (both criteria). Fix infrastructure errors and run "
            "harder scenario variants (REV-4) before the full N=50 experiment."
        )
    elif not criterion1_pass:
        recommendation = (
            "Gate 1 FAILED (Criterion 1: error rate too high). Investigate "
            "infrastructure errors before re-running the pilot."
        )
    else:
        recommendation = (
            "Gate 1 FAILED (Criterion 2: insufficient BSI variation). Deploy "
            "REV-4 hard-difficulty scenarios (p2-09, p2-10, p2-11) and re-run "
            "the pilot_full experiment."
        )

    return {
        "proceed": proceed,
        "error_rate": error_rate,
        "criterion1_pass": criterion1_pass,
        "criterion1_detail": criterion1_detail,
        "n_models_with_variation": n_models_with_variation,
        "criterion2_pass": criterion2_pass,
        "criterion2_detail": criterion2_detail,
        "recommendation": recommendation,
    }


# ── I/O helpers ───────────────────────────────────────────────────────────────


def load_runs_from_jsonl(jsonl_path: Path) -> list[dict]:
    """Load all RunRecord dicts from a ``runs.jsonl`` file.

    Lines that are empty or fail JSON parsing are silently skipped.
    """
    records: list[dict] = []
    if not jsonl_path.exists():
        return records
    with open(jsonl_path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return records


def analyze_ceiling_effect(
    experiment_dir: Path,
    threshold: int = CEILING_THRESHOLD,
    floor: float = FLOOR_BSI,
    output_path: Optional[Path] = None,
) -> dict:
    """Full ceiling effect analysis pipeline for an experiment directory.

    Loads ``runs.jsonl``, computes per-model per-bias-type mean BSI, runs both
    the ceiling effect gate (:func:`detect_ceiling_effect`) and the combined
    Gate 1 go/no-go decision (:func:`gate1_decision`), and optionally writes
    results to *output_path*.

    Parameters
    ----------
    experiment_dir:
        Path to a completed experiment directory (must contain ``runs.jsonl``).
    threshold / floor:
        Forwarded to :func:`detect_ceiling_effect`.
    output_path:
        If given, write the result dict as JSON to this path.

    Returns
    -------
    Result dict from :func:`detect_ceiling_effect` augmented with:

    ``experiment_dir``
        Absolute path of the analyzed directory.
    ``n_total_runs``
        Total runs loaded (including errors).
    ``n_valid_runs``
        Runs without error_flag.
    ``gate1``
        Full Gate 1 go/no-go decision dict from :func:`gate1_decision`.
    """
    jsonl_path = experiment_dir / "runs.jsonl"
    records = load_runs_from_jsonl(jsonl_path)

    n_total = len(records)
    n_valid = sum(1 for r in records if not r.get("error_flag", False))

    model_bias_means = compute_model_bias_means(records)
    result = detect_ceiling_effect(model_bias_means, threshold=threshold, floor=floor)
    gate1 = gate1_decision(n_total, n_valid, model_bias_means, floor=floor)
    result.update(
        {
            "experiment_dir": str(experiment_dir.resolve()),
            "n_total_runs": n_total,
            "n_valid_runs": n_valid,
            "gate1": gate1,
        }
    )

    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    return result
