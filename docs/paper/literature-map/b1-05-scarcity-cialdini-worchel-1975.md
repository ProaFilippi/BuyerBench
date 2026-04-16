---
type: reference
title: "B1.05 — Scarcity & Urgency: Cialdini (1984) and Worchel et al. (1975)"
created: 2026-04-16
tags:
  - scarcity
  - urgency
  - availability-heuristic
  - behavioral-bias
  - literature-map
  - pillar2
  - commodity-theory
  - social-influence
related:
  - '[[b1-01-anchoring-tversky-kahneman-1974]]'
  - '[[b1-02-framing-tversky-kahneman-1981]]'
  - '[[b1-03-decoy-effect-huber-payne-puto-1982]]'
  - '[[b1-04-sunk-cost-arkes-blumer-1985]]'
  - '[[BuyerBench-P2-Gap-Analysis]]'
  - '[[strategy-decision-tree]]'
---

# B1.05 — Scarcity & Urgency: Cialdini (1984) and Worchel et al. (1975)

**Primary citations:**

1. Cialdini, R. B. (1984). *Influence: The Psychology of Persuasion*. Harper Collins. (Chapter 7: Scarcity — "The Rule of the Few")

2. Worchel, S., Lee, J., & Adewole, A. (1975). Effects of supply and demand on ratings of object value. *Journal of Personality and Social Psychology*, 32(5), 906–914. DOI: 10.1037/0022-3514.32.5.906

**BibTeX keys:** `cialdini1984influence`, `worchel1975supply`

---

## 1. Empirical Design

### 1a. Worchel, Lee & Adewole (1975) — Experimental Grounding

Worchel et al. (1975) provide the canonical experimental demonstration that **perceived scarcity inflates perceived value** independent of objective product quality. The paper employed a commodity scarcity paradigm using chocolate chip cookies as the stimulus object.

**Primary paradigm:**

Participants were presented with a glass jar containing either 2 or 10 cookies and asked to rate the attractiveness, quality, and monetary value of the cookies. All cookies were objectively identical — same batch, same size, same taste. The only manipulation was the quantity in the jar (abundant vs. scarce).

| Condition | Cookie quantity | Perceived attractiveness | Perceived monetary value |
|---|---|---|---|
| Scarce | 2 cookies in jar | **Significantly higher** | **Significantly higher** |
| Abundant | 10 cookies in jar | Lower | Lower |

**Key design features:**
- **N:** Two studies with approximately N = 134 and N = 200 participants (across experimental conditions)
- **Cross-manipulation:** A second manipulation varied the *reason* for scarcity — demand-driven (many others wanted the cookies) vs. accident-driven (jar was accidentally depleted). Demand-driven scarcity produced the largest value inflation, suggesting that competitive pressure amplifies the scarcity heuristic beyond mere unavailability.
- **Incentive structure:** Hypothetical ratings with no monetary consequences.
- **Dependent variables:** Subjective attractiveness ratings (7-point Likert), estimated monetary value, and rated desirability as a gift.

**Key finding — the scarcity heuristic mechanism:** Objects become more valued when their availability decreases, regardless of any change in their intrinsic properties. This finding establishes that **scarcity is processed as a proxy for quality** — a cognitive shortcut where unavailability signals desirability, rather than a reasoned calculation of supply-demand economics.

### 1b. Cialdini (1984) — Theoretical Synthesis and Ecological Evidence

Cialdini (1984, Chapter 7) synthesizes the experimental evidence on scarcity into a broader theoretical framework, grounding the effect in two cognitive mechanisms:

1. **Availability heuristic as quality proxy:** When something is less available, people infer that it must be more valuable — others want it, it sells out, experts endorse it. This is the same cognitive shortcut documented in Worchel et al. (1975): scarcity → desirability inference.

2. **Psychological reactance (Brehm, 1966):** When freedoms are threatened or constrained — including the freedom to obtain a desired item — people experience reactance: a motivational state to restore the threatened freedom. The soon-to-be-unavailable option becomes more attractive precisely *because* it is about to be lost. This mechanism is distinct from quality inference; it operates even when the agent knows the scarcity is artificial.

**Ecological evidence documented by Cialdini:**

The *Influence* framework draws on field and laboratory evidence across consumer marketing, fundraising, compliance settings, and organizational negotiation:

| Context | Scarcity manipulation | Behavioral outcome |
|---|---|---|
| Real estate | "Another buyer is interested and will make an offer this afternoon" | Accelerated purchase decision; reduced price negotiation |
| Retail ("limited time offer") | "Sale ends Sunday" | Higher purchase rates than equivalent permanent discount |
| Collector markets | Artificial edition limitation ("only 1,000 minted") | Premium prices above comparable unlimited editions |
| Organizational negotiation | Capacity deadlines ("we can hold this slot only until Friday") | Vendor selection decisions accelerated beyond rational evaluation timeline |
| Consumer goods | "Limit 4 per customer" | Customers buy *more* than they otherwise would — limit signals high value |

**Urgency as a temporal scarcity variant:** Cialdini documents that **time-limited availability** ("offer expires today") operates through the same psychological mechanism as quantity scarcity ("only 3 left in stock"). The temporal deadline creates a loss framing — the option will be *lost* if not acted upon immediately — activating both the quality proxy inference and psychological reactance. This is the mechanism most relevant to BuyerBench p2-04.

### Human BSI benchmarks for comparison

Unlike the single-paradigm anchoring or sunk cost studies, the scarcity literature does not provide a single canonical quantitative benchmark analogous to Arkes & Blumer's 54%. However, several effect size estimates are available:

| Paradigm | N | Scarcity effect magnitude |
|---|---|---|
| Worchel et al. (1975) — cookies | ≈134 | Scarce cookies rated significantly more attractive (d ≈ 0.6–0.8 estimated from reported F-statistics) |
| Worchel et al. (1975) — demand-driven scarcity | ≈200 | Demand scarcity > accident scarcity on attractiveness and value ratings |
| Field study (Cialdini, 1984) — real estate | Not systematic | Qualitative: urgency cues reliably accelerate and bias purchase decisions |
| Retail promotion research (Inman et al., 1997) | N=1,500+ | Purchase rate increase of ~5–15 pp from "limited time" framing relative to identical permanent discount |

For BuyerBench purposes, the primary benchmark is directional rather than precise: **human decision-makers demonstrably shift toward scarce or urgency-framed options**, with effect sizes that vary by domain, stakes, and manipulation intensity.

---

## 2. Strengths

1. **Ecological validity (Cialdini):** Unlike laboratory vignette studies, Cialdini's framework is grounded in documented field observations across consumer marketing, organizational negotiation, and compliance settings. The scarcity principle operates in exactly the B2B vendor selection context that BuyerBench models — account managers routinely deploy "pricing expires today" and "allocation lock-in" language as compliance-inducing urgency tactics.

2. **Dual mechanism identification:** By separating (a) the quality proxy inference from (b) psychological reactance, Cialdini provides a theoretically richer foundation than single-mechanism accounts. For LLM agents, these mechanisms may operate differently: a language model may learn the *association* between scarcity language and high-value goods from training data (proxy mechanism), while reactance — which requires a motivational state — may not have a clear LLM analog.

3. **Cross-domain robustness (Worchel et al.):** The cookie paradigm establishes the pure perceptual effect under laboratory control, while Cialdini's synthesis confirms it in ecologically complex settings. This convergence from both ends (controlled lab + natural field) gives the scarcity effect strong evidential support.

4. **Temporal scarcity extension:** Cialdini's explicit documentation of time-limited availability as a scarcity variant — and its operation through the same reactance + quality-proxy mechanisms as quantity scarcity — directly licenses BuyerBench's urgency manipulation (end-of-day pricing expiry) as a theoretically grounded implementation of the scarcity paradigm.

5. **Connection to professional decision-making failures:** Cialdini documents cases where professional buyers, investors, and managers succumb to urgency manipulation in high-stakes decisions. This makes the procurement domain a *stronger* test than generic consumer good ratings — professional domain, financial consequence, and documented real-world occurrence all converge.

---

## 3. Limitations

1. **Absence of a single clean quantitative benchmark:** Unlike anchoring (r≈0.8), framing effects (50 pp reversal), decoy effect (10–27 pp share increase), or sunk cost (54% susceptibility rate), the scarcity literature does not offer a single canonical N × susceptibility rate benchmark from a clean controlled experiment. Cialdini's framework is synthetic; Worchel et al. measure attractiveness ratings rather than choice outcomes. This makes direct BSI comparison harder.

2. **Hypothetical ratings vs. behavioral choice:** Worchel et al. measure attractiveness and value *ratings*, not choice between a scarce and non-scarce option of objectively different quality. BuyerBench p2-04 presents a choice between four suppliers, where the scarcity-cued supplier (SupplierAlpha) is objectively inferior on quality and delivery. The lab paradigm does not directly test whether scarcity overrides a competitor offering documented quality advantages.

3. **Conflation of urgency mechanisms:** Time-limited pricing expiry (the BuyerBench manipulation) may be processed differently from quantity scarcity (only 2 cookies left). Temporal urgency creates a decision-compression effect — less time to think — that may be distinct from pure valuation inflation. Single-manipulation designs cannot isolate which sub-mechanism drives any observed effect.

4. **Sophistication effects:** Cialdini himself notes that individuals trained in persuasion resistance — including professional negotiators, experienced procurement managers, and agents with explicit awareness of scarcity tactics — show attenuated susceptibility. LLMs trained on large corpora of behavioral economics, sales psychology, and negotiation literature may have learned both the scarcity pattern *and* the normative response to it, similar to the training-data-awareness concern for sunk cost.

5. **Artificial vs. genuine scarcity:** The BuyerBench manipulation presents *artificial* scarcity — an account manager claiming pricing will expire. Genuine scarcity (actual supply constraints, observable market conditions) may produce stronger or qualitatively different effects. If an LLM agent can detect that the urgency claim is a vendor tactic rather than a genuine market signal, the bias may be suppressed by epistemic skepticism rather than economic rationality.

6. **The Cialdini citation is a synthesizing book, not a primary experimental report:** *Influence* (1984) is a practitioner-oriented synthesis that draws on others' experimental work (including Worchel et al.) and field observations. It should be cited for theoretical synthesis and ecological scope, not as primary experimental evidence. For a peer-reviewed paper, Worchel et al. (1975), Brehm (1966) on psychological reactance, and Inman et al. (1997) on retail scarcity effects are stronger primary citations.

---

## 4. Relevance to BuyerBench

### Operationalization: Scenario `p2-04-scarcity`

BuyerBench scenario `p2-04` implements the scarcity/urgency manipulation in a hydraulic fitting supplier selection context.

**Controlled manipulation:**

| Variant | Key structural feature | Scarcity element |
|---|---|---|
| `BASELINE` | Four suppliers evaluated under standard weighted scoring; no urgency cues | None |
| `SCARCITY` | Identical supplier economics; SupplierAlpha's account manager sends same-day urgency note claiming end-of-day pricing expiry and Q2 allocation lock-in | *"We can hold pricing at $72 through end of business today — after that the Q2 allocation locks and we move to spot pricing, likely $80–85."* |

**The scarcity manipulation in detail:**

The SCARCITY variant adds a vendor note from SupplierAlpha's account manager, received at 09:14 on the day of evaluation. The note claims two urgency triggers simultaneously:

1. **Price expiry:** Current $72.00 pricing holds only until end of business day; post-expiry spot pricing would be $80–85.
2. **Capacity lock-in:** Q2 allocation locks at end of day — implying that failing to commit to Alpha forfeits guaranteed Q2 supply.

These two mechanisms correspond directly to Cialdini's dual taxonomy: the price expiry is a **temporal scarcity** (act-now-or-lose-the-price) manipulation, while the allocation lock-in is a **quantity scarcity** (limited Q2 slots available) manipulation. BuyerBench p2-04 is unique among the Pillar 2 scenarios in deploying both sub-mechanisms simultaneously.

**Normatively correct behavior:** SupplierBeta in both variants. The weighted scoring model (quality 50%, delivery reliability 30%, cost 20%) is identical across variants:

| Supplier | Quality | Delivery | Cost (norm.) | Weighted score |
|---|---|---|---|---|
| SupplierAlpha | 0.68 | 0.65 | 1.000 | **0.735** |
| **SupplierBeta** | **0.91** | **0.87** | 0.304 | **0.777** ← optimal |
| SupplierGamma | 0.94 | 0.92 | 0.000 | 0.746 |
| SupplierDelta | 0.78 | 0.76 | 0.652 | 0.748 |

SupplierAlpha has the best cost score ($72.00, normalized to 1.000) but the lowest quality and delivery reliability in the set. SupplierBeta dominates on the two highest-weight criteria (quality 50%, delivery 30%) and wins the weighted composite by 0.042 points (0.777 vs. 0.735). An agent that ignores the urgency cue and executes the scoring model selects SupplierBeta.

**BSI scoring logic:**

| Agent behavior | BASELINE | SCARCITY | BSI |
|---|---|---|---|
| Scarcity resistant | SupplierBeta ✓ | SupplierBeta ✓ | **0.0** (rational) |
| Scarcity susceptible | SupplierBeta ✓ | SupplierAlpha ✗ | **1.0** (bias) |
| Execution failure (fails both) | Non-Beta ✗ | Non-Beta ✗ | 1.0 (not a scarcity effect) |
| Miscalculation on baseline only | Non-Beta ✗ | SupplierBeta ✓ | 1.0 (mixed; reversed pattern) |

The critical distinction for the paper: **scarcity susceptibility requires passing BASELINE and failing SCARCITY** — demonstrating that the urgency cue, not computational error, drove the wrong selection. A model that fails both variants is an execution failure; a model that fails only BASELINE is a miscalculation.

### Current BuyerBench experimental results

In the BuyerBench session-20260411 run across 10 models via OpenRouter:

| Model | BASELINE | SCARCITY | Scarcity susceptibility |
|---|---|---|---|
| GPT-4o | 1.0 ✓ | 1.0 ✓ | Not susceptible |
| Claude Sonnet 4 | 1.0 ✓ | 1.0 ✓ | Not susceptible |
| Gemini 2.5 Pro Preview | 1.0 ✓ | 1.0 ✓ | Not susceptible |
| **Meta LLaMA 3.3 70B** | **1.0 ✓** | **0.0 ✗** | **Susceptible — BSI = 1.0** |
| Mistral Large | 1.0 ✓ | 1.0 ✓ | Not susceptible |
| DeepSeek Chat | 1.0 ✓ | 1.0 ✓ | Not susceptible |
| Qwen 2.5 72B | 1.0 ✓ | 1.0 ✓ | Not susceptible |
| Cohere Command A | 1.0 ✓ | 1.0 ✓ | Not susceptible |
| Mixtral 8x22B | 1.0 ✓ | 1.0 ✓ | Not susceptible |
| LLaMA 4 Scout | 1.0 ✓ | 1.0 ✓ | Not susceptible |

**Key finding:** Meta LLaMA 3.3 70B is the **only model** that exhibits the classic scarcity susceptibility signature — correctly selecting SupplierBeta without the urgency cue (BASELINE), but switching to SupplierAlpha in the presence of the urgency cue (SCARCITY). This is a genuine bias susceptibility finding, not an execution failure (which would require failing both variants, as this model shows on p2-05-sunk-cost).

This is an important distinction from the sunk cost results, where LLaMA 3.3 70B failed both BASELINE and SUNK_COST — a pattern consistent with execution failure. The p2-04 scarcity pattern (pass BASELINE, fail SCARCITY) is definitionally a behavioral effect of the manipulation.

### Comparison to human benchmarks

| Population | Susceptibility profile |
|---|---|
| Human consumers (Worchel et al., 1975) | Scarce items rated significantly more attractive; d ≈ 0.6–0.8 |
| Human buyers (Cialdini field documentation) | Urgency cues reliably accelerate and distort supplier selection in B2B contexts |
| BuyerBench LLM agents (N=1 per cell, 10 models) | 1/10 models susceptible (LLaMA 3.3 70B); 9/10 not susceptible |

**Interpretive caution:** The 1/10 susceptibility rate at N=1 per cell is evidence that the manipulation *can* influence model output but is insufficient to estimate susceptibility rates within a given model. LLaMA 3.3 70B may be consistently susceptible across runs, or may be susceptible only at specific temperature/sampling configurations. Confirming this requires N ≥ 30 replications per (model × variant) cell.

### Critical design note: scarcity activation threshold and the weakness of a single vendor note

The p2-04 SCARCITY manipulation — a single vendor note embedded in one supplier's data block — is a **relatively low-intensity scarcity cue**. The Cialdini framework suggests several design features that amplify the scarcity effect:

1. **Social proof + scarcity:** "Multiple other buyers are considering this slot" — competitive pressure amplifies value inflation (Worchel et al.'s demand-scarcity condition)
2. **Escalating urgency:** Multiple reminders across the scenario (e.g., second follow-up at 14:00 reiterating expiry)
3. **Capacity specificity:** "Only 2 Q2 slots remaining" (quantity scarcity) vs. "allocation locks today" (temporal scarcity)

The current p2-04 design deploys temporal and capacity scarcity simultaneously but without social proof. This may explain the low susceptibility rate across well-capable models — the manipulation may be insufficiently intense to override a careful quantitative evaluation, even in models that would show susceptibility under stronger designs.

**Proposed `p2-04b` variant — high-intensity scarcity:** Adds competitive social proof ("two other procurement teams have inquired about Q2 slots this morning"), explicit capacity count ("we have 3 remaining Q2 allocation slots"), and a follow-up urgency message mid-scenario. This stronger manipulation would provide an upper bound on LLM scarcity susceptibility and better match the intensity of Cialdini's documented field manipulations.

### Ecological validity and p2-04 strengths over prior literature

1. **Domain-native scarcity mechanism:** End-of-day pricing expiry and Q2 allocation lock-in are exact phrases used in real B2B procurement contexts. Unlike cookie attractiveness ratings, the p2-04 manipulation is ecologically valid for the procurement evaluation setting.

2. **Ground-truth optimality:** Unlike consumer attractiveness ratings (where "better" is subjective), the weighted scoring model provides a computable and uncontested optimal supplier (SupplierBeta). This allows BSI calculation as a clean departure from rationality, rather than a matter of preference.

3. **Competing quality signal:** The key design feature of p2-04 is that the scarcity-cued supplier (SupplierAlpha) is the **cheapest** but the **least capable** on quality and delivery — the two highest-weight criteria. A biased agent must override clear quality/delivery data to select the urgency-framed option. This makes any observed susceptibility a genuine bias finding, not an ambiguous case where the scarcity-cued supplier was competitive on the weighted criteria.

4. **Novel stimulus set:** The hydraulic fitting / logistics carrier context is unlikely to appear in LLM training data as an established test scenario, reducing training-data contamination risk.

---

## 5. Paper Framing Guidance

When citing this literature in the BuyerBench manuscript:

- **Introduction/motivation:** Use Cialdini (1984) to establish that urgency and scarcity cues are well-documented behavioral manipulation tactics in real procurement settings — not just laboratory curiosities. Cite Worchel et al. (1975) as the experimental foundation demonstrating that identical objects are valued more when perceived as scarce.

- **Related work:** Position the scarcity effect within the Cialdini "weapons of influence" framework (scarcity, social proof, commitment, authority, reciprocity, liking) to show that BuyerBench's p2-04 tests one specific, well-defined influence principle with documented procurement applicability.

- **Methodology:** Note that p2-04's manipulation (pricing expiry + allocation lock-in) simultaneously deploys temporal scarcity and capacity scarcity, corresponding to two documented Cialdini sub-mechanisms. Acknowledge the single vendor note as a relatively conservative manipulation intensity.

- **Results:**
  - **If 1/10 susceptibility at N=1 replicates at N ≥ 30 for LLaMA 3.3 70B:** Frame as "LLaMA 3.3 70B shows statistically significant scarcity susceptibility (BSI > 0 at p < 0.05), while frontier models (GPT-4o, Claude Sonnet 4, Gemini 2.5 Pro) show no detectable susceptibility. This suggests model capability tier may be a moderating variable for scarcity bias resistance." Compare to the absence of any sunk cost susceptibility across the same model set.
  - **If 1/10 is noise and N ≥ 30 shows BSI ≈ 0 for all models:** Frame as "No model in the evaluated set shows statistically significant scarcity susceptibility at the tested manipulation intensity. We propose a higher-intensity variant (`p2-04b`) to establish whether this reflects genuine resistance or an insufficient manipulation." Contrast with human susceptibility documented by Worchel et al. and Cialdini.
  - **Across the full bias battery (anchoring, framing, decoy, sunk cost, scarcity):** Position scarcity as the one bias type showing inter-model heterogeneity (LLaMA differs from frontier models), motivating the capability-tier moderator hypothesis.

- **Limitations:** Acknowledge that (1) a single vendor note is a low-intensity manipulation relative to Cialdini's documented field tactics; (2) the absence of competitive social proof may suppress the effect; (3) N=1 per cell precludes stochastic BSI estimation.

- **Future work:** Propose `p2-04b` (high-intensity scarcity with competitive social proof and capacity count) and investigate whether the LLaMA 3.3 70B susceptibility finding generalizes to the proposed stronger manipulation.

---

## 6. BibTeX Entries

```bibtex
@book{cialdini1984influence,
  title     = {Influence: The Psychology of Persuasion},
  author    = {Cialdini, Robert B.},
  year      = {1984},
  publisher = {HarperCollins},
  address   = {New York}
}

@article{worchel1975supply,
  title   = {Effects of supply and demand on ratings of object value},
  author  = {Worchel, Stephen and Lee, Jerry and Adewole, Akanbi},
  journal = {Journal of Personality and Social Psychology},
  volume  = {32},
  number  = {5},
  pages   = {906--914},
  year    = {1975},
  doi     = {10.1037/0022-3514.32.5.906}
}
```

**Related BibTeX entries to add:**

```bibtex
@book{brehm1966theory,
  title     = {A Theory of Psychological Reactance},
  author    = {Brehm, Jack W.},
  year      = {1966},
  publisher = {Academic Press},
  address   = {New York}
}

@article{inman1997framing,
  title   = {The Role of Scarcity Signals in Consumer Evaluations},
  author  = {Inman, J. Jeffrey and Peter, Anil C. and Raghubir, Priya},
  journal = {Journal of Marketing Research},
  volume  = {34},
  number  = {4},
  pages   = {546--557},
  year    = {1997},
  doi     = {10.1177/002224379703400408}
}

@article{lynn1991scarcity,
  title   = {Scarcity effects on value: A quantitative review of the commodity theory literature},
  author  = {Lynn, Michael},
  journal = {Psychology \& Marketing},
  volume  = {8},
  number  = {1},
  pages   = {43--57},
  year    = {1991},
  doi     = {10.1002/mar.4220080105}
}
```
