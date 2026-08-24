"""Independent running-intersection verification on a fixed join tree."""

from __future__ import annotations

from typing import Any

import networkx as nx
import numpy as np

from ahsl.trees import validate_labeled_tree


def _as_numpy(incidence: Any) -> np.ndarray:
    if hasattr(incidence, "detach"):
        incidence = incidence.detach().cpu().numpy()
    return np.asarray(incidence)


def running_intersection_violations(
    incidence: Any, tree: nx.Graph
) -> dict[str, int | list[int] | list[bool]]:
    """Check whether every incidence row induces a non-empty connected subtree.

    A row with zero active hyperedges is invalid. Connectivity is verified by an
    explicit traversal here; no sampling or enumeration routine is reused.
    """
    m = validate_labeled_tree(tree)
    binary = _as_numpy(incidence)
    if binary.ndim != 2 or binary.shape[1] != m:
        raise ValueError("incidence must have shape (n, number_of_tree_nodes)")

    connected_flags: list[bool] = []
    violating: list[int] = []
    for vertex, row in enumerate(binary):
        active = set(np.flatnonzero(row > 0.5).tolist())
        if not active:
            is_connected = False
        else:
            start = next(iter(active))
            reached = {start}
            stack = [start]
            while stack:
                current = stack.pop()
                for neighbor in tree.neighbors(current):
                    if neighbor in active and neighbor not in reached:
                        reached.add(neighbor)
                        stack.append(neighbor)
            is_connected = reached == active
        connected_flags.append(is_connected)
        if not is_connected:
            violating.append(vertex)

    return {
        "num_violating_vertices": len(violating),
        "violating_vertices": violating,
        "per_vertex_connected": connected_flags,
    }

