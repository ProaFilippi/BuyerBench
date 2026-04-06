---
type: person
title: "Amine Allouah"
created: 2026-04-06
tags:
  - researcher
  - academic
  - columbia
  - behavioral-bias
  - agentic-ecommerce
  - pillar2
related:
  - '[[ACES-AI-Agent-Buying]]'
  - '[[Omar-Besbes]]'
  - '[[NegMAS]]'
---

# Amine Allouah

> Lead author of ACES (arXiv:2508.02630), the Columbia Business School RCT benchmark that documented position bias, price elasticity distortion, and endorsement effects in AI buyer agents — the core empirical foundation for BuyerBench Pillar 2

## Role

PhD Researcher / Postdoctoral Researcher, Columbia Business School (Decision, Risk, and Operations Division)

## Background

Amine Allouah completed his PhD at Columbia Business School, concentrating in algorithmic game theory, revenue management, and decision optimization. He works within the Decision, Risk, and Operations (DRO) division — an operations research and economics group, not a traditional ML lab. This positioning explains why the ACES paper approaches AI buyer agents through the lens of **economic rationality and market microstructure** rather than capability benchmarking.

| Field | Detail |
|-------|--------|
| Institution | Columbia Business School |
| Division | Decision, Risk, and Operations (DRO) |
| Specialization | Algorithmic game theory, optimization, e-commerce |
| Affiliations | MyCustomAI (applied research) |
| Location | New York City, USA |
| Google Scholar | [Amine Allouah](https://scholar.google.com/citations?user=MY3w0CsAAAAJ&hl=en) |

## Key Contributions to Agentic Commerce

**ACES: Agentic e-CommercE Simulator** (Aug 2025, arXiv:2508.02630)

Allouah's primary contribution to the agentic commerce field is the ACES framework — a fully controlled, provider-agnostic e-commerce sandbox designed to audit AI buyer agent decision-making under realistic conditions.

### ACES Methodology

ACES operates as a mock Amazon-style marketplace that allows researchers to:
- **Control product attributes independently** (price, position, description, reviews, endorsements)
- **Run RCTs** where only one variable differs between product listings
- **Measure** whether agents make economically rational choices vs. biased ones

### Key Empirical Findings (from the paper)

| Bias Type | Measured Effect |
|-----------|----------------|
| Position bias | 5× preference for top-listed item regardless of economic merit |
| Endorsement effect | +1.0 to +1.9 price premium tolerated for "AI recommended" badge |
| Price elasticity distortion | −1.6 to −2.2 (agents over-penalize price increases) |
| Choice homogeneity | Demand concentrated on few "modal" products; most listings ignored |
| Model instability | Model updates drastically reshuffle market share with no economic basis |

### Implication for Agentic Commerce

The paper reveals a structural market risk: if AI agents systematically prefer top-positioned and "recommended" items, market power could concentrate among platforms controlling listing positions — independent of product quality or price. This is a **Pillar 2 design foundation** for BuyerBench.

## Co-Authors

- **Omar Besbes** — Columbia Business School professor (senior author); see [[Omar-Besbes]]
- **Yash Kanoria** — Columbia Business School professor, mechanism design and market microstructure
- **Josué D. Figueroa** — Columbia / applied research
- **Akshit Kumar** — Columbia Business School PhD

## Public Statements / Papers

- *"What Is Your AI Agent Buying? Evaluation, Biases, Model Dependence, & Emerging Implications for Agentic E-Commerce"* — arXiv:2508.02630, Aug 2025
- SSRN preprint: [papers.ssrn.com/sol3/papers.cfm?abstract_id=5381574](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5381574)
- Columbia Business School article: [What Happens When AI Does Your Shopping?](https://business.columbia.edu/insights/digital-future-initiative/ai-shopping-agents)

## BuyerBench Pillar Relevance

> **BuyerBench relevance:** The ACES paper is the **primary empirical source** for BuyerBench Pillar 2 scenario design. All behavioral bias categories in Pillar 2 (position bias, anchoring, framing/endorsement effects, price elasticity) map directly to Allouah et al.'s findings. BuyerBench extends their methodology by adding procedural (multi-step workflow) contexts where biases compound across decision points.

## Sources

- [arXiv:2508.02630](https://arxiv.org/abs/2508.02630)
- [Columbia Business School Directory](https://www8.gsb.columbia.edu/cbs-directory/phd/MAllouah19)
- [SSRN Paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5381574)
- [Columbia Business School Article](https://business.columbia.edu/insights/digital-future-initiative/ai-shopping-agents)
