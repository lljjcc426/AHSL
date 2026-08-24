# AHSL Phase A0.75 Theory: Noise-Corrected Join-Tree Recovery

## 1. First-moment correction

Let `X_ij` be a clean binary incidence and let `Y_ij^(r)` be an independent
observation with false-positive probability `p_+` and false-negative probability
`p_-`. Conditional on `X_ij`,

```text
E[Y_ij^(r) | X_ij]
  = p_+ + (1 - p_- - p_+) X_ij.
```

Write `delta = 1 - p_- - p_+` and let `Y_bar` be the mean of `R` repeated
observations. When `delta != 0`, define

```text
Z_ij = (Y_bar_ij - p_+) / delta.
```

Linearity gives `E[Z_ij | X_ij] = X_ij`. The correction need not lie in
`[0,1]`; clipping it would invalidate this equality.

## 2. Unbiased pairwise intersections

For two distinct hyperedge columns `j != k`, assume their incidence-noise
variables are conditionally independent given the clean incidence matrix. Then

```text
E[Z_ij Z_ik | X]
  = E[Z_ij | X_ij] E[Z_ik | X_ik]
  = X_ij X_ik.
```

Therefore

```text
W_hat[j,k] = sum_i Z_ij Z_ik
```

is conditionally unbiased for the clean intersection weight
`W[j,k] = |e_j intersect e_k|`. The corrected estimator is unbiased for
pairwise hyperedge-intersection weights, not necessarily an unbiased estimator
of the final discrete MWST.

## 3. Assumptions

The result requires the stated channel probabilities, `delta != 0`, repeated
measurements with the stated conditional means, and conditional independence
between the noise variables in distinct hyperedge columns for the product step.
Independence across original-vertex rows is not needed for the conditional mean
identity, although it affects concentration and bootstrap interpretation.

## 4. Why the diagonal is irrelevant

An MST uses only edges between distinct tree nodes. Values `W_hat[j,j]` are not
candidate tree-edge weights, so the implementation sets the diagonal to zero
without changing the recovered tree.

## 5. Correlated-noise limitation

If noise in columns `j` and `k` is conditionally correlated, then
`E[Z_ij Z_ik | X]` includes a covariance term. The proposed correction removes
the marginal channel bias but not that covariance. Unknown or heterogeneous
noise rates introduce additional misspecification.

## 6. Binary versus noise-corrected MWST

Binary MWST first turns observations into a hard incidence matrix and uses its
raw intersection counts. NoiseCorrectedMWST instead forms `Z`, retains negative
corrected values and negative pairwise weights, and applies the same
deterministic maximum-spanning-tree decoder. The difference isolates the
statistical weight estimator rather than the combinatorial tree algorithm.

## 7. Downstream value is the target

Every candidate tree is evaluated using the same
`DPNoiseAwareConnectedMLE`. The primary quantity is clean Hamming error in the
decoded incidence. Edge disagreement is diagnostic because multiple labeled
trees can provide similar or identical connected-subtree regularization.

## 8. Generating-tree recovery is not the main target

The synthetic generating tree need not be the unique join tree of the sampled
hypergraph. A tree with high labeled-edge disagreement may still be a valid join
tree or may induce nearly the same useful decisions. Conversely, better edge
overlap need not guarantee better downstream denoising. The true tree is used as
an information oracle under the fixed decoder, not as the sole scientific
definition of success.

## 9. Kill criteria

Neural A1 is cancelled when a classical estimator has mean downstream excess at
most `0.005` with upper paired-bootstrap 95% CI at most `0.010`, or when it
closes at least 80% of the BinaryMWST gap while leaving excess below `0.01`.
Join-tree recovery as a primary direction is cancelled when the first
preregistered random tree is within `0.005` Hamming error of the true-tree
oracle. A learned direction is allowed only if all continuation requirements in
the A0.75 protocol hold.

## 10. Scope of the result

This phase does not prove consistency of corrected MWST, unbiasedness of the
discrete tree, uniqueness or identifiability of a join tree, robustness to
correlated or unknown noise, or usefulness on real hypergraphs. It does not test
neural models, learn subtree priors, or change the uniform connected-subtree
decoder. It is a bounded classical kill-test of whether latent tree estimation
retains enough downstream value to justify a separate learned subproject.
