from __future__ import annotations

from collections.abc import Mapping
from enum import StrEnum

import numpy as np

from .estimands.mobius import Subset, mobius_transform


class SupportLabel(StrEnum):
    STRONG_POSITIVE = "STRONG_POSITIVE"
    STRONG_NEGATIVE = "STRONG_NEGATIVE"
    UNCERTAIN_OR_NULL = "UNCERTAIN_OR_NULL"
    UNKNOWN = "UNKNOWN"


def label_from_interval(lower: float, upper: float, *, minimum_magnitude: float = 0.0) -> SupportLabel:
    if lower > 0 and lower >= minimum_magnitude:
        return SupportLabel.STRONG_POSITIVE
    if upper < 0 and -upper >= minimum_magnitude:
        return SupportLabel.STRONG_NEGATIVE
    return SupportLabel.UNCERTAIN_OR_NULL


def bootstrap_mobius(
    replicates: Mapping[Subset, np.ndarray],
    universe: tuple[str, ...],
    *,
    n_bootstrap: int = 500,
    seed: int = 20260827,
) -> dict[Subset, np.ndarray]:
    """Bootstrap full-factorial coefficients by resampling each measured cell."""
    rng = np.random.default_rng(seed)
    output = {subset: np.empty(n_bootstrap) for subset in replicates}
    for draw in range(n_bootstrap):
        means = {
            subset: float(np.mean(rng.choice(values, size=len(values), replace=True)))
            for subset, values in replicates.items()
        }
        coefficients = mobius_transform(means, universe)
        for subset, value in coefficients.items():
            output[subset][draw] = value
    return output
