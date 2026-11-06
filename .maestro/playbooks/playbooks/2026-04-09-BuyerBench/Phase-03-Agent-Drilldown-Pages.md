# Phase 03: Agent Drilldown Pages — Bias, Security, and Skills Delta

This phase adds per-agent detail pages at `/agent/[id]`, surfacing the three analytical tables from FULL-REPORT.json that are invisible on the leaderboard: the Bias Susceptibility Index (BSI) by bias type, Security Violation frequency per scenario, and the Skills/MCP capability delta showing how much tools improve an agent. Each page follows the same brutalist layout but with data-dense table components unique to each section.

## Tasks

- [x] Add three new helper exports to `web/src/lib/loadReport.ts`:
  <!-- Done: all four functions were already implemented (getBiasRowsForAgent, getSecurityRowsForAgent, getDeltaRowsForAgent, getAllAgentIds). TypeScript checks pass with no errors. -->
  - `getBiasRowsForAgent(report: FullReport, agentId: string): BiasSusceptibilityRow[]` — filter `bias_susceptibility_table` by `agent_id`, sort by `bsi` descending.
  - `getSecurityRowsForAgent(report: FullReport, agentId: string): SecurityViolationRow[]` — filter `security_violation_table` by `agent_id`.
  - `getDeltaRowsForAgent(report: FullReport, agentId: string): SkillsDeltaRow[]` — filter `skills_mcp_delta_table` by `agent_id`.
  - `getAllAgentIds(report: FullReport): string[]` — unique sorted agent IDs from `per_pillar_aggregate`.

- [x] Create `web/src/components/BiasTable.tsx`. Props: `rows: BiasSusceptibilityRow[]`. Renders a `<table>` with columns: BIAS TYPE · BSI · DECISION CHANGED · PAIR ID. BSI values render as a `<ScoreBar>` using a gradient color: `0–0.2` green, `0.2–0.5` yellow (`var(--accent2)`), `>0.5` red (`var(--accent)`). `decision_changed` renders as a bold `✗ CHANGED` in red or `✓ STABLE` in green. If `rows` is empty, render a `brutal-box` message `NO BIAS DATA — AGENT NOT TESTED ON PILLAR 2`. Export as default.
  <!-- Done: BiasTable.tsx implemented with bsiColor() threshold helper, ScoreBar integration, HTML entity ✓/✗ markers, and brutal-box empty state. TypeScript passes with no errors. -->

- [x] Create `web/src/components/SecurityTable.tsx`. Props: `rows: SecurityViolationRow[]`. Renders a `<table>` with columns: SCENARIO · COMPLIANCE RATE · VIOLATION FREQ · SCORE. All three numeric columns use `<ScoreBar>` — compliance and score in green, violation frequency inverted (red bar, lower is better, with a note label `LOWER = BETTER`). If empty, render `NO SECURITY DATA — AGENT NOT TESTED ON PILLAR 3`. Export as default.
  <!-- Done: SecurityTable.tsx implemented with green ScoreBars for compliance_adherence_rate and score, red ScoreBar for security_violation_frequency (higher bar = more violations = visually bad), block-style LOWER = BETTER sub-label in the column header, and brutal-box empty state. TypeScript passes with no errors. -->

- [x] Create `web/src/components/DeltaTable.tsx`. Props: `rows: SkillsDeltaRow[]`. Renders a `<table>` with columns: PILLAR · MODE · BASELINE · WITH TOOLS · DELTA. Delta column: positive delta renders `+X.XX` in green bold, negative in red bold, zero in gray. Baseline and variant columns use `<ScoreBar>` in muted gray. Group rows by pillar (PILLAR1/2/3 as section headers with `brutal-border-bottom`). If empty, render `NO DELTA DATA — THIS IS A BASELINE AGENT`. Export as default.
  <!-- Done: DeltaTable.tsx implemented with dynamic pillar grouping via Set, muted-gray ScoreBars for baseline/variant columns, colored +/- delta display, brutal section headers with borderBottom, and brutal-box empty state. TypeScript passes with no errors. -->

- [x] Create `web/src/components/AgentHeader.tsx`. Props: `agentId: string`, `summary: AgentSummary | undefined`. Renders the agent page hero: large monospace agent ID, a row of three pill-style score badges (P1/P2/P3), and an OVERALL score in the largest font on the page (6rem, bold, brutalist). If `summary` is undefined, show `NOT RANKED` in the score position.
  <!-- Done: AgentHeader.tsx already implemented with PillarBadge sub-component (inline pill badges with translucent pillar colors), 6rem bold overall score using var(--font-sans), and "NOT RANKED" fallback when summary is undefined. TypeScript passes with no errors. -->

- [x] Create `web/src/pages/agent/[id].tsx`. Use `getStaticPaths` (returning all agent IDs from `getAllAgentIds`) and `getStaticProps` (loads report, extracts bias, security, delta rows, and overall summary for the agent). Page layout:
  1. `<AgentHeader>` at top
  2. Section `BEHAVIORAL BIAS RESISTANCE` with `<BiasTable>` — prefaced by a one-line explainer: `BSI measures how often framing changes the agent's decision. 0.0 = fully rational, 1.0 = fully manipulable.`
  3. Section `SECURITY & COMPLIANCE` with `<SecurityTable>` — prefaced by `Compliance adherence rate and security violation frequency across Pillar 3 scenarios.`
  4. Section `TOOL AUGMENTATION DELTA` with `<DeltaTable>` — prefaced by `Score change when adding Skills or MCP server vs. baseline prompt-only mode.`
  5. A `← BACK TO RANKINGS` link at top-left styled as a brutalist button.
  Each section uses a `brutal-box` container with a bold uppercase section title and a thin separator line.
  <!-- Done: already fully implemented with getStaticPaths/getStaticProps, all four sections with brutal-box containers, back button with box-shadow brutalist style, and summary null→undefined coercion for AgentHeader. TypeScript checks pass with no errors. -->

- [x] Update `web/src/pages/index.tsx` to make agent IDs in the rankings tables clickable links to `/agent/{agent_id}`. The link text should be the formatted agent display name. Style the links with `color: var(--fg); text-decoration: underline; text-decoration-style: wavy;` to maintain brutalist aesthetic without a standard blue hyperlink.
  <!-- Done: already implemented. OVERALL tab in index.tsx uses <Link href={`/agent/${agent.agent_id}`}> with wavy underline styling; per-pillar tabs delegate to PillarTable.tsx which has the same <Link> pattern plus e.stopPropagation() to prevent the row expand/collapse from firing on click. TypeScript clean. -->

- [x] Run `npx tsc --noEmit`, then `npm run build` to verify static export generates HTML for each agent page. Fix any errors. Spot-check that `/agent/mock-agent-v1` renders correctly with sample data.
  <!-- Done: `npx tsc --noEmit` passed with zero errors. `npm run build` succeeded — 6 static pages generated including /agent/negmas and /agent/stripe-toolkit (the two agents present in the real FULL-REPORT.json). The mock-agent-v1 page is not generated because the real report is found and loaded (the sample data fallback is only used when FULL-REPORT.json is absent). Spot-checked /agent/negmas.html: all five sections render correctly — BEHAVIORAL BIAS RESISTANCE (with NO BIAS DATA empty state), SECURITY & COMPLIANCE, TOOL AUGMENTATION DELTA, AgentHeader, and ← BACK TO RANKINGS button. TypeScript clean, build clean. -->
