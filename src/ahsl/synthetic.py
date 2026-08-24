"""Synthetic alpha-acyclic hypergraphs generated from connected tree subsets."""

from __future__ import annotations

from typing import Any

import networkx as nx
import numpy as np

from ahsl.acyclicity import running_intersection_violations
from ahsl.hypergraph import incidence_from_subtrees
from ahsl.subtree import sample_connected_subtree
from ahsl.trees import validate_labeled_tree


def generate_alpha_acyclic_hypergraph(
    n: int,
    m: int,
    tree: nx.Graph,
    branch_probability: float,
    min_subtree_size: int = 1,
    max_subtree_size: int | None = None,
    seed: int = 0,
) -> dict[str, Any]:
    """Generate a hypergraph whose row supports satisfy running intersection.

    Each original vertex is assigned a non-empty connected subset of the fixed
    join tree. Empty hyperedges are allowed in A0; no post-hoc incidence repair
    is applied because that would change the specified sampling distribution.
    """
    if n < 1:
        raise ValueError("n must be at least 1")
    if validate_labeled_tree(tree) != m:
        raise ValueError("m must equal the number of nodes in tree")

    rng = np.random.default_rng(seed)
    vertex_subtrees = [
        sample_connected_subtree(
            tree,
            branch_probability,
            rng,
            min_size=min_subtree_size,
            max_size=max_subtree_size,
        )
        for _ in range(n)
    ]
    incidence = incidence_from_subtrees(vertex_subtrees, m)
    verification = running_intersection_violations(incidence, tree)
    if verification["num_violating_vertices"] != 0:
        raise RuntimeError("connected-subtree construction failed")
    return {
        "tree": tree,
        "incidence": incidence,
        "vertex_subtrees": vertex_subtrees,
    }

