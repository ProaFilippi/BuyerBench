"""Experiment manifest generation and freezing.

An ExperimentManifest is created once at run start, frozen to disk as
manifest.json, and never mutated — ensuring full reproducibility.
"""
# TODO: Implement manifest creation and persistence (see schemas.py for the
# ExperimentManifest dataclass and PILLAR2-RESEARCH-06 Section L.4 for spec).
