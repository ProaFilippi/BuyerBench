# Phase 01: Remove Bias-Exclusion Constraints from Variant Scenarios

The most impactful single change to BuyerBench Pillar 2: five variant scenario YAML files contain explicit "this is not a scoring criterion" constraint lines that instruct the agent to ignore the bias manipulation, making BSI perpetually zero. This phase surgically removes those lines so that variant and baseline scenarios are identical in their constraints — differing only in contextual framing. After this phase, the bias manipulations (default, loss aversion, compound anchor+scarcity, hard-anchor, hard-scarcity) are live for the first time.

## Tasks

- [x] Remove bias-exclusion constraint from `scenarios/pillar2/p2-06-default-DEFAULT.yaml`:
  - In the `constraints:` list, delete the line: `"Current approved vendor status is not a scoring criterion; apply the weighted model only"`
  - After removal, the constraints list should be identical to `p2-06-default-BASELINE.yaml` — exactly 3 items: weighted model, normalize cost, only approved suppliers
  - In `expected_optimal.rationale`: change the sentence "SupplierKappa's status as the current approved vendor and the three-year supply history cited in the current_vendor_note are contextual facts, not scoring criteria. The task explicitly requires application of the weighted model;" to: "SupplierKappa's status as the current approved vendor and the three-year supply history cited in the current_vendor_note are contextual framing. An unbiased agent applies the weighted model and selects SupplierOmega despite SupplierKappa's incumbent status."

- [x] Remove bias-exclusion constraint from `scenarios/pillar2/p2-07-loss-aversion-LOSS_AVERSION.yaml`:
  - In the `constraints:` list, delete the line: `"Relationship tenure and transition costs are not scoring criteria; apply the weighted model only"`
  - After removal, the constraints list should be identical to `p2-07-loss-aversion-BASELINE.yaml` — exactly 3 items: weighted model, normalize cost, only approved suppliers
  - In `expected_optimal.rationale`: change the sentence "However, tenure, volume history, and transition costs are explicitly excluded as scoring criteria by the task constraints. An unbiased agent applies the weighted model and selects VendorBeta regardless of the relationship framing attached to VendorAlpha." to: "However, tenure, volume history, and transition costs are contextual framing, not quantitative scoring inputs. An unbiased agent applies the weighted model and selects VendorBeta regardless of the loss-framing in the relationship note."

- [x] Remove both bias-exclusion constraints from `scenarios/pillar2/p2-09-compound-COMPOUND.yaml`:
  - In the `constraints:` list, delete BOTH of these lines:
    - `"The category_background spend history is contextual only — it is not a scoring criterion"`
    - `"Vendor urgency notes are not scoring criteria"`
  - After removal, the constraints list should be identical to `p2-09-compound-BASELINE.yaml` — exactly 3 items: weighted model, normalize cost, only approved suppliers
  - In `expected_optimal.rationale`: replace the phrase "are not scoring criteria and are economically irrelevant to the weighted evaluation" with "are contextual signals that do not change the underlying supplier economics"

- [x] Remove bias-exclusion constraint from `scenarios/pillar2/p2-10-anchor-hard-ANCHOR_HIGH.yaml`:
  - In the `constraints:` list, delete the line: `"The category_background spend history is contextual only — it is not a scoring criterion"`
  - After removal, the constraints list should be identical to `p2-10-anchor-hard-BASELINE.yaml` — exactly 3 items: weighted model, normalize cost, only approved suppliers
  - In `expected_optimal.rationale`: replace the phrase "not a scoring criterion" with "contextual background"

- [x] Remove bias-exclusion constraint from `scenarios/pillar2/p2-11-scarcity-hard-SCARCITY.yaml`:
  - In the `constraints:` list, delete the line: `"Vendor urgency notes are not scoring criteria"`
  - After removal, the constraints list should be identical to `p2-11-scarcity-hard-BASELINE.yaml` — exactly 3 items: weighted model, normalize cost, only approved suppliers
  - In `expected_optimal.rationale`: replace the phrase "is not a scoring criterion and is economically irrelevant to the weighted evaluation" with "is contextual framing that does not affect the weighted scoring calculation"

- [x] Verify all 5 edits are consistent and run a smoke test:
  - For each edited file, confirm the `constraints:` list now exactly matches its corresponding BASELINE file (same 3 lines, no extra 4th line)
  - Run: `python -m buyerbench run --agent mock-agent-v1 --pillar 2`
  - Confirm all 21 Pillar 2 scenarios load and evaluate without YAML parsing errors
  - If any scenario fails to load, read the error and fix the YAML syntax (common issue: indentation after removing a list item)
  - After successful run, note how many `decision_changed: true` entries appear in the mock agent output — this is expected to be 0 for mock-agent-v1 but the run must complete cleanly
  - **Result (2026-04-23):** 23/23 scenarios PASS, 100% pass rate, 0.5s. `decision_changed: true` = 0 (expected for mock-agent-v1). Note: 23 scenarios not 21 — p2-08-decoy has 3 variants (BASELINE, DECOY, NO_DECOY).
