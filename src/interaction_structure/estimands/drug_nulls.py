from __future__ import annotations

import numpy as np


def bliss_expected_growth(single_growth: np.ndarray) -> np.ndarray:
    """Bliss independence on a relative-growth scale."""
    return np.prod(np.asarray(single_growth, dtype=float), axis=-1)


def highest_single_agent_growth(single_growth: np.ndarray) -> np.ndarray:
    """HSA reference for growth: the most inhibitory single agent."""
    return np.min(np.asarray(single_growth, dtype=float), axis=-1)
