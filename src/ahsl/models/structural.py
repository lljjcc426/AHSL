"""Exact non-learned estimators over all connected subtrees."""

from __future__ import annotations

import numpy as np

from ahsl.models.common import repeated_observations


class NearestConnectedSubtree:
    """Project each observed row onto a minimum-Hamming connected subtree.

    Candidate order provides a deterministic tie break; no clean-incidence
    information enters the selection.
    """

    name = "NearestConnectedSubtree"

    def __init__(self, candidates: np.ndarray) -> None:
        self.candidates = np.asarray(candidates, dtype=np.int8)

    def fit(self, observed: np.ndarray) -> "NearestConnectedSubtree":
        repetitions = repeated_observations(observed).astype(np.int8)
        n = repetitions.shape[1]
        prediction = np.empty((n, repetitions.shape[2]), dtype=np.int8)
        minimum_distances = np.empty(n, dtype=float)
        for vertex in range(n):
            distances = np.not_equal(
                self.candidates[:, None, :], repetitions[:, vertex, :][None, :, :]
            ).sum(axis=(1, 2))
            best = int(np.argmin(distances))
            prediction[vertex] = self.candidates[best]
            minimum_distances[vertex] = distances[best]
        self.prediction_ = prediction
        self.train_loss_ = float(minimum_distances.mean() / (repetitions.shape[0] * repetitions.shape[2]))
        return self

    def predict(self) -> np.ndarray:
        return self.prediction_.copy()

    def predict_proba(self) -> np.ndarray:
        return self.prediction_.astype(float)


def _log_probability(probability: float) -> float:
    if probability == 0.0:
        return -np.inf
    return float(np.log(probability))


class NoiseAwareMAPSubtree:
    """Maximum-likelihood connected subtree under known independent flip rates."""

    name = "NoiseAwareMAPSubtree"

    def __init__(
        self,
        candidates: np.ndarray,
        p_false_negative: float,
        p_false_positive: float,
    ) -> None:
        self.candidates = np.asarray(candidates, dtype=np.int8)
        self.p_false_negative = p_false_negative
        self.p_false_positive = p_false_positive

    def fit(self, observed: np.ndarray) -> "NoiseAwareMAPSubtree":
        repetitions = repeated_observations(observed).astype(np.int8)
        if self.p_false_negative == self.p_false_positive:
            probability = self.p_false_negative
            if probability <= 0.5:
                projection = NearestConnectedSubtree(self.candidates).fit(repetitions)
                self.prediction_ = projection.predict()
                mismatch_rate = projection.train_loss_
            else:
                n, m = repetitions.shape[1:]
                prediction = np.empty((n, m), dtype=np.int8)
                maximum_distances = np.empty(n, dtype=float)
                for vertex in range(n):
                    distances = np.not_equal(
                        self.candidates[:, None, :],
                        repetitions[:, vertex, :][None, :, :],
                    ).sum(axis=(1, 2))
                    best = int(np.argmax(distances))
                    prediction[vertex] = self.candidates[best]
                    maximum_distances[vertex] = distances[best]
                self.prediction_ = prediction
                mismatch_rate = float(
                    maximum_distances.mean()
                    / (repetitions.shape[0] * repetitions.shape[2])
                )
            if probability == 0.0:
                self.train_loss_ = 0.0 if mismatch_rate == 0.0 else np.inf
            elif probability == 1.0:
                self.train_loss_ = np.inf if mismatch_rate < 1.0 else 0.0
            else:
                self.train_loss_ = float(
                    -mismatch_rate * np.log(probability)
                    - (1.0 - mismatch_rate) * np.log(1.0 - probability)
                )
            return self

        log_true_observed_one = _log_probability(1.0 - self.p_false_negative)
        log_true_observed_zero = _log_probability(self.p_false_negative)
        log_false_observed_one = _log_probability(self.p_false_positive)
        log_false_observed_zero = _log_probability(1.0 - self.p_false_positive)

        n, m = repetitions.shape[1:]
        prediction = np.empty((n, m), dtype=np.int8)
        best_log_likelihoods = np.empty(n, dtype=float)
        candidate_truth = self.candidates[:, None, :].astype(bool)
        for vertex in range(n):
            row_observations = repetitions[:, vertex, :]
            log_if_true = np.where(
                row_observations[None, :, :] == 1,
                log_true_observed_one,
                log_true_observed_zero,
            )
            log_if_false = np.where(
                row_observations[None, :, :] == 1,
                log_false_observed_one,
                log_false_observed_zero,
            )
            log_likelihoods = np.where(candidate_truth, log_if_true, log_if_false).sum(axis=(1, 2))
            best = int(np.argmax(log_likelihoods))
            prediction[vertex] = self.candidates[best]
            best_log_likelihoods[vertex] = log_likelihoods[best]

        self.prediction_ = prediction
        self.train_loss_ = float(-best_log_likelihoods.mean() / (repetitions.shape[0] * m))
        return self

    def predict(self) -> np.ndarray:
        return self.prediction_.copy()

    def predict_proba(self) -> np.ndarray:
        return self.prediction_.astype(float)
