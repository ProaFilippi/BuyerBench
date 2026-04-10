"""Tests for buyerbench.home — first-launch detection and onboarding."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from buyerbench.home import _is_first_launch, _show_onboarding, _show_home


# ── _is_first_launch ──────────────────────────────────────────────────────────


class TestIsFirstLaunch:
    def test_true_when_no_sessions_and_no_results(self, tmp_path):
        results = tmp_path / "results"
        sessions = tmp_path / "sessions"
        assert _is_first_launch(results, sessions) is True

    def test_false_when_sessions_dir_exists(self, tmp_path):
        results = tmp_path / "results"
        sessions = tmp_path / "sessions"
        sessions.mkdir()
        assert _is_first_launch(results, sessions) is False

    def test_false_when_results_has_json(self, tmp_path):
        results = tmp_path / "results"
        results.mkdir()
        (results / "run.json").write_text(json.dumps({"status": "done"}))
        sessions = tmp_path / "sessions"
        assert _is_first_launch(results, sessions) is False

    def test_false_when_both_exist(self, tmp_path):
        results = tmp_path / "results"
        results.mkdir()
        (results / "run.json").write_text("{}")
        sessions = tmp_path / "sessions"
        sessions.mkdir()
        assert _is_first_launch(results, sessions) is False

    def test_true_when_results_dir_exists_but_empty(self, tmp_path):
        """An empty results dir with no JSON files still counts as first launch."""
        results = tmp_path / "results"
        results.mkdir()
        sessions = tmp_path / "sessions"
        assert _is_first_launch(results, sessions) is True

    def test_false_when_results_has_nested_json(self, tmp_path):
        """JSON files in subdirectories are found via rglob."""
        results = tmp_path / "results"
        subdir = results / "exp-01"
        subdir.mkdir(parents=True)
        (subdir / "result.json").write_text("{}")
        sessions = tmp_path / "sessions"
        assert _is_first_launch(results, sessions) is False


# ── _show_onboarding ──────────────────────────────────────────────────────────


class TestShowOnboarding:
    def test_prints_welcome_and_waits_for_enter(self, monkeypatch, capsys):
        from rich.prompt import Prompt

        prompts_seen = []
        monkeypatch.setattr(
            Prompt,
            "ask",
            staticmethod(lambda prompt, **kw: prompts_seen.append(prompt) or ""),
        )
        _show_onboarding()
        assert any("Enter" in p or "continue" in str(p).lower() for p in prompts_seen)


# ── _show_home with first-launch gate ────────────────────────────────────────


class TestShowHomeFirstLaunch:
    """Verify _show_home() shows the onboarding panel on first launch."""

    def _patch_paths(self, monkeypatch, tmp_path, *, with_json: bool = False):
        """Redirect _RESULTS_ROOT and _SESSIONS_ROOT to tmp_path subdirs."""
        import buyerbench.home as home_mod

        results = tmp_path / "results"
        sessions = tmp_path / "sessions"
        if with_json:
            results.mkdir(parents=True)
            (results / "run.json").write_text("{}")
        monkeypatch.setattr(home_mod, "_RESULTS_ROOT", results)
        monkeypatch.setattr(home_mod, "_SESSIONS_ROOT", sessions)
        return results, sessions

    def test_onboarding_called_on_first_launch(self, monkeypatch, tmp_path):
        self._patch_paths(monkeypatch, tmp_path)
        onboarding_called = []

        import buyerbench.home as home_mod
        from rich.prompt import Prompt

        monkeypatch.setattr(home_mod, "_show_onboarding", lambda: onboarding_called.append(True))
        # Prompt.ask returns "q" so _show_home() exits cleanly after the menu
        monkeypatch.setattr(
            Prompt, "ask", staticmethod(lambda *a, **kw: "q")
        )
        home_mod._show_home()
        assert onboarding_called == [True]

    def test_onboarding_not_called_when_results_exist(self, monkeypatch, tmp_path):
        self._patch_paths(monkeypatch, tmp_path, with_json=True)
        onboarding_called = []

        import buyerbench.home as home_mod
        from rich.prompt import Prompt

        monkeypatch.setattr(home_mod, "_show_onboarding", lambda: onboarding_called.append(True))
        monkeypatch.setattr(
            Prompt, "ask", staticmethod(lambda *a, **kw: "q")
        )
        home_mod._show_home()
        assert onboarding_called == []

    def test_onboarding_not_called_when_sessions_dir_exists(self, monkeypatch, tmp_path):
        results, sessions = self._patch_paths(monkeypatch, tmp_path)
        sessions.mkdir()
        onboarding_called = []

        import buyerbench.home as home_mod
        from rich.prompt import Prompt

        monkeypatch.setattr(home_mod, "_show_onboarding", lambda: onboarding_called.append(True))
        monkeypatch.setattr(
            Prompt, "ask", staticmethod(lambda *a, **kw: "q")
        )
        home_mod._show_home()
        assert onboarding_called == []
