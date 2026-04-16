"""Run orchestration.

Accepts an ExperimentManifest, expands the run plan, and invokes the
BuyerBench runner for each (model, scenario, variant, run_index, temperature,
prompt_version, seed) cell.  Writes RunRecords to a JSONL file in real time.

Supports:
  --dry-run   Print plan + cost estimate without invoking any models.
  --resume    Skip cells whose run_id already appears in the output JSONL.
"""
# TODO: Implement orchestration loop (see PILLAR2-RESEARCH-06 Section L.3 for spec).
