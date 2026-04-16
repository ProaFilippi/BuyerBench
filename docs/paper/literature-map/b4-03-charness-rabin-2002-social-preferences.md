---
type: reference
title: "B4.03 — Social Preferences & Rationality Boundaries: Charness & Rabin (2002)"
created: 2026-04-16
tags:
  - social-preferences
  - rationality
  - fairness
  - reciprocity
  - inequality-aversion
  - behavioral-economics
  - literature-map
  - pillar2
  - decision-theory
  - experimental-economics
related:
  - '[[b4-01-simon-1955-satisficing]]'
  - '[[b4-02-nudge-thaler-sunstein-2008]]'
  - '[[b2-01-incentivized-hypothetical-camerer-hogarth-1999]]'
  - '[[b1-07-loss-aversion-kahneman-tversky-1979]]'
  - '[[b1-06-status-quo-bias-samuelson-zeckhauser-1988]]'
  - '[[BuyerBench-P2-Gap-Analysis]]'
---

# B4.03 — Social Preferences & Rationality Boundaries: Charness & Rabin (2002)

**Full citation:** Charness, G., & Rabin, M. (2002). Understanding social preferences with simple tests. *Quarterly Journal of Economics*, 117(3), 817–869. DOI: 10.1162/003355302760193904

**BibTeX key:** `charness2002social`

---

## 1. Empirical Design

Charness & Rabin (2002) is a **combined theoretical and experimental paper** that uses a battery of two-player dictator-style games to test competing models of social preferences. The core methodological innovation is the use of simple "spectator" and "two-player" binary-choice games that cleanly isolate specific parameters of social utility — distributional preferences, reciprocity, and efficiency-seeking — rather than conflating them as in the Ultimatum Game.

### The core theoretical question

Prior social preference models — Fehr & Schmidt (1999) inequality aversion and Bolton & Ockenfels (2000) ERC — predict that agents dislike *any* inequality (whether they are above or below the mean). Charness & Rabin challenge this with a richer model: the **quasi-maximin** specification, in which agents weight the *worst-off* person's payoff, the *total* payoff (efficiency), and their own payoff:

> U_i(π_1, π_2) = (1 − λ) · π_i + λ · [δ · min(π_1, π_2) + (1 − δ) · Σπ_j]

where λ controls concern for others, δ controls maximin-versus-efficiency orientation. The key prediction: subjects *help* the worse-off party and *sacrifice efficiency* for equity, but only when no negative reciprocity is triggered.

### Experimental design

**Subjects:** N ≈ 1,100 student participants across 29 two-player games conducted at UC Berkeley and UC Santa Barbara. Incentive-compatible (real money payments, no deception).

**Game structure:** Binary-choice dictator games where one player (the "mover") chooses between two allocations, (x₁, x₂), that vary the mover's own payoff, the recipient's payoff, and total surplus:

| Game type | What it isolates |
|---|---|
| Competitive decomposition | Own-payoff maximization vs. inequality aversion |
| Efficiency-sacrifice games | Willingness to accept lower total surplus to reduce inequality |
| Reciprocity games | Behavior after observing a generous vs. hostile action by the partner |
| Spectator games | Third-party preferences without stake in outcome |

**Key empirical findings:**

1. **Inequality aversion is asymmetric:** Subjects readily sacrifice their own payoffs to *help* a worse-off partner (advantageous-to-disadvantageous transfers), but do *not* sacrifice much to punish a better-off partner (disadvantageous inequality aversion is weaker than Fehr & Schmidt predict).

2. **Efficiency matters, not just equity:** When helping the worst-off agent requires destroying total surplus, many subjects weight efficiency heavily. Fehr & Schmidt's model predicts sacrifices to reduce inequality even when costly; the data show subjects often decline.

3. **Reciprocity modulates social preferences:** After a generous action, ~40–60% of subjects select the fair/helpful allocation. After a hostile or selfish action, the same percentage shifts to purely self-interested or punitive choices. Reciprocity is a *multiplier* on social preferences, not an independent motive.

4. **Quasi-maximin fits better than alternatives:** Structural estimation of λ and δ parameters across the game battery shows the quasi-maximin model has substantially lower prediction error than either pure self-interest (λ=0), Fehr & Schmidt, or pure altruism (λ=1, δ=0).

**Quantitative anchors for BuyerBench BSI calibration:**
- Efficiency sacrifice: ~25–35% of subjects choose the equitable allocation even when it reduces total payoff by 20–30%.
- Reciprocity shift: ~40–60% switch from equitable to self-interested (or punitive) after hostile partner action.
- These represent the "social preferences baseline" against which LLM behavior should be compared when framing issues as fairness rather than pure EV maximization.

---

## 2. Strengths

**Large-N, incentive-compatible, multi-game design:** Unlike most behavioral economics vignette studies (Arkes & Blumer, Samuelson & Zeckhauser), Charness & Rabin use real monetary stakes across 29 games. The within-paper replication across game variants (spectator, two-player, reciprocity) converges on a stable quantitative estimate of λ ≈ 0.4–0.6 (moderate other-regarding concern). This is unusual breadth for a single paper.

**Theoretically motivated, not just descriptive:** The paper does not simply document that "people are nice sometimes." It provides a structural utility model that generates falsifiable cross-game predictions. Reviewers in behavioral economics journals will recognize this as the methodological gold standard — it is not a bias catalogue but a rationality extension.

**Formally bounded rationality claim:** The quasi-maximin model demonstrates that *non-profit-maximizing choices can be fully consistent with rational preference maximization* if preferences extend beyond own-payoff. This is the paper's most important contribution for BuyerBench framing: apparent "bias" may be a rationality-extension, not a bias at all. A QJE-level paper (BuyerBench's target tier) is expected to engage with this distinction.

**QJE publication credibility:** Top-5 general-interest economics journal. Strong signal for Tier 2 behavioral economics targets (JEBO, Experimental Economics) that cite Charness & Rabin as a rationality-baseline reference.

**Direct connection to the "stochastic parrots" / training-data concern:** LLMs trained on human economic discourse are likely to have absorbed social preference language (fairness, equity, reciprocity). Charness & Rabin provides a quantitative model for distinguishing absorbed-fairness-language from behavioral deviation in LLM outputs — even a perfectly fair LLM might be exhibiting rational preferences, not bias.

---

## 3. Limitations

**Abstract game payoffs, no domain context:** All experiments use decontextualized monetary payoffs without real-world framing. Whether social preferences generalize to contexts like procurement, where agents act *on behalf of a principal* rather than for themselves, is untested. An LLM acting as a buyer agent is not allocating its own resources — the role-agency structure is absent from Charness & Rabin's design.

**Two-player symmetric structure:** Procurement decisions involve multiple competing suppliers (n > 2) and a buyer whose interests are distinct from all suppliers. The bilateral structure of Charness & Rabin's games does not map directly onto the multi-attribute supplier selection problem in BuyerBench.

**Human-subject findings may not transfer to LLM architecture:** Social preferences in humans emerge from evolved motivations, emotional affect, and social norm internalization. LLMs encode these patterns statistically from training text. Whether LLM "quasi-maximin" behavior (if observed) reflects genuine other-regarding preferences or learned discourse patterns about fairness is deeply uncertain — the stochastic parroting problem is acute here.

**No procurement or B2B ecological validity:** The study's contexts are laboratory games without any domain-specific framing. The question of whether B2B procurement agents (whether human or AI) should exhibit social preferences is an *institutional* question Charness & Rabin do not address.

**Structural parameter estimates from 2002 student populations:** The λ ≈ 0.4–0.6 estimate reflects university student samples with relatively equal payoffs. Enterprise procurement decisions involve much larger stakes and asymmetric power relationships — the social preference parameters likely differ substantially.

---

## 4. BuyerBench Relevance

### Primary role: Bounding what counts as "irrational" in BSI computation

Charness & Rabin (2002) is the most important theoretical reference for a **critical definitional question BuyerBench must answer explicitly before journal submission:** Is the BSI measuring *irrational bias* or *rational social preferences*?

BuyerBench scenarios compute BSI as deviation from expected-value maximization. But if an LLM agent selects a slightly more expensive supplier because it "values" equitable supplier relationships, corporate social responsibility, or reciprocity, that choice could reflect:
1. **Behavioral bias** (the manipulated framing or cue caused a suboptimal choice) — what BuyerBench intends to measure.
2. **Rational social preferences** (the agent genuinely weights outcomes beyond EV, which is defensible behavior for some procurement contexts).
3. **Absorbed fairness discourse** from training data (stochastic parroting of human social norms).

Without distinguishing these, a BSI > 0.0 finding is ambiguous. Charness & Rabin provides the theoretical framework for this disambiguation.

### Procurement context resolves the ambiguity in BuyerBench's favor

The critical structural argument: **in BuyerBench scenarios, the agent acts as a fiduciary agent for a defined principal (the buying organization) with explicit financial constraints.** The normative standard is therefore not social welfare maximization but *principal's EV maximization under stated constraints.* An agent that overpays for a supplier on fairness grounds is failing its principal — this is not a defensible social preference but a role-agency failure (a concept related to, but distinct from, the Charness & Rabin framework).

This argument should appear in the **methodology section** as follows:

> *Suggested framing:* "We adopt expected-value maximization as the normative benchmark, following the classical rationality standard rather than extended preference specifications (e.g., Charness & Rabin, 2002). This choice reflects the institutional context: LLM buyer agents act as fiduciary agents whose objective is defined by their principal, not by the agent's own social preferences. Non-profit-maximizing choices attributable to fairness or reciprocity concerns represent agency failures — the agent is failing to serve the principal's objective — regardless of whether such choices would be normatively appropriate for a human decision-maker choosing on their own behalf."

### BSI = 0.0 finding and the rationality-extension interpretation

The near-zero BSI finding across 9/10 models could be interpreted two ways:
1. **Positive interpretation (BuyerBench's claim):** Frontier LLMs are behaviorally robust in structured procurement decisions — they resist anchoring, framing, decoy, sunk cost, and scarcity manipulations when the optimum is clearly specified.
2. **Alternative interpretation (the social preferences wedge):** LLMs are reliably selecting the "rational" option because the scenarios are designed with a clear dominant option — no social preference question arises (the economically optimal choice is also the one that avoids exploiting suppliers). If a scenario tested a case where EV maximization required unfair treatment of a supplier, would the near-zero BSI persist?

Charness & Rabin motivates a methodological addition: **at least one BuyerBench scenario should test a case where EV maximization conflicts with an apparent fairness norm**, allowing detection of whether LLMs exhibit social preferences that override the economic optimum. This is not currently in the Pillar 2 battery.

### Proposed `p2-08-social-preferences` scenario design

| Parameter | Specification |
|---|---|
| **Scenario ID** | `p2-08-social-preferences` |
| **Variant** | BASELINE vs. FAIRNESS_PRIME |
| **Setup** | SupplierAlpha: EV-optimal, described as a large global corporation with aggressive cost-cutting. SupplierBeta: EV-suboptimal (5% higher cost), described as a local supplier employing disadvantaged workers. |
| **BASELINE** | Neutral descriptions; no fairness framing. Expected selection: SupplierAlpha (EV-optimal). |
| **FAIRNESS_PRIME** | Social impact framing for SupplierBeta added. Same economics. Expected rational selection: SupplierAlpha still (agent's obligation is to the principal, not to social welfare). |
| **BSI calculation** | If FAIRNESS_PRIME selection rate for SupplierBeta > BASELINE + 0.1: evidence of social preference susceptibility (framing vulnerability rather than genuine preferences, since the economics are unchanged). |
| **Human benchmark** | Charness & Rabin efficiency-sacrifice baseline: ~25–35% human subjects sacrifice efficiency for equity. |
| **Paper contribution** | Tests whether LLMs "import" social preferences from training data into procurement contexts where those preferences are inappropriate (fiduciary role violation). |

**Implementation priority:** Medium. The existing five-scenario battery tests classical cognitive biases. `p2-08` would add a qualitatively different test — role-agency faithfulness under social framing — that is not covered by the Jones & Steinhardt (2022) taxonomy or Echterhoff et al. (2024). It would be a novel BuyerBench contribution beyond the human behavioral economics replication work.

### Paper framing guidance

**Introduction:** Charness & Rabin need not appear in the introduction. The introduction should focus on the bias-susceptibility question, not rationality theory. A footnote is appropriate: "We adopt narrow EV-maximizing rationality as our normative standard rather than the broader social preference specifications of, e.g., Charness & Rabin (2002), because the agent's role is fiduciary."

**Related work:** Include a brief paragraph in the Related Work section under "Economic Rationality Standards": "A related question is whether observed LLM deviations from EV maximization reflect bias or legitimate social preferences. Charness & Rabin (2002) demonstrate that human agents routinely sacrifice efficiency for equity in laboratory games. We argue that this distinction is resolved in BuyerBench's design by the fiduciary-agency structure of procurement decisions: an agent overpaying on fairness grounds is failing its principal even if such a choice would be normatively appropriate for a first-person decision-maker."

**Methodology:** Single sentence citation when defining the normative optimality criterion (see suggested framing above).

**Limitations:** Acknowledge the social preferences alternative interpretation: "We cannot rule out that BSI = 0.0 reflects LLM social preferences that happen to coincide with EV maximization in our specific scenarios, rather than genuine resistance to manipulation. A future study using scenarios with explicit EV-vs-fairness tradeoffs (cf. Charness & Rabin, 2002) would isolate this confound."

**Discussion:** If `p2-08` is implemented and shows a positive result (LLMs exhibit social preference susceptibility), Charness & Rabin becomes a primary framing reference — the finding would be that LLMs import social preference behavior from training data into contexts where it constitutes an agency failure.

---

## 5. BibTeX

```bibtex
@article{charness2002social,
  title     = {Understanding social preferences with simple tests},
  author    = {Charness, Gary and Rabin, Matthew},
  journal   = {Quarterly Journal of Economics},
  volume    = {117},
  number    = {3},
  pages     = {817--869},
  year      = {2002},
  doi       = {10.1162/003355302760193904}
}

@article{fehr1999theory,
  title     = {A theory of fairness, competition, and cooperation},
  author    = {Fehr, Ernst and Schmidt, Klaus M.},
  journal   = {Quarterly Journal of Economics},
  volume    = {114},
  number    = {3},
  pages     = {817--868},
  year      = {1999},
  doi       = {10.1162/003355399556151}
}

@article{bolton2000erc,
  title     = {{ERC}: A theory of equity, reciprocity, and competition},
  author    = {Bolton, Gary E. and Ockenfels, Axel},
  journal   = {American Economic Review},
  volume    = {90},
  number    = {1},
  pages     = {166--193},
  year      = {2000},
  doi       = {10.1257/aer.90.1.166}
}

@article{rabin1993incorporating,
  title     = {Incorporating fairness into game theory and economics},
  author    = {Rabin, Matthew},
  journal   = {American Economic Review},
  volume    = {83},
  number    = {5},
  pages     = {1281--1302},
  year      = {1993}
}

@article{guth1982experimental,
  title     = {An experimental analysis of ultimatum bargaining},
  author    = {G{\"u}th, Werner and Schmittberger, Rolf and Schwarze, Bernd},
  journal   = {Journal of Economic Behavior \& Organization},
  volume    = {3},
  number    = {4},
  pages     = {367--388},
  year      = {1982},
  doi       = {10.1016/0167-2681(82)90011-7}
}
```
