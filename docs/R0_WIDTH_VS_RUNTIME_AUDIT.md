# R0 Width versus Runtime Audit

## What was measured

R0 computed min-fill/min-degree induced-width upper bounds, maximum intermediate
arity, peak dense entries, total joined entries and exact runtime on a bounded
subset. These are order-dependent proxies, not exact treewidth. Exact GHW/FHW
was not computed or claimed.

## Findings

On the seven representative models, the native domain/factor-size heuristic
never improved peak entries over min-fill. It tied min-fill on six models and
was 2x worse on `2bitcomp_5`. This provides no positive evidence that the local
native-scope score guides execution better than primal fill structure.

Equal induced width did not imply identical wall time: on `Grids_12`, all four
strategies have induced width 13 and peak 16,384, yet measured times varied by
1.46x and total joined entries by 1.48x. On `CSP_12`, all have induced width 11
and peak 524,288, with only a 1.28x runtime spread. This confirms that width is
not a perfect micro-cost model, but the residual was below the learning gate.

`ObjectDetection_74` illustrates domain size: induced width 6 still implies a
19,487,171-entry dense peak because its median domain size is 11. Reporting
treewidth alone would be misleading.

`Promedus_24` illustrates a high-order but easy structural family: 200 binary
variables, maximum arity three and half the factors order at least three, yet
all classical policies have peak 32 and total 1,516 entries. High-order identity
does not imply a strategy-learning opportunity.

## Hypergraph-width status

Alpha-acyclicity was evaluated only when unique-scope counts made the exact GYO
diagnostic cheap; 23 models were certified non-alpha-acyclic and 152 were left
unclassified by this bounded check. No GHD/FHD number appears in the results.
HyperBench supplies certified decomposition evidence but lacks factor execution,
so width-runtime correlation cannot be transferred to UAI without a new joined
artifact.

## Gate implication

R0 did not establish G8: a hypergraph-native feature/decomposition does not
outperform primal min-fill on real/accepted factor instances. The theoretical
single-hyperedge separation remains a toy example, not empirical support.
