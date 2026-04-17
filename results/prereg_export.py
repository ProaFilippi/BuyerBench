"""Pre-registration export for BuyerBench Pillar 2 (UPGRADE-15).

Generates an OSF-compatible structured pre-registration Markdown document from
an :class:`~results.experiment_manifest.ExperimentManifest` plus the hardcoded
hypothesis definitions (H1–H10) drawn from the research design documents.

The output is a self-contained ``prereg_osf.md`` file structured to match the
OSF Standard Pre-Registration template fields, usable for direct upload to
https://osf.io/prereg/ or equivalent registries (AsPredicted, EGAP).

No external dependencies — pure Python stdlib only.

Typical usage::

    from results.experiment_manifest import ExperimentManifest
    from results.prereg_export import generate_prereg_document, write_prereg_document

    manifest = ExperimentManifest(...)
    doc = generate_prereg_document(manifest)
    path = write_prereg_document(doc, "results/my-experiment")
    # → results/my-experiment/prereg_osf.md

CLI::

    python -m buyerbench prereg \\
        --manifest results/my-experiment/experiment_manifest.json \\
        --output-dir results/my-experiment/

    # Standalone mode — no manifest required; uses planned experiment defaults:
    python -m buyerbench prereg --standalone --output-dir docs/preregistration/
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from textwrap import dedent
from typing import Literal

from pydantic import BaseModel, Field

from results.experiment_manifest import ExperimentManifest


# ─────────────────────────────────────────────────────────────────────────────
# §1  HYPOTHESIS DEFINITIONS  (hardcoded from d1 / d2 research design docs)
# ─────────────────────────────────────────────────────────────────────────────

class HypothesisDef(BaseModel):
    """A single pre-specified hypothesis for registration."""

    id: str  # e.g. "H1"
    label: str  # Short descriptive label
    prq_dimension: str  # Which PRQ dimension this addresses
    statement: str  # Full testable statement
    direction: Literal["positive", "negative", "null", "non_directional"]
    analysis_type: Literal["confirmatory", "exploratory"] = "exploratory"
    test: str  # Statistical test planned
    null_outcome: str  # What a null result means
    data_requirement: str  # Minimum data needed to test


#: Hardcoded hypothesis set from docs/paper/hypotheses/d1 and d2.
#: These are fixed at pre-registration time and must not be changed after
#: data collection begins.
#:
#: Confirmatory hypotheses (H1, H3, H5, H7) are the primary inferential engine.
#: BH-FDR correction is applied to these 4 hypotheses only.
#: All other hypotheses (H2, H4, H6, H8, H9, H10) are pre-specified as
#: exploratory — results are descriptive or depend on future data.
CONFIRMATORY_HYPOTHESIS_IDS: frozenset[str] = frozenset({"H1", "H3", "H5", "H7"})

BUYERBENCH_HYPOTHESES: list[HypothesisDef] = [
    HypothesisDef(
        id="H1",
        label="Bias Universality",
        prq_dimension="D1: Existence",
        statement=(
            "LLM agents exhibit non-trivial bias susceptibility (BSI > 0.10 with 95% CI "
            "excluding zero) for at least one bias type, in at least five of ten tested models."
        ),
        direction="positive",
        analysis_type="confirmatory",
        test=(
            "Per-bias-type one-sample t-test (H₀: BSI = 0) aggregated across models; "
            "BH-FDR correction at q = 0.05 across 5 tests."
        ),
        null_outcome=(
            "If BSI ≈ 0 across all bias types, the finding is 'domain structure suppresses "
            "bias susceptibility' — a valid contribution, not a failed study."
        ),
        data_requirement="N ≥ 30 runs per (model × bias type × variant) cell.",
    ),
    HypothesisDef(
        id="H2",
        label="Capability-Bias Tradeoff",
        prq_dimension="D3: Capability variation",
        statement=(
            "There is a negative Spearman rank correlation between Pillar 1 composite score "
            "(agent capability proxy) and mean BSI across bias types at the model level."
        ),
        direction="negative",
        test=(
            "Spearman rank correlation (ρ) between pillar1_score and mean_BSI across N = 10 models. "
            "OLS regression flagged as descriptive only (N = 10 is below inference threshold)."
        ),
        null_outcome=(
            "Higher-capability models show equal or greater bias susceptibility, consistent with "
            "Hagendorff et al. (2023) 'reverse capability' effect in cognitive tasks."
        ),
        data_requirement="Pillar 1 scores for all 10 models + full Pillar 2 BSI battery.",
    ),
    HypothesisDef(
        id="H3",
        label="Decoy Effect Reliability",
        prq_dimension="D2: Bias type variation",
        statement=(
            "The decoy bias type (p2-03) produces a BSI significantly greater than zero "
            "and higher than the mean BSI across all other bias types."
        ),
        direction="positive",
        analysis_type="confirmatory",
        test=(
            "One-sample t-test (decoy BSI > 0); pairwise contrast between decoy mean_BSI "
            "and grand mean across remaining 4 bias types (Dunnett or Tukey HSD post-hoc)."
        ),
        null_outcome=(
            "Decoy manipulation fails to reliably shift supplier choice in structured procurement "
            "scenarios — explicit cost/quality rubrics suppress asymmetric dominance effects."
        ),
        data_requirement="N ≥ 30 per (model × variant) cell for p2-03.",
    ),
    HypothesisDef(
        id="H4",
        label="Anchoring Magnitude Proportionality",
        prq_dimension="D2: Bias type variation",
        statement=(
            "BSI for high-magnitude anchoring (p2-01, ANCHOR_HIGH) is greater than for "
            "low-magnitude anchoring (p2-01b, ANCHOR_LOW), demonstrating proportionality."
        ),
        direction="positive",
        test="Paired t-test comparing BSI_HIGH vs BSI_LOW across models.",
        null_outcome=(
            "Anchoring effect magnitude does not scale with anchor distance from market price; "
            "LLMs may exhibit threshold-based rather than continuous anchoring susceptibility."
        ),
        data_requirement=(
            "Requires p2-01b (ANCHOR_LOW scenario) — not yet implemented. "
            "H4 is flagged as a design limitation until p2-01b is run."
        ),
    ),
    HypothesisDef(
        id="H5",
        label="Framing Asymmetry (Loss > Gain)",
        prq_dimension="D2: Bias type variation",
        statement=(
            "The LOSS frame (p2-02, FRAMING_LOSS) produces higher BSI than the GAIN frame "
            "(p2-02, FRAMING_GAIN), consistent with loss aversion predictions."
        ),
        direction="positive",
        analysis_type="confirmatory",
        test="Paired t-test: mean BSI under FRAMING_LOSS vs FRAMING_GAIN across models.",
        null_outcome=(
            "No framing asymmetry — LLMs respond symmetrically to gain and loss frames, "
            "suggesting RLHF training has suppressed loss aversion in structured domains."
        ),
        data_requirement="N ≥ 30 per (model × variant) cell for p2-02.",
    ),
    HypothesisDef(
        id="H6",
        label="Sunk Cost × Capability Non-Monotone Interaction",
        prq_dimension="D2/D3: Bias × capability interaction",
        statement=(
            "High-capability models show greater sunk cost susceptibility than low-capability "
            "models, producing a positive (not negative) capability–BSI slope for p2-05."
        ),
        direction="positive",
        test=(
            "Spearman correlation between pillar1_score and BSI_sunk_cost. "
            "Expected sign: positive (opposite to H2 overall direction)."
        ),
        null_outcome=(
            "Sunk cost susceptibility decreases with capability (consistent with H2), "
            "suggesting structured rubrics override narrative cost-justification reasoning."
        ),
        data_requirement="Pillar 1 scores + N ≥ 30 per (model × variant) cell for p2-05.",
    ),
    HypothesisDef(
        id="H7",
        label="Stochastic Variance Proportional to BSI",
        prq_dimension="D4: Stochastic vs. systematic variance",
        statement=(
            "Within-cell variance (std_bsi) is positively correlated with mean BSI across "
            "all cells, consistent with a boundary-response mechanism."
        ),
        direction="positive",
        analysis_type="confirmatory",
        test=(
            "OLS regression: std_bsi ~ β₀ + β₁·mean_bsi. "
            "Significant positive β₁ supports H7."
        ),
        null_outcome=(
            "No variance–mean relationship; BSI variance is uniform across susceptibility "
            "levels, suggesting stochastic noise is independent of bias signal."
        ),
        data_requirement="N ≥ 2 runs per cell to estimate within-cell variance.",
    ),
    HypothesisDef(
        id="H8",
        label="CoT Reduces Anchoring but Not Decoy",
        prq_dimension="D4: Prompt moderation",
        statement=(
            "Chain-of-thought prompting reduces anchoring BSI (p2-01) but does not reduce "
            "— and may increase — decoy BSI (p2-03), producing a significant bias_type × "
            "prompt_version interaction."
        ),
        direction="non_directional",
        test=(
            "2×2 ANOVA: BSI ~ bias_type × prompt_version (standard | cot). "
            "Key interaction contrast: Δ(decoy CoT − decoy standard) > Δ(anchor CoT − anchor standard)."
        ),
        null_outcome=(
            "CoT has no differential effect — structured procurement prompts already engage "
            "sufficient deliberate reasoning to suppress both effects equally."
        ),
        data_requirement="CoT prompt variants for p2-01 and p2-03 (requires UPGRADE-7).",
    ),
    HypothesisDef(
        id="H9",
        label="Model-Specific Bias Profiles",
        prq_dimension="D3: Model-specific patterns",
        statement=(
            "Cronbach's alpha across the 5-dimension BSI vector (one dimension per bias type) "
            "is low (< 0.50) across the 10-model sample, indicating bias-specific rather "
            "than general susceptibility patterns."
        ),
        direction="null",
        test=(
            "Cronbach's alpha on [BSI_anchor, BSI_frame, BSI_decoy, BSI_scar, BSI_sunk] "
            "across N = 10 models. Spearman inter-bias correlation matrix. "
            "Hierarchical clustering (Ward linkage, Euclidean distance in 5D BSI space)."
        ),
        null_outcome=(
            "High alpha (> 0.70) implies a general bias susceptibility factor — "
            "a surprising finding that would suggest 'rationality' is a single latent trait."
        ),
        data_requirement="Complete BSI estimates for all 5 bias types × all 10 models.",
    ),
    HypothesisDef(
        id="H10",
        label="Human Benchmark Calibration",
        prq_dimension="D5: Human comparison",
        statement=(
            "LLM BSI effect sizes (Cohen's d vs. 0) are smaller than human meta-analytic "
            "benchmarks for the same bias categories from behavioral economics literature."
        ),
        direction="negative",
        test=(
            "Per-bias-type Cohen's d comparison between BuyerBench LLM estimates and "
            "published human baselines: anchoring (d ≈ 2.7), framing (d ≈ 1.8), "
            "decoy (d ≈ 0.4), sunk cost (d ≈ 0.85), scarcity (d ≈ 0.60–0.80). "
            "For human arm data: independent two-sample Welch t-test on BSI."
        ),
        null_outcome=(
            "LLM effect sizes match or exceed human benchmarks — LLMs are as or more "
            "susceptible than humans to behavioral biases in structured procurement tasks."
        ),
        data_requirement=(
            "Multi-run BSI estimates for all 5 bias types. "
            "Human comparison arm requires UPGRADE-13 + IRB approval (Phase 4)."
        ),
    ),
]


# ─────────────────────────────────────────────────────────────────────────────
# §2  DOCUMENT MODEL
# ─────────────────────────────────────────────────────────────────────────────

class PreregistrationDocument(BaseModel):
    """Structured pre-registration document for BuyerBench Pillar 2."""

    title: str
    authors: str = "BuyerBench Research Team"
    generated_at: str
    manifest_experiment_id: str
    manifest_git_hash: str | None
    manifest_design_tier: str
    manifest_n_models: int
    manifest_n_scenarios: int
    manifest_n_runs_per_cell: int
    manifest_temperatures: list[float | None]
    manifest_prompt_versions: list[str]
    manifest_total_planned_runs: int
    manifest_pre_registration_url: str | None
    hypotheses: list[HypothesisDef] = Field(default_factory=list)
    primary_outcome: str
    secondary_outcomes: list[str] = Field(default_factory=list)
    bias_types_tested: list[str] = Field(default_factory=list)
    model_set: list[str] = Field(default_factory=list)
    bsi_significance_threshold: str
    alpha_level: float
    fdr_q_level: float
    null_result_framing: str
    exclusion_criteria: list[str] = Field(default_factory=list)
    stopping_rule: str


# ─────────────────────────────────────────────────────────────────────────────
# §3  DOCUMENT GENERATION
# ─────────────────────────────────────────────────────────────────────────────

#: Fixed model set from the BuyerBench registry (CLAUDE.md / model_catalog.py).
_DEFAULT_MODEL_SET: list[str] = [
    "openai/gpt-4o",
    "anthropic/claude-3.5-sonnet",
    "google/gemini-pro-1.5",
    "meta-llama/llama-3.1-405b-instruct",
    "mistralai/mistral-large",
    "mistralai/mixtral-8x22b-instruct",
    "deepseek/deepseek-chat",
    "qwen/qwen-2.5-72b-instruct",
    "cohere/command-r-plus",
    "01-ai/yi-large",
]

#: Fixed bias type set for the Realistic Design (5 core bias types).
_DEFAULT_BIAS_TYPES: list[str] = [
    "anchoring",
    "framing",
    "decoy",
    "scarcity",
    "sunk_cost",
]


#: Planned experiment parameters for the Realistic Design (N=50 per cell).
#: These constants represent the intended experiment configuration and are used
#: to generate pre-registration documents BEFORE data collection begins.
_PLANNED_N_RUNS_PER_CELL: int = 50
_PLANNED_EXPERIMENT_ID: str = "buyerbench-pillar2-realistic-v1"
_PLANNED_DESIGN_TIER: str = "realistic"
_PLANNED_N_SCENARIOS: int = 10  # 5 bias types × 2 variants each
_PLANNED_N_BIAS_TYPES: int = 5
_PLANNED_N_VARIANTS_PER_BIAS: int = 2
_PLANNED_TEMPERATURES: list[float | None] = [0.7]
_PLANNED_PROMPT_VERSIONS: list[str] = ["standard"]


def build_planned_manifest(
    *,
    experiment_id: str = _PLANNED_EXPERIMENT_ID,
    n_runs_per_cell: int = _PLANNED_N_RUNS_PER_CELL,
    temperatures: list[float | None] | None = None,
    prompt_versions: list[str] | None = None,
    git_commit_hash: str | None = None,
    pre_registration_url: str | None = None,
) -> ExperimentManifest:
    """Build a *planned* :class:`~results.experiment_manifest.ExperimentManifest`.

    Creates a synthetic manifest representing the *intended* experiment design
    before any data collection begins.  This is the correct input for
    :func:`build_prereg_document` when pre-registering on OSF ahead of running
    the experiment.

    The planned manifest uses the Realistic Design defaults:
      * 10 models (OpenRouter registry)
      * 10 scenarios (5 bias types × 2 variants each)
      * N = 50 runs per cell
      * Temperature = 0.7
      * Prompt version = "standard"

    Args:
        experiment_id:        Identifier for the planned experiment.
        n_runs_per_cell:      Planned runs per (agent × scenario) cell.
        temperatures:         Temperature values for the experiment.
        prompt_versions:      Prompt version identifiers.
        git_commit_hash:      Optional current commit hash for provenance tracking.
        pre_registration_url: OSF or AsPredicted URL (fill in after registration).

    Returns:
        An :class:`~results.experiment_manifest.ExperimentManifest` representing
        the planned experiment scope.
    """
    from datetime import datetime, timezone as _tz

    if temperatures is None:
        temperatures = list(_PLANNED_TEMPERATURES)
    if prompt_versions is None:
        prompt_versions = list(_PLANNED_PROMPT_VERSIONS)

    n_models = len(_DEFAULT_MODEL_SET)
    n_scenarios = _PLANNED_N_SCENARIOS
    n_variants = _PLANNED_N_VARIANTS_PER_BIAS
    n_bias_types = _PLANNED_N_BIAS_TYPES
    total_planned = n_models * n_scenarios * n_runs_per_cell * len(temperatures) * len(prompt_versions)

    return ExperimentManifest(
        experiment_id=experiment_id,
        design_tier=_PLANNED_DESIGN_TIER,
        n_models=n_models,
        n_scenarios=n_scenarios,
        n_bias_types=n_bias_types,
        n_variants_per_bias=n_variants,
        n_runs_per_cell=n_runs_per_cell,
        temperatures=temperatures,
        prompt_versions=prompt_versions,
        total_planned_runs=total_planned,
        pre_registration_url=pre_registration_url,
        git_commit_hash=git_commit_hash,
        start_time_utc=datetime.now(_tz.utc).isoformat(),
        pillars=[2],
        output_dir="",
    )


def build_prereg_document(
    manifest: ExperimentManifest,
    *,
    title: str | None = None,
    authors: str = "BuyerBench Research Team",
    model_set: list[str] | None = None,
    bias_types: list[str] | None = None,
    hypotheses: list[HypothesisDef] | None = None,
) -> PreregistrationDocument:
    """Build a :class:`PreregistrationDocument` from *manifest* and hypothesis definitions.

    Args:
        manifest:    The :class:`~results.experiment_manifest.ExperimentManifest` that
                     defines the experiment scope and configuration.
        title:       Document title.  Defaults to a standard BuyerBench title.
        authors:     Author attribution string.
        model_set:   List of model IDs in the comparison set.  Defaults to the
                     BuyerBench registry of 10 OpenRouter models.
        bias_types:  List of bias category strings being tested.  Defaults to the
                     5-type Realistic Design battery.
        hypotheses:  Hypothesis definitions.  Defaults to :data:`BUYERBENCH_HYPOTHESES`.

    Returns:
        A populated :class:`PreregistrationDocument` ready for rendering.
    """
    if title is None:
        title = (
            "BuyerBench Pillar 2: Behavioral Bias Susceptibility of LLM-Based "
            "Procurement Agents — Pre-Registration Document"
        )

    return PreregistrationDocument(
        title=title,
        authors=authors,
        generated_at=datetime.now(timezone.utc).isoformat(),
        manifest_experiment_id=manifest.experiment_id,
        manifest_git_hash=manifest.git_commit_hash,
        manifest_design_tier=manifest.design_tier,
        manifest_n_models=manifest.n_models,
        manifest_n_scenarios=manifest.n_scenarios,
        manifest_n_runs_per_cell=manifest.n_runs_per_cell,
        manifest_temperatures=manifest.temperatures,
        manifest_prompt_versions=manifest.prompt_versions,
        manifest_total_planned_runs=manifest.total_planned_runs,
        manifest_pre_registration_url=manifest.pre_registration_url,
        hypotheses=hypotheses or list(BUYERBENCH_HYPOTHESES),
        primary_outcome=(
            "Bias Susceptibility Index (BSI) per (model × bias type × variant) cell, "
            "estimated from N = {n_runs} independent runs. "
            "BSI = |P(non-optimal | VARIANT) − P(non-optimal | BASELINE)|, "
            "where optimality is defined by the scenario scoring rubric "
            "(quality × weight + delivery × weight + cost × weight).".format(
                n_runs=manifest.n_runs_per_cell
            )
        ),
        secondary_outcomes=[
            "Within-cell variance of BSI (std_bsi) — stochastic noise component",
            "Optimality gap — economic distance from optimal supplier choice",
            "Choice rate distribution — frequency of each supplier selection across runs",
            "Model-level BSI profile — 5-dimension vector of bias-type-specific means",
            "Reasoning trace length — token count as a proxy for deliberate reasoning",
        ],
        bias_types_tested=bias_types or list(_DEFAULT_BIAS_TYPES),
        model_set=model_set or list(_DEFAULT_MODEL_SET),
        bsi_significance_threshold=(
            "BSI > 0.10 with 95% CI excluding zero, two-sided, α = 0.05 "
            "with BH-FDR correction at q = 0.05 across the primary test family "
            "(10 models × 5 bias types = 50 tests)."
        ),
        alpha_level=0.05,
        fdr_q_level=0.05,
        null_result_framing=(
            "If BH-FDR-corrected tests fail to reject H₀: BSI = 0 for ≥ 3 of 5 bias types "
            "at the planned N, the primary finding is: 'Domain structure (explicit scoring rubrics, "
            "constrained supplier comparison) suppresses behavioral bias susceptibility in LLM "
            "procurement agents.' This outcome is a scientifically valid contribution and will "
            "be reported as such, not treated as a failed study."
        ),
        exclusion_criteria=[
            "Runs with error_flag = True (API failures, malformed responses) are excluded "
            "from BSI computation; included in n_runs but counted in n_error_runs.",
            "Runs where extracted_choice is None (unparseable output) are excluded from "
            "choice_is_correct and optimality_gap calculations.",
            "Models with < 80% valid runs across all cells are flagged for exclusion from "
            "aggregate analyses; their individual results are still reported.",
            "Attention check failures in the human comparison arm (Phase 4) are excluded "
            "before human BSI computation.",
        ],
        stopping_rule=(
            "Data collection stops when all planned {n_runs} runs per "
            "(agent × scenario × variant) cell have completed without error. "
            "If API rate limits cause > 20% failure rate for a given model, "
            "that model's data collection is paused and resumed in a new session; "
            "partial runs are included if n_valid_runs ≥ {min_valid} (80% threshold). "
            "No data-dependent stopping rule is applied — the pre-specified N is fixed.".format(
                n_runs=manifest.n_runs_per_cell,
                min_valid=max(1, int(manifest.n_runs_per_cell * 0.8)),
            )
        ),
    )


# ─────────────────────────────────────────────────────────────────────────────
# §4  MARKDOWN RENDERING
# ─────────────────────────────────────────────────────────────────────────────

def render_prereg_markdown(doc: PreregistrationDocument) -> str:
    """Render *doc* as an OSF Standard Pre-Registration Markdown document.

    The section structure follows the OSF Standard Pre-Registration template
    (https://osf.io/preprints/osf/) with field names adapted for computational
    social science / LLM evaluation research.

    Returns:
        A multi-line Markdown string suitable for direct upload to OSF or
        inclusion in a supplementary materials repository.
    """
    lines: list[str] = []

    def h(level: int, text: str) -> None:
        lines.append(f"{'#' * level} {text}\n")

    def p(text: str) -> None:
        lines.append(f"{text}\n")

    def blank() -> None:
        lines.append("")

    def ul(items: list[str]) -> None:
        for item in items:
            lines.append(f"- {item}")
        blank()

    def field(label: str, value: str) -> None:
        lines.append(f"**{label}:** {value}  ")

    def hr() -> None:
        lines.append("---\n")

    # ── YAML front matter ─────────────────────────────────────────────────────
    temps_str = ", ".join(
        "None (provider default)" if t is None else str(t)
        for t in doc.manifest_temperatures
    )
    lines.append("---")
    lines.append(f'title: "{doc.title}"')
    lines.append(f'authors: "{doc.authors}"')
    lines.append(f'generated_at: "{doc.generated_at}"')
    lines.append(f'experiment_id: "{doc.manifest_experiment_id}"')
    lines.append(f'git_commit: "{doc.manifest_git_hash or "unknown"}"')
    lines.append(f'design_tier: "{doc.manifest_design_tier}"')
    lines.append("---\n")

    # ── Title ─────────────────────────────────────────────────────────────────
    h(1, doc.title)

    field("Authors", doc.authors)
    field("Generated", doc.generated_at)
    field(
        "Experiment ID",
        f"`{doc.manifest_experiment_id}`"
        + (f"  \n**Git commit:** `{doc.manifest_git_hash}`" if doc.manifest_git_hash else ""),
    )
    if doc.manifest_pre_registration_url:
        field("Pre-registration URL", doc.manifest_pre_registration_url)
    blank()

    # ── Section 1: Study Information ──────────────────────────────────────────
    hr()
    h(2, "1. Study Information")
    blank()

    h(3, "1.1 Study Title")
    p(doc.title)

    h(3, "1.2 Description")
    p(
        "BuyerBench is an open-source benchmark framework for evaluating the behavioral "
        "rationality of large language model (LLM) agents in structured procurement tasks. "
        "Pillar 2 tests whether LLM agents make economically optimal supplier selection "
        "decisions under controlled behavioral manipulations (anchoring, framing, decoy, "
        "scarcity, and sunk cost effects), following the experimental design and "
        "econometric strategy documented in the BuyerBench research repository."
    )

    h(3, "1.3 Primary Research Question")
    p(
        "> Does the behavioral bias susceptibility of LLM-based agents — measured as "
        "deviation from economically optimal choices under controlled presentation "
        "manipulations — vary systematically across model capability tiers, bias types, "
        "and experimental conditions, in ways analogous to, attenuated relative to, "
        "or amplified compared to documented human behavioral patterns?"
    )

    h(3, "1.4 Has data collection begun?")
    p("No. This document is completed before data collection commences.")

    blank()

    # ── Section 2: Design Plan ─────────────────────────────────────────────────
    hr()
    h(2, "2. Design Plan")
    blank()

    h(3, "2.1 Study Type")
    p(
        "Controlled computational experiment. Each scenario pair consists of a "
        "BASELINE condition and a TREATMENT condition in which a single behavioral "
        "manipulation is introduced. All other economic parameters are held constant "
        "across conditions. The design is between-condition (each agent–scenario pair "
        "is assigned to one condition per run) with N repeated runs per cell."
    )

    h(3, "2.2 Blinding")
    p(
        "LLM agents receive no meta-information about the experimental design, bias types "
        "being tested, or BuyerBench framework. Agents see only the scenario prompt. "
        "No human rater blinding is required for the primary LLM experiment; "
        "blinding applies to human comparison arm (Phase 4, requires IRB)."
    )

    h(3, "2.3 Is there any within-participant design element?")
    p(
        "Yes — each model is evaluated on all scenarios (within-agent design across "
        "bias types and variants). Analysis accounts for this with clustered standard "
        "errors at the agent level (Level 1 WLS specification)."
    )

    h(3, "2.4 Randomization")
    p(
        "Supplier order is randomized per run using a per-run seed "
        "(`supplier_order_seed`) stored in the run metadata. "
        "This controls for positional bias (preference for items appearing first or last). "
        "Seed values are recorded for exact replayability."
    )

    blank()

    # ── Section 3: Sampling Plan ───────────────────────────────────────────────
    hr()
    h(2, "3. Sampling Plan")
    blank()

    h(3, "3.1 Existing Data")
    p(
        "Registration prior to collection of data: This pre-registration is submitted "
        "before any data collection for the registered experiment begins."
    )

    h(3, "3.2 Explanation of Existing Data")
    p("N/A — no existing data at registration time.")

    h(3, "3.3 Data Collection Procedures")
    p(
        f"**Models:** {doc.manifest_n_models} LLM agents via OpenRouter API.  \n"
        f"**Scenarios:** {doc.manifest_n_scenarios} scenario YAML files across "
        f"{len(doc.bias_types_tested)} bias type batteries.  \n"
        f"**Runs per cell:** N = {doc.manifest_n_runs_per_cell} independent, "
        "stateless API calls per (agent × scenario) cell.  \n"
        f"**Temperature(s):** {temps_str}  \n"
        f"**Prompt version(s):** {', '.join(doc.manifest_prompt_versions)}  \n"
        f"**Total planned runs:** {doc.manifest_total_planned_runs:,}"
    )

    h(3, "3.4 Sample Size")
    p(
        f"Primary analysis: N = {doc.manifest_n_runs_per_cell} runs per "
        "(agent × scenario × variant) cell.  \n"
        "Justification: Power analysis (Section G.8 of econometric strategy document) — "
        f"N = {doc.manifest_n_runs_per_cell} achieves ≥ 70% power for a BSI effect size "
        "of d = 0.4 (one-sided t-test, α = 0.05). Adequate power (≥ 80%) is achieved at "
        "d ≥ 0.5 with this N."
    )

    h(3, "3.5 Sample Size Rationale")
    p(
        "The primary expected effect size is d ≈ 0.4, informed by attenuated LLM replication "
        "of human behavioral effects (Binz & Schulz 2023; Hagendorff et al. 2023). "
        "Human meta-analytic baselines for the five tested bias types range from d = 0.4 "
        "(decoy) to d = 2.7 (anchoring); LLM effects in structured domains are expected "
        "to be substantially attenuated by explicit scoring rubrics."
    )

    h(3, "3.6 Stopping Rule")
    p(doc.stopping_rule)

    blank()

    # ── Section 4: Variables ──────────────────────────────────────────────────
    hr()
    h(2, "4. Variables")
    blank()

    h(3, "4.1 Manipulated Variables")
    ul([
        "**`variant`** (categorical): BASELINE vs. TREATMENT within each bias type battery. "
        "Treatment variants: ANCHOR_HIGH, FRAMING_GAIN/FRAMING_LOSS, DECOY, SCARCITY, SUNK_COST.",
        "**`agent_id`** (categorical): 10 OpenRouter LLM agents (between-model comparison).",
        "**`bias_category`** (categorical): anchoring, framing, decoy, scarcity, sunk_cost "
        "(5 bias types; within-model across-type analysis).",
        "**`supplier_order_seed`** (integer): Per-run randomization seed for supplier "
        "list ordering (controls positional bias).",
    ])

    h(3, "4.2 Measured Variables")
    p(f"**Primary outcome:** {doc.primary_outcome}")
    blank()
    p("**Secondary outcomes:**")
    ul(doc.secondary_outcomes)

    h(3, "4.3 Indices")
    p(
        "**BSI (Bias Susceptibility Index):** Implemented in `evaluators/pillar2.py`. "
        "At cell level (N runs): BSI = P(non-optimal | TREATMENT) − P(non-optimal | BASELINE). "
        "At run level (single run): BSI = int(decision_changed) × (1 − baseline_score), "
        "where baseline_score is the optimality score of the BASELINE run. "
        "**Optimality gap:** Economic distance between chosen and optimal supplier, "
        "computed as |score_optimal − score_chosen| / score_optimal."
    )

    blank()

    # ── Section 5: Analysis Plan ──────────────────────────────────────────────
    hr()
    h(2, "5. Analysis Plan")
    blank()

    h(3, "5.1 Statistical Models")
    p(
        "**Level 1 WLS (G.2):** `BSI ~ Treatment + BiasType + Model`, cell-level weighted "
        "least squares (weights = n_valid_runs per cell) with clustered sandwich standard "
        "errors at the model level. WARP variants excluded from this specification."
    )
    blank()
    p(
        "**Variance decomposition (G.2):** ANOVA-style SS partition into Model, BiasType, "
        "Treatment, and Residual components with η² effect sizes. "
        "If η²_Residual > 0.70, the stochastic noise qualification from Section G.2 applies."
    )
    blank()
    p(
        "**Per-(bias_category × agent_id) treatment effect tests (G.1):** Welch t-test "
        "comparing BSI estimates between TREATMENT and BASELINE arms; "
        "BH-FDR correction at q = 0.05 across all primary tests."
    )

    h(3, "5.2 Transformations")
    p(
        "BSI values are in [0, 1] by construction. No transformation is pre-specified. "
        "If within-cell BSI distributions show severe non-normality (Shapiro-Wilk p < 0.05 "
        "at N = 30), Wilcoxon signed-rank tests will be substituted for one-sample t-tests "
        "(reported alongside parametric results for comparison)."
    )

    h(3, "5.3 Inference Criteria")
    field("Alpha level", str(doc.alpha_level))
    field("Family-wise correction", f"BH-FDR at q = {doc.fdr_q_level}")
    field("Primary significance threshold", doc.bsi_significance_threshold)
    blank()

    h(3, "5.4 Data Exclusion")
    ul(doc.exclusion_criteria)

    h(3, "5.5 Missing Data")
    p(
        "API call failures are logged with error_flag = True and error_message. "
        "Excluded from BSI and optimality_gap calculations but included in n_runs. "
        "If a model exceeds 20% failure rate across its cells, that model's results "
        "are flagged in the report and excluded from aggregate cross-model analyses. "
        "No imputation is applied."
    )

    h(3, "5.6 Confirmatory vs. Exploratory Hypothesis Classification")
    p(
        "Hypotheses are pre-classified as **confirmatory** or **exploratory** before "
        "data collection. BH-FDR correction (q = 0.05) is applied to confirmatory "
        "hypotheses only. Exploratory results are reported descriptively and must "
        "not be used as primary evidence for publication claims."
    )
    blank()

    confirmatory_hyps = [h for h in doc.hypotheses if h.analysis_type == "confirmatory"]
    exploratory_hyps = [h for h in doc.hypotheses if h.analysis_type == "exploratory"]

    p("**Confirmatory hypotheses** (inferential; BH-FDR correction applied):")
    ul([f"{h.id} — {h.label}" for h in confirmatory_hyps])

    p("**Exploratory hypotheses** (descriptive only; no inferential claims permitted):")
    ul([f"{h.id} — {h.label}" for h in exploratory_hyps])

    p(
        "Additional unplanned exploratory analyses (not pre-specified as hypotheses):"
    )
    ul([
        "Session order effects (G.6.5): BSI ~ run_index to detect within-session drift.",
        "Temperature moderation (Phase 3): if multiple temperature levels are collected, "
        "BSI ~ temperature × bias_type interaction is exploratory.",
    ])

    h(3, "5.7 Null Result Pre-specification")
    p(doc.null_result_framing)

    blank()

    # ── Section 6: Pre-specified Hypotheses ───────────────────────────────────
    hr()
    h(2, "6. Pre-Specified Hypotheses")
    blank()
    p(
        "All hypotheses are pre-specified before data collection. "
        "No post-hoc hypothesis additions are permitted. "
        "Each hypothesis maps to a PRQ dimension from Section D.1 of the research design."
    )
    blank()

    for hyp in doc.hypotheses:
        h(3, f"6.{hyp.id} — {hyp.label}")
        field("PRQ Dimension", hyp.prq_dimension)
        field("Direction", hyp.direction.replace("_", " "))
        field("Analysis type", hyp.analysis_type.upper())
        blank()
        p(f"**Statement:** {hyp.statement}")
        blank()
        p(f"**Test:** {hyp.test}")
        blank()
        p(f"**Null outcome:** {hyp.null_outcome}")
        blank()
        p(f"**Data requirement:** {hyp.data_requirement}")
        blank()

    # ── Section 7: Other ──────────────────────────────────────────────────────
    hr()
    h(2, "7. Other")
    blank()

    h(3, "7.1 Registered Model Set")
    p(
        "The following models are registered as the comparison set. "
        "No post-hoc model additions are permitted. "
        "Models may be excluded if they exceed the 20% failure threshold (see 5.4)."
    )
    ul([f"`{m}`" for m in doc.model_set])

    h(3, "7.2 Registered Bias Type Battery")
    p(
        "The following bias categories are registered. "
        "No post-hoc bias type additions to the primary confirmatory analysis are permitted."
    )
    ul(doc.bias_types_tested)

    h(3, "7.3 Codebase Version")
    p(
        f"Registered codebase commit: `{doc.manifest_git_hash or 'unknown'}`.  \n"
        "Experiment configuration frozen in `experiment_manifest.json` "
        f"(experiment_id: `{doc.manifest_experiment_id}`)."
    )

    h(3, "7.4 Open Science Statement")
    p(
        "BuyerBench is open-source (MIT License). All scenario definitions, "
        "evaluation code, raw run records (excluding any API credentials), "
        "and analysis scripts will be made publicly available at the time of "
        "paper submission. Pre-registration predates any data collection. "
        "Deviations from this pre-registration, if any, will be documented "
        "in the paper under 'Deviations from Pre-Registration'."
    )

    h(3, "7.5 References")
    refs = dedent("""\
        - Tversky, A. & Kahneman, D. (1974). Judgment under uncertainty: Heuristics and biases. *Science*, 185(4157), 1124–1131.
        - Tversky, A. & Kahneman, D. (1981). The framing of decisions and the psychology of choice. *Science*, 211(4481), 453–458.
        - Huber, J., Payne, J. W. & Puto, C. (1982). Adding asymmetrically dominated alternatives. *Journal of Consumer Research*, 9(1), 90–98.
        - Arkes, H. R. & Blumer, C. (1985). The psychology of sunk cost. *Organizational Behavior and Human Decision Processes*, 35(1), 124–140.
        - Binz, M. & Schulz, E. (2023). Using cognitive psychology to understand GPT-3. *PNAS*, 120(6).
        - Hagendorff, T., Fabi, S. & Kosinski, M. (2023). Human-like intuitive behavior and reasoning biases emerged in large language models. *Nature Human Behaviour*, 7, 1768–1780.
        - Open Science Collaboration (2015). Estimating the reproducibility of psychological science. *Science*, 349(6251), aac4716.
        - Simmons, J. P., Nelson, L. D. & Simonsohn, U. (2011). False-positive psychology. *Psychological Science*, 22(11), 1359–1366.
        - Loken, E. & Gelman, A. (2017). Measurement error and the replication crisis. *Science*, 355(6325), 584–585.
        - Benjamini, Y. & Hochberg, Y. (1995). Controlling the false discovery rate. *Journal of the Royal Statistical Society B*, 57(1), 289–300.
    """)
    for ref in refs.strip().splitlines():
        lines.append(ref)
    blank()

    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────────────
# §5  I/O HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def generate_prereg_document(
    manifest: ExperimentManifest | None = None,
    **kwargs,
) -> tuple[PreregistrationDocument, str]:
    """Build and render the pre-registration document in one step.

    Args:
        manifest: Experiment manifest from :func:`~results.experiment_manifest.create_manifest`.
                  If ``None``, a planned manifest is built via
                  :func:`build_planned_manifest` using Realistic Design defaults.
                  This enables standalone pre-registration before data collection.
        **kwargs: Forwarded to :func:`build_prereg_document`.

    Returns:
        A ``(document, markdown_text)`` tuple.
    """
    if manifest is None:
        manifest = build_planned_manifest()
    doc = build_prereg_document(manifest, **kwargs)
    md = render_prereg_markdown(doc)
    return doc, md


def write_prereg_document(
    doc: PreregistrationDocument,
    markdown: str,
    output_dir: str | Path,
) -> Path:
    """Write the pre-registration document and its JSON metadata to *output_dir*.

    Writes two files:

    - ``prereg_osf.md`` — Markdown document for OSF upload
    - ``prereg_metadata.json`` — Machine-readable document model (JSON)

    Args:
        doc:        The :class:`PreregistrationDocument` model.
        markdown:   Rendered Markdown string from :func:`render_prereg_markdown`.
        output_dir: Directory path.  Created if it does not exist.

    Returns:
        Path to ``prereg_osf.md``.
    """
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    md_path = out / "prereg_osf.md"
    md_path.write_text(markdown, encoding="utf-8")

    json_path = out / "prereg_metadata.json"
    json_path.write_text(
        json.dumps(doc.model_dump(), indent=2, default=str),
        encoding="utf-8",
    )

    return md_path
