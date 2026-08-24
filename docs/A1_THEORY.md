# A1 Theory: A Percolation-Cluster Likelihood on a Labeled Tree

## 1. Generative model

Let `T=(V,E)` be a tree on `m=|V|` labeled hyperedge nodes. For each incidence
row, choose an anchor `A` uniformly from `V`. Starting at `A`, accept each
outward boundary edge independently with probability `q`; a rejected edge
blocks its entire branch. The included nodes form a nonempty connected set
`S`. Conditional on `X_j = 1[j in S]`, repeated observations are independent
with

```text
P(Y_j^r=1 | X_j=0) = p_+,
P(Y_j^r=0 | X_j=1) = p_-.
```

Rows are iid conditional on `(T,q,p_+,p_-)`.

## 2. Subtree prior

Fix a nonempty connected set `S` and an anchor `a in S`. Because `T[S]` is a
tree, exactly `|S|-1` accepted edges are required to reach every node in `S`.
Every edge in the boundary

```text
delta_T(S) = {uv in E : u in S, v not in S}
```

must be rejected. Decisions beyond a rejected boundary edge are never visited.
Thus

```text
P(S | A=a,T,q)
  = q^(|S|-1) (1-q)^|delta_T(S)|       if a in S,
  = 0                                           otherwise.
```

There are `|S|` compatible anchors, each with probability `1/m`, so

```text
P(S | T,q)
  = |S|/m q^(|S|-1) (1-q)^|delta_T(S)|.
```

Equivalently, open every tree edge independently with probability `q`, choose a
uniform vertex, and return its open component. The factor `|S|/m` is the usual
vertex-size bias of that percolation cluster.

## 3. Emissions and exact marginal likelihood

For one row, combine all `R` observations at node `j` into

```text
L_j(x) = product_r P(Y_j^r | X_j=x),  x in {0,1}.
```

Then

```text
P(Y | T,q)
  = sum_{nonempty connected S}
      P(S | T,q) product_j L_j(1[j in S]).
```

The dataset log likelihood is the sum of the row log likelihoods. This is an
observed-data likelihood, not a profile likelihood over `S`.

## 4. Anchor-conditioned messages

For a directed edge `u->v`, remove `{u,v}` and consider the component on the
`u` side. Define

```text
E_{u->v} = likelihood of that entire component being excluded,
I_{u->v} = likelihood conditional on u being reached by an accepted edge.
```

The recurrences are

```text
E_{u->v}
  = L_u(0) product_{w in N(u)\{v}} E_{w->u},

I_{u->v}
  = L_u(1) product_{w in N(u)\{v}}
      [(1-q) E_{w->u} + q I_{w->u}].
```

For anchor `a`,

```text
A_a = L_a(1) product_{u in N(a)}
        [(1-q) E_{u->a} + q I_{u->a}],

P(Y | T,q) = (1/m) sum_a A_a.
```

### Correctness

Conditioned on the anchor, each incident branch has exactly two disjoint cases:
reject its first edge and exclude the whole branch, or accept it and include
the adjacent node, after which the same independent construction recurses.
Multiplication is valid because branches are conditionally independent. Every
anchor-conditioned generated support appears once. After summing anchors, a
fixed connected `S` appears once for each `a in S`, producing the prior factor
`|S|/m`. Hence the recurrence equals the explicit connected-support sum.

Repeated observations affect only `L_j`; the recurrence is unchanged.

## 5. Normalization

Set every emission to one. By induction, all directed `E` and `I` messages are
one. Every anchor likelihood is one, hence

```text
(1/m) sum_a A_a = 1.
```

Therefore the connected-support prior is normalized. This proof also covers
`q=0` and `q=1` as mathematical boundary values.

## 6. Log-space implementation and complexity

Use

```text
log E = log L_u(0) + sum log E_child,
log I = log L_u(1)
        + sum logaddexp(log(1-q)+log E_child,
                        log(q)+log I_child).
```

All directed messages can be computed by one postorder and one preorder pass.
With prefix/suffix sums or total-minus-one-neighbor sums, all messages and all
anchor scores cost `O(m)` time and `O(m)` memory per row. Scoring `n` rows costs
`O(nm)`. No arbitrary epsilon is part of the probability model; exact zeros are
represented by negative infinity.

This is a specialized instance of classical sum-product on a tree.

## 7. Posterior inference

The anchor posterior is immediately available:

```text
P(A=a | Y,T,q) = A_a / sum_b A_b.
```

The matched posterior MAP support is

```text
argmax_S [log P(Y|S) + log P(S|T,q)],
```

which is the existing generator-prior connected MAP objective when the prior
formula and noise convention match. It is the primary downstream decoder.
Uniform-prior connected MLE remains a secondary continuity analysis.

Node marginals and entropy are computable with richer messages or automatic
differentiation of local fields, but they are not needed for the A1 decision.

## 8. Estimating q

For a fixed tree, maximize train or validation observed likelihood over a
preregistered compact interval such as `[0.02,0.98]`. A one-dimensional bounded
optimization is exact up to numerical tolerance and avoids unnecessary EM.

If complete supports were observed, the likelihood contribution involving `q`
would be

```text
(|S|-1) log q + |delta_T(S)| log(1-q),
```

and an EM-style update would divide the posterior expected number of accepted
edges by the expected number of accepted plus rejected frontier edges. A1 does
not need this update because direct scalar optimization is simpler and scores
the actual observed likelihood.

## 9. Tree objective and optimization

The estimator maximizes

```text
ell(T,q) = sum_{i in train} log P(Y_i | T,q)
```

over labeled trees, initialized by NoiseCorrectedMWST. A deterministic
best-improvement search evaluates valid one-edge swaps. An accepted move must
strictly increase the train observed likelihood. Validation data select `q` or
an iteration/model where required; clean data never enter fitting or selection.

The score does not decompose into fixed pairwise edge weights because changing
an edge changes which support sets are connected and their boundaries. An MST
closed form is therefore not established for this likelihood.

## 10. Why literal Structural EM is not selected

Structural EM is the correct broad framework for hidden-data structure
learning, but its usual efficient structural step assumes expected sufficient
statistics can score alternate structures on a common completion space. Here
the support of the latent variable depends on `T`: some sets connected under
the current tree are impossible under a candidate tree. A direct expected
complete-data score can consequently become negative infinity for ordinary
tree moves. Exact observed-likelihood local search is more transparent for this
small labeled-tree problem.

## 11. Profile versus marginal likelihood

Profile likelihood keeps only the best support per row and ignores the number
and prior mass of alternative explanations. Marginal likelihood sums every
connected support with its generative probability. A0.75 showed that improving
the profile objective can worsen clean recovery; A1 tests whether the matched
observed-data objective fixes that mismatch.

## 12. Generating tree versus downstream-optimal tree

The generating tree is a parameter of the synthetic distribution. It is
population-identifiable in the interior regime described below, but finite-data
MAP decoding under model misspecification can still favor another tree for
Hamming loss. Tree edge disagreement is therefore secondary to held-out NLL and
clean test recovery.

## 13. Identifiability summary

For labeled columns, `m>=2`, `0<q<1`, known noise with
`p_+ + p_- != 1`, the population distribution identifies `T` and `q`:

1. the binary noise channel is an invertible Kronecker product, so the clean
   support distribution is recoverable from the noisy distribution;
2. a two-node support has positive clean probability exactly for a tree edge,
   identifying every edge of `T`;
3. `P(S=V)=q^(m-1)`, identifying `q`.

This is a population argument, not a finite-sample guarantee. The endpoints
`q=0,1`, an uninformative noise channel, and `m=1` are nonidentifiable. Near the
endpoints the model is identifiable but weakly separated.

## 14. What is classical

- alpha-acyclicity, join trees, and their nonuniqueness;
- the maximum-weight spanning-tree characterization of join trees;
- bond-percolation clusters and size-biased component sampling;
- exact sum-product / belief propagation on trees;
- latent-variable marginal likelihood and structural search;
- noisy tree-model recovery and likelihood-based tree estimation.

## 15. What may remain new

The possible contribution is the precise combination of noisy hypergraph
incidence, a latent connected-support distribution over labeled hyperedge
columns, exact likelihood-based tree selection, and a tractability certificate,
plus evidence showing whether that combination has held-out value. This is a
narrow modeling and evaluation claim, not a claim of a new general DP.

