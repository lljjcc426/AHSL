"""Noise-aware estimators without a connected-subtree constraint."""

from __future__ import annotations

import numpy as np

from ahsl.models.noise_likelihood import node_log_likelihoods


def _equal(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    return np.isclose(left, right, rtol=1e-12, atol=1e-12)


class NoiseAwareIndependentMLE:
    """Select every latent incidence independently by exact likelihood."""

    name = "NoiseAwareIndependentMLE"

    def __init__(self, p_false_negative: float, p_false_positive: float) -> None:
        self.p_false_negative = p_false_negative
        self.p_false_positive = p_false_positive

    def fit(self, observed: np.ndarray) -> "NoiseAwareIndependentMLE":
        log_zero, log_one, repetitions = node_log_likelihoods(
            observed, self.p_false_negative, self.p_false_positive
        )
        ties = _equal(log_zero, log_one)
        prediction = (log_one > log_zero) & ~ties
        chosen = np.where(prediction, log_one, log_zero)
        self.prediction_ = prediction.astype(np.int8)
        self.row_objectives_ = chosen.sum(axis=1)
        self.row_ties_ = ties.any(axis=1)
        self.optimal_tie_fraction_ = float(self.row_ties_.mean())
        self.selected_sizes_ = self.prediction_.sum(axis=1)
        self.train_loss_ = float(
            -self.row_objectives_.mean() / (repetitions * prediction.shape[1])
        )
        self.log_if_zero_ = log_zero
        self.log_if_one_ = log_one
        return self

    def predict(self) -> np.ndarray:
        return self.prediction_.copy()

    def predict_proba(self) -> np.ndarray:
        return self.prediction_.astype(float)


class NoiseAwareIndependentNonemptyMLE(NoiseAwareIndependentMLE):
    """Independent MLE plus only the requirement that each row is non-empty."""

    name = "NoiseAwareIndependentNonemptyMLE"

    def fit(self, observed: np.ndarray) -> "NoiseAwareIndependentNonemptyMLE":
        super().fit(observed)
        for row in range(self.prediction_.shape[0]):
            if self.prediction_[row].any():
                continue
            advantages = self.log_if_one_[row] - self.log_if_zero_[row]
            feasible = np.isfinite(self.log_if_one_[row])
            if not feasible.any():
                raise ValueError("no positive-likelihood non-empty row exists")
            best_advantage = np.max(advantages[feasible])
            tied_nodes = np.flatnonzero(
                feasible
                & np.isclose(
                    advantages,
                    best_advantage,
                    rtol=1e-12,
                    atol=1e-12,
                )
            )
            selected = int(tied_nodes[0])
            self.prediction_[row, selected] = 1
            self.row_objectives_[row] += advantages[selected]
            self.row_ties_[row] |= len(tied_nodes) > 1
        self.selected_sizes_ = self.prediction_.sum(axis=1)
        self.optimal_tie_fraction_ = float(self.row_ties_.mean())
        repetitions = 1 if np.asarray(observed).ndim == 2 else np.asarray(observed).shape[0]
        self.train_loss_ = float(
            -self.row_objectives_.mean()
            / (repetitions * self.prediction_.shape[1])
        )
        return self

