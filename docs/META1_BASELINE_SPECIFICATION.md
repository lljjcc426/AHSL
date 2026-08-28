# META1 baseline specification

All baselines operate in the same AND/Möbius design and receive identical revealed communities for uniform comparisons. Hyperparameters are selected by revealed-response validation, BIC-like criteria, or revealed-data stability; complete-panel support is never a tuning label.

| Family | Role | Selection/tuning principle |
|---|---|---|
| Lasso | historical sparse prediction baseline | revealed-response validation over alpha |
| Elastic Net | strong correlated-design baseline | revealed-response validation over alpha and l1 ratio |
| OMP | greedy support baseline | revealed-response validation over sparsity |
| weak/strong heredity | structural baselines | parent-closure constraints plus revealed-response selection |
| stability selection | resampled sparse support | BIC-selected or fixed inclusion thresholds 0.6/0.9 |
| sparse Möbius IHT | feasible noisy AND-basis/ASMT-style comparator | bounded sparsity and validation/BIC search |
| lower-order response | mismatch diagnostic | interactions of order at most two; cannot recover primary HOI support |
| ARD support | direct sparse Bayesian support baseline | evidence-driven relevance pruning, no oracle support labels |

Fourteen uniform method families were evaluated: the eight families above with heredity/stability variants, plus P1 noise weighting, P2 FDR filtering, P3 order penalty, and a justified combined v1. The ledger retains 51,168 tuning-trial evaluations across conditions. This number counts condition-specific evaluations, not 51,168 distinct hyperparameter tuples.

Elastic Net is the strongest broad primary baseline. Its uniform panel means are:

| Panel | signed F1 | precision | recall | AP | FDR | response RMSE |
|---|---:|---:|---:|---:|---:|---:|
| Ishizawa | 0.2356 | 0.2620 | 0.2713 | 0.5017 | 0.7380 | 0.1916 |
| Díaz-Colunga | 0.0490 | 0.0524 | 0.0580 | 0.1815 | 0.9476 | 0.1277 |

ARD is an important counterexample to a lasso-only story. Its Díaz mean F1 is 0.0788, and at budget 192 it reaches F1 0.2248, precision 0.7713, FDR 0.2288, and response RMSE 0.0959. It does not close the low-budget Ishizawa design-aware gain, but it materially narrows the claim space.
