from __future__ import annotations

import numpy as np

from .sparse_regression import fit_omp


def omp_recovery(design: np.ndarray, response: np.ndarray, *, sparsity: int) -> np.ndarray:
    return fit_omp(design, response, nonzero_terms=sparsity)
