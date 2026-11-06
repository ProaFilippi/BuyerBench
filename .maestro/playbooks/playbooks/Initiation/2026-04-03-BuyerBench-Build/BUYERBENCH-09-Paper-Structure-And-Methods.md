# Phase 09: Research Paper — Structure, Introduction, Related Work, and Methodology

This phase scaffolds the full research paper and writes its first half: the Introduction (motivation, contributions, paper outline), Related Work (drawing from the Phase 02-03 literature reviews), and Methodology (benchmark design, scenario taxonomy, evaluation protocol). These sections can be drafted before all experimental results are final because they depend on the framework design, not the outcome data. The paper lives in `docs/paper/` as a structured Markdown document suitable for rendering on GitHub and conversion to LaTeX for venue submission.

## Tasks

- [x] Scaffold the paper directory and structure:
  - Create `docs/paper/` with these files:
    - `docs/paper/buyerbench-paper.md` — the main paper document; use a flat Markdown structure with `##` section headers matching standard IMRaD layout; add YAML front matter: `type: paper, title: "BuyerBench: A Multi-Dimensional Benchmark for Evaluating AI Buyer Agents", tags: [research-paper, benchmark, buyer-agents, procurement, ai-evaluation]`
    - `docs/paper/figures/` — placeholder folder for figures referenced in the paper (charts from Phase 07 notebook go here)
    - `docs/paper/references.bib` — BibTeX references file; pre-populate with references for all key papers cited in literature reviews (Kahneman & Tversky 1974, AgentBench, GAIA, HELM, PCI DSS, EMV 3DS, ISO 42001, key vendor papers cited in deep-research-report.md)
    - `docs/paper/PAPER-STATUS.md` — section-by-section writing status tracker (front matter `type: note, tags: [paper, status]`); columns: Section | Status (Draft/Review/Done) | Notes
  - Add `docs/paper/` to `docs/literature/INDEX.md` with a pointer

- [x] Write the Abstract and Introduction section of the paper:
  - **Abstract** (150-200 words): state the problem (AI buyer agents are increasingly autonomous but lack standardized evaluation), introduce BuyerBench (open-source, three-pillar, Python framework), summarize key findings (fill in "TBD — results from Phase 07" placeholders), state availability (GitHub)
  - **Introduction** (~800 words): motivate the problem with 3-4 concrete examples from the agent landscape (cite Amazon Rufus auto-buy, Visa Intelligent Commerce, agentic commerce protocols); state the three research questions BuyerBench addresses (one per pillar); enumerate contributions (framework, scenario suite, evaluation methodology, empirical results); provide paper outline; use `[[Agent-Landscape-Summary]]` wiki-link as a source
  - Draw directly from `docs/literature/RESEARCH-GAPS.md` for the "gap" argument

- [x] Write the Related Work section:
  - **AI Agent Evaluation** subsection: summarize findings from `docs/literature/eval-methodology/agent-evaluation-overview.md` and `eval-methodology/reproducibility-in-benchmarks.md`; contrast BuyerBench's multi-pillar approach with single-axis benchmarks (AgentBench focuses on capability, HELM focuses on language, SWE-bench focuses on coding)
  - **Behavioral Economics and AI Bias** subsection: summarize `docs/literature/pillar2-economics/behavioral-economics-foundations.md` and `bias-in-llm-agents.md`; position BuyerBench as the first procurement-domain benchmark for bias susceptibility measurement
  - **Payment Security and Agentic Commerce** subsection: summarize `docs/literature/pillar3-security/payment-security-standards.md` and `agentic-commerce-protocols.md`; position BuyerBench as the first framework to operationalize PCI DSS and EMV 3DS as agent evaluation criteria
  - **Buyer Agent Systems** subsection: briefly survey the 23 catalogued agents from the agent landscape summary; use the category taxonomy from `deep-research-report.md`

- [x] Write the Methodology section:
  - **Benchmark Design Philosophy** subsection: explain the three-pillar structure and why multi-dimensional profiling is necessary; explain why a single score is insufficient; explain the "separate capability from policy compliance" design principle
  - **Scenario Design** subsection: explain the scenario schema (Scenario model fields); describe the controlled variant design for Pillar 2 with a worked example (the anchoring pair); provide the full scenario taxonomy table (18 scenarios, organized by pillar, variant, difficulty)
  - **Agent Interface and Harness** subsection: describe the prompt serialization approach, subprocess invocation, output parsing, and the three evaluation modes (baseline, skills, MCP); include a figure placeholder `[Figure: harness architecture diagram]`
  - **Evaluation Metrics** subsection: formally define each metric family — capability metrics (task completion rate, supplier selection accuracy, policy adherence), economic metrics (optimality gap, expected value regret, bias susceptibility index), security metrics (compliance adherence rate, fraud detection F1, security violation frequency); include mathematical notation where appropriate
  - **Evaluated Agents** subsection: list all evaluated agents (CLI agents × 3 modes + open-source agents); note inaccessible commercial agents and reference evaluation stubs

- [x] Update `docs/paper/PAPER-STATUS.md` and create a cross-reference map:
  - Mark Abstract, Introduction, Related Work, Methodology as "Draft" status
  - Create `docs/paper/FIGURE-PLAN.md`: list all planned figures with descriptions (radar chart, BSI bar chart, heatmap, architecture diagram) and note which Phase 07 notebook cell produces each; front matter `type: note, tags: [paper, figures]`
