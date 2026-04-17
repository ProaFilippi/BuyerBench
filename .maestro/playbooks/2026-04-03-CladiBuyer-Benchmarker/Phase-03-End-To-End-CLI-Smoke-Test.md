# Phase 03: Add End-to-End CLI Smoke Test

Unit tests cover individual components but nothing catches a regression where the CLI entry point itself breaks — a bad import, a missing scenario file, or a report rendering crash that only surfaces when all pieces run together. This phase adds an integration smoke test that invokes `python -m buyerbench demo` as a real subprocess, asserts a zero exit code, and checks for key output strings, giving confidence that the full demo pipeline is intact on every `pytest` run.

## Tasks

- [ ] Read existing test infrastructure to understand conventions before writing new tests:
  - Read `tests/test_demo.py` to see how demo-related tests are currently structured and what fixtures or helpers already exist
  - Read `tests/conftest.py` (if it exists) for shared fixtures
  - Check if there is a `pytest.ini`, `pyproject.toml [tool.pytest]`, or `setup.cfg` with test markers or timeout config
  - Note whether `subprocess` or `click.testing.CliRunner` is already used anywhere in the test suite

- [ ] Create `tests/test_smoke.py` with an end-to-end CLI smoke test:
  - Import `subprocess`, `sys`, and any needed stdlib modules only — no new test dependencies
  - Write a test `test_demo_e2e_smoke` that:
    - Invokes `[sys.executable, "-m", "buyerbench", "demo"]` via `subprocess.run()` with `capture_output=True`, `text=True`, and a generous `timeout=60`
    - Asserts `returncode == 0` (prints `result.stderr` in the assertion message for diagnostics)
    - Asserts that `result.stdout` contains the string `"scenarios evaluated"` (matches the fixed dynamic count from Phase 01)
    - Asserts that `result.stdout` contains at least one of: `"Pillar"`, `"Score"`, or `"mock-agent"` (confirms the results table rendered)
  - Mark the test with `@pytest.mark.slow` or `@pytest.mark.integration` so it can be excluded from fast unit test runs: `pytest -m "not integration"`
  - Add a module-level docstring explaining that this test launches a real subprocess and depends on scenario files being present

- [ ] Write a complementary smoke test for the `check` command:
  - In `tests/test_smoke.py`, add `test_check_command_smoke`:
    - Invokes `[sys.executable, "-m", "buyerbench", "check"]` with same subprocess approach
    - Asserts `returncode == 0`
    - Asserts stdout contains `"preflight"` or `"check"` (case-insensitive) confirming the check ran
  - This guards against import-time breakage in `harness/preflight.py`

- [ ] Run the smoke tests and the full suite, confirm everything passes:
  - Run: `pytest tests/test_smoke.py -v -s 2>&1`
  - Run: `pytest --tb=short -q 2>&1 | tail -10`
  - If the smoke test fails, read stdout/stderr from the subprocess result to diagnose (do NOT skip or mark `xfail` — fix the underlying issue)
  - Confirm the `integration` marker correctly excludes the slow tests: `pytest -m "not integration" -q 2>&1 | tail -5`
