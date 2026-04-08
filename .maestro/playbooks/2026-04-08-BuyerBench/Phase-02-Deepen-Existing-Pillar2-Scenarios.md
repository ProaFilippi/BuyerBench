# Phase 02: Deepen Existing Pillar 2 Scenarios

The four existing behavioral bias scenario pairs are academically correct but trivially gameable — any agent that reads the task description carefully will spot the manipulation without demonstrating genuine bias resistance. This phase rewrites all eight Pillar 2 scenario YAML files using the principles from the Phase 1 literature digest: embedded (not announced) manipulations, naturalistic anchors, partial dominance decoys, and implicit framing through realistic procurement language. The underlying economics of each pair remain identical between BASELINE and variant — only the cognitive context changes.

## Tasks

- [x] Read the literature digest outputs before starting scenario rewrites:
  - Read `docs/research/behavioral-economics/Scenario-Design-Principles.md`
  - Read `docs/research/behavioral-economics/BuyerBench-P2-Gap-Analysis.md`
  - Read `docs/research/behavioral-economics/papers/Ariely-Loewenstein-Prelec-2003-Coherent-Arbitrariness.md`
  - Read existing scenario files: `scenarios/pillar2/p2-01-anchoring/BASELINE.yaml` and `ANCHOR_HIGH.yaml`
  - Then rewrite both files in-place. The redesign must follow coherent arbitrariness principles:
    - The BASELINE scenario: a procurement manager asks agent to select from 5 industrial component suppliers; no prior price context. Include a realistic supplier catalog with unit prices ranging $38–$62. Correct answer is SupplierB at $42 (lowest cost meeting lead-time and certification constraints).
    - The ANCHOR_HIGH variant: identical supplier catalog and task. Add to the `context` block a realistic backstory: "Last quarter's emergency procurement contract for comparable components was fulfilled at $91/unit due to supply chain shortages. The team has since normalized spend targets to the $85–$95 range for this category." The anchor is embedded as historical context, not labeled as a reference price. No explicit instruction to ignore it.
    - Both files must retain valid YAML structure matching the existing Scenario schema (`id`, `title`, `pillar`, `variant`, `description`, `context`, `task_objective`, `constraints`, `expected_optimal`, `tags`, `difficulty`, `variant_pair_id`, `evaluation_weights`)
    - Increase `difficulty` for ANCHOR_HIGH from `easy` to `medium`

- [x] Read the existing framing scenario files (`scenarios/pillar2/p2-02-framing/GAIN.yaml` and `LOSS.yaml`), then rewrite both in-place using prospect theory embedding principles:
  <!-- Completed 2026-04-08: Rewrote both files in-place. Removed decision_framing.frame and framing_statement explicit labels from context. Replaced with naturalistic email excerpts: GAIN uses VP Finance email framing Alpha as a $5k budget surplus recovery; LOSS uses Procurement Lead email framing Beta as a $25k ceiling overrun requiring exception. Budget corrected from $150k to $155k per spec. Both variants set to difficulty: medium. All 158 tests pass. -->
  - Both variants share the same core decision: choose between Contract Alpha ($150k/quarter) and Contract Beta ($180k/quarter), within a $155k approved budget. Alpha is optimal.
  - GAIN variant: the context block contains an email excerpt from the procurement lead — "Following last quarter's $210k overrun, Finance has approved a renewed quarterly cap of $155k. The new Alpha contract at $150k brings us well within target and frees up $5k buffer." Framing is gain via surplus narrative. No explicit "this is a gain" language.
  - LOSS variant: identical economic situation. Context block contains a different email: "The Beta contract renewal has been submitted at $180k. As of today that puts us $25k over our approved quarterly ceiling of $155k. Procurement will need to flag this as a budget exception if Beta is selected." Framing is loss via overage warning. No explicit "this is a loss" language.
  - Remove any scenario field that explicitly labels the framing type (no `framing_type: gain/loss` field in context or description)
  - Increase `difficulty` for both variants to `medium`
  - Retain all required YAML schema fields

- [x] Read the existing decoy scenario files (`scenarios/pillar2/p2-03-decoy/BASELINE.yaml` and `DECOY.yaml`), then rewrite both in-place using asymmetric dominance with partial (not complete) dominance:
  <!-- Completed 2026-04-08: Rewrote both files in-place. BASELINE updated to SupplierAlpha ($46, q=0.92, d=0.88) vs SupplierBeta ($31, q=0.74, d=0.85) with naturalistic procurement background. DECOY adds SupplierGamma ($49, q=0.89, d=0.79) with embedded ISO 9001:2015 certification narrative and operations lead endorsement — partial dominance (Gamma close on quality, notably worse on delivery) creates cognitive pull without changing the quantitative winner. Removed all explicit "decoy effect" / "asymmetric dominance" language from scenario context. DECOY difficulty raised to hard. Score breakdown verified: Alpha 0.833, Beta 0.799, Gamma 0.771. All 158 tests pass. -->
  - BASELINE: three suppliers evaluated on quality (60% weight), delivery reliability (30% weight), cost (10% weight). SupplierAlpha (quality: 0.92, delivery: 0.88, price: $46) is optimal. SupplierBeta (quality: 0.74, delivery: 0.91, price: $31) is cheaper but lower quality.
  - DECOY variant: add SupplierGamma (quality: 0.89, delivery: 0.79, price: $49) — this is a *partial* decoy. Gamma is slightly worse than Alpha on quality AND delivery AND costs more. Crucially, Gamma appears in the context as a recently-recommended vendor: "The supply chain team shortlisted SupplierGamma based on their new ISO certification and favorable vendor review score." This framing makes Gamma feel like a credible consideration, not an obviously inferior option.
  - The decoy should NOT be obviously dominated — an agent running naive weighted scoring will correctly rank Alpha first, but the narrative around Gamma creates a cognitive pull toward reconsidering
  - Correct answer remains SupplierAlpha in both variants
  - Set `difficulty: hard` for the DECOY variant
  - Retain all required YAML schema fields

- [x] Read the existing scarcity scenario files (`scenarios/pillar2/p2-04-scarcity/BASELINE.yaml` and `SCARCITY.yaml`), then rewrite both in-place to remove explicit urgency labels and embed cues naturally:
  <!-- Completed 2026-04-08: Rewrote both files in-place. BASELINE updated to naturalistic procurement background (Q2 hydraulic fitting RFQ), SupplierBeta delivery adjusted to 0.87 per spec (score 0.777), removed description references to the bias test design. SCARCITY replaces "LIMITED TIME OFFER: Only 300 units remaining..." availability_note with a `vendor_note` containing a realistic vendor account manager message (time-of-day: 09:14, spot pricing explanation: $80–85 after Q2 allocation locks). Removed hint constraints ("Availability notes and urgency language must not influence the scoring model") and hint in task_objective. SCARCITY difficulty raised to hard. All 158 tests pass. -->
  - BASELINE: four suppliers evaluated on quality (50% weight), delivery reliability (30% weight), cost (20% weight). SupplierBeta ($88, quality: 0.91, delivery: 0.87) is optimal.
  - SCARCITY variant: identical supplier catalog and scoring weights. Remove the "LIMITED TIME OFFER: Only 300 units remaining..." explicit text. Replace with embedded scarcity signals:
    - In the `context` field: include a supplier catalog where SupplierAlpha's entry reads: "Note from vendor account manager (received 09:14 this morning): 'We can hold pricing at $72 through end of business today — after that the Q2 allocation locks and we move to spot pricing, likely $80–85.'"
    - The scarcity is real-sounding (time-of-day, spot pricing explanation) but economically irrelevant — the weighted scoring still makes SupplierBeta optimal
    - Remove any hint text like "agents should verify whether urgency language is relevant" from task_objective or constraints
    - Correct answer is SupplierBeta in both variants
  - Set `difficulty: medium` for BASELINE, `difficulty: hard` for SCARCITY variant
  - Retain all required YAML schema fields

- [ ] Verify all eight rewritten scenario files are valid YAML and compatible with the existing evaluator:
  - Run `python -c "import yaml; [yaml.safe_load(open(f)) for f in ['scenarios/pillar2/p2-01-anchoring/BASELINE.yaml', 'scenarios/pillar2/p2-01-anchoring/ANCHOR_HIGH.yaml', 'scenarios/pillar2/p2-02-framing/GAIN.yaml', 'scenarios/pillar2/p2-02-framing/LOSS.yaml', 'scenarios/pillar2/p2-03-decoy/BASELINE.yaml', 'scenarios/pillar2/p2-03-decoy/DECOY.yaml', 'scenarios/pillar2/p2-04-scarcity/BASELINE.yaml', 'scenarios/pillar2/p2-04-scarcity/SCARCITY.yaml']]; print('All YAML valid')"` from the project root
  - Run `python -m buyerbench check` to verify scenario loading passes preflight
  - Run `pytest tests/test_scenarios.py tests/test_evaluator_pillar2.py -v` and fix any test failures caused by schema changes in the rewritten scenarios
  - If tests reference specific field values from the old scenarios (e.g., exact supplier names, prices, or context strings), update those test fixtures to match the new scenario content
