# Phase 03: Academic Report Generator via Claude CLI

This phase builds the academic paper generation pipeline. After a benchmark run completes, the user provides a short "test context" string describing the experiment (e.g., dataset scope, hardware, date, research question). BuyerBench then invokes Claude CLI with a structured prompt that includes the results JSON, the test context, and the full contents of `docs/paper/references.bib`. Claude writes a complete academic paper in IEEE/Markdown format with a properly formatted bibliography. The output is saved as `ACADEMIC-REPORT.md` alongside the session results.

## Tasks

- [x] Read `buyerbench/review.py` in full (the existing Claude CLI invocation pattern), `docs/paper/references.bib` (note the citation keys available — e.g., `kahneman1979`, `tversky1981`, `stripefraud2023`), and `results/session_export.py` before writing anything. Understand the subprocess invocation pattern and the existing data structures for results.

- [x] Create `buyerbench/academic_report.py` with a `build_academic_prompt()` function:
  - Signature: `build_academic_prompt(results: list[dict], session_meta: dict, test_context: str, references_bib: str) -> str`
  - The prompt must instruct Claude to write a full academic paper with these sections: Abstract (150 words), 1. Introduction, 2. Related Work (cite ≥5 sources from the bib using `[@key]` syntax), 3. Methodology (describe the BuyerBench 3-pillar framework), 4. Experimental Setup (inject `test_context` verbatim here), 5. Results (embed per-agent score tables in Markdown), 6. Discussion (bias susceptibility findings, security posture), 7. Conclusion, References (full bibliography from `references.bib`)
  - The prompt should include the full `references.bib` content in a fenced block labeled `BIBLIOGRAPHY SOURCE` with instructions: "Cite only from these keys. Format all in-text citations as [@key]. Render the References section as a numbered list with full BibTeX-formatted entries."
  - Embed the results as a JSON block labeled `BENCHMARK RESULTS`
  - Keep the prompt under 8000 tokens to fit within typical Claude CLI context budgets

- [x] Add `generate_academic_report()` to `buyerbench/academic_report.py`:
  - Signature: `generate_academic_report(results_dir: str, test_context: str, output_path: str = "ACADEMIC-REPORT.md", cli_path: str = "claude", timeout: int = 600, bib_path: str = "docs/paper/references.bib") -> str`
  - Load result JSON files from `results_dir` (same pattern as `_load_results()` in `review.py` — skip status=skipped)
  - Read `bib_path` file contents
  - Build prompt via `build_academic_prompt()`
  - Invoke `claude --print <prompt>` via `subprocess.run()` with `timeout=timeout`, capture stdout
  - Write the output to `output_path` with a YAML front matter header:
    ```yaml
    ---
    type: report
    title: BuyerBench Academic Report
    created: <ISO date>
    tags: [benchmark, academic, buyer-agent, evaluation]
    ---
    ```
  - Return the generated text or a descriptive error string if the subprocess fails

- [x] Add an `academic-report` command to `buyerbench/__main__.py`:
  - Usage: `python -m buyerbench academic-report --results-dir <dir> [--test-context <str>] [--test-context-file <path>] [--output ACADEMIC-REPORT.md] [--bib-path docs/paper/references.bib] [--cli-path claude]`
  - `--test-context` and `--test-context-file` are mutually exclusive; if neither is provided, use a default: `"Evaluation conducted on BuyerBench v1.0. See session-config.yaml for agent and scenario configuration."`
  - Call `generate_academic_report()` with the resolved arguments
  - Print a progress spinner ("Generating academic report via Claude CLI...") while the subprocess runs
  - On completion, print the output path and first 3 lines of the generated abstract

- [x] Wire the academic report generation into the `run` command's post-run flow in `buyerbench/__main__.py`:
  - Add optional `--academic-report / --no-academic-report` flag (default: `--no-academic-report`)
  - Add optional `--test-context TEXT` flag used only when `--academic-report` is set
  - After session export (MD + CSV), if `--academic-report` is set, call `generate_academic_report()` with `results_dir=output_dir` and save to `<output_dir>/ACADEMIC-REPORT.md`

- [x] Write tests in `tests/test_academic_report.py`:
  - Test `build_academic_prompt()` returns a string containing "Abstract", "Related Work", "References", and at least one `[@` citation reference
  - Test that the prompt includes the test_context string verbatim
  - Test that the references.bib content appears in the prompt
  - Mock `subprocess.run` to return a fake paper string; test `generate_academic_report()` writes the front matter + content to the output file
  - Run `pytest tests/test_academic_report.py -v` and confirm all pass
