# PILLAR2-RESEARCH-04 — Data Generation Plan & BuyerBench Evolution
## BuyerBench Pillar 2: Economic Rationality & Behavioral Biases in LLM Agents

> **Purpose:** Define the exact data schema, metadata requirements, and collection plan for reproducible research. Then critically assess the current BuyerBench system and specify upgrades needed for each design tier.

---

## SECTION H — DATA GENERATION PLAN

### H.1 Unit of Observation

- [x] **Primary unit:** A single *run* — one invocation of one LLM model on one scenario variant.
  - Identified by: `run_id = f"{session_id}_{agent_id}_{scenario_id}_{run_index}"`
  - ✅ **Verified (2026-04-16):** `session_id` format `session-YYYYMMDD-HHMMSS` is already implemented in `results/session_export.py:generate_session_id()`. `agent_id` and `scenario_id` are present in `EvaluationResult` (`buyerbench/models.py`). `run_index` is not yet implemented — planned as **UPGRADE-1** (Section I.2). Run ID is naturally time-sortable and collision-free given timestamp precision.

- [x] **Aggregation levels:**
  - Cell: (agent_id, scenario_id, variant) — primary analysis unit
  - Model: (agent_id) — capability comparisons
  - Bias type: (bias_category) — cross-model patterns
  - ✅ **Verified (2026-04-16):**
    - **Cell level** — *implicit but not explicit*. Each `EvaluationResult` in `buyerbench/models.py` carries `agent_id` and `scenario_id`, making one row per cell. However, `variant` lives on `Scenario` (not on `EvaluationResult`), so cell-level grouping by `(agent_id, scenario_id, variant)` cannot be done directly from the result record. `variant_pair_id` on `EvaluationResult` is the current proxy — it groups baseline+variant pairs for Pillar 2 bias analysis (`evaluators/aggregate.py:64-86`). **Gap:** `variant` (or `bias_category`) should be promoted to `EvaluationResult` to enable direct cell-level slicing. This is planned as **UPGRADE-4** (Section I.2).
    - **Model level** — *fully implemented*. Grouping by `agent_id` is the primary aggregation dimension throughout the codebase: `results/report.py:35-73` (`generate_summary_report`), `results/academic_tables.py:44-160` (`render_model_comparison_table`), and `buyerbench/dashboard.py:38-68` (`_aggregate`) all produce per-agent means, std, and pass rates.
    - **Bias type level** — *partially implemented*. `evaluators/pillar2.py:113-151` (`aggregate_bias_report`) groups BSI by `variant_type` extracted from `PillarScore.notes` (e.g., "Variant: ANCHOR_HIGH"). `evaluators/aggregate.py:256+` (`compute_bsi_from_experiment_dir`) calls this per agent and produces cross-agent summaries. **Gap:** `bias_category` is not a first-class field — it is inferred from scenario_id naming conventions (e.g., "p2-01-anchoring") and variant enum values, not stored as a structured attribute. The Run Record schema in H.2 introduces `bias_category` as an explicit field, which will require a schema extension.

### H.2 Data Schema

- [ ] **Run Record (per observation):**
  ```json
  {
    "run_id": "string (UUID)",
    "session_id": "string",
    "agent_id": "string (from registry)",
    "model_family": "string (openai|anthropic|google|meta|mistral|deepseek|qwen|cohere|01ai)",
    "model_version": "string (exact API model ID)",
    "scenario_id": "string (e.g., p2-01-anchoring)",
    "bias_category": "string (anchoring|framing|decoy|scarcity|sunk_cost|default|loss_aversion|warp)",
    "variant": "string (BASELINE|ANCHOR_HIGH|FRAMING_GAIN|FRAMING_LOSS|DECOY|SCARCITY|SUNK_COST|DEFAULT)",
    "run_index": "int (1-indexed within cell)",
    "temperature": "float",
    "prompt_version": "string (standard|cot|expert_role)",
    "supplier_order_seed": "int (random seed for supplier ordering randomization)",
    "timestamp_utc": "ISO 8601 string",
    "agent_output_raw": "string (full raw text response)",
    "extracted_choice": "string (supplier name or null)",
    "choice_is_correct": "bool",
    "optimal_choice": "string (ground truth)",
    "bsi": "float (0.0-1.0; bias susceptibility index for this run)",
    "optimality_gap": "float (economic utility distance from optimum)",
    "token_count_input": "int",
    "token_count_output": "int",
    "api_cost_usd": "float",
    "error_flag": "bool",
    "error_message": "string or null"
  }
  ```

- [ ] **Cell Aggregate Record (derived):**
  ```json
  {
    "cell_id": "string ({agent_id}__{scenario_id}__{variant}__{prompt_version}__{temperature})",
    "agent_id": "string",
    "scenario_id": "string",
    "bias_category": "string",
    "variant": "string",
    "n_runs": "int",
    "n_valid_runs": "int (excluding errors)",
    "mean_bsi": "float",
    "std_bsi": "float",
    "ci_lower_95": "float",
    "ci_upper_95": "float",
    "choice_rate_correct": "float",
    "choice_rate_distribution": "dict {supplier_name: count}",
    "mean_optimality_gap": "float",
    "treatment_effect_vs_baseline": "float or null (BSI_treatment - BSI_baseline; null if this IS baseline)"
  }
  ```

- [ ] **Experiment Manifest (one per experiment run):**
  ```json
  {
    "experiment_id": "string (date-slug)",
    "design_tier": "realistic|flagship",
    "n_models": "int",
    "n_bias_types": "int",
    "n_variants_per_bias": "int",
    "n_runs_per_cell": "int",
    "temperatures": "[float]",
    "prompt_versions": "[string]",
    "total_planned_runs": "int",
    "total_completed_runs": "int",
    "total_api_cost_usd": "float",
    "pre_registration_url": "string or null",
    "git_commit_hash": "string (exact code version)",
    "start_time_utc": "ISO 8601",
    "end_time_utc": "ISO 8601"
  }
  ```

### H.3 Experiment Scale (Realistic Design)

- [ ] **Dimensions:**
  - Bias types: 5 (existing)
  - Variants per bias: 2 (BASELINE + TREATMENT)
  - Models: 10 (existing registry)
  - Runs per cell: 50 (minimum viable for power)
  - Temperature: 1 (fixed at 0.7)
  - Prompt version: 1 (standard)

- [ ] **Total runs:** 5 × 2 × 10 × 50 = **5,000 runs**
- [ ] **Estimated cost:** ~$750 (at ~$0.15/run average; cost varies by model)
- [ ] **Estimated wall time:** ~15 hours serial; ~3 hours with max parallelism (rate limits permitting)

### H.4 Experiment Scale (Flagship Design — Phased)

- [ ] **Phase 1 (add new scenarios):** Expand to 8 bias types (add default, loss aversion, WARP)
- [ ] **Phase 2 (add prompt variants):** 3 prompt versions × existing 5 bias types × 10 models × 50 runs
- [ ] **Phase 3 (temperature sweep):** 4 temperatures × 5 bias types × 10 models × 30 runs
- [ ] **Phase 4 (human comparison):** 100 Prolific subjects × 8 scenarios (IRB required)

- [ ] **Total LLM runs (Flagship, Phases 1–3):** ~45,000 (use fractional factorial to reduce to ~20,000)
- [ ] **Budget estimate:** $3,000–$6,000 depending on model costs

### H.5 Metadata for Reproducibility

- [ ] Pin all model versions at experiment start (log exact `model` param returned by OpenRouter API)
- [ ] Fix `supplier_order_seed` per scenario-run to enable exact replay
- [ ] Log full prompt text (not just template) per run
- [ ] Archive raw API responses (not just extracted fields)
- [ ] Store `git_commit_hash` of BuyerBench codebase per experiment
- [ ] Use content-addressable run IDs (hash of: agent_id + scenario_id + variant + run_index + seed)

### H.6 Justification of Numbers

- [ ] **Why N=50 per cell?** Power analysis (Section G.8): provides 70% power for d=0.5 effect. Underpowered but labeled exploratory for d<0.5. Upgrade to N=100 for flagship.
- [ ] **Why 10 models?** Existing registry; covers major model families (OpenAI, Anthropic, Google, Meta, Mistral, DeepSeek, Qwen, Cohere, 01.AI). Adding more models is additive but not required for minimum paper.
- [ ] **Why 5 bias types for minimum?** Existing validated scenarios. Each new scenario requires validation (does it actually induce the intended bias in humans?). 5 is enough for cross-bias variance analysis.
- [ ] **Why temperature=0.7?** Standard default across most models. Robustness check at temp=0.0 (deterministic) is mandatory.

---

## SECTION I — BUYERBENCH EVOLUTION PLAN

### I.1 Critical Assessment of Current System

- [ ] **What is usable now:**
  - 5 Pillar 2 scenarios with controlled variant pairs (anchoring, framing, decoy, scarcity, sunk cost) — well-designed, single-variable isolation
  - 10 OpenRouter models in registry — covers major families
  - BSI metric implemented in `evaluators/pillar2.py` — computes deviation from optimum
  - Session runner with parallelism — can scale runs
  - Result schemas with JSON/CSV/Markdown output

- [ ] **What is underpowered:**
  - **Only 1 run per cell** in current sessions — no stochasticity modeling whatsoever
  - No temperature variation — temperature fixed at model default
  - No prompt variants — only standard prompt
  - No supplier order randomization — positional bias uncontrolled
  - No run index tracking — can't tell if results drift across runs

- [ ] **What is missing:**
  - No multi-run orchestration with configurable N per cell
  - No prompt variant support (CoT, expert-role)
  - No supplier order randomization seed
  - Missing 3 bias scenarios (default, loss aversion, WARP)
  - No variance decomposition in reporting
  - No cell-level confidence intervals in output
  - No pre-registration support (no frozen experiment manifest)

### I.2 Minimal Upgrade (Realistic Paper — ~2 weeks engineering)

- [ ] **[UPGRADE-1] Multi-run support:** Add `--n-runs N` CLI parameter to `buyerbench run`. Re-run each scenario N times independently per model. Log `run_index`.
  - Implementation: loop in `harness/runner.py`; each run gets fresh session; store run_index in result
  - Estimated effort: 2 days

- [ ] **[UPGRADE-2] Supplier order randomization:** Add `supplier_order_seed` parameter to scenario runner. Shuffle supplier list in prompt before each run using this seed.
  - Implementation: `harness/prompt.py`: accept seed, shuffle `context.suppliers` list
  - Estimated effort: 0.5 days

- [ ] **[UPGRADE-3] Temperature parameter support:** Pass `temperature` param to OpenRouter agent adapter. Add `--temperature FLOAT` to CLI.
  - Implementation: `agents/openrouter_agent.py`: expose temperature in API call
  - Estimated effort: 0.5 days

- [ ] **[UPGRADE-4] Run metadata logging:** Extend `EvaluationResultJSON` schema to include `run_index`, `temperature`, `timestamp_utc`, `token_count`, `api_cost_usd`.
  - Implementation: `results/schemas.py` + evaluator pass-through
  - Estimated effort: 1 day

- [ ] **[UPGRADE-5] Cell-level aggregate output:** After N runs per cell, compute mean_bsi, std_bsi, CI_95, and treatment_effect. Output as `cell_aggregates.json` alongside run-level data.
  - Implementation: new `results/aggregate_cells.py`
  - Estimated effort: 1 day

- [ ] **[UPGRADE-6] Robustness at temp=0.0:** Add one temperature=0.0 pass as mandatory robustness check in `buyerbench run` when `--research-mode` flag is used.
  - Estimated effort: 0.5 days

### I.3 Medium Upgrade (Extended Realistic Paper — ~6 weeks)

- [ ] **[UPGRADE-7] Prompt variant support:** Add `prompt_version` parameter (standard|cot|expert_role) to scenario runner. Define CoT and expert-role prompt templates in `harness/prompt.py`.
  - CoT template: prefix with "Think step by step through each option before making your final decision."
  - Expert-role template: prefix with "You are a senior procurement officer with 20 years of experience in industrial supply chain management."
  - Estimated effort: 2 days

- [ ] **[UPGRADE-8] New scenario — Default/Status Quo Bias (p2-06):** Design and validate scenario pair. Baseline: choose between two suppliers with equal presentation. Treatment: one supplier pre-selected/highlighted as "current approved vendor."
  - Estimated effort: 2 days (scenario design + YAML + evaluator test)

- [ ] **[UPGRADE-9] New scenario — Loss Aversion Switching (p2-07):** Baseline: switch from incumbentA to betterB (framed neutrally). Treatment: switch framed as "giving up established relationship worth $X."
  - Estimated effort: 2 days

- [ ] **[UPGRADE-10] WARP Battery (p2-08):** 3 binary pairwise choice tasks (A vs B, B vs C, A vs C) — run as 3 separate scenarios, then measure transitivity. Requires multi-scenario session grouping.
  - Estimated effort: 3 days (complex: requires session pairing logic)

- [ ] **[UPGRADE-11] Experiment manifest:** Auto-generate frozen `experiment_manifest.json` at run start with all configuration parameters and git commit hash.
  - Estimated effort: 0.5 days

### I.4 Full Research Platform (Flagship Paper — ~3 months)

- [ ] **[UPGRADE-12] Fractional factorial design orchestrator:** Given experiment dimensions, auto-generate a fractional factorial run plan that maximizes coverage while minimizing total runs. Output run plan CSV.

- [ ] **[UPGRADE-13] Human comparison survey harness:** Export scenarios to Qualtrics-compatible survey format. Parse survey responses back into BSI format.

- [ ] **[UPGRADE-14] Statistical analysis pipeline:** Integrated R or Python stats module that runs regression specs from Section G automatically after data collection.

- [ ] **[UPGRADE-15] Pre-registration export:** Generate OSF pre-registration document from experiment manifest + hypothesis definitions. (Format compatible with OSF structured pre-reg.)

- [ ] **[UPGRADE-16] Literature benchmark calibration:** Load human BSI benchmarks from literature (hardcoded from key papers) and auto-overlay on results plots as reference lines.
