# PILLAR2-RESEARCH-05 — Paper Outlines & Draft Text (Dual Track)
## BuyerBench Pillar 2: Economic Rationality & Behavioral Biases in LLM Agents

> **Purpose:** Create paper outlines for both tracks and draft key text sections with placeholders clearly marked. No fake results. All data claims are placeholders until experiments are run.

---

## SECTION J — PAPER OUTLINES (DUAL TRACK)

### J.1 REALISTIC WORKING PAPER OUTLINE

**Venue:** Experimental Economics / Journal of Economic Psychology  
**Length target:** 10,000–12,000 words  
**Data required:** 5,000 runs (5 bias × 2 variants × 10 models × 50 runs)

- [x] **Abstract** (200 words): Problem, method, key finding, implication
- [x] **1. Introduction** (800 words)
  - Economic relevance: AI buyer agents making procurement decisions at scale
  - The bias question: do LLMs inherit human cognitive shortcuts?
  - What we do: BuyerBench as a controlled-variant bias battery
  - Key findings: [PLACEHOLDER — after experiment]
  - Contribution: first multi-model, stochasticity-aware bias measurement in procurement

- [x] **2. Related Literature** (1,500 words)
  - 2.1 Behavioral biases in human decision-making (Tversky & Kahneman legacy)
  - 2.2 Prior work on LLM cognitive biases (Binz & Schulz 2023; Hagendorff 2023; Echterhoff 2024)
  - 2.3 How BuyerBench differs: domain specificity, ground-truth optimality, multi-model, stochasticity

- [x] **3. Experimental Design** (2,000 words)
  - 3.1 BuyerBench Pillar 2: controlled-variant methodology
  - 3.2 Bias categories and scenario structure (Table: 5 bias types × design description)
  - 3.3 Agent models (Table: 10 models with family, parameters, capability tier)
  - 3.4 Run protocol: N=50 per cell; temperature=0.7; between-subject; session independence
  - 3.5 Bias Susceptibility Index (BSI): formal definition
  - 3.6 Statistical approach: mixed-effects regression; BH correction; pre-registration link

- [x] **4. Results** (3,000 words) — ALL PLACEHOLDER UNTIL DATA
  - 4.1 Aggregate bias susceptibility by model (Figure: heatmap — model × bias type)
  - 4.2 Main effects: which bias types produce highest BSI?
  - 4.3 Model capability gradient: does P1 score predict lower BSI?
  - 4.4 Stochastic variance: within-cell variance vs. between-model variance
  - 4.5 Individual model profiles: notable patterns

- [x] **5. Discussion** (1,500 words)
  - 5.1 Implications for AI agent deployment in procurement
  - 5.2 Comparison to human benchmarks (where available from literature)
  - 5.3 Why do high-capability models sometimes show MORE bias? (reasoning amplifies sunk cost?)
  - 5.4 Limitations: single domain, no incentives, prompt sensitivity

- [x] **6. Conclusion** (500 words)
- [x] **Appendix A:** Full scenario text for all 10 scenario variants
- [x] **Appendix B:** Pre-registration document
- [x] **Appendix C:** Additional regression tables
- [x] **Appendix D:** Robustness checks (temp=0.0; permutation tests)

---

### J.2 FLAGSHIP PAPER OUTLINE

**Venue:** JEBO / Experimental Economics (with human arm: broader consideration)  
**Length target:** 15,000–18,000 words  
**Data required:** 20,000+ LLM runs + 100 human subjects

- [x] All sections from realistic paper, PLUS:
- [x] **3.7 Prompt variants:** CoT vs. standard vs. expert-role
- [x] **3.8 Human comparison arm:** Prolific design; incentive structure; IRB protocol
- [x] **3.9 Temperature sensitivity analysis**
- [x] **4.6 Prompt × Bias interactions** (Figure: 3-way interaction plot)
- [x] **4.7 Human vs. LLM comparison** (Figure: side-by-side BSI by bias type)
- [x] **4.8 Capability × Bias interactions:** does CoT help more for anchoring than decoy?
- [x] **5.5 Structural interpretation:** what does differential bias susceptibility tell us about LLM architecture?
- [x] **Online Appendix:** Full dataset + replication code

---

## SECTION K — DRAFT TEXT

### K.1 Title Options

- [x] **Option A (Working Paper):** "Behavioral Bias Susceptibility in Large Language Models: Evidence from a Controlled Procurement Evaluation Benchmark"
- [x] **Option B (Field Journal):** "Do AI Buyer Agents Suffer from Cognitive Biases? Experimental Evidence from LLM-Based Procurement Systems"
- [x] **Option C (Flagship — if human arm):** "Machine Minds and Human Biases: Comparative Experimental Evidence on Economic Rationality in Large Language Model Agents"
- [x] **Option D (Catchy):** "Anchored, Framed, and Deceived: Mapping Behavioral Bias Susceptibility Across Ten Large Language Models"

### K.2 Abstract (Placeholder Version)

- [x] Draft abstract — mark all result claims as [PLACEHOLDER]:

> "Large language model (LLM) agents are increasingly deployed in high-stakes economic decision environments including procurement, supplier selection, and contract negotiation. Whether these agents inherit the behavioral biases well-documented in human economic psychology — anchoring, framing effects, decoy distortions, scarcity-induced urgency, and sunk cost fallacies — remains an open empirical question with direct implications for AI system design and deployment policy. We introduce BuyerBench Pillar 2, a controlled-variant evaluation framework that administers matched economic decision scenarios to LLM agents, varying only the psychological manipulation while holding underlying economics constant. We apply this framework to [10] commercially available LLM-based agents across five canonical bias categories, running [N] independent trials per agent-bias cell to characterize both mean susceptibility and stochastic variance. We find that [PLACEHOLDER: key finding about which biases appear, which models are most susceptible, and how susceptibility varies]. Bias susceptibility is neither universal nor absent — it is heterogeneous across bias type and model family, with [PLACEHOLDER] explaining [X%] of cross-model variance. These findings have implications for the design of AI procurement agents and the use of LLMs as synthetic respondents in economic experiments."

### K.3 Introduction Draft

- [x] Write introduction (~800 words) with these required elements:

> **[ECONOMIC HOOK — DRAFT]**
> The global procurement software market exceeds $9 billion annually, and AI-powered buyer agents — systems that autonomously evaluate suppliers, compare quotes, and execute purchasing decisions — are moving from prototype to production deployment. Unlike a human procurement officer who may consult a manager or seek second opinions on large decisions, an AI agent typically acts autonomously at the moment of its optimization. If that optimization is subject to systematic cognitive biases, the economic costs compound with scale: an agent anchoring on a high reference price, persistently overweighting sunk costs, or selecting suboptimal suppliers due to decoy options embedded in catalogs may impose substantial and invisible efficiency losses across thousands of transactions.

> **[RESEARCH QUESTION — DRAFT]**
> Whether LLM-based agents — the predominant architecture for AI buyer agents — exhibit systematic behavioral biases analogous to those documented in human economic psychology is an empirical question we cannot answer from first principles. Transformer architectures trained on human text might absorb human cognitive patterns; or instruction tuning and RLHF might scrub them; or the structure of the decision task might interact with model capability in unpredictable ways.

> **[WHAT WE DO — DRAFT]**
> We answer this question with BuyerBench Pillar 2, a controlled experimental framework designed along the lines of classical behavioral economics experiments but adapted for evaluating stochastic AI agents. The key methodological innovation is the controlled-variant design: for each bias type, we create matched scenario pairs in which the underlying economics (supplier qualities, prices, delivery reliability) are identical, but the presentation is manipulated to trigger a specific cognitive bias. The agent's behavioral inconsistency across matched pairs — measured as the Bias Susceptibility Index (BSI) — is our primary dependent variable.

> **[CONTRIBUTION STATEMENT — DRAFT]**
> This paper makes three contributions. First, it introduces BuyerBench Pillar 2 as a reproducible evaluation protocol for behavioral bias in LLM agents operating in economically structured settings. Second, it provides the first multi-model, multi-bias, stochasticity-aware empirical characterization of bias susceptibility across [10] commercial LLMs. Third, it identifies systematic patterns — [PLACEHOLDER: pattern description] — that have implications for the design and deployment of AI agents in procurement and related economic tasks.

### K.4 Methodology Key Passage — Bias Susceptibility Index (BSI)

- [x] Draft the formal BSI definition to appear in Section 3.5:

> **Definition (Bias Susceptibility Index):** Let $a^*(s)$ denote the economically optimal choice in scenario $s$, defined as the supplier maximizing the weighted utility function $U(q_i, d_i, p_i; w)$ where $q_i$, $d_i$, $p_i$ are quality, delivery reliability, and price of supplier $i$, and $w$ is the evaluation weight vector specified in the scenario. Let $a_{m,s,r}$ denote the choice made by model $m$ in scenario $s$ on run $r$. The **Bias Susceptibility Index** for a model in a treatment scenario $s_T$ relative to its baseline $s_B$ is:
>
> $$BSI(m, b) = \frac{1}{R} \sum_{r=1}^{R} \left[ \mathbf{1}[a_{m,s_T,r} \neq a^*(s_T)] - \mathbf{1}[a_{m,s_B,r} \neq a^*(s_B)] \right]^+$$
>
> where $[\cdot]^+$ denotes the positive part (we measure *additional* error induced by the manipulation, not baseline error).
>
> $BSI \in [0, 1]$: $BSI = 0$ indicates the model is no more likely to err under the biasing manipulation than in the baseline; $BSI = 1$ indicates the model always errs under manipulation but never in baseline.

- [x] NOTE: Review this definition against the current `evaluators/pillar2.py` implementation and reconcile any discrepancies.
  > **⚠️ Discrepancy found.** The `compute_bias_susceptibility` function at `evaluators/pillar2.py:95` computes `bsi = int(decision_changed) * (1.0 - baseline_score_obj.score)`. This gives BSI=0 when baseline was correct and treatment caused an error (the canonical bias case), and BSI=1 when baseline was already wrong and the decision changed — the inverse of the paper formula. The correct implementation is `bsi = max(0.0, variant_error - baseline_error)` where `error = 1 - score`. This must be fixed before running the full experiment. Full analysis documented in `Working/PILLAR2-PAPER-DRAFT.md` Section K.4.

### K.5 Limitations Section Draft

- [x] Write limitations section (~400 words) including these required items:
  - Single domain (procurement supplier selection) — generalizability unknown
  - LLMs cannot receive monetary payoffs — "bias" is purely behavioral, not incentivized
  - Prompt sensitivity: results may change with minor wording changes — robustness check documented but not exhaustive
  - Model versioning: commercial APIs update without notice — results may not replicate on future model versions
  - Stochasticity: at N=50/cell we have moderate power for d≥0.5; smaller effects are not reliably detected
  - Training data contamination: if scenario text appeared in training data, responses may reflect memorization not genuine reasoning
  - No mechanism identification: we measure susceptibility but do not identify why biases appear or disappear
