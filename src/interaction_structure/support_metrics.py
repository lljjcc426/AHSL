from __future__ import annotations

import numpy as np
from sklearn.metrics import average_precision_score, precision_recall_fscore_support


def binary_support_metrics(truth: np.ndarray, scores: np.ndarray, selected: np.ndarray) -> dict[str, float]:
    truth = np.asarray(truth, dtype=bool)
    selected = np.asarray(selected, dtype=bool)
    precision, recall, f1, _ = precision_recall_fscore_support(
        truth, selected, average="binary", zero_division=0
    )
    return {
        "precision": float(precision),
        "recall": float(recall),
        "f1": float(f1),
        "average_precision": float(average_precision_score(truth, np.asarray(scores, dtype=float))),
    }


def support_stability(a: dict, b: dict, *, threshold_a: float, threshold_b: float) -> dict[str, float]:
    common = sorted(set(a) & set(b), key=lambda x: (len(x), tuple(sorted(map(str, x)))))
    support_a = {key for key in common if abs(a[key]) >= threshold_a}
    support_b = {key for key in common if abs(b[key]) >= threshold_b}
    overlap = support_a & support_b
    union = support_a | support_b
    sign_agreement = np.mean([np.sign(a[key]) == np.sign(b[key]) for key in overlap]) if overlap else np.nan
    return {
        "support_a": len(support_a),
        "support_b": len(support_b),
        "overlap": len(overlap),
        "jaccard": len(overlap) / len(union) if union else 1.0,
        "sign_agreement": float(sign_agreement),
    }
