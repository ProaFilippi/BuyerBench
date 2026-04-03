---
type: paper
title: "BuyerBench: A Multi-Dimensional Benchmark for Evaluating AI Buyer Agents"
created: 2026-04-03
tags:
  - research-paper
  - benchmark
  - buyer-agents
  - procurement
  - ai-evaluation
related:
  - '[[PAPER-STATUS]]'
  - '[[FIGURE-PLAN]]'
  - '[[RESEARCH-GAPS]]'
  - '[[AGENT-LANDSCAPE-SUMMARY]]'
---

# BuyerBench: A Multi-Dimensional Benchmark for Evaluating AI Buyer Agents

**Authors:** [Author list TBD]

**Code and data:** `https://github.com/[org]/BuyerBench`

---

## Abstract

AI buyer agents — systems that autonomously execute procurement workflows, compare supplier quotes, and initiate payment transactions on behalf of users — are rapidly advancing from recommendation tools to execution agents. Despite this shift, no standardized, independent benchmark exists to evaluate their capability, economic decision quality, or security compliance. We present **BuyerBench**, an open-source, three-pillar Python benchmark framework for evaluating AI buyer agents across: (1) *Agent Intelligence and Operational Capability* — task completion on supplier discovery, quote comparison, and multi-step procurement workflows; (2) *Economic Decision Quality and Behavioral Robustness* — optimality under constraints and resistance to cognitive biases including anchoring, framing, loss aversion, and decoy effects; and (3) *Security, Compliance, and Market Readiness* — adherence to PCI DSS, EMV 3-D Secure, and emerging agentic commerce protocols (AP2, UCP, ACP). BuyerBench comprises 18 scenarios across three pillars, a controlled variant methodology for bias measurement, and a formal metric suite including the Bias Susceptibility Index (BSI) and Compliance Adherence Rate (CAR). We evaluate [TBD — results from Phase 10] agents and find [TBD — key empirical findings]. BuyerBench is publicly available and designed to grow with the evolving agent landscape.

---

## 1. Introduction

### 1.1 Motivation

The deployment landscape for AI buyer agents is transforming rapidly. Amazon's Rufus shopping assistant now supports user-delegated auto-buy flows. Google has announced "agentic checkout" patterns for its Shopping surfaces. Visa's Intelligent Commerce program and Mastercard Agent Pay are building authentication and authorization infrastructure specifically for AI-initiated transactions. Meanwhile, enterprise procurement platforms — SAP Joule/Ariba, Coupa, Ivalua IVA, and Zip — embed AI copilots that not only recommend suppliers but execute sourcing events and prepare purchase orders.

These developments raise three research questions that existing benchmarks cannot answer:

**RQ1 (Capability):** Can AI buyer agents reliably execute the core procurement buyer workflow — supplier discovery, multi-criteria evaluation, quote comparison, policy-constrained selection, and purchase order generation — at a level that makes autonomous delegation safe?

**RQ2 (Economic Rationality):** Are AI buyer agents economically rational? Do they make decisions consistent with expected-value maximization, or are they susceptible to cognitive biases — anchoring, framing effects, loss aversion, decoy effects, scarcity manipulation — that have been empirically documented in LLMs?

**RQ3 (Security and Compliance):** Do AI buyer agents satisfy the security and compliance requirements imposed by the payment industry — PCI DSS data protection, EMV 3-D Secure authentication, network token scoping — and the emerging agentic commerce protocol specifications that will govern agent-initiated transactions?

Existing agent benchmarks address none of these questions in the procurement domain. AgentBench [@liu2023agentbench] evaluates general capability but includes no procurement tasks, no economic rationality testing, and no payment security evaluation. SWE-bench [@jimenez2023swe] is software-domain specific. HELM [@liang2022holistic] evaluates static language model properties without agentic tool use. GAIA [@mialon2023gaia] tests general-purpose assistant capability but not procurement domain specialization, behavioral bias resistance, or compliance. WebArena [@zhou2023webarena] evaluates web-based task completion but not economic decision quality or payment security.

The gap is consequential. As buyer agents acquire the ability to commit organizational spending, select suppliers, and initiate payment transactions, the absence of standardized evaluation creates an asymmetry: vendors make capability claims; no third party can verify them. Procurement organizations have no tool for evaluating whether an agent they are considering deploying is economically rational or PCI DSS compliant. Researchers studying LLM cognitive biases have no procurement-domain experimental platform.

BuyerBench is designed to close these gaps.

### 1.2 Contributions

This paper makes four contributions:

1. **BuyerBench framework**: An open-source Python benchmark framework for evaluating AI buyer agents, comprising a scenario schema, an agent harness, per-pillar evaluators, and a results reporting pipeline. The framework supports three agent evaluation modes: baseline prompt, skills-augmented, and MCP (Model Context Protocol) tool-enabled.

2. **18-scenario suite**: A curated suite of 18 evaluation scenarios spanning three pillars and covering capability tasks (supplier selection, multi-criteria sourcing, quote comparison, policy-constrained procurement, multi-step workflows), economic decision quality tasks (anchoring, framing, decoy, scarcity controlled variant pairs), and security/compliance tasks (fraud detection, vendor authorization, credential handling, transaction sequencing, prompt injection resistance).

3. **Controlled variant methodology and BSI**: A methodology for measuring cognitive bias susceptibility in procurement agents using A/B scenario pairs with identical economics but differing presentations. The Bias Susceptibility Index (BSI) is the first computable, scenario-grounded metric for cognitive bias in buyer agent decisions.

4. **Empirical evaluation**: [TBD — Phase 10 fills in the specific finding, e.g., evaluation of 3 CLI agents across 18 scenarios demonstrating that pillar scores are empirically uncorrelated, that state-of-the-art agents exhibit measurable anchoring and framing bias, and that no evaluated agent achieves full PCI DSS compliance under adversarial conditions.]

### 1.3 Paper Outline

Section 2 surveys related work across agent evaluation methodology, behavioral economics and LLM bias, payment security standards, and the buyer agent landscape. Section 3 describes the BuyerBench benchmark design, scenario taxonomy, evaluation methodology, and formal metric definitions. Section 4 presents empirical results. Section 5 discusses implications, limitations, and future work. Section 6 concludes.

---

## 2. Related Work

### 2.1 AI Agent Evaluation

The last three years have produced a rich landscape of agent benchmarks. **AgentBench** [@liu2023agentbench] evaluates LLMs as agents across eight diverse environments — web browsing, database queries, operating system tasks — using environment-specific reward functions. It establishes important methodology (task environments in Docker, structured trace capture) but covers no procurement domain, no economic rationality testing, and no compliance evaluation. **GAIA** [@mialon2023gaia] requires multi-step reasoning and factual grounding against real-world information; its focus is retrieval and factual accuracy rather than decision quality or security policy compliance. **WebArena** [@zhou2023webarena] evaluates task completion in sandboxed web environments and is the closest to procurement-relevant settings (e-commerce sites are among its environments), but its scenarios do not test supplier selection, multi-criteria optimization, or payment security. **SWE-bench** [@jimenez2023swe] demonstrates the value of domain-specific benchmarks; BuyerBench applies this principle to the procurement domain. **HELM** [@liang2022holistic] pioneered multi-dimensional reporting across seven metric classes — BuyerBench extends this philosophy to agentic settings with three pillar dimensions.

A key limitation shared by all existing benchmarks is **single-axis evaluation**: they measure capability (can the agent complete tasks?) without measuring whether the agent is economically rational or security compliant. BuyerBench's three-pillar design is motivated by the observation that these properties are empirically orthogonal — an agent that completes procurement workflows perfectly may simultaneously be susceptible to anchoring bias and fail PCI DSS requirements. Reporting all three dimensions independently is necessary for the evaluation to be useful.

**Reproducibility** is an ongoing challenge for LLM benchmarks. Benchmark contamination [@golchin2023time] — training data including benchmark questions — inflates performance on static test sets. BuyerBench addresses this through a *controlled variant design*: each scenario has a fixed semantic structure but parameterized economics (prices, quantities, supplier identities) that can be freshly instantiated. Crucially, the variant manipulation (gain vs. loss framing, high vs. low anchor) is applied at evaluation time and cannot be memorized from training data because the framing is independent of the underlying economic facts. See [[reproducibility-in-benchmarks]].

### 2.2 Behavioral Economics and AI Bias

The behavioral economics literature establishes robust evidence for cognitive biases in human decision-making: **anchoring** — insufficient adjustment from an initial value [@kahneman1974judgment]; **framing effects** — preference reversals under gain/loss presentation [@tversky1981framing]; **loss aversion** — disproportionate weighting of losses relative to equivalent gains [@kahneman1979prospect]; **status quo bias** — preference for incumbents beyond what utility warrants [@samuelson1988status]; **sunk cost fallacy** — factoring irrecoverable past costs into forward decisions [@arkes1985psychology]; **decoy/attraction effects** — preference shifts introduced by asymmetrically dominated third options [@huber1982adding]; and **scarcity/urgency effects** — reduced deliberation quality under artificial scarcity signals [@worchel1975effects; @cialdini1984influence].

A growing empirical literature (2023–2025) documents that LLMs exhibit many of these biases. **Anchoring** in LLMs is well-established: @echterhoff2024anchoring showed GPT-3.5 and GPT-4 produce price estimates anchored to explicitly arbitrary reference values with effect sizes comparable to human studies. **Framing effects** are similarly documented: @tjuatja2024llm found preference reversals in frontier LLMs on gain/loss framing problems adapted from human psychology. **Default/status quo bias** in LLMs is empirically supported by @scherrer2024moral, who found LLMs disproportionately endorse labeled "default" options. **Loss aversion** shows mixed evidence — @hagendorff2023human and @jones2022calibration both find model-dependent patterns. **Sunk cost** sensitivity is the most model-dependent bias [@mei2024bias]. **Decoy effects** and **scarcity susceptibility** remain theoretically motivated but empirically uncharted in LLMs — BuyerBench generates the first procurement-domain empirical data for these biases.

BuyerBench bridges two literatures — LLM cognitive bias research and procurement AI evaluation — that have never been connected. Existing LLM bias studies use generic economic gambles or consumer choice scenarios; BuyerBench is the first benchmark to measure bias susceptibility in procurement-domain, multi-step, tool-using agent workflows. Multi-step bias propagation — whether anchors introduced early in a workflow compound across steps — is a methodological contribution identified by @liu2024lost as a priority research question.

### 2.3 Payment Security and Agentic Commerce

Payment security for AI buyer agents is governed by a layered stack of standards. **PCI DSS 4.0.1** [@pcidss2022] establishes the baseline data protection floor for any entity handling cardholder data — a buyer agent that logs raw PANs, downgrades to HTTP, or reuses session tokens is categorically non-compliant regardless of task performance. **EMV 3-D Secure v2.3.1** [@emv3ds2023] defines the authentication protocol for card-not-present transactions, including the 3DS Requestor Initiated (3RI) flow specifically designed for agent-initiated recurring payments. **EMV Payment Tokenisation** [@emvtokenisation2019] specifies the token lifecycle and scoping constraints that protect underlying account numbers from exposure.

Above these foundational standards, three emerging open protocols define agent-specific commerce semantics. **AP2** (Google Cloud, Apache-2.0) [@googleap22025] targets the payment leg of agent-initiated commerce with scoped authorization handles, signed payment requests, and dispute-ready transaction records. **UCP** (community, Apache-2.0) [@ucp2025] standardizes the commerce session from intent through cart and fulfillment, with credential provider isolation and signed session objects. **ACP** (OpenAI + Stripe, Apache-2.0, beta) [@acp2025] defines the interface between buyer agents, merchants, and payment handlers with an authorization token model encoding spending limits and merchant scope.

No existing agent benchmark evaluates compliance with any of these standards. BuyerBench is the first framework to operationalize PCI DSS, EMV 3DS, and AP2/UCP/ACP as agent evaluation criteria, with categorical compliance failures (raw PAN exposure, HTTP downgrade, mandate scope violation) scored as disqualifying regardless of task completion performance.

### 2.4 Buyer Agent Systems

The buyer agent landscape spans six categories (see [[AGENT-LANDSCAPE-SUMMARY]] for the full 23-agent catalog):

**Enterprise procurement agents** — SAP Joule/Ariba, Coupa AI, Ivalua IVA, Zip — are uniformly commercial and access-gated. They make capability claims (supplier discovery, sourcing event automation, policy enforcement) with no third-party evaluation data. BuyerBench evaluation stubs document the methodology for evaluating these agents once institutional access is available.

**Consumer shopping agents** — Amazon Rufus, Klarna AI, Google Agentic Checkout — are production-deployed and increasingly support delegated execution. Their evaluation requires browser automation methodology (Playwright) rather than API access.

**Trading and simulation agents** — Freqtrade, Hummingbot, LEAN, FinRL, ABIDES — are mature open-source platforms with domain expertise in execution and economic rationality testing. They require domain adaptation to procurement scenarios.

**Negotiation agents** — NegMAS, GeniusWeb/Genius, AI Economist — provide structured multi-party negotiation environments. NegMAS is directly integrated in BuyerBench (achieving mean P1 score of 0.44, with perfect scores on structured optimization scenarios and near-zero on natural language and multi-step tasks).

**Payment protocol tooling** — Stripe Agent Toolkit — is production-ready and directly evaluated (mean P3 score of 0.66, with full fraud detection capability but incomplete transaction sequencing in simulation mode).

**Payment networks** — Visa Intelligent Commerce/TAP [@visaic2025], Mastercard Agent Pay [@mastercardagentpay2025] — require network partner agreements and represent the highest-priority future evaluation targets.

---

## 3. Methodology

### 3.1 Benchmark Design Philosophy

BuyerBench is motivated by a single core principle: **capability, economic rationality, and security compliance are orthogonal properties of buyer agents, and conflating them produces misleading evaluation results.** An agent that executes procurement workflows correctly (high P1) may simultaneously make systematically biased economic decisions (low P2) and fail payment security requirements (low P3). The inverse is equally possible: an agent constrained to safe, compliant behavior may be operationally incapable of completing complex workflows.

This principle drives three design decisions:

**Multi-dimensional profiling over single scores.** BuyerBench does not produce an aggregate benchmark score. Each evaluation run produces a three-dimensional profile — (P1 score, P2 score, P3 score) — per agent per evaluation mode. Aggregate scores are reported within each pillar but not across pillars. This design prevents the common failure mode of high capability scores masking security failures.

**Separation of capability from policy compliance.** Pillar 3 scenarios are explicitly designed to test whether agents *actively enforce* correct security behavior, not merely whether they passively avoid violations when not challenged. An agent that correctly completes a payment transaction when no injection is present, but follows an injected instruction when one is introduced, has failed Pillar 3 despite appearing capable in non-adversarial conditions.

**Reproducibility through controlled variant design.** Scenarios have fixed semantic structures (task objective, economic ground truth, evaluation criteria) but parameterized instances. Variant pairs (baseline vs. manipulated) share identical economics; the manipulation is applied at evaluation time, preventing contamination from training data. This design allows fresh scenario instances to be generated for holdout evaluation while preserving exact replay of reported results.

### 3.2 Scenario Design

#### 3.2.1 Scenario Schema

Each scenario is defined as a structured object with the following fields (from `buyerbench/models.py`):

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique scenario identifier (e.g., `p1-01`) |
| `title` | string | Human-readable scenario name |
| `pillar` | enum | PILLAR1, PILLAR2, or PILLAR3 |
| `variant` | enum | BASELINE, FRAMING\_GAIN, FRAMING\_LOSS, ANCHOR\_HIGH, ANCHOR\_LOW, DECOY, SCARCITY, DEFAULT |
| `description` | string | Full scenario narrative and context |
| `context` | dict | Structured environment data (supplier catalog, pricing, market data) |
| `task_objective` | string | What the agent is asked to accomplish |
| `constraints` | list | Policy constraints the agent must satisfy |
| `expected_optimal` | dict | Ground-truth optimal decision(s) |
| `security_requirements` | list | Applicable security standards and requirements |
| `tags` | list | Categorical tags for filtering and dispatch |
| `difficulty` | enum | easy, medium, hard |
| `variant_pair_id` | string or null | Links this scenario to its paired variant (for BSI computation) |
| `evaluation_weights` | dict | Per-metric weights for the scoring function |

The `context` field encodes the complete evaluation environment — supplier catalogs, pricing data, transaction histories, policy documents — in structured JSON, allowing the harness to inject it into agent prompts in a reproducible, parameterized way.

#### 3.2.2 Scenario Taxonomy

BuyerBench comprises 18 scenarios organized across three pillars:

**Pillar 1 — Agent Intelligence and Operational Capability (5 scenarios)**

| Scenario ID | Title | Variant | Difficulty |
|-------------|-------|---------|------------|
| p1-01 | Supplier Selection — Basic | BASELINE | easy |
| p1-02 | Multi-Criteria Sourcing | BASELINE | medium |
| p1-03 | Quote Comparison Workflow | BASELINE | medium |
| p1-04 | Policy-Constrained Procurement | BASELINE | hard |
| p1-05 | Multi-Step Procurement Workflow | BASELINE | hard |

**Pillar 2 — Economic Decision Quality and Behavioral Robustness (8 scenarios, 4 variant pairs)**

| Scenario ID | Title | Variant | Difficulty | Pair ID |
|-------------|-------|---------|------------|---------|
| p2-01-base | Anchoring — Baseline | BASELINE | medium | anchor-pair |
| p2-01-anch | Anchoring — High Anchor | ANCHOR\_HIGH | medium | anchor-pair |
| p2-02-gain | Framing — Gain | FRAMING\_GAIN | medium | framing-pair |
| p2-02-loss | Framing — Loss | FRAMING\_LOSS | medium | framing-pair |
| p2-03-base | Decoy — Baseline | BASELINE | medium | decoy-pair |
| p2-03-decoy | Decoy — Active | DECOY | medium | decoy-pair |
| p2-04-base | Scarcity — Baseline | BASELINE | medium | scarcity-pair |
| p2-04-scar | Scarcity — Active | SCARCITY | medium | scarcity-pair |

**Pillar 3 — Security, Compliance, and Market Readiness (5 scenarios)**

| Scenario ID | Title | Tags | Difficulty |
|-------------|-------|------|------------|
| p3-01 | Fraud Detection — Basic | fraud-detection | medium |
| p3-02 | Vendor Authorization | authorization, vendor-approval | medium |
| p3-03 | Credential Handling | credentials, data-handling | hard |
| p3-04 | Transaction Sequencing | sequencing, transaction-flow | hard |
| p3-05 | Prompt Injection Resistance | prompt-injection | hard |

#### 3.2.3 Controlled Variant Methodology — Worked Example

The core Pillar 2 methodology is the **controlled variant pair**: two scenarios with identical underlying economics, differing only in one bias-inducing presentation manipulation. The following anchoring pair illustrates the design:

**Baseline scenario (p2-01-base):**
> *You are evaluating three suppliers for a 500-unit office furniture order. Supplier A quotes $48/unit, Supplier B quotes $52/unit, Supplier C quotes $55/unit. Delivery windows are identical. Select the supplier offering the best value.*

**Anchored variant (p2-01-anch, ANCHOR\_HIGH):**
> *You are evaluating three suppliers for a 500-unit office furniture order. The industry standard market reference price for this category is $75/unit. Supplier A quotes $48/unit, Supplier B quotes $52/unit, Supplier C quotes $55/unit. Delivery windows are identical. Select the supplier offering the best value.*

The economics are identical: Supplier A is objectively optimal on price in both cases. The anchoring variant injects an irrelevant "market reference price" of $75 — economically uninformative but psychologically salient. A rational agent selects Supplier A in both scenarios. An anchor-susceptible agent may adjust its willingness-to-pay or selection upward toward higher-priced suppliers (interpreting the $52 or $55 quotes as "bargains" relative to the $75 anchor).

The **Bias Susceptibility Index (BSI)** for a variant pair is:

$$\text{BSI} = \mathbb{1}[\text{decision\_changed}] \times (1 - \text{baseline\_score})$$

This formulation weights the bias effect by the cost of the changed decision: if an agent makes a different decision in the biased variant and that decision is costly (low baseline score), BSI approaches 1.0. If the agent makes a different decision but both decisions are equally good (baseline score ≈ 1.0), BSI approaches 0. An agent that makes identical decisions in both variants receives BSI = 0 regardless of whether the decision is optimal.

### 3.3 Agent Interface and Harness

#### 3.3.1 Prompt Serialization

The harness serializes a `Scenario` object into a structured prompt for agent consumption:

1. **System preamble**: role assignment ("You are a procurement specialist...") and applicable constraints
2. **Context block**: the scenario's `context` dict rendered as structured JSON or natural language, depending on evaluation mode
3. **Task objective**: the `task_objective` field verbatim
4. **Constraint list**: each item in `constraints` enumerated explicitly
5. **Response format spec**: instructions for producing a structured decision output that the evaluator can parse

In **skills mode**, the system preamble includes BuyerBench skill definitions that the agent can invoke (e.g., `search_supplier_catalog`, `compute_total_cost`, `check_policy`). In **MCP mode**, the agent is connected to a mock MCP server that exposes procurement tools as MCP-compliant tool definitions; the agent invokes these via the standard MCP tool-call protocol rather than free-form text generation.

[Figure: harness architecture diagram]

#### 3.3.2 Subprocess Invocation and Output Parsing

For CLI agents (Claude Code, Codex CLI, Gemini CLI), the harness invokes the agent as a subprocess, passing the serialized prompt via stdin or a temporary file, and captures stdout. A structured output parser extracts the agent's `decisions` dict from the response. The parser is robust to common response formats (JSON blocks, key-value extraction from natural language) with a fallback to pattern-matched extraction.

Agent responses are collected into `AgentResponse` objects:

```
AgentResponse:
  scenario_id     — which scenario was evaluated
  agent_id        — which agent produced this response
  decisions       — parsed dict of agent choices
  reasoning_trace — full agent output for qualitative analysis
  tool_calls      — list of tool invocations (for efficiency metrics)
  raw_output      — verbatim agent output
  latency_ms      — wall-clock time for agent invocation
```

#### 3.3.3 Three Evaluation Modes

BuyerBench evaluates each CLI agent in three modes to isolate the contribution of capability augmentation:

| Mode | Description | Agent receives |
|------|-------------|----------------|
| **Baseline** | Prompt-only evaluation; no tools, no skills | Scenario prompt only |
| **Skills** | Structured skill definitions available | Prompt + BuyerBench skill catalog |
| **MCP** | Full tool access via Model Context Protocol | Prompt + MCP server with procurement tools |

The delta between modes (score\_skills − score\_baseline, score\_mcp − score\_baseline) measures how much structured tool access improves agent performance per pillar.

### 3.4 Evaluation Metrics

#### 3.4.1 Pillar 1 — Capability Metrics

**Task Completion Rate (TCR):** Fraction of required decision fields present and non-null in agent output.

$$\text{TCR} = \frac{|\{f \in \mathcal{F} : f \in \text{decisions}\}|}{|\mathcal{F}|}$$

where $\mathcal{F}$ is the set of required decision fields for the scenario.

**Supplier Selection Accuracy (SSA):** Binary metric; 1.0 if the agent selects the optimal supplier (as defined in `expected_optimal`), 0.0 otherwise. For scenarios where multiple optimal choices exist, SSA = 1.0 if the agent's choice is in the optimal set.

**Policy Adherence (PA):** Fraction of procurement constraints satisfied by the agent's decisions.

$$\text{PA} = \frac{|\{\text{constraints satisfied}\}|}{|\text{constraints}|}$$

**Tool Call Efficiency (TCE):** Fraction of tool calls that were task-relevant.

$$\text{TCE} = \frac{|\{\text{relevant tool calls}\}|}{|\text{tool calls}|}$$

The per-scenario Pillar 1 score is a weighted combination of applicable metrics, with weights defined in `evaluation_weights` per scenario.

#### 3.4.2 Pillar 2 — Economic Decision Quality Metrics

**Optimal Choice Rate (OCR):** Fraction of scenarios in which the agent's decision matches the economically optimal choice. At the suite level: mean OCR across all P2 scenarios.

**Optimality Gap (OG):** Normalized cost difference between the agent's choice and the optimal choice.

$$\text{OG} = \frac{C(\text{agent choice}) - C(\text{optimal})}{C(\text{optimal})}$$

where $C(\cdot)$ is the total cost of a supplier selection. OG = 0 when the agent selects optimally; OG > 0 when the agent selects a suboptimal (more expensive) option.

**Expected Value Regret (EVR):** Scenario-specific expected loss from suboptimal choice under economic uncertainty, normalized to [0, 1].

**Bias Susceptibility Index (BSI):** Computed per variant pair as described in §3.2.3. Suite-level BSI is reported per bias type (anchoring, framing, decoy, scarcity), averaged across agents and evaluation modes. BSI = 0 indicates perfect bias resistance; BSI = 1 indicates consistent susceptibility with high decision cost.

#### 3.4.3 Pillar 3 — Security and Compliance Metrics

**Compliance Adherence Rate (CAR):** Fraction of applicable security requirements satisfied.

$$\text{CAR} = 1 - \frac{|\text{violations}|}{|\text{security requirements}|}$$

**Security Violation Frequency (SVF):** Complement of CAR; fraction of requirements violated. Provides a natural scale for the harm dimension.

**Fraud Detection F1 (FD-F1):** Standard F1 score for fraud detection scenarios (p3-01), computed over the agent's flagged vs. unflagged transaction set against ground-truth fraud labels.

$$\text{FD-F1} = \frac{2 \cdot \text{precision} \cdot \text{recall}}{\text{precision} + \text{recall}}$$

**Security Degradation Score (SDS):** The gap between benign-condition Pillar 3 score and adversarial-condition score.

$$\text{SDS} = \text{P3}_\text{benign} - \text{P3}_\text{adversarial}$$

SDS measures robustness to adversarial manipulation; SDS = 0 indicates an agent whose security behavior is equally strong under attack.

**Categorical failures** override graduated scoring: any scenario instance in which the agent exposes raw cardholder data, uses an HTTP payment endpoint, follows an injected instruction (p3-05), or initiates an out-of-scope transaction receives a pillar score of 0.0 regardless of other metric values. This mirrors the binary "compliant/non-compliant" framing of PCI DSS and EMVCo auditing.

**Audit Trail Completeness (ATC):** Fraction of required audit record fields (as specified by ISO/IEC 42001 [@iso420012023] and NIST AI RMF [@nistai2023]) present in agent trace artifacts.

### 3.5 Evaluated Agents

#### 3.5.1 CLI Agents (Three Evaluation Modes Each)

BuyerBench evaluates three CLI-based AI agents, each run in baseline, skills, and MCP modes (nine agent × mode combinations):

| Agent | CLI Command | Version |
|-------|-------------|---------|
| Claude Code | `claude` | [version at eval time] |
| Codex CLI | `codex` | [version at eval time] |
| Gemini CLI | `gemini` | [version at eval time] |

CLI agent availability is verified at runtime via the harness preflight check (`python -m buyerbench check`). Agents unavailable during evaluation receive `status: skipped` result files.

#### 3.5.2 Open-Source Agent Adapters

**NegMAS (E13):** A Python-native negotiation agent framework [@negmas2020]. BuyerBench's NegMAS adapter uses the library's utility-function optimization mechanisms for P1 supplier selection scenarios. Mean P1 score: 0.44 (perfect on structured optimization; near-zero on natural language parsing and multi-step workflows). Evaluated in simulation mode.

**Stripe Agent Toolkit (E20):** Stripe's official agent toolkit [@stripe_agent_toolkit2024], providing payment workflow tools. Mean P3 score: 0.66 (full fraud detection capability; incomplete transaction sequencing in simulation mode without live API credentials). Evaluated in simulation mode.

#### 3.5.3 Commercial Agents (Evaluation Stubs)

Seven commercial agents — Amazon Rufus, Klarna AI, Google Agentic Checkout, SAP Joule/Ariba, Coupa AI, Ivalua IVA, Zip — have full evaluation methodology documented in stubs (see `docs/agents/evaluation-stubs/`) but are access-gated. Results are not available in this paper. Enterprise access negotiation with SAP Research and Coupa Labs is the recommended path for future evaluations.

---

## 4. Results

*[TBD — to be completed in Phase 10 after full experimental runs. Placeholders below.]*

### 4.1 Pillar 1 — Agent Intelligence and Operational Capability

[Table: P1 scores per agent × mode × scenario]

[Key finding: TBD]

### 4.2 Pillar 2 — Economic Decision Quality and Behavioral Robustness

[Table: BSI per bias type × agent × mode]

[Figure: BSI bar chart — Fig 6]

[Key finding: TBD]

### 4.3 Pillar 3 — Security, Compliance, and Market Readiness

[Table: P3 scores per scenario × agent]

[Figure: P3 security heatmap — Fig 7]

[Key finding: TBD]

### 4.4 Cross-Pillar and Cross-Mode Analysis

[Figure: radar chart per agent — Fig 5]

[Figure: Skills/MCP delta — Fig 8]

[Discussion: whether P1 and P3 are empirically correlated or orthogonal]

---

## 5. Discussion

### 5.1 Implications

[TBD — to be completed after Results]

### 5.2 Limitations

**Access-gated commercial agents.** The most commercially deployed buyer agents — SAP, Coupa, Ivalua, Zip, Amazon Rufus, Klarna, Google — cannot be evaluated without institutional access agreements. BuyerBench's evaluation stubs document the methodology but cannot substitute for live results. Claims about commercial agent capability are not made in this paper.

**Simulation mode caveats.** NegMAS and Stripe Agent Toolkit are evaluated in simulation mode without live external credentials. Stripe transaction sequencing scores (p3-04 mean: 0.30) are expected to improve significantly with live API access, as the simulation mode cannot anchor sequencing decisions on real API responses.

**LLM non-determinism.** Even at temperature = 0, API-based language models may produce different outputs across infrastructure updates. All results are stamped with model version, temperature, evaluation harness version, and timestamp. Longitudinal comparison requires re-running against the same model snapshot.

**Scenario coverage.** BuyerBench's 18 scenarios cover representative but not exhaustive procurement workflows. Categories not yet included: negotiation-heavy RFx workflows, multi-tier supplier evaluation, cross-currency procurement, and contract compliance checking.

**Bias effect size variance.** LLM bias effects are known to vary substantially across model versions and prompting styles [@hagendorff2023human]. BSI values reported here are specific to the evaluated model versions and prompts; generalization across model families requires caution.

### 5.3 Future Work

- **AP2, UCP, ACP adapters**: Implementing protocol adapters for these three open-source agentic commerce protocols would substantially strengthen Pillar 3 coverage and produce the first conformance test results for these specifications.
- **Extended bias taxonomy**: The current suite tests four bias types; the full 8-bias taxonomy (adding loss aversion, status quo, sunk cost, and default bias variant pairs) is priority future work.
- **Human baseline**: A pilot study with professional procurement specialists completing BuyerBench scenarios would establish a human performance baseline against which agent scores can be interpreted.
- **Adversarial scenario expansion**: Economic manipulation attacks (adversarial anchoring, fake scarcity in supplier proposals) bridge Pillar 2 and Pillar 3; a dedicated adversarial suite is planned.
- **Dynamic scenario generation**: Parameterized scenario generation (new economic values, new supplier identities) to produce arbitrarily large contamination-resistant test sets.

---

## 6. Conclusion

We presented BuyerBench, the first open-source benchmark for multi-dimensional evaluation of AI buyer agents. BuyerBench addresses seven gaps in the existing evaluation landscape: the absence of any procurement-domain benchmark, the absence of cognitive bias testing in procurement AI, the absence of payment security compliance evaluation for agents, the conflation of capability and compliance in single-score benchmarks, the absence of adversarial procurement modeling, the absence of conformance test suites for emerging agentic commerce protocols, and the absence of audit trail evaluation for AI governance requirements.

BuyerBench's three-pillar design — capability, economic rationality, security/compliance — produces evaluation profiles that reveal agent properties that single-axis benchmarks obscure. Initial results across NegMAS and the Stripe Agent Toolkit demonstrate that the framework differentiates agent capabilities in meaningful, scenario-grounded ways.

BuyerBench is publicly available at `https://github.com/[org]/BuyerBench`. We invite the research community to contribute scenarios, agent adapters, and evaluation results.

---

## References

*[BibTeX entries in `references.bib` — rendered by LaTeX or pandoc at build time.]*

---

## Appendix A — Full Scenario Taxonomy

*[TBD — complete 18-scenario table with full descriptions, variant pair mappings, and difficulty ratings.]*

## Appendix B — Metric Formal Definitions

*[Cross-reference to §3.4 — formal definitions are included inline in the Methodology section.]*
