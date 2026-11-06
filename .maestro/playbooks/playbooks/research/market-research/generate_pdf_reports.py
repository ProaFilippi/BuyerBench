#!/usr/bin/env python3
"""
BuyerBench Market Research PDF Generator
=========================================
Converts vault markdown files to two professional PDF reports:
  1. Global-Market-Research-Report.pdf  — 37-entity global analysis
  2. Brazil-Market-Analysis.pdf         — 25-entity Brazil deep-dive

Run:
    python3 generate_pdf_reports.py
"""

import re
import sys
from pathlib import Path
import markdown2
from weasyprint import HTML, CSS

# ─── Paths ────────────────────────────────────────────────────────────────────

VAULT = Path(__file__).parent / "vault"
OUTPUT_DIR = Path(__file__).parent

# ─── Markdown helpers ─────────────────────────────────────────────────────────

def strip_frontmatter(text: str) -> str:
    """Remove YAML frontmatter delimited by ---."""
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[end + 4:].lstrip("\n")
    return text


def process_wikilinks(text: str) -> str:
    """Convert [[path|label]] → label, [[path]] → readable name."""
    # [[path|label]] → label
    text = re.sub(r'\[\[([^\]|]+)\|([^\]]+)\]\]', r'\2', text)
    # [[path]] → last segment, hyphens → spaces
    def to_name(m):
        seg = m.group(1).split("/")[-1]
        return seg.replace("-", " ").replace("_", " ")
    text = re.sub(r'\[\[([^\]]+)\]\]', to_name, text)
    return text


def load(path) -> str:
    """Read, strip frontmatter, and normalise wiki-links."""
    try:
        raw = Path(path).read_text(encoding="utf-8")
    except FileNotFoundError:
        return f"*File not found: {path}*\n"
    raw = strip_frontmatter(raw)
    raw = process_wikilinks(raw)
    return raw


def to_html(md: str) -> str:
    return markdown2.markdown(
        md,
        extras=[
            "tables", "fenced-code-blocks", "header-ids",
            "strike", "cuddled-lists", "footnotes",
        ],
    )


# ─── CSS ──────────────────────────────────────────────────────────────────────

BASE_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Page setup ─────────────────────────────────────────────── */
@page {
    size: A4;
    margin: 22mm 20mm 25mm 22mm;
    @top-center {
        content: string(chapter-title);
        font-family: 'Inter', sans-serif;
        font-size: 8pt;
        color: #6b7280;
        letter-spacing: 0.04em;
    }
    @bottom-center {
        content: counter(page) " / " counter(pages);
        font-family: 'Inter', sans-serif;
        font-size: 8pt;
        color: #9ca3af;
    }
    @bottom-left {
        content: "BuyerBench Research — Confidential";
        font-family: 'Inter', sans-serif;
        font-size: 7.5pt;
        color: #d1d5db;
    }
}

@page :first { margin-top: 0; @top-center { content: ""; } @bottom-left { content: ""; } @bottom-center { content: ""; } }

/* ── Reset ───────────────────────────────────────────────────── */
* { box-sizing: border-box; margin: 0; padding: 0; }

body {
    font-family: 'Inter', 'Helvetica Neue', Arial, sans-serif;
    font-size: 9.5pt;
    line-height: 1.65;
    color: #1f2937;
    background: white;
}

/* ── Cover page ──────────────────────────────────────────────── */
.cover-page {
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 60pt 50pt;
    background: #0f172a;
    color: white;
    page-break-after: always;
}

.cover-eyebrow {
    font-size: 8pt;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #60a5fa;
    margin-bottom: 24pt;
}

.cover-title {
    font-size: 28pt;
    font-weight: 700;
    line-height: 1.2;
    color: white;
    margin-bottom: 16pt;
    max-width: 440pt;
}

.cover-subtitle {
    font-size: 13pt;
    font-weight: 300;
    color: #94a3b8;
    line-height: 1.5;
    max-width: 400pt;
    margin-bottom: 48pt;
}

.cover-meta {
    font-size: 8.5pt;
    color: #64748b;
    line-height: 2;
}

.cover-accent {
    width: 60pt;
    height: 4pt;
    background: #3b82f6;
    margin-bottom: 24pt;
    border-radius: 2pt;
}

.cover-stats {
    display: flex;
    gap: 32pt;
    margin-top: 40pt;
    padding-top: 24pt;
    border-top: 1pt solid #1e3a5f;
}

.stat-block { flex: 1; }
.stat-number {
    font-size: 22pt;
    font-weight: 700;
    color: #60a5fa;
    display: block;
}
.stat-label {
    font-size: 8pt;
    color: #64748b;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

/* ── TOC page ────────────────────────────────────────────────── */
.toc-page {
    page-break-before: always;
    page-break-after: always;
    padding: 30pt 0;
}

.toc-page h2 {
    font-size: 18pt;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 24pt;
    padding-bottom: 8pt;
    border-bottom: 2pt solid #e2e8f0;
}

.toc-section { margin-bottom: 8pt; }
.toc-section a {
    text-decoration: none;
    color: #1e40af;
    font-size: 10pt;
    display: flex;
    justify-content: space-between;
}
.toc-part {
    font-size: 11pt;
    font-weight: 600;
    color: #0f172a;
    margin-top: 12pt;
    margin-bottom: 4pt;
    letter-spacing: 0.02em;
}
.toc-sub {
    padding-left: 16pt;
    font-size: 9pt;
    color: #4b5563;
    line-height: 1.9;
}

/* ── Section divider ─────────────────────────────────────────── */
.section-divider {
    page-break-before: always;
    padding: 50pt 0 30pt 0;
    border-bottom: 3pt solid #1e40af;
    margin-bottom: 28pt;
}

.section-number {
    font-size: 10pt;
    font-weight: 600;
    color: #3b82f6;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 8pt;
}

.section-title {
    font-size: 22pt;
    font-weight: 700;
    color: #0f172a;
    line-height: 1.2;
    margin-bottom: 8pt;
}

.section-description {
    font-size: 10.5pt;
    color: #6b7280;
    line-height: 1.5;
    max-width: 480pt;
}

/* ── Card/profile wrapper ────────────────────────────────────── */
.profile-card {
    border: 1pt solid #e5e7eb;
    border-radius: 6pt;
    padding: 18pt 20pt;
    margin: 16pt 0;
    background: #fafafa;
    page-break-inside: avoid;
}

.profile-card h2 {
    font-size: 14pt !important;
    border-bottom: none !important;
    padding-bottom: 0 !important;
    margin-bottom: 8pt !important;
    color: #1e40af !important;
}

/* ── Typography ──────────────────────────────────────────────── */
h1 {
    font-size: 20pt;
    font-weight: 700;
    color: #0f172a;
    line-height: 1.25;
    margin: 28pt 0 12pt;
    padding-bottom: 8pt;
    border-bottom: 2pt solid #e2e8f0;
    string-set: chapter-title content();
}

h1:first-child { margin-top: 0; }

h2 {
    font-size: 14pt;
    font-weight: 600;
    color: #1e3a5f;
    margin: 22pt 0 8pt;
    padding-bottom: 4pt;
    border-bottom: 1pt solid #e5e7eb;
}

h3 {
    font-size: 11.5pt;
    font-weight: 600;
    color: #374151;
    margin: 16pt 0 6pt;
}

h4 {
    font-size: 10pt;
    font-weight: 600;
    color: #4b5563;
    margin: 12pt 0 4pt;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

p {
    margin: 6pt 0 8pt;
    text-align: justify;
    hyphens: auto;
}

/* ── Tables ──────────────────────────────────────────────────── */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 12pt 0 16pt;
    font-size: 8.5pt;
    page-break-inside: avoid;
}

thead {
    background: #1e3a5f;
    color: white;
}

th {
    padding: 7pt 9pt;
    text-align: left;
    font-weight: 600;
    font-size: 8pt;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

td {
    padding: 6pt 9pt;
    border-bottom: 0.5pt solid #e5e7eb;
    vertical-align: top;
    line-height: 1.5;
}

tr:nth-child(even) td { background: #f8fafc; }
tr:hover td { background: #eff6ff; }

/* ── Blockquote ──────────────────────────────────────────────── */
blockquote {
    border-left: 3pt solid #3b82f6;
    padding: 8pt 14pt;
    margin: 12pt 0;
    background: #eff6ff;
    border-radius: 0 4pt 4pt 0;
    font-size: 9pt;
    color: #1e3a5f;
    font-style: italic;
}

/* ── Code ────────────────────────────────────────────────────── */
code {
    font-family: 'JetBrains Mono', 'Courier New', monospace;
    font-size: 8pt;
    background: #f1f5f9;
    padding: 1pt 4pt;
    border-radius: 2pt;
    color: #be185d;
}

pre {
    background: #0f172a;
    color: #e2e8f0;
    padding: 12pt;
    border-radius: 4pt;
    overflow: hidden;
    font-size: 7.5pt;
    margin: 10pt 0;
    white-space: pre-wrap;
    word-break: break-all;
    page-break-inside: avoid;
}

pre code {
    background: transparent;
    color: #e2e8f0;
    padding: 0;
}

/* ── Lists ───────────────────────────────────────────────────── */
ul, ol {
    margin: 4pt 0 8pt 18pt;
    padding: 0;
}

li {
    margin: 3pt 0;
    line-height: 1.55;
}

li > ul, li > ol { margin-top: 2pt; margin-bottom: 2pt; }

/* ── Horizontal rule ─────────────────────────────────────────── */
hr {
    border: none;
    border-top: 1pt solid #e5e7eb;
    margin: 20pt 0;
}

/* ── Utility ─────────────────────────────────────────────────── */
.page-break { page-break-after: always; }
.avoid-break { page-break-inside: avoid; }

.badge {
    display: inline-block;
    background: #dbeafe;
    color: #1d4ed8;
    font-size: 7pt;
    font-weight: 600;
    padding: 2pt 6pt;
    border-radius: 10pt;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-left: 4pt;
    vertical-align: middle;
}

.badge-green { background: #d1fae5; color: #065f46; }
.badge-orange { background: #fed7aa; color: #9a3412; }
.badge-red { background: #fee2e2; color: #991b1b; }

.caption {
    font-size: 8pt;
    color: #9ca3af;
    font-style: italic;
    text-align: center;
    margin-top: -8pt;
    margin-bottom: 12pt;
}

strong { font-weight: 600; color: #111827; }
em { color: #374151; }

a { color: #1d4ed8; text-decoration: none; }
"""

# ─── Cover page builder ────────────────────────────────────────────────────────

def cover_page(title: str, subtitle: str, stats: list[tuple[str, str]]) -> str:
    stats_html = "".join(
        f'<div class="stat-block"><span class="stat-number">{n}</span>'
        f'<span class="stat-label">{l}</span></div>'
        for n, l in stats
    )
    return f"""
<div class="cover-page">
  <div class="cover-eyebrow">BuyerBench Research Vault · April 2026</div>
  <div class="cover-accent"></div>
  <div class="cover-title">{title}</div>
  <div class="cover-subtitle">{subtitle}</div>
  <div class="cover-meta">
    Produced by: CladiBuyer Benchmarker · Agent ID: c3979248-d3dc-4fb4-b1ec-77fe56642647<br>
    Research period: 2026-04-04 — 2026-04-06<br>
    Classification: Internal Research · BuyerBench Framework v1.0
  </div>
  <div class="cover-stats">{stats_html}</div>
</div>
"""


def section_div(num: str, title: str, desc: str = "") -> str:
    desc_html = f'<div class="section-description">{desc}</div>' if desc else ""
    return f"""
<div class="section-divider">
  <div class="section-number">{num}</div>
  <div class="section-title">{title}</div>
  {desc_html}
</div>
"""


# ─── Report 1: Global ─────────────────────────────────────────────────────────

def build_global_report() -> str:
    parts = []

    # Cover
    parts.append(cover_page(
        "AI Buyer Agents &amp; Autonomous Procurement",
        "Global Market Research Report — Competitive Landscape, Pricing Registry, "
        "Company &amp; Protocol Profiles, Security Frameworks, and Research Foundations",
        [
            ("37", "Entities Profiled"),
            ("100%", "Vault Coverage"),
            ("$15T+", "B2B AI Agent TAM by 2028"),
            ("22", "Key Market Events"),
        ],
    ))

    # TOC
    parts.append("""
<div class="toc-page">
<h2>Table of Contents</h2>

<div class="toc-part">Part I — Executive Overview</div>
<div class="toc-sub">
  Market Snapshot &amp; Navigation Guide<br>
  Recent Developments (2025–2026)
</div>

<div class="toc-part">Part II — Competitive Landscape</div>
<div class="toc-sub">
  4-Layer Market Map<br>
  Competitive Clusters &amp; Head-to-Head Analysis<br>
  Events Timeline (Apr 2025 – Apr 2026)<br>
  White Space &amp; Market Gaps
</div>

<div class="toc-part">Part III — Global Pricing Registry</div>
<div class="toc-sub">
  AI Model API Costs (OpenAI, Google, Amazon)<br>
  Agent Runtime &amp; Orchestration Infrastructure<br>
  Consumer Subscription Tiers<br>
  Payment Infrastructure Per-Transaction Rates<br>
  Pricing Observations &amp; Brazil Comparison
</div>

<div class="toc-part">Part IV — Company Profiles (10 Companies)</div>
<div class="toc-sub">
  Procure AI · Omnea · Zycus · Fairmarkit · Skyfire<br>
  Amazon Agentic Commerce · OpenAI Agent Platform · Google Agentic Commerce<br>
  Stripe Agent Payments · Coinbase Agent Payments
</div>

<div class="toc-part">Part V — Product &amp; Platform Profiles (5 Products)</div>
<div class="toc-sub">
  Amazon Rufus / Buy for Me / Alexa+<br>
  ChatGPT Operator · Perplexity Comet<br>
  Salesforce Agentforce · NegMAS
</div>

<div class="toc-part">Part VI — Protocols &amp; Standards (5 Protocols)</div>
<div class="toc-sub">
  ACP (Agentic Commerce Protocol)<br>
  AP2 / UCP (Google) · x402 (Coinbase)<br>
  Visa Intelligent Commerce + TAP · Mastercard Agent Pay
</div>

<div class="toc-part">Part VII — Security &amp; Compliance Frameworks (5 Frameworks)</div>
<div class="toc-sub">
  PCI DSS v4.0 · EMV 3-D Secure (3DS2)<br>
  NIST AI RMF 1.0 · ISO/IEC 42001:2023 · FATF AML/CFT
</div>

<div class="toc-part">Part VIII — Academic Research Foundations (5 Papers)</div>
<div class="toc-sub">
  ACES · LLM Agent Benchmarking Survey<br>
  AgentBench · WebArena · WebShop
</div>

<div class="toc-part">Part IX — Key People (7 Profiles)</div>
<div class="toc-sub">
  Amine Allouah · Omar Besbes · Yasser Mohammad<br>
  Kevin Frechette · Amir Sarhangi · Rubail Birwadker · Jorn Lambert
</div>
</div>
""")

    # Part I — Executive Overview
    parts.append(section_div("Part I", "Executive Overview",
        "Global market snapshot, navigation guide, and recent competitive developments "
        "as of April 2026 across the AI buyer agent and autonomous procurement ecosystem."))
    parts.append(to_html(load(VAULT / "INDEX.md")))

    # Part II — Competitive Landscape
    parts.append(section_div("Part II", "Global Competitive Landscape",
        "4-layer market map, 4 competitive clusters, 12 head-to-head comparison tables, "
        "22-event timeline, and 8 identified white-space opportunities."))
    parts.append(to_html(load(VAULT / "Competitive-Landscape.md")))

    # Part III — Pricing Registry
    parts.append(section_div("Part III", "Global Pricing Registry",
        "Consolidated pricing across all 37 vault entities — model APIs, agent runtimes, "
        "consumer subscriptions, enterprise SaaS, and payment infrastructure."))
    parts.append(to_html(load(VAULT / "Pricing-Registry.md")))

    # Part IV — Company Profiles
    company_order = [
        "Procure-AI", "Omnea", "Zycus", "Fairmarkit", "Skyfire",
        "Amazon-Agentic-Commerce", "OpenAI-Agent-Platform",
        "Google-Agentic-Commerce", "Stripe-Agent-Payments", "Coinbase-Agent-Payments",
    ]
    parts.append(section_div("Part IV", "Company Profiles",
        "Detailed profiles of 10 key companies across procurement platforms, "
        "AI agent runtimes, and payment infrastructure."))
    for name in company_order:
        path = VAULT / "Companies" / f"{name}.md"
        parts.append(f'<div class="profile-card">')
        parts.append(to_html(load(path)))
        parts.append('</div>')

    # Part V — Product Profiles
    product_order = [
        "Amazon-Rufus-BuyForMe", "ChatGPT-Operator", "Perplexity-Comet",
        "Salesforce-Agentforce", "NegMAS",
    ]
    parts.append(section_div("Part V", "Product &amp; Platform Profiles",
        "Five key products spanning consumer shopping agents, enterprise procurement platforms, "
        "and open-source negotiation frameworks."))
    for name in product_order:
        path = VAULT / "Products" / f"{name}.md"
        parts.append('<div class="profile-card">')
        parts.append(to_html(load(path)))
        parts.append('</div>')

    # Part VI — Protocols & Standards
    parts.append(section_div("Part VI", "Protocols &amp; Standards",
        "Five active commerce protocols governing agent identity, payment authorization, "
        "and transaction execution as of April 2026."))
    # ACP is in Technologies/
    parts.append('<div class="profile-card">')
    parts.append(to_html(load(VAULT / "Technologies" / "ACP.md")))
    parts.append('</div>')
    for name in ["AP2-UCP", "x402", "Visa-Intelligent-Commerce", "Mastercard-Agent-Pay"]:
        parts.append('<div class="profile-card">')
        parts.append(to_html(load(VAULT / "Protocols" / f"{name}.md")))
        parts.append('</div>')

    # Part VII — Security & Compliance
    frameworks = ["PCI-DSS-v4", "EMV-3DS2", "NIST-AI-RMF", "ISO-42001", "FATF-AML-CFT"]
    parts.append(section_div("Part VII", "Security &amp; Compliance Frameworks",
        "Five regulatory and security frameworks defining the compliance requirements "
        "for AI buyer agents and autonomous payment systems."))
    for name in frameworks:
        parts.append('<div class="profile-card">')
        parts.append(to_html(load(VAULT / "Security-Compliance" / f"{name}.md")))
        parts.append('</div>')

    # Part VIII — Research Papers
    papers = [
        "ACES-AI-Agent-Buying", "LLM-Agent-Benchmarking-Survey",
        "AgentBench", "WebArena", "WebShop",
    ]
    parts.append(section_div("Part VIII", "Academic Research Foundations",
        "Five foundational research papers that ground BuyerBench's evaluation methodology "
        "across all three pillars."))
    for name in papers:
        parts.append('<div class="profile-card">')
        parts.append(to_html(load(VAULT / "Research-Papers" / f"{name}.md")))
        parts.append('</div>')

    # Part IX — Key People
    people = [
        "Amine-Allouah", "Omar-Besbes", "Yasser-Mohammad",
        "Kevin-Frechette", "Amir-Sarhangi", "Rubail-Birwadker", "Jorn-Lambert",
    ]
    parts.append(section_div("Part IX", "Key People",
        "Seven key individuals across academic research, procurement technology, "
        "and payment infrastructure shaping the AI buyer agent landscape."))
    for name in people:
        parts.append('<div class="profile-card">')
        parts.append(to_html(load(VAULT / "People" / f"{name}.md")))
        parts.append('</div>')

    html_body = "\n".join(parts)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>AI Buyer Agents &amp; Autonomous Procurement — Global Market Research Report</title>
</head>
<body>
{html_body}
</body>
</html>"""


# ─── Report 2: Brazil ─────────────────────────────────────────────────────────

def build_brazil_report() -> str:
    parts = []

    # Cover
    parts.append(cover_page(
        "AI Buyer Agents in Brazil — Market Analysis",
        "Deep-dive into Brazil's AI procurement ecosystem: Pix infrastructure, "
        "TOTVS dominance, LGPD/Open Finance compliance stack, domestic startups, "
        "and global player localization gaps.",
        [
            ("25", "Brazil Entities"),
            ("R$234B", "Brazil B2B E-Commerce"),
            ("18.42%", "B2B CAGR"),
            ("4", "Compliance Planes"),
        ],
    ))

    # TOC
    parts.append("""
<div class="toc-page">
<h2>Table of Contents</h2>

<div class="toc-part">Part I — Brazil vs. Global Analysis</div>
<div class="toc-sub">
  Market Size Comparison<br>
  Infrastructure Contrast: Pix vs. Card Networks<br>
  ERP Ecosystem: TOTVS vs. SAP/Oracle<br>
  Regulatory Architecture: Four-Plane Compliance<br>
  Localization Gaps for Global Players<br>
  Market Entry Priority Framework
</div>

<div class="toc-part">Part II — Market Context</div>
<div class="toc-sub">
  Brazil AI Procurement Landscape<br>
  Brazil B2B Marketplace Landscape<br>
  Brazil ERP Landscape<br>
  Brazil Fintech &amp; Payment Landscape<br>
  Global Players: Brazil Presence Analysis
</div>

<div class="toc-part">Part III — Brazil Company Profiles (9 Companies)</div>
<div class="toc-sub">
  AI Procurement Startups: Freedom · Zinit · Linkana · Pipefy<br>
  Fintech &amp; Payments: Nubank Nu Empresas · Stone (StoneCo)<br>
  Celcoin · ASAAS · Belvo
</div>

<div class="toc-part">Part IV — Brazil Product &amp; Platform Profiles (5 Platforms)</div>
<div class="toc-sub">
  Mercado Livre Negócios · TOTVS ERP + Procurement<br>
  Compras.gov.br / PNCP · B2Brazil · Nomos Legislativo
</div>

<div class="toc-part">Part V — Regulatory Frameworks (6 Documents)</div>
<div class="toc-sub">
  LGPD · Pix · Open Finance Brazil<br>
  BACEN AI Governance · Brazil Procurement Regulation<br>
  Brazil Compliance Overview (4-Plane Synthesis)
</div>
</div>
""")

    # Part I — Brazil vs Global
    parts.append(section_div("Part I", "Brazil vs. Global — AI Buyer Agent Market",
        "Dimension-by-dimension comparison of Brazil vs. global (US/EU) across payment rails, "
        "ERP ecosystem, regulatory architecture, and competitive positioning."))
    parts.append(to_html(load(VAULT / "Brazil" / "Brazil-vs-Global-Analysis.md")))

    # Part II — Market Context
    market_context_order = [
        "Brazil-AI-Procurement-Landscape",
        "Brazil-B2B-Marketplace-Landscape",
        "Brazil-ERP-Landscape",
        "Brazil-Fintech-Payment-Landscape",
        "Global-Players-Brazil-Presence",
    ]
    parts.append(section_div("Part II", "Brazil Market Context",
        "Five market landscape analyses covering domestic AI startups, B2B marketplace platforms, "
        "ERP vendors, fintech payment infrastructure, and global player gaps."))
    for name in market_context_order:
        parts.append('<div class="profile-card">')
        parts.append(to_html(load(VAULT / "Brazil" / "Market-Context" / f"{name}.md")))
        parts.append('</div>')

    # Part III — Brazil Companies
    brazil_companies = [
        "Freedom", "Zinit", "Linkana", "Pipefy",
        "Nubank-Nu-Empresas", "Stone-StoneCo", "Celcoin", "ASAAS", "Belvo",
    ]
    parts.append(section_div("Part III", "Brazil Company Profiles",
        "Nine Brazilian companies spanning AI procurement startups and fintech/payment infrastructure."))
    for name in brazil_companies:
        parts.append('<div class="profile-card">')
        parts.append(to_html(load(VAULT / "Brazil" / "Companies" / f"{name}.md")))
        parts.append('</div>')

    # Part IV — Brazil Products
    brazil_products = [
        "Mercado-Livre-Negocios", "TOTVS-ERP-Procurement",
        "Compras-gov-br", "B2Brazil", "Nomos-Legislativo",
    ]
    parts.append(section_div("Part IV", "Brazil Product &amp; Platform Profiles",
        "Five B2B marketplace and procurement platforms serving the Brazilian market."))
    for name in brazil_products:
        parts.append('<div class="profile-card">')
        parts.append(to_html(load(VAULT / "Brazil" / "Products" / f"{name}.md")))
        parts.append('</div>')

    # Part V — Regulatory
    regulatory_order = [
        "LGPD", "Pix", "Open-Finance-Brazil",
        "BACEN-AI-Governance", "Brazil-Procurement-Regulation",
        "Brazil-Compliance-Overview",
    ]
    parts.append(section_div("Part V", "Brazil Regulatory Frameworks",
        "Six regulatory frameworks forming Brazil's four-plane compliance architecture "
        "for AI buyer agents: data privacy, payment systems, open finance, and procurement law."))
    for name in regulatory_order:
        parts.append('<div class="profile-card">')
        parts.append(to_html(load(VAULT / "Brazil" / "Regulatory" / f"{name}.md")))
        parts.append('</div>')

    html_body = "\n".join(parts)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>AI Buyer Agents in Brazil — Market Analysis</title>
</head>
<body>
{html_body}
</body>
</html>"""


# ─── Main ─────────────────────────────────────────────────────────────────────

def render(html: str, css: str, out_path: Path, label: str) -> None:
    print(f"  Rendering {label} ...", flush=True)
    HTML(string=html, base_url=str(OUTPUT_DIR)).write_pdf(
        str(out_path),
        stylesheets=[CSS(string=css)],
        optimize_images=True,
    )
    size_mb = out_path.stat().st_size / 1_048_576
    print(f"  ✓ {out_path.name}  ({size_mb:.1f} MB, {out_path.stat().st_size:,} bytes)")


def main() -> None:
    print("\nBuyerBench PDF Report Generator")
    print("=" * 40)

    print("\n[1/4] Building Global Market Research HTML ...", flush=True)
    global_html = build_global_report()

    print("[2/4] Building Brazil Market Analysis HTML ...", flush=True)
    brazil_html = build_brazil_report()

    print("[3/4] Rendering PDFs ...", flush=True)
    global_out = OUTPUT_DIR / "Global-Market-Research-Report.pdf"
    brazil_out = OUTPUT_DIR / "Brazil-Market-Analysis.pdf"

    render(global_html, BASE_CSS, global_out, "Global Report")
    render(brazil_html, BASE_CSS, brazil_out, "Brazil Analysis")

    print("\n[4/4] Done.")
    print(f"  → {global_out}")
    print(f"  → {brazil_out}")
    print()


if __name__ == "__main__":
    main()
