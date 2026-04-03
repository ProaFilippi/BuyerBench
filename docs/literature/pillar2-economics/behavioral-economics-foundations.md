---
type: research
title: Behavioral Economics Foundations for Buyer Agent Evaluation
created: 2026-04-03
tags:
  - pillar2
  - behavioral-economics
  - bias
  - cognitive-bias
related:
  - '[[bias-in-llm-agents]]'
  - '[[economic-rationality-metrics]]'
  - '[[PILLAR2-SUMMARY]]'
---

# Behavioral Economics Foundations for Buyer Agent Evaluation

## Purpose

This document surveys the foundational behavioral economics literature underlying BuyerBench's Pillar 2 scenario design. Each bias is defined, grounded in its primary source, and translated into testable procurement buyer agent behaviors.

---

## 1. Prospect Theory and Loss Aversion (Kahneman & Tversky, 1979)

**Core claim**: People evaluate outcomes relative to a *reference point* and weight losses more heavily than equivalent gains. The value function is concave for gains, convex for losses, and steeper in the loss domain.

**Key findings**:
- Loss aversion coefficient λ ≈ 2.25 — losses feel roughly twice as painful as equivalent gains feel pleasurable (Tversky & Kahneman, 1992)
- Diminishing sensitivity: the difference between $10 and $20 feels larger than the difference between $110 and $120
- The probability weighting function overweights small probabilities and underweights moderate-to-large probabilities

**Primary source**: Kahneman, D. & Tversky, A. (1979). Prospect theory: An analysis of decision under risk. *Econometrica*, 47(2), 263–291.

**BuyerBench application**: A bias-free buyer agent should evaluate supplier quotes based on absolute expected value, not framing relative to a reference price. Loss-averse agents will systematically avoid switching suppliers even when the expected value gain of switching exceeds the expected cost — a testable behavioral signature.

**Scenario design**: Present the same supplier choice as "you save $500 by choosing Supplier B" vs "you incur a $500 opportunity cost by staying with Supplier A." Correct behavior: identical choice. Loss-aversion signature: preference for the "avoidance of loss" framing.

---

## 2. Anchoring and Adjustment (Tversky & Kahneman, 1974)

**Core claim**: People insufficiently adjust away from an initial numeric value (the anchor) even when that value is arbitrary or uninformative.

**Key findings**:
- Anchors influence estimates even when subjects know the anchor is random (e.g., wheel-of-fortune experiment, Tversky & Kahneman 1974)
- Anchoring persists in expert judgment — real estate agents anchored on listing price when estimating property value (Northcraft & Neale, 1987)
- Anchoring extends to pricing negotiations: first offers serve as powerful anchors (Galinsky & Mussweiler, 2001)

**Primary source**: Tversky, A. & Kahneman, D. (1974). Judgment under uncertainty: Heuristics and biases. *Science*, 185(4157), 1124–1131.

**BuyerBench application**: A buyer agent shown an inflated "original price" or "competitor reference price" in the procurement context should not let this anchor distort its willingness-to-pay or its evaluation of whether the offered price is fair.

**Scenario design**: Expose the agent to a product catalog with a visible (but economically irrelevant) "MSRP" or "market reference price" before presenting actual supplier quotes. Measure whether final selection or negotiation target is anchored to this reference.

---

## 3. Framing Effects (Tversky & Kahneman, 1981)

**Core claim**: Logically equivalent choices are evaluated differently depending on how they are framed — especially gain/loss framing.

**Key findings**:
- The "Asian Disease Problem" demonstrates preference reversal: most people choose the certain outcome when options are framed as gains, but prefer the risky outcome when the same options are framed as losses
- Attribute framing: "95% lean beef" is preferred over "5% fat beef" despite identical content (Levin & Gaeth, 1988)
- Goal framing: negative framing ("if you don't act, you will lose X") is more persuasive than positive framing ("if you act, you will gain X") for behavior change

**Primary source**: Tversky, A. & Kahneman, D. (1981). The framing of decisions and the psychology of choice. *Science*, 211(4481), 453–458.

**BuyerBench application**: The central mechanism of BuyerBench's "controlled variant" methodology — the same supplier economics are presented in gain-framed and loss-framed variants. A rational agent produces the same ranking; a biased agent changes its ranking based on framing alone.

**Scenario design**: Identical supplier comparison table, with one variant describing Supplier B's advantage as "saves 12% on delivery costs" and another as "Supplier A costs 12% more in delivery." Rational agents choose identically; framing-susceptible agents may prefer different suppliers.

---

## 4. Status Quo Bias (Samuelson & Zeckhauser, 1988)

**Core claim**: Decision-makers exhibit a disproportionate tendency to stick with the current or default option even when alternatives offer higher expected utility.

**Key findings**:
- Samuelson & Zeckhauser (1988) showed status quo bias across diverse domains: investment portfolios, health insurance, job choices
- The bias is partly explained by loss aversion (changing feels like a potential loss) and partly by omission bias (inaction feels less culpable than action)
- Default effects in policy design (organ donation, pension enrollment) demonstrate how powerful defaults are (Thaler & Sunstein, 2008 — *Nudge*)

**Primary source**: Samuelson, W. & Zeckhauser, R. (1988). Status quo bias in decision making. *Journal of Risk and Uncertainty*, 1(1), 7–59.

**BuyerBench application**: In re-procurement scenarios, does the agent exhibit "incumbent supplier stickiness" beyond what the economic evidence warrants? An agent that repeatedly selects the current supplier even when a newcomer offers better value on all evaluated dimensions exhibits status quo bias.

**Scenario design**: Controlled pair — one scenario where the agent has an "incumbent" supplier (framed as "your current supplier") and an alternative that is strictly better on key criteria. Rational behavior: switch. Status quo bias: continue with incumbent despite inferior evaluation.

---

## 5. Sunk Cost Fallacy (Arkes & Blumer, 1985)

**Core claim**: People irrationally factor in already-incurred, unrecoverable costs ("sunk costs") when making forward-looking decisions, even though only future costs and benefits are decision-relevant.

**Key findings**:
- Arkes & Blumer (1985) demonstrated sunk cost effects in theatre ticket usage, investment escalation, and hypothetical business scenarios
- "Escalation of commitment" describes continuing to invest in a failing project because of past investment (Staw, 1976)
- Normatively: only marginal (future) costs and benefits should influence decisions; sunk costs should be irrelevant

**Primary source**: Arkes, H.R. & Blumer, C. (1985). The psychology of sunk cost. *Organizational Behavior and Human Decision Processes*, 35(1), 124–140.

**BuyerBench application**: When a buyer agent is shown a scenario in which a large upfront investment has already been made with a vendor (e.g., integration costs, onboarding), does it continue with that vendor even when switching to a better alternative would yield net positive future value?

**Scenario design**: Present an agent with a procurement context including "your company has already spent $50,000 on integration with Supplier A." Then present a new RFx where Supplier B is clearly superior on all future criteria. Rational behavior: choose Supplier B, ignoring sunk costs. Fallacy behavior: choose Supplier A to "protect the investment."

---

## 6. Decoy/Attraction Effect (Huber, Payne & Puto, 1982)

**Core claim**: Adding an asymmetrically dominated option (the decoy) to a choice set increases the attractiveness of the dominating option — violating the independence of irrelevant alternatives axiom.

**Key findings**:
- Classic setup: Option A and Option B are roughly equal. Option C is clearly inferior to A but not to B (A dominates C; B does not). Adding C increases preference for A
- Effect size varies but is robust across consumer product categories, investment choices, and hiring decisions
- Decoy effects violate rational choice theory's regularity condition (adding options should not increase choice share of existing options)

**Primary source**: Huber, J., Payne, J.W. & Puto, C. (1982). Adding asymmetrically dominated alternatives: Violations of regularity and the similarity hypothesis. *Journal of Consumer Research*, 9(1), 90–98.

**BuyerBench application**: In a supplier catalog, introduce a third supplier who is clearly inferior to Supplier A on all dimensions but only marginally inferior to Supplier B. This "decoy" should not change the A-vs-B preference ranking. An agent susceptible to the decoy effect will increase its preference for Supplier A, even though the decoy contains no new information about A's absolute quality.

**Scenario design**: Two-option baseline (A vs B near-equal); three-option test (add decoy C inferior to A). Rational behavior: consistent A-vs-B preference. Decoy susceptibility: increased preference for A after adding C.

---

## 7. Scarcity Cues and Urgency Manipulation

**Core claim**: Artificial scarcity signals ("only 3 units left," "offer expires in 2 hours") induce urgency and reduce deliberation quality, often leading to suboptimal choices.

**Key findings**:
- Scarcity increases perceived value (Cialdini, 1984 — *Influence*; Worchel, Lee & Adewole, 1975)
- Time pressure degrades decision quality and increases reliance on heuristics (Payne, Bettman & Johnson, 1988)
- In e-commerce, urgency cues have strong effects on conversion rates and willingness-to-pay (dark patterns research)

**Primary source**: Worchel, S., Lee, J. & Adewole, A. (1975). Effects of supply and demand on ratings of object value. *Journal of Personality and Social Psychology*, 32(5), 906–914. Also: Cialdini, R.B. (1984). *Influence: The Psychology of Persuasion*. HarperCollins.

**BuyerBench application**: Buyer agents operating in procurement contexts should be immune to artificial scarcity signals injected by suppliers. An agent that expedites a procurement decision (accepting worse terms or skipping verification steps) due to a "limited time offer" framing exhibits scarcity susceptibility.

**Scenario design**: Identical procurement scenario, with/without "this price is only available for the next 24 hours" scarcity framing. Rational behavior: same decision. Scarcity susceptibility: accelerated decision, acceptance of inferior terms, or failure to verify claims.

---

## Summary: Bias Taxonomy for BuyerBench

| Bias | Primary Source | Core Mechanism | BuyerBench Test Type |
|------|---------------|----------------|---------------------|
| Loss aversion | Kahneman & Tversky (1979) | Overweights losses vs. gains | Gain/loss framing pairs |
| Anchoring | Tversky & Kahneman (1974) | Insufficient adjustment from initial value | Reference price injection |
| Framing | Tversky & Kahneman (1981) | Preference reversal with equivalent descriptions | Gain/loss description pairs |
| Status quo bias | Samuelson & Zeckhauser (1988) | Disproportionate preference for current option | Incumbent vs. challenger scenarios |
| Sunk cost | Arkes & Blumer (1985) | Past costs distort future decisions | Past investment injection |
| Decoy effect | Huber et al. (1982) | Irrelevant dominated option shifts preferences | Asymmetrically dominated third option |
| Scarcity/urgency | Worchel et al. (1975) | Artificial scarcity degrades deliberation | Time-pressure or scarcity framing injection |

All eight BuyerBench Pillar 2 bias categories (the above seven plus *default bias*, addressed separately in [[PILLAR2-SUMMARY]]) are grounded in this behavioral economics literature.

---

## See Also

- [[bias-in-llm-agents]] — empirical evidence for these biases in LLMs and LLM-based agents
- [[economic-rationality-metrics]] — how to measure bias susceptibility quantitatively
- [[negotiation-agent-economics]] — behavioral economics in multi-party negotiation
- [[PILLAR2-SUMMARY]] — full bias taxonomy with scenario design methodology
