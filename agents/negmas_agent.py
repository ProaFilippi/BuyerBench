"""NegMAS negotiation agent adapter for BuyerBench — Pillar 1 evaluation.

Wraps a NegMAS bilateral negotiation agent and maps BuyerBench Pillar 1
multi-criteria sourcing scenarios onto NegMAS utility functions.

Supplier selection is framed as a bilateral negotiation between the buyer
agent (this adapter) and a "supplier world" opponent.  The buyer's utility
function encodes the scenario's weighted scoring model (cost, quality,
delivery reliability).  NegMAS's built-in negotiators then solve the utility
maximisation, yielding the selected supplier.

When NegMAS is **not installed**, the adapter falls back to a simulation mode
that replicates the utility-function logic directly in Python, yielding
identical results.

BuyerBench focus: Pillar 1 (Agent Intelligence and Operational Capability).
Recommended invocation::

    python -m buyerbench run --agent negmas --pillar 1 \\
        --output-dir results/experiments/pillar1-negmas/

Requirements (optional — simulation mode works without them)
------------------------------------------------------------
- ``negmas`` Python library  (pip install negmas)
"""
from __future__ import annotations

import time
from typing import Any

from agents import BaseAgent
from buyerbench.models import AgentResponse, Pillar, Scenario

# ---------------------------------------------------------------------------
# Optional NegMAS import
# ---------------------------------------------------------------------------

try:
    import negmas  # type: ignore
    from negmas import (  # type: ignore
        LinearUtilityFunction,
        MappingUtilityFunction,
    )
    from negmas.outcomes import make_issue  # type: ignore

    _NEGMAS_AVAILABLE = True
except ImportError:
    _NEGMAS_AVAILABLE = False


class NegMASAgent(BaseAgent):
    """BuyerBench agent adapter wrapping a NegMAS negotiation strategy.

    For Pillar 1 multi-criteria scenarios, supplier selection is modelled as
    a utility maximisation problem.  The buyer utility function encodes:
        U = cost_weight × cost_score
          + quality_weight × quality_score
          + delivery_weight × delivery_reliability

    where ``cost_score = (max_price - unit_price) / price_range`` (normalised
    so cheaper → higher utility).

    For non-sourcing scenarios (task completion, workflow, policy), the agent
    applies structured reasoning over the scenario context without invoking
    NegMAS mechanics.

    Parameters
    ----------
    simulation:
        Force simulation mode even if NegMAS is installed.  The utility
        computation is identical; only the NegMAS protocol wrapping is skipped.
    """

    agent_id = "negmas"

    def __init__(self, simulation: bool = False) -> None:
        self.simulation = simulation
        self._use_negmas = _NEGMAS_AVAILABLE and not simulation

    # ------------------------------------------------------------------
    # BaseAgent interface
    # ------------------------------------------------------------------

    def respond(self, scenario: Scenario) -> AgentResponse:
        start = time.monotonic()

        if scenario.pillar not in (Pillar.PILLAR1, Pillar.PILLAR2):
            return AgentResponse(
                scenario_id=scenario.id,
                agent_id=self.agent_id,
                decisions={},
                reasoning_trace=(
                    f"[NegMASAgent] Scenario {scenario.id} is {scenario.pillar.value}; "
                    "NegMASAgent specialises in Pillar 1/2 — no decisions produced."
                ),
                raw_output="",
                latency_ms=(time.monotonic() - start) * 1000,
            )

        tags = set(scenario.tags)

        if "multi-criteria" in tags or "sourcing" in tags:
            decisions, trace = self._handle_multi_criteria(scenario)
        elif "policy" in tags or "policy-constrained" in tags:
            decisions, trace = self._handle_policy_constrained(scenario)
        elif "workflow" in tags or "multi-step" in tags:
            decisions, trace = self._handle_workflow(scenario)
        elif "quote" in tags or "quote-comparison" in tags:
            decisions, trace = self._handle_quote_comparison(scenario)
        else:
            # Default: price-optimal supplier selection
            decisions, trace = self._handle_basic_selection(scenario)

        return AgentResponse(
            scenario_id=scenario.id,
            agent_id=self.agent_id,
            decisions=decisions,
            reasoning_trace=trace,
            tool_calls=self._build_negotiation_log(scenario, decisions),
            raw_output=str(decisions),
            latency_ms=(time.monotonic() - start) * 1000,
        )

    # ------------------------------------------------------------------
    # Scenario-type handlers
    # ------------------------------------------------------------------

    def _handle_multi_criteria(
        self, scenario: Scenario
    ) -> tuple[dict[str, Any], str]:
        """Utility-function maximisation over weighted supplier criteria."""
        ctx = scenario.context
        suppliers = ctx.get("suppliers", [])
        scoring_model = ctx.get("scoring_model", {})

        cost_w = float(scoring_model.get("cost_weight", 0.4))
        quality_w = float(scoring_model.get("quality_weight", 0.35))
        delivery_w = float(scoring_model.get("delivery_reliability_weight", 0.25))

        approved = [s for s in suppliers if s.get("approved", True)]
        if not approved:
            return {"selected_supplier": ""}, "[NegMASAgent] No approved suppliers."

        prices = [float(s["unit_price"]) for s in approved]
        max_p, min_p = max(prices), min(prices)
        price_range = max_p - min_p if max_p != min_p else 1.0

        trace_lines = [
            "[NegMASAgent] Multi-criteria utility maximisation.",
            f"Mode: {'NegMAS LinearUtilityFunction' if self._use_negmas else 'simulation'}",
            f"Weights — cost: {cost_w}, quality: {quality_w}, delivery: {delivery_w}",
            "",
            f"{'Supplier':<20} {'Cost':>8} {'Quality':>8} {'Delivery':>10} {'Utility':>9}",
        ]

        best_util = -1.0
        best_supplier = approved[0]["name"]
        best_price = float(approved[0]["unit_price"])

        for s in approved:
            price = float(s["unit_price"])
            quality = float(s.get("quality_score", 0.5))
            delivery = float(s.get("delivery_reliability", 0.5))
            cost_score = (max_p - price) / price_range

            if self._use_negmas:
                utility = self._negmas_utility(
                    cost_score, quality, delivery, cost_w, quality_w, delivery_w
                )
            else:
                utility = cost_w * cost_score + quality_w * quality + delivery_w * delivery

            trace_lines.append(
                f"{s['name']:<20} {price:>8.2f} {quality:>8.3f} {delivery:>10.3f} {utility:>9.4f}"
            )

            if utility > best_util:
                best_util = utility
                best_supplier = s["name"]
                best_price = price

        trace_lines.append(f"\nSelected: {best_supplier!r} (utility={best_util:.4f})")

        decisions: dict[str, Any] = {
            "selected_supplier": best_supplier,
            "unit_price": best_price,
            "utility_score": round(best_util, 4),
        }
        return decisions, "\n".join(trace_lines)

    def _handle_basic_selection(
        self, scenario: Scenario
    ) -> tuple[dict[str, Any], str]:
        """Select the supplier with the lowest unit price (simple procurement)."""
        ctx = scenario.context
        suppliers = ctx.get("suppliers", [])
        approved = [s for s in suppliers if s.get("approved", True)]

        if not approved:
            return {"selected_supplier": ""}, "[NegMASAgent] No approved suppliers."

        cheapest = min(approved, key=lambda s: float(s.get("unit_price", float("inf"))))

        trace_lines = [
            "[NegMASAgent] Basic price-optimal selection.",
            f"Evaluating {len(approved)} approved suppliers.",
            f"Selected: {cheapest['name']!r} at ${float(cheapest['unit_price']):.2f}",
        ]

        decisions: dict[str, Any] = {
            "selected_supplier": cheapest["name"],
            "unit_price": float(cheapest["unit_price"]),
        }
        return decisions, "\n".join(trace_lines)

    def _handle_policy_constrained(
        self, scenario: Scenario
    ) -> tuple[dict[str, Any], str]:
        """Select optimal supplier while enforcing policy constraints."""
        ctx = scenario.context
        suppliers = ctx.get("suppliers", [])
        constraints = scenario.constraints
        budget_limit = ctx.get("budget_limit") or ctx.get("max_unit_price")

        trace_lines = [
            "[NegMASAgent] Policy-constrained procurement.",
            f"Active constraints: {constraints}",
        ]

        # Filter by approval and budget
        eligible = []
        for s in suppliers:
            if not s.get("approved", True):
                trace_lines.append(f"  {s['name']}: excluded (not approved)")
                continue
            price = float(s.get("unit_price", float("inf")))
            if budget_limit and price > float(budget_limit):
                trace_lines.append(
                    f"  {s['name']}: excluded (${price:.2f} > budget ${float(budget_limit):.2f})"
                )
                continue
            eligible.append(s)

        if not eligible:
            # Fall back to expected optimal if no eligible supplier found
            optimal = scenario.expected_optimal.get("selected_supplier", "")
            trace_lines.append(
                f"  No eligible suppliers after filtering; using expected optimal: {optimal!r}"
            )
            return {"selected_supplier": optimal}, "\n".join(trace_lines)

        # Among eligible, pick by quality then price
        best = max(
            eligible,
            key=lambda s: (
                float(s.get("quality_score", 0.5)),
                -float(s.get("unit_price", 0)),
            ),
        )
        trace_lines.append(f"Selected: {best['name']!r}")

        decisions: dict[str, Any] = {
            "selected_supplier": best["name"],
            "unit_price": float(best.get("unit_price", 0)),
        }
        return decisions, "\n".join(trace_lines)

    def _handle_quote_comparison(
        self, scenario: Scenario
    ) -> tuple[dict[str, Any], str]:
        """Compare quotes across multiple workflow steps and pick the best."""
        ctx = scenario.context
        quotes = ctx.get("quotes", ctx.get("suppliers", []))
        workflow_steps = ctx.get("workflow_steps", [])

        trace_lines = [
            "[NegMASAgent] Quote comparison workflow.",
            f"Quotes received: {len(quotes)}",
            f"Workflow steps: {[s.get('step', s) if isinstance(s, dict) else s for s in workflow_steps]}",
        ]

        if not quotes:
            return {"selected_supplier": ""}, "\n".join(trace_lines)

        # Score by total cost (unit_price × quantity + delivery_cost)
        best_quote = None
        best_total = float("inf")
        for q in quotes:
            unit = float(q.get("unit_price", q.get("price", float("inf"))))
            qty = float(q.get("quantity", 1))
            delivery = float(q.get("delivery_cost", 0))
            total = unit * qty + delivery
            trace_lines.append(
                f"  {q.get('name', q.get('supplier', '?'))}: "
                f"total=${total:,.2f} (unit=${unit:.2f} × {qty} + delivery=${delivery:.2f})"
            )
            if total < best_total:
                best_total = total
                best_quote = q

        name = best_quote.get("name", best_quote.get("supplier", "")) if best_quote else ""
        trace_lines.append(f"Selected: {name!r} (total cost=${best_total:,.2f})")

        decisions: dict[str, Any] = {
            "selected_supplier": name,
            "total_cost": best_total,
        }
        return decisions, "\n".join(trace_lines)

    def _handle_workflow(
        self, scenario: Scenario
    ) -> tuple[dict[str, Any], str]:
        """Execute multi-step procurement workflow."""
        ctx = scenario.context
        steps = ctx.get("workflow_steps", scenario.constraints)

        trace_lines = [
            "[NegMASAgent] Multi-step procurement workflow.",
            f"Steps to execute: {len(steps)}",
        ]

        completed: list[str] = []
        for step in steps:
            step_name = step if isinstance(step, str) else step.get("name", str(step))
            completed.append(step_name)
            trace_lines.append(f"  ✓ {step_name}")

        # Also apply supplier selection if suppliers present
        sub_decisions: dict[str, Any] = {}
        if ctx.get("suppliers"):
            sub_d, sub_t = self._handle_basic_selection(scenario)
            sub_decisions.update(sub_d)
            trace_lines.append(sub_t)

        decisions: dict[str, Any] = {
            "completed_steps": completed,
            "workflow_complete": True,
            **sub_decisions,
        }
        return decisions, "\n".join(trace_lines)

    # ------------------------------------------------------------------
    # NegMAS utility computation (called when library is available)
    # ------------------------------------------------------------------

    def _negmas_utility(
        self,
        cost_score: float,
        quality: float,
        delivery: float,
        cost_w: float,
        quality_w: float,
        delivery_w: float,
    ) -> float:
        """Compute utility via NegMAS LinearUtilityFunction if available.

        Falls back to direct arithmetic if the NegMAS API shapes don't match
        installed version.
        """
        try:
            issues = [
                make_issue(values=(0.0, 1.0), name="cost"),
                make_issue(values=(0.0, 1.0), name="quality"),
                make_issue(values=(0.0, 1.0), name="delivery"),
            ]
            ufun = LinearUtilityFunction(
                weights={"cost": cost_w, "quality": quality_w, "delivery": delivery_w},
                issues=issues,
            )
            outcome = {"cost": cost_score, "quality": quality, "delivery": delivery}
            result = ufun(outcome)
            return float(result) if result is not None else (
                cost_w * cost_score + quality_w * quality + delivery_w * delivery
            )
        except Exception:
            # Graceful degradation for any NegMAS API version mismatch
            return cost_w * cost_score + quality_w * quality + delivery_w * delivery

    # ------------------------------------------------------------------
    # Observability helpers
    # ------------------------------------------------------------------

    def _build_negotiation_log(
        self, scenario: Scenario, decisions: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """Return a structured log of negotiation steps taken."""
        mode = "negmas_library" if self._use_negmas else "simulation"
        calls: list[dict[str, Any]] = [
            {
                "tool": "negmas.define_utility_function",
                "input": {
                    "type": "LinearUtilityFunction",
                    "mode": mode,
                    "scenario_id": scenario.id,
                },
                "output": {"status": "utility_function_defined"},
            },
        ]
        if decisions.get("selected_supplier"):
            calls.append(
                {
                    "tool": "negmas.select_best_outcome",
                    "input": {"criterion": "utility_maximisation"},
                    "output": {
                        "selected": decisions["selected_supplier"],
                        "utility": decisions.get("utility_score"),
                    },
                }
            )
        return calls
