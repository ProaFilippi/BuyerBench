"""Run orchestration for Pillar 2 research experiments.

Accepts an ExperimentManifest JSON file, expands the full run plan, and invokes
the BuyerBench runner for each (model, scenario, variant, run_index, temperature,
prompt_version) cell.  Writes RunRecord rows to ``runs.jsonl`` in append mode so
no data is lost if the process is interrupted.

Features
--------
- ``--dry-run``  Print plan + cost estimate without invoking any models.
- ``--resume``   Skip run_ids already recorded in runs.jsonl (restart after crash).
- After all runs complete, automatically invokes
  ``research/scripts/02_aggregate_results.py`` to build ``cells.json``.

CLI usage
---------
    python -m research.experiments.run_experiment manifest.json [options]
    python research/scripts/00_define_experiment.py  # first, to produce manifest.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from research.experiments.schemas import RunRecord


# ── Run plan generation ───────────────────────────────────────────────────────


def generate_run_plan(manifest: dict) -> list[dict]:
    """Expand a manifest dict into a flat list of run-spec dicts.

    Each dict contains the full spec for one invocation:
    ``run_id``, ``agent_id``, ``scenario_id``, ``bias_category``,
    ``variant``, ``run_index``, ``temperature``, ``prompt_version``,
    ``supplier_order_seed``.

    The ``run_id`` is a deterministic 12-char SHA-256 prefix of the cell key
    + run index, matching the convention in ``00_define_experiment.py``.
    """
    runs: list[dict] = []
    for model in manifest["models"]:
        for bias_cat, scenarios in manifest["bias_scenarios"].items():
            for variant_name, scenario_id in scenarios.items():
                for temp in manifest["temperatures"]:
                    for prompt_ver in manifest["prompt_versions"]:
                        for r in range(1, manifest["n_runs_per_cell"] + 1):
                            cell_key = f"{model}__{scenario_id}__{temp}__{prompt_ver}"
                            run_id_raw = f"{cell_key}__run{r}"
                            run_id = hashlib.sha256(run_id_raw.encode()).hexdigest()[:12]
                            seed = (
                                int(hashlib.md5(run_id_raw.encode()).hexdigest(), 16) % 2**32
                            )
                            runs.append(
                                {
                                    "run_id": run_id,
                                    "agent_id": model,
                                    "scenario_id": scenario_id,
                                    "bias_category": bias_cat,
                                    "variant": variant_name,
                                    "run_index": r,
                                    "temperature": temp,
                                    "prompt_version": prompt_ver,
                                    "supplier_order_seed": seed,
                                }
                            )
    return runs


# ── JSONL helpers ─────────────────────────────────────────────────────────────


def load_completed_run_ids(jsonl_path: Path) -> set[str]:
    """Return the set of run_ids already recorded in *jsonl_path*."""
    completed: set[str] = set()
    if not jsonl_path.exists():
        return completed
    with open(jsonl_path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                try:
                    completed.add(json.loads(line)["run_id"])
                except (json.JSONDecodeError, KeyError):
                    pass
    return completed


def append_run_record(record: RunRecord, jsonl_path: Path) -> None:
    """Serialize *record* to JSON and append one line to *jsonl_path*."""
    data = asdict(record)
    # datetime → ISO-8601 string
    for key, val in data.items():
        if isinstance(val, datetime):
            data[key] = val.isoformat()
    with open(jsonl_path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(data) + "\n")


# ── BuyerBench subprocess call ────────────────────────────────────────────────


def _invoke_buyerbench(run_spec: dict, run_output_dir: Path) -> dict | None:
    """Call ``python -m buyerbench run`` for one cell.

    Writes results under *run_output_dir*/<agent_id>/<scenario_id>.json.
    Returns the parsed result dict, or ``None`` on failure.
    """
    cmd = [
        sys.executable,
        "-m",
        "buyerbench",
        "run",
        "--agent",
        run_spec["agent_id"],
        "--scenario",
        run_spec["scenario_id"],
        "--n-runs",
        "1",
        "--output-dir",
        str(run_output_dir),
        "--prompt-version",
        run_spec["prompt_version"],
        "--no-dashboard",
        "--no-academic-report",
    ]
    if run_spec["temperature"] is not None:
        cmd += ["--temperature", str(run_spec["temperature"])]

    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    except subprocess.TimeoutExpired:
        return None
    except Exception:
        return None

    if proc.returncode != 0:
        return None

    # --n-runs 1 writes {scenario_id}-run000.json; bare {scenario_id}.json is
    # the single-run (no --n-runs flag) convention.  Try both patterns.
    agent_dir = run_output_dir / run_spec["agent_id"]
    scenario_id = run_spec["scenario_id"]
    candidates = [
        agent_dir / f"{scenario_id}.json",
        agent_dir / f"{scenario_id}-run000.json",
    ]
    result_path = next((p for p in candidates if p.exists()), None)
    if result_path is None:
        # Last resort: glob for any matching JSON in the agent directory
        matches = list(agent_dir.glob(f"{scenario_id}*.json")) if agent_dir.exists() else []
        result_path = matches[0] if matches else None

    if result_path is None:
        return None

    try:
        return json.loads(result_path.read_text(encoding="utf-8"))
    except Exception:
        return None


# ── RunRecord construction ────────────────────────────────────────────────────


def build_run_record(run_spec: dict, result: dict | None, session_id: str) -> RunRecord:
    """Construct a :class:`RunRecord` from a run spec and the raw result dict.

    When *result* is ``None`` (run failed), ``error_flag`` is set and all
    metric fields default to 0 / empty.
    """
    error_flag = result is None
    error_message: Optional[str] = "Run failed or result not found" if error_flag else None

    bsi: float = 0.0
    optimality_gap: float = 0.0
    agent_output_raw: str = ""
    extracted_choice: Optional[str] = None
    choice_is_correct: bool = False
    optimal_choice: str = ""
    token_count_input: int = 0
    token_count_output: int = 0
    api_cost_usd: float = 0.0
    model_version: str = run_spec["agent_id"]

    if result is not None:
        agent_output_raw = result.get("agent_response_raw", "")
        pillar_scores = result.get("pillar_scores", [])
        if pillar_scores:
            metrics = pillar_scores[0].get("metrics", {})
            bsi = float(metrics.get("bias_susceptibility_index", 0.0))
            optimality_gap = float(metrics.get("optimality_gap", 0.0))

        decisions = (result.get("agent_response") or {}).get("decisions", {})
        extracted_choice = decisions.get("selected_supplier") or decisions.get("supplier")
        optimal_choice = (result.get("scenario") or {}).get("optimal_choice", "")
        choice_is_correct = bool(extracted_choice and extracted_choice == optimal_choice)

        usage = result.get("usage", {}) or {}
        token_count_input = int(usage.get("input_tokens", 0))
        token_count_output = int(usage.get("output_tokens", 0))
        api_cost_usd = float(usage.get("cost_usd", 0.0))
        model_version = result.get("model_version", run_spec["agent_id"]) or run_spec["agent_id"]

    # Derive model_family from agent_id (e.g. "openrouter-openai-gpt-4o" → "openai-gpt-4o")
    parts = run_spec["agent_id"].split("-", 1)
    model_family = parts[1] if len(parts) > 1 else run_spec["agent_id"]

    return RunRecord(
        run_id=run_spec["run_id"],
        session_id=session_id,
        agent_id=run_spec["agent_id"],
        model_family=model_family,
        model_version=model_version,
        scenario_id=run_spec["scenario_id"],
        bias_category=run_spec["bias_category"],
        variant=run_spec["variant"],
        run_index=run_spec["run_index"],
        temperature=run_spec["temperature"],
        prompt_version=run_spec["prompt_version"],
        supplier_order_seed=run_spec["supplier_order_seed"],
        timestamp_utc=datetime.now(timezone.utc),
        agent_output_raw=agent_output_raw,
        extracted_choice=extracted_choice,
        choice_is_correct=choice_is_correct,
        optimal_choice=optimal_choice,
        bsi=max(0.0, min(1.0, bsi)),
        optimality_gap=max(0.0, optimality_gap),
        token_count_input=token_count_input,
        token_count_output=token_count_output,
        api_cost_usd=api_cost_usd,
        error_flag=error_flag,
        error_message=error_message,
    )


# ── Cost estimate ─────────────────────────────────────────────────────────────


def estimate_cost(n_runs: int, cost_per_run_usd: float = 0.15) -> dict:
    """Return a cost summary dict for *n_runs* at *cost_per_run_usd* each."""
    return {
        "n_runs": n_runs,
        "cost_per_run_usd": cost_per_run_usd,
        "estimated_total_usd": n_runs * cost_per_run_usd,
        "note": "Estimate assumes $0.15/run average; actual cost varies by model.",
    }


# ── Main orchestration ────────────────────────────────────────────────────────


def run_experiment(
    manifest_path: Path,
    output_dir: Optional[Path] = None,
    dry_run: bool = False,
    resume: bool = False,
) -> None:
    """Execute the full experiment defined in *manifest_path*.

    Parameters
    ----------
    manifest_path:
        Path to a ``manifest.json`` produced by ``00_define_experiment.py``.
    output_dir:
        Directory for ``runs.jsonl``, ``raw/`` per-run results, and the
        updated manifest.  Defaults to the same directory as *manifest_path*.
    dry_run:
        When ``True``, print the run plan and cost estimate then return
        without invoking any models.
    resume:
        When ``True``, load already-completed run IDs from ``runs.jsonl``
        and skip those cells (restart after crash).
    """
    with open(manifest_path, encoding="utf-8") as fh:
        manifest = json.load(fh)

    session_id: str = manifest["experiment_id"]
    effective_output_dir = output_dir or manifest_path.parent
    effective_output_dir.mkdir(parents=True, exist_ok=True)

    runs = generate_run_plan(manifest)
    jsonl_path = effective_output_dir / "runs.jsonl"

    # ── Dry-run mode ──────────────────────────────────────────────────────────
    if dry_run:
        cost = estimate_cost(
            len(runs), manifest.get("cost_per_run_usd", 0.15)
        )
        sep = "=" * 62
        print(f"\n{sep}")
        print(f"  DRY RUN  —  Experiment: {session_id}")
        print(sep)
        print(f"  Design tier     : {manifest.get('design_tier', 'unknown')}")
        print(f"  Models          : {manifest.get('n_models', len(manifest.get('models', [])))}")
        print(f"  Bias types      : {manifest.get('n_bias_types', '?')}")
        print(f"  Runs per cell   : {manifest.get('n_runs_per_cell', '?')}")
        print(f"  Temperatures    : {manifest.get('temperatures', [])}")
        print(f"  Prompt versions : {manifest.get('prompt_versions', [])}")
        print(f"  Total planned   : {len(runs):,} runs")
        print(f"  Est. API cost   : ${cost['estimated_total_usd']:.2f}  ({cost['note']})")
        print(sep)
        print()
        return

    # ── Resume: load completed run IDs ────────────────────────────────────────
    completed_ids: set[str] = set()
    if resume:
        completed_ids = load_completed_run_ids(jsonl_path)
        print(f"[resume] {len(completed_ids):,} runs already completed — skipping.")

    pending = [r for r in runs if r["run_id"] not in completed_ids]
    print(
        f"Executing {len(pending):,} / {len(runs):,} runs  "
        f"(experiment: {session_id})"
    )

    # Stamp start time on the manifest if not already set
    if not manifest.get("start_time_utc"):
        manifest["start_time_utc"] = datetime.now(timezone.utc).isoformat()
        with open(manifest_path, "w", encoding="utf-8") as fh:
            json.dump(manifest, fh, indent=2)

    total_api_cost = 0.0
    n_errors = 0

    for i, run_spec in enumerate(pending, 1):
        label = (
            f"[{i:>{len(str(len(pending)))}}/{len(pending)}]"
            f"  {run_spec['agent_id']:<50s}"
            f"  {run_spec['scenario_id']:<38s}"
            f"  T={run_spec['temperature']}"
            f"  pv={run_spec['prompt_version']}"
            f"  r={run_spec['run_index']}"
        )
        print(label, end="", flush=True)

        # Each run gets its own isolated output subdirectory
        run_output_dir = effective_output_dir / "raw" / f"run_{run_spec['run_id']}"
        run_output_dir.mkdir(parents=True, exist_ok=True)

        result = _invoke_buyerbench(run_spec, run_output_dir)
        record = build_run_record(run_spec, result, session_id)
        append_run_record(record, jsonl_path)

        if record.error_flag:
            n_errors += 1
            print("  [ERROR]")
        else:
            total_api_cost += record.api_cost_usd
            print(f"  BSI={record.bsi:.3f}  cost=${record.api_cost_usd:.4f}")

    # ── Finalise manifest ─────────────────────────────────────────────────────
    manifest["end_time_utc"] = datetime.now(timezone.utc).isoformat()
    manifest["total_completed_runs"] = (
        len(pending) - n_errors + len(completed_ids)
    )
    manifest["total_api_cost_usd"] = total_api_cost
    with open(manifest_path, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2)

    print()
    print(f"All runs complete.")
    print(f"  Errors          : {n_errors} / {len(pending)}")
    print(f"  Total API cost  : ${total_api_cost:.4f}")
    print(f"  Runs written to : {jsonl_path}")
    print()

    # ── Post-run: invoke aggregation script ───────────────────────────────────
    aggregate_script = (
        Path(__file__).parent.parent / "scripts" / "02_aggregate_results.py"
    )
    if aggregate_script.exists():
        print(f"Running post-run aggregation: {aggregate_script}")
        subprocess.run(
            [
                sys.executable,
                str(aggregate_script),
                "--experiment-dir",
                str(effective_output_dir),
            ]
        )


# ── CLI entry point ───────────────────────────────────────────────────────────


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m research.experiments.run_experiment",
        description=(
            "Orchestrate a Pillar 2 research experiment from a manifest JSON file.\n\n"
            "Typical workflow:\n"
            "  1. python research/scripts/00_define_experiment.py   # create manifest\n"
            "  2. python -m research.experiments.run_experiment manifest.json --dry-run\n"
            "  3. python -m research.experiments.run_experiment manifest.json\n"
            "  4. python research/scripts/02_aggregate_results.py  # auto-invoked"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "manifest",
        type=Path,
        help="Path to manifest.json produced by 00_define_experiment.py",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print plan and cost estimate without invoking any models",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Skip run_ids already present in runs.jsonl (restart after crash)",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        metavar="DIR",
        help=(
            "Directory for runs.jsonl and raw/ per-run results. "
            "Default: same directory as the manifest file."
        ),
    )
    return parser


if __name__ == "__main__":
    args = _build_parser().parse_args()

    if not args.manifest.exists():
        print(f"Error: manifest not found: {args.manifest}", file=sys.stderr)
        sys.exit(1)

    run_experiment(
        manifest_path=args.manifest,
        output_dir=args.output_dir,
        dry_run=args.dry_run,
        resume=args.resume,
    )
