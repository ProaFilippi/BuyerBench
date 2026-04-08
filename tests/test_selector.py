"""Tests for buyerbench.model_catalog and buyerbench.selector."""
from __future__ import annotations

import yaml
from pathlib import Path

import pytest
from click.testing import CliRunner

from buyerbench.model_catalog import MODEL_CATALOG, filter_catalog
from buyerbench.selector import load_selection, save_selection


# ---------------------------------------------------------------------------
# model_catalog tests
# ---------------------------------------------------------------------------


def test_model_catalog_complete():
    """Catalog must contain exactly 10 entries, all with required non-empty fields."""
    assert len(MODEL_CATALOG) == 10
    for entry in MODEL_CATALOG:
        assert entry.agent_id, f"Empty agent_id for {entry}"
        assert entry.provider, f"Empty provider for {entry}"
        assert entry.description, f"Empty description for {entry}"


def test_filter_by_tag():
    """filter_catalog(tags=['open-source']) should return only open-source models."""
    results = filter_catalog(tags=["open-source"])
    assert len(results) > 0
    for entry in results:
        assert "open-source" in entry.capability_tags, (
            f"{entry.display_name} lacks 'open-source' tag"
        )
    # Models WITHOUT the tag must not appear
    non_open = [e for e in MODEL_CATALOG if "open-source" not in e.capability_tags]
    result_ids = {e.agent_id for e in results}
    for entry in non_open:
        assert entry.agent_id not in result_ids, (
            f"{entry.display_name} should not appear in open-source filter"
        )


def test_filter_by_provider():
    """filter_catalog(providers=['Mistral']) should return exactly Mistral Large and Mixtral 8x22B."""
    results = filter_catalog(providers=["Mistral"])
    assert len(results) == 2
    result_ids = {e.agent_id for e in results}
    assert "openrouter-mistralai-mistral-large" in result_ids
    assert "openrouter-mistralai-mixtral-8x22b-instruct" in result_ids


def test_filter_by_cost_tier():
    """filter_catalog(cost_tiers=['high']) should only return high-cost entries."""
    results = filter_catalog(cost_tiers=["high"])
    assert len(results) > 0
    for entry in results:
        assert entry.cost_tier == "high"


def test_filter_multiple_criteria():
    """Combining providers + tags acts as AND (intersection)."""
    results = filter_catalog(providers=["Mistral"], tags=["moe"])
    assert len(results) == 1
    assert results[0].agent_id == "openrouter-mistralai-mixtral-8x22b-instruct"


def test_filter_empty_result():
    """filter_catalog with contradictory criteria should return an empty list."""
    results = filter_catalog(providers=["OpenAI"], tags=["open-source"])
    assert results == []


def test_filter_no_criteria():
    """filter_catalog with no args should return all 10 entries."""
    assert filter_catalog() == MODEL_CATALOG


# ---------------------------------------------------------------------------
# save / load roundtrip tests
# ---------------------------------------------------------------------------


def test_save_load_roundtrip(tmp_path: Path):
    """Saving 3 agent IDs and loading them back must produce an equal list."""
    selection_file = tmp_path / "sel.yaml"
    ids = [
        "openrouter-openai-gpt-4o",
        "openrouter-deepseek-deepseek-chat",
        "openrouter-cohere-command-r-plus",
    ]
    save_selection(ids, str(selection_file))

    assert selection_file.exists()
    loaded = load_selection(str(selection_file))
    assert loaded == ids


def test_save_selection_yaml_structure(tmp_path: Path):
    """Saved YAML must include 'selected_agents' and 'created_at' keys."""
    path = tmp_path / "sel.yaml"
    save_selection(["openrouter-openai-gpt-4o"], str(path))
    raw = yaml.safe_load(path.read_text())
    assert "selected_agents" in raw
    assert "created_at" in raw
    assert raw["selected_agents"] == ["openrouter-openai-gpt-4o"]


# ---------------------------------------------------------------------------
# CLI command tests
# ---------------------------------------------------------------------------


def test_select_command_exists():
    """'buyerbench select --help' should exit 0 and advertise expected options."""
    from buyerbench.__main__ import cli

    runner = CliRunner()
    result = runner.invoke(cli, ["select", "--help"])
    assert result.exit_code == 0, result.output
    assert "--output" in result.output
    assert "--filter-tag" in result.output


def test_run_from_selection(tmp_path: Path):
    """'buyerbench run --from-selection <file> --dry-run' should run without error."""
    from buyerbench.__main__ import cli

    selection_file = tmp_path / "sel.yaml"
    # Use two OpenRouter agent IDs that are always registered
    ids = [
        "openrouter-openai-gpt-4o",
        "openrouter-deepseek-deepseek-chat",
    ]
    save_selection(ids, str(selection_file))

    runner = CliRunner()
    result = runner.invoke(
        cli,
        ["run", "--from-selection", str(selection_file), "--dry-run"],
    )
    assert result.exit_code == 0, result.output


def test_run_agent_and_from_selection_mutually_exclusive(tmp_path: Path):
    """Providing both --agent and --from-selection must exit with code 1."""
    from buyerbench.__main__ import cli

    selection_file = tmp_path / "sel.yaml"
    save_selection(["openrouter-openai-gpt-4o"], str(selection_file))

    runner = CliRunner()
    result = runner.invoke(
        cli,
        ["run", "--agent", "mock-agent-v1", "--from-selection", str(selection_file), "--dry-run"],
    )
    assert result.exit_code == 1


def test_run_requires_agent_or_from_selection():
    """'buyerbench run' with neither --agent nor --from-selection must exit 1."""
    from buyerbench.__main__ import cli

    runner = CliRunner()
    result = runner.invoke(cli, ["run", "--dry-run"])
    assert result.exit_code == 1


def test_select_non_tty_exits_1():
    """'buyerbench select' in a non-TTY context must exit with code 1."""
    from buyerbench.__main__ import cli

    runner = CliRunner()
    # CliRunner uses a non-TTY stdin by default
    result = runner.invoke(cli, ["select"])
    assert result.exit_code == 1
    assert "TTY" in result.output or "interactive" in result.output
