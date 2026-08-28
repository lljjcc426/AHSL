from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter
from typing import Callable

import numpy as np


@dataclass(frozen=True, slots=True)
class SearchResult:
    masks: tuple[int, ...]
    score: float
    evaluations: int
    accepted_swaps: int
    runtime_seconds: float


def optimize_rows(
    dimension: int,
    budget: int,
    objective: Callable[[tuple[int, ...]], float],
    *,
    seed: int,
    starts: tuple[tuple[int, ...], ...] = (),
    restarts: int = 3,
    proposals_per_round: int = 48,
    patience: int = 4,
) -> SearchResult:
    """Deterministic multi-start exchange over feasible Boolean rows."""
    start_time = perf_counter()
    rng = np.random.default_rng(seed)
    candidates = np.arange(1, 1 << dimension)
    initial: list[tuple[int, ...]] = [tuple(sorted(set(value) | {0})) for value in starts]
    while len(initial) < restarts:
        chosen = rng.choice(candidates, size=budget - 1, replace=False)
        initial.append(tuple(sorted((0, *chosen.tolist()))))
    best_masks: tuple[int, ...] | None = None
    best_score = -np.inf
    evaluations = 0
    accepted = 0
    for current in initial[:restarts]:
        if len(current) != budget:
            continue
        current_score = objective(current)
        evaluations += 1
        failures = 0
        while failures < patience:
            selected = set(current)
            removable = np.asarray(sorted(selected - {0}))
            available = np.asarray(sorted(set(candidates.tolist()) - selected))
            proposals: list[tuple[int, ...]] = []
            for _ in range(proposals_per_round):
                proposal = tuple(sorted((selected - {int(rng.choice(removable))}) | {int(rng.choice(available))}))
                proposals.append(proposal)
            proposal_scores = [objective(proposal) for proposal in proposals]
            evaluations += len(proposals)
            index = int(np.argmax(proposal_scores))
            if proposal_scores[index] > current_score + 1e-12:
                current, current_score = proposals[index], proposal_scores[index]
                accepted += 1
                failures = 0
            else:
                failures += 1
        if current_score > best_score:
            best_masks, best_score = current, current_score
    if best_masks is None:
        raise ValueError("no valid start design matched the requested budget")
    return SearchResult(best_masks, float(best_score), evaluations, accepted, perf_counter() - start_time)
