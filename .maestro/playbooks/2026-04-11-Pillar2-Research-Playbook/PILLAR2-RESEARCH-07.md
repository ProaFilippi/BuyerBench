# PILLAR2-RESEARCH-07 — Red Team Critique, Revised Plan & Execution Roadmap
## BuyerBench Pillar 2: Economic Rationality & Behavioral Biases in LLM Agents

> **Purpose:** Attack the full research design from a skeptical reviewer's perspective, then update the plan to address genuine weaknesses. Close with a concrete execution roadmap.

---

## SECTION M — RED TEAM CRITIQUE

> **Rule:** Be brutal. Assume a skeptical experimental economics referee who has seen many AI papers with inflated claims.

### M.1 Identification Weaknesses

- [x] **CRITIQUE 1 — No ground truth for "bias":**
  > "Your BSI measures deviation from your *defined* optimal. But you defined the optimal. If your evaluation weights are wrong, your 'bias' is just optimal behavior under different weights. You haven't established that your ground truth reflects genuine economic rationality."
  - **Severity:** High
  - **Response:** The optimal is algorithmically derivable from the scenario's stated evaluation weights (explicit in the YAML). This is an *internal* rationality test — does the agent optimize the stated objective? This is defensible. The paper must be explicit: we test whether agents optimize *the stated objective function*, not whether that function is itself rational.
  - **Implementation:** Added module-level docstring to `evaluators/pillar2.py` that explicitly frames the evaluator as testing internal rationality against the scenario's stated objective function, not external/universal optimality. Also updated `score_pillar2` and `compute_bias_susceptibility` docstrings to reinforce this scope. These docstrings serve as code-level anchors for the paper's claim framing (2026-04-16).

- [x] **CRITIQUE 2 — Single domain:**
  > "You tested supplier selection in procurement. All your results are specific to this exact context. You cannot generalize to anchoring 'in general' — an anchoring effect in procurement says nothing about anchoring in contract negotiation or investment decisions."
  - **Severity:** Medium
  - **Response:** Acknowledged as limitation. Restrict claims: "Bias susceptibility in LLM-based procurement decision-making." Frame domain specificity as a *feature* for applied relevance. Future work extends to other domains.
  - **Implementation:** Added `DOMAIN SCOPE` section to `evaluators/pillar2.py` module docstring (2026-04-16). The section: (1) names the exact canonical claim string ("LLM-based procurement decision-making"), (2) articulates three reasons domain specificity is a feature (applied relevance, ecological validity, scope control), (3) provides explicit MUST / MUST NOT examples for paper claim phrasing, and (4) documents future-work extension path. Also added `domain_scope` field to both return paths of `aggregate_bias_report` so the limitation is machine-readable in all downstream JSON/CSV exports.

- [x] **CRITIQUE 3 — Prompt sensitivity / researcher degrees of freedom:**
  > "You chose specific prompt wording. A different author with slightly different wording might find completely different BSI values. Your results are a property of *your prompts*, not of the models."
  - **Severity:** High
  - **Response:** This is a genuine threat. Mandatory robustness check: re-run with 2 minor prompt rephrasing variants and report sensitivity. If BSI changes by >0.1 with minor rephrasing, the result is not robust and must be flagged or dropped.
  - **Implementation:** Added `PROMPT SENSITIVITY` section to `evaluators/pillar2.py` module docstring documenting: (1) the threat framing, (2) the REV-5 go/no-go gate (CV > 0.50 → redesign), (3) a three-level interpretation table (CV ≤ 0.20 low / 0.20–0.50 moderate / > 0.50 high), and (4) the zero-mean edge case. Implemented `compute_prompt_sensitivity(bsi_by_phrasing, cv_threshold=0.50)` function that accepts per-phrasing pilot BSI lists, computes per-phrasing means, grand mean, population std-dev, and CV, and returns a `recommendation` of `"PROCEED"` or `"REDESIGN"` along with all intermediate values. Added 10 tests covering: identical phrasings (CV=0), high variation (REDESIGN), zero-BSI edge case, moderate variation, custom threshold, error on single phrasing, schema completeness, mean computation correctness, phrasings count, and exact-threshold boundary (≤, not <). All 62 pillar2 tests pass (2026-04-16).

- [x] **CRITIQUE 4 — No incentives:**
  > "LLMs don't receive monetary payoffs. The classic behavioral economics results (Kahneman, Thaler) were established with real stakes. Your 'biases' might be superficial text patterns, not genuine decision-theoretic failures."
  - **Severity:** High — fundamental to the framing
  - **Response:** This is unavoidable given the technology. Frame explicitly: "We test behavioral consistency, not incentivized decision-making. The LLM agent is making a decision it believes is consequential (it's been told it is). This is analogous to hypothetical-choice studies in behavioral economics, which do show bias effects comparable to incentivized designs (Camerer & Hogarth, 1999)." This response weakens the objection but does not eliminate it.
  - **Implementation:** Added `HYPOTHETICAL CHOICE FRAMING` section to `evaluators/pillar2.py` module docstring documenting: (1) the threat framing (no monetary payoffs), (2) the required claim framing ("behavioral consistency in hypothetical-choice tasks"), (3) the Camerer & Hogarth 1999 citation as methodological precedent, and (4) MUST / MUST NOT phrasing examples. Added `incentive_framing` field to both return paths of `aggregate_bias_report` — a machine-readable anchor so every downstream JSON/CSV export carries the limitation metadata alongside the BSI values. Also reinforced in `compute_bias_susceptibility` docstring (already present from prior work). Added 5 tests in `TestAggregateBiasReportIncentiveFraming` covering: field presence in empty report, field presence in non-empty report, value is a string, value mentions "hypothetical", and value is consistent across empty/non-empty calls. All 67 pillar2 tests pass (2026-04-16).

### M.2 Statistical Overclaims

- [x] **CRITIQUE 5 — Current data: N=1 run per cell:**
  > "Your session results show N=1 run per (model × scenario) cell. You have exactly one data point per cell. There is no possible inference. You've observed a realization, not a distribution."
  - **Severity:** Critical
  - **Response:** This is the core motivation for UPGRADE-1 (multi-run support). The current data is exploratory only. The paper cannot use current single-run data as evidence. **Do not claim results from current sessions — they are only useful for planning.**
  - **Implementation:** Added `SAMPLE SIZE LIMITATION` section to `evaluators/pillar2.py` module docstring documenting: (1) why N=1 is uninformative (a biased model with p=0.4 scores BSI=0 60% of the time), (2) three critical implications (BSI=0 ≠ unbiased, BSI=1 ≠ reliably biased, no statistical test is valid), (3) the N=50 inference threshold and N=5 pilot gate, and (4) the safe-by-default protocol (current session data = exploratory only). Added `n_runs_per_cell: int | None = None` parameter to `aggregate_bias_report` and two new fields: `exploratory_only` (True when n_runs_per_cell is None or ≤ 1) and `sample_size_warning` (constant string for JSON/CSV consumers). Added 14 tests in `TestAggregateBiasReportSampleSizeLimitation` covering: field presence in empty and non-empty reports, n_runs_per_cell echoed back, exploratory_only=True for None/0/1, exploratory_only=False for 2/50, warning is non-empty string, warning mentions "exploratory", warning is constant across n_runs values and empty/non-empty inputs. All 81 pillar2 tests pass (2026-04-16).

- [ ] **CRITIQUE 6 — N=10 models is too small for regression:**
  > "You ran a regression with N=10 units (models). That's not a regression — it's a description. Any OLS estimates have enormous uncertainty and no statistical meaning."
  - **Severity:** High
  - **Response:** Correct. All cross-model regressions (H2, capability gradient) must be labeled "descriptive patterns only." No inferential claims at the model level. Within-model tests (H1, H3, H5, H7) are the primary inferential engines with N=50+ runs per cell.

- [ ] **CRITIQUE 7 — Multiple comparisons without pre-registration:**
  > "You have 10 models × 5 bias types × 2 variants = 100 cells. At α=0.05, you expect 5 false positives by chance. Without pre-registration, you've picked the significant results."
  - **Severity:** High
  - **Response:** Pre-register before collecting data. Specify exactly which tests are confirmatory vs. exploratory. Apply BH correction. Label all unplanned analyses as exploratory. This must be done *before* running experiments.

### M.3 AI Evaluation Weaknesses

- [ ] **CRITIQUE 8 — Stochastic parroting:**
  > "LLMs trained on human text will reproduce human survey response patterns. Your 'biases' might just be training data memorization of human experiment results, not genuine cognitive patterns."
  - **Severity:** Medium
  - **Response:** Our scenarios use novel procurement contexts with specific numerical values unlikely to appear in training data. However, this cannot be fully ruled out. Frame as: "We cannot exclude training data effects; our results characterize behavioral patterns in deployment conditions regardless of mechanism." For flagship: include novel scenarios generated after models' knowledge cutoffs.

- [ ] **CRITIQUE 9 — Prompt injection via anchors:**
  > "When you put 'previous emergency procurement was $91/unit' in the prompt, you're not testing anchoring — you're testing whether the model can correctly ignore irrelevant information when explicitly told to. That's an instruction-following test, not a bias test."
  - **Severity:** Medium
  - **Response:** This is a genuine tension. The scenario design tries to make the anchor feel contextually natural, not explicitly irrelevant. But sophisticated models *will* try to reason about why the information is there. This may reduce effect sizes. Frame as: "Instruction-following ability and bias resistance may be empirically correlated in these models — we cannot fully separate them."

- [ ] **CRITIQUE 10 — Pillar 2 ceiling effect:**
  > "8 out of 10 models score 1.0 on Pillar 2 with N=1 run. Either your scenarios are trivially easy for frontier models, or something is wrong with your scoring. If everyone scores perfect, you have nothing to study."
  - **Severity:** High — this is the most pressing practical concern
  - **Response:** With N=1 run per cell, perfect scores are expected even for biased models (if bias probability < 1.0). At N=50 runs per cell, BSI will reveal stochastic bias rates that single runs obscure. Additionally, scenario difficulty should be increased for frontier models: more suppliers, more complex trade-offs, more realistic framing. If N=50 still shows ceiling effects, the paper must pivot to "LLMs show surprising resistance to standard behavioral biases" — which is *also* a publishable finding with different implications.

### M.4 External Validity

- [ ] **CRITIQUE 11 — These aren't real agents:**
  > "Real buyer agents don't just answer a single question from a chat prompt. They retrieve information from databases, call APIs, maintain multi-turn context. Your prompt-level 'agent' is a toy."
  - **Severity:** Medium
  - **Response:** Acknowledged. Frame scope precisely: "We evaluate the decision-making module of LLM agents — specifically, the judgment call made when an agent receives structured procurement options and must select among them. Tool use and retrieval are upstream; the decision bias occurs at this final selection stage."

---

## SECTION N — REVISED FINAL PLAN

> Incorporating all red team critiques above.

### N.1 Mandatory Revisions to Design

- [ ] **REV-1 (from M.1):** Add explicit statement in every results section: "Optimality is defined relative to the scenario's stated evaluation weights. We test internal rationality, not external optimality."

- [ ] **REV-2 (from M.3):** Pre-register before any data collection. Post OSF pre-registration with exact hypotheses, regression specs, and correction procedures.

- [ ] **REV-3 (from M.2 CRITIQUE 5):** Current single-run data is EXPLORATORY ONLY. Label clearly. Do not use in paper as evidence. Run N=50 minimum per cell before any claims.

- [ ] **REV-4 (from M.3 CRITIQUE 10 — Ceiling Effect):** Implement increased scenario difficulty variants:
  - More suppliers (5–8 instead of 3–4)
  - Closer utility scores (reducing δ between optimal and suboptimal from ~0.2 to ~0.05)
  - Compound manipulations (anchor + scarcity simultaneously)
  - These are needed if frontier models score 1.0 at N=50

- [ ] **REV-5 (from M.1 CRITIQUE 3):** Prompt robustness: before main experiment, run 5-run pilot at 3 prompt phrasings. If BSI coefficient of variation > 50%, do not proceed — redesign scenarios first.

- [ ] **REV-6 (from M.2 CRITIQUE 6):** Never use cross-model regression for inference. Present capability scatter as descriptive figure only. No p-values on cross-model comparisons.

- [ ] **REV-7 (from M.4):** Scope statement in abstract and introduction: "We evaluate the final selection stage of AI buyer agents — specifically, the economic judgment call when structured options are presented — not the full agent pipeline."

### N.2 Revised Paper Hierarchy of Claims

- [ ] **Tier A — Fully Defensible (confirm with data):**
  - "At temperature=0.7, [X] of 10 models show BSI > 0.1 on at least one bias type at N=50 runs per cell"
  - "Within-cell stochastic variance accounts for [Y%] of total BSI variance"
  - "Model X shows significantly elevated BSI on bias type Y (BH-corrected p < 0.05)"

- [ ] **Tier B — Suggestive (present with hedging):**
  - "Models with higher capability scores (Pillar 1) tend to show lower mean BSI (descriptive pattern, N=10)"
  - "The decoy effect appears in more models than the scarcity manipulation, suggesting [...]"

- [ ] **Tier C — Speculative (frame as future work, not findings):**
  - Any claim about *why* biases appear or disappear mechanistically
  - Any claim about generalization beyond procurement domain
  - Any claim about model architecture → bias pathway

---

## SECTION O — EXECUTION ROADMAP

### O.1 Next 2 Weeks (Concrete Steps)

**Week 1 — Infrastructure**

- [ ] **Day 1–2:** Implement UPGRADE-1 (multi-run support): add `--n-runs N` to `buyerbench run`; verify runs are independent (fresh session per run)
- [ ] **Day 2:** Implement UPGRADE-2 (supplier order randomization seed)
- [ ] **Day 3:** Implement UPGRADE-3 (temperature parameter support)
- [ ] **Day 3–4:** Implement UPGRADE-4 (run metadata logging: run_index, temperature, timestamp, tokens)
- [ ] **Day 4–5:** Implement UPGRADE-5 (cell-level aggregate output)
- [ ] **Day 5:** Write and run `research/scripts/00_define_experiment.py` — generate run_plan.csv and cost estimate
- [ ] **Day 5:** Run pilot experiment: N=5 runs per cell (50 total) to verify infrastructure. Check for errors, schema issues, rate limits.

**Week 2 — Pre-Registration & Pilot Analysis**

- [ ] **Day 6–7:** Write pre-registration document (OSF pre-reg template). Define primary hypotheses H1, H3, H5, H7 as confirmatory. All others exploratory. Register on OSF.
- [ ] **Day 7:** Run prompt robustness pilot (REV-5): 3 prompt phrasings × 5 runs × 2 bias types × 1 model. Compute BSI CV. Go/no-go decision.
- [ ] **Day 8–9:** Create `research/analysis/bsi.py` — reconcile BSI definition with `evaluators/pillar2.py`. Ensure formula is consistent.
- [ ] **Day 9–10:** Run realistic design at N=30 per cell as "pilot full run" (cost ~$450). Analyze: are ceiling effects present? Adjust scenario difficulty if needed.
- [ ] **Day 10:** Review pilot results. Decision gate: if ≥7/10 models score mean_BSI < 0.05 on all bias types → scenarios need harder variants (UPGRADE hardening pass). If some variation → proceed to N=50 run.

### O.2 Next 2–3 Months (Research Program)

**Month 1 — Data Collection**

- [ ] Week 3: If pilot clears decision gate → run full realistic design at N=50/cell. Total: 5,000 runs (~$750, ~15 hours).
- [ ] Week 3: Run temperature=0.0 robustness pass (N=30 per cell; deterministic): 3,000 runs (~$450).
- [ ] Week 4: Implement UPGRADE-7 (CoT and expert-role prompt variants).
- [ ] Week 4: Run CoT prompt variant experiment (N=30 per cell × 3 prompt versions): 4,500 runs (~$675).

**Month 2 — Analysis & Writing**

- [ ] Week 5: Run `research/analysis/regression.py` — primary mixed-effects model + variance decomposition
- [ ] Week 5: Generate all figures (Figures 1–4)
- [ ] Week 6: Write Sections 1–4 of working paper. All result claims templated from actual data.
- [ ] Week 6: Write Appendix B (pre-registration) and Appendix D (robustness checks)
- [ ] Week 7: Internal review / red team the draft. Apply N.2 claim-tier filter.
- [ ] Week 8: Revise draft. Prepare submission package.

**Month 3 — Flagship Expansion (Parallel Track)**

- [ ] Implement UPGRADE-8, UPGRADE-9, UPGRADE-10 (3 new bias scenarios: default, loss aversion, WARP)
- [ ] Prepare Prolific survey for human comparison arm
- [ ] Submit IRB application (if institution requires it for human subjects)
- [ ] Draft flagship paper outline incorporating human comparison arm data (placeholder sections)
- [ ] Run flagship LLM experiments (N=50 per cell × 8 bias types × 3 prompts): ~24,000 runs (~$3,600)

### O.3 Decision Gates (Explicit Go/No-Go Criteria)

- [ ] **Gate 1 (after Week 1 pilot):** Proceed to full N=50 run ONLY IF:
  - Infrastructure produces valid run records (error rate < 5%)
  - At least 2/10 models show mean_BSI > 0.05 on at least 1 bias type across N=5 pilot runs

- [ ] **Gate 2 (after prompt robustness check):** Proceed to main experiment ONLY IF:
  - BSI coefficient of variation across 3 prompt phrasings < 60% (i.e., results are not hypersensitive to exact wording)

- [ ] **Gate 3 (after N=50 full run):** Proceed to flagship/human arm ONLY IF:
  - At least 3/10 models show statistically detectable bias on at least 2/5 bias types (BH-corrected p < 0.10)
  - If all models show BSI ≈ 0 → pivot to "robust rationality" framing → still publishable, different journal

- [ ] **Gate 4 (before submission):** Apply Section N.2 claim tier filter. Every result statement must be labeled A, B, or C. No Tier C claims in main text.

### O.4 Risk Register

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Ceiling effect: all models score BSI≈0 | Medium | High | Harder scenario variants; pivot to robust rationality paper |
| API costs exceed budget | Low | Medium | Fractional factorial design; prioritize confirmatory hypotheses |
| Model versioning: models update between runs | Low-Medium | High | Pin exact model IDs at experiment start; log versions |
| Prompt sensitivity wipes out results | Medium | High | Robustness pilot (REV-5) before full run |
| N=10 models insufficient for inference | Certain | Medium | Acknowledged limitation; all cross-model analyses are descriptive |
| IRB delay for human arm | High | Medium | Start IRB application in Month 2; human arm is flagship only |
| Prior publication of nearly identical work | Low | High | Monitor arXiv weekly; adjust positioning if needed |
