from __future__ import annotations

import numpy as np
from sklearn.linear_model import ElasticNet, Lasso

from .ensemble import RecoveryScenario
from .structure import and_dictionary


def signed_target_metrics(truth: np.ndarray, estimate: np.ndarray, terms: np.ndarray) -> dict[str, float]:
    high = np.asarray([int(term).bit_count() >= 3 for term in terms])
    truth_sign = np.sign(truth[high]).astype(int)
    estimate_sign = np.where(np.abs(estimate[high]) > 1e-9, np.sign(estimate[high]), 0).astype(int)
    true = truth_sign != 0
    selected = estimate_sign != 0
    correct = true & selected & (truth_sign == estimate_sign)
    tp = int(correct.sum())
    fp = int(selected.sum() - tp)
    fn = int(true.sum() - tp)
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        "signed_f1": float(f1),
        "precision": float(precision),
        "recall": float(recall),
        "exact_target_sign": float(np.array_equal(truth_sign, estimate_sign)),
        "sign_errors": int(np.count_nonzero(truth_sign != estimate_sign)),
    }


def simulate_recovery(
    masks: tuple[int, ...],
    scenario: RecoveryScenario,
    *,
    dimension: int = 6,
    estimator: str = "lasso",
    l1_ratio: float = 0.5,
) -> dict[str, float]:
    full, terms = and_dictionary(dimension)
    design = full[np.asarray(masks)]
    scale = np.sqrt(np.mean(design**2, axis=0))
    nonzero = scale > 1e-12
    scaled = np.zeros_like(design)
    scaled[:, nonzero] = design[:, nonzero] / scale[nonzero]
    term_to_col = {int(term): index for index, term in enumerate(terms)}
    truth = np.zeros(len(terms))
    for term, effect in zip(scenario.active, scenario.effects, strict=True):
        truth[term_to_col[term]] = effect
    rng = np.random.default_rng(scenario.noise_seed + 41)
    response = design @ truth + rng.normal(0.0, scenario.sigma, size=len(masks))
    alpha = scenario.sigma * np.sqrt(2.0 * np.log(len(terms)) / len(masks))
    if estimator == "lasso":
        model = Lasso(alpha=alpha, fit_intercept=False, max_iter=20_000)
    elif estimator == "elastic_net":
        model = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, fit_intercept=False, max_iter=20_000)
    else:
        raise ValueError(f"unknown estimator: {estimator}")
    model.fit(scaled, response)
    estimate = np.zeros_like(truth)
    estimate[nonzero] = model.coef_[nonzero] / scale[nonzero]
    return signed_target_metrics(truth, estimate, terms)
