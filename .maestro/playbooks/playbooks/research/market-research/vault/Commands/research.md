# Research Entity

Research a specific entity and add it to the AI Buyer Agents and Autonomous Procurement knowledge vault.

## Usage
Provide the entity type and name to research.

## Process
1. Identify the appropriate agent for the entity type:
   - Company → use company-researcher agent
   - Product → use product-researcher agent
   - Person → use person-researcher agent
   - Technology → use technology-researcher agent
   - Trend → use trend-researcher agent

2. Spawn the agent with the Task tool to research the entity

3. Verify the profile was created and INDEX.md was updated

## Examples

```
Research the company Coupa Software
→ Spawns company-researcher agent
→ Creates Companies/Coupa-Software.md
→ Updates INDEX.md

Research the technology Agentic Commerce Protocol
→ Spawns technology-researcher agent
→ Creates Technologies/Agentic-Commerce-Protocol.md
→ Updates INDEX.md

Research the trend delegated checkout
→ Spawns trend-researcher agent
→ Creates Trends/Delegated-Checkout.md
→ Updates INDEX.md
```

## Entity Type Guide

| If the subject is... | Use agent... | Saves to... |
|---------------------|-------------|-------------|
| A company or organization | company-researcher | Companies/ |
| A product, tool, or service | product-researcher | Products/ |
| A person (executive, researcher, founder) | person-researcher | People/ |
| A protocol, framework, standard, or platform | technology-researcher | Technologies/ |
| A market trend, shift, or pattern | trend-researcher | Trends/ |
