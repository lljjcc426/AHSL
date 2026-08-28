# META1 method-development log

| Stage | Change | Result | Disposition |
|---|---|---|---|
| Reference | replicate bootstrap + practical threshold | stable enough for Development; Díaz scale/rule sensitivity remains | frozen as R1 |
| Baselines | tuned Lasso, Elastic Net, OMP, heredity, stability, IHT, lower-order, ARD | Elastic Net strongest broad F1; ARD strong at Díaz high budget | retained |
| P1 | revealed-replicate inverse-variance weighting | vs Lasso: Ishizawa +0.0592 F1, Díaz +0.0058; vs Elastic Net: -0.0187 and -0.0126 | no standalone promotion |
| P2 | stability/FDR threshold 0.9 | reduces discoveries/FDR mainly by abstention; F1 and recall collapse | failed mechanism |
| P3 | order-dependent penalty without heredity | vs Lasso: Ishizawa -0.0004, Díaz +0.0224; vs Elastic Net: -0.0783, +0.0039 | no promotion |
| Combined v1 | weighted + order penalty | does not beat Elastic Net | retained, not promoted |
| Acquisition v0 | row-cosine heuristic | increases exact aliasing in important regimes | retained as failed v0 |
| Acquisition v1 | fully D-optimal/pivoted rows | Ishizawa F1 +0.0409, but response RMSE worsens about 32%; Díaz loses sharply | guardrail failure |
| Hybrid search | D-opt fractions 0.25/0.50/0.75 + uniform fill | 0.50 gives the best Ishizawa low-budget Pareto result | Development candidate |

P1's gain has essentially no association with replicate SNR (Spearman rho 0.002, p=0.987), so the evidence does not support the intended heteroscedastic-noise mechanism. Its benefit over Lasso is more plausibly attributable to additional Elastic Net flexibility/regularization.

All 3,200 experiment rows and 51,168 condition-specific tuning evaluations are retained. No losing method row was deleted. Some Elastic Net candidate convergence warnings occurred during search; selected runs completed and the warnings are not interpreted as scientific evidence.

The final ledger records 213.19 seconds of cumulative per-method runtime, 0 GPU hours, and a 268.59 MiB peak process working set during staged regeneration. The method-runtime sum is not an end-to-end wall-clock measurement.
