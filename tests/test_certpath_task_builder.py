from certpath.hypergraph_builder import DirectedHypergraph, Hyperedge
from certpath.reactome_adapter import PathwayRecord, ReactomeSnapshot
from certpath.task_builder import build_natural_tasks


def _snapshot():
    graph = DirectedHypergraph([
        Hyperedge("r1", frozenset({"outside"}), frozenset({"mid"})),
        Hyperedge("r2", frozenset({"mid", "cofactor"}), frozenset({"target"})),
    ])
    pathways = {
        "family": PathwayRecord("family", "Family", frozenset(), frozenset({"leaf"})),
        "leaf": PathwayRecord("leaf", "Leaf", frozenset({"lr1", "lr2"}), frozenset()),
    }
    return ReactomeSnapshot(1, graph, pathways, {"lr1": "r1", "lr2": "r2"})


def test_pathway_membership_and_boundary_are_deterministic():
    tasks = build_natural_tasks(_snapshot())
    assert len(tasks) == 1
    task = tasks[0]
    assert task.gold_reactions == frozenset({"r1", "r2"})
    assert task.boundary_sources == frozenset({"outside", "cofactor"})
    assert task.targets == frozenset({"target"})
    assert task.family == "Family"


def test_builder_does_not_add_gold_internal_repair_sources():
    snapshot = _snapshot()
    task = build_natural_tasks(snapshot)[0]
    assert "mid" not in task.boundary_sources
