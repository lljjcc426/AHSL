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

## Implementation and exact audit

- Added analytic reverse-mode differentiation of the frozen A1 likelihood
  circuit; finite differences and automatic differentiation were not used.
- Added the three preregistered actions with deterministic canonical ties.
- The exhaustive audit covered 1,760 posterior/decision rows and 12,320 node
  marginals. Marginal, MAP, median, and connected-MBR mismatches were all zero.
- Maximum marginal error was `2.5535e-15`; maximum posterior normalization
  error was `1.8874e-15`; maximum root-invariance error was `2.1094e-15`.
- All 191 repository tests passed.
- No implementation defect was found in the frozen A1 MAP decoder for its A1
  interior regime. A1.5 added exact q=0/q=1 behavior and a small-tree
  deterministic-noise reference path without changing A1 artifacts.

## A1 reproduction audit

The 840 frozen A1 matched-prior records were paired with A1.5 records using the
same dataset, tree source, and appropriate q treatment. Maximum differences in
Hamming, exact-row recovery, and tree-edge disagreement were all exactly zero.
No historical numerical result requires correction.

## Interpretation after A1.5

- A1's MAP reporting remains technically correct for exact-support loss but is
  decision-misaligned with its primary Hamming evaluation.
- Correcting the action improved Hamming, but did not rescue marginal tree
  selection. Deployable ConnectedBayesHamming TreeGain was `0.0009288`, with
  paired 95% CI `[-0.0009722, 0.0028388]`.
- Only random and path exceeded the `0.005` topology threshold; balanced did
  not, and star favored BinaryMWST.
- Unique/non-tied TreeGain was `0.0001511`, with CI crossing zero.
- The latent-tree stop rule fired; the wider alpha warning did not.
- ConnectedBayesHamming improved MAP Hamming for all seven tree sources, with
  every paired 95% DecoderGain CI strictly above zero. This is the meaningful
  positive posterior/subtree signal specified by the second stop rule.
- Final selection: **Decision B**. The `0.005` materiality threshold applies to
  TreeGain; it is not imposed on DecoderGain by the preregistered prompt.
