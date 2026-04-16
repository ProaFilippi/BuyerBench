"""ExperimentManifest — frozen pre-run record of experiment configuration (UPGRADE-11).

Written to ``experiment_manifest.json`` in the output directory *before* execution
begins (capturing design intent) and updated once after completion (adding
``total_completed_runs``, ``total_api_cost_usd``, and ``end_time_utc``).

Schema aligns with the H.2 Experiment Manifest definition in the research playbook.
"""
from __future__ import annotations

import json
import subprocess
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from buyerbench.models import EvaluationResult, Scenario


def _get_git_commit_hash() -> str | None:
    """Return the current HEAD commit hash, or ``None`` if unavailable.

    Appends ``-dirty`` if the working tree has uncommitted changes.
    """
    try:
        repo_root = Path(__file__).parent.parent
        commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_root,
            stderr=subprocess.DEVNULL,
        ).decode().strip()
        status = subprocess.check_output(
            ["git", "status", "--porcelain"],
            cwd=repo_root,
            stderr=subprocess.DEVNULL,
        ).decode().strip()
        if status:
            commit += "-dirty"
        return commit
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return None


class ExperimentManifest(BaseModel):
    """Frozen pre-run declaration of experiment configuration.

    Written before the agent execution loop begins so that the experiment
    scope is captured independent of results (supporting pre-registration).
    Updated post-run with completion metadata.
    """

    experiment_id: str
    design_tier: str = "realistic"
    n_models: int
    n_scenarios: int
    n_bias_types: int | None = None
    n_variants_per_bias: int | None = None
    n_runs_per_cell: int
    temperatures: list[float | None] = Field(default_factory=list)
    prompt_versions: list[str] = Field(default_factory=list)
    total_planned_runs: int
    total_completed_runs: int = 0
    total_api_cost_usd: float | None = None
    pre_registration_url: str | None = None
    git_commit_hash: str | None = None
    start_time_utc: str
    end_time_utc: str | None = None
    pillars: list[int] = Field(default_factory=list)
    output_dir: str = ""


def _infer_bias_counts(scenarios: list[Scenario]) -> tuple[int | None, int | None]:
    """Infer ``(n_bias_types, n_variants_per_bias)`` from a Pillar 2 scenario list.

    Returns ``(None, None)`` if the list contains no Pillar 2 scenarios.
    """
    from buyerbench.models import Pillar

    p2 = [s for s in scenarios if s.pillar == Pillar.PILLAR2]
    if not p2:
        return None, None

    pair_ids = {s.variant_pair_id for s in p2 if s.variant_pair_id}
    n_bias_types = len(pair_ids) or None

    pair_counts = Counter(s.variant_pair_id for s in p2 if s.variant_pair_id)
    n_variants_per_bias = max(pair_counts.values()) if pair_counts else None

    return n_bias_types, n_variants_per_bias


def create_manifest(
    *,
    session_id: str,
    agents: list[str],
    scenarios: list[Scenario],
    n_runs: int,
    temperature: float | None,
    prompt_version: str,
    pillars: list[int],
    research_mode: bool,
    output_dir: str,
    started_at: datetime,
) -> ExperimentManifest:
    """Create a pre-run :class:`ExperimentManifest` from CLI configuration.

    Args:
        session_id:     Session identifier (used as ``experiment_id``).
        agents:         List of agent IDs being evaluated.
        scenarios:      Loaded Scenario objects after all CLI filters are applied.
        n_runs:         ``--n-runs`` value.
        temperature:    ``--temperature`` value (``None`` = provider default).
        prompt_version: ``--prompt-version`` value.
        pillars:        Which pillar integers are being tested.
        research_mode:  Whether ``--research-mode`` is active.
        output_dir:     Output directory path.
        started_at:     UTC datetime when the run was initiated.
    """
    n_bias_types, n_variants_per_bias = _infer_bias_counts(scenarios)

    temperatures: list[float | None] = [temperature]
    if research_mode and temperature != 0.0:
        temperatures.append(0.0)

    n_models = len(agents)
    n_scenarios = len(scenarios)
    total_planned = n_models * n_scenarios * n_runs
    if research_mode:
        total_planned *= 2

    return ExperimentManifest(
        experiment_id=session_id,
        design_tier="realistic",
        n_models=n_models,
        n_scenarios=n_scenarios,
        n_bias_types=n_bias_types,
        n_variants_per_bias=n_variants_per_bias,
        n_runs_per_cell=n_runs,
        temperatures=temperatures,
        prompt_versions=[prompt_version],
        total_planned_runs=total_planned,
        total_completed_runs=0,
        total_api_cost_usd=None,
        pre_registration_url=None,
        git_commit_hash=_get_git_commit_hash(),
        start_time_utc=started_at.isoformat(),
        end_time_utc=None,
        pillars=pillars,
        output_dir=output_dir,
    )


def finalize_manifest(
    manifest: ExperimentManifest,
    results: list[EvaluationResult],
    completed_at: datetime,
) -> ExperimentManifest:
    """Return an updated manifest with post-run completion data.

    Args:
        manifest:     The pre-run manifest to update.
        results:      List of ``EvaluationResult`` objects from the run.
        completed_at: UTC datetime when the run completed.

    Returns:
        A new manifest with ``total_completed_runs``, ``total_api_cost_usd``,
        and ``end_time_utc`` populated. The original is not mutated.
    """
    cost_values = [r.api_cost_usd for r in results if r.api_cost_usd is not None]
    total_cost: float | None = sum(cost_values) if cost_values else None

    return manifest.model_copy(
        update={
            "total_completed_runs": len(results),
            "total_api_cost_usd": total_cost,
            "end_time_utc": completed_at.isoformat(),
        }
    )


def write_manifest(manifest: ExperimentManifest, output_dir: str) -> Path:
    """Serialize *manifest* to ``experiment_manifest.json`` in *output_dir*.

    Creates the output directory if it does not exist.

    Returns:
        :class:`~pathlib.Path` to the written file.
    """
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    path = out / "experiment_manifest.json"
    path.write_text(json.dumps(manifest.model_dump(), indent=2, default=str))
    return path
