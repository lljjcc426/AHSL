from __future__ import annotations

from .hypergraph_builder import DirectedHypergraph


def gold_is_feasible(
    graph: DirectedHypergraph,
    sources: frozenset[str],
    targets: frozenset[str],
    gold_reactions: frozenset[str],
) -> bool:
    return graph.is_feasible(sources, targets, gold_reactions)
