from __future__ import annotations

from itertools import combinations

import numpy as np


RETIRED_RESERVE_SEEDS = frozenset({505, 606})


def validate_development_seed(seed: int) -> None:
    """Keep retired reserve seeds outside every META1.6 development path."""
    if int(seed) in RETIRED_RESERVE_SEEDS:
        raise ValueError("META1.6 forbids retired reserve seeds 505 and 606")


def boolean_rows(dimension: int) -> np.ndarray:
    masks = np.arange(1 << dimension, dtype=np.int64)
    return ((masks[:, None] >> np.arange(dimension)) & 1).astype(np.int8)


def and_dictionary(dimension: int) -> tuple[np.ndarray, np.ndarray]:
    """Return the Boolean AND dictionary for all rows and 63 nonempty terms."""
    rows = np.arange(1 << dimension, dtype=np.int64)
    terms = np.arange(1, 1 << dimension, dtype=np.int64)
    matrix = ((rows[:, None] & terms[None, :]) == terms[None, :]).astype(float)
    return matrix, terms


def partition_terms(dimension: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    terms = np.arange(1, 1 << dimension, dtype=np.int64)
    orders = np.asarray([int(term).bit_count() for term in terms])
    return terms, np.flatnonzero(orders <= 2), np.flatnonzero(orders >= 3)


def numerical_rank(matrix: np.ndarray, relative_tolerance: float = 1e-9) -> int:
    if matrix.size == 0:
        return 0
    singular = np.linalg.svd(matrix, compute_uv=False)
    if singular.size == 0 or singular[0] <= 1e-9:
        return 0
    threshold = max(1e-9, relative_tolerance * singular[0])
    return int(np.count_nonzero(singular > threshold))


def residualize_targets(
    selected_matrix: np.ndarray,
    low_indices: np.ndarray,
    high_indices: np.ndarray,
    *,
    ridge: float = 0.0,
) -> np.ndarray:
    low = selected_matrix[:, low_indices]
    high = selected_matrix[:, high_indices]
    if ridge == 0:
        fitted = low @ np.linalg.pinv(low) @ high
    else:
        gram = low.T @ low + ridge * np.eye(low.shape[1])
        fitted = low @ np.linalg.solve(gram, low.T @ high)
    return high - fitted


def _alias_pairs(matrix: np.ndarray, left: np.ndarray, right: np.ndarray, same: bool) -> int:
    count = 0
    for offset, first in enumerate(left):
        start = offset + 1 if same else 0
        for second in right[start:]:
            if np.array_equal(matrix[:, first], matrix[:, second]):
                count += 1
    return count


def _mutual_coherence(matrix: np.ndarray) -> float:
    norms = np.linalg.norm(matrix, axis=0)
    keep = norms > 1e-12
    if np.count_nonzero(keep) < 2:
        return 1.0
    normalized = matrix[:, keep] / norms[keep]
    gram = np.abs(normalized.T @ normalized)
    np.fill_diagonal(gram, 0.0)
    return float(np.max(gram))


def structural_diagnostics(dimension: int, masks: tuple[int, ...], *, ridge: float = 0.0) -> dict[str, float | int]:
    full, _ = and_dictionary(dimension)
    _, low, high = partition_terms(dimension)
    selected = full[np.asarray(masks)]
    target = selected[:, high]
    residual = residualize_targets(selected, low, high, ridge=ridge)
    residual_norm = np.linalg.norm(residual, axis=0)
    residual_singular = np.linalg.svd(residual, compute_uv=False)
    positive = residual_singular[residual_singular > 1e-9 * (residual_singular[0] if residual_singular.size else 1.0)]
    restricted_min = float(positive[-1]) if positive.size else 0.0
    return {
        "budget": len(masks),
        "rank_full": numerical_rank(selected),
        "rank_low": numerical_rank(selected[:, low]),
        "rank_target": numerical_rank(target),
        "rank_residual_target": numerical_rank(residual),
        "zero_target_columns": int(np.count_nonzero(np.linalg.norm(target, axis=0) <= 1e-12)),
        "zero_residual_target_columns": int(np.count_nonzero(residual_norm <= 1e-9)),
        "target_target_alias_pairs": _alias_pairs(selected, high, high, True),
        "target_low_alias_pairs": _alias_pairs(selected, high, low, False),
        "target_coherence": _mutual_coherence(target),
        "residual_target_coherence": _mutual_coherence(residual),
        "residual_restricted_min_sv": restricted_min,
        "residual_nullity": int(len(high) - numerical_rank(residual)),
    }


def sparse_nullspace_diagnostics(
    dimension: int,
    masks: tuple[int, ...],
    *,
    max_exact_sparsity: int = 3,
    sampled_four_sets: int = 512,
    seed: int = 0,
) -> dict[str, int | float]:
    full, _ = and_dictionary(dimension)
    _, _, high = partition_terms(dimension)
    target = full[np.asarray(masks)][:, high]
    zero = int(np.count_nonzero(np.linalg.norm(target, axis=0) <= 1e-12))
    dependent: dict[int, int] = {1: zero}
    total: dict[int, int] = {1: target.shape[1]}
    for size in range(2, max_exact_sparsity + 1):
        dependent[size] = 0
        total[size] = 0
        for subset in combinations(range(target.shape[1]), size):
            total[size] += 1
            block = target[:, subset]
            if numerical_rank(block) < size:
                dependent[size] += 1
    rng = np.random.default_rng(seed)
    dependent[4] = 0
    total[4] = sampled_four_sets
    for _ in range(sampled_four_sets):
        subset = rng.choice(target.shape[1], size=4, replace=False)
        if numerical_rank(target[:, subset]) < 4:
            dependent[4] += 1
    output: dict[str, int | float] = {}
    for size in sorted(total):
        output[f"q{size}_tested"] = total[size]
        output[f"q{size}_dependent"] = dependent[size]
        output[f"q{size}_dependent_rate"] = dependent[size] / total[size]
    return output
