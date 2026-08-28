from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter

import numpy as np
from sklearn.linear_model import ARDRegression, ElasticNet, Lasso, OrthogonalMatchingPursuit

from .protocol import RevealedPanel


@dataclass
class MethodFit:
    coefficients: np.ndarray
    selected: np.ndarray
    scores: np.ndarray
    hyperparameters: str
    validation_mse: float
    runtime: float
    trials: list[dict]


def _column_scale(design: np.ndarray) -> np.ndarray:
    scale = np.sqrt(np.mean(design**2, axis=0))
    scale[scale < 1e-12] = 1.0
    return scale


def _split(n_rows: int, seed: int) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    order = rng.permutation(n_rows)
    n_validation = max(2, int(round(0.2 * n_rows)))
    return order[n_validation:], order[:n_validation]


def _expand(coef: np.ndarray, terms: np.ndarray, size: int) -> np.ndarray:
    output = np.zeros(size, dtype=float)
    output[terms] = coef
    return output


def _fit_penalized(
    panel: RevealedPanel,
    *,
    family: str,
    seed: int,
    max_order: int | None = None,
    weighted: bool = False,
    order_gamma: float = 0.0,
) -> MethodFit:
    start = perf_counter()
    design, terms = panel.design(max_order=max_order)
    response = panel.means()
    train, validation = _split(len(response), seed)
    base_scale = _column_scale(design[train])
    order = np.asarray([int(term).bit_count() for term in terms])
    penalty = np.where(order >= 3, np.power(np.maximum(order - 2, 1), order_gamma), 1.0)
    scale = base_scale * penalty
    scaled = design / scale
    alphas = (1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2, 1e-1)
    mixes = (1.0,) if family == "lasso" else (0.25, 0.5, 0.75)
    variance = panel.variances()
    variance_floor = float(np.median(variance[variance > 0])) if np.any(variance > 0) else 1.0
    weights = 1.0 / (variance / np.asarray([len(values) for values in panel.replicates]) + 0.25 * variance_floor)
    weights /= np.mean(weights)
    best: tuple[float, np.ndarray, float, float] | None = None
    trials: list[dict] = []
    for mix in mixes:
        for alpha in alphas:
            if family == "lasso":
                model = Lasso(alpha=alpha, fit_intercept=False, max_iter=20_000)
            else:
                model = ElasticNet(alpha=alpha, l1_ratio=mix, fit_intercept=False, max_iter=20_000)
            fit_kwargs = {"sample_weight": weights[train]} if weighted else {}
            model.fit(scaled[train], response[train], **fit_kwargs)
            coefficient = model.coef_ / scale
            mse = float(np.mean((design[validation] @ coefficient - response[validation]) ** 2))
            trials.append({"alpha": alpha, "l1_ratio": mix, "validation_mse": mse, "order_gamma": order_gamma})
            if best is None or mse < best[0]:
                best = (mse, coefficient, alpha, mix)
    assert best is not None
    _, _, alpha, mix = best
    model = Lasso(alpha=alpha, fit_intercept=False, max_iter=20_000) if family == "lasso" else ElasticNet(alpha=alpha, l1_ratio=mix, fit_intercept=False, max_iter=20_000)
    fit_kwargs = {"sample_weight": weights} if weighted else {}
    model.fit(scaled, response, **fit_kwargs)
    coefficient = model.coef_ / scale
    full = _expand(coefficient, terms, 1 << panel.dimension)
    selected = np.abs(full) > 1e-9
    return MethodFit(full, selected, np.abs(full), f"alpha={alpha};l1_ratio={mix};gamma={order_gamma};weighted={weighted}", best[0], perf_counter() - start, trials)


def fit_lasso(panel: RevealedPanel, seed: int) -> MethodFit:
    return _fit_penalized(panel, family="lasso", seed=seed)


def fit_elastic_net(panel: RevealedPanel, seed: int) -> MethodFit:
    return _fit_penalized(panel, family="elastic_net", seed=seed)


def fit_lower_order(panel: RevealedPanel, seed: int) -> MethodFit:
    return _fit_penalized(panel, family="lasso", seed=seed, max_order=2)


def fit_noise_weighted(panel: RevealedPanel, seed: int) -> MethodFit:
    return _fit_penalized(panel, family="elastic_net", seed=seed, weighted=True)


def fit_order_penalty(panel: RevealedPanel, seed: int) -> MethodFit:
    candidates = [
        _fit_penalized(panel, family="lasso", seed=seed, order_gamma=gamma)
        for gamma in (-1.0, -0.5, 0.5, 1.0)
    ]
    best = min(candidates, key=lambda fit: fit.validation_mse)
    best.trials = [dict(trial, candidate_gamma=float(fit.hyperparameters.split("gamma=")[1].split(";")[0])) for fit in candidates for trial in fit.trials]
    return best


def fit_combined_v1(panel: RevealedPanel, seed: int) -> MethodFit:
    candidates = [
        _fit_penalized(panel, family="elastic_net", seed=seed, weighted=True, order_gamma=gamma)
        for gamma in (-0.5, 0.5)
    ]
    best = min(candidates, key=lambda fit: fit.validation_mse)
    best.trials = [dict(trial, candidate_gamma=gamma) for gamma, fit in zip((-0.5, 0.5), candidates, strict=True) for trial in fit.trials]
    best.hyperparameters += ";combined=noise_weighted_order_elastic_net"
    return best


def fit_omp(panel: RevealedPanel, seed: int) -> MethodFit:
    start = perf_counter()
    design, terms = panel.design()
    response = panel.means()
    train, validation = _split(len(response), seed)
    scale = _column_scale(design[train])
    scaled = design / scale
    candidates = tuple(k for k in (2, 4, 8, 12, 16, 24, 32) if k < len(train))
    trials: list[dict] = []
    best: tuple[float, int] | None = None
    for k in candidates:
        model = OrthogonalMatchingPursuit(n_nonzero_coefs=k, fit_intercept=False)
        model.fit(scaled[train], response[train])
        coefficient = model.coef_ / scale
        mse = float(np.mean((design[validation] @ coefficient - response[validation]) ** 2))
        trials.append({"nonzero_terms": k, "validation_mse": mse})
        if best is None or mse < best[0]:
            best = (mse, k)
    assert best is not None
    model = OrthogonalMatchingPursuit(n_nonzero_coefs=min(best[1], len(response) - 1), fit_intercept=False)
    model.fit(design / _column_scale(design), response)
    coefficient = model.coef_ / _column_scale(design)
    full = _expand(coefficient, terms, 1 << panel.dimension)
    return MethodFit(full, np.abs(full) > 1e-9, np.abs(full), f"nonzero_terms={best[1]}", best[0], perf_counter() - start, trials)


def _iht(design: np.ndarray, response: np.ndarray, sparsity: int, iterations: int = 150) -> np.ndarray:
    scale = _column_scale(design)
    x = design / scale
    coefficient = np.zeros(x.shape[1])
    step = 1.0 / (np.linalg.norm(x, ord=2) ** 2 + 1e-12)
    keep = min(sparsity + 1, x.shape[1], max(1, x.shape[0] - 1))
    for _ in range(iterations):
        proposal = coefficient + step * x.T @ (response - x @ coefficient)
        active = np.argpartition(np.abs(proposal), -keep)[-keep:]
        active = np.unique(np.append(active, 0))
        updated = np.zeros_like(coefficient)
        updated[active] = np.linalg.lstsq(x[:, active], response, rcond=None)[0]
        if np.linalg.norm(updated - coefficient) <= 1e-8 * (1 + np.linalg.norm(coefficient)):
            coefficient = updated
            break
        coefficient = updated
    return coefficient / scale


def fit_sparse_mobius_iht(panel: RevealedPanel, seed: int) -> MethodFit:
    start = perf_counter()
    design, terms = panel.design()
    response = panel.means()
    candidates = tuple(k for k in (2, 4, 8, 12, 16, 24, 32) if k < len(response) - 1)
    trials: list[dict] = []
    best: tuple[float, np.ndarray, int] | None = None
    for k in candidates:
        coefficient = _iht(design, response, k)
        residual = response - design @ coefficient
        active = max(1, int(np.count_nonzero(np.abs(coefficient) > 1e-9)))
        bic = len(response) * np.log(np.mean(residual**2) + 1e-12) + active * np.log(len(response))
        trials.append({"sparsity": k, "bic": float(bic), "validation_mse": float(np.mean(residual**2))})
        if best is None or bic < best[0]:
            best = (float(bic), coefficient, k)
    assert best is not None
    full = _expand(best[1], terms, 1 << panel.dimension)
    return MethodFit(full, np.abs(full) > 1e-9, np.abs(full), f"sparsity={best[2]};criterion=BIC", float(np.mean((design @ best[1] - response) ** 2)), perf_counter() - start, trials)


def _heredity_filter(coefficients: np.ndarray, rule: str) -> np.ndarray:
    output = coefficients.copy()
    active = set(np.flatnonzero(np.abs(output) > 1e-9))
    for raw_mask in sorted(active):
        mask = int(raw_mask)
        if mask.bit_count() < 2:
            continue
        parents = {mask ^ (1 << bit) for bit in range(mask.bit_length()) if mask & (1 << bit)}
        keep = parents <= active if rule == "strong" else bool(parents & active)
        if not keep:
            output[mask] = 0.0
    return output


def fit_heredity(panel: RevealedPanel, seed: int, rule: str) -> MethodFit:
    base = fit_lasso(panel, seed)
    coefficient = _heredity_filter(base.coefficients, rule)
    base.coefficients = coefficient
    base.selected = np.abs(coefficient) > 1e-9
    base.scores = np.abs(coefficient)
    base.hyperparameters += f";heredity={rule}"
    return base


def fit_stability(
    panel: RevealedPanel,
    seed: int,
    *,
    fdr_conservative: bool,
    fixed_probability: float | None = None,
) -> MethodFit:
    start = perf_counter()
    base = fit_lasso(panel, seed)
    alpha = float(base.hyperparameters.split("alpha=")[1].split(";")[0])
    design, terms = panel.design()
    response = panel.means()
    scale = _column_scale(design)
    rng = np.random.default_rng(seed + 101)
    n_bootstrap = 24
    coefficient_draws = np.zeros((n_bootstrap, design.shape[1]))
    for draw in range(n_bootstrap):
        rows = rng.choice(len(response), size=max(8, int(round(0.75 * len(response)))), replace=True)
        boot_response = np.asarray([
            np.mean(rng.choice(panel.replicates[row], size=len(panel.replicates[row]), replace=True))
            for row in rows
        ])
        model = Lasso(alpha=alpha, fit_intercept=False, max_iter=20_000)
        model.fit(design[rows] / scale, boot_response)
        coefficient_draws[draw] = model.coef_ / scale
    nonzero = np.abs(coefficient_draws) > 1e-9
    positive = np.mean(coefficient_draws > 1e-9, axis=0)
    negative = np.mean(coefficient_draws < -1e-9, axis=0)
    frequency = np.maximum(positive, negative)
    thresholds = (fixed_probability,) if fixed_probability is not None else ((0.9,) if fdr_conservative else (0.6, 0.75, 0.9))
    trials: list[dict] = []
    best: tuple[float, np.ndarray, float] | None = None
    for threshold in thresholds:
        active = np.flatnonzero(frequency >= threshold)
        if 0 not in active:
            active = np.unique(np.append(active, 0))
        coefficient = np.zeros(design.shape[1])
        coefficient[active] = np.linalg.lstsq(design[:, active], response, rcond=None)[0]
        residual = response - design @ coefficient
        bic = len(response) * np.log(np.mean(residual**2) + 1e-12) + len(active) * np.log(len(response))
        trials.append({"selection_probability": threshold, "bic": float(bic), "validation_mse": float(np.mean(residual**2))})
        if best is None or bic < best[0]:
            best = (float(bic), coefficient, threshold)
    assert best is not None
    full = _expand(best[1], terms, 1 << panel.dimension)
    scores = _expand(frequency, terms, 1 << panel.dimension)
    selected = scores >= best[2]
    return MethodFit(full, selected, scores, f"alpha={alpha};pi={best[2]};bootstraps={n_bootstrap}", float(np.mean((design @ best[1] - response) ** 2)), perf_counter() - start, base.trials + trials)


def fit_ard_support(panel: RevealedPanel, seed: int) -> MethodFit:
    start = perf_counter()
    design, terms = panel.design()
    response = panel.means()
    train, validation = _split(len(response), seed)
    scale = _column_scale(design[train])
    scaled = design / scale
    thresholds = (1e2, 1e3, 1e4, 1e5)
    trials: list[dict] = []
    best: tuple[float, float] | None = None
    for threshold in thresholds:
        model = ARDRegression(max_iter=500, threshold_lambda=threshold, fit_intercept=False)
        model.fit(scaled[train], response[train])
        coefficient = model.coef_ / scale
        mse = float(np.mean((design[validation] @ coefficient - response[validation]) ** 2))
        trials.append({"threshold_lambda": threshold, "validation_mse": mse, "active_terms": int(np.count_nonzero(np.abs(coefficient) > 1e-9))})
        if best is None or mse < best[0]:
            best = (mse, threshold)
    assert best is not None
    model = ARDRegression(max_iter=500, threshold_lambda=best[1], fit_intercept=False)
    model.fit(design / _column_scale(design), response)
    coefficient = model.coef_ / _column_scale(design)
    full = _expand(coefficient, terms, 1 << panel.dimension)
    return MethodFit(full, np.abs(full) > 1e-9, np.abs(full), f"threshold_lambda={best[1]}", best[0], perf_counter() - start, trials)
