---
type: research
title: "Samuelson & Zeckhauser (1988) — Status Quo Bias"
created: 2026-04-08
tags:
  - status-quo-bias
  - default-effect
  - omission-bias
  - inertia
related:
  - '[[Kahneman-Tversky-1979-Prospect-Theory]]'
  - '[[Tversky-Simonson-1993-Asymmetric-Dominance]]'
---

# Samuelson & Zeckhauser (1988) — Status Quo Bias

## Citation

Samuelson, W., & Zeckhauser, R. (1988). Status quo bias in decision making. *Journal of Risk and Uncertainty*, 1(1), 7–59.

## Core Finding

People disproportionately prefer the current state of affairs over alternative options, even when switching would produce a net gain. This bias cannot be explained by transaction costs alone — the psychological inflation of switching costs systematically exceeds any rational economic explanation. In experiments where participants were given an identical choice set but one option was framed as the "status quo," that option was chosen significantly more often across domains including financial portfolios, policy choices, and consumer decisions.

## Key Mechanisms

### Default Effects

Options framed as defaults are chosen far more often than the same options presented as active choices. The difference between opt-out and opt-in enrollment rates — sometimes exceeding 40 percentage points — cannot be attributed to rational inertia. Defaults function as implicit recommendations and exploit omission bias: not switching feels like a non-action even when it has real consequences.

### Loss Aversion Interaction

Status quo bias is substantially amplified by loss aversion (from [[Kahneman-Tversky-1979-Prospect-Theory]]). Switching from the current option is psychologically coded as a loss even when the alternative is objectively superior. The asymmetric weight placed on losses (~2.25x gains) means the pain of "giving up" the incumbent option outweighs the expected gain from switching, even at favorable exchange rates.

### Omission vs. Commission Asymmetry

Maintaining the status quo feels like an omission (inaction) rather than a commission (active choice), which further reduces perceived responsibility for negative outcomes. This asymmetry makes status quo persistence feel "safe" even when sticking is demonstrably costly.

### Competence and Regret Anticipation

Choosers anticipate greater regret from bad outcomes of active switches than from equivalent bad outcomes of passive non-switches. This anticipated regret cost adds to the effective switching threshold.

## Procurement Application

**Incumbent supplier advantages**: An existing supplier benefits from status quo protection even when a new vendor is strictly better on cost, quality, and terms. Procurement agents must actively overcome the psychological inertia of "we've always used them."

**Unchallenged contract renewals**: Default payment terms, auto-renewing contracts, and standard SLA structures persist unchallenged through renewal cycles not because they are optimal, but because the burden of switching — even a minor contract renegotiation — is psychologically overweighted.

**Decision inertia under time pressure**: When procurement agents face cognitive load or time constraints, they default to the current arrangement. A rational agent should evaluate each contract cycle on its merits, resetting the reference point rather than carrying forward prior commitments.

**Platform and tool lock-in**: Technology procurement decisions exhibit pronounced status quo bias because switching costs are highly visible (migration effort, retraining) while the opportunity costs of staying are diffuse and future-dated.

## Scenario Design Implication

Present one supplier option as the "current contract" or "existing arrangement" with a known renewal option, and introduce an alternative that is economically superior across the relevant dimensions. The correct decision is to switch, but the status quo framing creates a psychologically loaded default.

**Critical design rule**: do not explicitly label the bias or announce that inertia is being tested. The "current arrangement" language in the scenario briefing should be matter-of-fact, the same way a real procurement context would present it. The agent must overcome status quo inertia through active evaluation, not be prompted to watch for it.

**Compound scenario opportunity**: pair status quo bias with sunk cost (Thaler 1980) by specifying that significant prior investment has been made in the incumbent vendor's integration. This compound design reflects realistic procurement dynamics and tests whether agents can disentangle irrelevant sunk costs from the status quo inertia.

## Related Biases

- **Sunk Cost Fallacy** (Thaler 1980): prior expenditure in the incumbent creates additional lock-in pressure on top of status quo inertia
- **Decoy Effect** ([[Tversky-Simonson-1993-Asymmetric-Dominance]]): asymmetric dominance can be used to make the incumbent appear as the "safe compromise" when a new vendor enters the consideration set
- **Loss Aversion** ([[Kahneman-Tversky-1979-Prospect-Theory]]): the foundational mechanism amplifying switching cost perception

## Detection Signal in Agent Behavior

An agent exhibiting status quo bias will:
1. Select the incumbent option despite explicit evidence that an alternative has better expected value
2. Underweight or fail to quantify the opportunity cost of staying
3. Invoke qualitative risk language ("reliability", "established relationship") without calculating whether these justify the cost premium
4. Fail to request additional information about the alternative before defaulting to the incumbent

A rational agent will re-evaluate each option from a neutral reference point, compute expected utility across options on equal terms, and select the alternative if it dominates on the relevant dimensions.
