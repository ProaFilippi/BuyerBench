---
type: analysis
title: Tier 4 — Primary Submission Strategy for BuyerBench Pillar 2
created: 2026-04-15
tags:
  - journal-strategy
  - submission-planning
  - behavioral-economics
  - pillar2
related:
  - '[[tier1-top-general-interest-journals]]'
  - '[[tier2-field-behavioral-journals]]'
  - '[[tier3-adjacent-journals]]'
  - '[[tier5-fallback-journals]]'
  - '[[SUBMISSION-CHECKLIST]]'
  - '[[PAPER-STATUS]]'
  - '[[BuyerBench-P2-Gap-Analysis]]'
---

# Tier 4 — Realistic Primary Submission Strategy

This document translates the journal fit analyses (Tiers 1–3) into a concrete, actionable submission plan for the BuyerBench Pillar 2 flagship paper. "Tier 4" is not a prestige designation — it is the **practical first-submission target** given current evidence capacity, timelines, and the BuyerBench evidence roadmap. The recommended primary target is **JEBO (Journal of Economic Behavior & Organization)**, with *Experimental Economics* as the first backup.

> **One-sentence strategy:** Submit the BuyerBench bias battery paper to JEBO first. If rejected on scope, reframe and submit to Experimental Economics. If rejected for power or methodology, address the specific gap and resubmit to JEBO or fall through to Tier 5 (Journal of Economic Psychology, JDM, PLOS ONE).

---

## Why JEBO as the Primary Target

JEBO is the most achievable high-impact submission for BuyerBench Pillar 2, for four concrete reasons:

1. **Broadest scope in Tier 2.** JEBO explicitly accepts computational agent studies, simulated markets, and non-human decision actors. No other top behavioral economics journal has this scope breadth. The editorial risk of a desk reject on scope grounds is lower at JEBO than at Experimental Economics, JBDM, or GEB.

2. **Methodological contribution counts.** JEBO regularly publishes papers where the primary contribution is a new measurement framework alongside empirical findings. BuyerBench's controlled-variant design and BSI metric formalization are legitimate JEBO contributions — not just the empirical results.

3. **Impact factor is the highest viable target.** JEBO's ~3.5 impact factor is achievable, contrasted with Tier 1 venues (~10–15) which require a theoretical mechanism far beyond current BuyerBench evidence. This is the correct "ambitious but realistic" positioning.

4. **Evidence bar is completable in one intensive data collection sprint.** N ≥ 30 runs per (bias type × model) cell × 5 bias types × 10 models = 1,500 runs at ~$225 via OpenRouter. No lab, no IRB, no human subjects. This timeline is one weekend of data collection, two weeks of analysis.

---

## Submission Decision Gate

Use this decision tree before submitting:

```
STEP 1: Check empirical power
  → N ≥ 50 runs per (bias × model) cell?
      YES → Proceed to STEP 2 (preferred N)
      NO  → N ≥ 30?
                YES → Proceed to STEP 2 with "exploratory" framing caveat
                NO  → STOP. Do not submit to JEBO. Add runs or target JBDM/Tier 5.

STEP 2: Check model and bias coverage
  → ≥ 8 models covering ≥ 2 capability tiers?
      YES → Proceed to STEP 3
      NO  → STOP. Add models or target JBDM.
  → ≥ 5 bias types with controlled-variant pairs?
      YES → Proceed to STEP 3
      NO  → STOP. Implement missing scenarios or target JBDM.

STEP 3: Check analysis completeness
  → Mixed-effects regression implemented?         YES / NO
  → Multiple comparison correction applied?       YES / NO
  → Variance decomposition (model vs. bias type)? YES / NO
  → Stochasticity/temperature analysis present?   YES / NO
  → BSI metric formally defined with equations?   YES / NO
  → Benchmark code publicly released?             YES / NO

  → All YES → Submit to JEBO (primary)
  → 4–5 YES → Submit to JEBO with planned revision note OR target Experimental Economics
  → < 4 YES → Target JBDM or Tier 5; do not submit to JEBO

STEP 4: JEBO vs. Experimental Economics routing
  → Is the temperature ablation study complete?
      YES + pre-registration exists → Route to Experimental Economics (secondary)
      NO or exploratory → Route to JEBO (primary)
```

---

## Preparation Checklist Before Submission

### Data Collection
- [ ] N ≥ 30 (target 50) runs per (bias type × model) cell
- [ ] ≥ 5 bias types: anchoring (p2-01), framing (p2-02), decoy/IIA (p2-03), scarcity (p2-04), sunk cost (p2-05)
- [ ] ≥ 8 models, spanning at least 2 capability tiers (e.g., 4o-mini class vs. GPT-4o class vs. Claude Opus class)
- [ ] Temperature settings documented; at least 1 ablation (temperature 0 vs. default) run

### Statistical Analysis
- [ ] Mixed-effects regression: BSI ~ bias_type + capability_tier + (1|model) + (1|run)
- [ ] FDR correction (Benjamini-Hochberg) across all 50 hypothesis tests (5 bias × 10 models)
- [ ] Variance decomposition: proportion of BSI variance explained by model vs. bias type vs. residual
- [ ] Cohen's d effect sizes with 95% CIs for each bias × model cell
- [ ] Post-hoc power analysis: report minimum detectable effect at observed N

### Economic Framing
- [ ] BSI metric formally defined: BSI = (agent_choice_value - optimal_value) / (worst_possible_value - optimal_value)
- [ ] Ground-truth optimal computed for each scenario and documented in data release
- [ ] Discussion of economic magnitude: what does BSI = 0.3 mean in dollar terms for a representative procurement decision?
- [ ] Literature comparison: cite human BSI benchmarks from Tversky & Kahneman (1974, 1981), Arkes & Blumer (1985) for calibration

### Methodology and Replication
- [ ] Full prompt templates included in supplementary materials or appendix
- [ ] API version, temperature, model IDs, and random seeds documented for all runs
- [ ] Code and data released on GitHub with DOI (Zenodo or OSF) before submission
- [ ] Incentive compatibility section: explicitly address that LLMs cannot receive monetary payoffs and frame their responses as simulated procurement recommendations

### Positioning
- [ ] Introduction foregrounds the *behavioral economics research question*, not the AI evaluation framework
- [ ] Literature review covers: (1) canonical human bias studies, (2) LLM behavioral studies (Binz & Schulz, Hagendorff, Echterhoff), (3) experimental methods literature (repeated measurement, stochastic agents)
- [ ] Discussion positions BuyerBench contribution against Echterhoff et al. (2024) specifically (most relevant prior work)
- [ ] JEBO-specific framing: situate LLMs as "non-human economic agents" within JEBO's tradition of studying simulated and artificial agents

---

## Submission Timeline

| Milestone | Target Date | Notes |
|---|---|---|
| Data collection sprint (1,500 runs) | T + 0 weeks | One weekend; ~$225 API cost |
| Econometric analysis complete | T + 2–3 weeks | Mixed-effects, variance decomp, power |
| First complete draft | T + 5–7 weeks | Full manuscript with all required sections |
| Internal review + revision | T + 8–10 weeks | Revise for JEBO framing and reviewer anticipation |
| Code/data released to public repo | T + 10 weeks | Before submission; JEBO increasingly checks this |
| JEBO submission | T + 10–12 weeks | ~3 months post data collection |
| Expected first decision | T + 22–30 weeks | JEBO typical turnaround: 3–4 months |
| Revision turnaround (if R&R) | T + 34–40 weeks | 6–8 weeks for revisions |
| Final decision | T + 46–54 weeks | 10–12 months from submission |

Total realistic timeline from data collection to JEBO acceptance: **12–15 months**.

---

## Rejection Cascade Strategy

If JEBO desk-rejects or rejects after review, the path forward depends on the stated reason:

### Rejection Reason → Response

**"Interesting but not an economic insight; pure measurement"**
- This is the core Tier 1 rejection, inappropriately applied. Revise the introduction to foreground cross-model heterogeneity as an empirical regularity with implications for behavioral economics theory (e.g., "bias susceptibility is not a property of model capability alone — bias category predicts susceptibility better than benchmark score, which is a substantive finding about the structure of bounded rationality in AI agents").
- Re-submit to JEBO with revised framing, or move to Experimental Economics.

**"Insufficient power; N too small"**
- Do not submit to Experimental Economics with the same N. Run additional data collection.
- Alternatively, re-frame as exploratory pilot and target JBDM (Tier 2) or DSS (Tier 3) where power requirements are lower.

**"No human comparison arm; cannot assess whether these biases are meaningful"**
- Run an MTurk human comparison study: N = 100 subjects × 5 scenarios = $500–$700 at $0.10/response.
- This converts a JEBO rejection into a substantially stronger resubmission or an Experimental Economics original submission.
- Timeline: 2–3 additional weeks for MTurk data collection; 2 weeks for comparative analysis.

**"Stochastic outputs not properly modeled; results may be noise"**
- Add a temperature ablation study (temperature 0 vs. 0.5 vs. 1.0) to show that bias susceptibility persists across temperature settings.
- Formally model within-model variance and show that BSI estimates are robust to sampling noise at the observed N.
- This is also required for Experimental Economics, so address this proactively.

**"Wrong journal; out of scope for behavioral economics"**
- This is unlikely for JEBO given its breadth, but if it occurs, route to DSS (Tier 3) or JBDM (Tier 2) with adjusted framing.
- Do not re-submit to JEBO without a scope consultation with the editor.

**"Framework not publicly available"**
- Release the BuyerBench code and data immediately. Resubmit within 4 weeks.
- This rejection is fully within our control to address.

### Full Cascade Order

```
1. JEBO (primary)
     ↓ reject: revise per above reasons
2. Experimental Economics (if design is pre-registered and temperature-ablated)
     ↓ reject: revise framing
3. JBDM (if power is borderline; reframe as JDM contribution)
     ↓ reject or scope mismatch
4. DSS (if procurement/IS framing is strengthened)
     ↓ reject
5. Tier 5: Journal of Economic Psychology, JDM, or PLOS ONE
     (see [[tier5-fallback-journals]])
```

---

## What to Do If Rejected From Everything Through Tier 4

This outcome is unlikely if the preparation checklist is complete, but it signals one of three problems:

1. **Power is genuinely insufficient.** Solution: run more data. There is no shortcut — N ≥ 30 is the minimum acceptable and reviewers across all these journals enforce it.

2. **The finding is null.** If no model shows statistically significant bias susceptibility above chance, the paper's contribution changes: it becomes a null result about LLM rationality. This is publishable at PLOS ONE and potentially valuable as a counterpoint to prior work claiming LLMs are biased. Reframe accordingly.

3. **The framing is not connecting.** Seek a co-author from behavioral economics or experimental economics to advise on positioning. A collaborator with JEBO/Experimental Economics publication history substantially increases acceptance probability.

---

## Cross-References

- Journal fit analysis by prestige tier:
  - [[tier1-top-general-interest-journals]] — AER, QJE, JPE, Econometrica
  - [[tier2-field-behavioral-journals]] — JEBO, Experimental Economics, JBDM, GEB
  - [[tier3-adjacent-journals]] — JAIR, AI & Society, DSS, Management Science IS
  - [[tier5-fallback-journals]] — Journal of Economic Psychology, JDM, PLOS ONE
- Empirical data collection plan: [[PILLAR2-RESEARCH-02]] Section E
- BSI metric formal definition: [[economic-rationality-metrics]]
- Statistical analysis plan: [[PILLAR2-RESEARCH-03]]
- Human comparison arm design: [[PILLAR2-RESEARCH-02]] Section E.5
- Research gap claims: [[RESEARCH-GAPS]]
- Submission checklist (live tracking): [[SUBMISSION-CHECKLIST]]
