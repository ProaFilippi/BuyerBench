# PILLAR2-RESEARCH-02 — Hypotheses & Empirical Design Options
## BuyerBench Pillar 2: Economic Rationality & Behavioral Biases in LLM Agents

> **Purpose:** Operationalize the research question into testable hypotheses and evaluate candidate empirical designs before committing to a final design.

---

## SECTION D — HYPOTHESES

> **Rule:** Each hypothesis must have unit of observation, DV, IV(s), expected sign, theory basis, identification logic.

### D.1 Primary Research Question (Formal)

- [x] **PRQ:** "Does the behavioral bias susceptibility of LLM-based agents — measured as deviation from economically optimal choices under controlled presentation manipulations — vary systematically across model capability tiers, bias types, and experimental conditions, in ways analogous to, attenuated relative to, or amplified compared to documented human behavioral patterns?"
  - ✅ *Completed 2026-04-16:* Full PRQ operationalization written at `docs/paper/hypotheses/d1-primary-research-question.md`. Five-dimensional decomposition: (1) **Existence** — BSI > 0 as Dimension 1 test, mapped to H1 and H7; null framing ("surprisingly robust") pre-specified as a valid outcome; (2) **Variation across bias types** — one-way ANOVA across 5 bias type categories with BH-FDR correction, primary hypotheses H1/H3/H5; (3) **Variation across capability tiers** — Spearman correlation + OLS with N=10 models flagged as descriptive, primary H2 and H6 (non-monotone sunk cost interaction); (4) **Variation across experimental conditions** — temperature ablation protocol and CoT variant design, primary H8; (5) **Human benchmark calibration** — Cohen's d comparison to meta-analytic baselines from b1-01 through b1-05, primary H10. Hypothesis Coverage Map table shows which H1–H10 hypotheses address each PRQ dimension. Outcome Frame Decision Tree formalizes the "analogous / attenuated / amplified" trichotomy into a pre-data-collection decision procedure. Pre-Registration Template locks bias types, model set, BSI threshold (d ≥ 0.20, BH-FDR q = .05 across 50 primary tests), and null-result framing before data collection. Identification Requirements Summary table shows current status and required actions for each design element (key gaps: H4 requires p2-01b anchor-magnitude variant; H8 requires CoT prompt variants; IRB not yet started for human arm).

### D.2 Secondary Research Questions

- [ ] **SRQ1:** Which of the 5 tested bias types (anchoring, framing, decoy, scarcity, sunk cost) produce statistically significant bias susceptibility in LLM agents across repeated trials?
- [ ] **SRQ2:** Does model capability (as proxied by Pillar 1 scores or model parameter count) predict lower bias susceptibility?
- [ ] **SRQ3:** How much of observed output variance is attributable to stochastic sampling vs. systematic bias?
- [ ] **SRQ4:** Does chain-of-thought (CoT) prompting attenuate or amplify bias susceptibility?
- [ ] **SRQ5:** Are bias susceptibility profiles correlated across bias types within a model, or are they bias-specific?

### D.3 Testable Hypotheses (6–12 required)

**H1 — Bias Universality (Null: uniform high performance)**
- Unit: (model, bias_type, run)
- DV: bias_susceptibility_index (BSI; 0=rational, 1=fully biased)
- IV: bias_type (5-category factor)
- Expected: At least 2 bias types show mean BSI > 0.2 across models; reject uniform rationality
- Theory: Hagendorff et al. (2023); System 1 patterns in LLMs
- Identification: Paired t-test across baseline vs. variant runs; requires ≥30 runs per cell
- **FLAG:** Current data shows 8/10 models at BSI=0.0 on Pillar 2. If this holds at N=30, fail to reject H1 — paper must then pivot to "LLMs are surprisingly robust" framing.

**H2 — Capability-Bias Tradeoff**
- Unit: model
- DV: mean_BSI (aggregated across bias types)
- IV: pillar1_score (capability proxy); model_parameter_count (secondary proxy)
- Expected sign: Negative (higher capability → lower BSI)
- Theory: More capable models have more robust world models; less susceptible to surface framing
- Identification: OLS regression across 10 models; limited N — treat as descriptive/exploratory
- **FLAG:** N=10 models is dangerously small for regression inference. Frame as "suggestive pattern" not "causal estimate."

**H3 — Decoy Effect as Most Reliable Bias**
- Unit: (model, run) restricted to p2-03 scenarios
- DV: chose_inferior_option (binary)
- IV: decoy_present (binary treatment)
- Expected: decoy_present → higher probability of choosing suboptimal option (Huber et al. 1982)
- Theory: IIA violation in prospect evaluation; LLMs may overweight explicit comparisons in context
- Identification: Logistic regression; compare GPT-4o (failed decoy) vs. others
- **FLAG:** Only 1 model showed decoy failure in current data. Must replicate at N≥30 per model.

**H4 — Anchoring Magnitude Proportional to Anchor Distance**
- Unit: (model, run, anchor_magnitude)
- DV: selected_price_deviation (chosen supplier price minus optimal price)
- IV: anchor_value (continuous: $X above market rate)
- Expected sign: Positive (larger anchor → larger upward price deviation)
- Theory: Insufficient adjustment from reference point (Tversky & Kahneman 1974)
- Identification: Requires multiple anchor levels (currently only 1 high anchor). **Requires new scenario variant.**

**H5 — Framing Asymmetry (Loss Frames More Powerful)**
- Unit: (model, run) in p2-02 scenarios
- DV: chose_risk_averse_option (binary)
- IV: frame_type (GAIN vs. LOSS)
- Expected: LOSS frame → more conservative supplier choice (higher quality, lower risk)
- Theory: Prospect theory; loss aversion λ≈2.25 in humans
- Identification: Logistic regression with model FE; power requires N≥30 per (model × frame) cell

**H6 — Sunk Cost Effect Absent in Low-Capability Models**
- Unit: (model, run) in p2-05 scenarios
- DV: chose_sunk_cost_option (binary; chose option justified by prior spend)
- IV: capability_tier (high/medium/low based on P1 score)
- Expected: Non-monotonic — high-capability models may show *more* sunk cost susceptibility because they can "reason" about prior spend; low-capability models may simply pick the better option
- Theory: Countervailing effects: capability enables sophisticated but potentially biased reasoning
- Identification: Interaction term (capability_tier × sunk_cost_mention); medium-N feasible

**H7 — Stochastic Variance Proportional to Bias Susceptibility**
- Unit: (model, bias_type)
- DV: within-cell variance of BSI across runs
- IV: mean_BSI (cell mean)
- Expected: Positive relationship — biased responses are noisier (boundary states)
- Theory: Signal detection: biased decisions are made at lower confidence → higher variance
- Identification: Variance regression; Levene test across BSI quartile groups

**H8 — CoT Prompting Reduces Anchoring But Not Decoy Effects**
- Unit: (model, run, prompt_type)
- DV: BSI by bias type
- IV: cot_prompt (standard vs. chain-of-thought variant)
- Expected: CoT reduces anchoring (explicit reasoning corrects anchor); CoT does not reduce decoy (comparison reasoning may *worsen* decoy susceptibility)
- Theory: System 2 engagement reduces anchoring but not comparison-based biases
- Identification: 2×2 factorial: (bias_type × prompt_type); **Requires new prompt variants.**

**H9 — Bias Profiles are Model-Specific, Not Universal**
- Unit: model
- DV: BSI per bias type (5-dim vector)
- IV: model identity
- Expected: Low inter-bias correlation within model (each model has idiosyncratic vulnerability profile)
- Theory: Different training data/RLHF → different bias landscapes
- Identification: Intra-model bias correlation matrix; Cronbach alpha < 0.5 expected

**H10 — Human Benchmark Calibration**
- Unit: bias type
- DV: effect_size_d (Cohen's d for BSI vs. 0)
- IV: agent_type (LLM vs. human from literature meta-analysis)
- Expected: LLM effect sizes smaller than human baselines for most biases
- Theory: RLHF + instruction tuning may attenuate "natural" cognitive shortcuts
- Identification: Compare our estimated d against meta-analytic estimates from human literature. **Requires literature benchmark table.**

---

## SECTION E — EMPIRICAL DESIGN OPTIONS

### E.1 Design Option 1: Bias Battery with Repeated Runs (Baseline Design)

**Description:** Run existing 5 bias pairs × N repetitions × 10 models. Fixed prompt; vary temperature to characterize stochasticity.

**Identification strength:** Medium. Good internal validity (controlled variants). Weak external validity (specific procurement context).

**Statistical power:** At N=30 per cell: Power≈0.80 for d=0.5 effect. At N=50: Power≈0.87 for d=0.5.

**Cost:** ~$0.15/run via OpenRouter × 30 runs × 10 scenarios × 10 models = $450. Feasible.

**Interpretability:** High. Direct comparison of BSI across models and bias types.

**Publication potential:** Tier 3–4. Sufficient for field journal if well-powered and corrected for multiplicity.

**Weaknesses:**
- Single domain (procurement supplier selection)
- No human comparison arm
- 5 bias types may not be enough to characterize "bias profile"

**Verdict:** Minimum viable paper design. Start here.

---

### E.2 Design Option 2: Economic Games Battery

**Description:** Administer classic economic games (Ultimatum Game, Dictator Game, Trust Game, Public Goods) to LLMs as synthetic players. Measure deviation from game-theoretic predictions.

**Identification strength:** High theoretical grounding (decades of human data). Clear prediction (SPNE, Nash Equilibrium).

**Cost:** Need multi-round conversation harness. Higher engineering cost. $200–$500 in API.

**Interpretability:** Medium. LLMs as "players" raises validity questions — they cannot actually receive payoffs.

**Weaknesses:**
- Incentive incompatibility is fundamental: LLMs don't face real payoffs → results are descriptive, not behavioral
- Prior work (Aher et al. 2023) already covers much of this space
- Procurement relevance lower

**Verdict:** Include as supplementary battery (Ultimatum Game to test fairness norms in supplier selection). Do NOT make it the primary design.

---

### E.3 Design Option 3: Multi-Factor Factorial Experiment

**Description:** Full 2^k factorial design crossing: (bias_type × prompt_version × model × temperature × task_complexity). Use fractional factorial or Latin square to manage combinations.

**Identification strength:** High. Allows main effects AND interactions. Can decompose variance: "How much of BSI variance is model vs. prompt vs. bias type?"

**Cost:** E.g., 5 bias × 3 prompt versions × 10 models × 10 temperatures × 2 complexity = 3,000 runs. At $0.15/run → $450. Feasible.

**Econometric fit:** Hierarchical linear model / variance decomposition (ANOVA-style). Clean regression structure.

**Weaknesses:**
- Requires designing new prompt variants (CoT, simplified, expert-framed)
- More complex to execute without automated harness
- Interaction interpretation can be difficult to communicate

**Verdict:** FLAGSHIP DESIGN. Implement after baseline. Requires BuyerBench prompt variant support.

---

### E.4 Design Option 4: Preference Consistency / WARP Battery

**Description:** Test Weak Axiom of Revealed Preference (WARP). Present agents with binary choices A>B, B>C; then test if they choose A>C. Repeat with shuffled context. Measure transitivity violations.

**Identification strength:** Very high conceptually (WARP is a core rationality axiom). Easy to falsify.

**Cost:** Need 3+ choice tasks per model per run. Low marginal cost.

**Interpretability:** High. WARP violations have a clean economic interpretation.

**Weaknesses:**
- Must control for prompt-order effects (if same session, violation may reflect context, not preference)
- Between-session design requires many runs
- Requires new scenario design (3-way supplier comparisons)

**Verdict:** Include as SECTION of flagship design. One WARP battery (3 suppliers, 3 pairwise comparisons) across 10 models × 30 runs.

---

### E.5 Design Option 5: Human Comparison Arm (Gold Standard)

**Description:** Administer same procurement scenarios to human subjects (MTurk/Prolific). Compare BSI distributions between humans and LLMs.

**Identification strength:** Strongest. Directly addresses "are LLMs more or less biased than humans?"

**Cost:** ~100 human subjects × 10 scenarios × $0.50/scenario = $500. Feasible.

**Weaknesses:**
- Human subjects require IRB approval (2–6 month delay)
- Procurement scenarios may have low ecological validity for MTurk workers (unfamiliar domain)
- Human responses also have variance; requires careful power analysis

**Verdict:** MANDATORY FOR FLAGSHIP PAPER. Optional for working paper. Plan IRB submission in parallel.

---

### E.6 Design Comparison Matrix

- [ ] Create formatted table comparing all 5 designs on:
  - Identification strength (1–5)
  - Statistical power (1–5)
  - Engineering cost (1–5, lower=cheaper)
  - Time to execute
  - Publication tier enabled
  - Key risk
