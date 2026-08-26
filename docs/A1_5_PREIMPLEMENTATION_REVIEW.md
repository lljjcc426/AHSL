# A1.5 Pre-implementation Review

## 1. Is MAP support Bayes-optimal for Hamming loss?

No. Posterior MAP minimizes complete-support 0-1 loss. It minimizes Hamming
only in special posterior configurations where the MAP action also happens to
minimize the sum of coordinate risks.

## 2. Is the coordinate median optimal for unconstrained Hamming loss?

Yes. For coordinate `j`, predicting one has risk `1-pi_j` and predicting zero
has risk `pi_j`; the smaller is chosen independently. A deterministic zero at
`pi_j=0.5` is Bayes-optimal among tied actions.

## 3. Is ConnectedBayesHamming exact?

Yes. For a connected nonempty prediction `S_hat`, posterior risk equals

```text
sum_j pi_j - sum_{j in S_hat}(2*pi_j-1).
```

The first term is action-independent. Exact maximum-weight connected-subtree
DP therefore gives the minimum-risk action within the required output class.

## 4. Is it a known construction?

Yes at the methodological level. It is a constrained centroid/maximum-expected-
accuracy decoder: posterior component marginals become additive gains and an
exact optimizer selects a legal structure. Carvalho and Lawrence (2008),
Hamada et al. (2009), and risk-based HMM posterior decoding are close precedents.

## 5. Can all node marginals be computed in O(m) per row?

Yes. A1's two-pass log-sum-product scorer is an `O(m)` arithmetic circuit.
Reverse-mode differentiation of the row log partition with respect to every
included-node log emission gives all `P(X_j=1|Y)` in one reverse traversal.
The batch cost is `O(nm)`. No finite differences or one-node-at-a-time reruns
are justified.

## 6. Is there a stronger decision rule?

Not for the declared loss and feasible output class. The exact constrained
Bayes action is definitionally optimal under the fitted posterior. Alternative
losses would answer different scientific questions and are out of scope.

## 7. Should A1.5 stop before implementation?

No. The correction can materially alter Hamming results, uses no new tree
estimator, has exact linear-time inference, and is the bounded final test
requested by the phase. Direct prior-art overlap prevents novelty claims but
does not invalidate the empirical audit.

## Literature gate

**GO**

Proceed with exact reverse-mode marginals, exhaustive small-tree validation,
the three frozen posterior actions, and the unchanged A1 primary datasets.
