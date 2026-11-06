# Phase 01: Next.js Scaffold + Data Loader + Brutalist Home Page

This phase bootstraps the entire BuyerBench rankings website from zero to a working local dev server. By the end, `npm run dev` in `web/` serves a brutalist leaderboard page that reads live data from `results/experiments/FULL-REPORT.json` — or falls back to rich sample data so the site always builds even without a prior benchmark run. This is the structural foundation every subsequent phase builds on.

## Tasks

- [x] Create `web/package.json` with Next.js 14 (Pages Router, static export), React 18, TypeScript, and no UI library. Set `"scripts"` to include `dev`, `build`, and `export` (`next build && next export`). Also create `web/tsconfig.json` (strict mode, target ES2020, `moduleResolution: bundler`, path alias `@/*` → `./src/*`), `web/.gitignore` (node_modules, .next, out), and `web/next.config.js` with `output: 'export'` and `trailingSlash: true`.

- [x] Run `npm install` inside the `web/` directory to install all dependencies before any code references them.

- [x] Create `web/src/types/report.ts` with TypeScript interfaces mirroring `FULL-REPORT.json`. Include:
  - `PillarAggregate` — `{ agent_id, pillar, mean_score, std, min, max, n_scenarios }`
  - `MetricRow` — `{ agent_id, metric, mean, min, max }`
  - `BiasSusceptibilityRow` — `{ bias_type, agent_id, mode, bsi, decision_changed, pair_id }`
  - `SecurityViolationRow` — `{ scenario_id, agent_id, compliance_adherence_rate, security_violation_frequency, score }`
  - `SkillsDeltaRow` — `{ family, mode, agent_id, pillar, baseline_score, variant_score, delta }`
  - `FullReport` — top-level object containing all five tables plus `generated_at` and `experiment_dir`
  - `AgentSummary` — derived type for homepage rankings: `{ agent_id, pillar1_score, pillar2_score, pillar3_score, overall_score, n_scenarios_total }` (computed by averaging across pillars)

- [x] Create `web/src/lib/loadReport.ts`. This module exports a single function `loadReport(): FullReport`. It uses Node.js `fs.readFileSync` to read `../../results/experiments/FULL-REPORT.json` relative to `process.cwd()` (i.e., the `web/` directory). If the file does not exist or fails to parse, it returns a hardcoded `SAMPLE_REPORT` constant defined in the same file. The sample must include at least 5 realistic agent entries across all three pillars so the homepage renders meaningfully during development. Include agents: `mock-agent-v1` (scores ~1.0), `claude-code-baseline` (~0.6/0.5/0.7), `codex-baseline` (~0.5/0.4/0.6), `openrouter-openai-gpt-4o` (~0.7/0.6/0.8), `negmas` (~0.4/0.3/0.2). Also export a helper `computeAgentSummaries(report: FullReport): AgentSummary[]` that groups `per_pillar_aggregate` by agent, computes `overall_score` as the mean of available pillar scores, and sorts by `overall_score` descending.

- [x] Create the brutalist CSS design system at `web/src/styles/globals.css`. Define CSS custom properties on `:root`:
  - `--bg: #f5f0e8` (off-white paper), `--fg: #0a0a0a` (near-black), `--accent: #ff3b00` (aggressive orange-red), `--accent2: #ffe500` (brutal yellow), `--border: 3px solid #0a0a0a`, `--font-mono: 'IBM Plex Mono', 'Courier New', monospace`, `--font-sans: 'Space Grotesk', 'Arial Black', sans-serif`
  - Apply `box-sizing: border-box` everywhere, `background: var(--bg)`, `color: var(--fg)`, `font-family: var(--font-mono)` on `body`
  - Define utility classes: `.brutal-border` (border: var(--border)), `.brutal-box` (brutal-border + no border-radius + box-shadow: 4px 4px 0 var(--fg)), `.tag` (inline-block, px-2, bg: var(--fg), color: var(--bg), font-size 0.7rem, uppercase, letter-spacing 0.1em)
  - Import Google Fonts `IBM Plex Mono` and `Space Grotesk` via `@import` at the top.

- [x] Create `web/src/pages/_app.tsx` (imports `globals.css`, renders `<Component {...pageProps} />`), `web/src/pages/_document.tsx` (sets `lang="en"`, adds `<meta name="description" content="BuyerBench — AI Buyer Agent Rankings">`), and `web/src/components/Layout.tsx` with a brutalist header bar containing `BUYERBENCH` in large monospace caps with a red `█` glyph, a nav with links to `/` (RANKINGS) and `/about` (ABOUT), and a footer showing the report's `generated_at` timestamp passed as a prop.

- [x] Create the homepage at `web/src/pages/index.tsx`. Use `getStaticProps` to call `loadReport()` and `computeAgentSummaries()`. The page renders:
  1. A hero section: large headline `AI BUYER AGENT RANKINGS` in black uppercase, subtitle `Pillar 1: Capability · Pillar 2: Economics · Pillar 3: Security`, a `<span className="tag">LIVE DATA</span>` or `<span className="tag">SAMPLE DATA</span>` badge (check if `generated_at` is in the real report)
  2. A full-width rankings table with columns: `RANK`, `AGENT`, `CAPABILITY (P1)`, `ECONOMICS (P2)`, `SECURITY (P3)`, `OVERALL`. Each score renders as a percentage bar: a narrow `<div>` where a filled inner div has `width: {score*100}%` background `var(--accent)` on P1, `var(--accent2)` on P2, a dark green `#00c853` on P3, all behind a `brutal-border` container. Rank 1 row gets a thick left border `6px solid var(--accent)`. Rows alternate between `--bg` and `#ece7d8`.
  3. Below the table, three side-by-side `brutal-box` stat cards: "AGENTS EVALUATED", "SCENARIOS TESTED", "PILLARS".
  Pass `generated_at` to `<Layout>`. Export types for `getStaticProps`.

- [x] Verify the site works: run `npm run dev` inside `web/` (in background or as a check), confirm no TypeScript errors by running `npx tsc --noEmit` in `web/`, and confirm `npm run build` completes without errors. If there are import or type errors, fix them before considering this task done.
  <!-- `npx tsc --noEmit` → 0 errors; `npm run build` → 4 static pages compiled successfully -->
