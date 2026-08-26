from __future__ import annotations

from collections.abc import Hashable, Iterable, Mapping
from itertools import combinations

import numpy as np

Subset = frozenset[Hashable]


def powerset(items: Iterable[Hashable]) -> list[Subset]:
    ordered = tuple(items)
    return [
        frozenset(group)
        for size in range(len(ordered) + 1)
        for group in combinations(ordered, size)
    ]


def mobius_transform(values: Mapping[Subset, float], universe: Iterable[Hashable] | None = None) -> dict[Subset, float]:
    """Return beta_S = sum_{T subset S} (-1)^(|S|-|T|) f(T)."""
    items = tuple(universe) if universe is not None else tuple(sorted(set().union(*values), key=str))
    subsets = powerset(items)
    missing = [subset for subset in subsets if subset not in values]
    if missing:
        raise ValueError(f"complete factorial required; {len(missing)} subsets are missing")
    return {
        subset: float(
            sum(
                (-1) ** (len(subset) - len(lower)) * values[lower]
                for lower in powerset(subset)
            )
        )
        for subset in subsets
    }


def inverse_mobius(coefficients: Mapping[Subset, float], universe: Iterable[Hashable] | None = None) -> dict[Subset, float]:
    """Invert a Boolean-lattice Möbius transform."""
    items = tuple(universe) if universe is not None else tuple(sorted(set().union(*coefficients), key=str))
    return {
        subset: float(sum(coefficients.get(lower, 0.0) for lower in powerset(subset)))
        for subset in powerset(items)
    }


def interaction_dictionary(
    observed_sets: Iterable[Subset],
    universe: Iterable[Hashable],
    *,
    max_order: int | None = None,
) -> tuple[np.ndarray, list[Subset]]:
    """Incidence design for f(A)=sum_{S subset A} beta_S."""
    items = tuple(universe)
    limit = len(items) if max_order is None else max_order
    terms = [s for s in powerset(items) if len(s) <= limit]
    rows = list(observed_sets)
    design = np.asarray([[float(term <= row) for term in terms] for row in rows])
    return design, terms
