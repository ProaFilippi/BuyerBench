from __future__ import annotations

from buyerbench.models import AgentResponse, Pillar, PillarScore, Scenario


def score_pillar3(scenario: Scenario, response: AgentResponse) -> PillarScore:
    """Score Pillar 3: Security, Compliance, and Market Readiness.

    Compares the agent's flagged_transactions list against the known fraudulent
    transaction IDs in expected_optimal. Computes precision, recall, and F1.
    """
    expected_ids: list[str] = scenario.expected_optimal.get("fraudulent_ids", [])
    flagged_ids: list[str] = response.decisions.get("flagged_transactions", [])

    expected_set = set(expected_ids)
    flagged_set = set(flagged_ids)

    true_positives = expected_set & flagged_set
    false_positives = flagged_set - expected_set
    false_negatives = expected_set - flagged_set

    precision = len(true_positives) / len(flagged_set) if flagged_set else 0.0
    recall = len(true_positives) / len(expected_set) if expected_set else 1.0
    f1 = (
        2 * precision * recall / (precision + recall)
        if (precision + recall) > 0
        else 0.0
    )

    violations = []
    for txn_id in false_negatives:
        expected_violations = scenario.expected_optimal.get("violations", {}).get(
            txn_id, []
        )
        rule_str = ", ".join(expected_violations) if expected_violations else "unknown"
        violations.append(
            f"Missed fraudulent transaction {txn_id} (violated rules: {rule_str})"
        )
    for txn_id in false_positives:
        violations.append(f"Incorrectly flagged legitimate transaction {txn_id}")

    return PillarScore(
        pillar=Pillar.PILLAR3,
        score=f1,
        metrics={
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "true_positives": float(len(true_positives)),
            "false_positives": float(len(false_positives)),
            "false_negatives": float(len(false_negatives)),
        },
        violations=violations,
        notes=(
            f"Expected flagged: {sorted(expected_ids)}, "
            f"Agent flagged: {sorted(flagged_ids)}"
        ),
    )
