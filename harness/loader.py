from __future__ import annotations

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


def load_scenario_pairs(root: str) -> list[tuple[Scenario, Scenario]]:
    """Return paired scenarios grouped by variant_pair_id.

    Each returned tuple contains exactly two Scenario objects that share the
    same variant_pair_id.  Groups with fewer or more than two members are
    silently skipped so callers can rely on the two-element tuple type.
    """
    scenarios = load_all_scenarios(root)
    groups: dict[str, list[Scenario]] = {}
    for scenario in scenarios:
        if scenario.variant_pair_id:
            groups.setdefault(scenario.variant_pair_id, []).append(scenario)
    return [(members[0], members[1]) for members in groups.values() if len(members) == 2]


def load_scenario_triplets(root: str) -> list[tuple[Scenario, Scenario, Scenario]]:
    """Return triplets of scenarios grouped by variant_pair_id.

    Each returned tuple contains exactly three Scenario objects that share
    the same variant_pair_id, sorted by variant value for consistent ordering
    (WARP_AB, WARP_AC, WARP_BC alphabetically).  Groups with fewer or more
    than three members are silently skipped.
    """
    scenarios = load_all_scenarios(root)
    groups: dict[str, list[Scenario]] = {}
    for scenario in scenarios:
        if scenario.variant_pair_id:
            groups.setdefault(scenario.variant_pair_id, []).append(scenario)
    result = []
    for members in groups.values():
        if len(members) == 3:
            ordered = sorted(members, key=lambda s: s.variant.value)
            result.append((ordered[0], ordered[1], ordered[2]))
    return result
