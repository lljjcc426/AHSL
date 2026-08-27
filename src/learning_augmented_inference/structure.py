"""Hypergraph and primal-graph structure used by the R0 diagnostics."""

from __future__ import annotations

from collections.abc import Iterable, Sequence

import networkx as nx


def primal_graph(
    scopes: Iterable[Iterable[int]], n_variables: int | None = None
) -> nx.Graph:
    graph = nx.Graph()
    if n_variables is not None:
        graph.add_nodes_from(range(n_variables))
    for scope in scopes:
        variables = tuple(scope)
        graph.add_nodes_from(variables)
        for index, left in enumerate(variables):
            graph.add_edges_from((left, right) for right in variables[index + 1 :])
    return graph


def is_alpha_acyclic(scopes: Sequence[Sequence[int]]) -> bool:
    """Return the GYO reduction result after removing empty/duplicate scopes."""

    edges = {frozenset(scope) for scope in scopes if scope}
    while edges:
        changed = False
        maximal = {
            edge
            for edge in edges
            if not any(edge < other for other in edges)
        }
        if maximal != edges:
            edges = maximal
            changed = True

        counts: dict[int, int] = {}
        for edge in edges:
            for variable in edge:
                counts[variable] = counts.get(variable, 0) + 1
        reduced = {
            frozenset(variable for variable in edge if counts[variable] > 1)
            for edge in edges
        }
        reduced.discard(frozenset())
        if reduced != edges:
            edges = reduced
            changed = True
        if not changed:
            return False
    return True
