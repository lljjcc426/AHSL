# R0 Database and Join Collision

FAQ expresses sum-product, MAP-like and database aggregates as variable
elimination over a semiring. Fractional edge covers and FAQ-width control
multiway joins. Worst-case optimal join algorithms avoid harmful sequences of
binary joins, and JoinInfer imports this machinery directly into exact PGM
inference.

Consequently the following R0 proposals nearly coincide with database work:

| R0 proposal | database analogue |
|---|---|
| elimination/factor order | join order |
| intermediate factor-size prediction | cardinality estimation |
| choose pairwise vs multiway product | physical operator selection |
| rank GHD bags/separators | join/decomposition planning |
| runtime prediction for plans | learned cost model |

Probabilistic factors add semiring values, normalization, evidence updates,
repeated marginals and deterministic zeros. Those distinctions affect execution
and amortization, but they do not automatically create a new strategy-learning
problem. A proposal must show an empirical residual that a learned database
cost/plan model could not already address.

JoinInfer is the key collision and positive control. It reports exact marginal
inference, GHD/WCOJ execution, large cross-engine speed differences and a
data-driven per-bag/engine heuristic. It also reports that high-order/sparse
advantages depend on support and total entries, and it induced sparsity in part
of its testbed. R0 found no later benchmark that turns this into a clean,
family-disjoint learning problem with affordable oracle labels.
