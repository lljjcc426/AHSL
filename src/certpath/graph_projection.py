from __future__ import annotations

import heapq
from typing import Iterable, Mapping

from .hypergraph_builder import DirectedHypergraph


def projected_shortest_reactions(
    graph: DirectedHypergraph,
    sources: Iterable[str],
    targets: Iterable[str],
    costs: Mapping[str, float] | None = None,
) -> frozenset[str]:
    adjacency: dict[str, list[tuple[str, float, str]]] = {}
    for edge in graph.edges.values():
        cost = 1.0 if costs is None else float(costs[edge.id])
        for tail in edge.tail:
            for head in edge.head:
                adjacency.setdefault(tail, []).append((head, cost, edge.id))
    source_set = set(sources)
    selected: set[str] = set()
    for target in targets:
        queue = [(0.0, source, ()) for source in source_set]
        heapq.heapify(queue)
        best = {source: 0.0 for source in source_set}
        found: tuple[str, ...] | None = () if target in source_set else None
        while queue and found is None:
            distance, vertex, path = heapq.heappop(queue)
            if distance != best.get(vertex):
                continue
            if vertex == target:
                found = path
                break
            for head, cost, edge_id in adjacency.get(vertex, ()):
                candidate = distance + cost
                if candidate < best.get(head, float("inf")):
                    best[head] = candidate
                    heapq.heappush(queue, (candidate, head, path + (edge_id,)))
        if found is not None:
            selected.update(found)
    return frozenset(selected)


def projection_semantically_valid(
    graph: DirectedHypergraph,
    sources: Iterable[str],
    targets: Iterable[str],
    reactions: Iterable[str],
) -> bool:
    return graph.is_feasible(sources, targets, reactions)
