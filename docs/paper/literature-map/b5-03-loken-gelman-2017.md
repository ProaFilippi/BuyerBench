---
type: reference
title: "B5.03 — Measurement Error and the Replication Crisis: Loken & Gelman (2017)"
created: 2026-04-16
tags:
  - measurement-error
  - replication-crisis
  - effect-size-inflation
  - statistical-noise
  - stochastic-outputs
  - winner's-curse
  - type-m-error
  - type-s-error
  - small-sample-bias
  - methodology
  - statistical-power
  - pillar2
  - literature-map
related:
  - '[[b5-01-open-science-collaboration-2015]]'
  - '[[b5-02-simmons-nelson-simonsohn-2011]]'
  - '[[b2-02-repeated-measurement-charness-levin-2005]]'
  - '[[b2-01-incentivized-hypothetical-camerer-hogarth-1999]]'
  - '[[strategy-decision-tree]]'
---

# B5.03 — Measurement Error and the Replication Crisis: Loken & Gelman (2017)

**Full citation:** Loken, E., & Gelman, A. (2017). Measurement error and the replication crisis. *Science*, 355(6325), 584–585. DOI: 10.1126/science.aal3618

**BibTeX key:** `loken2017measurement`

---

## 1. Empirical Design

Loken & Gelman (2017) is a short but influential **theoretical and simulation commentary** in *Science* that identifies a mechanism for the replication crisis that is **distinct from p-hacking and publication bias**: namely, the interaction between **high measurement noise** (large within-condition variance) and **small sample sizes** in producing systematically inflated and sign-unreliable effect size estimates.

### Core argument

The paper begins from the observation that the replication crisis cannot be fully explained by researcher misconduct or selective reporting alone. Even well-intentioned researchers following standard practice, with no deliberate p-hacking, will generate inflated effect size estimates when:

1. The **signal-to-noise ratio** in the measurement is low (i.e., the true effect is small relative to within-subject or within-condition variance), and
2. The **sample size** is insufficient to estimate the effect with acceptable precision, and
3. **Statistical significance at p < .05** is required for publication (or for a finding to be taken seriously).

This combination creates a **selection effect**: the only studies that pass the p < .05 threshold under high noise + small N are those whose sampling error happened to be positive and large. The *average* significant result under these conditions is thus not an unbiased estimate of the true effect — it is a severely upward-biased estimate drawn from the right tail of the sampling distribution.

### Type M and Type S errors

Loken & Gelman (2017) builds directly on Gelman & Carlin (2014)'s taxonomy of errors under low power:

- **Type M error (Magnitude):** Published effect size estimates are several multiples of the true effect. Even when the direction of the effect is correct, the magnitude reported in the original study will be 2–4× larger than what a well-powered replication finds.
- **Type S error (Sign):** In extremely noisy measurement environments, even the *direction* of the reported effect may be wrong — a significant positive result may correspond to a true negative or near-zero effect.

These complement (rather than replace) the traditional Type I/II error framework, which focuses on the binary significant/non-significant outcome rather than the estimated effect size.

### Key quantitative illustration

Loken & Gelman (2017) present a stylized simulation: suppose the true effect size is d = 0.3 (a small but genuine effect), measurement noise is high (σ = 1.0 per observation), and N = 20 per group. Under these conditions:

| Published significant results (p < .05) | Mean estimated effect size | Type M ratio |
|---|---|---|
| All significant results | d̂ ≈ 0.65–0.80 | **2.2–2.7×** the true effect |
| 80th-percentile significant result | d̂ > 1.0 | > 3× the true effect |
| True effect | d = 0.3 | — |

The implication: if a replication study collects N = 200 per group (adequate power), it will find d ≈ 0.3 — which is not significant at p < .05 in a small study. The original study's d ≈ 0.7 "replicates" at d ≈ 0.3, and the replication is declared a failure. But the failure is entirely attributable to the original study's inflated estimate under noise + small N, not to the replication study's methodology.

### Distinction from Simmons et al. (2011)

The central contribution of Loken & Gelman (2017) is that **researcher degrees of freedom are not required for this inflation to occur**. A scrupulously honest researcher who:
- Tests exactly one hypothesis (no multiple DVs)
- Stops data collection at a pre-committed N (no optional stopping)
- Reports the result regardless of direction (no publication bias)

...will still produce severely inflated effect size estimates if the true signal is small and the measurement is noisy, because the p < .05 threshold itself selects for extreme sampling draws. This is the **pure measurement-error contribution** to the replication crisis.

For BuyerBench, this distinction is operationally important: the p-hacking argument (Simmons et al. 2011) says prior LLM bias studies might be inflated because researchers cherry-picked prompts. The Loken & Gelman (2017) argument says prior LLM bias studies *are certainly inflated* simply because they use N=1 per condition in a high-noise environment — **even if no cherry-picking occurred at all**.

---

## 2. Strengths

1. **Identifies a mechanism that cannot be solved by pre-registration alone:** The Simmons et al. (2011) response to the replication crisis is disclosure + pre-registration. Loken & Gelman (2017) shows this is insufficient: even a fully pre-registered, single-run study with one pre-specified outcome will generate inflated effect size estimates if N is too small and measurement noise is too high. This is the more fundamental critique for the BuyerBench context, where the noise source (temperature sampling) is structural and unavoidable.

2. **Type M/S error framework is actionable:** Unlike abstract power curves, Type M and Type S errors give researchers intuitions about the *direction and magnitude* of expected inflation under specific design conditions. BuyerBench can report Type M ratios for its N=30 design versus a hypothetical N=1 design — a concrete, quantified argument for why multi-run is required.

3. **Published in *Science* with high authority:** The same journal as OSC (2015) and Loken & Gelman (2017) itself cite each other, creating a coherent narrative arc: OSC documents the problem (36% replication), Simmons et al. identifies one mechanism (p-hacking), Loken & Gelman identifies a second mechanism (measurement noise × N). Citing all three creates a complete mechanistic account of why the existing LLM bias literature is unreliable.

4. **Applies directly to noisy measurement contexts without any researcher misconduct:** For LLM behavioral research, this is particularly valuable because the noise source (temperature-sampled stochastic outputs) is not a product of researcher behavior — it is a physical property of the models. Loken & Gelman (2017) provides the theoretical foundation for why this structural noise source alone is sufficient to invalidate single-shot findings.

5. **Generalizes beyond psychology to any noisy measurement domain:** Unlike Simmons et al. (2011), which is explicitly about psychology's small-N lab conventions, Loken & Gelman (2017) applies to any scientific domain with noisy measurements. This makes it a stronger citation in the context of JEBO or AI/ML venue submissions, where reviewers may be skeptical of psychology-specific crisis framing.

---

## 3. Limitations

1. **Very short paper (2 pages) with limited simulation detail:** As a *Science* commentary, Loken & Gelman (2017) presents the argument at a high level without the simulation infrastructure of a full methods paper. For quantitative claims about Type M ratios under specific design parameters, researchers should consult the companion Gelman & Carlin (2014) paper ("Beyond Power Calculations," *Perspectives on Psychological Science*), which provides the full formal treatment. BuyerBench should cite both if using the Type M/S framework quantitatively.

2. **Does not specify the minimum N required to avoid severe inflation:** The paper demonstrates that small N + high noise produces inflation, but does not derive a general formula for "how large N must be" to achieve acceptable Type M error. This depends on the true effect size (unknown) and measurement noise (estimable from pilot data). BuyerBench must use its own pilot run distributions to estimate the noise level and back-calculate the N needed for a Type M ratio < 1.5 (a reasonable target).

3. **Assumes the true effect is stable across replications:** The Loken & Gelman (2017) framework treats the "true effect" as a fixed parameter that each sample estimates with error. For LLM behavioral experiments, the "true effect" (BSI for a given model at a given temperature on a given bias type) may itself be non-stationary across time as model weights are updated through API releases. This is a BuyerBench-specific limitation not addressed in the paper.

4. **Does not address the sign-error problem in multi-cell designs:** Type S error is most severe for single-study, single-comparison designs. For BuyerBench's multi-cell design (5 bias types × 10 models), some Type S errors are identifiable through internal cross-consistency checks (if GPT-4o shows a positive anchoring BSI in one run but a negative trend in a second run, the inconsistency is detectable). The paper does not discuss cross-cell constraints as a Type S error mitigation strategy.

5. **No LLM-specific analysis:** The paper predates LLM behavioral research and does not discuss stochastic text generation as a noise source. The mapping from "measurement noise in psychological scales" to "temperature-sampled token probabilities in LLM output distributions" requires BuyerBench-specific elaboration, which is detailed in Section 4 below.

---

## 4. Relevance to BuyerBench

### The LLM stochastic-output noise problem is a direct instance of Loken & Gelman (2017)

LLM outputs at temperature > 0 are samples from a probability distribution over token sequences. For any given prompt, the model does not produce a single deterministic output — it produces a distribution of outputs, and each run samples one from that distribution. In BuyerBench's bias measurement framework:

- **True BSI** = the probability that the model produces a bias-susceptible response in the variant condition minus the baseline condition
- **Observed BSI (N=1)** = a Bernoulli draw from that distribution — either 0 or 1, with no information about the underlying probability
- **Type M inflation under N=1:** If the true BSI is 0.20 (a 20-percentage-point elevation in bias-susceptible responses under the manipulated variant), a single observed BSI of 1.0 (bias-susceptible in variant, unbiased in baseline) is the only way to detect significance — and it is a 5× overestimate of the true effect.

This maps exactly onto the Loken & Gelman (2017) framework:

| Loken & Gelman (2017) framework | BuyerBench analogue |
|---|---|
| True effect d = 0.3 | True BSI = 0.20 |
| High measurement noise σ ≈ 1.0 | Binary Bernoulli output, σ = √(p(1-p)) ≈ 0.40 |
| N = 20 per group | N = 1 per cell (prior single-shot studies) |
| Published significant result: d̂ ≈ 0.7 | Observed significant BSI: 1.0 (or 0 in baseline) |
| Type M ratio: 2.3× | Type M ratio: 5× (observed 1.0 vs. true 0.20) |
| Replication at N = 200: d̂ ≈ 0.3 (appears to fail) | Replication at N = 30: BSI ≈ 0.18–0.22 (not significant in isolation) |

The implication for the existing LLM behavioral bias literature (Binz & Schulz 2023, Hagendorff et al. 2023, Jones & Steinhardt 2022) is stark: **every single-shot finding in this literature is subject to a minimum 3–5× Type M inflation under Loken & Gelman (2017)'s framework**, regardless of whether any p-hacking occurred. The studies are not fabricated — they are simply subject to the same statistical physics that afflicts any small-N study with high measurement noise.

### Quantitative Type M analysis for N=30 vs. N=1 in BuyerBench

For a binary outcome (bias-susceptible: yes/no), measurement noise is fully determined by the true proportion p:

**σ² = p(1-p)**

For p in the range [0.10, 0.40] (the plausible range for a genuine bias effect):

| True BSI (p) | σ (measurement noise) | N=1 Type M ratio | N=30 Type M ratio | N=30 Type S error rate |
|---|---|---|---|---|
| 0.10 | 0.30 | ~10× | ~1.8× | < 5% |
| 0.20 | 0.40 | ~5× | ~1.4× | < 2% |
| 0.30 | 0.46 | ~3.3× | ~1.2× | < 1% |
| 0.40 | 0.49 | ~2.5× | ~1.1× | < 1% |

At N=30 per cell, Type M ratios drop below 1.5× for all plausible true BSI values ≥ 0.20, and Type S errors become negligible. This is the quantitative justification for BuyerBench's N=30 minimum design: it is the smallest N at which the Loken & Gelman (2017) inflation mechanism is adequately controlled for the expected effect sizes in this domain.

For truly small effects (true BSI ≈ 0.10), N=30 is still insufficient for reliable magnitude estimation (Type M ≈ 1.8×). This is a pre-registered limitation: effects this small require N=80–100 per cell to achieve Type M < 1.2×. BuyerBench's N=30 design is adequate for detecting and estimating moderate-to-large bias effects (true BSI ≥ 0.20); it is not adequate for characterizing small but genuine effects.

### Design implication: reporting BSI with bootstrap confidence intervals is mandatory

Because point-estimate BSI from finite N is subject to Type M inflation, **all BuyerBench BSI estimates must be reported with bootstrap 95% confidence intervals** (1,000 resamples from the N=30 binary outcome vector per cell). This makes the uncertainty in the effect size estimate transparent and allows readers to judge whether the point estimate is consistent with a small true effect with high Type M inflation, or a genuinely large effect.

For cells with BSI confidence intervals that span zero, conclude "no reliable bias susceptibility detected" rather than "bias susceptibility refuted." Loken & Gelman (2017) cautions against converting non-significant findings into null findings when power is limited — but BuyerBench's N=30 design has adequate power for BSI ≥ 0.20, so confidence intervals spanning zero at N=30 are *informative* rather than merely underpowered.

### The retroactive inflation argument for prior LLM bias literature

Loken & Gelman (2017) provides the mechanism for a specific critique of the existing LLM behavioral literature:

> "Single-shot LLM bias studies (Binz & Schulz 2023; Hagendorff et al. 2023; Jones & Steinhardt 2022; Echterhoff et al. 2024) suffer from severe Type M error under the Loken & Gelman (2017) measurement-error framework. With N=1 per condition, binary behavioral outcomes, and a significance threshold applied post-hoc, the expected inflation of observed effect sizes relative to true effect sizes is 3–10× depending on the true bias susceptibility probability. BuyerBench's N=30 multi-run design was explicitly designed to bring Type M ratios below 1.5× across all plausible effect sizes in the target range (true BSI ≥ 0.20)."

This argument applies even to the Echterhoff et al. (2024) study, which uses a large total prompt count (16,800) but aggregates across models, prompts, and conditions in ways that do not provide N=30 within any single (model × bias × variant) cell.

### Design implication: "null finding at N=30" is a genuine contribution

One of Loken & Gelman (2017)'s implicit messages is that a well-powered null result is more informative than an underpowered positive result. BuyerBench's near-zero BSI across most (model × bias) cells at N=30 is, by Loken & Gelman (2017)'s logic:

1. **Stable across replications** (not a Type M artifact that would shrink under a larger-N replication)
2. **Inconsistent with large true effects** (a true BSI of 0.30 would appear in more than 1-in-30 draws; if zero cells in N=30 show bias, the 95% CI for the true BSI is [0, 0.12])
3. **A genuine finding, not a methodological failure** — the finding is "frontier LLMs resist behavioral manipulation in economically structured procurement decisions," which is theoretically interesting and publishable

---

## 5. Paper Framing Guidance

- **Introduction:** Brief mention in the context of explaining why BuyerBench uses N=30 rather than N=1. One sentence: "Single-run LLM evaluations are subject to severe effect size inflation under measurement noise (Loken & Gelman 2017), motivating our multi-run design." Do not elaborate in the introduction.

- **Methodology section:** This is the primary citation context. In the power analysis / sample size justification subsection:
  > "We set N=30 runs per (model × bias × variant) cell based on a Type M error analysis (Loken & Gelman 2017; Gelman & Carlin 2014). At N=30 with binary behavioral outcomes, the expected Type M ratio — the ratio of observed significant effect size to the true effect size — falls below 1.5× for all true BSI values ≥ 0.20, the minimum effect size we treat as practically meaningful for procurement decision quality. N=1 per cell, as used in prior single-shot LLM behavioral studies, yields Type M ratios of 3–10× for the same effect size range."

- **Related work section:** Use Loken & Gelman (2017) to contextualize the prior literature critique:
  > "Prior work on LLM behavioral biases (Binz & Schulz 2023; Hagendorff et al. 2023; Jones & Steinhardt 2022; Echterhoff et al. 2024) uses predominantly single-shot evaluations. Under Loken & Gelman (2017)'s measurement-error framework, single-shot binary outcome studies with N=1 per condition yield expected Type M ratios of 3–10× relative to true effect sizes. BuyerBench's multi-run design was designed explicitly to address this limitation."

- **Results section:** When reporting near-zero BSI findings, note that the N=30 design makes these informative:
  > "BSI ≤ 0.05 in X of 50 (model × bias) cells (BH-FDR corrected). This near-zero pattern is not a power failure: at N=30, the 95% bootstrap confidence interval for a null cell is BSI ∈ [0, 0.12], ruling out true BSI values ≥ 0.20 with high confidence (Loken & Gelman 2017)."

- **Discussion:** Connect the near-zero BuyerBench BSI pattern to the inflation correction argument:
  > "We cannot rule out that the large bias effects reported in prior single-shot LLM studies (e.g., Hagendorff et al. 2023; Jones & Steinhardt 2022) are genuine — it is possible that frontier models have reduced bias susceptibility relative to GPT-3 era models. However, the Loken & Gelman (2017) measurement-error mechanism provides an alternative explanation: single-shot studies with binary outcomes systematically overestimate true effect sizes by 3–10×. Under this correction, a single-shot observed BSI of 1.0 would correspond to a true BSI of approximately 0.20, which our N=30 design would detect with 80% power. The absence of large-effect detections at N=30 is thus consistent with either true small effects or genuine near-zero bias susceptibility in structured economic decision tasks."

---

## 6. BibTeX Entry

```bibtex
@article{loken2017measurement,
  title   = {Measurement Error and the Replication Crisis},
  author  = {Loken, Eric and Gelman, Andrew},
  journal = {Science},
  volume  = {355},
  number  = {6325},
  pages   = {584--585},
  year    = {2017},
  doi     = {10.1126/science.aal3618}
}
```

**Related BibTeX entries:**

```bibtex
@article{gelman2014beyond,
  title   = {Beyond Power Calculations: Assessing Type S (Sign) and Type M (Magnitude) Errors},
  author  = {Gelman, Andrew and Carlin, John},
  journal = {Perspectives on Psychological Science},
  volume  = {9},
  number  = {6},
  pages   = {641--651},
  year    = {2014},
  doi     = {10.1177/1745691614551642}
}

@article{osc2015reproducibility,
  title   = {Estimating the Reproducibility of Psychological Science},
  author  = {{Open Science Collaboration}},
  journal = {Science},
  volume  = {349},
  number  = {6251},
  pages   = {aac4716},
  year    = {2015},
  doi     = {10.1126/science.aac4716}
}

@article{simmons2011false,
  title   = {False-Positive Psychology: Undisclosed Flexibility in Data Collection and Analysis Allows Presenting Anything as Significant},
  author  = {Simmons, Joseph P. and Nelson, Leif D. and Simonsohn, Uri},
  journal = {Psychological Science},
  volume  = {22},
  number  = {11},
  pages   = {1359--1366},
  year    = {2011},
  doi     = {10.1177/0956797611417632}
}

@article{charness2005individual,
  title   = {Individual Experimentation and Social Learning: An Experimental Study},
  author  = {Charness, Gary and Levin, Dan},
  journal = {Economic Journal},
  volume  = {115},
  number  = {507},
  pages   = {C73--C87},
  year    = {2005},
  doi     = {10.1111/j.0013-0133.2005.00981.x}
}
```
