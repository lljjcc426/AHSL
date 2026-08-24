import networkx as nx
import numpy as np

from ahsl.subtree import enumerate_connected_subtrees
from ahsl.tree_dp import (
    generator_subtree_probability,
    maximum_weight_connected_subtree,
)
from ahsl.trees import SUPPORTED_TOPOLOGIES, generate_tree


def _brute_force(tree: nx.Graph, weights: np.ndarray) -> tuple[float, frozenset[int], bool]:
    candidates = enumerate_connected_subtrees(tree)
    scored = [(float(weights[list(nodes)].sum()), nodes) for nodes in candidates]
    best = max(score for score, _ in scored)
    optima = [nodes for score, nodes in scored if np.isclose(score, best)]
    chosen = min(optima, key=lambda nodes: (len(nodes), tuple(sorted(nodes))))
    return best, chosen, len(optima) > 1


def test_dp_returns_nonempty_connected_subset() -> None:
    tree = generate_tree(12, "random", 4)
    result = maximum_weight_connected_subtree(tree, np.arange(12) - 7)
    assert result["selected_nodes"]
    assert nx.is_connected(tree.subgraph(result["selected_nodes"]))


def test_all_negative_weights_return_best_lexicographic_singleton() -> None:
    tree = generate_tree(6, "star", 0)
    result = maximum_weight_connected_subtree(tree, [-1, -3, -1, -2, -4, -1])
    assert result["selected_nodes"] == frozenset({0})
    assert result["objective"] == -1
    assert result["has_tie"]


def test_all_positive_weights_return_whole_tree() -> None:
    tree = generate_tree(15, "balanced", 0)
    result = maximum_weight_connected_subtree(tree, np.ones(15))
    assert result["selected_nodes"] == frozenset(range(15))
    assert result["objective"] == 15
    assert not result["has_tie"]


def test_manual_path_and_star_cases() -> None:
    path = generate_tree(5, "path", 0)
    assert maximum_weight_connected_subtree(path, [-5, 4, 3, -10, 9])[
        "selected_nodes"
    ] == frozenset({4})
    star = generate_tree(5, "star", 0)
    assert maximum_weight_connected_subtree(star, [1, 3, -4, 2, -1])[
        "selected_nodes"
    ] == frozenset({0, 1, 3})


def test_randomized_dp_matches_brute_force_objective_and_canonical_subset() -> None:
    comparisons = 0
    for topology in SUPPORTED_TOPOLOGIES:
        for seed in range(50):
            m = 2 + seed % 8
            tree = generate_tree(m, topology, seed)
            rng = np.random.default_rng(seed + 1000)
            weights = rng.integers(-3, 4, size=m).astype(float)
            brute_score, brute_nodes, brute_tie = _brute_force(tree, weights)
            result = maximum_weight_connected_subtree(tree, weights)
            assert np.isclose(result["objective"], brute_score)
            assert result["selected_nodes"] == brute_nodes
            assert result["has_tie"] == brute_tie
            comparisons += 1
    assert comparisons == 200


def test_generator_prior_probabilities_sum_to_one() -> None:
    for topology in SUPPORTED_TOPOLOGIES:
        tree = generate_tree(5, topology, seed=8)
        total = sum(
            generator_subtree_probability(tree, subtree, 0.4)
            for subtree in enumerate_connected_subtrees(tree)
        )
        assert np.isclose(total, 1.0)


def test_generator_prior_monte_carlo_sanity() -> None:
    from ahsl.subtree import sample_connected_subtree

    tree = generate_tree(3, "path", 0)
    rng = np.random.default_rng(19)
    draws = 20_000
    target = frozenset({0, 1})
    frequency = sum(
        sample_connected_subtree(tree, 0.4, rng) == target for _ in range(draws)
    ) / draws
    expected = generator_subtree_probability(tree, target, 0.4)
    assert abs(frequency - expected) < 0.015

