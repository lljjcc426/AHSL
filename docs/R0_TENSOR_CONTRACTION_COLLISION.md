# R0 Tensor-Contraction Collision

A dense discrete factor is a tensor, and sum-product elimination is tensor
contraction. Variable order or binary factor grouping induces a contraction
tree; the largest intermediate tensor controls memory, and operation count
controls time. This is the same structural core as VE ordering.

The tensor-network field already provides:

- exact/dynamic-programming path search on small networks;
- greedy and treewidth/contraction-width heuristics;
- hyperparameter search, slicing and simulated annealing in cotengra;
- reinforcement-learning contraction ordering (for example RL-TNCO);
- quantum-circuit benchmark families with explicit FLOP/memory objectives.

PGMs/CSPs add nonnegative semiring factors, sparse/deterministic supports,
evidence, MAP versus sum operations, global constraints and repeated queries.
These can distinguish an execution engine, but not a generic learned ordering
proposal. If the learned output is only a contraction path and evaluation only
measures FLOPs or peak tensor size, R0 duplicates tensor-network planning.

The bounded UAI audit reinforces the collision: the native
`min_factor_entries` order did not beat primal min-fill in peak entries on the
selected models. No separate hypergraph-only strategy residual was measured.
