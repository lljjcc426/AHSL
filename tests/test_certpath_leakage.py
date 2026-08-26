from certpath.hypergraph_builder import DirectedHypergraph, Hyperedge
from certpath.overlap_audit import deterministic_family_split


def test_historical_snapshot_is_not_mutated_by_later_release():
    historical = DirectedHypergraph([Hyperedge("old", frozenset({"s"}), frozenset({"t"}))])
    later = DirectedHypergraph([
        Hyperedge("old", frozenset({"s"}), frozenset({"t"})),
        Hyperedge("new", frozenset({"s"}), frozenset({"future"})),
    ])
    assert "new" not in historical.edges
    assert "future" not in historical.vertices
    assert "new" in later.edges


def test_stable_ids_enable_release_overlap_without_reaction_parameters():
    old_ids = frozenset({"R-HSA-1", "R-HSA-2"})
    new_ids = frozenset({"R-HSA-2", "R-HSA-3"})
    assert old_ids & new_ids == {"R-HSA-2"}


def test_family_split_is_deterministic_and_group_disjoint():
    families = {"p3": "C", "p1": "A", "p2": "B", "p4": "A"}
    first = deterministic_family_split(families, {"A"})
    second = deterministic_family_split(dict(reversed(list(families.items()))), ["A"])
    assert first == second
    train, test = first
    assert train == {"p2", "p3"}
    assert test == {"p1", "p4"}
