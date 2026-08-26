from __future__ import annotations

from itertools import combinations


def heredity_classification(subset: frozenset, active: set[frozenset]) -> str:
    if len(subset) < 2:
        return "NOT_APPLICABLE"
    parents = {frozenset(parent) for parent in combinations(subset, len(subset) - 1)}
    present = len(parents & active)
    if present == len(parents):
        return "STRONG_HEREDITY"
    if present:
        return "WEAK_ONLY"
    return "PURE_NON_HEREDITARY"
