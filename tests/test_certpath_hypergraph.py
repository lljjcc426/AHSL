from certpath.hypergraph_builder import DirectedHypergraph, Hyperedge
from certpath.graph_projection import projected_shortest_reactions, projection_semantically_valid


def test_tail_head_and_multi_tail_and_semantics():
    graph = DirectedHypergraph([
        Hyperedge("make-a", frozenset({"s"}), frozenset({"a"})),
        Hyperedge("make-b", frozenset({"s"}), frozenset({"b"})),
        Hyperedge("join", frozenset({"a", "b"}), frozenset({"t"})),
    ])
    assert graph.edges["join"].tail == frozenset({"a", "b"})
    assert not graph.is_feasible({"s"}, {"t"}, {"make-a", "join"})
    assert graph.is_feasible({"s"}, {"t"}, graph.edges)


def test_pairwise_projection_can_violate_conjunction():
    graph = DirectedHypergraph([
        Hyperedge("make-a", frozenset({"s"}), frozenset({"a"})),
        Hyperedge("join", frozenset({"a", "missing"}), frozenset({"t"})),
    ])
    projected = projected_shortest_reactions(graph, {"s"}, {"t"})
    assert projected == frozenset({"make-a", "join"})
    assert not projection_semantically_valid(graph, {"s"}, {"t"}, projected)


def test_global_sources_include_self_loop_only_vertex():
    graph = DirectedHypergraph([
        Hyperedge("loop", frozenset({"x"}), frozenset({"x"})),
        Hyperedge("forward", frozenset({"x"}), frozenset({"y"})),
    ])
    assert "x" in graph.global_sources()


def test_cycle_detection_uses_incidence_direction():
    graph = DirectedHypergraph([
        Hyperedge("first", frozenset({"s"}), frozenset({"a", "b"})),
        Hyperedge("feedback", frozenset({"a"}), frozenset({"s", "t"})),
    ])
    assert graph.contains_cycle(graph.edges)
