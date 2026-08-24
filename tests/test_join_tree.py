import numpy as np

from ahsl.acyclicity import running_intersection_violations
from ahsl.synthetic import generate_alpha_acyclic_hypergraph
from ahsl.trees import SUPPORTED_TOPOLOGIES, generate_tree


def test_known_connected_and_disconnected_rows() -> None:
    tree = generate_tree(4, "path", seed=0)
    incidence = np.array(
        [
            [1, 0, 0, 0],
            [1, 1, 1, 0],
            [1, 0, 1, 0],
            [0, 0, 0, 0],
        ],
        dtype=np.int8,
    )
    result = running_intersection_violations(incidence, tree)
    assert result["violating_vertices"] == [2, 3]
    assert result["per_vertex_connected"] == [True, True, False, False]


def test_randomized_clean_generators_have_no_violations() -> None:
    for seed in range(10):
        for topology in SUPPORTED_TOPOLOGIES:
            tree = generate_tree(9, topology, seed)
            sample = generate_alpha_acyclic_hypergraph(
                n=30,
                m=9,
                tree=tree,
                branch_probability=0.4,
                seed=seed,
            )
            result = running_intersection_violations(sample["incidence"], tree)
            assert result["num_violating_vertices"] == 0

