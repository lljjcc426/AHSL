import numpy as np

from ahsl.corruption import corrupt_incidence
from ahsl.synthetic import generate_alpha_acyclic_hypergraph
from ahsl.trees import generate_tree


def test_synthetic_data_and_corruption_are_seed_reproducible() -> None:
    first_tree = generate_tree(8, "random", seed=12)
    second_tree = generate_tree(8, "random", seed=12)
    first = generate_alpha_acyclic_hypergraph(25, 8, first_tree, 0.4, seed=13)
    second = generate_alpha_acyclic_hypergraph(25, 8, second_tree, 0.4, seed=13)
    assert first["vertex_subtrees"] == second["vertex_subtrees"]
    assert np.array_equal(first["incidence"], second["incidence"])

    first_noise = corrupt_incidence(first["incidence"], 0.2, 0.1, seed=14)
    second_noise = corrupt_incidence(second["incidence"], 0.2, 0.1, seed=14)
    assert np.array_equal(first_noise["corrupted_incidence"], second_noise["corrupted_incidence"])
    assert np.array_equal(first_noise["false_negative_mask"], second_noise["false_negative_mask"])
    assert np.array_equal(first_noise["false_positive_mask"], second_noise["false_positive_mask"])


def test_incidence_reconstructs_stored_subtrees_exactly() -> None:
    tree = generate_tree(7, "balanced", seed=0)
    sample = generate_alpha_acyclic_hypergraph(20, 7, tree, 0.5, seed=31)
    reconstructed = np.zeros_like(sample["incidence"])
    for vertex, subtree in enumerate(sample["vertex_subtrees"]):
        reconstructed[vertex, list(subtree)] = 1
    assert np.array_equal(reconstructed, sample["incidence"])

