---
type: research
title: "B.6 — Literature Synthesis: What Is Known, Unresolved, and Where BuyerBench Contributes"
created: 2026-04-16
tags:
  - synthesis
  - literature-review
  - pillar2
  - behavioral-economics
  - llm-bias
related:
  - '[[b1-01-anchoring-tversky-kahneman-1974]]'
  - '[[b1-02-framing-tversky-kahneman-1981]]'
  - '[[b1-03-decoy-effect-huber-payne-puto-1982]]'
  - '[[b1-04-sunk-cost-arkes-blumer-1985]]'
  - '[[b1-05-scarcity-cialdini-worchel-1975]]'
  - '[[b1-06-status-quo-bias-samuelson-zeckhauser-1988]]'
  - '[[b1-07-loss-aversion-kahneman-tversky-1979]]'
  - '[[b2-01-incentivized-hypothetical-camerer-hogarth-1999]]'
  - '[[b2-02-repeated-measurement-charness-levin-2005]]'
  - '[[b2-03-within-between-subject-greenwald-1976]]'
  - '[[b3-01-binz-schulz-2023]]'
  - '[[b3-02-ortega-maini-2023-ai-safety-gridworlds]]'
  - '[[b3-03-hagendorff-2023]]'
  - '[[b3-04-aher-2023]]'
  - '[[b3-05-jones-steinhardt-2022]]'
  - '[[b3-06-echterhoff-2024]]'
  - '[[b4-01-simon-1955-satisficing]]'
  - '[[b4-02-nudge-thaler-sunstein-2008]]'
  - '[[b4-03-charness-rabin-2002-social-preferences]]'
  - '[[b5-01-open-science-collaboration-2015]]'
  - '[[b5-02-simmons-nelson-simonsohn-2011]]'
  - '[[b5-03-loken-gelman-2017]]'
---

# B.6 — Literature Synthesis

## What Is Known, What Is Unresolved, and Where BuyerBench Contributes

---

### What Is Known

The behavioral economics literature establishes a robust catalogue of human decision biases — anchoring (Tversky & Kahneman, 1974), framing effects (1981), the decoy effect (Huber et al., 1982), sunk cost fallacy (Arkes & Blumer, 1985), scarcity-driven valuation inflation (Cialdini, 1984; Worchel et al., 1975), status quo bias (Samuelson & Zeckhauser, 1988), and loss aversion (Kahneman & Tversky, 1979). Across decades of incentivized and hypothetical experiments, these biases have been replicated in human subjects with well-characterized effect sizes. Importantly, Camerer & Hogarth (1999) show that incentives do not reliably eliminate these effects for heuristic-dominated tasks, establishing a shared methodological foundation between human and LLM behavioral research.

A newer literature has documented analogous patterns in large language models. Binz & Schulz (2023) found that GPT-3 exhibits a mixed rational/biased profile across ten cognitive tasks. Hagendorff et al. (2023) demonstrated that GPT-4, despite greater capability, shows *more* System 1-type intuitive errors than GPT-3 on canonical CRT and conjunction fallacy tasks. Jones & Steinhardt (2022) systematically mapped LLM failures onto a cognitive bias taxonomy using adversarial NLP probes. Echterhoff et al. (2024) found large framing and anchoring effects in a college admissions domain across four models. Across all of this work, a consistent finding is that instruction-following and alignment training do not fully insulate frontier models from the influence of irrelevant contextual cues — a pattern consistent with Simon's (1955) satisficing framework and Thaler & Sunstein's (2008) characterization of decision-makers as nudgeable by choice architecture.

### What Is Unresolved

Four questions dominate the open frontier. First, **multi-model comparative variation**: do bias susceptibility profiles differ systematically across model families and capability tiers, or is susceptibility roughly uniform? No published study has adequately powered this comparison — Binz & Schulz tested one model; Hagendorff et al. used 9 models but a single run each; Echterhoff et al. used 4 models, only 2 of which are current-generation. Second, **domain specificity**: all prior LLM bias studies use abstract cognitive tasks (cognitive reflection, Asian Disease, bar-and-ball) or a non-procurement social domain (college admissions). Whether the documented biases transfer to economically consequential B2B procurement decisions — where rubrics, constraints, and financial stakes are explicit — is untested. Third, **stochastic output variance as confound**: single-shot designs (Binz & Schulz; Jones & Steinhardt; Hagendorff et al.) cannot distinguish genuine bias susceptibility from temperature-sampling noise. Loken & Gelman (2017) show that significance thresholds applied to noisy single-shot measurements produce Type M magnitude errors of 2–5×. No existing LLM bias study models or corrects for this inflation. Fourth, **economic rationality operationalization**: existing studies measure consistency (does the model choose differently across frames?) without a ground-truth optimal against which deviation is economically quantified. The Bias Susceptibility Index (BSI) as a normalized deviation from a computable rational benchmark has not been formally defined or applied.

### Where BuyerBench Contributes

BuyerBench addresses all four gaps simultaneously. It is the first controlled-variant bias battery in an economically consequential procurement decision domain where a ground-truth optimal is computable for every scenario. Its between-subject controlled-variant design (following Greenwald, 1976; avoiding demand-characteristic confounds specific to LLMs) isolates bias effects from capability confounds. Its multi-run architecture (N ≥ 30 per cell) directly models stochastic output variance, enabling Type M ratio estimation and bootstrap confidence intervals as recommended by Loken & Gelman (2017) and pre-registration protocols motivated by Simmons et al. (2011) and the Open Science Collaboration (2015). Its ten-model comparative scope enables the first adequately powered test of whether bias susceptibility is a property of model capability, architecture, or training regime. The resulting BSI formalization quantifies not merely whether a model's choice shifted under manipulation, but by how much it deviated from the economically optimal action — a standard imported from behavioral economics but not yet applied to LLM agent evaluation.

---

> **Word count:** ~510 words (extended from 400 target to accommodate the four-gap structure; can be trimmed to 400 for the paper by condensing the "What Is Known" section and removing citation parentheticals).

---

### BibTeX Summary (cross-reference to individual notes)

All primary references are documented with full BibTeX entries in the individual literature notes (b1-01 through b5-03). The synthesis draws specifically on:

- Tversky & Kahneman (1974, 1979, 1981) — canonical bias benchmarks
- Camerer & Hogarth (1999) — incentive equivalence foundation
- Greenwald (1976) — between-subject design rationale
- Binz & Schulz (2023); Hagendorff et al. (2023); Jones & Steinhardt (2022); Echterhoff et al. (2024) — prior LLM bias literature to extend/surpass
- Loken & Gelman (2017); Simmons et al. (2011); Open Science Collaboration (2015) — methodological robustness grounding
- Simon (1955); Thaler & Sunstein (2008) — bounded rationality theoretical framing
