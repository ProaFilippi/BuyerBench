# Phase 01: Fix Demo Bugs and utcnow Deprecations

This phase clears all known defects identified in the initial code review: a demo command that hardcodes "3 scenarios evaluated" regardless of how many actually ran, a wasteful double-invoke of the agent per scenario, and eight `datetime.utcnow()` call sites that produce DeprecationWarnings in Python 3.12+. These are all low-risk, surgical fixes that leave the test suite green and eliminate 611 warnings.

## Tasks

- [x] Fix `datetime.utcnow()` deprecation in `buyerbench/models.py` and `buyerbench/__main__.py`:
  - In `models.py`: change `default_factory=datetime.utcnow` → `default_factory=lambda: datetime.now(timezone.utc)` (add `timezone` to the `datetime` import)
  - In `__main__.py` line ~484 inside `_write_skipped_results()`: change `datetime.utcnow().isoformat()` → `datetime.now(timezone.utc).isoformat()` (update import as needed)

- [x] Fix `datetime.utcnow()` deprecation in `results/schemas.py` and `results/report.py`:
  - In `schemas.py` lines ~24 and ~57: update both `default_factory=datetime.utcnow` → `default_factory=lambda: datetime.now(timezone.utc)` (add `timezone` to import)
  - In `report.py` lines ~28, ~80, and ~239: replace all three `datetime.utcnow()` calls with `datetime.now(timezone.utc)` (update import)

- [x] Fix `datetime.utcnow()` deprecation in `evaluators/aggregate.py`:
  - Lines ~229 and ~355: replace both `datetime.utcnow()` calls with `datetime.now(timezone.utc)` (update import)

- [x] Fix the demo command double-invoke and hardcoded scenario count in `buyerbench/__main__.py`:
  - Locate the demo scenario loop — find where `agent.respond(scenario)` is called twice and refactor to call it once, storing the result in a variable reused for both display and evaluation
  - Fix the hardcoded `"3 scenarios evaluated"` string — replace with `f"{len(scenarios)} scenarios evaluated"` (or equivalent dynamic count derived from the actual loop)

- [x] Run the full test suite and confirm all tests pass with zero utcnow DeprecationWarnings:
  - Run: `pytest --tb=short -q 2>&1 | head -60`
  - Run: `python -W error::DeprecationWarning -m pytest tests/ -q 2>&1 | tail -20` to confirm warnings are gone
  - If any test fails, read the failure message, identify the root cause, and fix it before marking this task done
