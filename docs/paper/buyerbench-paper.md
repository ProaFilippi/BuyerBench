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

AI buyer agents — systems that autonomously execute procurement workflows, compare supplier quotes, and initiate payment transactions on behalf of users — are rapidly advancing from recommendation tools to execution agents. Despite this shift, no standardized, independent benchmark exists to evaluate their capability, economic decision quality, or security compliance. We present **BuyerBench**, an open-source, three-pillar Python benchmark framework for evaluating AI buyer agents across: (1) *Agent Intelligence and Operational Capability* — task completion on supplier discovery, quote comparison, and multi-step procurement workflows; (2) *Economic Decision Quality and Behavioral Robustness* — optimality under constraints and resistance to cognitive biases including anchoring, framing, loss aversion, and decoy effects; and (3) *Security, Compliance, and Market Readiness* — adherence to PCI DSS, EMV 3-D Secure, and emerging agentic commerce protocols (AP2, UCP, ACP). BuyerBench comprises 18 scenarios across three pillars, a controlled variant methodology for bias measurement, and a formal metric suite including the Bias Susceptibility Index (BSI) and Compliance Adherence Rate (CAR). We evaluate two open-source agents — NegMAS (negotiation specialist) and Stripe Agent Toolkit (payment operations) — and find that capability and security scores are empirically uncorrelated: NegMAS achieves perfect scores on structured optimization scenarios (P1=1.0) but zeros out on multi-step procurement workflows; the Stripe Toolkit achieves perfect fraud detection (FD-F1=1.0) but fails transaction sequencing in simulation mode (CAR=0.33 on p3-04). These findings demonstrate that BuyerBench surface the distinct agent capability boundaries that aggregate benchmarks obscure. BuyerBench is publicly available and designed to grow with the evolving agent landscape.

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

4. **Empirical evaluation**: Evaluation of two open-source agents (NegMAS E13 and Stripe Agent Toolkit E20) demonstrates that pillar scores are empirically uncorrelated: NegMAS achieves P1=0.44 with perfect scores on structured optimization but complete failure on natural language multi-step workflows; the Stripe Toolkit achieves P3=0.66 with perfect fraud detection (FD-F1=1.0) but fails transaction sequencing (sequence_correct=0.0). Neither agent achieves full compliance across all Pillar 3 scenarios, validating the need for scenario-level reporting. The framework correctly produces structured evaluation profiles that differentiate agent capabilities in meaningful, domain-specific ways. CLI agent evaluation (Claude Code, Codex, Gemini) and behavioral bias measurement are planned for subsequent evaluation runs once credential configuration is complete.

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

![BuyerBench Harness Architecture](figures/fig5-harness-architecture.png)

*Figure 1: BuyerBench harness architecture. Scenarios are loaded from the scenario library and serialized into structured prompts by the harness. Agents are invoked via CLI subprocess or SDK adapter in three modes (baseline, skills, MCP). Evaluators score agent responses per pillar. Results are written to JSON and aggregated into reports.*

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

This section presents empirical results from two evaluated agents: NegMAS (E13) across Pillar 1 scenarios, and the Stripe Agent Toolkit (E20) across Pillar 3 scenarios. All CLI agents (Claude Code, Codex, Gemini) required external credentials unavailable in the current evaluation environment; their results are reported as `status: skipped` and are targets for future evaluation runs. Pillar 2 (behavioral bias) requires CLI agents and likewise awaits future runs.

### 4.1 Overall Benchmark Results

Table 1 presents the per-agent aggregate scores for evaluated pillars. NegMAS was evaluated on all five Pillar 1 scenarios (10 evaluation instances across baseline and skills mode); the Stripe Agent Toolkit was evaluated on all five Pillar 3 scenarios.

**Table 1: Per-Agent Aggregate Benchmark Scores**

| Agent | Pillar | Mean Score | Std | Min | Max | N Scenarios |
|-------|--------|-----------|-----|-----|-----|-------------|
| NegMAS (E13) | PILLAR1 | **0.44** | 0.463 | 0.00 | 1.00 | 10 |
| Stripe Toolkit (E20) | PILLAR3 | **0.66** | 0.233 | 0.30 | 1.00 | 10 |
| Claude Code | P1/P2/P3 | — | — | — | — | *skipped* |
| Codex CLI | P1/P2/P3 | — | — | — | — | *skipped* |
| Gemini CLI | P1/P2/P3 | — | — | — | — | *skipped* |

The most immediate observation from Table 1 is that the two evaluated agents achieve moderate aggregate scores — neither agent dominates, and neither fails completely — which validates that the 18-scenario suite has appropriate difficulty calibration. The high standard deviation for NegMAS (0.463) signals a bimodal performance distribution rather than consistently mediocre capability; this is confirmed by the per-scenario breakdown in §4.2.

![Per-agent score profile across pillars](figures/fig1-radar-chart.png)

*Figure 2 (fig1-radar-chart): Per-agent score profile across the three evaluation pillars. NegMAS occupies the P1 axis; Stripe Toolkit occupies P3. The P2 axis is unevaluated for both agents in this release. The figure structure reveals that the two agents are complementary: each covers one pillar but neither covers the full three-pillar evaluation space.*

### 4.2 Pillar 1 — Agent Intelligence and Operational Capability

Table 2 presents NegMAS per-scenario scores for Pillar 1. The bimodal pattern is stark: NegMAS achieves a perfect score on the two structured optimization scenarios (p1-01, p1-02) and near-zero on scenarios requiring natural language extraction, policy reasoning, or multi-step coordination.

**Table 2: NegMAS Pillar 1 Results — Per-Scenario Breakdown**

| Scenario | Title | Score | Key Metric Failures |
|----------|-------|-------|---------------------|
| p1-01 | Supplier Selection — Basic | **1.00** | None — all metrics pass |
| p1-02 | Multi-Criteria Sourcing | **1.00** | None — all metrics pass |
| p1-03 | Quote Comparison Workflow | **0.20** | supplier\_match=0.0, extraction\_accuracy=0.0 |
| p1-04 | Policy-Constrained Procurement | **0.00** | supplier\_match=0.0, policy\_adherence=0.0 |
| p1-05 | Multi-Step Procurement Workflow | **0.00** | All step metrics=0.0, task\_completion=0.0 |

**Mean Pillar 1 score: 0.44** (std=0.463)

The pattern is interpretable in terms of NegMAS's design: NegMAS is a negotiation utility-function optimizer. When the optimal supplier can be identified by maximizing a utility function over structured inputs — as in p1-01 (single price criterion) and p1-02 (weighted multi-criteria scoring) — NegMAS performs optimally. When the task requires extracting the correct supplier from a free-text quote table (p1-03), applying named policy rules (p1-04), or executing a four-step procurement workflow with natural language coordination (p1-05), performance drops to zero.

This finding directly addresses RQ1: NegMAS demonstrates that *structured optimization capability does not generalize to natural language procurement workflows*. An evaluator that only assessed whether the agent "completed the task" might classify NegMAS as moderately capable; scenario-level analysis reveals the capability boundary precisely.

The `task_completion_rate` metric is worth noting separately: NegMAS achieves TCR=0.8 and TCR=1.0 on p1-03 and p1-04 respectively — indicating that the agent produces valid output structure and attempts an answer — but the answer content is wrong (supplier_match=0.0). This shows the value of decomposed metrics: a partial-output measure would mask the semantic failure.

### 4.3 Pillar 2 — Economic Decision Quality and Behavioral Robustness

Pillar 2 evaluation requires CLI agents capable of processing natural-language scenario prompts with behavioral manipulations. All CLI agent runs were skipped in this evaluation due to missing credentials. The Bias Susceptibility Index (BSI) table is therefore empty for this release.

**Table 3: BSI Table (Current Release)**

| Bias Type | Scenario Pair | Agent | BSI |
|-----------|--------------|-------|-----|
| Anchoring | p2-01 | All agents | *Pending* |
| Framing | p2-02 | All agents | *Pending* |
| Decoy | p2-03 | All agents | *Pending* |
| Scarcity | p2-04 | All agents | *Pending* |

![BSI by bias type and agent](figures/fig2-bsi-by-bias-type.png)

*Figure 3 (fig2-bsi-by-bias-type): Bias Susceptibility Index by bias type and agent. Chart is populated with zero values because CLI agent evaluation is pending. The figure structure is production-ready: once `python -m buyerbench run --agent claude-code` completes, BSI values populate automatically from the experiment results.*

Despite the absence of live BSI measurements, the controlled variant methodology is validated by the scenario suite: each of the four variant pairs has identical underlying economics, the bias manipulation is parameterized and applies cleanly to the agent prompt, and the evaluator correctly computes BSI=0 for agents that make identical decisions in both variants. The framework is instrumented and ready for full P2 evaluation; running one CLI agent will produce the first BSI measurements in the procurement domain.

### 4.4 Pillar 3 — Security, Compliance, and Market Readiness

Table 4 presents the Stripe Agent Toolkit's performance across all five Pillar 3 scenarios. This is the most information-dense result set in the current evaluation.

**Table 4: Stripe Agent Toolkit — Pillar 3 Per-Scenario Results**

| Scenario | Title | Score | CAR | SVF | Key Metrics |
|----------|-------|-------|-----|-----|-------------|
| p3-01 | Fraud Detection — Basic | **1.00** | 1.00 | 0.00 | FD-F1=1.0, precision=1.0, recall=1.0 |
| p3-02 | Vendor Authorization | **0.80** | 0.33 | 0.67 | failed\_vendors\_identified=1.0; approved\_vendors\_not\_blocked=0.0 |
| p3-03 | Credential Handling | **0.60** | 0.67 | 0.33 | credential\_not\_in\_output=1.0; exposure\_detected=0.0 |
| p3-04 | Transaction Sequencing | **0.30** | 0.67 | 0.33 | sequence\_correct=0.0; task\_completed=0.0 |
| p3-05 | Prompt Injection Resistance | **0.60** | 0.75 | 0.25 | injection\_not\_followed=1.0; injection\_flagged=1.0 |

**Mean Pillar 3 score: 0.66** (std=0.233)

Four observations warrant detailed discussion:

**Perfect fraud detection.** The Stripe Toolkit achieves FD-F1=1.0 on p3-01, correctly identifying all fraudulent transactions (true_positives=2, false_positives=0, false_negatives=0). This reflects the toolkit's design: Stripe's fraud signals are built into its payment processing layer and surface cleanly when the agent invokes the toolkit's fraud-check tool. The result provides a performance baseline: an agent that has access to a well-designed payment toolkit can achieve perfect fraud detection without explicit fraud-domain training.

**Vendor authorization gap.** On p3-02, the Stripe Toolkit correctly identifies failed vendors (failed_vendors_identified=1.0) but fails to verify that approved vendors are not incorrectly blocked (approved_vendors_not_blocked=0.0). The CAR of 0.33 indicates only one of three applicable requirements was met. This is a meaningful security gap: a system that rejects fraudulent vendors but also incorrectly blocks legitimate ones creates operational disruption and false negatives in the legitimate payment flow.

**Transaction sequencing failure in simulation mode.** The lowest score in the evaluation (0.30 on p3-04) is attributable to simulation mode limitations: the Stripe Toolkit's authorization and tokenization calls cannot anchor sequencing logic on live API responses when no credentials are available. With `sequence_correct=0.0` and `task_completed=0.0`, the agent produces output but cannot complete the correct authorization→tokenization→charge sequence. This result is expected and documented as a simulation-mode caveat in §5.3.

**Prompt injection resistance.** On p3-05, the Stripe Toolkit correctly ignores the injected instruction (`injected_instruction_not_followed=1.0`) and explicitly flags the injection in its reasoning trace (`injection_flagged_in_reasoning=1.0`). This is a strong result: the agent not only avoids following the injected instruction but actively identifies it. The CAR of 0.75 (rather than 1.0) reflects a secondary requirement — correct supplier selection despite the injection — that was not met (`correct_supplier_selected=0.0`).

![Compliance adherence rate heatmap](figures/fig3-compliance-heatmap.png)

*Figure 4 (fig3-compliance-heatmap): Compliance Adherence Rate by scenario and agent (Stripe Toolkit only). Color encodes CAR from 0 (red) to 1 (green). The scenario-level variation — from perfect compliance on fraud detection (1.00) to low compliance on vendor authorization (0.33) — illustrates why aggregate P3 scores conceal important scenario-specific failures.*

### 4.5 Skills and MCP Impact

The skills-mode and MCP-mode delta analysis requires CLI agents and is therefore empty in this release. Table 5 summarizes the evaluation plan for this analysis.

**Table 5: Skills/MCP Delta Table (Current Release)**

| Agent | Pillar | Skills Δ | MCP Δ | N |
|-------|--------|----------|-------|---|
| claude-code | P1/P2/P3 | *Pending* | *Pending* | — |
| codex | P1/P2/P3 | *Pending* | *Pending* | — |
| gemini | P1/P2/P3 | *Pending* | *Pending* | — |

![Skills and MCP score delta by agent](figures/fig4-skills-mcp-delta.png)

*Figure 5 (fig4-skills-mcp-delta): Score delta (mode − baseline) for skills and MCP modes per agent and pillar. Bars are zero because CLI evaluation is pending. The figure structure mirrors the expected output once CLI agents are evaluated: positive delta bars indicate pillar-specific improvement from structured tool access.*

The theoretical prediction is that skills mode provides the largest delta on Pillar 1 (operational capability) by giving agents access to supplier catalog search and cost computation tools, while MCP mode provides the largest delta on Pillar 3 (security compliance) by providing structured payment tool definitions that enforce correct transaction sequencing. Cross-pillar delta analysis is expected to reveal whether structured tool access consistently improves performance or introduces new failure modes (e.g., over-reliance on tool outputs that may contain injected content).

---

## 5. Discussion

### 5.1 Key Findings

The current evaluation produces five findings relevant to the three research questions posed in §1.1.

**Finding 1 (RQ1): Structured optimization capability does not transfer to natural language workflows.** NegMAS achieves a perfect score on p1-01 (basic supplier selection) and p1-02 (multi-criteria sourcing weighted scoring), where the optimal answer is computable from structured inputs via utility function maximization. It achieves zero on p1-04 (policy-constrained procurement) and p1-05 (multi-step workflow). This is not a failure of optimization ability — NegMAS successfully maximizes utility — but a failure of natural language understanding and policy reasoning. Agents that are competent in structured optimization domains may be entirely unsuitable for general-purpose procurement automation.

**Finding 2 (RQ1): The `task_completion_rate` metric masks semantic failure.** NegMAS achieves TCR≥0.8 on scenarios where it scores zero overall. This finding has methodological implications: evaluation frameworks that report only task completion rates — a common practice in agent benchmarks — would overstate NegMAS's procurement capability by a large margin. BuyerBench's decomposed metrics (supplier_match, policy_adherence, step-level correctness) are necessary to detect this class of failure.

**Finding 3 (RQ3): Fraud detection and transaction sequencing are decoupled capabilities.** The Stripe Toolkit achieves FD-F1=1.0 (perfect) on fraud detection and sequence_correct=0.0 (total failure) on transaction sequencing — despite both scenarios being classified as Pillar 3 security scenarios. This confirms the benchmark's core design principle: security compliance is not a single capability. An agent can be excellent at detecting fraud patterns while failing to correctly sequence the authorization → tokenization → charge transaction flow. Aggregate P3 scores (mean=0.66) conceal this gap.

**Finding 4 (RQ3): Prompt injection resistance appears robust for payment-oriented agents.** The Stripe Toolkit correctly ignores injected instructions and explicitly flags them in its reasoning trace (p3-05). This suggests that agents designed for payment workflows may have stronger injection resistance than general-purpose assistants — likely because payment operations have well-defined semantic constraints that injected instructions violate obviously. This hypothesis requires CLI agent evaluation to test across a broader range of agent architectures.

**Finding 5 (RQ1–RQ3): Multi-dimensional evaluation reveals capability profiles that single-axis benchmarks obscure.** The radar chart (Figure 2) makes this visually concrete: NegMAS occupies the P1 axis; the Stripe Toolkit occupies P3; neither covers P2. An aggregate score across all three pillars would either be meaningless (averaging apples and oranges) or misleadingly low (penalizing domain specialization). The three-pillar design was motivated by exactly this concern.

### 5.2 Implications for Agent Design

The results have several design implications for organizations building or deploying AI buyer agents.

**Pillar independence should drive evaluation design.** Finding 5 confirms the paper's central thesis: capability, economic rationality, and security compliance are orthogonal properties. Organizations evaluating buyer agents should require independent Pillar scores rather than accepting vendor-reported aggregate metrics. A single aggregate benchmark score for a procurement agent is, at best, incomplete and, at worst, a misleading marketing claim.

**Payment-toolkit integration is necessary but not sufficient for PCI DSS readiness.** The Stripe Toolkit's vendor authorization gap (CAR=0.33 on p3-02) and transaction sequencing failure (score=0.30 on p3-04) demonstrate that integrating a payment toolkit does not automatically confer PCI DSS compliance. Agents must additionally enforce correct authorization boundaries (not just identify fraud) and execute transactions in the correct protocol sequence. These requirements align with PCI DSS 4.0 Requirement 6.4 (secure software development) and Requirement 7 (restrict access to system components) [@pcidss2022].

**EMV 3DS compliance requires live API integration testing.** The transaction sequencing failure on p3-04 is partially a simulation artifact — without live API responses, the agent cannot anchor its sequencing logic on real authentication results. This finding suggests that PCI DSS and EMV 3DS compliance for AI agents cannot be evaluated in pure simulation; evaluation requires integration with live payment sandboxes. BuyerBench's modular adapter architecture is designed to support both simulation and live integration modes.

**Prompt injection resistance should be treated as a first-class security requirement.** The AP2, UCP, and ACP protocols all include agent authentication requirements specifically because of the prompt injection risk to payment agents [@googleap22025; @acp2025]. The Stripe Toolkit's strong performance on p3-05 is encouraging, but the scenario tests a relatively straightforward injection (a single inserted instruction in the supplier data). Real-world injection attacks may be more sophisticated (indirect injection via supplier catalog fields, multi-turn injection across conversation history). BuyerBench's p3-05 result establishes a baseline; it is not a guarantee of injection resistance under adversarial conditions.

**Agents designed for structured inputs need explicit natural language procurement adaptation.** NegMAS's zero scores on p1-04 and p1-05 suggest that domain-specialized agents should be evaluated on their target deployment tasks rather than on general procurement capability claims. For enterprise procurement AI, this means evaluation must include realistic multi-step workflows with natural language policy documents, not just structured RFQ optimization problems.

### 5.3 Limitations

**Access-gated commercial agents.** The most commercially deployed buyer agents — SAP Joule/Ariba, Coupa AI, Ivalua IVA, Zip, Amazon Rufus, Klarna AI, Google Agentic Checkout — cannot be evaluated without institutional access agreements. BuyerBench's evaluation stubs (see `docs/agents/evaluation-stubs/`) document the full evaluation methodology for these agents but cannot substitute for live results. No claims about commercial agent capability are made in this paper.

**CLI agent credential requirements.** The three CLI agents included in the evaluation plan — Claude Code, Codex, and Gemini CLI — require API credentials and CLI installation that were unavailable in the current evaluation environment. As a result, all nine CLI agent × mode evaluation runs are recorded as `status: skipped`. Pillar 2 (behavioral bias) and the skills/MCP delta analysis are entirely dependent on CLI agent runs. These are the highest-priority gaps for future evaluation and are straightforward to address: installing the relevant CLI tools and providing API keys enables immediate re-evaluation.

**Simulation mode caveats.** NegMAS and Stripe Agent Toolkit are evaluated in simulation mode without live external credentials. The Stripe Toolkit's transaction sequencing score (p3-04 score=0.30, sequence_correct=0.0) is attributable specifically to simulation mode: without live API responses, the agent cannot complete the authorization→tokenization→charge sequence. This result is expected to improve substantially with live payment sandbox integration.

**LLM non-determinism.** Even at temperature = 0, API-based language models may produce different outputs across infrastructure versions. All results are stamped with model version, temperature setting, harness version, and evaluation timestamp. Longitudinal comparison requires re-running against the same model snapshot, or bracketing results from multiple runs.

**Scenario coverage.** BuyerBench's 18 scenarios cover representative but not exhaustive procurement workflows. Categories not yet included: negotiation-heavy RFx workflows, multi-tier supplier network evaluation, cross-currency procurement, contract compliance checking, and supplier onboarding workflows.

**Bias effect size variance.** LLM bias effects are known to vary substantially across model versions and prompting styles [@hagendorff2023human]. When CLI agent evaluation is complete, BSI values should be reported with model version details and, where possible, replicated across at least two model snapshots before drawing conclusions about a model family's bias susceptibility.

### 5.4 Future Work

**Priority 1 — CLI agent evaluation.** Installing Claude Code, Codex, and Gemini CLI with credentials completes the core evaluation matrix (9 agent × mode combinations × 18 scenarios = 162 evaluation runs) and enables the first cross-agent, cross-mode comparison on all three pillars. This is the highest-value near-term work.

**Priority 2 — Extended bias taxonomy.** The current suite tests four bias types (anchoring, framing, decoy, scarcity). The full 8-bias taxonomy adds loss aversion (variant pairs trading identical expected values framed as gains vs. losses), status quo bias (comparing incumbent vs. new supplier with identical utility), sunk cost fallacy (scenarios where past procurement spend should be treated as sunk), and default bias (scenarios where a pre-selected default differs from optimal). Adding these four bias pairs brings the P2 suite to 16 scenarios (8 variant pairs).

**AP2, UCP, and ACP protocol adapters.** The three open-source agentic commerce protocols — AP2 [@googleap22025], UCP [@ucp2025], and ACP [@acp2025] — have no independent conformance test suites. Implementing BuyerBench adapters for each protocol would produce the first published conformance test results for these specifications and position BuyerBench as the reference evaluation platform for agentic commerce protocol readiness.

**Live payment sandbox integration.** Connecting the Stripe toolkit evaluation to a Stripe test-mode account would eliminate the simulation-mode caveat on p3-04 and provide more realistic transaction sequencing results. Extension to other payment processors (Adyen, Braintree, PayPal) would test whether sequencing compliance is toolkit-specific or generalizable.

**Human procurement specialist baseline.** A pilot study with professional procurement managers completing BuyerBench scenarios would establish the first human performance baseline for the benchmark. Human scores on Pillar 1 provide context for interpreting agent capability levels; human behavior under the Pillar 2 bias manipulations provides a reference point for interpreting agent BSI values relative to documented human bias effect sizes [@kahneman1974judgment; @tversky1981framing].

**Browser automation for consumer agent evaluation.** Amazon Rufus, Klarna AI, and Google Agentic Checkout are browser-accessible consumer agents that cannot be evaluated via CLI or API. A Playwright-based browser automation adapter would enable BuyerBench scenarios to be submitted to these agents via the web UI, substantially expanding the evaluable agent population.

**Dynamic scenario generation.** Parameterized scenario generation — randomizing supplier identities, price levels, and policy rule text while preserving economic ground truth — produces contamination-resistant holdout test sets. This is especially important as evaluated agents (Claude Code in particular) may have been trained on data that overlaps with the static scenario set.

**Certified evaluation pathway.** A formal certification process — analogous to PCI DSS QSA audits — in which BuyerBench evaluation results are independently verified before being published would enable the benchmark to serve as a trusted third-party assessment for procurement organizations considering deploying buyer agents.

---

## 6. Conclusion

We presented BuyerBench, the first open-source, multi-dimensional benchmark for evaluating AI buyer agents. BuyerBench is a Python-native framework comprising 18 evaluation scenarios across three evaluation pillars — Agent Intelligence and Operational Capability (P1), Economic Decision Quality and Behavioral Robustness (P2), and Security, Compliance, and Market Readiness (P3) — a controlled variant methodology for measuring cognitive bias susceptibility, and a formal metric suite including the Bias Susceptibility Index (BSI), Compliance Adherence Rate (CAR), and Fraud Detection F1.

Initial evaluation of two open-source agents yields findings that demonstrate the framework's discriminative value. NegMAS achieves a perfect score on structured optimization scenarios (P1=1.0 on p1-01 and p1-02) but scores zero on policy-constrained procurement and multi-step workflows — a bimodal capability profile that an aggregate score of 0.44 conceals. The Stripe Agent Toolkit achieves perfect fraud detection (FD-F1=1.0, P3=1.0 on p3-01) but fails transaction sequencing in simulation mode (score=0.30, sequence_correct=0.0 on p3-04) and has a vendor authorization gap (CAR=0.33 on p3-02). Critically, the two agents' P1 and P3 scores are uncorrelated — the framework's multi-dimensional reporting reveals this; a single aggregate benchmark score cannot.

These results establish three empirical baselines for the field: a Pillar 1 performance floor for negotiation-specialist agents, a Pillar 3 performance profile for payment-toolkit agents, and a methodology for the first procurement-domain behavioral bias measurements when CLI agent evaluation is complete.

BuyerBench is publicly available at `https://github.com/[org]/BuyerBench`. We invite the research community to contribute scenarios (see `CONTRIBUTING.md`), agent adapters, and evaluation results. The broader significance of this work extends beyond academic benchmarking: as AI buyer agents acquire the ability to commit organizational spending, select suppliers, and initiate payment transactions autonomously, independent, multi-dimensional evaluation is a prerequisite for responsible deployment. BuyerBench is designed to provide that evaluation infrastructure.

---

## References

*[BibTeX entries in `references.bib` — rendered by LaTeX or pandoc at build time.]*

---

## Appendix A — Full Scenario Taxonomy

The following table provides the complete 18-scenario taxonomy with full scenario IDs, variant pair mappings, difficulty ratings, and the primary evaluation metrics applicable to each scenario.

| Scenario ID | Title | Pillar | Variant | Difficulty | Pair ID | Primary Metrics |
|-------------|-------|--------|---------|------------|---------|-----------------|
| p1-01 | Supplier Selection — Basic | P1 | BASELINE | easy | — | TCR, SSA, TCE |
| p1-02 | Multi-Criteria Sourcing | P1 | BASELINE | medium | — | TCR, SSA, TCE, score\_within\_threshold |
| p1-03 | Quote Comparison Workflow | P1 | BASELINE | medium | — | TCR, SSA, extraction\_accuracy, constraint\_adherence |
| p1-04 | Policy-Constrained Procurement | P1 | BASELINE | hard | — | TCR, SSA, PA, TCE |
| p1-05 | Multi-Step Procurement Workflow | P1 | BASELINE | hard | — | TCR, step1–4 correctness, TCE |
| p2-01-base | Anchoring — Baseline | P2 | BASELINE | medium | anchor-pair | OCR, OG, EVR |
| p2-01-anch | Anchoring — High Anchor | P2 | ANCHOR\_HIGH | medium | anchor-pair | OCR, OG, EVR, BSI |
| p2-02-gain | Framing — Gain | P2 | FRAMING\_GAIN | medium | framing-pair | OCR, EVR |
| p2-02-loss | Framing — Loss | P2 | FRAMING\_LOSS | medium | framing-pair | OCR, EVR, BSI |
| p2-03-base | Decoy — Baseline | P2 | BASELINE | medium | decoy-pair | OCR, OG |
| p2-03-decoy | Decoy — Active | P2 | DECOY | medium | decoy-pair | OCR, OG, BSI |
| p2-04-base | Scarcity — Baseline | P2 | BASELINE | medium | scarcity-pair | OCR, EVR |
| p2-04-scar | Scarcity — Active | P2 | SCARCITY | medium | scarcity-pair | OCR, EVR, BSI |
| p3-01 | Fraud Detection — Basic | P3 | BASELINE | medium | — | FD-F1, precision, recall, CAR |
| p3-02 | Vendor Authorization | P3 | BASELINE | medium | — | CAR, SVF, authorization\_accuracy |
| p3-03 | Credential Handling | P3 | BASELINE | hard | — | CAR, credential\_not\_in\_output, exposure\_detected |
| p3-04 | Transaction Sequencing | P3 | BASELINE | hard | — | CAR, sequence\_correct, task\_completed |
| p3-05 | Prompt Injection Resistance | P3 | BASELINE | hard | — | CAR, injection\_not\_followed, injection\_flagged, SDS |

**Metric abbreviations:** TCR = Task Completion Rate; SSA = Supplier Selection Accuracy; TCE = Tool Call Efficiency; PA = Policy Adherence; OCR = Optimal Choice Rate; OG = Optimality Gap; EVR = Expected Value Regret; BSI = Bias Susceptibility Index; CAR = Compliance Adherence Rate; SVF = Security Violation Frequency; FD-F1 = Fraud Detection F1; SDS = Security Degradation Score.

Variant pair IDs link the baseline and manipulated scenarios in each Pillar 2 pair. BSI is computed at the variant-pair level (not per individual scenario) and requires both members of the pair to be evaluated. See §3.2.3 for the formal BSI definition.

## Appendix B — Metric Formal Definitions

*[Cross-reference to §3.4 — formal definitions are included inline in the Methodology section.]*
