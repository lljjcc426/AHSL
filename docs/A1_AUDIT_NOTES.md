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

## Implementation decisions

- The exact scorer uses log-space two-pass E/I messages and computes all anchor
  likelihoods in `O(nm)` time for a fixed tree and q.
- The measured full `m=16` single-edge-swap neighborhood contained 369 unique
  trees and took 0.47 seconds for 180 rows, so A1 used the complete neighborhood
  rather than A0.75's top-24 pruning.
- q estimation uses a bounded 21-point grid followed by scalar refinement.
- Literal Structural EM was not implemented: candidate trees change which
  clean supports are feasible, so direct observed-likelihood search is the
  cleaner exact classical objective here.

## Completed validation and experiments

- Brute-force validation: 1,440 row comparisons, zero mismatches, maximum
  absolute log-likelihood error `5.33e-15`.
- Small global search: 12 datasets at `m=6`; local search reached the globally
  best likelihood tree in all 12, with zero objective and downstream gap.
- Known-tree q diagnostic mean absolute error: `0.03783` at `n=100`, `0.01597`
  at `n=300`, and `0.01017` at `n=1000`.
- Primary experiment: 120 datasets and 1,680 method/decoder records, with 180
  train, 60 validation, and 60 held-out test rows per dataset.

## Empirical decision

- BinaryMWST matched-decoder excess: `0.02248`.
- OracleQMarginalTree excess: `0.02299`.
- EstimatedQMarginalTree excess: `0.02377`; gap closure `-5.7%`.
- Random-tree minus generating-tree Hamming: `0.05009`, so tree identity still
  has held-out value.
- Marginal likelihood improved held-out likelihood on average but did not
  improve clean held-out Hamming over BinaryMWST.
- Final decision: `C`. The current marginal formulation fails its own model
  kill condition; no neural model should be built from this result.
