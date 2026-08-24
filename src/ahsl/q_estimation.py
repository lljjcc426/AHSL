"""One-dimensional likelihood estimation for the subtree branch probability."""

from __future__ import annotations

from dataclasses import dataclass

import networkx as nx
import numpy as np
from scipy.optimize import minimize_scalar

from ahsl.models.noise_likelihood import node_log_likelihoods
from ahsl.subtree_marginal import marginal_log_likelihood_from_node_logs


@dataclass(frozen=True)
class QEstimate:
    q: float
    log_likelihood: float
    evaluations: int


def estimate_q_mle(
    tree: nx.Graph,
    observed: np.ndarray,
    p_false_negative: float,
    p_false_positive: float,
    bounds: tuple[float, float] = (0.02, 0.98),
    grid_size: int = 21,
) -> QEstimate:
    """Maximize exact observed likelihood using a coarse grid plus refinement."""
    lower, upper = bounds
    if not 0.0 < lower < upper < 1.0:
        raise ValueError("q bounds must satisfy 0 < lower < upper < 1")
    log_zero, log_one, _ = node_log_likelihoods(
        observed, p_false_negative, p_false_positive
    )

    evaluations = 0

    def score(q: float) -> float:
        nonlocal evaluations
        evaluations += 1
        return marginal_log_likelihood_from_node_logs(
            tree, log_zero, log_one, q
        ).log_likelihood

    grid = np.linspace(lower, upper, grid_size)
    grid_scores = np.array([score(float(q)) for q in grid])
    best_index = int(np.argmax(grid_scores))
    refine_lower = float(grid[max(0, best_index - 1)])
    refine_upper = float(grid[min(grid_size - 1, best_index + 1)])
    refined = minimize_scalar(
        lambda q: -score(float(q)),
        bounds=(refine_lower, refine_upper),
        method="bounded",
        options={"xatol": 1e-5, "maxiter": 80},
    )
    refined_q = float(refined.x)
    refined_score = -float(refined.fun)
    if float(grid_scores[best_index]) >= refined_score:
        return QEstimate(
            float(grid[best_index]), float(grid_scores[best_index]), evaluations
        )
    return QEstimate(refined_q, refined_score, evaluations)

