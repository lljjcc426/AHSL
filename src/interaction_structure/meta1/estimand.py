from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations

import numpy as np
import pandas as pd

from .data import Landscape


def mobius_matrix(dimension: int) -> np.ndarray:
    size = 1 << dimension
    matrix = np.zeros((size, size), dtype=float)
    for upper in range(size):
        for lower in range(size):
            if lower & ~upper == 0:
                matrix[upper, lower] = (-1.0) ** (upper.bit_count() - lower.bit_count())
    return matrix


def zeta_matrix(dimension: int) -> np.ndarray:
    return np.linalg.inv(mobius_matrix(dimension))


def transform_matrix(values: np.ndarray, dimension: int) -> np.ndarray:
    return mobius_matrix(dimension) @ np.asarray(values, dtype=float)


@dataclass(frozen=True)
class ReferenceEstimand:
    landscape_id: str
    panel_id: str
    scale: str
    coefficients: np.ndarray
    lower: np.ndarray
    upper: np.ndarray
    sign_stability: np.ndarray
    support_sign: np.ndarray
    practical_threshold: float
    bootstrap_seed: int
    n_bootstrap: int

    @property
    def pure_high_order(self) -> np.ndarray:
        pure = np.zeros_like(self.support_sign, dtype=bool)
        active = set(np.flatnonzero(self.support_sign))
        for raw_mask in active:
            mask = int(raw_mask)
            order = mask.bit_count()
            if order < 3:
                continue
            parents = {mask ^ (1 << bit) for bit in range(mask.bit_length()) if mask & (1 << bit)}
            pure[mask] = not bool(parents & active)
        return pure

    def to_frame(self) -> pd.DataFrame:
        return pd.DataFrame(
            {
                "panel_id": self.panel_id,
                "landscape_id": self.landscape_id,
                "response_scale": self.scale,
                "term_mask": np.arange(len(self.coefficients)),
                "order": [mask.bit_count() for mask in range(len(self.coefficients))],
                "coefficient": self.coefficients,
                "ci_lower": self.lower,
                "ci_upper": self.upper,
                "sign_stability": self.sign_stability,
                "support_sign": self.support_sign,
                "pure_hoi": self.pure_high_order,
                "practical_threshold": self.practical_threshold,
                "bootstrap_seed": self.bootstrap_seed,
                "n_bootstrap": self.n_bootstrap,
            }
        )


def practical_effect_threshold(landscape: Landscape, scale: str, transformed: dict[int, np.ndarray]) -> float:
    if landscape.panel_id == "ishizawa" and scale == "log10":
        return 0.10
    nonempty = np.concatenate([values for mask, values in transformed.items() if mask != 0])
    return 0.05 * float(np.median(np.abs(nonempty)))


def build_reference_estimand(
    landscape: Landscape,
    *,
    scale: str,
    n_bootstrap: int = 1000,
    seed: int = 20260828,
) -> ReferenceEstimand:
    transformed = landscape.transformed_replicates(scale)
    size = landscape.n_cells
    matrix = mobius_matrix(landscape.dimension)
    cell_means = np.asarray([np.mean(transformed[mask]) for mask in range(size)])
    point = matrix @ cell_means
    rng = np.random.default_rng(seed)
    bootstrap_means = np.empty((n_bootstrap, size), dtype=float)
    for mask in range(size):
        values = transformed[mask]
        indices = rng.integers(0, len(values), size=(n_bootstrap, len(values)))
        bootstrap_means[:, mask] = values[indices].mean(axis=1)
    bootstrap_coefficients = bootstrap_means @ matrix.T
    lower, upper = np.quantile(bootstrap_coefficients, [0.025, 0.975], axis=0)
    positive_frequency = np.mean(bootstrap_coefficients > 0, axis=0)
    negative_frequency = np.mean(bootstrap_coefficients < 0, axis=0)
    stability = np.maximum(positive_frequency, negative_frequency)
    threshold = practical_effect_threshold(landscape, scale, transformed)
    supported = (np.abs(point) >= threshold) & ((lower > 0) | (upper < 0))
    support_sign = np.where(supported, np.sign(point), 0).astype(int)
    return ReferenceEstimand(
        landscape.landscape_id,
        landscape.panel_id,
        scale,
        point,
        lower,
        upper,
        stability,
        support_sign,
        threshold,
        seed,
        n_bootstrap,
    )


def jaccard(left: np.ndarray, right: np.ndarray) -> float:
    a = set(np.flatnonzero(left))
    b = set(np.flatnonzero(right))
    return len(a & b) / len(a | b) if a | b else 1.0


def pairwise_stability(references: list[ReferenceEstimand]) -> tuple[float, float]:
    values = [
        jaccard(left.support_sign, right.support_sign)
        for left, right in combinations(references, 2)
    ]
    return float(np.median(values)), float(np.min(values))
