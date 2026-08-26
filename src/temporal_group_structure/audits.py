from __future__ import annotations

from collections import Counter
from itertools import combinations
from math import ceil
from typing import Iterable, Sequence

import numpy as np

from temporal_group_structure.event_identity import TemporalEvent


def classify_event(
    nodes: frozenset[str],
    historical_edges: set[frozenset[str]],
    historical_nodes: set[str],
    historical_pairs: set[frozenset[str]] | None = None,
) -> str:
    """Classify an event against information available strictly before it."""

    if nodes in historical_edges:
        return "EXACT_REPEAT"
    unseen = nodes - historical_nodes
    if unseen == nodes:
        return "ALL_NEW_TOGETHER"
    if unseen:
        return "CONTAINS_NEW_NODE"
    if historical_pairs is None:
        historical_pairs = {
            frozenset(pair)
            for edge in historical_edges
            for pair in combinations(edge, 2)
        }
    if any(frozenset(pair) in historical_pairs for pair in combinations(nodes, 2)):
        return "PARTIAL_REPEAT"
    return "NOVEL_COMBINATION"


def prequential_classes(
    history: Iterable[TemporalEvent], test: Sequence[TemporalEvent]
) -> list[str]:
    """Classify test batches without letting equal-time events see one another."""

    historical_edges = {event.nodes for event in history}
    historical_nodes = set().union(*(event.nodes for event in history)) if historical_edges else set()
    historical_pairs = {
        frozenset(pair)
        for event in history
        for pair in combinations(event.nodes, 2)
    }
    labels: list[str] = []
    position = 0
    while position < len(test):
        timestamp = test[position].timestamp
        end = position
        while end < len(test) and test[end].timestamp == timestamp:
            end += 1
        batch = test[position:end]
        labels.extend(
            classify_event(event.nodes, historical_edges, historical_nodes, historical_pairs)
            for event in batch
        )
        historical_edges.update(event.nodes for event in batch)
        historical_nodes.update(node for event in batch for node in event.nodes)
        historical_pairs.update(
            frozenset(pair)
            for event in batch
            for pair in combinations(event.nodes, 2)
        )
        position = end
    return labels


def cardinality_summary(events: Sequence[TemporalEvent]) -> dict[str, float | int]:
    sizes = np.asarray([len(event.nodes) for event in events], dtype=int)
    if not len(sizes):
        return {"events": 0}
    return {
        "events": int(len(sizes)),
        "nodes": int(len(set().union(*(event.nodes for event in events)))),
        "unique_edges": int(len({event.nodes for event in events})),
        "median_size": float(np.median(sizes)),
        "p95_size": float(np.quantile(sizes, 0.95, method="higher")),
        "size_1_fraction": float(np.mean(sizes == 1)),
        "size_2_fraction": float(np.mean(sizes == 2)),
        "size_ge3_fraction": float(np.mean(sizes >= 3)),
        "size_ge4_fraction": float(np.mean(sizes >= 4)),
        "max_size": int(sizes.max()),
    }


def audit_test_events(history: Sequence[TemporalEvent], test: Sequence[TemporalEvent]) -> dict[str, float | int]:
    labels = prequential_classes(history, test)
    counts = Counter(labels)
    total = len(test)
    train_edges = {event.nodes for event in history}
    train_nodes = set().union(*(event.nodes for event in history)) if history else set()
    train_exact = sum(event.nodes in train_edges for event in test)
    initial_history_new_node = sum(bool(event.nodes - train_nodes) for event in test)
    initial_history_all_new = sum(event.nodes.isdisjoint(train_nodes) for event in test)
    prequential_new_node = counts["CONTAINS_NEW_NODE"] + counts["ALL_NEW_TOGETHER"]
    return {
        **{f"class_{label.lower()}": int(counts[label]) for label in (
            "EXACT_REPEAT", "PARTIAL_REPEAT", "NOVEL_COMBINATION",
            "CONTAINS_NEW_NODE", "ALL_NEW_TOGETHER", "OTHER"
        )},
        "exact_repeat_rate": float(counts["EXACT_REPEAT"] / total) if total else 0.0,
        "exact_in_initial_history_rate": float(train_exact / total) if total else 0.0,
        "novel_set_events": int(total - counts["EXACT_REPEAT"]),
        "new_node_event_rate": float(prequential_new_node / total) if total else 0.0,
        "all_new_event_rate": float(counts["ALL_NEW_TOGETHER"] / total) if total else 0.0,
        "initial_history_new_node_event_rate": float(initial_history_new_node / total) if total else 0.0,
        "initial_history_all_new_event_rate": float(initial_history_all_new / total) if total else 0.0,
    }
