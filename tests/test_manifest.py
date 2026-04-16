"""Tests for research.experiments.manifest.

Covers:
- get_git_commit_hash: subprocess success + fallback
- _agent_id_to_openrouter_slug: known provider mapping including hyphenated providers
- query_openrouter_model_versions: no API key fallback, HTTP success, HTTP failure
- create_manifest: field population, total_planned_runs arithmetic, model pinning toggle
- freeze_manifest: directory creation, manifest.json content, FileExistsError guard
- load_manifest: round-trip
"""
from __future__ import annotations

import json
from io import BytesIO
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from research.experiments.manifest import (
    _agent_id_to_openrouter_slug,
    create_manifest,
    freeze_manifest,
    get_git_commit_hash,
    load_manifest,
    query_openrouter_model_versions,
)
from research.experiments.schemas import ExperimentManifest


# ── Fixtures ──────────────────────────────────────────────────────────────────


MINIMAL_DESIGN = {
    "design_tier": "realistic",
    "models": [
        "openrouter-openai-gpt-4o",
        "openrouter-anthropic-claude-3.5-sonnet",
    ],
    "bias_scenarios": {
        "anchoring": {
            "baseline": "p2-01-anchoring-BASELINE",
            "treatment": "p2-01-anchoring-ANCHOR_HIGH",
        },
        "framing": {
            "baseline": "p2-02-framing-FRAMING_GAIN",
            "treatment": "p2-02-framing-FRAMING_LOSS",
        },
    },
    "n_runs_per_cell": 3,
    "temperatures": [0.7],
    "prompt_versions": ["standard"],
}

_OPENROUTER_API_RESPONSE = {
    "data": [
        {"id": "openai/gpt-4o-2024-11-20", "name": "GPT-4o"},
        {"id": "anthropic/claude-3.5-sonnet-20241022", "name": "Claude 3.5 Sonnet"},
    ]
}


def _make_urlopen_mock(payload: dict):
    """Return a mock context manager that yields a file-like object with JSON."""
    raw = json.dumps(payload).encode()
    cm = MagicMock()
    cm.__enter__ = MagicMock(return_value=BytesIO(raw))
    cm.__exit__ = MagicMock(return_value=False)
    return cm


# ── get_git_commit_hash ───────────────────────────────────────────────────────


class TestGetGitCommitHash:
    def test_returns_string(self):
        result = get_git_commit_hash()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_fallback_on_failure(self):
        with patch("subprocess.check_output", side_effect=FileNotFoundError):
            result = get_git_commit_hash()
        assert result == "unknown"

    def test_strips_whitespace(self):
        with patch(
            "subprocess.check_output",
            return_value=b"abc123def456\n",
        ):
            result = get_git_commit_hash()
        assert result == "abc123def456"


# ── _agent_id_to_openrouter_slug ──────────────────────────────────────────────


class TestAgentIdToSlug:
    @pytest.mark.parametrize(
        "agent_id, expected_slug",
        [
            ("openrouter-openai-gpt-4o", "openai/gpt-4o"),
            ("openrouter-anthropic-claude-3.5-sonnet", "anthropic/claude-3.5-sonnet"),
            ("openrouter-google-gemini-pro-1.5", "google/gemini-pro-1.5"),
            ("openrouter-meta-llama-llama-3.1-405b-instruct", "meta-llama/llama-3.1-405b-instruct"),
            ("openrouter-mistralai-mistral-large", "mistralai/mistral-large"),
            ("openrouter-deepseek-deepseek-chat", "deepseek/deepseek-chat"),
            ("openrouter-qwen-qwen-2.5-72b-instruct", "qwen/qwen-2.5-72b-instruct"),
            ("openrouter-cohere-command-r-plus", "cohere/command-r-plus"),
            ("openrouter-01-ai-yi-large", "01-ai/yi-large"),
        ],
    )
    def test_known_providers(self, agent_id, expected_slug):
        assert _agent_id_to_openrouter_slug(agent_id) == expected_slug

    def test_unknown_provider_falls_back_to_first_hyphen(self):
        slug = _agent_id_to_openrouter_slug("openrouter-newco-model-v2")
        assert "/" in slug

    def test_meta_llama_not_split_at_first_hyphen(self):
        # meta-llama has a hyphen in the provider name — must not split there
        slug = _agent_id_to_openrouter_slug("openrouter-meta-llama-llama-3.1-405b-instruct")
        assert slug.startswith("meta-llama/")


# ── query_openrouter_model_versions ──────────────────────────────────────────


class TestQueryOpenrouterModelVersions:
    def test_empty_when_no_openrouter_agents(self):
        result = query_openrouter_model_versions(["mock-agent-v1", "negmas"])
        assert result == {}

    def test_version_unknown_when_no_api_key(self, monkeypatch):
        monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
        result = query_openrouter_model_versions(
            ["openrouter-openai-gpt-4o"],
            api_key=None,
        )
        assert result == {"openrouter-openai-gpt-4o": "version-unknown"}

    def test_version_unknown_on_http_error(self, monkeypatch):
        monkeypatch.setenv("OPENROUTER_API_KEY", "fake-key")
        from urllib.error import URLError

        with patch(
            "research.experiments.manifest.urlopen",
            side_effect=URLError("connection refused"),
        ):
            result = query_openrouter_model_versions(["openrouter-openai-gpt-4o"])
        assert result == {"openrouter-openai-gpt-4o": "version-unknown"}

    def test_happy_path_returns_pinned_ids(self, monkeypatch):
        monkeypatch.setenv("OPENROUTER_API_KEY", "fake-key")
        with patch(
            "research.experiments.manifest.urlopen",
            return_value=_make_urlopen_mock(_OPENROUTER_API_RESPONSE),
        ):
            result = query_openrouter_model_versions(
                [
                    "openrouter-openai-gpt-4o",
                    "openrouter-anthropic-claude-3.5-sonnet",
                ]
            )
        assert result["openrouter-openai-gpt-4o"] == "openai/gpt-4o-2024-11-20"
        assert result["openrouter-anthropic-claude-3.5-sonnet"] == "anthropic/claude-3.5-sonnet-20241022"

    def test_unknown_model_gets_pinned_unknown_suffix(self, monkeypatch):
        monkeypatch.setenv("OPENROUTER_API_KEY", "fake-key")
        with patch(
            "research.experiments.manifest.urlopen",
            return_value=_make_urlopen_mock({"data": []}),
        ):
            result = query_openrouter_model_versions(["openrouter-openai-gpt-4o"])
        assert "openrouter-openai-gpt-4o" in result
        assert "unknown" in result["openrouter-openai-gpt-4o"]

    def test_non_openrouter_agents_skipped(self, monkeypatch):
        monkeypatch.setenv("OPENROUTER_API_KEY", "fake-key")
        with patch(
            "research.experiments.manifest.urlopen",
            return_value=_make_urlopen_mock(_OPENROUTER_API_RESPONSE),
        ):
            result = query_openrouter_model_versions(
                ["openrouter-openai-gpt-4o", "mock-agent-v1"]
            )
        assert "mock-agent-v1" not in result
        assert "openrouter-openai-gpt-4o" in result


# ── create_manifest ───────────────────────────────────────────────────────────


class TestCreateManifest:
    def _create(self, design=None, **kwargs) -> ExperimentManifest:
        return create_manifest(
            design or MINIMAL_DESIGN,
            pin_model_versions=False,
            **kwargs,
        )

    def test_returns_experiment_manifest(self):
        m = self._create()
        assert isinstance(m, ExperimentManifest)

    def test_experiment_id_contains_design_tier(self):
        m = self._create()
        assert "realistic" in m.experiment_id

    def test_experiment_id_contains_timestamp(self):
        m = self._create()
        # Format: pillar2-realistic-YYYYMMDD-HHMMSS
        parts = m.experiment_id.split("-")
        assert len(parts) >= 4

    def test_n_models_correct(self):
        m = self._create()
        assert m.n_models == 2

    def test_n_bias_types_correct(self):
        m = self._create()
        assert m.n_bias_types == 2

    def test_n_variants_per_bias_correct(self):
        m = self._create()
        assert m.n_variants_per_bias == 2

    def test_total_planned_runs_arithmetic(self):
        # 2 models × 2 biases × 2 variants × 1 temp × 1 prompt × 3 runs = 24
        m = self._create()
        assert m.total_planned_runs == 24

    def test_total_completed_runs_is_zero(self):
        m = self._create()
        assert m.total_completed_runs == 0

    def test_git_commit_hash_captured(self):
        m = self._create()
        assert isinstance(m.git_commit_hash, str)
        assert len(m.git_commit_hash) > 0

    def test_created_at_utc_is_set(self):
        m = self._create()
        assert m.created_at_utc is not None

    def test_start_end_times_are_none(self):
        m = self._create()
        assert m.start_time_utc is None
        assert m.end_time_utc is None

    def test_models_preserved(self):
        m = self._create()
        assert m.models == MINIMAL_DESIGN["models"]

    def test_bias_scenarios_preserved(self):
        m = self._create()
        assert m.bias_scenarios == MINIMAL_DESIGN["bias_scenarios"]

    def test_no_pinning_when_disabled(self, monkeypatch):
        monkeypatch.setenv("OPENROUTER_API_KEY", "fake-key")
        m = create_manifest(MINIMAL_DESIGN, pin_model_versions=False)
        assert m.pinned_model_versions == {}

    def test_pinning_called_when_enabled(self, monkeypatch):
        monkeypatch.setenv("OPENROUTER_API_KEY", "fake-key")
        with patch(
            "research.experiments.manifest.urlopen",
            return_value=_make_urlopen_mock(_OPENROUTER_API_RESPONSE),
        ):
            m = create_manifest(MINIMAL_DESIGN, pin_model_versions=True)
        assert "openrouter-openai-gpt-4o" in m.pinned_model_versions
        assert m.pinned_model_versions["openrouter-openai-gpt-4o"] != ""

    def test_total_planned_runs_multi_temp(self):
        design = {**MINIMAL_DESIGN, "temperatures": [0.0, 0.7], "n_runs_per_cell": 1}
        m = create_manifest(design, pin_model_versions=False)
        # 2 models × 2 biases × 2 variants × 2 temps × 1 prompt × 1 run = 16
        assert m.total_planned_runs == 16

    def test_total_planned_runs_multi_prompt(self):
        design = {**MINIMAL_DESIGN, "prompt_versions": ["standard", "cot"], "n_runs_per_cell": 1}
        m = create_manifest(design, pin_model_versions=False)
        # 2 × 2 × 2 × 1 × 2 × 1 = 16
        assert m.total_planned_runs == 16


# ── freeze_manifest ───────────────────────────────────────────────────────────


class TestFreezeManifest:
    def _manifest(self) -> ExperimentManifest:
        return create_manifest(MINIMAL_DESIGN, pin_model_versions=False)

    def test_creates_manifest_json(self, tmp_path):
        m = self._manifest()
        path = freeze_manifest(m, tmp_path)
        assert path.exists()
        assert path.name == "manifest.json"

    def test_manifest_json_is_valid(self, tmp_path):
        m = self._manifest()
        path = freeze_manifest(m, tmp_path)
        data = json.loads(path.read_text())
        assert data["experiment_id"] == m.experiment_id

    def test_experiment_subdir_created(self, tmp_path):
        m = self._manifest()
        freeze_manifest(m, tmp_path)
        exp_dir = tmp_path / m.experiment_id
        assert exp_dir.is_dir()

    def test_subdirectories_created(self, tmp_path):
        m = self._manifest()
        freeze_manifest(m, tmp_path)
        exp_dir = tmp_path / m.experiment_id
        for sub in ("raw", "figures", "tables"):
            assert (exp_dir / sub).is_dir(), f"Missing subdirectory: {sub}"

    def test_raises_if_manifest_already_exists(self, tmp_path):
        m = self._manifest()
        freeze_manifest(m, tmp_path)
        with pytest.raises(FileExistsError, match="already exists"):
            freeze_manifest(m, tmp_path)

    def test_git_hash_in_json(self, tmp_path):
        m = self._manifest()
        path = freeze_manifest(m, tmp_path)
        data = json.loads(path.read_text())
        assert "git_commit_hash" in data
        assert data["git_commit_hash"] == m.git_commit_hash

    def test_pinned_model_versions_in_json(self, tmp_path, monkeypatch):
        monkeypatch.setenv("OPENROUTER_API_KEY", "fake-key")
        with patch(
            "research.experiments.manifest.urlopen",
            return_value=_make_urlopen_mock(_OPENROUTER_API_RESPONSE),
        ):
            m = create_manifest(MINIMAL_DESIGN, pin_model_versions=True)
        path = freeze_manifest(m, tmp_path)
        data = json.loads(path.read_text())
        assert "pinned_model_versions" in data
        assert data["pinned_model_versions"]["openrouter-openai-gpt-4o"] == "openai/gpt-4o-2024-11-20"

    def test_returns_path_to_manifest(self, tmp_path):
        m = self._manifest()
        path = freeze_manifest(m, tmp_path)
        assert isinstance(path, Path)
        assert path.suffix == ".json"


# ── load_manifest ─────────────────────────────────────────────────────────────


class TestLoadManifest:
    def test_round_trip(self, tmp_path):
        m = create_manifest(MINIMAL_DESIGN, pin_model_versions=False)
        path = freeze_manifest(m, tmp_path)
        loaded = load_manifest(path)
        assert loaded["experiment_id"] == m.experiment_id
        assert loaded["n_models"] == m.n_models
        assert loaded["models"] == m.models

    def test_loaded_dict_contains_all_fields(self, tmp_path):
        m = create_manifest(MINIMAL_DESIGN, pin_model_versions=False)
        path = freeze_manifest(m, tmp_path)
        loaded = load_manifest(path)
        for field_name in (
            "experiment_id",
            "design_tier",
            "n_models",
            "git_commit_hash",
            "temperatures",
            "prompt_versions",
            "total_planned_runs",
            "pinned_model_versions",
        ):
            assert field_name in loaded, f"Missing field: {field_name}"
