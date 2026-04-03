---
type: analysis
title: Research Gaps BuyerBench Addresses — Cross-Pillar Synthesis
created: 2026-04-03
tags:
  - gaps
  - motivation
  - contribution
related:
  - '[[PILLAR1-SUMMARY]]'
  - '[[PILLAR2-SUMMARY]]'
  - '[[PILLAR3-SUMMARY]]'
  - '[[INDEX]]'
---

# Research Gaps BuyerBench Addresses — Cross-Pillar Synthesis

## Purpose

This document identifies the 7 most significant research gaps across the three BuyerBench literature pillars that the benchmark directly addresses. Each gap is stated as a falsifiable claim, grounded in specific literature findings, and paired with BuyerBench's response. This synthesis forms the core "motivation" argument for the paper's Introduction and Related Work sections.

---

## Gap 1 — No Open-Source Third-Party Benchmark for AI Buyer Agents

**The gap**: All four major enterprise procurement AI platforms (SAP/Joule/Ariba, Coupa, Ivalua IVA, Zip) publish capability claims with no independent, publicly replicable evaluation. The only evaluation data that exists comes from vendor self-reporting. There is no academic or open-source benchmark analogous to SWE-bench or GAIA that targets the procurement buyer workflow domain.

**Primary evidence**: [[procurement-ai-survey]] — systematic review of vendor documentation found zero published third-party evaluations. [[agent-evaluation-overview]] — general-purpose agent benchmarks (AgentBench, WebArena, GAIA) do not include procurement domain tasks.

**BuyerBench response**: BuyerBench is, to our knowledge, the first open-source benchmark specifically designed to evaluate AI buyer agents on procurement domain tasks. Its scenario suite targets exactly the capability claims vendors make — supplier discovery, quote comparison, multi-step purchase workflows — making results directly interpretable against commercial baselines.

**Paper positioning**: This gap alone justifies the paper's existence. Every reviewer will ask "why isn't this covered by existing benchmarks?" and the answer is: it isn't.

---

## Gap 2 — Cognitive Bias Testing Is Absent from All Procurement AI Evaluation

**The gap**: A substantial body of literature (2023–2025) empirically documents that frontier LLMs exhibit anchoring, framing, default bias, loss aversion, sunk cost fallacy, and status quo bias in controlled decision tasks. However, none of this research applies bias testing to procurement-domain scenarios. Existing procurement AI evaluations use binary task completion metrics that are blind to the consistency and rationality of agent reasoning.

**Primary evidence**: [[bias-in-llm-agents]] — eight cognitive biases now have empirical LLM evidence (Echterhoff et al. 2024, Tjuatja et al. 2024, Jones & Steinhardt 2022, Fu et al. 2024). [[procurement-ai-survey]] — vendor benchmarks measure task completion, not decision rationality. [[PILLAR2-SUMMARY]] — synthesizes the eight-bias taxonomy with evidence classification.

**BuyerBench response**: Pillar 2 introduces controlled variant methodology — A/B scenario pairs with identical economics but one bias-inducing manipulation — to measure cognitive bias susceptibility in realistic procurement contexts. The bias susceptibility index (BSI) is the first computable metric for bias in buyer agent decisions.

**Paper positioning**: Bridges two literatures (behavioral economics / LLM bias studies) and (procurement AI systems) that have never been connected. This is the clearest interdisciplinary contribution.

---

## Gap 3 — Payment Security Compliance Is Never Tested for AI Agents

**The gap**: PCI DSS, EMV 3-D Secure, and EMV Payment Tokenisation define detailed, enforceable requirements for payment system behavior. These standards have been audited and enforced in human-operated systems for decades. However, no benchmark evaluates whether AI agents handling payment-adjacent tasks comply with these standards. The introduction of agent-initiated transaction flows (recurring purchases, delegated authorization, mandate-bound spending) creates new compliance requirements (e.g., EMV 3DS 3RI flows) that are not addressed by any existing agent evaluation framework.

**Primary evidence**: [[payment-security-standards]] — full mapping of PCI DSS/EMV requirements to testable agent behaviors reveals a complete absence of existing evaluations. [[agentic-commerce-protocols]] — AP2, UCP, and ACP introduce agent-specific authorization semantics for which no conformance test suite exists.

**BuyerBench response**: Pillar 3 introduces categorical compliance evaluation — bright-line pass/fail for payment security standards — alongside graduated security metrics (Compliance Adherence Rate, Security Violation Frequency) that distinguish between minor conformance gaps and disqualifying violations. BuyerBench is the first benchmark to evaluate AI agent behavior against PCI DSS, EMV 3DS, and emerging agentic commerce protocol specifications.

**Paper positioning**: Critical for the security and FinTech communities. Makes the case that "safe" and "capable" are orthogonal agent properties that must be measured independently.

---

## Gap 4 — The Multi-Dimensional Independence of Capability, Rationality, and Security Is Ignored

**The gap**: Existing agent benchmarks implicitly assume that capability (can the agent complete tasks?) and safety (is the agent's behavior correct?) are correlated or that only one dimension matters. The procurement domain makes this assumption untenable: an agent can be operationally capable (completes workflows) while simultaneously irrational (susceptible to anchoring) and insecure (fails PCI compliance). No existing evaluation framework separates these three dimensions or measures their cross-agent correlation.

**Primary evidence**: [[evaluation-metrics-taxonomy]] — surveys existing metrics; none cross-tabulate capability and bias resistance. [[PILLAR3-SUMMARY]] — "Relationship to Other Pillars" section articulates the orthogonality argument: P1-capable + P3-non-compliant = dangerous; P3-compliant + P1-incapable = useless.

**BuyerBench response**: BuyerBench's three-pillar structure produces a multi-dimensional evaluation profile per agent, not a single aggregate score. By evaluating all three pillars independently and reporting them separately, BuyerBench enables discovery of cross-pillar performance patterns — including agents that excel on capability while failing security, and the reverse. This profile is the unit of evaluation, not any single metric.

**Paper positioning**: A methodological contribution: the paper can show empirically (across the 3 CLI agents) that pillar scores are indeed uncorrelated, justifying the three-dimensional approach over a single composite score.

---

## Gap 5 — Adversarial Procurement Environments Are Not Modeled in Any Benchmark

**The gap**: Agent benchmarks that include adversarial scenarios almost exclusively test code injection or command-line prompt injection. No benchmark tests the specific adversarial surface of procurement buyer agents: indirect prompt injection via product catalog data, adversarial price anchoring in supplier proposals, fake scarcity manipulation in vendor communications, and protocol downgrade attacks in payment flows. This attack surface is unique to agents that consume business-domain natural language as task-relevant data.

**Primary evidence**: [[fraud-patterns-and-attacks]] — catalogues six attack categories specific to buyer agents, none of which appear in existing agent security benchmarks. [[bias-in-llm-agents]] — economic manipulation attacks exploit documented LLM biases, creating a Pillar 2/3 overlap. Greshake et al. (2023) and Debenedetti et al. (2024) document the indirect prompt injection threat but not in procurement contexts.

**BuyerBench response**: Pillar 3 adversarial scenarios model the buyer-agent-specific attack surface. Critically, economic manipulation attacks (adversarial anchoring, fake scarcity) bridge Pillar 2 and Pillar 3: they are simultaneously bias exploitation and security attacks. The Security Degradation Score (SDS) — the gap between benign and adversarial performance — measures how much an agent's safe task execution degrades under attack.

**Paper positioning**: Novel threat modeling contribution. The buyer agent adversarial attack surface has not been systematically catalogued before; the paper can claim this taxonomy as a standalone contribution.

---

## Gap 6 — Emerging Agentic Commerce Protocols Have No Conformance Test Suite

**The gap**: Three emerging agentic commerce protocol specifications — AP2 (Google), UCP (universal-commerce-protocol), and ACP (agentic-commerce-protocol) — and two payment network initiatives — Visa Trusted Agent Protocol (TAP) and Mastercard Agent Pay — define new technical standards for agent-initiated commerce. All are in active development (beta/v0.1 status). Despite their significance for the future of AI-mediated commerce, no conformance test suite exists for any of them. Implementers and evaluators have no way to verify protocol-conformant agent behavior.

**Primary evidence**: [[agentic-commerce-protocols]] — documents AP2/UCP/ACP spec structures and behavioral requirements; no conformance suite found. [[network-initiatives]] — documents Visa TAP and Mastercard Agent Pay; both note that behavioral testing is the only available proxy (live network access is gated).

**BuyerBench response**: Pillar 3 protocol conformance scenarios provide behavioral test cases for AP2, UCP, and ACP (pinned to specific spec versions). These are the closest publicly available approximation of a conformance test suite for these protocols, and BuyerBench's versioned scenario design means test cases can be updated as specs evolve. The benchmark documents which protocol version each scenario targets.

**Paper positioning**: Timely contribution to an emerging ecosystem. The paper should be explicit that BuyerBench's protocol conformance scenarios are version-pinned and that spec evolution will require scenario maintenance — this is a feature, not a limitation, because it tracks the evolving standard.

---

## Gap 7 — Agent Trace Artifacts Are Neither Required Nor Evaluated in Existing Benchmarks

**The gap**: Existing agent benchmarks evaluate outcomes (did the task succeed?) and sometimes actions (which tools were called?). None require agents to emit structured audit trail artifacts — records of decision rationale, applied constraints, credential access events, and policy compliance checks — that would satisfy real-world governance requirements. This gap is consequential: ISO/IEC 42001 requires documented AI decision audit trails; NIST AI RMF requires auditability and accountability. An agent that makes correct decisions without producing verifiable records is ungovernable in high-stakes deployment.

**Primary evidence**: [[ai-governance-standards]] — ISO 42001/23894 and NIST AI RMF requirements for audit trails explicitly not met by current agent frameworks. [[multi-agent-eval]] — ReAct and ToolBench introduce trace evaluation but focus on task traces, not compliance audit artifacts. [[PILLAR3-SUMMARY]] — "AI governance audit trail" scenario category directly addresses this gap.

**BuyerBench response**: BuyerBench's harness requires agents to emit structured trace artifacts that serve as evaluation evidence for all three pillars. The Audit Trail Completeness (ATC) metric in Pillar 3 measures how well these artifacts satisfy ISO 42001 and NIST AI RMF governance requirements. This positions BuyerBench as an evaluation tool for AI governance claims, not just capability claims.

**Paper positioning**: Connects to the growing AI governance literature. Makes BuyerBench relevant not just to ML/AI researchers but to policy and compliance audiences.

---

## Cross-Gap Summary Table

| Gap | Pillar(s) | Primary literature | BuyerBench metric/feature |
|---|---|---|---|
| No procurement AI benchmark | P1 | [[procurement-ai-survey]], [[agent-evaluation-overview]] | First open-source procurement benchmark |
| No cognitive bias testing in procurement | P2 | [[bias-in-llm-agents]], [[behavioral-economics-foundations]] | Bias Susceptibility Index (BSI), controlled variants |
| Payment security compliance untested | P3 | [[payment-security-standards]], [[agentic-commerce-protocols]] | Compliance Adherence Rate (CAR), categorical failures |
| Pillar independence ignored | P1+P2+P3 | [[evaluation-metrics-taxonomy]], [[PILLAR3-SUMMARY]] | Multi-dimensional profile (no aggregate score) |
| Adversarial procurement not modeled | P2+P3 | [[fraud-patterns-and-attacks]], [[bias-in-llm-agents]] | Security Degradation Score (SDS), adversarial variants |
| Agentic commerce protocol conformance | P3 | [[agentic-commerce-protocols]], [[network-initiatives]] | Versioned protocol conformance scenarios |
| Agent audit trail not evaluated | P1+P3 | [[ai-governance-standards]], [[multi-agent-eval]] | Audit Trail Completeness (ATC) |

---

## Authorship Note

This synthesis is intended to be used directly as source material for the BuyerBench paper's Introduction ("Motivation") and Related Work ("Research Gaps") sections. Each gap entry corresponds to a claim the paper should make, with the supporting literature already catalogued.
