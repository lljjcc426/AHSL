from itertools import combinations

from certpath.attainability import check_positive_cost_attainability, robust_optimality_margin
from certpath.hypergraph_builder import DirectedHypergraph, Hyperedge
from certpath.solver_adapter import solve_shortest_superpath


def _powerset(items):
    for size in range(len(items) + 1):
        yield from combinations(items, size)


def test_redundant_gold_branch_is_unattainable():
    graph = DirectedHypergraph([
        Hyperedge("direct", frozenset({"s"}), frozenset({"t"})),
        Hyperedge("branch", frozenset({"s"}), frozenset({"unused"})),
    ])
    result = check_positive_cost_attainability(graph, frozenset({"s"}), frozenset({"t"}), frozenset(graph.edges))
    assert result.feasible
    assert not result.attainable
    assert result.minimum_size == 1


def test_minimal_gold_is_positive_cost_attainable():
    graph = DirectedHypergraph([
        Hyperedge("left", frozenset({"s"}), frozenset({"a"})),
        Hyperedge("right", frozenset({"a"}), frozenset({"t"})),
    ])
    result = check_positive_cost_attainability(graph, frozenset({"s"}), frozenset({"t"}), frozenset(graph.edges))
    assert result.attainable
    assert result.minimum_size == 2


def test_exact_solver_matches_exhaustive_enumeration_on_cyclic_multitail_case():
    graph = DirectedHypergraph([
        Hyperedge("a", frozenset({"s"}), frozenset({"x", "z"})),
        Hyperedge("b", frozenset({"x", "z"}), frozenset({"y"})),
        Hyperedge("cycle", frozenset({"y"}), frozenset({"x", "t"})),
        Hyperedge("parallel", frozenset({"s"}), frozenset({"t"})),
        Hyperedge("self", frozenset({"z"}), frozenset({"z"})),
    ])
    ids = sorted(graph.edges)
    feasible = [set(subset) for subset in _powerset(ids) if graph.is_feasible({"s"}, {"t"}, subset)]
    exact = solve_shortest_superpath(graph, {"s"}, {"t"})
    assert exact.status == "OPTIMAL"
    assert len(exact.edge_ids) == min(map(len, feasible))


def test_robust_margin_is_second_exact_solve():
    graph = DirectedHypergraph([
        Hyperedge("chosen", frozenset({"s"}), frozenset({"t"})),
        Hyperedge("alt-1", frozenset({"s"}), frozenset({"a"})),
        Hyperedge("alt-2", frozenset({"a"}), frozenset({"t"})),
    ])
    lower = {"chosen": 0.9, "alt-1": 0.8, "alt-2": 0.8}
    upper = {"chosen": 1.1, "alt-1": 1.0, "alt-2": 1.0}
    margin, competitor = robust_optimality_margin(
        graph, frozenset({"s"}), frozenset({"t"}), frozenset({"chosen"}), lower, upper
    )
    assert competitor.edge_ids == frozenset({"alt-1", "alt-2"})
    assert abs(margin - 0.5) < 1e-8
