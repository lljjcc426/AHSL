"""Exact nodewise likelihoods for the independent incidence-noise channel."""

from __future__ import annotations

import numpy as np

from ahsl.models.common import repeated_observations


def _bernoulli_sequence_log_likelihood(
    observed_ones: np.ndarray,
    repetitions: int,
    probability_of_one: float,
) -> np.ndarray:
    observed_zeros = repetitions - observed_ones
    if probability_of_one == 0.0:
        return np.where(observed_ones == 0, 0.0, -np.inf)
    if probability_of_one == 1.0:
        return np.where(observed_zeros == 0, 0.0, -np.inf)
    return (
        observed_ones * np.log(probability_of_one)
        + observed_zeros * np.log1p(-probability_of_one)
    )


def node_log_likelihoods(
    observed: np.ndarray,
    p_false_negative: float,
    p_false_positive: float,
) -> tuple[np.ndarray, np.ndarray, int]:
    """Return log likelihoods for latent states zero and one at every entry."""
    if not 0.0 <= p_false_negative <= 1.0:
        raise ValueError("p_false_negative must lie in [0, 1]")
    if not 0.0 <= p_false_positive <= 1.0:
        raise ValueError("p_false_positive must lie in [0, 1]")
    repetitions = repeated_observations(observed).astype(np.int8)
    count = repetitions.shape[0]
    observed_ones = repetitions.sum(axis=0)
    log_if_zero = _bernoulli_sequence_log_likelihood(
        observed_ones, count, p_false_positive
    )
    log_if_one = _bernoulli_sequence_log_likelihood(
        observed_ones, count, 1.0 - p_false_negative
    )
    impossible = np.isneginf(log_if_zero) & np.isneginf(log_if_one)
    if impossible.any():
        row, column = np.argwhere(impossible)[0]
        raise ValueError(
            "observations have zero likelihood under both latent states at "
            f"row={row}, column={column}"
        )
    return log_if_zero, log_if_one, count

