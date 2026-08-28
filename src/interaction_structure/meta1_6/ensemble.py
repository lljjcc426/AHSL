from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .structure import partition_terms, validate_development_seed


@dataclass(frozen=True, slots=True)
class RecoveryScenario:
    scenario_id: str
    active: tuple[int, ...]
    signs: tuple[int, ...]
    effects: tuple[float, ...]
    sigma: float
    k_high: int
    k_low: int
    snr: float
    noise_seed: int


def make_support_ensemble(
    dimension: int = 6,
    *,
    seed: int = 1601,
    k_high_values: tuple[int, ...] = (2, 4, 8),
    k_low_values: tuple[int, ...] = (2, 6),
    snr_values: tuple[float, ...] = (0.75, 1.5, 3.0),
    replicates: int = 2,
) -> list[RecoveryScenario]:
    """Outcome-independent, order-balanced support prior used by every design."""
    validate_development_seed(seed)
    terms, low_indices, high_indices = partition_terms(dimension)
    low_terms = terms[low_indices]
    high_terms = terms[high_indices]
    order_groups = {order: high_terms[[int(term).bit_count() == order for term in high_terms]] for order in range(3, dimension + 1)}
    rng = np.random.default_rng(seed)
    scenarios: list[RecoveryScenario] = []
    counter = 0
    for k_high in k_high_values:
        for k_low in k_low_values:
            for snr in snr_values:
                for replicate in range(replicates):
                    high_support: list[int] = []
                    orders = list(order_groups)
                    for index in range(k_high):
                        group = order_groups[orders[index % len(orders)]]
                        available = np.asarray([term for term in group if int(term) not in high_support])
                        if available.size == 0:
                            available = np.asarray([term for term in high_terms if int(term) not in high_support])
                        high_support.append(int(rng.choice(available)))
                    low_support = rng.choice(low_terms, size=k_low, replace=False).astype(int).tolist()
                    active = tuple(low_support + high_support)
                    signs = tuple(int(value) for value in rng.choice((-1, 1), size=len(active)))
                    effects = tuple(float(snr * sign) for sign in signs)
                    scenarios.append(
                        RecoveryScenario(
                            scenario_id=f"pi_{counter:03d}",
                            active=active,
                            signs=signs,
                            effects=effects,
                            sigma=1.0,
                            k_high=k_high,
                            k_low=k_low,
                            snr=snr,
                            noise_seed=seed * 10_000 + counter * 97 + replicate,
                        )
                    )
                    counter += 1
    return scenarios


def prior_variant(name: str, seed: int = 1611) -> list[RecoveryScenario]:
    variants = {
        "sparser": dict(k_high_values=(2, 4), k_low_values=(2, 4), snr_values=(0.75, 1.5, 3.0)),
        "primary": dict(k_high_values=(2, 4, 8), k_low_values=(2, 6), snr_values=(0.75, 1.5, 3.0)),
        "denser": dict(k_high_values=(4, 8, 12), k_low_values=(6, 10), snr_values=(0.75, 1.5, 3.0)),
        "weak": dict(k_high_values=(2, 4, 8), k_low_values=(2, 6), snr_values=(0.5, 0.75, 1.0)),
    }
    if name not in variants:
        raise ValueError(f"unknown prior variant: {name}")
    return make_support_ensemble(seed=seed, replicates=1, **variants[name])
