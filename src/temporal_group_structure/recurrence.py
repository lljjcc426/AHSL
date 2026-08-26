from __future__ import annotations

from collections.abc import Mapping
from itertools import combinations
from math import log1p

from temporal_group_structure.candidate_search import Edge


def score_edge(edge: Edge, stats: Mapping, method: str) -> float:
    edge_count = stats["edge_count"]
    if method == "exact_frequency":
        return float(edge_count[edge])
    if method == "most_recent":
        return float(stats["edge_last"].get(edge, -1))
    if method == "node_frequency_product":
        return sum(log1p(stats["node_count"][node]) for node in edge)
    pairs = [frozenset(pair) for pair in combinations(edge, 2)]
    if method == "pair_sum":
        return sum(log1p(stats["pair_count"][pair]) for pair in pairs)
    if method == "pair_min":
        return min((stats["pair_count"][pair] for pair in pairs), default=0.0)
    if method == "pair_hawkes":
        return sum(log1p(stats["pair_decay"][pair]) for pair in pairs)
    if method == "triple_support":
        if len(edge) > 12:
            return 0.0
        triples = [frozenset(group) for group in combinations(edge, 3)]
        return sum(log1p(stats["triple_count"][group]) for group in triples)
    raise ValueError(f"unknown method: {method}")
