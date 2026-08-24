"""Independent false-negative and false-positive incidence corruption."""

from __future__ import annotations

import numpy as np


def corrupt_incidence(
    clean_incidence: np.ndarray,
    p_false_negative: float,
    p_false_positive: float,
    seed: int,
) -> dict[str, np.ndarray | int]:
    """Flip clean incidences under the independent asymmetric noise model.

    True entries are removed with probability ``p_false_negative`` and absent
    entries are inserted with probability ``p_false_positive``. The corrupted
    output is not repaired to satisfy alpha-acyclicity.
    """
    if not 0.0 <= p_false_negative <= 1.0:
        raise ValueError("p_false_negative must lie in [0, 1]")
    if not 0.0 <= p_false_positive <= 1.0:
        raise ValueError("p_false_positive must lie in [0, 1]")

    clean = np.asarray(clean_incidence, dtype=np.int8)
    if clean.ndim != 2:
        raise ValueError("clean_incidence must be a matrix")
    rng = np.random.default_rng(seed)
    draws = rng.random(clean.shape)
    false_negative_mask = (clean == 1) & (draws < p_false_negative)
    false_positive_mask = (clean == 0) & (draws < p_false_positive)
    corrupted = clean.copy()
    corrupted[false_negative_mask] = 0
    corrupted[false_positive_mask] = 1
    return {
        "corrupted_incidence": corrupted,
        "false_negative_mask": false_negative_mask,
        "false_positive_mask": false_positive_mask,
        "num_flipped": int(false_negative_mask.sum() + false_positive_mask.sum()),
    }

