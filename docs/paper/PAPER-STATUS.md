---
type: note
title: BuyerBench Paper — Section Writing Status
created: 2026-04-03
tags:
  - paper
  - status
related:
  - '[[buyerbench-paper]]'
  - '[[FIGURE-PLAN]]'
---

# BuyerBench Paper — Section Writing Status

Section-by-section tracker for the BuyerBench research paper (`buyerbench-paper.md`).

## Status Legend

| Status | Meaning |
|--------|---------|
| **Draft** | Initial text written; content complete but not polished |
| **Review** | Draft complete; internal review pass underway |
| **Done** | Finalized and ready for submission |
| **Pending** | Not yet started; depends on results or other sections |
| **Stub** | Placeholder headings only |

---

## Section Status Table

| Section | Subsection | Status | Word Count (approx.) | Notes |
|---------|-----------|--------|----------------------|-------|
| Abstract | — | **Done** | ~220 | TBD placeholders filled with actual results |
| 1. Introduction | Motivation | **Done** | ~400 | Draws from RESEARCH-GAPS.md; 3 RQs stated |
| 1. Introduction | Contributions | **Done** | ~200 | All 4 contributions filled in, incl. empirical finding |
| 1. Introduction | Paper outline | **Done** | ~80 | Standard paragraph outline |
| 2. Related Work | AI Agent Evaluation | **Done** | ~350 | AgentBench, GAIA, SWE-bench, HELM contrasted |
| 2. Related Work | Behavioral Economics & AI Bias | **Done** | ~380 | 8-bias taxonomy; positions as first procurement-domain bias benchmark |
| 2. Related Work | Payment Security & Agentic Commerce | **Done** | ~280 | PCI DSS, EMV 3DS, AP2/UCP/ACP covered |
| 2. Related Work | Buyer Agent Systems | **Done** | ~300 | 23 agents catalogued; 6 categories |
| 3. Methodology | Benchmark Design Philosophy | **Done** | ~250 | Three-pillar rationale; multi-dimensional profiling |
| 3. Methodology | Scenario Design | **Done** | ~650 | 18-scenario taxonomy table; controlled variant example |
| 3. Methodology | Agent Interface & Harness | **Done** | ~400 | Prompt serialization, subprocess invocation, 3 modes; Fig 1 embedded |
| 3. Methodology | Evaluation Metrics | **Done** | ~500 | Formal definitions for P1/P2/P3 metric families |
| 3. Methodology | Evaluated Agents | **Done** | ~300 | CLI agents × 3 modes; NegMAS; Stripe; stubs |
| 4. Results | Overall Benchmark Results | **Done** | ~280 | Table 1: per-agent aggregate; NegMAS + Stripe; Fig 2 |
| 4. Results | Pillar 1 — Capability | **Done** | ~380 | Table 2: per-scenario breakdown; bimodal pattern explained; Fig ref |
| 4. Results | Pillar 2 — Economic Decision Quality | **Done** | ~220 | Table 3: pending placeholder; methodology validated |
| 4. Results | Pillar 3 — Security & Compliance | **Done** | ~460 | Table 4: full Stripe Toolkit breakdown; 4 key findings |
| 4. Results | Skills and MCP Impact | **Done** | ~200 | Table 5: pending; theoretical prediction stated |
| 5. Discussion | Key Findings | **Done** | ~480 | 5 findings; connected to RQ1/RQ2/RQ3 |
| 5. Discussion | Implications for Agent Design | **Done** | ~480 | PCI DSS, EMV 3DS, injection resistance; deployment implications |
| 5. Discussion | Limitations | **Done** | ~380 | 6 limitations documented; CLI credential gap noted |
| 5. Discussion | Future Work | **Done** | ~480 | 7 extensions prioritized |
| 6. Conclusion | — | **Done** | ~290 | Key empirical findings stated; contribution clear |
| References | — | **Done** | — | BibTeX in references.bib; ~38 entries; self-citation added |
| Appendix A | Scenario Taxonomy Table | **Done** | ~250 | Full 18-scenario table with metrics and pair IDs |
| Appendix B | Metric Formal Definitions | **Done** | — | Included inline in §3.4 |

---

## Word Count Summary

| Section | Target | Actual (approx.) |
|---------|--------|------------------|
| Abstract | ~200 | ~220 |
| Introduction | ~800 | ~680 |
| Related Work | ~1200 | ~1310 |
| Methodology | ~1500 | ~2100 |
| Results | ~1500 | ~1540 |
| Discussion | ~800 | ~1820 |
| Conclusion | ~300 | ~290 |
| **Total (excl. appendix)** | **~6300** | **~7960** |

Note: Discussion and Methodology exceed targets due to the depth of the findings analysis and the limitation/future-work sections. For venue submissions with strict page limits, the Discussion §5.2 (Implications) and Future Work §5.4 can be condensed.

---

## Phase Mapping

| Phase | Paper sections affected |
|-------|------------------------|
| Phase 09 | Abstract, Introduction, Related Work, Methodology |
| Phase 10 (complete) | Results, Discussion, Conclusion, Appendix A, references |

---

## Pillar 2 Working Paper (`pillar2-working-paper.md`)

Separate focused paper for the Pillar 2 pre-registered bias study.

| Section | Status | Notes |
|---|---|---|
| Abstract | **Review** | Tier-A/B separation applied (Week 7 review); "second highest bias type" moved to Tier-B sentence; "boundary-response mechanism" scoped to pre-specified frame |
| 1. Introduction | **Draft** | Motivation, scope (REV-7), contributions, limitations |
| 2. Related Work | **Draft** | Human biases, LLM bias lit, procurement AI, methodology rigor |
| 3. Methodology | **Draft** | Design, scenario battery, BSI formula, stats plan, robustness; H4/H6 gap noted for Week 8 |
| 4. Results | **Template** | All cells `{{RESULT:...}}`; tier labels audited (Week 7); Section 4.8 (hard-difficulty) added; requires N=50 experiment data |
| 5. Discussion | **Draft** | Written Week 8: 5.1 H1–H7 verdict interpretation (incl. robust rationality pivot), 5.2 deployment implications (incl. power analysis for H2), 5.3 pipeline scope limitations, 5.4 pre-reg deviations, 5.5 future work |
| 6. Conclusion | **Draft** | Written Week 8; templated on result placeholders; ready for data |
| Appendix A (Pre-reg deviations) | **Stub** | Filled post-experiment |
| Appendix B (Pre-registration document) | **Draft** | Full condensed pre-reg: metadata, design, sampling, variables, analysis plan, H1–H10 table, registered model set |
| Appendix C (Scenario YAML metadata) | **Draft** | Evaluation weights and δ table included |
| Appendix D (Robustness checks) | **Draft** | D.1–D.4 complete; ordering bug fixed (was placed after E, now correctly before E) |
| Appendix E (Model versions) | **Stub** | Filled at experiment execution time; ordering fixed (now correctly after D) |

---

## Open Issues

- [ ] Fill in author names once known
- [ ] Replace `[org]` placeholder in GitHub URL once repository is public
- [ ] Confirm venue/format target (NeurIPS Datasets & Benchmarks, EMNLP, or arXiv-first)
- [ ] Run CLI agents (Claude Code, Codex, Gemini) to populate P1/P2/P3 CLI results and update Tables 3, 5
- [ ] Add human baseline scores to Pillar 1 Results once pilot study runs
- [ ] Verify all BibTeX DOIs and arXiv IDs before submission
- [ ] Create .pdf and .svg exports of figures for camera-ready submission

### Pillar 2 Working Paper — Week 8 Priority Issues (from Week 7 review)

- [x] **P0** Write Section 5 (Discussion): 5.1 H1–H7 verdict interpretation, 5.2 deployment implications, 5.3 pipeline scope limitations, 5.4 pre-reg deviations, 5.5 future work (2026-04-17)
- [x] **P0** Write Section 6 (Conclusion) (2026-04-17)
- [x] **P0** Strip all `[TIER-X]` labels from result text; replaced with in-text hedges throughout Sections 4, Abstract (2026-04-17)
- [x] **P1** Add H4 deferred-to-flagship note in Section 3.4 (2026-04-17)
- [x] **P1** Add H6 (Sunk Cost–Capability correlation) to Section 3.4 exploratory list (2026-04-17)
- [x] **P1** Reconcile H2 direction: updated Section 3.4 and 4.6 to reflect pre-reg says "negative direction" but both directions theoretically motivated; result interpreted descriptively (2026-04-17)
- [x] **P1** Verified BibTeX keys; added 10 missing entries to `references.bib`: `@tversky1974judgment`, `@ariely2003coherent`, `@simonson1989choice`, `@thaler1980toward`, `@loken2017measurement`, `@simmons2011false`, `@opensciencecollaboration2015`, `@greenwald1976within`, `@binz2023using`, `@camerer1999effects` (2026-04-17)
- [x] **P2** Power analysis for Spearman ρ at N=10 stated in Sections 3.4 and 5.2 (~40% power for ρ=0.5) (2026-04-17)
- [ ] **P2** Register pre-registration on OSF; fill in OSF URL and commit hash in Appendix B.1 (manual step — requires OSF account)
- [ ] **P2** Finalize author list; replace `[Author list TBD]` placeholder
- [ ] **P2** Make GitHub repository public; replace `[org]` placeholder

### Human Comparison Arm (Flagship Month 3)

| Item | Status | Notes |
|---|---|---|
| Prolific survey instruments (QSF) | **Done** | `survey/survey_A_baseline.json`, `survey_B_treatment.json` |
| Prolific configuration guide | **Done** | `survey/prolific_config.md` — eligibility criteria, setup steps, data export |
| IRB application draft | **Draft** | `docs/paper/irb-application-draft.md` — ready for institutional submission; all `[PLACEHOLDER]` fields require institution-specific details |
| IRB submission | **Pending** | Manual step — requires PI/co-PI with active CITI training and institutional IRB portal access |
| IRB approval | **Pending** | ~2–8 weeks after submission (Exempt category anticipated) |
| Prolific study activation | **Pending** | Blocked until IRB approval |

---

### Remaining Gate-Blocked Items (require N=50 experiment data)

- [ ] Replace all `{{RESULT:...}}` placeholders with actual data
- [ ] Verify `@echterhoff2024anchoring` arXiv ID (currently placeholder `arXiv:2402.xxxxx`)
