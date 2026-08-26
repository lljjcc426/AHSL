# A1.5 Audit Notes

## Frozen base

- Parent commit: `dd275e7d8cdfbcc5399640baaa2088e078642d3e`.
- Branch: `phase-a1.5-decision-aligned-posterior-risk`.
- A0, A0.5, A0.75, and A1 artifacts are historical and are not modified.

## Interpretation audit

- A1's MAP Hamming measurements are numerically valid.
- Their decoder is Bayes-optimal for exact-support 0-1 loss, not Hamming loss.
- This is a decision/evaluation mismatch, not a correction to the saved A1
  numbers or to the A1 marginal-likelihood derivation.
- A1.5 reuses every tree estimator and the exact A1 data-generation convention.
- No new tree search or learned model is permitted.

## Literature gate

- Gate: `GO`.
- The decoder is classical constrained MBR/centroid methodology.
- The scientific purpose is a final bounded falsification test, not algorithmic
  novelty.

Implementation and empirical findings will be appended after validation.
