# META1.6 synthetic validation

Synthetic responses are generated from the exact nonempty AND dictionary with iid Gaussian noise. The primary estimator is Lasso with the frozen universal lambda; target signed F1 and exact target-sign recovery are measured.

A1–A8 are: uniform, D-opt, `hybrid_d50`, HILS, symmetric candidate, target-aware mean candidate, candidate omitting integrated singular loss, and the full candidate. DCD is separate. Full results are in `results/meta1_6/raw/synthetic_runs.csv` and aggregates in `results/meta1_6/aggregated/synthetic_summary.csv`.

The full candidate's cross-budget mean signed-F1 is lower than HILS by 0.0207 and lower than D-opt by a larger margin. This fails the synthetic superiority condition.
