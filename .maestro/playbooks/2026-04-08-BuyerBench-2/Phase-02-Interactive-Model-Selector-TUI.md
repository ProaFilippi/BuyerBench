# Phase 02: Interactive Model Selector TUI

This phase adds a `buyerbench select` command that presents an interactive Rich-powered terminal UI for choosing which OpenRouter models to benchmark. The selector shows model metadata (provider, context window, cost tier, capability tags) in a filterable checklist, saves the selection to a session config file, and integrates with `buyerbench run` so a saved selection can be replayed without re-entering choices.

## Tasks

- [x] Create `buyerbench/model_catalog.py` — a static registry of the 10 OpenRouter models with rich metadata. Define a `ModelEntry` dataclass with fields: `agent_id: str`, `model_id: str`, `display_name: str`, `provider: str`, `context_k: int` (context window in thousands of tokens), `cost_tier: str` (one of "free", "low", "mid", "high"), `capability_tags: list[str]` (e.g. `["reasoning", "coding", "long-context"]`), and `description: str` (one sentence). Populate a module-level `MODEL_CATALOG: list[ModelEntry]` with all 10 models matching the registry from Phase 01:
  - GPT-4o: provider=OpenAI, context_k=128, cost_tier="high", tags=["reasoning","coding","multimodal"]
  - Claude 3.5 Sonnet: provider=Anthropic, context_k=200, cost_tier="high", tags=["reasoning","coding","long-context"]
  - Gemini Pro 1.5: provider=Google, context_k=1000, cost_tier="mid", tags=["long-context","multimodal"]
  - Llama 3.1 405B: provider=Meta, context_k=128, cost_tier="low", tags=["open-source","reasoning"]
  - Mistral Large: provider=Mistral, context_k=32, cost_tier="mid", tags=["reasoning","european"]
  - DeepSeek V3: provider=DeepSeek, context_k=64, cost_tier="low", tags=["coding","open-source"]
  - Qwen 2.5 72B: provider=Alibaba, context_k=128, cost_tier="low", tags=["multilingual","open-source"]
  - Command R+: provider=Cohere, context_k=128, cost_tier="mid", tags=["rag","enterprise"]
  - Mixtral 8x22B: provider=Mistral, context_k=64, cost_tier="low", tags=["moe","open-source"]
  - Yi Large 34B: provider=01.AI, context_k=32, cost_tier="low", tags=["multilingual","open-source"]
  
  Also add a `filter_catalog(providers: list[str] | None = None, tags: list[str] | None = None, cost_tiers: list[str] | None = None) -> list[ModelEntry]` function for programmatic filtering.

- [x] Create `buyerbench/selector.py` — the interactive selection engine using Rich. Import `rich.console.Console`, `rich.table.Table`, `rich.prompt.Prompt`, `rich.panel.Panel`, and `rich.text.Text`. Implement:
  - `display_catalog_table(catalog: list[ModelEntry], selected_ids: set[str]) -> None`: renders a Rich Table with columns: #, Model Name, Provider, Context, Cost, Tags, Selected (✓/·). Color-code cost tiers (green=low, yellow=mid, red=high). Use `rich.style` for selected rows highlight.
  - `interactive_select(catalog: list[ModelEntry] | None = None) -> list[str]`: the main TUI loop. Show the catalog table. Prompt for comma-separated numbers to toggle (e.g. "1,3,5"), "a" to select all, "c" to clear all, "f <tag>" to filter by tag, "p <provider>" to filter by provider, "done" to confirm. Re-render table after each action. Return list of selected `agent_id` strings. Validate that at least 1 model is selected before allowing "done".
  - `save_selection(agent_ids: list[str], path: str = "session-selection.yaml") -> None`: write YAML with `selected_agents: [...]` and `created_at: <ISO timestamp>`.
  - `load_selection(path: str = "session-selection.yaml") -> list[str]`: read YAML, return `selected_agents` list.

- [x] Add `select` command to the CLI in `buyerbench/__main__.py`. Read the file first to understand the exact click group and command pattern. Add:
  ```
  @cli.command()
  @click.option("--output", default="session-selection.yaml", help="Path to save the selection YAML")
  @click.option("--filter-tag", default=None, help="Pre-filter catalog by capability tag")
  @click.option("--filter-provider", default=None, help="Pre-filter catalog by provider name")
  def select(output, filter_tag, filter_provider):
  ```
  The command calls `interactive_select()` with any filters applied, then calls `save_selection(result, output)`, and prints a Rich confirmation panel showing the selected models and the output path. If the terminal is non-interactive (not a TTY), print an error and exit with code 1.

- [x] Add `--from-selection` option to the existing `run` command in `buyerbench/__main__.py`. When `--from-selection <path>` is provided (and `--agent` is not), load the YAML via `load_selection(path)` and run all selected agents in sequence using the existing run loop. The option should be mutually exclusive with `--agent all` but compatible with `--pillar` and `--dry-run`. Print a Rich panel at the start showing which models will be evaluated and from which selection file.

- [x] Write tests in `tests/test_selector.py`:
  - `test_model_catalog_complete`: assert `len(MODEL_CATALOG) == 10` and all entries have non-empty `agent_id`, `provider`, `description`.
  - `test_filter_by_tag`: `filter_catalog(tags=["open-source"])` returns only models with that tag.
  - `test_filter_by_provider`: `filter_catalog(providers=["Mistral"])` returns exactly Mistral Large and Mixtral 8x22B.
  - `test_save_load_roundtrip`: save a selection of 3 IDs to a temp file, load it back, assert the lists match.
  - `test_select_command_exists`: use `click.testing.CliRunner` to invoke `buyerbench select --help` and assert it exits 0 and shows `--output` and `--filter-tag` in the output.
  - `test_run_from_selection`: use CliRunner with `buyerbench run --from-selection <tmpfile> --dry-run` where tmpfile contains 2 openrouter agent IDs, assert the command runs without error.

- [x] Run `pytest tests/test_selector.py -v` and fix any failures. Then run the full test suite `pytest` to confirm no regressions from the `__main__.py` changes.
