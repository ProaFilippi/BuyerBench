# PILLAR2-RESEARCH-01 — Journal Strategy, Literature Map & Research Gap
## BuyerBench Pillar 2: Economic Rationality & Behavioral Biases in LLM Agents

> **Purpose:** Establish the academic positioning, literature foundation, and defensible research gap before any empirical design decisions. All subsequent phases build on this.

---

## SECTION A — JOURNAL STRATEGY

### A.1 Tiered Journal Map

- [x] **[TIER 1 — Top General-Interest]** Document fit analysis for AER, QJE, JPE, Econometrica
  - Fit rationale: These require a novel economic *insight*, not merely novel *measurement*. A behavioral paper here must show LLM-bias patterns that revise or extend human behavioral theory (e.g., biases appear in a qualitatively different pattern, or a new mechanism is identified). Current BuyerBench data alone is insufficient — requires large N, multiple replications, human comparison arms.
  - Required evidence level: N > 500 agent-runs per bias type; human comparison arm (MTurk or lab); causal identification of *why* biases emerge; theory-grounded structural model.
  - Rejection triggers: "Interesting measurement but no economic insight"; "results don't generalize beyond these specific prompts"; "no theory"; "stochastic outputs treated as deterministic".
  - ✅ *Completed 2026-04-15:* Full journal-by-journal analysis written at `docs/paper/journal-strategy/tier1-top-general-interest-journals.md`. Per-journal fit rationale, evidence thresholds, rejection triggers, and strategic timeline documented for AER, QJE, JPE, and Econometrica. Tier 1 is a 5–10 year horizon; near-term target remains JEBO/Experimental Economics (Tier 2).

- [x] **[TIER 2 — Top Field: Behavioral & Experimental]** Document fit for Journal of Economic Behavior & Organization (JEBO), Experimental Economics, Journal of Behavioral Decision Making, Games and Economic Behavior
  - Fit rationale: These journals accept well-identified empirical studies with solid methodology. A bias battery with clean controlled variants, proper statistical power, and credible stochasticity modeling can publish here without a human comparison arm — though it is preferred.
  - Required evidence level: N ≥ 30 runs per (bias × model × architecture) cell; mixed-effects regression; multiple bias types; variance decomposition by model family vs. prompt vs. temperature.
  - Rejection triggers: "Only descriptive statistics"; "no power justification"; "one-shot runs treated as evidence"; "no correction for multiple comparisons".
  - ✅ *Completed 2026-04-15:* Full journal-by-journal analysis written at `docs/paper/journal-strategy/tier2-field-behavioral-journals.md`. Per-journal fit rationale, evidence thresholds, rejection triggers, and strategic timeline documented for JEBO, Experimental Economics, JBDM, and GEB. Decision gate and minimum viable paper specification included. **Primary recommendation: JEBO** (1,500 runs, $225 API cost, achievable in one weekend). Fast-path option: JBDM. GEB is a follow-on target for the WARP battery study only.

- [x] **[TIER 3 — Adjacent Credible]** Document fit for Journal of Artificial Intelligence Research (JAIR), AI & Society, Decision Support Systems, Management Science (IS track)
  - Fit rationale: Methodological contribution (BuyerBench as evaluation framework) is sufficient if paired with substantive empirical findings. Management Science IS track values applied rigor.
  - Required evidence level: Reproducible benchmark; clear protocol; 2+ models; systematic results. Human comparison optional.
  - Rejection triggers: "Pure benchmarking paper without economic contribution"; "no comparison to prior work"; framework not publicly released.
  - ✅ *Completed 2026-04-15:* Full journal-by-journal analysis written at `docs/paper/journal-strategy/tier3-adjacent-journals.md`. Per-journal fit rationale, evidence thresholds, rejection triggers, and strategic timeline documented for JAIR, AI & Society, DSS, and Management Science IS. **Primary Tier 3 recommendation: DSS** (highest IF at 7.5; direct procurement domain fit) with JAIR as a recommended first publication to establish the framework in the AI literature. Management Science IS is a long-horizon (18–24 month) follow-on target requiring economic consequence quantification. Recommended publication sequence: JAIR (3–6 mo) → JEBO/DSS (6–12 mo) → Management Science IS (18–24 mo).

- [x] **[TIER 4 — Realistic Primary Target]** JEBO or Experimental Economics as primary submission
  - Strategy: Submit flagship version here first. If rejected for scope, revise down to field-journal working paper tier.
  - ✅ *Completed 2026-04-15:* Full primary submission strategy written at `docs/paper/journal-strategy/tier4-primary-submission-strategy.md`. Document covers: (1) why JEBO is the primary target over other Tier 2 journals, (2) a concrete decision gate (go/no-go criteria before submitting), (3) a preparation checklist for data, analysis, framing, and reproducibility, (4) a realistic milestone timeline (12–15 months from data collection to acceptance), (5) a rejection cascade strategy mapping each rejection reason to a specific corrective action and next venue, and (6) a structured cascade order: JEBO → Experimental Economics → JBDM → DSS → Tier 5. Document explicitly frames Tier 4 as a submission priority tier distinct from the prestige tier numbering in the journal fit analysis.

- [ ] **[TIER 5 — Fallback]** Journal of Economic Psychology, Judgment and Decision Making, PLOS ONE
  - These accept descriptive behavioral studies with modest N. Working paper version is publishable here.

### A.2 Strategy Decision Tree

- [ ] Document the decision gate: "If we can run N=50 per cell across ≥6 bias types and ≥8 models → target JEBO. If N<30 or <5 bias types → target Journal of Economic Psychology."
- [ ] Define the minimum viable paper: 5 bias types × 10 models × 30 runs = 1,500 observations. Feasible via OpenRouter API in one weekend.

---

## SECTION B — LITERATURE MAP

> **Rule:** For each paper: (1) empirical design, (2) strengths, (3) limitations, (4) relevance to BuyerBench.

### B.1 Canonical Behavioral Bias Studies

- [ ] **Anchoring** — Tversky & Kahneman (1974) "Judgment Under Uncertainty: Heuristics and Biases". Science.
  - Design: Wheel-of-fortune anchor + Africa % estimate. N≈500 students.
  - Strength: Clean manipulation; large effect size (r≈0.8). Limitation: Lab, incentive-free, US students.
  - Relevance: BuyerBench p2-01 directly operationalizes this. Our anchor (historical price) is ecologically valid for procurement.

- [ ] **Framing Effects** — Tversky & Kahneman (1981) "The Framing of Decisions". Science.
  - Design: Asian Disease problem; gain vs. loss frame. N≈152.
  - Strength: Identical EV, clean reversal. Limitation: single-item, student sample.
  - Relevance: BuyerBench p2-02 uses contract-selection framing. Different domain but structurally isomorphic.

- [ ] **Decoy Effect (IIA Violation)** — Huber, Payne & Puto (1982) "Adding Asymmetrically Dominated Alternatives". JCR.
  - Design: Choice sets with asymmetrically dominated decoy. N≈153.
  - Strength: First lab proof of IIA violation in consumer choice. Limitation: incentive-free.
  - Relevance: BuyerBench p2-03. GPT-4o failed this (score 0.9 vs 1.0 for others) — potentially genuine finding.

- [ ] **Sunk Cost Fallacy** — Arkes & Blumer (1985) "The Psychology of Sunk Cost". OBHDP.
  - Design: Theater ticket + ski trip vignette experiments. Multiple studies N≈60–200.
  - Relevance: BuyerBench p2-05. Document the measured BSI benchmarks for human subjects from this paper.

- [ ] **Scarcity/Urgency** — Cialdini (1984) *Influence*. Worchel et al. (1975) "Effects of Supply and Demand on Ratings of Object Value".
  - Relevance: BuyerBench p2-04. Artificial urgency cues in supplier context.

- [ ] **Status Quo Bias** — Samuelson & Zeckhauser (1988) "Status Quo Bias in Decision Making". J Risk Uncertainty.
  - Relevance: Not yet implemented in BuyerBench. Candidate for Phase I expansion (p2-06).

- [ ] **Loss Aversion** — Kahneman & Tversky (1979) "Prospect Theory". Econometrica.
  - Relevance: Partially covered by framing; loss-aversion switching scenario not yet implemented. Candidate p2-07.

### B.2 Experimental Economics Methods

- [ ] **Incentivized vs. Hypothetical Choice** — Camerer & Hogarth (1999). Document: does lack of monetary incentives in LLM prompts bias our findings? (They cannot receive money; design implication.)
- [ ] **Repeated Measurement & Learning** — Charness & Levin (2005). Document: LLMs don't learn across sessions — this is both a limitation and a clean advantage (no learning confound).
- [ ] **Within-Subject vs. Between-Subject** — Greenwald (1976). Our design is between-subject (each model sees either baseline OR variant, not both). Document why: avoid demand effects.

### B.3 AI/LLM Behavioral Studies (Key Prior Work to Beat)

- [ ] **Binz & Schulz (2023)** "Using cognitive psychology to understand GPT-3." PNAS.
  - Design: Administered 10 classic cognitive psychology tasks to GPT-3. N=1 model.
  - Strength: Systematic battery. Limitation: Single model, no temperature variation, no replication.
  - BuyerBench difference: Multi-model, procurement domain, controlled variants, stochasticity modeling.

- [ ] **Ortega & Maini (2023)** "AI Safety Gridworlds" — discusses instrumental reasoning. Not bias-specific but methodologically relevant.

- [ ] **Hagendorff et al. (2023)** "Human-like intuitive behavior and reasoning biases emerged in LLMs." Nature Human Behaviour.
  - Design: CRT tasks, conjunction fallacy, bat-and-ball. Found intuitive (System 1) patterns.
  - Limitation: No procurement domain, no multi-model comparison, single-shot.
  - BuyerBench difference: Economically consequential domain with ground-truth optimal.

- [ ] **Aher et al. (2023)** "Using Large Language Models to Simulate Multiple Humans." ICML.
  - Design: Replicates classic experiments (Ultimatum Game, etc.) with LLMs as synthetic respondents.
  - Limitation: "Stochastic parroting" concern — LLMs may reproduce training data patterns, not genuine decision processes.
  - BuyerBench response: Our scenarios use novel procurement contexts with ground-truth computability — harder to parrot.

- [ ] **Jones & Steinhardt (2022)** "Capturing Failures of Large Language Models via Human Cognitive Biases." NeurIPS.
  - Survey of LLM failures mapped to cognitive bias categories.
  - Relevance: Our bias taxonomy should be positioned relative to this.

- [ ] **Echterhoff et al. (2024)** "Cognitive Bias in High-Stakes Decision-Making with LLMs." arXiv.
  - Most relevant prior work. Must beat or substantially extend.
  - Document their methodology and what BuyerBench adds (procurement domain, economic optimality metric, controlled-variant design, multi-model comparison).

### B.4 Rationality & Bounded Rationality

- [ ] **Simon (1955)** "A Behavioral Model of Rational Choice." QJE. — Satisficing concept.
- [ ] **Thaler & Sunstein (2008)** *Nudge* — Choice architecture. Relevant to default bias design.
- [ ] **Charness & Rabin (2002)** Social preferences in games — bound on "rationality" definition.

### B.5 Variance, Replication & Stochastic Agents

- [ ] **Open Science Collaboration (2015)** "Estimating Reproducibility of Psychological Science." Science. — Replication crisis context; motivates our multi-run design.
- [ ] **Simmons, Nelson & Simonsohn (2011)** "False-Positive Psychology." Psych Science. — p-hacking; motivates pre-registration and multiple comparison correction.
- [ ] **Loken & Gelman (2017)** "Measurement error and the replication crisis." Science. — Noise in measurement. Directly applicable to temperature-sampled LLM outputs.

### B.6 Literature Synthesis

- [ ] Write 400-word synthesis: "What is known, what is unresolved, where BuyerBench contributes"
  - Known: LLMs show System 1/System 2 behavior patterns; anchoring and framing effects documented in lab-style prompts; single-model, single-shot studies dominate.
  - Unresolved: Multi-model variation in bias susceptibility; domain-specificity (procurement vs. general); whether stochastic output variance swamps effect sizes; whether high-capability models are less biased.
  - BuyerBench contribution: First controlled-variant bias battery in economically consequential procurement domain; multi-model; stochasticity-aware; ground-truth optimal defined.

---

## SECTION C — RESEARCH GAP

- [ ] **Gap 1 (Primary — Benchmarking):** No existing benchmark evaluates LLM behavioral biases in procurement decision-making with ground-truth economic optimality. Existing studies use generic cognitive tasks (CRT, bat-and-ball) without domain-specific economic structure.

- [ ] **Gap 2 (Secondary — Multi-Model Comparative):** Prior work is predominantly single-model. We do not know whether bias susceptibility is a property of model capability, model family, architecture, or training data.

- [ ] **Gap 3 (Methodological):** No existing study explicitly models stochastic LLM output variance as a confound in bias detection. Effect sizes from single-run studies may be entirely driven by temperature sampling noise.

- [ ] **Gap 4 (Economic):** The economic concept of "bias susceptibility index" — measuring deviation from rational optimum as a normalized index — has not been formalized and applied to LLM agents.

- [ ] **Contribution Ranking:**
  1. **Measurement/Benchmarking** (most defensible) — BuyerBench as a reproducible protocol
  2. **Methodological** (strong) — stochasticity modeling, variance decomposition, BSI formalization
  3. **Behavioral economics insight** (cautious) — cross-model patterns with appropriate hedging
  4. **Theory** (speculative, not for this paper) — mechanism for why biases appear/disappear

- [ ] **Defensibility statement:** Write one paragraph explicitly distinguishing what we can claim vs. what requires future work. Core defensible claim: "We find that [X of 10 models] show statistically significant bias susceptibility on at least one of 5 bias categories, with inter-model variance explained primarily by [model family / capability tier / prompt structure]. Bias susceptibility is neither universal nor absent — it is heterogeneous across bias type and model."
