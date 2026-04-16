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

- [x] **[TIER 5 — Fallback]** Journal of Economic Psychology, Judgment and Decision Making, PLOS ONE
  - These accept descriptive behavioral studies with modest N. Working paper version is publishable here.
  - ✅ *Completed 2026-04-15:* Full journal-by-journal analysis written at `docs/paper/journal-strategy/tier5-fallback-journals.md`. Per-journal fit rationale, evidence thresholds, rejection triggers, and strategic recommendations documented for JEP, JDM, and PLOS ONE. Key addition over prior tiers: explicit **null result strategy** — PLOS ONE is the correct venue if bias susceptibility is statistically indistinguishable from noise (an outcome the prior tiers do not accommodate). Three distinct strategic roles for Tier 5 documented: (1) pilot publication before the large-scale data collection sprint, (2) null result publication, (3) fallback after cascade rejection. Decision guide (which Tier 5 venue to use) and minimum evidence table included. JDM recommended when replicating canonical paradigms; JEP for behavioral economics framing; PLOS ONE as unconditional publication floor for methodologically sound work regardless of outcome direction.

### A.2 Strategy Decision Tree

- [x] Document the decision gate: "If we can run N=50 per cell across ≥6 bias types and ≥8 models → target JEBO. If N<30 or <5 bias types → target Journal of Economic Psychology."
  - ✅ *Completed 2026-04-15:* Full strategy decision tree written at `docs/paper/journal-strategy/strategy-decision-tree.md`. Three-gate decision flow (sample size → coverage → analysis completeness) formalizes the routing logic from the tier analyses into a standalone quick-reference. Fallback gate explicitly routes N<30 to JEP and null results to PLOS ONE.
- [x] Define the minimum viable paper: 5 bias types × 10 models × 30 runs = 1,500 observations. Feasible via OpenRouter API in one weekend.
  - ✅ *Completed 2026-04-15:* Minimum viable paper specification documented in `docs/paper/journal-strategy/strategy-decision-tree.md` with cost estimate (~$225 at $0.15/run), execution timeline (one weekend), and the preferred "strong" specification (N=50 per cell + temperature ablation + human comparison arm). Pre-submission checklist (Gate 3 expanded) also included.

---

## SECTION B — LITERATURE MAP

> **Rule:** For each paper: (1) empirical design, (2) strengths, (3) limitations, (4) relevance to BuyerBench.

### B.1 Canonical Behavioral Bias Studies

- [x] **Anchoring** — Tversky & Kahneman (1974) "Judgment Under Uncertainty: Heuristics and Biases". Science.
  - Design: Wheel-of-fortune anchor + Africa % estimate. N≈500 students.
  - Strength: Clean manipulation; large effect size (r≈0.8). Limitation: Lab, incentive-free, US students.
  - Relevance: BuyerBench p2-01 directly operationalizes this. Our anchor (historical price) is ecologically valid for procurement.
  - ✅ *Completed 2026-04-15:* Full literature note written at `docs/paper/literature-map/b1-01-anchoring-tversky-kahneman-1974.md`. Covers: (1) empirical design including wheel-of-fortune paradigm, follow-up demonstrations, and N≈500 student sample; (2) strengths — r≈0.8 effect size, multiple converging paradigms, mechanism robustness under incentives; (3) limitations — lab/student sample, single-item measurement, mechanism ambiguity, no learning/feedback; (4) BuyerBench relevance — exact BASELINE vs. ANCHOR_HIGH controlled-variant mapping for p2-01, ecological validity discussion (causally plausible vs. arbitrary anchor), human benchmark BSI comparison table, stochasticity advantage, and paper-framing guidance for intro, related work, methodology, and results sections.

- [x] **Framing Effects** — Tversky & Kahneman (1981) "The Framing of Decisions". Science.
  - Design: Asian Disease problem; gain vs. loss frame. N≈152.
  - Strength: Identical EV, clean reversal. Limitation: single-item, student sample.
  - Relevance: BuyerBench p2-02 uses contract-selection framing. Different domain but structurally isomorphic.
  - ✅ *Completed 2026-04-16:* Full literature note written at `docs/paper/literature-map/b1-02-framing-tversky-kahneman-1981.md`. Covers: (1) empirical design including the Asian Disease paradigm, N≈152 student samples and physician replication, preference reversal of 50 percentage points, and Prospect Theory grounding; (2) strengths — description invariance falsification, expert replication (physicians susceptible), multiple domains, theory-linked mechanism; (3) limitations — hypothetical stakes, binary choice structure, training data confound for LLMs; (4) BuyerBench relevance — critical methodological note that p2-02 tests **context/attribute framing** (Levin et al., 1998 taxonomy), NOT T&K's risky choice framing paradigm. The hard budget constraint ($155k ceiling, Beta at $180k) makes Alpha the objectively correct choice in both frames; BSI=0.0 across all successfully executing models reflects framing resistance in constraint-enforcing decisions, not general framing immunity. Training data contamination argument (novel stimulus set avoids memorized Asian Disease responses) documented. Proposed `p2-02b` EV-equivalent upgrade scenario for genuine risky choice framing replication. BibTeX entries for T&K 1981, Levin et al. 1998, and McNeil et al. 1982 included.

- [x] **Decoy Effect (IIA Violation)** — Huber, Payne & Puto (1982) "Adding Asymmetrically Dominated Alternatives". JCR.
  - Design: Choice sets with asymmetrically dominated decoy. N≈153.
  - Strength: First lab proof of IIA violation in consumer choice. Limitation: incentive-free.
  - Relevance: BuyerBench p2-03. GPT-4o failed this (score 0.9 vs 1.0 for others) — potentially genuine finding.
  - ✅ *Completed 2026-04-16:* Full literature note written at `docs/paper/literature-map/b1-03-decoy-effect-huber-payne-puto-1982.md`. Covers: (1) empirical design — asymmetric dominance manipulation across 6 product domains (N≈153), dual falsification of regularity assumption and IIA, 10–27 pp preference share increases, and the attribute-space positioning mechanism; (2) strengths — cross-domain replication within a single paper, simultaneous falsification of two axioms, first systematic IIA violation in consumer choice; (3) limitations — incentive-free, small within-domain N, two-attribute product abstraction, student sample; (4) BuyerBench relevance — full p2-03 operationalization analysis including SupplierGamma as asymmetrically dominated decoy (dominated by Alpha, not Beta), failure mode taxonomy distinguishing genuine IIA violations from execution/parsing failures (GPT-4o's BSI=1.0 is most likely an operational failure, not a behavioral bias), human benchmark comparison table (Heath & Chatterjee meta-analysis: ~12.5 pp mean share increase), and stochasticity design notes for within-model IIA violation rate estimation; (5) critical design note: explicit weighted rubric in p2-03 prompt may suppress decoy effect relative to human literature — proposed p2-03b variant without explicit weights; BibTeX for Huber 1982, Tversky & Simonson 1993, Simonson 1989, and Heath & Chatterjee 1995 included.

- [x] **Sunk Cost Fallacy** — Arkes & Blumer (1985) "The Psychology of Sunk Cost". OBHDP.
  - Design: Theater ticket + ski trip vignette experiments. Multiple studies N≈60–200.
  - Relevance: BuyerBench p2-05. Document the measured BSI benchmarks for human subjects from this paper.
  - ✅ *Completed 2026-04-16:* Full literature note written at `docs/paper/literature-map/b1-04-sunk-cost-arkes-blumer-1985.md`. Covers: (1) empirical design — ten studies using vignette methodology (theater ticket, ski trip, investment escalation); primary benchmark: ~54% human susceptibility in the ski trip paradigm (Study 3, N≈200); (2) strengths — multi-paradigm within a single paper, cross-domain (consumer + organizational), mechanism isolation via $0 subsidy condition (Study 4); (3) limitations — hypothetical vignettes, student samples, mechanism conflation, training data contamination risk for LLMs; (4) BuyerBench relevance — full p2-05 operationalization including the $72,000 prior CarrierA trial and account manager "don't let it go to waste" framing; current experimental results show BSI ≈ 0.0 across all 9 correctly-executing models (human benchmark: ~54%); critical design note that the explicit constraint "past expenditures are sunk costs" in the prompt may suppress susceptibility by naming the fallacy, rather than reflecting genuine economic rationality; proposed `p2-05b` unlabeled variant to disentangle constraint-following from forward-looking reasoning; BibTeX for Arkes & Blumer 1985, Staw 1981, Thaler 1980, Garland 1990, and Larrick et al. 1990 included.

- [x] **Scarcity/Urgency** — Cialdini (1984) *Influence*. Worchel et al. (1975) "Effects of Supply and Demand on Ratings of Object Value".
  - Relevance: BuyerBench p2-04. Artificial urgency cues in supplier context.
  - ✅ *Completed 2026-04-16:* Full literature note written at `docs/paper/literature-map/b1-05-scarcity-cialdini-worchel-1975.md`. Covers: (1) empirical design — Worchel et al.'s cookie scarcity paradigm (N≈134/200) showing d≈0.6–0.8 value inflation for scarce objects, Cialdini's dual-mechanism synthesis (quality proxy inference + psychological reactance), and ecological field evidence across B2B procurement contexts; (2) strengths — domain-native manipulation, dual mechanism identification, cross-domain robustness from lab (Worchel) + field (Cialdini); (3) limitations — no single clean quantitative BSI benchmark, cookie ratings ≠ forced choice, low-intensity manipulation in p2-04 vs. Cialdini's documented field tactics; (4) BuyerBench relevance — p2-04 simultaneously deploys temporal scarcity (end-of-day pricing expiry) and capacity scarcity (Q2 allocation lock-in) for SupplierAlpha; **notable finding: LLaMA 3.3 70B is the only model that passed BASELINE (SupplierBeta ✓) but failed SCARCITY (SupplierAlpha ✗) — a genuine bias susceptibility signature, distinguished from its execution failure on p2-05-sunk-cost**; 9/10 frontier models show BSI = 0.0; proposed `p2-04b` high-intensity variant with competitive social proof and explicit capacity count; BibTeX for Cialdini 1984, Worchel et al. 1975, Brehm 1966 (reactance theory), Inman et al. 1997, and Lynn 1991 meta-analysis included.

- [x] **Status Quo Bias** — Samuelson & Zeckhauser (1988) "Status Quo Bias in Decision Making". J Risk Uncertainty.
  - Relevance: Not yet implemented in BuyerBench. Candidate for Phase I expansion (p2-06).
  - ✅ *Completed 2026-04-16:* Full literature note written at `docs/paper/literature-map/b1-06-status-quo-bias-samuelson-zeckhauser-1988.md`. Covers: (1) empirical design — four between-subjects survey experiments (investment allocation, health insurance, government policy, job choice; N≈80–200 per study) with the status quo label rotated across options to isolate the labeling effect; status quo premium of ~20–30 pp above neutral baseline choice rate for the 4-option investment allocation paradigm; increasing-alternatives amplification effect documented; (2) strengths — within-paper label rotation cleanly identifies the status quo label as the causal driver (not pre-existing option properties), cross-domain robustness (four domains), quantified premium usable as BSI calibration baseline; (3) limitations — hypothetical vignettes, Harvard student sample, mechanism conflation (loss aversion vs. regret vs. cognitive cost avoidance), LLMs lack a genuine prior relationship so the "incumbent" is a text label rather than lived experience; (4) BuyerBench relevance — full proposed `p2-06-status-quo` scenario design specification: BASELINE (no prior relationship) vs. STATUS_QUO (SupplierAlpha designated as 30-day-expiring incumbent contract), BSI scoring logic, human benchmark prediction (~20–30 pp susceptibility for 4-supplier set), three reasons why status quo bias is a high-priority expansion candidate (incumbent relationships are the norm; ecologically validated at population scale via 401(k) and organ donation defaults; potential interaction with scarcity bias in compound scenario); implementation notes covering framing, avoiding demand effects, and secondary reasoning-trace measurement; BibTeX for Samuelson & Zeckhauser 1988, Madrian & Shea 2001 (401(k)), Johnson & Goldstein 2003 (organ donation), Loomes & Sugden 1982 (regret theory), and Kahneman, Knetsch & Thaler 1991 (endowment effect and SQB) included.

- [x] **Loss Aversion** — Kahneman & Tversky (1979) "Prospect Theory". Econometrica.
  - Relevance: Partially covered by framing; loss-aversion switching scenario not yet implemented. Candidate p2-07.
  - ✅ *Completed 2026-04-16:* Full literature note written at `docs/paper/literature-map/b1-07-loss-aversion-kahneman-tversky-1979.md`. Covers: (1) empirical design — the certainty effect, reflection effect, isolation effect, and probability overweighting documented across student samples (N≈72–95 per problem), with the reflection effect (~70–80 pp preference reversal between gain and loss frames) as the core BSI calibration benchmark; (2) strengths — quantified λ ≈ 2.25 loss aversion coefficient, massive cross-domain replication record, field evidence in golf/real estate/taxi labor supply; (3) limitations — hypothetical stakes, highest training-data-contamination risk in the battery (most-cited economics paper in LLM corpora), reference point ambiguity, and the critical distinction from p2-02 framing (risky choice vs. attribute framing); (4) BuyerBench relevance — detailed p2-07-loss-aversion scenario design with SupplierAlpha (EV = $144,750, variable) vs. SupplierBeta ($148,000 certain) against a $160k budget reference point; controlled GAIN_FRAME/LOSS_FRAME variants isolating the reflection effect; BSI scoring table including reasoning-trace secondary measure; implementation priority analysis relative to existing battery; (5) paper framing guidance distinguishing p2-07 from p2-02 at the mechanism level; BibTeX for Kahneman & Tversky 1979, Tversky & Kahneman 1992 (cumulative), Pope & Schweitzer 2011 (golf), Genesove & Mayer 2001 (real estate), Camerer et al. 1997 (taxi drivers), and Levin et al. 1998 (framing typology) included.

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
