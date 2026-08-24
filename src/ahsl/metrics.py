"""Recovery, structural, and hyperedge-level metrics for Phase A0."""

from __future__ import annotations

from typing import Any

import networkx as nx
import numpy as np

from ahsl.acyclicity import running_intersection_violations


def _binary_scores(clean: np.ndarray, predicted: np.ndarray) -> tuple[float, float, float]:
    true_positive = int(np.logical_and(clean == 1, predicted == 1).sum())
    false_positive = int(np.logical_and(clean == 0, predicted == 1).sum())
    false_negative = int(np.logical_and(clean == 1, predicted == 0).sum())
    precision = true_positive / (true_positive + false_positive) if true_positive + false_positive else 0.0
    recall = true_positive / (true_positive + false_negative) if true_positive + false_negative else 0.0
    f1 = 2.0 * precision * recall / (precision + recall) if precision + recall else 0.0
    return precision, recall, f1


def binary_cross_entropy(probabilities: np.ndarray, targets: np.ndarray) -> float:
    """Mean Bernoulli cross-entropy, averaged over repeated observations if present."""
    probability = np.asarray(probabilities, dtype=float)
    target = np.asarray(targets, dtype=float)
    if target.ndim == 2:
        target = target[None, ...]
    clipped = np.clip(probability, 1e-7, 1.0 - 1e-7)
    losses = -(target * np.log(clipped) + (1.0 - target) * np.log(1.0 - clipped))
    return float(losses.mean())


def recovery_metrics(
    clean_incidence: np.ndarray,
    predicted_incidence: np.ndarray,
    tree: nx.Graph,
    observed_incidence: np.ndarray,
    predicted_probabilities: np.ndarray | None = None,
) -> dict[str, Any]:
    """Evaluate incidence, exact-row, hyperedge, and running-intersection recovery."""
    clean = np.asarray(clean_incidence, dtype=np.int8)
    predicted = np.asarray(predicted_incidence, dtype=np.int8)
    if clean.shape != predicted.shape:
        raise ValueError("clean and predicted incidence matrices must have equal shape")

    precision, recall, f1 = _binary_scores(clean, predicted)
    row_differences = np.not_equal(clean, predicted).sum(axis=1)
    hyperedge_jaccard: list[float] = []
    hyperedge_f1: list[float] = []
    exact_hyperedges: list[bool] = []
    for column in range(clean.shape[1]):
        truth = clean[:, column].astype(bool)
        estimate = predicted[:, column].astype(bool)
        union = int(np.logical_or(truth, estimate).sum())
        intersection = int(np.logical_and(truth, estimate).sum())
        hyperedge_jaccard.append(intersection / union if union else 1.0)
        column_precision, column_recall, column_f1 = _binary_scores(
            truth.astype(np.int8), estimate.astype(np.int8)
        )
        if not truth.any() and not estimate.any():
            column_f1 = 1.0
        hyperedge_f1.append(column_f1)
        exact_hyperedges.append(bool(np.array_equal(truth, estimate)))

    probabilities = predicted.astype(float) if predicted_probabilities is None else predicted_probabilities
    violations = running_intersection_violations(predicted, tree)
    return {
        "clean_precision": precision,
        "clean_recall": recall,
        "clean_f1": f1,
        "hamming_error": float(np.not_equal(clean, predicted).mean()),
        "exact_row_recovery": float(np.equal(clean, predicted).all(axis=1).mean()),
        "mean_symmetric_difference": float(row_differences.mean()),
        "running_intersection_violations": int(violations["num_violating_vertices"]),
        "predicted_density": float(predicted.mean()),
        "clean_density": float(clean.mean()),
        "observed_density": float(np.asarray(observed_incidence).mean()),
        "reconstruction_bce": binary_cross_entropy(probabilities, observed_incidence),
        "average_hyperedge_jaccard": float(np.mean(hyperedge_jaccard)),
        "average_hyperedge_f1": float(np.mean(hyperedge_f1)),
        "exact_hyperedge_recovery": float(np.mean(exact_hyperedges)),
    }

