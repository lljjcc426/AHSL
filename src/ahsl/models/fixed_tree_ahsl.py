"""Exact-candidate fixed-tree AHSL model."""

from __future__ import annotations

import numpy as np
import torch
from torch.nn import functional as F

from ahsl.models.common import repeated_observations
from ahsl.reproducibility import set_all_seeds


class FixedTreeAHSL:
    """Learn a categorical distribution over every connected subtree per row.

    The soft prediction lies in the convex hull of connected-subtree incidence
    vectors. Discrete inference selects one candidate, so its row support is
    connected exactly, without repair or an acyclicity penalty.
    """

    name = "FixedTreeAHSL"

    def __init__(
        self,
        candidates: np.ndarray,
        epochs: int = 150,
        learning_rate: float = 0.1,
        entropy_weight: float = 0.0,
        size_weight: float = 0.0,
        seed: int = 0,
    ) -> None:
        candidate_array = np.asarray(candidates, dtype=np.float32)
        if candidate_array.ndim != 2 or candidate_array.shape[0] == 0:
            raise ValueError("candidates must be a non-empty matrix")
        self.candidates = candidate_array
        self.epochs = epochs
        self.learning_rate = learning_rate
        self.entropy_weight = entropy_weight
        self.size_weight = size_weight
        self.seed = seed

    def fit(self, observed: np.ndarray) -> "FixedTreeAHSL":
        set_all_seeds(self.seed)
        target_numpy = repeated_observations(observed).mean(axis=0)
        if target_numpy.shape[1] != self.candidates.shape[1]:
            raise ValueError("candidate width must match observed incidence width")
        target = torch.as_tensor(target_numpy, dtype=torch.float32)
        candidate_tensor = torch.as_tensor(self.candidates, dtype=torch.float32)
        logits = torch.nn.Parameter(torch.zeros((target.shape[0], candidate_tensor.shape[0])))
        optimizer = torch.optim.Adam([logits], lr=self.learning_rate)
        final_loss = torch.zeros(())

        for _ in range(self.epochs):
            optimizer.zero_grad()
            distribution = torch.softmax(logits, dim=1)
            probabilities = distribution @ candidate_tensor
            reconstruction = F.binary_cross_entropy(probabilities, target)
            entropy = -(distribution * torch.log(distribution.clamp_min(1e-12))).sum(dim=1).mean()
            expected_size = (distribution @ candidate_tensor.sum(dim=1)).mean()
            final_loss = (
                reconstruction
                + self.entropy_weight * entropy
                + self.size_weight * expected_size
            )
            final_loss.backward()
            optimizer.step()

        with torch.no_grad():
            distribution = torch.softmax(logits, dim=1)
            probabilities = distribution @ candidate_tensor
            choices = distribution.argmax(dim=1)
        self.logits_ = logits.detach()
        self.distribution_ = distribution.cpu().numpy()
        self.probabilities_ = probabilities.cpu().numpy()
        self.prediction_ = self.candidates[choices.cpu().numpy()].astype(np.int8)
        self.train_loss_ = float(final_loss.detach())
        return self

    def predict(self) -> np.ndarray:
        return self.prediction_.copy()

    def predict_proba(self) -> np.ndarray:
        return self.probabilities_.copy()

