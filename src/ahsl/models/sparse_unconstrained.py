"""Sparsity-regularized independent incidence logits."""

from __future__ import annotations

import torch

from ahsl.models.unconstrained import UnconstrainedIncidence


class SparseUnconstrained(UnconstrainedIncidence):
    """Add a scale-normalized L1 penalty ``lambda_s * mean(P)``.

    Normalization by the number of incidence entries makes a fixed lambda
    comparable across ``n`` and ``m``.
    """

    name = "SparseUnconstrained"

    def __init__(self, lambda_s: float, **kwargs: float | int) -> None:
        super().__init__(**kwargs)
        if lambda_s < 0.0:
            raise ValueError("lambda_s must be non-negative")
        self.lambda_s = lambda_s

    def _regularizer(self, probabilities: torch.Tensor) -> torch.Tensor:
        return self.lambda_s * probabilities.mean()

