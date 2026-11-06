# AI Buyer Agents and Autonomous Procurement Research Vault

## Purpose

This vault contains structured research about the **AI Buyer Agents and Autonomous Procurement** market, organized as interlinked markdown files compatible with Obsidian.

## Structure

- **Companies/** - Company profiles (enterprise vendors, startups, protocol maintainers)
- **Products/** - Product/service profiles (procurement suites, shopping agents, trading bots)
- **People/** - Key people in the market (founders, researchers, executives, standards authors)
- **Technologies/** - Technologies and platforms (AP2, UCP, ACP, EMV 3DS, PCI DSS, NegMAS, etc.)
- **Trends/** - Market trends and analyses (delegated checkout, agentic commerce, etc.)
- **Resources/** - Reports, data sources, reference documents
- **Agents/** - Research agents for each entity type
- **Commands/** - Slash commands for common operations

## Agents

Located in `Agents/` (also accessible via `.claude/agents`):

| Agent | Purpose |
|-------|---------|
| company-researcher | Research and profile companies |
| product-researcher | Research and profile products |
| person-researcher | Research and profile key people |
| technology-researcher | Research and profile technologies and standards |
| trend-researcher | Research and analyze market trends |

## Commands

Located in `Commands/` (also accessible via `.claude/commands`):

| Command | Purpose |
|---------|---------|
| /research | Research a specific entity |

## Conventions

- Use `[[Entity Name]]` for inter-page links
- Keep profiles factual with source citations (URLs)
- Update INDEX.md when adding new entities (increment counts in Statistics table)
- Use consistent naming: `Entity-Name.md` (kebab-case with hyphens)
- Prioritize information from 2024–2026

## Working in This Vault

1. Use the research agents to add new entities
2. Manually edit profiles to add context or corrections
3. Check INDEX.md for navigation and statistics
4. Use the graph view in Obsidian to explore entity connections

## BuyerBench Context

This vault supports the BuyerBench benchmark framework. Research here informs:
- **Pillar 1 scenarios**: Real-world supplier discovery and procurement workflows
- **Pillar 2 scenarios**: Behavioral bias patterns observed in actual buyer agent products
- **Pillar 3 scenarios**: Payment security standards (PCI DSS, EMV 3DS) and compliance requirements

When researching, flag findings that are directly relevant to BuyerBench scenario design with a `> **BuyerBench relevance:** ...` blockquote.
