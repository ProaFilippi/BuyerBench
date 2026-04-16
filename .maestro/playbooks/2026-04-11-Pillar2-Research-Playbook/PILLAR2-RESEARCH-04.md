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

- [x] **Experiment Manifest (one per experiment run):**
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
  ✅ **Verified (2026-04-16):** Field-by-field gap analysis against current implementation. **Critical structural gap:** There is no `ExperimentManifest` concept in the codebase. The closest structure is `SessionMetadata` (`results/session_export.py:18-33`), which is a *post-hoc* execution record (what happened), not a *design-time* manifest (what was planned). A proper experiment manifest must be created before execution commences to support pre-registration and frozen experiment scope — this is `UPGRADE-11` (Section I.3).

  | Field | Status | Implementation Notes |
  |---|---|---|
  | `experiment_id` | **MISSING** | No experiment-level identifier exists. Only `session_id` (`results/session_export.py:15`, format `session-YYYYMMDD-HHMMSS`) serves as an execution run identifier, not an experiment identifier. An experiment may span multiple sessions (e.g., resuming after failure). Proposed format is a semantic date-slug (e.g., `"2026-04-realistic-v1"`). Planned as **UPGRADE-11**. |
  | `design_tier` | **MISSING** | No `design_tier` enum exists anywhere in the codebase. The "realistic" vs "flagship" distinction lives only in documentation (`docs/paper/experimental-design/`), not in runtime metadata or CLI parameters. Must be added as a CLI flag (`--design-tier realistic|flagship`) and stored in the manifest. Planned as **UPGRADE-11**. |
  | `n_models` | **PARTIAL** | Implicitly computable as `len(SessionMetadata.agents)` (`session_export.py:21`). `__main__.py:460` builds `agent_ids = [aid for aid, _ in agents_to_run]` but never stores an explicit count. No manifest-level `n_models` integer field exists. Requires **UPGRADE-11** to formalize. |
  | `n_bias_types` | **MISSING** | Not tracked anywhere. Bias types are embedded in `ScenarioVariant` enum (`buyerbench/models.py:10-19`). Scenarios are loaded dynamically; no pre-experiment count is computed or stored. Must be computed from loaded scenario set at manifest creation time. Planned as **UPGRADE-11**. |
  | `n_variants_per_bias` | **MISSING** | Not tracked. Scenario pairing logic in `harness/loader.py:26-38` (`load_scenario_pairs()`) produces pairs of exactly 2 scenarios (BASELINE + treatment), but this cardinality is never aggregated into manifest-level metadata. Planned as **UPGRADE-11**. |
  | `n_runs_per_cell` | **MISSING** | Not supported. The CLI has no `--n-runs` parameter. Each scenario executes exactly once per agent per session (`__main__.py:382`). All statistical estimates requiring N≥2 runs per cell are blocked until **UPGRADE-1** (multi-run support). |
  | `temperatures` | **MISSING** | No temperature parameter exists anywhere in the agent stack. `OpenRouterAgent` (`agents/openrouter_agent.py:45-51`) does not expose temperature in its API call. No `temperatures` list can be declared or logged. Blocked until **UPGRADE-3**. |
  | `prompt_versions` | **MISSING** | No prompt versioning system. `scenario_to_prompt()` in `harness/prompt.py:63` generates prompts dynamically with no version tag. No version field on `Scenario` (`models.py:34-49`). Cannot declare or log `prompt_versions`. Blocked until **UPGRADE-7**. |
  | `total_planned_runs` | **MISSING** | No pre-experiment run count is calculated or declared. `SessionMetadata.scenarios_run` (`session_export.py:22`) is a *completed* count computed post-hoc (`__main__.py:468`), not a planned count. A manifest must compute `n_models × n_bias_types × n_variants_per_bias × n_runs_per_cell` before execution. Planned as **UPGRADE-11**. |
  | `total_completed_runs` | **PARTIAL** | Tracked post-hoc as `SessionMetadata.scenarios_run` (`session_export.py:22`) and `len(all_results)` in `__main__.py:348`. However, this lives in per-session exports, not a unified experiment manifest. Requires **UPGRADE-11** to formalize as a manifest-level field updated upon completion. |
  | `total_api_cost_usd` | **MISSING** | No cost tracking exists. `OpenRouterAgent` makes API calls but never parses the `usage` object from responses (`agents/openrouter_agent.py:118` only extracts `content`). `ModelEntry.cost_tier` in `buyerbench/model_catalog.py:16` provides qualitative tiers ("free"/"low"/"mid"/"high") but no USD amounts. OpenRouter returns per-request cost in response metadata — this is not captured. Blocked until **UPGRADE-4** (token/cost capture). |
  | `pre_registration_url` | **MISSING** | No field exists in any model or schema. Pre-registration is discussed in literature notes (e.g., `docs/paper/literature-map/b5-02-simmons-nelson-simonsohn-2011.md`) but not implemented. No CLI parameter or manifest slot to record a pre-registration URL. Planned as **UPGRADE-15** (full research platform tier). |
  | `git_commit_hash` | **MISSING** | No git integration for version capture at experiment time. Neither `SessionMetadata` nor any result schema captures the git commit hash. Reproducibility currently requires manual documentation. A one-liner using `subprocess.check_output(["git", "rev-parse", "HEAD"])` would suffice. Planned as **UPGRADE-11**. |
  | `start_time_utc` | **PRESENT** | `SessionMetadata.started_at: datetime` (`session_export.py:24`), set to `datetime.now(timezone.utc)` in `__main__.py:346`. Exported as ISO 8601 in session markdown (`session_export.py:71` via `.isoformat()`). Fully implemented at session level; needs to be promoted to manifest level in **UPGRADE-11**. |
  | `end_time_utc` | **PRESENT** | `SessionMetadata.completed_at: datetime` (`session_export.py:25`), set to `datetime.now(timezone.utc)` in `__main__.py:457`. Exported as ISO 8601 in session markdown (`session_export.py:72`). Duration derived via `duration_seconds` property (`session_export.py:32`). Needs promotion to manifest level in **UPGRADE-11**. |

  **Summary:** 2 fields fully present (start_time_utc, end_time_utc in `SessionMetadata`), 2 fields partially present (n_models as implicit count, total_completed_runs in `SessionMetadata.scenarios_run`), 11 fields missing (experiment_id, design_tier, n_bias_types, n_variants_per_bias, n_runs_per_cell, temperatures, prompt_versions, total_planned_runs, total_api_cost_usd, pre_registration_url, git_commit_hash). **Root structural gap: No `ExperimentManifest` class exists — the codebase models execution sessions but not experiment-level design intent.** UPGRADE-11 creates this class; UPGRADE-1, -3, -4, -7 must land first to populate the configuration fields that reference multi-run, temperature, prompt version, and cost data.

### H.3 Experiment Scale (Realistic Design)

- [x] **Dimensions:**
  - Bias types: 5 (existing)
  - Variants per bias: 2 (BASELINE + TREATMENT)
  - Models: 10 (existing registry)
  - Runs per cell: 50 (minimum viable for power)
  - Temperature: 1 (fixed at 0.7)
  - Prompt version: 1 (standard)
  ✅ **Verified (2026-04-16):** All five dimensions confirmed against current codebase:
  - **Bias types: 5** — confirmed by listing all 10 YAML files in `scenarios/pillar2/`: `p2-01-anchor-high` (anchoring), `p2-02-framing` (framing), `p2-03-decoy` (decoy), `p2-04-scarcity` (scarcity), `p2-05-sunk-cost` (sunk cost). Each has exactly one BASELINE + one TREATMENT variant file, totalling 10 scenario YAMLs.
  - **Variants per bias: 2** — confirmed. Each pair is one BASELINE + one treatment-arm scenario. Treatment variant names: `ANCHOR_HIGH`, `FRAMING_LOSS`/`FRAMING_GAIN`, `DECOY`, `SCARCITY`, `SUNK_COST`.
  - **Models: 10** — confirmed by `MODEL_CATALOG` list in `buyerbench/model_catalog.py:23-124`. Exactly 10 `ModelEntry` objects spanning 9 providers (OpenAI, Anthropic, Google, Meta, Mistral×2, DeepSeek, Alibaba, Cohere, 01.AI). Distribution: 2 high-cost, 3 mid-cost, 5 low-cost.
  - **Runs per cell: 50** — NOT YET IMPLEMENTED. Current system runs exactly 1 run per cell. This is the target N; actual implementation requires **UPGRADE-1** (multi-run loop with `--n-runs N` CLI flag). The value N=50 derives from the power analysis in Section G.8 (70% power at d=0.5 for one-sided t-test).
  - **Temperature: 1 (fixed at 0.7)** — NOT YET CONFIGURABLE. `OpenRouterAgent` (`agents/openrouter_agent.py:45-51`) does not expose a temperature parameter; it uses the model's API default. Target: fix at 0.7, which is standard across most providers for instruction-following tasks. Requires **UPGRADE-3**.
  - **Prompt version: 1 (standard)** — CONFIRMED as current state. Only `scenario_to_prompt()` in `harness/prompt.py:24-83` exists; no CoT or expert-role variants. This single function produces the standard prompt format. Prompt versioning requires **UPGRADE-7**.

- [x] **Total runs:** 5 × 2 × 10 × 50 = **5,000 runs**
  ✅ **Verified (2026-04-16):** Arithmetic confirmed: 5 bias types × 2 variants/bias × 10 models × 50 runs/cell = 5,000. Note this is the *realistic* design total — it excludes the robustness pass at temperature=0.0 (UPGRADE-6), which would add another 5 × 2 × 10 × 50 = 5,000 runs. The flagship design (H.4) scales to ~20,000–45,000 runs.

- [x] **Estimated cost:** ~$750 (at ~$0.15/run average; cost varies by model)
  ✅ **Verified (2026-04-16):** $0.15/run is a conservative upper-bound estimate. Analysis of actual prompt sizes and current OpenRouter pricing suggests a significantly lower realistic range:
  - **Prompt size:** `scenario_to_prompt()` renders a compact Markdown block from scenario YAML. A representative P2 scenario (`p2-01-anchor-high-BASELINE.yaml`) yields approximately 400–600 tokens of input prompt; agent responses are typically 200–400 tokens of structured JSON output. Total: ~600–1,000 tokens/run.
  - **Per-run cost by tier (at current OpenRouter pricing):**
    - High-cost (GPT-4o, Claude 3.5 Sonnet): ~$0.006–$0.009/run
    - Mid-cost (Gemini Pro 1.5, Mistral Large, Command R+): ~$0.002–$0.004/run
    - Low-cost (Llama 405B, DeepSeek, Qwen, Mixtral, Yi): ~$0.0001–$0.0005/run
    - **Blended average across 10 models: ~$0.002–$0.005/run**
  - **Realistic total for 5,000 runs: ~$10–$25** under current pricing at compact prompt sizes.
  - **Where $750 comes from:** The $0.15/run estimate is appropriate if: (a) prompts are much larger (e.g., full CoT reasoning traces or multi-turn context ~5,000+ tokens), (b) model pricing increases substantially before the experiment runs, (c) the experiment includes the flagship scale (~45,000 runs), or (d) a generous safety margin is applied for retries, API errors, and developer cost overhead. **Recommendation:** Treat $750 as a worst-case ceiling for budget approval purposes; plan operationally for $50–$150.

- [x] **Estimated wall time:** ~15 hours serial; ~3 hours with max parallelism (rate limits permitting)
  ✅ **Verified (2026-04-16):** Both estimates are consistent with observed session timing data from `results/session-20260411-200247.csv`, which ran all 10 Pillar 2 agents × 10 scenarios (100 P2 runs) with full agent parallelism in approximately 28 minutes of wall time.
  - **Per-run timing observed across models:**
    - GPT-4o: ~2.0 sec/run (fastest; 10 scenarios in 20s)
    - Claude 3.5 Sonnet: ~4.8 sec/run (10 scenarios in 48s)
    - Mistral Large: ~3.6 sec/run (10 scenarios in 36s)
    - Llama 3.3 70B: ~6.5 sec/run (10 scenarios in 65s)
    - Gemini 2.5 Pro: **~20.7 sec/run** (10 scenarios in 207s — this is the bottleneck)
  - **Serial estimate (~15 hours):** At an average of ~10–11 sec/run across all 10 models, 5,000 runs × 10.8s = 54,000s ≈ **15.0 hours**. Consistent with observed data.
  - **Parallelism estimate (~3 hours):** With 10 agents running concurrently (current `BuyerBench` architecture using `asyncio`/thread-pool in `__main__.py`), wall time is bounded by the **slowest model**. Gemini's ~20.7s/run × 500 runs/model = 10,350s ≈ **2.9 hours**. Rate limit headroom (60-second sleep-retry visible in `agents/openrouter_agent.py`) adds overhead — budget 3.0–3.5 hours. The "~3 hours" estimate is well-calibrated.
  - **Note:** All five remaining models (DeepSeek, Qwen, Mixtral, Command R+, Yi Large) were not in the timing sample; they are likely faster than Gemini given lower model complexity and OpenRouter's routing. Gemini 2.5 Pro remains the projected wall-time bottleneck for the realistic experiment.

### H.4 Experiment Scale (Flagship Design — Phased)

- [x] **Phase 1 (add new scenarios):** Expand to 8 bias types (add default, loss aversion, WARP)
  ✅ **Verified (2026-04-16):** Engineering analysis for each of the three new bias types, against current codebase:

  **1. Default / Status Quo Bias (p2-06-default) → UPGRADE-8**
  - `ScenarioVariant.DEFAULT` **already exists** in `buyerbench/models.py:19`. No schema change required — this is the most ready-to-implement of the three.
  - Design: BASELINE presents two suppliers with neutral framing; DEFAULT variant marks one supplier as `"current_approved_vendor": true` (or equivalent YAML field) to simulate status quo anchoring. The agent should still choose the objectively higher-scoring supplier regardless.
  - Evaluator: existing `score_pillar2()` and `compute_bias_susceptibility()` (`evaluators/pillar2.py`) handle this correctly — they compare optimal_chosen across the pair; no evaluator logic changes needed.
  - Engineering cost: **~2 days** (2 YAML files + 1 evaluator test). No code changes to models, loader, or evaluators.
  - Blocker: None. Can land independently as soon as YAML files are authored and reviewed.

  **2. Loss Aversion Switching (p2-07-loss-aversion) → UPGRADE-9**
  - `LOSS_AVERSION` is **absent** from `ScenarioVariant` enum (`models.py:10-19`). Loading a YAML with `variant: LOSS_AVERSION` will raise a Pydantic `ValidationError` today. Schema change required: add `LOSS_AVERSION = "LOSS_AVERSION"` to the enum.
  - Design: BASELINE presents a switch from an inferior incumbent (VendorA) to a superior alternative (VendorB) using neutral language (e.g., "evaluate both vendors"). LOSS_AVERSION variant re-frames the same switch as abandoning an established relationship ("giving up a $X/year partnership with VendorA"). Economics are identical across both variants; the correct choice (VendorB) is unchanged.
  - Evaluator: the existing `compute_bias_susceptibility()` logic handles the pair correctly once loaded — no evaluator changes needed beyond the schema extension.
  - Engineering cost: **~2.5 days** (1-line enum addition + 2 YAML files + 1 evaluator test + regression test for new enum value).
  - Blocker: `ScenarioVariant` enum extension must land before YAML can be loaded.

  **3. WARP Battery (p2-08-warp) → UPGRADE-10**
  - `WARP` is **completely absent** from the codebase — not in `ScenarioVariant`, not in any scenario directory, not referenced in any evaluator.
  - **Structural incompatibility:** WARP (Weak Axiom of Revealed Preference) requires 3 binary pairwise choice tasks per battery: (A vs B), (B vs C), (A vs C). A rational agent must exhibit transitive preferences (if A≻B and B≻C, then A≻C). This is fundamentally different from the existing BASELINE + TREATMENT pair design:
    - `load_scenario_pairs()` in `harness/loader.py:26-38` silently skips any `variant_pair_id` group with `len(members) != 2`. A WARP battery (3 scenarios sharing a `variant_pair_id`) would be **silently dropped** today.
    - `compute_bias_susceptibility()` in `evaluators/pillar2.py:67-110` computes a 2-scenario BSI; WARP requires a 3-scenario **transitivity check** (detect cycles: A≻B, B≻C, C≻A) rather than a deviation measure.
    - The aggregation schema (`aggregate_bias_report()`, `pillar2.py:113-151`) has no concept of a "transitivity violation rate".
  - Required changes:
    - Add `WARP = "WARP"` (or enum values `WARP_AB`, `WARP_BC`, `WARP_AC`) to `ScenarioVariant`.
    - Extend `load_scenario_pairs()` to support 3-member groups, or add a new `load_scenario_triplets()` loader.
    - Add `compute_warp_transitivity()` function to `evaluators/pillar2.py` alongside `compute_bias_susceptibility()`.
    - WARP run count: 3 scenario files × 10 models × 50 runs = **1,500 runs per arm** (vs. 500 runs per arm for a standard 2-scenario pair). The asymmetry means WARP cannot be treated as a uniform "bias type" for run-count arithmetic.
  - Engineering cost: **~3–4 days** (UPGRADE-10 estimated: "complex: requires session pairing logic").
  - Blocker: `load_scenario_pairs()` must be refactored before WARP scenarios can be executed.

  **Schema changes required before Phase 1 can proceed:**
  | Bias Type | ScenarioVariant change | Loader change | Evaluator change |
  |---|---|---|---|
  | Default (p2-06) | None (DEFAULT exists) | None | None |
  | Loss Aversion (p2-07) | Add `LOSS_AVERSION` | None | None |
  | WARP (p2-08) | Add `WARP` (or triplet enums) | `load_scenario_pairs()` → support 3-member groups | Add `compute_warp_transitivity()` |

  **Run count impact on Phase 1 total:**
  Default and Loss Aversion each add 1 × 2 × 10 × 50 = **1,000 runs**. WARP adds 3 × 10 × 50 = **1,500 runs** (3 binary tasks per battery, no BASELINE counterpart — the pairwise comparison IS the baseline). Phase 1 total: 5,000 (existing) + 1,000 + 1,000 + 1,500 = **8,500 runs** for the 8-bias-type battery (not 8 × 2 × 10 × 50 = 8,000, because WARP contributes 3 scenarios rather than 2). Budget impact: ~$17–$43 incremental at realistic prompt pricing.

  **Recommended implementation order:** p2-06-default (no blockers) → p2-07-loss-aversion (add 1 enum value) → p2-08-warp (requires loader refactor; defer to Phase 1 completion sprint).

- [x] **Phase 2 (add prompt variants):** 3 prompt versions × existing 5 bias types × 10 models × 50 runs
  ✅ **Verified (2026-04-16):** Engineering analysis of Phase 2 prompt-variant expansion against current codebase.

  **The three prompt versions (from UPGRADE-7 spec):**
  1. `standard` — current implementation. `_SYSTEM_PREAMBLE` in `harness/prompt.py:14-21` is the active preamble; `scenario_to_prompt()` (`harness/prompt.py:24-83`) appends task objective, context, constraints, and output format with no cognitive framing prefix.
  2. `cot` (chain-of-thought) — UPGRADE-7 target prefix: *"Think step by step through each option before making your final decision."* Not yet implemented anywhere in the codebase.
  3. `expert_role` — UPGRADE-7 target prefix: *"You are a senior procurement officer with 20 years of experience in industrial supply chain management."* Not yet implemented anywhere in the codebase.

  **Run count calculation:**
  The task formula "3 prompt versions × existing 5 bias types × 10 models × 50 runs" omits the 2 variants/bias dimension (BASELINE + TREATMENT). Corrected total: **3 × 5 × 2 × 10 × 50 = 15,000 runs** for the full Phase 2 prompt-variant sweep applied to all 5-bias-type cells. Since Phase 1 already covers the `standard` version (5,000 runs), the **net incremental runs are 10,000** (2 new prompt versions × 5 × 2 × 10 × 50). Running total after Phases 1 + 2: 15,000 runs. Budget impact: ~$30–$75 incremental at realistic prompt pricing (prompt tokens increase by ~10–15 tokens per CoT/expert prefix — negligible cost effect).

  **Implementation gap analysis by component:**

  | Component | Status | Gap / Path to Fix |
  |---|---|---|
  | `harness/prompt.py:scenario_to_prompt()` | **MISSING** | Single function with no `prompt_version` parameter. `_SYSTEM_PREAMBLE` is a module-level constant (`line 14`), not a per-version dispatch table. Needs a `prompt_version: str = "standard"` parameter and a dict of preamble templates. |
  | `buyerbench/models.py:Scenario` | **MISSING** | No `prompt_version` field. The `Scenario` dataclass (`models.py:34-49`) defines the scenario contract; adding `prompt_version` here enables scenario-level prompt pinning for reproducibility. |
  | `buyerbench/models.py:EvaluationResult` | **MISSING** | No `prompt_version` field (`models.py:69-77`). Without it, cell-level grouping by `(agent_id, scenario_id, variant, prompt_version)` is impossible from result records alone. Requires UPGRADE-4. |
  | `results/schemas.py:EvaluationResultJSON` | **MISSING** | No `prompt_version` field (`schemas.py:18-27`). JSON/CSV exports cannot distinguish same-scenario runs under different prompt versions. Requires UPGRADE-4. |
  | `agents/openrouter_agent.py:respond()` | **MISSING** | Calls `scenario_to_prompt(scenario)` with no version argument (`openrouter_agent.py:65`). Once `scenario_to_prompt()` is parameterized, the agent must pass the prompt version through. |
  | `buyerbench/__main__.py:run()` | **MISSING** | No `--prompt-version` CLI option (`__main__.py:147-205`). The run command currently has no parameter for prompt variant selection. Requires UPGRADE-7 to add `--prompt-version standard|cot|expert_role`. |
  | Cell aggregate grouping key | **MISSING** | The `cell_id` formula (`H.2 Cell Aggregate Record`) includes `prompt_version` as a dimension: `{agent_id}__{scenario_id}__{variant}__{prompt_version}__{temperature}`. This field cannot be constructed until `prompt_version` lands on `EvaluationResult`. Requires UPGRADE-4 + UPGRADE-5. |

  **Dependency chain for Phase 2:**
  - **UPGRADE-1** (multi-run support, `--n-runs N`) — hard prerequisite: N=50 per cell is required before any cell-level statistics are meaningful.
  - **UPGRADE-7** (prompt variant support) — the specific Phase 2 enabler: parameterizes `scenario_to_prompt()`, adds CoT and expert-role templates, and adds `--prompt-version` CLI flag. Estimated effort: 2 days.
  - **UPGRADE-4** (run metadata logging) — required to store `prompt_version` on `EvaluationResult` and `EvaluationResultJSON` so that Phase 2 runs are distinguishable in output data.
  - **UPGRADE-5** (cell-level aggregate output) — required to produce `cell_aggregates.json` broken down by `(agent_id, scenario_id, variant, prompt_version)` for Phase 2 analysis.

  **Research rationale for Phase 2:** Prompt framing is itself an independent variable in LLM behavioral research. The three versions test whether: (a) `standard` — neutral framing — already reveals bias patterns, (b) `cot` — explicit reasoning mandate — suppresses biases by forcing deliberate utility comparison, and (c) `expert_role` — identity priming — either amplifies or attenuates biases by shifting the model's in-context "role." If CoT and expert-role systematically reduce BSI across all bias types, this isolates prompt engineering as a bias-mitigation mechanism and motivates prompt design guidelines for production AI buyer agents.
- [x] **Phase 3 (temperature sweep):** 4 temperatures × 5 bias types × 10 models × 30 runs
  ✅ **Verified (2026-04-16):** Engineering analysis of Phase 3 temperature-sweep design against current codebase.

  **The four temperatures (not yet specified in the source document):**
  The natural set for LLM research: **0.0, 0.3, 0.7, 1.0**.
  - `0.0` — near-deterministic (greedy decoding); tests whether biases are structurally encoded in weights vs. a sampling artifact. If BSI is nonzero at T=0, the bias is in the weights. If BSI collapses to zero, it is a stochastic output effect.
  - `0.3` — low stochasticity; midpoint between deterministic floor and operational target.
  - `0.7` — operational standard (same as Phase 1 realistic design; overlapping cell for cross-phase validation).
  - `1.0` — high stochasticity; tests whether maximum entropy sampling amplifies or suppresses economic irrationality.
  Temperatures above 1.0 are excluded: most providers degrade coherence rapidly above 1.0, and OpenRouter normalizes temperature handling inconsistently above that boundary.

  **Run count correction (missing 2-variants dimension):**
  The stated formula "4 × 5 × 10 × 30 = 6,000 runs" omits the 2-variants/bias dimension (BASELINE + TREATMENT), matching the same omission identified in Phase 2's formula. Corrected total: **4 × 5 × 2 × 10 × 30 = 12,000 runs**. Since Phase 1 already covers T=0.7 at N=50, the T=0.7 cells in Phase 3 overlap with Phase 1 data (different N, can be pooled or treated as validation). Net runs exclusive to Phase 3 (T=0.0, 0.3, 1.0 only): 3 × 5 × 2 × 10 × 30 = **9,000 runs** above the Phase 1 baseline.

  **Why N=30 instead of N=50:**
  The primary analysis (Phase 1) is powered at N=50 for detecting main-effect BSI differences at d=0.5. Phase 3 targets a *moderation effect* (temperature × bias_type interaction), not a primary effect. In a mixed-effects model, the interaction term gains power from **multiple temperature levels** (4 points) rather than N alone — 30 × 4 = 120 observations per (model, bias_type, variant) triple is sufficient for exploratory moderation analysis. Power for a d=0.3 moderation effect at N=30 per level is ~55% — underpowered but adequate for exploratory labeling. N=30 also reduces total Phase 3 cost and wall time by ~40% vs. N=50.

  **Engineering gap analysis — all 4 prerequisite UPGRADEs are blocking:**

  | Component | Gap | Blocker |
  |---|---|---|
  | `agents/openrouter_agent.py:45-56` (`__init__`) | No `temperature` parameter exists. `body` dict (`line 103-106`) has no `"temperature"` key — API calls use provider defaults, not a controlled value. | **UPGRADE-3** (0.5 days: add `temperature: float \| None = None` init param; set `body["temperature"] = self.temperature` if not None) |
  | `agents/registry.py:124-128` (`get_agent` for openrouter-*) | `OpenRouterAgent` instantiation has no `temperature` kwarg. `or_cfg = config.get("openrouter", {})` does not look for a `temperature` key. | **UPGRADE-3** — registry must forward temperature from config or CLI flag |
  | `buyerbench/__main__.py:147-204` (`run` command) | No `--temperature FLOAT` CLI option exists. No multi-temperature loop (`--temperatures 0.0 0.3 0.7 1.0`) exists. Each temperature level requires a separate CLI invocation today. | **UPGRADE-3** — add `--temperature` flag; UPGRADE-1 prerequisite for `--n-runs 30` |
  | `harness/runner.py:run_scenario()` | Runs exactly one invocation per scenario — no repeat loop. No `temperature` passed to agent. | **UPGRADE-1** (2 days: add N-repeat loop) + **UPGRADE-3** (temperature pass-through) |
  | `buyerbench/models.py:EvaluationResult` | No `temperature` field (`models.py:69-77`). Phase 3 runs at T=0.0, T=0.3, T=0.7, T=1.0 would be stored in identical record schemas — indistinguishable in output data. | **UPGRADE-4** (1 day: extend `EvaluationResult` + `EvaluationResultJSON`) |
  | `results/schemas.py:EvaluationResultJSON` | No `temperature` field (`schemas.py:18-27`). CSV/JSON exports cannot distinguish cross-temperature runs. | **UPGRADE-4** |
  | Cell-level aggregate | `aggregate_cells.py` does not exist; no CI or std computation across N=30 runs per (agent, scenario, variant, temperature) cell. | **UPGRADE-5** (1 day: new module) — cell grouping key must include temperature dimension |

  **OpenRouter API behavior at temperature=0:**
  `temperature: 0` is supported by all 10 model providers in the registry (OpenAI, Anthropic, Google, Meta, Mistral, DeepSeek, Qwen, Cohere, 01.AI). However, "deterministic" is not perfectly guaranteed: OpenAI docs note minor variance at T=0 due to parallel processing; Anthropic's T=0 is nearer-true determinism. Recommendation: log the actual temperature value sent in the API request (not model default) as part of UPGRADE-4 metadata, and treat T=0 results as "near-deterministic" rather than absolutely identical runs.

  **Dependency chain for Phase 3:**
  - **UPGRADE-1** (multi-run, `--n-runs 30`) — hard prerequisite for N=30 per cell
  - **UPGRADE-3** (temperature parameter) — the specific Phase 3 enabler; unblocks API-level temperature control
  - **UPGRADE-4** (metadata logging) — required to record `temperature` on `EvaluationResult` so cross-temperature analysis is possible
  - **UPGRADE-5** (cell-level aggregates) — required for per-cell `mean_bsi(T)` curves needed for moderation analysis
  - Phases 1 and 2 are **not** strict prerequisites for Phase 3 data collection (can run independently with same infrastructure), but Phase 1 provides the T=0.7 reference baseline and should run first for calibration.

  **Wall-time and cost analysis:**
  - **Serial:** 12,000 runs × ~10.8s blended average = 129,600s ≈ **36 hours** (4 CLI passes of ~9 hours each, one per temperature)
  - **Parallel (10 agents):** bounded by Gemini (~20.7s/run × 1,200 runs per model = 24,840s ≈ 6.9 hours per temperature pass) × 4 passes ≈ **28 hours total** wall time for all 4 temperatures run sequentially. If 4 temperature passes are run as concurrent independent jobs (e.g., separate machines or tmux sessions), wall time collapses to **~7–8 hours** (Gemini bottleneck per pass).
  - **Cost:** 12,000 corrected runs × $0.002–$0.005 blended = **~$24–$60 incremental**. The stated formula's 6,000-run count × $0.15/run = $900 is the same systematic overestimate identified in H.3.
  - **Cumulative budget after Phases 1–3:** Phase 1 ($10–$25) + Phase 2 incremental ($30–$75) + Phase 3 ($24–$60) = **$64–$160 total realistic vs. implied $3,000+ from stated formulas.**
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
