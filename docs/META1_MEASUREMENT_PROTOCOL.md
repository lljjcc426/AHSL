# META1 partial-measurement protocol

The budget unit is the number of distinct communities revealed. Selecting a community exposes all of its available biological replicates; replicate count is not separately optimized in v1.

| Full cells | fractions | budgets |
|---:|---|---|
| 64 (each Ishizawa landscape) | 25%, 37.5%, 50%, 75% | 16, 24, 32, 48 |
| 256 (Díaz-Colunga) | 25%, 37.5%, 50%, 75% | 64, 96, 128, 192 |

Non-adaptive masks use Development seeds 101, 202, 303, and 404. Seeds 505 and 606 are generated and stored as a Confirmation reserve but were not used for fitting, policy selection, regime selection, or the META1 decision. The empty/reference cell is always included. Masks are deterministic and shared across competing uniform-sampling methods.

The estimator receives a `RevealedPanel` containing selected bitmasks, selected responses, and replicate statistics derived only from those responses. `EvaluationOracle` alone retains complete responses and reference coefficients. Acquisition policies may use the factorial design and previously revealed data; they cannot accept the oracle or inspect hidden responses.

The design-aware policies are fixed-budget selections on the column-scaled AND matrix. `d_optimal_rows` greedily pivots toward informative rows. Hybrid policies allocate 25%, 50%, or 75% of the budget to this deterministic design component and fill the remainder uniformly from the same seed. `row_cosine_v0` is retained as a failed early design rule because it increased rather than reduced problematic aliases.

Held-out response RMSE is calculated only on unmeasured communities. All support metrics use the complete-panel reference only after fitting. The full ledger in `results/meta1/raw/experiments.csv` records mask seed and acquisition policy per run.
