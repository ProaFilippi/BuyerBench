---
type: research
title: Agentic Commerce Protocols — AP2, UCP, and ACP
created: 2026-04-03
tags:
  - pillar3
  - ap2
  - ucp
  - acp
  - agentic-commerce
  - protocols
related:
  - '[[payment-security-standards]]'
  - '[[network-initiatives]]'
  - '[[fraud-patterns-and-attacks]]'
  - '[[PILLAR3-SUMMARY]]'
---

# Agentic Commerce Protocols — AP2, UCP, and ACP

## Purpose

This document provides an in-depth survey of three emerging open protocols designed to standardize the "intent → cart → payment" flow for AI buyer agents: **Agent Payments Protocol (AP2)**, **Universal Commerce Protocol (UCP)**, and **Agentic Commerce Protocol (ACP)**. For each protocol, the document covers governance model, specification maturity, security profile (credential scoping, signing, dispute-ready records), interoperability positioning, and translation into **testable agent behaviors** for BuyerBench.

All three protocols are in active development as of 2026 and address a core structural gap: the absence of any standardized, secure, auditable mechanism for agents to initiate commerce transactions on behalf of users without exposing raw credentials or bypassing payment-network controls.

---

## 1. Agent Payments Protocol (AP2)

### Overview and governance

AP2 is an open protocol (Apache-2.0) for agent-initiated payments. It was announced by Google Cloud and is maintained at `github.com/google-agentic-commerce/AP2`. The protocol ships with reference implementations in Python and Android, with v0.1.0 as the first versioned release. The governance model is community-driven through GitHub — issues, pull requests, and versioned releases serve as the standards-development process.

**Primary source**: Google Cloud. (2025). *Announcing Agents to Payments: AP2 Protocol*. Google Cloud Blog + GitHub repository.

### Specification scope and maturity

AP2 targets the "last mile" of agent-initiated commerce: the handoff between an AI agent (acting as the authorized buyer) and a payment provider. It supports multiple payment instrument types including cards, stablecoins, and real-time transfer flows. The protocol defines:

- **Session primitives**: how an agent establishes a payment session on behalf of a user
- **Authorization scope**: how spending limits, merchant allowlists, and currency constraints are encoded and enforced
- **Payment type dispatch**: how different instrument types (card, real-time transfer, stablecoin) route to different handlers
- **Audit record format**: the required transaction record structure for dispute resolution

Maturity label: **Emerging**. The v0.1.0 release indicates that the protocol specification and reference samples are functional, but the governance process for conformance testing, certification, and long-term stewardship remains in early stages.

### Security profile

**Credential scoping**: AP2 does not require agents to hold raw card credentials. Instead, it delegates credential management to the payment provider, with the agent operating on tokens/session handles. Agents receive an authorization handle scoped to a specific payment session, not a reusable credential.

**Authorization signing**: AP2 samples use cryptographic signing to authenticate agent requests. Each payment initiation includes a signature that can be verified by the merchant and payment provider — enabling non-repudiable audit trails. This mirrors the approach Visa Trusted Agent Protocol uses at the network layer (see [[network-initiatives]]).

**Dispute-ready records**: AP2 mandates that every transaction emit a structured record containing: session ID, agent identifier, authorization scope, payment type, amount, merchant, timestamp, and the cryptographic signature of the request. This record is designed to survive disputes — if a user contests an agent-initiated transaction, the record provides evidence of the scope of delegation.

**Interoperability with PCI/EMV**: AP2 positions itself as operating above the PCI DSS and EMV tokenisation layers, not replacing them. Merchants implementing AP2 still handle PCI compliance; AP2 adds agent-specific authorization semantics on top.

### Interoperability positioning

AP2 is explicitly designed to be compatible with UCP. Where UCP defines the commerce-session primitives (cart, checkout, fulfillment signals), AP2 focuses specifically on the payment leg. Together they are positioned as complementary: UCP handles the shopping session, AP2 handles payment authorization within that session.

### Testable agent behaviors derived from AP2

| AP2 requirement | Testable agent behavior | BuyerBench scenario type |
|---|---|---|
| Scoped authorization handle | Agent does not use a payment handle outside its provisioned session | Credential scoping |
| Signed payment request | Agent produces a verifiable signed record for each payment initiation | Audit trail integrity |
| Payment type correctness | Agent selects the correct instrument type and routes to the correct handler | Protocol correctness |
| Amount within delegation scope | Agent refuses payments exceeding the user's authorized limit | Authority enforcement |
| Dispute-ready record emission | Agent emits a complete, well-formed transaction record after every payment | Compliance auditability |

---

## 2. Universal Commerce Protocol (UCP)

### Overview and governance

UCP is an open standard (Apache-2.0) for interoperable commerce primitives among platforms, AI agents, businesses, payment service providers (PSPs), and credential providers. It is maintained at `github.com/universal-commerce-protocol/ucp` and is documented at `ucp.dev`. UCP was announced via the Google Developer Blog and is designed to work with existing retail infrastructure.

**Primary source**: UCP Authors / community. (2025). *Universal Commerce Protocol specification and documentation*. GitHub + ucp.dev.

### Specification scope and maturity

UCP focuses on standardizing the **commerce session** — the sequence from intent through cart construction, checkout, and fulfillment signals. Key specification primitives include:

- **Commerce session object**: a structured, signed representation of a buyer's intent, constraints, and cart, which can be passed among platforms without loss of context
- **Credential provider interface**: how payment credentials (tokens, handles) are requested and scoped without exposing raw account data
- **Merchant adapter**: how a merchant (or business) declares its supported payment methods, fulfillment capabilities, and return policies in a machine-readable form that agents can parse
- **Fulfillment signal**: a structured acknowledgment that the merchant has accepted the order and is processing fulfillment — the agent's signal that the transaction is complete

UCP explicitly supports **secure checkout sessions with or without human intervention**, making it directly applicable to autonomous buyer agent flows where the human authorizes the agent upfront and is not present at checkout time.

Maturity label: **Emerging**. Multi-language tooling and schema validators are available, and the standard has initial merchant/platform adoption under exploration, but conformance certification is not yet defined.

### Security profile

**Credential isolation**: UCP defines a credential provider role that is separate from the platform/agent role. The agent never holds the credential directly; it requests a scoped handle from the credential provider, which validates the agent's authorization before issuing it. This separation enforces least-privilege at the protocol level — analogous to the PCI DSS Requirement 7 principle.

**Commerce session integrity**: The commerce session object is designed to be cryptographically signed. A merchant receiving a session from an agent can verify that the session originated from an authorized agent acting on behalf of the stated user, and that the session content has not been tampered with.

**Interoperability security**: UCP defines how session data is serialized and validated across platform boundaries. The schema validators included in the repo enforce that sessions conform to spec — reducing implementation-level security gaps that arise from ad-hoc JSON handling.

**Dispute-ready records**: Like AP2, UCP mandates that session records — including agent identity, user delegation scope, cart contents, and fulfillment signals — be preserved in a dispute-ready format. These records align with the audit logging requirements of PCI DSS Requirement 10.

### Interoperability positioning

UCP is positioned as a **cross-protocol interoperability layer**. It is designed to sit above PCI DSS and EMV standards (which operate at the payment data layer) and can work alongside AP2 (payment) and ACP (agent-to-merchant commerce). The Google developer documentation references UCP compatibility with Google Pay APIs and Google Shopping surfaces, indicating platform-level commitment.

### Testable agent behaviors derived from UCP

| UCP requirement | Testable agent behavior | BuyerBench scenario type |
|---|---|---|
| Credential provider isolation | Agent requests a scoped credential handle; does not construct raw payment payloads | Credential scoping |
| Signed session construction | Agent produces a well-formed, signed commerce session object | Protocol correctness |
| Merchant adapter parsing | Agent correctly reads and respects merchant-declared payment methods and constraints | Workflow accuracy |
| Fulfillment signal handling | Agent waits for and validates the fulfillment signal before marking a transaction complete | Transaction integrity |
| Session scope enforcement | Agent does not reuse a session object for a different merchant or transaction | Authority enforcement |

---

## 3. Agentic Commerce Protocol (ACP)

### Overview and governance

ACP is an open standard (Apache-2.0) maintained by **OpenAI and Stripe** at `github.com/agentic-commerce-protocol/agentic-commerce-protocol`. The spec is documented at `agenticcommerce.dev` and is also referenced in OpenAI's developer documentation. ACP is **explicitly labelled "beta"** in the repository, reflecting that the specification is actively evolving and that implementations should expect breaking changes.

The governance model is more formally structured than AP2: the repository includes a `GOVERNANCE.md` defining decision-making processes, an RFC mechanism for proposing specification changes, and versioned spec snapshots (initial release + subsequent enhancements as RFCs). OpenAI and Stripe serve as co-stewards.

**Primary source**: OpenAI + Stripe. (2025). *Agentic Commerce Protocol specification and RFCs*. GitHub + agenticcommerce.dev.

### Specification scope and maturity

ACP focuses on the interface between **buyer agents, merchants, and payment providers** for completing purchases. Its core concepts include:

- **Purchase intent**: a structured representation of what the agent wants to buy, on whose behalf, and under what constraints (amount, merchant, timing)
- **Payment handler**: a role in the ACP spec for the entity (usually a PSP like Stripe) that processes the payment leg of the transaction
- **Merchant endpoint**: a defined interface that merchants implement to receive agent-initiated purchase intents and respond with order confirmations or rejections
- **Authorization token**: an agent-specific, time-limited authorization token that scopes the agent's ability to initiate payments — issued by the payment handler after verifying the user's delegation

ACP's beta status reflects that several critical security and interoperability profiles are still under active RFC discussion, including: dispute resolution workflows, token revocation propagation, and cross-PSP interoperability.

Maturity label: **Beta/Emerging**. The OpenAI + Stripe co-stewardship signals significant ecosystem commitment, but the beta label and active RFCs indicate that implementations must track spec evolution carefully.

### Security profile

**Authorization token model**: ACP's authorization token is central to its security design. The token encodes: user identity, agent identity, spending limit, merchant scope (allowlist or wildcard), and expiry. Agents present this token to merchants; merchants verify it with the payment handler before fulfilling orders.

**Signing and verification**: ACP defines signing requirements for purchase intents. A signed intent provides non-repudiation — if a user disputes an agent-initiated purchase, the signed intent shows the agent acted within (or outside) its authorized scope.

**Merchant endpoint security**: ACP requires merchant endpoints to implement rate limiting, token verification, and idempotency keys for purchase requests. This prevents replay attacks and double-charge vulnerabilities that could arise from agent retry logic.

**Spec churn risk**: Because ACP is in beta, security profiles defined today may be revised. BuyerBench scenarios testing ACP compliance must track spec versions and note which version of the protocol each scenario targets.

**Merchant-of-record boundaries**: ACP clarifies the boundary between the agent (buyer), the merchant (seller), and the payment handler (PSP). This clarity is important for liability: if the agent acts outside its scope, the signed intent record determines who bears responsibility.

### Interoperability positioning

ACP positions itself as a complement to existing payment infrastructure rather than a replacement. The "payment handler" role is designed for PSPs (Stripe being the canonical example), meaning ACP sits above the card-network and PSP layers. ACP is designed to be compatible with tokenized payment flows (EMV tokenisation) — agents use tokens rather than raw PANs, and the payment handler manages the tokenisation lifecycle.

### Comparison with AP2 and UCP

| Dimension | AP2 | UCP | ACP |
|---|---|---|---|
| Primary steward | Google Cloud | Community (Google-adjacent) | OpenAI + Stripe |
| Spec maturity | Emerging (v0.1.0) | Emerging | Beta (explicit) |
| Core focus | Payment leg | Commerce session | End-to-end agent-to-merchant |
| Payment handler role | Yes (protocol-defined) | Via credential provider | Yes (PSP role) |
| Signing/signing requirements | Yes | Yes | Yes |
| Formal governance | GitHub | GitHub | GitHub + governance.md + RFC process |
| PCI/EMV layer | Above | Above | Above |

### Testable agent behaviors derived from ACP

| ACP requirement | Testable agent behavior | BuyerBench scenario type |
|---|---|---|
| Authorization token presentation | Agent presents a valid, unexpired token to the merchant endpoint | Authentication protocol |
| Signed purchase intent | Agent produces a signed purchase intent that matches its authorization scope | Audit trail integrity |
| Token scope enforcement | Agent refuses to initiate purchases outside the token's merchant scope | Authority enforcement |
| Idempotency key usage | Agent uses a unique idempotency key per purchase attempt; does not reuse on retry | Replay attack resistance |
| Spec version declaration | Agent declares which ACP version it implements in its requests | Protocol correctness |

---

## Cross-protocol implications for BuyerBench

### The layered protocol stack

A compliant buyer agent in an agentic commerce environment operates across multiple protocol layers simultaneously:

```
User mandate (scope, limits, merchant allowlist)
    ↓
Commerce session (UCP — intent, cart, fulfillment)
    ↓
Payment authorization (AP2 or ACP — signed payment initiation)
    ↓
Token-based payment (EMV Tokenisation — PAN not exposed)
    ↓
CNP authentication (EMV 3DS — frictionless or 3RI)
    ↓
Data protection baseline (PCI DSS — audit logging, no raw CHD)
```

An agent failing at any layer fails the Pillar 3 evaluation. BuyerBench scenarios should test failures at each layer independently to identify where specific agent implementations break down.

### Interop volatility as a test dimension

The beta status of ACP and the emerging status of AP2 and UCP mean that **protocol conformance testing requires version pinning**. BuyerBench scenario metadata must record the protocol version targeted, so that results can be compared across agent implementations that may have been built against different spec revisions. This is analogous to dependency pinning in software testing.

### Common failure modes across all three protocols

1. **Credential leakage**: Agent extracts the authorization token or session credential and passes it in cleartext through tool arguments
2. **Scope bypass**: Agent constructs a manual payment payload that bypasses the protocol's authorization token mechanism
3. **Replay of signed records**: Agent reuses a signed purchase intent from a previous transaction
4. **Spec ignorance**: Agent ignores protocol-required fields (idempotency keys, version declarations) that appear optional but are required for compliance
5. **Fulfillment-before-confirmation**: Agent marks a transaction complete before receiving a valid merchant fulfillment signal

See [[fraud-patterns-and-attacks]] for detailed adversarial scenarios targeting protocol-level vulnerabilities, and [[network-initiatives]] for how Visa TAP and Mastercard Agent Pay implement agent-specific authentication that overlaps with these protocols.
