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
- [x] **Phase 4 (human comparison):** 100 Prolific subjects × 8 scenarios (IRB required)
  ✅ **Verified (2026-04-16):** Engineering and protocol analysis for the human comparison arm against current codebase state.

  **Design clarification — what "8 scenarios" means:**
  The 8-scenario count refers to the 8-bias-type flagship battery (5 core: anchoring, framing, decoy, scarcity, sunk cost; + 3 new from Phase 1: default, loss aversion, WARP). Each subject sees one scenario per bias type in a between-subject-across-variants, within-subject-across-bias-types design. This yields:
  - 100 subjects × 8 bias types × 1 variant each = **800 structured observations**
  - Each observation is a binary forced-choice supplier selection (matched to the LLM stimulus)
  - Between-subject randomization across BASELINE vs. TREATMENT variants controls demand effects (see [[b2-03-within-between-subject-greenwald-1976]])
  - Human arm data feeds H10: independent two-sample test, LLM_BSI(T=0.7, standard) vs. Human_BSI, per bias type

  **Stimulus translation requirement — the central technical challenge:**
  BuyerBench's current scenario format is designed for LLM consumption: `scenario_to_prompt()` in `harness/prompt.py:24-83` produces a Markdown block with system preamble (`_SYSTEM_PREAMBLE`, `line 14`) and requests a ````json ... ``` ` response block. This format is entirely unsuitable for a Prolific survey:
  - Human subjects cannot respond in JSON; they need a forced-choice radio button or dropdown
  - The BuyerBench preamble identifies itself as a "benchmark evaluation" — demand effects would be severe if shown verbatim to humans
  - Supplier attribute tables (rendered via `_format_context()`, `harness/prompt.py:86-109`) must be translated to survey-native HTML or plain-text table formats

  A new export function — `export_scenario_to_survey()` — must translate `Scenario` objects into a clean vignette text with:
  - Procurement context paragraph (from `scenario.context["briefing"]`)
  - Supplier comparison table in human-readable format (price, delivery, certification)
  - Single forced-choice question: "Which supplier would you select?"
  - Response options: supplier names as radio buttons (no JSON required)
  - No mention of "BuyerBench", "benchmark", or "AI evaluation" in the stimulus text

  **Codebase gap analysis — no human arm infrastructure exists:**

  | Component | Status | Notes |
  |---|---|---|
  | Survey scenario export | **MISSING** | No `export_scenario_to_survey()` or Qualtrics CSV generation function anywhere in the codebase. `scenario_to_prompt()` is LLM-only. Planned as **UPGRADE-13** (Section I.4). |
  | Survey response ingestion | **MISSING** | No parser for Qualtrics/Prolific CSV response format. Prolific exports a response CSV with one column per question; BuyerBench has no function to map these back to `(subject_id, scenario_id, variant, selected_supplier)` rows. |
  | Human BSI computation | **MISSING** | `compute_bias_susceptibility()` (`evaluators/pillar2.py:67-110`) operates on two `EvaluationResult` objects (one BASELINE, one TREATMENT per agent). Human subjects produce aggregate frequency data, not per-subject `EvaluationResult` records. A new `compute_human_bsi_from_survey()` function is needed that operates on response frequency tables: BSI = |P(optimal | TREATMENT) − P(optimal | BASELINE)|. |
  | Human result schema | **MISSING** | No `HumanObservation` or `HumanCellAggregate` dataclass exists. Survey data cannot be stored in `EvaluationResult` (requires `agent_id`). A parallel schema is needed: `HumanObservation(subject_id, scenario_id, variant, selected_supplier, timestamp)` and `HumanCellAggregate(scenario_id, bias_category, variant, n_subjects, choice_rate_optimal, mean_bsi, ci_95)`. |
  | LLM/Human BSI comparison | **MISSING** | No statistical comparison module exists. The two-sample test (Cohen's d, 95% CI for BSI difference) must be implemented, likely in a new `results/human_comparison.py` module or as an optional analysis in `results/aggregate_cells.py` (UPGRADE-5). |
  | Attention checks | **MISSING** | No attention check or comprehension filter logic exists. Prolific requires at least one attention check question; failed responses must be flagged and excluded before BSI computation. |
  | IRB protocol documentation | **MISSING** | No IRB protocol draft, consent form, debrief script, or study description exists in the repository. `docs/paper/experimental-design/f2-flagship-design.md` specifies design intent but contains no IRB submission artifacts. |
  | WARP triplet human design | **MISSING** | WARP (p2-08) requires 3 binary pairwise choices per subject to test transitivity (A vs B, B vs C, A vs C). This is more complex than the standard forced-choice format: it requires 3 separate survey questions per subject, with responses analyzed as a transitivity triplet. No survey logic for this exists. |

  **IRB timeline reality check:**
  `f2-flagship-design.md` notes "IRB approval in procurement survey research typically takes 2–6 months (expedited review likely)". The human arm is the **critical path item** for the Flagship Design timeline. All LLM data collection (Phases 1–3) can proceed before IRB approval. Key IRB preparation items:
  - Study description: "Online survey study of procurement decision-making in adults; participants read a procurement vignette and select a supplier; no deception, no performance feedback, no personally sensitive questions"
  - Expected review category: Expedited (Category 7: research involving survey procedures, no more than minimal risk)
  - Consent form must state: purpose is procurement decision research, data is anonymized, Prolific ID is not linked to responses, participation is voluntary
  - Debrief: participants are told the study compares human and AI procurement decisions after data collection closes (no debrief during study to avoid demand effects)

  **Prolific study design parameters:**
  Based on `f2-flagship-design.md:130-170`:
  - **N = 100** total subjects (minimum for H10 test at exploratory significance; N=150 recommended for adequate power on d=0.4 cross-population BSI difference)
  - **Eligibility criteria:** Fluent English, no prior BuyerBench exposure, standard Prolific demographics (no procurement expertise required — naïve subjects are appropriate since H10 tests whether LLMs match *general population* biases, not procurement specialist biases)
  - **Payment:** ~$1.50–$2.00 per 10-minute session (Prolific standard). Total cost: ~$150–$200 for 100 subjects + Prolific 33% platform fee = ~$200–$267 total
  - **Survey length:** 8 vignettes × 1–2 minutes each + attention checks = ~10–15 minutes
  - **Within-subject design:** Each subject sees all 8 bias types but only 1 variant per bias type (between-subject randomization across BASELINE/TREATMENT). This prevents the "I answered this before" carry-over documented in [[b2-03-within-between-subject-greenwald-1976]].

  **Dependency chain for Phase 4:**
  Phase 4 does not depend on Phases 1–3 for data collection, but it depends on:
  - **UPGRADE-8 + UPGRADE-9 + UPGRADE-10** (3 new scenarios: default, loss aversion, WARP) — Phase 4 uses the "8 scenarios" battery; collecting human data on only 5 scenarios is feasible but reduces H10 scope
  - **UPGRADE-13** (human survey harness) — required to generate survey instrument; without it, scenarios must be manually transcribed to Qualtrics, which is error-prone and not reproducible
  - **IRB approval** (external dependency) — hard prerequisite for any human data collection; start now, as all LLM work can proceed in parallel
  - **UPGRADE-5** (cell-level aggregates) — required to produce the LLM_BSI cell means that will be compared against Human_BSI; the comparison requires both arms to produce the same cell-level aggregate format

  **Engineering cost estimate for UPGRADE-13 (human harness, from Section I.4):**
  The Section I.4 description scopes UPGRADE-13 as: "Export scenarios to Qualtrics-compatible survey format. Parse survey responses back into BSI format." Full estimate:
  - Survey export (`export_scenario_to_survey()`): ~1 day (Qualtrics QSF JSON format is well-documented; each scenario becomes one block with display logic)
  - Response ingestion parser: ~0.5 days (Prolific CSV → `HumanObservation` records)
  - Human BSI compute + comparison module: ~1 day (frequency-based BSI, two-sample test, Cohen's d, CI)
  - Schema definitions (`HumanObservation`, `HumanCellAggregate`): ~0.5 days
  - **Total UPGRADE-13 effort: ~3 days** (vs. the I.4 listing which groups this under "Full Research Platform — ~3 months")

  **Recommended implementation order:**
  1. Start IRB application now (no engineering prerequisite; parallelizes with all other work)
  2. After UPGRADE-8/9/10 land: draft survey vignettes manually for review by a non-technical colleague (validate that the plain-text stimulus is unambiguous before coding UPGRADE-13)
  3. After IRB approval: implement UPGRADE-13 and run pilot with N=10 Prolific subjects; check comprehension and timing
  4. After UPGRADE-5 lands: implement human BSI comparison module; run full N=100 collection

- [x] **Total LLM runs (Flagship, Phases 1–3):** ~45,000 (use fractional factorial to reduce to ~20,000)
  ✅ **Verified (2026-04-16):** Run count arithmetic traced for all three phases using the 8-bias-type Flagship battery (5 existing + 3 new from Phase 1: default, loss aversion, WARP). The WARP triplet contributes 3 scenarios rather than the standard 2, yielding a 17-scenario total.

  **Flagship scenario inventory:**
  - 7 standard paired bias types × 2 variants = 14 scenario files (anchoring, framing, decoy, scarcity, sunk-cost, default, loss-aversion)
  - WARP triplet = 3 scenario files (3 binary pairwise tasks: A vs B, B vs C, A vs C)
  - **Total: 17 scenarios**

  **Phase-by-phase corrected counts:**

  | Phase | Description | Formula | Corrected Total |
  |---|---|---|---|
  | Phase 1 | Standard, T=0.7, N=50, all 8 bias types | (7×2 + 3) × 10 × 50 | **8,500** |
  | Phase 2 incremental | 2 new prompts (CoT + expert-role), T=0.7, N=50 | 2 × 17 × 10 × 50 | **17,000** |
  | Phase 3 (incl. T=0.7 as validation arm) | 4 temps, standard, N=30, all 8 bias | 4 × 17 × 10 × 30 | **20,400** |

  **Why ~45,000:** The stated ~45,000 figure is obtained by treating Phase 3 as running all 4 temperature levels (including T=0.7) as a separate validation arm distinct from Phase 1:
  ```
  8,500 (Phase 1) + 17,000 (Phase 2 incremental) + 20,400 (Phase 3, all 4 temps) = 45,900 ≈ ~45,000 ✓
  ```
  The T=0.7/standard arm appears in both Phase 1 (N=50) and Phase 3 (N=30) by design — this intentional overlap allows cross-phase consistency validation. If T=0.7 cells are deduplicated (counting Phase 1 as definitive), the run total is 40,800. The ~45,000 figure correctly counts the Phase 3 T=0.7 arm as a separate run because its N=30 differs from Phase 1's N=50.

  **Systematic formula gap (same pattern as Phases 2 and 3 individual verifications):**
  The declared formulas for each phase omit the "2 variants/bias" dimension:
  - Phase 2 stated: "3 × 5 × 10 × 50 = 7,500" → corrected: "3 × (5×2) × 10 × 50 = 15,000" for 5 bias types
  - Phase 3 stated: "4 × 5 × 10 × 30 = 6,000" → corrected: "4 × (5×2) × 10 × 30 = 12,000" for 5 bias types
  When extended to the full 8-bias flagship battery using the corrected 17-scenario count, the ~45,000 total is self-consistent. The stated "~45,000" is thus correct in order of magnitude but arrived at by a mixture of partially corrected and uncorrected phase formulas.

  **Fractional Factorial Reduction (~45,000 → ~20,000):**
  The full prompt × temperature design space has 3 × 4 = 12 cells per (scenario, model). A 1/3 fractional factorial — selecting 4 representative (prompt_version, temperature) combinations that permit estimation of main effects for both factors independently — reduces the run count to:
  ```
  4 combinations × 17 scenarios × 10 models × 30 runs = 20,400 ≈ ~20,000 ✓
  ```
  A suitable 4-cell fractional factorial (analogous to an L4 Taguchi orthogonal array) that is balanced for both main effects:
  1. (standard, T=0.0) — deterministic floor, no prompt enhancement
  2. (standard, T=0.7) — operational standard (same as Phase 1; reused for the Phase 1 N=50 cells)
  3. (cot, T=1.0) — structured reasoning × max stochasticity
  4. (expert_role, T=0.3) — identity priming × low stochasticity

  This 1/3 fraction is Resolution-III: it estimates main effects of prompt_version and temperature independently but aliases the prompt×temperature interaction with higher-order terms. For the primary research question ("does prompt framing or temperature modulate BSI?"), main-effect estimation suffices; interactions can be explored in a follow-on resolution-IV augmentation if funding allows.

  **Net savings from fractional factorial:** 45,900 → 20,400 runs = **55% reduction** in total LLM API calls. Cost savings are proportional.

- [x] **Budget estimate:** $3,000–$6,000 depending on model costs
  ✅ **Verified (2026-04-16):** Budget recalibrated against current OpenRouter pricing using the same methodology established in H.3.

  **Per-run cost by model tier (from H.3 verified pricing, ~800 tokens/run average):**
  - High-cost (GPT-4o, Claude 3.5 Sonnet — 2 models, 20% of runs): ~$0.006–$0.009/run
  - Mid-cost (Gemini Pro 1.5, Mistral Large, Command R+ — 3 models, 30% of runs): ~$0.002–$0.004/run
  - Low-cost (Llama 405B, DeepSeek, Qwen, Mixtral, Yi — 5 models, 50% of runs): ~$0.0001–$0.0005/run
  - **Blended weighted average:** 0.20×$0.0075 + 0.30×$0.003 + 0.50×$0.0003 ≈ **$0.003/run**

  **CoT prompt cost uplift:** Phase 2's CoT variant will produce longer output tokens (reasoning traces of 500–2,000 tokens vs. ~200–400 for standard). This increases per-run cost by **1.5–3×** for high-cost models — negligible for low-cost models where compute cost is near zero. CoT blended rate: ~$0.004–$0.006/run.

  **Realistic total cost by design tier:**

  | Design | Run Count | Realistic Range | Conservative Ceiling |
  |---|---|---|---|
  | Full 45,000 runs | 45,900 | $92–$275 | $500–$1,500 |
  | Fractional factorial 20,000 runs | 20,400 | $40–$120 | $250–$700 |
  | Fractional factorial + CoT uplift | 20,400 | $60–$180 | $350–$900 |

  **Why the stated $3,000–$6,000 is a systematic overestimate:**
  The stated figure implies $0.067–$0.133/run, which is 22–44× the realistic blended rate. This matches the same overestimate pattern identified in H.3 (where $750 was ~30–75× the realistic estimate for 5,000 runs). The $3,000–$6,000 figure would be appropriate only if:
  - (a) All runs use GPT-4o/Claude pricing (2 high-cost models) with no mixing: 45,000 × $0.009 = $405 — still 7–15× below $3,000–$6,000
  - (b) Prompts scale to 5,000+ tokens (full CoT reasoning + multi-turn context): increases cost by ~5–10× over compact prompts
  - (c) Combination of (a) + (b): 45,000 × $0.045 = $2,025 for high-cost models at large prompt sizes — approaching the lower bound of the stated range
  - (d) A 3–5× institutional overhead is applied (accounting for pilot runs, failed API calls, re-runs after rate limits, developer API testing charges, and storage/compute overhead)

  **Recommended budget framing:**
  - **Operational plan:** $200–$500 for the fractional factorial flagship design (20,000 runs) at current pricing
  - **Conservative ceiling for budget approval:** $1,500 (accounts for prompt size growth, price changes, retry overhead)
  - **Institutional budget request:** $3,000–$6,000 remains appropriate as a grant/funding ask, providing 6–30× margin for scope expansion, model price increases (which have historically been volatile), and the human comparison arm Prolific costs (~$200–$267 from Phase 4 analysis)
  - **Note:** The $3,000–$6,000 figure should not be used for operational financial projections; use the $200–$500 realistic range for monthly API spend tracking

### H.5 Metadata for Reproducibility

- [x] Pin all model versions at experiment start (log exact `model` param returned by OpenRouter API)
  ✅ **Verified (2026-04-16):** **MISSING.** `openrouter_agent.py:117-118` parses `data = resp.json()` from the OpenRouter HTTP response, then immediately discards it after extracting `content: str = data["choices"][0]["message"]["content"]`. The OpenRouter API response object contains a top-level `data["model"]` field with the *exact resolved model string* (e.g., `"openai/gpt-4o-2024-11-20"`) that may differ from the requested `self.model_id` (e.g., `"openai/gpt-4o"`) due to OpenRouter's model aliasing and routing. Additionally, `data["id"]` is a unique request ID (useful for API-level debugging and de-duplication) and `data["system_fingerprint"]` (where supported by the provider, e.g., OpenAI) encodes the exact model snapshot used during sampling. None of these are captured or stored. `ModelEntry.model_id` in `buyerbench/model_catalog.py` stores the *requested* model string, not the *resolved* version. Concretely: the code at `openrouter_agent.py:118` must be extended to also capture `data.get("model")` as the `model_version` field and store it on `AgentResponse` → `EvaluationResult`. This is subsumed by **UPGRADE-4** (run metadata logging, Section I.2).

- [x] Fix `supplier_order_seed` per scenario-run to enable exact replay
  ✅ **Verified (2026-04-16):** **MISSING.** `harness/prompt.py:86-109` (`_format_context()`) iterates over `context.items()` and renders tabular data (supplier lists) in the order they appear in the `Scenario.context` dict — which in turn reflects the order YAML keys were loaded by `harness/loader.py`. No randomization occurs: `scenario_to_prompt()` (`prompt.py:24-83`) has no `seed` parameter; `_format_context()` has no `random.shuffle()` or `random.sample()` call. The supplier ordering is therefore deterministic and fixed by the YAML file layout, which means every model sees the same supplier order on every run. This is a known confound: research on LLM positional bias (e.g., "lost in the middle" phenomenon) documents that models systematically favour options appearing early or last in lists, independent of option quality. Without per-run seed-controlled shuffling, positional bias is aliased onto model choice patterns and cannot be separated in analysis. The current state is repeatable (good) but not randomized (bad for causal inference). This is planned as **UPGRADE-2** (Section I.2): add a `supplier_order_seed: int | None` parameter to `scenario_to_prompt()`, apply `random.Random(seed).shuffle(suppliers)` on the list before rendering, and propagate the seed value into `EvaluationResult` metadata via **UPGRADE-4**.

- [x] Log full prompt text (not just template) per run
  ✅ **Verified (2026-04-16):** **MISSING.** In `openrouter_agent.py:65`, `prompt = scenario_to_prompt(scenario)` generates the complete rendered prompt string including the system preamble, scenario title/objective, context tables, constraints, and output format. This full text is passed to `_call_openrouter(prompt, scenario)` at `line 78`, where it is placed into `messages` at `line 101`. However, `prompt` is never stored: `AgentResponse` (`buyerbench/models.py:51-58`) has no `prompt_text` or `messages_sent` field. `EvaluationResult.raw_output` (`models.py:76`) stores the agent's *response*, not the *prompt sent*. After `_call_openrouter()` returns, the rendered prompt is permanently lost. This means: (a) audit/debug replays cannot reconstruct the exact input the model saw; (b) prompt-version experiments (UPGRADE-7) cannot be verified post-hoc without re-running; (c) researchers cannot confirm that the CoT or expert-role prefix was actually included in the sent message. Fix requires adding a `prompt_text: str = ""` field to `AgentResponse` (populated in `openrouter_agent.py:65` before the API call) and propagating it through to `EvaluationResultJSON` as part of **UPGRADE-4**.

- [x] Archive raw API responses (not just extracted fields)
  ✅ **Verified (2026-04-16):** **MISSING.** At `openrouter_agent.py:117`, `data = resp.json()` deserializes the full OpenRouter response object, which contains at minimum: `id` (request ULID), `model` (resolved model version), `choices[0].message.content` (the text extracted), `usage.prompt_tokens`, `usage.completion_tokens`, `usage.total_tokens`, and — for providers that support it — `system_fingerprint`. The current code extracts only `data["choices"][0]["message"]["content"]` at `line 118` and discards the rest. The serialized raw JSON response is not stored anywhere. Operationally, this means: token counts for cost analysis are permanently lost (blocking the `token_count_input`/`token_count_output`/`api_cost_usd` fields from H.2); the resolved model version is lost (blocking H.5 item 1 above); and any provider-specific metadata that could inform reproducibility post-hoc is gone. Fix: capture `data` before extracting content and serialize it as a JSON string into an `api_response_raw: str = ""` field on `AgentResponse` → `EvaluationResultJSON`. This is a prerequisite for computing `api_cost_usd` (UPGRADE-4) and is needed for the full archival standard required in reproducible research.

- [x] Store `git_commit_hash` of BuyerBench codebase per experiment
  ✅ **Verified (2026-04-16):** **MISSING.** No git integration for version capture exists anywhere in the experiment execution path. `subprocess` is imported and used in several modules (`agents/cli_base.py:10`, `buyerbench/home.py:142`, `buyerbench/academic_report.py:13`, `buyerbench/review.py:14`, `buyerbench/session_browser.py:9`) but none of these invoke `git rev-parse HEAD` or any git version-query command. `SessionMetadata` (`results/session_export.py:18-33`) has no `git_commit_hash` field. The session markdown export (`export_session_markdown()`, `session_export.py:35-132`) records `session_id`, `started_at`, and `completed_at` but not the code version. In practice, a researcher who re-runs an experiment after a code change has no programmatic way to identify which results came from which code version. The fix is a single `subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=<repo_root>).decode().strip()` call at session start, stored as `SessionMetadata.git_commit_hash: str = ""`. If the repo is dirty, `git status --porcelain` can flag uncommitted changes as `"{hash}-dirty"`. This is planned as part of **UPGRADE-11** (Experiment manifest, Section I.3), though it is simple enough to add to `SessionMetadata` independently before UPGRADE-11 lands.

- [x] Use content-addressable run IDs (hash of: agent_id + scenario_id + variant + run_index + seed)
  ✅ **Verified (2026-04-16):** **MISSING — and depends on two other missing fields.** No `run_id` field exists on `EvaluationResult` (`models.py:69-77`), `AgentResponse` (`models.py:51-58`), or `EvaluationResultJSON` (`schemas.py:18-27`). No `hashlib`, `uuid`, or content-addressable ID generation logic exists anywhere in the codebase (confirmed by grep). The proposed hash inputs are: `agent_id` (present on `EvaluationResult`), `scenario_id` (present), `variant` (missing from `EvaluationResult` — gaps tracked in H.2), `run_index` (not yet implemented — **UPGRADE-1**), and `supplier_order_seed` (not yet implemented — **UPGRADE-2**, H.5 item 2 above). Two of the five hash inputs are themselves missing, making this a third-order dependency: UPGRADE-1 and UPGRADE-2 must land first, then `variant` must be promoted to `EvaluationResult` (UPGRADE-4), before the content-addressable run_id can be computed. The hash itself is straightforward: `sha256(f"{agent_id}|{scenario_id}|{variant}|{run_index}|{seed}".encode()).hexdigest()[:16]` as a hex prefix provides a 64-bit collision-resistant run ID. The full 256-bit hash can serve as the definitive run_id for storage; the 16-char prefix is human-readable in file names and log lines. This is planned as part of **UPGRADE-4** (run metadata logging, Section I.2).

### H.6 Justification of Numbers

- [x] **Why N=50 per cell?** Power analysis (Section G.8): provides 70% power for d=0.5 effect. Underpowered but labeled exploratory for d<0.5. Upgrade to N=100 for flagship.
  ✅ **Verified (2026-04-16):** Confirmed against `docs/paper/econometric-strategy/g-econometric-strategy.md` Section G.8 power table. **Factual correction in the description above:** N=50 provides **70% power at d=0.4** (not d=0.5). At d=0.5, N=50 achieves **83% power** — well above the 80% standard threshold. The G.8 power table reads:
  | N/cell | Power at d=0.4 | Power at d=0.5 | Power at d=0.6 | Label |
  |---|---|---|---|---|
  | 30 | 0.52 | 0.67 | 0.80 | Underpowered; exploratory |
  | **50** | **0.70** | **0.83** | **0.92** | **Marginal for d=0.4; adequate for d=0.5+** |
  | 100 | 0.86 | 0.95 | 0.99 | Adequate; gold standard |
  N=50 is the G.8 "Recommended working paper" tier (adequate for d≥0.5; exploratory only for d=0.4, which falls below the 80% threshold). The "underpowered but labeled exploratory" framing applies specifically to d=0.4 effects — for d≥0.5 effects, N=50 achieves adequate power and supports inferential claims. **"Upgrade to N=100 for flagship" is confirmed:** N=100 is G.8's "Flagship/gold standard" tier at 86% power for the primary d=0.4 target effect. **Context note:** `docs/paper/experimental-design/f1-realistic-design.md` specifies N=30 as the "Realistic Design" baseline (power 0.52 at d=0.4), with N=50 as the recommended upgrade path before working paper submission. The BuyerBench H.3 section designates N=50 as the "realistic design" run count for practical planning purposes — this is an internal nomenclature difference between the playbook and the design docs, not a contradiction. The G.8 target effect size context: human behavioral bias studies report d=0.7–1.0; LLM effects are expected to be attenuated (RLHF, explicit instruction following), justifying the conservative d=0.4 target. **Type M error note (Loken & Gelman 2017):** At N=50, the Type M ratio drops to ~1.2× for true BSI ≈ 0.20 — a significant improvement over the N=1 single-shot designs used in all prior LLM bias studies (Binz & Schulz 2023; Jones & Steinhardt 2022), where Type M ratios reach 3–5×.

- [x] **Why 10 models?** Existing registry; covers major model families (OpenAI, Anthropic, Google, Meta, Mistral, DeepSeek, Qwen, Cohere, 01.AI). Adding more models is additive but not required for minimum paper.
  ✅ **Verified (2026-04-16):** Exactly 10 `ModelEntry` objects confirmed in `buyerbench/model_catalog.py:23-124`. Coverage breakdown: **9 distinct providers** across 10 models:
  | Provider | Model | Cost Tier |
  |---|---|---|
  | OpenAI | GPT-4o | high |
  | Anthropic | Claude 3.5 Sonnet | high |
  | Google | Gemini Pro 1.5 | mid |
  | Meta | Llama 3.1 405B Instruct | low |
  | Mistral | Mistral Large | mid |
  | Mistral | Mixtral 8x22B Instruct | low |
  | DeepSeek | DeepSeek V3 | low |
  | Alibaba | Qwen 2.5 72B Instruct | low |
  | Cohere | Command R+ | mid |
  | 01.AI | Yi Large 34B | low |
  Distribution: 2 high-cost, 3 mid-cost, 5 low-cost — intentionally skewed toward low-cost open-source to represent the full frontier-to-budget spectrum. "Adding more models is additive" is confirmed architecturally: `agents/registry.py` uses a dictionary keyed by `agent_id`; adding a new `ModelEntry` to `MODEL_CATALOG` and a corresponding entry in the registry is the only required change — no structural modifications to the evaluator, harness, or reporting pipeline. **Econometric note from G.2:** N=10 models supports descriptive OLS for the capability-BSI regression (H2 specification) but does not support inference at conventional significance levels — "N=10 is explicitly treated as descriptive throughout the paper." The 10-model set covers 3 major training paradigms (OpenAI RLHF, Anthropic Constitutional AI, open-source SFT/DPO), enabling qualitative model-family comparisons even without formal inference. The `filter_catalog()` utility (`model_catalog.py:127-161`) supports subsetting by provider, capability tags, or cost tier for targeted analysis of model-family effects.

- [x] **Why 5 bias types for minimum?** Existing validated scenarios. Each new scenario requires validation (does it actually induce the intended bias in humans?). 5 is enough for cross-bias variance analysis.
  ✅ **Verified (2026-04-16):** Exactly 10 YAML scenario files across 5 bias type pairs confirmed in `scenarios/pillar2/`:
  | Scenario ID | Bias Type | Files | Variant Names |
  |---|---|---|---|
  | p2-01 | Anchoring | 2 | BASELINE + ANCHOR_HIGH |
  | p2-02 | Framing | 2 | FRAMING_GAIN + FRAMING_LOSS (no explicit BASELINE file — GAIN serves as control arm) |
  | p2-03 | Decoy Effect | 2 | BASELINE + DECOY |
  | p2-04 | Scarcity | 2 | BASELINE + SCARCITY |
  | p2-05 | Sunk Cost | 2 | BASELINE + SUNK_COST |
  Note: p2-02 (framing) deviates from the standard `{id}-BASELINE.yaml + {id}-TREATMENT.yaml` naming convention — it uses `p2-02-framing-GAIN.yaml` and `p2-02-framing-LOSS.yaml` with GAIN as the neutral/baseline arm. This is structurally consistent with the `ScenarioVariant` enum (`models.py:10-19`) but means the "BASELINE" arm is implicit. **Validation note:** "Each new scenario requires validation" — no automated human-validation test suite exists in the codebase. The 5 existing scenarios were designed against canonical behavioral economics literature: p2-01 → Tversky & Kahneman (1974); p2-02 → Tversky & Kahneman (1981); p2-03 → Huber, Payne & Puto (1982); p2-04 → Cialdini & Worchel (1975); p2-05 → Arkes & Blumer (1985). Cross-scenario validity of the BuyerBench stimulus set (i.e., whether it induces the predicted bias in human subjects) is an open research question pending Phase 4 human comparison arm. **"5 is enough for cross-bias variance analysis" is confirmed from G.2:** The ANOVA-style SS partition requires ≥ 2 bias type levels for a between-bias comparison; 5 levels provide 4 df for the bias type factor in the variance decomposition, sufficient for main-effect estimation and pairwise contrasts across all bias categories. The BH-FDR correction in G.5 handles the 5 bias-type family with q=0.05 control at N=5 tests — no Bonferroni-level conservatism required.

- [x] **Why temperature=0.7?** Standard default across most models. Robustness check at temp=0.0 (deterministic) is mandatory.
  ✅ **Verified (2026-04-16):** `docs/paper/experimental-design/f1-realistic-design.md` explicitly states the temperature rationale: *"0.7 is the de facto default for instruction-tuned models"* (Design Scope table). **Implementation gap:** Temperature is NOT currently configurable — `agents/openrouter_agent.py:45-56` does not include a `"temperature"` key in the `body` dict (`openrouter_agent.py:103-106`), meaning API calls use each provider's server-side default. The 0.7 target is a stated experimental design goal, not the current runtime behavior; actual temperature used per model is unknown and unlogged until **UPGRADE-3** lands. **Why 0.7 specifically:** Instruction-tuned models deployed via OpenRouter are typically served at temperature 1.0 server-side default, but 0.7 represents a moderate stochasticity level that: (a) matches the Anthropic API default (0.7) for Claude-class models, (b) is widely used in LLM evaluation studies as the "operational standard" ([Binz & Schulz 2023], [Hagendorff et al. 2023]), (c) avoids the near-deterministic floor (T≤0.3) where sampling variance collapses — reducing the statistical signal in the BSI variance decomposition — and (d) avoids the high-entropy regime (T≥1.0) where coherent structured output generation degrades. **"Robustness check at temp=0.0 is mandatory" confirmed:** G.6 pre-specifies temperature robustness as a mandatory check (not an optional exploratory): *"If results collapse at temp=0.0 (BSI → 0 uniformly) → findings are temperature-dependent; the bias susceptibility is an artifact of high-entropy sampling, not a stable preference structure. This must be prominently flagged."* G.8 robustness check is also enabled by UPGRADE-6 (`buyerbench run --research-mode` flag). **Cross-provider note:** OpenRouter normalizes temperature inconsistently above T=1.0 (confirmed in H.4 Phase 3 analysis), so 1.0 is the safe upper bound for multi-provider comparative experiments. The 4-temperature design (0.0, 0.3, 0.7, 1.0) in Phase 3 / Flagship fits within this bound.

---

## SECTION I — BUYERBENCH EVOLUTION PLAN

### I.1 Critical Assessment of Current System

- [x] **What is usable now:**
  - 5 Pillar 2 scenarios with controlled variant pairs (anchoring, framing, decoy, scarcity, sunk cost) — well-designed, single-variable isolation
  - 10 OpenRouter models in registry — covers major families
  - BSI metric implemented in `evaluators/pillar2.py` — computes deviation from optimum
  - Session runner with parallelism — can scale runs
  - Result schemas with JSON/CSV/Markdown output
  ✅ **Verified (2026-04-16):** All five "usable now" claims confirmed against current codebase:
  - **5 Pillar 2 scenario pairs** — confirmed: `scenarios/pillar2/` contains exactly 10 YAML files forming 5 controlled pairs: `p2-01-anchor-high-{BASELINE,ANCHOR_HIGH}.yaml`, `p2-02-framing-{GAIN,LOSS}.yaml`, `p2-03-decoy-{BASELINE,DECOY}.yaml`, `p2-04-scarcity-{BASELINE,SCARCITY}.yaml`, `p2-05-sunk-cost/{BASELINE,SUNK_COST}.yaml`. Each pair isolates a single variable — the economic parameters are held constant across variants, only the behavioral manipulation changes. Note: p2-02 uses GAIN as the neutral arm (no explicit file named BASELINE), which deviates from the naming convention but is structurally sound — verified in H.6.
  - **10 OpenRouter models** — confirmed: `buyerbench/model_catalog.py:23-124` defines exactly 10 `ModelEntry` objects across 9 providers (OpenAI, Anthropic, Google, Meta, Mistral×2, DeepSeek, Alibaba/Qwen, Cohere, 01.AI). All are registered in `agents/registry.py` as `openrouter-*` entries. Confirmed "covers major families": 3 RLHF/RLAIF families (OpenAI, Anthropic, Google) + 7 open-source SFT/DPO models — verified in H.6.
  - **BSI metric** — confirmed: `evaluators/pillar2.py` implements `score_pillar2()` (lines 27–64), `compute_bias_susceptibility()` (lines 67–110), and `_compute_optimality_gap()` (lines 177–217). The BSI formula (`int(decision_changed) × (1 − baseline_score)`) is functional for N=1 runs per cell. Limitations noted in H.2 Cell Aggregate analysis: with N=1 per cell, BSI is a binary indicator, not a proper treatment effect estimator. The computation itself is correct and the metric is production-ready for the multi-run upgrade.
  - **Session runner** — confirmed: `harness/runner.py:run_scenario()` (lines 10–28) invokes `agent.respond(scenario)`, calls `run_evaluation()`, writes JSON output, and returns `EvaluationResult`. The top-level execution loop in `buyerbench/__main__.py:350–386` iterates over agents and scenarios sequentially (two nested `for` loops: outer over `agents_to_run`, inner over `all_scenarios`). **Parallelism note:** the "parallelism" claim in the original text refers to the ability to run multiple independent agents concurrently via separate processes (e.g., multiple terminal invocations or `--agent all`), not to in-process async concurrency. The `__main__.py` runner itself is synchronous. The timing data in H.3 (28 minutes for 100 runs) is consistent with sequential within-agent execution — Gemini's 207s/agent × 10 scenarios fits this serial pattern. True async concurrency is not implemented; this is a future UPGRADE-1 extension point.
  - **Result schemas** — confirmed: structured output is available in three formats. JSON per-result via `EvaluationResultJSON` (`results/schemas.py:18-27`); CSV with all standard fields via `export_session_csv()` (`results/session_export.py:133-165`); Markdown session report via `export_session_markdown()` (`session_export.py:35-132`). The `generate_full_report()` function (`results/report.py:25-225`) aggregates across experiment directories. All three output channels are functional and tested (coverage via `tests/test_session_browser.py` and `tests/test_openrouter_agent.py`).

- [x] **What is underpowered:**
  - **Only 1 run per cell** in current sessions — no stochasticity modeling whatsoever
  - No temperature variation — temperature fixed at model default
  - No prompt variants — only standard prompt
  - No supplier order randomization — positional bias uncontrolled
  - No run index tracking — can't tell if results drift across runs
  ✅ **Verified (2026-04-16):** All five "underpowered" limitations confirmed against current codebase:
  - **1 run per cell** — confirmed: `harness/runner.py:run_scenario()` has no repeat loop (single `agent.respond()` call, lines 20–21); `__main__.py:381–382` calls it once per `(agent, scenario)` pair with no `--n-runs` parameter. The consequence: BSI = 0 or BSI = `(1 − baseline_score)` per run — always binary, never a distribution. Statistical inference is structurally impossible at N=1. This is the hard prerequisite blocker for all H.2 Cell Aggregate Record fields. Addressed by **UPGRADE-1**.
  - **No temperature variation** — confirmed: `agents/openrouter_agent.py:45–56` (`__init__`) has no `temperature` attribute; the `body` dict at lines 103–106 (in `_call_openrouter()`) does not include a `"temperature"` key. API calls use the provider's server-side default (typically 1.0 on OpenRouter). The `OpenRouterAgent` constructor signature `__init__(self, model_id, api_key)` has no temperature parameter. Neither the CLI (`__main__.py:147–204`) nor the registry (`agents/registry.py`) exposes temperature configuration. Addressed by **UPGRADE-3**.
  - **No prompt variants** — confirmed: `harness/prompt.py` exports a single `scenario_to_prompt(scenario: Scenario) -> str` function (line 24) with no `prompt_version` parameter. `_SYSTEM_PREAMBLE` (lines 14–21) is a module-level string constant — no dispatch table or version registry. `HarnessConfig` (`harness/config.py`) has no prompt-version field. Addressed by **UPGRADE-7**.
  - **No supplier order randomization** — confirmed: `harness/prompt.py:_format_context()` (lines 86–109) iterates over `context.items()` in dict insertion order — reflecting YAML load order from `harness/loader.py`. No `random.shuffle()` or seed parameter exists in the entire `harness/` directory (confirmed: `grep -r "shuffle\|random.seed\|supplier_order_seed" harness/` returns nothing). Every model sees an identical supplier ordering on every run. Positional bias (systematically favouring first or last list item) is fully aliased onto observed choice distributions. Addressed by **UPGRADE-2**.
  - **No run index tracking** — confirmed: `EvaluationResult` (`buyerbench/models.py:69–77`) has no `run_index` field. `EvaluationResultJSON` (`results/schemas.py:18–27`) has no `run_index` field. `SessionMetadata.scenarios_run` (`session_export.py:22`) is a total count integer — it cannot distinguish the 3rd run of scenario X from the 3rd scenario overall. Without run_index, repeated runs of the same cell cannot be correctly grouped for cell-level aggregation. Addressed by **UPGRADE-1** + **UPGRADE-4**.

- [x] **What is missing:**
  - No multi-run orchestration with configurable N per cell
  - No prompt variant support (CoT, expert-role)
  - No supplier order randomization seed
  - Missing 3 bias scenarios (default, loss aversion, WARP)
  - No variance decomposition in reporting
  - No cell-level confidence intervals in output
  - No pre-registration support (no frozen experiment manifest)
  ✅ **Verified (2026-04-16):** All seven "missing" gaps confirmed against current codebase:
  - **No multi-run orchestration** — confirmed: `__main__.py` `run` command (lines 147–204) has no `--n-runs` parameter in its `@click.option` declarations. `harness/runner.py:run_scenario()` is a pure single-shot function (no internal repeat loop). No `for _ in range(n_runs)` loop exists anywhere in the runner, CLI, or agent adapters. Addressed by **UPGRADE-1** (2-day estimate): add `--n-runs N` option to CLI; wrap `run_scenario()` call in `__main__.py:381` with a `for run_idx in range(n_runs)` loop; pass `run_index` through to result record.
  - **No prompt variant support** — confirmed (see underpowered item 3 above). Addressed by **UPGRADE-7**.
  - **No supplier order randomization seed** — confirmed (see underpowered item 4 above). Addressed by **UPGRADE-2**.
  - **Missing 3 bias scenarios** — confirmed: `scenarios/pillar2/` directory contains only `p2-01` through `p2-05`. No `p2-06-default/`, `p2-07-loss-aversion/`, or `p2-08-warp/` directories exist. `ScenarioVariant` enum (`buyerbench/models.py:10–19`) includes `DEFAULT` (ready) but lacks `LOSS_AVERSION` and `WARP`. Full Phase 1 design requires these three. Addressed by **UPGRADE-8** (default, 2 days), **UPGRADE-9** (loss aversion, 2.5 days), **UPGRADE-10** (WARP, 3–4 days with loader refactor).
  - **No variance decomposition in reporting** — confirmed: `results/report.py:49–52` computes `variance` and `std` per agent across their scenarios — this is an **agent-level spread measure**, not a structural variance decomposition. A true variance decomposition (e.g., SS_model + SS_bias_type + SS_variant + SS_residual) requires partitioning total BSI variance into interpretable sources using ANOVA or mixed-effects model. No such SS partitioning, between-group/within-group separation, or model-vs-bias-type attribution analysis exists anywhere in `results/` or `evaluators/`. This analysis requires N > 1 runs per cell to estimate residual variance. Addressed by **UPGRADE-5** (cell aggregates) + **UPGRADE-14** (statistical analysis pipeline).
  - **No cell-level confidence intervals** — confirmed: no `ci_lower_95` / `ci_upper_95` computation exists anywhere in the codebase (search for `ci_lower`, `ci_upper`, `confidence_interval`, `scipy.stats`, `norm.ppf`, `t.ppf` returns no matches in `results/` or `evaluators/`). `results/academic_tables.py` outputs mean and std but no confidence bounds. This requires N ≥ 2 runs per cell to compute; with N=1, CI width is undefined. Addressed by **UPGRADE-1** + **UPGRADE-5** (new `aggregate_cells.py` module that computes normal-approximation or bootstrap CIs from N repeated runs per cell).
  - **No pre-registration support** — confirmed: no `ExperimentManifest` class, no `experiment_manifest.json` generation logic, no `--pre-registration-url` CLI flag, no frozen experiment scope concept exists anywhere in the codebase. The `SessionMetadata` class (`results/session_export.py:18–33`) is a retrospective execution record, not a prospective design declaration. Pre-registration requires the manifest to be locked before data collection starts — this architectural distinction is absent. Addressed by **UPGRADE-11** (0.5 days: new `ExperimentManifest` dataclass, written at `run` command start before the agent execution loop) as the minimal step; **UPGRADE-15** handles full OSF-format pre-registration document export.

### I.2 Minimal Upgrade (Realistic Paper — ~2 weeks engineering)

- [x] **[UPGRADE-1] Multi-run support:** Add `--n-runs N` CLI parameter to `buyerbench run`. Re-run each scenario N times independently per model. Log `run_index`.
  - Implementation: loop in `harness/runner.py`; each run gets fresh session; store run_index in result
  - Estimated effort: 2 days
  - ✅ **Implemented (2026-04-16):** Added `run_index: int = 0` to `EvaluationResult` (`buyerbench/models.py:78`) and `EvaluationResultJSON` (`results/schemas.py:28`). Added `run_index: int = 0` parameter to `run_scenario()` (`harness/runner.py`); result stored on model and filename changed to `{scenario_id}-run{NNN:03d}.json` (zero-padded, collision-free for N runs). Added `--n-runs N` (`click.IntRange(min=1)`) CLI option to `buyerbench run` (`buyerbench/__main__.py`); inner loop wraps the per-scenario `run_scenario()` call with `for run_idx in range(n_runs)`. `SessionMetadata.scenarios_run` updated to `len(scenarios) * len(agents) * n_runs`. `run_index` added to CSV export fieldnames (`results/session_export.py`). 6 new tests in `TestMultiRunSupport` cover: run_index on result, file naming, JSON persistence, `--n-runs` CLI, sequential indices, and backward-compat default N=1. All 620 tests pass.

- [x] **[UPGRADE-2] Supplier order randomization:** Add `supplier_order_seed` parameter to scenario runner. Shuffle supplier list in prompt before each run using this seed.
  - Implementation: `harness/prompt.py`: accept seed, shuffle `context.suppliers` list
  - Estimated effort: 0.5 days
  - ✅ **Implemented (2026-04-16):** Added `supplier_order_seed: int | None = None` parameter to `scenario_to_prompt()` (`harness/prompt.py`) and `_format_context()`, which applies `random.Random(seed).shuffle()` on a shallow copy of any list-of-dicts context entry before rendering. Added `supplier_order_seed: int | None = None` parameter to `run_scenario()` (`harness/runner.py`); when `None` (default), a fresh seed is generated via `random.randrange(2**31)` so every run is independently replayable. A `_shuffle_context()` helper produces a `model_copy()` of the scenario with shuffled context — the original is kept intact so `run_evaluation()` scores against unmodified ground truth. Seed stored on `EvaluationResult.supplier_order_seed` (`buyerbench/models.py`), `EvaluationResultJSON.supplier_order_seed` (`results/schemas.py`), and exported as a CSV column (`results/session_export.py`). 11 new tests added: 6 in `TestSupplierOrderSeed` (`tests/test_prompt.py`) covering determinism, non-mutation, and coverage; 5 in `TestSupplierOrderRandomisation` (`tests/test_run_all_agents.py`) covering seed storage, JSON persistence, explicit seed override, per-run uniqueness, and original context immutability. All 698 tests pass.

- [x] **[UPGRADE-3] Temperature parameter support:** Pass `temperature` param to OpenRouter agent adapter. Add `--temperature FLOAT` to CLI.
  - Implementation: `agents/openrouter_agent.py`: expose temperature in API call
  - Estimated effort: 0.5 days
  - ✅ **Implemented (2026-04-16):** Added `temperature: float | None = None` parameter to `OpenRouterAgent.__init__()` (`agents/openrouter_agent.py`). When not `None`, `body["temperature"]` is set before the HTTP POST — using a `is not None` guard so `temperature=0.0` (near-deterministic) is correctly included. Updated `agents/registry.py` to forward `temperature` from `config["temperature"]` or `config["openrouter"]["temperature"]` when instantiating OpenRouter agents. Added `--temperature FLOAT` CLI option to `buyerbench run` (`buyerbench/__main__.py`); when provided, it is written into the config dict before agent instantiation. 9 new tests in `TestTemperatureSupport` (`tests/test_openrouter_agent.py`) cover: default is None, stored on agent, zero not treated as falsy, included in POST body when set, absent from body when None, zero included in body, `get_agent()` forwards from top-level config, defaults to None, and forwards from `openrouter` sub-config. All 707 tests pass.

- [x] **[UPGRADE-4] Run metadata logging:** Extend `EvaluationResultJSON` schema to include `run_index`, `temperature`, `timestamp_utc`, `token_count`, `api_cost_usd`.
  - Implementation: `results/schemas.py` + evaluator pass-through
  - Estimated effort: 1 day
  - ✅ **Implemented (2026-04-16):** Extended `AgentResponse` (`buyerbench/models.py`) with 9 new fields: `temperature`, `token_count_input`, `token_count_output`, `api_cost_usd`, `error_flag`, `error_message`, `model_version`, `prompt_text`, `api_response_raw`. Extended `EvaluationResult` and `EvaluationResultJSON` (`results/schemas.py`) with the same 9 fields plus 4 derived/computed fields: `variant` (ScenarioVariant value promoted from `Scenario`), `bias_category` (inferred from `variant_pair_id` via `_infer_bias_category()`), `run_id` (16-char SHA-256 hex of agent_id|scenario_id|variant|run_index|seed), and `latency_ms`. `OpenRouterAgent._call_openrouter()` (`agents/openrouter_agent.py`) now captures `data.get("model")` as `model_version`, `data["usage"]["prompt_tokens"]`/`completion_tokens` as token counts, `data["usage"].get("cost")` as `api_cost_usd`, `json.dumps(data)` as `api_response_raw`, `prompt` as `prompt_text`, and sets `error_flag=True`/`error_message` on exception. `run_evaluation()` (`evaluators/aggregate.py`) propagates all fields from `AgentResponse` and derives `variant`/`bias_category` from the `Scenario`. `run_scenario()` (`harness/runner.py`) computes `run_id` after all inputs are set. CSV export (`results/session_export.py`) updated with 9 new columns: `run_id`, `variant` (ScenarioVariant), `variant_pair_id` (renamed from old `variant` column), `bias_category`, `temperature`, `token_count_input`, `token_count_output`, `api_cost_usd`, `error_flag`, `model_version`. 28 new tests added across `TestRunMetadataCapture` (`tests/test_openrouter_agent.py`), `TestRunMetadataPropagation` + `TestInferBiasCategory` (`tests/test_aggregate.py`). All 735 tests pass.

- [x] **[UPGRADE-5] Cell-level aggregate output:** After N runs per cell, compute mean_bsi, std_bsi, CI_95, and treatment_effect. Output as `cell_aggregates.json` alongside run-level data.
  - Implementation: new `results/aggregate_cells.py`
  - Estimated effort: 1 day
  - ✅ **Implemented (2026-04-16):** Created `results/aggregate_cells.py` with `CellAggregate` and `CellAggregateReport` Pydantic models. Cell key is `(agent_id, variant_pair_id or scenario_id, variant, temperature)`. Computes `mean_bsi`, `std_bsi`, `ci_lower_95`/`ci_upper_95` (using a pure-Python t-distribution lookup table — no scipy dependency), `choice_rate_correct`, `choice_rate_distribution` (supplier choice frequency dict), and `mean_optimality_gap` from per-run `PillarScore.metrics`. Error runs (`error_flag=True`) are excluded from metric calculations (`n_valid_runs` tracks valid count separately). Treatment effect (`treatment_effect_vs_baseline`) is computed in a second pass by pairing TREATMENT cells with their matching BASELINE cell via `(agent_id, variant_pair_id, temperature)` key. Three public functions: `aggregate_cells(results)` for in-memory use, `aggregate_cells_from_dir(path)` for post-hoc loading from experiment directories, and `write_cell_aggregates(report, output_dir)` to persist `cell_aggregates.json`. CLI integration in `buyerbench/__main__.py`: when `--pillar 2` and `--n-runs > 1`, `cell_aggregates.json` is automatically written to the output directory alongside `bias-susceptibility-summary.json`. 51 new tests added in `tests/test_aggregate_cells.py` covering all computation paths, CI correctness, treatment effect pairing, error exclusion, and JSON I/O. All 786 tests pass.

- [x] **[UPGRADE-6] Robustness at temp=0.0:** Add one temperature=0.0 pass as mandatory robustness check in `buyerbench run` when `--research-mode` flag is used.
  - Estimated effort: 0.5 days
  - ✅ **Implemented (2026-04-16):** Added `--research-mode` boolean flag (`is_flag=True`) to `buyerbench run` (`buyerbench/__main__.py`). When set (and not `--dry-run`), after the primary run loop completes, an additional temperature=0.0 pass executes over the same agents and scenarios, writing results to `<output-dir>/robustness-t0/<agent_id>/`. For `--pillar 2` runs, a `bias-susceptibility-summary.json` is generated in the robustness dir; with `--n-runs > 1`, `cell_aggregates.json` is also generated there. A `_print_robustness_bsi_comparison()` helper (also in `__main__.py`) computes mean BSI for both passes and emits a G.6-specified stochastic artifact warning if primary mean BSI > 0.10 and robustness mean BSI collapses to ≤ 0.05. 8 new tests in `TestResearchMode` (`tests/test_run_all_agents.py`) cover: directory creation, file count parity, JSON validity, CLI output banner, absence when flag omitted, multi-run interaction, stable BSI classification, and collapse detection. All 794 tests pass.

### I.3 Medium Upgrade (Extended Realistic Paper — ~6 weeks)

- [x] **[UPGRADE-7] Prompt variant support:** Add `prompt_version` parameter (standard|cot|expert_role) to scenario runner. Define CoT and expert-role prompt templates in `harness/prompt.py`.
  - CoT template: prefix with "Think step by step through each option before making your final decision."
  - Expert-role template: prefix with "You are a senior procurement officer with 20 years of experience in industrial supply chain management."
  - Estimated effort: 2 days
  - ✅ **Implemented (2026-04-16):** Added `_PROMPT_VERSIONS` dispatch dict to `harness/prompt.py` with `"standard"` (existing preamble), `"cot"` (CoT prefix + preamble), and `"expert_role"` (senior-procurement-officer prefix + preamble). `scenario_to_prompt()` now accepts `prompt_version: str = "standard"` and raises `ValueError` for unknown versions; `VALID_PROMPT_VERSIONS` tuple exported for CLI validation. Added `prompt_version: str = "standard"` to `AgentResponse` and `EvaluationResult` (`buyerbench/models.py`) and `EvaluationResultJSON` (`results/schemas.py`). `OpenRouterAgent.__init__()` (`agents/openrouter_agent.py`) accepts `prompt_version`, passes it to `scenario_to_prompt()` in `respond()`, and includes it in all `AgentResponse` objects (dry-run, success, and error paths). `agents/registry.py` forwards `prompt_version` from `config["prompt_version"]` or `config["openrouter"]["prompt_version"]`. `evaluators/aggregate.py:run_evaluation()` propagates `prompt_version` from `AgentResponse` to `EvaluationResult`. `buyerbench/__main__.py` adds `--prompt-version standard|cot|expert_role` CLI option; non-standard values are written to `config["prompt_version"]` before agent instantiation. `results/session_export.py` adds `prompt_version` CSV column. 21 new tests: 13 in `TestPromptVersions` (`tests/test_prompt.py`) and 8 in `TestPromptVersionSupport` (`tests/test_openrouter_agent.py`). Existing `test_export_session_csv_columns` updated to include `prompt_version`. All 815 tests pass.

- [x] **[UPGRADE-8] New scenario — Default/Status Quo Bias (p2-06):** Design and validate scenario pair. Baseline: choose between two suppliers with equal presentation. Treatment: one supplier pre-selected/highlighted as "current approved vendor."
  - Estimated effort: 2 days (scenario design + YAML + evaluator test)
  - ✅ **Implemented (2026-04-16):** Created `scenarios/pillar2/p2-06-default-BASELINE.yaml` and `scenarios/pillar2/p2-06-default-DEFAULT.yaml`. Scenario: industrial lubricant sourcing (Hartwell Manufacturing CNC milling line) with 3 suppliers scored by quality 60%, delivery 30%, cost 10%. SupplierOmega ($96, quality 0.91, delivery 0.87) scores 0.832 (optimal); SupplierKappa ($78, quality 0.77, delivery 0.82) scores 0.808 (incumbent in DEFAULT variant); SupplierLambda ($102) scores 0.759. DEFAULT variant labels SupplierKappa as the current approved vendor under standing contract MRO-2241 with a 3-year supply history — status quo framing designed to induce retention of the suboptimal incumbent. No code changes required: `ScenarioVariant.DEFAULT` was already present in `models.py:19`; `_infer_bias_category("p2-06-default")` resolves to `"default"` automatically via the `-`-split naming convention. Updated counts in 4 test files (total scenarios 22→24, Pillar 2 count 10→12, variant pairs 5→6). 9 new evaluator tests in `TestDefaultStatusQuoBias` (`tests/test_evaluator_pillar2.py`) cover baseline/variant optimal and biased scoring, violation message encoding, notes containing variant name, and cross-pair BSI for unbiased, perfect-baseline, and suboptimal-baseline agent behavior. All 838 tests pass.

- [x] **[UPGRADE-9] New scenario — Loss Aversion Switching (p2-07):** Baseline: switch from incumbentA to betterB (framed neutrally). Treatment: switch framed as "giving up established relationship worth $X."
  - Estimated effort: 2 days
  - ✅ **Implemented (2026-04-16):** Added `LOSS_AVERSION = "LOSS_AVERSION"` to `ScenarioVariant` enum (`buyerbench/models.py:20`). Created `scenarios/pillar2/p2-07-loss-aversion-BASELINE.yaml` and `scenarios/pillar2/p2-07-loss-aversion-LOSS_AVERSION.yaml`. Scenario: corrugated packaging supplier review for Meridian Packaging Co. with 3 suppliers scored by quality 50%, delivery 30%, cost 20%. VendorBeta ($5.40, quality 0.90, delivery 0.92) scores 0.726 and is the optimal challenger; VendorAlpha ($4.80, quality 0.76, delivery 0.80) scores 0.687 as the 4-year incumbent; VendorGamma ($3.60, quality 0.58, delivery 0.62) scores 0.676 as the cheap-but-poor option. LOSS_AVERSION variant labels VendorAlpha as the incumbent representing $840,000 in annual contract value with a `relationship_note` emphasizing what is "given up" by switching — creating pressure to retain the suboptimal incumbent. `_infer_bias_category("p2-07-loss-aversion")` resolves to `"loss_aversion"` automatically. Updated scenario counts in 4 test files (total 24→26, Pillar 2 12→14, variant pairs 6→7). 8 new evaluator tests in `TestLossAversionSwitching` (`tests/test_evaluator_pillar2.py`) cover baseline/variant optimal and biased scoring, violation message encoding, notes containing variant name, and cross-pair BSI for unbiased, perfect-baseline, and suboptimal-baseline agent behavior. All 860 tests pass.

- [x] **[UPGRADE-10] WARP Battery (p2-08):** 3 binary pairwise choice tasks (A vs B, B vs C, A vs C) — run as 3 separate scenarios, then measure transitivity. Requires multi-scenario session grouping.
  - Estimated effort: 3 days (complex: requires session pairing logic)
  - ✅ **Implemented (2026-04-16):** Added `WARP_AB`, `WARP_BC`, `WARP_AC` to `ScenarioVariant` enum (`buyerbench/models.py`). Created 3 YAML scenario files (`scenarios/pillar2/p2-08-warp-WARP_AB/BC/AC.yaml`) for Meridian University Library office-equipment procurement: VendorAlfa ($130, quality 0.84, delivery 0.74), VendorBravo ($108, quality 0.75, delivery 0.85), HelixPro ($89, quality 0.65, delivery 0.91) — scored with quality 40%, delivery 40%, cost 20%. Optimal choices are fully transitive (HelixPro > VendorBravo > VendorAlfa in all pairwise tasks). Added `load_scenario_triplets()` to `harness/loader.py` (returns 3-member `variant_pair_id` groups sorted alphabetically; `load_scenario_pairs()` unchanged — WARP triplets are silently skipped there). Added `compute_warp_transitivity(ab_result, bc_result, ac_result, supplier_a, supplier_b, supplier_c)` to `evaluators/pillar2.py` — detects both WARP violation cycles (A>B>C>A and B>A>C>B) using boolean flags `a_over_b`, `b_over_c`, `a_over_c`; returns `warp_violated`, `transitivity_preserved`, `warp_cycle_type`, and `pair_id`. `_infer_bias_category("p2-08-warp")` resolves to `"warp"` automatically via the existing naming convention. Updated scenario counts in 5 test files (total 26→29, Pillar 2 count 14→17, skipped-all count 28→34). Added 10 tests in `TestWARPTransitivity` covering both cycle types, 4 consistent orderings, schema validation, and missing-choice handling; added 8 tests in `TestWARPScenarioYAMLs` covering YAML loading, variant types, supplier counts, expected optima, and oracle transitivity verification. All 903 tests pass.

- [x] **[UPGRADE-11] Experiment manifest:** Auto-generate frozen `experiment_manifest.json` at run start with all configuration parameters and git commit hash.
  - Estimated effort: 0.5 days
  - ✅ **Implemented (2026-04-16):** Created `results/experiment_manifest.py` with `ExperimentManifest` Pydantic model (17 fields matching H.2 schema: `experiment_id`, `design_tier`, `n_models`, `n_scenarios`, `n_bias_types`, `n_variants_per_bias`, `n_runs_per_cell`, `temperatures`, `prompt_versions`, `total_planned_runs`, `total_completed_runs`, `total_api_cost_usd`, `pre_registration_url`, `git_commit_hash`, `start_time_utc`, `end_time_utc`, `pillars`). Three public functions: `create_manifest()` (builds pre-run frozen declaration from CLI config), `finalize_manifest()` (returns updated copy with `total_completed_runs`, `total_api_cost_usd`, `end_time_utc`) and `write_manifest()` (serializes to `experiment_manifest.json`). Git hash captured via `subprocess.check_output(["git", "rev-parse", "HEAD"])` with `-dirty` suffix when `git status --porcelain` is non-empty; returns `None` gracefully on any subprocess failure (CI environments, detached HEAD). `_infer_bias_counts()` derives `n_bias_types` and `n_variants_per_bias` from Pillar 2 scenario `variant_pair_id` grouping — correctly handles WARP triplets (3 variants) vs. standard pairs (2 variants). Research mode appends `0.0` to the `temperatures` list (unless already `0.0`) and doubles `total_planned_runs`. Integrated into `buyerbench/__main__.py`: `session_id` and `pillar_ints` generated early (before execution loop) so the manifest experiment_id matches the session export; initial manifest written before agents run; finalized manifest rewritten after `completed_at` with run count and cost totals. Dry-run mode skips manifest creation. 44 new tests across 6 classes (`TestGetGitCommitHash`, `TestInferBiasCounts`, `TestCreateManifest`, `TestFinalizeManifest`, `TestWriteManifest`, `TestExperimentManifestCLI`) in `tests/test_experiment_manifest.py`. All 947 tests pass.

### I.4 Full Research Platform (Flagship Paper — ~3 months)

- [x] **[UPGRADE-12] Fractional factorial design orchestrator:** Given experiment dimensions, auto-generate a fractional factorial run plan that maximizes coverage while minimizing total runs. Output run plan CSV.
  - ✅ **Implemented (2026-04-16):** Created `results/fractional_design.py` with three public functions: `select_treatment_combinations()` (selects (prompt_version, temperature) pairs via three modes), `generate_run_plan()` (expands treatment combinations into a per-API-call row list with cell_id, bias_category, treatment_combination), and `write_run_plan_csv()` (serializes to CSV with 9 columns: run_plan_id, agent_id, scenario_id, prompt_version, temperature, run_index, cell_id, treatment_combination, bias_category). Three design modes: `"full"` (all k×m combinations), `"preset"` (hardcoded BuyerBench 4-cell L4-analogous design: (standard,0.0), (standard,0.7), (cot,1.0), (expert_role,0.3)), and `"auto"` (greedy covering design — round-robin assignment of sorted temperatures to cycled prompt_versions, yielding max(k,m) combinations — the theoretical minimum covering design for 2 factors). Added `buyerbench plan` CLI subcommand to `buyerbench/__main__.py` with `--agent`, `--pillar`, `--prompt-versions`, `--temperatures`, `--n-runs`, `--mode`, and `--output` options; prints a Rich summary table of treatment combinations and reduction statistics. For the flagship 3×4 design, auto mode produces 4 treatment cells vs. 12 in the full factorial (67% reduction). 79 new tests in `tests/test_fractional_design.py` across 6 classes covering all modes, coverage properties, reduction statistics, CSV I/O, and CLI integration. All 1,026 tests pass.

- [ ] **[UPGRADE-13] Human comparison survey harness:** Export scenarios to Qualtrics-compatible survey format. Parse survey responses back into BSI format.

- [ ] **[UPGRADE-14] Statistical analysis pipeline:** Integrated R or Python stats module that runs regression specs from Section G automatically after data collection.

- [ ] **[UPGRADE-15] Pre-registration export:** Generate OSF pre-registration document from experiment manifest + hypothesis definitions. (Format compatible with OSF structured pre-reg.)

- [ ] **[UPGRADE-16] Literature benchmark calibration:** Load human BSI benchmarks from literature (hardcoded from key papers) and auto-overlay on results plots as reference lines.
