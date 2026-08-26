from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence

import numpy as np

from temporal_group_structure.candidate_search import Edge
from temporal_group_structure.event_identity import TemporalEvent


def deterministic_ranking(scores: Mapping[Edge, float]) -> list[Edge]:
    return sorted(scores, key=lambda edge: (-scores[edge], len(edge), tuple(sorted(edge))))


def exact_set_metrics(
    truth: Sequence[TemporalEvent] | Iterable[Edge],
    ranking: Sequence[Edge],
) -> dict[str, float]:
    truth_edges = [item.nodes if isinstance(item, TemporalEvent) else item for item in truth]
    rank = {edge: index + 1 for index, edge in enumerate(ranking)}
    ranks = np.asarray([rank.get(edge, len(ranking) + 1) for edge in truth_edges], dtype=float)
    found = np.asarray([edge in rank for edge in truth_edges], dtype=bool)
    if not len(ranks):
        return {"hit_at_1": 0.0, "recall_at_10": 0.0, "mrr": 0.0, "average_rank": 0.0, "candidate_recall": 0.0}
    reciprocal = np.where(found, 1.0 / ranks, 0.0)
    return {
        "hit_at_1": float(np.mean(ranks <= 1)),
        "recall_at_10": float(np.mean(ranks <= 10)),
        "mrr": float(np.mean(reciprocal)),
        "average_rank": float(np.mean(ranks)),
        "candidate_recall": float(np.mean(found)),
    }


def member_metrics(truth: Edge, prediction: Edge) -> dict[str, float]:
    intersection = len(truth & prediction)
    union = len(truth | prediction)
    precision = intersection / len(prediction) if prediction else 0.0
    recall = intersection / len(truth) if truth else 0.0
    return {
        "jaccard": intersection / union if union else 1.0,
        "member_precision": precision,
        "member_recall": recall,
        "member_f1": 2 * precision * recall / (precision + recall) if precision + recall else 0.0,
        "cardinality_error": float(abs(len(prediction) - len(truth))),
    }
