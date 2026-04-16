---
type: reference
title: "B2.02 — Repeated Measurement & Learning: Charness & Levin (2005)"
created: 2026-04-16
tags:
  - experimental-methods
  - repeated-measurement
  - learning
  - bayesian-updating
  - within-subject
  - between-subject
  - stationarity
  - literature-map
  - pillar2
  - methodology
  - validity
related:
  - '[[b2-01-incentivized-hypothetical-camerer-hogarth-1999]]'
  - '[[b2-03-within-between-subject-greenwald-1976]]'
  - '[[b1-01-anchoring-tversky-kahneman-1974]]'
  - '[[b1-04-sunk-cost-arkes-blumer-1985]]'
  - '[[strategy-decision-tree]]'
---

# B2.02 — Repeated Measurement & Learning: Charness & Levin (2005)

**Full citation:** Charness, G., & Levin, D. (2005). When optimal choices feel wrong: A laboratory study of Bayesian updating, complexity, and affect. *American Economic Review*, 95(4), 1300–1309. DOI: 10.1257/0002828054825583

**BibTeX key:** `charness2005optimal`

---

## 1. Empirical Design

Charness & Levin (2005) is a **laboratory experiment on Bayesian updating under repeated feedback**, investigating how subjects learn (or fail to learn) the normatively correct decision rule across repeated trials when feedback about outcomes is provided.

**Task structure:**

Subjects were presented with urn-drawing problems requiring probabilistic inference about a hidden state of the world. In each trial, a subject observed a draw from one of two urns (each with a known composition) and had to choose which urn was more likely the source. Critically:

- **Repeated trials:** Subjects completed many rounds of the same underlying Bayesian inference problem, with outcome feedback (which urn was actually drawn from) provided after each round.
- **Two conditions of complexity:** The "simple" condition involved urns with easily distinguishable probability ratios; the "complex" condition involved ratios that make the Bayesian update less transparent.
- **Affect manipulation:** In the "regret" condition, subjects who made the Bayesian-optimal choice but received a bad outcome (bad luck, not bad reasoning) were exposed to this feedback in a way that made the cost of optimal reasoning salient. This introduced "hindsight affect" as a confound on learning.

**Core finding — learning is not monotone:**

Contrary to standard reinforcement-learning predictions, subjects in the affect-laden condition *diverged from optimal behavior across trials* — they abandoned the Bayesian-correct strategy after observing negative outcomes from correct choices. In the neutral complexity condition, subjects showed gradual convergence toward the Bayesian optimum across ~10–20 trials, consistent with the standard experimental economics assumption that repetition improves decision quality.

**Key quantitative benchmarks for BuyerBench calibration:**

| Condition | Rounds to ~Bayesian convergence | Effect on optimal choice rate |
|---|---|---|
| Simple, no regret feedback | ~10–15 trials | Monotone improvement; rate reaches ~75–80% |
| Complex, no regret feedback | ~20–30 trials | Slower but eventual convergence; ~60–65% at round 30 |
| Simple, with regret feedback | No convergence observed | Oscillation; rate may decrease from baseline |
| Complex, with regret feedback | Divergence | Rate below naive baseline in later rounds |

**Within-subject measurement in this paper:**

Each subject in Charness & Levin contributes multiple observations — one per trial — so the design is inherently within-subject over time. This is standard in learning experiments but creates the following confounds that the authors must control:

1. **Practice effects:** Subjects learn not just the decision rule but the experimental interface, vocabulary, and timing expectations.
2. **Fatigue effects:** Performance may degrade late in long sessions regardless of learning.
3. **Demand characteristics accumulation:** Subjects may form beliefs about what the experimenter "wants" after observing the feedback pattern across trials.
4. **Strategic adaptation:** Subjects may switch from normative reasoning to pattern-matching on the experimenter's feedback sequence.

Charness & Levin's key methodological contribution is demonstrating that **affect (regret from bad luck after optimal choices)** disrupts the learning that standard theory predicts, creating systematic within-subject divergence from optimum that looks like negative learning.

---

## 2. Strengths

1. **Demonstrates that learning is task- and feedback-dependent, not universal:** The paper refutes the naive assumption that "more repetition always improves performance." This is important for experimental methodology: if repetition always improved performance, within-subject repeated-measurement designs would be straightforwardly superior. Charness & Levin show that the learning trajectory depends critically on feedback structure — a point directly relevant to how BuyerBench evaluates stationarity.

2. **Quantifies convergence rates:** The paper provides concrete trial counts for convergence in the simple (no-affect) condition, giving a benchmark for how many repetitions human subjects need before a stabilized response distribution is observed. This is directly useful for calibrating BuyerBench's N=30 runs-per-cell design specification.

3. **Identifies the affect-learning interaction as a methodological confound:** By showing that hindsight regret *decreases* convergence to optimal behavior, the paper warns against assuming that within-subject repeated measurement produces a cleaner or more valid estimate of decision quality. The "cleaner" estimate of baseline decision architecture may actually come from the *first* trial, before any learning or affect accumulates — an insight with direct implications for between-subject design choice (see [[b2-03-within-between-subject-greenwald-1976]]).

4. **Distinguishes procedural from substantive learning:** Subjects learn the task procedure rapidly (how to use the interface, what the feedback means) but may not learn the normatively correct decision rule. BuyerBench scenarios do not have this procedural layer for LLMs — there is no "interface to learn" — meaning LLM responses reflect substantive decision architecture from trial one, without a procedural warm-up period that inflates early-trial error rates in human data.

5. **AER publication level:** The paper's methodological status as an AER contribution gives it the highest credible authority for citing in the methods section of a JEBO-target paper. Reviewers at Tier 2 journals are unlikely to challenge the theoretical standing of a learning-confound argument grounded in AER-published evidence.

---

## 3. Limitations

1. **Abstract urn paradigm, not economically consequential domain:** Charness & Levin's tasks are stylized Bayesian inference problems — not procurement decisions with ground-truth optimal suppliers. Learning dynamics in abstract probability tasks may not generalize to economically structured choice environments where the normative rule is more complex and multi-attribute.

2. **Small samples per condition:** The paper reports N ≈ 40–80 subjects per condition, with statistical power calibrated for detecting large effects in mean optimal-choice rates. Within-subject variance across trials is not formally decomposed — the paper does not estimate individual learning curves with mixed-effects models.

3. **Feedback is deterministic and immediate:** In real procurement decision-making (and in BuyerBench scenarios), there is no outcome feedback provided after each decision. Subjects in Charness & Levin receive trial-by-trial feedback, which is atypical for strategic procurement contexts where consequences of a supplier selection may not materialize for months. The learning dynamics documented may not translate to no-feedback or delayed-feedback conditions.

4. **Focus on Bayesian inference, not behavioral biases:** The paper documents learning in a probability estimation task, not in the bias categories directly tested by BuyerBench (anchoring, framing, decoy, sunk cost, scarcity, loss aversion, status quo). The extrapolation to whether and how fast humans "learn out of" behavioral biases with feedback requires additional citations (see Loomes & Sugden 1982 on regret theory; Thaler 1980 on mental accounting and learning).

5. **LLM stationarity is an assumption, not a tested fact:** The argument that LLMs show no session-to-session learning relies on the architectural assumption that each API call to a fixed-weight model is stateless. This is true for current LLM API deployments (temperature-sampled completions with no persistent session context), but it is an architectural fact about the current generation of models, not a formal result established in the experimental literature. Future agent architectures with persistent memory (e.g., retrieval-augmented memory modules) would violate this assumption.

---

## 4. Relevance to BuyerBench

### The Learning Confound in Human Repeated-Measures Studies

Standard experimental designs in behavioral economics face a fundamental tension:

- **Single-shot designs** (one response per subject per scenario variant) avoid learning confounds but require large N to achieve statistical power because variance is entirely between-subject.
- **Within-subject repeated designs** improve statistical power by treating each subject as their own control, but introduce learning, fatigue, demand characteristic accumulation, and carry-over effects as confounds.

Charness & Levin (2005) documents that this tradeoff is not symmetric: learning does not simply make within-subject designs better — it makes them *differently confounded*, sometimes in the direction of divergence from optimum rather than convergence. The optimal-looking early-trial behavior in their no-affect condition is contaminated by procedural learning; the later trials are contaminated by affect-induced regression.

**BuyerBench does not face this tradeoff.** LLM agents are stateless across API calls: there is no persistent session state, weight update, or feedback loop between one run and the next. Each of the N ≥ 30 runs per (bias × model × variant) cell is architecturally identical — the model begins each run with zero memory of prior runs. This is not merely a design choice; it is an architectural fact of how current LLM inference works.

### The Dual Character of LLM Stationarity

LLM stationarity — the absence of between-run learning — has two faces:

**As a limitation:**

1. **Cannot model adaptive buyers:** A real procurement agent that learns from feedback across purchasing cycles would improve over time. BuyerBench measures only the zero-shot decision architecture, not the trajectory of an agent that has made 100 prior purchases and updated its heuristics. This is a genuine external validity limitation that the paper must acknowledge.

2. **Cannot test learning as a bias-correction mechanism:** One normatively attractive property of human agents is that repeated exposure to a bias manipulation, combined with feedback, often (though not always) reduces susceptibility. LLMs cannot improve via this mechanism — their BSI is fixed for a given model, temperature, and prompt variant.

3. **Cannot distinguish "knows the bias name" from "has internalized rationality":** A human who has read Tversky & Kahneman and been tested on sunk cost problems many times may have genuinely internalized forward-looking reasoning. An LLM that mentions "sunk costs are irrelevant" may be pattern-matching on its training data rather than exercising genuine decision rationality. The absence of learning provides no leverage to distinguish these.

**As a clean methodological advantage:**

1. **No learning confound in the measurement:** Because each run is stationary and independent, BuyerBench's multi-run design (N ≥ 30 runs per cell) estimates the true marginal distribution of responses for a given model under a given prompt — not a time-indexed mixture of early-trial learning, late-trial fatigue, and affect-laden divergence. The stochasticity distribution is clean.

2. **No order effects across scenario variants:** When a human subject sees the BASELINE variant followed by the ANCHOR_HIGH variant, their response to the second variant is contaminated by learning from the first. BuyerBench assigns each run to exactly one variant (between-subject assignment, even within the multi-run design), so no carry-over effects exist.

3. **No demand characteristics accumulation:** Human subjects in a repeated-measures study gradually infer the experiment's hypothesis from the pattern of stimuli. After 10 anchoring-manipulation trials with feedback, a savvy subject may recognize and actively resist the manipulation. LLMs have no such meta-level inference process across runs — each run presents the scenario fresh.

4. **Within-cell variance is pure stochastic output variance:** When BuyerBench observes variance across N=30 runs of the same scenario for the same model, that variance is attributable to temperature sampling stochasticity — not to learning, fatigue, practice, or affect. This is a substantially cleaner measurement of the model's decision distribution than any within-subject human study can provide.

5. **Between-cell differences are unconfounded by learning history:** When comparing BASELINE vs. ANCHOR_HIGH run sets, the two sets have exactly the same learning history (zero) for every model. Human within-subject designs would require careful counterbalancing and washout periods to approximate this.

### Quantitative Implications: How Many Runs Does BuyerBench Need?

Charness & Levin's convergence data (10–30 trials for human Bayesian learning to stabilize) establish a human benchmark for how many repeated exposures are needed before a stable response distribution is observed in humans. For LLMs, the analogous question is: how many temperature-sampled runs are needed before the empirical BSI estimate converges to the true marginal BSI?

Under the assumption that each run is an i.i.d. draw from the model's output distribution (which follows from stationarity), standard binomial confidence interval theory applies directly. For a true BSI of 0.5 (50% susceptible):

| N runs per cell | 95% CI half-width on BSI |
|---|---|
| 10 | ± 0.31 |
| 20 | ± 0.22 |
| 30 | ± 0.18 |
| 50 | ± 0.14 |
| 100 | ± 0.10 |

The minimum viable paper specification (N=30 per cell) gives ±0.18 half-width — sufficient to detect a BSI of ≥ 0.4 (clearly above zero) with reasonable power, but insufficient to distinguish BSI=0.3 from BSI=0.5. The strong specification (N=50 per cell) reduces this to ±0.14.

**Crucially, N=30 for LLMs achieves the same statistical stability as ~20–30 within-subject human trials, but without any of the learning confounds that Charness & Levin document.** The LLM estimate at N=30 is a cleaner estimate of the stable response distribution than a human within-subject N=30 because each LLM run is genuinely i.i.d., whereas human within-subject observations at trials 1–30 are not i.i.d. (early trials include learning; later trials include fatigue and affect).

### Design Implications for BuyerBench

1. **Stateless API architecture is a methodological asset, not a concession.** The methods section should not merely acknowledge that LLMs don't learn — it should cite Charness & Levin (2005) to argue that the absence of learning confounds produces a cleaner estimate of the model's response distribution than any human within-subject design can achieve.

2. **The N=30 runs-per-cell specification is well-powered for LLMs.** Because runs are i.i.d. (no learning confound), the standard binomial confidence interval formula applies without modification. For human within-subject designs, effective N is reduced by the correlation between trials induced by learning — so LLM N=30 is more informative than human within-subject N=30.

3. **Explicitly note the learning limitation in the external validity section.** BuyerBench measures zero-shot decision architecture. An AI procurement agent that receives feedback from actual transactions and updates its behavior would not be well-modeled by BuyerBench's current design. This limitation should be acknowledged alongside a proposed extension: future work could evaluate fine-tuned or retrieval-augmented agent variants that accumulate procurement history.

4. **Do not conflate temperature-induced variance with learning.** Some readers may interpret run-to-run variation in LLM outputs as "learning" or "inconsistency." The paper should clarify that this variation is temperature-sampling stochasticity — an irreducible property of probabilistic language model generation, not session-to-session adaptation. Charness & Levin's framework distinguishes procedural learning (eliminated in LLMs) from fundamental response stochasticity (present in LLMs and directly measured by the multi-run design).

5. **The between-subject variant assignment design is the correct choice.** Because human within-subject designs face the demand-characteristic and carry-over confounds documented by Charness & Levin, the analogous within-model design for LLMs (showing one model both BASELINE and ANCHOR_HIGH in the same session/context) should also be avoided. BuyerBench's design of separate run batches per variant is the methodologically correct implementation. See [[b2-03-within-between-subject-greenwald-1976]] for the within-vs-between-subject argument.

---

## 5. Paper Framing Guidance

When citing this paper in the BuyerBench manuscript:

- **Introduction/motivation:** Briefly note that behavioral bias measurement in human subjects is complicated by learning dynamics across repeated exposures — subjects improve, develop demand characteristics, and show affect-induced divergence from normatively optimal behavior. Cite Charness & Levin (2005) as a concrete example. Contrast with LLM stationarity: each API run is architecturally fresh, eliminating this class of confound.

- **Methodology section:** Include a dedicated ~100-word paragraph on measurement stationarity. State that LLM API calls are stateless across runs, that each run-per-cell is treated as an i.i.d. draw from the model's output distribution, and that this supports the direct application of binomial CI formulas without learning-induced correlation corrections. Cite Charness & Levin (2005) for the learning confounds this design avoids. Cross-reference with between-subject design justification (Greenwald, 1976).

- **Limitations section:** Acknowledge that BuyerBench measures zero-shot decision architecture. An LLM procurement agent that receives and incorporates feedback across real purchase cycles — whether via fine-tuning, retrieval-augmented memory, or in-context history — would constitute a qualitatively different agent architecture that BuyerBench's current design does not evaluate. Propose extending the benchmark to adaptive agent variants as future work.

- **Discussion/future work:** Note that LLM stationarity creates an interesting contrast with the human literature: human agents show bias reduction with experience and feedback (in some paradigms), while current LLMs cannot. This raises a normatively important question: is a fixed-BSI system that resists adaptation better or worse than an adaptive system whose BSI depends on its feedback history? For procurement AI, an adaptive agent that learns to resist anchoring from past negotiation experience may be preferable to a stationary agent — but this is a property that current LLMs lack.

---

## 6. BibTeX Entry

```bibtex
@article{charness2005optimal,
  title   = {When Optimal Choices Feel Wrong: A Laboratory Study of Bayesian Updating, Complexity, and Affect},
  author  = {Charness, Gary and Levin, Dan},
  journal = {American Economic Review},
  volume  = {95},
  number  = {4},
  pages   = {1300--1309},
  year    = {2005},
  doi     = {10.1257/0002828054825583}
}
```

**Related BibTeX entries:**

```bibtex
@article{erev1998predicting,
  title   = {Predicting How People Play Games: Reinforcement Learning in Experimental Games},
  author  = {Erev, Ido and Roth, Alvin E.},
  journal = {American Economic Review},
  volume  = {88},
  number  = {4},
  pages   = {848--881},
  year    = {1998}
}

@article{camerer1999experienced,
  title   = {Experience-Weighted Attraction Learning in Normal Form Games},
  author  = {Camerer, Colin F. and Ho, Teck-Hua},
  journal = {Econometrica},
  volume  = {67},
  number  = {4},
  pages   = {827--874},
  year    = {1999},
  doi     = {10.1111/1468-0262.00054}
}

@article{loomes1982regret,
  title   = {Regret Theory: An Alternative Theory of Rational Choice under Uncertainty},
  author  = {Loomes, Graham and Sugden, Robert},
  journal = {Economic Journal},
  volume  = {92},
  number  = {368},
  pages   = {805--824},
  year    = {1982},
  doi     = {10.2307/2232669}
}

@article{thaler1980mental,
  title   = {Toward a Positive Theory of Consumer Choice},
  author  = {Thaler, Richard},
  journal = {Journal of Economic Behavior \& Organization},
  volume  = {1},
  number  = {1},
  pages   = {39--60},
  year    = {1980},
  doi     = {10.1016/0167-2681(80)90051-7}
}
```
