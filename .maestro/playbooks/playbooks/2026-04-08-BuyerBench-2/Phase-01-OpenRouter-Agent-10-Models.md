# Phase 01: OpenRouter Agent Adapter + 10 Curated Models

This phase wires BuyerBench into OpenRouter's OpenAI-compatible API, registers 10 carefully selected models spanning frontier and open-source tiers, and plumbs the API key through the existing config and preflight systems. By the end, `python -m buyerbench run --agent openrouter-gpt-4o --dry-run` works, and `python -m buyerbench check` reports OpenRouter status alongside the existing CLI checks.

## Tasks

- [x] Add `requests` to `pyproject.toml` under `[project] dependencies` (alongside pydantic, pyyaml, rich, click). Also add an `[project.optional-dependencies]` entry `openrouter = ["requests"]` for documentation purposes. Run `pip install -e ".[dev]"` to install the updated dependencies.

- [x] Create `agents/openrouter_agent.py` implementing an OpenRouter HTTP adapter. The class `OpenRouterAgent` must inherit from `agents.__init__.BaseAgent` (NOT CLIAgent — this is a direct HTTP call, not a subprocess). Key implementation details:
  - Constructor: `__init__(self, model_id: str, timeout: int = 120, dry_run: bool = False)`. Store `self.model_id = model_id`, set `self.agent_id = f"openrouter-{model_id}"` (replacing `/` with `-` in model_id for safe IDs), `self.dry_run = dry_run`, `self.timeout = timeout`.
  - `respond(self, scenario: Scenario) -> AgentResponse`: call `harness.prompt.scenario_to_prompt(scenario)` to get the prompt string. If `self.dry_run`, print the prompt and return a stub `AgentResponse` with `decisions={}`, `raw_output="[dry-run]"`. Otherwise call `self._call_openrouter(prompt)`.
  - `_call_openrouter(self, prompt: str) -> AgentResponse`: measure latency with `time.monotonic()`. POST to `https://openrouter.ai/api/v1/chat/completions` with headers `Authorization: Bearer <key>`, `HTTP-Referer: https://github.com/BuyerBench`, `X-Title: BuyerBench`. Body: `{"model": self.model_id, "messages": [{"role": "user", "content": prompt}]}`. Read `OPENROUTER_API_KEY` from `os.environ`. On HTTP error or timeout, return `AgentResponse` with `raw_output=str(e)`. On success, extract `choices[0].message.content`, call `harness.prompt.parse_agent_output(content, scenario)`, and return `AgentResponse(scenario_id=scenario.id, agent_id=self.agent_id, decisions=parsed, raw_output=content, latency_ms=elapsed_ms)`.

- [x] Register all 10 OpenRouter model variants in `agents/registry.py`. First import `OpenRouterAgent` at the top. In `AGENT_REGISTRY`, add these 10 entries using the pattern `"openrouter-<slug>": OpenRouterAgent` where slug is the model_id with `/` replaced by `-`:
  - `"openrouter-openai-gpt-4o"` → model_id `"openai/gpt-4o"`
  - `"openrouter-anthropic-claude-3.5-sonnet"` → model_id `"anthropic/claude-3.5-sonnet"`
  - `"openrouter-google-gemini-pro-1.5"` → model_id `"google/gemini-pro-1.5"`
  - `"openrouter-meta-llama-llama-3.1-405b-instruct"` → model_id `"meta-llama/llama-3.1-405b-instruct"`
  - `"openrouter-mistralai-mistral-large"` → model_id `"mistralai/mistral-large"`
  - `"openrouter-deepseek-deepseek-chat"` → model_id `"deepseek/deepseek-chat"`
  - `"openrouter-qwen-qwen-2.5-72b-instruct"` → model_id `"qwen/qwen-2.5-72b-instruct"`
  - `"openrouter-cohere-command-r-plus"` → model_id `"cohere/command-r-plus"`
  - `"openrouter-mistralai-mixtral-8x22b-instruct"` → model_id `"mistralai/mixtral-8x22b-instruct"`
  - `"openrouter-01-ai-yi-large"` → model_id `"01-ai/yi-large"`
  
  Update `get_agent()` to handle the `openrouter-` prefix: if `agent_id.startswith("openrouter-")`, look up the model_id via a reverse map from the registry or a hardcoded `OPENROUTER_MODEL_MAP` dict at the top of the file, then instantiate `OpenRouterAgent(model_id=model_id, **config_kwargs)`. Pass `dry_run` and `timeout` from config dict if present.

- [x] Extend `harness/config.py` to support OpenRouter. In `load_config()`, add a new section to the returned dict: `config.setdefault("openrouter", {"api_key": None, "timeout": 60})`. Then add env-var override: `if key := os.environ.get("OPENROUTER_API_KEY"): config["openrouter"]["api_key"] = key`. Also respect `BUYERBENCH_TIMEOUT` for openrouter timeout. This follows the exact same pattern already used for `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, and `GOOGLE_API_KEY`.

- [x] Extend `harness/preflight.py` to check the OpenRouter API key. In `check_environment()`, after the existing API key checks for Claude/Codex/Gemini, add a new check block for OpenRouter:
  - Check if `OPENROUTER_API_KEY` is set in env (same pattern as other key checks).
  - Attempt a lightweight HTTP GET to `https://openrouter.ai/api/v1/models` with `Authorization: Bearer <key>` and a 5-second timeout using `requests`. If the response is 200, mark available. If key is missing or request fails, mark unavailable with reason.
  - Add all 10 `openrouter-*` agent IDs to `available_agents` in the result if the check passes.
  - Wrap in try/except ImportError in case `requests` is not installed — fail gracefully with a note to `pip install requests`.

- [x] Add OpenRouter configuration example to `buyerbench.config.yaml.example`. Add a new `openrouter:` section with `api_key: ""` and `timeout: 60`, plus a comment listing the 10 registered model IDs and a note that the key can also be set via the `OPENROUTER_API_KEY` environment variable. Read the existing file first to match the formatting style.

- [x] Update `CLAUDE.md`'s "Available agent IDs" comment block (in the `Commands` section) to list all 10 new `openrouter-*` agent IDs with one-line descriptions. Read the file first to find the exact location of the existing agent ID list and append below the `negmas` and `stripe-toolkit` entries.

- [x] Write tests for the OpenRouter adapter in `tests/test_openrouter_agent.py`:
  - `test_openrouter_agent_dry_run`: instantiate `OpenRouterAgent("openai/gpt-4o", dry_run=True)`, call `respond()` with a minimal mock Scenario, assert `raw_output == "[dry-run]"` and `decisions == {}`.
  - `test_openrouter_agent_id_format`: verify `agent_id` is `"openrouter-openai-gpt-4o"` (slashes become dashes).
  - `test_all_10_registered`: import `AGENT_REGISTRY` and assert all 10 `openrouter-*` keys are present.
  - `test_get_agent_openrouter`: call `get_agent("openrouter-openai-gpt-4o", {"dry_run": True})` and assert it returns an `OpenRouterAgent` instance.
  - Mock `requests.post` with `unittest.mock.patch` for a happy-path test: verify the POST body contains `model` and `messages` keys.

- [x] Verify the full integration with a dry-run smoke test and confirm tests pass:
  <!-- 506 tests pass. Dry-run for openrouter-openai-gpt-4o --pillar 1 prints 6 scenario prompts cleanly. -->
  - Run `python -m buyerbench run --agent openrouter-openai-gpt-4o --dry-run --pillar 1` and verify it prints scenario prompts without errors.
  - Run `pytest tests/test_openrouter_agent.py -v` and confirm all tests pass.
  - Run `python -m buyerbench check` and confirm OpenRouter section appears in the preflight report.
