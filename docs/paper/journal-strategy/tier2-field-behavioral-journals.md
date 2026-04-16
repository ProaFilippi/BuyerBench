---
type: analysis
title: Tier 2 Journal Fit Analysis — JEBO, Experimental Economics, Journal of Behavioral Decision Making, Games and Economic Behavior
created: 2026-04-15
tags:
  - journal-strategy
  - submission-planning
  - behavioral-economics
  - pillar2
related:
  - '[[tier1-top-general-interest-journals]]'
  - '[[SUBMISSION-CHECKLIST]]'
  - '[[PAPER-STATUS]]'
  - '[[BuyerBench-P2-Gap-Analysis]]'
  - '[[PILLAR2-SUMMARY]]'
---

# Tier 2 Journal Fit Analysis — Top Field Journals in Behavioral and Experimental Economics

This document assesses the feasibility of submitting BuyerBench Pillar 2 results to the four leading field journals in behavioral economics and experimental methods: *Journal of Economic Behavior & Organization* (JEBO), *Experimental Economics*, *Journal of Behavioral Decision Making* (JBDM), and *Games and Economic Behavior* (GEB). These are the **realistic near-term submission targets** for the BuyerBench flagship paper, offering an achievable evidence threshold without sacrificing scientific rigor or citation impact.

> **Verdict summary:** A Tier 2 submission — specifically JEBO or Experimental Economics — is the correct primary target for the BuyerBench flagship paper. The evidence bar is achievable with one weekend of API-based data collection: N ≥ 30 runs per (bias type × model) cell across 5 bias types and 10 models. This tier values methodological contribution alongside empirical findings and does not require a human comparison arm for first publication, though one is strongly preferred.

---

## Overview: What Tier 2 Field Journals Require

Tier 2 behavioral and experimental journals share a common standard: well-identified empirical contributions with proper statistical power and credible methodology. Unlike Tier 1 general-interest journals, they do not require a theoretical mechanism that revises mainstream economic theory. A paper can contribute by:

1. **Extending a known phenomenon to a new population or domain** — showing that documented human biases generalize (or fail to generalize) to LLM agents in economically consequential settings
2. **Introducing a methodological contribution** — a new framework (BuyerBench) for bias measurement with reproducible protocol and public data
3. **Generating a novel empirical pattern** — cross-model heterogeneity in bias susceptibility that generates testable predictions

The core editorial question at JEBO/Experimental Economics is: "Is this result well-identified, well-powered, and interpretable in the context of the behavioral economics literature?" BuyerBench can answer yes — and sooner than Tier 1.

---

## Journal-by-Journal Analysis

### Journal of Economic Behavior & Organization (JEBO)

**Publisher:** Elsevier  
**Impact:** Impact Factor ~3.5; one of the oldest and broadest behavioral economics journals; indexed in all major databases  
**Scope:** Behavioral, institutional, and experimental economics; explicitly accepts papers on non-human decision agents and computational simulation alongside traditional lab experiments

**Fit rationale for BuyerBench:**

JEBO is unusually hospitable to non-standard agents and interdisciplinary methodology. The journal has published work on robot traders, simulated agents in experimental markets, and AI decision systems — making it the most natural home for a first LLM bias battery in the economics literature. JEBO's editorial scope explicitly includes "economic behavior of organizations and institutions," which encompasses AI procurement systems as organizational decision-making agents.

The optimal BuyerBench angle for JEBO: **a systematic bias battery with controlled-variant design, multi-model comparison, and variance decomposition.** JEBO does not require a human comparison arm for publication, though the discussion should position LLM BSI estimates relative to documented human effect sizes from the literature meta-analysis. The paper can be framed as a methodological contribution (introducing BuyerBench as a reproducible evaluation protocol) combined with substantive empirical findings (cross-model heterogeneity in bias susceptibility across 5 bias categories).

JEBO also frequently publishes papers that use novel data sources to test established behavioral economics predictions — exactly the BuyerBench design structure. The controlled-variant approach (identical economics, presentation manipulation) maps cleanly onto JEBO's standard experimental methodology.

**Required evidence level for JEBO submission:**
- N ≥ 30 runs per (bias type × model) cell — minimum viable; N = 50 preferred for 80% power at d = 0.5
- At least 5 bias types with controlled-variant pairs (baseline vs. manipulated condition)
- At least 8–10 models spanning capability tiers (not just flagship models)
- Mixed-effects regression with model as random effect; bias type and capability tier as fixed effects
- Multiple comparison correction (Bonferroni or FDR-adjusted p-values across bias × model cells)
- Variance decomposition: partition observed BSI variance into model-level, bias-type-level, and residual components
- Publicly released benchmark code and data (JEBO increasingly expects reproducibility)
- Discussion of stochastic sampling as a confound: explicitly model temperature-driven variance

**What would push JEBO to reject:**
- "Only descriptive statistics" — means, percentages, and bar charts without regression analysis will not pass review at JEBO
- "No power justification" — reviewers will ask how you determined N; must cite power analysis pre-hoc or at minimum post-hoc
- "One-shot runs treated as evidence" — running each model once and reporting the result will be dismissed immediately; repeated runs are necessary
- "No correction for multiple comparisons" — testing 5 bias types × 10 models = 50 cells; uncorrected p-values will fail review
- "No behavioral economics framing" — the paper must position itself in the behavioral economics literature, not just the NLP/AI literature; JEBO reviewers are economists, not AI researchers
- "Framework paper without empirical substance" — describing BuyerBench as a tool without reporting substantial empirical findings from it will be rejected as a methodology note

**Realistic assessment:** JEBO is the most achievable Tier 2 target. The BuyerBench design is already structurally sound for a JEBO submission; the primary gap is statistical power. N ≥ 30 runs per cell across 5 bias types × 10 models = 1,500 total agent runs. At $0.15/run via OpenRouter, this is $225 in API costs — feasible in one weekend. The key investment is the econometric analysis (mixed-effects models, variance decomposition) and the literature positioning. Realistic timeline: **6–12 months from now**.

---

### Experimental Economics

**Publisher:** Springer (Economic Science Association)  
**Impact:** Impact Factor ~2.8; the leading journal specifically dedicated to experimental methodology in economics  
**Scope:** Laboratory and field experiments; computational experiments; experimental methodology; agent-based models that connect to experimental predictions

**Fit rationale for BuyerBench:**

Experimental Economics is the methodological flagship of the Economic Science Association and places the highest value on **experimental design rigor** among all behavioral journals. What distinguishes publishable work here is not just the finding but the design architecture: control, identification, power, and protocol transparency. BuyerBench's controlled-variant design — where the economic structure is held constant and only the presentation varies — is exactly the experimental design logic that Experimental Economics rewards.

The BuyerBench angle that best fits Experimental Economics: **the methodological contribution of treating LLM temperature as an experimental treatment.** Unlike human subjects, LLMs allow the researcher to parametrically control response stochasticity. This is an unprecedented experimental capability: you can run the same agent at temperature 0.0 (near-deterministic) and temperature 1.0 (high variance) and observe how bias susceptibility changes. No human subjects experiment can hold cognitive noise constant in this way. This design novelty is an Experimental Economics contribution in its own right.

A secondary angle: **replication of canonical behavioral economics experiments in a new population.** Experimental Economics has published replication studies extensively, particularly in the wake of the replication crisis. A paper that replicates Tversky & Kahneman (1974) anchoring and Tversky & Kahneman (1981) framing in LLM agents using the original design structure, with proper power, is a legitimate replication contribution.

**Required evidence level for Experimental Economics submission:**
- All JEBO requirements, plus:
- Explicit protocol documentation: the paper must include a complete methods section that allows full replication; scripts, prompts, and data must be published
- Pre-registered hypotheses (or acknowledgment that study is exploratory with appropriate hedging): Experimental Economics increasingly requires pre-registration for confirmatory claims
- Temperature ablation analysis: at minimum 3 temperature settings (0.0, 0.5, 1.0) to characterize stochasticity-bias interaction
- Effect size reporting: Cohen's d or partial η² for all bias comparisons, with confidence intervals
- Incentive compatibility discussion: explicit acknowledgment that LLMs cannot receive monetary incentives and discussion of what this means for interpreting "choices"
- Where possible: structural equivalence to classic human experiments (same stimulus materials or clearly isomorphic variants)

**What would push Experimental Economics to reject:**
- "Protocol not replicable" — the entire BuyerBench protocol must be documented precisely enough that an independent lab can reproduce it
- "No incentive compatibility" — while the journal accepts hypothetical-choice designs, the paper must explicitly address whether LLM "choices" are comparable to incentivized human choices; a compelling argument must be made
- "Confounded design" — any scenario where the baseline and variant differ on more than the targeted manipulation will be caught; the controlled-variant design must be airtight
- "No pre-registration or exploration acknowledgment" — confirmatory claims (H1, H2…) without pre-registration will receive extra scrutiny; frame as exploratory or register
- "Insufficient model heterogeneity" — a single-model paper will be rejected as insufficient generalization; the cross-model comparison is essential

**Realistic assessment:** Experimental Economics is marginally harder than JEBO due to the methodology standards, but the BuyerBench design is fundamentally aligned with what the journal values. The key additions beyond JEBO are: (1) protocol documentation sufficient for full replication, (2) temperature ablation, (3) pre-registration or explicit exploratory framing. Timeline: **9–15 months**, with pre-registration at AsPredicted/OSF before data collection.

---

### Journal of Behavioral Decision Making (JBDM)

**Publisher:** Wiley  
**Impact:** Impact Factor ~2.5; interdisciplinary behavioral decision research; accepts psychology, economics, and management science contributions  
**Scope:** Judgment and decision making; heuristics and biases; risk perception; individual and group decision processes; computational modeling of decision behavior

**Fit rationale for BuyerBench:**

JBDM occupies a broader interdisciplinary space than the economics-specific journals above. It publishes work from psychology, behavioral economics, operations research, and management science — and explicitly accepts computational and simulation approaches alongside traditional lab experiments. Kahneman, Tversky, and colleagues published foundational work here; more recently, it has published computational modeling papers that simulate decision behavior using formal models.

The BuyerBench angle for JBDM: **LLMs as a new class of decision-making agents that can be administered classic judgment-and-decision-making tasks.** JBDM is less demanding about economic theory contribution and more receptive to "here is a new phenomenon documented rigorously." The bias battery framing — 5 canonical bias tasks administered to 10 models, with controlled manipulations, repeated measures, and effect-size comparison to human benchmarks — is a complete JBDM paper. The journal frequently publishes N = 3–5 conditions with N = 80–200 participants; BuyerBench's N = 30 runs per (bias × model) cell is competitive.

JBDM also publishes reviews and meta-analyses. A secondary publication strategy: **a review article mapping the emerging literature on LLM decision biases** (Binz & Schulz, Hagendorff, Aher, Echterhoff, plus BuyerBench) would be a natural JBDM contribution once the empirical paper is published.

**Required evidence level for JBDM submission:**
- N ≥ 20 runs per cell minimum (JBDM has lower power standards than economics journals; N = 30 is comfortable)
- Effect size comparison to human benchmarks from the literature — this is JBDM's key value-add interest
- At minimum 3 bias types (anchoring, framing, and one additional)
- Discussion of cognitive process — not just BSI numbers, but interpretation through the lens of dual-process theory (System 1/System 2), heuristics, or prospect theory
- Comparison to at least one prior study of LLM decision behavior (Binz & Schulz, Hagendorff, or Echterhoff)
- Discussion of ecological validity: are these procurement decisions representative of real LLM deployment contexts?

**What would push JBDM to reject:**
- "No connection to decision science theory" — JBDM reviewers are psychologists and behavioral scientists; the paper must engage with JDM theory (dual process, prospect theory, construal level) not just report metrics
- "Pure AI/NLP paper" — if the paper reads like a benchmark paper (as would be appropriate for NeurIPS), JBDM will reject it as out of scope; it must read as a decision science paper that happens to use LLMs
- "No human benchmarks" — JBDM readers want to know how LLM performance compares to humans; at minimum, cite human effect sizes from meta-analyses
- "No discussion of mechanisms" — "why" LLMs show these biases matters to JBDM readers even if a formal model is not required; gesture toward training data, RLHF dynamics, or architectural constraints

**Realistic assessment:** JBDM is the most accessible of the four Tier 2 journals for BuyerBench — lower power requirements, interdisciplinary scope, receptive to LLM behavioral research. The risk is positioning: the paper can be too NLP-focused for JBDM or too JDM-focused for NLP venues. A JBDM submission requires a careful reframe of the introduction and discussion to foreground decision science contributions. Timeline: **3–6 months** for a well-positioned working paper version. JBDM is the fastest credible publication path if speed matters.

---

### Games and Economic Behavior (GEB)

**Publisher:** Elsevier  
**Impact:** Impact Factor ~2.0; leading journal in game theory and strategic interaction  
**Scope:** Game theory; mechanism design; laboratory experiments on strategic behavior; bounded rationality in strategic settings; auction theory and experiments

**Fit rationale for BuyerBench:**

GEB is specialized toward strategic interaction and game theory — not the natural home for a unilateral bias battery. However, BuyerBench has a GEB-relevant angle: **LLM behavior in procurement negotiation and supplier selection as a strategic game.** Supplier selection is not a one-shot decision in isolation; it occurs in a market where suppliers observe buyer behavior and adjust strategies accordingly. If LLM buyers are predictably anchored or susceptible to framing, rational suppliers will exploit this — and GEB cares about the strategic implications of bounded rationality.

The specific GEB angle: **testing whether LLM agents satisfy game-theoretic rationality axioms.** This maps to BuyerBench Design Option 4 (WARP battery) and Design Option 2 (economic games). If LLMs violate WARP in multi-supplier choice contexts, this is a GEB paper — it demonstrates that LLM choice behavior cannot be represented by a utility function, with implications for mechanism design and market theory.

A viable GEB submission would focus narrowly on the rationality axiom violations: WARP tests across 10+ models, with repeated runs, and interpretation through the lens of revealed preference theory. This is a methodologically clean contribution that GEB values: testing a fundamental axiom (WARP/GARP) in a new population (LLM agents), with clean identification.

**Required evidence level for GEB submission:**
- WARP/GARP violation tests: at minimum 3-alternative choice sets with all pairwise comparisons administered between-run
- N ≥ 50 runs per (model × choice set) to characterize stochastic choice probabilities
- Formal test of WARP violation: not just descriptive, but a statistical test comparing observed choice frequencies against WARP-consistent distributions
- At least 8 models; ideally spanning capability tiers to test whether game-theoretic rationality scales with capability
- Connection to existing GEB literature on bounded rationality and stochastic choice (Luce (1959), Tversky (1972), Gul & Pesendorfer (2006))
- Discussion of implications for mechanism design: if LLMs violate WARP, standard auction/procurement mechanisms are not incentive-compatible for AI buyers

**What would push GEB to reject:**
- "No game-theoretic content" — a pure bias battery without strategic interaction framing is out of scope for GEB
- "No formal rationality test" — descriptive reporting of choice patterns without formal axiom tests will not satisfy GEB reviewers
- "No connection to existing theory" — GEB reviewers are game theorists; the paper must engage with the theory literature (revealed preference, stochastic choice, bounded rationality models)
- "Small N on rationality tests" — GEB is as quantitatively demanding as Experimental Economics; stochastic choice tests require high N to distinguish true WARP violations from sampling noise

**Realistic assessment:** GEB is a lower priority and narrower fit than JEBO, Experimental Economics, or JBDM for the flagship BuyerBench paper. It is the right target for a specific follow-on paper focused on WARP violations and mechanism design implications. The BuyerBench Design Option 4 (WARP battery) is the GEB paper, not the full bias battery. Timeline: **18–24 months**, as it requires implementing and running the WARP battery as a distinct study.

---

## Minimum Evidence Requirements — Tier 2 Submission Bar

| Requirement | Current State | JEBO / Exp. Econ. | JBDM | GEB |
|---|---|---|---|---|
| Runs per (bias × model) cell | ~1–3 runs | N ≥ 30 (N = 50 preferred) | N ≥ 20 | N ≥ 50 (WARP-focused) |
| Model coverage | 8–10 models | 8–10 minimum | 5+ minimum | 8–10 minimum |
| Bias types | 5 types | 5 types | 3+ types | WARP battery (separate design) |
| Mixed-effects regression | Not yet run | Required | Preferred | Required |
| Multiple comparison correction | Not applied | Required (Bonferroni/FDR) | Preferred | Required |
| Effect size vs. human benchmarks | Not computed | Preferred (strong) | Required | Not required |
| Temperature/stochasticity model | Basic | Required | Preferred | Required |
| Human comparison arm | None | Preferred; not required | Preferred; not required | Not required |
| Protocol public + reproducible | Code public (partial) | Required | Preferred | Required |
| Pre-registration | None | Strongly preferred | Preferred | Strongly preferred |
| Incentive compatibility discussion | None | Required | Required | Required |

---

## Common Rejection Triggers Across All Four Tier 2 Journals

1. **"Only descriptive statistics"** — all four journals expect regression analysis. Means and bar charts are introduction material, not results.

2. **"One-shot runs treated as evidence"** — the most acute risk for BuyerBench. Running each model once and reporting the output is methodologically unsound for any of these journals. Repeated runs (N ≥ 30) are the minimum viable evidence.

3. **"No power justification"** — reviewers will ask how you determined your sample size. Must cite a power analysis (or a sensitivity analysis showing detectable effect size at observed N).

4. **"No correction for multiple comparisons"** — testing 5 bias types × 10 models = 50 hypothesis tests. Uncorrected p-values will fail review at JEBO and Experimental Economics.

5. **"Wrong journal framing"** — BuyerBench must be framed as a behavioral economics contribution (for JEBO/Exp. Econ./GEB) or a judgment-and-decision-making contribution (for JBDM), not as an AI benchmark paper. The introduction must foreground the behavioral economics research question, not the AI evaluation framework.

6. **"LLM choices not comparable to human choices"** — all four journals will raise the incentive incompatibility issue. The paper must address this explicitly: LLMs cannot receive monetary payoffs; their "choices" are generated responses, not incentivized decisions. A defensible framing: LLM outputs simulate the decision recommendation that an AI procurement system would execute; the economically relevant question is whether those recommendations are systematically biased, regardless of internal motivation.

---

## Strategic Recommendation for Tier 2

**JEBO is the primary submission target for the BuyerBench flagship paper.** It is the broadest in scope, most receptive to methodological contributions alongside empirical findings, and the most cited of the four for behavioral economics work. A well-powered JEBO submission (N = 50 per cell, 5 bias types, 10 models, mixed-effects regression, FDR correction) establishes BuyerBench as a credible research program in the behavioral economics literature.

**Experimental Economics is the backup submission** if JEBO rejects on scope or if the protocol documentation is particularly strong. The key additional investment for Experimental Economics is temperature ablation and pre-registration.

**JBDM is the fast-path option** if speed of publication matters more than economics citation impact. It has the lowest evidence bar and the most interdisciplinary receptivity. Useful as a second publication (e.g., the JBDM paper focuses on effect-size comparison to human benchmarks; the JEBO paper focuses on methodology and multi-model comparison).

**GEB is a follow-on target**, not a primary target. The WARP battery study should be designed, run, and submitted separately once the flagship bias battery paper is accepted.

### Decision Gate

```
If N ≥ 50 per cell AND ≥ 6 bias types AND ≥ 8 models AND mixed-effects model implemented:
    → Target JEBO (primary) or Experimental Economics (secondary)

If N = 30–49 per cell AND ≥ 5 bias types AND ≥ 8 models:
    → Target JEBO with "exploratory" framing or JBDM

If N < 30 per cell OR < 5 bias types:
    → Target JBDM (working paper tier) — do not submit to JEBO/Exp. Econ.
    → Treat as pilot; expand before flagship submission

If WARP battery completed at N ≥ 50 per model:
    → Target GEB (separate paper)
```

### Minimum Viable Paper for JEBO

**5 bias types × 10 models × 30 runs = 1,500 total observations**

- API cost: ~$225 via OpenRouter ($0.15/run)
- Execution time: one weekend of data collection
- Analysis time: ~2 weeks for mixed-effects models, variance decomposition, power analysis
- Writing time: 4–6 weeks for journal-quality manuscript

This is the achievable minimum. The addition of a human comparison arm (N = 100 MTurk subjects × 10 scenarios = $500) would substantially strengthen the submission and potentially push it from a JEBO desk reject risk to a likely acceptance with revisions.

---

## Cross-References

- Tier 1 analysis (AER, QJE, JPE, Econometrica): [[tier1-top-general-interest-journals]]
- Tier 3–5 analysis (JAIR, AI & Society, Decision Support Systems): [[tier3-adjacent-journals.md]]
- Current paper submission target: [[SUBMISSION-CHECKLIST]]
- Statistical power and N justification: [[PILLAR2-RESEARCH-01]] Section B.5
- Empirical design options and cost estimates: [[PILLAR2-RESEARCH-02]] Section E
- BSI formal definition: [[economic-rationality-metrics]]
- Human comparison arm planning: [[PILLAR2-RESEARCH-02]] Section E.5
- Research gap claims: [[RESEARCH-GAPS]]
