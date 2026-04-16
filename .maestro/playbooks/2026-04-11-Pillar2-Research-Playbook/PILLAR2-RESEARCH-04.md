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

- [x] **Run Record (per observation):**
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
  ✅ **Verified (2026-04-16):** Field-by-field gap analysis against current implementation:

  | Field | Status | Implementation Notes |
  |---|---|---|
  | `run_id` | **MISSING** | No unique run identifier exists. Must be added as **UPGRADE-4** (Section I.2). UUID or content-addressable hash of (agent_id + scenario_id + variant + run_index + seed). |
  | `session_id` | **PARTIAL** | `generate_session_id()` in `results/session_export.py:13-15` produces `session-YYYYMMDD-HHMMSS`. Not stored on `EvaluationResult` — tracked only in `SessionMetadata`. Needs to be propagated to run-level records. |
  | `agent_id` | **PRESENT** | `EvaluationResult.agent_id` (`buyerbench/models.py:71`). Already in `EvaluationResultJSON` (`results/schemas.py:21`). |
  | `model_family` | **PRESENT (indirect)** | `ModelEntry.provider` in `buyerbench/model_catalog.py:16` (e.g., "OpenAI", "Anthropic"). Not denormalized onto result records; must be joined via `agent_id` lookup. Normalization to the target enum (lowercase) needed. |
  | `model_version` | **MISSING** | `model_id` in `ModelEntry` (e.g., `"openai/gpt-4o"`) is static config, not captured from API response. OpenRouter returns exact model version in responses but it is not parsed. |
  | `scenario_id` | **PRESENT** | `EvaluationResult.scenario_id` (`models.py:70`). Also in CSV export (`session_export.py:147`). |
  | `bias_category` | **PARTIAL** | `ScenarioVariant` enum (`models.py:10-19`) covers BASELINE, FRAMING_GAIN, FRAMING_LOSS, DECOY, ANCHOR_HIGH, ANCHOR_LOW, SCARCITY, SUNK_COST. The string bias_category (e.g. "anchoring") is inferred from scenario_id naming convention (e.g. "p2-01-anchoring"), not stored as a first-class field. Confirmed gap from H.1 verification — promoted to **UPGRADE-4**. |
  | `variant` | **PRESENT (indirect)** | `Scenario.variant: ScenarioVariant` (`models.py:38`). Available during evaluation but not propagated to `EvaluationResult`. `variant_pair_id` is the current proxy (`models.py:75`). Explicit `variant` field needed on `EvaluationResult`. |
  | `run_index` | **MISSING** | Not tracked anywhere. Only one run per cell currently. Planned as **UPGRADE-1** (Section I.2). |
  | `temperature` | **MISSING** | Not configurable or logged. `OpenRouterAgent` (`agents/openrouter_agent.py:31-57`) does not expose temperature in its API call. Planned as **UPGRADE-3**. |
  | `prompt_version` | **MISSING** | `scenario_to_prompt()` in `harness/prompt.py` has no versioning concept. Planned as **UPGRADE-7** (Section I.3). |
  | `supplier_order_seed` | **MISSING** | `_format_context()` in `harness/prompt.py:86-109` renders supplier lists deterministically. No shuffling or seeding logic exists. Planned as **UPGRADE-2**. |
  | `timestamp_utc` | **PRESENT** | `EvaluationResult.timestamp: datetime` (`models.py:74`) defaults to `datetime.now(timezone.utc)`. Also exported in CSV (`session_export.py:154`). |
  | `agent_output_raw` | **PRESENT** | `EvaluationResult.raw_output: str` (`models.py:76`). Full agent response text captured. Also in `EvaluationResultJSON.raw_output` (`schemas.py:26`). |
  | `extracted_choice` | **PRESENT (indirect)** | `EvaluationResult.decisions: dict[str, Any]` (`models.py:77`) holds parsed decisions from `parse_agent_output()` (`harness/prompt.py:154-182`). Key is scenario-specific (e.g., `"selected_supplier"`); no normalized `extracted_choice` string field. |
  | `choice_is_correct` | **PRESENT (indirect)** | `PillarScore.metrics["optimal_chosen"]` in `evaluators/pillar2.py:54` (float 0.0/1.0, not a bool). Accessible via `EvaluationResult.pillar_scores[0].metrics`. |
  | `optimal_choice` | **PRESENT (indirect)** | `Scenario.expected_optimal: dict[str, Any]` (`models.py:43`). Ground truth stored per scenario but not on result record — must be joined via scenario lookup. |
  | `bsi` | **PRESENT (indirect)** | `PillarScore.metrics["bias_susceptibility_index"]` (`pillar2.py:57`). Per-run BSI is 0.0 (optimal) or scaled by `(1.0 - baseline_score)` for variant runs (`pillar2.py:95`). Accessible but nested. |
  | `optimality_gap` | **PRESENT (indirect)** | `PillarScore.metrics["optimality_gap"]` (`pillar2.py:55`). Computed by `_compute_optimality_gap()` (`pillar2.py:177-217`). Accessible but nested. |
  | `token_count_input` | **MISSING** | OpenRouter API response includes a `usage` object but it is not parsed. Only `content` is extracted (`agents/openrouter_agent.py:118`). |
  | `token_count_output` | **MISSING** | Same as above — `usage.completion_tokens` not parsed. |
  | `api_cost_usd` | **MISSING** | `ModelEntry.cost_tier` provides qualitative cost tier ("free"/"low"/"mid"/"high") but no per-run USD cost is computed. OpenRouter API returns cost in response metadata which is not captured. |
  | `error_flag` | **PARTIAL** | Exceptions are caught in `agents/openrouter_agent.py:119` and stored as string in `raw_output` (`line 125`). No explicit `bool` error_flag field. |
  | `error_message` | **PARTIAL** | Exception message captured in `raw_output` on error (`openrouter_agent.py:125`). No separate structured field; conflated with valid output. |

  **Summary:** 7 fields fully present (agent_id, scenario_id, timestamp_utc, agent_output_raw, and 3 indirect), 5 fields partially present (session_id, model_family, bias_category, error_flag, error_message), 12 fields missing (run_id, model_version, variant on result, run_index, temperature, prompt_version, supplier_order_seed, token_count_input, token_count_output, api_cost_usd, extracted_choice as normalized string, optimal_choice on result). All 12 missing fields are addressed by UPGRADE-1 through UPGRADE-4 (Section I.2).

- [x] **Cell Aggregate Record (derived):**
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
  ✅ **Verified (2026-04-16):** Field-by-field gap analysis for the Cell Aggregate Record. **Critical prerequisite gap:** The Cell Aggregate Record presupposes N ≥ 2 runs per cell. The current system produces exactly 1 run per cell (one scenario execution per agent per scenario), making mean, std, and CI computations meaningless. UPGRADE-1 (multi-run support) must land before this record is populatable. No `results/aggregate_cells.py` module exists (confirmed by search); UPGRADE-5 proposes creating it.

  | Field | Status | Implementation Notes |
  |---|---|---|
  | `cell_id` | **MISSING** | No cell abstraction exists anywhere in the codebase. The closest is `variant_pair_id` on `EvaluationResult` (`models.py:75`), which identifies a 2-scenario pair but is not a multi-run cell ID. Cell ID construction requires `variant` and `temperature` fields which are themselves missing from `EvaluationResult`. Planned as **UPGRADE-4** + **UPGRADE-5**. |
  | `agent_id` | **PRESENT** | `EvaluationResult.agent_id` (`models.py:71`). Directly available. |
  | `scenario_id` | **PRESENT** | `EvaluationResult.scenario_id` (`models.py:70`). Directly available. |
  | `bias_category` | **MISSING** | Same gap as H.2 Run Record. Inferred from scenario_id naming convention (e.g., "p2-01-anchoring" → "anchoring") but not stored as a structured field on `EvaluationResult` or any aggregate schema. Requires **UPGRADE-4**. |
  | `variant` | **MISSING (on result)** | `Scenario.variant: ScenarioVariant` (`models.py:38`) — present on the scenario definition but never propagated to `EvaluationResult`. `variant_pair_id` is the current proxy but is only a pair grouping key, not a variant label. Cell-level grouping by `(agent_id, scenario_id, variant)` is impossible from result records alone. Requires **UPGRADE-4**. |
  | `n_runs` | **MISSING** | No multi-run support exists. Each scenario is executed exactly once per agent. `run_index` does not exist on `EvaluationResult`. Requires **UPGRADE-1** before this field has meaning. |
  | `n_valid_runs` | **MISSING** | No `error_flag` boolean field on `EvaluationResult`. Errors are embedded in `raw_output` as string patterns (e.g., "Client Error:"), detected heuristically in `generate_full_report()` (`report.py:127-129`). No structured error count per cell. Requires **UPGRADE-4**. |
  | `mean_bsi` | **PARTIAL** | `aggregate_bias_report()` in `evaluators/pillar2.py:113-151` computes `mean_bsi` across variant pairs per bias type — but this is **pair-level aggregation** (N=1 observation per pair), not **cell-level aggregation** (N ≥ 2 runs per cell arm). The current mean is a mean across bias types, not a mean across repeated runs of the same cell. Requires UPGRADE-1 to become meaningful. |
  | `std_bsi` | **MISSING** | `aggregate_bias_report()` does not compute standard deviation — only mean and count per variant type. No std computed anywhere in the codebase for BSI. Requires UPGRADE-1 (need N runs) + UPGRADE-5 (new aggregate module). |
  | `ci_lower_95` | **MISSING** | No confidence interval logic anywhere in the codebase. Requires UPGRADE-1 + UPGRADE-5. For N=50 runs, a normal approximation CI is straightforward; bootstrap CI would be appropriate for non-normal BSI distributions. |
  | `ci_upper_95` | **MISSING** | Same as `ci_lower_95`. |
  | `choice_rate_correct` | **PARTIAL** | `PillarScore.metrics["optimal_choice_rate"]` (`pillar2.py:18`) is 0.0 or 1.0 per run. `per_metric_breakdown` in `generate_full_report()` (`report.py:186-202`) computes mean per agent×pillar, but **not per cell** (agent × scenario × variant). Across N=1 run, this is identical to `choice_is_correct`. Requires UPGRADE-1 + UPGRADE-5 for meaningful cell-level rate. |
  | `choice_rate_distribution` | **MISSING** | No supplier choice frequency tracking exists. `EvaluationResult.decisions` (`models.py:77`) stores the chosen supplier per run, but there is no accumulation of counts across runs. Requires UPGRADE-1 + UPGRADE-5. |
  | `mean_optimality_gap` | **PARTIAL** | `PillarScore.metrics["optimality_gap"]` (`pillar2.py:55`) is computed per run by `_compute_optimality_gap()` (`pillar2.py:177-217`). `per_metric_breakdown` in `generate_full_report()` computes mean across scenarios per agent — but this is **agent-level**, not **cell-level** (single scenario × single variant). Requires UPGRADE-1 + UPGRADE-5 for proper per-cell mean. |
  | `treatment_effect_vs_baseline` | **MISSING** | `compute_bias_susceptibility()` (`pillar2.py:67-110`) computes a pair-level proxy: `int(decision_changed) * (1 - baseline_score)`. This is a single-observation treatment indicator, **not** a proper treatment effect estimate (i.e., not `E[BSI | treatment] - E[BSI | baseline]` across N runs). The BSI formula penalizes decision changes proportional to baseline suboptimality rather than computing a mean difference estimator. The H.2 schema field definition (`BSI_treatment - BSI_baseline`) requires N runs per arm. Requires UPGRADE-1 + UPGRADE-5 plus reformulation of the treatment effect estimator. |

  **Summary:** 2 fields fully present (agent_id, scenario_id), 3 fields partially present (mean_bsi as pair-level proxy, choice_rate_correct as single-run value, mean_optimality_gap as agent-level mean), 10 fields missing (cell_id, bias_category, variant on result, n_runs, n_valid_runs, std_bsi, ci_lower_95, ci_upper_95, choice_rate_distribution, treatment_effect_vs_baseline as proper mean-difference estimator). **Root cause of all gaps: UPGRADE-1 (multi-run support) is the hard prerequisite — no cell aggregate record is meaningful without N ≥ 2 runs per cell. UPGRADE-4 and UPGRADE-5 unlock the remaining fields.**

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
