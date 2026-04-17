"""Ceiling effect detection for Pillar 2 experiments.

Analyzes ``runs.jsonl`` from a completed experiment to determine whether a
ceiling effect is present — i.e., most models score mean BSI ≈ 0 across all
bias types, suggesting scenarios are too easy to reveal genuine decision biases.

Gate decision (Section O.3 — Day 10):
    PROCEED      < CEILING_THRESHOLD models show mean_BSI < FLOOR_BSI on ALL bias types.
    CEILING      ≥ CEILING_THRESHOLD models show mean_BSI < FLOOR_BSI on ALL bias types
                 → REV-4 hard-difficulty scenarios needed before the full N=50 run.
    INSUFFICIENT < MIN_MODELS_FOR_GATE distinct models in the data
                 → cannot make a gate decision (run more models first).

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

    Loads ``runs.jsonl``, computes per-model per-bias-type mean BSI, runs the
    ceiling effect gate, and optionally writes results to *output_path*.

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
    """
    jsonl_path = experiment_dir / "runs.jsonl"
    records = load_runs_from_jsonl(jsonl_path)

    n_total = len(records)
    n_valid = sum(1 for r in records if not r.get("error_flag", False))

    model_bias_means = compute_model_bias_means(records)
    result = detect_ceiling_effect(model_bias_means, threshold=threshold, floor=floor)
    result.update(
        {
            "experiment_dir": str(experiment_dir.resolve()),
            "n_total_runs": n_total,
            "n_valid_runs": n_valid,
        }
    )

    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    return result
