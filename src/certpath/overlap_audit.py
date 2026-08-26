from __future__ import annotations

from itertools import combinations
from typing import Iterable, Mapping


def deterministic_family_split(
    task_families: Mapping[str, str],
    test_families: Iterable[str],
) -> tuple[frozenset[str], frozenset[str]]:
    held_out = frozenset(test_families)
    test = frozenset(task_id for task_id, family in task_families.items() if family in held_out)
    train = frozenset(task_families) - test
    return train, test


def pairwise_overlap(reaction_sets: dict[str, frozenset[str]]) -> list[dict[str, float | str | int | bool]]:
    rows = []
    for left, right in combinations(sorted(reaction_sets), 2):
        a, b = reaction_sets[left], reaction_sets[right]
        shared = len(a & b)
        union = len(a | b)
        rows.append({
            "left": left,
            "right": right,
            "shared_reactions": shared,
            "jaccard": shared / union if union else 1.0,
            "exact_duplicate": a == b,
            "left_subset_right": a < b,
            "right_subset_left": b < a,
        })
    return rows
