"""Incidence-matrix utilities for labeled A0 hypergraphs."""

from __future__ import annotations

from collections.abc import Iterable

import numpy as np


def incidence_from_subtrees(
    vertex_subtrees: Iterable[Iterable[int]], m: int
) -> np.ndarray:
    """Construct ``B[i, j] = 1`` exactly when hyperedge ``j`` is in row subtree ``i``."""
    rows = list(vertex_subtrees)
    incidence = np.zeros((len(rows), m), dtype=np.int8)
    for vertex, subtree in enumerate(rows):
        nodes = list(subtree)
        if not nodes:
            raise ValueError("each original vertex must belong to at least one hyperedge")
        incidence[vertex, nodes] = 1
    return incidence


def incidence_to_hyperedges(incidence: np.ndarray) -> list[frozenset[int]]:
    """Return labeled hyperedges as sets of original vertex indices."""
    binary = np.asarray(incidence)
    return [frozenset(np.flatnonzero(binary[:, column])) for column in range(binary.shape[1])]

