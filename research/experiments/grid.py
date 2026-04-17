"""Experiment grid definition.

Defines the full factorial grid: models × biases × variants × configs.
Imported by ``research/scripts/00_define_experiment.py`` (orchestration) and
by the test suite.

Design tiers
------------
realistic
    10 models × 5 bias types × 2 variants × 1 temperature × 1 prompt version
    × 50 runs = 5,000 total runs.  Primary published experiment.
flagship
    Same models / biases, but 100 runs per cell, 2 temperatures (0.7 + 0.0),
    and 2 prompt versions (standard + cot) = 40,000 total runs.
pilot_full
    Same 10 real models as realistic, but N=30 per cell (3,000 total runs ≈ $450).
    Run before the full realistic design to detect ceiling effects and validate
    statistical power at reduced cost.  Section O.1 Day 9–10.
pilot
    1 mock agent × 5 runs per cell = 50 total runs (infrastructure validation only).
"""
from __future__ import annotations

# ── Realistic Design ──────────────────────────────────────────────────────────

REALISTIC_DESIGN: dict = {
    "design_tier": "realistic",
    "models": [
        "openrouter-openai-gpt-4o",
        "openrouter-anthropic-claude-3.5-sonnet",
        "openrouter-google-gemini-pro-1.5",
        "openrouter-meta-llama-llama-3.1-405b-instruct",
        "openrouter-mistralai-mistral-large",
        "openrouter-deepseek-deepseek-chat",
        "openrouter-qwen-qwen-2.5-72b-instruct",
        "openrouter-cohere-command-r-plus",
        "openrouter-mistralai-mixtral-8x22b-instruct",
        "openrouter-01-ai-yi-large",
    ],
    "bias_scenarios": {
        "anchoring": {
            "baseline": "p2-01-anchor-high-BASELINE",
            "treatment": "p2-01-anchor-high-ANCHOR_HIGH",
        },
        "framing": {
            # GAIN is the reference variant; LOSS is the treatment.
            "baseline": "p2-02-framing-GAIN",
            "treatment": "p2-02-framing-LOSS",
        },
        "decoy": {
            "baseline": "p2-03-decoy-BASELINE",
            "treatment": "p2-03-decoy-DECOY",
        },
        "scarcity": {
            "baseline": "p2-04-scarcity-BASELINE",
            "treatment": "p2-04-scarcity-SCARCITY",
        },
        "sunk_cost": {
            "baseline": "p2-05-sunk-cost-BASELINE",
            "treatment": "p2-05-sunk-cost-SUNK_COST",
        },
    },
    "n_runs_per_cell": 50,
    # Primary temperature.  Add 0.0 in the flagship design for robustness.
    "temperatures": [0.7],
    # CoT and expert_role prompt variants are added in the flagship design.
    "prompt_versions": ["standard"],
    # Approximate cost per invocation — actual cost varies by model family.
    "cost_per_run_usd": 0.15,
}

# ── Flagship Design (inherits all settings; overrides what changes) ───────────

FLAGSHIP_DESIGN: dict = {
    **REALISTIC_DESIGN,
    "design_tier": "flagship",
    "n_runs_per_cell": 100,
    "temperatures": [0.7, 0.0],
    "prompt_versions": ["standard", "cot"],
    "cost_per_run_usd": 0.20,
}

# ── Pilot Full Design (N=30 per cell; real models; ceiling-effect check) ──────

PILOT_FULL_DESIGN: dict = {
    **REALISTIC_DESIGN,
    "design_tier": "pilot_full",
    # N=30 gives enough power to detect a ceiling effect at lower cost (~$450)
    # while still allowing the Day 10 go/no-go gate decision before the full
    # N=50 realistic run (~$750).  Section O.1 Day 9–10.
    "n_runs_per_cell": 30,
    "cost_per_run_usd": 0.15,  # 10 × 5 × 2 × 30 = 3,000 runs ≈ $450
}

# ── Pilot Design (infrastructure verification — mock agent, N=5 per cell) ─────

PILOT_DESIGN: dict = {
    **REALISTIC_DESIGN,
    "design_tier": "pilot",
    # Single mock agent: always available, zero cost, validates full pipeline.
    "models": ["mock-agent-v1"],
    "n_runs_per_cell": 5,
    "temperatures": [0.7],
    "prompt_versions": ["standard"],
    "cost_per_run_usd": 0.00,
}

# ── Registry ──────────────────────────────────────────────────────────────────

DESIGNS: dict[str, dict] = {
    "realistic": REALISTIC_DESIGN,
    "flagship": FLAGSHIP_DESIGN,
    "pilot_full": PILOT_FULL_DESIGN,
    "pilot": PILOT_DESIGN,
}
