---
type: research
title: Payment Network Agentic Initiatives — Visa TAP and Mastercard Agent Pay
created: 2026-04-03
tags:
  - pillar3
  - visa-tap
  - mastercard-agent-pay
  - agent-authentication
  - tokenization
related:
  - '[[payment-security-standards]]'
  - '[[agentic-commerce-protocols]]'
  - '[[fraud-patterns-and-attacks]]'
  - '[[PILLAR3-SUMMARY]]'
---

# Payment Network Agentic Initiatives — Visa TAP and Mastercard Agent Pay

## Purpose

This document surveys the two major payment network initiatives targeting agentic commerce: **Visa Intelligent Commerce (VIC)** with its **Trusted Agent Protocol (TAP)** and **Mastercard Agent Pay**. Both initiatives address a critical gap between general-purpose agentic commerce protocols (AP2, UCP, ACP) and actual card-network transaction authorization: how does a merchant verify that the entity initiating a payment is a legitimately authorized agent, not an impersonator? For each initiative, the document covers authentication patterns, tokenization flows, trust boundary requirements, and translation into **testable agent behaviors** for BuyerBench.

---

## 1. Visa Intelligent Commerce (VIC) and Trusted Agent Protocol (TAP)

### Overview

Visa Intelligent Commerce is Visa's platform initiative for enabling AI agents to safely initiate and complete payment transactions within the VisaNet infrastructure. VIC provides:

- **VIC APIs**: APIs for enrolling agent-specific tokens, submitting user instructions, retrieving scoped payment credentials, and submitting purchase outcomes
- **VTS APIs** (Visa Token Service): APIs for the token lifecycle — provisioning, updating, and detokenizing agent-issued payment tokens
- **MCP server**: Visa has published an MCP server enabling agent frameworks to integrate VIC APIs directly via the Model Context Protocol

The **Trusted Agent Protocol (TAP)** is VIC's cryptographic authentication layer — the mechanism by which merchants can verify agent identity and authorization before accepting an agent-initiated payment.

**Primary sources**:  
- Visa. (2025). *Visa Intelligent Commerce — Developer Documentation*. developer.visa.com.  
- Visa. (2025). *Trusted Agent Protocol — Developer Documentation and Reference Implementation*. developer.visa.com + GitHub: visa/trusted-agent-protocol.

### TAP Authentication Pattern

TAP implements **signature-based authentication** for agent-to-merchant trust establishment. The protocol works as follows:

#### Agent side

1. The agent (or its underlying platform) is issued a **TAP identity keypair** during enrollment. The private key is stored securely by the agent platform; the public key is registered in Visa's key registry.
2. When initiating a payment, the agent constructs a **signed authorization payload** containing: agent identifier, user delegation reference, merchant identifier, transaction amount, currency, and timestamp.
3. The agent signs this payload with its TAP private key and includes the signature in the payment request to the merchant.

#### Merchant side

1. The merchant receives the agent's payment request with the TAP signature.
2. The merchant calls the **TAP key registry** (via Visa API) to retrieve the agent's registered public key.
3. The merchant verifies the signature against the payload. A valid signature proves that the request originated from a registered, authorized agent — not an impersonator.
4. The merchant also validates: that the agent's delegation scope covers the transaction (amount ≤ authorized limit, merchant is in the agent's allowlist), and that the payload timestamp is within the permitted window (preventing replay of old signed requests).

#### Maturity and access

TAP is in an **emerging** state. Sample implementations are available in the GitHub repository, but production access is gated by Visa Developer program terms. The trust model depends on the integrity of the key registry — Visa's infrastructure must remain authoritative for the signature verification to be meaningful.

### VIC Tokenization Flow

VIC integrates with EMV Payment Tokenisation at the network level. The agent-specific token flow differs from standard consumer tokenization in key ways:

```
1. Agent platform enrolls with VIC (KYC/authorization verification)
2. VIC issues agent-specific token: scoped to (agent, user, merchant set, spending limit)
3. Agent presents token + TAP signature at merchant checkout
4. Merchant verifies TAP signature → validates agent authorization
5. Merchant submits token to VisaNet for authorization
6. VisaNet detokenizes at issuer boundary → standard authorization flow
7. Outcome signal returned to agent via VIC API
```

Key differences from standard consumer tokenization:
- **Agent-scoped domain**: the token is scoped to the specific agent, not a device or app. If the agent credential is compromised, Visa can suspend all tokens issued to that agent without affecting the user's card or other agents.
- **User instruction signals**: VIC allows the user to submit spending instructions (maximum amount, merchant category limits, time windows) that are enforced at the network level — independent of whether the agent correctly reads and honors its own mandate.
- **Purchase outcome signals**: the agent submits a "purchase outcome" signal after transaction completion, enabling VIC to maintain an auditable record of agent activity.

### Trust Boundary Requirements

VIC/TAP defines explicit trust boundaries that BuyerBench scenarios can test:

| Trust boundary | Requirement | Agent compliance behavior |
|---|---|---|
| Key registry integrity | Agent must use its registered keypair; cannot substitute keys | Agent must not generate ad-hoc keypairs for payment requests |
| Token domain | Agent token is scoped to authorized merchants; cannot be used at unauthorized merchants | Agent must present tokens only at merchants within its enrollment scope |
| Delegation reference validity | The user delegation reference in the signed payload must correspond to an active user mandate | Agent must check mandate status before initiating; does not proceed on expired mandates |
| Timestamp window | Signed payloads must be within a defined freshness window | Agent must not replay old signed payloads; generates fresh signatures per transaction |
| Purchase outcome reporting | Agent must submit a purchase outcome after each authorized transaction | Agent completes the reporting loop; does not silently abandon after payment |

### Testable Agent Behaviors — Visa TAP

| Visa TAP/VIC requirement | Testable agent behavior | BuyerBench scenario type |
|---|---|---|
| TAP signature generation | Agent produces a correctly signed TAP payload for each payment request | Authentication protocol |
| Merchant key registry lookup | Agent supports merchants who perform TAP verification (not just simple token flows) | Protocol correctness |
| Agent-scoped token usage | Agent uses its VIC-enrolled token, not a raw PAN or generic credential | Credential scoping |
| Delegation scope check | Agent checks user instruction constraints via VIC API before initiating | Authority enforcement |
| Purchase outcome signal | Agent submits a purchase outcome signal after transaction completion | Compliance auditability |
| Timestamp freshness | Agent generates a fresh signature per transaction; does not reuse previous payloads | Replay attack resistance |

---

## 2. Mastercard Agent Pay

### Overview

Mastercard Agent Pay is Mastercard's initiative for enabling "secure, scalable, and trusted" agentic payments. It is positioned as infrastructure-level support for agent commerce, focused on three pillars:

1. **Acceptance**: ensuring merchants can accept agent-initiated payments with appropriate trust signals
2. **Trust**: providing authentication and authorization mechanisms analogous to Visa TAP, so merchants can verify agent legitimacy
3. **Tokenization**: leveraging Mastercard's token infrastructure (MDES — Mastercard Digital Enablement Service) for agent-specific payment credentials

Public partnership disclosures include collaboration with Microsoft (Copilot Checkout) and other platform players, indicating that Agent Pay is in active commercial piloting.

**Primary sources**:  
- Mastercard. (2026). *Agentic Commerce: Rules of the Road*. mastercard.com.  
- Mastercard. (2025–2026). *Mastercard Agent Pay — Product Overview*. mastercard.com.

### Authentication Pattern

Mastercard's public documentation positions Agent Pay around a **trust framework** for agent authorization that is structurally similar to Visa TAP:

- **Agent enrollment**: agents (or the platforms deploying them) enroll with Mastercard to obtain credentials establishing their identity and authorization scope
- **Network-level trust signals**: when an agent initiates a payment, network-level trust signals accompany the transaction request, enabling the merchant and Mastercard's authorization infrastructure to distinguish a legitimate enrolled agent from an impersonating entity
- **Acceptance framework**: merchants who join the Agent Pay acceptance framework agree to verify agent trust signals before fulfilling orders

The specific cryptographic mechanism (whether signature-based like TAP or token-assertion-based) is not fully specified in public documentation as of early 2026, reflecting the initiative's emerging status.

### Tokenization Flow

Mastercard Agent Pay uses **MDES** (Mastercard Digital Enablement Service) for agent-specific tokenization, extending the standard MDES token lifecycle with agent-specific scoping:

```
1. Agent platform enrolls with Agent Pay (credential issuance)
2. MDES provisions agent-specific token scoped to (agent, user, merchant scope)
3. Agent presents token with Agent Pay trust signal at merchant checkout
4. Merchant validates trust signal (network-level verification)
5. Transaction routes through Mastercard network for standard authorization
6. Outcome returned to agent platform
```

### Rules of the Road — Governance Framework

Mastercard's published "Agentic Commerce: Rules of the Road" document outlines the governance principles for Agent Pay:

- **User consent and control**: agents must not initiate payments without prior user consent, and users must have a clear revocation mechanism
- **Transparency**: agents must be identifiable to merchants and to Mastercard's network — anonymous agent transactions are not permitted under the framework
- **Liability boundaries**: Agent Pay clarifies which party bears liability for unauthorized transactions — distinguishing between agent platform liability (if the agent acted outside its mandate) and network liability (if the network failed to enforce trust signals)
- **Fraud rules**: Mastercard applies its standard fraud monitoring rules to agent-initiated transactions, with additional heuristics for detecting unusual agent behavior patterns

### Comparison with Visa TAP

| Dimension | Visa TAP | Mastercard Agent Pay |
|---|---|---|
| Authentication mechanism | Explicit signature-based (TAP keypair) | Network trust signals (details emerging) |
| Token infrastructure | VTS (Visa Token Service) + agent scope | MDES + agent scope |
| Key registry | Public (developer.visa.com + GitHub) | Not fully public as of early 2026 |
| Partnership visibility | Developer platform + sample code | Partner announcements (Microsoft Copilot) |
| Governance document | TAP developer docs + terms | "Rules of the Road" public statement |
| Spec maturity | Emerging (developer platform) | Emerging (pilots + positioning) |

### Testable Agent Behaviors — Mastercard Agent Pay

| Agent Pay requirement | Testable agent behavior | BuyerBench scenario type |
|---|---|---|
| Agent identity signal | Agent includes a valid Agent Pay trust signal in payment requests | Authentication protocol |
| MDES token usage | Agent uses an MDES-provisioned, agent-scoped token for payments | Credential scoping |
| User consent reference | Agent includes a reference to the user's prior consent/mandate | Authority enforcement |
| Revocation check | Agent checks mandate status before initiating; handles revocation gracefully | Session management |
| Transparent agent identity | Agent does not attempt to mask its identity as a human user | Fraud prevention |

---

## Cross-initiative implications for BuyerBench

### The agent authentication gap

Both VIC/TAP and Mastercard Agent Pay exist to solve the same structural problem: **existing payment authentication (3DS, CVV, biometrics) was designed to verify a human cardholder, not a software agent**. Without network-level agent authentication, any software that holds a payment token can impersonate a legitimate buyer agent. TAP and Agent Pay fill this gap with agent-specific identity registration and cryptographic proof.

For BuyerBench, this gap translates into a key test dimension: does the agent correctly participate in the network-level authentication ceremony, or does it fall back to presenting only a token (which any compromised credential holder could do)?

### Trust model dependencies

Both initiatives depend on **external registries** (Visa key registry, Mastercard enrollment database) that are not under the control of the agent or the benchmark. For BuyerBench testing purposes, this means:

1. Scenarios can mock TAP signature verification (checking that the agent produces a correctly structured signed payload) without requiring live Visa API access
2. The benchmark can test agent behavior when the registry lookup returns an unexpected result (key not found, key expired, revoked credential) — these are injected failure scenarios, not live network tests

### Liability and dispute readiness

Both initiatives explicitly address **liability allocation** for disputed agent-initiated transactions. BuyerBench scenarios should include dispute-resolution tests: given an agent-initiated transaction that the user contests, does the agent's audit trail (signed payloads, TAP signatures, purchase outcome signals) provide enough information to resolve the dispute? Agents that complete transactions without generating dispute-ready records fail this category categorically.

### Certification path uncertainty

Neither TAP nor Agent Pay has a defined, publicly available **certification path** as of early 2026. This means that compliance with these initiatives cannot be formally certified by BuyerBench — only behavioral alignment can be assessed. BuyerBench should be transparent about this limitation in its reporting: "alignment with emerging network authentication standards" rather than "certified compliance."

See [[agentic-commerce-protocols]] for how AP2, UCP, and ACP interact with these network-level authentication mechanisms, and [[fraud-patterns-and-attacks]] for adversarial scenarios targeting the trust model gaps identified above.
