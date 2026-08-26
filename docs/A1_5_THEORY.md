# A1.5 Decision Theory and Posterior Inference

## 1. Decision losses

For latent support `S` and action `A`, complete-support loss is
`1[A != S]`; Hamming loss is `|A symmetric_difference S|`. Their Bayes actions
need not coincide.

## 2. Posterior MAP support

Conditional complete-support risk is `1-P(S=A|Y)`. Hence any posterior mode
minimizes exact-support 0-1 loss. The frozen `GeneratorPriorConnectedMAP` is the
exact action for this loss in the interior-noise regime.

## 3. Unconstrained Bayes-Hamming decoder

Let `pi_j=P(X_j=1|Y,T,q)`. Predicting one at coordinate `j` incurs risk
`1-pi_j`; predicting zero incurs `pi_j`. Therefore

```text
x_hat_j = 1[pi_j > 1/2]
```

is Bayes-optimal over all binary vectors. At equality A1.5 deterministically
chooses zero. This action may be empty or disconnected and is diagnostic only.

## 4. Connected Bayes-Hamming derivation

For a nonempty connected action `A`,

```text
R(A|Y) = sum_{j in A}(1-pi_j) + sum_{j not in A}pi_j
       = sum_j pi_j - sum_{j in A}(2*pi_j-1).
```

The first term is independent of `A`. Thus minimizing posterior Hamming risk in
the alpha-connected output class is exactly

```text
maximize sum_{j in A}(2*pi_j-1)
subject to A nonempty and T[A] connected.
```

A1's canonical maximum-weight connected-subtree DP solves this problem.

## 5. Posterior node marginals

Write the per-row partition function as

```text
Z(h) = sum_S P(Y,S|T,q) exp(sum_{j in S} h_j).
```

Replacing included emission `L_j(1)` by `L_j(1)exp(h_j)` gives

```text
d log Z(h)/d h_j at h=0 = P(X_j=1|Y,T,q).
```

This follows by differentiating the finite sum and dividing by `Z`.

## 6. Sum-product and reverse recurrence

A1 computes directed log messages

```text
e[u->v] = l0[u] + sum_{w != v} e[w->u]
i[u->v] = l1[u] + sum_{w != v} mix(e[w->u],i[w->u])
mix(e,i) = log((1-q)exp(e)+q exp(i)).
```

Anchor log weights are `a[u]=l1[u]+sum_w mix(w->u)`, and
`log Z=logsumexp(a)-log m`.

Initialize reverse adjoints of `a[u]` to its anchor posterior. Reverse each
addition and each mix. For an interior q, the mix derivatives are the normalized
excluded/included branch responsibilities. At q=0 or q=1 the surviving branch
has derivative one and the other zero. The adjoint accumulated at `l1[j]` is
exactly `pi_j`; the adjoint at `l0[j]` is `1-pi_j`.

The rerooted forward pass uses sum-except aggregates. Its reverse pass also uses
aggregate outgoing adjoints, avoiding quadratic work at high-degree nodes.

## 7. Root invariance

The partition is a finite sum over supports and contains no computational root.
Every rooted message schedule evaluates the same polynomial; exact derivatives
of that polynomial are therefore root-invariant. Numerical tests compare all
roots on several tree families.

## 8. Posterior risk

For any binary action `A`, posterior expected Hamming count is

```text
sum_{j in A}(1-pi_j) + sum_{j not in A}pi_j.
```

A1.5 records the normalized risk divided by `m`, matching the empirical
Hamming-error scale.

## 9. Connectivity cost

The model-implied cost is

```text
R(ConnectedBayesHamming)-R(PosteriorMedianUnconstrained) >= 0,
```

because the median optimizes over a superset of actions. The empirical cost
replaces posterior risk with realized clean Hamming. A disagreement diagnoses
posterior or model misspecification rather than a decoder bug.

## 10. Complexity

All node posterior marginals cost `O(m)` time per row and `O(nm)` for a batch.
MAP decoding remains `O(m^2)` because of the nonadditive `log |S|` size bonus.
Median decoding is `O(m)` and ConnectedBayesHamming is `O(m)` per row, aside
from deliberately tie-heavy canonical reconstruction.

## 11. Relationship to MBR literature

This is a connected-subtree centroid/maximum-expected-accuracy decoder. The
construction follows established posterior-decoding practice: compute component
marginals, express expected gain additively, and optimize over valid outputs.

## 12. What is classical

Bayes actions, coordinate medians, sum-product marginals, reverse derivatives
of a partition circuit, and additive maximum-subtree DP are classical.

## 13. What A1.5 does not prove

A1.5 does not establish real-data usefulness, unknown-noise identifiability,
novel MBR theory, neural-model necessity, or a reason to move to GHW greater
than one. It only tests whether A1's tree comparison changes under the correct
Bayes action for its declared Hamming loss.
