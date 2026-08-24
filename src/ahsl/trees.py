"""Join-tree generation for labeled hyperedges."""

from __future__ import annotations

import networkx as nx
import numpy as np


SUPPORTED_TOPOLOGIES = ("random", "path", "star", "balanced")


def generate_tree(m: int, topology: str, seed: int) -> nx.Graph:
    """Generate a tree on labeled hyperedge nodes ``0, ..., m - 1``.

    ``random`` uses a uniformly sampled Pruefer sequence, hence is uniform over
    labeled trees. ``balanced`` uses the parent map of a binary heap.
    """
    if m < 1:
        raise ValueError("m must be at least 1")
    if topology not in SUPPORTED_TOPOLOGIES:
        raise ValueError(f"unsupported topology: {topology}")

    if topology == "path":
        tree = nx.path_graph(m)
    elif topology == "star":
        tree = nx.star_graph(m - 1)
    elif topology == "balanced":
        tree = nx.Graph()
        tree.add_nodes_from(range(m))
        tree.add_edges_from(((child - 1) // 2, child) for child in range(1, m))
    else:
        if m <= 2:
            tree = nx.path_graph(m)
        else:
            rng = np.random.default_rng(seed)
            pruefer = rng.integers(0, m, size=m - 2).tolist()
            tree = nx.from_prufer_sequence(pruefer)

    if not nx.is_tree(tree):
        raise RuntimeError("tree generator violated its contract")
    return tree


def validate_labeled_tree(tree: nx.Graph) -> int:
    """Validate the A0 tree convention and return its number of nodes."""
    if not nx.is_tree(tree):
        raise ValueError("tree must be connected and acyclic")
    m = tree.number_of_nodes()
    if set(tree.nodes) != set(range(m)):
        raise ValueError("tree nodes must be labeled consecutively from 0 to m - 1")
    return m

