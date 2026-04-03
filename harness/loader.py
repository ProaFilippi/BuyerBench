from __future__ import annotations

import os
from pathlib import Path

import yaml

from buyerbench.models import Scenario


def load_scenario(path: str) -> Scenario:
    """Load and validate a single scenario from a YAML file."""
    with open(path, "r") as f:
        data = yaml.safe_load(f)
    return Scenario.model_validate(data)


def load_all_scenarios(root: str) -> list[Scenario]:
    """Walk the scenarios/ directory tree and load every YAML file found."""
    scenarios = []
    root_path = Path(root)
    for yaml_file in sorted(root_path.rglob("*.yaml")):
        scenarios.append(load_scenario(str(yaml_file)))
    return scenarios
