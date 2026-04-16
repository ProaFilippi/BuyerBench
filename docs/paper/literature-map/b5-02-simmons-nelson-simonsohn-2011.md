---
type: reference
title: "B5.02 — False-Positive Psychology: Simmons, Nelson & Simonsohn (2011)"
created: 2026-04-16
tags:
  - false-positives
  - p-hacking
  - researcher-degrees-of-freedom
  - multiple-comparisons
  - pre-registration
  - methodology
  - statistical-power
  - replication-crisis
  - behavioral-bias
  - literature-map
  - pillar2
related:
  - '[[b5-01-open-science-collaboration-2015]]'
  - '[[b5-03-loken-gelman-2017]]'
  - '[[b2-01-incentivized-hypothetical-camerer-hogarth-1999]]'
  - '[[b2-02-repeated-measurement-charness-levin-2005]]'
  - '[[strategy-decision-tree]]'
---

# B5.02 — False-Positive Psychology: Simmons, Nelson & Simonsohn (2011)

**Full citation:** Simmons, J. P., Nelson, L. D., & Simonsohn, U. (2011). False-positive psychology: Undisclosed flexibility in data collection and analysis allows presenting anything as significant. *Psychological Science*, 22(11), 1359–1366. DOI: 10.1177/0956797611417632

**BibTeX key:** `simmons2011false`

---

## 1. Empirical Design

Simmons, Nelson & Simonsohn (2011) is a landmark **methodological demonstration and simulation paper** that quantifies how **undisclosed researcher degrees of freedom** — flexible data collection and analysis practices not reported in the final paper — dramatically inflate the false-positive rate beyond the nominal α = .05 level.

**Core argument:** Researchers routinely make post-hoc decisions about when to stop collecting data, which covariates to include, which conditions to report, and which dependent variables to analyze. None of these decisions are fraudulent in isolation. But their combination, under selective reporting of significant outcomes, converts the nominal 5% Type I error rate into an operational error rate that can exceed 60%.

**Study 1 — Empirical demonstration (N≈20–30 per condition):**
The authors ran two experiments testing whether listening to a children's song ("When I'm 64" by The Beatles) made participants feel older compared to a control song — a manifestly implausible hypothesis. Using standard psychological analysis practices but applying flexible researcher choices (adding covariates, extending data collection when results were marginal, reporting only the significant outcome), they produced a statistically significant result with p < .05 for this absurd prediction. This serves as a *proof-by-construction* that current norms allow confirming false hypotheses.

**Simulation — Quantified inflation table:**
The core quantitative contribution is a simulation study showing how Type I error accumulates under combinations of flexible practices:

| Researcher degrees of freedom exercised | Actual false-positive rate |
|---|---|
| Baseline (none) | 5.0% |
| Optional stopping (check at N=20, extend to N=30) | 7.7% |
| Include one additional DV | 9.5% |
| Include gender as covariate | 11.7% |
| Drop one of three conditions | 12.6% |
| All four practices combined | **60.7%** |

The 60.7% figure is the paper's landmark contribution: the same study, analyzed by a researcher who uses all four practices simultaneously, will produce a false positive at 60× the nominal rate. Since none of these practices are disclosed in the paper, the reader cannot detect the inflation.

**Requirements for disclosure (Table 3):** The paper proposes six specific disclosure requirements that would make false-positive inflation detectable:
1. Report all studied variables
2. Report all run conditions
3. Report the N-determination rule before data collection
4. Report exclusion rules applied
5. Report all covariates tested
6. Report whether the effect holds with/without covariates

These requirements are the precursors to modern pre-registration standards. The paper explicitly calls for journals to mandate these disclosures as a condition of publication — a recommendation subsequently adopted by *Psychological Science* and the APA.

---

## 2. Strengths

1. **Proof-by-construction methodology is rhetorically powerful and scientifically precise:** The Beatles-aging experiment is not a demonstration of a hypothetical problem — it is an actual dataset in which standard practices produce a false significant result. This makes the paper maximally persuasive in a way that simulations alone cannot be. The empirical demonstration answers the "but I would never do that" objection: researchers using these practices need not intend to inflate false positives; standard norms are sufficient.

2. **Quantified inflation table provides actionable calibration:** The simulation's 60.7% composite false-positive rate gives every researcher who reads this paper a concrete number to cite when explaining why reporting requirements matter. Unlike OSC (2015), which documents the *consequences* of the crisis (low replication rates), Simmons et al. (2011) documents the *mechanism*, with a precise causal model. This makes it the stronger methodological citation when explaining *why* p-hacking is a problem rather than merely *that* it occurs.

3. **Six disclosure requirements are immediately implementable:** The practical prescriptions in Table 3 are not aspirational — they are concrete, checkable, and adoptable within existing journal submission systems. This distinguishes the paper from prior critiques (Cohen 1994, Meehl 1978) that identified problems without actionable solutions.

4. **Established the "researcher degrees of freedom" vocabulary:** The paper named and formalized the concept of researcher degrees of freedom, which became the standard terminology for discussing flexible analysis in the post-2011 literature. For BuyerBench, the parallel concept — **analyst degrees of freedom in LLM experiment design** — is a direct extension of this vocabulary.

5. **Publication in *Psychological Science* maximizes impact:** Publishing the methodological critique in the same journal that had published many of the studies being implicitly criticized gave the paper unusual institutional force. A *Psychological Science* paper that says "this journal publishes false positives at 60%" cannot be dismissed as external critique.

---

## 3. Limitations

1. **Focuses on psychology norms specifically:** The four researcher practices (optional stopping, extra DVs, covariate flexibility, condition dropping) are most prevalent in psychology's small-N between-subject lab studies. In behavioral economics and experimental economics (JEBO, Experimental Economics), study designs are typically pre-specified more formally and N is larger — the baseline false-positive rate for JEBO-tier research is likely lower than the 60.7% composite figure. BuyerBench should not claim a "60% false-positive rate in LLM behavioral research" based on this paper.

2. **Simulation assumes independence of degrees-of-freedom choices:** The 60.7% figure compounds four independent practices. In practice, some practices are correlated (researchers who add covariates often also stop early), which may make the actual inflation somewhat lower or higher than 60.7% depending on the correlation structure. The paper acknowledges this is an approximation but does not formally quantify the correlation-adjusted estimate.

3. **Pre-registration is proposed but not empirically validated in this paper:** The disclosure requirements in Table 3 are plausible solutions but were not empirically tested. Whether disclosures alone (without enforcement) reduce false-positive rates is left to subsequent work (Nosek et al. 2018, Registered Report literature). The paper identifies the problem and proposes a solution; the efficacy of the solution is an empirical question not answered here.

4. **Does not address publication bias as a separate mechanism:** Simmons et al. (2011) focuses on *within-researcher* flexibility. But even a researcher who follows the disclosure requirements perfectly contributes to false-positive inflation through *publication bias* — the journal system selects significant results for publication regardless of individual researcher behavior. OSC (2015) shows the combined effect; Simmons et al. (2011) isolates only one mechanism.

5. **Training-data contamination risk for LLM research is not discussed:** The paper predates LLM behavioral research entirely. The specific degrees-of-freedom problems in LLM experiments include choices that Simmons et al. (2011) do not address: model version selection (testing multiple API versions and reporting the one with the largest effect), prompt-wording iteration (testing multiple phrasings and reporting the clearest result), temperature selection (running at multiple temperatures and reporting the setting that supports the hypothesis), and temperature-stratified optional stopping.

---

## 4. Relevance to BuyerBench

### The LLM analyst degrees-of-freedom problem

Simmons et al. (2011)'s "researcher degrees of freedom" framework translates directly into an **analyst degrees of freedom** problem for LLM behavioral experiments. The specific inflating practices in LLM research include:

| Human researcher DOF (Simmons et al.) | LLM analyst analogue | BuyerBench design response |
|---|---|---|
| Optional stopping (check at N=20, extend to N=30) | Run 10 samples, check significance, run 20 more if marginal | Pre-commit to N=30 per cell before running; no mid-batch checks |
| Include extra DVs (test multiple outcomes) | Report BSI, task completion, AND reasoning quality; report whichever shows the effect | Pre-specify **BSI as the primary outcome**; treat task completion as secondary |
| Add covariates | Add model capability tier or instruction-following score as covariate when raw BSI is non-significant | Pre-specify covariates (model family, temperature) in the analysis plan; no post-hoc covariate discovery |
| Drop conditions | Exclude GPT-4o from the anchoring analysis because "it behaved oddly" | Report all pre-specified models regardless of direction of effects; use outlier criteria established before data collection |
| Condition-switching | Report only the ANCHOR_HIGH variant, omitting BASELINE because "the baseline result was confusing" | Report BASELINE and ANCHOR_HIGH jointly; BSI is defined as a within-pair comparison |
| **LLM-specific DOF 1** | Select among multiple tested model API versions and report the one with the largest effect | Lock model versions in the pre-analysis plan (e.g., gpt-4o-2024-08-06); report exact version strings in all tables |
| **LLM-specific DOF 2** | Iterate prompt wording until significance is achieved | Lock scenario prompt text before data collection; any changes require a new pre-registration amendment |
| **LLM-specific DOF 3** | Select temperature parameter to maximize apparent effect (or minimize it for a null-result paper) | Pre-specify temperature = 1.0 for all bias-susceptibility runs; temperature ablation is a separate pre-specified secondary analysis |

The three LLM-specific degrees of freedom (model version selection, prompt iteration, temperature selection) are **not addressed by Simmons et al. (2011)** but follow directly from the same logic. Each provides a researcher with an undisclosed choice point that can shift the false-positive rate in the direction of a desired result.

### Multiple comparison correction as a non-negotiable design requirement

Simmons et al. (2011)'s simulation shows that running just one additional dependent variable inflates Type I error from 5% to 9.5%. BuyerBench's full battery involves:

- 5 bias types × 10 models = **50 primary BSI tests** in the minimum viable design
- 5 bias types × 10 models × 2 (BASELINE + variant) = 100 total condition cells
- 50 + exploratory subgroup comparisons (model family, capability tier) ≈ **60–80 total significance tests**

Under no correction, with α = .05 per test and 80 independent tests, the expected number of false positives is 4.0 — even if every true BSI is exactly zero. This is the direct analogue of Simmons et al.'s multiple-DV problem applied to the BuyerBench battery.

**Required correction:**
Apply **Benjamini-Hochberg False Discovery Rate (FDR) correction** at q = .05 across the full set of pre-specified primary tests (the 50 (model × bias) BSI tests). This controls the expected proportion of false discoveries among all rejected hypotheses at 5%, without requiring the stringent family-wise control of Bonferroni (which would set per-test α ≈ .001 for 50 tests — overly conservative for exploratory behavioral research).

Pre-register the correction method explicitly before data collection. The specific FDR-adjusted p-value threshold will depend on the ordered p-values observed; state this in the pre-analysis plan so it cannot be changed post-hoc.

**Secondary analyses** (reasoning-trace quality, model family comparisons, temperature ablations) should be reported with uncorrected p-values but clearly labeled as exploratory — not subject to the primary FDR correction but not combined with primary tests in the correction calculation.

### Pre-registration implementation checklist for BuyerBench

Following Simmons et al. (2011)'s disclosure requirements, adapted for LLM behavioral research:

1. **Pre-specify all models to be tested** — the full 10-model list; no adding or dropping models after seeing preliminary data
2. **Pre-specify all bias types** — the 5 current bias scenarios; no adding scenarios that happen to show significance
3. **Pre-specify the primary outcome metric** — BSI (proportion of N=30 runs showing bias-susceptible response in the variant vs. baseline) is the primary DV; reasoning trace quality scores are secondary
4. **Pre-specify the N-determination rule** — N=30 per (model × bias × variant) cell, fixed; no optional stopping based on mid-run significance checks
5. **Pre-specify all covariates** — model capability tier and model family are the only pre-specified covariates; no adding covariates that happen to correct non-significant findings
6. **Pre-specify the model version strings** — exact API version identifiers locked before data collection; no mid-study model version switching
7. **Pre-specify prompt text** — scenario prompts locked; any changes constitute a new study requiring a separate pre-registration
8. **Pre-specify the analysis plan** — BH-FDR at q = .05 across primary tests; mixed-effects logistic regression for secondary analysis; bootstrap 95% CIs for all BSI point estimates

For JEBO or Experimental Economics submission, consider submitting as a **Registered Report** — a two-stage submission in which Stage 1 (study design, pre-analysis plan) is reviewed and accepted before data collection, guaranteeing publication of methodologically sound results regardless of direction. This is the strongest possible defense against the Simmons et al. (2011) critique, and several behavioral economics journals (including Experimental Economics since 2022) now support this format.

### Why BuyerBench's near-zero BSI findings are *more* credible than large-effect findings

Simmons et al. (2011)'s analysis implies an asymmetry: **large effects are more suspicious than small effects in under-constrained research designs**, because analyst degrees of freedom consistently inflate rather than deflate effect sizes under selective reporting. The researcher who finds BSI = 0.7 had many ways to arrive at that finding; the researcher who finds BSI ≈ 0.0 had no incentive to keep going.

BuyerBench's current near-zero BSI pattern across most models and bias types is therefore methodologically conservative in the right direction:

- If the true BSI is near zero, Simmons et al. (2011)-style p-hacking would have *increased* apparent effect sizes — so the absence of large effects is inconsistent with systematic p-hacking in the data.
- If the true BSI is near zero and BuyerBench pre-registers and reports that finding at N=30, this constitutes exactly the kind of null-result contribution that Simmons et al. (2011) argues is undervalued (and that PLOS ONE is designed to accept).
- The one exception — LLaMA 3.3 70B showing apparent scarcity bias susceptibility in p2-04 — is precisely where the pre-registration and N=30 design matters most: a single anomalous finding requires replication before it is treated as evidence.

### The "anything as significant" problem applied to LLM prompt sensitivity

The most direct application of Simmons et al. (2011) to LLM research is the **prompt iteration problem**. An LLM researcher who tests 10 phrasings of an anchoring prompt and reports only the one that produces a significant BSI has done something structurally identical to the Beatles-aging experiment: through undisclosed flexibility, they have found a "significant result" for a hypothesis that may be false.

BuyerBench's specific defense is the **locked stimulus design**: scenario prompts are written once, reviewed for domain validity, and locked before the data collection sprint. The procurement domain framing makes arbitrary reformulation implausible in a way that abstract cognitive-task prompts do not. But this defense is only valid if the scenario text is actually locked before running — post-hoc prompt editing to improve BSI scores would directly violate the Simmons et al. (2011) standard.

---

## 5. Paper Framing Guidance

- **Introduction:** Do not cite Simmons et al. (2011) in the introduction. The false-positive psychology problem is background context for *why methodology matters*, not a novel finding of this paper. One brief mention in a footnote (e.g., "We follow Simmons et al. (2011) and pre-register all analyses before data collection") is sufficient.

- **Methodology section:** This is the primary citation context. In the statistical analysis subsection: "To guard against inflated Type I error from multiple comparisons across the 50 primary (model × bias) hypothesis tests, we apply the Benjamini-Hochberg false discovery rate procedure at q = .05 (Simmons et al. 2011; Benjamini & Hochberg 1995). All scenario prompts, model versions, N-per-cell, and analysis procedures are pre-specified in a pre-analysis plan registered at [OSF URL] before data collection." The Simmons et al. citation here signals methodological sophistication to behavioral economics reviewers who are sensitized to p-hacking concerns.

- **Limitations section:** Acknowledge the three LLM-specific degrees of freedom (model version, prompt wording, temperature) that Simmons et al. (2011) does not cover: "While we follow Simmons et al. (2011) pre-registration standards for sample size, outcome specification, and covariate pre-commitment, LLM research faces additional flexibility in model version selection and prompt wording that we address through version locking and scenario text pre-commitment." This demonstrates awareness of the limitation without conceding that the paper is subject to it.

- **Results section:** When reporting FDR-corrected significance, cite Simmons et al. (2011) alongside the Benjamini-Hochberg citation: "After FDR correction for 50 simultaneous tests (Benjamini & Hochberg 1995; following Simmons et al. 2011 multiple comparison guidance), [N] of the 50 (model × bias) cells show statistically significant bias susceptibility at q < .05."

- **Discussion:** Simmons et al. (2011) provides leverage for the "why should we believe null findings" argument. Frame as: "Prior single-shot LLM bias studies (Binz & Schulz 2023; Hagendorff et al. 2023; Jones & Steinhardt 2022) are subject to the analyst degrees-of-freedom concerns quantified by Simmons et al. (2011). BuyerBench's pre-registered, multi-run, FDR-corrected design addresses these concerns; our near-zero BSI findings are therefore substantively informative rather than merely the absence of evidence from an underpowered study."

---

## 6. BibTeX Entry

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
```

**Related BibTeX entries:**

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

@article{benjamini1995controlling,
  title   = {Controlling the False Discovery Rate: A Practical and Powerful Approach to Multiple Testing},
  author  = {Benjamini, Yoav and Hochberg, Yosef},
  journal = {Journal of the Royal Statistical Society: Series B},
  volume  = {57},
  number  = {1},
  pages   = {289--300},
  year    = {1995},
  doi     = {10.1111/j.2517-6161.1995.tb02031.x}
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

@article{cohen1994earth,
  title   = {The Earth Is Round (p < .05)},
  author  = {Cohen, Jacob},
  journal = {American Psychologist},
  volume  = {49},
  number  = {12},
  pages   = {997--1003},
  year    = {1994},
  doi     = {10.1037/0003-066X.49.12.997}
}
```
