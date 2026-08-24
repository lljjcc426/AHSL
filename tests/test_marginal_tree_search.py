import inspect

import networkx as nx
import numpy as np

from ahsl.marginal_tree_search import (
    EstimatedQMarginalTree,
    MarginalLikelihoodTreeSearch,
    enumerate_labeled_trees,
    single_edge_swap_neighbors,
    tree_edge_signature,
)
from ahsl.q_estimation import estimate_q_mle
from ahsl.synthetic import generate_alpha_acyclic_hypergraph
from ahsl.trees import generate_tree
from ahsl.experiments.a1_runner import _fit_primary_trees, _split_rows


def test_full_swap_neighborhood_contains_only_unique_trees() -> None:
    tree = generate_tree(7, "balanced", seed=0)
    neighbors = single_edge_swap_neighbors(tree)
    signatures = [tree_edge_signature(candidate) for candidate in neighbors]
    assert len(signatures) == len(set(signatures))
    assert all(nx.is_tree(candidate) for candidate in neighbors)


def test_prufer_enumeration_covers_all_labeled_trees() -> None:
    trees = list(enumerate_labeled_trees(4))
    assert len(trees) == 4 ** 2
    assert len({tree_edge_signature(tree) for tree in trees}) == len(trees)


def test_search_is_deterministic_and_monotone() -> None:
    observed = np.random.default_rng(8).integers(0, 2, size=(20, 7), dtype=np.int8)
    first = MarginalLikelihoodTreeSearch(0.2, 0.2, 0.4, max_iterations=3).fit(
        observed
    )
    second = MarginalLikelihoodTreeSearch(0.2, 0.2, 0.4, max_iterations=3).fit(
        observed
    )
    assert tree_edge_signature(first.predict_tree()) == tree_edge_signature(
        second.predict_tree()
    )
    assert np.all(np.diff(first.objective_history_) > 0.0)


def test_q_estimation_uses_only_observations_and_recovers_large_sample_value() -> None:
    tree = generate_tree(8, "random", seed=12)
    clean = generate_alpha_acyclic_hypergraph(
        n=1000,
        m=8,
        tree=tree,
        branch_probability=0.4,
        seed=13,
    )["incidence"]
    estimate = estimate_q_mle(tree, clean, 0.0, 0.0)
    assert abs(estimate.q - 0.4) < 0.04
    assert list(inspect.signature(estimate_q_mle).parameters)[:2] == [
        "tree",
        "observed",
    ]


def test_estimated_q_interface_has_no_clean_data() -> None:
    assert list(inspect.signature(EstimatedQMarginalTree.fit).parameters) == [
        "self",
        "train_observed",
        "validation_observed",
    ]
    assert "clean" not in inspect.signature(_fit_primary_trees).parameters


def test_a1_row_split_is_disjoint_and_complete() -> None:
    clean = np.arange(50).reshape(10, 5)
    observed = clean + 100
    splits = _split_rows(clean, observed, [0.6, 0.2, 0.2])
    assert [len(splits[name][0]) for name in ["train", "validation", "test"]] == [
        6,
        2,
        2,
    ]
    reconstructed = np.concatenate(
        [splits[name][0] for name in ["train", "validation", "test"]]
    )
    assert np.array_equal(reconstructed, clean)
