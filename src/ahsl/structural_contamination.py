"""Size-preserving contamination outside a fixed-tree connected-subtree class."""

from __future__ import annotations

from typing import Any

import networkx as nx
import numpy as np

from ahsl.acyclicity import running_intersection_violations
from ahsl.trees import validate_labeled_tree


def contaminate_incidence_rows(
    clean_incidence: np.ndarray,
    tree: nx.Graph,
    contamination_probability: float,
    seed: int,
) -> dict[str, Any]:
    """Replace selected connected rows by disconnected supports of equal size.

    Rows without a valid leaf/remplacement pair remain unchanged; the returned
    actual fraction, rather than the requested probability, is used in analysis.
    """
    m = validate_labeled_tree(tree)
    if not 0.0 <= contamination_probability <= 1.0:
        raise ValueError("contamination_probability must lie in [0, 1]")
    incidence = np.asarray(clean_incidence, dtype=np.int8)
    if incidence.ndim != 2 or incidence.shape[1] != m:
        raise ValueError("incidence width must match the labeled tree")

    rng = np.random.default_rng(seed)
    requested_mask = rng.random(incidence.shape[0]) < contamination_probability
    contaminated = incidence.copy()
    actual_mask = np.zeros(incidence.shape[0], dtype=bool)
    for row in np.flatnonzero(requested_mask):
        support = set(np.flatnonzero(incidence[row]))
        if len(support) < 2:
            continue
        induced = tree.subgraph(support)
        leaves = sorted(node for node in support if induced.degree(node) <= 1)
        rng.shuffle(leaves)
        replacement: tuple[int, int] | None = None
        for leaf in leaves:
            remaining = support - {leaf}
            candidates = [
                node
                for node in range(m)
                if node not in support
                and all(not tree.has_edge(node, kept) for kept in remaining)
            ]
            if candidates:
                replacement = (leaf, candidates[int(rng.integers(len(candidates)))])
                break
        if replacement is None:
            continue
        removed, added = replacement
        contaminated[row, removed] = 0
        contaminated[row, added] = 1
        if running_intersection_violations(contaminated[row : row + 1], tree)[
            "num_violating_vertices"
        ] != 1:
            raise RuntimeError("accepted contamination did not violate connectivity")
        actual_mask[row] = True

    violations = running_intersection_violations(contaminated, tree)
    return {
        "incidence": contaminated,
        "requested_mask": requested_mask,
        "contamination_mask": actual_mask,
        "requested_fraction": float(requested_mask.mean()),
        "offclass_fraction": float(actual_mask.mean()),
        "clean_riv": int(violations["num_violating_vertices"]),
    }

