---
type: analysis
title: "Week 7 Internal Review — Pillar 2 Working Paper Red Team + Claim-Tier Audit"
created: 2026-04-17
tags:
  - pillar2
  - review
  - claim-tiers
  - red-team
related:
  - '[[pillar2-working-paper]]'
  - '[[PAPER-STATUS]]'
  - '[[PILLAR2-RESEARCH-07]]'
  - '[[prereg_osf]]'
---

# Week 7 Internal Review — Pillar 2 Working Paper

> **Purpose:** Red-team the draft from the perspective of a skeptical Experimental Economics / JEBO referee. Apply the N.2 claim-tier filter to every result-adjacent statement. Document all issues for Week 8 revision.

---

## 1. Structural Gaps (Critical — Block Submission)

### 1.1 Missing Sections 5 and 6

**Status:** Paper jumps from Section 4 (Results) directly to References. Sections 5 (Discussion) and 6 (Conclusion) are absent.

- Section 1.4 (Paper Outline) explicitly promises: "Section 5 discusses implications, limitations, and future work. Section 6 concludes."
- PAPER-STATUS.md marks both as **Pending**.
- **Action (Week 8):** Write both sections before submission prep.

Required content for Section 5:
- 5.1 Interpretation of H1–H7 verdicts (including robust-rationality pivot if H1 fails)
- 5.2 Implications for deployed buyer agent systems
- 5.3 Pipeline scope limitation (explicitly referenced in Section 3.1 "See Section 5.3")
- 5.4 Pre-registration deviations (if any; also Appendix A)
- 5.5 Future work: flagship expansion, human comparison arm, other procurement domains

### 1.2 Appendix D / E Ordering Bug

**Status:** Appendix E (Registered Model Versions) appears **before** Appendix D (Robustness Checks) in the file. Correct order: A → B → C → D → E.

- **Fixed in this review pass** (see Section 4 below).

### 1.3 Hard-Difficulty Scenarios Have No Results Section

**Status:** Table 2 footnote says hard variants (p2-09 through p2-11) "are reported separately" — but Section 4 contains no such subsection.

- Current sections: 4.1 (sample quality), 4.2 (H1), 4.3 (H3/H5), 4.4 (H7), 4.5 (regression), 4.6 (exploratory), 4.7 (robustness).
- **Action (Week 8):** Add Section 4.8 placeholder for hard-difficulty ceiling-effect results.

---

## 2. Claim-Tier Filter Violations

### 2.1 Abstract — Mixed Tier-A/B Claims in Single TIER-A Block

**Location:** Abstract, final paragraph (`[TIER-A PLACEHOLDER]` block).

**Violation:** "The decoy effect produces the highest mean BSI (`{{RESULT: mean_BSI_decoy}}`), **followed by `{{RESULT: second_highest_bias_type}}`**."

- "Decoy BSI > cross-bias mean" is **TIER-A** (confirmed by H3 one-sample t + Dunnett; pre-registered).
- "Followed by `{{RESULT: second_highest_bias_type}}`" — ranking which non-decoy bias type is second-highest — is **TIER-B** (descriptive pattern, N=10, no pre-registered test for this ordering). Placing it inside the TIER-A block is a tier contamination.
- **Fixed in this review pass**: moved second-highest to a hedged TIER-B sentence.

### 2.2 Abstract — "Boundary-Response Mechanism" Language

**Location:** Abstract, final sentence of TIER-A block: "consistent with a **boundary-response mechanism**."

**Issue:** A mechanistic explanation (why variance and BSI correlate) approaches TIER-C territory. H7 is confirmatory, but the *mechanism* interpretation is theoretically motivated, not confirmed by the data. A strict referee will flag "mechanism" as over-claim.

**Mitigation applied:** Added parenthetical "(pre-specified interpretive frame for H7; mechanism not directly tested)" to make the scope explicit. This is the weakest permissible language for a TIER-A block.

**Residual concern for Week 8:** If the Discussion section uses "mechanism" language, it must be explicitly relegated to "speculation" or "consistent with" framing and labeled TIER-C in that context.

### 2.3 Section 4.1 — No Tier Label on Section Header

**Location:** `### 4.1 Sample Quality and Descriptive Statistics`

**Issue:** Table 3 (execution summary) is execution metadata — no tier claim needed. Table 4 (per-model descriptives) is explicitly labeled `[TIER-B]`. But the section header itself carries no label, creating ambiguity about whether execution-summary claims (Gate 1 verdict) are Tier-A or Tier-B.

- Gate 1 verdict ("Infrastructure verdict: proceed if error rate < 5%...") is Tier-A infrastructure — it's a pre-specified go/no-go criterion, not an interpretive claim.
- **Fixed in this review pass**: added `[TIER-A: execution gate / TIER-B: per-model descriptives]` to section header.

### 2.4 Section 4.7 — Prompt Sensitivity Result Has No Tier Label

**Location:** `### 4.7 Robustness Checks` — "**Prompt sensitivity (REV-5):**" paragraph.

**Issue:** The REV-5 gate verdict ("All CV values are reported in Appendix D") has no tier label. This is a pre-specified methodological gate — Tier-A infrastructure (go/no-go, not an interpretive claim). Without a label, readers cannot distinguish this gate from a Tier-B pattern.

**Fixed in this review pass**: added `[TIER-A: pre-specified REV-5 gate]` to the prompt sensitivity line.

---

## 3. Analysis Plan Gaps

### 3.1 H4 (Anchor Magnitude) — Absent from Section 3.4

**Location:** Section 3.4, "Confirmatory analyses" and "Exploratory analyses" lists.

**Issue:** H4 appears in pre-reg Appendix B.7 as exploratory, flagged "(not yet implemented: p2-01b missing)" — but is not mentioned anywhere in the main analysis plan (Section 3.4). This creates an internal inconsistency.

- H4 requires a second anchoring variant (p2-01b, low anchor) not yet implemented.
- A referee reading Section 3.4 will be confused by H4's appearance in Table B.7 without mention in the main plan.
- **Action (Week 8):** Add a brief note in Section 3.4 Exploratory analyses: "H4 (Anchor Magnitude) requires a low-anchor variant (p2-01b, not yet implemented); this hypothesis is deferred to the flagship expansion (Section 5.5)."

### 3.2 H6 (Sunk Cost–Capability Correlation) — Absent from Section 3.4

**Location:** Section 3.4, Exploratory analyses list.

**Issue:** H6 (Spearman ρ for p2-05 specifically; opposite direction from H2) is in Table B.7 but absent from Section 3.4's exploratory list. Readers of the main text will not know H6 is planned.

- **Action (Week 8):** Add H6 to the Section 3.4 exploratory list: "H6 (Sunk Cost Capability Correlation): Spearman ρ between Pillar 1 score and p2-05 BSI specifically (pre-specified counter-direction to H2); descriptive, N=10."

---

## 4. Minor Consistency and Wording Issues

### 4.1 Section 5.3 Self-Reference Without Section Existing

**Location:** Section 3.1: "Upstream pipeline components... are not evaluated. This scope choice enables clean identification of the bias signal... See Section 5.3 for limitations arising from this scope restriction."

- Section 5.3 does not exist yet (Section 5 is Pending).
- **Acceptable pre-write:** This is a draft; forward references to pending sections are fine. Document for Week 8 as a "must write" target.

### 4.2 Section 4.6 H2 — Theoretically Motivated Both Directions

**Location:** Section 4.6 H2 note: "both a negative... and positive... correlation are theoretically motivated; neither direction constitutes a pre-specified confirmatory prediction."

**Assessment:** This is correctly handled. The pre-reg (B.7) does register H2 as "negative" direction, but also marks it exploratory. This minor inconsistency (pre-reg says "negative direction" but main text says "neither direction pre-specified") should be reconciled.

- **Action (Week 8):** Update H2 text to: "H2 is pre-registered as negative direction (higher capability → less bias), but is exploratory; the reverse has also been reported [@hagendorff2023human], so the result is interpreted descriptively regardless of direction."

### 4.3 Human d Comparison in Table (Section 4.7 / H10)

**Assessment:** The table comparing human meta-analytic d to LLM BSI includes "LLM d (approx.)" column. The footnote correctly notes this is "illustrative and does not constitute a formal test." This is properly hedged as TIER-B. No change needed, but Week 8 Discussion (Section 5) should explicitly call this out as a theoretical calibration exercise.

### 4.4 References — Missing Section Numbers in Some Citations

**Minor:** Some inline `[@citation]` references in Section 2.1 use BibTeX keys that may not exist in `references.bib`. Before submission, verify all citation keys against `docs/paper/references.bib`.
- Observed potentially unverified keys: `@binz2023using`, `@scherrer2024moral` (used in 2.2), `@loken2017measurement` (2.4 and 2.2).
- The paper imports `@opensciencecollaboration2015` — unusual key format; verify.

---

## 5. Red Team Referee Simulation

Simulating a JEBO/Management Science referee review of the current draft (prior to Sections 5–6 completion):

**Objection R1:** "Your abstract claims N=50 results but Section 4 is entirely `{{RESULT:...}}` placeholders. This submission is not ready — you're submitting a research design, not results."
- **Response:** Working paper status is explicit. The abstract version note says "full results will be reported at the pre-specified N=50." This is appropriate for a pre-registered working paper circulated before data collection.
- **Mitigation:** Ensure the "Working paper" header and version note are highly visible.

**Objection R2:** "You have 10 models in Section 4.6 but call it 'cross-model patterns.' That's not a pattern — that's a description of 10 data points."
- **Response:** Section 4.6 correctly labels all analyses TIER-B with the blockquote warning: "No p-values on cross-model comparisons should be interpreted as inferential evidence." This is the right framing.
- **Mitigation:** Week 8 Discussion must reiterate that cross-model findings are explicitly not inferential.

**Objection R3:** "Your H1 is circular — you define 'bias' as deviation from your own rubric."
- **Response:** REV-1 is already implemented: the paper consistently frames this as "internal rationality" against the stated objective function. The scope statement in the abstract, Section 1.2, Section 3.1, and Section 3.3 all reiterate this.
- **Mitigation:** Check that the Discussion (Section 5.1) explicitly revisits this when interpreting H1.

**Objection R4:** "Your N=50 is insufficient for a reliable Spearman ρ on N=10 model observations."
- **Response:** The paper already acknowledges N=10 is below inference threshold for cross-model analyses (TIER-B everywhere).
- **Mitigation:** Explicitly compute the power of Spearman ρ at N=10 in the Discussion. (For ρ=0.5, N=10 gives ~40% power — barely better than chance. This must be stated.)

**Objection R5:** "The TIER-A/TIER-B/TIER-C system is internal methodology scaffolding. A submitted paper should not contain these labels."
- **Response:** These labels serve as author-side quality control during draft writing. They must be **removed before submission** and replaced with appropriate hedging language in-text.
- **Action (Week 8):** Strip all `[TIER-X]` labels from results text; replace with in-text hedges ("In a descriptive analysis of N=10 models...", "Pre-registered confirmatory analysis yields...").

---

## 6. Changes Applied in This Review Pass

| # | Location | Change |
|---|---|---|
| 1 | Appendix ordering | Swapped E and D so D (Robustness Checks) precedes E (Model Versions) |
| 2 | Abstract TIER-A block | Separated "second highest bias type" into hedged TIER-B sentence |
| 3 | Abstract TIER-A block | Added parenthetical to "boundary-response mechanism" limiting claim scope |
| 4 | Section 4.1 header | Added tier clarification `[TIER-A: execution gate / TIER-B: per-model descriptives]` |
| 5 | Section 4.7 prompt sensitivity | Added `[TIER-A: pre-specified REV-5 gate]` label |
| 6 | Section 4.8 (new) | Added placeholder subsection for hard-difficulty ceiling scenario results |
| 7 | PAPER-STATUS.md | Updated open issues with Week 7 review findings |

---

## 7. Action Items for Week 8

| Priority | Item | Section |
|---|---|---|
| **P0** | Write Section 5 (Discussion) — 5.1–5.5 | § 5 |
| **P0** | Write Section 6 (Conclusion) | § 6 |
| **P0** | Strip `[TIER-X]` labels; replace with in-text hedges | § 4 throughout |
| **P1** | Add H4 deferred-to-flagship note in Section 3.4 | § 3.4 |
| **P1** | Add H6 to Section 3.4 exploratory list | § 3.4 |
| **P1** | Reconcile H2 direction: pre-reg says "negative"; main text says "neither" | § 4.6 |
| **P1** | Verify all BibTeX citation keys against `references.bib` | References |
| **P2** | Compute and report power of Spearman ρ at N=10 in Discussion | § 5 |
| **P2** | Finalize author list and OSF pre-registration URL | Abstract |
| **P2** | Replace `[org]` GitHub URL placeholder | Abstract |
