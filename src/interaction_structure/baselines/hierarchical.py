from __future__ import annotations

from itertools import combinations

import numpy as np


def heredity_filtered_coefficients(
    coefficients: np.ndarray,
    terms: list[frozenset],
    *,
    rule: str = "weak",
    tolerance: float = 1e-10,
) -> np.ndarray:
    """Diagnostic post-filter showing the cost of heredity constraints."""
    output = np.asarray(coefficients, dtype=float).copy()
    active = {term for term, value in zip(terms, output, strict=True) if abs(value) > tolerance}
    for index, term in enumerate(terms):
        if len(term) < 2 or abs(output[index]) <= tolerance:
            continue
        parents = {frozenset(parent) for parent in combinations(term, len(term) - 1)}
        retain = parents <= active if rule == "strong" else bool(parents & active)
        if not retain:
            output[index] = 0.0
    return output
