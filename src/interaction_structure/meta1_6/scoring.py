from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .ensemble import RecoveryScenario
from .structure import and_dictionary


@dataclass(frozen=True, slots=True)
class KKTScore:
    score: float
    mean_probability: float
    lower_quantile: float
    cvar: float
    singular_fraction: float
    scenario_probabilities: tuple[float, ...]


def _standardized_selected(dimension: int, masks: tuple[int, ...]) -> tuple[np.ndarray, np.ndarray]:
    full, terms = and_dictionary(dimension)
    design = full[np.asarray(masks)]
    scale = np.sqrt(np.mean(design**2, axis=0))
    scaled = np.zeros_like(design)
    nonzero = scale > 1e-12
    scaled[:, nonzero] = design[:, nonzero] / scale[nonzero]
    return scaled, terms


def _scenario_probability(
    design: np.ndarray,
    terms: np.ndarray,
    scenario: RecoveryScenario,
    *,
    target_only: bool,
    draws: int,
    lambda_multipliers: tuple[float, ...],
) -> tuple[float, bool]:
    term_to_col = {int(term): index for index, term in enumerate(terms)}
    active = np.asarray([term_to_col[term] for term in scenario.active], dtype=int)
    signs = np.asarray(scenario.signs, dtype=float)
    beta = np.asarray(scenario.effects, dtype=float)
    high = np.asarray([int(term).bit_count() >= 3 for term in terms])
    high_active_position = np.asarray([scenario.active[index].bit_count() >= 3 for index in range(len(active))])
    target_inactive = np.flatnonzero(high & ~np.isin(np.arange(len(terms)), active))
    all_inactive = np.flatnonzero(~np.isin(np.arange(len(terms)), active))
    inactive = target_inactive if target_only else all_inactive
    if np.any(np.linalg.norm(design[:, active], axis=0) <= 1e-12):
        return 0.0, True
    gram = design[:, active].T @ design[:, active] / len(design)
    if np.linalg.matrix_rank(gram, tol=1e-9) < len(active):
        return 0.0, True
    inverse = np.linalg.inv(gram)
    rng = np.random.default_rng(scenario.noise_seed)
    noise = rng.normal(0.0, scenario.sigma, size=(len(design), draws))
    score = design.T @ noise / len(design)
    active_score = score[active]
    cross = design[:, inactive].T @ design[:, active] / len(design) if len(inactive) else np.empty((0, len(active)))
    base_lambda = scenario.sigma * np.sqrt(2.0 * np.log(len(terms)) / len(design))
    best = 0.0
    for multiplier in lambda_multipliers:
        regularization = multiplier * base_lambda
        estimate = beta[:, None] + inverse @ (active_score - regularization * signs[:, None])
        sign_event = np.sign(estimate) == signs[:, None]
        if target_only:
            sign_ok = np.all(sign_event[high_active_position], axis=0)
        else:
            sign_ok = np.all(sign_event, axis=0)
        if len(inactive):
            residual_score = score[inactive] - cross @ (inverse @ active_score)
            deterministic = regularization * (cross @ (inverse @ signs))[:, None]
            inactive_ok = np.all(np.abs(residual_score + deterministic) <= regularization + 1e-12, axis=0)
        else:
            inactive_ok = np.ones(draws, dtype=bool)
        best = max(best, float(np.mean(sign_ok & inactive_ok)))
    return best, False


def score_design(
    masks: tuple[int, ...],
    scenarios: list[RecoveryScenario],
    *,
    dimension: int = 6,
    target_only: bool = True,
    aggregator: str = "cvar",
    draws: int = 32,
    lambda_multipliers: tuple[float, ...] = (0.65, 1.0, 1.5),
    integrate_singular: bool = True,
) -> KKTScore:
    design, terms = _standardized_selected(dimension, masks)
    probabilities: list[float] = []
    singular = 0
    for scenario in scenarios:
        probability, failed = _scenario_probability(
            design,
            terms,
            scenario,
            target_only=target_only,
            draws=draws,
            lambda_multipliers=lambda_multipliers,
        )
        singular += int(failed)
        if integrate_singular or not failed:
            probabilities.append(probability)
    if not probabilities:
        probabilities = [0.0]
    values = np.asarray(probabilities)
    lower_quantile = float(np.quantile(values, 0.2))
    tail_count = max(1, int(np.ceil(0.2 * len(values))))
    cvar = float(np.mean(np.sort(values)[:tail_count]))
    mean = float(np.mean(values))
    scores = {
        "mean": mean,
        "lower_quantile": lower_quantile,
        "cvar": cvar,
        "maximin": float(np.min(values)),
        "robust": 0.8 * mean + 0.2 * cvar,
    }
    if aggregator not in scores:
        raise ValueError(f"unknown aggregator: {aggregator}")
    return KKTScore(scores[aggregator], mean, lower_quantile, cvar, singular / len(scenarios), tuple(values.tolist()))


def dcd_score(masks: tuple[int, ...], scenarios: list[RecoveryScenario], dimension: int = 6) -> float:
    design, terms = _standardized_selected(dimension, masks)
    term_to_col = {int(term): index for index, term in enumerate(terms)}
    values: list[float] = []
    for scenario in scenarios:
        active = np.asarray([term_to_col[term] for term in scenario.active], dtype=int)
        inactive = np.flatnonzero(~np.isin(np.arange(len(terms)), active))
        block = design[:, active]
        gram = block.T @ block / len(design)
        if np.linalg.matrix_rank(gram, tol=1e-9) < len(active):
            values.append(0.0)
            continue
        smallest = float(np.linalg.eigvalsh(gram)[0])
        inverse = np.linalg.inv(gram)
        signs = np.asarray(scenario.signs)
        cross = design[:, inactive].T @ block / len(design)
        irrepresentable = float(np.max(np.abs(cross @ inverse @ signs))) if len(inactive) else 0.0
        values.append(max(0.0, smallest) * max(0.0, 1.0 - irrepresentable))
    return float(np.mean(values))
