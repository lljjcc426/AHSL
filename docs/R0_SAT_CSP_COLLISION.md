# R0 SAT/CSP Collision

XCSP3 preserves arrays, global constraints, intension/extension and other
native modeling structure; its public ecosystem contains more than 23,000
instances and annual 2024--2026 competitions. It is a strong accepted benchmark
route for exact/certified solving, but it is not automatically a factor-marginal
inference benchmark.

Modern CP/SAT research already learns or configures:

- branching variables and values;
- restart and propagation choices;
- solver/portfolio selection;
- clause, cut and node priorities;
- diving and neighborhood decisions.

The correctness pattern is the same as R0: predictions guide search, while the
exact solver remains authoritative. Recent GNN-powered backtracking and 2024
learned branching work demonstrate that this interface is active.

High-arity constraints do not by themselves create an R0 residual. Global
constraints often have specialized propagators or compact intensional
representations; clique-expanding them is a poor cost model, but GHD/FHD is not
necessarily the solver's operative bottleneck either. If R0 predicts a branch
or solver using scope features, the contribution is generic CP algorithm
selection unless it proves that a native hypergraph decomposition quantity
changes exact inference cost beyond standard propagation/search features.

The available XCSP route therefore supports G1/G2/G4/G9, but it triggers the
generic-solver collision and does not supply the same repeated probabilistic
inference task as UAI.
