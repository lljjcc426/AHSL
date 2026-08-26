from __future__ import annotations

from collections import Counter
from collections.abc import Sequence

import numpy as np

from temporal_group_structure.candidate_search import Edge


def random_same_cardinality(
    positive: Edge,
    nodes: Sequence[str],
    forbidden: set[Edge],
    rng: np.random.Generator,
) -> Edge:
    while True:
        candidate = frozenset(rng.choice(nodes, size=len(positive), replace=False).tolist())
        if candidate not in forbidden and candidate != positive:
            return candidate


def one_member_corruption(
    positive: Edge,
    nodes: Sequence[str],
    forbidden: set[Edge],
    rng: np.random.Generator,
) -> Edge:
    members = sorted(positive)
    for _ in range(100):
        removed = members[int(rng.integers(len(members)))]
        replacement = nodes[int(rng.integers(len(nodes)))]
        candidate = frozenset((* (positive - {removed}), replacement))
        if len(candidate) == len(positive) and candidate not in forbidden and candidate != positive:
            return candidate
    return random_same_cardinality(positive, nodes, forbidden, rng)


def sampled_rank(true_score: float, negative_scores: Sequence[float]) -> int:
    return 1 + sum(score >= true_score for score in negative_scores)


def recall_at_k_from_ranks(ranks: Sequence[int], k: int) -> float:
    return float(np.mean(np.asarray(ranks) <= k)) if ranks else 0.0
