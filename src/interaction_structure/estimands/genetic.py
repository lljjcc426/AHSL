from __future__ import annotations

import numpy as np


def multiplicative_epsilon(observed_fitness: np.ndarray, component_fitness: np.ndarray) -> np.ndarray:
    """Deviation from independent multiplicative fitness."""
    return np.asarray(observed_fitness, dtype=float) - np.prod(np.asarray(component_fitness, dtype=float), axis=-1)


def tau_sga(raw_trigenic_epsilon: np.ndarray, epsilon_ik: np.ndarray, epsilon_jk: np.ndarray, fitness_i: np.ndarray, fitness_j: np.ndarray) -> np.ndarray:
    """Published tau-SGA adjustment used for matched trigenic screens."""
    return (
        np.asarray(raw_trigenic_epsilon, dtype=float)
        - np.asarray(epsilon_ik, dtype=float) * np.asarray(fitness_j, dtype=float)
        - np.asarray(epsilon_jk, dtype=float) * np.asarray(fitness_i, dtype=float)
    )
