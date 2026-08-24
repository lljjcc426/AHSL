# A1 Audit Notes

## Frozen base

- Parent commit: `e6cc495fbc0e3e2b594cec514edb1da97145f6bc`.
- Branch: `phase-a1-marginal-likelihood-latent-tree`.
- A0, A0.5, and A0.75 source results are treated as historical and are not
  modified by A1.

## Pre-implementation decisions

- Literature Gate: `MODIFY`.
- The anchor process is documented as a uniformly rooted, size-biased bond-
  percolation cluster.
- The message algorithm is documented as specialized tree sum-product.
- "Join-tree recovery" is not used as the primary scientific target.
- Direct observed-likelihood local search is preferred over literal Structural
  EM because the feasible latent-support set changes with the candidate tree.
- No neural estimator is in A1.

## Validation policy

Validation is proportional to the actual numerical and scientific risks:

- exhaustive connected-support comparisons for the required small trees;
- focused tests for train/validation/test separation and accepted-move
  monotonicity;
- no repeated hash checks or generic smoke-test grids.

Implementation and experimental decisions will be added here as they occur.

