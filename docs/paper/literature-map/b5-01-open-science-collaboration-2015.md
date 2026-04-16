---
type: reference
title: "B5.01 — Replication Crisis: Open Science Collaboration (2015)"
created: 2026-04-16
tags:
  - replication-crisis
  - methodology
  - statistical-power
  - multi-run-design
  - behavioral-bias
  - literature-map
  - pillar2
  - reproducibility
  - false-positives
  - variance
related:
  - '[[b5-02-simmons-nelson-simonsohn-2011]]'
  - '[[b5-03-loken-gelman-2017]]'
  - '[[b2-01-incentivized-hypothetical-camerer-hogarth-1999]]'
  - '[[b2-02-repeated-measurement-charness-levin-2005]]'
  - '[[b2-03-within-between-subject-greenwald-1976]]'
  - '[[strategy-decision-tree]]'
---

# B5.01 — Replication Crisis: Open Science Collaboration (2015)

**Full citation:** Open Science Collaboration. (2015). Estimating the reproducibility of psychological science. *Science*, 349(6251), aac4716. DOI: 10.1126/science.aac4716

**BibTeX key:** `osc2015reproducibility`

---

## 1. Empirical Design

The Open Science Collaboration (2015) is a **large-scale coordinated replication project** involving 270 contributing researchers who attempted to replicate 100 studies from three high-impact psychology journals (*Psychological Science*, *Journal of Personality and Social Psychology*, and *Journal of Experimental Psychology: Learning, Memory, and Cognition*) published in 2008.

**Sampling frame:** 100 studies were selected from 2008 publication years — a year chosen to provide sufficient temporal distance for independent replication teams to be unlikely to overlap with original authors. Studies covered social, cognitive, and developmental psychology subfields.

**Replication protocol:**
- Replication teams were assigned to specific original studies and given access to original materials, stimuli, and analysis code where available
- Each replication team pre-registered their protocol before data collection
- The standard criterion was: collect N sufficient to detect the original effect size at 80% power (i.e., deliberately powered to detect the *reported* effect, which itself may be inflated by publication bias and p-hacking)

**Key quantitative findings:**

| Replication metric | Result |
|---|---|
| Statistical significance replication rate (p < .05) | ~36–39% of original 97 significant results |
| Mean original effect size (r) | 0.403 |
| Mean replication effect size (r) | 0.197 — approximately **half** of the original |
| Subjective replication success (expert ratings) | ~47% |
| High original significance (p < .001) predicts success | Yes: 47% replication rate vs. 28% for p < .05 |
| Original effect size predicts replication success | Yes: larger original ES → higher replication probability |

**Domain variation:**
- Cognitive psychology replicated at a higher rate (~50%) than social psychology (~25%)
- Studies using within-subject designs replicated more reliably than between-subject designs
- Studies with larger original samples replicated more reliably

**Theoretical interpretation:**
The paper explicitly does not attribute the replication failure rate to fraud, but rather to a combination of: (a) underpowered original studies (low N inflates false-positive rate under flexible analysis), (b) publication bias (only significant results get published, selecting for effects that were chance occurrences), (c) *p*-hacking and researcher degrees of freedom (optional stopping, covariate selection, outlier exclusion), and (d) genuine context-sensitivity of effects (results do not generalize across samples, labs, and time).

---

## 2. Strengths

1. **Largest coordinated replication in psychology history:** 100 simultaneous replications provide a statistical power to characterize the *distribution* of replication success rates, not merely document individual failures. The collaborative design prevents the "replication failure = methodological difference" deflection by following original protocols closely.

2. **Multiple correlated replication metrics:** The paper reports five independent indicators of replication success (p-value replication, effect-size correlation, effect size significantly different from original, meta-analytic combination, subjective expert rating). Their convergence strengthens the central finding beyond any single metric's limitations. The ~36% p-value rate and ~47% subjective rate bracket a plausible "true" replication rate in the 40–50% range.

3. **Effect size shrinkage is a direct, quantified signal:** The finding that replication effect sizes average 50% of the original is arguably more important than the significance rate, because it gives a concrete correction factor. It establishes that single-study effect size estimates are systematically biased upward — a prior every researcher should have when reading *any* behavioral science study (including BuyerBench's own results).

4. **Pre-registration as a design feature:** Every replication was pre-registered before data collection. This makes the replication project itself resistant to the p-hacking critique and provides a methodological gold standard that BuyerBench can emulate.

5. **Domain differentiation (cognitive vs. social):** The higher replication rate in cognitive psychology (~50%) vs. social psychology (~25%) supports the hypothesis that effects involving basic cognitive mechanisms are more reproducible than those involving complex social context. Behavioral bias effects in BuyerBench span both domains — the domain stratification from OSC (2015) provides a calibration prior for expected BSI stability.

---

## 3. Limitations

1. **Selection bias in study sample:** The 100 studies were limited to three journals from 2008, which may not be representative of the broader psychological literature. Higher-prestige journals with shorter articles and surprising findings may have *higher* false-positive rates than the field average — meaning OSC's ~36% replication rate may overestimate the crisis severity for applied behavioral economics journals like JEBO and Experimental Economics (which tend to have larger N and pre-specified designs).

2. **Direct replication ≠ conceptual replication:** OSC attempted *direct* replication (same methods, same stimuli). However, many effects are contextually sensitive — a framing effect found in 2008 US students may not replicate in 2015 US students due to intervening cultural shifts, changes in the political environment, or training data in subjects who have since encountered behavioral economics in popular media. This makes the ~36% figure somewhat pessimistic relative to theoretical robustness.

3. **"Powered to the original effect" is a double-edged design:** If the original effect was inflated by p-hacking, being powered to detect the inflated effect may *still* underpowering relative to the true effect. This creates an asymmetry: a replication failure could mean "the effect is zero" OR "the effect is smaller than the original but we weren't powered to detect the true size." OSC (2015) cannot distinguish these cases from effect size alone.

4. **No cost-benefit analysis of replication investment:** The paper does not address whether the effort (270 researchers, years of work) produced commensurate epistemic value relative to alternative designs (e.g., high-powered original studies). This is not a critique of the paper's contribution — but it means the "replication crisis" frame may incentivize direct replication over well-powered original work, which is a misallocation if the latter is more cost-efficient.

5. **Does not directly address computational agent research:** All 100 studies involve human subjects; the replication failure mechanisms (p-hacking, publication bias, researcher degrees of freedom) partially differ for LLM studies. LLM studies face *additional* failure modes (model version drift, training data changes, prompt-wording sensitivity) and at least one *reduced* failure mode (observer effects and demand characteristics are absent).

---

## 4. Relevance to BuyerBench

### The single-shot study problem for LLM behavioral research

The most common design in early LLM behavioral studies (Binz & Schulz 2023, Hagendorff et al. 2023, Aher et al. 2023) is **single-run or very-low-N per condition**: one model, one run, one observation per scenario variant. This design is exactly what OSC (2015) identifies as the primary source of irreproducibility in psychology — underpowered studies whose significant results are drawn from the tail of the sampling distribution and do not represent the population parameter.

For BuyerBench, the parallel is direct. An LLM response at temperature > 0 is a **draw from a probability distribution over the output token space**. A single run is a sample of N=1 from that distribution. If the BSI for a given (model, bias, scenario) cell is computed from N=1 run, the variance of that estimator is unbounded — the "finding" could be any value between 0.0 and 1.0 with equal credibility.

**The effect size shrinkage lesson for BSI calibration:**
OSC (2015) found that original effect sizes average approximately *twice* the replication effect size. Applied to BuyerBench: if a single-run study of an LLM reports a large BSI (e.g., 0.7 for anchoring), the best prior expectation for that BSI under a properly powered N=30 multi-run design would be approximately 0.35 — assuming the OSC shrinkage factor applies. This prior should make BuyerBench conservative about effect size claims from any single-run observation.

### Quantifying the minimum reliable N per cell

**From the OSC (2015) findings, the following design implications follow for BuyerBench:**

| OSC finding | BuyerBench implication |
|---|---|
| ~36% replication rate for single studies | A single-run LLM bias "finding" is unreliable by default |
| Effect sizes shrink ~50% on replication | BSI estimates from N=1 are likely inflated by ~2x; N=30 gives a converging estimate |
| Studies with p < .001 replicate at 47% vs. 28% for p < .05 | Target BSI effect sizes that yield p < .001 across N=30 runs to ensure the finding is not marginal |
| Within-subject designs replicate more reliably | For LLMs, within-cell consistency (temperature variance) is the analogue: low σ within cell = high-replication-probability finding |
| Cognitive effects replicate better than social effects | Anchoring/decoy (more mechanistic) may be more stable across LLM runs than framing/sunk cost (more context-sensitive) |

**Power analysis for N=30 per cell:**
- Assume a true BSI of 0.3 (30% susceptibility rate) in the population of runs for a given (model, bias) cell
- Standard deviation of BSI across runs ≈ √(0.3 × 0.7) / √30 ≈ 0.084 (standard error)
- 95% CI half-width: 1.96 × 0.084 ≈ ±0.16
- A true BSI of 0.3 would be distinguishable from BSI = 0.0 with a one-sample z-test at p < .001 with N = 30, assuming binary susceptibility coding
- A true BSI of 0.1 (10% susceptibility) would require N ≈ 85 runs per cell to achieve p < .05 — important for null-result precision

This analysis motivates the **N=30 per cell floor** in the minimum viable paper specification (strategy-decision-tree.md), and suggests that **N=50 per cell is the "strong" design** for detecting BSI ≥ 0.2 at p < .001 — the level associated with reliable replication under OSC (2015) standards.

### Pre-registration as a BuyerBench methodological commitment

OSC (2015) demonstrates that pre-registration dramatically increases replication rates. All replications that followed a pre-registered protocol replicated at a higher rate than ad hoc replications. For BuyerBench:

1. **Bias type pre-specification:** The five current bias types (anchoring, framing, decoy, sunk cost, scarcity) should be pre-specified before data collection — no adding or dropping bias types based on preliminary results.
2. **Model set pre-specification:** The 10 OpenRouter models should be committed to before running — not selected after seeing which ones show interesting patterns.
3. **BSI threshold pre-specification:** The criterion for "statistically significant bias" (e.g., BSI > 0 at p < .05 after FDR correction across all tests) should be defined in a pre-analysis plan, not post-hoc.
4. **Registered Report option:** Several journals (including those in the BuyerBench cascade — JEBO, Experimental Economics) now accept Registered Reports that guarantee publication conditional on methodological soundness, regardless of results. This is the strongest pre-registration commitment and fully eliminates publication bias — a direct methodological response to OSC (2015).

### The "LLM replication crisis" forecast

Given that OSC (2015) found a ~36% replication rate in psychology, and LLM behavioral research has additional replication risk factors (prompt-wording sensitivity, model version drift, training data contamination), BuyerBench should anticipate that **a substantial fraction of published single-run LLM bias findings will not replicate under multi-run designs with updated models**. This is not merely a methodological concern — it is a strategic opportunity.

**BuyerBench's structural advantage over prior work:**
- Multi-run design with N ≥ 30 per cell makes BSI estimates statistically reliable
- Controlled-variant design (BASELINE vs. bias variant) isolates the manipulation from confounds
- Open benchmark protocol enables systematic replication across model versions and time
- Pre-specified scenarios with locked stimuli prevent prompt-wording drift between studies

This positions BuyerBench not just as a first-mover in procurement bias measurement, but as a methodologically superior alternative to the single-shot studies that dominate the current literature — the same literature that OSC (2015) has shown will largely fail to replicate.

### What BuyerBench's near-zero BSI findings mean in light of OSC (2015)

The dominant finding from existing BuyerBench runs is BSI ≈ 0.0 across most models and most bias types. In light of OSC (2015):

1. **This is the correct finding direction:** Low BSI findings are *harder* to explain away as false positives than high BSI findings. A large-effect claim (BSI = 0.7) is more likely to shrink under replication; a near-zero finding is more likely to be stable.

2. **But null findings require power to be credible:** A null BSI finding from N=1 run is just as uninformative as a positive BSI finding from N=1 run. The N=30 per cell design is needed to establish that BSI is close to zero with tight confidence intervals — not just "we ran it once and it got it right."

3. **The paper's contribution is amplified by null findings:** If BSI ≈ 0.0 across all models and bias types at N=30 per cell, that is a *strong, policy-relevant, and publication-worthy* finding in its own right — "frontier LLMs are not susceptible to classical behavioral biases in structured procurement decisions" is a defensible contribution with direct deployment implications. OSC (2015) establishes that this claim requires adequate power to be credible; BuyerBench's design provides it.

### Design implications checklist

| OSC (2015) lesson | BuyerBench implementation |
|---|---|
| Underpowered studies → false positives | N ≥ 30 runs per (model × bias × variant) cell |
| Effect size inflation → overclaiming | Report BSI with 95% CI, not just point estimates |
| Multiple testing → inflated alpha | Apply FDR correction (Benjamini-Hochberg) across all hypothesis tests |
| Researcher degrees of freedom | Pre-specify primary outcome (BSI) and model set before data collection |
| Publication bias → file drawer | Use Registered Report format or pre-registration at OSF |
| Domain moderates replication rate | Report results separately by bias type; do not aggregate into a single "LLM bias score" |
| Between-lab variance in human studies | Report temperature and model version in all tables; provide full run logs for replication |

---

## 5. Paper Framing Guidance

- **Introduction:** Mention the replication crisis briefly (one sentence) to contextualize why prior single-shot LLM bias studies may not be reliable. Do not dwell — this is not the primary contribution. Cite OSC (2015) as motivation for the multi-run design, not as criticism of prior work by name.

- **Methodology section:** Dedicate a ~100-word paragraph to statistical power and the multi-run design. State: "We follow OSC (2015) and subsequent methodological guidance in ensuring adequate statistical power per condition (N=30 runs per cell, providing 80% power to detect BSI ≥ 0.28 at α = .05, two-tailed). Effect size estimates are reported with 95% confidence intervals computed via bootstrap resampling. All hypothesis tests are corrected for multiple comparisons using the Benjamini-Hochberg false discovery rate procedure across the full battery of [N] tests."

- **Results section:** Every BSI value should appear as `BSI = X.XX [95% CI: X.XX, X.XX]`, not as a bare point estimate. This makes the paper directly comparable to OSC (2015) standards and signals methodological sophistication to behavioral economics reviewers.

- **Limitations section:** Acknowledge that BuyerBench's findings may themselves not replicate across model versions (GPT-4o today ≠ GPT-4o in 6 months), as model updates change the training distribution. Propose systematic re-running as future work, analogous to the multi-lab replication design in OSC (2015). Note that the open benchmark protocol makes this technically feasible at low cost.

- **Discussion:** Frame BuyerBench's methodological design as a direct response to the replication crisis in LLM behavioral research. The combination of (a) pre-specified scenarios, (b) locked stimuli, (c) multi-run N ≥ 30 per cell, (d) pre-registered analysis plan, and (e) open reproducible benchmark constitutes a replication-crisis-aware design that the prior literature does not achieve.

---

## 6. BibTeX Entry

```bibtex
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
```

**Related BibTeX entries:**

```bibtex
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

@article{ioannidis2005most,
  title   = {Why Most Published Research Findings Are False},
  author  = {Ioannidis, John P. A.},
  journal = {PLOS Medicine},
  volume  = {2},
  number  = {8},
  pages   = {e124},
  year    = {2005},
  doi     = {10.1371/journal.pmed.0020124}
}

@article{nosek2018preregistration,
  title   = {The Preregistration Revolution},
  author  = {Nosek, Brian A. and Ebersole, Charles R. and DeHaven, Alexander C. and Mellor, David T.},
  journal = {Proceedings of the National Academy of Sciences},
  volume  = {115},
  number  = {11},
  pages   = {2600--2606},
  year    = {2018},
  doi     = {10.1073/pnas.1708274114}
}
```
