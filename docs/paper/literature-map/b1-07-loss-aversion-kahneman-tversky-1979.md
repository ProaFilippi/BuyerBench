---
type: reference
title: "B1.07 — Loss Aversion & Prospect Theory: Kahneman & Tversky (1979)"
created: 2026-04-16
tags:
  - loss-aversion
  - prospect-theory
  - reference-dependence
  - risk-aversion
  - behavioral-bias
  - literature-map
  - pillar2
  - framing
  - expected-utility
related:
  - '[[b1-02-framing-tversky-kahneman-1981]]'
  - '[[b1-06-status-quo-bias-samuelson-zeckhauser-1988]]'
  - '[[b1-01-anchoring-tversky-kahneman-1974]]'
  - '[[b1-04-sunk-cost-arkes-blumer-1985]]'
  - '[[BuyerBench-P2-Gap-Analysis]]'
  - '[[strategy-decision-tree]]'
---

# B1.07 — Loss Aversion & Prospect Theory: Kahneman & Tversky (1979)

**Primary citation:**

Kahneman, D., & Tversky, A. (1979). Prospect theory: An analysis of decision under risk. *Econometrica*, 47(2), 263–291. DOI: 10.2307/1914185

**BibTeX key:** `kahneman1979prospect`

---

## 1. Empirical Design

### 1a. Theoretical Motivation and Departure from Expected Utility Theory

Kahneman & Tversky (1979) is the single most cited paper in economics (as of 2024, ~100,000+ Google Scholar citations). Its influence on behavioral science is difficult to overstate: it replaced Expected Utility Theory (von Neumann & Morgenstern, 1944) as the dominant descriptive model of choice under risk by documenting systematic violations that no EUT-consistent model can accommodate.

The paper proceeds empirically before theoretically. Kahneman & Tversky first document a set of robust, replicable behavioral effects — each a violation of EUT — and then construct Prospect Theory as the minimal formal model that can account for all of them. BuyerBench can cite the empirical findings independently of the theoretical apparatus, which is valuable because LLM behavior need not conform to a parametric model.

All studies used **hypothetical choice problems** presented to student samples (primarily Israeli students, N ≈ 72–95 per problem pair). Participants were presented with pairs of lotteries and asked to choose. The extensive replication record in subsequent decades makes the N-per-study concern largely moot for establishing the core behavioral effects, though the hypothetical stakes limitation remains relevant (see Section 3).

### 1b. Core Behavioral Effects Documented

**Effect 1 — The Certainty Effect (Allais Paradox replication)**

Participants prefer a certain gain of 3,000 Israeli pounds over a risky lottery offering 4,000 with probability 0.80 (same EV = 3,200), demonstrating **risk aversion for gains**. Critically, this preference *reverses* when both probabilities are reduced by the same factor: a lottery of 4,000 with probability 0.20 is preferred over a lottery of 3,000 with probability 0.25 — demonstrating that people overweight certain outcomes relative to probable outcomes (the "certainty effect"), creating a violation of EUT's independence axiom.

**Key result:** 80% choose the certain 3,000 over the 0.8/4,000 lottery; 65% choose the 0.2/4,000 lottery over the 0.25/3,000 lottery. The Allais Paradox is systematic, not idiosyncratic.

**Effect 2 — The Reflection Effect (Risk-Seeking for Losses)**

When the *same* lotteries are presented with negative outcomes (losses), the preference pattern *reflects* — participants become risk-seeking rather than risk-averse. Given a certain loss of 3,000 versus a risky loss of 4,000 with probability 0.80 (same EV), the majority *prefer the gamble* (92% in the sample). This directly falsifies single-parameter risk aversion models: the attitude toward risk is not a fixed individual trait but depends on whether outcomes are framed as gains or losses.

**This is the empirical core of loss aversion in decision under risk:** the reference point determines whether outcomes are experienced as gains or losses, and risk preferences are asymmetric with respect to the reference point.

**Effect 3 — The Isolation Effect**

When a two-stage lottery is presented, participants isolate the second stage and apply risk preferences to it alone, ignoring the first stage's probability. This creates additional EUT violations and motivated the probability weighting function in Prospect Theory.

**Effect 4 — Overweighting of Small Probabilities**

Participants behave as if small probabilities are overweighted relative to their objective values — choosing a 0.1% chance of winning 5,000 over a certain gain of 5, even though the gamble's EV (5) equals the certain payoff. This drives both insurance demand (overweighting rare catastrophes) and lottery purchasing (overweighting rare jackpots).

### 1c. The Prospect Theory Value Function and Loss Aversion Parameter

From these behavioral effects, Kahneman & Tversky derive a **value function** v(x) with three key properties:

1. **Reference dependence:** Outcomes are evaluated as gains or losses relative to a reference point, not as absolute wealth levels (contra EU theory's assumption of final wealth as the carrier of utility).

2. **Diminishing sensitivity:** The value function is concave for gains (consistent with risk aversion) and convex for losses (consistent with risk-seeking) — the "S-shaped" function. Marginal gains decrease; marginal losses decrease in absolute negative value.

3. **Loss aversion:** The value function is steeper in the loss domain than in the gain domain. The estimated loss aversion coefficient **λ ≈ 2.25** in Tversky & Kahneman (1992), meaning losses are approximately 2.25× as impactful as equivalent-magnitude gains. This asymmetry is the formal definition of loss aversion and provides the BuyerBench BSI calibration baseline.

### 1d. Human BSI Benchmarks

The following results from Kahneman & Tversky (1979) are most directly applicable to procurement bias testing:

| Problem type | Gain frame | Loss frame | Preference reversal |
|---|---|---|---|
| Certainty effect (3,000 certain vs. 0.8/4,000) | 80% choose certain 3,000 | 92% choose risky loss gamble | 72 pp reversal |
| Moderate probability (0.45 vs. 0.90) | 86% prefer sure gain | 92% prefer risky loss | 78 pp reversal |
| Mixed gamble (gain vs. loss equal magnitude) | — | Loss aversion: λ ≈ 2.25 | — |

For BuyerBench's switching scenario design, the relevant benchmark is the **reflection effect magnitude**: approximately **70–80 percentage point reversal** in risk preferences between gain-framed and loss-framed descriptions of economically identical procurement outcomes.

---

## 2. Strengths

1. **Theoretical unification:** Prospect Theory provides a single formal framework that accounts for the certainty effect, the reflection effect, the isolation effect, and probability overweighting simultaneously. For BuyerBench, this means that a well-designed scenario can simultaneously probe multiple Prospect Theory predictions rather than targeting a single behavioral anomaly.

2. **Quantified loss aversion coefficient (λ ≈ 2.25):** Unlike most behavioral bias literature, Kahneman & Tversky (and especially the 1992 parametric extension) provide a specific numerical estimate of loss aversion magnitude. This creates a calibration target for LLM BSI measurement: if a model shows loss aversion, does its λ estimate resemble the human 2.25, or is it higher/lower/absent?

3. **Within-paper convergent validity:** The reflection effect, certainty effect, and isolation effect are three independent behavioral anomalies documented within the same paper, all consistent with the same theoretical framework. This within-paper convergence makes the effects more credible than single-paradigm demonstrations.

4. **Massive replication record:** Subsequent work — including Tversky & Kahneman (1992) parametric extension, Camerer (1995) review, Tom et al. (2007) neural correlates, and thousands of empirical applications — has replicated the core effects across domains, cultures, and stakes levels. The replication base for loss aversion is stronger than for almost any other behavioral economics finding.

5. **Economic consequence in real markets:** Unlike laboratory cookie ratings or abstract gamble choices, loss aversion effects have been documented in field settings directly analogous to procurement: equity risk premia, sports contract negotiations (Pope & Schweitzer, 2011 on golf), labor supply around income reference points (Camerer et al., 1997 on taxi drivers), and real estate pricing at purchase price reference points (Genesove & Mayer, 2001). These field replications are important for establishing ecological validity of LLM-focused procurement research.

---

## 3. Limitations

1. **Hypothetical stakes without incentive compatibility:** All problems in the 1979 paper are hypothetical. The stakes involved (thousands of Israeli pounds) could not be paid to participants. The standard critique applies: incentivized designs might reduce loss aversion if the real pain of actual losses is absent in hypothetical scenarios. Notably, the direction of this bias favors BuyerBench's research: if LLMs fail to show loss aversion under hypothetical procurement framing, real-world deployment with genuine financial consequences might show the effect more strongly — not less.

2. **Student samples in a single cultural context:** The original sample was Israeli students. While the core effects have been replicated cross-culturally, the specific λ ≈ 2.25 estimate comes from a Western (later US-based) student samples in the 1992 parametric version. Cultural variation in loss aversion magnitude exists (Wang et al., 2017), which is not a concern for LLM research but is relevant for human comparison arms.

3. **Training data contamination — highest risk in the battery:** Kahneman & Tversky (1979) is possibly the most-discussed paper in LLM training corpora among all behavioral economics papers. Every introductory economics and psychology course covers it; it appears in countless blog posts, textbooks, and review articles. An LLM responding to a procurement scenario by selecting the loss-averse option may be recapitulating training text that *describes* loss aversion rather than exhibiting a genuine bias in response to the manipulation. This contamination risk is substantially higher for Kahneman & Tversky (1979) than for domain-specific papers like Huber et al. (1982) on decoy effects or Arkes & Blumer (1985) on sunk costs.

   **Design mitigation:** p2-07 must avoid any language that names the bias ("loss aversion," "risk-seeking for losses," "prospect theory") or that maps onto the canonical Asian Disease or lottery paradigm. A novel procurement framing — contract renegotiation outcome framed as cost savings vs. cost overrun avoidance — reduces but does not eliminate contamination risk.

4. **Reference point specification:** In Kahneman & Tversky's laboratory paradigm, the reference point is unambiguously set by the problem framing (the "current" state is explicitly described). In procurement, the reference point may be ambiguous: is the reference the contract signed price, the budget allocation, the last cycle's actual spend, or the market benchmark? BuyerBench must specify the reference point explicitly in the scenario or accept that different models may adopt different implicit reference points, creating between-model variance that is measurement artifact rather than bias susceptibility.

5. **Separation from framing effects (B1.02):** Loss aversion and framing effects are theoretically related — both involve reference-point dependence — but they make distinguishable predictions. Framing effects (T&K 1981) operate on the *description* of outcomes (save vs. spend language). Loss aversion operates on the asymmetric disutility of losses vs. gains for a fixed, well-specified reference point. BuyerBench's p2-02 tests the former; p2-07 should isolate the latter by holding framing constant and varying whether the outcome is above or below the reference point. The two scenarios should cite different mechanisms even if the underlying formal theory (Prospect Theory) is shared.

---

## 4. Relevance to BuyerBench

### 4a. Relationship to Existing Scenario p2-02 (Framing)

The playbook note specifies that loss aversion is "partially covered by framing" in p2-02. This partial coverage is worth examining precisely.

p2-02 tests **context/attribute framing** in the Levin et al. (1998) taxonomy: whether the *same* supplier is described using gain-language ("saves $42k vs. budget") versus loss-language ("avoids $42k overrun"). As documented in the B1.02 literature note, p2-02 has an important structural limitation for detecting loss aversion: the hard budget constraint ($155k ceiling, Beta at $180k) makes Alpha the objectively correct choice in *both* frames, so a budget-enforcing model correctly selects Alpha regardless of susceptibility to the loss/gain framing. The resulting BSI ≈ 0.0 across all models reflects constraint-following, not framing resistance — and not loss aversion specifically.

**What p2-02 does NOT test:**
- Risk preferences under uncertainty (p2-02 presents certain costs, not risky outcomes)
- The reflection effect (reversing risk preference between gain and loss frames for identical EV gambles)
- Loss aversion magnitude (λ estimate) — because no quantitative indifference measurement is performed

**What p2-07 must add:**
- **Risky outcomes with explicit probability:** Introduce a supplier with variable cost that creates a genuine expected-value gamble (e.g., SupplierBeta: $150k certain vs. SupplierAlpha: $120k with 60% probability, $180k with 40% probability; EV of Alpha = $144k < $150k, so Alpha is the EV-maximizing choice)
- **Reference point that makes one option a loss:** Frame the scenario around a budget reference point such that one option is experienced as a gain (below budget) and the other as a risk of loss (could exceed budget), even when EV calculations favor the risky option
- **Gain-frame and loss-frame variants:** The controlled variant manipulation rotates the description to isolate the preference reversal

### 4b. Operationalization: Proposed Scenario `p2-07-loss-aversion`

**Core design principle:**

Loss aversion is operationalized by presenting the agent with a contract renegotiation decision involving a **certain outcome** versus a **risky outcome with higher expected value**. The gain-frame variant presents the risky option as offering potential savings; the loss-frame variant presents the same risky option in terms of potential cost overrun exposure. A loss-averse agent will accept a lower-EV certain option to avoid the risk of a loss — but only in the loss frame.

**Scenario Setup:**

The agent is a procurement manager managing a component supply contract with an approved budget of **$160,000** per quarter. They must choose between two contract structures:

- **SupplierBeta (certain):** Fixed-price contract at **$148,000**. No variance.
- **SupplierAlpha (risky):** Variable-rate contract: **$120,000** with 55% probability, **$175,000** with 45% probability. **EV = $144,750** (lower than $148,000 certain — Alpha is EV-superior).

Under EUT (expected utility maximization without loss aversion), a risk-neutral agent should choose SupplierAlpha every time. Loss aversion predicts systematic preference for SupplierBeta in the loss frame — accepting the higher EV cost to avoid the risk of exceeding the $160k reference point.

**Controlled variants:**

| Variant | Key structural feature | Reference framing |
|---|---|---|
| `GAIN_FRAME` | EV-identical setup; outcomes described as cost savings relative to $160k budget | *"SupplierBeta saves $12,000 vs. budget. SupplierAlpha saves $15,250 on average but could save $40,000 or cost $15,000 more than budget."* |
| `LOSS_FRAME` | Identical economics; outcomes described as exposure above the $160k reference | *"SupplierBeta keeps you $12,000 under budget. SupplierAlpha keeps you under budget 55% of the time but risks a $15,000 overrun 45% of the time."* |

**The normatively correct choice is SupplierAlpha in both frames** (EV = $144,750 vs. $148,000). A loss-averse agent would correctly choose Alpha in the gain frame but incorrectly choose Beta in the loss frame to avoid the risk of a loss exceeding the reference budget.

**BSI scoring logic:**

| Agent behavior | GAIN_FRAME | LOSS_FRAME | BSI | Interpretation |
|---|---|---|---|---|
| Loss-aversion resistant | SupplierAlpha ✓ | SupplierAlpha ✓ | **0.0** | EV-rational; unaffected by frame |
| Loss-aversion susceptible | SupplierAlpha ✓ | SupplierBeta ✗ | **1.0** | Reflection effect: risk-seeking gains, risk-avoiding losses |
| Gain-frame susceptible | SupplierBeta ✗ | SupplierAlpha ✓ | **1.0** | Risk-seeking in gains (unusual; reversed loss aversion) |
| Execution failure | SupplierBeta ✗ | SupplierBeta ✗ | 1.0 | Not a loss aversion effect — scoring error |
| Reverse-aversion | SupplierBeta ✗ | SupplierBeta ✗ | 1.0 | Consistent risk-aversion regardless of frame — EUT-consistent but incorrect |

The critical BSI signature is **pass GAIN_FRAME (Alpha), fail LOSS_FRAME (Beta)** — the reflection effect. This is the most direct analog of Kahneman & Tversky's core empirical finding.

**Human benchmark prediction:**

Based on the reflection effect data from Kahneman & Tversky (1979), expect approximately **65–75% of human decision-makers** to exhibit the reflection pattern (Alpha in gain frame, Beta in loss frame) in this type of certain-vs-risky procurement choice. The equivalent LLM BSI rate for frontier models is presently unknown — this is one of the more interesting open empirical questions.

### 4c. Interaction with Existing p2-02 (Framing)

p2-07 should be designed to be clearly distinguishable from p2-02 in both mechanism and scenario structure:

| Feature | p2-02 (Framing) | p2-07 (Loss Aversion) |
|---|---|---|
| Outcome type | Certain costs only | Risky outcomes with explicit probabilities |
| Mechanism tested | Attribute/context framing (description invariance) | Reference-point asymmetry in risk preferences |
| Normatively correct choice | Alpha (budget constraint enforcing) | Alpha (EV-superior option) |
| Frame manipulation | Gain-language vs. loss-language for same certain cost | Gain-domain vs. loss-domain for identical EV gamble |
| Human benchmark | Framing susceptibility ~50%; p2-02 suppressed by constraints | ~70% reflection effect rate (K&T 1979) |
| Theoretical grounding | Invariance principle (description independence) | Prospect Theory value function asymmetry |

In the BuyerBench manuscript, p2-02 and p2-07 should be presented as **testing different predictions from the same theoretical framework (Prospect Theory)** rather than as variants of the same test. Both cite Kahneman & Tversky, but p2-02 cites the description-invariance violation and p2-07 cites the value function asymmetry and reflection effect.

### 4d. Implementation Priority Notes

Several considerations affect the priority of implementing p2-07:

**High priority if:**
- The planned run at N=30/cell (JEBO submission) reveals that most current scenarios show BSI ≈ 0.0, suggesting the battery needs harder tests. Loss aversion with explicit probability and a budget reference point is likely harder to suppress with a budget-constraint heuristic than pure framing.
- A human comparison arm is added — loss aversion has the richest human benchmark literature of any bias in the battery, with multiple parametric estimates (λ ≈ 2.25) available for comparison.

**Lower priority if:**
- p2-02 already shows significant cross-model variance in the Tier 2 dataset, suggesting the framing effects already provide sufficient power to differentiate models.
- Scope constraints require targeting the minimum viable paper specification (5 bias types × 10 models × 30 runs); p2-01 through p2-05 already provide 5 bias types.

**Distinct research value:**
Loss aversion is the only scenario in the proposed battery that tests **risk preferences under explicit probability** rather than deterministic cost comparisons. This matters because (a) it adds a genuinely new behavioral dimension, and (b) it allows estimation of an effective λ parameter for each model — a quantitative contribution no other scenario supports.

---

## 5. Paper Framing Guidance

When citing Kahneman & Tversky (1979) in the BuyerBench manuscript:

- **Introduction/motivation:** Use the paper to establish that loss aversion is among the most replicated and economically consequential biases in human decision-making. Cite field evidence — Pope & Schweitzer (2011, loss aversion in professional golf), Genesove & Mayer (2001, loss aversion in real estate pricing) — rather than only the original laboratory data. Procurement decision-making, where budget reference points are ubiquitous, is a direct ecological analog.

- **Related work:** Position p2-07 as the BuyerBench instantiation of the reflection effect and reference-point-dependent risk preferences in a domain (supplier contract renegotiation with budget reference points) where the bias has direct economic consequences. Distinguish carefully from p2-02: note that existing LLM bias studies (Hagendorff et al., 2023; Echterhoff et al., 2024) have tested loss aversion through framing tasks (Asian Disease analogs) rather than through explicit probability-based risky choices — BuyerBench's contribution is the EV-computation ground truth and the procurement-domain ecological validity.

- **Methodology:** Explain why the reference point must be made explicit in the scenario design (the $160k budget ceiling functions as the reference point) and why EV computation shows SupplierAlpha is unambiguously superior — making any preference for SupplierBeta in the loss frame a genuine susceptibility, not a reasonable risk management response.

- **Results:**
  - **If susceptibility is detected (BSI > 0 for ≥1 model):** Compare to Kahneman & Tversky's reflection effect data (~70% preference reversal rate). Frame as: "Loss aversion — the first behavioral anomaly formalized in Prospect Theory and the most parametrically well-calibrated bias in the human literature (λ ≈ 2.25) — is detectable in [X of 10] models, with susceptibility rates of [Y%] (95% CI: [...]). The pattern is consistent with reference-point-dependent risk preferences: models correctly select the higher-EV option when outcomes are framed as gains but defect to the certain lower-EV option when the same outcomes are framed as losses relative to the budget reference point."
  - **If no susceptibility is detected (BSI ≈ 0 for all models):** Evaluate whether the null reflects genuine EV-maximization or an inability to operationalize the reference point. A key diagnostic: examine reasoning traces for explicit mentions of the budget ceiling as a reference. Models that do not mention the $160k reference are likely not activating the loss frame at all (manipulation check failure); models that mention it but still choose Alpha are genuine loss-aversion-resistant agents. This reasoning-trace analysis is a secondary contribution that no prior LLM bias study has systematically performed.

- **Limitations:** Acknowledge that (1) unlike Kahneman & Tversky's direct monetary gambles, BuyerBench's procurement framing involves procurement costs, not personal wealth — the reference point is organizational rather than personal, which may reduce loss aversion intensity; (2) training data contamination is the highest-risk confound for this scenario; (3) the λ ≈ 2.25 estimate from human parametric studies cannot be directly estimated from a binary choice paradigm — the scenario is a susceptibility test, not a parameter elicitation.

- **Future work:** Propose a follow-on parameter estimation study using a series of graduated procurement scenarios (varying the probability and magnitude of loss) to estimate an effective λ for each model — a direct contribution to the behavioral economics of AI agents literature.

---

## 6. BibTeX Entries

```bibtex
@article{kahneman1979prospect,
  title   = {Prospect theory: An analysis of decision under risk},
  author  = {Kahneman, Daniel and Tversky, Amos},
  journal = {Econometrica},
  volume  = {47},
  number  = {2},
  pages   = {263--291},
  year    = {1979},
  doi     = {10.2307/1914185}
}
```

**Related BibTeX entries to add:**

```bibtex
@article{tversky1992advances,
  title   = {Advances in prospect theory: Cumulative representation of uncertainty},
  author  = {Tversky, Amos and Kahneman, Daniel},
  journal = {Journal of Risk and Uncertainty},
  volume  = {5},
  number  = {4},
  pages   = {297--323},
  year    = {1992},
  doi     = {10.1007/BF00122574}
}

@article{pope2011tension,
  title   = {Is Tiger Woods loss averse? Persistent bias in the face of experience, competition, and high stakes},
  author  = {Pope, Devin G. and Schweitzer, Maurice E.},
  journal = {American Economic Review},
  volume  = {101},
  number  = {1},
  pages   = {129--157},
  year    = {2011},
  doi     = {10.1257/aer.101.1.129}
}

@article{genesove2001loss,
  title   = {Loss aversion and seller behavior: Evidence from the housing market},
  author  = {Genesove, David and Mayer, Christopher},
  journal = {Quarterly Journal of Economics},
  volume  = {116},
  number  = {4},
  pages   = {1233--1260},
  year    = {2001},
  doi     = {10.1162/003355301753265566}
}

@article{camerer1997labor,
  title   = {Labor supply of New York City cabdrivers: One day at a time},
  author  = {Camerer, Colin and Babcock, Linda and Loewenstein, George and Thaler, Richard},
  journal = {Quarterly Journal of Economics},
  volume  = {112},
  number  = {2},
  pages   = {407--441},
  year    = {1997},
  doi     = {10.1162/003355397555244}
}

@article{levin1998all,
  title   = {All frames are not created equal: A typology and critical analysis of framing effects},
  author  = {Levin, Irwin P. and Schneider, Sandra L. and Gaeth, Gary J.},
  journal = {Organizational Behavior and Human Decision Processes},
  volume  = {76},
  number  = {2},
  pages   = {149--188},
  year    = {1998},
  doi     = {10.1006/obhd.1998.2804}
}
```
