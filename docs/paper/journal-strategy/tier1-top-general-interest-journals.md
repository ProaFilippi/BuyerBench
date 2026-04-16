---
type: analysis
title: Tier 1 Journal Fit Analysis — AER, QJE, JPE, Econometrica
created: 2026-04-15
tags:
  - journal-strategy
  - submission-planning
  - behavioral-economics
  - pillar2
related:
  - '[[SUBMISSION-CHECKLIST]]'
  - '[[PAPER-STATUS]]'
  - '[[BuyerBench-P2-Gap-Analysis]]'
  - '[[PILLAR2-SUMMARY]]'
---

# Tier 1 Journal Fit Analysis — Top General-Interest Economics Journals

This document assesses the feasibility of submitting BuyerBench Pillar 2 results to the four premier general-interest economics journals: *American Economic Review* (AER), *Quarterly Journal of Economics* (QJE), *Journal of Political Economy* (JPE), and *Econometrica*. It documents fit rationale, required evidence level, realistic barriers, and what a publication-ready submission would need to contain.

> **Verdict summary:** Tier 1 submission is a *realistic long-term target*, not a near-term strategy. The core scientific question — whether LLM behavioral biases follow, deviate from, or mechanistically explain human cognitive biases — is sufficiently novel and economically important to belong in these journals. The gap is evidentiary, not conceptual. The path is defined.

---

## Overview: What Tier 1 General-Interest Journals Require

All four journals share a common standard: a behavioral or empirical paper must contribute a **novel economic insight**, not merely novel measurement. Demonstrating that LLMs show anchoring bias is interesting; *explaining why* in a way that revises or extends prospect theory, the dual-process framework, or cognitive economics theory is publishable here.

The core editorial question at AER/QJE/JPE/Econometrica is not "is this result interesting?" but "does this result teach economists something they did not know about the structure of decision-making?" BuyerBench can answer yes — but only with the right evidence architecture.

---

## Journal-by-Journal Analysis

### American Economic Review (AER)

**Publisher:** American Economic Association  
**Impact:** Impact Factor ~9; most-cited general economics journal  
**Scope:** All fields of economics; accepts experimental, behavioral, and applied work alongside theory

**Fit rationale for BuyerBench:**

AER publishes behavioral economics experiments when they contain a theoretical contribution. Thaler & Sunstein's nudge research, Kahneman's dual-process work applied to policy, and experimental results on market anomalies all found homes here because they *revised* mainstream economic models of behavior. BuyerBench would need to fit the same mold: not "LLMs show anchoring" but "LLMs show anchoring at effect sizes that are [larger than / structurally different from / absent for] humans in the same procurement domain, and this pattern is explained by [mechanism X]."

A viable AER angle: **LLMs as a controlled behavioral agent.** Unlike human subjects, LLM temperature settings allow direct manipulation of response stochasticity. This creates an unprecedented experimental opportunity — an agent whose cognitive noise can be parametrically varied while holding all other features constant. This methodological novelty, combined with a structural model of how stochasticity interacts with bias susceptibility, could constitute an AER-worthy theoretical contribution.

**Required evidence level for AER submission:**
- N > 500 agent-runs per (bias type × model) cell — minimum; N > 1,000 preferred
- Human comparison arm: ideally a matched MTurk experiment using identical procurement vignettes with human respondents (not a student lab sample)
- Causal identification: the paper must argue *why* biases emerge, not merely *that* they emerge. Possible mechanisms: training data composition, RLHF reward structure, token prediction dynamics, emergent satisficing from transformer architecture
- Theory-grounded structural model: a formal model (utility-theoretic or cognitive) that generates testable predictions about which bias types should be stronger/weaker across model capability levels
- Replication: results should replicate across at least two independent replication runs and across multiple model families

**What would push AER to reject:**
- "Interesting measurement but no economic insight" — the most common rejection reason for benchmark papers
- "Results don't generalize beyond these specific prompts" — prompt sensitivity is the Achilles heel; AER reviewers will ask why these particular procurement prompts aren't cherry-picked
- "No theory" — descriptive statistics without a formal model will not survive AER review
- "Stochastic outputs treated as deterministic" — treating each model run as a stable observation without modeling temperature-driven variance
- Insufficient external validity — AER reviewers will ask whether procurement AI systems in deployment show the same biases, requiring some ecological validation

**Realistic assessment:** AER is a 5–10 year horizon target assuming BuyerBench generates significant follow-on work. The first step is establishing the benchmark (NeurIPS/arXiv), then running the human comparison arm, then building the structural theory. The paper that belongs in AER is probably the third or fourth paper in the BuyerBench research program, not the first.

---

### Quarterly Journal of Economics (QJE)

**Publisher:** Harvard University (Oxford University Press)  
**Impact:** Highest impact factor in economics (~12); known for elegant, clean papers with large insights  
**Scope:** General economics; particularly strong in behavioral, labor, public, and development economics

**Fit rationale for BuyerBench:**

QJE has a history of publishing "surprising" results — findings that invert conventional wisdom or reveal hidden mechanisms in economic behavior. Examples: Chetty et al. on salience and tax perception; Mas & Moretti on peer effects in productivity. The BuyerBench result that would attract QJE attention: **more capable models are not less biased — or conversely, that capability and rationality are orthogonal properties.** If we find that GPT-4 level models exhibit stronger anchoring than GPT-3.5 level models in procurement contexts (because higher capability enables more sophisticated rationalization of biased choices), that is a QJE-worthy surprise.

Another viable QJE angle: **the procurement market implications of biased AI buyers.** If AI buyer agents are systematically susceptible to anchoring and framing, what does this mean for market equilibrium, price discovery, and supplier manipulation strategies? This bridges to industrial organization and market design, which QJE covers well.

**Required evidence level for QJE submission:**
- Everything required for AER, plus:
- Cross-model variation that maps to economic theory (e.g., capability tier predicts bias pattern, not just bias level)
- Market-level implications: ideally a model of a two-sided market where buyers are AI agents with documented bias profiles
- Field validation: any evidence (even a small study) that real deployed AI procurement systems exhibit analogous biases

**What would push QJE to reject:**
- "Pure benchmarking paper" — QJE wants the economic implications, not the methodology
- Limited model heterogeneity — if all models show similar biases, the variation needed for identification is absent
- No credible counterfactual for "what would a rational agent do" — the BSI metric must be clean and defended
- Overclaiming — QJE referees are particularly harsh on papers that oversell weak correlations as causal mechanisms

**Realistic assessment:** QJE requires the surprise finding plus the economic mechanism. BuyerBench's current result set (8 models tested) is below the heterogeneity threshold needed. Expanding to 20+ models with explicit capability-tier categorization and finding a non-obvious pattern is a prerequisite.

---

### Journal of Political Economy (JPE)

**Publisher:** University of Chicago (University of Chicago Press)  
**Impact:** Impact Factor ~8; prestige equivalent to QJE  
**Scope:** General economics with a historically strong preference for theory and well-identified causal empirics; Chicago tradition of price theory and rational choice

**Fit rationale for BuyerBench:**

JPE is the most skeptical of the four journals regarding behavioral economics (historically). The Chicago tradition emphasizes rational choice as a baseline, and behavioral papers need a particularly strong identification strategy to overcome this editorial prior. However, JPE has published behavioral work when it contains clean causal identification and tight theory — Thaler's seminal work on consumer choice anomalies appeared here.

For BuyerBench, the JPE angle is most naturally **the failure of rationality as a maintained assumption in AI agent markets.** JPE readers care about market design and general equilibrium; a paper showing that AI agents deployed in procurement markets deviate from rational choice in predictable, exploitable ways — and that this creates systematic market inefficiency — is conceptually aligned with JPE's price-theory tradition.

The JPE-specific contribution requirement: **causal identification of the bias mechanism.** JPE reviewers will want an experimental design that cleanly isolates one manipulation variable, and a theoretical framework that predicts the observed pattern from first principles (e.g., from transformer architecture + RLHF training dynamics, derive the predicted direction and magnitude of anchoring bias).

**Required evidence level for JPE submission:**
- All AER requirements, plus:
- A structural identification strategy: explain *causally* why biases arise (not just document their presence)
- An equilibrium analysis: what happens to prices or market outcomes when buyers are systematically biased?
- Ideally a lab-in-the-field design: procurement simulation where AI buyers interact with simulated suppliers and equilibrium prices are observed
- Robustness: multiple prompt phrasings, multiple model versions, temperature ablations

**What would push JPE to reject:**
- "Behavioral results without structural explanation" — JPE is less tolerant of "LLMs are like humans" framing without formal theory
- "Benchmark contribution" framing — JPE does not value methodology papers; it values economic results
- Small N or single model — JPE reviewers are trained to look for identification threats and will find them in sparse data
- "So what?" — the welfare and policy implications must be made explicit and defensible

**Realistic assessment:** JPE is likely the hardest of the four for BuyerBench because of the rational-choice prior. A paper could land here if it combines a clean structural model with credible identification and market equilibrium implications — but this is a 10+ year horizon requiring significant theoretical development beyond the current benchmark.

---

### Econometrica

**Publisher:** Econometric Society  
**Impact:** Impact Factor ~6; most prestigious methodology and theory journal in economics  
**Scope:** Economic theory, mathematical economics, econometric methods; accepts experimental and behavioral work with strong formal foundations

**Fit rationale for BuyerBench:**

Econometrica's value proposition is different from the other three: it publishes formal contributions, not just findings. Prospect Theory (Kahneman & Tversky 1979) appeared in Econometrica not because it described human behavior but because it was a formal theory with testable axioms. For BuyerBench to reach Econometrica, it would need to contribute a **formal model of bounded-rational AI agency** — a theory of how and when LLM decision-making departs from rational choice, with axioms and testable predictions.

A viable Econometrica angle: **Axiomatizing stochastic LLM choice behavior.** If we can show that LLM choice behavior violates WARP (Weak Axiom of Revealed Preference) in systematic, predictable ways, and if we can axiomatize the deviation structure (e.g., a formal "anchoring axiom" that characterizes LLM choice under reference-point manipulation), this could be an Econometrica methodological contribution to the theory of bounded rationality.

A second angle: **statistical identification of bias in stochastic agents.** LLMs produce multinomial distributions over choices, not deterministic choices. Identifying bias in a stochastic agent requires a formal statistical framework — potentially a new contribution to econometric methodology.

**Required evidence level for Econometrica submission:**
- A formal theoretical model with proofs — empirical results alone are insufficient
- Formal characterization of LLM choice behavior as a class of decision rules (not just a description)
- WARP violation tests with proper statistical power and multiple comparison correction
- Structural estimation: if proposing a model, it must be estimated from data with credible identification

**What would push Econometrica to reject:**
- "Empirical paper without theory" — Econometrica publishes empirical work only when it is tightly coupled to formal methodology
- "No mathematical contribution" — benchmarking and descriptive statistics cannot stand alone
- "Interesting but not foundational" — Econometrica wants results that will be cited for decades as definitional papers in the field

**Realistic assessment:** Econometrica is the most appropriate Tier 1 venue if BuyerBench evolves into a theoretical contribution — specifically, if the BSI formalization becomes a formal decision-theoretic characterization of bounded-rational AI agents with axioms and estimation theory. This is a high-value but long-horizon goal.

---

## Minimum Evidence Requirements — Tier 1 Submission Bar

| Requirement | Current State | Required for Tier 1 |
|---|---|---|
| Agent-run sample size per bias | 30 runs (BuyerBench baseline) | N > 500 per (bias × model) cell |
| Model coverage | 8–10 models | 15+ models across capability tiers |
| Human comparison arm | None | MTurk N ≥ 200 per condition, same vignettes |
| Structural theory | None | Formal model of bias mechanism from first principles |
| Causal identification | Controlled variants (between-subject) | Plus instrument or within-subject design with demand-effect correction |
| Temperature/stochasticity modeling | Basic variance reporting | Formal statistical model of choice distributions |
| Market implications | None | Equilibrium analysis or field evidence |
| Pre-registration | None | Required for credible causal claims |

---

## Common Rejection Triggers Across All Four Journals

1. **"Interesting measurement, no economic insight"** — the most common rejection for benchmark papers at top economics journals. The contribution must extend, revise, or challenge economic theory, not just document a fact.

2. **"Results don't generalize beyond these specific prompts"** — prompt sensitivity threatens external validity. Requires robustness tests across multiple prompt phrasings, domains, and model versions.

3. **"No theory"** — descriptive results without a formal model are insufficient. The paper must explain *why* biases arise from AI architecture or training, not just *that* they arise.

4. **"Stochastic outputs treated as deterministic"** — running a model once at temperature T and treating the output as a measurement is methodologically unsound. Temperature-sampling variance must be modeled as a confound.

5. **"Sample too small"** — economics reviewers are trained to look for statistical power. N = 30 runs per condition is publishable at behavioral psychology journals, not at AER/QJE/JPE/Econometrica.

6. **"No comparison to rational benchmark"** — the BSI metric must be defended rigorously. What does "rational" mean for an LLM? How is the oracle optimal computed? These definitions must be air-tight.

---

## Strategic Recommendation for Tier 1

**Do not target Tier 1 as the primary submission for the current paper.** The current BuyerBench paper is a benchmark contribution appropriate for NeurIPS Datasets & Benchmarks or EMNLP. It establishes priority, creates the methodology, and enables follow-on work.

**The path to Tier 1:**
1. **Year 1:** Publish benchmark paper at NeurIPS/arXiv (establishes priority, gets community feedback)
2. **Year 1–2:** Run large-scale empirical study: N ≥ 100 runs per (bias × model) cell, 15+ models
3. **Year 2:** Add human comparison arm (MTurk vignette study using same procurement scenarios)
4. **Year 2–3:** Develop structural theory of LLM bias mechanisms (collaboration with behavioral/decision economists)
5. **Year 3–4:** Submit flagship behavioral-economics paper to JEBO or Experimental Economics (Tier 2) — see [[tier2-field-journals.md]]
6. **Year 4–5+:** If Tier 2 paper generates strong findings, extend with market equilibrium model and submit to AER/QJE

**Tier 1 is a 5–10 year horizon.** The current BuyerBench work is the foundation. The journal that should receive the near-term flagship submission is JEBO or Experimental Economics (see Tier 2 analysis).

---

## Cross-References

- Tier 2 analysis (JEBO, Experimental Economics): [[tier2-field-behavioral-journals.md]]
- Current paper submission target: [[SUBMISSION-CHECKLIST]]
- Evidence requirements for statistical power: see Section B.5 ([[PILLAR2-RESEARCH-01]])
- Structural model development: future work, see [[PAPER-STATUS]] §5.4 (Future Work)
- BSI formal definition: [[economic-rationality-metrics]]
- Research gap claims: [[RESEARCH-GAPS]]
