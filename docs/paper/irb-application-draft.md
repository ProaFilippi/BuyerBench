---
type: reference
title: "IRB Application Draft — BuyerBench Human Comparison Arm"
created: 2026-04-17
tags:
  - irb
  - human-arm
  - human-subjects
  - prolific
  - flagship
related:
  - '[[pillar2-working-paper]]'
  - '[[prereg_osf]]'
  - '[[prolific_config]]'
---

# IRB Application Draft
## BuyerBench Pillar 2 — Human Comparison Arm
### Procurement Decision-Making Study

> **Status:** Draft — ready for institutional submission.  
> **Anticipated review category:** Exempt (45 CFR 46.104(d)(2) — survey/interview research, no identifiable private information, no sensitive topics).  
> **Action required before submission:** Fill in all `[PLACEHOLDER]` fields with institution-specific information. Attach `survey_A_baseline.json` and `survey_B_treatment.json` (exported to PDF/DOCX for review board) and this narrative.

---

## Section 1 — Title and Investigators

| Field | Value |
|---|---|
| **Protocol title** | Procurement Decision-Making: An Online Behavioral Survey Study |
| **Short title (for IRB tracking)** | BuyerBench-P2-HumanArm-v1 |
| **Principal Investigator** | [PLACEHOLDER: PI Full Name], [PLACEHOLDER: Title], [PLACEHOLDER: Department], [PLACEHOLDER: Institution] |
| **Co-Investigators** | [PLACEHOLDER: Co-PI names if any] |
| **Faculty Sponsor** | [PLACEHOLDER: Required if PI is a student] |
| **Study start date (requested)** | [PLACEHOLDER: Date — must be after IRB approval] |
| **Study end date (requested)** | [PLACEHOLDER: Estimated 3 months after start] |
| **Funding source** | [PLACEHOLDER: Grant number / "Unfunded" / "Departmental funds"] |
| **Contact email** | [PLACEHOLDER: PI institutional email] |

---

## Section 2 — Abstract / Study Summary

This study collects behavioral data from human participants on a series of structured procurement decision-making scenarios. Participants are presented with information about fictional suppliers (price per unit, delivery lead time, quality rating, reliability score) and asked to select the best supplier. The study is designed as a human comparison arm for a computational benchmark (BuyerBench) that evaluates large language model (LLM) agents on the same scenarios.

The study uses a between-subjects design: participants are randomly assigned to either a **baseline** version (neutral scenario presentation) or a **treatment** version (scenarios with controlled behavioral manipulations such as anchor prices, gain/loss framing, or scarcity cues). Within their assigned version, each participant sees all five scenario domains (anchoring, framing, decoy, scarcity, sunk cost).

**Purpose:** To establish a human behavioral baseline against which LLM agent decision-making quality can be compared.  
**Risk level:** Minimal — anonymous online survey, no sensitive information, no deception, no compensation above Prolific minimum rate.  
**Target N:** 100 adults (50 per survey version).  
**Duration:** 8–12 minutes per participant.  
**Platform:** Prolific (participant recruitment) + Qualtrics (survey instrument).

---

## Section 3 — Purpose and Scientific Background

### 3.1 Background

Behavioral economics has documented robust human decision-making biases — including anchoring effects (Tversky & Kahneman, 1974), loss aversion and framing effects (Kahneman & Tversky, 1979), decoy effects (Simonson, 1989), and scarcity effects — across a wide range of economic domains including consumer choice, negotiation, and procurement.

Recent work in AI has examined whether large language models (LLMs) exhibit analogous bias patterns when acting as decision-making agents (Binz & Schulz, 2023; Jones & Steinhardt, 2022; Echterhoff et al., 2024). However, a key methodological gap is the absence of directly comparable human data collected under equivalent experimental conditions.

### 3.2 Purpose

This study closes that methodological gap. Participants complete the same procurement selection scenarios used to evaluate LLM agents in the BuyerBench benchmark (Pillar 2). The resulting human Bias Susceptibility Index (BSI) scores — measuring the proportion of participants who deviate from the economically optimal choice under bias manipulations — serve as an interpretive anchor for LLM BSI scores.

### 3.3 Significance

Without a human baseline, it is unclear whether an LLM BSI of, say, 0.30 represents more or less bias susceptibility than a typical human. The human comparison arm enables the following analysis:

- Compare LLM BSI vs. human BSI per bias type (Hypothesis H10 in the pre-registration).
- Frame LLM findings as "LLMs show X% lower/higher bias rates than humans on [bias type] in this task."
- Assess whether higher-capability LLMs converge toward or diverge from human-level decision quality.

### 3.4 Pre-Registration

The human comparison arm is registered as **exploratory** Hypothesis H10 in the BuyerBench pre-registration document (OSF: [PLACEHOLDER: OSF DOI once registered]). The analysis plan is: independent two-sample comparison of LLM BSI vs. human BSI per bias type; effect size via Cohen's d; no multiple-comparisons correction (exploratory, pre-specified).

---

## Section 4 — Participant Population

### 4.1 Inclusion Criteria

- Age 18–65
- Fluent English speaker (self-reported)
- Prolific approval rate ≥ 95%
- At least 20 prior approved Prolific submissions (experienced platform users)
- Country of residence: UK, US, Australia, or Canada

### 4.2 Exclusion Criteria

- Age < 18 or > 65
- Approval rate < 95% on Prolific
- Fails ≥ 1 attention check embedded in the survey (excluded from analysis; counted against N)
- Completes the survey in < 3 minutes (speed-through indicator)

### 4.3 Rationale for Exclusions

**No domain-expertise screener:** The study is designed to capture naïve procurement decision intuitions, analogous to the LLM-as-agent setting where models are not trained specialists. Screening for procurement expertise would introduce a self-selection bias and reduce external validity for the LLM comparison.

**Prolific filters (English fluency, approval rate, N submissions):** Standard Prolific quality controls. Participants with low approval rates or few submissions tend to produce lower-quality data.

### 4.4 Sample Size Justification

**Target N = 100 (50 per version).**

The unit of analysis for the LLM comparison is the cell-level BSI (proportion choosing suboptimally). At N=50 per version, the standard error of a proportion p is SE = √(p(1−p)/N). For p=0.5 (maximum variance case), SE ≈ 0.071. This is sufficient to detect a BSI difference of 0.20 between humans and LLMs with 80% power at α=0.05 (two-sample z-test, one-tailed). Given that the LLM results will be pre-computed before human data collection, this is the relevant power target.

**Attention check exclusion buffer:** We recruit 120 participants to achieve 100 valid responses (assuming ~15% attention check failure rate based on comparable Prolific survey studies).

---

## Section 5 — Study Procedures

### 5.1 Recruitment

Participants are recruited via Prolific (prolific.com) using the study description below. Two simultaneous studies are posted: one for Survey Version A (BASELINE) targeting N=60, one for Survey Version B (TREATMENT) targeting N=60. Prolific randomly presents studies to eligible participants who choose to enroll.

**Prolific study title:** "Procurement Decision-Making Study (10 min)"

**Prolific description:**
> We are studying how people make purchasing decisions in professional procurement contexts. You will be presented with a series of supplier selection scenarios and asked to choose the best supplier based on the information provided. There are no right or wrong answers — we are interested in your natural decision-making process. The study takes approximately 8–12 minutes. Reward: £1.50 for completing the full study.

### 5.2 Consent

Participants read an information screen (the consent equivalent for anonymous online surveys) before proceeding. The information screen informs participants that:

- The study is about purchasing decision-making.
- Participation is voluntary and they may withdraw at any time.
- Responses are anonymous; no personally identifiable information is collected.
- The data may be published in academic research.
- Contact information is provided for questions.

By clicking "Next" on the information screen, participants indicate informed assent to participate. See **Section 9** for the full information screen text.

### 5.3 Survey Protocol

The survey is administered via Qualtrics. The survey flow is:

1. **Information screen** (consent / participant rights) — 1 page
2. **Attention check 1 (ATTN1):** "Which of the following prices is higher: $12 or $89?" (correct: $89) — 1 question
3. **Scenario 1:** Anchoring domain (Version A = BASELINE; Version B = ANCHOR_HIGH manipulation)
4. **Scenario 2:** Framing domain (Version A = GAIN framing; Version B = LOSS framing)
5. **Attention check 2 (ATTN2):** "Please select 'Option C' for this question to confirm you are reading carefully." (correct: Option C) — 1 question
6. **Scenario 3:** Decoy domain
7. **Scenario 4:** Scarcity domain
8. **Scenario 5:** Sunk cost domain
9. **Brief demographics (optional, 3 questions):** Age range (7 bands: 18–24, 25–34, 35–44, 45–54, 55–64, 65+, prefer not to say), highest education level (5 levels), have you made purchasing decisions at work? (Yes/No/Occasionally)
10. **Debrief screen** (post-task, no deception used so standard completion message)

Each scenario presents:
- A procurement task framing (e.g., "You are selecting a supplier for office equipment")
- A table of 3–8 fictional suppliers with price, delivery time, quality rating, and reliability score
- A forced-choice question: "Which supplier would you select?"
- One follow-up: "How confident are you in this choice?" (5-point Likert)

**Scenario instruments:** See `survey/survey_A_baseline.json` and `survey/survey_B_treatment.json` (Qualtrics QSF format). These are the exact instruments used in the Prolific study.

### 5.4 Compensation

£1.50 per participant (~$1.90 USD), paid via Prolific automatic payment on completion. This equals approximately £9/hour, above Prolific's minimum recommended rate of £6/hour.

**Total estimated cost:** £180 for 120 recruited participants (+ Prolific service fee ≈ 33%, total ≈ £240 / ~$300 USD).

### 5.5 Data Collection Duration

Estimated 2–4 weeks for full recruitment at standard Prolific throughput for these eligibility criteria.

---

## Section 6 — Risks and Benefits

### 6.1 Anticipated Risks

**Risk level: Minimal.**

- The survey content is non-sensitive: fictional procurement scenarios involving supplier price and delivery time data. No health, financial, political, legal, religious, or sexual content is involved.
- No deception is used. Participants are informed they are in a decision-making study.
- No personally identifiable information (PII) is collected. Prolific assigns an anonymous participant ID that is not linked to name, email, or other identifiers.
- No physical risk. The survey is completed online at the participant's discretion.
- Potential for minor frustration or boredom (minimal, ~10-minute task).

### 6.2 Anticipated Benefits

**Direct benefits to participants:** None beyond compensation (£1.50).  
**Benefits to science:** Establishes a human behavioral benchmark for AI agent evaluation, enabling rigorous comparison of LLM decision-making quality against human baselines. Contributes to the emerging field of AI behavioral evaluation methodology.

### 6.3 Risk/Benefit Assessment

The risks are minimal and the study involves no sensitive information, deception, or vulnerable populations. The scientific benefit of establishing a human baseline for AI agent evaluation justifies the minor inconvenience of participation.

---

## Section 7 — Confidentiality and Data Management

### 7.1 Data Collected

- Qualtrics survey responses (supplier selections, confidence ratings, 3 optional demographic questions)
- Prolific participant ID (anonymous random string, not linked to real identity)
- Qualtrics metadata: response timestamp, duration, device type (no IP address stored if Qualtrics anonymization is enabled)
- Attention check responses

**What is NOT collected:**
- Name, email address, or contact information
- IP address (Qualtrics anonymization enabled)
- Geolocation beyond Prolific-reported country of residence
- Financial information
- Any information about AI or LLM systems (participants are not informed this is an AI study)

### 7.2 Data Storage

- Qualtrics data: stored on institutional Qualtrics instance ([PLACEHOLDER: institution's Qualtrics server or cloud]) with access restricted to PI and co-investigators
- Exported CSV: stored on encrypted institutional storage ([PLACEHOLDER: e.g., OneDrive/Box/institutional server]) accessible only to study team
- Prolific dashboard: accessible only via PI's Prolific account

### 7.3 Data Retention

Survey data will be retained for a minimum of 5 years after publication, per standard academic research data retention requirements. Data may be deposited in a public data repository (OSF, Zenodo) as an anonymized CSV without Prolific IDs, in support of open science practices.

### 7.4 Publication Plan

Individual participant responses will not be published. Only aggregate statistics (proportion choosing each option, mean confidence, BSI per scenario) will appear in publications. The anonymized response-level CSV (without Prolific IDs) may be released as supplementary data.

---

## Section 8 — Special Populations

This study does not involve any special populations requiring additional protections:

- **Children:** Excluded (Prolific eligibility requires age 18+)
- **Prisoners:** Not eligible via Prolific
- **Pregnant persons:** Not excluded, no physical risk
- **Cognitively impaired individuals:** Not targeted; standard eligibility criteria
- **Students at [PLACEHOLDER: institution]:** Not specifically targeted; Prolific sampling draws from the general public

---

## Section 9 — Participant Information Screen (Consent Equivalent)

> ---
> **Study Title:** Procurement Decision-Making Study
>
> **Research Team:** [PLACEHOLDER: PI Name], [PLACEHOLDER: Department], [PLACEHOLDER: Institution]
>
> **What is this study about?**
> This research investigates how people make purchasing decisions when comparing supplier options. You will read short descriptions of procurement scenarios and choose which supplier you would select.
>
> **What will you be asked to do?**
> You will complete 5 short supplier selection scenarios and 2 brief attention checks. The study takes approximately 8–12 minutes.
>
> **Are there any risks?**
> This study involves no physical, psychological, financial, legal, or reputational risks. The scenarios are fictional and do not involve any real organizations or financial transactions.
>
> **Is participation voluntary?**
> Yes. Your participation is completely voluntary. You may stop at any time without penalty. If you withdraw after starting, your Prolific submission will be returned and you will receive no payment.
>
> **How will your privacy be protected?**
> Your responses are anonymous. We do not collect your name, email address, or any information that could identify you. Your Prolific participant ID is used only to verify completion and process payment; it is deleted from the research dataset before analysis.
>
> **Who funded this research?**
> [PLACEHOLDER: Funding source / "This research was not externally funded."]
>
> **Questions or concerns?**
> Contact the PI at [PLACEHOLDER: institutional email]. If you have concerns about your rights as a research participant, contact [PLACEHOLDER: IRB office contact information].
>
> **By clicking "Next" below, you confirm that you have read this information, that you are 18 years of age or older, and that you consent to participate in this study.**
> ---

---

## Section 10 — Debrief (Post-Completion)

No deception was used. Standard completion screen:

> **Thank you for completing the study!**
>
> Your responses have been recorded. This study is investigating how people make procurement decisions — specifically, how information presentation affects supplier selection choices.
>
> The scenarios you completed were part of a research project studying decision-making patterns. There are no "correct" answers — all responses are valuable.
>
> Your completion code for Prolific is: **[COMPLETION_CODE]**  
> Please return to Prolific and enter this code to receive your payment.
>
> If you have any questions about this research, please contact [PLACEHOLDER: PI email].

---

## Section 11 — Checklist for Submission

Before submitting to the IRB, ensure the following are attached or completed:

- [ ] This narrative document (as PDF)
- [ ] Qualtrics survey instruments (export each survey as PDF/DOCX): `survey_A_baseline.json` → PDF, `survey_B_treatment.json` → PDF
- [ ] IRB application form from [PLACEHOLDER: institution's IRB portal, e.g., eProtocol, IRBNet, ARROW, Kuali]
- [ ] PI CV or biosketch (typically required)
- [ ] CITI training certificate for PI and all co-investigators ([PLACEHOLDER: confirm active training in Human Subjects Research])
- [ ] Pre-registration URL ([PLACEHOLDER: OSF DOI — register at osf.io before data collection])
- [ ] Grant/funding approval (if externally funded)
- [ ] Signed departmental/faculty sponsor approval (if PI is a student)

---

## Section 12 — Exempt Status Justification

This study qualifies for **Exempt** status under **45 CFR 46.104(d)(2)** — Research involving the use of survey procedures where:

> "(i) The information obtained is recorded by the investigator in such a manner that the identity of the human subjects cannot readily be ascertained, directly or through identifiers linked to the subjects; (ii) any disclosure of the human subjects' responses outside the research would not reasonably place the subjects at risk of criminal or civil liability or be damaging to the subjects' financial standing, employability, educational advancement, or reputation; and (iii) the research does not involve the collection of sensitive aspects of the subject's own behavior."

All three criteria are satisfied:
1. **(i)** Prolific IDs are anonymous strings not linked to real identity; IDs are deleted before research dataset creation.
2. **(ii)** Scenario responses (fictional supplier selections) pose no legal, financial, employment, or reputational risk to participants.
3. **(iii)** The study content (supplier selection from fictional catalogs) is entirely non-sensitive.

---

## Section 13 — Timeline

| Milestone | Estimated Date |
|---|---|
| IRB submission | [PLACEHOLDER] |
| IRB approval (anticipated Exempt) | [PLACEHOLDER + 2–8 weeks] |
| Prolific study activation | Day after IRB approval |
| Data collection complete | Approval date + 2–4 weeks |
| Data exported and parsed | Within 1 week of collection complete |
| Human BSI results incorporated into paper | Within 2 weeks of data export |

> **Note:** LLM benchmark experiments do NOT require IRB approval and can proceed in parallel. IRB approval is only required before activating the Prolific study and collecting human data.

---

## References (for narrative)

- Binz, M., & Schulz, E. (2023). Using cognitive psychology to understand GPT-3. *PNAS*, 120(6).
- Camerer, C., & Hogarth, R. (1999). The effects of financial incentives in experiments. *Journal of Risk and Uncertainty*, 19, 7–42.
- Echterhoff, J., et al. (2024). Cognitive bias in high-stakes decision-making with LLMs. arXiv:2402.xxxxx.
- Kahneman, D., & Tversky, A. (1979). Prospect theory. *Econometrica*, 47(2), 263–291.
- Simonson, I. (1989). Choice based on reasons. *Journal of Consumer Research*, 16(2), 158–174.
- Tversky, A., & Kahneman, D. (1974). Judgment under uncertainty: Heuristics and biases. *Science*, 185(4157), 1124–1131.
