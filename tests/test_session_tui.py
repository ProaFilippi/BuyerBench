"""Tests for SessionConfig dataclasses, YAML round-trip persistence,
interactive_skill_select logic, and interactive_scenario_select logic.
"""
from __future__ import annotations

import os
import tempfile
from dataclasses import dataclass, field
from enum import Enum

import pytest

from buyerbench.selector import (
    AgentSlot,
    SessionConfig,
    interactive_scenario_select,
    interactive_skill_select,
    load_session_config,
    run_session_tui,
    save_session_config,
)


# ── Minimal stub types used by interactive_scenario_select tests ────────────

class _Pillar(str, Enum):
    PILLAR1 = "PILLAR1"
    PILLAR2 = "PILLAR2"
    PILLAR3 = "PILLAR3"


class _Difficulty(str, Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"


@dataclass
class _Scenario:
    id: str
    title: str
    pillar: _Pillar
    difficulty: _Difficulty
    tags: list = field(default_factory=list)


def _make_scenarios():
    return [
        _Scenario("p1-01", "Supplier Discovery", _Pillar.PILLAR1, _Difficulty.easy),
        _Scenario("p1-02", "Quote Comparison", _Pillar.PILLAR1, _Difficulty.medium),
        _Scenario("p2-01", "Anchoring Bias", _Pillar.PILLAR2, _Difficulty.medium),
        _Scenario("p2-02", "Framing Effect", _Pillar.PILLAR2, _Difficulty.hard),
        _Scenario("p3-01", "Secure Transaction", _Pillar.PILLAR3, _Difficulty.easy),
    ]


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


class TestInteractiveSkillSelect:
    """Unit-tests for interactive_skill_select using simulated input sequences."""

    _AGENTS = [
        "openrouter-openai-gpt-4o",
        "openrouter-anthropic-claude-3.5-sonnet",
        "openrouter-google-gemini-pro-1.5",
    ]

    def _run(self, agent_ids, inputs, monkeypatch):
        """Monkey-patch Prompt.ask and run interactive_skill_select."""
        from rich.prompt import Prompt

        responses = iter(inputs)
        monkeypatch.setattr(Prompt, "ask", staticmethod(lambda _prompt: next(responses)))
        return interactive_skill_select(agent_ids)

    def test_defaults_to_baseline(self, monkeypatch):
        result = self._run(self._AGENTS, ["done"], monkeypatch)
        assert all(v == "baseline" for v in result.values())
        assert set(result.keys()) == set(self._AGENTS)

    def test_set_single_agent_to_skills(self, monkeypatch):
        result = self._run(self._AGENTS, ["1 s", "done"], monkeypatch)
        assert result[self._AGENTS[0]] == "skills"
        assert result[self._AGENTS[1]] == "baseline"

    def test_set_single_agent_to_mcp(self, monkeypatch):
        result = self._run(self._AGENTS, ["2 m", "done"], monkeypatch)
        assert result[self._AGENTS[1]] == "mcp"
        assert result[self._AGENTS[0]] == "baseline"

    def test_batch_set_all_to_skills(self, monkeypatch):
        result = self._run(self._AGENTS, ["a s", "done"], monkeypatch)
        assert all(v == "skills" for v in result.values())

    def test_batch_set_all_then_override_one(self, monkeypatch):
        result = self._run(self._AGENTS, ["a m", "1 b", "done"], monkeypatch)
        assert result[self._AGENTS[0]] == "baseline"
        assert result[self._AGENTS[1]] == "mcp"
        assert result[self._AGENTS[2]] == "mcp"

    def test_unknown_command_does_not_crash(self, monkeypatch):
        """Unknown input is silently ignored and loop continues."""
        result = self._run(self._AGENTS, ["garbage", "done"], monkeypatch)
        assert all(v == "baseline" for v in result.values())

    def test_out_of_range_index_does_not_crash(self, monkeypatch):
        result = self._run(self._AGENTS, ["99 s", "done"], monkeypatch)
        assert all(v == "baseline" for v in result.values())

    def test_unknown_mode_abbrev_does_not_crash(self, monkeypatch):
        result = self._run(self._AGENTS, ["1 x", "done"], monkeypatch)
        assert result[self._AGENTS[0]] == "baseline"

    def test_quit_raises_system_exit(self, monkeypatch):
        from rich.prompt import Prompt

        responses = iter(["q"])
        monkeypatch.setattr(Prompt, "ask", staticmethod(lambda _prompt: next(responses)))
        with pytest.raises(SystemExit):
            interactive_skill_select(self._AGENTS)

    def test_single_agent(self, monkeypatch):
        result = self._run(["mock-agent-v1"], ["1 m", "done"], monkeypatch)
        assert result == {"mock-agent-v1": "mcp"}

    def test_empty_input_skipped(self, monkeypatch):
        """Empty input string is ignored and loop continues."""
        result = self._run(self._AGENTS, ["", "done"], monkeypatch)
        assert all(v == "baseline" for v in result.values())


class TestInteractiveScenarioSelect:
    """Unit-tests for interactive_scenario_select using simulated input sequences."""

    def _run(self, scenarios, inputs, monkeypatch):
        """Monkey-patch Prompt.ask and run interactive_scenario_select."""
        from rich.prompt import Prompt

        responses = iter(inputs)
        monkeypatch.setattr(Prompt, "ask", staticmethod(lambda _prompt: next(responses)))
        return interactive_scenario_select(scenarios)

    def test_done_with_no_selection_returns_empty(self, monkeypatch):
        result = self._run(_make_scenarios(), ["done"], monkeypatch)
        assert result == []

    def test_toggle_single_item(self, monkeypatch):
        result = self._run(_make_scenarios(), ["1", "done"], monkeypatch)
        assert result == ["p1-01"]

    def test_toggle_multiple_comma_separated(self, monkeypatch):
        result = self._run(_make_scenarios(), ["1,3,5", "done"], monkeypatch)
        assert result == ["p1-01", "p2-01", "p3-01"]

    def test_toggle_multiple_space_separated(self, monkeypatch):
        result = self._run(_make_scenarios(), ["2 4", "done"], monkeypatch)
        assert result == ["p1-02", "p2-02"]

    def test_toggle_deselects_on_second_press(self, monkeypatch):
        """Toggling the same index twice removes the scenario."""
        result = self._run(_make_scenarios(), ["1", "1", "done"], monkeypatch)
        assert result == []

    def test_select_all(self, monkeypatch):
        scenarios = _make_scenarios()
        result = self._run(scenarios, ["a", "done"], monkeypatch)
        assert result == [s.id for s in scenarios]

    def test_clear_all(self, monkeypatch):
        result = self._run(_make_scenarios(), ["a", "c", "done"], monkeypatch)
        assert result == []

    def test_pillar_filter_p1(self, monkeypatch):
        result = self._run(_make_scenarios(), ["p1", "done"], monkeypatch)
        assert result == ["p1-01", "p1-02"]

    def test_pillar_filter_p2(self, monkeypatch):
        result = self._run(_make_scenarios(), ["p2", "done"], monkeypatch)
        assert result == ["p2-01", "p2-02"]

    def test_pillar_filter_p3(self, monkeypatch):
        result = self._run(_make_scenarios(), ["p3", "done"], monkeypatch)
        assert result == ["p3-01"]

    def test_pillar_filters_are_additive(self, monkeypatch):
        result = self._run(_make_scenarios(), ["p1", "p3", "done"], monkeypatch)
        assert result == ["p1-01", "p1-02", "p3-01"]

    def test_unknown_command_ignored(self, monkeypatch):
        result = self._run(_make_scenarios(), ["garbage", "done"], monkeypatch)
        assert result == []

    def test_empty_input_skipped(self, monkeypatch):
        result = self._run(_make_scenarios(), ["", "1", "done"], monkeypatch)
        assert result == ["p1-01"]

    def test_out_of_range_index_ignored(self, monkeypatch):
        result = self._run(_make_scenarios(), ["99", "done"], monkeypatch)
        assert result == []

    def test_quit_raises_system_exit(self, monkeypatch):
        from rich.prompt import Prompt

        responses = iter(["q"])
        monkeypatch.setattr(Prompt, "ask", staticmethod(lambda _prompt: next(responses)))
        with pytest.raises(SystemExit):
            interactive_scenario_select(_make_scenarios())

    def test_result_order_matches_input_order(self, monkeypatch):
        """Selected IDs are returned in the same order as the input scenarios list."""
        result = self._run(_make_scenarios(), ["3", "1", "5", "done"], monkeypatch)
        assert result == ["p1-01", "p2-01", "p3-01"]


class TestRunSessionTui:
    """Unit-tests for run_session_tui using mocked sub-steps."""

    _AGENTS = [
        "openrouter-openai-gpt-4o",
        "openrouter-anthropic-claude-3.5-sonnet",
    ]
    _SCENARIOS = _make_scenarios()  # 5 scenarios across all 3 pillars

    def _run_tui(
        self,
        monkeypatch,
        selected_agents=None,
        skill_modes=None,
        scenario_ids=None,
    ) -> SessionConfig:
        """Patch sub-steps and run run_session_tui()."""
        import buyerbench.selector as sel_mod
        import harness.loader as loader_mod

        if selected_agents is None:
            selected_agents = self._AGENTS
        if skill_modes is None:
            skill_modes = {a: "baseline" for a in selected_agents}
        if scenario_ids is None:
            scenario_ids = [s.id for s in self._SCENARIOS]

        monkeypatch.setattr(sel_mod, "interactive_select", lambda *a, **kw: selected_agents)
        monkeypatch.setattr(sel_mod, "interactive_skill_select", lambda *a, **kw: skill_modes)
        monkeypatch.setattr(sel_mod, "interactive_scenario_select", lambda *a, **kw: scenario_ids)
        monkeypatch.setattr(loader_mod, "load_all_scenarios", lambda *a, **kw: self._SCENARIOS)

        return run_session_tui()

    def test_returns_session_config(self, monkeypatch):
        result = self._run_tui(monkeypatch)
        assert isinstance(result, SessionConfig)

    def test_agents_populated(self, monkeypatch):
        result = self._run_tui(monkeypatch)
        assert len(result.agents) == len(self._AGENTS)
        assert result.agents[0].agent_id == self._AGENTS[0]

    def test_skill_modes_applied(self, monkeypatch):
        skill_modes = {self._AGENTS[0]: "skills", self._AGENTS[1]: "mcp"}
        result = self._run_tui(monkeypatch, skill_modes=skill_modes)
        assert result.agents[0].skill_mode == "skills"
        assert result.agents[1].skill_mode == "mcp"

    def test_scenario_ids_populated(self, monkeypatch):
        result = self._run_tui(monkeypatch)
        assert len(result.scenario_ids) == len(self._SCENARIOS)
        assert result.scenario_ids == [s.id for s in self._SCENARIOS]

    def test_created_at_is_iso8601(self, monkeypatch):
        result = self._run_tui(monkeypatch)
        assert result.created_at
        assert "T" in result.created_at  # ISO 8601 separator

    def test_round_trip_after_tui(self, monkeypatch, tmp_path):
        """Output of run_session_tui can be saved and reloaded without loss."""
        result = self._run_tui(monkeypatch)
        path = str(tmp_path / "tui-session.yaml")
        save_session_config(result, path)
        loaded = load_session_config(path)
        assert len(loaded.agents) == len(result.agents)
        assert loaded.scenario_ids == result.scenario_ids
        assert loaded.created_at == result.created_at

    def test_partial_scenario_selection(self, monkeypatch):
        """Only selected scenarios appear in the config."""
        scenario_ids = ["p1-01", "p3-01"]
        result = self._run_tui(monkeypatch, scenario_ids=scenario_ids)
        assert result.scenario_ids == ["p1-01", "p3-01"]

    def test_single_agent(self, monkeypatch):
        single = [self._AGENTS[0]]
        skill_modes = {self._AGENTS[0]: "mcp"}
        result = self._run_tui(monkeypatch, selected_agents=single, skill_modes=skill_modes)
        assert len(result.agents) == 1
        assert result.agents[0].skill_mode == "mcp"
