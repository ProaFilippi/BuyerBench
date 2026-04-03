---
type: research
title: Supplier Selection — Academic and Applied Literature
created: 2026-04-03
tags:
  - pillar1
  - supplier-selection
  - optimization
  - procurement
related:
  - '[[procurement-ai-survey]]'
  - '[[workflow-completion-metrics]]'
  - '[[PILLAR1-SUMMARY]]'
---

# Supplier Selection — Academic and Applied Literature

## Overview

Supplier selection is one of the most-studied problems in operations management and procurement research. The challenge: select one or more suppliers from a candidate set based on multiple, often conflicting criteria (price, quality, delivery reliability, capacity, compliance). This body of literature provides the **formal grounding for what "optimal" means** in BuyerBench Pillar 1 scenarios.

---

## Multi-Criteria Decision Making (MCDM)

The supplier selection problem is a canonical MCDM problem. The general formulation:

- **Decision alternatives**: a set of n suppliers {S₁, S₂, ..., Sₙ}
- **Criteria**: a set of m attributes {C₁, C₂, ..., Cₘ} (price, delivery time, quality, compliance, etc.)
- **Weights**: importance weights {w₁, w₂, ..., wₘ} reflecting buyer preferences
- **Objective**: rank or select the alternative(s) that best satisfy the weighted criteria

The richness of the MCDM literature gives BuyerBench a well-validated mathematical basis for defining "the correct answer" — the agent's selection can be compared against the MCDM-optimal solution.

---

## Key Methods

### Analytic Hierarchy Process (AHP)
**Origin**: Saaty (1980)  
**Approach**: Decomposes the decision into a hierarchy: goal → criteria → sub-criteria → alternatives. Pairwise comparisons between criteria yield a consistency-checked weight vector. Suppliers are then scored against each criterion.

**Relevance to BuyerBench**: AHP-derived criterion weights can be embedded in scenario specifications (e.g., "quality is twice as important as price") to define ground-truth optimal choices without ambiguity.

**Limitation**: Requires consistent pairwise comparisons; inconsistency is measurable (consistency ratio). In BuyerBench, this is a feature — we can test whether agents respect declared criterion weights.

### TOPSIS (Technique for Order Preference by Similarity to Ideal Solution)
**Origin**: Hwang & Yoon (1981)  
**Approach**: Each alternative is scored by its geometric distance from the "ideal best" (best value on all criteria) and "ideal worst" (worst value on all criteria). Ranking is by closeness to the ideal best.

**Relevance to BuyerBench**: TOPSIS provides a deterministic ranking for any normalized supplier comparison matrix. It is the recommended "ground truth oracle" for BuyerBench Pillar 1 scoring because:
- It handles mixed criteria (lower is better for price; higher is better for quality)
- It produces a total order (ties are possible but rare with continuous attributes)
- It is auditable and replicable given the input matrix

### VIKOR (VIseKriterijumska Optimizacija I Kompromisno Resenje)
**Origin**: Opricovic (1998)  
**Approach**: Similar to TOPSIS but focuses on maximizing group utility and minimizing individual regret. Useful when there is no single dominant alternative — returns a compromise solution.

**Relevance to BuyerBench**: VIKOR-based scoring is useful when scenarios intentionally have no single dominant supplier (testing whether the agent identifies and selects the compromise choice correctly).

### Data Envelopment Analysis (DEA)
**Origin**: Charnes, Cooper & Rhodes (1978)  
**Approach**: Identifies the efficient frontier — suppliers that cannot be strictly dominated by any linear combination of other suppliers. Efficient suppliers are rated 1.0; inefficient ones receive a score < 1.0.

**Relevance to BuyerBench**: DEA can identify scenarios where multiple suppliers are Pareto-optimal — testing whether the agent correctly recognizes a multi-winner scenario rather than forcing a single selection.

### Fuzzy Set Methods
Extends MCDM methods to handle uncertain or linguistic criteria (e.g., "supplier quality is HIGH, delivery reliability is MEDIUM"). Fuzzy AHP and Fuzzy TOPSIS are widely used in procurement research.

**Relevance to BuyerBench**: Introduces epistemic uncertainty into scenarios — agents must reason under partial information, which is realistic in procurement contexts.

---

## The Supplier Selection as a Constraint Satisfaction Problem

Beyond MCDM, supplier selection often involves hard constraints:
- **Budget ceiling**: total spend must not exceed X
- **Approved vendor lists (AVL)**: only pre-approved suppliers are eligible
- **Delivery deadlines**: supplier must meet required delivery date
- **Minimum order quantities (MOQ)**: some suppliers require minimum order sizes
- **Geographic restrictions**: regulatory or policy limits on supplier country of origin

This constraint layer converts the selection problem from pure optimization to **constrained optimization** — and provides BuyerBench with a natural mechanism for testing compliance enforcement (an agent that violates an AVL constraint is failing both capability *and* compliance).

---

## Behavioral Factors in Real Supplier Selection

Academic literature also documents how human procurement decisions deviate from MCDM optima:

- **Anchoring**: negotiators anchor on the first price they see, even when it's arbitrary
- **Relationship bias**: existing suppliers receive preference even when new suppliers are objectively superior
- **Risk aversion**: buyers prefer lower-variance suppliers even when higher-variance options have better expected value
- **Attribute weighting drift**: stated criterion weights differ from revealed preferences in practice

These behavioral factors are directly relevant to BuyerBench Pillar 2: the hypothesis is that AI buyer agents may replicate human behavioral biases, not merely calculate MCDM optima.

---

## Grounding BuyerBench Scenarios in MCDM

For each Pillar 1 scenario, the ground-truth "optimal" supplier selection is defined using the following process:
1. Construct the supplier attribute matrix (normalized scores per criterion)
2. Apply declared criterion weights
3. Compute TOPSIS ranking
4. Identify the top-ranked supplier as the ground-truth optimal
5. Agent's selection is scored against this ground truth (exact match = full credit; adjacent rank = partial credit)

This gives BuyerBench an objective, defensible scoring basis for capability evaluation.

---

## See Also

- [[procurement-ai-survey]] — enterprise procurement AI capability claims
- [[workflow-completion-metrics]] — how multi-step procurement completion is measured
- [[PILLAR1-SUMMARY]] — synthesis and implications for scenario design
