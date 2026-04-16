# PILLAR2-RESEARCH-03 — Final Designs (Flagship + Realistic) & Econometric Strategy
## BuyerBench Pillar 2: Economic Rationality & Behavioral Biases in LLM Agents

> **Purpose:** Commit to two concrete experimental designs (ambitious + achievable), then specify the full econometric strategy including estimands, regression equations, and power analysis.

---

## SECTION F — FINAL DESIGN (DUAL TRACK)

### F.1 REALISTIC WORKING PAPER DESIGN

> ✅ *Completed 2026-04-16:* Full Realistic Working Paper Design specification written at `docs/paper/experimental-design/f1-realistic-design.md`. Covers scope (5 bias types, 10 models, N=30/cell, T=0.7, between-subject, standard prompts), statistical summary (3,000 runs, $450, 8–12 hours wall time), three controls (session independence, supplier-order randomization, run metadata logging), primary outputs (BSI per cell, choice correctness binary, output text, run metadata), a design capabilities table (what it allows vs. cannot support), the recommended N=50 upgrade path, and BibTeX cross-references to 6 supporting papers.

**Target journal:** Experimental Economics or Journal of Economic Psychology  
**Claim level:** "We provide the first multi-model, stochasticity-aware measurement of behavioral bias susceptibility in LLM agents operating in economically structured procurement tasks."

**Scope:**
- [x] 5 bias types (existing BuyerBench Pillar 2: anchoring, framing, decoy, scarcity, sunk cost)
- [x] 10 models (existing OpenRouter registry)
- [x] 30 runs per (bias_type × variant × model) cell
- [x] Fixed temperature = 0.7; secondary robustness at temp = 0.0 and 1.0
- [x] Between-subject design (no model sees both baseline AND variant in same session)
- [x] Standard prompts only (no CoT variants)

**Total runs:** 5 bias × 2 variants × 10 models × 30 runs = 3,000 agent invocations  
**Estimated API cost:** $450 (at ~$0.15/run average)  
**Estimated wall time:** 8–12 hours with parallelism

**Controls:**
- [x] Session independence: fresh session per run (no conversation history carryover)
- [x] Prompt randomization: randomize supplier ordering within each prompt to control positional bias
- [x] Run metadata: timestamp, temperature, token count, model version logged

**Primary outputs:**
- [x] BSI per (model, bias_type, variant)
- [x] Choice correctness binary per run
- [x] Output text for qualitative analysis

**What this design allows:**
- Main effects of bias_type and model on BSI
- Inter-model variance decomposition
- Within-cell (stochastic) variance quantification
- Basic hypothesis tests for H1, H3, H5, H7, H9

**What this design CANNOT support:**
- Causal claims about *why* biases appear
- Human comparison
- Interaction effects between prompt and bias type
- Generalizability beyond procurement domain

---

### F.2 FLAGSHIP PAPER DESIGN

> ✅ *Completed 2026-04-16:* Full Flagship Paper Design specification written at `docs/paper/experimental-design/f2-flagship-design.md`. Covers all 6 additional components beyond the Realistic Design: (1) three prompt versions (standard, CoT, expert-role) with demand-effect caution notes; (2) three new bias types (p2-06 status quo, p2-07 loss aversion, WARP battery) with full scenario specifications; (3) three anchor levels for dose-response H4 testing; (4) human comparison arm design (Prolific, N=100, IRB timeline, incentive justification via Camerer & Hogarth); (5) 4-level temperature sweep (0.0, 0.3, 0.7, 1.0); (6) N=50/cell upgrade. Full factorial count (96,000 runs full / 20,000 fractional), cost estimates ($3,000–$14,400), identification logic table for each effect, and engineering requirements checklist.

**Target journal:** JEBO or Experimental Economics (with human arm: QJE-adjacent)  
**Claim level:** "LLM bias susceptibility is heterogeneous across model capability, bias type, and prompt structure; high-capability models show lower susceptibility on average but exhibit distinctive vulnerability profiles."

**Additional components beyond Realistic Design:**

- [x] **3 prompt versions:** (1) standard, (2) chain-of-thought instruction, (3) expert-role framing ("You are a senior procurement officer with 20 years of experience")
- [x] **3 bias types added:** default/status quo (p2-06), loss aversion switching (p2-07), WARP battery (3-way transitivity)
- [x] **3 anchor levels for anchoring scenarios:** low ($60), baseline ($75), high ($91) — enables dose-response curve
- [x] **Human comparison arm:** 100 subjects on Prolific; same scenarios; standard survey format
- [x] **Temperature sweep:** runs at temp ∈ {0.0, 0.3, 0.7, 1.0} to map stochasticity surface
- [x] **N=50 per cell** (vs. 30 in realistic design)

**Total runs (LLM):** 8 bias × 2 variants × 10 models × 3 prompts × 3 temperatures × 50 runs ≈ 72,000 (stratified sample feasible at 20,000 with fractional factorial)  
**Human subjects:** 100 × 10 scenarios = 1,000 observations  
**Estimated LLM cost (full):** $3,000; (fractional factorial): $1,200  
**Engineering requirement:** Prompt variant support in harness; multi-temperature sweep; WARP multi-turn session support

**Identification logic:**
- Bias effect: Compare BSI(variant) vs BSI(baseline) within model — within-model paired comparison
- Model effect: Compare BSI across models within bias type — between-model comparison
- Prompt effect: 3-level within-model comparison (controlling bias type and model)
- Temperature effect: Variance decomposition across 4 temperature levels
- Human comparison: Independent two-sample test per bias type: LLM_BSI vs. Human_BSI

---

## SECTION G — ECONOMETRIC STRATEGY

> ✅ *Completed 2026-04-16:* Full econometric strategy written at `docs/paper/econometric-strategy/g-econometric-strategy.md`. All 9 subsections (G.1–G.9) are specified in a single comprehensive document: (G.1) four formal primary estimands with notation, identification logic, and hypothesis mappings; (G.2) three regression specifications (run-level OLS, mixed-effects extension, H2 capability OLS, ANOVA-style variance decomposition); (G.3) fixed vs. random effects rationale including reviewer response language; (G.4) model-level clustering with 10-cluster warning, wild cluster bootstrap recommendation, and within-model pair bootstrap; (G.5) BH-FDR correction for primary (H1–H10) and secondary (50-test) families with pre-registration requirement; (G.6) five mandatory robustness checks; (G.7) three falsification tests (placebo, null model, reversed optimal); (G.8) full power analysis table (N=30/50/100 × d=0.4/0.5/0.6), design decision table, and Type M error analysis; (G.9) pre-registration plan covering AEA RCT Registry/OSF, 10-item content checklist, labeling requirements, and registered vs. exploratory appendix table.

### G.1 Primary Estimands

- [x] **τ_bias(b, m)** = E[BSI | bias=b, model=m, variant=TREATMENT] - E[BSI | bias=b, model=m, variant=BASELINE]
  - This is the core estimand: within-model, within-bias treatment effect
  - Identified by: controlled variant pairing; repeated runs for noise reduction

- [x] **σ²_stoch(m, b)** = Var[BSI | model=m, bias=b] across runs
  - Stochastic variance component: how much variance is pure sampling noise?

- [x] **σ²_model** = Var[E[BSI | model=m]] across models
  - Between-model variance: how different are models from each other?

- [x] **Δ_capability** = ∂E[BSI] / ∂P1_score
  - Capability gradient: does higher capability reduce bias susceptibility?

### G.2 Primary Regression Equation

**Level 1 (run-level):**
```
BSI_{i,m,b,r} = α + β_b · BiasType_b + β_m · Model_m + β_t · Treatment_i
              + β_bm · (BiasType_b × Model_m)
              + β_tm · (Treatment_i × Model_m)
              + ε_{i,m,b,r}
```

Where:
- i = scenario instance (bias type × variant combination)
- m = model
- b = bias type
- r = run index
- Treatment_i = 1 if variant is TREATMENT (vs. BASELINE)

- [x] **Hierarchical (Mixed-Effects) Extension:**
```
BSI_{i,m,b,r} = α + X_i β + Z_m u_m + Z_b v_b + ε_{i,m,b,r}

u_m ~ N(0, Σ_model)   [random effects for model]
v_b ~ N(0, Σ_bias)    [random effects for bias type]
```

- [x] **Specification for H2 (Capability-BSI relationship):**
```
mean_BSI_m = α + β_1 · P1Score_m + β_2 · log(Parameters_m) + β_3 · ModelFamily_m + ε_m
```
Note: N=10 → present as descriptive OLS only; no inference claims.

- [x] **Variance Decomposition (ANOVA-style):**
```
BSI = μ + Model_effect + BiasType_effect + Prompt_effect + Temperature_effect + Residual
```
Report SS partition table: what fraction of total BSI variance is attributable to each factor?

### G.3 Fixed vs. Random Effects Decision

- [x] Model effects: Use **fixed effects** if comparing specific named models (GPT-4o, Claude, Gemini etc.) — we care about each specific model, not a "population of models"
- [x] Bias type effects: Use **fixed effects** — 5 specific bias categories, not a sample from a population
- [x] Run effects: Random (stochastic draws from model's distribution)
- [x] Document rationale for FE/RE choice — reviewers will ask

### G.4 Standard Errors & Clustering

- [x] Cluster standard errors at **model level** (10 clusters — warn this is at the boundary of reliable clustering; report both clustered and heteroscedasticity-robust SEs)
- [x] For within-model tests: pair bootstrap (resample runs within cell, compute test statistic)
- [x] Report: number of clusters, cluster-robust SE, and note small-cluster limitation

### G.5 Multiple Hypothesis Correction

- [x] Primary family: 10 hypotheses (H1–H10) → Apply Benjamini-Hochberg FDR correction
- [x] Secondary: within-bias-type model comparisons (10 models × 5 bias types = 50 tests) → Apply Bonferroni or BH
- [x] Pre-register corrections before data collection to avoid ex-post manipulation
- [x] Report both corrected and uncorrected p-values in appendix

### G.6 Robustness Checks (MANDATORY)

- [x] **Temperature robustness:** Re-run primary regressions at temp=0.0 (deterministic). If results collapse → findings are temperature-sensitive; flag this.
- [x] **Prompt wording robustness:** Re-run with minor rephrasing of scenario (different supplier names, different dollar amounts). If BSI changes substantially → surface-level sensitivity, not deep bias.
- [x] **Model version stability:** If possible, test 2 versions of same model family (e.g., GPT-4o-mini vs. GPT-4o). Does the ordering hold?
- [x] **Outlier robustness:** Drop top/bottom 5% of BSI scores; re-estimate. Are results driven by extreme outputs?
- [x] **Session order effects:** Check if run order (1st vs. 30th run) affects BSI. No session history → should be flat; document if not.

### G.7 Falsification Tests

- [x] **Placebo test:** Create "null variants" where the manipulation is identical surface presentation but economically identical choice (e.g., change supplier name but identical numbers). BSI should be 0. If not → our measurement instrument is contaminated.
- [x] **Null model test:** MockAgent (deterministic, no LLM) should have BSI=0 by construction. Verify this.
- [x] **Reversed optimal test:** Invert which option is "correct" in a subset of runs. Models should score 0 (always wrong). If they partially get it right → their reasoning is correlated with correctness by something other than bias detection.

### G.8 Power Analysis

- [x] **Target effect:** d = 0.4 (moderate; smaller than typical human bias effects d≈0.7–1.0, reflecting expected attenuated LLM effects)
- [x] **α = 0.05 (two-tailed), power = 0.80**
- [x] Required N per cell: ~100 observations (per G*Power for two-sample t-test d=0.4)
- [x] At N=30/cell: power = 0.52 → **underpowered for d=0.4. Sufficient only for d≥0.6.**
- [x] At N=50/cell: power = 0.70 → **marginal.**
- [x] At N=100/cell: power = 0.86 → **adequate.**

- [x] **DECISION:** Minimum viable paper requires N=50/cell. Flagship requires N=100/cell.
  - Realistic design (N=30): underpowered — label all results as exploratory; use confidence intervals not p-values
  - Realistic design target upgrade: N=50 per cell (cost: $750 total)

- [x] **Minimum viable sample table:**
  | Target d | N per cell | Total runs (5 bias × 2 variants × 10 models) | Est. cost |
  |---|---|---|---|
  | 0.6 (strong) | 30 | 3,000 | $450 |
  | 0.5 (moderate) | 50 | 5,000 | $750 |
  | 0.4 (modest) | 100 | 10,000 | $1,500 |

- [x] **Gold-standard sample:** N=100/cell + 3 prompt versions + 3 temperatures = 45,000 LLM runs (~$6,750)

### G.9 Pre-Registration Plan

- [x] Register on AEA RCT Registry or OSF before data collection
- [x] Pre-register: primary hypotheses, estimands, regression specs, correction procedures
- [x] Label all exploratory analyses as exploratory in the paper
- [x] Keep a "registered vs. exploratory" table in the appendix
