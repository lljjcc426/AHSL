from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping

import networkx as nx


@dataclass(frozen=True, slots=True)
class Hyperedge:
    id: str
    tail: frozenset[str]
    head: frozenset[str]
    reaction_type: str = "Conversion"
    name: str = ""

    def __post_init__(self) -> None:
        if not self.head:
            raise ValueError("A reaction hyperedge must have a non-empty head")


class DirectedHypergraph:
    """Directed reaction hypergraph with conjunctive (AND) tails."""

    def __init__(self, edges: Iterable[Hyperedge]):
        self.edges: dict[str, Hyperedge] = {edge.id: edge for edge in edges}
        self.vertices = frozenset(
            vertex
            for edge in self.edges.values()
            for vertex in edge.tail | edge.head
        )

    def closure(
        self,
        sources: Iterable[str],
        edge_ids: Iterable[str] | None = None,
    ) -> frozenset[str]:
        active = self.edges if edge_ids is None else {
            edge_id: self.edges[edge_id] for edge_id in edge_ids
        }
        reached = set(sources)
        changed = True
        while changed:
            changed = False
            for edge in active.values():
                if edge.tail <= reached and not edge.head <= reached:
                    reached.update(edge.head)
                    changed = True
        return frozenset(reached)

    def is_feasible(
        self,
        sources: Iterable[str],
        targets: Iterable[str],
        edge_ids: Iterable[str],
    ) -> bool:
        return set(targets) <= self.closure(sources, edge_ids)

    def global_sources(self) -> frozenset[str]:
        incoming: dict[str, list[Hyperedge]] = {v: [] for v in self.vertices}
        for edge in self.edges.values():
            for vertex in edge.head:
                incoming[vertex].append(edge)
        return frozenset(
            vertex
            for vertex, in_edges in incoming.items()
            if not in_edges
            or all(vertex in edge.tail for edge in in_edges)
        )

    def contains_cycle(self, edge_ids: Iterable[str]) -> bool:
        graph = nx.DiGraph()
        for edge_id in edge_ids:
            edge = self.edges[edge_id]
            edge_node = ("edge", edge_id)
            for vertex in edge.tail:
                graph.add_edge(("vertex", vertex), edge_node)
            for vertex in edge.head:
                graph.add_edge(edge_node, ("vertex", vertex))
        return not nx.is_directed_acyclic_graph(graph)

    def subset(self, edge_ids: Iterable[str]) -> "DirectedHypergraph":
        return DirectedHypergraph(self.edges[edge_id] for edge_id in edge_ids)

    def tail_arity(self, edge_ids: Iterable[str] | None = None) -> Mapping[str, int]:
        ids = self.edges if edge_ids is None else edge_ids
        return {edge_id: len(self.edges[edge_id].tail) for edge_id in ids}
