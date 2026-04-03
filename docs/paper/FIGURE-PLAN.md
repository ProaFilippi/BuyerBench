---
type: note
title: BuyerBench Paper — Figure Plan
created: 2026-04-03
tags:
  - paper
  - figures
related:
  - '[[buyerbench-paper]]'
  - '[[PAPER-STATUS]]'
---

# BuyerBench Paper — Figure Plan

All planned figures for the BuyerBench research paper. For each figure: description, source notebook cell or script, placement in paper, and status.

---

## Figure List

| ID | Title | Description | Source | Placement | Status |
|----|-------|-------------|--------|-----------|--------|
| Fig 1 | BuyerBench Three-Pillar Architecture | Diagram showing the three evaluation pillars (P1 Capability, P2 Economic Rationality, P3 Security/Compliance) and their relationship to the scenario → agent → evaluator pipeline | Manual (draw.io or Mermaid) | §1 Introduction or §3 Methodology | Planned |
| Fig 2 | Harness Architecture Diagram | System diagram: scenario YAML → harness loader → prompt serializer → agent subprocess (3 modes: baseline/skills/MCP) → evaluator → EvaluationResult | Manual (draw.io or Mermaid) | §3.3 Agent Interface & Harness | Planned |
| Fig 3 | Scenario Taxonomy Overview | Visual taxonomy of 18 scenarios by pillar, variant type, and difficulty (heatmap or tree) | Manual or matplotlib from scenario YAML metadata | §3.2 Scenario Design | Planned |
| Fig 4 | Controlled Variant Methodology | Schematic of A/B variant pairs: same economic structure → two presentations → consistency check produces BSI | Manual (illustrative diagram) | §3.2 Scenario Design | Planned |
| Fig 5 | Per-Agent Radar Chart | Spider/radar chart with 3 axes (P1 mean, P2 mean, P3 mean) per evaluated agent — shows multi-dimensional profile at a glance | `notebooks/results-analysis.ipynb` — radar chart cell | §4 Results (overview) | Pending (data) |
| Fig 6 | BSI Bar Chart | Grouped bar chart of Bias Susceptibility Index per bias type × agent × evaluation mode | `notebooks/results-analysis.ipynb` — BSI visualization cell | §4.2 Pillar 2 Results | Pending (data) |
| Fig 7 | P3 Security Heatmap | Heatmap of security/compliance scores per scenario × agent — color encodes pass/partial/fail | `notebooks/results-analysis.ipynb` — P3 heatmap cell | §4.3 Pillar 3 Results | Pending (data) |
| Fig 8 | Skills/MCP Score Delta | Bar chart showing score improvement (Δ) for skills and MCP modes vs. baseline per pillar | `notebooks/results-analysis.ipynb` — delta table visualization | §4.4 Cross-Mode Analysis | Pending (data) |
| Fig 9 | Protocol Compliance Stack | Layered diagram of the agentic commerce protocol stack (PCI DSS → EMV Tokenisation → EMV 3DS → AP2/UCP/ACP → User Mandate) | Manual | §2.3 or §3.2 | Planned |

---

## Figure File Naming Convention

Files go in `docs/paper/figures/` with the naming pattern:

```
fig-01-architecture-diagram.{png,svg,pdf}
fig-02-harness-architecture.{png,svg,pdf}
fig-03-scenario-taxonomy.{png,svg,pdf}
...
```

For final submission, provide:
- `.pdf` for vector figures (diagrams, charts)
- `.png` at ≥300 DPI for rasterized figures
- `.svg` source files for manual diagrams

---

## Notebook → Figure Mapping

The `notebooks/results-analysis.ipynb` notebook (Phase 07) produces figures 5–8. Each figure corresponds to a named cell in the notebook. To regenerate:

```bash
jupyter nbconvert --to notebook --execute notebooks/results-analysis.ipynb
```

Export individual cells to PDF/PNG using `matplotlib.pyplot.savefig()` calls already present in the notebook.

---

## Placeholder Files

Placeholder files (`fig-05-radar-chart-placeholder.md` etc.) will be created in `docs/paper/figures/` once the figure IDs are finalized, to reserve spots and describe expected content for co-authors.
