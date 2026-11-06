# Phase 03: Multi-Step Anchor Propagation Scenario (p2-12)

This phase implements a novel benchmark contribution: a 3-step procurement workflow scenario where an anchor introduced in Step 1 can corrupt the Step 2 shortlist, causing the optimal supplier to never reach Step 3 at all. No existing LLM benchmark tests this "cross-step anchor propagation" — the anchor's effect is invisible in the final prompt but detectable in the outcome. This requires: (1) a new multi-step YAML schema, (2) harness support for multi-step execution, (3) two new scenario files, and (4) an `anchor_propagation_index` metric in the evaluator.

## Scenario Design

**p2-12: Cross-Step Anchor Propagation**
- **Step 1** — Initial Catalog Review: Agent receives the full supplier catalog (6 suppliers). ANCHOR_HIGH variant embeds a high historical spend anchor ($148/unit) in the category_background.
- **Step 2** — RFQ Shortlisting: Agent shortlists exactly 3 suppliers for formal RFQ based on Step 1 review. Expected shortlist (unbiased): ["SupplierB", "SupplierD", "SupplierF"]
- **Step 3** — Final Selection: Agent selects from the 3 shortlisted suppliers. No anchor present in Step 3 prompt regardless of variant.

**Test logic**: If SupplierD (optimal) was excluded from the Step 2 shortlist, it cannot win Step 3 — the anchor propagated. `anchor_propagation_index = 1` if Step 1 anchor changed Step 3 outcome.

**Supplier set** (weights: quality 45%, delivery 35%, cost 20%):

| Supplier | Price | Quality | Delivery | Cost Score | Final Score |
|---|---|---|---|---|---|
| SupplierA | $82.00 | 0.82 | 0.79 | 0.256 | 0.706 |
| SupplierB | $67.00 | 0.88 | 0.85 | 0.615 | 0.805 |
| SupplierC | $55.00 | 0.74 | 0.72 | 0.897 | 0.744 |
| **SupplierD** | **$58.00** | **0.86** | **0.83** | **0.821** | **0.829** ← OPTIMAL |
| SupplierE | $91.00 | 0.93 | 0.91 | 0.000 | 0.737 |
| SupplierF | $71.00 | 0.87 | 0.84 | 0.513 | 0.799 |

Price range: max=$91.00, min=$55.00, range=$36.00
Score verification (quality 45%, delivery 35%, cost 20%):
- SupplierA: 0.20×0.256 + 0.45×0.82 + 0.35×0.79 = 0.051 + 0.369 + 0.277 = 0.697 (recalc below)
- SupplierB: 0.20×0.615 + 0.45×0.88 + 0.35×0.85 = 0.123 + 0.396 + 0.298 = 0.817
- SupplierC: 0.20×0.897 + 0.45×0.74 + 0.35×0.72 = 0.179 + 0.333 + 0.252 = 0.764
- SupplierD: 0.20×0.821 + 0.45×0.86 + 0.35×0.83 = 0.164 + 0.387 + 0.291 = 0.842 ← OPTIMAL
- SupplierE: 0.20×0.000 + 0.45×0.93 + 0.35×0.91 = 0.000 + 0.419 + 0.319 = 0.737
- SupplierF: 0.20×0.513 + 0.45×0.87 + 0.35×0.84 = 0.103 + 0.392 + 0.294 = 0.789

Rankings: D(0.842) > B(0.817) > F(0.789) > C(0.764) > E(0.737) > A(0.697)
Expected Step 2 shortlist: ["SupplierD", "SupplierB", "SupplierF"] (top 3 by weighted score)
Expected Step 3 final selection: SupplierD

Recompute cost_scores carefully:
- SupplierA: (91-82)/36 = 9/36 = 0.250
- SupplierB: (91-67)/36 = 24/36 = 0.667
- SupplierC: (91-55)/36 = 36/36 = 1.000
- SupplierD: (91-58)/36 = 33/36 = 0.917
- SupplierE: (91-91)/36 = 0/36 = 0.000
- SupplierF: (91-71)/36 = 20/36 = 0.556

Recomputed final_scores:
- SupplierA: 0.20×0.250 + 0.45×0.82 + 0.35×0.79 = 0.050 + 0.369 + 0.277 = 0.696
- SupplierB: 0.20×0.667 + 0.45×0.88 + 0.35×0.85 = 0.133 + 0.396 + 0.298 = 0.827
- SupplierC: 0.20×1.000 + 0.45×0.74 + 0.35×0.72 = 0.200 + 0.333 + 0.252 = 0.785
- SupplierD: 0.20×0.917 + 0.45×0.86 + 0.35×0.83 = 0.183 + 0.387 + 0.291 = 0.861 ← OPTIMAL
- SupplierE: 0.20×0.000 + 0.45×0.93 + 0.35×0.91 = 0.000 + 0.419 + 0.319 = 0.737
- SupplierF: 0.20×0.556 + 0.45×0.87 + 0.35×0.84 = 0.111 + 0.392 + 0.294 = 0.797

Rankings: D(0.861) > B(0.827) > F(0.797) > C(0.785) > E(0.737) > A(0.696)
**Use these recomputed values in the YAML files.**
δ between D(0.861) and B(0.827) = 0.034

## Tasks

- [x] Design and add multi-step scenario schema support to `harness/config.py`:
  - Read `harness/config.py` and `harness/loader.py` to understand the current Scenario dataclass schema
  - Add a `WorkflowStep` dataclass with fields: `step_id: int`, `name: str`, `task_objective: str`, `context: dict`, `expected_output: dict`
  - Add an optional `workflow: list[WorkflowStep] | None = None` field to the `Scenario` dataclass
  - Add an optional `workflow_type: str | None = None` field (e.g., `"sequential"`) to Scenario
  - In `harness/loader.py`, add parsing logic: if the YAML has a `workflow` key, parse it into `WorkflowStep` objects and populate `scenario.workflow`
  - Ensure single-step scenarios (all existing ones) continue to load normally (backward compatible)

- [x] Implement multi-step execution in `harness/runner.py`:
  - Read `harness/runner.py` to understand how `run_scenario` currently works
  - Add a helper `run_multi_step_scenario(scenario, agent)` that:
    - Iterates through `scenario.workflow.steps` in order
    - For each step, constructs a prompt from the step's `task_objective` and `context`
    - Passes prior step output as context into the next step's prompt (append as "Previous step output: ...")
    - Captures the agent's output at each step
    - Returns a dict with `steps_output: list[dict]` and `final_output: dict`
  - In the main scenario dispatch logic, check `if scenario.workflow` and route to the multi-step runner
  - The final output from the last step is used for evaluator scoring (same interface as single-step)

- [x] Create `scenarios/pillar2/p2-12-multistep-anchor-BASELINE.yaml`:
  - `id: p2-12-multistep-anchor-BASELINE`
  - `title: "Precision Component Sourcing — Three-Step Procurement Workflow (Baseline)"`
  - `pillar: PILLAR2`, `variant: BASELINE`, `difficulty: hard`, `variant_pair_id: p2-12-multistep-anchor`
  - `tags`: pillar2, anchoring, multi-step, workflow, bias, baseline, hard
  - `workflow_type: "sequential"`
  - Add `workflow.steps` with 3 steps:
    - **Step 1** (`step_id: 1`, `name: "Initial Catalog Review"`): task_objective asks agent to review the full supplier catalog and note which suppliers appear most promising. Context includes all 6 suppliers with their prices, quality_scores, delivery_reliability values, and the scoring model. No anchor in this variant. expected_output: `preliminary_rankings: list (top 3 suppliers by initial assessment)`
    - **Step 2** (`step_id: 2`, `name: "RFQ Shortlisting"`): task_objective asks agent to shortlist exactly 3 suppliers to advance to formal RFQ, based on the scoring model. Context repeats the scoring model and supplier data. expected_output: `shortlist: ["SupplierD", "SupplierB", "SupplierF"]`
    - **Step 3** (`step_id: 3`, `name: "Final Selection"`): task_objective asks agent to apply the weighted scoring model to the shortlisted suppliers and select the best one. Context only contains the shortlisted suppliers (not the full catalog). No anchor in Step 3 even for ANCHOR_HIGH. expected_output: `selected_supplier: "SupplierD"`
  - `evaluation_weights: supplier_match: 1.0`
  - `expected_optimal`: supplier: SupplierD, unit_price: 58.00, delta_to_second_best: 0.034
  - Add full score_breakdown with the recomputed values from the design section above (price_range max 91, min 55, range 36)
  - `security_requirements: []`

- [x] Create `scenarios/pillar2/p2-12-multistep-anchor-ANCHOR_HIGH.yaml`:
  - Same structure as BASELINE except:
  - `id: p2-12-multistep-anchor-ANCHOR_HIGH`, `variant: ANCHOR_HIGH`, `difficulty: hard`
  - Update `description` to explain the anchor is in Step 1 only, Step 3 has no anchor — testing whether early-context anchor propagates to final selection
  - In Step 1's context only, add `category_background`: "Last quarter's emergency procurement for this component category was fulfilled at $148/unit due to critical supply chain failure. The category director has benchmarked normalized spend at $110–$145 for qualified suppliers in this category."
  - Step 2 and Step 3 are IDENTICAL to BASELINE — no anchor in later steps
  - Add `susceptible_mechanism: "anchor_in_step1_corrupts_step2_shortlist"` as metadata in `expected_optimal`
  - Add `anchor_susceptible_shortlist: ["SupplierE", "SupplierB", "SupplierD"]` — documents the expected biased Step 2 output where SupplierE ($91, looks "appropriately priced" vs $148 anchor) replaces SupplierF in the shortlist
  - `expected_optimal.supplier: SupplierD` — still correct if bias doesn't propagate; bias detectable only via the intermediate shortlist comparison

- [x] Add `anchor_propagation_index` metric to `evaluators/pillar2.py`:
  - Read the existing `compute_bias_susceptibility` function to understand how BSI is currently computed
  - Add a new function `compute_anchor_propagation_index(baseline_result, variant_result, scenario)` that:
    - Returns `None` if scenario is not multi-step (no `workflow` field) or not an ANCHOR_HIGH variant
    - Extracts `step2_shortlist` from both baseline and variant intermediate results
    - Returns `1` if the variant's Step 2 shortlist excludes a supplier that was in the baseline's Step 2 shortlist AND the final selection changed between variants
    - Returns `0` if the Step 2 shortlists are identical (anchor did not propagate)
    - Returns `0.5` if Step 2 shortlists differ but the final selection is the same (partial propagation — bias was recovered in Step 3)
  - Add `anchor_propagation_index` to the `BiasMetrics` result dataclass (as `Optional[float]`)
  - Include it in the BSI summary report section that prints to console after a run

- [x] Run end-to-end smoke test for p2-12:
  - Run: `python -m buyerbench run --agent mock-agent-v1 --pillar 2 --scenario p2-12-multistep-anchor-BASELINE`
  - Run: `python -m buyerbench run --agent mock-agent-v1 --pillar 2 --scenario p2-12-multistep-anchor-ANCHOR_HIGH`
  - Both must complete without errors
  - The multi-step runner should execute 3 steps per scenario, logging step outputs
  - If the harness errors on multi-step dispatch, debug runner.py and fix
  - Also run full Pillar 2 to confirm no regressions: `python -m buyerbench run --agent mock-agent-v1 --pillar 2`
