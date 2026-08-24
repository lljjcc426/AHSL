"""Small shared utilities for incidence estimators."""

from __future__ import annotations

import numpy as np


def repeated_observations(observed: np.ndarray) -> np.ndarray:
    """Normalize one or repeated incidence observations to shape ``(R, n, m)``."""
    array = np.asarray(observed, dtype=np.float32)
    if array.ndim == 2:
        return array[None, ...]
    if array.ndim == 3:
        return array
    raise ValueError("observed incidence must have shape (n, m) or (R, n, m)")

