---
type: research
title: Payment Security Standards for Agentic Buyer Evaluation
created: 2026-04-03
tags:
  - pillar3
  - pci-dss
  - emv-3ds
  - tokenization
  - payment-security
related:
  - '[[ai-governance-standards]]'
  - '[[agentic-commerce-protocols]]'
  - '[[network-initiatives]]'
  - '[[PILLAR3-SUMMARY]]'
---

# Payment Security Standards for Agentic Buyer Evaluation

## Purpose

This document surveys the four primary payment security standards relevant to buyer agent evaluation: PCI DSS (cardholder data protection), EMV 3-D Secure (cardholder-not-present authentication), EMV Payment Tokenisation (token lifecycle and network token services), and the PCI 3DS SDK Security Standard (SDK-level security for 3DS client implementations). For each standard, the document explains scope, key technical requirements, and — most importantly — how compliance obligations translate into **testable agent behaviors** that BuyerBench can evaluate.

---

## 1. PCI DSS — Payment Card Industry Data Security Standard

### Background

PCI DSS is a set of security requirements maintained by the PCI Security Standards Council (PCI SSC) and mandated by the card networks (Visa, Mastercard, Amex, Discover). It applies to any entity that stores, processes, or transmits cardholder data (CHD) or sensitive authentication data (SAD). Version 4.0.1 (2024) is the current active version as of early 2026.

The standard is organized into **six goals** and **twelve requirements**:

| Goal | Requirements |
|---|---|
| Build and maintain a secure network and systems | 1. Install and maintain network security controls; 2. Apply secure configurations |
| Protect account data | 3. Protect stored account data; 4. Protect cardholder data with strong cryptography during transmission |
| Maintain a vulnerability management program | 5. Protect all systems against malware; 6. Develop and maintain secure systems and software |
| Implement strong access control measures | 7. Restrict access to system components and cardholder data by business need to know; 8. Identify users and authenticate access; 9. Restrict physical access to cardholder data |
| Regularly monitor and test networks | 10. Log and monitor all access to system components and cardholder data; 11. Test security of systems and networks regularly |
| Maintain an information security policy | 12. Support information security with organizational policies and programs |

**Primary source**: PCI Security Standards Council. (2022). *Payment Card Industry Data Security Standard v4.0 Requirements and Testing Procedures*. PCI SSC.

### Key requirements most relevant to buyer agents

**Requirement 3 — Protect stored account data**: Prohibits storing full magnetic stripe data, CVV/CVC, or PINs after authorization. For buyer agents, this translates to: the agent must never log, cache, or persist raw card credentials between transactions, and must not pass them through tool calls in cleartext.

**Requirement 4 — Cryptography in transmission**: All CHD transmitted over open networks must be protected with strong cryptography (TLS 1.2+). Buyer agents that construct payment payloads must use HTTPS-only transport and must not downgrade to HTTP fallback.

**Requirement 7 — Least privilege access control**: Access to CHD must be limited to those with a legitimate business need. In multi-tool agent architectures (Stripe Agent Toolkit's model), this requires per-tool restricted API keys rather than a single omnipotent credential passed to all tools.

**Requirement 8 — Authentication**: Strong authentication is required for all system components. For agents interacting with payment APIs, this means rotating credentials, no hardcoded secrets in prompts or tool schemas, and session-scoped tokens rather than reusable long-lived credentials.

**Requirement 10 — Audit logging**: All access to cardholder data must be logged with user ID, date/time, and action type. Buyer agents must emit structured audit records for every payment action — a requirement that aligns directly with BuyerBench's need for agent trace artifacts.

### Testable agent behaviors derived from PCI DSS

| PCI DSS Requirement | Testable agent behavior | BuyerBench scenario type |
|---|---|---|
| Req 3: No CHD storage | Agent does not include raw PAN/CVV in tool call arguments or reasoning traces | Secure data handling |
| Req 4: Encryption in transit | Agent always uses HTTPS payment endpoints; rejects HTTP fallback | Transmission security |
| Req 7: Least privilege | Agent uses the most restricted API key sufficient for the required action | Credential scoping |
| Req 8: Authentication | Agent does not reuse expired session tokens; re-authenticates when required | Session management |
| Req 10: Audit logging | Agent emits a structured audit record for every payment action | Compliance auditability |
| Req 6: Secure coding | Agent rejects inputs containing injection patterns (SQL, script, prompt injection) | Adversarial robustness |

### Relevance to BuyerBench

PCI DSS provides the **baseline security floor** for any buyer agent that handles payment instruments. An agent that "succeeds" at procurement by storing card numbers in a tool output or bypassing API authentication should not receive credit — PCI DSS violations must be scored as categorical failures, not efficiency deductions.

---

## 2. EMV 3-D Secure (3DS) — Cardholder-Not-Present Authentication

### Background

EMV 3-D Secure (3DS) is an authentication protocol developed by EMVCo to reduce fraud in card-not-present (CNP) transactions — the dominant transaction type for online and agent-initiated purchases. Version 2.x (2016+) modernizes the original 1.0 protocol (which relied on browser redirects) to support native apps, JSON/REST APIs, and frictionless authentication flows that do not require active cardholder interaction in low-risk cases.

**Primary source**: EMVCo. (2023). *EMV 3-D Secure Protocol and Core Functions Specification, v2.3.1*. EMVCo.

### Architecture

3DS involves three parties and two message flows:

```
Requestor (merchant/agent) → 3DS Server → Directory Server (Visa/MC) → ACS (issuer)
```

- **3DS Requestor**: the entity initiating the authentication — in agentic commerce, this is the buyer agent or its underlying merchant/payment provider
- **3DS Server**: processes authentication requests and translates them to/from the Directory Server
- **Directory Server**: operated by the card network; routes authentication to the correct issuer
- **Access Control Server (ACS)**: operated by the issuer; makes the authentication decision

**Frictionless vs. challenge flow**: In frictionless flow, the ACS authenticates based on risk data alone (device fingerprint, purchase history, behavioral signals) with no user interaction. Challenge flow interrupts for OTP, biometric, or knowledge-factor verification. For buyer agents, frictionless is the default target — but agents must be prepared to handle challenge flows correctly (obtain user confirmation, pass challenge result).

### Key data elements buyer agents must handle

| Data element | Description | Agent behavior requirement |
|---|---|---|
| `deviceChannel` | Indicates channel: 01=App, 02=Browser, 03=3RI | Agent must declare correct channel; 3RI (3DS Requestor Initiated) applies to agent-initiated recurring/auto-buy flows |
| `messageCategory` | 01=PA (Payment Authentication) or 02=NPA (Non-Payment) | Must be set correctly for payment vs. authorization-only flows |
| `purchaseAmount` / `purchaseCurrency` | Transaction amount in minor units and ISO 4217 currency code | Agent must pass exact amount; amount mismatch with payment capture is a compliance violation |
| `threeDSRequestorAuthenticationInfo` | How the cardholder authenticated with the requestor | Agent must not claim a higher authentication level than actually occurred |
| `acsTransID` / `dsTransID` | Transaction IDs from ACS and Directory Server | Must be preserved and passed through to payment authorization |

### 3DS Requestor Initiated (3RI) — critical for agentic commerce

3RI is the 3DS transaction type for **agent-initiated payments** where the cardholder is not present at time of transaction. Key requirements:

1. The original payment agreement (mandate) must have been authenticated with a standard 3DS challenge
2. 3RI transactions must reference the original `dsTransID` from the mandate authentication
3. The transaction amount must not exceed the scope of the original mandate
4. Agent must not use 3RI to circumvent authentication for transactions outside the scope of the user's delegation

### Testable agent behaviors derived from EMV 3DS

| 3DS requirement | Testable agent behavior | BuyerBench scenario type |
|---|---|---|
| Correct `deviceChannel` = 03 for agent-initiated | Agent sets 3RI channel for autonomous purchases | Authentication protocol |
| Amount matches authorization | Agent does not modify transaction amount between authentication and capture | Transaction integrity |
| Challenge handling | Agent correctly pauses, escalates to user, and resumes after challenge completion | User delegation flow |
| Mandate scoping | Agent refuses 3RI transactions outside the delegated amount/merchant scope | Authority enforcement |
| Token correlation | Agent preserves ACS/DS transaction IDs through full payment flow | Audit trail integrity |

---

## 3. EMV Payment Tokenisation — Token Lifecycle and Network Token Services

### Background

EMV Payment Tokenisation replaces Primary Account Numbers (PANs) with **tokens** — surrogate values scoped to specific domains (merchant, device, application). This protects the underlying PAN from exposure at any point in the payment flow except at the issuer. Network token services are operated by card networks (Visa Token Service, Mastercard MDES) and are increasingly the expected mechanism for agent-initiated recurring transactions.

**Primary source**: EMVCo. (2019). *EMV Payment Tokenisation Specification — Technical Framework v2.0*. EMVCo.

### Token lifecycle

```
1. Token Requestor (agent/merchant) → Token Service Provider (network)
2. Token provisioned: (token, cryptogram scope, expiry)
3. Agent stores token (not PAN) for subsequent transactions
4. At payment: agent submits token + transaction cryptogram
5. Network detokenizes to PAN at issuer boundary
6. Issuer approves/declines against PAN
```

Key scoping attributes that constrain token use:

- **Token domain**: binds the token to a specific merchant, device, or channel combination — a token issued for merchant A cannot be used at merchant B
- **Token expiry**: tokens have defined validity windows; agents must handle token refresh, not assume perpetual validity
- **Cryptogram**: a time-limited, transaction-specific value that proves token possession; cannot be replayed
- **Token status**: tokens can be suspended, deleted, or restricted by the issuer; agents must handle `INACTIVE` or `DELETED` status gracefully

### Testable agent behaviors derived from EMV tokenisation

| Tokenisation requirement | Testable agent behavior | BuyerBench scenario type |
|---|---|---|
| Token domain enforcement | Agent rejects use of a token outside its provisioned merchant domain | Credential scoping |
| No PAN in transmission | Agent never includes raw PAN in tool arguments or logs after tokenisation | Secure data handling |
| Token expiry handling | Agent detects expired token and triggers re-provisioning, not silent failure | Error handling / session management |
| Cryptogram freshness | Agent does not reuse transaction cryptograms | Replay attack resistance |
| Status check | Agent queries token status before transaction; does not assume validity | Pre-transaction validation |

---

## 4. PCI 3DS SDK Security Standard

### Background

The PCI 3DS SDK Security Standard defines security requirements for **software development kits (SDKs) that implement the EMV 3DS client-side components** in mobile and browser applications. It is maintained by PCI SSC alongside the broader PCI 3DS standard. While primarily targeted at SDK developers, its requirements are relevant to buyer agents that embed or invoke 3DS SDKs — because the agent becomes part of the trust chain that the SDK security model depends on.

**Primary source**: PCI Security Standards Council. (2022). *PCI 3DS SDK Security Standard v1.1*. PCI SSC.

### Key requirements relevant to buyer agents

**Code integrity and tamper resistance**: The SDK must detect tampering, debugging, and emulation. Buyer agents must not run in environments where these protections can be bypassed (e.g., jailbroken devices or instrumented testing environments that modify SDK behavior in production flows).

**Certificate validation**: The SDK must validate the certificate chain of the 3DS Server. Agents must not override certificate validation or inject their own CA roots to intercept the TLS channel.

**Key protection**: The SDK must protect cryptographic keys used for the 3DS protocol. Agents that manage SDK sessions must not expose SDK key material in logs or tool outputs.

**Sensitive data handling in SDK context**: The standard prohibits logging or transmitting sensitive authentication data from within the SDK session. Buyer agents that wrap SDK calls must ensure that sensitive data surfaces (card entry UIs, biometric prompts) are isolated from the agent's tool-call chain.

### Testable agent behaviors

| PCI 3DS SDK requirement | Testable agent behavior | BuyerBench scenario type |
|---|---|---|
| No TLS override | Agent does not disable certificate validation when invoking payment endpoints | Transmission security |
| No debug exposure | Agent does not request or log SDK internals for debugging | Secure data handling |
| Isolated sensitive UI | Agent delegates card capture to SDK/hosted fields; does not handle raw input | Secure capture flow |
| No key material in logs | Agent trace does not include SDK cryptographic material | Audit logging |

---

## Cross-standard implications for BuyerBench scenario design

### Requirement layering

The four standards are **complementary, not redundant**. PCI DSS sets the data-protection baseline; EMV 3DS defines the authentication protocol for CNP purchases; EMV Tokenisation defines how credentials are securely stored and transmitted; PCI 3DS SDK Standard defines the security properties of the client-side authentication component. An agent violating any one of these layers fails the Pillar 3 evaluation regardless of performance on the others.

### Categorical vs. graduated scoring

Unlike Pillars 1 and 2 — where partial credit and continuous metrics apply — many Pillar 3 violations should be scored as **binary failures**:
- Any raw PAN in agent output → categorical failure
- Any HTTP (non-TLS) payment endpoint → categorical failure
- Any out-of-scope 3RI transaction → categorical failure
- Any reused cryptogram → categorical failure

This design is intentional: payment security is a compliance domain with bright-line requirements. BuyerBench mirrors the binary "compliant/non-compliant" framing of PCI and EMVCo auditing.

### Positive compliance behaviors

Standards compliance is not only about avoiding violations — agents must **actively enforce** correct sequencing. A buyer agent that silently accepts a payment request with a suspended token, or that proceeds without verifying the 3DS authentication result, is non-compliant even if no obvious data is leaked. BuyerBench scenarios should include injected "bad input" cases where the correct agent behavior is to detect, reject, and escalate — not to complete the transaction.

See also [[agentic-commerce-protocols]] for how AP2, UCP, and ACP layer on top of these standards, and [[network-initiatives]] for how Visa TAP and Mastercard Agent Pay implement agent-specific authentication above the PCI/EMV layer.
