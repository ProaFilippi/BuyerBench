---
type: market-context
title: "Brazil ERP Landscape — AI Agent Integration Status 2025–2026"
created: 2026-04-06
tags:
  - brazil
  - erp
  - procurement
  - ai-integration
  - totvs
  - sap
  - senior-sistemas
  - sankhya
  - oracle
related:
  - '[[INDEX]]'
  - '[[Brazil-AI-Procurement-Landscape]]'
  - '[[Brazil-B2B-Marketplace-Landscape]]'
  - '[[TOTVS-ERP-Procurement]]'
---

# Brazil ERP Landscape — AI Agent Integration Status 2025–2026

## Market Overview

Brazil's ERP market is one of the most structurally unique in the world: it is dominated not by SAP or Oracle but by a domestic champion (**TOTVS**) commanding ~50% market share, alongside a robust tier of Brazilian-native challengers (**Senior Sistemas**, **Sankhya**) and global players with substantial local presence (SAP, Oracle). The market is approximately **R$ 12–15 billion annually** (2025 estimate), driven by mandatory fiscal compliance complexity (SPED, Nota Fiscal-e, eSocial), unique tax regimes (Simples Nacional, Lucro Real, Lucro Presumido), and Open Finance mandates from the Banco Central do Brasil.

By 2025–2026, all five major players have announced dedicated AI agent roadmaps. This represents a structural inflection: procurement AI agents operating in Brazil will almost always be interacting with one of these five ERP backbones, making ERP integration capability a first-class evaluation dimension for BuyerBench.

### Brazil ERP Market Share (Estimated, 2025)

| Vendor | Estimated Market Share | HQ | Primary Segment |
|---|---|---|---|
| **TOTVS** | ~50% | São Paulo, SP | SME → Enterprise |
| **SAP** | ~15–20% | São Leopoldo, RS (Brazil HQ) | Large Enterprise |
| **Senior Sistemas** | ~5–8% | Blumenau, SC | SME → Mid-Market |
| **Sankhya** | ~5–7% | Uberlândia, MG | SME → Mid-Market |
| **Oracle** | ~5–8% | São Paulo, SP | Large Enterprise |
| Others (Totvs Rm, Linx, etc.) | ~10–15% | Various | Various |

---

## Key Players

### 1. TOTVS — Dominant Domestic Champion

**Company Profile:**
- ~50% of the Brazilian ERP market
- Listed on B3 (TOTS3); ~R$ 5.5B market cap (2025)
- Products: Protheus (legacy ERP), TFS (financial services), TOTVS Techfin (banking-as-a-service)
- 12,000+ employees; 45,000+ clients across Brazil

**AI Agent Strategy — TOTVS Copilot & Agent Store:**
TOTVS announced its full AI agent strategy at **Universo TOTVS 2025**, centering on:
- **TOTVS Copilot**: generative AI assistant embedded across all TOTVS platforms; accessible to all cloud clients regardless of platform used
- **Agent Store (Loja de Agentes)**: marketplace of specialized agents available for TOTVS Cloud customers — agents can be deployed without custom development
- **Procurement Agent (Agente de Compras)**: analyzes recurring spending patterns, suggests supplier renegotiations, automates purchase orders based on historical behavior

**Procurement-Specific AI Features:**
- Recurring spend analysis and supplier negotiation triggers
- Automated requisition-to-order workflows
- Historical purchasing pattern recognition
- Integration with Nota Fiscal-e validation flows

**AI Integration in Protheus 12.1.2510 (latest release 2025):**
- Native TOTVS Copilot integration across procurement, finance, HR modules
- Natural language querying of procurement data
- Automated supplier qualification workflows

**Pricing Tiers (2025 estimates; TOTVS does not publish list prices):**

| Tier | Modality | Estimated Cost |
|---|---|---|
| SME Entry (Protheus cloud, basic modules) | SaaS subscription | From ~R$ 1,800/month |
| Mid-Market (multi-module, cloud) | SaaS subscription | R$ 5,000–25,000/month |
| Enterprise (on-premise perpetual + modules) | Perpetual license | R$ 50,000–500,000+ upfront |
| TOTVS Copilot / Agent Store | Add-on (pricing not disclosed publicly) | Bundled with TOTVS Cloud plans |

**BuyerBench Relevance:** Any Brazil scenario set in a manufacturing, retail, or agribusiness company will likely involve Protheus as the ERP backbone. TOTVS Copilot's procurement agent is a **direct functional analog** to what BuyerBench evaluates — making TOTVS the primary integration target for Brazil pillar testing.

---

### 2. SAP — Global Leader with Deep Brazil Roots

**Company Profile:**
- Brazil operations since 1994; Brazil HQ in São Leopoldo (RS)
- ~15–20% ERP market share (predominantly large enterprise)
- Key products: SAP S/4HANA Cloud, SAP Ariba, SAP Business One (SME)
- Infrastructure: AWS São Paulo region since 2024 expansion

**AI Agent Strategy — Joule & Agentic Procurement:**
SAP's AI story in Brazil centers on **Joule**, its conversational AI assistant, embedded in S/4HANA Cloud for:
- Natural language procurement queries and workflow initiation
- **Sourcing Agent**: automates RFP creation — reduces time to create an RFP by up to **70%**
- **Multi-Agent Collaboration**: Finance Agent + Procurement Agent + Production Agent collaborate in real-time; if a production line fails, Production Agent queries Finance Agent for budget impact while instructing Procurement Agent to expedite parts

**Brazil-Specific Developments (2025):**
- BRF (Brazil Foods) is SAP's **strategic early adopter** for AI services in Latin America, with demonstrated supply chain planning AI deployments
- SAP Q2 2025 AI Release added Joule to SAP Fieldglass for contingent workforce procurement
- AWS São Paulo availability ensures LGPD data residency compliance

**Procurement AI Features:**
- Quote to Purchase Requisition automation (email-to-requisition via Joule)
- AI-assisted supplier scoring in SAP Ariba
- Spend analysis with generative AI summaries
- Automated three-way matching (invoice, PO, receipt)

**Pricing:**
Enterprise contract-based; SAP S/4HANA Cloud Public Edition starts at approximately USD 250/user/month internationally (BRL equivalent ~R$ 1,250+/user/month at current rates). SAP Ariba is separately priced by spend volume. Brazil pricing is negotiated through SAP's local partner ecosystem.

**BuyerBench Relevance:** SAP is the benchmark for large-enterprise procurement AI in Brazil. BRF's documented AI adoption creates a realistic case study basis. Joule's multi-agent coordination model closely mirrors BuyerBench's multi-agent orchestration evaluation scenarios.

---

### 3. Senior Sistemas — AI-Centric ERP Pioneer

**Company Profile:**
- Brazilian-native ERP vendor; headquartered in Blumenau, SC
- ~5–8% market share, primarily SME and mid-market
- Specializations: manufacturing, services, construction, agribusiness, logistics
- Claims 50% faster ERP implementation than market average

**AI Agent Strategy — "ERP AI-Centric" Concept:**
Senior is pioneering the concept of **ERP AI-Centric** in Brazil — a platform architecture where AI is not bolted on but is the operational core:
- **50+ specialized intelligent agents** announced for 2025 across Industry, Construction, Agribusiness, Logistics, and Services
- Agents function as conversational assistants that understand natural language, access data, generate analyses, and take **automated actions in real time**
- Areas covered: finance, logistics, construction, sales, stock management

**Procurement & Supply Chain AI Features:**
- Stock replenishment analysis with automated purchase requisition generation
- Procurement prospecting: automated supplier identification based on demand forecasting
- BPM (Business Process Management) integration with customizable procurement bots
- Intelligent reports on margin, productivity, and procurement cost analysis
- Collection and payment schedule automation

**Pricing:**
Not publicly disclosed; Senior pricing is via authorized reseller network in Brazil. Market estimates suggest mid-market plans run R$ 2,000–15,000/month depending on modules and user count.

**BuyerBench Relevance:** Senior's agribusiness and construction specializations are highly relevant for Brazil-specific BuyerBench scenarios (e.g., agricultural commodity procurement, civil construction supplier management). The "AI-Centric" claim invites direct comparative evaluation of how deeply AI is integrated versus bolted on.

---

### 4. Sankhya — EIP Platform with Deploy Agent Innovation

**Company Profile:**
- Brazilian ERP vendor; headquartered in Uberlândia, MG
- 35,000+ customers across Brazil; primarily SME and mid-market
- Recently evolved branding to **EIP (Enterprise Intelligence Platform)**
- Products: Sankhya ERP (100% web + mobile), Bia AI Assistant, Deploy Agent

**AI Agent Strategy — Deploy Agent & Bia:**
Sankhya's 2025 AI breakthrough is the **Deploy Agent** — an AI that automates the *implementation* of Sankhya ERP itself:
- Analyzes fiscal documents (entry/exit invoices, product codes, tax regimes, cost structures) to automatically reconstruct the business's operational logic
- Reduces ERP implementation from 9–12 months → ~30 days
- Processed 100+ projects in 2 months in 2025; goal for 2026 is to be main growth driver

**Bia — AI Procurement & Operations Assistant:**
- Conversational AI assistant integrated into Sankhya ERP
- Acts as "internal consultant always available" for fiscal, financial, and procurement questions
- Generates reports and analyses on demand
- Identifies operational bottlenecks and interprets KPIs
- Suggests process improvements based on operational data

**Procurement-Specific Features:**
- SRM (Supply Relationship Management) module: holistic supplier relationship management
- Electronic ordering: identifies purchasing needs based on inventory turnover, automates supply contracts
- Online quotation portal: suppliers receive negotiation portal to register offers based on demand analysis
- AI-powered spend analysis and bottleneck identification via Bia

**Pricing:**
Not publicly disclosed. Capterra/GetApp listings indicate pricing is quote-based. Market estimates: R$ 1,500–12,000/month depending on modules and company size.

**BuyerBench Relevance:** Sankhya's 35,000-customer base makes it Brazil's de facto SME ERP standard in many inland markets. The Deploy Agent's use of fiscal document analysis (NF-e, tax regime data) to drive procurement automation is a novel pattern worth modeling in BuyerBench — it represents AI procurement grounded in Brazilian regulatory artifacts.

---

### 5. Oracle — Global Enterprise with Fusion Agentic Applications

**Company Profile:**
- Brazil operations since 1990s; São Paulo HQ
- ~5–8% ERP market share (large enterprise only)
- Products: Oracle Fusion Cloud ERP, Oracle Procurement Cloud, NetSuite (SME)
- Infrastructure: AWS São Paulo and Oracle Cloud Infrastructure (OCI) São Paulo region

**AI Agent Strategy — Fusion Agentic Applications (Oct 2025):**
Oracle launched **Fusion Agentic Applications** in October 2025 — the most comprehensive enterprise AI agent release in the global ERP market:
- **22 agentic applications** across Finance, HR, Supply Chain, and CX
- **Quote to Purchase Requisition Agent**: captures supplier quotes from email, generates requisitions with full quote details in Oracle Self Service Procurement — directly maps to physical procurement workflows
- **Oracle Fusion Applications AI Agent Marketplace**: partner-built agents deployable within Oracle Fusion environment (launched Oct 2025)
- PwC partnership for Agentic AI deployment on Oracle Fusion Cloud

**Brazil-Specific Context:**
- OCI and AWS São Paulo regions ensure LGPD data residency
- Brazil localization package: NF-e, SPED, REINF, eSocial compliance modules
- No Brazil-specific AI procurement case studies found in 2025 research (Oracle Brazil AI adoption appears to lag global announcements by 6–12 months)

**Pricing:**
Enterprise contract-based; Oracle Fusion Cloud Procurement pricing is module-based, starting from approximately USD 300–500/user/month internationally. Brazil pricing negotiated through Oracle Latin America.

**BuyerBench Relevance:** Oracle's Quote-to-Requisition Agent is functionally the closest global analog to BuyerBench Pillar 1 capability scenarios. The Fusion Agentic Applications marketplace model — where third-party agents run within the ERP — mirrors BuyerBench's agent adapter architecture.

---

## AI Agent Integration Status Per ERP (Summary Matrix)

| Dimension | TOTVS | SAP | Senior | Sankhya | Oracle |
|---|---|---|---|---|---|
| **AI Agent Launch** | Q3 2025 (Universo TOTVS) | Rolling 2024–2025 (Joule) | 2025 (AI-Centric ERP) | 2025 (Deploy Agent + Bia) | Q4 2025 (Fusion Agentic) |
| **Procurement Agent** | Yes — Agente de Compras | Yes — Sourcing Agent + Joule | Yes — requisition automation | Yes — Bia + SRM module | Yes — Quote-to-Requisition |
| **NF-e / Fiscal Integration** | Native (Protheus) | Localization module | Native | Native | Localization module |
| **Natural Language Interface** | TOTVS Copilot | Joule | Conversational agents | Bia assistant | Oracle AI Agent Studio |
| **Multi-Agent Orchestration** | Limited (Agent Store) | Yes — Finance+Procurement+Production | Limited | Limited | Yes — 22 agentic apps |
| **Public API for AI Agents** | TOTVS Fluig / REST APIs | SAP BTP / Joule API | Senior REST APIs | Sankhya SDK | Oracle Integration Cloud |
| **Pricing Transparency** | Low (quote-based) | Low (enterprise contract) | Low (reseller network) | Low (quote-based) | Low (enterprise contract) |
| **BRL Pricing Available** | Partial (~R$1,800+/mo base) | No (USD-denominated) | No | No | No (USD-denominated) |
| **LGPD Compliance** | Yes (cloud-native) | Yes (AWS SP region) | Yes | Yes | Yes (OCI SP region) |

---

## Pricing Tiers — Summary (BRL, 2025 Estimates)

| Vendor | Entry Tier | Mid-Market | Enterprise |
|---|---|---|---|
| **TOTVS Protheus** | ~R$ 1,800/month (SaaS, basic) | R$ 5,000–25,000/month | R$ 50K–500K+ (perpetual) |
| **SAP Business One** | ~R$ 3,000/month (10 users) | SAP S/4HANA: R$ 6,000+/mo | Enterprise: negotiated |
| **Senior Sistemas** | ~R$ 2,000/month | R$ 5,000–15,000/month | Negotiated |
| **Sankhya** | ~R$ 1,500/month | R$ 3,000–12,000/month | Negotiated |
| **Oracle Fusion** | Not SME-accessible | NetSuite ~R$ 3,000+/month | Fusion: negotiated (USD) |

*All figures are market estimates based on public sources and partner disclosures. Official pricing requires direct vendor engagement.*

---

## Key Structural Themes for Brazil ERP + AI

1. **Fiscal Compliance as AI Forcing Function**: Brazil's SPED/NF-e/eSocial ecosystem means ERP AI agents must natively handle fiscal document workflows — this is not optional. Any AI procurement agent that doesn't understand Nota Fiscal-e validation, CNPJ verification, and tax regime matching will fail basic Brazil scenarios.

2. **TOTVS Lock-in Reality**: With ~50% market share, TOTVS Protheus integration is the *de facto* requirement for any Brazil-focused AI procurement solution. An AI buyer agent that cannot call Protheus APIs or interpret Protheus-format procurement data is not production-ready for Brazil.

3. **Domestic Vendor AI Race**: TOTVS, Senior, and Sankhya are all declaring AI-native ERPs simultaneously (2025–2026). This is unusual globally — most ERP markets see one or two leaders invest in AI while others follow. The competitive pressure means Brazil AI procurement capabilities may advance faster than other LatAm markets.

4. **Pricing Opacity Problem**: None of the five major vendors publish transparent, BRL-denominated AI agent pricing. All AI agent tiers are either bundled into cloud contracts or require sales engagement. This creates an information asymmetry that BuyerBench scenario design must account for (simulate "pricing discovery" as part of the agent task).

5. **Multi-Agent Coordination Gap**: Only SAP (Joule multi-agent) and Oracle (22 agentic apps) have publicly demonstrated multi-agent orchestration. TOTVS, Senior, and Sankhya are in single-agent or sequential automation territory as of 2025. This gap is a BuyerBench differentiator opportunity.

6. **Pix + ERP Integration**: All domestic vendors (TOTVS, Senior, Sankhya) have native Pix payment integrations — instant payment workflows are now table stakes for Brazilian ERP. AI procurement agents that trigger payments must route through Pix-aware ERP modules, not legacy SWIFT/boleto-only paths.

---

## Implications for BuyerBench Brazil Test Scenarios

### Pillar 1 — Capability Scenarios

| Scenario Idea | ERP Context | Key Evaluation |
|---|---|---|
| **RFQ via TOTVS Protheus API** | Agent issues RFQ through Protheus procurement module | Can agent generate valid Protheus-format RFQ with correct CNPJ/NF-e fields? |
| **SAP Sourcing Agent benchmark** | Compare BuyerBench agent vs. SAP Joule Sourcing Agent on same RFP | Head-to-head capability comparison metric |
| **Sankhya SRM supplier onboarding** | Agent onboards new supplier in Sankhya via Bia-style natural language | Natural language → ERP action success rate |
| **Multi-ERP quote consolidation** | Agent queries 3 suppliers across TOTVS, SAP, Oracle ERPs | Cross-system data aggregation capability |

### Pillar 2 — Behavioral Bias Scenarios

| Scenario Idea | ERP Context | Bias Being Tested |
|---|---|---|
| **TOTVS preferred supplier default** | TOTVS recommends incumbent supplier; agent must override | Default bias / Status quo bias |
| **SAP Ariba anchor pricing** | SAP Ariba shows "market price" that is manipulated | Anchoring bias resistance |
| **Senior AI-Centric "recommendation" trap** | Senior's AI agent suggests expensive option framed as "optimal" | Framing effect / Authority bias |

### Pillar 3 — Security & Compliance Scenarios

| Scenario Idea | ERP Context | Compliance Domain |
|---|---|---|
| **NF-e validation gate** | Agent must reject supplier without valid NF-e from TOTVS | Nota Fiscal-e compliance |
| **CNPJ verification before PO issuance** | Agent must verify CNPJ active status before creating Oracle Fusion PO | Supplier authentication |
| **Pix payment authorization chain** | Agent must follow Sankhya + Pix authorization flow for payment | Payment security (Pillar 3) |
| **LGPD data minimization in supplier profile** | Agent must not store CPF/CNPJ beyond transaction necessity | LGPD compliance |

---

## ERP API Integration Reference

| Vendor | Primary API | Documentation Status | Agent-Friendly? |
|---|---|---|---|
| TOTVS Protheus | TOTVS Fluig REST + Protheus REST APIs | Public docs available | Moderate (complex fiscal fields) |
| SAP | SAP BTP API Hub; Joule API (limited preview) | Well-documented | High (SAP API Business Hub) |
| Senior Sistemas | Senior REST APIs | Partner portal (limited public) | Low-moderate |
| Sankhya | Sankhya SDK + Web API | Public (sankhya.com.br/developer) | Moderate |
| Oracle Fusion | Oracle Integration Cloud; Oracle REST APIs | Well-documented | High (OCI + Fusion REST) |

---

## Sources

- [TOTVS Agentes de IA — TNU Sistemas](https://www.tnusistemas.com.br/agentes-de-ia-a-nova-fronteira-da-inteligencia-artificial-nas-empresas/)
- [TOTVS revoluciona com agentes de IA no Universo TOTVS — Revna](https://revna.com.br/noticias-de-tecnologia/technology/totvs-revoluciona-com-agentes-de-ia-no-universo-totvs)
- [TOTVS IA no Protheus — GKCMP](https://gkcmp.com.br/blog/tecnologia/como-a-totvs-usa-ia-no-protheus/)
- [TOTVS Protheus preço — Logos Technology](https://logostechnology.com.br/totvs-protheus-preco/)
- [SAP Business AI Q2 2025 Release Highlights — SAP News Center](https://news.sap.com/2025/07/sap-business-ai-release-highlights-q2-2025/)
- [BRF Uses AI for Supply Chain Planning — SAP News Center](https://news.sap.com/2025/08/brf-ai-transformative-supply-chain-planning-farm-to-table/)
- [SAP S/4HANA Agentic AI Strategy 2026 — PerfecTwin](https://blog.perfectwin.ai/sap-s4hana-agentic-ai-strategy-2026)
- [Senior ERP AI-Centric — Inforchannel](https://inforchannel.com.br/2025/09/25/no-erp-ai-centric-a-inteligencia-artificial-e-o-nucleo-da-plataforma-de-gestao-diz-senior-sistemas/)
- [Senior Sistemas ERP AI — Exame](https://exame.com/tecnologia/senior-erp-ia/)
- [Senior Sistemas no ERP Summit 2025](https://site.senior.com.br/en/)
- [Sankhya Deploy Agent — Mobiletime](https://www.mobiletime.com.br/noticias/14/11/2025/sankhya-agente-de-ia-erp/)
- [Sankhya Deploy Agent nova era — Infomoney](https://www.infomoney.com.br/patrocinados/sankhya-solucoes/sankhya-inaugura-nova-era-deploy-agent-erp/)
- [Oracle Fusion Agentic Applications launch — Oracle News](https://www.oracle.com/news/announcement/ai-world-oracle-advances-enterprise-ai-with-new-agents-across-fusion-applications-2025-10-15/)
- [Oracle Fusion AI Agent Marketplace — Oracle News](https://www.oracle.com/news/announcement/ai-world-oracle-launches-fusion-applications-ai-agent-marketplace-to-accelerate-enterprise-ai-adoption-2025-10-15/)
- [PwC Agentic AI for Oracle Fusion](https://www.pwc.com/gx/en/services/alliances/oracle/agentic-ai-for-oracle-fusion.html)
