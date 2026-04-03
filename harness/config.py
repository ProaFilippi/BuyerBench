"""Configuration loader for BuyerBench.

Loads agent configuration from ``buyerbench.config.yaml`` (or a custom path)
and merges in environment variable overrides.  Returns a plain dict so callers
can freely inspect or override values without touching files.

Config file format: see ``buyerbench.config.yaml.example`` in the repo root.

Environment variable overrides (take precedence over file values)
-----------------------------------------------------------------
  ANTHROPIC_API_KEY    → claude_code.api_key
  OPENAI_API_KEY       → codex.api_key
  GOOGLE_API_KEY       → gemini.api_key
  GEMINI_API_KEY       → gemini.api_key  (alias)
  BUYERBENCH_TIMEOUT   → timeout (global subprocess timeout in seconds)
  BUYERBENCH_DRY_RUN   → dry_run (set to "1" or "true" to enable)
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml

_DEFAULT_CONFIG_PATH = Path("buyerbench.config.yaml")


def load_config(path: str | Path | None = None) -> dict[str, Any]:
    """Load BuyerBench configuration, applying environment variable overrides.

    Parameters
    ----------
    path:
        Path to a YAML config file.  Defaults to ``buyerbench.config.yaml``
        in the current working directory.  Missing files are silently skipped
        (env vars alone are sufficient for minimal operation).

    Returns
    -------
    dict
        Merged configuration dict.  Always contains at minimum the keys
        ``"claude_code"``, ``"codex"``, ``"gemini"``, ``"timeout"``,
        and ``"dry_run"``.
    """
    config_path = Path(path) if path else _DEFAULT_CONFIG_PATH
    config: dict[str, Any] = {}

    if config_path.exists():
        with open(config_path) as fh:
            loaded = yaml.safe_load(fh)
            if isinstance(loaded, dict):
                config = loaded

    # Ensure top-level family keys exist
    config.setdefault("claude_code", {})
    config.setdefault("codex", {})
    config.setdefault("gemini", {})
    config.setdefault("timeout", 120)
    config.setdefault("dry_run", False)

    # Apply env var overrides
    if key := os.environ.get("ANTHROPIC_API_KEY"):
        config["claude_code"]["api_key"] = key
    if key := os.environ.get("OPENAI_API_KEY"):
        config["codex"]["api_key"] = key
    if key := os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY"):
        config["gemini"]["api_key"] = key
    if timeout_str := os.environ.get("BUYERBENCH_TIMEOUT"):
        try:
            config["timeout"] = int(timeout_str)
        except ValueError:
            pass
    if dry_run_str := os.environ.get("BUYERBENCH_DRY_RUN"):
        config["dry_run"] = dry_run_str.lower() in ("1", "true", "yes")

    return config
