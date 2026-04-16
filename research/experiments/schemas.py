"""Research-specific data schemas.

Primary unit of observation: RunRecord (one LLM invocation).
Aggregation unit: CellAggregate (one model × scenario × variant × prompt × temp cell).
Experiment configuration: ExperimentManifest (frozen at run start).
"""
# TODO: Implement dataclasses (see PILLAR2-RESEARCH-06 Section L.2 for full spec).
