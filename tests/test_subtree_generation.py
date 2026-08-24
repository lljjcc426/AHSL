import networkx as nx
import numpy as np

from ahsl.subtree import (
    enumerate_connected_subtrees,
    sample_connected_subtree,
)
from ahsl.trees import generate_tree


def test_sampled_subtrees_are_nonempty_connected_and_bounded() -> None:
    tree = generate_tree(15, "random", seed=4)
    rng = np.random.default_rng(5)
    for _ in range(100):
        subtree = sample_connected_subtree(
            tree, branch_probability=0.5, rng=rng, min_size=2, max_size=8
        )
        assert 2 <= len(subtree) <= 8
        assert nx.is_connected(tree.subgraph(subtree))


def test_path_enumeration_contains_exactly_all_intervals() -> None:
    tree = generate_tree(4, "path", seed=0)
    actual = set(enumerate_connected_subtrees(tree))
    expected = {
        frozenset(range(left, right + 1))
        for left in range(4)
        for right in range(left, 4)
    }
    assert actual == expected
    assert frozenset({0, 2}) not in actual
    assert frozenset({0, 3}) not in actual
    assert frozenset({0, 2, 3}) not in actual


def test_star_enumeration_has_all_center_sets_and_only_singleton_leaf_sets() -> None:
    tree = generate_tree(5, "star", seed=0)
    actual = set(enumerate_connected_subtrees(tree))
    assert len(actual) == 2**4 + 4
    for leaf_mask in range(1 << 4):
        leaves = {leaf + 1 for leaf in range(4) if leaf_mask & (1 << leaf)}
        assert frozenset({0, *leaves}) in actual
    assert frozenset({1}) in actual
    assert frozenset({1, 2}) not in actual

