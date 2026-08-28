from __future__ import annotations

import numpy as np
from sklearn.metrics import average_precision_score

from .estimand import ReferenceEstimand


def signed_support_metrics(
    reference: ReferenceEstimand,
    coefficients: np.ndarray,
    selected: np.ndarray,
) -> dict[str, float]:
    orders = np.asarray([mask.bit_count() for mask in range(len(coefficients))])
    high = orders >= 3
    truth_sign = reference.support_sign[high]
    predicted_sign = np.where(selected[high], np.sign(coefficients[high]), 0).astype(int)
    truth = truth_sign != 0
    predicted = predicted_sign != 0
    correct = predicted & truth & (predicted_sign == truth_sign)
    tp = int(correct.sum())
    fp = int(predicted.sum() - tp)
    fn = int(truth.sum() - tp)
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    pure = reference.pure_high_order[high]
    pure_recall = float(np.mean(correct[pure])) if pure.any() else np.nan
    return {
        "primary_f1": float(f1),
        "precision": float(precision),
        "recall": float(recall),
        "average_precision": float(average_precision_score(truth, np.abs(coefficients[high]))),
        "empirical_fdr": float(fp / (tp + fp)) if tp + fp else 0.0,
        "pure_hoi_recall": pure_recall,
        "coefficient_rmse": float(np.sqrt(np.mean((coefficients[high] - reference.coefficients[high]) ** 2))),
        "true_support": int(truth.sum()),
        "selected_support": int(predicted.sum()),
        "sign_flips": int((predicted & truth & (predicted_sign != truth_sign)).sum()),
        "false_hoi": int((predicted & ~truth).sum()),
        "missed_positive_hoi": int(((truth_sign > 0) & ~correct).sum()),
        "missed_negative_hoi": int(((truth_sign < 0) & ~correct).sum()),
        "pure_hoi_miss": int((pure & ~correct).sum()),
    }
