# Phase 01: Behavioral Economics Literature Digest

This phase produces a structured research vault that will directly inform scenario redesign in later phases. The agent synthesizes eight landmark behavioral economics papers — mapping each paper's core mechanisms to procurement decision contexts. By the end of this phase, the vault contains individual paper analyses, a cross-paper bias taxonomy, scenario design principles grounded in theory, and a gap analysis of BuyerBench's current Pillar 2 scenarios. This knowledge base is the foundation everything else builds on.

## Tasks

- [x] Create the research vault directory structure and write paper analysis for **Kahneman & Tversky (1979) — Prospect Theory** and **Thaler (1980) — Mental Accounting**:
  <!-- Completed 2026-04-08: Created docs/research/behavioral-economics/papers/ directory and wrote both paper analyses with YAML front matter, wiki-links, procurement applications, and scenario design implications. -->
  - Create folder: `docs/research/behavioral-economics/papers/`
  - Write `docs/research/behavioral-economics/papers/Kahneman-Tversky-1979-Prospect-Theory.md` with YAML front matter (`type: research`, `tags: [prospect-theory, loss-aversion, value-function, behavioral-economics]`) covering:
    - Core finding: value function is S-shaped — concave for gains, convex for losses, steeper in losses (loss aversion coefficient ~2.25x)
    - Reference point dependence: identical outcomes evaluated differently depending on framing anchor
    - Probability weighting: small probabilities overweighted, near-certain probabilities underweighted
    - Procurement application: supplier offers framed as "savings vs. baseline spend" vs. "cost vs. budget ceiling" trigger asymmetric reactions; loss-aversion makes agents overpay to avoid downside frames
    - Scenario design implication: embed a natural budget reference point; frame variants should shift the reference, not state the frame explicitly
    - Wiki-link: `[[Thaler-1980-Mental-Accounting]]`, `[[Shafir-Diamond-Tversky-1997-Money-Illusion]]`
  - Write `docs/research/behavioral-economics/papers/Thaler-1980-Mental-Accounting.md` with YAML front matter (`type: research`, `tags: [mental-accounting, sunk-cost, transaction-utility, segregation-integration]`) covering:
    - Core finding: people maintain separate cognitive "accounts" for different spending categories; losses in one account don't offset gains in another
    - Transaction utility: value of a deal relative to a reference price, independent of acquisition utility (the actual value of the good)
    - Sunk cost effect: past irrecoverable expenditures influence future decisions via the "don't waste" mental account
    - Segregation vs. integration: multiple small gains feel better separated; multiple losses feel better combined
    - Procurement application: prior PO investment creates sunk cost pressure; "deal" framing on a supplier discount activates transaction utility independent of actual quality; agents should evaluate only marginal costs going forward
    - Scenario design implication: introduce prior expenditure that is economically irrelevant but psychologically loaded; agents should ignore it
    - Wiki-link: `[[Kahneman-Tversky-1979-Prospect-Theory]]`, `[[Samuelson-Zeckhauser-1988-Status-Quo-Bias]]`

- [ ] Write paper analyses for **Samuelson & Zeckhauser (1988) — Status Quo Bias** and **Ariely, Loewenstein & Prelec (2003) — Coherent Arbitrariness**:
  - Write `docs/research/behavioral-economics/papers/Samuelson-Zeckhauser-1988-Status-Quo-Bias.md` with YAML front matter (`type: research`, `tags: [status-quo-bias, default-effect, omission-bias, inertia]`) covering:
    - Core finding: people disproportionately prefer the current state of affairs; switching costs are psychologically inflated relative to economic reality
    - Default effects: options framed as defaults are chosen far more often; opt-out vs. opt-in rates dramatically different
    - Loss aversion interaction: switching feels like a loss even when net utility favors switching
    - Procurement application: incumbent supplier advantages; agents resist renegotiating contracts mid-cycle even when a new vendor is strictly better; default payment terms persist unchallenged
    - Scenario design implication: present one option as the "current contract" or "existing arrangement" — the agent must overcome status quo inertia to select the objectively better alternative
    - Wiki-link: `[[Kahneman-Tversky-1979-Prospect-Theory]]`, `[[Tversky-Simonson-1993-Asymmetric-Dominance]]`
  - Write `docs/research/behavioral-economics/papers/Ariely-Loewenstein-Prelec-2003-Coherent-Arbitrariness.md` with YAML front matter (`type: research`, `tags: [anchoring, coherent-arbitrariness, willingness-to-pay, arbitrary-coherence]`) covering:
    - Core finding: initial (arbitrary) anchors establish a reference WTP; subsequent evaluations remain coherent *relative to that anchor* even when the anchor is random or irrelevant
    - Coherence within sessions: once an anchor sets a scale, relative preferences become internally consistent but are shifted by that anchor
    - The "anchor then adjust" failure: people adjust insufficiently from anchors, especially when the anchor is plausible-sounding
    - Procurement application: a "market benchmark" price in the briefing material anchors cost perception; even if labelled as industry average, agents will anchor to it when evaluating supplier quotes
    - Scenario design implication: embed a market benchmark in the scenario context (not as explicit manipulation), make it plausible but irrelevant to the actual supply set; test whether agent adjusts fully
    - Wiki-link: `[[Kahneman-Tversky-1979-Prospect-Theory]]`, `[[Scenario-Design-Principles]]`

- [ ] Write paper analyses for **Tversky & Simonson (1993) — Asymmetric Dominance** and **Loewenstein & Prelec (1992) — Hyperbolic Discounting**:
  - Write `docs/research/behavioral-economics/papers/Tversky-Simonson-1993-Asymmetric-Dominance.md` with YAML front matter (`type: research`, `tags: [decoy-effect, asymmetric-dominance, compromise-effect, context-dependence]`) covering:
    - Core finding: adding an option that is dominated by only one alternative (the "decoy") increases preference for the dominating option (asymmetric dominance / attraction effect)
    - Compromise effect: options positioned as moderate compromises between extremes gain preference boost
    - Context dependence violation: standard economic theory predicts adding options shouldn't change ranking of existing options (IIA); decoys violate this
    - Partial dominance: most realistic decoys are only partially dominated — better on one attribute, worse on another vs. the target
    - Procurement application: supplier catalog may include an option that makes your preferred vendor look superior on the key dimension (cost or quality) without being obviously useless
    - Scenario design implication: design decoys that are partially (not completely) dominated — slightly better on a minor attribute, clearly worse on the key one; don't label or hint at decoy role
    - Wiki-link: `[[Samuelson-Zeckhauser-1988-Status-Quo-Bias]]`, `[[Bias-Taxonomy]]`
  - Write `docs/research/behavioral-economics/papers/Loewenstein-Prelec-1992-Hyperbolic-Discounting.md` with YAML front matter (`type: research`, `tags: [hyperbolic-discounting, present-bias, time-inconsistency, impatience]`) covering:
    - Core finding: discount rates are not constant over time — people show extreme impatience for near-future outcomes but near-indifference for far-future ones
    - Time inconsistency: preferences reverse as time horizons shift; plans made for future selves are violated when the moment arrives
    - Present bias in procurement: agents may over-weight immediate savings (lower price now) vs. longer-term benefits (quality, reliability, better terms over multi-year contract)
    - Procurement application: payment terms with early payment discounts; spot buying vs. long-term contracts; emergency procurement under time pressure
    - Scenario design implication: frame two equivalent contracts with different payment schedules where one has a front-loaded "discount" vs. better lifecycle value
    - Wiki-link: `[[Thaler-1980-Mental-Accounting]]`, `[[Scenario-Design-Principles]]`

- [ ] Write paper analyses for **Bazerman & Neale (1992) — Negotiating Rationally** and **Shafir, Diamond & Tversky (1997) — Money Illusion**:
  - Write `docs/research/behavioral-economics/papers/Bazerman-Neale-1992-Negotiating-Rationally.md` with YAML front matter (`type: research`, `tags: [negotiation, mythical-fixed-pie, reactive-devaluation, overconfidence, procurement]`) covering:
    - Core finding: negotiators systematically err by assuming fixed-pie (zero-sum) distributions, engaging in reactive devaluation, and over-anchoring on first offers
    - Mythical fixed-pie: negotiators assume all items are disputed even when both parties prefer different things — optimal trades go unmade
    - Reactive devaluation: offers from adversarial parties are devalued merely because of their source, regardless of content
    - Escalation of commitment: parties over-invest in failing negotiations due to sunk costs and public commitment
    - Procurement application: multi-attribute supplier negotiations where agents over-focus on price while ignoring exploitable trade-offs in delivery, payment terms, warranty
    - Scenario design implication: present a negotiation scenario where the "right move" is to trade price concession for delivery speed — agents that treat it as pure cost minimization miss the optimal deal
    - Wiki-link: `[[Thaler-1980-Mental-Accounting]]`, `[[Loewenstein-Prelec-1992-Hyperbolic-Discounting]]`
  - Write `docs/research/behavioral-economics/papers/Shafir-Diamond-Tversky-1997-Money-Illusion.md` with YAML front matter (`type: research`, `tags: [money-illusion, nominal-vs-real, inflation-confusion, currency]`) covering:
    - Core finding: people evaluate economic transactions in nominal terms, failing to account for inflation, currency conversion, or real purchasing power
    - Contract evaluation: workers prefer 2% nominal raise in 4% inflation over 0% raise in 0% inflation, even though the former is a real pay cut
    - Procurement application: multi-currency vendor comparison; price increases framed as "below inflation" vs. stated in real terms; year-over-year contract renewal with cost-of-living adjustments
    - Scenario design implication: present quotes in different currencies or with inflation adjustments; correct agent ignores nominal framing and calculates real cost
    - Wiki-link: `[[Kahneman-Tversky-1979-Prospect-Theory]]`, `[[Bias-Taxonomy]]`

- [ ] Write the cross-paper **Bias Taxonomy** synthesis document and **Scenario Design Principles** guide:
  - Write `docs/research/behavioral-economics/Bias-Taxonomy.md` with YAML front matter (`type: analysis`, `tags: [taxonomy, bias-categories, procurement, scenario-design]`) that organizes all biases into a structured table:
    - Column headers: Bias Name | Paper Source | Mechanism | Procurement Trigger | Detection Signal | Current BuyerBench Coverage
    - Rows for: Loss Aversion, Anchoring, Status Quo Bias, Decoy Effect, Sunk Cost, Hyperbolic Discounting, Money Illusion, Framing Effects, Compromise Effect, Reactive Devaluation
    - Mark current coverage as: SHALLOW / MISSING / ADEQUATE for each
    - Wiki-links to all individual paper files
  - Write `docs/research/behavioral-economics/Scenario-Design-Principles.md` with YAML front matter (`type: reference`, `tags: [scenario-design, best-practices, behavioral-economics]`) covering these principles with rationale:
    1. **Embed, Don't Announce**: manipulations must be woven into realistic procurement context, not flagged as test conditions
    2. **Partial Dominance Only**: decoy options should be partially dominated (not completely), as in real supplier catalogs
    3. **Naturalistic Anchors**: reference prices must be sourced from realistic context (industry benchmarks, prior POs, quoted norms) not arbitrary labels
    4. **Reference Point Separation**: BASELINE and variant must share identical economics but different reference points — never change the underlying math
    5. **Compound Bias Scenarios**: advanced scenarios should layer two compatible biases (e.g., anchoring + scarcity, sunk cost + status quo)
    6. **Measurement Depth**: scoring should capture *how much* reasoning changed (utility gap, reasoning trace divergence), not just binary choice outcome
    7. **Implicit vs. Explicit Framing**: loss/gain framing should emerge from natural contract language, not from explicit "this is a loss" labels
    - Wiki-links: `[[Bias-Taxonomy]]`, all 8 paper files

- [ ] Write the **Gap Analysis** document for current BuyerBench Pillar 2 scenarios:
  - Read the existing scenario files before writing:
    - `scenarios/pillar2/p2-01-anchoring/BASELINE.yaml` and `ANCHOR_HIGH.yaml`
    - `scenarios/pillar2/p2-02-framing/GAIN.yaml` and `LOSS.yaml`
    - `scenarios/pillar2/p2-03-decoy/BASELINE.yaml` and `DECOY.yaml`
    - `scenarios/pillar2/p2-04-scarcity/BASELINE.yaml` and `SCARCITY.yaml`
  - Write `docs/research/behavioral-economics/BuyerBench-P2-Gap-Analysis.md` with YAML front matter (`type: analysis`, `tags: [gap-analysis, pillar2, scenarios, bias-testing]`) containing:
    - Per-scenario analysis table: Scenario ID | Bias Tested | Current Weakness | Paper It Violates | Redesign Direction
    - p2-01 anchoring: anchor is round number label ($95 benchmark), not embedded in context; violates Ariely et al. coherent arbitrariness — redesign with realistic prior-PO history and industry report citation
    - p2-02 framing: gain/loss labels are explicit statement additions; violates Kahneman & Tversky — redesign so framing emerges from contract language (budget surplus narrative vs. overage warning in email thread)
    - p2-03 decoy: SupplierGamma dominated on ALL attributes; violates Tversky & Simonson partial dominance principle — redesign with partial dominance (better on one minor attribute)
    - p2-04 scarcity: urgency language is explicitly labeled "LIMITED TIME OFFER"; violates embedding principle — redesign with scarcity embedded in supplier communication tone, not flagged text
    - Missing biases section: sunk cost (Thaler 1980), status quo bias (Samuelson & Zeckhauser), hyperbolic discounting (Loewenstein & Prelec), money illusion (Shafir et al.)
    - Recommended new scenario pairs for each missing bias
    - Wiki-links: `[[Scenario-Design-Principles]]`, `[[Bias-Taxonomy]]`, all relevant paper files

- [ ] Validate the research vault is complete and internally consistent:
  - Verify all 8 paper files exist in `docs/research/behavioral-economics/papers/`
  - Verify `Bias-Taxonomy.md`, `Scenario-Design-Principles.md`, and `BuyerBench-P2-Gap-Analysis.md` exist in `docs/research/behavioral-economics/`
  - Verify every document has valid YAML front matter with `type`, `title` (if missing, add it), `created: 2026-04-08`, and at least 2 tags
  - Verify all wiki-links in each document point to files that actually exist (check `[[FileName]]` references)
  - Print a summary table: File | Exists | Has Front Matter | Wiki-Links Valid
