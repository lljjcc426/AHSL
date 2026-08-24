"""Independent learnable incidence logits without tree information."""

from __future__ import annotations

import numpy as np
import torch
from torch.nn import functional as F

from ahsl.models.common import repeated_observations
from ahsl.reproducibility import set_all_seeds


class UnconstrainedIncidence:
    """Fit one free Bernoulli logit per incidence entry."""

    name = "UnconstrainedIncidence"

    def __init__(
        self,
        epochs: int = 150,
        learning_rate: float = 0.1,
        threshold: float = 0.5,
        seed: int = 0,
    ) -> None:
        self.epochs = epochs
        self.learning_rate = learning_rate
        self.threshold = threshold
        self.seed = seed

    def _regularizer(self, probabilities: torch.Tensor) -> torch.Tensor:
        return torch.zeros((), dtype=probabilities.dtype)

    def fit(self, observed: np.ndarray) -> "UnconstrainedIncidence":
        set_all_seeds(self.seed)
        target_numpy = repeated_observations(observed).mean(axis=0)
        target = torch.as_tensor(target_numpy, dtype=torch.float32)
        logits = torch.nn.Parameter(torch.zeros_like(target))
        optimizer = torch.optim.Adam([logits], lr=self.learning_rate)
        final_loss = torch.zeros(())
        for _ in range(self.epochs):
            optimizer.zero_grad()
            probabilities = torch.sigmoid(logits)
            final_loss = F.binary_cross_entropy_with_logits(logits, target)
            final_loss = final_loss + self._regularizer(probabilities)
            final_loss.backward()
            optimizer.step()

        self.logits_ = logits.detach()
        self.probabilities_ = torch.sigmoid(self.logits_).cpu().numpy()
        self.train_loss_ = float(final_loss.detach())
        return self

    def predict(self) -> np.ndarray:
        return (self.probabilities_ >= self.threshold).astype(np.int8)

    def predict_proba(self) -> np.ndarray:
        return self.probabilities_.copy()

