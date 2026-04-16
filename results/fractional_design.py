"""Fractional factorial design orchestrator for BuyerBench experiments (UPGRADE-12).

Given experiment dimensions (agent IDs, scenario IDs, prompt versions, temperatures,
n_runs per cell), auto-generates a fractional factorial run plan that maximises
coverage while minimising total API calls. Outputs a run plan CSV and summary stats.

Background
----------
The full prompt × temperature design space for a flagship experiment has
3 × 4 = 12 treatment combinations per (scenario, model). A 1/3 fractional
factorial — selecting 4 representative (prompt_version, temperature) pairs that
permit estimation of main effects for both factors independently — reduces total
runs by ~55%.

See Section H.4 of PILLAR2-RESEARCH-04.md for the research design rationale.

Modes
-----
``"full"``
    All combinations of prompt_versions × temperatures (full factorial).

``"preset"``
    The hardcoded 4-cell BuyerBench L4-analogous design:
      (standard, 0.0), (standard, 0.7), (cot, 1.0), (expert_role, 0.3)
    Valid only for the standard 3-prompt × 4-temperature flagship setup.
    Raises ``ValueError`` if the supplied factor levels do not match.

``"auto"`` *(default)*
    Greedy covering design: assigns temperatures to prompt_versions in
    round-robin order (sorted ascending) so every level of both factors
    appears at least once. Produces ``max(len(prompt_versions),
    len(temperatures))`` combinations — the theoretical minimum for a
    covering design (Resolution-III for 2 factors).
"""
from __future__ import annotations

import csv
import itertools
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

# ── Constants ─────────────────────────────────────────────────────────────────

#: The 4-cell BuyerBench preset analogous to an L4 Taguchi orthogonal array.
#: Resolution-III: estimates main effects of prompt_version and temperature
#: independently while aliasing the interaction with higher-order terms.
BUYERBENCH_PRESET: list[tuple[str, float | None]] = [
    ("standard", 0.0),
    ("standard", 0.7),
    ("cot", 1.0),
    ("expert_role", 0.3),
]

#: Expected factor levels for the preset mode.
PRESET_PROMPT_VERSIONS: tuple[str, ...] = ("standard", "cot", "expert_role")
PRESET_TEMPERATURES: tuple[float, ...] = (0.0, 0.3, 0.7, 1.0)

DesignMode = Literal["full", "preset", "auto"]

CSV_FIELDNAMES: tuple[str, ...] = (
    "run_plan_id",
    "agent_id",
    "scenario_id",
    "prompt_version",
    "temperature",
    "run_index",
    "cell_id",
    "treatment_combination",
    "bias_category",
)


# ── Data classes ──────────────────────────────────────────────────────────────


@dataclass
class RunPlanRow:
    """One row in the run plan CSV — a single (agent, scenario, treatment, repeat) triple."""

    run_plan_id: int
    agent_id: str
    scenario_id: str
    prompt_version: str
    temperature: float | None
    run_index: int
    cell_id: str
    treatment_combination: str
    bias_category: str = ""


@dataclass
class RunPlanSummary:
    """Summary statistics for a generated run plan."""

    mode: str
    n_agents: int
    n_scenarios: int
    n_treatment_combinations: int
    n_runs_per_cell: int
    total_planned_runs: int
    full_factorial_runs: int
    reduction_pct: float
    treatment_combinations: list[tuple[str, float | None]]
    generated_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


# ── Internal helpers ──────────────────────────────────────────────────────────


_COMPOUND_BIAS_SLUGS: dict[str, str] = {
    # Maps the primary slug (parts[2]) to a compound bias category name when the
    # following lowercase segment is part of the category name, not the variant.
    "sunk": "sunk_cost",          # p2-05-sunk-cost-BASELINE
    "loss": "loss_aversion",      # p2-07-loss-aversion-LOSS_AVERSION
}


def _infer_bias_category(scenario_id: str) -> str:
    """Infer bias category from scenario_id using the BuyerBench naming convention.

    Returns the bias category slug (e.g. ``"anchoring"``, ``"sunk_cost"``,
    ``"loss_aversion"``, ``"warp"``), or an empty string if the scenario_id does
    not follow the ``p2-NN-<slug>-VARIANT`` pattern.

    The variant suffix is distinguished from the bias slug by being all-uppercase
    (e.g. ``"BASELINE"``, ``"ANCHOR_HIGH"``, ``"FRAMING_LOSS"``).

    Examples::

        "p2-01-anchor-high-BASELINE"      → "anchor"
        "p2-02-framing-FRAMING_LOSS"      → "framing"
        "p2-05-sunk-cost-BASELINE"        → "sunk_cost"
        "p2-07-loss-aversion-LOSS_AVERSION" → "loss_aversion"
        "p2-08-warp-WARP_AB"              → "warp"
        "p1-01-supplier-discovery"        → ""   (not Pillar-2)
    """
    if not scenario_id:
        return ""
    parts = scenario_id.split("-")
    # Must start with "p2" to be a Pillar-2 scenario
    if len(parts) < 3 or parts[0] != "p2":
        return ""
    # parts[2] is the primary bias slug (always lowercase in BuyerBench naming)
    primary = parts[2].lower()
    # Handle known compound bias slugs: "sunk-cost" and "loss-aversion".
    # The compound extension is the segment at parts[3] when it is lowercase
    # (variant suffixes are all-uppercase, e.g. "BASELINE", "FRAMING_LOSS").
    if primary in _COMPOUND_BIAS_SLUGS and len(parts) > 3 and not parts[3].isupper():
        return _COMPOUND_BIAS_SLUGS[primary]
    return primary


def _cell_id(
    agent_id: str,
    scenario_id: str,
    prompt_version: str,
    temperature: float | None,
) -> str:
    """Construct the composite cell identifier."""
    temp_str = "" if temperature is None else str(temperature)
    return f"{agent_id}__{scenario_id}__{prompt_version}__{temp_str}"


def _treatment_label(prompt_version: str, temperature: float | None) -> str:
    """Human-readable treatment combination label."""
    temp_str = "default" if temperature is None else f"T={temperature}"
    return f"{prompt_version}×{temp_str}"


# ── Core design selection ─────────────────────────────────────────────────────


def select_treatment_combinations(
    prompt_versions: list[str],
    temperatures: list[float | None],
    mode: DesignMode = "auto",
) -> list[tuple[str, float | None]]:
    """Select the (prompt_version, temperature) treatment combinations for the experiment.

    Args:
        prompt_versions: Ordered list of prompt version labels (e.g. ``["standard",
            "cot", "expert_role"]``). Must be non-empty.
        temperatures: Ordered list of temperature values to include. ``None`` means
            "use provider default". Must be non-empty.
        mode: Design mode — ``"full"``, ``"preset"``, or ``"auto"`` (default).

    Returns:
        Ordered list of ``(prompt_version, temperature)`` tuples representing the
        selected treatment combinations.

    Raises:
        ValueError: If *mode* is invalid, or if *mode* is ``"preset"`` but the
            supplied factor levels do not match the hardcoded preset.
    """
    if not prompt_versions:
        raise ValueError("prompt_versions must be non-empty")
    if not temperatures:
        raise ValueError("temperatures must be non-empty")

    if mode == "full":
        return list(itertools.product(prompt_versions, temperatures))

    if mode == "preset":
        # Validate that the supplied levels match the preset expectations
        supplied_prompts = set(prompt_versions)
        supplied_temps = {t for t in temperatures if t is not None}
        expected_prompts = set(PRESET_PROMPT_VERSIONS)
        expected_temps = set(PRESET_TEMPERATURES)
        if supplied_prompts != expected_prompts or supplied_temps != expected_temps:
            raise ValueError(
                f"Preset mode requires prompt_versions={sorted(expected_prompts)} "
                f"and temperatures={sorted(expected_temps)}. "
                f"Got prompt_versions={sorted(supplied_prompts)}, "
                f"temperatures={sorted(str(t) for t in supplied_temps)}."
            )
        return list(BUYERBENCH_PRESET)

    if mode == "auto":
        # Greedy covering design: round-robin assignment of temperatures to prompt_versions.
        #
        # Sort temperatures (None last) so numeric ordering is preserved; cycle
        # through prompt_versions so every version appears at least once.
        #
        # Result: max(len(prompt_versions), len(temperatures)) combinations —
        # the theoretical minimum covering design for 2 factors.
        sorted_temps: list[float | None] = sorted(
            temperatures, key=lambda t: (t is None, t or 0.0)
        )
        prompt_cycle = itertools.cycle(prompt_versions)
        seen: set[tuple[str, float | None]] = set()
        selected: list[tuple[str, float | None]] = []
        for temp in sorted_temps:
            prompt = next(prompt_cycle)
            combo = (prompt, temp)
            if combo not in seen:
                seen.add(combo)
                selected.append(combo)
        return selected

    raise ValueError(f"Unknown design mode: {mode!r}. Expected 'full', 'preset', or 'auto'.")


# ── Public API ────────────────────────────────────────────────────────────────


def generate_run_plan(
    *,
    agent_ids: list[str],
    scenario_ids: list[str],
    prompt_versions: list[str],
    temperatures: list[float | None],
    n_runs: int = 1,
    mode: DesignMode = "auto",
) -> tuple[list[RunPlanRow], RunPlanSummary]:
    """Generate a fractional factorial run plan.

    Args:
        agent_ids:       List of agent identifiers to include.
        scenario_ids:    List of scenario identifiers to include.
        prompt_versions: Prompt version labels (e.g. ``["standard", "cot"]``).
        temperatures:    Temperature values (``None`` = provider default).
        n_runs:          Number of independent repeat runs per cell (≥1).
        mode:            Design mode — ``"full"``, ``"preset"``, or ``"auto"``.

    Returns:
        A tuple of:
          - ``rows``: ordered list of :class:`RunPlanRow` objects (one per API call).
          - ``summary``: :class:`RunPlanSummary` with coverage and reduction stats.

    Raises:
        ValueError: If any input list is empty, ``n_runs < 1``, or *mode* is invalid.
    """
    if not agent_ids:
        raise ValueError("agent_ids must be non-empty")
    if not scenario_ids:
        raise ValueError("scenario_ids must be non-empty")
    if n_runs < 1:
        raise ValueError(f"n_runs must be ≥1, got {n_runs}")

    combos = select_treatment_combinations(prompt_versions, temperatures, mode=mode)

    rows: list[RunPlanRow] = []
    row_id = 1
    for agent_id in agent_ids:
        for scenario_id in scenario_ids:
            for prompt_ver, temp in combos:
                for run_idx in range(1, n_runs + 1):
                    rows.append(
                        RunPlanRow(
                            run_plan_id=row_id,
                            agent_id=agent_id,
                            scenario_id=scenario_id,
                            prompt_version=prompt_ver,
                            temperature=temp,
                            run_index=run_idx,
                            cell_id=_cell_id(agent_id, scenario_id, prompt_ver, temp),
                            treatment_combination=_treatment_label(prompt_ver, temp),
                            bias_category=_infer_bias_category(scenario_id),
                        )
                    )
                    row_id += 1

    n_full = (
        len(agent_ids) * len(scenario_ids) * len(prompt_versions) * len(temperatures) * n_runs
    )
    total = len(rows)
    reduction = 100.0 * (1.0 - total / n_full) if n_full > 0 else 0.0

    summary = RunPlanSummary(
        mode=mode,
        n_agents=len(agent_ids),
        n_scenarios=len(scenario_ids),
        n_treatment_combinations=len(combos),
        n_runs_per_cell=n_runs,
        total_planned_runs=total,
        full_factorial_runs=n_full,
        reduction_pct=round(reduction, 1),
        treatment_combinations=combos,
    )
    return rows, summary


def write_run_plan_csv(rows: list[RunPlanRow], output_path: str | Path) -> Path:
    """Write a run plan to a CSV file.

    Args:
        rows:        List of :class:`RunPlanRow` objects from :func:`generate_run_plan`.
        output_path: Destination path for the CSV file. Parent directories are
                     created automatically.

    Returns:
        Resolved :class:`~pathlib.Path` to the written file.
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(CSV_FIELDNAMES))
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "run_plan_id": row.run_plan_id,
                    "agent_id": row.agent_id,
                    "scenario_id": row.scenario_id,
                    "prompt_version": row.prompt_version,
                    "temperature": "" if row.temperature is None else row.temperature,
                    "run_index": row.run_index,
                    "cell_id": row.cell_id,
                    "treatment_combination": row.treatment_combination,
                    "bias_category": row.bias_category,
                }
            )
    return path.resolve()
