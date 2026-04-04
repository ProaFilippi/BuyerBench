# Entity Discovery - Find Research Targets

## Context
- **Playbook:** Market Research
- **Agent:** CladiBuyer Benchmarker
- **Auto Run Folder:** /home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks
- **Loop:** 00001

## Objective

Discover specific entities to research within the target market. Use web search to find companies, products, people, and other relevant entities that should be included in the knowledge vault.

## Instructions

1. **Read the market analysis** from `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/LOOP_00001_MARKET_ANALYSIS.md`
2. **Read existing entities** from `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/LOOP_00001_ENTITIES.md` (if it exists)
3. **Focus on ONE entity category** that needs more discovery
4. **Use web search** to find specific entities in that category
5. **Document discoveries** in `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/LOOP_00001_ENTITIES.md`

## Discovery Checklist

- [x] **Discover entities (or mark all covered)**: Read the market analysis from `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/LOOP_00001_MARKET_ANALYSIS.md` to understand priority categories. Read existing entities from `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/LOOP_00001_ENTITIES.md` (if it exists). If ALL priority entity categories already have 3+ entities discovered, append a section `## ALL_CATEGORIES_COVERED` to `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/LOOP_00001_ENTITIES.md` and mark this task complete. Otherwise, pick ONE category that needs more entities discovered. Use web search to find 3-5 specific entities in that category. Append findings to `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/LOOP_00001_ENTITIES.md` with basic info and discovery source.

  > **Completed 2026-04-04 (Loop 00001):** Created `LOOP_00001_ENTITIES.md` with **Companies** as the first category discovered. Found 5 entities via web search: Procure AI ($13M seed), Omnea ($50M Series B), Zycus (Merlin ANA — autonomous negotiation), Fairmarkit (tail-spend sourcing automation), and Skyfire (AI agent payment rails + KYA identity). Remaining priority categories to discover in subsequent loops: Protocols & Standards, Products & Platforms, Research Papers, Security & Compliance Frameworks.

## Search Strategies by Entity Type

### Companies
- Search: "[market] companies", "[market] startups", "[market] market leaders"
- Check: Crunchbase, LinkedIn, industry reports, news articles
- Look for: Funding announcements, product launches, partnerships

### Products/Services
- Search: "[market] products", "[market] solutions", "[market] platforms"
- Check: G2, Capterra, Product Hunt, company websites
- Look for: Product comparisons, reviews, feature lists

### People
- Search: "[market] CEO", "[market] founder", "[market] analyst"
- Check: LinkedIn, Twitter/X, conference speakers, podcast guests
- Look for: Thought leaders, frequent commentators, industry veterans

### Technologies
- Search: "[market] technology", "[market] standards", "[market] protocols"
- Check: Technical blogs, GitHub, academic papers, patents
- Look for: Emerging tech, dominant platforms, open standards

### Trends
- Search: "[market] trends 2024", "[market] predictions", "[market] future"
- Check: Industry reports, analyst commentary, news roundups
- Look for: Growth areas, disruptions, shifting dynamics

### Investors
- Search: "[market] investors", "[market] VC", "[market] funding"
- Check: Crunchbase, PitchBook, funding announcements
- Look for: Active investors, fund sizes, portfolio companies

## Output Format

Append to `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/LOOP_00001_ENTITIES.md`:

```markdown
---

## [Category Name] - Discovered [YYYY-MM-DD]

### [Entity Name 1]
- **Type:** [Company | Product | Person | Technology | Trend | Investor]
- **Brief:** [One sentence description]
- **Why Notable:** [Why this entity matters in the market]
- **Discovery Source:** [URL where you found this]
- **Status:** PENDING

### [Entity Name 2]
- **Type:** [Type]
- **Brief:** [Description]
- **Why Notable:** [Relevance]
- **Discovery Source:** [URL]
- **Status:** PENDING

### [Entity Name 3]
...

### Discovery Summary
- **Category:** [Category researched]
- **Entities Found:** [count]
- **Search Queries Used:**
  - "[query 1]"
  - "[query 2]"
- **Sources Checked:**
  - [Source 1]
  - [Source 2]
```

## Entity Status Values

| Status | Meaning |
|--------|---------|
| `PENDING` | Discovered, not yet researched |
| `RESEARCHED` | Full profile created in vault |
| `SKIP` | Not relevant enough to research |
| `DUPLICATE` | Already covered under another entity |

## Guidelines

- **One category per run** - Focus discovery efforts for better results
- **Quality over quantity** - 3-5 well-chosen entities beat 20 marginal ones
- **Note why each matters** - Helps prioritization later
- **Include discovery source** - Enables verification and deeper research
- **Check for duplicates** - Don't re-discover entities already in the list
- **Diversify within category** - Mix of leaders, challengers, and emerging players

## How to Know You're Done

This task is complete when ONE of the following is true:

**Option A - Discovered entities:**
1. You've picked ONE category that needed more entities discovered
2. You've used web search to find 3-5 specific entities in that category
3. You've appended findings to `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/LOOP_00001_ENTITIES.md`

**Option B - All categories covered:**
1. ALL priority entity categories in the market analysis already have 3+ entities discovered
2. You've appended `## ALL_CATEGORIES_COVERED` to `/home/superiora/Documents/CODE/BuyerBench/.maestro/playbooks/LOOP_00001_ENTITIES.md`

The `ALL_CATEGORIES_COVERED` marker signals to downstream documents that discovery is complete.
