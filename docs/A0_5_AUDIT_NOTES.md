# Phase A0.5 Audit Notes for the Frozen A0 Baseline

The A0 baseline is frozen at commit
`2a8a6f10f2dde3e8bea9d26ac0ed213a6f5030a1`. Phase A0.5 does not rewrite its
code, configurations, or saved results. The following points were found while
building exact DP replacements and are recorded without retroactively changing
A0 evidence.

## Findings

1. `NoiseAwareMAPSubtree` in A0 maximizes the known-noise likelihood over a
   uniform connected-subtree candidate set. Mathematically it is a constrained
   MLE, or equivalently a MAP estimator only under a uniform prior. A0.5 uses the
   explicit name `DPNoiseAwareConnectedMLE` and reserves MAP terminology for the
   generator-prior oracle.
2. A0 exhaustive enumeration resolves tied optima through candidate enumeration
   order. A0.5 records tie frequency and fixes one canonical rule: maximize the
   objective, minimize subtree size, then choose the lexicographically smallest
   node tuple. The objective values remain valid, but tied exact-recovery and F1
   values can depend on the selected representative.
3. The learnable `FixedTreeAHSL` categorical distribution is a valid
   connected-subtree parameterization. Its row-specific categorical logits are
   not, however, a statistically identifiable structural model from a single
   direct observation without additional sharing or prior assumptions. This is
   a limitation of the learning question, not an implementation failure.
4. The A0 synthetic generator permits empty hyperedges and repeated hyperedge
   columns. That is consistent with its original broad prototype scope. The A1
   MWST gate requires a simple-hypergraph mode, so A0.5 adds opt-in regeneration
   until hyperedges are non-empty and distinct while preserving the A0 default.

## Disposition

No severe implementation bug requiring an A0 result rewrite was found. These
issues affect nomenclature, interpretation, tie reproducibility, and the scope
of the classical join-tree gate. They are handled prospectively in A0.5.

