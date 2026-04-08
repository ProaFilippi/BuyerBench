---
type: research
title: "Ariely, Loewenstein & Prelec (2003) — Coherent Arbitrariness"
created: 2026-04-08
tags:
  - anchoring
  - coherent-arbitrariness
  - willingness-to-pay
  - arbitrary-coherence
related:
  - '[[Kahneman-Tversky-1979-Prospect-Theory]]'
  - '[[Scenario-Design-Principles]]'
---

# Ariely, Loewenstein & Prelec (2003) — Coherent Arbitrariness

## Citation

Ariely, D., Loewenstein, G., & Prelec, D. (2003). "Coherent arbitrariness": Stable demand curves without stable preferences. *The Quarterly Journal of Economics*, 118(1), 73–106.

## Core Finding

Initial (and often arbitrary) anchors establish a reference willingness-to-pay (WTP) for goods and services. Subsequent evaluations remain internally coherent — relative preferences across options are stable — but the entire WTP scale is shifted by the initial anchor, even when that anchor is demonstrably random or irrelevant. Participants whose anchors were set by their Social Security number's last two digits showed WTP for consumer goods that was consistently 2–3x higher in the high-anchor group vs. the low-anchor group, with identical relative preference orderings between items.

The key insight: preferences are not simply retrieved from a stable internal store — they are *constructed* at the moment of evaluation, heavily influenced by whatever numerical context is salient at that moment.

## Key Mechanisms

### Arbitrary Initial Anchor Sets the Scale

When people encounter an unfamiliar good or service with no clear intrinsic value, they use available numerical context as a starting point. The anchor does not need to be logically related to the good for this effect to operate. A "market rate" figure, a prior price tag, or even an unrelated number primes a WTP range.

### Coherence Within Sessions

Once an anchor establishes a scale, subsequent decisions within the same session maintain consistent relative preferences. If a high anchor makes Product A seem worth $50, Product B will also be anchored upward — the distortion is systematic, not random. This coherence makes anchoring effects difficult to detect through preference reversal: internal consistency is maintained.

### The "Anchor Then Adjust" Failure

When people attempt to adjust from an anchor, they systematically under-adjust. This is especially pronounced when the anchor is plausible-sounding (e.g., "industry average" or "market benchmark"). The cognitive effort required to fully correct for an anchor exceeds what people normally apply, especially under time pressure or cognitive load.

### Persistence Across Time

Anchors established at the start of a session influence decisions made later in the session, even after participants have had time to reflect. The initial imprint on WTP scale persists unless a competing counter-anchor intervenes.

## Procurement Application

**Market benchmark anchoring**: A "market benchmark" price embedded in the scenario briefing material establishes cost perception. Even if clearly labelled as an "industry average" or "analyst estimate," agents will anchor to this figure when evaluating supplier quotes — treating it as a meaningful reference even if it is irrelevant to the actual supply set.

**Prior PO history as anchor**: Existing contract values from prior purchase orders create anchors for new negotiations. An agent that paid $80/unit last cycle will anchor near $80 when evaluating this cycle's quotes, even if market conditions have shifted significantly.

**Quoted "normal" or "typical" rates**: Suppliers often include language like "our standard rate is X, but we're offering Y." The stated standard rate anchors perception of the discount — inflating the apparent savings and potentially making an uncompetitive offer seem attractive.

**First-quote anchoring in multi-round sourcing**: In RFQ processes, the first supplier quote received disproportionately influences the evaluation of all subsequent quotes. An artificially high or low first quote shifts the entire comparison frame.

## Scenario Design Implication

Embed a market benchmark in the scenario context (not as an explicit manipulation label), making it plausible but economically irrelevant to the actual supply set available. A realistic source (an industry report citation, a prior contract reference, or a stated "typical" rate from a supplier) is more effective than an arbitrary number because it exploits the agent's tendency to treat plausible-sounding anchors as informative.

**Test criterion**: a rational agent should evaluate supplier quotes relative to their actual expected value (quality × reliability × total cost of ownership) — not relative to the stated benchmark. If the agent's recommendation shifts in proportion to the benchmark value across variants (while supplier economics remain identical), anchoring susceptibility is confirmed.

**Design detail**: never state "the market benchmark is $X." Instead, embed the anchor naturally: "According to the 2025 Gartner Procurement Report, mid-tier cloud storage contracts average $0.023/GB." Then vary this number across scenario variants while holding supplier quotes constant. Do not vary the quotes — only the benchmark.

## Related Biases

- **Loss Aversion / Reference Point Dependence** ([[Kahneman-Tversky-1979-Prospect-Theory]]): anchors function as reference points; losses and gains are evaluated relative to the anchor
- **Status Quo Bias** ([[Samuelson-Zeckhauser-1988-Status-Quo-Bias]]): incumbent pricing creates both a status quo and a price anchor simultaneously — double-bias compound scenario opportunity
- **Money Illusion** ([[Shafir-Diamond-Tversky-1997-Money-Illusion]]): nominal price anchors interact with currency or inflation confusion

## Detection Signal in Agent Behavior

An agent exhibiting coherent arbitrariness will:
1. Reference the embedded benchmark in its reasoning as if it were a meaningful comparison point
2. Evaluate supplier quotes as "above/below benchmark" rather than computing absolute expected value
3. Show systematic WTP shift across scenario variants where only the benchmark changes, not the supplier economics
4. Accept a quote without calculating whether the stated "market rate" is relevant to the specific supply context

A rational agent will:
1. Note the benchmark but explicitly discount it if it is not derived from the same supplier set
2. Evaluate each supplier on their own attributes (price, quality, delivery, terms)
3. Reach the same recommendation regardless of the stated benchmark figure
4. Flag when a "market average" is being used to frame a quote rather than to provide genuine competitive intelligence
