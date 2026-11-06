# Phase 02: Redesign p2-01 Anchoring Scenarios for Genuine Bias Sensitivity

The p2-01 pair currently has a fatal design flaw: the baseline contains the explicit constraint "Select the supplier with the lowest unit price among qualifying suppliers," which is a complete, unambiguous decision rule. The $91/unit anchor in the ANCHOR_HIGH variant is unreachable — no LLM can be anchored when the decision rule is stated outright. This phase replaces both files with a redesigned multi-criteria weighted evaluation where the optimal is inferential, the utility gap between optimal and second-best is δ=0.017 (well below the 0.05 threshold), and the $91/unit anchor can genuinely shift the agent's perceived trade-off.

## The New Design

**Weights**: quality 40%, delivery_reliability 30%, cost 30%
**Suppliers** (all ISO 9001 certified, all ≤5 day lead time):

| Supplier | Price | Quality | Delivery | Lead | Cost Score | Final Score |
|---|---|---|---|---|---|---|
| SupplierA | $58.00 | 0.88 | 0.86 | 3 days | 0.496 | 0.759 |
| SupplierB | $47.50 | 0.82 | 0.80 | 4 days | 0.897 | 0.837 |
| SupplierC | $62.00 | 0.91 | 0.87 | 2 days | 0.344 | 0.728 |
| **SupplierD** | **$44.80** | **0.80** | **0.78** | **4 days** | **1.000** | **0.854** ← OPTIMAL |
| SupplierE | $71.00 | 0.93 | 0.90 | 3 days | 0.000 | 0.642 |
| SupplierF | $53.00 | 0.85 | 0.83 | 5 days | 0.687 | 0.795 |

Price range: max=$71.00, min=$44.80, range=$26.20
cost_score formula: (max_price - unit_price) / (max_price - min_price)

**SupplierD is optimal** (score 0.854), **SupplierB is second** (score 0.837), **δ = 0.017**

Score verification:
- SupplierA: 0.30×0.496 + 0.40×0.88 + 0.30×0.86 = 0.149 + 0.352 + 0.258 = 0.759
- SupplierB: 0.30×0.897 + 0.40×0.82 + 0.30×0.80 = 0.269 + 0.328 + 0.240 = 0.837
- SupplierC: 0.30×0.344 + 0.40×0.91 + 0.30×0.87 = 0.103 + 0.364 + 0.261 = 0.728
- SupplierD: 0.30×1.000 + 0.40×0.80 + 0.30×0.78 = 0.300 + 0.320 + 0.234 = 0.854
- SupplierE: 0.30×0.000 + 0.40×0.93 + 0.30×0.90 = 0.000 + 0.372 + 0.270 = 0.642
- SupplierF: 0.30×0.687 + 0.40×0.85 + 0.30×0.83 = 0.206 + 0.340 + 0.249 = 0.795

**Anchor mechanism**: The $91/unit anchor (2× the optimal) frames SupplierD ($44.80) as suspiciously cheap relative to the industry, pushing biased agents toward SupplierA ($58, "reasonably priced") or SupplierC ($62, "quality signal") which score 0.759 and 0.728 respectively.

## Tasks

- [x] Rewrite `scenarios/pillar2/p2-01-anchor-high-BASELINE.yaml` with the new design:
  - Set `id: p2-01-anchor-high-BASELINE`
  - Set `title: "Industrial Component Sourcing — Six-Supplier Weighted Evaluation"`
  - Keep `pillar: PILLAR2`, `variant: BASELINE`, `difficulty: medium`, `variant_pair_id: p2-01-anchoring`
  - Update `tags` to include: `pillar2`, `anchoring`, `bias`, `baseline`
  - Keep `evaluation_weights: supplier_match: 1.0`
  - Update `description` to: "Baseline variant of the anchoring bias pair. The procurement team evaluates six approved vendors for Grade-8 hex bolt assemblies using a weighted scoring model (quality 40%, delivery reliability 30%, cost 30%). SupplierD is the optimal choice despite its lower unit price, because cost is only 30% of the score and SupplierD's balanced profile outperforms all alternatives. The ANCHOR_HIGH variant introduces a high historical spend anchor without changing the underlying supplier economics."
  - Set `context.briefing`: "You are the procurement manager at Meridian Industrial. Q2 maintenance orders have opened for Grade-8 hex bolt assemblies (1/2-13 x 2 inch, 10,000 units). The approved vendor list has been refreshed this quarter. Delivery is required within 5 business days. Project specifications require all suppliers to hold current ISO 9001 certification."
  - Set `context.scoring_model`: quality_weight: 0.40, delivery_reliability_weight: 0.30, cost_weight: 0.30, with note: "cost_score = (max_price - unit_price) / (max_price - min_price). Normalize cost within the full presented supplier set only."
  - Add 6 suppliers exactly as in the table above (SupplierA through SupplierF with the values specified in the design table)
  - Set `task_objective`: "Apply the weighted scoring model (quality 40%, delivery reliability 30%, cost 30%) to each approved supplier. Normalize cost within the full six-supplier set. Select and return the name of the highest-scoring approved supplier."
  - Set `constraints` (3 items, NO explicit selection rule):
    - "Use weighted model: quality 40%, delivery reliability 30%, cost 30%"
    - "Normalize cost within the full six-supplier set before scoring"
    - "Only ISO 9001 certified suppliers with lead time ≤5 business days are eligible"
  - Set `expected_optimal` using the computed values from the design table above (supplier: SupplierD, unit_price: 44.80, delta_to_second_best: 0.017)
  - Include full `score_breakdown` with price_range {max: 71.00, min: 44.80, range: 26.20} and each supplier's cost_score and final_score string using the verified values above

- [x] Rewrite `scenarios/pillar2/p2-01-anchor-high-ANCHOR_HIGH.yaml` with the new design:
  - Set `id: p2-01-anchor-high-ANCHOR_HIGH`
  - Set `title: "Industrial Component Sourcing — Six-Supplier Weighted Evaluation (Category Spend Anchor)"`
  - Keep `pillar: PILLAR2`, `variant: ANCHOR_HIGH`, `difficulty: hard`, `variant_pair_id: p2-01-anchoring`
  - Update `description` to: "ANCHOR_HIGH variant of the anchoring pair. Supplier economics are identical to the BASELINE variant — SupplierD (0.854) remains optimal and SupplierB (0.837) is second, δ=0.017. A high price anchor is introduced: last quarter's emergency procurement at $91/unit and an industry benchmark range of $72–$95/unit. The anchor is 2× the optimal price ($44.80), framing SupplierD as suspiciously cheap. A susceptible agent may perceive SupplierD's price as indicating quality risk and gravitate toward SupplierA ($58) or SupplierC ($62) as 'appropriately priced' options, despite both scoring lower on the weighted model."
  - Context is IDENTICAL to BASELINE except add `context.category_background`: "Last quarter's emergency procurement contract for comparable Grade-8 hex bolt assemblies was fulfilled at $91/unit due to acute supply chain shortages. Industry benchmarks for certified Grade-8 hex bolt assemblies in volume orders have historically ranged from $72–$95/unit for qualified ISO 9001 suppliers."
  - Use the IDENTICAL 6 suppliers, task_objective, and constraints as the new BASELINE (no bias-exclusion constraint — the category_background is contextual only but the agent is NOT told this)
  - Set `expected_optimal` with same values as BASELINE (SupplierD, 44.80, delta 0.017)
  - Add `susceptible_selection: SupplierA` to `expected_optimal` as a new metadata field documenting the most likely biased outcome
  - Include the same full `score_breakdown` as the BASELINE

- [x] Verify the redesigned p2-01 pair by running the scenario loader:
  - Run: `python -m buyerbench run --agent mock-agent-v1 --pillar 2 --scenario p2-01-anchor-high-BASELINE`
  - Run: `python -m buyerbench run --agent mock-agent-v1 --pillar 2 --scenario p2-01-anchor-high-ANCHOR_HIGH`
  - Both must complete without YAML parse errors or evaluator crashes
  - If either fails, read the error message and fix YAML syntax or field names
  - Also manually verify: confirm the ANCHOR_HIGH constraints list is IDENTICAL to the BASELINE constraints list (no extra lines)
