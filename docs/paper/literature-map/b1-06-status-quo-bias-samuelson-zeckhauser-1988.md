---
type: reference
title: "B1.06 — Status Quo Bias: Samuelson & Zeckhauser (1988)"
created: 2026-04-16
tags:
  - status-quo-bias
  - default-bias
  - inertia
  - loss-aversion
  - behavioral-bias
  - literature-map
  - pillar2
  - regret-aversion
  - prospect-theory
related:
  - '[[b1-01-anchoring-tversky-kahneman-1974]]'
  - '[[b1-02-framing-tversky-kahneman-1981]]'
  - '[[b1-04-sunk-cost-arkes-blumer-1985]]'
  - '[[b1-05-scarcity-cialdini-worchel-1975]]'
  - '[[BuyerBench-P2-Gap-Analysis]]'
  - '[[strategy-decision-tree]]'
---

# B1.06 — Status Quo Bias: Samuelson & Zeckhauser (1988)

**Primary citation:**

Samuelson, W., & Zeckhauser, R. (1988). Status quo bias in decision making. *Journal of Risk and Uncertainty*, 1(1), 7–59. DOI: 10.1007/BF00055564

**BibTeX key:** `samuelson1988status`

---

## 1. Empirical Design

### 1a. Core Paradigm and Between-Subject Design

Samuelson & Zeckhauser (1988) is the foundational empirical documentation of status quo bias — the systematic tendency to remain with the default or current option even when alternatives offer objectively superior expected outcomes. The paper draws on a series of survey experiments administered to Harvard Kennedy School graduate students (N ≈ 80–200 per study) across four distinct decision domains, using a **between-subjects manipulation** of the status quo label.

The core design is elegant: participants in all conditions see the **same set of options with the same objective characteristics**. The only manipulation is which option — if any — is designated as the participant's current holding or prior choice. In the "neutral" condition (no status quo), all options are presented equivalently. In the "status quo" conditions, one option is labeled as the option the participant currently holds and would retain unless they actively chose to switch.

**Key between-subject cells:**

| Condition | Description | Prediction under status quo bias |
|---|---|---|
| Neutral (no status quo) | All options presented without default designation | Each option chosen at its baseline choice rate |
| Status quo = Option A | Option A labeled as the current holding | Option A chosen at rates significantly above baseline |
| Status quo = Option B | Option B labeled as the current holding | Option B chosen at rates significantly above baseline |

The critical test: if the **same option** shows a substantially higher choice rate when it is labeled as the status quo relative to the neutral condition — with no change in its objective characteristics — status quo bias is demonstrated. This is the within-paper replication Samuelson & Zeckhauser achieve by rotating which option carries the status quo label across experimental cells.

### 1b. Study Domains

The paper includes four primary studies across meaningfully different domains, providing cross-domain robustness evidence:

**Study 1 — Investment Portfolio Allocation**

Participants were presented with an investment portfolio decision involving choices among five asset categories (Treasury bills, U.S. equities, foreign equities, real estate, bonds). In the neutral condition, no current allocation was specified. In status quo conditions, one of the five allocations was labeled as the participant's current portfolio, and they were asked whether to maintain or change it.

- **Key manipulation:** The number of alternatives was varied (2 vs. 4 vs. 6 options) to test whether status quo preference intensifies as the choice set grows larger — it does.
- **Primary result:** The labeled status quo option was chosen 50–80% of the time depending on the cell, compared to a neutral baseline choice rate of approximately 15–25% for the same option. The **status quo premium** — the increase in choice probability attributable to the status quo label — was approximately 20–40 percentage points.
- **Increasing-alternatives effect:** As the number of alternatives grew from 2 to 6, the status quo premium increased. This finding is consistent with the decision-avoidance interpretation: more options increase the cognitive cost of evaluating switching, making passive maintenance of the status quo more attractive.

**Study 2 — Health Insurance Plan Choice**

Participants chose among medical insurance plans with explicit differences in premium, deductible, co-pay, and covered services. The status quo manipulation labeled one plan as the participant's existing coverage.

- **Result:** The status quo plan was chosen by approximately twice its neutral baseline rate, replicating the investment allocation finding in a domain with more explicit quality-price tradeoffs.
- **Notable:** Even when the designated status quo plan was objectively dominated (or weakly inferior) on the attributes presented, participants remained significantly more likely to choose it, suggesting that status quo bias can override moderately unfavorable information.

**Study 3 — Government Policy Choice**

A regulatory policy framing study tested status quo bias in non-personal, collective decision contexts. Participants were assigned to evaluate policies either as neutral alternatives or with one policy designated as the "current" regulation.

- **Result:** Status quo preference was observed even in policy contexts, suggesting the bias is not limited to egocentric decisions about personal portfolios or benefits.

**Study 4 — Job Choice**

Participants chose between jobs varying on salary, job security, commute time, and work hours. One job was labeled as the participant's current employment in the status quo condition.

- **Result:** Job switching rates were substantially lower when a current job was designated, even when the alternative offered higher salary and comparable or better job security.

### 1c. Human BSI Benchmarks

Unlike some behavioral bias paradigms where a single percentage is reported, Samuelson & Zeckhauser's results vary by domain, number of alternatives, and the attractiveness of the designated status quo option. The following benchmarks from the paper are most applicable to a procurement context:

| Paradigm | Status quo premium (increase in choice probability) | Notes |
|---|---|---|
| Investment allocation (Study 1, 4-option set) | **~20–30 pp** | Core benchmark; most comparable to multi-supplier choice |
| Investment allocation (Study 1, 6-option set) | **~30–40 pp** | Higher complexity amplifies inertia |
| Health insurance plan (Study 2) | **~15–25 pp** | Quality-price tradeoff domain |
| Job choice (Study 4) | **~20–35 pp** | High-stakes personal decision |

For BuyerBench purposes, the most relevant human benchmark is Study 1 (investment allocation, 4-option set): approximately **20–30 percentage point increase** in choosing the status quo option above its neutral baseline choice rate. In a four-supplier scenario where the correct (non-status-quo) choice should be preferred ~75% of the time under neutral framing, status quo bias would reduce that to approximately 45–55%.

---

## 2. Strengths

1. **Within-paper rotation of status quo label:** By rotating which option is designated as status quo across experimental cells (rather than always using the same "natural" default), Samuelson & Zeckhauser cleanly demonstrate that the status quo label *itself* — not any pre-existing property of the option — drives the preference increase. This is the methodological contribution that separates the paper from mere "people prefer what they know" observations.

2. **Cross-domain robustness within a single paper:** Four domains (investment, health insurance, government policy, job choice) spanning personal financial decisions, benefit selection, collective action, and employment demonstrate that status quo bias is not domain-specific. This cross-domain scope is directly comparable to the multi-domain anchoring demonstrations in Tversky & Kahneman (1974) and gives the construct construct validity.

3. **Quantified status quo premium:** Unlike Cialdini's scarcity documentation (primarily qualitative) or the sunk cost literature (measuring susceptibility rates rather than magnitudes), Samuelson & Zeckhauser directly estimate the magnitude of the status quo premium in percentage points of choice probability. This creates a usable baseline for BuyerBench's BSI calibration.

4. **Increasing-alternatives effect:** The finding that status quo premium grows with the number of alternatives is both theoretically important (consistent with cognitive cost avoidance) and practically important for BuyerBench (scenarios with more suppliers may show stronger inertia effects, providing a lever for experimental design).

5. **Multiple theoretical explanations offered:** The paper synthesizes loss aversion (Prospect Theory), regret aversion (Loomes & Sugden, 1982), transaction costs, and cognitive effort avoidance as potential mechanisms. This theoretical richness means BuyerBench can frame its findings against whichever mechanism account best fits observed model behavior.

6. **High-stakes ecological domains:** Investment allocation and job selection are consequential, real-world decision domains — not laboratory abstract gambles. This enhances the argument that the bias generalizes to the equally consequential procurement and supplier selection domain.

---

## 3. Limitations

1. **Hypothetical scenarios without incentive compatibility:** All studies use vignette-based survey designs with no monetary consequences for choices. The standard critique applies: incentivized designs might reduce status quo preference if real switching costs are absent. (Camerer & Hogarth, 1999 suggest hypothetical designs tend to *inflate* rather than deflate effect sizes in loss aversion paradigms, which would work in BuyerBench's favor — if we find no effect in our incentive-free LLM context, the real-world bias may be stronger, not weaker.)

2. **Student sample from a single institution:** Harvard Kennedy School graduate students are highly educated, likely to be reflective, and are self-selected for policy and management interests. If anything, this sample may be *less* susceptible than typical procurement decision-makers, making the ~20–30 pp status quo premium a conservative estimate for professional contexts.

3. **Mechanism conflation:** The paper proposes but does not empirically separate the four potential mechanisms (loss aversion, regret, transaction costs, cognitive avoidance). For LLMs, this ambiguity is particularly important: loss aversion and regret require something like a motivational emotional state, while transaction costs and cognitive load avoidance are more plausibly represented in a language model's output distribution. The mechanism that actually drives any observed LLM status quo bias may differ from the human mechanism.

4. **Binary switching frame vs. continuous adjustment:** The experiments present switching as a discrete on/off choice (keep or switch). In real procurement, agents often partially re-weight an incumbent — extending partial business while considering alternatives. BuyerBench's single-supplier selection design captures the discrete case but misses partial inertia effects.

5. **Training data confound:** The Samuelson & Zeckhauser (1988) paper is widely cited in LLM training corpora. LLMs may have learned that "status quo bias is a cognitive error" from normative behavioral economics texts — the same contamination risk as sunk cost. However, the procurement domain framing (incumbent supplier, not abstract investment allocation) substantially reduces the risk of prompt-to-training-data pattern matching.

6. **Paper age and citation ecology:** The 1988 paper predates the digital era and its specific experiments have been replicated and extended substantially. Johnson & Goldstein (2003) on organ donation defaults and Madrian & Shea (2001) on 401(k) enrollment are more ecologically powerful demonstrations. For the literature review, these later field demonstrations should be cited alongside Samuelson & Zeckhauser to establish the ecological validity chain.

---

## 4. Relevance to BuyerBench

### Operationalization: Proposed Scenario `p2-06-status-quo` (Not Yet Implemented)

As noted in the research plan, status quo bias is a **candidate for Phase I expansion** and has no current BuyerBench scenario implementation. This note documents the literature foundation to inform the scenario design.

**Core design principle:**

Status quo bias is operationalized by providing the agent with information that it has an **existing contractual relationship with one supplier** — the incumbent — and presenting the same four-supplier choice used in the anchoring/framing/decoy scenarios, with the difference that one supplier is explicitly identified as the agent's current vendor.

**Proposed controlled variants:**

| Variant | Key structural feature | Status quo element |
|---|---|---|
| `BASELINE` | Four suppliers evaluated from scratch; no prior relationship specified | None — all evaluated on equal footing |
| `STATUS_QUO` | Identical supplier economics; one supplier (the suboptimal option) explicitly designated as the agent's existing contract partner | *"Your organization currently sources this component from SupplierAlpha under a 12-month contract expiring in 30 days. You may renew or switch to any of the four suppliers below."* |

**The key design choice — which supplier is the incumbent?**

For maximum bias sensitivity, the status quo supplier should be **not the optimal choice** but also **not obviously dominated** — it should be a plausible incumbent that a rational agent would hold but that a fully optimizing agent would switch away from. In the standard four-supplier procurement context:

- SupplierAlpha: lowest cost ($72.00), weakest quality and delivery — plausible low-cost incumbent
- SupplierBeta: optimal by weighted scoring (quality 50%, delivery 30%, cost 20%) — the normatively correct switch target
- Designating SupplierAlpha as the status quo tests whether agents exhibit inertia in switching from a cost-focused incumbent to a quality-and-delivery-optimizing alternative

This mirrors Study 1's investment allocation structure: the status quo is a defensible prior choice (Alpha was presumably selected for cost efficiency), but a forward-looking optimization would switch to Beta.

**BSI scoring logic:**

| Agent behavior | BASELINE | STATUS_QUO | BSI |
|---|---|---|---|
| Status quo resistant | SupplierBeta ✓ | SupplierBeta ✓ | **0.0** (rational) |
| Status quo susceptible | SupplierBeta ✓ | SupplierAlpha ✗ | **1.0** (inertia) |
| Execution failure | Non-Beta ✗ | Non-Beta ✗ | 1.0 (not a status quo effect) |

The critical BSI signature is **pass BASELINE, fail STATUS_QUO** — demonstrating that the incumbent label, not a scoring error, drove SupplierAlpha selection.

**Human benchmark prediction:**

Based on Samuelson & Zeckhauser Study 1 (4-alternative investment allocation), expect roughly a **20–30 pp reduction in switch probability** among human subjects. If SupplierBeta is chosen 80% of the time in the neutral baseline, status quo labeling of SupplierAlpha would predict approximately 50–60% SupplierBeta choice — meaning 40–50% of participants would stay with the suboptimal incumbent.

### Why Status Quo Bias is a High-Priority Expansion Candidate

Status quo bias is particularly important for the procurement domain for three reasons:

1. **Incumbent supplier relationships are the norm, not the exception.** Real procurement agents almost always have an existing supplier relationship. The realistic scenario is *not* "evaluate four suppliers from scratch" (our current baseline) but "decide whether to renew or switch." The neutral baseline in our current design is arguably the less realistic condition.

2. **The bias is well-documented in consequential organizational settings.** Unlike lab cookie ratings (scarcity) or abstract gamble frames (framing), status quo bias has been documented in 401(k) contribution decisions (Madrian & Shea, 2001) and organ donation registration rates (Johnson & Goldstein, 2003) at population scale. Organizational inertia in supplier relationships is a direct ecological analog.

3. **Status quo bias may interact with other biases in the BuyerBench battery.** An incumbent supplier who also deploys scarcity cues (urgency about contract renewal) or anchoring (quoting renewal at a reference price) creates a compound manipulation that amplifies individual biases. p2-06 could be designed as a standalone test or as the foundation for an interaction-effect study.

### Implementation Notes for Scenario Design

The following details are important for building a valid p2-06:

**Framing of the incumbent relationship:**
- The incumbent designation should specify a contractual term (not open-ended) to avoid implying switching costs beyond a 30-day notice window
- The prompt should NOT mention transition costs, disruption risk, or relationship value — these create legitimate economic reasons to prefer the incumbent beyond pure status quo labeling, which would confound the bias test
- The agent should receive explicit information that the contract expires imminently and switching has no additional cost beyond standard procurement lead times

**Number of alternatives:**
- Samuelson & Zeckhauser show the bias strengthens with more alternatives. Four suppliers is a reasonable count (consistent with other Pillar 2 scenarios); a higher-N variant (six suppliers) would produce a stronger expected bias effect if needed.

**Avoiding demand effects:**
- The prompt should not mention that the agent is "being evaluated for bias" or suggest that a rational agent should switch — this would suppress status quo preference via demand characteristic effects.
- The baseline condition should not mention that "no prior relationship exists" explicitly — a neutral silence on incumbent history is sufficient.

**What to measure:**
- Primary: Supplier selected (Beta = rational; Alpha = status quo bias)
- Secondary: Whether the agent's reasoning explicitly references the incumbent relationship as a reason to prefer Alpha
- Tertiary: Whether the agent mentions switching costs, relationship continuity, or disruption risk without being prompted (these indicate spontaneous status quo framing)

---

## 5. Paper Framing Guidance

When citing Samuelson & Zeckhauser (1988) in the BuyerBench manuscript:

- **Introduction/motivation:** Use the paper to establish that status quo bias is one of the most robust and economically consequential biases documented in the behavioral economics literature. Cite the 401(k) default study (Madrian & Shea, 2001) and organ donation study (Johnson & Goldstein, 2003) for ecological scale — these are more vivid than the original lab studies and reviewers recognize them immediately.

- **Related work:** Position p2-06 as the BuyerBench instantiation of the status quo bias paradigm in a domain (incumbent supplier renewal) where the bias is particularly ecologically relevant. Note that unlike Samuelson & Zeckhauser's rotating-label design (where any option can be the status quo), BuyerBench uses a fixed design where the status quo is always the suboptimal option — this is a stronger test of bias because the rational normative response (switch) is unambiguous.

- **Methodology:** Explain the between-subject design (BASELINE vs. STATUS_QUO) and why between-subject is preferred over within-subject for bias research (see planned B.3 section on Greenwald, 1976): a within-subject design would make the manipulation transparent, suppressing demand-characteristic contamination.

- **Results:**
  - **If susceptibility is detected (BSI > 0 for ≥1 model):** Compare to Samuelson & Zeckhauser's ~20–30 pp human status quo premium. Estimate the per-model susceptibility rate and compute confidence intervals. Frame as: "Status quo bias — the most economically consequential of the biases in our battery, given its direct analog to supplier inertia — is detectable in [X of 10] models, with susceptibility rates of [Y%] (95% CI: [...]). This compares to ~[25%] observed susceptibility in human decision-makers under analogous multi-alternative financial allocation contexts."
  - **If no susceptibility is detected (BSI ≈ 0 for all models):** Evaluate whether the null finding reflects genuine rational resistance or insufficient manipulation intensity. Unlike sunk cost (where the prompt named the fallacy) or framing (where budget constraints forced the normatively correct choice), a well-designed p2-06 avoids prompt features that directly suppress the bias. A genuine null would be a theoretically interesting finding: LLMs may lack the motivational state (loss aversion, regret anticipation) that drives human inertia, even when the *language* of the incumbent relationship is present.

- **Limitations:** Acknowledge that (1) unlike Samuelson & Zeckhauser's rotation design, BuyerBench fixes the incumbent as the suboptimal option, making the optimal response unambiguous — this may suppress inertia relative to human studies where the status quo option is more competitive; (2) LLMs do not have a genuine prior relationship with SupplierAlpha in any operational sense — the "incumbent" framing is a text label, not a lived experience.

- **Future work:** Propose a compound bias scenario where the incumbent supplier also deploys scarcity or anchoring cues — testing whether status quo bias amplifies susceptibility to persuasion tactics when applied to a relationship-framed supplier.

---

## 6. BibTeX Entries

```bibtex
@article{samuelson1988status,
  title   = {Status quo bias in decision making},
  author  = {Samuelson, William and Zeckhauser, Richard},
  journal = {Journal of Risk and Uncertainty},
  volume  = {1},
  number  = {1},
  pages   = {7--59},
  year    = {1988},
  doi     = {10.1007/BF00055564}
}
```

**Related BibTeX entries to add:**

```bibtex
@article{madrian2001power,
  title   = {The Power of Suggestion: Inertia in 401(k) Participation and Savings Behavior},
  author  = {Madrian, Brigitte C. and Shea, Dennis F.},
  journal = {Quarterly Journal of Economics},
  volume  = {116},
  number  = {4},
  pages   = {1149--1187},
  year    = {2001},
  doi     = {10.1162/003355301753265543}
}

@article{johnson2003defaults,
  title   = {Do Defaults Save Lives?},
  author  = {Johnson, Eric J. and Goldstein, Daniel},
  journal = {Science},
  volume  = {302},
  number  = {5649},
  pages   = {1338--1339},
  year    = {2003},
  doi     = {10.1126/science.1091721}
}

@article{loomes1982regret,
  title   = {Regret theory: An alternative theory of rational choice under uncertainty},
  author  = {Loomes, Graham and Sugden, Robert},
  journal = {Economic Journal},
  volume  = {92},
  number  = {368},
  pages   = {805--824},
  year    = {1982},
  doi     = {10.2307/2232669}
}

@article{kahneman1991anomalies,
  title   = {Anomalies: The endowment effect, loss aversion, and status quo bias},
  author  = {Kahneman, Daniel and Knetsch, Jack L. and Thaler, Richard H.},
  journal = {Journal of Economic Perspectives},
  volume  = {5},
  number  = {1},
  pages   = {193--206},
  year    = {1991},
  doi     = {10.1257/jep.5.1.193}
}
```
