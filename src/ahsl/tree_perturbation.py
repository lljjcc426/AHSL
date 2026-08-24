"""Deterministic diagnostics and valid edge-swap perturbations for join trees."""

from __future__ import annotations

import networkx as nx
import numpy as np

from ahsl.trees import validate_labeled_tree


def _canonical_edges(tree: nx.Graph) -> set[tuple[int, int]]:
    return {tuple(sorted((left, right))) for left, right in tree.edges}


def tree_edge_disagreement(reference: nx.Graph, estimate: nx.Graph) -> float:
    """Return one minus labeled-edge overlap, normalized by `m - 1`."""
    m = validate_labeled_tree(reference)
    if validate_labeled_tree(estimate) != m:
        raise ValueError("trees must have the same labeled node set")
    if m == 1:
        return 0.0
    overlap = len(_canonical_edges(reference) & _canonical_edges(estimate))
    return 1.0 - overlap / (m - 1)


def perturb_tree_by_edge_swaps(
    tree: nx.Graph,
    num_swaps: int,
    seed: int,
) -> nx.Graph:
    """Apply valid tree edge swaps without changing the labeled node set."""
    m = validate_labeled_tree(tree)
    if num_swaps < 0:
        raise ValueError("num_swaps must be non-negative")
    if m <= 2 and num_swaps:
        raise ValueError("a labeled tree with at most two nodes has no different edge swap")
    rng = np.random.default_rng(seed)
    perturbed = tree.copy()
    for _ in range(num_swaps):
        edges = sorted(_canonical_edges(perturbed))
        removal_order = rng.permutation(len(edges))
        completed = False
        for edge_index in removal_order:
            removed = edges[int(edge_index)]
            perturbed.remove_edge(*removed)
            components = [sorted(component) for component in nx.connected_components(perturbed)]
            candidates = [
                (left, right)
                for left in components[0]
                for right in components[1]
                if tuple(sorted((left, right))) != removed
            ]
            if candidates:
                added = candidates[int(rng.integers(len(candidates)))]
                perturbed.add_edge(*added)
                completed = True
                break
            perturbed.add_edge(*removed)
        if not completed:
            raise RuntimeError("no valid alternative cross-component edge was available")
    if not nx.is_tree(perturbed):
        raise RuntimeError("edge-swap perturbation failed to preserve a tree")
    return perturbed

