"""
Script 03: Run Regressions
============================
Loads cells.json and runs the full regression pipeline:
  - Primary mixed-effects model (BSI ~ BiasType + Model + Treatment + BiasType×Model + (1|run))
  - Capability OLS (mean_BSI ~ P1Score)
  - Variance decomposition ANOVA
  - BH-FDR correction on all p-values

Run: python research/scripts/03_run_regressions.py --experiment-dir results/experiments/pillar2/<id>
"""
# TODO: Implement regression pipeline.
