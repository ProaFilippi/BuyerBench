---
type: reference
title: "Pillar 2 Working Paper — Submission Package Checklist"
created: 2026-04-17
tags:
  - pillar2
  - submission
  - working-paper
  - pre-registration
related:
  - '[[pillar2-working-paper]]'
  - '[[PAPER-STATUS]]'
  - '[[prereg_osf]]'
  - '[[review-notes-week7]]'
---

# Pillar 2 Working Paper — Submission Package Checklist

Pre-submission requirements for `docs/paper/pillar2-working-paper.md`.

---

## Status as of Week 8 Revision (2026-04-17)

| Item | Status | Notes |
|---|---|---|
| Section 1 Introduction | **Done** | REV-7 scope statement, contributions, outline |
| Section 2 Related Work | **Done** | Human biases, LLM bias lit, procurement AI, methodology rigor |
| Section 3 Methodology | **Done** | H4/H6 gaps documented; H2 direction reconciled |
| Section 4 Results | **Template** | All `{{RESULT:...}}`; tier labels stripped (Week 8) |
| Section 5 Discussion | **Draft** | Written Week 8; 5.1–5.5 complete; power analysis in 5.2 |
| Section 6 Conclusion | **Draft** | Written Week 8; templated for final results |
| Appendix A Pre-reg Deviations | **Stub** | Fill post-experiment |
| Appendix B Pre-registration | **Draft** | Full H1–H10 table; confirmatory/exploratory split |
| Appendix C Scenario YAML | **Draft** | All 16 scenario pairs listed |
| Appendix D Robustness Checks | **Draft** | D.1–D.4 complete |
| Appendix E Model Versions | **Stub** | Fill at experiment execution |
| References / BibTeX | **Done** | All 10 missing keys added (Week 8) |

---

## Gate-Blocked Items (require data)

The following items cannot be completed until the N=50 pre-registered experiment has run:

- [ ] Replace all `{{RESULT:...}}` placeholders in Sections 4, 5.1, 5.2, 6, Appendix D
- [ ] Fill Appendix A (pre-registration deviations, if any)
- [ ] Fill Appendix E (pinned model versions)
- [ ] Confirm prompt sensitivity REV-5 gate verdict (requires real-model robustness pilot)
- [ ] Confirm Gate 1 verdict (requires `OPENROUTER_API_KEY` + pilot_full run)
- [ ] Complete Gate 3 verdict (requires N=50 full experiment)
- [ ] Compute actual Spearman ρ for H2 (Section 4.6, 5.2)

---

## Pre-Submission Checklist (content)

### Claim Integrity

- [x] All `[TIER-X]` labels stripped; replaced with in-text hedges
- [x] Section 5 Discussion written (5.1 H1–H7 verdicts, 5.2 implications, 5.3 scope limitations, 5.4 pre-reg deviations, 5.5 future work)
- [x] Section 6 Conclusion written
- [x] H4 deferral note in Section 3.4 (requires p2-01b, not yet implemented)
- [x] H6 added to Section 3.4 exploratory list
- [x] H2 direction reconciled (pre-reg = negative; main text clarifies both directions theoretically motivated; exploratory)
- [x] Power analysis for Spearman ρ at N=10 stated in Sections 3.4 and 5.2 (~40% at ρ=0.5)
- [x] "Boundary-response mechanism" scoped to "pre-specified interpretive frame, not confirmed mechanism" in abstract and Discussion 5.1
- [ ] All `{{RESULT:...}}` placeholders replaced with actual data
- [ ] Abstract updated to final empirical findings (remove placeholder blocks)

### References

- [x] `@tversky1974judgment` added to references.bib
- [x] `@ariely2003coherent` added
- [x] `@simonson1989choice` added
- [x] `@thaler1980toward` added
- [x] `@loken2017measurement` added
- [x] `@simmons2011false` added
- [x] `@opensciencecollaboration2015` added
- [x] `@greenwald1976within` added
- [x] `@binz2023using` added
- [x] `@camerer1999effects` added
- [ ] Verify all `arXiv:xxxx.xxxxx` placeholder DOIs resolved (see bib entries with `arXiv:2402.xxxxx`, `arXiv:2401.xxxxx`, `arXiv:2404.xxxxx`)
- [ ] Verify `@echterhoff2024anchoring` arXiv ID (currently `arXiv:2402.xxxxx` — verify actual ID)

### OSF Pre-Registration

- [ ] Upload `docs/preregistration/prereg_osf.md` to OSF **before** running first data collection call
- [ ] Record OSF registration ID and URL in Appendix B.1
- [ ] Record codebase commit hash at registration (`git rev-parse HEAD`)
- [ ] Fill `[TBD]` OSF fields in working paper header and Appendix B.1

### Code and Data

- [ ] GitHub repository is public; replace `[org]` placeholder throughout paper
- [ ] `pip install -e ".[dev]"` runs on Python 3.11+
- [ ] `python -m buyerbench demo` completes without errors
- [ ] `pytest` passes 100% of tests (current: 2,414 passing)
- [ ] All scenario YAML files in repository (`scenarios/pillar2/`)
- [ ] Raw run records from N=50 experiment uploaded to data repository
- [ ] `docs/preregistration/prereg_osf.md` included in repository

### Formatting (for final submission)

- [ ] Author names filled in
- [ ] Figures generated from actual data (run `research/scripts/04_generate_figures.py`)
- [ ] Figures exported at ≥300 DPI PNG + PDF vector for camera-ready
- [ ] Paper compiles cleanly with pandoc/LaTeX (no undefined BibTeX keys)

---

## Venue Recommendations (Pillar 2 Focused)

| Venue | Fit | Notes |
|---|---|---|
| **arXiv** (econ.GN + cs.AI) | Excellent | First disclosure; arXiv-first strategy recommended |
| **JEBO** (J. Econ. Behav. Org.) | Excellent | Natural venue for behavioral economics computational replication |
| **Management Science** | Very Good | Broad readership; procurement / operations management interest |
| **Journal of Marketing Research** | Good | Consumer behavior / LLM bias angle |
| **NeurIPS D&B Track** | Good | If framed as benchmark contribution; June deadline |
| **EMNLP** | Good | LLM behavioral bias scope fits; June deadline |
| **ICML Workshop (FinML/Agentic)** | Good for early release | Lower bar; community feedback before journal submission |

**Recommended sequence:**
1. arXiv preprint (cs.AI + econ.GN) once N=50 data is collected and placeholders filled
2. JEBO or Management Science journal submission (3–6 month review cycle)
3. NeurIPS Datasets & Benchmarks as parallel conference track

---

## Anonymization Requirements (for double-blind venues)

- Remove author names and affiliations from header
- Replace GitHub URL with `https://github.com/[anonymized]/BuyerBench` or supplementary only
- Replace `[org]` GitHub placeholder consistently before anonymizing
- Omit or replace acknowledgments section
- Verify `@buyerbench2026` self-citation does not reveal author identity in double-blind context
