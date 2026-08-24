import networkx as nx
import numpy as np

from ahsl.acyclicity import running_intersection_violations
from ahsl.structural_contamination import contaminate_incidence_rows
from ahsl.synthetic import generate_alpha_acyclic_hypergraph
from ahsl.tree_perturbation import (
    perturb_tree_by_edge_swaps,
    tree_edge_disagreement,
)
from ahsl.trees import generate_tree


def test_simple_hypergraph_mode_has_no_empty_or_duplicate_hyperedges() -> None:
    tree = generate_tree(8, "balanced", 0)
    sample = generate_alpha_acyclic_hypergraph(
        100,
        8,
        tree,
        0.4,
        seed=12,
        simple_hypergraph=True,
    )
    assert not sample["has_empty_hyperedges"]
    assert sample["num_duplicate_hyperedge_pairs"] == 0


def test_tree_perturbation_is_reproducible_and_preserves_tree() -> None:
    tree = generate_tree(20, "random", 3)
    first = perturb_tree_by_edge_swaps(tree, 8, seed=9)
    second = perturb_tree_by_edge_swaps(tree, 8, seed=9)
    assert nx.is_tree(first)
    assert sorted(first.edges()) == sorted(second.edges())
    disagreement = tree_edge_disagreement(tree, first)
    assert 0.0 < disagreement <= 1.0


def test_zero_tree_swaps_preserve_tree_exactly() -> None:
    tree = generate_tree(12, "path", 0)
    unchanged = perturb_tree_by_edge_swaps(tree, 0, seed=1)
    assert tree_edge_disagreement(tree, unchanged) == 0.0


def test_offclass_contamination_is_size_preserving_and_disconnected() -> None:
    tree = generate_tree(6, "path", 0)
    clean = np.array(
        [[1, 1, 0, 0, 0, 0], [0, 1, 1, 0, 0, 0], [0, 0, 1, 1, 0, 0]],
        dtype=np.int8,
    )
    result = contaminate_incidence_rows(clean, tree, 1.0, seed=4)
    contaminated = result["incidence"]
    assert np.array_equal(contaminated.sum(axis=1), clean.sum(axis=1))
    assert result["contamination_mask"].all()
    assert running_intersection_violations(contaminated, tree)[
        "num_violating_vertices"
    ] == clean.shape[0]


def test_robustness_components_share_seed_reproducibility() -> None:
    tree = generate_tree(15, "random", 21)
    sample_a = generate_alpha_acyclic_hypergraph(80, 15, tree, 0.5, seed=22)
    sample_b = generate_alpha_acyclic_hypergraph(80, 15, tree, 0.5, seed=22)
    contamination_a = contaminate_incidence_rows(sample_a["incidence"], tree, 0.2, 23)
    contamination_b = contaminate_incidence_rows(sample_b["incidence"], tree, 0.2, 23)
    assert np.array_equal(sample_a["incidence"], sample_b["incidence"])
    assert np.array_equal(
        contamination_a["incidence"], contamination_b["incidence"]
    )
    assert np.array_equal(
        contamination_a["contamination_mask"],
        contamination_b["contamination_mask"],
    )

