"""Tests for UPGRADE-15: OSF pre-registration export."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from results.experiment_manifest import ExperimentManifest
from results.prereg_export import (
    BUYERBENCH_HYPOTHESES,
    CONFIRMATORY_HYPOTHESIS_IDS,
    HypothesisDef,
    PreregistrationDocument,
    build_planned_manifest,
    build_prereg_document,
    generate_prereg_document,
    render_prereg_markdown,
    write_prereg_document,
)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _make_manifest(**kwargs) -> ExperimentManifest:
    defaults = dict(
        experiment_id="session-20260416-100000",
        n_models=10,
        n_scenarios=10,
        n_runs_per_cell=30,
        temperatures=[0.7],
        prompt_versions=["standard"],
        total_planned_runs=3000,
        start_time_utc="2026-04-16T10:00:00+00:00",
        pillars=[2],
        output_dir="/tmp/test-run",
        git_commit_hash="abc1234",
        design_tier="realistic",
        n_bias_types=5,
        n_variants_per_bias=2,
    )
    defaults.update(kwargs)
    return ExperimentManifest(**defaults)


# ── TestHypothesisDef ─────────────────────────────────────────────────────────

class TestHypothesisDef:
    def test_buyerbench_hypotheses_count(self):
        assert len(BUYERBENCH_HYPOTHESES) == 10

    def test_hypothesis_ids_unique(self):
        ids = [h.id for h in BUYERBENCH_HYPOTHESES]
        assert len(ids) == len(set(ids))

    def test_hypothesis_ids_h1_to_h10(self):
        ids = {h.id for h in BUYERBENCH_HYPOTHESES}
        assert ids == {f"H{i}" for i in range(1, 11)}

    def test_all_hypotheses_have_required_fields(self):
        for hyp in BUYERBENCH_HYPOTHESES:
            assert hyp.label, f"{hyp.id} missing label"
            assert hyp.statement, f"{hyp.id} missing statement"
            assert hyp.test, f"{hyp.id} missing test"
            assert hyp.null_outcome, f"{hyp.id} missing null_outcome"
            assert hyp.data_requirement, f"{hyp.id} missing data_requirement"
            assert hyp.prq_dimension, f"{hyp.id} missing prq_dimension"

    def test_hypothesis_directions_valid(self):
        valid_directions = {"positive", "negative", "null", "non_directional"}
        for hyp in BUYERBENCH_HYPOTHESES:
            assert hyp.direction in valid_directions, (
                f"{hyp.id} has invalid direction: {hyp.direction}"
            )

    def test_h1_bias_universality(self):
        h1 = next(h for h in BUYERBENCH_HYPOTHESES if h.id == "H1")
        assert "Universality" in h1.label
        assert "BSI" in h1.statement
        assert "D1" in h1.prq_dimension

    def test_h2_capability_bias(self):
        h2 = next(h for h in BUYERBENCH_HYPOTHESES if h.id == "H2")
        assert h2.direction == "negative"
        assert "Spearman" in h2.test

    def test_h10_human_benchmark(self):
        h10 = next(h for h in BUYERBENCH_HYPOTHESES if h.id == "H10")
        assert "Human" in h10.label
        assert h10.direction == "negative"
        assert "Cohen" in h10.test


# ── TestBuildPreregDocument ───────────────────────────────────────────────────

class TestBuildPreregDocument:
    def test_returns_prereg_document(self):
        manifest = _make_manifest()
        doc = build_prereg_document(manifest)
        assert isinstance(doc, PreregistrationDocument)

    def test_experiment_id_propagated(self):
        manifest = _make_manifest(experiment_id="session-20260416-999999")
        doc = build_prereg_document(manifest)
        assert doc.manifest_experiment_id == "session-20260416-999999"

    def test_git_hash_propagated(self):
        manifest = _make_manifest(git_commit_hash="deadbeef")
        doc = build_prereg_document(manifest)
        assert doc.manifest_git_hash == "deadbeef"

    def test_git_hash_none_propagated(self):
        manifest = _make_manifest(git_commit_hash=None)
        doc = build_prereg_document(manifest)
        assert doc.manifest_git_hash is None

    def test_n_models_propagated(self):
        manifest = _make_manifest(n_models=5)
        doc = build_prereg_document(manifest)
        assert doc.manifest_n_models == 5

    def test_n_scenarios_propagated(self):
        manifest = _make_manifest(n_scenarios=8)
        doc = build_prereg_document(manifest)
        assert doc.manifest_n_scenarios == 8

    def test_n_runs_per_cell_propagated(self):
        manifest = _make_manifest(n_runs_per_cell=50)
        doc = build_prereg_document(manifest)
        assert doc.manifest_n_runs_per_cell == 50

    def test_temperatures_propagated(self):
        manifest = _make_manifest(temperatures=[0.0, 0.7])
        doc = build_prereg_document(manifest)
        assert doc.manifest_temperatures == [0.0, 0.7]

    def test_temperature_none_propagated(self):
        manifest = _make_manifest(temperatures=[None])
        doc = build_prereg_document(manifest)
        assert doc.manifest_temperatures == [None]

    def test_prompt_versions_propagated(self):
        manifest = _make_manifest(prompt_versions=["standard", "cot"])
        doc = build_prereg_document(manifest)
        assert doc.manifest_prompt_versions == ["standard", "cot"]

    def test_total_planned_runs_propagated(self):
        manifest = _make_manifest(total_planned_runs=5000)
        doc = build_prereg_document(manifest)
        assert doc.manifest_total_planned_runs == 5000

    def test_pre_registration_url_none_by_default(self):
        manifest = _make_manifest()
        doc = build_prereg_document(manifest)
        assert doc.manifest_pre_registration_url is None

    def test_pre_registration_url_propagated(self):
        manifest = _make_manifest(pre_registration_url="https://osf.io/test123")
        doc = build_prereg_document(manifest)
        assert doc.manifest_pre_registration_url == "https://osf.io/test123"

    def test_default_hypotheses_loaded(self):
        manifest = _make_manifest()
        doc = build_prereg_document(manifest)
        assert len(doc.hypotheses) == 10

    def test_custom_hypotheses_accepted(self):
        manifest = _make_manifest()
        custom = [
            HypothesisDef(
                id="HC1",
                label="Custom Test",
                prq_dimension="D1",
                statement="Test statement.",
                direction="positive",
                test="t-test",
                null_outcome="No effect.",
                data_requirement="N=10",
            )
        ]
        doc = build_prereg_document(manifest, hypotheses=custom)
        assert len(doc.hypotheses) == 1
        assert doc.hypotheses[0].id == "HC1"

    def test_default_bias_types_set(self):
        manifest = _make_manifest()
        doc = build_prereg_document(manifest)
        assert "anchoring" in doc.bias_types_tested
        assert "framing" in doc.bias_types_tested
        assert "decoy" in doc.bias_types_tested
        assert "scarcity" in doc.bias_types_tested
        assert "sunk_cost" in doc.bias_types_tested

    def test_custom_bias_types_accepted(self):
        manifest = _make_manifest()
        doc = build_prereg_document(manifest, bias_types=["anchoring", "framing"])
        assert doc.bias_types_tested == ["anchoring", "framing"]

    def test_default_model_set_has_10_models(self):
        manifest = _make_manifest()
        doc = build_prereg_document(manifest)
        assert len(doc.model_set) == 10

    def test_custom_model_set_accepted(self):
        manifest = _make_manifest()
        custom_models = ["openai/gpt-4o", "anthropic/claude-3.5-sonnet"]
        doc = build_prereg_document(manifest, model_set=custom_models)
        assert doc.model_set == custom_models

    def test_default_title_contains_buyerbench(self):
        manifest = _make_manifest()
        doc = build_prereg_document(manifest)
        assert "BuyerBench" in doc.title

    def test_custom_title_accepted(self):
        manifest = _make_manifest()
        doc = build_prereg_document(manifest, title="My Custom Study")
        assert doc.title == "My Custom Study"

    def test_authors_default(self):
        manifest = _make_manifest()
        doc = build_prereg_document(manifest)
        assert "BuyerBench" in doc.authors

    def test_custom_authors_accepted(self):
        manifest = _make_manifest()
        doc = build_prereg_document(manifest, authors="Jane Doe, John Smith")
        assert doc.authors == "Jane Doe, John Smith"

    def test_primary_outcome_references_n_runs(self):
        manifest = _make_manifest(n_runs_per_cell=50)
        doc = build_prereg_document(manifest)
        assert "50" in doc.primary_outcome

    def test_secondary_outcomes_not_empty(self):
        manifest = _make_manifest()
        doc = build_prereg_document(manifest)
        assert len(doc.secondary_outcomes) >= 3

    def test_bsi_threshold_contains_alpha(self):
        manifest = _make_manifest()
        doc = build_prereg_document(manifest)
        assert "0.05" in doc.bsi_significance_threshold

    def test_stopping_rule_references_n_runs(self):
        manifest = _make_manifest(n_runs_per_cell=30)
        doc = build_prereg_document(manifest)
        assert "30" in doc.stopping_rule

    def test_null_result_framing_not_empty(self):
        manifest = _make_manifest()
        doc = build_prereg_document(manifest)
        assert doc.null_result_framing
        # The framing describes the outcome when H₀ is not rejected (BSI ≈ 0)
        assert "BSI" in doc.null_result_framing or "bias" in doc.null_result_framing.lower()

    def test_exclusion_criteria_not_empty(self):
        manifest = _make_manifest()
        doc = build_prereg_document(manifest)
        assert len(doc.exclusion_criteria) >= 2

    def test_alpha_level(self):
        manifest = _make_manifest()
        doc = build_prereg_document(manifest)
        assert doc.alpha_level == 0.05

    def test_fdr_q_level(self):
        manifest = _make_manifest()
        doc = build_prereg_document(manifest)
        assert doc.fdr_q_level == 0.05


# ── TestRenderPreregMarkdown ──────────────────────────────────────────────────

class TestRenderPreregMarkdown:
    def _doc(self, **kwargs) -> PreregistrationDocument:
        return build_prereg_document(_make_manifest(**kwargs))

    def test_returns_string(self):
        doc = self._doc()
        md = render_prereg_markdown(doc)
        assert isinstance(md, str)
        assert len(md) > 500

    def test_has_yaml_front_matter(self):
        doc = self._doc()
        md = render_prereg_markdown(doc)
        assert md.startswith("---")
        assert "experiment_id" in md

    def test_has_section_1_study_information(self):
        doc = self._doc()
        md = render_prereg_markdown(doc)
        assert "1. Study Information" in md

    def test_has_section_2_design_plan(self):
        doc = self._doc()
        md = render_prereg_markdown(doc)
        assert "2. Design Plan" in md

    def test_has_section_3_sampling_plan(self):
        doc = self._doc()
        md = render_prereg_markdown(doc)
        assert "3. Sampling Plan" in md

    def test_has_section_4_variables(self):
        doc = self._doc()
        md = render_prereg_markdown(doc)
        assert "4. Variables" in md

    def test_has_section_5_analysis_plan(self):
        doc = self._doc()
        md = render_prereg_markdown(doc)
        assert "5. Analysis Plan" in md

    def test_has_section_6_hypotheses(self):
        doc = self._doc()
        md = render_prereg_markdown(doc)
        assert "6. Pre-Specified Hypotheses" in md

    def test_has_section_7_other(self):
        doc = self._doc()
        md = render_prereg_markdown(doc)
        assert "7. Other" in md

    def test_all_hypothesis_ids_present(self):
        doc = self._doc()
        md = render_prereg_markdown(doc)
        for i in range(1, 11):
            assert f"H{i}" in md, f"H{i} not found in markdown"

    def test_experiment_id_in_document(self):
        doc = build_prereg_document(
            _make_manifest(experiment_id="session-20260416-TEST")
        )
        md = render_prereg_markdown(doc)
        assert "session-20260416-TEST" in md

    def test_git_hash_in_document(self):
        doc = build_prereg_document(_make_manifest(git_commit_hash="cafebabe"))
        md = render_prereg_markdown(doc)
        assert "cafebabe" in md

    def test_git_hash_none_shows_unknown(self):
        doc = build_prereg_document(_make_manifest(git_commit_hash=None))
        md = render_prereg_markdown(doc)
        assert "unknown" in md

    def test_pre_registration_url_included_when_set(self):
        doc = build_prereg_document(
            _make_manifest(pre_registration_url="https://osf.io/abc123")
        )
        md = render_prereg_markdown(doc)
        assert "https://osf.io/abc123" in md

    def test_pre_registration_url_absent_when_none(self):
        doc = build_prereg_document(_make_manifest(pre_registration_url=None))
        md = render_prereg_markdown(doc)
        assert "https://osf.io" not in md

    def test_model_set_present(self):
        doc = self._doc()
        md = render_prereg_markdown(doc)
        assert "openai/gpt-4o" in md

    def test_bias_types_present(self):
        doc = self._doc()
        md = render_prereg_markdown(doc)
        for bias in ["anchoring", "framing", "decoy", "scarcity", "sunk_cost"]:
            assert bias in md, f"{bias} not in markdown"

    def test_bh_fdr_mentioned(self):
        doc = self._doc()
        md = render_prereg_markdown(doc)
        assert "BH-FDR" in md

    def test_n_runs_per_cell_mentioned(self):
        doc = build_prereg_document(_make_manifest(n_runs_per_cell=50))
        md = render_prereg_markdown(doc)
        assert "50" in md

    def test_temperature_listed(self):
        doc = build_prereg_document(_make_manifest(temperatures=[0.7]))
        md = render_prereg_markdown(doc)
        assert "0.7" in md

    def test_temperature_none_shows_provider_default(self):
        doc = build_prereg_document(_make_manifest(temperatures=[None]))
        md = render_prereg_markdown(doc)
        assert "provider default" in md.lower()

    def test_references_section_present(self):
        doc = self._doc()
        md = render_prereg_markdown(doc)
        assert "Tversky" in md
        assert "Kahneman" in md
        assert "Benjamini" in md

    def test_null_result_framing_present(self):
        doc = self._doc()
        md = render_prereg_markdown(doc)
        assert "null result" in md.lower() or "null outcome" in md.lower()

    def test_open_science_statement_present(self):
        doc = self._doc()
        md = render_prereg_markdown(doc)
        assert "open-source" in md.lower() or "Open Science" in md

    def test_custom_author_appears_in_document(self):
        doc = build_prereg_document(_make_manifest(), authors="Dr. Smith")
        md = render_prereg_markdown(doc)
        assert "Dr. Smith" in md

    def test_custom_bias_types_in_registered_battery_section(self):
        """Custom bias types appear in the registered battery section (Section 7.2)."""
        doc = build_prereg_document(
            _make_manifest(), bias_types=["anchoring", "framing"]
        )
        md = render_prereg_markdown(doc)
        # The registered battery section should list only our custom types
        assert "7.2 Registered Bias Type Battery" in md
        # Both custom types appear in the document
        assert "anchoring" in md
        assert "framing" in md
        # sunk_cost is NOT in our custom list and should not appear in the
        # registered battery section — though it may appear in hypothesis text
        battery_section = md.split("7.2 Registered Bias Type Battery")[1].split("\n##")[0]
        assert "sunk_cost" not in battery_section

    def test_custom_model_set_in_document(self):
        doc = build_prereg_document(
            _make_manifest(), model_set=["openai/gpt-4o"]
        )
        md = render_prereg_markdown(doc)
        assert "openai/gpt-4o" in md


# ── TestGeneratePreregDocument ────────────────────────────────────────────────

class TestGeneratePreregDocument:
    def test_returns_tuple(self):
        manifest = _make_manifest()
        result = generate_prereg_document(manifest)
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_first_element_is_document(self):
        manifest = _make_manifest()
        doc, _ = generate_prereg_document(manifest)
        assert isinstance(doc, PreregistrationDocument)

    def test_second_element_is_string(self):
        manifest = _make_manifest()
        _, md = generate_prereg_document(manifest)
        assert isinstance(md, str)

    def test_document_and_markdown_consistent(self):
        manifest = _make_manifest(experiment_id="session-CONSISTENCY")
        doc, md = generate_prereg_document(manifest)
        assert doc.manifest_experiment_id == "session-CONSISTENCY"
        assert "session-CONSISTENCY" in md

    def test_kwargs_forwarded_to_build(self):
        manifest = _make_manifest()
        doc, _ = generate_prereg_document(manifest, title="Custom Title")
        assert doc.title == "Custom Title"


# ── TestWritePreregDocument ───────────────────────────────────────────────────

class TestWritePreregDocument:
    def test_creates_md_file(self, tmp_path):
        manifest = _make_manifest()
        doc, md = generate_prereg_document(manifest)
        path = write_prereg_document(doc, md, tmp_path)
        assert path.exists()
        assert path.name == "prereg_osf.md"

    def test_creates_json_file(self, tmp_path):
        manifest = _make_manifest()
        doc, md = generate_prereg_document(manifest)
        write_prereg_document(doc, md, tmp_path)
        json_path = tmp_path / "prereg_metadata.json"
        assert json_path.exists()

    def test_md_file_content_correct(self, tmp_path):
        manifest = _make_manifest(experiment_id="session-WRITE-TEST")
        doc, md = generate_prereg_document(manifest)
        path = write_prereg_document(doc, md, tmp_path)
        content = path.read_text(encoding="utf-8")
        assert "session-WRITE-TEST" in content

    def test_json_file_is_valid_json(self, tmp_path):
        manifest = _make_manifest()
        doc, md = generate_prereg_document(manifest)
        write_prereg_document(doc, md, tmp_path)
        data = json.loads((tmp_path / "prereg_metadata.json").read_text())
        assert isinstance(data, dict)

    def test_json_file_contains_experiment_id(self, tmp_path):
        manifest = _make_manifest(experiment_id="session-JSON-TEST")
        doc, md = generate_prereg_document(manifest)
        write_prereg_document(doc, md, tmp_path)
        data = json.loads((tmp_path / "prereg_metadata.json").read_text())
        assert data["manifest_experiment_id"] == "session-JSON-TEST"

    def test_json_file_contains_hypotheses(self, tmp_path):
        manifest = _make_manifest()
        doc, md = generate_prereg_document(manifest)
        write_prereg_document(doc, md, tmp_path)
        data = json.loads((tmp_path / "prereg_metadata.json").read_text())
        assert "hypotheses" in data
        assert len(data["hypotheses"]) == 10

    def test_creates_output_dir_if_missing(self, tmp_path):
        manifest = _make_manifest()
        doc, md = generate_prereg_document(manifest)
        new_dir = tmp_path / "nested" / "output"
        assert not new_dir.exists()
        write_prereg_document(doc, md, new_dir)
        assert new_dir.exists()
        assert (new_dir / "prereg_osf.md").exists()

    def test_returns_path_to_md_file(self, tmp_path):
        manifest = _make_manifest()
        doc, md = generate_prereg_document(manifest)
        result = write_prereg_document(doc, md, tmp_path)
        assert isinstance(result, Path)
        assert result.name == "prereg_osf.md"

    def test_string_path_accepted(self, tmp_path):
        manifest = _make_manifest()
        doc, md = generate_prereg_document(manifest)
        path = write_prereg_document(doc, md, str(tmp_path))
        assert path.exists()

    def test_json_round_trip(self, tmp_path):
        """Document model survives JSON serialization."""
        manifest = _make_manifest(git_commit_hash="abc123")
        doc, md = generate_prereg_document(manifest)
        write_prereg_document(doc, md, tmp_path)
        data = json.loads((tmp_path / "prereg_metadata.json").read_text())
        assert data["manifest_git_hash"] == "abc123"
        assert isinstance(data["hypotheses"], list)
        assert data["hypotheses"][0]["id"] == "H1"


# ── TestCLIIntegration ────────────────────────────────────────────────────────

class TestCLIIntegration:
    def test_prereg_command_writes_files(self, tmp_path):
        """End-to-end: CLI reads manifest JSON, writes prereg_osf.md."""
        from click.testing import CliRunner
        from buyerbench.__main__ import cli

        manifest = _make_manifest(experiment_id="session-CLI-TEST")
        manifest_path = tmp_path / "experiment_manifest.json"
        manifest_path.write_text(
            json.dumps(manifest.model_dump(), default=str), encoding="utf-8"
        )

        runner = CliRunner()
        result = runner.invoke(
            cli,
            [
                "prereg",
                "--manifest",
                str(manifest_path),
                "--output-dir",
                str(tmp_path),
            ],
        )
        assert result.exit_code == 0, result.output
        assert (tmp_path / "prereg_osf.md").exists()
        assert (tmp_path / "prereg_metadata.json").exists()

    def test_prereg_command_output_contains_experiment_id(self, tmp_path):
        from click.testing import CliRunner
        from buyerbench.__main__ import cli

        manifest = _make_manifest(experiment_id="session-CLI-OUTPUT")
        manifest_path = tmp_path / "experiment_manifest.json"
        manifest_path.write_text(
            json.dumps(manifest.model_dump(), default=str), encoding="utf-8"
        )

        runner = CliRunner()
        runner.invoke(
            cli,
            [
                "prereg",
                "--manifest",
                str(manifest_path),
                "--output-dir",
                str(tmp_path),
            ],
        )
        content = (tmp_path / "prereg_osf.md").read_text()
        assert "session-CLI-OUTPUT" in content

    def test_prereg_command_nonexistent_manifest_exits_1(self, tmp_path):
        from click.testing import CliRunner
        from buyerbench.__main__ import cli

        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["prereg", "--manifest", str(tmp_path / "nonexistent.json")],
        )
        assert result.exit_code == 1

    def test_prereg_command_custom_title(self, tmp_path):
        from click.testing import CliRunner
        from buyerbench.__main__ import cli

        manifest = _make_manifest()
        manifest_path = tmp_path / "experiment_manifest.json"
        manifest_path.write_text(
            json.dumps(manifest.model_dump(), default=str), encoding="utf-8"
        )

        runner = CliRunner()
        runner.invoke(
            cli,
            [
                "prereg",
                "--manifest",
                str(manifest_path),
                "--output-dir",
                str(tmp_path),
                "--title",
                "Custom Study Title",
            ],
        )
        content = (tmp_path / "prereg_osf.md").read_text()
        assert "Custom Study Title" in content

    def test_prereg_command_custom_authors(self, tmp_path):
        from click.testing import CliRunner
        from buyerbench.__main__ import cli

        manifest = _make_manifest()
        manifest_path = tmp_path / "experiment_manifest.json"
        manifest_path.write_text(
            json.dumps(manifest.model_dump(), default=str), encoding="utf-8"
        )

        runner = CliRunner()
        runner.invoke(
            cli,
            [
                "prereg",
                "--manifest",
                str(manifest_path),
                "--output-dir",
                str(tmp_path),
                "--authors",
                "Alice Smith",
            ],
        )
        content = (tmp_path / "prereg_osf.md").read_text()
        assert "Alice Smith" in content

    def test_prereg_defaults_output_to_manifest_dir(self, tmp_path):
        """--output-dir defaults to parent of --manifest."""
        from click.testing import CliRunner
        from buyerbench.__main__ import cli

        manifest = _make_manifest()
        manifest_path = tmp_path / "experiment_manifest.json"
        manifest_path.write_text(
            json.dumps(manifest.model_dump(), default=str), encoding="utf-8"
        )

        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["prereg", "--manifest", str(manifest_path)],
        )
        assert result.exit_code == 0, result.output
        assert (tmp_path / "prereg_osf.md").exists()

    def test_prereg_invalid_manifest_json_exits_1(self, tmp_path):
        from click.testing import CliRunner
        from buyerbench.__main__ import cli

        manifest_path = tmp_path / "experiment_manifest.json"
        manifest_path.write_text("not valid json", encoding="utf-8")

        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["prereg", "--manifest", str(manifest_path), "--output-dir", str(tmp_path)],
        )
        assert result.exit_code == 1

    def test_prereg_standalone_writes_files(self, tmp_path):
        """Standalone mode generates prereg document without a manifest file."""
        from click.testing import CliRunner
        from buyerbench.__main__ import cli

        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["prereg", "--standalone", "--output-dir", str(tmp_path)],
        )
        assert result.exit_code == 0, result.output
        assert (tmp_path / "prereg_osf.md").exists()
        assert (tmp_path / "prereg_metadata.json").exists()

    def test_prereg_standalone_document_contains_hypotheses(self, tmp_path):
        """Standalone prereg document includes the registered hypotheses."""
        from click.testing import CliRunner
        from buyerbench.__main__ import cli

        runner = CliRunner()
        runner.invoke(
            cli, ["prereg", "--standalone", "--output-dir", str(tmp_path)]
        )
        content = (tmp_path / "prereg_osf.md").read_text()
        assert "H1" in content
        assert "H10" in content
        assert "BuyerBench" in content

    def test_prereg_standalone_and_manifest_mutually_exclusive(self, tmp_path):
        """--standalone and --manifest together should exit with code 1."""
        from click.testing import CliRunner
        from buyerbench.__main__ import cli

        manifest = _make_manifest()
        manifest_path = tmp_path / "experiment_manifest.json"
        manifest_path.write_text(
            json.dumps(manifest.model_dump(), default=str), encoding="utf-8"
        )

        runner = CliRunner()
        result = runner.invoke(
            cli,
            ["prereg", "--standalone", "--manifest", str(manifest_path), "--output-dir", str(tmp_path)],
        )
        assert result.exit_code == 1

    def test_prereg_no_flags_exits_1(self, tmp_path):
        """Calling prereg without --manifest or --standalone exits with code 1."""
        from click.testing import CliRunner
        from buyerbench.__main__ import cli

        runner = CliRunner()
        result = runner.invoke(
            cli, ["prereg", "--output-dir", str(tmp_path)]
        )
        assert result.exit_code == 1


# ── TestBuildPlannedManifest ──────────────────────────────────────────────────

class TestBuildPlannedManifest:
    def test_returns_experiment_manifest(self):
        manifest = build_planned_manifest()
        assert isinstance(manifest, ExperimentManifest)

    def test_default_n_models_is_10(self):
        manifest = build_planned_manifest()
        assert manifest.n_models == 10

    def test_default_n_scenarios_is_10(self):
        manifest = build_planned_manifest()
        assert manifest.n_scenarios == 10

    def test_default_n_runs_per_cell_is_50(self):
        manifest = build_planned_manifest()
        assert manifest.n_runs_per_cell == 50

    def test_default_design_tier_is_realistic(self):
        manifest = build_planned_manifest()
        assert manifest.design_tier == "realistic"

    def test_default_pillars_is_2(self):
        manifest = build_planned_manifest()
        assert manifest.pillars == [2]

    def test_default_temperatures(self):
        manifest = build_planned_manifest()
        assert manifest.temperatures == [0.7]

    def test_default_prompt_versions(self):
        manifest = build_planned_manifest()
        assert manifest.prompt_versions == ["standard"]

    def test_total_planned_runs_computed(self):
        # 10 models × 10 scenarios × 50 runs × 1 temperature × 1 prompt version = 5000
        manifest = build_planned_manifest()
        assert manifest.total_planned_runs == 5000

    def test_custom_n_runs_per_cell(self):
        manifest = build_planned_manifest(n_runs_per_cell=30)
        assert manifest.n_runs_per_cell == 30

    def test_custom_n_runs_changes_total_planned(self):
        manifest = build_planned_manifest(n_runs_per_cell=30)
        assert manifest.total_planned_runs == 10 * 10 * 30  # 3000

    def test_custom_experiment_id(self):
        manifest = build_planned_manifest(experiment_id="my-experiment-v2")
        assert manifest.experiment_id == "my-experiment-v2"

    def test_default_pre_registration_url_is_none(self):
        manifest = build_planned_manifest()
        assert manifest.pre_registration_url is None

    def test_pre_registration_url_can_be_set(self):
        manifest = build_planned_manifest(pre_registration_url="https://osf.io/abc123")
        assert manifest.pre_registration_url == "https://osf.io/abc123"

    def test_git_commit_hash_defaults_to_none(self):
        manifest = build_planned_manifest()
        assert manifest.git_commit_hash is None

    def test_git_commit_hash_can_be_set(self):
        manifest = build_planned_manifest(git_commit_hash="deadbeef")
        assert manifest.git_commit_hash == "deadbeef"

    def test_custom_temperatures(self):
        manifest = build_planned_manifest(temperatures=[0.0, 0.7])
        assert manifest.temperatures == [0.0, 0.7]

    def test_custom_prompt_versions(self):
        manifest = build_planned_manifest(prompt_versions=["standard", "cot"])
        assert manifest.prompt_versions == ["standard", "cot"]

    def test_multiple_temperatures_scales_total_runs(self):
        manifest = build_planned_manifest(temperatures=[0.0, 0.7])
        assert manifest.total_planned_runs == 10 * 10 * 50 * 2  # 10000

    def test_multiple_prompt_versions_scales_total_runs(self):
        manifest = build_planned_manifest(prompt_versions=["standard", "cot"])
        assert manifest.total_planned_runs == 10 * 10 * 50 * 2  # 10000

    def test_start_time_utc_is_set(self):
        manifest = build_planned_manifest()
        assert manifest.start_time_utc is not None
        assert "T" in manifest.start_time_utc  # ISO datetime format

    def test_n_bias_types_is_5(self):
        manifest = build_planned_manifest()
        assert manifest.n_bias_types == 5

    def test_n_variants_per_bias_is_2(self):
        manifest = build_planned_manifest()
        assert manifest.n_variants_per_bias == 2


# ── TestGeneratePreregDocumentStandalone ──────────────────────────────────────

class TestGeneratePreregDocumentStandalone:
    def test_none_manifest_returns_tuple(self):
        """generate_prereg_document(None) uses planned manifest defaults."""
        result = generate_prereg_document(None)
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_none_manifest_document_has_10_hypotheses(self):
        doc, _ = generate_prereg_document(None)
        assert len(doc.hypotheses) == 10

    def test_none_manifest_document_has_50_runs(self):
        doc, _ = generate_prereg_document(None)
        assert doc.manifest_n_runs_per_cell == 50

    def test_none_manifest_markdown_is_nonempty_string(self):
        _, md = generate_prereg_document(None)
        assert isinstance(md, str)
        assert len(md) > 100

    def test_none_manifest_title_is_set(self):
        doc, _ = generate_prereg_document(None)
        assert "BuyerBench" in doc.title

    def test_no_args_call_is_equivalent_to_none_manifest(self):
        """generate_prereg_document() with no args == generate_prereg_document(None)."""
        doc1, _ = generate_prereg_document()
        doc2, _ = generate_prereg_document(None)
        assert doc1.manifest_experiment_id == doc2.manifest_experiment_id
        assert doc1.manifest_n_runs_per_cell == doc2.manifest_n_runs_per_cell

    def test_none_manifest_accepts_kwargs(self):
        doc, _ = generate_prereg_document(None, title="Custom Standalone Title")
        assert doc.title == "Custom Standalone Title"

    def test_explicit_manifest_still_works(self):
        """Passing an actual manifest still works as before."""
        manifest = _make_manifest(n_runs_per_cell=20)
        doc, _ = generate_prereg_document(manifest)
        assert doc.manifest_n_runs_per_cell == 20


# ── TestConfirmatoryExploratorySplit ─────────────────────────────────────────

class TestConfirmatoryExploratorySplit:
    """Tests for the confirmatory/exploratory analysis_type classification."""

    def test_confirmatory_ids_constant_has_four_elements(self):
        assert len(CONFIRMATORY_HYPOTHESIS_IDS) == 4

    def test_confirmatory_ids_are_h1_h3_h5_h7(self):
        assert CONFIRMATORY_HYPOTHESIS_IDS == {"H1", "H3", "H5", "H7"}

    def test_h1_is_confirmatory(self):
        h1 = next(h for h in BUYERBENCH_HYPOTHESES if h.id == "H1")
        assert h1.analysis_type == "confirmatory"

    def test_h3_is_confirmatory(self):
        h3 = next(h for h in BUYERBENCH_HYPOTHESES if h.id == "H3")
        assert h3.analysis_type == "confirmatory"

    def test_h5_is_confirmatory(self):
        h5 = next(h for h in BUYERBENCH_HYPOTHESES if h.id == "H5")
        assert h5.analysis_type == "confirmatory"

    def test_h7_is_confirmatory(self):
        h7 = next(h for h in BUYERBENCH_HYPOTHESES if h.id == "H7")
        assert h7.analysis_type == "confirmatory"

    def test_h2_is_exploratory(self):
        h2 = next(h for h in BUYERBENCH_HYPOTHESES if h.id == "H2")
        assert h2.analysis_type == "exploratory"

    def test_h4_is_exploratory(self):
        h4 = next(h for h in BUYERBENCH_HYPOTHESES if h.id == "H4")
        assert h4.analysis_type == "exploratory"

    def test_h6_is_exploratory(self):
        h6 = next(h for h in BUYERBENCH_HYPOTHESES if h.id == "H6")
        assert h6.analysis_type == "exploratory"

    def test_h8_is_exploratory(self):
        h8 = next(h for h in BUYERBENCH_HYPOTHESES if h.id == "H8")
        assert h8.analysis_type == "exploratory"

    def test_h9_is_exploratory(self):
        h9 = next(h for h in BUYERBENCH_HYPOTHESES if h.id == "H9")
        assert h9.analysis_type == "exploratory"

    def test_h10_is_exploratory(self):
        h10 = next(h for h in BUYERBENCH_HYPOTHESES if h.id == "H10")
        assert h10.analysis_type == "exploratory"

    def test_confirmatory_set_matches_constant(self):
        confirmatory = {h.id for h in BUYERBENCH_HYPOTHESES if h.analysis_type == "confirmatory"}
        assert confirmatory == CONFIRMATORY_HYPOTHESIS_IDS

    def test_exploratory_count_is_six(self):
        exploratory = [h for h in BUYERBENCH_HYPOTHESES if h.analysis_type == "exploratory"]
        assert len(exploratory) == 6

    def test_analysis_type_default_is_exploratory(self):
        """HypothesisDef defaults to exploratory so old tests remain valid."""
        hyp = HypothesisDef(
            id="HC1",
            label="Custom",
            prq_dimension="D1",
            statement="Test.",
            direction="positive",
            test="t-test",
            null_outcome="No effect.",
            data_requirement="N=10",
        )
        assert hyp.analysis_type == "exploratory"

    def test_analysis_type_invalid_value_raises(self):
        with pytest.raises(Exception):
            HypothesisDef(
                id="HC1",
                label="Custom",
                prq_dimension="D1",
                statement="Test.",
                direction="positive",
                analysis_type="invalid",
                test="t-test",
                null_outcome="No effect.",
                data_requirement="N=10",
            )

    def test_markdown_shows_confirmatory_for_h1(self):
        doc = build_prereg_document(_make_manifest())
        md = render_prereg_markdown(doc)
        h1_section = md.split("6.H1")[1].split("6.H2")[0]
        assert "CONFIRMATORY" in h1_section

    def test_markdown_shows_exploratory_for_h2(self):
        doc = build_prereg_document(_make_manifest())
        md = render_prereg_markdown(doc)
        h2_section = md.split("6.H2")[1].split("6.H3")[0]
        assert "EXPLORATORY" in h2_section

    def test_markdown_section_56_lists_confirmatory_hypotheses(self):
        doc = build_prereg_document(_make_manifest())
        md = render_prereg_markdown(doc)
        assert "5.6 Confirmatory vs. Exploratory" in md
        section_56 = md.split("5.6 Confirmatory vs. Exploratory")[1].split("5.7")[0]
        for hid in ["H1", "H3", "H5", "H7"]:
            assert hid in section_56, f"{hid} not listed in section 5.6"

    def test_markdown_section_56_lists_exploratory_hypotheses(self):
        doc = build_prereg_document(_make_manifest())
        md = render_prereg_markdown(doc)
        section_56 = md.split("5.6 Confirmatory vs. Exploratory")[1].split("5.7")[0]
        for hid in ["H2", "H4", "H6", "H8", "H9", "H10"]:
            assert hid in section_56, f"{hid} not listed in section 5.6"

    def test_markdown_section_56_mentions_bh_fdr(self):
        doc = build_prereg_document(_make_manifest())
        md = render_prereg_markdown(doc)
        section_56 = md.split("5.6 Confirmatory vs. Exploratory")[1].split("5.7")[0]
        assert "BH-FDR" in section_56

    def test_json_metadata_contains_analysis_type(self, tmp_path):
        manifest = _make_manifest()
        doc, md = generate_prereg_document(manifest)
        write_prereg_document(doc, md, tmp_path)
        data = json.loads((tmp_path / "prereg_metadata.json").read_text())
        h1 = next(h for h in data["hypotheses"] if h["id"] == "H1")
        assert h1["analysis_type"] == "confirmatory"
        h2 = next(h for h in data["hypotheses"] if h["id"] == "H2")
        assert h2["analysis_type"] == "exploratory"
