import networkx as nx
import pytest

from ahsl.trees import SUPPORTED_TOPOLOGIES, generate_tree


@pytest.mark.parametrize("topology", SUPPORTED_TOPOLOGIES)
@pytest.mark.parametrize("m", [1, 2, 8])
def test_generated_graph_is_labeled_tree(topology: str, m: int) -> None:
    tree = generate_tree(m, topology, seed=17)
    assert set(tree.nodes) == set(range(m))
    assert tree.number_of_edges() == m - 1
    assert nx.is_tree(tree)


def test_random_tree_seed_is_reproducible() -> None:
    first = generate_tree(12, "random", seed=91)
    second = generate_tree(12, "random", seed=91)
    assert sorted(first.edges()) == sorted(second.edges())

