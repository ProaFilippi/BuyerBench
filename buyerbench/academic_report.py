"""Academic paper generation pipeline for BuyerBench.

Reads benchmark result JSONs from a results directory, builds a structured
prompt, and invokes the Claude CLI to produce a full IEEE-style academic paper
with a properly formatted bibliography.

Usage (via CLI):
    python -m buyerbench academic-report --results-dir results/my-run
"""
from __future__ import annotations

import json
import subprocess
from datetime import date
from pathlib import Path


def _load_results(results_dir: Path) -> list[dict]:
    """Load all non-skipped scenario result JSONs from *results_dir*."""
    results = []
    for path in sorted(results_dir.glob("*.json")):
        try:
            data = json.loads(path.read_text())
        except (json.JSONDecodeError, OSError):
            continue
        if data.get("status") == "skipped":
            continue
        results.append(data)
    return results


def build_academic_prompt(
    results: list[dict],
    session_meta: dict,
    test_context: str,
    references_bib: str,
) -> str:
    """Build the Claude prompt for academic paper generation.

    Parameters
    ----------
    results:
        List of per-scenario result dicts (as loaded from JSON files).
    session_meta:
        Session metadata dict (e.g. agent_ids, session_id, timestamps).
    test_context:
        Free-text description of the experiment injected verbatim into §4.
    references_bib:
        Full content of the references.bib file.

    Returns
    -------
    A prompt string ready to be passed to ``claude --print``.
    """
    results_block = json.dumps(results, indent=2)
    agent_ids = session_meta.get("agents", [])
    agent_list = ", ".join(agent_ids) if agent_ids else "unknown"

    return f"""You are an expert academic writer specialising in AI evaluation research. \
Write a complete academic paper in IEEE/Markdown format based on the BuyerBench benchmark \
results provided below.

## PAPER STRUCTURE

Write **all** of the following numbered sections in order:

### Abstract
A single paragraph of approximately 150 words summarising the research question, \
methodology (the 3-pillar BuyerBench framework), key findings, and conclusions.

### 1. Introduction
Motivate the problem of evaluating AI buyer agents in procurement workflows. \
Explain why a multi-dimensional benchmark (capability, economic rationality, security) \
is needed. State the paper's contributions. Cite relevant background work using [@key] syntax.

### 2. Related Work
Survey at least 5 related works from the bibliography below. Cover: agent benchmarks, \
LLM cognitive bias, payment security standards, and agentic commerce protocols. \
Use [@key] in-text citations for every work cited.

### 3. Methodology
Describe the BuyerBench 3-pillar evaluation framework in detail:
- **Pillar 1 — Agent Intelligence & Operational Capability**: supplier discovery, \
  quote comparison, multi-step procurement workflows, tool usage.
- **Pillar 2 — Economic Decision Quality & Behavioral Robustness**: optimality gap, \
  expected-value regret, bias susceptibility index (BSI), framing/anchoring/decoy/sunk-cost tests.
- **Pillar 3 — Security, Compliance & Market Readiness**: PCI-DSS compliance, fraud \
  detection, prompt injection resistance, credential handling, transaction sequencing.

### 4. Experimental Setup
Inject the following test context **verbatim** (do not paraphrase):

> {test_context}

Also note that the following agent(s) were evaluated: {agent_list}.

### 5. Results
Present per-agent score tables in Markdown. Include at minimum:
- A table of mean Pillar 1 / Pillar 2 / Pillar 3 scores per agent.
- A bias susceptibility summary (BSI values by bias type where available).
- A security compliance summary (compliance rate, violation frequency where available).
Derive these tables from the BENCHMARK RESULTS block below.

### 6. Discussion
Analyse the findings:
- Which agents showed strong vs. weak bias susceptibility? What does this imply?
- What is the security posture of each agent? Which failures represent production risks?
- What are the limitations of this evaluation (scenario coverage, scoring methodology, \
  generalisability)?

### 7. Conclusion
Summarise the key contributions and findings in 2–3 paragraphs. Propose future work.

### References
Render a numbered reference list. Include **only** entries whose citation keys appear \
in the body of the paper. Format each entry in BibTeX-derived prose style \
(Author(s), "Title", *Journal/Venue*, year. DOI/URL if available).

---

## BIBLIOGRAPHY SOURCE

```bibtex
{references_bib}
```

**Instructions for citations:**
- Cite **only** from the keys defined in the BIBLIOGRAPHY SOURCE above.
- Format all in-text citations as `[@key]` (e.g. `[@kahneman1979prospect]`).
- In the References section, render a numbered list with full bibliographic entries.
- Do **not** invent or hallucinate citation keys that are not in the bib file.

---

## BENCHMARK RESULTS

```json
{results_block}
```

---

**Formatting requirements:**
- Use Markdown headings (`##`, `###`) for sections and subsections.
- Use standard Markdown tables for all tabular data.
- Write for a technical audience. Be precise, not diplomatic.
- Do **not** add a YAML front matter block — that will be added by the caller.
- Do **not** truncate or abbreviate — write the full paper.
"""


def generate_academic_report(
    results_dir: str,
    test_context: str,
    output_path: str = "ACADEMIC-REPORT.md",
    cli_path: str = "claude",
    timeout: int = 600,
    bib_path: str = "docs/paper/references.bib",
) -> str:
    """Invoke the Claude CLI to generate a full academic paper from benchmark results.

    Parameters
    ----------
    results_dir:
        Path to the directory containing per-scenario result JSON files.
    test_context:
        Free-text experiment description injected verbatim into §4 of the paper.
    output_path:
        File path for the generated ``ACADEMIC-REPORT.md``.
    cli_path:
        Path to the ``claude`` binary. Defaults to ``"claude"`` (PATH lookup).
    timeout:
        Subprocess timeout in seconds.
    bib_path:
        Path to the BibTeX references file.

    Returns
    -------
    The generated paper text (with front matter prepended) as a string.
    Returns a descriptive error string (not an exception) if the CLI fails.
    """
    results_path = Path(results_dir)
    if not results_path.exists():
        return f"ERROR: Results directory not found: {results_dir}"

    results = _load_results(results_path)
    if not results:
        return f"ERROR: No valid result files found in {results_dir}"

    bib_file = Path(bib_path)
    if not bib_file.exists():
        return f"ERROR: Bibliography file not found: {bib_path}"

    references_bib = bib_file.read_text(encoding="utf-8")

    agent_ids = sorted({r.get("agent_id", "unknown") for r in results})
    session_meta = {"agents": agent_ids}

    prompt = build_academic_prompt(results, session_meta, test_context, references_bib)

    try:
        proc = subprocess.run(
            [cli_path, "--print", prompt],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        paper_text = proc.stdout.strip()
        if proc.returncode != 0 and not paper_text:
            paper_text = proc.stderr.strip()
        if not paper_text:
            return "ERROR: Claude CLI returned empty output."
    except subprocess.TimeoutExpired:
        return f"ERROR: Claude CLI timed out after {timeout}s."
    except FileNotFoundError:
        return f"ERROR: Claude CLI not found at '{cli_path}'."

    iso_date = date.today().isoformat()
    front_matter = (
        "---\n"
        "type: report\n"
        "title: BuyerBench Academic Report\n"
        f"created: {iso_date}\n"
        "tags: [benchmark, academic, buyer-agent, evaluation]\n"
        "---\n\n"
    )

    full_output = front_matter + paper_text
    Path(output_path).write_text(full_output, encoding="utf-8")
    return full_output
