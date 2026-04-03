# Phase 02: Literature Review — AI Evaluation Methodology + Pillar 1 (Capability)

This phase builds the research foundation for BuyerBench's paper and scenario design by conducting two literature reviews in parallel: (1) the broader field of AI agent evaluation methodology, and (2) agent capability specifically in procurement and workflow contexts. All findings are written as structured Markdown files with YAML front matter and wiki-links, organized for graph navigation in Obsidian or Maestro's DocGraph. These documents will be directly referenced in the paper's Related Work and Methodology sections.

## Tasks

- [x] Set up the docs knowledge base structure:
  - Create folder tree: `docs/literature/eval-methodology/`, `docs/literature/pillar1-capability/`, `docs/literature/pillar2-economics/`, `docs/literature/pillar3-security/`, `docs/paper/`
  - Create `docs/literature/INDEX.md` — a top-level index of all literature review documents with one-line descriptions and wiki-links to each file; use front matter: `type: index, title: Literature Index, tags: [index]`
  - This index will be updated as each phase adds new documents

- [x] Research and document AI agent evaluation methodology — general frameworks:
  - Search for key works: AgentBench, GAIA benchmark, WebArena, SWE-bench, HELM, BIG-Bench, LLM-as-judge methods, agent evaluation taxonomies (2023–2025)
  - Create `docs/literature/eval-methodology/agent-evaluation-overview.md` with front matter: `type: research, title: AI Agent Evaluation — Overview and Taxonomy, tags: [evaluation, benchmarking, agents, methodology]`; cover: what makes a good agent benchmark (coverage, reproducibility, adversarial robustness, multi-dimensional scoring), key papers and their approaches, gaps in existing benchmarks
  - Create `docs/literature/eval-methodology/llm-as-judge.md`: cover LLM-as-judge methods, their strengths and biases, positional bias, verbosity bias, self-enhancement bias; relevance to BuyerBench scoring; front matter `tags: [evaluation, llm-judge, scoring]`
  - Create `docs/literature/eval-methodology/multi-agent-eval.md`: cover evaluation of multi-agent and tool-using agents; agent traces as evaluation artifacts; front matter `tags: [evaluation, multi-agent, tool-use]`
  - Add wiki-links between files using `[[agent-evaluation-overview]]`, `[[llm-as-judge]]`, `[[multi-agent-eval]]`

- [x] Research and document AI agent evaluation methodology — reproducibility and rigor:
  - Create `docs/literature/eval-methodology/reproducibility-in-benchmarks.md`: cover issues of benchmark contamination, train-test leakage, static vs dynamic benchmarks, snapshot vs live evaluation; how BuyerBench addresses these with controlled scenario variants; front matter `tags: [reproducibility, benchmarking, methodology]`
  - Create `docs/literature/eval-methodology/evaluation-metrics-taxonomy.md`: catalogue metric types — capability (task completion rate, accuracy), efficiency (latency, token cost), robustness (variance across variants), safety/alignment (violation rates); how these map to BuyerBench's three pillars; front matter `tags: [metrics, evaluation, taxonomy]`; include `related: ['[[agent-evaluation-overview]]', '[[BuyerBench-Pillar-Mapping]]']`

- [x] Research and document Pillar 1 capability literature — procurement and workflow agents:
  - Create `docs/literature/pillar1-capability/procurement-ai-survey.md`: survey enterprise procurement AI systems (SAP Joule/Ariba, Coupa, Ivalua IVA, Zip — already catalogued in deep-research-report.md); document capability claims, evaluation approaches used by vendors, gaps in third-party evaluation; front matter `type: research, tags: [pillar1, procurement, enterprise-ai, capability]`
  - Create `docs/literature/pillar1-capability/workflow-completion-metrics.md`: cover workflow completion rate measurement in agent systems; multi-step task decomposition; tool call accuracy; partial credit scoring; front matter `tags: [pillar1, metrics, workflow, tool-use]`
  - Create `docs/literature/pillar1-capability/supplier-selection-literature.md`: cover academic and applied work on supplier selection problems (multi-criteria decision making, AHP, TOPSIS); how these ground the "optimal choice" definition in BuyerBench Pillar 1 scenarios; front matter `tags: [pillar1, supplier-selection, optimization, procurement]`

- [x] Research and document CLI agent landscape for Pillar 1 evaluation targets:
  - Create `docs/literature/pillar1-capability/cli-agents-landscape.md`: profile the three primary evaluation targets — Claude Code CLI, Codex CLI (OpenAI), Gemini CLI — document their tool-use capabilities, agentic features, skills/MCP support, publicly documented strengths/weaknesses; note which features enable which BuyerBench task types; front matter `tags: [pillar1, cli-agents, claude, codex, gemini, evaluation-targets]`
  - Include a comparison table: Agent | Tool use | MCP support | Skills support | Procurement-relevant capabilities | Notes

- [x] Update the literature index and summarize Pillar 1 findings:
  - Update `docs/literature/INDEX.md` to include all files created in this phase with one-line descriptions
  - Create `docs/literature/pillar1-capability/PILLAR1-SUMMARY.md` with front matter `type: analysis, tags: [pillar1, summary]`: synthesize the 3-5 most important findings that inform BuyerBench scenario design for Pillar 1; include wiki-links to source documents; note gaps that BuyerBench is positioned to fill
