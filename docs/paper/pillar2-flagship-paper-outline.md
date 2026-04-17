---
type: paper
title: "Behavioral Bias Susceptibility in LLM Procurement Agents: An Eight-Bias, Human-Calibrated Flagship Study"
created: 2026-04-17
status: outline
experiment_id: buyerbench-pillar2-flagship-v1
tags:
  - pillar2
  - behavioral-economics
  - llm-bias
  - procurement
  - flagship
  - human-comparison
  - warp
  - loss-aversion
  - default-bias
  - outline
related:
  - '[[pillar2-working-paper]]'
  - '[[PAPER-STATUS]]'
  - '[[prereg_osf]]'
  - '[[irb-application-draft]]'
  - '[[SUBMISSION-PACKAGE-PILLAR2]]'
---

# Behavioral Bias Susceptibility in LLM Procurement Agents: An Eight-Bias, Human-Calibrated Flagship Study

**Authors:** [Author list TBD]

**Pre-registration:** OSF registration ID [TBD — register flagship pre-reg addendum before data collection begins; extends `docs/preregistration/prereg_osf.md` with H8/H9/H10 confirmatory designations]

**Code and data:** `https://github.com/[org]/BuyerBench` (MIT License)

**Relationship to prior work:** This is the flagship expansion of the pre-registered realistic design study (`pillar2-working-paper.md`, experiment ID `buyerbench-pillar2-realistic-v1`). That study covers 5 bias types × N=50 per cell × 10 models. This study expands to 8 bias types × N=100 per cell × 10 models × 2 temperatures × 2 prompt versions, and adds a human comparison arm (N=100 Prolific participants). All realistic-design results are incorporated here; no findings are duplicated.

**Version:** Outline. All result cells marked `{{RESULT:...}}` require data from the flagship experiment and human survey arm. No result figures should be populated before Gate 3 clearance and IRB approval.

> **Scope statement (REV-7):** This paper evaluates the *final selection stage* of LLM-based buyer agents — specifically, the economic judgment made when structured procurement options are presented — and not the full agent pipeline (retrieval, API calls, multi-turn context). See §3.1 for full justification.

> **Data status (REV-3):** All `{{RESULT:...}}` placeholders require flagship N=100/cell data and human arm data. Single-run and N=50 pilot data are cited as infrastructure validation only.

---

## Abstract

[PLACEHOLDER — write after data collection, following the template below]

*Template:* We present a flagship expansion of a pre-registered benchmark measuring behavioral bias susceptibility in LLM-based procurement agents. Extending our prior five-bias realistic study to eight canonical bias types — adding default/status-quo bias, loss aversion, and preference transitivity (WARP) — and calibrating against human decision-maker baselines via a pre-registered Prolific survey, we evaluate `{{RESULT: n_models}}` frontier language models across `{{RESULT: n_total_runs}}` independent procurement decision trials. Using the Bias Susceptibility Index (BSI), we find `{{RESULT: n_models_with_bias}}` models show detectable bias on at least one type at N=100/cell (BH-FDR q=0.05). LLM effect sizes (Cohen's d) are `{{RESULT: human_comparison_direction}}` human behavioral benchmarks (H10; p = `{{RESULT: H10_p}}`). WARP transitivity violations occur in `{{RESULT: warp_violation_rate}}` of model–run pairs, indicating systematic preference intransitivity under pairwise framing. Chain-of-thought prompting reduces anchoring susceptibility (`{{RESULT: cot_anchoring_reduction}}`) but does not attenuate decoy effects (H8; interaction contrast p = `{{RESULT: H8_p}}`).

---

## 1. Introduction

### 1.1 Motivation

[Inherit from `pillar2-working-paper.md` §1.1 — expand with flagship context]

The realistic design study (experiment ID: `buyerbench-pillar2-realistic-v1`) established baseline measurements for five canonical bias types in ten frontier LLMs across N=50 independent runs per cell. The present flagship expansion addresses three gaps left open by that study:

1. **Coverage:** Three bias types well-documented in the human behavioral economics literature — default/status-quo bias, loss aversion with switching costs, and preference transitivity (WARP violations) — were excluded from the realistic design to control scope. These are added here as UPGRADE-8/9/10.

2. **Human calibration:** The realistic study tests whether LLMs are *internally inconsistent* (BSI > 0) but cannot compare effect magnitudes to human behavioral benchmarks. The human comparison arm (N=100 Prolific participants; pre-registered between-subjects design) enables a direct H10 comparison: are LLMs more or less susceptible than humans in the same procurement domain?

3. **Prompting robustness:** The CoT × bias-type interaction (H8) was pre-registered but not the primary focus of the realistic design. The flagship allocates N=100 per cell × 2 prompt versions to provide adequate power for the full interaction test.

### 1.2 Scope and Limitations

[Inherit from `pillar2-working-paper.md` §1.2; add the following:]

**Human arm scope:** The human comparison arm uses the same scenario prompts as the LLM experiments (Qualtrics survey delivery; between-subjects variant assignment). Participants are Prolific workers meeting eligibility criteria (native English, no prior BuyerBench exposure; see §3.6). This arm provides calibration benchmarks for H10 only — it is not a replication of the full LLM battery.

**WARP arm scope:** WARP (Weak Axiom of Revealed Preference) is tested via three pairwise binary choices (Supplier A vs. B; B vs. C; A vs. C) across N=100 independent runs per pair per model. WARP violations are detected post-hoc as intransitive choice cycles (A ≻ B, B ≻ C, C ≻ A) and quantified as rates per model. This is a preference-consistency test, not a bias-manipulation test; no "baseline vs. treatment" framing applies.

### 1.3 Contributions

[Extend `pillar2-working-paper.md` §1.3 with three additional contributions:]

5. **Eight-bias coverage:** First benchmark to cover WARP transitivity and default/status-quo bias in LLM procurement agents alongside the five canonical types, providing a comprehensive behavioral profile of frontier LLMs on structured supplier-selection tasks.

6. **Human calibration arm:** First direct comparison of LLM vs. human behavioral bias susceptibility in the procurement domain, enabling a quantitative answer to whether LLMs amplify, replicate, or attenuate the biases measured in human procurement decision-makers (H10).

7. **CoT interaction evidence:** Systematic comparison of chain-of-thought vs. standard prompting across all eight bias types at N=100/cell, providing the first adequately powered test of whether CoT's bias-attenuation effect is uniform (H8: decoy is expected to resist CoT; anchoring to respond to it).

### 1.4 Paper Outline

Section 2 surveys the behavioral economics literature for each of the eight bias types, the LLM-bias literature, and the prior realistic study. Section 3 describes the extended methodology: eight-scenario battery, WARP triplet design, human arm procedures, and the full statistical analysis plan. Section 4 presents results: pre-registered confirmatory hypotheses H1–H10, exploratory descriptive analyses, human-LLM comparison, and WARP transitivity rates. Section 5 discusses implications, limitations, and future work. Section 6 concludes.

---

## 2. Related Work

### 2.1 Human Behavioral Bias Benchmarks (Eight Bias Types)

[Inherit §2.1 from `pillar2-working-paper.md` for anchoring, framing, decoy, scarcity, sunk cost; add:]

**Default / Status-Quo Bias:** The tendency to prefer the current or default option over alternatives, even when switching is costless and dominated alternatives are present. @samuelson1988status documents a d ≈ 0.90 effect in resource allocation; @johnson2003defaults show opt-in vs. opt-out default assignment shifts choice rates by 40–85 percentage points in organ donation and retirement savings. In procurement, this manifests as an unwillingness to switch incumbent suppliers even when a new entrant offers strictly superior price–quality–delivery trade-offs. **Expected LLM behavior:** Structured rubrics make the current supplier's score computable; if the agent optimizes the rubric it should switch. We predict default bias is substantially attenuated in LLMs relative to human baselines, but residual status-quo preference from RLHF training (optimizing for consistency with prior outputs) may produce nonzero BSI.

**Loss Aversion / Switching Cost:** The tendency to weight potential losses more heavily than equivalent gains, as formalized by Prospect Theory [@kahneman1979prospect]. In the BuyerBench scenario, loss framing (switching away from a known supplier with a guaranteed price vs. switching to a new supplier with a potentially lower but uncertain price) is expected to produce BSI when the expected-value calculation under stated weights would recommend switching. Human baselines: loss aversion coefficient λ ≈ 2.25 (Kahneman & Tversky 1979); switching cost framing effect d ≈ 0.50–0.80. **Expected LLM behavior:** LLMs trained on economic text have extensive exposure to prospect theory and loss aversion framing, which may either reproduce the bias (memorization) or suppress it (metalinguistic awareness of the effect).

**WARP / Preference Transitivity:** The Weak Axiom of Revealed Preference [@samuelson1938note] requires that if option A is chosen over B and B over C, then A must be chosen over C in pairwise binary choice. WARP violations indicate preference intransitivity — a fundamental inconsistency incompatible with rational choice theory. The LLM mechanism is different from classical bias manipulations: no framing manipulation is applied; the three pairwise choices are presented independently (fresh session per run), making WARP violations a property of stochastic choice patterns across runs rather than within-session manipulation effects. **Expected LLM behavior:** With N=100 runs per pair per model, we expect WARP violation rates of `{{RESULT: warp_prior_violation_rate}}`. Even small rates are scientifically significant as they are incompatible with rationality axioms.

### 2.2 LLM Cognitive Bias Literature

[Inherit from `pillar2-working-paper.md` §2.2]

### 2.3 Procurement AI Evaluation Gap

[Inherit from `pillar2-working-paper.md` §2.3]

### 2.4 Human–AI Decision-Making Comparison

[New section for flagship:]

A growing literature compares human and LLM behavioral patterns using matched stimuli. @binz2023using evaluate 12 cognitive biases using Kahneman & Tversky–style vignettes and find GPT-4 shows human-like patterns on several — but the mechanism (training data memorization vs. emergent cognitive consistency) remains debated. The critical gap: no prior study uses matched human and LLM data on the *same domain-specific procurement tasks*, preventing apples-to-apples effect size comparison. The H10 arm of this study is the first to fill that gap.

---

## 3. Methodology

### 3.1 Decision Module Scope and Pipeline Rationale

[Inherit from `pillar2-working-paper.md` §3.1]

### 3.2 Experimental Design — LLM Arm

**Factorial structure:**

| Dimension | Realistic Design (prior paper) | Flagship Design (this paper) |
|---|---|---|
| Models | 10 OpenRouter models | Same 10 models |
| Bias types | 5 | 8 (+ default, loss_aversion, WARP) |
| Variants per type | 2 (baseline + treatment) | 2 (+ WARP: 3 pairwise pairs) |
| N per cell | 50 | 100 |
| Temperatures | [0.7] | [0.7, 0.0] |
| Prompt versions | [standard] | [standard, cot] |
| Total scenario slots | 10 | 17 (WARP = 3 slots) |
| Total LLM runs | 5,000 | 68,000 |
| Estimated cost | $750 | $13,600 |

**Scenario identifiers:**

| Bias type | Baseline | Treatment | Notes |
|---|---|---|---|
| Anchoring | `p2-01-anchor-high-BASELINE` | `p2-01-anchor-high-ANCHOR_HIGH` | Prior paper |
| Framing | `p2-02-framing-GAIN` | `p2-02-framing-LOSS` | Prior paper; GAIN is reference |
| Decoy | `p2-03-decoy-BASELINE` | `p2-03-decoy-DECOY` | Prior paper |
| Scarcity | `p2-04-scarcity-BASELINE` | `p2-04-scarcity-SCARCITY` | Prior paper |
| Sunk Cost | `p2-05-sunk-cost-BASELINE` | `p2-05-sunk-cost-SUNK_COST` | Prior paper |
| Default | `p2-06-default-BASELINE` | `p2-06-default-DEFAULT` | UPGRADE-8 |
| Loss Aversion | `p2-07-loss-aversion-BASELINE` | `p2-07-loss-aversion-LOSS_AVERSION` | UPGRADE-9 |
| WARP | `p2-08-warp-WARP_AB` | `p2-08-warp-WARP_BC` / `p2-08-warp-WARP_AC` | UPGRADE-10; triplet |

**Hard-difficulty variants** (activated if N=50 realistic run shows ceiling at ≥7/10 models):

| Scenario ID | Suppliers | δ | Manipulation |
|---|---|---|---|
| `p2-09-compound` | 6 | 0.031 | Anchor ($118/unit) + scarcity (4 slots, closes EOD) simultaneously |
| `p2-10-anchor-hard` | 7 | 0.039 | Very high anchor at $148/unit (2.2× catalog max) |
| `p2-11-scarcity-hard` | 8 | 0.005 | Scarcity cue on cheapest supplier; near-zero utility gap |

### 3.3 Experimental Design — Human Arm

**Design:** Between-subjects. Survey Version A (baseline scenarios only) vs. Survey Version B (treatment scenarios only). Each participant completes all five core bias-type scenarios (anchoring, framing, decoy, scarcity, sunk cost); WARP and the new UPGRADE-8/9/10 types are included as exploratory extensions with N≥25 per condition.

**Recruitment:** Prolific platform. Eligibility: US-based, native English, no prior exposure to BuyerBench. Target N=50 per version (100 total).

**Attention checks:** Two pre-designed checks embedded at positions 2 and 5 of the 7-question survey (including ATTN1: $12 vs. $89 price comparison; ATTN2: instruction reading check). Participants failing either check are excluded before BSI computation.

**Survey instruments:** `survey/survey_A_baseline.json`, `survey/survey_B_treatment.json` (QSF format, ready for Qualtrics import).

**IRB:** Exempt (45 CFR 46.104(d)(2)) — no sensitive data, no deception. IRB application at `docs/paper/irb-application-draft.md`. Study activation blocked until institutional IRB approval.

**Human BSI computation:** Same formula as LLM arm: `bsi = int(decision_changed) * (1 - baseline_score)`. For human participants, `decision_changed = (response_B ≠ modal_response_A)`, where `modal_response_A` is the modal choice in the Version A (baseline) group for each scenario.

### 3.4 Scenario Difficulty: Hard Variants

[Describe REV-4 hard-difficulty scenarios if activated by Gate 3 ceiling check — see §3.2 table above]

### 3.5 BSI Formula and Estimation

[Inherit from `pillar2-working-paper.md` §3.3; add:]

**WARP-specific measurement:** WARP violations are not measured via BSI. Instead, for each model we compute the empirical choice distribution over N=100 runs for each of the three pairwise pairs, then compute the WARP violation rate as the fraction of simulated (A≻B, B≻C, C≻A) or (A≺B, B≺C, C≺A) cycles among all possible run-triplets. A run-triplet is one draw from each of the three pairs' empirical distributions.

Formally:

```
warp_violation_rate(model) = P(A≻B) × P(B≻C) × P(C≻A) + P(A≺B) × P(B≺C) × P(C≺A)
```

where probabilities are estimated from the N=100 runs per pair. Under rationality, `warp_violation_rate = 0`.

### 3.6 Statistical Analysis Plan

**Confirmatory tests (BH-FDR at q=0.05, all pre-registered):**

| Hypothesis | Type | Test | New in flagship? |
|---|---|---|---|
| H1 — Bias Universality | Confirmatory | Proportion test: ≥1 model BSI > 0.10 on ≥1 type | No |
| H3 — Decoy Reliability | Confirmatory | Dunnett's test vs. cross-bias mean | No |
| H5 — Framing Asymmetry | Confirmatory | Paired t-test: Loss BSI > Gain BSI | No |
| H7 — Variance Proportionality | Confirmatory | OLS: std_bsi ~ mean_bsi | No |
| H8 — CoT × Bias Interaction | Confirmatory | WLS interaction: CoT × BiasType | **Yes** |
| H10 — Human Calibration | Confirmatory | Cohen's d comparison: LLM vs. human meta-analytic baselines; Welch t-test for human arm | **Yes** |

**Exploratory analyses:**

| Hypothesis | Test |
|---|---|
| H2 — Capability-Bias Tradeoff | Spearman ρ: Pillar 1 score vs. mean BSI (N=10 models, descriptive) |
| H4 — Anchoring Magnitude Proportionality | Requires p2-01b (ANCHOR_LOW) — deferred to future work |
| H6 — Sunk Cost × Capability | Spearman ρ: Pillar 1 vs. BSI_sunk_cost |
| H9 — Model-Specific Bias Profiles | Per-model radar chart (8-axis); hierarchical clustering |
| Default bias UPGRADE-8 | BSI_default comparison to BSI cross-type mean; human vs. LLM |
| Loss aversion UPGRADE-9 | BSI_loss_aversion; λ-implied vs. observed switching rates |
| WARP rate by model | warp_violation_rate per model; capability correlation |
| WARP rate by temperature | warp_violation_rate at T=0.7 vs. T=0.0 |

**Regressions:**

- *Level 1 WLS (G.2):* `BSI ~ Treatment + BiasType + Model` (cell-level, weights = n_valid_runs; excludes WARP)
- *Level 2 WLS:* `mean_BSI_model ~ Pillar1Score` (model-level, N=10; descriptive only — no p-values reported)
- *CoT interaction:* `BSI ~ PromptVersion × BiasType + Model` (confirmatory for H8; WARP excluded)
- *Variance decomposition:* ANOVA partition into Model, BiasType, Treatment, Temperature, PromptVersion, residual
- *WARP logistic:* `P(WARP_violation) ~ Model + Temperature` (exploratory; N=10 models × 2 temperatures)

---

## 4. Results

> **Status:** All cells contain `{{RESULT:...}}` placeholders. Do not populate before flagship experiment data is available (Gate 3 clearance + IRB approval for human arm).

### 4.1 Infrastructure and Pilot Validation

{{RESULT: pilot_validation_summary}} (error rate, schema validity, run_id uniqueness)

| Run | Total | Valid | Error rate | Gate 1 |
|---|---|---|---|---|
| Pilot (mock, N=5) | 50 | 50 | 0% | PASS |
| Pilot full (real, N=30) | 3,000 | `{{RESULT: pilot_full_valid}}` | `{{RESULT: pilot_full_error_rate}}` | `{{RESULT: gate1_decision}}` |
| Flagship (N=100) | 68,000 | `{{RESULT: flagship_valid}}` | `{{RESULT: flagship_error_rate}}` | — |

### 4.2 Confirmatory Results: H1 — Bias Universality

**Hypothesis:** At least one model shows BSI > 0.10 on at least one bias type at N=100/cell (BH-corrected p < 0.05).

**Result:** `{{RESULT: H1_verdict}}` (SUPPORTED / NOT SUPPORTED)

| Metric | Value |
|---|---|
| Models with BSI > 0.10 on ≥1 bias type (BH p < 0.05) | `{{RESULT: H1_n_models}}` / 10 |
| Bias type with highest prevalence | `{{RESULT: H1_top_bias_type}}` |
| BH-corrected p-value (H1 test) | `{{RESULT: H1_p_bh}}` |

### 4.3 Confirmatory Results: H3 — Decoy Effect Reliability

**Result:** `{{RESULT: H3_verdict}}`

| Metric | Value |
|---|---|
| Decoy mean BSI | `{{RESULT: H3_decoy_mean_bsi}}` |
| Cross-bias mean BSI | `{{RESULT: H3_cross_bias_mean_bsi}}` |
| Dunnett's d | `{{RESULT: H3_dunnett_d}}` |
| BH-corrected p | `{{RESULT: H3_dunnett_p_bh}}` |

### 4.4 Confirmatory Results: H5 — Framing Asymmetry (Loss > Gain)

**Result:** `{{RESULT: H5_verdict}}`

| Metric | Value |
|---|---|
| Mean BSI (LOSS) | `{{RESULT: H5_loss_bsi}}` |
| Mean BSI (GAIN) | `{{RESULT: H5_gain_bsi}}` |
| Paired t-statistic | `{{RESULT: H5_t}}` |
| BH-corrected p | `{{RESULT: H5_p_bh}}` |

### 4.5 Confirmatory Results: H7 — Stochastic Variance Proportional to BSI

**Result:** `{{RESULT: H7_verdict}}`

| Metric | Value |
|---|---|
| β₁ (std_bsi ~ mean_bsi slope) | `{{RESULT: H7_beta}}` |
| R² | `{{RESULT: H7_r2}}` |
| BH-corrected p | `{{RESULT: H7_p_bh}}` |

### 4.6 Confirmatory Results: H8 — CoT Reduces Anchoring but Not Decoy

**Hypothesis:** Chain-of-thought prompting reduces anchoring BSI more than decoy BSI (interaction contrast).

**Result:** `{{RESULT: H8_verdict}}`

| Bias type | BSI (standard) | BSI (CoT) | Δ BSI | Interaction p (BH) |
|---|---|---|---|---|
| Anchoring | `{{RESULT: H8_anchoring_standard}}` | `{{RESULT: H8_anchoring_cot}}` | `{{RESULT: H8_anchoring_delta}}` | `{{RESULT: H8_anchoring_p}}` |
| Decoy | `{{RESULT: H8_decoy_standard}}` | `{{RESULT: H8_decoy_cot}}` | `{{RESULT: H8_decoy_delta}}` | `{{RESULT: H8_decoy_p}}` |
| Framing | `{{RESULT: H8_framing_standard}}` | `{{RESULT: H8_framing_cot}}` | `{{RESULT: H8_framing_delta}}` | `{{RESULT: H8_framing_p}}` |
| Scarcity | `{{RESULT: H8_scarcity_standard}}` | `{{RESULT: H8_scarcity_cot}}` | `{{RESULT: H8_scarcity_delta}}` | `{{RESULT: H8_scarcity_p}}` |
| Sunk Cost | `{{RESULT: H8_sunk_cost_standard}}` | `{{RESULT: H8_sunk_cost_cot}}` | `{{RESULT: H8_sunk_cost_delta}}` | `{{RESULT: H8_sunk_cost_p}}` |
| Default | `{{RESULT: H8_default_standard}}` | `{{RESULT: H8_default_cot}}` | `{{RESULT: H8_default_delta}}` | exploratory |
| Loss Aversion | `{{RESULT: H8_loss_av_standard}}` | `{{RESULT: H8_loss_av_cot}}` | `{{RESULT: H8_loss_av_delta}}` | exploratory |

### 4.7 Confirmatory Results: H10 — Human Benchmark Calibration

**Hypothesis:** LLM BSI effect sizes are smaller than human meta-analytic benchmarks for the same bias categories.

**Result:** `{{RESULT: H10_verdict}}`

**Table 1. LLM vs. Human Bias Effect Sizes**

| Bias type | Human baseline d (literature) | LLM mean BSI | LLM Cohen's d | Ratio (LLM/human) | H10 direction |
|---|---|---|---|---|---|
| Anchoring | d ≈ 2.70 | `{{RESULT: h10_llm_bsi_anchoring}}` | `{{RESULT: h10_llm_d_anchoring}}` | `{{RESULT: h10_ratio_anchoring}}` | `{{RESULT: h10_dir_anchoring}}` |
| Framing | d ≈ 1.80 | `{{RESULT: h10_llm_bsi_framing}}` | `{{RESULT: h10_llm_d_framing}}` | `{{RESULT: h10_ratio_framing}}` | `{{RESULT: h10_dir_framing}}` |
| Decoy | d ≈ 0.40 | `{{RESULT: h10_llm_bsi_decoy}}` | `{{RESULT: h10_llm_d_decoy}}` | `{{RESULT: h10_ratio_decoy}}` | `{{RESULT: h10_dir_decoy}}` |
| Scarcity | d ≈ 0.70 | `{{RESULT: h10_llm_bsi_scarcity}}` | `{{RESULT: h10_llm_d_scarcity}}` | `{{RESULT: h10_ratio_scarcity}}` | `{{RESULT: h10_dir_scarcity}}` |
| Sunk Cost | d ≈ 0.85 | `{{RESULT: h10_llm_bsi_sunk_cost}}` | `{{RESULT: h10_llm_d_sunk_cost}}` | `{{RESULT: h10_ratio_sunk_cost}}` | `{{RESULT: h10_dir_sunk_cost}}` |
| Default | d ≈ 0.90 (Samuelson & Zeckhauser 1988) | `{{RESULT: h10_llm_bsi_default}}` | `{{RESULT: h10_llm_d_default}}` | `{{RESULT: h10_ratio_default}}` | exploratory |
| Loss Aversion | d ≈ 0.60–0.80 | `{{RESULT: h10_llm_bsi_loss_av}}` | `{{RESULT: h10_llm_d_loss_av}}` | `{{RESULT: h10_ratio_loss_av}}` | exploratory |

**Human arm comparison (Welch t-test; N=50 per condition):**

| Bias type | Human mean BSI (Version B vs. A) | LLM mean BSI | Welch t | p |
|---|---|---|---|---|
| Anchoring | `{{RESULT: h10_human_bsi_anchoring}}` | `{{RESULT: h10_llm_bsi_anchoring}}` | `{{RESULT: h10_welch_t_anchoring}}` | `{{RESULT: h10_welch_p_anchoring}}` |
| Framing | `{{RESULT: h10_human_bsi_framing}}` | `{{RESULT: h10_llm_bsi_framing}}` | `{{RESULT: h10_welch_t_framing}}` | `{{RESULT: h10_welch_p_framing}}` |
| Decoy | `{{RESULT: h10_human_bsi_decoy}}` | `{{RESULT: h10_llm_bsi_decoy}}` | `{{RESULT: h10_welch_t_decoy}}` | `{{RESULT: h10_welch_p_decoy}}` |
| Scarcity | `{{RESULT: h10_human_bsi_scarcity}}` | `{{RESULT: h10_llm_bsi_scarcity}}` | `{{RESULT: h10_welch_t_scarcity}}` | `{{RESULT: h10_welch_p_scarcity}}` |
| Sunk Cost | `{{RESULT: h10_human_bsi_sunk_cost}}` | `{{RESULT: h10_llm_bsi_sunk_cost}}` | `{{RESULT: h10_welch_t_sunk_cost}}` | `{{RESULT: h10_welch_p_sunk_cost}}` |

### 4.8 Exploratory: Default Bias (UPGRADE-8)

**Table 2. Default Bias Results — `{{RESULT: default_n_models_biased}}` / 10 models show BSI > 0.05**

| Model | BSI (BASELINE) | BSI (DEFAULT treatment) | Δ BSI | Decision change rate |
|---|---|---|---|---|
| GPT-4o | `{{RESULT: default_gpt4o_baseline}}` | `{{RESULT: default_gpt4o_treatment}}` | `{{RESULT: default_gpt4o_delta}}` | `{{RESULT: default_gpt4o_change_rate}}` |
| Claude 3.5 Sonnet | `{{RESULT: default_claude_baseline}}` | `{{RESULT: default_claude_treatment}}` | `{{RESULT: default_claude_delta}}` | `{{RESULT: default_claude_change_rate}}` |
| Gemini Pro 1.5 | `{{RESULT: default_gemini_baseline}}` | `{{RESULT: default_gemini_treatment}}` | `{{RESULT: default_gemini_delta}}` | `{{RESULT: default_gemini_change_rate}}` |
| [remaining 7 models] | ... | ... | ... | ... |

### 4.9 Exploratory: Loss Aversion (UPGRADE-9)

**Table 3. Loss Aversion Results — `{{RESULT: loss_av_n_models_biased}}` / 10 models show BSI > 0.05**

| Model | BSI (BASELINE) | BSI (LOSS_AVERSION treatment) | Δ BSI | Implied λ (Prospect Theory) |
|---|---|---|---|---|
| GPT-4o | `{{RESULT: loss_av_gpt4o_baseline}}` | `{{RESULT: loss_av_gpt4o_treatment}}` | `{{RESULT: loss_av_gpt4o_delta}}` | `{{RESULT: loss_av_gpt4o_lambda}}` |
| [remaining 9 models] | ... | ... | ... | ... |
| Cross-model mean | — | — | `{{RESULT: loss_av_mean_delta}}` | `{{RESULT: loss_av_mean_lambda}}` |

*Note on implied λ:* For each model, the implied Prospect Theory loss-aversion coefficient is estimated as the switching-threshold BSI relative to the expected-value-optimal switching point, assuming a simple two-outcome lottery framing. This is a descriptive approximation; formal parameter estimation requires a richer choice battery.

### 4.10 Exploratory: WARP Transitivity Violations (UPGRADE-10)

**Table 4. WARP Violation Rates — `{{RESULT: warp_n_models_with_violations}}` / 10 models show violation rate > 0**

| Model | P(A≻B) | P(B≻C) | P(A≻C) | WARP violation rate | T=0.7 | T=0.0 |
|---|---|---|---|---|---|---|
| GPT-4o | `{{RESULT: warp_gpt4o_pab}}` | `{{RESULT: warp_gpt4o_pbc}}` | `{{RESULT: warp_gpt4o_pac}}` | `{{RESULT: warp_gpt4o_rate}}` | — | — |
| [remaining 9 models] | ... | ... | ... | ... | ... | ... |
| Cross-model mean | — | — | — | `{{RESULT: warp_mean_rate}}` | `{{RESULT: warp_mean_rate_t07}}` | `{{RESULT: warp_mean_rate_t00}}` |

*Interpretation:* Under rationality (consistent preferences), the WARP violation rate should be zero. Nonzero rates at T=0.0 (deterministic decoding) indicate structural intransitivity in the model's preference function, not just sampling noise.

### 4.11 Exploratory: Temperature Robustness

**Table 5. BSI at T=0.7 vs. T=0.0 — Cross-Model Mean**

| Bias type | BSI (T=0.7) | BSI (T=0.0) | Δ (T=0.7 − T=0.0) | Interpretation |
|---|---|---|---|---|
| Anchoring | `{{RESULT: t_anchoring_07}}` | `{{RESULT: t_anchoring_00}}` | `{{RESULT: t_anchoring_delta}}` | `{{RESULT: t_anchoring_interp}}` |
| Framing | `{{RESULT: t_framing_07}}` | `{{RESULT: t_framing_00}}` | `{{RESULT: t_framing_delta}}` | `{{RESULT: t_framing_interp}}` |
| Decoy | `{{RESULT: t_decoy_07}}` | `{{RESULT: t_decoy_00}}` | `{{RESULT: t_decoy_delta}}` | `{{RESULT: t_decoy_interp}}` |
| Scarcity | `{{RESULT: t_scarcity_07}}` | `{{RESULT: t_scarcity_00}}` | `{{RESULT: t_scarcity_delta}}` | `{{RESULT: t_scarcity_interp}}` |
| Sunk Cost | `{{RESULT: t_sunk_cost_07}}` | `{{RESULT: t_sunk_cost_00}}` | `{{RESULT: t_sunk_cost_delta}}` | `{{RESULT: t_sunk_cost_interp}}` |
| Default | `{{RESULT: t_default_07}}` | `{{RESULT: t_default_00}}` | `{{RESULT: t_default_delta}}` | `{{RESULT: t_default_interp}}` |
| Loss Aversion | `{{RESULT: t_loss_av_07}}` | `{{RESULT: t_loss_av_00}}` | `{{RESULT: t_loss_av_delta}}` | `{{RESULT: t_loss_av_interp}}` |

*Interpretation guide:* If Δ ≈ 0, the result is temperature-robust (structural). If Δ > 0.10, the bias manifests primarily through stochastic sampling and may not constitute a stable deployed-system risk. If Δ < 0 (T=0.0 produces higher BSI), the effect is structural and replicated under deterministic decoding — the strongest evidence of genuine preference inconsistency.

### 4.12 Exploratory: Model-Specific Bias Profiles (H9)

[Figure: Radar chart with 8 axes (one per bias type) per model; Figure: Hierarchical cluster dendrogram of models by BSI profile]

**Table 6. BSI Heatmap — 10 Models × 8 Bias Types**

| Model | Anchoring | Framing | Decoy | Scarcity | Sunk Cost | Default | Loss Av. | WARP rate |
|---|---|---|---|---|---|---|---|---|
| GPT-4o | `{{RESULT:...}}` | ... | ... | ... | ... | ... | ... | `{{RESULT:...}}` |
| Claude 3.5 Sonnet | ... | ... | ... | ... | ... | ... | ... | ... |
| Gemini Pro 1.5 | ... | ... | ... | ... | ... | ... | ... | ... |
| LLaMA 3.1 405B | ... | ... | ... | ... | ... | ... | ... | ... |
| Mistral Large | ... | ... | ... | ... | ... | ... | ... | ... |
| DeepSeek Chat | ... | ... | ... | ... | ... | ... | ... | ... |
| Qwen 2.5 72B | ... | ... | ... | ... | ... | ... | ... | ... |
| Cohere Command R+ | ... | ... | ... | ... | ... | ... | ... | ... |
| Mixtral 8x22B | ... | ... | ... | ... | ... | ... | ... | ... |
| Yi Large | ... | ... | ... | ... | ... | ... | ... | ... |

### 4.13 Exploratory: Variance Decomposition

**Table 7. ANOVA Variance Partition (% of total BSI variance)**

| Source | SS | % variance | Interpretation |
|---|---|---|---|
| Model | `{{RESULT: vd_model_ss}}` | `{{RESULT: vd_model_pct}}` | Between-model heterogeneity |
| BiasType | `{{RESULT: vd_bias_ss}}` | `{{RESULT: vd_bias_pct}}` | Differential susceptibility by type |
| Treatment | `{{RESULT: vd_treatment_ss}}` | `{{RESULT: vd_treatment_pct}}` | Manipulation efficacy |
| Temperature | `{{RESULT: vd_temp_ss}}` | `{{RESULT: vd_temp_pct}}` | T=0.7 vs. T=0.0 contribution |
| PromptVersion | `{{RESULT: vd_prompt_ss}}` | `{{RESULT: vd_prompt_pct}}` | Standard vs. CoT contribution |
| Residual (within-cell) | `{{RESULT: vd_resid_ss}}` | `{{RESULT: vd_resid_pct}}` | Stochastic run-to-run variance |

### 4.14 Hard-Difficulty Scenarios (REV-4)

[Activate this section only if Gate 3 ceiling check shows ≥7/10 models with BSI < 0.05 across all 8 types]

**Table 8. Hard-Difficulty Scenario Results (p2-09 through p2-11)**

| Scenario | Suppliers | δ | Manipulation | N models biased (BSI>0.05) | Cross-model mean BSI |
|---|---|---|---|---|---|
| p2-09-compound | 6 | 0.031 | Anchor + scarcity | `{{RESULT:...}}` | `{{RESULT:...}}` |
| p2-10-anchor-hard | 7 | 0.039 | Very high anchor | `{{RESULT:...}}` | `{{RESULT:...}}` |
| p2-11-scarcity-hard | 8 | 0.005 | Scarcity + minimal gap | `{{RESULT:...}}` | `{{RESULT:...}}` |

---

## 5. Discussion

### 5.1 Interpretation of Confirmatory Results (H1–H10)

[Populate after data; use `pillar2-working-paper.md` §5.1 as template; extend with H8 and H10 interpretation]

**Template:** Pre-registered confirmatory findings for H1/H3/H5/H7 are inherited from the realistic design study. The flagship adds two new confirmatory results:

*H8 (CoT × BiasType interaction):* If supported — chain-of-thought reasoning selectively attenuates biases that involve explicit numerical anchors (anchoring, loss aversion) but not biases that operate through option-set structure (decoy, WARP). This is consistent with the hypothesis that CoT allows the model to "step back" from numerical reference points but does not overcome the structural pressure of dominated alternatives.

*H10 (Human calibration):* If LLM effect sizes are smaller (supported H10) — LLMs show "engineered rationality" in structured domains: the explict scoring rubric acts as a commitment device that partially overrides trained behavioral patterns. If LLM effect sizes are larger (H10 not supported) — LLMs are *more* susceptible than humans, possibly because they lack the metacognitive correction that humans apply when they notice they are "being tested."

**Robust rationality pivot framing:** If H1 is not supported (all models BSI ≈ 0 at N=100/cell), the flagship pivot claim is: "LLMs show robust decision-theoretic rationality on structured multi-attribute procurement tasks, withstanding eight canonical bias types that reliably affect human decision-makers. This suggests structured rubrics function as a commitment mechanism that may be a useful design tool for deployed buyer agents."

### 5.2 WARP Violations and Rationality Axioms

[Populate after data:]

WARP violations deserve separate discussion because they are structurally different from BSI-measured biases: they are not manipulated — they emerge from the model's stochastic choice distribution across independent runs. A nonzero WARP violation rate at T=0.0 (deterministic decoding) implies that the model's *modal* preference ordering is intransitive — a fundamental departure from rational choice axioms that cannot be attributed to sampling noise.

Possible mechanisms: (1) context-sensitivity: the three pairwise scenarios present slightly different contextual emphasis, which may shift the model's implicit weighting even when evaluation weights are stated identically; (2) training data memorization: if training contains conflicting recommendations about supplier attributes, the model may resolve each pairwise comparison by different heuristics; (3) attention bias: in pairwise prompts, different attributes may be attended to more depending on which pair is presented.

### 5.3 Human–LLM Comparison: Mechanisms and Limitations

[Populate after data; address the stochastic parroting confound explicitly:]

The H10 result must be interpreted with two confounds in mind. First, the *stochastic parroting* confound: LLMs may reproduce human survey response patterns from training data, not because they genuinely process the procurement options but because they have memorized how humans respond to similar vignettes. Our novel post-cutoff scenario texts partially mitigate this, but it cannot be ruled out. Second, the *instruction-following / bias resistance confound* (Critique 9): a model that ignores an anchor may be doing so because it is unbiased or because it is a capable instruction follower. The human arm does not resolve this confound; it provides a benchmark effect size regardless of mechanism.

### 5.4 Deployment Implications

[Populate after data; extend `pillar2-working-paper.md` §5.2 with flagship-specific findings:]

The addition of WARP, default bias, and loss aversion findings has direct implications for enterprise procurement system design:

- *WARP violations at T=0.0:* Deployed systems using deterministic decoding are not protected against preference intransitivity. Organizations that elicit multiple pairwise evaluations (e.g., bracket-style supplier tournaments) may obtain inconsistent outcomes depending on pairing order.

- *Default bias:* AI-assisted procurement systems that present a "current supplier" as a salient default option may artificially retain incumbents. Mitigations: randomize default position; require agent to score new entrant before incumbent.

- *Loss aversion:* Contract renewal contexts (keeping a known supplier vs. switching to a lower-cost alternative) are structurally framed as losses. LLM buyer agents may recommend against economically beneficial switches. Mitigations: strip gain/loss framing from contract renewal prompts; present all alternatives as positive options.

### 5.5 Limitations

[Inherit from `pillar2-working-paper.md` §5.3; add:]

- *Human arm scope:* Only five of eight bias types are included in the human arm (N≥25 per condition for UPGRADE-8/9/10 variants). Effect size comparisons for default, loss aversion, and WARP are against literature benchmarks only, not matched in-study human data.

- *WARP mechanism:* We detect WARP violations but cannot identify the causal mechanism (attention, context-sensitivity, or training memorization). The WARP result is descriptive.

- *RLHF alignment effect:* All tested models are RLHF-aligned. The alignment process may introduce systematic consistency pressures that artificially reduce BSI. Testing base (non-RLHF) models is a meaningful extension.

### 5.6 Future Work

[Extend `pillar2-working-paper.md` §5.4:]

1. **Anchoring magnitude proportionality (H4):** Implement `p2-01b` (ANCHOR_LOW) to test whether BSI scales with anchor magnitude, as prospect theory predicts.
2. **Multi-turn bias propagation:** Extend the decision module to multi-turn negotiation scenarios; test whether biases compound across conversation turns.
3. **Tool-use agents:** Evaluate buyer agents with actual retrieval and API-call capabilities to test whether tool access mitigates or amplifies bias susceptibility.
4. **WARP mechanism:** Ablation study varying attribute salience across pairwise prompts to identify which features drive intransitivity.
5. **Non-RLHF base models:** Compare base model BSI to aligned model BSI to isolate the alignment effect.

---

## 6. Conclusion

[Populate after data:]

This flagship study extends the pre-registered realistic design to eight bias types, two temperature conditions, two prompt versions, and a human comparison arm, providing the most comprehensive measurement of behavioral bias susceptibility in LLM-based procurement agents to date.

*If H1, H3, H5, H7, H8, H10 are all supported:* Frontier LLMs exhibit systematic behavioral bias susceptibility in structured procurement decision-making, with effect sizes `{{RESULT: h10_comparison_summary}}` human behavioral benchmarks. Chain-of-thought prompting selectively attenuates biases involving explicit numerical anchors but not structural option-set biases. WARP violations occur in `{{RESULT: warp_mean_rate}}` of cases, indicating preference intransitivity that persists under deterministic decoding. These findings have direct implications for the design and deployment of AI buyer agents in enterprise and consumer procurement workflows.

*If H1 not supported (robust rationality pivot):* LLM procurement agents show surprising robustness to eight canonical behavioral bias types, withstanding manipulations that reliably affect human decision-makers. This suggests that explicit multi-attribute scoring rubrics function as a commitment mechanism sufficient to override trained behavioral patterns — a practically significant finding for the design of AI buyer agent systems.

---

## References

[Extend `references.bib` from the realistic design paper. New entries needed:]

- `@samuelson1988status` — Samuelson & Zeckhauser (1988). Status quo bias in decision making. *JRBU*.
- `@johnson2003defaults` — Johnson & Goldstein (2003). Do defaults save lives? *Science*.
- `@samuelson1938note` — Samuelson (1938). A note on the pure theory of consumer's behaviour. *Economica*.
- `@kahneman1979prospect` — Kahneman & Tversky (1979). Prospect theory: An analysis of decision under risk. *Econometrica*.

---

## Appendices

### Appendix A — Pre-Registration Deviations (Flagship)

[Stub — complete post-experiment. Document any deviations from the flagship pre-registration addendum, including:]
- Any bias types removed due to scenario quality concerns
- Any model substitutions (model retired or unavailable at experiment time)
- Any N-per-cell reductions due to budget or API availability
- Any hard-difficulty scenario activations triggered by Gate 3 ceiling check

### Appendix B — Flagship Pre-Registration Document

[Complete before data collection — extend `docs/preregistration/prereg_osf.md` with:]
- H8 promoted to confirmatory (H1/H3/H5/H7/H8 = 5 confirmatory tests)
- H10 promoted to confirmatory
- Updated BH correction scope: 6 confirmatory tests (H1/H3/H5/H7/H8/H10)
- Updated N: 68,000 LLM runs + 100 human participants
- Updated model set: same 10 OpenRouter models; pin exact version IDs at start
- Human arm procedures: between-subjects, 5 bias types, N=50 per version, attention check exclusions

### Appendix C — Scenario YAML Metadata (Flagship Battery)

[Extend from realistic design appendix:]

| Scenario ID | Bias type | n_suppliers | δ (optimal − suboptimal utility) | Manipulation |
|---|---|---|---|---|
| p2-01-anchor-high | Anchoring | 4 | ~0.15 | Emergency procurement anchor at $91/unit |
| p2-02-framing | Framing | 3 | ~0.12 | Gain vs. loss framing of same outcome |
| p2-03-decoy | Decoy | 3 + decoy | ~0.18 | Asymmetrically dominated decoy (Supplier D) |
| p2-04-scarcity | Scarcity | 4 | ~0.10 | "Limited availability" urgency signal |
| p2-05-sunk-cost | Sunk Cost | 4 | ~0.14 | Prior $45k investment in incumbent |
| p2-06-default | Default bias | 4 | ~0.16 | Current supplier as salient default |
| p2-07-loss-aversion | Loss aversion | 4 | ~0.13 | Switching cost framing |
| p2-08-warp (AB) | WARP | 2 | varies | Supplier A vs. B pairwise |
| p2-08-warp (BC) | WARP | 2 | varies | Supplier B vs. C pairwise |
| p2-08-warp (AC) | WARP | 2 | varies | Supplier A vs. C pairwise |
| p2-09-compound | Compound | 6 | 0.031 | Anchor + scarcity simultaneous |
| p2-10-anchor-hard | Hard anchoring | 7 | 0.039 | Very high anchor ($148/unit) |
| p2-11-scarcity-hard | Hard scarcity | 8 | 0.005 | Scarcity on cheapest; minimal gap |

### Appendix D — Human Arm Vignettes

[Cross-reference `survey/scenario_previews.md` for full vignette text. Include attention check question text here for transparency.]

**ATTN1 (position 2 in survey):**
> *A supplier offers widgets at $12 per unit. Another supplier offers the same widgets at $89 per unit. To confirm you are reading carefully, please select the supplier with the lower price.*
> Options: [Supplier A ($12)] [Supplier B ($89)]

**ATTN2 (position 5 in survey):**
> *This question is a reading-comprehension check. Please select "Option B — Second choice" from the list below.*
> Options: [Option A — First choice] [Option B — Second choice] [Option C — Third choice]

### Appendix E — Registered Model Versions (Flagship)

[Stub — fill at experiment execution time. Exact version IDs for all 10 OpenRouter models as returned by the `/models` API at experiment start date.]

| Agent ID | Model family | Version string | Pinned at |
|---|---|---|---|
| openrouter-openai-gpt-4o | GPT-4o | [TBD] | [date] |
| openrouter-anthropic-claude-3.5-sonnet | Claude 3.5 Sonnet | [TBD] | [date] |
| openrouter-google-gemini-pro-1.5 | Gemini Pro 1.5 | [TBD] | [date] |
| openrouter-meta-llama-llama-3.1-405b-instruct | LLaMA 3.1 405B | [TBD] | [date] |
| openrouter-mistralai-mistral-large | Mistral Large | [TBD] | [date] |
| openrouter-deepseek-deepseek-chat | DeepSeek Chat | [TBD] | [date] |
| openrouter-qwen-qwen-2.5-72b-instruct | Qwen 2.5 72B | [TBD] | [date] |
| openrouter-cohere-command-r-plus | Cohere Command R+ | [TBD] | [date] |
| openrouter-mistralai-mixtral-8x22b-instruct | Mixtral 8x22B | [TBD] | [date] |
| openrouter-01-ai-yi-large | Yi Large | [TBD] | [date] |

### Appendix F — Robustness Checks (Flagship)

**F.1 Prompt Sensitivity (REV-5)**
[Same template as `pillar2-working-paper.md` Appendix D.1; run for all 8 bias types at N=5/cell before flagship launch]

| Phrasing | Anchoring CV | Framing CV | Decoy CV | Scarcity CV | Sunk Cost CV | Default CV | Loss Av. CV | Gate |
|---|---|---|---|---|---|---|---|---|
| robustness_a | `{{RESULT:...}}` | ... | ... | ... | ... | ... | ... | `{{RESULT:...}}` |
| robustness_b | `{{RESULT:...}}` | ... | ... | ... | ... | ... | ... | `{{RESULT:...}}` |
| robustness_c | `{{RESULT:...}}` | ... | ... | ... | ... | ... | ... | `{{RESULT:...}}` |
| **Overall gate** | — | — | — | — | — | — | — | **`{{RESULT: rev5_gate}}`** |

**F.2 Temperature Robustness (T=0.7 vs. T=0.0)**
[Inherit template from `pillar2-working-paper.md` Appendix D.2; extend to 8 bias types; see Table 5 in Section 4.11]

**F.3 CoT Prompt Variant Analysis (H8 full table)**
[See Table in Section 4.6; this appendix provides per-model CoT Δ BSI for all 8 bias types]

**F.4 Supplier Order Stability**
[Inherit from `pillar2-working-paper.md` Appendix D.4; same HMAC-SHA256 seeding mechanism applies; extend assertion to flagship N=100 seed range]

**F.5 Human Arm Robustness: Attention Check Exclusion Sensitivity**
[New in flagship:] Report H10 results with and without the attention check exclusion criterion to assess sensitivity of human BSI estimates to exclusion rate.

| Exclusion rule | N included | N excluded | H10 anchoring d | H10 decoy d | H10 framing d |
|---|---|---|---|---|---|
| No exclusions | 100 | 0 | `{{RESULT:...}}` | `{{RESULT:...}}` | `{{RESULT:...}}` |
| ATTN1 fails only | `{{RESULT:...}}` | `{{RESULT:...}}` | `{{RESULT:...}}` | `{{RESULT:...}}` | `{{RESULT:...}}` |
| ATTN1 or ATTN2 fails | `{{RESULT:...}}` | `{{RESULT:...}}` | `{{RESULT:...}}` | `{{RESULT:...}}` | `{{RESULT:...}}` |
