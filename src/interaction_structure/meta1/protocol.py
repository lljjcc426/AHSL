from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from .data import Landscape
from .estimand import zeta_matrix


@dataclass(frozen=True, slots=True)
class RevealedPanel:
    panel_id: str
    landscape_id: str
    dimension: int
    selected_masks: tuple[int, ...]
    replicates: tuple[np.ndarray, ...]
    response_scale: str

    def means(self) -> np.ndarray:
        return np.asarray([np.mean(values) for values in self.replicates], dtype=float)

    def variances(self) -> np.ndarray:
        return np.asarray([np.var(values, ddof=1) if len(values) > 1 else 0.0 for values in self.replicates])

    def design(self, *, max_order: int | None = None) -> tuple[np.ndarray, np.ndarray]:
        full = zeta_matrix(self.dimension)
        terms = np.arange(1 << self.dimension)
        if max_order is not None:
            keep = np.asarray([mask.bit_count() <= max_order for mask in terms])
            return full[np.asarray(self.selected_masks)][:, keep], terms[keep]
        return full[np.asarray(self.selected_masks)], terms


@dataclass(frozen=True, slots=True)
class AcquisitionState:
    dimension: int
    selected_masks: tuple[int, ...]
    revealed_means: tuple[float, ...]
    revealed_variances: tuple[float, ...]


class EvaluationOracle:
    __slots__ = ("_landscape", "_scale")

    def __init__(self, landscape: Landscape, scale: str):
        self._landscape = landscape
        self._scale = scale

    def hidden_response_rmse(self, coefficients: np.ndarray, selected_masks: tuple[int, ...]) -> float:
        transformed = self._landscape.transformed_replicates(self._scale)
        means = np.asarray([np.mean(transformed[mask]) for mask in range(self._landscape.n_cells)])
        predicted = zeta_matrix(self._landscape.dimension) @ coefficients
        hidden = np.asarray([mask not in set(selected_masks) for mask in range(self._landscape.n_cells)])
        return float(np.sqrt(np.mean((predicted[hidden] - means[hidden]) ** 2))) if hidden.any() else 0.0


def reveal(landscape: Landscape, masks: tuple[int, ...], scale: str) -> RevealedPanel:
    transformed = landscape.transformed_replicates(scale)
    return RevealedPanel(
        landscape.panel_id,
        landscape.landscape_id,
        landscape.dimension,
        tuple(sorted(masks)),
        tuple(transformed[mask].copy() for mask in sorted(masks)),
        scale,
    )


def make_measurement_masks(
    n_cells: int,
    budgets: tuple[int, ...],
    seeds: tuple[int, ...],
    *,
    mandatory_masks: tuple[int, ...] = (0,),
) -> pd.DataFrame:
    rows: list[dict[str, int]] = []
    mandatory = set(mandatory_masks)
    candidates = np.asarray([mask for mask in range(n_cells) if mask not in mandatory])
    for seed in seeds:
        rng = np.random.default_rng(seed)
        ordering = rng.permutation(candidates)
        for budget in budgets:
            chosen = sorted(mandatory | set(ordering[: budget - len(mandatory)].tolist()))
            for mask in chosen:
                rows.append({"n_cells": n_cells, "budget": budget, "mask_seed": seed, "community_mask": mask})
    return pd.DataFrame(rows)


def design_balanced_mask(dimension: int, budget: int, seed: int) -> tuple[int, ...]:
    design = zeta_matrix(dimension)
    column_norms = np.linalg.norm(design, axis=0)
    normalized = design / np.maximum(column_norms[None, :], 1e-12)
    rng = np.random.default_rng(seed)
    selected = [0]
    remaining = set(range(1, 1 << dimension))
    first = normalized[0] / np.linalg.norm(normalized[0])
    basis = first[None, :]
    while len(selected) < budget:
        pool = np.asarray(sorted(remaining))
        candidates = normalized[pool]
        residual_energy = np.sum(candidates**2, axis=1) - np.sum((candidates @ basis.T) ** 2, axis=1)
        score = residual_energy + rng.uniform(0, 1e-12, size=len(pool))
        choice = int(pool[np.argmax(score)])
        selected.append(choice)
        remaining.remove(choice)
        residual = normalized[choice] - (normalized[choice] @ basis.T) @ basis
        norm = np.linalg.norm(residual)
        if norm > 1e-10:
            basis = np.vstack([basis, residual / norm])
    return tuple(sorted(selected))


def hybrid_design_mask(dimension: int, budget: int, seed: int, design_fraction: float) -> tuple[int, ...]:
    n_design = max(1, min(budget, int(round(budget * design_fraction))))
    selected = set(design_balanced_mask(dimension, n_design, seed))
    rng = np.random.default_rng(seed + 17)
    remaining = np.asarray([mask for mask in range(1 << dimension) if mask not in selected])
    fill = rng.permutation(remaining)[: budget - len(selected)]
    selected.update(fill.tolist())
    return tuple(sorted(selected))
