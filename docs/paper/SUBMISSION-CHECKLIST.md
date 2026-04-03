---
type: reference
title: BuyerBench Paper — Submission Checklist
created: 2026-04-03
tags:
  - paper
  - submission
  - venues
related:
  - '[[buyerbench-paper]]'
  - '[[PAPER-STATUS]]'
---

# BuyerBench Paper — Submission Checklist

Pre-submission checklist and venue comparison for the BuyerBench research paper.

---

## General Pre-Submission Checklist

### Content

- [ ] All TBD/placeholder text resolved (`[TBD]`, `[Author list TBD]`, `[org]`)
- [ ] Abstract states key empirical findings (not "we will evaluate")
- [ ] All figures have captions and are referenced from the text
- [ ] All tables are numbered and referenced from the text
- [ ] All in-text citations have corresponding BibTeX entries
- [ ] BibTeX entries have correct DOIs / arXiv IDs (not `xxxxx` placeholders)
- [ ] Appendix A scenario taxonomy matches the actual scenario suite
- [ ] Results section findings connect explicitly to Introduction RQ1/RQ2/RQ3

### Code and Data

- [ ] GitHub repository is public and URL is live
- [ ] `pip install -e ".[dev]"` runs cleanly on a fresh Python 3.11+ environment
- [ ] `python -m buyerbench demo` runs to completion without errors
- [ ] `pytest` passes 100% of tests
- [ ] All 18 scenario YAML/JSON files are in the repository
- [ ] `results/experiments/FULL-REPORT.json` reflects the final evaluation run
- [ ] Figures in `docs/paper/figures/` are ≥300 DPI PNG

### Formatting

- [ ] Figure files are provided in both PNG (300 DPI) and PDF/vector format
- [ ] Paper compiles cleanly with pandoc or LaTeX (no undefined references)
- [ ] Word count fits within venue page limit (see per-venue notes below)

---

## Venue Comparison

### arXiv (cs.AI + cs.IR cross-list)

| Property | Value |
|----------|-------|
| Deadline | Rolling (submit anytime) |
| Page limit | None |
| Anonymization | Not required |
| Review | None (public preprint) |
| Format | PDF (LaTeX or pandoc) |
| Code requirement | Encouraged; no formal requirement |
| **Fit** | **Excellent** — first public disclosure; establishes priority; enables community feedback before conference submission |

**Recommended action:** Submit to arXiv first (cs.AI primary, cs.IR + cs.CY secondary) to establish priority and invite community contributions, then submit to a venue below.

---

### NeurIPS Datasets & Benchmarks Track

| Property | Value |
|----------|-------|
| Typical deadline | June (for December conference) |
| Page limit | 9 pages (+ unlimited references) |
| Anonymization | Double-blind |
| Review | 3 reviewers, rebuttal |
| Format | NeurIPS LaTeX style |
| Code requirement | Required; must include reproducibility checklist |
| **Fit** | **Excellent** — dedicated benchmark/dataset track; evaluates novelty of benchmark design, quality of scenarios, and reproducibility |

**Preparation notes:**
- Anonymize author list and GitHub URL for initial submission
- Complete the NeurIPS reproducibility checklist (license, code availability, hyperparameters, seeds)
- 9-page limit requires condensing Discussion §5.2 and §5.4 (see PAPER-STATUS.md word counts)
- Reviewers will expect CLI agent results; plan evaluation run before submission deadline

---

### EMNLP (Main or Findings)

| Property | Value |
|----------|-------|
| Typical deadline | June (for November conference) |
| Page limit | 8 pages (Findings: 4) |
| Anonymization | Double-blind |
| Review | 3 reviewers |
| Format | ACL LaTeX style |
| Code requirement | Encouraged; artifact evaluation track |
| **Fit** | **Good** — behavioral bias in LLMs is within NLP scope; the framing/anchoring results are linguistically motivated; benchmark paper format is acceptable |

**Preparation notes:**
- Focus on the behavioral bias (Pillar 2) angle for EMNLP positioning
- CLI agent results (BSI measurements) are needed to make the P2 case
- Artifact evaluation badge requires repository passes CI

---

### ACL Rolling Review (ARR) → ACL / NAACL / EACL

| Property | Value |
|----------|-------|
| Deadline | Rolling monthly |
| Page limit | 8 pages |
| Anonymization | Double-blind |
| Review | 3 reviewers; commitment to venue after reviews |
| Format | ACL LaTeX style |
| Code requirement | Encouraged |
| **Fit** | **Good** — especially for NAACL (AI applications focus) or ACL System Demonstrations track |

---

### ICML (Workshops)

| Property | Value |
|----------|-------|
| Typical deadline | April (for July conference) |
| Page limit | 4–8 pages (workshop-dependent) |
| Anonymization | Often single-blind |
| Review | Program committee |
| Format | ICML or custom LaTeX |
| **Fit** | **Good for workshops** — "ML for Finance" or "Agentic AI" workshop; lower bar than main track; good venue for early-stage benchmark results |

**Relevant workshops (recurring):**
- FinML — Machine Learning for Finance
- AgentWorkshop — Agentic AI Evaluation
- RTML — Reliable ML in the Wild

---

### IEEE S&P (Security Track) or ACM CCS

| Property | Value |
|----------|-------|
| Deadline | Annual (S&P: Dec/Apr cycles; CCS: Jan/Apr) |
| Page limit | 12–18 pages |
| Anonymization | Double-blind |
| Review | Rigorous (3+ reviews, shepherd) |
| Format | IEEE or ACM style |
| **Fit** | **Good for Pillar 3 angle** — payment security, PCI DSS evaluation, prompt injection resistance are core security topics; positions BuyerBench as a security evaluation tool |

**Preparation notes:**
- For security venues, foreground the Pillar 3 design and PCI DSS/EMV 3DS operationalization
- Frame as "security evaluation methodology" rather than "AI capability benchmark"
- Needs strong adversarial scenario results (prompt injection, fraud detection)

---

## Recommended Submission Sequence

1. **Immediate:** Submit to arXiv once CLI agent results are available (establishes priority)
2. **Near-term:** Submit to NeurIPS Datasets & Benchmarks (June deadline; high-impact venue for the benchmark framing)
3. **Contingency:** Submit to EMNLP Findings (lower bar; faster turnaround) if NeurIPS is rejected

---

## Anonymization Requirements

For double-blind venues, the following must be anonymized:

- Author names and affiliations (in paper header)
- GitHub URL — use `https://github.com/[anonymized]/BuyerBench` or submit as supplementary material only
- Any self-citations that reveal author identity — check references for authored work
- Acknowledgments section — omit or replace with "omitted for blind review"
- System-identifying details in agent evaluation tables (if running against your own systems)
