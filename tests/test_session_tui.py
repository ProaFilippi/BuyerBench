"""Tests for SessionConfig dataclasses and YAML round-trip persistence.

Covers: AgentSlot, SessionConfig, save_session_config, load_session_config.
"""
from __future__ import annotations

import os
import tempfile

import pytest

from buyerbench.selector import (
    AgentSlot,
    SessionConfig,
    load_session_config,
    save_session_config,
)


def _make_config() -> SessionConfig:
    return SessionConfig(
        agents=[
            AgentSlot(agent_id="openrouter-openai-gpt-4o", skill_mode="baseline"),
            AgentSlot(agent_id="openrouter-anthropic-claude-3.5-sonnet", skill_mode="skills"),
        ],
        scenario_ids=[
            "p1-01-supplier-discovery",
            "p2-01-anchoring-bias",
            "p3-01-secure-transaction",
        ],
        created_at="2026-04-08T12:00:00+00:00",
    )


class TestAgentSlot:
    def test_fields(self):
        slot = AgentSlot(agent_id="mock-agent-v1", skill_mode="mcp")
        assert slot.agent_id == "mock-agent-v1"
        assert slot.skill_mode == "mcp"


class TestSessionConfig:
    def test_fields(self):
        cfg = _make_config()
        assert len(cfg.agents) == 2
        assert len(cfg.scenario_ids) == 3
        assert cfg.created_at == "2026-04-08T12:00:00+00:00"

    def test_agent_slots_preserved(self):
        cfg = _make_config()
        assert cfg.agents[0].agent_id == "openrouter-openai-gpt-4o"
        assert cfg.agents[0].skill_mode == "baseline"
        assert cfg.agents[1].skill_mode == "skills"


class TestRoundTrip:
    def test_save_then_load(self, tmp_path):
        original = _make_config()
        path = str(tmp_path / "test-session.yaml")

        save_session_config(original, path)
        loaded = load_session_config(path)

        assert len(loaded.agents) == len(original.agents)
        assert len(loaded.scenario_ids) == len(original.scenario_ids)
        assert loaded.created_at == original.created_at

        for orig_slot, loaded_slot in zip(original.agents, loaded.agents):
            assert loaded_slot.agent_id == orig_slot.agent_id
            assert loaded_slot.skill_mode == orig_slot.skill_mode

        assert loaded.scenario_ids == original.scenario_ids

    def test_yaml_structure(self, tmp_path):
        """Confirm the serialized YAML has the expected human-readable structure."""
        import yaml

        cfg = _make_config()
        path = str(tmp_path / "structure-test.yaml")
        save_session_config(cfg, path)

        with open(path) as fh:
            data = yaml.safe_load(fh)

        assert "agents" in data
        assert "scenario_ids" in data
        assert "created_at" in data
        assert data["agents"][0]["agent_id"] == "openrouter-openai-gpt-4o"
        assert data["agents"][0]["skill_mode"] == "baseline"
        assert data["agents"][1]["skill_mode"] == "skills"

    def test_empty_agents(self, tmp_path):
        cfg = SessionConfig(agents=[], scenario_ids=["p1-01"], created_at="2026-01-01T00:00:00")
        path = str(tmp_path / "empty-agents.yaml")
        save_session_config(cfg, path)
        loaded = load_session_config(path)
        assert loaded.agents == []
        assert loaded.scenario_ids == ["p1-01"]

    def test_empty_scenarios(self, tmp_path):
        cfg = SessionConfig(
            agents=[AgentSlot(agent_id="mock-agent-v1", skill_mode="baseline")],
            scenario_ids=[],
            created_at="2026-01-01T00:00:00",
        )
        path = str(tmp_path / "empty-scenarios.yaml")
        save_session_config(cfg, path)
        loaded = load_session_config(path)
        assert loaded.scenario_ids == []
        assert loaded.agents[0].agent_id == "mock-agent-v1"

    def test_default_path_uses_session_config_yaml(self, tmp_path, monkeypatch):
        """save_session_config default filename is session-config.yaml."""
        monkeypatch.chdir(tmp_path)
        cfg = _make_config()
        save_session_config(cfg)  # uses default path
        loaded = load_session_config()  # uses default path
        assert len(loaded.agents) == 2
        assert len(loaded.scenario_ids) == 3
