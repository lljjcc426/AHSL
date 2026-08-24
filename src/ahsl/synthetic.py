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
    simple_hypergraph: bool = False,
    max_generation_attempts: int = 1000,
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
    attempts = 0
    while True:
        attempts += 1
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
        empty_hyperedges = int((incidence.sum(axis=0) == 0).sum())
        column_signatures = [incidence[:, column].tobytes() for column in range(m)]
        signature_counts: dict[bytes, int] = {}
        for signature in column_signatures:
            signature_counts[signature] = signature_counts.get(signature, 0) + 1
        duplicate_pairs = sum(
            count * (count - 1) // 2 for count in signature_counts.values()
        )
        if not simple_hypergraph or (empty_hyperedges == 0 and duplicate_pairs == 0):
            break
        if attempts >= max_generation_attempts:
            raise RuntimeError(
                "failed to generate a non-empty, duplicate-free hypergraph within "
                f"{max_generation_attempts} attempts"
            )
    verification = running_intersection_violations(incidence, tree)
    if verification["num_violating_vertices"] != 0:
        raise RuntimeError("connected-subtree construction failed")
    return {
        "tree": tree,
        "incidence": incidence,
        "vertex_subtrees": vertex_subtrees,
        "num_generation_attempts": attempts,
        "has_empty_hyperedges": empty_hyperedges > 0,
        "num_duplicate_hyperedge_pairs": duplicate_pairs,
    }
