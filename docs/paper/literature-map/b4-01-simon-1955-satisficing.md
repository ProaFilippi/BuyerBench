---
type: reference
title: "B4.01 — Bounded Rationality & Satisficing: Simon (1955)"
created: 2026-04-16
tags:
  - bounded-rationality
  - satisficing
  - aspiration-level
  - rationality
  - behavioral-economics
  - literature-map
  - pillar2
  - decision-theory
  - economic-theory
related:
  - '[[b1-01-anchoring-tversky-kahneman-1974]]'
  - '[[b1-02-framing-tversky-kahneman-1981]]'
  - '[[b1-06-status-quo-bias-samuelson-zeckhauser-1988]]'
  - '[[b2-01-incentivized-hypothetical-camerer-hogarth-1999]]'
  - '[[strategy-decision-tree]]'
  - '[[BuyerBench-P2-Gap-Analysis]]'
---

# B4.01 — Bounded Rationality & Satisficing: Simon (1955)

**Full citation:** Simon, H. A. (1955). A behavioral model of rational choice. *Quarterly Journal of Economics*, 69(1), 99–118. DOI: 10.2307/1884852

**BibTeX key:** `simon1955behavioral`

---

## 1. Empirical Design

Simon (1955) is a **theoretical paper**, not an empirical study — there is no participant sample, no experimental manipulation, and no statistical analysis. Its contribution is a **formal critique and replacement** of the classical economic model of rationality (global optimization under perfect information) with a behaviorally realistic alternative grounded in cognitive and informational constraints.

**Core theoretical claim:** Classical economic theory assumes agents (1) possess complete knowledge of all alternatives; (2) hold well-ordered, stable preferences; (3) compute the optimal choice across the entire alternative set. Simon argues that real agents — humans *and*, as he would later extend, any information-processing system — never satisfy these assumptions. Cognitive capacity, time, and information are all bounded. What emerges in practice is **satisficing**: agents search sequentially through alternatives until they find one that exceeds a **satisficing threshold** (aspiration level), then stop. The aspiration level itself adapts: if satisfactory options are found easily, the threshold rises; if no options meet the threshold, it falls.

### The satisficing mechanism

The formal model Simon introduces has four components:

| Component | Definition | Classical alternative |
|---|---|---|
| Aspiration level | A threshold value V* below which alternatives are rejected and above which search stops | Global utility function U(x) to be maximized |
| Sequential search | Alternatives are drawn from a distribution and evaluated in sequence until one exceeds V* | Exhaustive comparison of all alternatives before choosing |
| Adaptive threshold | V* rises after high-quality finds; falls after repeated failures | Fixed preference ordering |
| Stopping rule | Stop at first satisficing alternative — no backtracking to compare with prior finds | Choose global max after full search |

**The key prediction:** In environments with a satisfactory solution near the start of the search sequence, satisficers make a *good enough* choice quickly. In environments where no option clearly exceeds the threshold — such as forced-choice between two imperfect suppliers — the agent faces an aspiration level adjustment problem, not an optimization problem.

Simon's 1955 paper was followed by several extensions:
- **Simon (1956)** "Rational choice and the structure of the environment" — argues that satisficing is *ecologically rational* given the structure of most real environments.
- **March & Simon (1958)** *Organizations* — extended satisficing to organizational decision-making, arguing that firms satisfice on profit rather than maximize.
- **Simon (1979)** Nobel Prize lecture — coined the term "bounded rationality" and summarized the three-decade research program.

### Why this is a rationality *framework*, not a bias

A subtle but important distinction for paper positioning: Simon's bounded rationality is **not** a bias in the Tversky & Kahneman (1974) sense. Biases are systematic deviations from a normative standard that arise from cognitive heuristics even when optimization is computationally feasible. Satisficing, by contrast, is presented as *rational under the actual computational constraints of the agent* — it minimizes total search costs given information acquisition costs. This distinction matters for how BuyerBench's contribution is framed:

- **Tversky-Kahneman biases**: Agents deviate from the optimum even when the optimum is clearly specified and computationally accessible.
- **Simon satisficing**: Agents terminate search before finding the global optimum because full search is too costly.

BuyerBench scenarios test Tversky-Kahneman style deviations (all options are presented simultaneously with full attributes; the optimum is computable from given data), not Simon-style satisficing. This makes the distinction a tool for *sharpening* the BuyerBench contribution claim: our findings are about biases that cannot be explained by computational constraints, because the optimal choice is computationally trivial to identify from the prompt.

---

## 2. Strengths

**Foundational theoretical framework:** Simon (1955) established bounded rationality as a mainstream alternative to neoclassical optimization, eventually earning a Nobel Prize (1978). Its canonical status means a single citation carries enormous theoretical weight.

**Ecologically validated mechanism:** Satisficing has been operationalized across consumer behavior (willingness to accept the first "good enough" apartment), organizational decision-making (budget satisficing in firms), and foraging theory (optimal stopping in animal search) — the mechanism has substantial cross-domain support.

**Aspiration-level dynamics provide a falsifiable prediction for LLM agents:** If LLMs satisfice, we would expect them to select the *first* listed option that meets a threshold rather than the option with the highest computed expected value. This is a testable positional-order effect distinct from anchoring (which requires a high/low anchor manipulation).

**Directly grounds the distinction between economic rationality and behavioral rationality:** The paper formalizes why a benchmark like BuyerBench must specify the *normative standard* before measuring deviations. Without specifying whether the standard is optimization or satisficing, a "bias" finding is uninterpretable.

---

## 3. Limitations

**Pure theory, no human behavioral benchmarks:** Unlike Tversky & Kahneman (1974) or Arkes & Blumer (1985), Simon (1955) provides no direct human choice data for use as BuyerBench BSI comparison baselines. Quantitative human satisficing benchmarks must be sourced from later applied work (e.g., Schwartz et al.'s (2002) maximizers vs. satisficers scale; Iyengar & Lepper's (2000) choice overload studies).

**Seventy-year-old model:** The formal model is pre-computational and pre-cognitive science. Contemporary bounded rationality models (Gigerenzer & Todd, 1999; Gabaix et al., 2006 for rational inattention) are more precise and empirically calibrated. A reviewer from a behavioral economics journal may note that the 1955 version is too coarse to generate falsifiable predictions without additional specification.

**Satisficing vs. optimization cannot be distinguished from single observed choices:** An agent that happens to choose the best option in a set may have done so by satisficing (the best option was presented first and exceeded the aspiration level) or by optimizing. Distinguishing the two mechanisms requires positional manipulation experiments (e.g., varying which option is presented first, holding attributes constant), which current BuyerBench scenarios do not include.

**Mechanism predicts *order effects*, not the specific biases BuyerBench tests:** Anchoring, framing, decoy, and scarcity are not satisficing failures. A satisficing agent may resist framing effects (it just needs a "good enough" choice in any frame) or amplify them (the framed option is selected first because it exceeds the threshold before the superior option is evaluated). The relationship is not straightforward.

---

## 4. BuyerBench Relevance

### Role in the paper: Theoretical grounding for the optimality criterion

Simon (1955) is not cited as a study BuyerBench is positioned *against* (unlike Binz & Schulz, Hagendorff et al., or Echterhoff et al.). Rather, it is cited in the **theory section** to do three jobs:

**Job 1 — Ground the optimality criterion.** BuyerBench computes a BSI by comparing agent choices against a *normative optimal* derived from the scenario's explicit economics. Citing Simon (1955) in the methodology section clarifies why we adopt this standard: we test for deviations from *rational optimization* (the classical standard Simon was critiquing), not from satisficing. This makes the normative benchmark explicit and reviewer-robust.

> *Suggested methodology citation:* "Following the classical rationality standard critiqued by Simon (1955), we define BSI as deviation from the expected-value-maximizing choice under the stated constraints, rather than from a satisficing threshold. This choice is deliberate: BuyerBench scenarios present all alternatives simultaneously with full attribute specification, making computational optimization trivially feasible within a single prompt context. Satisficing explanations — which arise when search costs constrain the agent's information set — do not apply."

**Job 2 — Anticipate the "LLMs don't really optimize" reviewer objection.** A likely reviewer challenge: "Of course LLMs don't maximize expected value — they're not designed to optimize; they're designed to generate plausible text, which may approximate satisficing over the training distribution." Simon (1955) and Simon (1956) are the correct theoretical anchors for this objection. The response: satisficing predicts *order effects* and *threshold dynamics* that are testable independently of bias manipulation. BuyerBench's between-subject controlled-variant design holds option order constant while varying framing/anchors — any BSI difference across variants is attributable to the manipulation, not to satisficing over the presented attribute set.

**Job 3 — Motivate the positional-order control in methodology.** Because satisficing predicts that the first option exceeding the aspiration level is selected, counterbalancing option presentation order across runs (or documenting the fixed order) is a methodological requirement. Any positive-BSI finding could otherwise be confounded by a first-option advantage (the biasing variant happens to position the inferior option first, and the model satisfices on it). **Current BuyerBench scenarios should be audited for consistent option ordering before publication.** If SupplierAlpha is always listed first in the ANCHOR_HIGH variant and second in the BASELINE variant, apparent anchoring effects are partially confounded with a presentation-order/satisficing explanation.

### Satisficing vs. LLM behavior: an empirical prediction

Simon's satisficing model, if applied to LLMs, would predict:
- Models select the *first option listed that exceeds a vague quality threshold derived from training* rather than computing a numerical expected value comparison.
- Under this model, a model that appears "rational" (BSI ≈ 0.0) may simply be satisficing on the objectively superior option because it appears first in the prompt.

**Current BuyerBench data (BSI ≈ 0.0 across 9/10 models) is consistent with satisficing but does not require it.** To rule out satisficing as the mechanism behind the low BSI finding, a positional manipulation study would be needed (randomly rotate which supplier appears first in the numbered list across runs). This is noted as a **methodological limitation** in the paper discussion section.

### Aspiration-level dynamics and status quo bias

Simon's aspiration-level mechanism has a theoretical connection to status quo bias (Samuelson & Zeckhauser, 1988; [[b1-06-status-quo-bias-samuelson-zeckhauser-1988]]): an incumbent supplier who has already "satisficed" in a prior period may serve as an aspiration anchor for the current period, generating apparent status quo preference not from loss aversion but from a satisficing threshold already calibrated to the incumbent's attribute values. This is a candidate theoretical mechanism for the proposed `p2-06-status-quo` scenario — worth noting in the discussion section to distinguish the Samuelson & Zeckhauser loss-aversion account from a Simon satisficing-threshold account.

---

## 5. BibTeX

```bibtex
@article{simon1955behavioral,
  title     = {A behavioral model of rational choice},
  author    = {Simon, Herbert A.},
  journal   = {Quarterly Journal of Economics},
  volume    = {69},
  number    = {1},
  pages     = {99--118},
  year      = {1955},
  doi       = {10.2307/1884852}
}

@article{simon1956rational,
  title     = {Rational choice and the structure of the environment},
  author    = {Simon, Herbert A.},
  journal   = {Psychological Review},
  volume    = {63},
  number    = {2},
  pages     = {129--138},
  year      = {1956},
  doi       = {10.1037/h0042769}
}

@book{march1958organizations,
  title     = {Organizations},
  author    = {March, James G. and Simon, Herbert A.},
  year      = {1958},
  publisher = {Wiley},
  address   = {New York}
}

@article{gigerenzer1999fast,
  title     = {Fast and frugal heuristics: The adaptive toolbox},
  author    = {Gigerenzer, Gerd and Todd, Peter M.},
  journal   = {Simple Heuristics That Make Us Smart},
  pages     = {3--34},
  year      = {1999},
  publisher = {Oxford University Press}
}

@article{schwartz2002maximizing,
  title     = {Maximizing versus satisficing: Happiness is a matter of choice},
  author    = {Schwartz, Barry and Ward, Andrew and Monterosso, John and Lyubomirsky, Sonja and White, Katherine and Lehman, Darrin R.},
  journal   = {Journal of Personality and Social Psychology},
  volume    = {83},
  number    = {5},
  pages     = {1178--1197},
  year      = {2002},
  doi       = {10.1037/0022-3514.83.5.1178}
}
```
