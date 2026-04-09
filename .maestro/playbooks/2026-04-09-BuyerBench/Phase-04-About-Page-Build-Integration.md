# Phase 04: About Page, Build Polish, and Python-CLI Integration

This phase completes the site: adds an About page explaining the evaluation methodology, wires the Python benchmark CLI to automatically trigger a site rebuild after each report generation, and adds a convenience `npm run serve` command for previewing the static export locally. After this phase, the full workflow is: run benchmark → generate report → rebuild site → open browser.

## Tasks

- [x] Create `web/src/pages/about.tsx`. Static page (no `getStaticProps` needed). Brutalist layout with sections:
  1. `WHAT IS BUYERBENCH` — one paragraph on the three-pillar evaluation framework
  2. `PILLAR 1 — CAPABILITY` — bullet list of key metrics (task completion, supplier match, tool efficiency)
  3. `PILLAR 2 — BEHAVIORAL ECONOMICS` — explanation of bias variant testing (BASELINE vs ANCHOR_HIGH/FRAMING_GAIN/DECOY/SCARCITY/SUNK_COST), what BSI measures
  4. `PILLAR 3 — SECURITY & COMPLIANCE` — fraud detection, credential protection, prompt injection resistance
  5. `HOW TO RUN` — code block with the three commands: `pip install -e ".[dev]"`, `python -m buyerbench run --agent <name>`, `python -m buyerbench report --experiment-dir results/experiments`, `cd web && npm run build`
  6. `DATA FORMAT` — one-line description of FULL-REPORT.json and where it lives
  Each section uses a `brutal-box` with a thick left border in `var(--accent)`. Include a `← BACK TO RANKINGS` link at the top.

- [x] Add `web/src/components/ScenarioCount.tsx`. A small client-side component that reads `n_scenarios` from `per_pillar_aggregate` passed as a prop and renders a grid of three stat boxes (Pillar 1 scenarios, Pillar 2 scenarios, Pillar 3 scenarios) styled as `brutal-box`. Export and use it on the About page (pass static counts from the sample data or real report via `getStaticProps`).
  <!-- Completed 2026-04-09: Created ScenarioCount.tsx with 3-column brutal-box grid keyed by pillar; uses max(n_scenarios) per pillar across agents. Updated about.tsx with getStaticProps loading per_pillar_aggregate from loadReport(), rendered ScenarioCount between headline and Section 1. TypeScript clean. -->

- [ ] Update `web/next.config.js` to set `distDir: 'out'` (so static export lands in `web/out/`). Add a `serve` script to `web/package.json` using `npx serve out -p 3001 --single` so `npm run serve` previews the static build without Next.js dev server. Also add a combined `export` script: `"export": "next build"` (since `output: 'export'` in next.config already handles the static export).

- [ ] Add `web/src/styles/print.css` and import it in `_app.tsx`. Print styles: hide nav, hide footer, remove background colors so rankings tables print cleanly on white. This makes the site useful for academic paper workflows.

- [ ] Update `web/src/components/Layout.tsx` to add a build info bar below the header: a thin monospace strip showing `GENERATED: {generated_at}` and a `REBUILD SITE` note in a muted color. Also update the `<title>` tag dynamically: homepage should be `BuyerBench Rankings`, agent pages `{agentId} — BuyerBench`, about page `About — BuyerBench`.

- [ ] Run the full build chain to verify end-to-end: `npm run build` inside `web/`, confirm `web/out/` is created, confirm `web/out/index.html` exists, confirm `web/out/agent/` contains subdirectories for each agent ID (from `getStaticPaths`). Run `npm run serve` and confirm the site serves at `http://localhost:3001`. Fix any 404s or missing pages.

- [ ] Add `web/` to the repo's `.gitignore` exclusion list review: open the root `.gitignore` and ensure `web/node_modules/`, `web/.next/`, and `web/out/` are ignored. Also add a brief `web/README.md` (just 10 lines max) documenting: prerequisites (Node 18+), `npm install`, `npm run dev`, `npm run build`, and that data comes from `../results/experiments/FULL-REPORT.json`. This is the only documentation file needed.
