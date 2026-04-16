"""Mixed-effects regression wrappers.

Primary models:
  - run_primary_regression(df): BSI ~ BiasType + Model + Treatment + BiasType×Model + (1|run)
  - run_capability_regression(cell_df, p1_scores): OLS mean_BSI ~ P1Score (descriptive, N=10)
  - run_variance_decomposition(df): ANOVA-style SS partition
  - apply_bh_correction(pvalues, alpha): Benjamini-Hochberg FDR correction

Backend: statsmodels.formula.api.mixedlm; optional rpy2 bridge for lme4.
"""
# TODO: Implement regression templates (see PILLAR2-RESEARCH-06 Section L.6 for spec).
