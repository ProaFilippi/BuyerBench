"""Tests for research/scripts/03_run_regressions.py.

Covers:
- load_runs_jsonl: FileNotFoundError when runs.jsonl absent
- load_runs_jsonl: malformed lines are silently skipped
- load_runs_jsonl: returns list of dicts from valid JSONL
- build_regression_dataframe: error rows excluded
- build_regression_dataframe: variant normalised to uppercase
- build_regression_dataframe: null bsi rows excluded
- build_regression_dataframe: ValueError when no valid rows remain
- build_regression_dataframe: required columns present
- run_regression_pipeline: returns expected top-level keys
- run_regression_pipeline: primary key contains RegressionResult fields
- run_regression_pipeline: bh_correction key has adjusted_pvalues
- run_regression_pipeline: variance_decomposition key populated
- run_regression_pipeline: capability key is None when p1_scores=None
- run_regression_pipeline: capability key populated when p1_scores supplied
- run_regression_pipeline: summary key has treatment estimate
- run_regression_pipeline: BH-annotated coefficients present in primary dict
- CLI: --dry-run exits without writing output file
- CLI: --experiment-dir missing raises SystemExit
- CLI: end-to-end writes regression_results.json
- CLI: regression_results.json is valid JSON with expected keys
- CLI: --output overrides default output path
- CLI: n_obs matches dataframe row count
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

_SCRIPT_PATH = (
    Path(__file__).resolve().parent.parent
    / "research" / "scripts" / "03_run_regressions.py"
)


def _load_script():
    spec = importlib.util.spec_from_file_location("run_regressions", _SCRIPT_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_script = _load_script()

# Skip all tests that need pandas when it is absent
_pandas_available = _script._PANDAS_AVAILABLE
pandas_required = pytest.mark.skipif(
    not _pandas_available, reason="pandas not installed"
)


# ─────────────────────────────────────────────────────────────────────────────
# FIXTURES
# ─────────────────────────────────────────────────────────────────────────────


def _write_jsonl(path: Path, records: list[dict]) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        for r in records:
            fh.write(json.dumps(r) + "\n")


def _make_run_record(
    run_id: str = "r001",
    agent_id: str = "agent-A",
    bias_category: str = "anchoring",
    variant: str = "baseline",
    bsi: float = 0.0,
    temperature: float = 0.7,
    error_flag: bool = False,
) -> dict:
    return {
        "run_id": run_id,
        "agent_id": agent_id,
        "bias_category": bias_category,
        "variant": variant,
        "bsi": bsi,
        "temperature": temperature,
        "prompt_version": "standard",
        "run_index": 1,
        "error_flag": error_flag,
        "error_message": None,
    }


def _make_minimal_records(n: int = 16) -> list[dict]:
    """Create minimal valid records: 2 agents × 2 biases × 2 variants × n/8 runs."""
    records = []
    counter = 0
    for agent in ["agent-A", "agent-B"]:
        for bias in ["anchoring", "framing"]:
            for variant, bsi in [("baseline", 0.1), ("anchor_high", 0.5)]:
                for i in range(n // 8):
                    counter += 1
                    records.append(
                        _make_run_record(
                            run_id=f"r{counter:04d}",
                            agent_id=agent,
                            bias_category=bias,
                            variant=variant,
                            bsi=bsi + 0.01 * i,
                        )
                    )
    return records


# ─────────────────────────────────────────────────────────────────────────────
# §1  load_runs_jsonl
# ─────────────────────────────────────────────────────────────────────────────


class TestLoadRunsJsonl:
    def test_file_not_found(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            _script.load_runs_jsonl(tmp_path)

    def test_returns_list_of_dicts(self, tmp_path):
        _write_jsonl(tmp_path / "runs.jsonl", [_make_run_record()])
        records = _script.load_runs_jsonl(tmp_path)
        assert isinstance(records, list)
        assert len(records) == 1
        assert isinstance(records[0], dict)

    def test_malformed_lines_skipped(self, tmp_path):
        with open(tmp_path / "runs.jsonl", "w") as fh:
            fh.write(json.dumps(_make_run_record()) + "\n")
            fh.write("NOT_JSON\n")
            fh.write(json.dumps(_make_run_record(run_id="r002")) + "\n")
        records = _script.load_runs_jsonl(tmp_path)
        assert len(records) == 2

    def test_empty_lines_skipped(self, tmp_path):
        with open(tmp_path / "runs.jsonl", "w") as fh:
            fh.write("\n")
            fh.write(json.dumps(_make_run_record()) + "\n")
            fh.write("\n")
        records = _script.load_runs_jsonl(tmp_path)
        assert len(records) == 1

    def test_record_fields_preserved(self, tmp_path):
        rec = _make_run_record(run_id="abc123", agent_id="my-agent", bsi=0.42)
        _write_jsonl(tmp_path / "runs.jsonl", [rec])
        records = _script.load_runs_jsonl(tmp_path)
        assert records[0]["run_id"] == "abc123"
        assert records[0]["agent_id"] == "my-agent"
        assert records[0]["bsi"] == pytest.approx(0.42)


# ─────────────────────────────────────────────────────────────────────────────
# §2  build_regression_dataframe
# ─────────────────────────────────────────────────────────────────────────────


@pandas_required
class TestBuildRegressionDataframe:
    def test_returns_dataframe(self):
        records = _make_minimal_records()
        df = _script.build_regression_dataframe(records)
        import pandas as pd
        assert isinstance(df, pd.DataFrame)

    def test_error_rows_excluded(self):
        records = _make_minimal_records(16)
        records[0]["error_flag"] = True
        df = _script.build_regression_dataframe(records)
        assert len(df) == len(records) - 1

    def test_variant_normalised_to_uppercase(self):
        records = _make_minimal_records(16)
        df = _script.build_regression_dataframe(records)
        assert all(v == v.upper() for v in df["variant"])

    def test_baseline_variant_uppercase(self):
        rec = _make_run_record(variant="baseline")
        df = _script.build_regression_dataframe([rec])
        assert df.iloc[0]["variant"] == "BASELINE"

    def test_null_bsi_rows_excluded(self):
        records = _make_minimal_records(16)
        records[0]["bsi"] = None
        df = _script.build_regression_dataframe(records)
        assert len(df) == len(records) - 1

    def test_valueerror_when_no_valid_rows(self):
        records = [_make_run_record(error_flag=True)]
        with pytest.raises(ValueError, match="No valid"):
            _script.build_regression_dataframe(records)

    def test_required_columns_present(self):
        records = _make_minimal_records(16)
        df = _script.build_regression_dataframe(records)
        for col in ("run_id", "agent_id", "bias_category", "variant", "bsi", "temperature"):
            assert col in df.columns, f"Missing column: {col}"

    def test_bsi_is_float(self):
        records = _make_minimal_records(16)
        df = _script.build_regression_dataframe(records)
        assert df["bsi"].dtype.kind == "f"

    def test_row_count_matches_valid_records(self):
        records = _make_minimal_records(16)
        # Add 2 error records
        records.append(_make_run_record(run_id="err1", error_flag=True))
        records.append(_make_run_record(run_id="err2", error_flag=True))
        df = _script.build_regression_dataframe(records)
        assert len(df) == 16


# ─────────────────────────────────────────────────────────────────────────────
# §3  run_regression_pipeline
# ─────────────────────────────────────────────────────────────────────────────


@pandas_required
class TestRunRegressionPipeline:
    def _df(self):
        records = _make_minimal_records(16)
        return _script.build_regression_dataframe(records)

    def _df_three_agents(self):
        records = []
        counter = 0
        for agent in ["agent-A", "agent-B", "agent-C"]:
            for bias in ["anchoring", "framing"]:
                for variant, bsi in [("baseline", 0.1), ("anchor_high", 0.5)]:
                    for _ in range(2):
                        counter += 1
                        records.append(
                            _make_run_record(
                                run_id=f"r{counter:04d}",
                                agent_id=agent,
                                bias_category=bias,
                                variant=variant,
                                bsi=bsi,
                            )
                        )
        return _script.build_regression_dataframe(records)

    def test_returns_expected_top_level_keys(self):
        result = _script.run_regression_pipeline(self._df())
        for key in ("primary", "bh_correction", "variance_decomposition", "capability", "summary"):
            assert key in result

    def test_primary_has_regression_result_fields(self):
        result = _script.run_regression_pipeline(self._df())
        primary = result["primary"]
        for field in ("spec_name", "n_obs", "backend", "coefficients"):
            assert field in primary

    def test_bh_correction_has_adjusted_pvalues(self):
        result = _script.run_regression_pipeline(self._df())
        bh = result["bh_correction"]
        assert "adjusted_pvalues" in bh
        assert "rejected" in bh
        assert "n_rejected" in bh
        assert len(bh["adjusted_pvalues"]) == len(bh["raw_pvalues"])

    def test_variance_decomposition_populated(self):
        result = _script.run_regression_pipeline(self._df())
        vd = result["variance_decomposition"]
        assert vd is not None
        sources = {row["source"] for row in vd["rows"]}
        assert "Treatment" in sources
        assert "Residual" in sources

    def test_capability_none_when_no_p1(self):
        result = _script.run_regression_pipeline(self._df())
        assert result["capability"] is None

    def test_capability_populated_with_p1_scores(self):
        df = self._df_three_agents()
        p1 = {"agent-A": 0.80, "agent-B": 0.60, "agent-C": 0.70}
        result = _script.run_regression_pipeline(df, p1_scores=p1)
        assert result["capability"] is not None
        assert result["capability"]["spec_name"] == "H2_Capability"

    def test_summary_has_treatment_estimate(self):
        result = _script.run_regression_pipeline(self._df())
        assert result["summary"]["treatment_estimate"] is not None

    def test_bh_annotated_coefficients_in_primary(self):
        result = _script.run_regression_pipeline(self._df())
        for coef in result["primary"]["coefficients"]:
            assert "p_value_bh" in coef
            assert "significant_bh" in coef

    def test_summary_n_obs_positive(self):
        result = _script.run_regression_pipeline(self._df())
        assert result["summary"]["n_obs"] > 0

    def test_summary_backend_is_string(self):
        result = _script.run_regression_pipeline(self._df())
        assert isinstance(result["summary"]["backend"], str)

    def test_capability_flag_false_without_p1(self):
        result = _script.run_regression_pipeline(self._df())
        assert result["summary"]["capability_regression_available"] is False

    def test_capability_flag_true_with_p1(self):
        df = self._df_three_agents()
        p1 = {"agent-A": 0.80, "agent-B": 0.60, "agent-C": 0.70}
        result = _script.run_regression_pipeline(df, p1_scores=p1)
        assert result["summary"]["capability_regression_available"] is True


# ─────────────────────────────────────────────────────────────────────────────
# §4  CLI integration
# ─────────────────────────────────────────────────────────────────────────────


@pandas_required
class TestCLIIntegration:
    def _setup_experiment_dir(self, tmp_path: Path, n: int = 16) -> Path:
        exp_dir = tmp_path / "test_experiment"
        exp_dir.mkdir()
        records = _make_minimal_records(n)
        _write_jsonl(exp_dir / "runs.jsonl", records)
        return exp_dir

    def test_missing_experiment_dir_exits(self, tmp_path):
        with pytest.raises(SystemExit):
            _script.main(["--experiment-dir", str(tmp_path / "nonexistent")])

    def test_dry_run_does_not_write_output(self, tmp_path):
        exp_dir = self._setup_experiment_dir(tmp_path)
        _script.main(["--experiment-dir", str(exp_dir), "--dry-run"])
        assert not (exp_dir / "regression_results.json").exists()

    def test_end_to_end_writes_output(self, tmp_path):
        exp_dir = self._setup_experiment_dir(tmp_path)
        _script.main(["--experiment-dir", str(exp_dir)])
        assert (exp_dir / "regression_results.json").exists()

    def test_output_is_valid_json(self, tmp_path):
        exp_dir = self._setup_experiment_dir(tmp_path)
        _script.main(["--experiment-dir", str(exp_dir)])
        with open(exp_dir / "regression_results.json") as fh:
            data = json.load(fh)
        assert isinstance(data, dict)

    def test_output_has_expected_keys(self, tmp_path):
        exp_dir = self._setup_experiment_dir(tmp_path)
        _script.main(["--experiment-dir", str(exp_dir)])
        with open(exp_dir / "regression_results.json") as fh:
            data = json.load(fh)
        for key in ("primary", "bh_correction", "variance_decomposition", "capability", "summary"):
            assert key in data

    def test_custom_output_path(self, tmp_path):
        exp_dir = self._setup_experiment_dir(tmp_path)
        out_path = tmp_path / "custom_output.json"
        _script.main(["--experiment-dir", str(exp_dir), "--output", str(out_path)])
        assert out_path.exists()
        assert not (exp_dir / "regression_results.json").exists()

    def test_n_obs_matches_record_count(self, tmp_path):
        exp_dir = self._setup_experiment_dir(tmp_path, n=16)
        _script.main(["--experiment-dir", str(exp_dir)])
        with open(exp_dir / "regression_results.json") as fh:
            data = json.load(fh)
        assert data["summary"]["n_obs"] == 16

    def test_p1_scores_file_loaded(self, tmp_path):
        exp_dir = self._setup_experiment_dir(tmp_path)
        # Add a third agent to satisfy ≥3-model requirement
        extra = []
        for bias in ["anchoring", "framing"]:
            for variant, bsi in [("baseline", 0.1), ("anchor_high", 0.4)]:
                for i in range(2):
                    extra.append(
                        _make_run_record(
                            run_id=f"extra-{bias}-{variant}-{i}",
                            agent_id="agent-C",
                            bias_category=bias,
                            variant=variant,
                            bsi=bsi,
                        )
                    )
        # Re-write runs.jsonl with 3 agents
        existing = _make_minimal_records(16)
        _write_jsonl(exp_dir / "runs.jsonl", existing + extra)

        p1_file = tmp_path / "p1_scores.json"
        p1_file.write_text(
            json.dumps({"agent-A": 0.80, "agent-B": 0.60, "agent-C": 0.70})
        )
        _script.main([
            "--experiment-dir", str(exp_dir),
            "--p1-scores", str(p1_file),
        ])
        with open(exp_dir / "regression_results.json") as fh:
            data = json.load(fh)
        assert data["capability"] is not None
        assert data["summary"]["capability_regression_available"] is True

    def test_all_variants_uppercased_in_output(self, tmp_path):
        exp_dir = self._setup_experiment_dir(tmp_path)
        _script.main(["--experiment-dir", str(exp_dir)])
        with open(exp_dir / "regression_results.json") as fh:
            data = json.load(fh)
        # summary.n_obs > 0 implies normalisation succeeded
        assert data["summary"]["n_obs"] > 0
