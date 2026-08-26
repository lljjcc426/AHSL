# S1.0 classical baselines

## Implemented comparisons

On each of seven microbial focal landscapes, the 64 real cell means define an AND/Möbius design with all 64 coefficients. For budgets 16, 24, 32, and 48, five deterministic masks are sampled. Within each mask, 80% selects a hyperparameter and the full mask refits it.

- Lasso alpha grid: `1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2, 1e-1`; selected by validation response MSE.
- OMP sparsity grid: `2,4,8,12,16,24`; selected by validation response MSE.
- Weak-heredity lasso is an explicitly labeled diagnostic post-filter, not a claim to reproduce `hierNet`.
- Exact Möbius is the full-data contrast and operational truth construction.

All fits use fixed seed `20260827`; lasso uses cyclic coordinate descent with 20,000 iterations. The real-data run converged. The tiny degenerate unit test emits two sklearn convergence warnings because its objective and tolerance are exactly zero; this does not affect the real fits.

## Budget 48 results

| Method | Precision | Recall | F1 | AP | Pure-HOI recall | Response RMSE |
|---|---:|---:|---:|---:|---:|---:|
| lasso | 0.387 | 0.204 | **0.235** | 0.506 | **0.425** | **0.102** |
| OMP / greedy CS | 0.141 | 0.030 | 0.047 | 0.479 | 0.050 | 0.115 |
| weak-heredity lasso diagnostic | 0.366 | 0.189 | 0.218 | **0.509** | 0.350 | 0.103 |

Full exact Möbius has F1 1 by construction and response RMSE 0; its coefficient-magnitude AP is 0.921 because bootstrap significance is not a monotone function of point magnitude.

## Methods inspected but not forced onto incompatible settings

- OLS is underdetermined whenever budget is below 64 and equals exact inversion at the full square design.
- `hierNet`, glinternet, FAMILY, and RAMP primarily target pairwise/quadratic interactions and hierarchy. Forcing them to all orders 3--6 on seven `p=6` landscapes would not be a faithful published reproduction. The weak-heredity filter quantifies the relevant structural assumption without mislabeling it.
- Group lasso lacks a scientifically justified grouping here; arbitrary grouping would manufacture an advantage or disadvantage.
- Yeast query-rate is a design-confounding diagnostic, not a serious competitor to Dango. Random split F1/AP are 0.167/0.147; query-pair-disjoint F1 is 0 and AP equals prevalence 0.0535.
- Drug data were not fit because a fixed set-level label failed the context audit; fitting first would optimize an invalid target.

## Ranking distinction

Response RMSE and support F1 do not give identical scientific conclusions. At budget 48, lasso has the best RMSE and F1, but weak-heredity lasso has slightly higher AP. More importantly, RMSE around 0.10 coexists with support recall near 0.20. Response prediction therefore understates structural failure.
