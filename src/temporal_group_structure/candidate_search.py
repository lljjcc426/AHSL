from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations
from typing import Iterable, Sequence

from temporal_group_structure.event_identity import TemporalEvent

Edge = frozenset[str]


def history_statistics(events: Sequence[TemporalEvent]) -> dict:
    edge_count: Counter[Edge] = Counter()
    edge_last: dict[Edge, int] = {}
    node_count: Counter[str] = Counter()
    pair_count: Counter[frozenset[str]] = Counter()
    pair_decay: Counter[frozenset[str]] = Counter()
    triple_count: Counter[frozenset[str]] = Counter()
    half_life = max(1.0, 0.10 * len(events))
    for index, event in enumerate(events):
        edge_count[event.nodes] += 1
        edge_last[event.nodes] = index
        node_count.update(event.nodes)
        decay = 2.0 ** (-(len(events) - 1 - index) / half_life)
        for pair in combinations(event.nodes, 2):
            key = frozenset(pair)
            pair_count[key] += 1
            pair_decay[key] += decay
        if len(event.nodes) <= 12:
            triple_count.update(frozenset(group) for group in combinations(event.nodes, 3))
    neighbors: dict[str, set[str]] = defaultdict(set)
    for pair in pair_count:
        left, right = tuple(pair)
        neighbors[left].add(right)
        neighbors[right].add(left)
    return {
        "edge_count": edge_count,
        "edge_last": edge_last,
        "node_count": node_count,
        "pair_count": pair_count,
        "pair_decay": pair_decay,
        "triple_count": triple_count,
        "neighbors": neighbors,
        "history_length": len(events),
    }


def cns_candidates(
    events: Sequence[TemporalEvent],
    *,
    source_limit: int = 5_000,
    replacements_per_slot: int = 2,
    candidate_limit: int = 50_000,
    max_size: int = 10,
    statistics: dict | None = None,
) -> set[Edge]:
    """Deterministic clique-negative-style one-member replacement candidates."""

    stats = history_statistics(events) if statistics is None else statistics
    observed = set(stats["edge_count"])
    pair_count = stats["pair_count"]
    neighbors = stats["neighbors"]
    sources = sorted(
        (edge for edge in observed if 2 <= len(edge) <= max_size),
        key=lambda edge: (-stats["edge_count"][edge], -stats["edge_last"][edge], tuple(sorted(edge))),
    )[:source_limit]
    output: set[Edge] = set()
    for source in sources:
        if len(output) >= candidate_limit:
            break
        for removed in sorted(source):
            base = source - {removed}
            if not base:
                continue
            common = None
            for node in base:
                common = set(neighbors.get(node, ())) if common is None else common & neighbors.get(node, set())
                if not common:
                    break
            if not common:
                continue
            ranked = sorted(
                common - source,
                key=lambda node: (
                    -sum(pair_count[frozenset((node, member))] for member in base),
                    node,
                ),
            )
            for replacement in ranked[:replacements_per_slot]:
                candidate = frozenset((*base, replacement))
                if candidate not in observed:
                    output.add(candidate)
                    if len(output) >= candidate_limit:
                        break
            if len(output) >= candidate_limit:
                break
    return output


def one_replacement_eligible(edge: Edge, historical_edges: set[Edge]) -> bool:
    """Whether a same-size historical edge differs in exactly one member."""

    return any(len(edge & old) == len(edge) - 1 and len(old) == len(edge) for old in historical_edges)


def candidate_recall(events: Iterable[TemporalEvent], candidates: set[Edge]) -> float:
    items = list(events)
    return sum(event.nodes in candidates for event in items) / len(items) if items else 0.0
