---
type: research-paper
title: "ACES — Agentic e-CommercE Simulator: AI Buyer Agent Bias Evaluation Framework"
created: 2026-04-05
tags:
  - benchmark
  - buyer-agent
  - behavioral-bias
  - evaluation
  - pillar-2
  - position-bias
  - anchoring
  - e-commerce
  - rct
related:
  - '[[AgentBench]]'
  - '[[WebShop]]'
  - '[[WebArena]]'
  - '[[Fairmarkit]]'
  - '[[INDEX]]'
---

# ACES (Agentic e-CommercE Simulator)

> The first randomized-controlled-trial benchmark for AI buyer agent behavioral bias — measuring position bias, endorsement effects, price elasticity, and seller manipulation susceptibility across frontier models

## Citation

**Full title:** "What Is Your AI Agent Buying? Evaluation, Biases, Model Dependence, & Emerging Implications for Agentic E-Commerce"

| Field | Value |
|-------|-------|
| Authors | Amine Allouah, Omar Besbes, Josué D Figueroa, Yash Kanoria, Akshit Kumar |
| arXiv ID | [2508.02630](https://arxiv.org/abs/2508.02630) |
| Submitted | August 4, 2025 |
| Latest revision | December 17, 2025 (v3) |
| Subject areas | cs.AI, cs.CY, cs.HC, cs.MA, econ.GN |
| Venue | arXiv preprint (not yet published at a named conference as of 2026-04-05) |
| Institutional affiliations | Columbia University (Business School) |

## Abstract Summary

ACES examines how autonomous AI agents make purchasing decisions on e-commerce platforms. The paper's central finding is that agents exhibit **choice homogeneity** — concentrating demand on a small number of "modal" products while ignoring alternatives — and that these preferences shift substantially and unpredictably with model version updates. Agents demonstrate strong position biases, sponsor tag penalties, and platform endorsement rewards in ways that would distort competitive markets if AI-mediated shopping scales broadly. The paper frames its contribution as "Algorithmic Economic Auditing" — a governance methodology for detecting market distortions caused by AI buying agents.

> **BuyerBench relevance (Pillar 2):** ACES is the primary academic precedent for BuyerBench's Pillar 2 design. Its controlled-variant methodology — holding product economics constant while randomizing presentation attributes — directly validates BuyerBench's approach to measuring bias susceptibility indices. Every BuyerBench Pillar 2 scenario involving framing variants, decoy options, or scarcity cues should cite ACES as its methodological foundation. The paper's quantitative bias coefficients (position effect magnitudes, endorsement multipliers, price elasticity estimates) should serve as calibration benchmarks for BuyerBench's own bias scoring.

> **BuyerBench relevance (Pillar 1):** ACES's "instruction following and basic rationality" test suite maps directly to Pillar 1 capability assessment. Their finding that latest models achieve near-zero errors on price/rating comparisons (vs. 9–71.7% failure rates in earlier versions) provides a performance trajectory benchmark for Pillar 1 scoring on supplier comparison tasks.

## Key Findings

### Position Bias

Agents exhibit dramatic sensitivity to the spatial position of product listings — persisting even in text-only "headless" interfaces where no visual rendering occurs:

| Effect | Magnitude |
|--------|-----------|
| Position uplift (bottom-right → top-row) | 5× increase in selection probability (Claude Sonnet 4) |
| Persistence in headless mode | Yes — text-only interfaces show the same position ordering bias |
| Consistency across models | Varies significantly by provider and model version |

### Sponsored Tag Penalty

All tested models systematically penalize listings tagged as sponsored:

| Model | Coefficient | Selection rate impact (from 10% baseline) |
|-------|-------------|------------------------------------------|
| Range across all models | −0.135 to −0.371 | 7.9–8.9% (reduction of ~1–2.1pp) |

### Platform Endorsement Reward ("Overall Pick" badge)

The largest single bias effect in the dataset — platform endorsements dramatically amplify selection:

| Model | Coefficient | Selection rate impact (from 10% baseline) |
|-------|-------------|------------------------------------------|
| Range across all models | +1.060 to +1.897 | 19.9–42.6% (2–4× baseline) |

This means a platform's choice of which product to badge "Overall Pick" can shift AI-mediated market share by an order of magnitude — raising significant governance concerns.

### Price Elasticity

| Metric | Estimate |
|--------|----------|
| Price elasticity of agent demand | −1.6 to −2.2 (varies by model) |

Consistent directionally with rational economic behavior, but with substantial cross-model variance suggesting the "rationality" is unstable.

### Rating Sensitivity

| Metric | Estimate |
|--------|----------|
| Rating coefficient range | +4.224 to +11.148 |
| Interpretation | A +0.1 rating point increases selection probability by 5–67% depending on model |

### Model Volatility (Market Share Instability)

A defining feature of ACES findings: AI-mediated markets are far more volatile than human-driven markets.

| Category | Model | Market share |
|----------|-------|-------------|
| Fitbit Inspire | Claude Sonnet 4 (Aug 2025) | 45% |
| Fitbit Inspire | Claude upgrade (Dec 2025) | 77% |
| Fitbit Inspire | GPT upgrade (Dec 2025) | 6% |

A single model version update can shift market share by 39–71 percentage points — a fragility with major implications for sellers and platform governance.

### Rationality Improvement Over Time

| Model generation | Error rate on marginal price/rating comparisons |
|-----------------|-------------------------------------------------|
| Earlier models (Aug 2025 cohort) | 9–71.7% error |
| Latest models (Dec 2025 cohort) | Near-zero error |

Frontier models are converging toward basic rationality on explicit comparisons, but structural biases (position, endorsement) persist independently.

### Seller Manipulation Susceptibility

One-shot AI-generated product description rewrites (without changing price or quality) produced statistically significant market share gains in 5 of 6 tested buyer models:

| Category | Share gain (pp) |
|----------|-----------------|
| Typical gain | +3.66 to +14.89 pp |
| Office lamp category (high variation) | +7.1 to +80.4 pp |

This documents a concrete manipulation attack surface: adversarial sellers can exploit AI buyer agent biases through description engineering without legitimate product improvement.

## Methodology

### Experimental Design

ACES uses **randomized controlled trials (RCTs)** — the gold standard for causal inference — rather than observational task-completion scoring used by most prior agent benchmarks:

- **Unit of observation:** A single product selection decision from a simulated 8-product 2×4 grid
- **Trials per category:** 500 randomized trials
- **Randomization scope:** Product position (all 8 positions shuffled uniformly), tag assignment (Sponsored / Overall Pick / scarcity labels), attribute values (price multipliers log-normal σ=0.3, ratings ±0.8 variance, review counts log-normal σ=1.0)
- **Identification strategy:** Exogenous variation independent of product quality — isolates causal effects cleanly
- **Statistical model:** Conditional logit regression on individual-level choice data

This design means ACES measures *why* agents make choices (causal) rather than merely *what* choices they make (descriptive) — a critical methodological distinction for BuyerBench's bias susceptibility scoring.

### Controlled Variants

ACES's controlled-variant approach: **identical products, randomized presentation** — allowing direct estimation of bias coefficients without confounding from product quality differences. This is the ACES analog of BuyerBench's framing/decoy variant design in Pillar 2.

### Models Tested

**August 2025 cohort:**
- Claude Sonnet 4
- GPT-4.1
- Gemini 2.5 Flash

**December 2025 cohort (revision v3):**
- Claude Opus 4.5
- GPT-5.1
- Gemini 3.0 Pro Preview

### Evaluation Dimensions vs. Prior Benchmarks

| Dimension | ACES | AgentBench / WebArena | WebShop |
|-----------|------|-----------------------|---------|
| **Focus** | Single product-selection step (causal) | End-to-end web navigation | Instruction-following product search + purchase |
| **Methodology** | RCTs + conditional logit regression | Task completion scoring (binary/partial) | Reward-based scoring |
| **Metrics** | Causal bias coefficients, market concentration, elasticity | Task success rate, efficiency | Score (0–1), human comparison |
| **Domain** | E-commerce choice behavior | Multi-domain web tasks | Amazon product search |
| **Sample size** | 500 trials per category × multiple models | Fixed task sets | Fixed task sets |
| **Insight type** | Causal (why agents choose what they choose) | Capability (can agents complete tasks) | Capability + partial quality |

ACES's self-described positioning: "our emphasis is different: rather than evaluating end-to-end web navigation, we focus on a single critical step — selecting which product to buy."

## Datasets Used

ACES uses a **simulated e-commerce environment** rather than a live scrape:

- Products drawn from real Amazon listings (categories include consumer electronics, fitness trackers, office supplies, and others)
- 8-product grids per shopping session (2×4 layout)
- Product attributes (price, rating, reviews, tags) varied synthetically within realistic ranges
- No proprietary dataset — the evaluation environment is fully synthetic, making it reproducible without Amazon API access

The simulation approach is a key design choice: it enables the RCT randomization that observational data cannot support, at the cost of ecological validity (lab vs. field).

## Implications for BuyerBench Pillar 2 Design

### 1. Adopt RCT-Based Variant Design

ACES validates the controlled-variant approach for bias measurement. BuyerBench Pillar 2 scenarios should hold underlying economics identical across variants and randomize only presentation features (framing, ordering, labeling, decoys).

### 2. Calibrate Bias Scoring Against ACES Coefficients

The ACES coefficients (position effects: ~5× probability shift; endorsement effects: +1.0 to +1.9; price elasticity: −1.6 to −2.2) provide empirical anchors for BuyerBench's bias susceptibility scoring. A BuyerBench result showing 2× position sensitivity is "below ACES levels"; 6× is "above ACES levels."

### 3. Test Both Explicit Rationality and Structural Biases

ACES reveals a dissociation: latest models are nearly rational on explicit comparisons but still highly susceptible to structural biases (position, endorsement). BuyerBench Pillar 2 must test both dimensions separately — rationality tests ≠ bias tests.

### 4. Include Model-Version Drift as a Scenario

ACES's market volatility findings suggest BuyerBench should track scores across model versions, not just agents. A Pillar 2 supplementary metric: "market share volatility coefficient" across 2 model versions of the same agent.

### 5. Document Seller Adversarial Manipulation Attack Surface

ACES shows description-engineering attacks yield +3–80pp market share gains. BuyerBench Pillar 2 (and potentially Pillar 3) should include adversarial scenario variants testing agent susceptibility to manipulated product descriptions.

### 6. Frame Output as "Algorithmic Economic Auditing"

ACES's governance framing — continuous, counterfactual auditing to detect competitive distortions — should inform BuyerBench's evaluation output format. Rather than just scoring agents, BuyerBench should produce market-level reports: which biases, at what magnitudes, create which distortions.

## Related Entities
- [[AgentBench]] — Multi-environment LLM agent benchmark; ACES is scoped more narrowly to buying decisions but with causal methodology AgentBench lacks
- [[WebShop]] — Foundational shopping benchmark; ACES cites WebShop as prior art and extends it with causal RCT design
- [[WebArena]] — Web navigation benchmark with e-commerce domain; ACES explicitly distinguishes its focus from WebArena's end-to-end navigation approach
- [[Fairmarkit]] — AI procurement vendor; ACES's bias findings are directly relevant to evaluating whether tools like Fairmarkit's AI recommendation engine exhibits similar position/endorsement biases in B2B contexts
- [[LLM-Agent-Benchmarking-Survey]] — Survey of LLM agent evaluation methodologies; ACES represents the economics-first approach the survey classifies as underrepresented

## Sources

1. [ACES arXiv abstract (2508.02630)](https://arxiv.org/abs/2508.02630) — Accessed 2026-04-05
2. [ACES full paper HTML](https://arxiv.org/html/2508.02630) — Accessed 2026-04-05

---
*Last updated: 2026-04-05*
