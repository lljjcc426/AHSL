import numpy as np

from ahsl.acyclicity import running_intersection_violations
from ahsl.join_tree_recovery import IntersectionMWSTJoinTree
from ahsl.synthetic import generate_alpha_acyclic_hypergraph
from ahsl.tree_perturbation import tree_edge_disagreement
from ahsl.trees import SUPPORTED_TOPOLOGIES, generate_tree


def test_mwst_is_deterministic_tree() -> None:
    incidence = np.array(
        [[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 1]], dtype=np.int8
    )
    first = IntersectionMWSTJoinTree().fit(incidence).predict_tree()
    second = IntersectionMWSTJoinTree().fit(incidence).predict_tree()
    assert sorted(first.edges()) == sorted(second.edges())


def test_mwst_is_valid_join_tree_for_clean_simple_alpha_acyclic_samples() -> None:
    for topology in SUPPORTED_TOPOLOGIES:
        for seed in range(5):
            generating_tree = generate_tree(8, topology, seed)
            sample = generate_alpha_acyclic_hypergraph(
                150,
                8,
                generating_tree,
                0.4,
                seed=seed + 100,
                simple_hypergraph=True,
            )
            estimated = IntersectionMWSTJoinTree().fit(sample["incidence"]).predict_tree()
            assert running_intersection_violations(sample["incidence"], estimated)[
                "num_violating_vertices"
            ] == 0
            assert 0.0 <= tree_edge_disagreement(generating_tree, estimated) <= 1.0

