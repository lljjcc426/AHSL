# META1.6 real Development results

The real audit uses the seven Ishizawa focal-strain landscapes, frozen log10 response, budgets 16/24/32, and Development seeds 101/202/303/404. The reference signed support is the pre-existing META1 full-panel CI/practical-effect estimand. It is used only after Pi and row objectives are frozen.

The primary comparison uses Lasso and landscape-macro signed high-order F1. HILS and the full candidate also receive an ElasticNet transfer check. Raw paired results are in `results/meta1_6/raw/real_development_runs.csv`; macro summaries are in `results/meta1_6/aggregated/real_summary.csv`.

Across budgets, the full candidate trails HILS by 0.0394 signed-F1 on average. Precision/FDR, recall, sign flips, and hidden-response RMSE do not supply a compensating guardrail victory. Therefore the data do not support continuation of the modified design direction.
