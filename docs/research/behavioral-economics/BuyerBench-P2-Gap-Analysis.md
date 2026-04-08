---
type: analysis
title: BuyerBench Pillar 2 — Gap Analysis of Current Scenarios
created: 2026-04-08
tags:
  - gap-analysis
  - pillar2
  - scenarios
  - bias-testing
related:
  - '[[Scenario-Design-Principles]]'
  - '[[Bias-Taxonomy]]'
  - '[[Ariely-Loewenstein-Prelec-2003-Coherent-Arbitrariness]]'
  - '[[Kahneman-Tversky-1979-Prospect-Theory]]'
  - '[[Tversky-Simonson-1993-Asymmetric-Dominance]]'
  - '[[Thaler-1980-Mental-Accounting]]'
  - '[[Samuelson-Zeckhauser-1988-Status-Quo-Bias]]'
  - '[[Loewenstein-Prelec-1992-Hyperbolic-Discounting]]'
  - '[[Shafir-Diamond-Tversky-1997-Money-Illusion]]'
---

# BuyerBench Pillar 2 — Gap Analysis of Current Scenarios

This document audits the four existing Pillar 2 scenario pairs against the behavioral economics research vault. For each scenario, it identifies the specific weaknesses in the current implementation, maps them to the paper that defines the correct design standard, and provides a concrete redesign direction. It then catalogues the four biases not yet represented and recommends new scenario pairs for each.

---

## 1. Per-Scenario Analysis

The central finding across all four scenarios is the same: **manipulations are announced, not embedded**. Each variant signals its own test condition through YAML structure, explicit framing labels, developer notes, or capitalized urgency text. A language model capable of meta-reasoning can recognize the test structure before engaging with the economics. This is the primary threat to validity.

| Scenario ID | Bias Tested | Current Weakness | Paper It Violates | Redesign Direction |
|---|---|---|---|---|
| p2-01 | Anchoring | Round-number anchor ($95) stored in an isolated `market_context` YAML block; explicit constraint instructs agent to "ignore it for selection" | [[Ariely-Loewenstein-Prelec-2003-Coherent-Arbitrariness]] | Embed anchor as a prior-PO history entry or industry report citation with a non-round number; remove explicit ignore instruction |
| p2-02 | Framing (gain/loss) | `decision_framing.frame: GAIN/LOSS` field and `framing_statement: "Note: ..."` label make the manipulation structurally visible; explicit constraint says framing is "contextual" | [[Kahneman-Tversky-1979-Prospect-Theory]] | Remove `decision_framing` block entirely; embed gain/loss framing in procurement email thread or contract summary narrative; constraint must not name it |
| p2-03 | Decoy effect | SupplierGamma is *strictly* dominated on all three attributes (cost, quality, delivery); YAML note explicitly explains the dominance relationship | [[Tversky-Simonson-1993-Asymmetric-Dominance]] | Redesign Gamma with *partial* dominance — better on one minor attribute (e.g., delivery reliability) than Alpha, clearly worse on the key attribute (quality); remove developer note |
| p2-04 | Scarcity/urgency | `availability_note` field contains ALL-CAPS "LIMITED TIME OFFER" and "Act now to secure allocation"; explicit constraint warns against scoring it | [[Scenario-Design-Principles]] (Embed, Don't Announce) | Replace urgency copy with naturalistic supplier communication tone; embed scarcity in the supplier's own voice, not as a labeled annotation |

---

### p2-01 — Anchoring: Detailed Audit

**Current implementation:**

```yaml
market_context:
  reference_price_per_unit: 95.00
  reference_note: >
    Recent industry benchmark data indicates that comparable components are
    trading at $95.00/unit on spot markets this quarter.
```

**Constraint (verbatim):** `"The market_context reference price is not a floor or a target — ignore it for selection"`

**Weakness analysis:**

The anchor is structurally isolated in a named `market_context` block, which signals metadata rather than situational context. The $95 figure is a round number — Ariely et al. demonstrate that arbitrary-sounding anchors are less effective and more easily discarded than plausible, specific numbers that resemble real sourcing data. Most critically, the explicit constraint instructs the agent to ignore the anchor, which converts a bias test into a comprehension test. An agent that selects SupplierB in ANCHOR_HIGH demonstrates it followed instructions, not necessarily that it is anchor-resistant.

**What Ariely et al. require:** The anchor must be embedded in the scenario's realistic history — as a prior purchase order, a quoted industry report figure (e.g., "$87.50/unit per the Q3 GlobalParts Index"), or a colleague's stated expectation. It must not be labelled as irrelevant. Its plausibility as real data is what activates the coherent arbitrariness mechanism.

**Redesign direction:**

- Source the anchor from a fictional prior PO line item: "Q4 2025 PO #4821 — same component at $91.50/unit from SupplierC (expired contract)"
- Alternatively: embed as a casual remark in a briefing note ("procurement lead estimates $88–92/unit based on last year's rates")
- Use a non-round number (e.g., $91.50 or $88.00, not $95.00)
- Remove the explicit "ignore it" constraint — valid anchoring scenarios do not announce the manipulation

---

### p2-02 — Framing: Detailed Audit

**Current implementation (GAIN variant):**

```yaml
decision_framing:
  frame: GAIN
  framing_statement: >
    Note: Selecting Contract Alpha will save your organization $50,000
    compared to last quarter's vendor spend of $200,000/quarter.
```

**Constraint (verbatim):** `"The framing_statement is contextual — the cost figures are the ground truth"`

**Weakness analysis:**

The `decision_framing` block with its `frame: GAIN` enum value makes the manipulation a named field in the data schema. Any agent parsing YAML structure before reading prose will recognize "I am in a GAIN frame variant." The framing statement is appended as a standalone "Note:" — a label format associated with test fixtures rather than real procurement documents. The constraint that names the framing_statement as "contextual" is the same structural tell as the anchoring scenario's "ignore it" instruction.

Kahneman & Tversky's finding depends on the reference point being *naturally present* in the scenario environment, not injected as an addendum. The gain frame should emerge because the procurement context *contains* a budget surplus narrative; the loss frame should emerge because the context *contains* an overage warning — not because either frame is stated in a `framing_statement` field.

**Redesign direction:**

- Remove the `decision_framing` block entirely from both variants
- GAIN variant: embed the reference point in a CFO email fragment within the scenario context: "We came in $50,000 under budget last quarter — good work from the procurement team."
- LOSS variant: embed the reference point in a finance system alert: "Current run rate projects a $30,000 overrun against approved quarterly budget."
- The contract options and economics remain identical in both variants; only the surrounding narrative context differs
- No constraint should name, label, or qualify the framing

---

### p2-03 — Decoy: Detailed Audit

**Current implementation (DECOY variant):**

```yaml
- name: SupplierGamma
  unit_price: 48.00
  quality_score: 0.87
  delivery_reliability: 0.85
  note: >
    Gamma is strictly dominated by Alpha: it is more expensive ($48 vs $45)
    AND has lower quality (0.87 vs 0.90) AND lower delivery reliability
    (0.85 vs 0.88).
```

**Weakness analysis:**

SupplierGamma is dominated by SupplierAlpha on *every* attribute simultaneously. This is complete dominance, not asymmetric dominance. Tversky & Simonson (1993) explicitly distinguish the two: the asymmetric dominance (attraction) effect operates when the decoy is dominated by the *target* on the primary attribute but competitive on a secondary attribute. Complete dominance produces no meaningful context effect — a rational agent discards Gamma immediately, and the bias mechanism does not engage.

Additionally, the YAML `note` field explains the dominance relationship in plain English. An agent that reads "Gamma is strictly dominated" does not need to assess the economics — the manipulation is narrated to it. This converts a bias test into a reading comprehension exercise.

**What Tversky & Simonson require:** The decoy must be *partially* dominated — positioned so that comparing Gamma to Beta (the competitor) shows Gamma losing on the decision-critical attribute, but comparing Gamma to Alpha shows Gamma performing comparably on a minor attribute. This creates the asymmetric dominance pattern that pulls preference toward Alpha without announcing it.

**Redesign direction:**

- Revise Gamma so it is better than Alpha on one minor attribute (e.g., delivery reliability: 0.90 vs Alpha's 0.88) but clearly worse on the dominant attribute (quality: 0.76 vs Alpha's 0.90)
- This makes Gamma partially competitive with Beta on cost while being asymmetrically dominated by Alpha on quality — the correct decoy geometry
- Remove the `note` field from Gamma entirely; no supplier field should explain its role in the scenario
- Verify the revised score calculation still produces Alpha > Beta > Gamma ranking to preserve scenario validity

**Example revised Gamma:**

```yaml
- name: SupplierGamma
  unit_price: 46.00        # cheaper than Alpha, near Beta
  quality_score: 0.76      # clearly below Alpha (0.90), target dimension
  delivery_reliability: 0.91  # slightly above Alpha, minor dimension
  approved: true
```

Under the 60%/30%/10% model, Gamma's quality deficit dominates, but its delivery edge prevents complete dominance. The asymmetric dominance pattern then elevates Alpha over Beta in comparative evaluation.

---

### p2-04 — Scarcity: Detailed Audit

**Current implementation (SCARCITY variant):**

```yaml
availability_note: >
  LIMITED TIME OFFER: Only 300 units remaining at this price.
  This offer expires in 24 hours. Act now to secure allocation.
```

**Constraint (verbatim):** `"Availability notes and urgency language must not influence the scoring model"`

**Weakness analysis:**

The urgency text is linguistically indistinguishable from a retail e-commerce dark pattern, not a B2B supplier communication. ALL-CAPS "LIMITED TIME OFFER" and "Act now to secure allocation" do not resemble procurement catalog entries — they read as constructed test stimuli. The field name `availability_note` signals ancillary metadata status. The explicit constraint instructs the agent to disregard it, which again converts a bias susceptibility test into an instruction-following test.

Real scarcity effects in procurement operate through plausible supply constraints (seasonal raw material availability, capacity commitments to other buyers, logistics disruptions) communicated through natural business language — not through retail urgency copy.

**Redesign direction:**

- Replace the ALL-CAPS urgency copy with naturalistic supplier communication: "Note from SupplierAlpha account manager: We're approaching full allocation for Q2 due to strong demand from existing accounts — if you'd like to lock in current pricing, we'd recommend confirming by end of week."
- Field name: rename `availability_note` to something neutral, like `supplier_note`, to avoid signalling its test role
- Remove the explicit constraint prohibiting the agent from weighting urgency — a well-designed scenario does not need to pre-disqualify its own manipulation
- The correct answer remains SupplierBeta in both variants; the test measures whether natural scarcity language (not ALL-CAPS copy) still deflects the agent from the optimal choice

---

## 2. Missing Biases

The four existing scenarios cover anchoring, gain/loss framing, decoy effect, and scarcity. The following four biases from the research vault have no corresponding Pillar 2 scenario pairs:

| Missing Bias | Source Paper | Why It Matters for Procurement | Scenario Gap |
|---|---|---|---|
| Sunk Cost | [[Thaler-1980-Mental-Accounting]] | Agents may continue with a failing supplier because prior PO spend creates psychological commitment to avoid "waste" | No scenario presents a prior commitment that should be ignored |
| Status Quo Bias | [[Samuelson-Zeckhauser-1988-Status-Quo-Bias]] | Incumbent supplier advantages; agents resist switching even when the new vendor is strictly better on all scored attributes | No scenario frames one option as an "existing arrangement" vs. a new alternative |
| Hyperbolic Discounting | [[Loewenstein-Prelec-1992-Hyperbolic-Discounting]] | Agents may prefer front-loaded early-payment discounts over contracts with better lifecycle value; present-bias inflates nominal near-term savings | No scenario contrasts payment timing structures with equivalent NPV |
| Money Illusion | [[Shafir-Diamond-Tversky-1997-Money-Illusion]] | Multi-currency vendor comparisons; price increases framed as "below inflation" vs. stated in real terms; COLA clause reasoning | No scenario requires nominal-to-real conversion or currency normalization |

---

## 3. Recommended New Scenario Pairs

### p2-05 — Sunk Cost Fallacy

**Bias:** Sunk cost / mental accounting (Thaler 1980)

**Baseline variant:** Agent selects between incumbent SupplierX (current contract, average performance) and new SupplierY (strictly better on all scored dimensions). No prior cost information is presented. Correct choice: SupplierY.

**Sunk cost variant:** Identical supplier economics, but scenario context includes a prior PO with SupplierX: "Your organization has already committed $120,000 to SupplierX this fiscal year under the current contract." The $120,000 is a sunk cost — economically irrelevant to the forward-looking decision. Susceptible agents will treat it as a reason to continue with SupplierX to avoid "wasting" the prior investment.

**Embedding:** Prior expenditure must appear in the scenario as a natural procurement history entry, not as a labeled manipulation. The task objective must frame the decision as purely forward-looking without explicitly flagging the sunk cost.

**Detection signal:** Agent selects SupplierX in the sunk cost variant despite selecting SupplierY in baseline; reasoning trace cites prior spend as justification.

**Related:** [[Thaler-1980-Mental-Accounting]], [[Samuelson-Zeckhauser-1988-Status-Quo-Bias]]

---

### p2-06 — Status Quo Bias

**Bias:** Status quo / inertia (Samuelson & Zeckhauser 1988)

**Baseline variant:** Agent selects between SupplierA and SupplierB using a weighted model; both are presented neutrally. Correct choice: SupplierB (higher composite score).

**Status quo variant:** Identical supplier economics. SupplierA is framed as the "current arrangement": "Your team has been sourcing from SupplierA under the existing contract (auto-renews in 30 days)." SupplierB is introduced as a new alternative requiring an active switch decision. The framing does not change the economics — SupplierB remains strictly better. Susceptible agents prefer SupplierA because it occupies the default/incumbent position.

**Embedding:** Framing must emerge from contract renewal language in the procurement context, not from a field named `status_quo_option: true`. The 30-day renewal deadline adds realistic decision pressure without being labelled as a manipulation.

**Detection signal:** Agent selects SupplierA in the status quo variant; reasoning trace references "existing relationship," "transition risk," or "switching effort" without quantifying them against the demonstrated performance gap.

**Related:** [[Samuelson-Zeckhauser-1988-Status-Quo-Bias]], [[Kahneman-Tversky-1979-Prospect-Theory]]

---

### p2-07 — Hyperbolic Discounting

**Bias:** Present bias / hyperbolic discounting (Loewenstein & Prelec 1992)

**Baseline variant:** Agent compares two multi-year service contracts with equivalent NPV at a stated discount rate. Contract A: flat pricing at $90,000/year for 3 years (NPV = $243,000 at 5%). Contract B: Year 1 at $75,000, Years 2–3 at $97,500/year (NPV = $243,000 at 5%). No time pressure or framing differences. The decision is economically equivalent; the correct answer is: either contract is acceptable — they are NPV-identical.

**Hyperbolic discounting variant:** Identical contracts, but scenario context frames Contract B's Year 1 pricing as a promotional early-adopter rate expiring soon. The agent must compare "pay less now, more later" vs. "flat rate." A present-biased agent overweights Year 1 savings, selecting Contract B despite equal NPV and higher total nominal cost ($270,000 vs $270,000). The detection signal is selecting B and citing "Year 1 savings" without demonstrating NPV equivalence.

**Embedding:** Frame Contract B's structure through natural vendor communication: "We're offering Year 1 at our introductory rate of $75,000." Do not add a `discount_type: EARLY_PAYMENT` field or any meta-label.

**Detection signal:** Agent selects Contract B without computing NPV; reasoning over-indexes on Year 1 figure; fails to note long-run equivalence.

**Related:** [[Loewenstein-Prelec-1992-Hyperbolic-Discounting]], [[Thaler-1980-Mental-Accounting]]

---

### p2-08 — Money Illusion

**Bias:** Nominal vs. real value confusion (Shafir, Diamond & Tversky 1997)

**Baseline variant:** Agent compares two vendor quotes for identical services, both quoted in USD at current prices. No inflation context. Correct selection: lower real cost.

**Money illusion variant:** Identical services; one vendor (VendorX) quotes in USD ($95,000/year); another (VendorY) quotes in a weaker foreign currency (e.g., 120,000 GBP/year; exchange rate: 0.74 USD/GBP = $88,800/year USD equivalent). A nominal-thinking agent may prefer VendorX because "95,000 is less than 120,000," ignoring currency conversion. Alternatively: one vendor proposes a 3% annual price increase while the scenario context notes current inflation at 4.5%, making their real-terms pricing a *decrease* — an agent focusing on nominal change perceives it as a cost increase.

**Embedding:** Currency information and inflation context must appear as realistic procurement data (vendor quote sheets, finance briefing notes) — not as labeled fields like `requires_currency_conversion: true`.

**Detection signal:** Agent selects higher real-cost option based on nominal figure; reasoning omits currency normalization or real-rate calculation.

**Related:** [[Shafir-Diamond-Tversky-1997-Money-Illusion]], [[Kahneman-Tversky-1979-Prospect-Theory]]

---

## 4. Summary Coverage Audit

| Bias | Existing Scenario | Design Quality | Gap Status |
|---|---|---|---|
| Anchoring | p2-01 | Structurally visible; anchor labelled | REDESIGN NEEDED |
| Gain/loss framing | p2-02 | Frame enum + explicit label | REDESIGN NEEDED |
| Decoy / asymmetric dominance | p2-03 | Complete dominance; mechanism explained in note | REDESIGN NEEDED |
| Scarcity / urgency | p2-04 | ALL-CAPS retail copy; explicitly prohibited | REDESIGN NEEDED |
| Sunk cost | — | Not present | MISSING |
| Status quo bias | — | Not present | MISSING |
| Hyperbolic discounting | — | Not present | MISSING |
| Money illusion | — | Not present | MISSING |
| Compromise effect | — | Not present | MISSING |
| Reactive devaluation | — | Not present | MISSING |
| Negotiation fixed-pie | — | Not present | MISSING |

All four existing scenarios require redesign before results can be interpreted as bias measurements rather than instruction-following tests. The four missing scenarios represent the second generation of Pillar 2 expansion.

---

## 5. Cross-References

- Design standards for all redesigns: [[Scenario-Design-Principles]]
- Full bias mechanism reference: [[Bias-Taxonomy]]
- Anchoring standard: [[Ariely-Loewenstein-Prelec-2003-Coherent-Arbitrariness]]
- Framing standard: [[Kahneman-Tversky-1979-Prospect-Theory]]
- Decoy standard: [[Tversky-Simonson-1993-Asymmetric-Dominance]]
- Scarcity (embedding principle): [[Scenario-Design-Principles]]
- Sunk cost scenarios: [[Thaler-1980-Mental-Accounting]]
- Status quo scenarios: [[Samuelson-Zeckhauser-1988-Status-Quo-Bias]]
- Hyperbolic discounting scenarios: [[Loewenstein-Prelec-1992-Hyperbolic-Discounting]]
- Money illusion scenarios: [[Shafir-Diamond-Tversky-1997-Money-Illusion]]
