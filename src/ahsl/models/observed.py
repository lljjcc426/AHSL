"""Raw observed-incidence baseline."""

from __future__ import annotations

import numpy as np

from ahsl.models.common import repeated_observations


class ObservedBaseline:
    """Return the observation, or majority incidence across repeated observations."""

    name = "ObservedBaseline"

    def fit(self, observed: np.ndarray) -> "ObservedBaseline":
        repetitions = repeated_observations(observed)
        self.probabilities_ = repetitions.mean(axis=0)
        self.prediction_ = (self.probabilities_ >= 0.5).astype(np.int8)
        self.train_loss_ = 0.0
        return self

    def predict(self) -> np.ndarray:
        return self.prediction_.copy()

    def predict_proba(self) -> np.ndarray:
        return self.probabilities_.copy()

