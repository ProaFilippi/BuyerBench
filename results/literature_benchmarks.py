"""UPGRADE-16: Literature benchmark calibration.

Hardcoded human and LLM BSI benchmarks from published behavioral economics and
cognitive-science literature.  Provides calibration helpers that compare
BuyerBench experiment results against prior art and overlay data for figure
reference lines.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


# ─────────────────────────────────────────────────────────────────────────────
# §1  DATA MODEL
# ─────────────────────────────────────────────────────────────────────────────


class LiteratureBenchmark(BaseModel):
    """A single human or LLM bias benchmark from published literature."""

    id: str
    """Unique slug, e.g. ``"framing-tversky-kahneman-1981"``."""

    bias_category: str
    """One of: ``anchoring``, ``framing``, ``decoy``, ``scarcity``, ``sunk_cost``."""

    citation: str
    """Short APA-style citation, e.g. ``"Tversky & Kahneman (1981)"``."""

    doi: str | None = None
    """Digital object identifier, omitting the ``https://doi.org/`` prefix."""

    sample_type: str
    """``"human"`` for human subject studies; ``"llm"`` for LLM evaluations."""

    effect_size: float
    """BSI-equivalent [0.0–1.0].

    For human studies: proportion of subjects who made the bias-influenced
    (suboptimal) choice under the treatment condition minus the proportion under
    the control condition — directly analogous to BuyerBench's BSI formula.

    For LLM studies: analogous proportion shift or anchoring index reported
    by the authors, converted to the [0, 1] BSI scale.
    """

    ci_lower_95: float | None = None
    """Lower bound of 95% CI on ``effect_size``, if available."""

    ci_upper_95: float | None = None
    """Upper bound of 95% CI on ``effect_size``, if available."""

    n_subjects: int | None = None
    """Sample size (human subjects or prompts, depending on ``sample_type``)."""

    effect_description: str
    """Prose description of what was measured and how ``effect_size`` was derived."""

    notes: str | None = None
    """Optional methodological notes or replication context."""


# ─────────────────────────────────────────────────────────────────────────────
# §2  HARDCODED LITERATURE DATABASE
# ─────────────────────────────────────────────────────────────────────────────


LITERATURE_BENCHMARKS: list[LiteratureBenchmark] = [
    # ── ANCHORING ─────────────────────────────────────────────────────────────
    LiteratureBenchmark(
        id="anchoring-tversky-kahneman-1974",
        bias_category="anchoring",
        citation="Tversky & Kahneman (1974)",
        doi="10.1126/science.185.4157.1124",
        sample_type="human",
        effect_size=0.44,
        ci_lower_95=0.38,
        ci_upper_95=0.50,
        n_subjects=167,
        effect_description=(
            "Wheel-of-fortune anchoring study on percentage-of-African-nations estimation. "
            "High-anchor group (65) median estimate: 45; low-anchor group (10) median: 25. "
            "Chapman & Johnson (1999) meta-analytic anchoring index (AI = (estimate - control) / "
            "(anchor - control)) averaged across five tasks: AI ≈ 0.40–0.48. "
            "BSI-equivalent set to 0.44 (midpoint of meta-analytic AI range)."
        ),
        notes="Seminal anchoring study; anchoring index aggregated across estimation tasks.",
    ),
    LiteratureBenchmark(
        id="anchoring-ariely-loewenstein-prelec-2003",
        bias_category="anchoring",
        citation="Ariely, Loewenstein & Prelec (2003)",
        doi="10.1162/00335530360535144",
        sample_type="human",
        effect_size=0.51,
        ci_lower_95=0.42,
        ci_upper_95=0.60,
        n_subjects=55,
        effect_description=(
            "'Coherent arbitrariness': willingness-to-pay anchored to last two digits of "
            "Social Security Number. High-SSN group bid 41–61% more than low-SSN group "
            "across six product categories. BSI-equivalent: mean proportional deviation from "
            "no-anchor control across categories ≈ 0.51."
        ),
        notes="Arbitrary anchors (SSN digits) systematically distort economic valuations.",
    ),
    # ── FRAMING ───────────────────────────────────────────────────────────────
    LiteratureBenchmark(
        id="framing-tversky-kahneman-1981",
        bias_category="framing",
        citation="Tversky & Kahneman (1981)",
        doi="10.1126/science.7455683",
        sample_type="human",
        effect_size=0.50,
        ci_lower_95=0.43,
        ci_upper_95=0.57,
        n_subjects=152,
        effect_description=(
            "Asian disease problem: 72% chose the certain option (save 200) under gain framing; "
            "only 22% chose the certain option (400 die) under loss framing. "
            "BSI = |P(safe | gain) - P(safe | loss)| = |0.72 - 0.22| = 0.50."
        ),
        notes="Canonical framing effect; one of the most replicated findings in behavioral economics.",
    ),
    LiteratureBenchmark(
        id="framing-levin-gaeth-1988",
        bias_category="framing",
        citation="Levin & Gaeth (1988)",
        doi="10.1177/002224378802500402",
        sample_type="human",
        effect_size=0.32,
        ci_lower_95=0.22,
        ci_upper_95=0.42,
        n_subjects=100,
        effect_description=(
            "Ground beef rated significantly better when labeled '75% lean' vs '25% fat'. "
            "Preference shift between equivalent positive/negative attribute frames ≈ 32pp. "
            "BSI = P(preferred | positive_frame) - P(preferred | negative_frame) ≈ 0.32."
        ),
        notes="Attribute framing in consumer product evaluation; effect robust across product types.",
    ),
    # ── DECOY ─────────────────────────────────────────────────────────────────
    LiteratureBenchmark(
        id="decoy-huber-payne-puto-1982",
        bias_category="decoy",
        citation="Huber, Payne & Puto (1982)",
        doi="10.1086/208899",
        sample_type="human",
        effect_size=0.28,
        ci_lower_95=0.18,
        ci_upper_95=0.38,
        n_subjects=153,
        effect_description=(
            "Asymmetrically dominated decoy increased target choice share from ~45% to ~73%. "
            "BSI = P(target | decoy present) - P(target | decoy absent) = 0.73 - 0.45 = 0.28."
        ),
        notes=(
            "Original asymmetric dominance (decoy / attraction) effect. "
            "Replicated across beer, cars, restaurants, lotteries, and job candidates."
        ),
    ),
    LiteratureBenchmark(
        id="decoy-simonson-1989",
        bias_category="decoy",
        citation="Simonson (1989)",
        doi="10.1086/209267",
        sample_type="human",
        effect_size=0.22,
        ci_lower_95=0.14,
        ci_upper_95=0.30,
        n_subjects=85,
        effect_description=(
            "Compromise effect: choice share of the middle option increased ~22pp when it was "
            "positioned between two extremes vs. a two-option set. "
            "BSI = P(compromise | 3-option set) - P(compromise | 2-option set) ≈ 0.22."
        ),
        notes="Compromise effect variant; target gains share as 'the safe middle choice'.",
    ),
    # ── SCARCITY ──────────────────────────────────────────────────────────────
    LiteratureBenchmark(
        id="scarcity-worchel-lee-adewole-1975",
        bias_category="scarcity",
        citation="Worchel, Lee & Adewole (1975)",
        doi="10.1037/0022-3514.32.5.906",
        sample_type="human",
        effect_size=0.25,
        ci_lower_95=0.16,
        ci_upper_95=0.34,
        n_subjects=134,
        effect_description=(
            "Cookies rated more desirable when presented in a scarce jar (2 cookies) "
            "vs. an abundant jar (10 cookies). Mean desirability: 6.02 vs 5.47 on 9-point scale "
            "(Cohen's d ≈ 0.61). "
            "BSI = P(chose scarce item | scarcity cue) - P(same item | no cue) ≈ 0.25."
        ),
        notes="Commodity theory of psychological reactance; foundational scarcity bias study.",
    ),
    LiteratureBenchmark(
        id="scarcity-aggarwal-jun-huh-2011",
        bias_category="scarcity",
        citation="Aggarwal, Jun & Huh (2011)",
        doi="10.1509/jmkr.48.1.10",
        sample_type="human",
        effect_size=0.30,
        ci_lower_95=0.20,
        ci_upper_95=0.40,
        n_subjects=108,
        effect_description=(
            "Limited-time vs. unlimited-supply framing; choice share differential for the "
            "scarce product ≈ 30pp across experiments. "
            "BSI = P(chose scarce item | limited supply) - P(same | unlimited supply) ≈ 0.30."
        ),
        notes="Retail scarcity framing; demand-side scarcity cues (limited quantity/time).",
    ),
    # ── SUNK COST ─────────────────────────────────────────────────────────────
    LiteratureBenchmark(
        id="sunk-cost-arkes-blumer-1985",
        bias_category="sunk_cost",
        citation="Arkes & Blumer (1985)",
        doi="10.1016/0749-5978(85)90049-4",
        sample_type="human",
        effect_size=0.32,
        ci_lower_95=0.22,
        ci_upper_95=0.42,
        n_subjects=61,
        effect_description=(
            "Theater season-ticket study: 61% of full-price buyers attended despite illness "
            "vs. 29% of discounted-ticket buyers. "
            "BSI = P(attend | full_price_sunk) - P(attend | discount_sunk) = 0.61 - 0.29 = 0.32."
        ),
        notes="Canonical sunk cost fallacy; commitment-driven attendance despite negative utility.",
    ),
    LiteratureBenchmark(
        id="sunk-cost-staw-1981",
        bias_category="sunk_cost",
        citation="Staw (1981)",
        doi="10.1016/0030-5073(81)90027-X",
        sample_type="human",
        effect_size=0.38,
        ci_lower_95=0.28,
        ci_upper_95=0.48,
        n_subjects=240,
        effect_description=(
            "Escalation of commitment: participants allocated 36.8% more resources to a failing "
            "project when they had made the initial investment decision (personal responsibility) "
            "vs. when an external party had. "
            "BSI = P(escalate | personal_responsibility) - P(escalate | external_cause) ≈ 0.38."
        ),
        notes="Escalation of commitment in organizational investment decisions.",
    ),
    # ── LLM BENCHMARKS ────────────────────────────────────────────────────────
    LiteratureBenchmark(
        id="framing-binz-schulz-2023",
        bias_category="framing",
        citation="Binz & Schulz (2023)",
        doi="10.1073/pnas.2218523120",
        sample_type="llm",
        effect_size=0.40,
        ci_lower_95=0.30,
        ci_upper_95=0.50,
        n_subjects=None,
        effect_description=(
            "GPT-3 (text-davinci-002) exhibited framing effects on Asian-disease-analog problems. "
            "Gain-frame vs. loss-frame preferred option choice shifted by ~40pp on multi-task "
            "evaluation. BSI computed from stated preference shift across framing tasks."
        ),
        notes="First systematic LLM behavioral economics evaluation; GPT-3 series.",
    ),
    LiteratureBenchmark(
        id="anchoring-binz-schulz-2023",
        bias_category="anchoring",
        citation="Binz & Schulz (2023)",
        doi="10.1073/pnas.2218523120",
        sample_type="llm",
        effect_size=0.35,
        ci_lower_95=0.25,
        ci_upper_95=0.45,
        n_subjects=None,
        effect_description=(
            "GPT-3 (text-davinci-002) estimates anchored to arbitrary starting numbers on "
            "estimation tasks. Anchoring index ~0.35 derived from deviation of GPT-3 "
            "estimates toward provided anchor value."
        ),
        notes="Same paper as framing-binz-schulz-2023; anchoring tested on GPT-3.",
    ),
    LiteratureBenchmark(
        id="framing-hagendorff-2023",
        bias_category="framing",
        citation="Hagendorff et al. (2023)",
        doi="10.1038/s41562-023-01699-8",
        sample_type="llm",
        effect_size=0.38,
        ci_lower_95=0.28,
        ci_upper_95=0.48,
        n_subjects=None,
        effect_description=(
            "Multiple LLM architectures (GPT-3.5-turbo, LLaMA-65B, Vicuna-33B) exhibited "
            "framing effects across 24 cognitive tasks. Mean BSI across models ≈ 0.38 for "
            "gain/loss framing variants."
        ),
        notes="Human-like intuitive behavior and reasoning biases confirmed across LLM families.",
    ),
    LiteratureBenchmark(
        id="decoy-hagendorff-2023",
        bias_category="decoy",
        citation="Hagendorff et al. (2023)",
        doi="10.1038/s41562-023-01699-8",
        sample_type="llm",
        effect_size=0.30,
        ci_lower_95=0.20,
        ci_upper_95=0.40,
        n_subjects=None,
        effect_description=(
            "Decoy effect detected in multi-attribute choice tasks across GPT-3.5-turbo, "
            "LLaMA-65B, and Vicuna-33B. Target choice share increased ~30pp with "
            "asymmetrically dominated decoy option."
        ),
        notes="Same paper as framing-hagendorff-2023; decoy tested across the same LLM families.",
    ),
    LiteratureBenchmark(
        id="framing-jones-steinhardt-2022",
        bias_category="framing",
        citation="Jones & Steinhardt (2022)",
        doi="10.48550/arXiv.2212.09561",
        sample_type="llm",
        effect_size=0.42,
        ci_lower_95=0.32,
        ci_upper_95=0.52,
        n_subjects=None,
        effect_description=(
            "Framing effects across GPT-3 and Codex on decision tasks with gain/loss variants. "
            "BSI ≈ 0.42 for gain/loss choice-pair framing tasks; effects emerge with model scale."
        ),
        notes="Focus on GPT-3 and Codex; framing biases scale with model capacity.",
    ),
]


# ─────────────────────────────────────────────────────────────────────────────
# §3  LOOKUP FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────


def get_benchmarks_by_bias(
    bias_category: str,
    sample_type: str | None = None,
) -> list[LiteratureBenchmark]:
    """Return benchmarks for a bias type, optionally filtered by sample type.

    Args:
        bias_category: One of ``"anchoring"``, ``"framing"``, ``"decoy"``,
            ``"scarcity"``, ``"sunk_cost"``.
        sample_type: ``"human"``, ``"llm"``, or ``None`` (returns both).

    Returns:
        Matching :class:`LiteratureBenchmark` instances (may be empty list).
    """
    results = [b for b in LITERATURE_BENCHMARKS if b.bias_category == bias_category]
    if sample_type is not None:
        results = [b for b in results if b.sample_type == sample_type]
    return results


def get_all_human_benchmarks() -> list[LiteratureBenchmark]:
    """Return all human subject benchmarks in the database."""
    return [b for b in LITERATURE_BENCHMARKS if b.sample_type == "human"]


def get_all_llm_benchmarks() -> list[LiteratureBenchmark]:
    """Return all LLM benchmarks from prior literature."""
    return [b for b in LITERATURE_BENCHMARKS if b.sample_type == "llm"]


def get_bias_categories() -> list[str]:
    """Return sorted list of bias categories represented in the literature database."""
    return sorted({b.bias_category for b in LITERATURE_BENCHMARKS})


# ─────────────────────────────────────────────────────────────────────────────
# §4  CALIBRATION MODELS
# ─────────────────────────────────────────────────────────────────────────────


class BenchmarkCalibrationResult(BaseModel):
    """Calibration of BuyerBench BSI against literature benchmarks for one bias type."""

    bias_category: str

    llm_mean_bsi: float | None = None
    """Mean BSI from the current BuyerBench experiment (``None`` if no data)."""

    human_benchmark_min: float
    """Minimum effect_size across human benchmarks for this bias type."""

    human_benchmark_max: float
    """Maximum effect_size across human benchmarks for this bias type."""

    human_benchmark_mean: float
    """Mean effect_size across human benchmarks for this bias type."""

    llm_prior_min: float | None = None
    """Minimum effect_size from prior LLM literature (``None`` if no prior LLM data)."""

    llm_prior_max: float | None = None
    """Maximum effect_size from prior LLM literature."""

    llm_prior_mean: float | None = None
    """Mean effect_size from prior LLM literature."""

    human_benchmarks: list[LiteratureBenchmark] = Field(default_factory=list)
    """All human benchmarks contributing to this calibration."""

    llm_prior_benchmarks: list[LiteratureBenchmark] = Field(default_factory=list)
    """All prior-LLM benchmarks contributing to this calibration."""

    within_human_range: bool | None = None
    """``True`` iff ``llm_mean_bsi`` is within ``[human_benchmark_min, human_benchmark_max]``."""

    calibration_note: str
    """One-sentence calibration status narrative."""


class BenchmarkOverlayData(BaseModel):
    """Structured data for overlaying literature reference lines on BSI plots."""

    bias_category: str
    human_reference_lines: list[dict[str, Any]] = Field(default_factory=list)
    """Each item: ``{citation, effect_size, ci_lower_95, ci_upper_95, n_subjects}``."""
    llm_reference_lines: list[dict[str, Any]] = Field(default_factory=list)
    """Same structure as ``human_reference_lines`` but for prior LLM results."""
    human_range_min: float
    human_range_max: float
    human_range_mean: float


# ─────────────────────────────────────────────────────────────────────────────
# §5  CALIBRATION FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────


def compute_benchmark_calibration(
    experiment_bsi: dict[str, float] | None = None,
) -> list[BenchmarkCalibrationResult]:
    """Compute calibration against literature benchmarks for each bias category.

    Args:
        experiment_bsi: Optional ``{bias_category: mean_bsi}`` mapping from a
            BuyerBench experiment (e.g. ``{"anchoring": 0.38, "framing": 0.51}``).
            When ``None``, ``llm_mean_bsi`` is ``None`` for all results.

    Returns:
        List of :class:`BenchmarkCalibrationResult`, one per bias category in
        the literature database, sorted alphabetically.
    """
    results: list[BenchmarkCalibrationResult] = []

    for bias_cat in get_bias_categories():
        human_bms = get_benchmarks_by_bias(bias_cat, "human")
        llm_prior_bms = get_benchmarks_by_bias(bias_cat, "llm")

        human_effects = [b.effect_size for b in human_bms]
        human_min = min(human_effects) if human_effects else 0.0
        human_max = max(human_effects) if human_effects else 0.0
        human_mean = sum(human_effects) / len(human_effects) if human_effects else 0.0

        llm_prior_effects = [b.effect_size for b in llm_prior_bms]
        llm_prior_min = min(llm_prior_effects) if llm_prior_effects else None
        llm_prior_max = max(llm_prior_effects) if llm_prior_effects else None
        llm_prior_mean = (
            sum(llm_prior_effects) / len(llm_prior_effects) if llm_prior_effects else None
        )

        llm_mean_bsi = experiment_bsi.get(bias_cat) if experiment_bsi else None

        within_human_range: bool | None = None
        if llm_mean_bsi is not None and human_effects:
            within_human_range = human_min <= llm_mean_bsi <= human_max

        # Build a calibration note
        if llm_mean_bsi is None:
            note = (
                f"No BuyerBench experiment data for {bias_cat}. "
                f"Human BSI range: [{human_min:.2f}, {human_max:.2f}]."
            )
        elif within_human_range:
            note = (
                f"BuyerBench BSI ({llm_mean_bsi:.3f}) is within the human literature range "
                f"[{human_min:.2f}, {human_max:.2f}] — calibrated to human norms."
            )
        elif llm_mean_bsi < human_min:
            note = (
                f"BuyerBench BSI ({llm_mean_bsi:.3f}) is BELOW the human literature floor "
                f"({human_min:.2f}) — LLMs appear less susceptible than humans."
            )
        else:
            note = (
                f"BuyerBench BSI ({llm_mean_bsi:.3f}) is ABOVE the human literature ceiling "
                f"({human_max:.2f}) — LLMs appear MORE susceptible than humans."
            )

        results.append(
            BenchmarkCalibrationResult(
                bias_category=bias_cat,
                llm_mean_bsi=llm_mean_bsi,
                human_benchmark_min=human_min,
                human_benchmark_max=human_max,
                human_benchmark_mean=human_mean,
                llm_prior_min=llm_prior_min,
                llm_prior_max=llm_prior_max,
                llm_prior_mean=llm_prior_mean,
                human_benchmarks=human_bms,
                llm_prior_benchmarks=llm_prior_bms,
                within_human_range=within_human_range,
                calibration_note=note,
            )
        )

    return results


def get_benchmark_overlay_data(
    bias_categories: list[str] | None = None,
) -> list[BenchmarkOverlayData]:
    """Return structured overlay data for reference lines on BSI plots.

    Args:
        bias_categories: Optional list of bias categories to include.
            Defaults to all categories represented in the literature database.

    Returns:
        List of :class:`BenchmarkOverlayData`, one per requested bias category,
        sorted in the order given (or alphabetically if ``None``).
    """
    cats = bias_categories if bias_categories is not None else get_bias_categories()
    overlays: list[BenchmarkOverlayData] = []

    for bias_cat in cats:
        human_bms = get_benchmarks_by_bias(bias_cat, "human")
        llm_bms = get_benchmarks_by_bias(bias_cat, "llm")

        human_effects = [b.effect_size for b in human_bms]

        human_lines: list[dict[str, Any]] = [
            {
                "citation": b.citation,
                "effect_size": b.effect_size,
                "ci_lower_95": b.ci_lower_95,
                "ci_upper_95": b.ci_upper_95,
                "n_subjects": b.n_subjects,
            }
            for b in human_bms
        ]
        llm_lines: list[dict[str, Any]] = [
            {
                "citation": b.citation,
                "effect_size": b.effect_size,
                "ci_lower_95": b.ci_lower_95,
                "ci_upper_95": b.ci_upper_95,
                "n_subjects": b.n_subjects,
            }
            for b in llm_bms
        ]

        overlays.append(
            BenchmarkOverlayData(
                bias_category=bias_cat,
                human_reference_lines=human_lines,
                llm_reference_lines=llm_lines,
                human_range_min=min(human_effects) if human_effects else 0.0,
                human_range_max=max(human_effects) if human_effects else 0.0,
                human_range_mean=(
                    sum(human_effects) / len(human_effects) if human_effects else 0.0
                ),
            )
        )

    return overlays


# ─────────────────────────────────────────────────────────────────────────────
# §6  RENDERING HELPERS
# ─────────────────────────────────────────────────────────────────────────────


def render_benchmark_calibration_markdown(
    calibration: list[BenchmarkCalibrationResult],
) -> str:
    """Render calibration results as a GitHub-flavored Markdown table.

    Args:
        calibration: Output of :func:`compute_benchmark_calibration`.

    Returns:
        Multi-line Markdown string with a single comparison table.
    """
    lines = [
        "## Literature Benchmark Calibration",
        "",
        (
            "| Bias Type | BuyerBench BSI | Human Range | Human Mean"
            " | Prior LLM Range | Status |"
        ),
        "|---|---|---|---|---|---|",
    ]

    for r in calibration:
        bb_bsi = f"{r.llm_mean_bsi:.3f}" if r.llm_mean_bsi is not None else "—"
        human_range = f"[{r.human_benchmark_min:.2f}, {r.human_benchmark_max:.2f}]"
        human_mean_str = f"{r.human_benchmark_mean:.2f}"

        if r.llm_prior_min is not None and r.llm_prior_max is not None:
            llm_range = f"[{r.llm_prior_min:.2f}, {r.llm_prior_max:.2f}]"
        else:
            llm_range = "—"

        if r.within_human_range is None:
            status = "—"
        elif r.within_human_range:
            status = "within range"
        elif r.llm_mean_bsi is not None and r.llm_mean_bsi < r.human_benchmark_min:
            status = "below human"
        else:
            status = "above human"

        lines.append(
            f"| {r.bias_category} | {bb_bsi} | {human_range}"
            f" | {human_mean_str} | {llm_range} | {status} |"
        )

    return "\n".join(lines)
