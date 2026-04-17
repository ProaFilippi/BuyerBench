"""Pillar 2 evaluator — Economic Decision Quality and Behavioral Robustness.

INTERNAL RATIONALITY SCOPE
--------------------------
This evaluator tests *internal* rationality: whether an agent optimizes the
objective function *as stated* in each scenario's ``evaluation_weights`` YAML
field.  We do NOT claim that those weights represent the uniquely correct or
universally rational preference ordering.  The ground truth here is
algorithmic — derived deterministically from the scenario definition — not an
externally validated economic optimum.

Concretely:
  * ``expected_optimal`` in each scenario YAML is computed from the scenario's
    own evaluation weights.
  * ``optimal_choice_rate`` == 1.0 means the agent matched that scenario-defined
    best choice, nothing more.
  * ``bias_susceptibility_index`` (BSI) measures whether the agent's choice
    changes across economically-equivalent presentation variants (baseline vs.
    framing/anchor/decoy).  A BSI > 0 means the agent's choice is *inconsistent
    with its own stated objective* across variants — not that the agent is irrational
    in some absolute sense.

This framing is the correct response to the "no ground truth" critique: we
measure deviation from the stated objective, making the claim falsifiable and
scope-limited.  Any cross-scenario generalization must restrict claims to
"procurement decision-making" and label them accordingly.

DOMAIN SCOPE
------------
All results produced by this evaluator are scoped to **LLM-based procurement
decision-making** — specifically, the final supplier/contract selection step
when structured options are presented to an agent.

Domain specificity is a deliberate feature, not a flaw:
  * Applied relevance: procurement automation is an active deployment context
    for LLM agents, making bias effects here practically significant.
  * Ecological validity: scenarios mirror real procurement inputs (supplier
    catalogs, unit prices, quality scores, delivery terms) rather than abstract
    lotteries, increasing applicability to deployed systems.
  * Scope control: restricting to one domain enables tighter experimental
    control and avoids conflating context effects across dissimilar tasks.

Claims about anchoring, framing, decoy, or scarcity effects from this
evaluator MUST be stated as:
  "Bias susceptibility in LLM-based procurement decision-making."

Claims MUST NOT be stated as:
  "LLMs exhibit anchoring bias [in general]" — that requires replication
  across additional domains (contract negotiation, investment decisions,
  hiring, etc.) and is explicitly out of scope for this study.

Future work: extending these scenarios to contract negotiation and capital
allocation domains would test whether procurement-observed effects generalize.

PROMPT SENSITIVITY
------------------
A genuine threat to validity: BSI values may be a property of the *specific
prompt wording* chosen by researchers rather than a stable model property.
Slight rephrasing (e.g., "Please select the best supplier" vs. "Which supplier
would you recommend?") can shift BSI by >0.1, making results non-replicable.

This threat cannot be eliminated by design — it must be measured and reported.

Mandatory robustness check (REV-5 from the red-team plan): before the main
experiment, run a 5-run pilot at 3 prompt phrasings per scenario.  Compute
the coefficient of variation (CV = population_std / mean) of mean-BSI across
phrasings.  If CV > 0.50, the scenario wording is unstable and must be
redesigned before data collection proceeds.  This is an explicit go/no-go gate.

The ``compute_prompt_sensitivity`` function in this module implements the check.
All CV values — whether robust or not — must be reported in the paper's
Appendix D (robustness checks).  Do not selectively report only passing checks.

Interpretation of CV:
  * CV ≤ 0.20 — low sensitivity; wording has negligible effect
  * 0.20 < CV ≤ 0.50 — moderate; report but may proceed
  * CV > 0.50 — high sensitivity; result is wording-dependent → redesign

Edge case: if mean BSI across all phrasings is 0.0 (model always chooses
optimally regardless of prompt wording), CV is defined as 0.0 — this is
actually the most robust finding possible.

HYPOTHETICAL CHOICE FRAMING
---------------------------
LLMs do not receive monetary payoffs.  Classic behavioral economics results
(Kahneman, Thaler, Tversky) were established with real financial stakes.
This raises the objection that our measured "biases" may be superficial text
pattern reproduction rather than genuine decision-theoretic failures.

This limitation is unavoidable given current technology.  The appropriate
response is to frame results explicitly:

  "We test *behavioral consistency* — whether an agent's choice changes
   across economically equivalent presentation variants — not incentivized
   decision-making.  The agent operates in a context where it has been told
   its procurement decision is consequential.  This is analogous to
   hypothetical-choice studies in behavioral economics (Camerer & Hogarth,
   1999), which show bias effects comparable to incentivized designs."

This framing does not eliminate the objection, but it accurately characterizes
the study scope and situates it within established methodological practice.

Claims from this evaluator MUST be stated as:
  "Behavioral consistency under [bias type] presentation manipulations,
   in hypothetical-choice procurement tasks."

Claims MUST NOT be stated as:
  "LLMs exhibit [bias] in the same way that humans with real financial stakes
   do" — that requires incentivized replication and is out of scope.

The ``incentive_framing`` field in ``aggregate_bias_report`` output is a
machine-readable anchor for this limitation so that all downstream JSON/CSV
consumers carry this framing alongside the BSI values.

SAMPLE SIZE LIMITATION
----------------------
With N=1 run per (model × scenario) cell, BSI values are single-realization
observations, not distributions.  A model that exhibits a bias with probability
p=0.4 will score BSI=0 roughly 60% of the time from a single run — making
single-run data entirely uninformative about true bias rates.

Critical implications:
  * Single-run BSI == 0 does NOT mean the model is unbiased.
  * Single-run BSI == 1 does NOT mean the model is reliably biased.
  * No statistical test (t-test, BH correction, mixed-effects model) is valid
    on N=1 per cell data.  A "significant" result from a single run is
    meaningless.

The mandatory minimum is **N=50 independent runs per (model × scenario)
cell** before any inferential claim.  N=5 is adequate for pilot feasibility
checks (Gate 1) but not for paper evidence.

Use protocol:
  * Current single-run session data is EXPLORATORY ONLY — use it to verify
    infrastructure, check schema correctness, and estimate costs.
  * Do not report single-run BSI values as evidence in the paper.
  * Gate 1 (pilot at N=5): verify error rate < 5% and at least 2/10 models
    show mean_BSI > 0.05 on at least 1 bias type.

The ``exploratory_only`` field in ``aggregate_bias_report`` is True whenever
``n_runs_per_cell`` is None or ≤ 1, providing a machine-readable flag that
downstream consumers can check before treating BSI values as inference-valid.
The ``sample_size_warning`` field carries the limitation text for JSON/CSV
consumers that log metadata alongside results.

CROSS-MODEL REGRESSION SCOPE
-----------------------------
The BuyerBench benchmark evaluates N=10 models.  N=10 is a critical
statistical threshold: OLS regression at N=10 units (models) provides no
meaningful inferential value.  Standard errors span the full coefficient
magnitude, confidence intervals are enormous, and reported p-values are
unreliable.  Any cross-model OLS regression (e.g., "models with higher
Pillar 1 scores show lower mean BSI") is a *description of the 10 observed
models*, not a statistical estimate of a population effect.

This has direct implications for how results must be labeled:

  * Cross-model analyses (H2, capability gradient scatter, inter-model
    comparisons) are DESCRIPTIVE PATTERNS ONLY.  Do not report p-values,
    regression coefficients, or confidence intervals for cross-model
    comparisons.  Present as scatter plots or tables with no inferential
    claim.

  * Within-model analyses (H1, H3, H5, H7) are the primary inferential
    engines.  These use N=50+ runs per (model × scenario) cell, which is
    sufficient for mixed-effects models and BH-corrected hypothesis tests.

  * The key distinction: across models is N=10 (descriptive), within a
    single model across runs is N=50+ (inferential).

Claims from cross-model comparisons MUST be stated as:
  "Descriptive pattern across 10 evaluated models (N=10 units; no
   inferential claim)."

Claims MUST NOT be stated as:
  "Higher Pillar 1 capability is associated with lower bias susceptibility
   (β = ..., p < 0.05)" — that framing requires far larger N at the model
   level and is not supported by this study design.

The ``cross_model_analysis`` field in ``aggregate_bias_report`` is a
machine-readable anchor for this limitation so that all downstream JSON/CSV
consumers carry the scope label alongside BSI values.

MULTIPLE COMPARISONS WITHOUT PRE-REGISTRATION
----------------------------------------------
The full BuyerBench Pillar 2 experiment spans a large implicit test space:
10 models × 5 bias types × 2 variants per bias type = 100 (model × cell)
comparisons.  At a nominal significance level of α = 0.05, approximately
5 false positives are expected *by chance alone*, even under the null
hypothesis that no model exhibits any bias.  Without pre-registration,
researchers can consciously or unconsciously select and emphasize
statistically significant results from this space, inflating the apparent
evidence for bias.

This is a genuine threat that cannot be eliminated post hoc — it must be
addressed through study design before data collection begins:

  1. **Pre-registration (REV-2):** Post a pre-registration on OSF *before*
     any data is collected.  The registration must specify:
       - Which hypotheses are *confirmatory* (H1, H3, H5, H7) and which
         are *exploratory* (H2, H4, H6, H8+).
       - The exact regression specification for each confirmatory test.
       - The multiple-comparison correction procedure (Benjamini-Hochberg).
       - The α level (recommended: 0.05 BH-corrected across confirmatory
         tests only).
     Any analysis not listed in the pre-registration must be labeled
     "unplanned / exploratory" and cannot be used to confirm hypotheses.

  2. **Benjamini-Hochberg (BH) correction:** Apply BH correction across all
     *confirmatory* hypothesis tests within a single experiment.  Do not
     apply BH across exploratory and confirmatory tests together — that
     dilutes power for the confirmatory tests.

  3. **Labeling discipline:** Every result table and figure must clearly
     label each reported p-value as: (a) confirmatory (pre-registered,
     BH-corrected), (b) exploratory (unplanned, no correction implied), or
     (c) descriptive (no test performed).

Claims from confirmatory analyses MUST be stated as:
  "Pre-registered confirmatory test, BH-corrected p < 0.05 across H1/H3/H5/H7."

Claims MUST NOT be stated as:
  "Model X shows significant anchoring bias (p = 0.03)" — without explicitly
  stating whether this was pre-registered and whether BH correction was
  applied.  An uncorrected p-value selected from 100 cells is meaningless.

The ``multiple_comparisons`` field in ``aggregate_bias_report`` is a
machine-readable anchor for this limitation so that all downstream JSON/CSV
consumers carry a reminder that BH correction and pre-registration are
required before any inferential p-value is reported.

STOCHASTIC PARROTING / TRAINING DATA CONFOUND
----------------------------------------------
LLMs are pre-trained on vast corpora of human text, including published
behavioral economics papers, psychology textbooks, and popular accounts of
cognitive biases (anchoring, framing, decoy, etc.).  A plausible alternative
explanation for any observed bias in our scenarios: the model is not exhibiting
a genuine decision-theoretic failure, but is instead reproducing statistical
patterns from training documents that describe *human* behavioral biases in
similar contexts.

This threat is sometimes called "stochastic parroting" — the model outputs
what commonly follows in training text, not what would follow from independent
evaluation of the choice set.  It is distinct from genuine preference
inconsistency.

This confound cannot be fully excluded within the current experimental design.
The appropriate response is transparent framing:

  "We cannot exclude training data effects.  Our results characterize
   behavioral *patterns in deployment conditions* regardless of underlying
   mechanism — whether driven by learned text patterns or genuine
   decision-theoretic failures.  The practical implication (the agent
   makes systematically different choices under framing manipulations) is
   the same in either case."

This framing remains empirically honest: practitioners deploying LLM buyer
agents care about decision consistency in production regardless of mechanism.

Additional mitigation for the flagship study: include at least 2 novel
scenarios whose numerical values and supplier names were generated *after*
the knowledge cutoffs of all evaluated models.  Novel-context results that
match standard-context BSI provide weak evidence against pure memorization,
though they cannot fully resolve the confound.

Claims from this evaluator MUST be stated as:
  "Behavioral patterns under [bias type] presentation manipulations,
   observed in deployment conditions; training data confound unexcluded."

Claims MUST NOT be stated as:
  "LLMs exhibit [bias] as a cognitive failure independent of training data"
  — that would require experiments specifically designed to rule out
  memorization (e.g., entirely novel domains generated post-cutoff).

The ``training_data_confound`` field in ``aggregate_bias_report`` is a
machine-readable anchor for this limitation so that all downstream JSON/CSV
consumers carry a reminder that training-data effects cannot be excluded
from any observed BSI pattern.

ANCHOR VALIDITY / INSTRUCTION-FOLLOWING CONFOUND
-------------------------------------------------
A structural ambiguity in anchor-type scenarios: when the prompt contains
phrasing such as "the previous emergency procurement was $91/unit," a
sophisticated model may correctly recognize this information as irrelevant
to the current selection task and deliberately ignore it.  In that case
the model is exhibiting *instruction-following ability* — it is reasoning
"this prior datum is not a valid input to the current decision" — rather
than manifesting or resisting an *anchoring bias*.

This creates an identification problem: a model that scores BSI=0 (no bias
detected) on anchor scenarios might be either (a) genuinely not susceptible
to anchoring, or (b) capable enough to detect and override the anchor cue.
The two mechanisms are empirically indistinguishable with this design —
they produce identical BSI values for opposite reasons.

The appropriate response is to acknowledge that instruction-following ability
and bias resistance are likely *empirically correlated* across models in this
study, and to frame results accordingly:

  "We cannot fully separate bias resistance from instruction-following
   ability in anchor-type scenarios.  A high-capability model that ignores
   the anchor may be optimizing the stated objective *or* detecting and
   discarding an irrelevant cue.  These mechanisms are observationally
   equivalent in our design; effect sizes may be attenuated in frontier
   models that are stronger instruction followers."

This correlation may actually underlie the expected capability gradient:
higher-capability models (higher Pillar 1 scores) may show lower BSI on
anchor scenarios not because they are less susceptible to anchoring per se,
but because they are better at recognizing contextually irrelevant signals —
which is a different (and arguably more operationally important) property.

Claims from anchor-type scenarios MUST acknowledge this framing:
  "BSI on anchor scenarios reflects a combination of bias susceptibility
   and instruction-following ability; the two cannot be separated in this
   design."

Claims MUST NOT be stated as:
  "Model X is not susceptible to anchoring bias" — that requires a design
  where the anchor cannot be consciously detected and overridden, which
  is not achievable with explicit prompt-level anchors.

The ``anchor_instruction_following_confound`` field in ``aggregate_bias_report``
is a machine-readable anchor for this limitation so that all downstream
JSON/CSV consumers carry a reminder that instruction-following ability and
bias resistance are confounded in anchor scenarios.

CEILING EFFECT
--------------
With N=1 run per (model × scenario) cell, perfect BSI=0 scores are expected
even for models that are genuinely biased.  Consider a model that exhibits an
anchoring bias with probability p=0.4: in a single run, P(BSI=0) = 0.6
regardless of the true bias rate.  When 8 out of 10 models score BSI=0 at
N=1, this is entirely consistent with models that are biased 40% of the time —
the single-run data simply cannot distinguish the two.

At N=50 independent runs per cell, the binomial sampling distribution tightens
and stochastic bias rates become estimable.  A model biased at p=0.4 will show
mean BSI ≈ 0.4 (±95%-CI ~0.26–0.54) at N=50, compared to mean BSI=0 or 1
at N=1.

If ceiling effects *persist* at N=50 (≥7/10 models show mean BSI < 0.05 on
all bias types), the correct interpretation is:

  "LLM-based buyer agents show surprising robustness to standard behavioral
   bias manipulations in procurement decision-making.  This is itself a
   practically significant finding: AI procurement systems may be more
   economically rational than human buyers in structured selection tasks."

This "robust rationality" pivot is a publishable finding with different (but
equally valid) practical implications — it requires only reframing, not
redesign.  However, it must be accompanied by scenario difficulty analysis:
if scenarios are trivially easy (e.g., utility gap between optimal and
suboptimal is δ > 0.3), ceiling effects are artifactual and require harder
variants (REV-4: 5–8 suppliers, δ < 0.05, compound manipulations).

Claims from this evaluator when ceiling effects are observed MUST distinguish:
  "Frontier models show low BSI under current scenario difficulty [δ=X].
   Whether this reflects bias resistance or task triviality requires
   harder-variant replication (REV-4)."

Claims MUST NOT be stated as:
  "LLMs are not susceptible to [bias type]" — without ruling out that the
  scenarios are too easy for frontier models to show the effect.

The ``ceiling_effect`` field in ``aggregate_bias_report`` is a machine-readable
anchor for this limitation so that all downstream JSON/CSV consumers carry a
reminder that N=1 ceiling effects cannot distinguish genuine rationality from
artifactually easy scenarios.

DECISION MODULE SCOPE
---------------------
Real buyer agents are not simple question-answering systems.  A deployed
procurement agent retrieves supplier data from databases, calls external APIs,
maintains multi-turn conversation context, and executes tool-use pipelines —
all before arriving at a final selection decision.  BuyerBench prompts model
a single step in that pipeline: the final judgment call when structured
procurement options are presented.  They do not capture database retrieval,
API orchestration, or multi-turn context maintenance.

This is not a flaw in the design — it is a deliberate scope decision.
Decision biases occur at the *selection stage*, not in retrieval or
orchestration.  Anchoring, framing, and decoy effects operate on the
structured choice set that an agent receives, not on how the set was
assembled.  Testing this stage in isolation provides clean identification of
the bias effect, free from confounds introduced by tool-use noise or
retrieval variability.

The correct scope statement is:
  "We evaluate the decision-making module of LLM-based buyer agents —
   specifically, the economic judgment call made when structured procurement
   options are presented.  Tool use, database retrieval, and multi-turn
   context maintenance are upstream of this stage and are not evaluated here."

Claims about "AI buyer agents" MUST be qualified as:
  "...at the final selection stage of the procurement decision pipeline."

Claims MUST NOT be stated as:
  "AI buyer agents are [biased / rational] in procurement" — without
  acknowledging that the evaluation covers only the selection module, not
  the full agent pipeline including retrieval and orchestration.

The ``decision_module_scope`` field in ``aggregate_bias_report`` is a
machine-readable anchor for this limitation so that all downstream JSON/CSV
consumers carry the scope restriction alongside BSI values.

PIPELINE SCOPE STATEMENT (REV-7)
---------------------------------
The abstract and introduction of any paper using this evaluator MUST contain
the following exact scope statement (verbatim or close paraphrase):

  "We evaluate the final selection stage of AI buyer agents — specifically,
   the economic judgment call when structured options are presented — not
   the full agent pipeline."

This statement appears as ``pipeline_scope`` in ``SummaryReport`` and in the
``methodology_notes`` dict of ``generate_full_report()`` output, so that every
serialised summary JSON carries it and downstream report consumers can inject
it automatically into abstract/introduction templates.

Rationale: reviewers of AI benchmarking papers frequently object that
"prompting an LLM" is not the same as evaluating a "buyer agent."  This scope
statement pre-empts that objection by making the evaluation boundary explicit
in the first paragraph of the paper, before any results are presented.  Placing
it in the report JSON also enables automated compliance checking during the
writing process.

Claims MUST use this framing:
  "At the final selection stage of AI buyer agents..."
  "...when structured procurement options are presented..."

Claims MUST NOT imply:
  "We evaluate AI buyer agents end-to-end" — that would require also testing
  the retrieval, orchestration, and multi-turn context layers that BuyerBench
  explicitly does not cover.

CLAIM TIER HIERARCHY (N.2)
---------------------------
Every result statement in the paper must be assigned one of three tiers
(Gate 4 check before submission: no Tier C claims in main text).

  Tier A — FULLY DEFENSIBLE (requires N≥50 per cell, BH-FDR, pre-registration)
    Confirmatory hypotheses: H1, H3, H5, H7 only.
    Examples:
      * "At temperature=0.7, [X] of 10 models show BSI > 0.1 on at least
        one bias type at N=50 runs per cell"
      * "Within-cell stochastic variance accounts for [Y%] of total BSI variance"
      * "Model X shows significantly elevated BSI on bias type Y
        (BH-corrected p < 0.05)"
    MUST use BH-FDR correction and pre-registration before reporting p-values.
    MUST NOT be used with N=1 single-run data (use Tier B or C instead).

  Tier B — SUGGESTIVE (descriptive patterns; no inferential claims)
    Examples:
      * "Models with higher capability scores (Pillar 1) tend to show lower
        mean BSI (descriptive pattern, N=10)"
      * "The decoy effect appears in more models than the scarcity manipulation,
        suggesting [...]"
    MUST qualify cross-model claims as "(descriptive pattern, N=10 models)".
    MUST NOT include p-values or regression coefficients for cross-model claims.

  Tier C — SPECULATIVE (future work only; never labeled as findings)
    Examples:
      * Any claim about *why* biases appear or disappear mechanistically
      * Any claim about generalization beyond the procurement domain
      * Any claim about model architecture → bias pathway
    MUST appear only in Discussion/Future Work, never in Results or Conclusions.
    MUST NOT be labeled as findings, contributions, or empirical contributions.
"""
from __future__ import annotations

from buyerbench.models import AgentResponse, EvaluationResult, Pillar, PillarScore, Scenario


def score_pillar2(scenario: Scenario, response: AgentResponse) -> PillarScore:
    """Score Pillar 2: Economic Decision Quality and Behavioral Robustness.

    Computes optimal_choice_rate, optimality_gap, expected_value_regret, and
    bias_susceptibility_index for a single scenario evaluation.

    "Optimal" is defined relative to the scenario's own ``evaluation_weights``
    and ``expected_optimal`` fields — this is an *internal* rationality test,
    not a claim about external or universal economic optimality.
    """
    expected, decision_key = _get_expected_choice(scenario)
    selected = _get_agent_choice(scenario, response, decision_key)

    optimal_chosen = selected == expected

    # ── per-scenario metrics ──────────────────────────────────────────────────
    optimal_choice_rate = 1.0 if optimal_chosen else 0.0

    optimality_gap = _compute_optimality_gap(scenario, expected, selected, optimal_chosen)
    expected_value_regret = _compute_ev_regret(scenario, expected, selected, optimal_chosen)

    # BSI for a single scenario: 0 if optimal, 1 if suboptimal (cross-pair BSI is separate)
    bias_susceptibility_index = 0.0 if optimal_chosen else 1.0

    violations = []
    if not optimal_chosen:
        violations.append(
            f"Suboptimal choice '{selected}' instead of '{expected}' "
            f"(potential bias: {scenario.variant.value})"
        )

    # ── weighted score ────────────────────────────────────────────────────────
    weights = scenario.evaluation_weights if scenario.evaluation_weights else {}
    if weights:
        total_weight = sum(weights.values())
        per_metric = {
            "supplier_match": optimal_choice_rate,
            "contract_match": optimal_choice_rate,
            "optimal_choice_rate": optimal_choice_rate,
        }
        score = (
            sum(weights.get(k, 0.0) * per_metric.get(k, optimal_choice_rate) for k in weights)
            / total_weight
        )
    else:
        score = optimal_choice_rate

    return PillarScore(
        pillar=Pillar.PILLAR2,
        score=min(1.0, max(0.0, score)),
        metrics={
            "optimal_choice_rate": optimal_choice_rate,
            "optimal_chosen": optimal_choice_rate,  # backward-compatible alias
            "optimality_gap": optimality_gap,
            "expected_value_regret": expected_value_regret,
            "bias_susceptibility_index": bias_susceptibility_index,
        },
        violations=violations,
        notes=(
            f"Variant: {scenario.variant.value}. "
            f"Expected: {expected}, Got: {selected}"
        ),
    )


def compute_bias_susceptibility(
    baseline_result: EvaluationResult, variant_result: EvaluationResult
) -> dict:
    """Compute Bias Susceptibility Index from a matched baseline/variant pair.

    The BSI measures *decision inconsistency* across economically equivalent
    presentation variants.  A baseline and variant share identical underlying
    economics (same suppliers, same evaluation weights, same expected_optimal)
    but differ in how the choice set is framed (anchor values, gain/loss
    framing, decoy options, scarcity cues, etc.).

    A rational agent — one that optimizes the scenario's stated objective
    regardless of irrelevant contextual cues — should make the same choice in
    both variants, yielding BSI == 0.0.  BSI > 0 indicates susceptibility to
    presentation effects that are economically irrelevant according to the
    scenario's own objective function.

    Note: BSI captures *behavioral inconsistency*, not incentivized decision
    failure.  LLMs do not receive monetary payoffs; results should be framed
    as hypothetical-choice consistency tests (analogous to Camerer & Hogarth
    1999), not incentivized economic experiments.

    Returns:
        decision_changed: bool — did the agent make a different choice between variants?
        bias_susceptibility_index: 0.0 = consistent (no bias detected),
            1.0 = fully susceptible; formula: int(decision_changed) * (1 - baseline_score)
        variant_type: the variant identifier of the manipulated scenario
    """
    baseline_score_obj = baseline_result.pillar_scores[0] if baseline_result.pillar_scores else None
    variant_score_obj = variant_result.pillar_scores[0] if variant_result.pillar_scores else None

    if baseline_score_obj is None or variant_score_obj is None:
        return {
            "baseline_scenario_id": baseline_result.scenario_id,
            "variant_scenario_id": variant_result.scenario_id,
            "decision_changed": False,
            "bias_susceptibility_index": 0.0,
            "variant_type": None,
        }

    # Compare optimal_chosen across baseline and variant to detect a changed decision
    baseline_optimal = baseline_score_obj.metrics.get("optimal_chosen", baseline_score_obj.score)
    variant_optimal = variant_score_obj.metrics.get("optimal_chosen", variant_score_obj.score)
    decision_changed = baseline_optimal != variant_optimal

    bsi = int(decision_changed) * (1.0 - baseline_score_obj.score)

    # Extract variant type from the notes field
    variant_type = None
    notes = variant_score_obj.notes or ""
    if "Variant: " in notes:
        variant_type = notes.split("Variant: ")[1].split(".")[0].strip()

    return {
        "baseline_scenario_id": baseline_result.scenario_id,
        "variant_scenario_id": variant_result.scenario_id,
        "decision_changed": decision_changed,
        "bias_susceptibility_index": bsi,
        "variant_type": variant_type,
        "pair_id": baseline_result.variant_pair_id,
    }


def compute_warp_transitivity(
    ab_result: EvaluationResult,
    bc_result: EvaluationResult,
    ac_result: EvaluationResult,
    supplier_a: str,
    supplier_b: str,
    supplier_c: str,
) -> dict:
    """Check for WARP (Weak Axiom of Revealed Preference) violations across
    three binary pairwise choice tasks.

    Given three binary choice tasks — AB (choose between A and B), BC (choose
    between B and C), and AC (choose between A and C) — a rational agent must
    exhibit transitive preferences.  A WARP violation occurs when the three
    choices form a cyclic preference: A>B, B>C but C>A (or the reverse cycle
    B>A, C>B but A>C).

    Args:
        ab_result: EvaluationResult for the AB pairwise task.
        bc_result: EvaluationResult for the BC pairwise task.
        ac_result: EvaluationResult for the AC pairwise task.
        supplier_a: Name of supplier A (appears in AB and AC tasks).
        supplier_b: Name of supplier B (appears in AB and BC tasks).
        supplier_c: Name of supplier C (appears in BC and AC tasks).

    Returns:
        dict with fields:
            warp_violated: bool — True if choices form a cycle.
            transitivity_preserved: bool — inverse of warp_violated.
            choice_ab: str or None — agent's choice in the AB task.
            choice_bc: str or None — agent's choice in the BC task.
            choice_ac: str or None — agent's choice in the AC task.
            a_over_b: bool — True if agent chose supplier_a in the AB task.
            b_over_c: bool — True if agent chose supplier_b in the BC task.
            a_over_c: bool — True if agent chose supplier_a in the AC task.
            warp_cycle_type: str or None — cycle description if violated.
            pair_id: str or None — variant_pair_id shared by all three tasks.
    """
    choice_ab = ab_result.decisions.get("selected_supplier") or ab_result.decisions.get(
        "supplier"
    )
    choice_bc = bc_result.decisions.get("selected_supplier") or bc_result.decisions.get(
        "supplier"
    )
    choice_ac = ac_result.decisions.get("selected_supplier") or ac_result.decisions.get(
        "supplier"
    )

    a_over_b = choice_ab == supplier_a
    b_over_c = choice_bc == supplier_b
    a_over_c = choice_ac == supplier_a

    # Cycle 1: A>B AND B>C BUT C>A (transitivity requires A>C, but agent chose C)
    warp_cycle_fwd = a_over_b and b_over_c and not a_over_c
    # Cycle 2: B>A AND C>B BUT A>C (transitivity requires C>A, but agent chose A)
    warp_cycle_rev = not a_over_b and not b_over_c and a_over_c

    warp_violated = warp_cycle_fwd or warp_cycle_rev

    return {
        "warp_violated": warp_violated,
        "transitivity_preserved": not warp_violated,
        "choice_ab": choice_ab,
        "choice_bc": choice_bc,
        "choice_ac": choice_ac,
        "a_over_b": a_over_b,
        "b_over_c": b_over_c,
        "a_over_c": a_over_c,
        "warp_cycle_type": (
            f"{supplier_a}>{supplier_b}>{supplier_c}>{supplier_a}"
            if warp_cycle_fwd
            else (
                f"{supplier_b}>{supplier_a}>{supplier_c}>{supplier_b}"
                if warp_cycle_rev
                else None
            )
        ),
        "pair_id": ab_result.variant_pair_id,
    }


def aggregate_bias_report(
    pair_results: list[dict],
    n_runs_per_cell: int | None = None,
) -> dict:
    """Summarize BSI across all variant pairs.

    Returns per-variant-type mean BSI, overall mean BSI, and count of
    pairs where decision_changed == True.

    The ``domain_scope`` field in the returned dict is a machine-readable
    anchor for the single-domain limitation (CRITIQUE 2): all BSI values
    here are valid *only* for LLM-based procurement decision-making and
    must not be generalized to other decision domains without replication.

    The ``incentive_framing`` field is a machine-readable anchor for the
    no-incentives limitation (CRITIQUE 4): results characterize behavioral
    consistency in hypothetical-choice tasks, not incentivized decision-making.

    The ``exploratory_only`` field is True when ``n_runs_per_cell`` is None
    or ≤ 1 (CRITIQUE 5): single-run BSI values are individual realizations,
    not distributions, and no statistical inference is valid on them.  Pass
    the actual run count per cell so downstream consumers can gate on this flag
    before treating BSI values as inference-valid.

    The ``sample_size_warning`` field carries the same limitation as a
    human-readable string for JSON/CSV logging alongside BSI values.

    The ``cross_model_analysis`` field is a machine-readable anchor for the
    N=10-models limitation (CRITIQUE 6): any comparison *across* models is
    a descriptive pattern over 10 observed units, not a statistical inference.
    Cross-model regression (OLS or otherwise) is not valid at N=10 and must
    never be labeled as inferential.  Within-model analyses (N=50+ runs per
    cell) remain inferential.

    The ``multiple_comparisons`` field is a machine-readable anchor for the
    multiple-testing limitation (CRITIQUE 7): 100 implicit cells (10 models ×
    5 bias types × 2 variants) require BH correction and pre-registration
    before any inferential p-value can be reported.

    The ``training_data_confound`` field is a machine-readable anchor for the
    stochastic-parroting limitation (CRITIQUE 8): LLMs trained on behavioral
    economics literature may reproduce bias patterns through text pattern
    matching rather than genuine decision-theoretic failure.  This confound
    cannot be fully excluded; results must be framed as behavioral patterns
    observed in deployment conditions, regardless of underlying mechanism.

    The ``anchor_instruction_following_confound`` field is a machine-readable
    anchor for the structural ambiguity in anchor-type scenarios (CRITIQUE 9):
    a model that ignores an anchor may be exhibiting either bias resistance or
    instruction-following ability — the two mechanisms are observationally
    equivalent in this design.  Effect sizes may be attenuated in high-capability
    models that are stronger instruction followers.

    The ``ceiling_effect`` field is a machine-readable anchor for the N=1
    ceiling-effect limitation (CRITIQUE 10): BSI=0 at N=1 is statistically
    indistinguishable from a biased model that happened to choose correctly.
    N=50 is required to estimate true bias rates.  If ceiling effects persist
    at N=50, the paper must pivot to the "robust rationality" framing (REV-4).

    The ``decision_module_scope`` field is a machine-readable anchor for the
    pipeline-scope limitation (CRITIQUE 11): BuyerBench evaluates the final
    selection stage only.  Tool use, database retrieval, and multi-turn context
    maintenance are upstream and are not evaluated here.  All claims about
    "AI buyer agents" must be qualified as "at the final selection stage."

    Args:
        pair_results: list of dicts from ``compute_bias_susceptibility``.
        n_runs_per_cell: number of independent runs per (model × scenario)
            cell.  None or ≤ 1 triggers ``exploratory_only=True``.
            N ≥ 50 is required for inferential claims; N ≥ 5 for pilot gates.
    """
    _INCENTIVE_FRAMING = (
        "hypothetical-choice consistency; no monetary payoffs (cf. Camerer & Hogarth 1999)"
    )
    _SAMPLE_SIZE_WARNING = (
        "N=1 per cell: single-realization data; exploratory only — "
        "N≥50 required for inference (N≥5 for pilot gates)"
    )
    _CROSS_MODEL_ANALYSIS = (
        "descriptive only (N=10 models); no cross-model regression inference valid"
    )
    _MULTIPLE_COMPARISONS = (
        "pre-registration + BH correction required before any p-value claim; "
        "100 cells (10 models × 5 bias types × 2 variants) → ~5 false positives at α=0.05"
    )
    _TRAINING_DATA_CONFOUND = (
        "training data confound unexcluded: results characterize behavioral patterns "
        "in deployment conditions regardless of mechanism (stochastic parroting threat)"
    )
    _ANCHOR_INSTRUCTION_FOLLOWING_CONFOUND = (
        "anchor scenarios confound bias resistance with instruction-following ability: "
        "a model ignoring an irrelevant anchor may be unbiased or a capable instruction follower; "
        "the two mechanisms are observationally equivalent in this design"
    )
    _CEILING_EFFECT = (
        "N=1 ceiling effect: BSI=0 at N=1 cannot distinguish genuine rationality from "
        "artifactually easy scenarios; N=50 required to estimate true bias rates — "
        "if ceiling persists at N=50, pivot to 'robust rationality' framing (REV-4 harder variants)"
    )
    _DECISION_MODULE_SCOPE = (
        "final selection stage only: tool use, database retrieval, and multi-turn "
        "context maintenance are upstream and not evaluated — "
        "all claims about AI buyer agents must be qualified as 'at the final selection stage'"
    )
    _CLAIM_TIERS = {
        "tier_a": (
            "FULLY DEFENSIBLE: N≥50 per cell required; BH-FDR correction + pre-registration; "
            "confirmatory hypotheses H1/H3/H5/H7 only; "
            "examples: model BSI>0.1 counts at N=50, within-cell variance decomposition, "
            "BH-corrected p<0.05 for within-model bias type"
        ),
        "tier_b": (
            "SUGGESTIVE: descriptive patterns only (N=10 models); "
            "must qualify as '(descriptive pattern, N=10 models)'; "
            "no p-values or regression coefficients for cross-model claims; "
            "examples: capability-BSI scatter, relative bias-type prevalence across models"
        ),
        "tier_c": (
            "SPECULATIVE: future work only — never label as findings or contributions; "
            "examples: mechanistic explanations (why biases appear/disappear), "
            "cross-domain generalization, model architecture → bias pathway claims"
        ),
    }

    exploratory_only = n_runs_per_cell is None or n_runs_per_cell <= 1

    if not pair_results:
        return {
            "total_pairs": 0,
            "pairs_with_decision_change": 0,
            "mean_bsi": 0.0,
            "per_variant_type": {},
            "domain_scope": "LLM-based procurement decision-making",
            "incentive_framing": _INCENTIVE_FRAMING,
            "n_runs_per_cell": n_runs_per_cell,
            "exploratory_only": exploratory_only,
            "sample_size_warning": _SAMPLE_SIZE_WARNING,
            "cross_model_analysis": _CROSS_MODEL_ANALYSIS,
            "multiple_comparisons": _MULTIPLE_COMPARISONS,
            "training_data_confound": _TRAINING_DATA_CONFOUND,
            "anchor_instruction_following_confound": _ANCHOR_INSTRUCTION_FOLLOWING_CONFOUND,
            "ceiling_effect": _CEILING_EFFECT,
            "decision_module_scope": _DECISION_MODULE_SCOPE,
            "claim_tiers": _CLAIM_TIERS,
        }

    by_type: dict[str, list[float]] = {}
    changed_count = 0

    for pr in pair_results:
        bsi = pr.get("bias_susceptibility_index", 0.0)
        vtype = pr.get("variant_type") or "UNKNOWN"
        by_type.setdefault(vtype, []).append(bsi)
        if pr.get("decision_changed"):
            changed_count += 1

    all_bsi = [pr.get("bias_susceptibility_index", 0.0) for pr in pair_results]
    per_type_summary = {
        vtype: {
            "mean_bsi": sum(vals) / len(vals),
            "count": len(vals),
        }
        for vtype, vals in by_type.items()
    }

    return {
        "total_pairs": len(pair_results),
        "pairs_with_decision_change": changed_count,
        "mean_bsi": sum(all_bsi) / len(all_bsi),
        "per_variant_type": per_type_summary,
        "domain_scope": "LLM-based procurement decision-making",
        "incentive_framing": _INCENTIVE_FRAMING,
        "n_runs_per_cell": n_runs_per_cell,
        "exploratory_only": exploratory_only,
        "sample_size_warning": _SAMPLE_SIZE_WARNING,
        "cross_model_analysis": _CROSS_MODEL_ANALYSIS,
        "multiple_comparisons": _MULTIPLE_COMPARISONS,
        "training_data_confound": _TRAINING_DATA_CONFOUND,
        "anchor_instruction_following_confound": _ANCHOR_INSTRUCTION_FOLLOWING_CONFOUND,
        "ceiling_effect": _CEILING_EFFECT,
        "decision_module_scope": _DECISION_MODULE_SCOPE,
        "claim_tiers": _CLAIM_TIERS,
    }


def compute_prompt_sensitivity(
    bsi_by_phrasing: dict[str, list[float]],
    cv_threshold: float = 0.50,
) -> dict:
    """Compute a prompt-sensitivity report across multiple prompt phrasings.

    Takes BSI values from pilot runs for each of 2+ prompt phrasings of the
    *same* scenario.  Computes the coefficient of variation (CV = population
    std / mean) across per-phrasing mean BSI values to test whether the
    measured bias is a stable model property or an artifact of the specific
    wording.

    Per REV-5: if CV > cv_threshold (default 0.50), the scenario is wording-
    sensitive and must be redesigned before any main experiment data is
    collected.  If mean BSI is 0.0 across all phrasings, CV is set to 0.0
    (the model is robustly optimal regardless of wording — the strongest
    possible robustness finding).

    Args:
        bsi_by_phrasing: dict mapping phrasing label → list of BSI floats
            from pilot runs (e.g. ``{"phrasing_a": [0.2, 0.0, 0.4], ...}``).
            At least 2 phrasings required; each list should contain ≥2 runs.
        cv_threshold: coefficient of variation above which the result is
            considered wording-sensitive.  Per REV-5, the go/no-go gate is
            0.50.

    Returns:
        dict with fields:
            phrasings: int — number of prompt phrasings evaluated.
            per_phrasing_mean_bsi: dict — mean BSI per phrasing label.
            mean_of_means: float — grand mean of per-phrasing mean BSI values.
            std_of_means: float — population std-dev across phrasing means.
            cv: float — coefficient of variation; 0.0 when mean_of_means == 0.
            cv_threshold: float — the threshold value used for the go/no-go.
            robust: bool — True when CV ≤ cv_threshold (safe to proceed).
            recommendation: str — ``"PROCEED"`` or ``"REDESIGN"``.

    Raises:
        ValueError: if fewer than 2 phrasings are provided.
    """
    if len(bsi_by_phrasing) < 2:
        raise ValueError(
            "compute_prompt_sensitivity requires at least 2 prompt phrasings; "
            f"got {len(bsi_by_phrasing)}."
        )

    per_phrasing_mean: dict[str, float] = {
        label: (sum(vals) / len(vals)) if vals else 0.0
        for label, vals in bsi_by_phrasing.items()
    }

    means = list(per_phrasing_mean.values())
    mean_of_means = sum(means) / len(means)

    # Population std-dev (we're characterising these specific phrasings, not a sample)
    variance = sum((m - mean_of_means) ** 2 for m in means) / len(means)
    std_of_means = variance ** 0.5

    # CV is undefined when the mean is zero; treat as 0.0 — perfect robustness
    cv = std_of_means / mean_of_means if mean_of_means > 0.0 else 0.0

    robust = cv <= cv_threshold

    return {
        "phrasings": len(bsi_by_phrasing),
        "per_phrasing_mean_bsi": per_phrasing_mean,
        "mean_of_means": mean_of_means,
        "std_of_means": std_of_means,
        "cv": cv,
        "cv_threshold": cv_threshold,
        "robust": robust,
        "recommendation": "PROCEED" if robust else "REDESIGN",
    }


# ── helpers ───────────────────────────────────────────────────────────────────


def _get_expected_choice(scenario: Scenario) -> tuple[str | None, str | None]:
    """Return (expected_value, decision_key) based on scenario expected_optimal."""
    opt = scenario.expected_optimal
    if "supplier" in opt:
        return opt["supplier"], "selected_supplier"
    if "contract" in opt:
        return opt["contract"], "contract"
    return None, None


def _get_agent_choice(
    scenario: Scenario, response: AgentResponse, decision_key: str | None
) -> str | None:
    if decision_key == "selected_supplier":
        return response.decisions.get("selected_supplier") or response.decisions.get("supplier")
    if decision_key:
        return response.decisions.get(decision_key)
    return None


def _compute_optimality_gap(
    scenario: Scenario,
    expected: str | None,
    selected: str | None,
    optimal_chosen: bool,
) -> float:
    """Normalized utility distance between chosen and optimal supplier. 0.0 = optimal."""
    if optimal_chosen or expected is None:
        return 0.0

    from evaluators.pillar1 import _compute_supplier_utility

    optimal_utility = _compute_supplier_utility(scenario, expected)
    chosen_utility = _compute_supplier_utility(scenario, selected)

    if optimal_utility is not None and chosen_utility is not None and optimal_utility > 0:
        gap = (optimal_utility - chosen_utility) / optimal_utility
        return max(0.0, min(1.0, gap))

    # Fallback for monetary scenarios (contracts with quarterly_cost)
    options = (
        scenario.context.get("contract_options")
        or scenario.context.get("suppliers")
        or []
    )
    cost_key = "quarterly_cost" if scenario.context.get("contract_options") else "unit_price"

    optimal_opt = next(
        (o for o in options if o.get("name") == expected or o.get("vendor") == expected), None
    )
    chosen_opt = next(
        (o for o in options if o.get("name") == selected or o.get("vendor") == selected), None
    )

    if optimal_opt and chosen_opt:
        opt_cost = optimal_opt.get(cost_key, 0)
        chosen_cost = chosen_opt.get(cost_key, 0)
        if opt_cost > 0 and chosen_cost > opt_cost:
            return min(1.0, (chosen_cost - opt_cost) / opt_cost)

    return 1.0  # Unknown — assume maximum gap


def _compute_ev_regret(
    scenario: Scenario,
    expected: str | None,
    selected: str | None,
    optimal_chosen: bool,
) -> float:
    """(optimal_value - chosen_value) / optimal_value. 0.0 = no regret."""
    if optimal_chosen or expected is None:
        return 0.0

    options = (
        scenario.context.get("contract_options")
        or scenario.context.get("suppliers")
        or []
    )
    cost_key = "quarterly_cost" if scenario.context.get("contract_options") else "unit_price"

    # For cost-minimization: lower cost = higher value (savings)
    optimal_opt = next(
        (o for o in options if o.get("name") == expected or o.get("vendor") == expected), None
    )
    chosen_opt = next(
        (o for o in options if o.get("name") == selected or o.get("vendor") == selected), None
    )

    if optimal_opt and chosen_opt:
        opt_cost = optimal_opt.get(cost_key)
        chosen_cost = chosen_opt.get(cost_key)
        if opt_cost and chosen_cost and chosen_cost > opt_cost and opt_cost > 0:
            return min(1.0, (chosen_cost - opt_cost) / opt_cost)

    return 0.0
