"""Tests for buyerbench.session_browser — browse_sessions() and helper utilities."""
from __future__ import annotations

import subprocess
from pathlib import Path

import pytest
import yaml

from buyerbench.selector import AgentSlot, SessionConfig, save_session_config
from buyerbench.session_browser import (
    _find_session_configs,
    _format_created_at,
    _has_results,
    browse_sessions,
)


# ── Fixtures ──────────────────────────────────────────────────────────────────


def _make_config(
    experiment_name: str = "test-exp",
    agents: int = 2,
    scenario_ids: list[str] | None = None,
    recurrence: str | None = None,
    output_dir: str = "results",
) -> SessionConfig:
    return SessionConfig(
        agents=[
            AgentSlot(agent_id=f"openrouter-openai-gpt-4o-{i}", skill_mode="baseline")
            for i in range(agents)
        ],
        scenario_ids=scenario_ids or ["p1-01", "p2-01"],
        created_at="2026-04-09T10:30:00+00:00",
        experiment_name=experiment_name,
        recurrence=recurrence,
        output_dir=output_dir,
    )


def _write_session(tmp_path: Path, subdir: str, config: SessionConfig) -> Path:
    session_dir = tmp_path / "sessions" / subdir
    session_dir.mkdir(parents=True, exist_ok=True)
    config_path = session_dir / "session-config.yaml"
    save_session_config(config, str(config_path))
    return config_path


# ── _format_created_at ────────────────────────────────────────────────────────


class TestFormatCreatedAt:
    def test_iso_timestamp(self):
        assert _format_created_at("2026-04-09T10:30:00+00:00") == "2026-04-09"

    def test_empty_string(self):
        assert _format_created_at("") == "—"

    def test_date_only(self):
        assert _format_created_at("2026-04-09") == "2026-04-09"


# ── _find_session_configs ─────────────────────────────────────────────────────


class TestFindSessionConfigs:
    def test_finds_configs_in_sessions_dir(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        config = _make_config()
        _write_session(tmp_path, "exp-1/", config)
        _write_session(tmp_path, "exp-2/", config)

        found = _find_session_configs()
        assert len(found) == 2

    def test_returns_empty_when_no_sessions(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        assert _find_session_configs() == []

    def test_falls_back_to_results(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        # No sessions/ dir; put config in results/
        results_dir = tmp_path / "results" / "legacy-exp"
        results_dir.mkdir(parents=True)
        config_path = results_dir / "session-config.yaml"
        save_session_config(_make_config(), str(config_path))

        found = _find_session_configs()
        assert len(found) == 1
        assert found[0].name == "session-config.yaml"

    def test_sessions_takes_priority_over_results(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        # Both exist — sessions/ wins
        _write_session(tmp_path, "session-exp/", _make_config())
        results_dir = tmp_path / "results" / "legacy-exp"
        results_dir.mkdir(parents=True)
        save_session_config(_make_config(), str(results_dir / "session-config.yaml"))

        found = _find_session_configs()
        assert all("sessions" in str(p) for p in found)


# ── _has_results ──────────────────────────────────────────────────────────────


class TestHasResults:
    def test_returns_true_when_results_dir_exists(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        config = _make_config(experiment_name="my-exp", output_dir="results")
        # Create matching results subdirectory
        (tmp_path / "results" / "my-exp-run1").mkdir(parents=True)
        assert _has_results(config) is True

    def test_returns_false_when_no_results_dir(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        config = _make_config(experiment_name="no-results-exp")
        assert _has_results(config) is False

    def test_returns_false_with_empty_experiment_name(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        config = _make_config(experiment_name="")
        (tmp_path / "results").mkdir()
        assert _has_results(config) is False


# ── browse_sessions ───────────────────────────────────────────────────────────


class TestBrowseSessions:
    """Integration-style tests for browse_sessions() using monkeypatched I/O."""

    def _setup_sessions(self, tmp_path: Path) -> list[Path]:
        return [
            _write_session(tmp_path, "alpha-exp/", _make_config("alpha-exp")),
            _write_session(tmp_path, "beta-exp/", _make_config("beta-exp")),
        ]

    def test_returns_none_when_no_sessions(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        result = browse_sessions()
        assert result is None

    def test_back_choice_returns_none(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        self._setup_sessions(tmp_path)

        from rich.prompt import Prompt

        responses = iter(["q"])
        monkeypatch.setattr(Prompt, "ask", staticmethod(lambda *a, **kw: next(responses)))

        result = browse_sessions()
        assert result is None

    def test_select_session_then_back(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        self._setup_sessions(tmp_path)

        from rich.prompt import Prompt

        # Select session 1, then choose [b] back
        responses = iter(["1", "b"])
        monkeypatch.setattr(Prompt, "ask", staticmethod(lambda *a, **kw: next(responses)))

        result = browse_sessions()
        assert result is None

    def test_view_config_then_back(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        self._setup_sessions(tmp_path)

        from rich.prompt import Prompt

        # Select session 1 → view → back
        responses = iter(["1", "v", "b"])
        monkeypatch.setattr(Prompt, "ask", staticmethod(lambda *a, **kw: next(responses)))

        result = browse_sessions()
        assert result is None

    def test_rerun_invokes_subprocess(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        self._setup_sessions(tmp_path)

        from rich.prompt import Prompt

        responses = iter(["1", "r"])
        monkeypatch.setattr(Prompt, "ask", staticmethod(lambda *a, **kw: next(responses)))

        captured_args = []

        def fake_run(args, **kw):
            captured_args.extend(args)

        monkeypatch.setattr("buyerbench.session_browser.subprocess.run", fake_run)

        browse_sessions()

        assert "--from-session" in captured_args
        # The path is relative (CWD is tmp_path) — just check the experiment dir is present
        assert any("alpha-exp" in arg for arg in captured_args)

    def test_modify_calls_wizard_with_prefill(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        self._setup_sessions(tmp_path)

        from rich.prompt import Prompt
        import buyerbench.selector as sel_mod

        responses = iter(["1", "m"])
        monkeypatch.setattr(Prompt, "ask", staticmethod(lambda *a, **kw: next(responses)))

        received_prefill = []

        def fake_wizard(prefill=None):
            received_prefill.append(prefill)

        # Patch wizard_new_session in the selector module (browse_sessions does a local import)
        monkeypatch.setattr(sel_mod, "wizard_new_session", fake_wizard)

        browse_sessions()

        assert len(received_prefill) == 1
        assert isinstance(received_prefill[0], SessionConfig)
        assert received_prefill[0].experiment_name == "alpha-exp"

    def test_skips_malformed_configs(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        # Write a valid and an invalid config
        _write_session(tmp_path, "valid-exp/", _make_config("valid-exp"))
        bad_dir = tmp_path / "sessions" / "bad-exp"
        bad_dir.mkdir(parents=True)
        (bad_dir / "session-config.yaml").write_text("not: valid: yaml: [[[")

        from rich.prompt import Prompt

        responses = iter(["q"])
        monkeypatch.setattr(Prompt, "ask", staticmethod(lambda *a, **kw: next(responses)))

        # Should not raise even with one malformed config
        result = browse_sessions()
        assert result is None


# ── wizard_new_session prefill ────────────────────────────────────────────────


class TestWizardPrefill:
    """Tests that wizard_new_session() correctly applies prefill defaults."""

    _AGENTS = ["openrouter-openai-gpt-4o"]

    def _make_prefill(self) -> SessionConfig:
        return SessionConfig(
            agents=[AgentSlot(agent_id="openrouter-openai-gpt-4o", skill_mode="skills")],
            scenario_ids=["p1-01", "p2-01"],
            created_at="2026-04-09T10:00:00+00:00",
            experiment_name="prefilled-exp",
            research_objective="Evaluate anchoring bias",
            research_notes="Run 3 iterations",
            recurrence=None,
        )

    def test_prefill_keeps_existing_when_user_accepts_defaults(self, tmp_path, monkeypatch):
        from rich.prompt import Prompt
        import buyerbench.selector as sel_mod
        import harness.loader as loader_mod
        from buyerbench.selector import wizard_new_session
        from dataclasses import dataclass
        from enum import Enum

        @dataclass
        class _Scenario:
            id: str
            title: str
            pillar: object
            difficulty: object

        class _Pillar(str, Enum):
            PILLAR1 = "PILLAR1"

        class _Diff(str, Enum):
            easy = "easy"

        fake_scenarios = [_Scenario("p1-01", "T1", _Pillar.PILLAR1, _Diff.easy)]

        monkeypatch.setattr(loader_mod, "load_all_scenarios", lambda *a, **kw: fake_scenarios)

        prefill = self._make_prefill()

        # Simulate user accepting all defaults:
        # Step 1: name=<Enter>, objective=<Enter>
        # Step 2: keep models=y
        # Step 3: keep skills=y
        # Step 4: keep scenarios=y
        # Step 5: schedule=1 (one-shot)
        # Step 6: notes=<Enter>
        # Confirm: y
        prompt_inputs = iter([
            prefill.experiment_name,   # Step 1 name (as default)
            prefill.research_objective,  # Step 1 objective
            "y",  # Step 2: keep models
            "y",  # Step 3: keep skills
            "y",  # Step 4: keep scenarios
            "1",  # Step 5: one-shot
            prefill.research_notes,  # Step 6: notes
            "y",  # Confirm save
        ])

        monkeypatch.setattr(
            Prompt, "ask", staticmethod(lambda *a, **kw: next(prompt_inputs))
        )

        monkeypatch.chdir(tmp_path)
        config = wizard_new_session(prefill=prefill)

        assert config.experiment_name == "prefilled-exp"
        assert config.agents[0].agent_id == "openrouter-openai-gpt-4o"
        assert config.agents[0].skill_mode == "skills"
        assert config.scenario_ids == ["p1-01", "p2-01"]
        assert config.research_notes == "Run 3 iterations"

    def test_wizard_without_prefill_works_unchanged(self, tmp_path, monkeypatch):
        """Calling wizard_new_session() without prefill behaves as before."""
        from dataclasses import dataclass
        from enum import Enum
        from rich.prompt import Prompt
        import buyerbench.selector as sel_mod
        import harness.loader as loader_mod
        from buyerbench.selector import wizard_new_session

        @dataclass
        class _Scenario:
            id: str
            title: str
            pillar: object
            difficulty: object

        class _Pillar(str, Enum):
            PILLAR1 = "PILLAR1"

        class _Diff(str, Enum):
            easy = "easy"

        fake_scenarios = [_Scenario("p1-01", "T1", _Pillar.PILLAR1, _Diff.easy)]

        monkeypatch.setattr(loader_mod, "load_all_scenarios", lambda *a, **kw: fake_scenarios)
        monkeypatch.setattr(
            sel_mod, "interactive_select", lambda *a, **kw: ["openrouter-openai-gpt-4o"]
        )
        monkeypatch.setattr(
            sel_mod, "interactive_skill_select",
            lambda *a, **kw: {"openrouter-openai-gpt-4o": "baseline"},
        )
        monkeypatch.setattr(
            sel_mod, "interactive_scenario_select", lambda *a, **kw: ["p1-01"]
        )

        prompt_inputs = iter([
            "no-prefill-exp",  # Step 1 name
            "",                # Step 1 objective
            "1",               # Step 5: one-shot
            "",                # Step 6: notes
            "y",               # Confirm
        ])
        monkeypatch.setattr(
            Prompt, "ask", staticmethod(lambda *a, **kw: next(prompt_inputs))
        )

        monkeypatch.chdir(tmp_path)
        config = wizard_new_session()

        assert config.experiment_name == "no-prefill-exp"
        assert config.agents[0].agent_id == "openrouter-openai-gpt-4o"
