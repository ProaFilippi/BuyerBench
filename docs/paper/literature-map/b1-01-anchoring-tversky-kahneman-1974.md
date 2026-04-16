---
type: reference
title: "B1.01 — Anchoring: Tversky & Kahneman (1974)"
created: 2026-04-15
tags:
  - anchoring
  - behavioral-bias
  - literature-map
  - pillar2
  - heuristics-and-biases
related:
  - '[[b1-02-framing-tversky-kahneman-1981]]'
  - '[[b1-03-decoy-effect-huber-payne-puto-1982]]'
  - '[[b1-04-sunk-cost-arkes-blumer-1985]]'
  - '[[BuyerBench-P2-Gap-Analysis]]'
  - '[[strategy-decision-tree]]'
---

# B1.01 — Anchoring: Tversky & Kahneman (1974)

**Full citation:** Tversky, A., & Kahneman, D. (1974). Judgment under uncertainty: Heuristics and biases. *Science*, 185(4157), 1124–1131. DOI: 10.1126/science.185.4157.1124

**BibTeX key:** `kahneman1974judgment`

---

## 1. Empirical Design

Tversky and Kahneman (1974) introduced anchoring as one of three foundational heuristics in their landmark *Science* paper alongside representativeness and availability. The anchoring demonstration used a wheel-of-fortune paradigm:

1. A wheel rigged to stop at either 10 or 65 was visibly spun in front of participants.
2. Participants were asked to adjust from that anchor to estimate the percentage of African nations in the United Nations.
3. Adjustment from the arbitrary wheel value was systematically insufficient — participants who saw 10 anchored their estimates low (median ~25%) while those who saw 65 anchored high (median ~45%), despite the wheel value being obviously irrelevant.

**N:** Approximately 500 students across multiple experiments reported in the paper.

**Incentive structure:** Hypothetical (no monetary payment for accuracy). Participants were explicitly told the wheel number was random.

**Manipulation strength:** The anchor manipulation was between-subjects: each participant saw either the low anchor (10) or the high anchor (65).

**Effect size:** Pearson r ≈ 0.8 between anchor value and final estimate, one of the largest effect sizes in the heuristics-and-biases literature. The effect persisted even when participants were offered monetary incentives for accuracy in follow-up experiments (Tversky & Kahneman reported this robustness as evidence that anchoring is not mere satisficing but a genuine cognitive phenomenon).

**Additional anchoring demonstrations in the paper:**
- "Product of 8" vs. "product of 1" estimation: 8×7×6×5×4×3×2×1 estimated far higher than 1×2×3×4×5×6×7×8 (median estimates 2,250 vs. 512; true answer 40,320). This shows anchoring on the first number seen in a sequence.
- Probability estimation tasks where starting probability assessments pulled final estimates toward the starting point.

---

## 2. Strengths

1. **Methodological elegance:** The wheel-of-fortune paradigm isolates the anchor effect with maximal clarity — participants cannot rationalize the wheel number as informative, yet it still pulls estimates. This eliminates the alternative explanation that anchors are informative signals.

2. **Large, replicable effect:** r ≈ 0.8 is unusually large for a behavioral manipulation. The effect has been replicated hundreds of times across populations, domains, and methods, including with real-estate appraisers, legal sentencing decisions, clinical diagnoses, and salary negotiations. It is among the most robust findings in behavioral science.

3. **Multiple converging paradigms:** The paper demonstrates anchoring across logically distinct tasks (wheel estimation, multi-digit multiplication, probability elicitation), reducing concern that the effect is paradigm-specific.

4. **Theoretical framing:** Anchoring was placed within a broader cognitive theory (insufficient adjustment from an initial starting value), which generated clear predictions about *when* effects should be larger (when the correct answer is harder to compute) and allowed systematic follow-up work.

5. **Publication venue and citations:** Published in *Science* at N ≈ 500; now one of the most-cited papers in social science (>30,000 citations per Google Scholar). No reviewers or editors have seriously contested the anchoring paradigm itself.

---

## 3. Limitations

1. **Lab setting with student samples:** All experiments used university students in controlled lab conditions, raising standard external validity concerns about generalizability to real procurement professionals or automated agents.

2. **Hypothetical judgments, no consequential stakes:** The Africa percentage estimate has no real-world consequence for participants. While Tversky & Kahneman noted that financial incentives did not eliminate anchoring, the size of the effect under high-stakes, repeated, professional judgment remains disputed (see meta-analytic evidence that incentives reduce but do not eliminate anchoring: Furnham & Boo, 2011).

3. **Single-item measures:** Each participant answered one estimation question. No within-subject variance is available; the entire effect is between-subject, making it impossible to separate individual differences from the manipulation.

4. **US-centric student samples:** All reported studies were conducted with North American (primarily US and Israeli) students. Cross-cultural generalizability is an assumption, not a finding, in the original paper.

5. **Mechanism ambiguity:** The "insufficient adjustment" explanation remained vague in the original paper. Subsequent decades of research identified at least two distinct mechanisms — numeric priming (Chapman & Johnson, 1999) and selective accessibility/confirmatory hypothesis testing (Strack & Mussweiler, 1997) — suggesting the original framing was incomplete. For our purposes, the *outcome* (bias in estimates) is what BuyerBench measures; the mechanism is left for theory-level papers.

6. **No learning or feedback:** Participants received no feedback on their estimates and saw only one trial. Real procurement agents (human or AI) might calibrate against historical performance. BuyerBench's design shares this limitation deliberately (LLMs do not learn across sessions).

---

## 4. Relevance to BuyerBench

### Direct operationalization: Scenario `p2-01-anchoring`

BuyerBench scenario `p2-01` directly operationalizes the anchoring paradigm in a procurement-native context. The controlled manipulation is:

| Variant | Anchor Introduced |
|---|---|
| `BASELINE` | No price history mentioned; five suppliers listed |
| `ANCHOR_HIGH` | "Last quarter's emergency procurement contract was fulfilled at **$91/unit**" embedded in briefing |

The optimal answer is identical across variants: **SupplierB at $42.00** is the lowest-price qualified supplier (SupplierC at $38.00 fails the 5-day lead time constraint; SupplierD at $62.00 lacks ISO 9001). A model anchored on the $91 category spend context would be expected to make one of two errors:

1. **Accept an overpriced supplier** (e.g., SupplierA at $58 or SupplierE at $51) as "reasonable" given the anchor, missing the $42 optimal.
2. **Express hesitation** about SupplierB being "too cheap" relative to the anchored range, potentially adding unneeded caveats in reasoning even if the final selection is correct.

Error type (1) produces a non-zero `bias_susceptibility_index`; error type (2) may be invisible in the current scoring but detectable in reasoning trace analysis.

### Ecological validity improvement over the original paradigm

BuyerBench's anchor is **causally plausible**: a historical emergency-procurement price is a legitimate data point a real buyer might weigh. This is *better* ecological validity than the wheel-of-fortune anchor, but it introduces a theoretical confound — the $91 anchor is *plausibly informative* (it may reflect actual market conditions for that component category), while the wheel number is obviously uninformative. This distinction must be addressed in the paper:

> "Unlike the arbitrary numerical anchors used in laboratory demonstrations (Tversky & Kahneman, 1974), BuyerBench's anchors are *ecologically plausible* — a prior contract price is a legitimate data signal in real procurement settings. This raises the ecological validity of our operationalization but requires us to establish, via the baseline variant, that the historical price is normatively irrelevant to the optimal current-period decision. The optimal choice is identical across variants; any shift toward higher-priced suppliers in the ANCHOR_HIGH variant must be attributed to non-normative anchoring rather than legitimate Bayesian updating."

### Human benchmark effect sizes for comparison

For paper positioning, the relevant comparison benchmarks from the human literature are:

| Study | Domain | Effect size |
|---|---|---|
| Tversky & Kahneman (1974) | Abstract estimation | r ≈ 0.80 |
| Northcraft & Neale (1987) | Real estate appraisal | High anchor +$13K vs. low anchor, appraisers and students both anchored |
| Chapman & Johnson (1999) | Meta-analysis | d ≈ 0.50–0.70 across domains |
| Ariely et al. (2003) | Willingness-to-pay | First written SSN digit predicted bids, r ≈ 0.40 |

BuyerBench's BSI for the anchoring scenario measures a binary outcome (correct supplier selected vs. not). Cross-model BSI values should be compared to a calibrated human benchmark rate (from the literature, most human subjects in analogous tasks show anchoring on ~60–75% of trials under high anchors).

### Stochasticity note

The original T&K study used single-shot between-subjects measurement. In BuyerBench, each (model × variant) cell runs N ≥ 30 times at temperature > 0. This enables:

1. **Stochastic bias rate estimation** rather than deterministic pass/fail.
2. **Intra-model variance decomposition**: how much of the apparent bias is stable vs. sampling noise?
3. **Inter-model comparison**: does capability (MMLU score, benchmark rank) predict anchoring susceptibility?

This methodological improvement directly addresses the major limitation of single-run LLM bias studies (Jones & Steinhardt, 2022; Binz & Schulz, 2023).

---

## 5. Paper Framing Guidance

When citing this paper in the BuyerBench manuscript:

- **Introduction/motivation:** Use T&K (1974) as the canonical anchoring reference and establish that this effect is among the most robustly documented in behavioral science — motivating *why* we test for it in LLMs.
- **Related work:** Position relative to Echterhoff et al. (2024) and Hagendorff et al. (2023) by noting that prior LLM anchoring tests used abstract lab-style prompts; BuyerBench uses a procurement domain with computable ground-truth optimals.
- **Methodology:** Cite as the theoretical basis for the controlled-variant design (baseline vs. ANCHOR_HIGH), noting that BuyerBench preserves the between-subjects manipulation logic to avoid demand effects (a within-subjects design would let the model infer the experimental hypothesis).
- **Results:** If models show non-trivial BSI on anchoring, compare effect magnitudes to human benchmarks (d ≈ 0.5–0.7 from meta-analyses). If BSI ≈ 0 across models, that is itself a finding (LLMs may be less susceptible to numerical anchoring than humans — an interesting null result worth reporting in PLOS ONE or JDM).

---

## 6. BibTeX Entry (Confirmed in `references.bib`)

```bibtex
@article{kahneman1974judgment,
  title   = {Judgment under Uncertainty: Heuristics and Biases},
  author  = {Tversky, Amos and Kahneman, Daniel},
  journal = {Science},
  volume  = {185},
  number  = {4157},
  pages   = {1124--1131},
  year    = {1974},
  doi     = {10.1126/science.185.4157.1124}
}
```
