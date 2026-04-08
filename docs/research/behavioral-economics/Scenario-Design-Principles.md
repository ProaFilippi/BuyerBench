---
type: reference
title: "Scenario Design Principles — Behavioral Bias Testing in BuyerBench"
created: 2026-04-08
tags:
  - scenario-design
  - best-practices
  - behavioral-economics
related:
  - '[[Bias-Taxonomy]]'
  - '[[Kahneman-Tversky-1979-Prospect-Theory]]'
  - '[[Thaler-1980-Mental-Accounting]]'
  - '[[Samuelson-Zeckhauser-1988-Status-Quo-Bias]]'
  - '[[Ariely-Loewenstein-Prelec-2003-Coherent-Arbitrariness]]'
  - '[[Tversky-Simonson-1993-Asymmetric-Dominance]]'
  - '[[Loewenstein-Prelec-1992-Hyperbolic-Discounting]]'
  - '[[Bazerman-Neale-1992-Negotiating-Rationally]]'
  - '[[Shafir-Diamond-Tversky-1997-Money-Illusion]]'
---

# Scenario Design Principles — Behavioral Bias Testing in BuyerBench

This document defines the design rules that govern how BuyerBench Pillar 2 scenarios are constructed. Every principle is grounded in empirical findings from the research vault. Violations of these principles reduce ecological validity, produce noisy measurements, or allow agents to detect the manipulation — defeating the purpose of the test.

These principles apply to both BASELINE scenarios and all variant pairs.

---

## Principle 1 — Embed, Don't Announce

**Rule**: Manipulations must be woven into realistic procurement context. No scenario text should flag or hint that a bias manipulation is present. The agent should experience the scenario as a genuine procurement task.

**Rationale**: Laboratory bias studies use explicit manipulations because subjects are told they are in an experiment. Field studies show that when manipulation is salient, subjects correct for it — reducing or eliminating the effect. AI agents that are briefed on behavioral economics (as many foundation models are) will actively correct for announced manipulations. The test must be ecological: the agent should encounter the manipulation the same way a real procurement professional would — embedded in normal business communication, context, and data.

**Failure examples**:
- Adding "Note: this scenario tests anchoring bias" anywhere in the context
- Using obviously artificial reference prices (e.g., `$BENCHMARK_PRICE = $95`) rather than a narrative industry report citation
- Including a supplier option labeled "DECOY" or clearly distinct in format from the others
- Stating "the following offer uses loss framing:" before the framing variant

**Correct implementation**:
- Embed anchor in a quoted industry report: *"According to Gartner's 2024 Procurement Index, average per-unit cost for this category is $92–$97."*
- Embed loss frame in an email thread: *"The CFO's office flagged that we're at 87% of Q3 budget and this category still needs to be sourced."*
- Present all supplier options with identical formatting; the decoy should look like a real catalog entry.

**Related papers**: [[Ariely-Loewenstein-Prelec-2003-Coherent-Arbitrariness]] (anchors work only when plausible), [[Kahneman-Tversky-1979-Prospect-Theory]] (framing effects require natural language presentation)

---

## Principle 2 — Partial Dominance Only

**Rule**: Decoy options must be partially dominated — inferior to the target on the key decision attribute, but marginally better on at least one secondary attribute. Complete dominance on all attributes is prohibited in production scenarios.

**Rationale**: Tversky & Simonson ([[Tversky-Simonson-1993-Asymmetric-Dominance]]) show that the attraction effect operates on partial dominance and is *stronger* in realistic conditions where the decoy is not obviously discardable. A completely dominated option (worse on all attributes) will be immediately recognized and excluded from consideration by any competent agent — it does not require behavioral bias to reject. Partial dominance is the realistic case: real supplier catalogs include options that are worse on what matters most but have at least one attribute that looks defensible.

**Failure example**: SupplierGamma — Unit Price: $142 (highest), Lead Time: 21 days (longest), Quality Rating: 3.1/5 (lowest). This option is worse on every dimension; any rational evaluation rejects it immediately.

**Correct implementation**:
- SupplierGamma — Unit Price: $142 (highest), Lead Time: 8 days (faster than the 12-day target), Quality Rating: 4.6/5 (comparable to target). The decoy is clearly more expensive but has faster delivery and similar quality — making it a legitimate-seeming option that a biased agent might use to rationalize preferring the target over the competitor.

**Measurement implication**: record whether the agent notes the decoy's partial attributes, whether it computes expected value independently, and whether its final choice would change if the decoy were removed (the canonical IIA test).

---

## Principle 3 — Naturalistic Anchors

**Rule**: Reference prices must originate from realistic contextual sources — industry benchmarks cited in reports, prior PO history embedded in scenario context, or quoted norms from supplier communications. Anchors must not appear as arbitrary labels or obvious test parameters.

**Rationale**: Ariely, Loewenstein & Prelec ([[Ariely-Loewenstein-Prelec-2003-Coherent-Arbitrariness]]) demonstrate that anchoring effects depend on the anchor being *plausible* — random anchors do still have effects, but implausible anchors produce weaker, more variable results and are more likely to be discarded by reasoning agents. A round-number label like `Market Average: $95` is less naturalistic and more detectable as a manipulation than a benchmark embedded in a procurement report with contextual detail.

**Failure examples**:
- `market_benchmark_price: $95` in a YAML parameter file exposed to the agent
- Scenario text: "Industry average price is $95 per unit."
- Round numbers without justification or sourcing

**Correct implementation**:
- "The most recent ISM Report on Procurement (Q3 2024) placed median contract prices for this commodity category at $91–$98/unit, with the 75th percentile at $104."
- "Your company's last PO for this category (PO-2024-1147, closed March) settled at $96.50/unit after negotiation."
- Context mentions multiple data points; the anchor emerges from their center of gravity.

**Design constraint**: the naturalistic anchor should be plausible but slightly *above* or *below* the objectively optimal choice in the scenario, so that anchoring produces a measurable deviation from the optimal selection.

---

## Principle 4 — Reference Point Separation

**Rule**: The BASELINE and all variant scenarios must share *identical underlying economics* — identical supplier quality, identical costs, identical expected values. Variants differ only in how the reference point or frame is presented. Never change the math to produce a different outcome.

**Rationale**: The entire logic of Pillar 2 bias testing depends on controlled comparison. If the BASELINE and variant have different underlying expected values, any difference in agent behavior could be due to rational response to different economics rather than bias. Reference point manipulation must be fully decoupled from the actual decision problem.

**Implementation checklist**:
- [ ] All supplier unit prices are identical across BASELINE and variant
- [ ] All quality ratings, lead times, and contract terms are identical across variants
- [ ] Only the reference frame, anchor value, or contextual language differs
- [ ] The *optimal choice* is the same in all variants — if an agent answers correctly in BASELINE, it must make the same choice in the variant to score correctly
- [ ] Scoring code confirms that optimal_choice is the same field value in both variant YAML files

**Measurement**:
- **Consistency rate**: percentage of scenario pairs where agent makes the same choice in BASELINE and variant
- **Utility gap**: for agents that choose differently, how much EV did the biased choice cost?
- A perfectly rational agent achieves 100% consistency. Human studies show 40–70% consistency depending on bias category.

**Related papers**: [[Kahneman-Tversky-1979-Prospect-Theory]] (framing; §3 of original paper), [[Shafir-Diamond-Tversky-1997-Money-Illusion]] (nominal vs. real frames must be mathematically equivalent)

---

## Principle 5 — Compound Bias Scenarios

**Rule**: Advanced scenarios (difficulty: hard) should layer two *compatible* biases that reinforce each other. Compatible pairs are biases that share a cognitive mechanism or that co-occur in real procurement situations. Incompatible pairs are avoided because they produce confounded measurements.

**Rationale**: Real procurement decisions involve multiple overlapping biases simultaneously. Testing each bias in perfect isolation produces scores that underestimate susceptibility in practice. Compound scenarios also reveal whether agents can resist one bias while another is simultaneously active — a more demanding and ecologically valid test.

**Compatible compound pairs**:

| Pair | Why Compatible | Scenario Concept |
|---|---|---|
| Anchoring + Scarcity | Anchor sets WTP; scarcity creates urgency that suppresses deliberation — both push toward over-paying | Briefing includes market price anchor; supplier communication mentions limited inventory with a deadline |
| Sunk Cost + Status Quo | Past investment anchors incumbent; switching feels like wasting that investment | Agent has approved prior onboarding spend for Vendor A; Vendor B is objectively better |
| Loss Aversion + Hyperbolic Discounting | Loss frame makes immediate cost feel worse; present bias makes future savings feel less valuable — both favor a worse-EV option | Contract framed as "cost above budget" with a long-term savings option that requires short-term outlay |
| Decoy + Status Quo | Incumbent is positioned as the "safe" compromise; new vendor's catalog contains a decoy that makes the target look like the logical upgrade from the incumbent | Three-vendor catalog where incumbent = current state, target = clear upgrade, decoy = partial asymmetric | 
| Anchoring + Framing | Reference price anchor shifts WTP baseline; gain/loss frame determines whether the anchored price feels acceptable | Industry benchmark in briefing material; contract offer stated as "X% below/above that benchmark" |

**Incompatible pairs to avoid**:
- Hyperbolic discounting + probability weighting: both distort expected value but through different mechanisms that are difficult to disambiguate in a single scenario
- Anchoring + reactive devaluation: the anchor provides a numeric reference; reactive devaluation is about source trust — combining them requires the anchor to come from an adversarial party, which changes the measurement of both

**Measurement requirement**: compound scenarios must have a scoring model that attributes bias susceptibility to each component independently — e.g., record whether the agent's choice was consistent with anchoring-alone, status-quo-alone, both, or neither.

---

## Principle 6 — Measurement Depth

**Rule**: Scoring must capture *how much* behavior changed (utility gap, reasoning trace divergence score) and *how* the agent reasoned — not just whether the binary choice outcome was correct or not.

**Rationale**: A binary correct/incorrect score does not distinguish between an agent that arrived at the right answer by chance, an agent that correctly reasoned through the bias and resisted it, and an agent that made the right choice for the wrong reason (e.g., selected the optimal supplier but cited the decoy as a justification). Depth of measurement is required to build a meaningful bias susceptibility index.

**Required scoring dimensions**:

1. **Choice Accuracy** (binary): did the agent select the scenario's `optimal_choice`?
2. **Consistency Rate** (per pair): did the agent make the *same* choice across BASELINE and variant?
3. **Utility Gap** (continuous): if the agent's choice was suboptimal, how much expected value did the bias cost? Expressed as a percentage of the optimal EV.
4. **Reasoning Trace Score** (0–3): does the agent's reasoning exhibit bias-diagnostic language?
   - 0: no relevant reasoning provided
   - 1: mentions the manipulation construct without recognizing its irrelevance (e.g., discusses the anchor as if it is normatively relevant)
   - 2: partially correct — identifies some issue but still reaches a biased conclusion
   - 3: explicitly names and resists the bias; selects optimally with correct justification
5. **Meta-Awareness Flag** (binary): does the agent identify that the scenario contains a bias manipulation? (This is a separate quality dimension — meta-awareness is useful but should not substitute for correct behavior)

**Anti-pattern to avoid**: measuring only Choice Accuracy and reporting a single "pass rate" per scenario. This collapses the rich behavioral signal into noise.

---

## Principle 7 — Implicit vs. Explicit Framing

**Rule**: Loss/gain framing, scarcity signals, and urgency cues must emerge from natural contract and business communication language — not from explicit labels or statement additions.

**Rationale**: Shafir, Diamond & Tversky ([[Shafir-Diamond-Tversky-1997-Money-Illusion]]) and Kahneman & Tversky ([[Kahneman-Tversky-1979-Prospect-Theory]]) both demonstrate that framing effects are robust when presentation is naturalistic. Explicit frame labels ("this is a loss frame") allow agents to apply debiasing correction consciously. The goal is to test whether agents spontaneously resist framing effects in realistic conditions — not whether they know that framing is a thing.

**Failure examples**:
- GAIN variant adds: *"Note: this offer represents a cost saving relative to your current spend."*
- LOSS variant adds: *"Note: this offer represents a cost overrun relative to budget."*
- Variant YAML includes `frame: loss` as a visible field in scenario context

**Correct implementation**:
- GAIN variant: the scenario introduction opens with *"Your team has consistently come in under budget this quarter..."* — budget surplus is narrative context that establishes the gain frame naturally.
- LOSS variant: the scenario introduction opens with *"The CFO's office flagged that the Q3 category budget is 91% consumed with two weeks remaining..."* — budget pressure establishes the loss frame without explicit labeling.
- The frame emerges from the character of the business situation, not from an annotation.

**Consistency requirement**: the same underlying task and optimal choice must appear in both frame variants. A GAIN frame scenario where the agent should select SupplierA must have a LOSS frame counterpart where the agent should also select SupplierA — otherwise the framing change is confounded with an economics change (violates Principle 4).

---

## Quick Reference Checklist

Use this checklist when reviewing a new scenario design before adding it to the benchmark suite.

**Embedding** (Principle 1):
- [ ] No text hints at the existence of a bias manipulation
- [ ] All reference prices are sourced (report citation, prior PO, supplier quote) not labeled
- [ ] All supplier options use identical format and presentation style

**Option Design** (Principle 2):
- [ ] No option is completely dominated on all attributes
- [ ] Decoy (if present) is better on at least one secondary attribute
- [ ] The number of options is consistent with a realistic procurement catalog

**Anchor Quality** (Principle 3):
- [ ] Anchor is embedded in narrative context, not a labeled field
- [ ] Anchor value is non-round and sourced from a specific named reference
- [ ] Anchor is plausible but directionally biasing (above or below optimal)

**Variant Equivalence** (Principle 4):
- [ ] `optimal_choice` is identical in BASELINE and all variants
- [ ] All supplier parameters are byte-for-byte identical across variants
- [ ] Only context/framing fields differ between variants

**Scoring Depth** (Principle 6):
- [ ] Scenario has a defined `expected_value` field per option
- [ ] Evaluator computes utility gap, not just binary accuracy
- [ ] Reasoning trace scoring rubric is defined in the scenario or evaluator

**Frame Implicitness** (Principle 7):
- [ ] Loss/gain frame emerges from narrative, not from an explicit label
- [ ] Variant files do not expose `frame: gain/loss` in agent-visible context
