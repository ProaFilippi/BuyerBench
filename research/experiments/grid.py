"""Experiment grid definition.

Defines the full factorial grid: models × biases × variants × configs.
Imported by ``research/scripts/00_define_experiment.py`` (orchestration) and
by the test suite.

Design tiers
------------
realistic
    10 models × 5 bias types × 2 variants × 1 temperature × 1 prompt version
    × 50 runs = 5,000 total runs.  Primary published experiment.
robustness_t0
    Same 10 models / biases as realistic, but temperature=0.0 (deterministic)
    and N=30 per cell (3,000 total runs ≈ $450).  Section O.2 Week 3.
    Run after Gate 1 clears to verify that BSI results are not stochastic
    artifacts of temperature=0.7 sampling.
cot_experiment
    UPGRADE-7: 10 models × 5 bias types × 2 variants × 3 prompt versions
    (standard, cot, expert_role) × 15 runs per cell = 4,500 total runs ≈ $675.
    Section O.2 Week 4.  Tests whether chain-of-thought and expert-role framing
    modulates BSI relative to the standard prompt.
flagship
    UPGRADE-8/9/10 expansion: 10 models × 8 bias types × 100 runs per cell ×
    2 temperatures (0.7 + 0.0) × 2 prompt versions (standard + cot).
    Bias types: anchoring, framing, decoy, scarcity, sunk_cost (realistic 5),
    plus default (p2-06), loss_aversion (p2-07), and warp (p2-08, triplet).
    WARP has 3 scenario slots (warp_ab, warp_bc, warp_ac); all others have 2.
    Total scenario slots = 5×2 + 2 + 2 + 3 = 17.
    Total runs = 10 × 17 × 2 × 2 × 100 = 68,000.
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

# ── Robustness T=0.0 Design (deterministic; N=30 per cell) ───────────────────

ROBUSTNESS_T0_DESIGN: dict = {
    **REALISTIC_DESIGN,
    "design_tier": "robustness_t0",
    # Deterministic temperature.  N=30 per cell is sufficient to detect
    # supplier-order effects while keeping cost ≈ $450.  Section O.2 Week 3.
    "n_runs_per_cell": 30,
    "temperatures": [0.0],
    "cost_per_run_usd": 0.15,  # 10 × 5 × 2 × 30 = 3,000 runs ≈ $450
}

# ── CoT Experiment Design (UPGRADE-7; N=15 per cell; 3 prompt versions) ───────

COT_EXPERIMENT_DESIGN: dict = {
    **REALISTIC_DESIGN,
    "design_tier": "cot_experiment",
    # UPGRADE-7: tests standard vs. cot vs. expert_role prompt framing.
    # N=15 per cell → 10 × 5 × 2 × 3 × 15 = 4,500 runs ≈ $675.
    # N=15 balances statistical power with cost given 3-way comparison.
    "n_runs_per_cell": 15,
    "temperatures": [0.7],
    "prompt_versions": ["standard", "cot", "expert_role"],
    "cost_per_run_usd": 0.15,  # 10 × 5 × 2 × 3 × 15 = 4,500 runs ≈ $675
}

# ── Flagship Bias Battery (UPGRADE-8/9/10 — 8 bias types) ────────────────────
#
# Realistic uses 5 standard pairs.  Flagship extends to 8:
#   - p2-06-default     (UPGRADE-8): status-quo / default bias
#   - p2-07-loss-aversion (UPGRADE-9): loss-aversion switching cost
#   - p2-08-warp          (UPGRADE-10): WARP transitivity battery (triplet)
#
# WARP is a triplet of pairwise binary choices (A vs B, B vs C, A vs C).
# All three run as independent scenarios; compute_warp_transitivity() in
# evaluators/pillar2.py performs the post-hoc transitivity check.

FLAGSHIP_8_BIAS_SCENARIOS: dict = {
    # ── Original 5 (Realistic Design) ────────────────────────────────────────
    "anchoring": {
        "baseline": "p2-01-anchor-high-BASELINE",
        "treatment": "p2-01-anchor-high-ANCHOR_HIGH",
    },
    "framing": {
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
    # ── UPGRADE-8: Default / Status-Quo Bias (p2-06) ─────────────────────────
    "default": {
        "baseline": "p2-06-default-BASELINE",
        "treatment": "p2-06-default-DEFAULT",
    },
    # ── UPGRADE-9: Loss Aversion / Switching Cost (p2-07) ────────────────────
    "loss_aversion": {
        "baseline": "p2-07-loss-aversion-BASELINE",
        "treatment": "p2-07-loss-aversion-LOSS_AVERSION",
    },
    # ── UPGRADE-10: WARP Transitivity Battery (p2-08, triplet) ───────────────
    # Three pairwise binary choices: AB, BC, AC.  No baseline/treatment framing
    # — all three are run as independent scenarios for post-hoc WARP analysis.
    "warp": {
        "warp_ab": "p2-08-warp-WARP_AB",
        "warp_bc": "p2-08-warp-WARP_BC",
        "warp_ac": "p2-08-warp-WARP_AC",
    },
}

# ── Flagship Design (UPGRADE-8/9/10: 8 bias types, N=100, T∈{0.7,0.0}) ──────

FLAGSHIP_DESIGN: dict = {
    **REALISTIC_DESIGN,
    "design_tier": "flagship",
    "bias_scenarios": FLAGSHIP_8_BIAS_SCENARIOS,
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
    "robustness_t0": ROBUSTNESS_T0_DESIGN,
    "cot_experiment": COT_EXPERIMENT_DESIGN,
    "flagship": FLAGSHIP_DESIGN,
    "pilot_full": PILOT_FULL_DESIGN,
    "pilot": PILOT_DESIGN,
}
