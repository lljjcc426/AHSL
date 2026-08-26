from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from sklearn.linear_model import Lasso, OrthogonalMatchingPursuit


@dataclass(frozen=True)
class SparseFit:
    coefficients: np.ndarray
    alpha: float
    validation_mse: float
    converged: bool


def fit_lasso_grid(
    design_train: np.ndarray,
    y_train: np.ndarray,
    design_validation: np.ndarray,
    y_validation: np.ndarray,
    *,
    alphas: tuple[float, ...] = (1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2, 1e-1),
    seed: int = 20260827,
) -> SparseFit:
    best: SparseFit | None = None
    for alpha in alphas:
        model = Lasso(alpha=alpha, fit_intercept=False, max_iter=20_000, selection="cyclic", random_state=seed)
        model.fit(design_train, y_train)
        mse = float(np.mean((model.predict(design_validation) - y_validation) ** 2))
        candidate = SparseFit(model.coef_.copy(), alpha, mse, model.n_iter_ < model.max_iter)
        if best is None or candidate.validation_mse < best.validation_mse:
            best = candidate
    assert best is not None
    return best


def fit_omp(design: np.ndarray, y: np.ndarray, *, nonzero_terms: int) -> np.ndarray:
    model = OrthogonalMatchingPursuit(
        n_nonzero_coefs=min(nonzero_terms, design.shape[0] - 1, design.shape[1]),
        fit_intercept=False,
    )
    model.fit(design, y)
    return model.coef_.copy()


def select_omp_sparsity(
    design_train: np.ndarray,
    y_train: np.ndarray,
    design_validation: np.ndarray,
    y_validation: np.ndarray,
    *,
    candidates: tuple[int, ...] = (2, 4, 8, 12, 16, 24),
) -> tuple[int, float]:
    best_sparsity = candidates[0]
    best_mse = np.inf
    for sparsity in candidates:
        coefficients = fit_omp(design_train, y_train, nonzero_terms=sparsity)
        mse = float(np.mean((design_validation @ coefficients - y_validation) ** 2))
        if mse < best_mse:
            best_sparsity, best_mse = sparsity, mse
    return best_sparsity, best_mse
