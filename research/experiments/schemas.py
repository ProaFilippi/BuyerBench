"""Research-specific data schemas.

Primary unit of observation: RunRecord (one LLM invocation).
Aggregation unit: CellAggregate (one model × scenario × variant × prompt × temp cell).
Experiment configuration: ExperimentManifest (frozen at run start).
"""
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


@dataclass
class RunRecord:
    """One LLM invocation — primary unit of observation.

    Each row in runs.jsonl corresponds to one RunRecord. Fields are kept
    flat (no nested objects) to allow easy loading into pandas DataFrames
    via ``pd.read_json('runs.jsonl', lines=True)``.
    """

    run_id: str
    """12-char SHA-256 prefix: deterministic hash of cell_key + run_index."""

    session_id: str
    """Parent experiment session ID (from ExperimentManifest.experiment_id)."""

    agent_id: str
    """BuyerBench agent identifier, e.g. 'openrouter-openai-gpt-4o'."""

    model_family: str
    """Canonical model family, e.g. 'gpt-4o', 'claude-3.5-sonnet'."""

    model_version: str
    """Exact model version string returned by the API at run time."""

    scenario_id: str
    """BuyerBench scenario ID, e.g. 'p2-01-anchoring-ANCHOR_HIGH'."""

    bias_category: str
    """Bias category, e.g. 'anchoring', 'framing', 'decoy'."""

    variant: str
    """Scenario variant name: 'baseline' or 'treatment'."""

    run_index: int
    """1-based index within the cell (1 … n_runs_per_cell)."""

    temperature: float
    """Sampling temperature used for this run."""

    prompt_version: str
    """Prompt engineering condition: 'standard' | 'cot' | 'expert_role'."""

    supplier_order_seed: int
    """Seed for deterministic supplier ordering: hash(run_id) % 2**32."""

    timestamp_utc: datetime
    """Wall-clock time at which the API call was initiated."""

    agent_output_raw: str
    """Full raw text output returned by the agent."""

    extracted_choice: Optional[str]
    """Parsed supplier/option choice; None if extraction failed."""

    choice_is_correct: bool
    """True if extracted_choice matches optimal_choice."""

    optimal_choice: str
    """Ground-truth optimal choice for this scenario variant."""

    bsi: float
    """Bias Susceptibility Index for this run (0.0 = rational, 1.0 = fully biased)."""

    optimality_gap: float
    """Economic distance from optimal decision (0.0 = optimal)."""

    token_count_input: int
    """Number of input tokens consumed by this run."""

    token_count_output: int
    """Number of output tokens produced by this run."""

    api_cost_usd: float
    """Estimated API cost in USD for this run."""

    error_flag: bool
    """True if the run encountered an error (API failure, extraction failure, etc.)."""

    error_message: Optional[str]
    """Human-readable error description; None when error_flag is False."""

    def __post_init__(self) -> None:
        if self.bsi < 0.0 or self.bsi > 1.0:
            raise ValueError(f"bsi must be in [0, 1], got {self.bsi}")
        if self.optimality_gap < 0.0:
            raise ValueError(f"optimality_gap must be >= 0, got {self.optimality_gap}")
        if self.run_index < 1:
            raise ValueError(f"run_index must be >= 1, got {self.run_index}")


@dataclass
class CellAggregate:
    """Aggregated statistics for one (model, scenario, variant, prompt, temperature) cell.

    Written to cells.json after all runs in the experiment are complete.
    Each CellAggregate summarises n_runs RunRecord rows.
    """

    cell_id: str
    """Canonical cell key: '{agent_id}__{scenario_id}__{temperature}__{prompt_version}'."""

    agent_id: str
    """BuyerBench agent identifier."""

    scenario_id: str
    """BuyerBench scenario ID."""

    bias_category: str
    """Bias category this cell belongs to."""

    variant: str
    """Scenario variant: 'baseline' or 'treatment'."""

    prompt_version: str
    """Prompt engineering condition."""

    temperature: float
    """Sampling temperature."""

    n_runs: int
    """Total attempted runs in this cell."""

    n_valid_runs: int
    """Runs without error_flag and with a non-None extracted_choice."""

    mean_bsi: float
    """Mean BSI across valid runs in this cell."""

    std_bsi: float
    """Standard deviation of BSI across valid runs."""

    ci_lower_95: float
    """Lower bound of the 95% bootstrap confidence interval for mean_bsi."""

    ci_upper_95: float
    """Upper bound of the 95% bootstrap confidence interval for mean_bsi."""

    choice_rate_correct: float
    """Fraction of valid runs where extracted_choice == optimal_choice."""

    choice_distribution: dict = field(default_factory=dict)
    """Mapping of choice → count across valid runs (e.g. {'SupplierA': 32, 'SupplierB': 18})."""

    mean_optimality_gap: float = 0.0
    """Mean optimality gap across valid runs."""

    treatment_effect: Optional[float] = None
    """BSI_treatment - BSI_baseline; populated only when a paired baseline cell is available."""

    def __post_init__(self) -> None:
        if self.n_valid_runs > self.n_runs:
            raise ValueError(
                f"n_valid_runs ({self.n_valid_runs}) cannot exceed n_runs ({self.n_runs})"
            )
        if not (0.0 <= self.choice_rate_correct <= 1.0):
            raise ValueError(
                f"choice_rate_correct must be in [0, 1], got {self.choice_rate_correct}"
            )


@dataclass
class ExperimentManifest:
    """Frozen configuration for one experiment run.

    Written to manifest.json at run start and never mutated.  The manifest
    is the single source of truth for reproducibility: it records the exact
    grid, git commit, and timing for the experiment.
    """

    experiment_id: str
    """Unique experiment identifier, e.g. 'pillar2-realistic-20260416-120000'."""

    design_tier: str
    """Experiment scale: 'realistic' (N=50), 'flagship' (N=100+CoT), 'pilot_full' (N=30), or 'pilot' (mock)."""

    n_models: int
    """Number of distinct model / agent IDs in the grid."""

    n_bias_types: int
    """Number of distinct bias categories (e.g. 5 for the realistic design)."""

    n_variants_per_bias: int
    """Number of variants per bias (always 2: baseline + treatment)."""

    n_runs_per_cell: int
    """Planned repetitions per (model, scenario, variant, temp, prompt) cell."""

    temperatures: list = field(default_factory=list)
    """List of sampling temperatures used in this experiment (e.g. [0.7])."""

    prompt_versions: list = field(default_factory=list)
    """List of prompt engineering conditions (e.g. ['standard'])."""

    models: list = field(default_factory=list)
    """Ordered list of agent_id strings included in the grid."""

    bias_scenarios: dict = field(default_factory=dict)
    """Mapping: bias_category → {variant_name → scenario_id}."""

    total_planned_runs: int = 0
    """Total number of RunRecords expected when experiment completes."""

    total_completed_runs: int = 0
    """Running count of successfully completed (non-error) runs; updated post-run."""

    total_api_cost_usd: float = 0.0
    """Accumulated API cost in USD; updated post-run."""

    pre_registration_url: Optional[str] = None
    """OSF or AsPredicted pre-registration URL; set before experiment starts."""

    git_commit_hash: str = "unknown"
    """Output of ``git rev-parse HEAD`` at manifest creation time."""

    pinned_model_versions: dict = field(default_factory=dict)
    """Mapping of agent_id → exact model ID string returned by OpenRouter at manifest creation.

    Example: {'openrouter-openai-gpt-4o': 'openai/gpt-4o-2024-11-20', ...}.
    Populated by ``manifest.query_openrouter_model_versions`` at experiment start.
    Empty dict when API is unavailable or for non-OpenRouter agents.
    """

    created_at_utc: Optional[str] = None
    """ISO-8601 UTC timestamp when the manifest was first written to disk."""

    start_time_utc: Optional[str] = None
    """ISO-8601 UTC timestamp when the first run was dispatched."""

    end_time_utc: Optional[str] = None
    """ISO-8601 UTC timestamp when the last run completed (or failed)."""

    _VALID_TIERS = frozenset({"realistic", "robustness_t0", "cot_experiment", "flagship", "pilot_full", "pilot"})

    def __post_init__(self) -> None:
        if self.design_tier not in self._VALID_TIERS:
            raise ValueError(
                f"design_tier must be one of {sorted(self._VALID_TIERS)}, "
                f"got '{self.design_tier}'"
            )
        if self.total_completed_runs > self.total_planned_runs and self.total_planned_runs > 0:
            raise ValueError(
                f"total_completed_runs ({self.total_completed_runs}) exceeds "
                f"total_planned_runs ({self.total_planned_runs})"
            )
