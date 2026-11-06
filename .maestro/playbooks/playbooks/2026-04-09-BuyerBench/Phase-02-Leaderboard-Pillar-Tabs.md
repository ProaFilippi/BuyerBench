# Phase 02: Full Leaderboard with Pillar Tabs and Metric Drilldown

This phase replaces the Phase 01 prototype table with a proper leaderboard experience: three brutalist tab panels (one per pillar) plus an OVERALL combined ranking, per-metric score breakdowns inside each row, and agent family grouping. The result is a publication-quality rankings page that communicates the full nuance of the BuyerBench evaluation.

## Tasks

- [x] Search `web/src/lib/loadReport.ts` for the existing `computeAgentSummaries` helper and extend it. Add a new export `computePillarLeaderboard(report: FullReport, pillar: 'PILLAR1' | 'PILLAR2' | 'PILLAR3'): PillarAggregate[]` that filters `per_pillar_aggregate` to the given pillar and sorts by `mean_score` descending. Add `getMetricsForAgent(report: FullReport, pillar: string, agentId: string): MetricRow[]` that filters `per_metric_breakdown[pillar]` to the given agent. These are the two helpers the leaderboard page needs.

- [x] Create `web/src/components/ScoreBar.tsx`. Props: `score: number` (0–1), `color: string`, `showLabel?: boolean`. Renders a fixed-height (20px) container with `brutal-border`, an inner filled div at `width: Math.round(score*100)%` with the given background color, and optionally a text label `{Math.round(score*100)}%` right-aligned in monospace outside the bar. Export as default.

- [x] Create `web/src/components/MetricRow.tsx`. Props: `metric: string`, `mean: number`, `min: number`, `max: number`. Renders a single table row: metric name (lowercase, replace underscores with spaces), a `<ScoreBar>` for mean in a neutral gray `#666`, and min/max as small monospace labels. Used inside expandable agent rows.

- [x] Create `web/src/components/PillarTable.tsx`. Props: `rows: PillarAggregate[]`, `metrics: Record<string, MetricRow[]>` (agent_id → metric rows), `pillar: string`, `accentColor: string`. Renders a full-width `<table>` with no border-collapse (keep cell gaps for brutalist look), sticky `<thead>` with columns RANK · AGENT · SCORE · VARIANCE · SCENARIOS. Each `<tbody>` row:
  - Shows rank number, agent ID (formatted — strip `openrouter-` prefix, replace `-` with spaces, uppercase family name), `<ScoreBar>` for `mean_score`, std as ±X.XX, and `n_scenarios`.
  - Row 1 has `border-left: 6px solid var(--accent)` and background `var(--accent2)`.
  - Clicking a row toggles an expanded sub-row spanning all columns that shows a nested `<table>` of `<MetricRow>` components for that agent's metrics in this pillar.
  - Use `useState` for expanded row tracking.

- [x] Create `web/src/components/PillarTabs.tsx`. Props: `activeTab: string`, `onChange: (tab: string) => void`, `tabs: { id: string; label: string }[]`. Renders a row of brutalist tab buttons. Active tab: `background: var(--fg); color: var(--bg)`. Inactive: `background: var(--bg); color: var(--fg); border: var(--border)`. No rounded corners. Font monospace uppercase. Clicking fires `onChange`. Export as default.

- [x] Update `web/src/pages/index.tsx` to use the full leaderboard. In `getStaticProps`, call `computePillarLeaderboard` for each of the three pillars and `getMetricsForAgent` to build the metrics lookup dict. Pass all pillar data as props. Replace the old single table with:
  1. Keep the hero section from Phase 01.
  2. Add an OVERALL rankings section (first, most prominent) using `computeAgentSummaries` — keep the overall bar chart table from Phase 01 but add `<ScoreBar>` components instead of inline divs.
  3. Add `<PillarTabs>` with tabs: OVERALL · CAPABILITY · ECONOMICS · SECURITY. Use `useState` to track active tab. The OVERALL tab shows the combined summary table; the three pillar tabs each show `<PillarTable>` with the correct `accentColor` (red for P1, yellow for P2, green for P3).
  4. Below the tabs, show a stat strip: total agent count, total scenario count, generated-at timestamp. Keep the three stat boxes from Phase 01.

- [x] Run `npx tsc --noEmit` inside `web/` and fix any type errors. Verify `npm run dev` renders the page with all three pillar tabs switching correctly and metric rows expanding on row click.
  <!-- TypeScript check passed with zero errors. -->
