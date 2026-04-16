"""Experiment manifest creation and freezing.

An ExperimentManifest is created once at run start, frozen to disk as
manifest.json, and never mutated — ensuring full reproducibility.

Reproducibility guarantees (PILLAR2-RESEARCH-06 Section L.4):
- Model versions pinned by querying the OpenRouter /models API at creation time
- supplier_order_seed derived deterministically from run_id (in run_experiment.py)
- git_commit_hash captured via subprocess at manifest creation
- All output files land under ``results/experiments/{experiment_id}/``
"""
from __future__ import annotations

import json
import os
import subprocess
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from urllib.error import URLError
from urllib.request import Request, urlopen

from research.experiments.schemas import ExperimentManifest


# ── Git hash ──────────────────────────────────────────────────────────────────


def get_git_commit_hash() -> str:
    """Return the current HEAD commit hash, or ``'unknown'`` if git unavailable."""
    try:
        return (
            subprocess.check_output(
                ["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL
            )
            .decode()
            .strip()
        )
    except Exception:
        return "unknown"


# ── OpenRouter model version pinning ─────────────────────────────────────────

_OPENROUTER_MODELS_URL = "https://openrouter.ai/api/v1/models"


def _agent_id_to_openrouter_slug(agent_id: str) -> str:
    """Map a BuyerBench agent_id to an OpenRouter model slug.

    Examples
    --------
    ``'openrouter-openai-gpt-4o'``           → ``'openai/gpt-4o'``
    ``'openrouter-anthropic-claude-3.5-sonnet'`` → ``'anthropic/claude-3.5-sonnet'``
    ``'openrouter-meta-llama-llama-3.1-405b-instruct'`` → ``'meta-llama/llama-3.1-405b-instruct'``
    """
    without_prefix = agent_id[len("openrouter-"):]
    # The provider portion ends at the first '-'; everything after is model name.
    # However some providers contain a hyphen themselves (e.g. 'meta-llama').
    # We rely on the known provider list to split correctly.
    _KNOWN_PROVIDERS = {
        "openai",
        "anthropic",
        "google",
        "meta-llama",
        "mistralai",
        "deepseek",
        "qwen",
        "cohere",
        "01-ai",
    }
    for provider in sorted(_KNOWN_PROVIDERS, key=len, reverse=True):
        if without_prefix.startswith(provider + "-"):
            model_part = without_prefix[len(provider) + 1:]
            return f"{provider}/{model_part}"
    # Fallback: split on first hyphen
    parts = without_prefix.split("-", 1)
    return "/".join(parts) if len(parts) == 2 else without_prefix


def query_openrouter_model_versions(
    agent_ids: list[str],
    api_key: Optional[str] = None,
) -> dict[str, str]:
    """Query the OpenRouter ``/api/v1/models`` endpoint to pin exact model IDs.

    Parameters
    ----------
    agent_ids:
        List of BuyerBench agent IDs, e.g. ``['openrouter-openai-gpt-4o', ...]``.
        Non-``openrouter-*`` agent IDs are silently skipped.
    api_key:
        OpenRouter API key.  Falls back to ``OPENROUTER_API_KEY`` env var.
        If neither is available, returns ``{agent_id: 'version-unknown'}`` for
        every OpenRouter agent without raising.

    Returns
    -------
    dict mapping ``agent_id → pinned OpenRouter model ID string``.

    The returned ID is the canonical ``id`` field from the OpenRouter model
    catalogue (e.g. ``'openai/gpt-4o-2024-11-20'``), which may differ from
    the shorthand slug used when submitting requests.  Storing this value
    allows exact reproduction even when the OpenRouter default for a model
    family is later updated.
    """
    effective_key = api_key or os.environ.get("OPENROUTER_API_KEY", "")

    openrouter_agents = [a for a in agent_ids if a.startswith("openrouter-")]
    if not openrouter_agents:
        return {}

    if not effective_key:
        return {a: "version-unknown" for a in openrouter_agents}

    try:
        req = Request(
            _OPENROUTER_MODELS_URL,
            headers={
                "Authorization": f"Bearer {effective_key}",
                "HTTP-Referer": "https://github.com/buyerbench/buyerbench",
            },
        )
        with urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
        models_by_id: dict[str, dict] = {m["id"]: m for m in data.get("data", [])}
    except (URLError, Exception):
        return {a: "version-unknown" for a in openrouter_agents}

    result: dict[str, str] = {}
    for agent_id in openrouter_agents:
        slug = _agent_id_to_openrouter_slug(agent_id)
        if slug in models_by_id:
            result[agent_id] = models_by_id[slug]["id"]
        else:
            # Try a prefix match (slug may be a shorthand for a versioned ID)
            matches = [mid for mid in models_by_id if mid.startswith(slug)]
            result[agent_id] = matches[0] if len(matches) == 1 else f"{slug}:pinned-unknown"

    return result


# ── Manifest creation ─────────────────────────────────────────────────────────


def create_manifest(
    design: dict,
    pin_model_versions: bool = True,
    openrouter_api_key: Optional[str] = None,
) -> ExperimentManifest:
    """Build and return an :class:`ExperimentManifest` from a design dict.

    Parameters
    ----------
    design:
        Design configuration dict (see ``REALISTIC_DESIGN`` in
        ``research/scripts/00_define_experiment.py``).  Required keys:
        ``design_tier``, ``models``, ``bias_scenarios``, ``n_runs_per_cell``,
        ``temperatures``, ``prompt_versions``.
    pin_model_versions:
        When ``True`` (default), call :func:`query_openrouter_model_versions`
        and store the result in ``manifest.pinned_model_versions``.
    openrouter_api_key:
        Optional override for the OpenRouter API key.  Falls back to
        ``OPENROUTER_API_KEY`` env var when ``None``.

    Returns
    -------
    :class:`ExperimentManifest` with all reproducibility fields populated.
    The manifest is NOT yet written to disk; call :func:`freeze_manifest` next.
    """
    models: list[str] = design["models"]
    bias_scenarios: dict = design["bias_scenarios"]
    temperatures: list[float] = design["temperatures"]
    prompt_versions: list[str] = design["prompt_versions"]
    n_runs_per_cell: int = design["n_runs_per_cell"]
    design_tier: str = design["design_tier"]

    n_variants_per_bias = (
        max(len(v) for v in bias_scenarios.values()) if bias_scenarios else 0
    )
    total_planned_runs = (
        len(models)
        * len(bias_scenarios)
        * n_variants_per_bias
        * len(temperatures)
        * len(prompt_versions)
        * n_runs_per_cell
    )

    now_utc = datetime.now(timezone.utc)
    experiment_id = f"pillar2-{design_tier}-{now_utc.strftime('%Y%m%d-%H%M%S')}"

    pinned: dict[str, str] = {}
    if pin_model_versions:
        pinned = query_openrouter_model_versions(models, api_key=openrouter_api_key)

    return ExperimentManifest(
        experiment_id=experiment_id,
        design_tier=design_tier,
        n_models=len(models),
        n_bias_types=len(bias_scenarios),
        n_variants_per_bias=n_variants_per_bias,
        n_runs_per_cell=n_runs_per_cell,
        temperatures=list(temperatures),
        prompt_versions=list(prompt_versions),
        models=list(models),
        bias_scenarios=dict(bias_scenarios),
        total_planned_runs=total_planned_runs,
        total_completed_runs=0,
        total_api_cost_usd=0.0,
        pre_registration_url=None,
        git_commit_hash=get_git_commit_hash(),
        pinned_model_versions=pinned,
        created_at_utc=now_utc.isoformat(),
        start_time_utc=None,
        end_time_utc=None,
    )


# ── Manifest I/O ─────────────────────────────────────────────────────────────


def freeze_manifest(manifest: ExperimentManifest, output_dir: Path) -> Path:
    """Write *manifest* to disk and create the experiment directory layout.

    Creates the following structure under ``output_dir / manifest.experiment_id``:

    .. code-block:: text

        {experiment_id}/
        ├── manifest.json   ← frozen here; raises FileExistsError if already present
        ├── runs.jsonl      ← written by run_experiment.py (append-mode)
        ├── cells.json      ← written by 02_aggregate_results.py
        ├── raw/            ← per-run subprocess output directories
        ├── figures/        ← generated plots
        └── tables/         ← LaTeX + CSV tables

    Parameters
    ----------
    manifest:
        :class:`ExperimentManifest` instance to persist.
    output_dir:
        Parent directory under which ``{experiment_id}/`` is created.
        Typically ``results/experiments/``.

    Returns
    -------
    :class:`pathlib.Path` pointing to the written ``manifest.json``.

    Raises
    ------
    FileExistsError
        If ``manifest.json`` already exists in the target directory (prevents
        accidental overwrite of a frozen manifest).
    """
    exp_dir = output_dir / manifest.experiment_id
    exp_dir.mkdir(parents=True, exist_ok=True)
    for sub in ("raw", "figures", "tables"):
        (exp_dir / sub).mkdir(exist_ok=True)

    manifest_path = exp_dir / "manifest.json"
    if manifest_path.exists():
        raise FileExistsError(
            f"Manifest already exists at {manifest_path}. "
            "Delete it or use a different output_dir to create a new experiment."
        )

    data = asdict(manifest)
    manifest_path.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")
    return manifest_path


def load_manifest(manifest_path: Path) -> dict:
    """Read and return the manifest as a plain dict from *manifest_path*."""
    return json.loads(manifest_path.read_text(encoding="utf-8"))
