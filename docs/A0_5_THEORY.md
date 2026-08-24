# AHSL Phase A0.5 Theory

## 1. Fixed-tree Hamming projection derivation

For one incidence row, let `Y[r, j]` be `R` repeated binary observations and
let `S` be the non-empty connected support selected on the fixed tree `T`.
Predicting zero at node `j` incurs

```text
c_j(0) = sum_r Y[r, j],
```

while predicting one incurs

```text
c_j(1) = sum_r (1 - Y[r, j]).
```

Writing `C0 = sum_j c_j(0)` and `w_j = c_j(0) - c_j(1)` gives

```text
C(S) = C0 - sum_{j in S} w_j.
```

Thus minimum-Hamming projection is exactly the maximum-weight non-empty
connected-subtree problem. For binary observations,
`w_j = 2 sum_r Y[r, j] - R`.

## 2. Maximum-weight connected subtree recurrence

Root `T` arbitrarily. Let `F(v)` be the best score of a connected subset that
lies in the rooted descendant subtree of `v` and contains `v`. Then

```text
F(v) = w_v + sum_{u child of v} max(0, F(u)).
```

A positive child branch is included and a negative child branch is excluded.
When `F(u) = 0`, inclusion preserves the primary objective but increases size,
so the default `min_size_then_lexicographic` rule excludes it. The best
non-empty connected subset anywhere has value `max_v F(v)`. All-negative
weights therefore return the best singleton rather than the empty set.

## 3. Correctness argument

Every non-empty connected subset has a unique selected node closest to the
global root. Call it `v`. All other selected nodes lie in descendant branches
of `v`. In any included child branch, connectivity forces the selected part to
contain that child; different child branches interact only through `v`.
Consequently each child contributes its optimal containing-child solution when
that contribution is positive, and contributes nothing otherwise. This proves
the recurrence by induction from leaves to the root. Maximizing over the unique
highest node covers every feasible connected subset exactly once.

## 4. Complexity and deterministic ties

Postorder score computation and reconstruction are `O(m)` in the absence of a
large global tie. The implementation maximizes score, minimizes selected size,
then compares sorted node tuples lexicographically. Exact lexicographic
comparison can materialize several tied candidates and has `O(m^2)` worst-case
tie overhead, while the optimization recurrence remains linear. `has_tie`
records multiplicity of the primary score optimum; hash or set iteration order
never determines a result.

For `n` rows and `R` observations, weight construction plus the ordinary tree
DP costs `O(n R m)` time and `O(m)` working memory per row.

## 5. Noise-aware MLE reduction

Under false-negative rate `p_-` and false-positive rate `p_+`, define

```text
l_j(x) = sum_r log P(Y[r, j] | x_j = x).
```

For rates strictly between zero and one,

```text
log P(Y | S) = sum_j l_j(0) + sum_{j in S} (l_j(1) - l_j(0)).
```

The connected MLE is therefore another maximum-weight connected-subtree
problem with `w_j = l_j(1) - l_j(0)`. At probability boundaries the code keeps
impossible events at negative infinity. It handles mandatory-one and
forbidden-one nodes through exact feasibility logic rather than clipping
probabilities or evaluating `inf - inf`.

## 6. Independent versus connected MLE

`NoiseAwareIndependentMLE` selects the larger of `l_j(0)` and `l_j(1)` at each
node and knows no structural constraint. `NoiseAwareIndependentNonemptyMLE`
adds only the requirement that at least one node be selected: if the independent
solution is empty it flips the node with the smallest likelihood loss.
`DPNoiseAwareConnectedMLE` adds connectivity. Therefore

```text
Independent -> Independent + nonempty -> Independent + nonempty + connected
```

isolates non-emptiness gain from genuine connectivity gain.

## 7. Generator subtree prior derivation

With a uniformly selected anchor and outward branch acceptance probability `q`,
a connected non-empty set `S` can be generated from any of its `|S|` anchors.
Its `|S|-1` internal tree edges must be accepted and every boundary edge must be
rejected. With no size truncation,

```text
P(S | T, q) = (|S| / m) q^(|S|-1) (1-q)^|delta(S)|.
```

For a connected set in a tree,

```text
|delta(S)| = sum_{v in S} degree_T(v) - 2(|S|-1).
```

The prior is additive over selected nodes except for `log |S|`. A tree-knapsack
DP retains the best connected solution for every size and evaluates the size
bonus globally. Its score-state convolution is `O(m^2)`; storing canonical node
sets for exact ties can add higher worst-case copying cost. This oracle is used
only at moderate `m`. The formula is not claimed for active minimum/maximum size
truncation.

## 8. Objective/argmax mismatch in old FixedTreeAHSL

The old model learns a categorical distribution `q_i(S)` but its BCE loss sees
only the marginal

```text
P_i = sum_S q_i(S) 1_S.
```

The linear map from `q_i` to `P_i` is generally many-to-one, so `q_i` is not
identifiable from a loss depending only on `P_i`. It follows that `argmax q_i`
need not be the optimal discrete subtree for the reconstruction decision. This
is a proof-level explanation of an objective/decision mismatch; it does not by
itself prove the empirical A0 performance gap. It motivates decision-aligned
exact estimators rather than more epochs or a larger neural network.

## 9. Join-tree MWST classical baseline

Given an incidence estimate `B`, define complete hyperedge-pair weights

```text
W[j, k] = sum_i B[i, j] B[i, k].
```

`IntersectionMWSTJoinTree` applies deterministic maximum-weight Kruskal to
these weights. Exact edge equality with the generating tree is secondary: a
different maximum spanning tree can still be a valid join tree. The primary
checks are the running-intersection violations of clean incidence on the
estimated tree and downstream denoising quality.

## 10. What A0.5 does not prove

A0.5 does not establish novelty of join trees, maximum-weight connected-subtree
DP, or maximum spanning trees. It does not establish consistency outside the
synthetic noise model, usefulness for arbitrary hypergraphs, or a need for a
neural latent-tree learner. Literature citations are intentionally omitted;
citation to be added after literature verification.
