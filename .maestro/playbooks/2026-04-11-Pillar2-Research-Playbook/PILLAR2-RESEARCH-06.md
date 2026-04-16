# PILLAR2-RESEARCH-06 — Python Implementation Plan
## BuyerBench Pillar 2: Economic Rationality & Behavioral Biases in LLM Agents

> **Purpose:** Deliver a concrete Python implementation plan with project structure, data schema, run orchestration, and first working script that defines the experiment grid and metadata.

---

## SECTION L — PYTHON IMPLEMENTATION PLAN

### L.1 Project Structure

- [x] Create directory structure for research analysis layer:
  ```
  research/
  ├── experiments/
  │   ├── __init__.py
  │   ├── grid.py               # Experiment grid definition (models × biases × variants × configs)
  │   ├── manifest.py           # Experiment manifest generation and freezing
  │   ├── run_experiment.py     # Orchestration: generates run plan, calls BuyerBench runner N times
  │   └── schemas.py            # Research-specific data schemas (RunRecord, CellAggregate)
  ├── analysis/
  │   ├── __init__.py
  │   ├── bsi.py                # BSI computation (reconcile with evaluators/pillar2.py)
  │   ├── variance.py           # Variance decomposition (model vs. bias vs. stochastic)
  │   ├── power.py              # Power analysis utilities
  │   ├── regression.py         # Mixed-effects regression wrappers (statsmodels / R bridge)
  │   └── corrections.py       # Multiple comparison corrections (BH, Bonferroni)
  ├── figures/
  │   ├── __init__.py
  │   ├── heatmap.py            # BSI heatmap: model × bias type
  │   ├── variance_plot.py      # Variance decomposition bar chart
  │   ├── capability_scatter.py # P1 score vs. mean BSI scatter
  │   └── distribution_plot.py  # Per-cell BSI distribution violins
  ├── tables/
  │   ├── __init__.py
  │   ├── main_results.py       # Table 1: main BSI results
  │   ├── regression_table.py   # Table 2: regression output (stargazer-style)
  │   └── power_table.py        # Table A1: power analysis
  ├── notebooks/
  │   ├── 01_experiment_design.ipynb   # Define grid, validate, estimate cost
  │   ├── 02_run_analysis.ipynb        # Load results, compute BSI, check data quality
  │   ├── 03_main_results.ipynb        # Main results: figures and tables
  │   ├── 04_robustness.ipynb          # Robustness checks
  │   └── 05_paper_figures.ipynb       # Final publication-ready figures
  └── scripts/
      ├── 00_define_experiment.py      # FIRST SCRIPT (see L.5 below)
      ├── 01_run_realistic_design.sh   # Shell script to run full realistic design
      ├── 02_aggregate_results.py      # Post-run aggregation
      ├── 03_run_regressions.py        # Automated regression pipeline
      └── 04_generate_tables.py        # Generate all paper tables
  ```

### L.2 Dataset Schema (Python Classes)

- [x] Create `research/experiments/schemas.py`:
  ```python
  from dataclasses import dataclass, field
  from typing import Optional
  from datetime import datetime

  @dataclass
  class RunRecord:
      """One LLM invocation — primary unit of observation."""
      run_id: str
      session_id: str
      agent_id: str
      model_family: str
      model_version: str
      scenario_id: str
      bias_category: str
      variant: str
      run_index: int
      temperature: float
      prompt_version: str  # "standard" | "cot" | "expert_role"
      supplier_order_seed: int
      timestamp_utc: datetime
      agent_output_raw: str
      extracted_choice: Optional[str]
      choice_is_correct: bool
      optimal_choice: str
      bsi: float
      optimality_gap: float
      token_count_input: int
      token_count_output: int
      api_cost_usd: float
      error_flag: bool
      error_message: Optional[str]

  @dataclass
  class CellAggregate:
      """Aggregated statistics for one (model, scenario, variant, prompt, temperature) cell."""
      cell_id: str
      agent_id: str
      scenario_id: str
      bias_category: str
      variant: str
      prompt_version: str
      temperature: float
      n_runs: int
      n_valid_runs: int
      mean_bsi: float
      std_bsi: float
      ci_lower_95: float
      ci_upper_95: float
      choice_rate_correct: float
      choice_distribution: dict
      mean_optimality_gap: float
      treatment_effect: Optional[float]  # BSI_treatment - BSI_baseline

  @dataclass
  class ExperimentManifest:
      """Frozen configuration for one experiment run."""
      experiment_id: str
      design_tier: str  # "realistic" | "flagship"
      n_models: int
      n_bias_types: int
      n_variants_per_bias: int
      n_runs_per_cell: int
      temperatures: list[float]
      prompt_versions: list[str]
      total_planned_runs: int
      total_completed_runs: int
      total_api_cost_usd: float
      pre_registration_url: Optional[str]
      git_commit_hash: str
      start_time_utc: datetime
      end_time_utc: Optional[datetime]
  ```

### L.3 Run Orchestration

- [x] Create `research/experiments/run_experiment.py`:
  <!-- Implemented: generate_run_plan, load_completed_run_ids, append_run_record, build_run_record, estimate_cost, run_experiment (--dry-run, --resume), CLI entry point. Tests: tests/test_run_experiment.py (45 tests, all pass). -->
  - Accept `ExperimentManifest` as input
  - Generate full run plan as list of (model, scenario, variant, run_index, temperature, prompt_version, seed)
  - Support `--dry-run` mode: print plan + cost estimate, do not invoke models
  - Support `--resume` mode: skip cells already in output file
  - Call `buyerbench run` for each cell; capture output
  - Write `RunRecord` to append-mode JSONL file in real time (no data loss on crash)
  - After all runs complete: invoke `aggregate_results.py`

### L.4 Reproducibility Plan

- [x] Pin all model versions at experiment start by querying OpenRouter model list and logging exact model IDs
- [x] Seed `supplier_order_seed = hash(run_id) % 2**32` for deterministic supplier ordering
- [x] Store `git_commit_hash = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip()` in manifest
- [x] All intermediate files in `results/experiments/{experiment_id}/`:
  - `manifest.json` — frozen at run start
  - `runs.jsonl` — append-mode run records
  - `cells.json` — aggregated after completion
  - `figures/` — generated plots
  - `tables/` — LaTeX and CSV tables
  <!-- Implemented: research/experiments/manifest.py — get_git_commit_hash, _agent_id_to_openrouter_slug, query_openrouter_model_versions, create_manifest, freeze_manifest, load_manifest. ExperimentManifest.pinned_model_versions field added to schemas.py. Tests: tests/test_manifest.py (47 tests, all pass). -->

### L.5 FIRST SCRIPT — Experiment Grid Definition

- [x] Create `research/scripts/00_define_experiment.py`:
  <!-- Implemented: REALISTIC_DESIGN and FLAGSHIP_DESIGN moved to research/experiments/grid.py (importable module); script imports from grid.py + manifest.py + run_experiment.py; main() writes manifest.json (via freeze_manifest), run_plan.csv, cost_estimate.txt under {output_dir}/{experiment_id}/; supports --design, --output-dir, --no-pin-versions flags; sys.path fix enables direct invocation. Tests: tests/test_define_experiment.py (41 tests, all pass). -->
  ```python
  """
  Script 00: Define Experiment Grid
  ==================================
  Defines the full experiment grid for the Realistic Design (Section F.1).
  Outputs: experiment_manifest.json, run_plan.csv, cost_estimate.txt

  Run: python research/scripts/00_define_experiment.py [--design realistic|flagship]
  """

  import json
  import hashlib
  import subprocess
  from datetime import datetime, timezone
  from itertools import product
  from pathlib import Path

  # ── Grid Definition ──────────────────────────────────────────────────────────

  REALISTIC_DESIGN = {
      "design_tier": "realistic",
      "models": [
          "openrouter-openai-gpt-4o",
          "openrouter-anthropic-claude-3.5-sonnet",
          "openrouter-google-gemini-pro-1.5",
          "openrouter-meta-llama-llama-3.1-405b-instruct",
          "openrouter-mistralai-mistral-large",
          "openrouter-deepseek-deepseek-chat",
          "openrouter-qwen-qwen-2.5-72b-instruct",
          "openrouter-cohere-command-r-plus",
          "openrouter-mistralai-mixtral-8x22b-instruct",
          "openrouter-01-ai-yi-large",
      ],
      "bias_scenarios": {
          "anchoring": {
              "baseline": "p2-01-anchoring-BASELINE",
              "treatment": "p2-01-anchoring-ANCHOR_HIGH",
          },
          "framing": {
              "baseline": "p2-02-framing-FRAMING_GAIN",  # Note: GAIN is baseline reference
              "treatment": "p2-02-framing-FRAMING_LOSS",
          },
          "decoy": {
              "baseline": "p2-03-decoy-BASELINE",
              "treatment": "p2-03-decoy-DECOY",
          },
          "scarcity": {
              "baseline": "p2-04-scarcity-BASELINE",
              "treatment": "p2-04-scarcity-SCARCITY",
          },
          "sunk_cost": {
              "baseline": "p2-05-sunk-cost-BASELINE",
              "treatment": "p2-05-sunk-cost-SUNK_COST",
          },
      },
      "n_runs_per_cell": 50,
      "temperatures": [0.7],          # Primary; 0.0 added as robustness
      "prompt_versions": ["standard"],  # CoT added in flagship
      "cost_per_run_usd": 0.15,        # Approximate; varies by model
  }

  # ── Run Plan Generation ───────────────────────────────────────────────────────

  def generate_run_plan(design: dict) -> list[dict]:
      """Generate list of all individual run specs."""
      runs = []
      run_index_counter = {}

      for model in design["models"]:
          for bias_cat, scenarios in design["bias_scenarios"].items():
              for variant_name, scenario_id in scenarios.items():
                  for temp in design["temperatures"]:
                      for prompt_ver in design["prompt_versions"]:
                          cell_key = f"{model}__{scenario_id}__{temp}__{prompt_ver}"
                          run_index_counter.setdefault(cell_key, 0)

                          for r in range(design["n_runs_per_cell"]):
                              run_index_counter[cell_key] += 1
                              run_id_raw = f"{cell_key}__run{r+1}"
                              run_id = hashlib.sha256(run_id_raw.encode()).hexdigest()[:12]
                              seed = int(hashlib.md5(run_id_raw.encode()).hexdigest(), 16) % 2**32

                              runs.append({
                                  "run_id": run_id,
                                  "agent_id": model,
                                  "scenario_id": scenario_id,
                                  "bias_category": bias_cat,
                                  "variant": variant_name,
                                  "run_index": r + 1,
                                  "temperature": temp,
                                  "prompt_version": prompt_ver,
                                  "supplier_order_seed": seed,
                              })
      return runs

  def estimate_cost(runs: list[dict], cost_per_run: float) -> dict:
      return {
          "n_runs": len(runs),
          "estimated_cost_usd": len(runs) * cost_per_run,
          "runs_per_model": len(runs) // len(REALISTIC_DESIGN["models"]),
          "note": "Cost estimate assumes average $0.15/run; varies by model family.",
      }

  # ── Manifest Generation ───────────────────────────────────────────────────────

  def get_git_hash() -> str:
      try:
          return subprocess.check_output(
              ["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL
          ).decode().strip()
      except Exception:
          return "unknown"

  def build_manifest(design: dict, runs: list[dict]) -> dict:
      now = datetime.now(timezone.utc).isoformat()
      return {
          "experiment_id": f"pillar2-realistic-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}",
          "design_tier": design["design_tier"],
          "n_models": len(design["models"]),
          "n_bias_types": len(design["bias_scenarios"]),
          "n_variants_per_bias": 2,
          "n_runs_per_cell": design["n_runs_per_cell"],
          "temperatures": design["temperatures"],
          "prompt_versions": design["prompt_versions"],
          "total_planned_runs": len(runs),
          "total_completed_runs": 0,
          "total_api_cost_usd": 0.0,
          "pre_registration_url": None,  # Fill before running
          "git_commit_hash": get_git_hash(),
          "created_at_utc": now,
          "start_time_utc": None,  # Set when run actually starts
          "end_time_utc": None,
          "models": design["models"],
          "bias_scenarios": design["bias_scenarios"],
      }

  # ── Main ─────────────────────────────────────────────────────────────────────

  if __name__ == "__main__":
      import argparse
      import csv

      parser = argparse.ArgumentParser()
      parser.add_argument("--design", choices=["realistic", "flagship"], default="realistic")
      parser.add_argument("--output-dir", default="results/experiments/pillar2")
      args = parser.parse_args()

      design = REALISTIC_DESIGN  # Extend for flagship

      runs = generate_run_plan(design)
      cost = estimate_cost(runs, design["cost_per_run_usd"])
      manifest = build_manifest(design, runs)

      out = Path(args.output_dir)
      out.mkdir(parents=True, exist_ok=True)

      with open(out / "manifest.json", "w") as f:
          json.dump(manifest, f, indent=2)
      print(f"Manifest written: {out / 'manifest.json'}")

      with open(out / "run_plan.csv", "w", newline="") as f:
          writer = csv.DictWriter(f, fieldnames=runs[0].keys())
          writer.writeheader()
          writer.writerows(runs)
      print(f"Run plan written: {out / 'run_plan.csv'} ({len(runs)} runs)")

      with open(out / "cost_estimate.txt", "w") as f:
          f.write(json.dumps(cost, indent=2))
      print(f"Cost estimate: ${cost['estimated_cost_usd']:.2f} for {cost['n_runs']} runs")
  ```

### L.6 Regression Templates

- [x] Create `research/analysis/regression.py` with these templates:
  - `run_primary_regression(df)` — mixed-effects model: BSI ~ BiasType + Model + Treatment + BiasType×Model + (1|run)
  - `run_capability_regression(cell_df, p1_scores)` — OLS: mean_BSI ~ P1Score (N=10 models; descriptive only)
  - `run_variance_decomposition(df)` — ANOVA-style: partition SS by model, bias_type, temperature, residual
  - `apply_bh_correction(pvalues, alpha=0.05)` — Benjamini-Hochberg FDR
  - Use `statsmodels.formula.api.mixedlm` for primary regression
  - Bridge to R's `lme4` via `rpy2` for robustness check if available
  <!-- Implemented: research/analysis/regression.py — run_primary_regression (statsmodels MixedLM + pure-Python WLS fallback + optional rpy2/lme4 robustness check), run_capability_regression (statsmodels OLS + fallback), run_variance_decomposition (pandas, includes Temperature factor), apply_bh_correction (consistent with results/stats_pipeline.py). All functions operate on pandas DataFrames of run-level records. Tests: tests/test_research_regression.py (63 tests, all pass). -->

### L.7 Figure Templates

- [x] **Figure 1 — BSI Heatmap:**
  - X-axis: model names (sorted by capability tier)
  - Y-axis: bias types
  - Color: mean BSI (0=blue, 1=red)
  - Annotation: cell value ± SD
  - Add human benchmark line (if available) as separate row

- [x] **Figure 2 — Capability Scatter:**
  - X-axis: Pillar 1 score (capability)
  - Y-axis: mean BSI across bias types
  - One point per model; label with model name
  - Add OLS regression line + 95% CI band
  - Annotation: "N=10 models; interpret as descriptive only"

- [x] **Figure 3 — Within-Cell Variance Distribution:**
  - Violin plots: one per (bias_type × variant)
  - Y-axis: BSI per run
  - Shows that single-run results are unreliable

- [x] **Figure 4 — Treatment Effects by Bias Type:**
  - Forest plot: point estimate (treatment_effect) + 95% CI per (bias_type × model)
  - Sorted by effect size within bias type
  - Reference line at 0 (no effect)
  <!-- Implemented: research/figures/heatmap.py (plot_bsi_heatmap), research/figures/capability_scatter.py (plot_capability_scatter), research/figures/distribution_plot.py (plot_bsi_distributions), research/figures/variance_plot.py (plot_variance_decomposition + plot_treatment_effects). All functions accept pandas DataFrames, return matplotlib.figure.Figure objects, use optional matplotlib/numpy imports with graceful ImportError, and include full column-name overrides. variance_plot.py implements both the variance decomposition bar chart (original stub spec) and the forest plot (L.7 Figure 4 spec). Tests: tests/test_research_figures.py (53 tests, all pass). Full suite: 1588 passed. -->

### L.8 Output Tables

- [ ] **Table 1 — Main Results:** Mean BSI × (10 models × 5 bias types); bold cells where BSI significantly > 0 (BH-corrected)
- [ ] **Table 2 — Regression Results:** Mixed-effects estimates; standard format (coefficient, SE, t-stat, p-value); significance stars
- [ ] **Table 3 — Variance Decomposition:** SS and % of variance for each factor (model, bias_type, stochastic)
- [ ] **Table A1 — Power Analysis:** Reproduce G.8 table in paper-ready format
- [ ] Use `pandas.to_latex()` + manual formatting; export as `.tex` files
