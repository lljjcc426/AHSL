"""Exact generation and enumeration of connected join-tree subsets."""

from __future__ import annotations

from collections import deque
from collections.abc import Iterable

import networkx as nx
import numpy as np

from ahsl.trees import validate_labeled_tree


def sample_connected_subtree(
    tree: nx.Graph,
    branch_probability: float,
    rng: np.random.Generator,
    min_size: int = 1,
    max_size: int | None = None,
) -> frozenset[int]:
    """Sample a non-empty connected node set by traversal from a random anchor.

    Every accepted frontier node is reached through an already active parent.
    A rejected frontier branch is not traversed further, so connectivity holds
    by construction. The orientation is created relative to the sampled anchor,
    rather than inherited from a global root.
    """
    m = validate_labeled_tree(tree)
    if not 0.0 <= branch_probability <= 1.0:
        raise ValueError("branch_probability must lie in [0, 1]")
    maximum = m if max_size is None else max_size
    if not 1 <= min_size <= maximum <= m:
        raise ValueError("subtree size bounds must satisfy 1 <= min <= max <= m")
    if branch_probability == 0.0 and min_size > 1:
        raise ValueError("branch_probability=0 cannot produce a subtree larger than one")

    while True:
        anchor = int(rng.integers(m))
        active = {anchor}
        visited = {anchor}
        frontier: deque[int] = deque([anchor])

        while frontier and len(active) < maximum:
            current = frontier.popleft()
            neighbors = [node for node in tree.neighbors(current) if node not in visited]
            rng.shuffle(neighbors)
            for neighbor in neighbors:
                visited.add(neighbor)
                if len(active) >= maximum:
                    break
                if rng.random() < branch_probability:
                    active.add(neighbor)
                    frontier.append(neighbor)

        if len(active) >= min_size:
            return frozenset(active)


def _adjacency_bitmasks(tree: nx.Graph) -> list[int]:
    m = validate_labeled_tree(tree)
    masks = [0] * m
    for left, right in tree.edges:
        masks[left] |= 1 << right
        masks[right] |= 1 << left
    return masks


def _bitmask_is_connected(mask: int, adjacency: list[int]) -> bool:
    first = mask & -mask
    seen = 0
    frontier = first
    while frontier:
        node_bit = frontier & -frontier
        frontier ^= node_bit
        node = node_bit.bit_length() - 1
        seen |= node_bit
        frontier |= adjacency[node] & mask & ~seen
    return seen == mask


def enumerate_connected_subtrees(tree: nx.Graph) -> list[frozenset[int]]:
    """Enumerate every non-empty connected induced node set exactly once.

    The Phase A0 implementation scans all ``2**m - 1`` non-empty masks and
    performs a bitset traversal for each. This is exact and intentionally
    exponential; callers must inspect the search-space diagnostic before using
    it for larger ``m``.
    """
    m = validate_labeled_tree(tree)
    adjacency = _adjacency_bitmasks(tree)
    connected: list[frozenset[int]] = []
    for mask in range(1, 1 << m):
        if _bitmask_is_connected(mask, adjacency):
            connected.append(
                frozenset(node for node in range(m) if mask & (1 << node))
            )
    return connected


def subtree_boundary_size(tree: nx.Graph, subtree: Iterable[int]) -> int:
    """Count tree edges with exactly one endpoint in a node subset."""
    selected = set(subtree)
    return sum((left in selected) != (right in selected) for left, right in tree.edges)


def generator_subtree_probability(
    tree: nx.Graph,
    subtree: Iterable[int],
    branch_probability: float,
) -> float:
    """Probability of a connected support under uniform-anchor branch growth."""
    m = validate_labeled_tree(tree)
    selected = frozenset(subtree)
    if not selected or not nx.is_connected(tree.subgraph(selected)):
        return 0.0
    q = float(branch_probability)
    return (
        len(selected)
        / m
        * q ** (len(selected) - 1)
        * (1.0 - q) ** subtree_boundary_size(tree, selected)
    )


def subtree_incidence_matrix(
    subtrees: Iterable[Iterable[int]], m: int
) -> np.ndarray:
    """Convert connected node sets into a binary candidate-incidence matrix."""
    subtree_list = list(subtrees)
    matrix = np.zeros((len(subtree_list), m), dtype=np.float32)
    for row, subtree in enumerate(subtree_list):
        matrix[row, list(subtree)] = 1.0
    return matrix


def enumeration_diagnostic(m: int, topology: str | None = None) -> dict[str, int]:
    """Return exact known counts and the brute-force search-space size.

    Counts are topology-independent only for paths and stars. Random and
    balanced trees must be instantiated before their exact count is known.
    """
    if m < 1:
        raise ValueError("m must be at least 1")
    diagnostic = {"search_space": (1 << m) - 1}
    if topology == "path":
        diagnostic["num_connected_subtrees"] = m * (m + 1) // 2
    elif topology == "star":
        diagnostic["num_connected_subtrees"] = (1 << (m - 1)) + m - 1
    return diagnostic
