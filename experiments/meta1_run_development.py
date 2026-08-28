from __future__ import annotations

import argparse
import json
from itertools import combinations
from pathlib import Path
from time import perf_counter

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import psutil

from interaction_structure.meta1.data import CompletePanel, Landscape, load_diaz_colunga, load_ishizawa, normalized_replicate_frame
from interaction_structure.meta1.estimand import ReferenceEstimand, build_reference_estimand, jaccard, pairwise_stability, zeta_matrix
from interaction_structure.meta1.evaluation import signed_support_metrics
from interaction_structure.meta1.methods import (
    MethodFit,
    fit_ard_support,
    fit_combined_v1,
    fit_elastic_net,
    fit_heredity,
    fit_lasso,
    fit_lower_order,
    fit_noise_weighted,
    fit_omp,
    fit_order_penalty,
    fit_sparse_mobius_iht,
    fit_stability,
)
from interaction_structure.meta1.protocol import EvaluationOracle, design_balanced_mask, hybrid_design_mask, make_measurement_masks, reveal

REFERENCE_SEED = 20260828
DEVELOPMENT_MASK_SEEDS = (101, 202, 303, 404)
CONFIRMATION_MASK_SEEDS = (505, 606)
ALL_MASK_SEEDS = DEVELOPMENT_MASK_SEEDS + CONFIRMATION_MASK_SEEDS
PRIMARY_SCALES = {"ishizawa": "log10", "diaz_colunga": "raw"}
SENSITIVITY_SCALES = {"ishizawa": ("log10", "raw"), "diaz_colunga": ("raw", "log1p")}
BUDGETS = {64: (16, 24, 32, 48), 256: (64, 96, 128, 192)}


def _write_manifest(path: Path, manifest: dict[str, object]) -> None:
    memory = psutil.Process().memory_info()
    peak_bytes = getattr(memory, "peak_wset", memory.rss)
    previous_peak = 0.0
    if path.exists():
        previous_peak = float(json.loads(path.read_text(encoding="utf-8")).get("peak_working_set_mb", 0.0))
    manifest["peak_working_set_mb"] = max(previous_peak, peak_bytes / (1024**2))
    path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))


def _directories(root: Path) -> tuple[Path, Path, Path]:
    raw = root / "raw"
    aggregated = root / "aggregated"
    figures = root / "figures"
    for path in (raw, aggregated, figures):
        path.mkdir(parents=True, exist_ok=True)
    return raw, aggregated, figures


def _landscapes(panels: tuple[CompletePanel, ...]) -> list[Landscape]:
    return [landscape for panel in panels for landscape in panel.landscapes]


def _data_audit(panels: tuple[CompletePanel, ...], scales: dict[str, str]) -> tuple[pd.DataFrame, pd.DataFrame]:
    audit_rows, replicate_rows = [], []
    for panel in panels:
        for landscape in panel.landscapes:
            transformed = landscape.transformed_replicates(scales[panel.panel_id])
            counts = np.asarray([len(values) for values in transformed.values()])
            all_values = np.concatenate(list(transformed.values()))
            audit_rows.append(
                {
                    "panel_id": panel.panel_id,
                    "landscape_id": landscape.landscape_id,
                    "dimension": landscape.dimension,
                    "expected_cells": landscape.n_cells,
                    "observed_cells": len(landscape.replicates),
                    "missing_cells": landscape.n_cells - len(landscape.replicates),
                    "replicate_min": int(counts.min()),
                    "replicate_max": int(counts.max()),
                    "replicate_total": int(counts.sum()),
                    "primary_scale": scales[panel.panel_id],
                    "response_min": float(all_values.min()),
                    "response_median": float(np.median(all_values)),
                    "response_max": float(all_values.max()),
                    "source_version": panel.source_version,
                }
            )
            for mask, values in transformed.items():
                replicate_rows.append(
                    {
                        "panel_id": panel.panel_id,
                        "landscape_id": landscape.landscape_id,
                        "community_mask": mask,
                        "community_bitmask": format(mask, f"0{landscape.dimension}b"),
                        "n_replicates": len(values),
                        "response_mean": float(np.mean(values)),
                        "response_variance": float(np.var(values, ddof=1)),
                        "response_scale": scales[panel.panel_id],
                    }
                )
    return pd.DataFrame(audit_rows), pd.DataFrame(replicate_rows)


def _reference_audit(landscapes: list[Landscape]) -> tuple[dict[str, ReferenceEstimand], pd.DataFrame, pd.DataFrame]:
    primary: dict[str, ReferenceEstimand] = {}
    reference_frames, sensitivity_rows = [], []
    for landscape in landscapes:
        primary_scale = PRIMARY_SCALES[landscape.panel_id]
        reference = build_reference_estimand(landscape, scale=primary_scale, n_bootstrap=1000, seed=REFERENCE_SEED)
        primary[landscape.landscape_id] = reference
        reference_frames.append(reference.to_frame())
        for scale in SENSITIVITY_SCALES[landscape.panel_id]:
            candidates = [
                build_reference_estimand(landscape, scale=scale, n_bootstrap=300, seed=REFERENCE_SEED + offset)
                for offset in range(1, 6)
            ]
            median_jaccard, minimum_jaccard = pairwise_stability(candidates)
            for candidate in candidates:
                high = np.asarray([mask.bit_count() >= 3 for mask in range(landscape.n_cells)])
                support = candidate.support_sign[high]
                sensitivity_rows.append(
                    {
                        "panel_id": landscape.panel_id,
                        "landscape_id": landscape.landscape_id,
                        "scale": scale,
                        "bootstrap_seed": candidate.bootstrap_seed,
                        "support_count": int(np.count_nonzero(support)),
                        "positive_count": int(np.sum(support > 0)),
                        "negative_count": int(np.sum(support < 0)),
                        "pure_hoi_count": int(candidate.pure_high_order.sum()),
                        "pairwise_seed_jaccard_median": median_jaccard,
                        "pairwise_seed_jaccard_min": minimum_jaccard,
                        "jaccard_to_primary": jaccard(candidate.support_sign[high], reference.support_sign[high]),
                        "threshold_multiplier": 1.0,
                    }
                )
        high = np.asarray([mask.bit_count() >= 3 for mask in range(landscape.n_cells)])
        for multiplier in (0.8, 1.2):
            alternate = reference.support_sign.copy()
            supported = (np.abs(reference.coefficients) >= multiplier * reference.practical_threshold) & ((reference.lower > 0) | (reference.upper < 0))
            alternate = np.where(supported, np.sign(reference.coefficients), 0).astype(int)
            sensitivity_rows.append(
                {
                    "panel_id": landscape.panel_id,
                    "landscape_id": landscape.landscape_id,
                    "scale": primary_scale,
                    "bootstrap_seed": REFERENCE_SEED,
                    "support_count": int(np.count_nonzero(alternate[high])),
                    "positive_count": int(np.sum(alternate[high] > 0)),
                    "negative_count": int(np.sum(alternate[high] < 0)),
                    "pure_hoi_count": np.nan,
                    "pairwise_seed_jaccard_median": np.nan,
                    "pairwise_seed_jaccard_min": np.nan,
                    "jaccard_to_primary": jaccard(alternate[high], reference.support_sign[high]),
                    "threshold_multiplier": multiplier,
                }
            )
    return primary, pd.concat(reference_frames, ignore_index=True), pd.DataFrame(sensitivity_rows)


def _mask_table() -> pd.DataFrame:
    frames = []
    for n_cells, budgets in BUDGETS.items():
        frame = make_measurement_masks(n_cells, budgets, ALL_MASK_SEEDS)
        frame["measurement_fraction"] = frame["budget"] / n_cells
        frame["role"] = np.where(frame["mask_seed"].isin(DEVELOPMENT_MASK_SEEDS), "development", "confirmation_reserve")
        frames.append(frame)
    return pd.concat(frames, ignore_index=True)


def _masks_for(mask_frame: pd.DataFrame, n_cells: int, budget: int, seed: int) -> tuple[int, ...]:
    rows = mask_frame[(mask_frame.n_cells == n_cells) & (mask_frame.budget == budget) & (mask_frame.mask_seed == seed)]
    return tuple(sorted(rows.community_mask.astype(int)))


def _method_factories():
    return {
        "lasso": lambda panel, seed: fit_lasso(panel, seed),
        "elastic_net": lambda panel, seed: fit_elastic_net(panel, seed),
        "omp": lambda panel, seed: fit_omp(panel, seed),
        "weak_heredity": lambda panel, seed: fit_heredity(panel, seed, "weak"),
        "strong_heredity": lambda panel, seed: fit_heredity(panel, seed, "strong"),
        "stability_selection": lambda panel, seed: fit_stability(panel, seed, fdr_conservative=False),
        "sparse_mobius_iht": lambda panel, seed: fit_sparse_mobius_iht(panel, seed),
        "lower_order_response": lambda panel, seed: fit_lower_order(panel, seed),
        "noise_weighted": lambda panel, seed: fit_noise_weighted(panel, seed),
        "stability_fdr": lambda panel, seed: fit_stability(panel, seed, fdr_conservative=True),
        "order_penalty": lambda panel, seed: fit_order_penalty(panel, seed),
        "stability_pi60": lambda panel, seed: fit_stability(panel, seed, fdr_conservative=False, fixed_probability=0.6),
        "ard_support": lambda panel, seed: fit_ard_support(panel, seed),
        "combined_v1": lambda panel, seed: fit_combined_v1(panel, seed),
    }


def _mechanism_features(landscape: Landscape, revealed, reference: ReferenceEstimand) -> dict[str, float]:
    design, _ = revealed.design()
    variable = np.std(design, axis=0) > 1e-12
    correlations = np.corrcoef(design[:, variable], rowvar=False) if variable.sum() > 1 else np.asarray([[1.0]])
    off_diagonal = np.abs(correlations - np.eye(len(correlations)))
    upper = off_diagonal[np.triu_indices_from(off_diagonal, k=1)] if len(off_diagonal) > 1 else np.asarray([0.0])
    singular = np.linalg.svd(design, compute_uv=False)
    positive_singular = singular[singular > 1e-9]
    sampling_variance = revealed.variances() / np.asarray([len(values) for values in revealed.replicates])
    variance_floor = float(np.median(sampling_variance[sampling_variance > 0])) if np.any(sampling_variance > 0) else 1e-12
    high = np.asarray([mask.bit_count() >= 3 for mask in range(landscape.n_cells)])
    support = reference.support_sign[high]
    return {
        "measurement_fraction": len(revealed.selected_masks) / landscape.n_cells,
        "design_coherence": float(off_diagonal.max()) if off_diagonal.size else 0.0,
        "design_coherence_p95": float(np.quantile(upper, 0.95)),
        "design_alias_fraction": float(np.mean(upper >= 0.999)),
        "design_condition": float(positive_singular.max() / positive_singular.min()),
        "replicate_variance": float(np.median(revealed.variances())),
        "replicate_snr": float(np.var(revealed.means()) / max(variance_floor, 1e-12)),
        "support_sparsity": float(np.count_nonzero(support) / len(support)),
        "pure_hoi_fraction": float(reference.pure_high_order[high].sum() / max(1, np.count_nonzero(support))),
        "positive_support_fraction": float(np.sum(support > 0) / max(1, np.count_nonzero(support))),
    }


def _support_string(fit: MethodFit) -> str:
    return ";".join(f"{mask}:{int(np.sign(fit.coefficients[mask]))}" for mask in np.flatnonzero(fit.selected) if mask.bit_count() >= 3)


def _run_one(
    run_id: str,
    landscape: Landscape,
    reference: ReferenceEstimand,
    masks: tuple[int, ...],
    seed: int,
    method: str,
    factory,
    adaptive_policy: str,
) -> tuple[dict, list[dict]]:
    scale = PRIMARY_SCALES[landscape.panel_id]
    revealed = reveal(landscape, masks, scale)
    fit = factory(revealed, seed)
    metrics = signed_support_metrics(reference, fit.coefficients, fit.selected)
    response_rmse = EvaluationOracle(landscape, scale).hidden_response_rmse(fit.coefficients, revealed.selected_masks)
    features = _mechanism_features(landscape, revealed, reference)
    row = {
        "run_id": run_id,
        "panel": landscape.panel_id,
        "landscape": landscape.landscape_id,
        "response_scale": scale,
        "support_estimand_version": "META1-R1-CI95-practical-effect",
        "measurement_budget": len(masks),
        "mask_seed": seed,
        "method": method,
        "method_variant": method,
        "hyperparameters": fit.hyperparameters,
        "adaptive_policy": adaptive_policy,
        **metrics,
        "response_rmse": response_rmse,
        "runtime": fit.runtime,
        "seed_stability": np.nan,
        "selected_signed_support": _support_string(fit),
        "notes": "tuned on revealed-response criterion only",
        **features,
    }
    trials = [
        {"run_id": run_id, "method": method, "trial": index, "candidate": json.dumps(trial, sort_keys=True), "validation_mse": trial.get("validation_mse", np.nan)}
        for index, trial in enumerate(fit.trials)
    ]
    return row, trials


def _seed_stability(frame: pd.DataFrame) -> pd.DataFrame:
    output = frame.copy()
    group_columns = ["panel", "landscape", "measurement_budget", "method", "adaptive_policy"]
    for _, index in output.groupby(group_columns).groups.items():
        supports = []
        for value in output.loc[index, "selected_signed_support"]:
            supports.append(set(value.split(";")) if isinstance(value, str) and value else set())
        pairs = [len(a & b) / len(a | b) if a | b else 1.0 for a, b in combinations(supports, 2)]
        output.loc[index, "seed_stability"] = float(np.median(pairs)) if pairs else 1.0
    return output


def _run_experiments(
    landscapes: list[Landscape],
    references: dict[str, ReferenceEstimand],
    masks: pd.DataFrame,
    *,
    method_names: tuple[str, ...] | None = None,
    include_balanced: bool = True,
    counter_start: int = 0,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows, trials = [], []
    factories = _method_factories()
    counter = counter_start
    selected_factories = factories if method_names is None else {name: factories[name] for name in method_names}
    for landscape in landscapes:
        for budget in BUDGETS[landscape.n_cells]:
            for seed in DEVELOPMENT_MASK_SEEDS:
                selected = _masks_for(masks, landscape.n_cells, budget, seed)
                for method, factory in selected_factories.items():
                    counter += 1
                    row, trial = _run_one(f"M1-{counter:05d}", landscape, references[landscape.landscape_id], selected, seed, method, factory, "uniform")
                    rows.append(row); trials.extend(trial)
                if include_balanced:
                    balanced = design_balanced_mask(landscape.dimension, budget, seed)
                    for method in ("sparse_mobius_iht", "order_penalty"):
                        counter += 1
                        row, trial = _run_one(f"M1-{counter:05d}", landscape, references[landscape.landscape_id], balanced, seed, method, factories[method], "d_optimal_rows")
                        rows.append(row); trials.extend(trial)
    return _seed_stability(pd.DataFrame(rows)), pd.DataFrame(trials)


def _aggregate(experiments: pd.DataFrame) -> dict[str, pd.DataFrame]:
    metrics = ["primary_f1", "precision", "recall", "average_precision", "empirical_fdr", "pure_hoi_recall", "coefficient_rmse", "response_rmse", "runtime", "seed_stability"]
    baselines = {"lasso", "elastic_net", "omp", "weak_heredity", "strong_heredity", "stability_selection", "stability_pi60", "ard_support", "sparse_mobius_iht", "lower_order_response"}
    grouped = experiments.groupby(["panel", "method", "adaptive_policy", "measurement_budget"])[metrics].agg(["mean", "std"]).reset_index()
    grouped.columns = ["_".join(column).rstrip("_") if isinstance(column, tuple) else column for column in grouped.columns]
    baseline_summary = grouped[grouped["method"].isin(baselines)].copy()
    method_summary = grouped[~grouped["method"].isin(baselines)].copy()
    panel_summary = experiments.groupby(["panel", "method", "adaptive_policy"])[metrics].mean().reset_index()
    snr_cut = experiments[["landscape", "replicate_snr"]].drop_duplicates().replicate_snr.median()
    coherence_cut = experiments[["landscape", "measurement_budget", "design_alias_fraction"]].drop_duplicates().design_alias_fraction.median()
    regime = experiments.copy()
    regime["regime"] = np.where(
        (regime.replicate_snr <= snr_cut) & (regime.design_alias_fraction >= coherence_cut),
        "low_snr_high_aliasing",
        "other",
    )
    regime_summary = regime.groupby(["regime", "method", "adaptive_policy"])[metrics].mean().reset_index()
    failures = experiments.groupby(["panel", "method", "measurement_budget"])[["missed_positive_hoi", "missed_negative_hoi", "sign_flips", "false_hoi", "pure_hoi_miss"]].mean().reset_index()
    return {
        "baseline_summary": baseline_summary,
        "method_summary": method_summary,
        "panel_summary": panel_summary,
        "regime_summary": regime_summary,
        "failure_taxonomy": failures,
    }


def _figures(experiments: pd.DataFrame, sensitivity: pd.DataFrame, figures: Path) -> None:
    uniform = experiments[experiments.adaptive_policy.eq("uniform")]
    style = {"lasso": "#666666", "sparse_mobius_iht": "#4472C4", "noise_weighted": "#ED7D31", "stability_fdr": "#70AD47", "order_penalty": "#A64D79"}
    shown = list(style)

    fig, ax = plt.subplots(figsize=(8, 5))
    for method in shown:
        group = uniform[uniform.method.eq(method)].groupby("measurement_fraction").primary_f1.mean()
        ax.plot(group.index, group.values, marker="o", label=method, color=style[method])
    ax.set(xlabel="measurement fraction", ylabel="macro signed-support F1", title="Support recovery versus measurement budget"); ax.legend(fontsize=8); fig.tight_layout(); fig.savefig(figures / "01_support_f1_vs_budget.png", dpi=180); plt.close(fig)

    fig, ax = plt.subplots(figsize=(6, 5))
    summary = uniform[uniform.method.isin(shown)].groupby("method")[["recall", "precision", "empirical_fdr"]].mean()
    for method, row in summary.iterrows(): ax.scatter(row.recall, row.precision, s=70, label=f"{method} (FDR={row.empirical_fdr:.2f})", color=style[method])
    ax.set(xlabel="signed recall", ylabel="signed precision", title="Precision-recall and empirical FDR"); ax.legend(fontsize=7); fig.tight_layout(); fig.savefig(figures / "02_precision_recall_fdr.png", dpi=180); plt.close(fig)

    fig, ax = plt.subplots(figsize=(6, 5))
    for method in shown:
        group = uniform[uniform.method.eq(method)]
        ax.scatter(group.response_rmse, group.primary_f1, alpha=0.35, s=18, label=method, color=style[method])
    ax.set(xlabel="hidden-cell response RMSE", ylabel="signed-support F1", title="Prediction and support are distinct"); ax.legend(fontsize=7); fig.tight_layout(); fig.savefig(figures / "03_support_f1_vs_response_rmse.png", dpi=180); plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 4))
    pure = uniform[uniform.method.isin(shown)].groupby("method").pure_hoi_recall.mean().sort_values()
    pure.plot.bar(ax=ax, color=[style[index] for index in pure.index]); ax.set(ylabel="pure-HOI recall", title="Pure high-order support recovery"); fig.tight_layout(); fig.savefig(figures / "04_pure_hoi_recall.png", dpi=180); plt.close(fig)

    primary_scale = sensitivity[sensitivity.threshold_multiplier.eq(1.0)].groupby(["panel_id", "scale"]).jaccard_to_primary.median().unstack()
    fig, ax = plt.subplots(figsize=(6, 4)); primary_scale.plot.bar(ax=ax); ax.set(ylabel="Jaccard to primary support", title="Response-scale estimand sensitivity"); fig.tight_layout(); fig.savefig(figures / "05_scale_stability.png", dpi=180); plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 4))
    boot = sensitivity[(sensitivity.threshold_multiplier == 1.0)].groupby("landscape_id").pairwise_seed_jaccard_median.median().sort_values()
    boot.plot.bar(ax=ax, color="#4472C4"); ax.set(ylabel="median bootstrap-seed Jaccard", title="Reference-support stability"); fig.tight_layout(); fig.savefig(figures / "06_bootstrap_stability.png", dpi=180); plt.close(fig)

    fig, ax = plt.subplots(figsize=(6, 5))
    for method in shown:
        group = uniform[uniform.method.eq(method)]
        ax.scatter(group.replicate_snr, group.primary_f1, alpha=0.35, s=18, label=method, color=style[method])
    ax.set_xscale("log"); ax.set(xlabel="revealed replicate SNR", ylabel="signed-support F1", title="Performance versus replicate SNR"); fig.tight_layout(); fig.savefig(figures / "07_performance_vs_snr.png", dpi=180); plt.close(fig)

    fig, ax = plt.subplots(figsize=(6, 5))
    for method in shown:
        group = uniform[uniform.method.eq(method)]
        ax.scatter(group.design_alias_fraction, group.primary_f1, alpha=0.35, s=18, label=method, color=style[method])
    ax.set(xlabel="fraction of exactly aliased design-column pairs", ylabel="signed-support F1", title="Performance versus partial-design aliasing"); fig.tight_layout(); fig.savefig(figures / "08_performance_vs_coherence.png", dpi=180); plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 4.5))
    pivot = uniform[uniform.method.isin(["lasso", "noise_weighted", "stability_fdr", "order_penalty"])].groupby(["landscape", "method"]).primary_f1.mean().unstack()
    improvement = pivot.drop(columns="lasso").subtract(pivot.lasso, axis=0)
    improvement.plot.bar(ax=ax); ax.axhline(0, color="black", linewidth=0.8); ax.set(ylabel="F1 difference from lasso", title="Per-landscape development effects"); fig.tight_layout(); fig.savefig(figures / "09_per_landscape_improvement.png", dpi=180); plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 4.5))
    adaptive = experiments[experiments.method.isin(["elastic_net", "order_penalty"])].groupby(["measurement_fraction", "method", "adaptive_policy"]).primary_f1.mean().unstack(["method", "adaptive_policy"])
    adaptive.plot(ax=ax, marker="o"); ax.set(ylabel="signed-support F1", title="Measurement-policy development curve"); ax.legend(fontsize=6); fig.tight_layout(); fig.savefig(figures / "10_measurement_efficiency.png", dpi=180); plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ishizawa", type=Path, required=True)
    parser.add_argument("--diaz", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("results/meta1"))
    parser.add_argument("--aggregate-only", action="store_true")
    parser.add_argument("--followup-only", action="store_true")
    parser.add_argument("--refresh-analysis-only", action="store_true")
    parser.add_argument("--acquisition-followup-only", action="store_true")
    parser.add_argument("--hybrid-acquisition-only", action="store_true")
    args = parser.parse_args()
    raw, aggregated, figures = _directories(args.output)
    start = perf_counter()
    if args.aggregate_only:
        experiments = pd.read_csv(raw / "experiments.csv")
        tuning_trials = pd.read_csv(raw / "tuning_trials.csv")
        sensitivity = pd.read_csv(raw / "estimand_sensitivity.csv")
        summaries = _aggregate(experiments)
        for name, frame in summaries.items():
            frame.to_csv(aggregated / f"{name}.csv", index=False)
        _figures(experiments, sensitivity, figures)
        manifest = {
            "source_versions": {"ishizawa": "PNAS-2024-supplement", "diaz_colunga": "35c150c85df2fc5964523f906ceeb8229f0b1666"},
            "landscapes": int(experiments.landscape.nunique()),
            "development_mask_seeds": DEVELOPMENT_MASK_SEEDS,
            "confirmation_mask_seeds_reserved": CONFIRMATION_MASK_SEEDS,
            "total_runs": len(experiments),
            "tuning_trials_retained": len(tuning_trials),
            "total_method_runtime_seconds": float(experiments.runtime.sum()),
            "aggregation_recovery": True,
            "gpu_hours": 0.0,
        }
        _write_manifest(raw / "run_manifest.json", manifest)
        return
    if args.followup_only:
        panels = (load_ishizawa(args.ishizawa), load_diaz_colunga(args.diaz))
        landscapes = _landscapes(panels)
        references = {
            landscape.landscape_id: build_reference_estimand(
                landscape,
                scale=PRIMARY_SCALES[landscape.panel_id],
                n_bootstrap=1000,
                seed=REFERENCE_SEED,
            )
            for landscape in landscapes
        }
        masks = pd.read_csv(raw / "masks.csv")
        existing = pd.read_csv(raw / "experiments.csv")
        existing_trials = pd.read_csv(raw / "tuning_trials.csv")
        followup_methods = ("stability_pi60", "ard_support", "combined_v1")
        existing = existing[~existing.method.isin(followup_methods)]
        old_ids = existing.run_id.str.extract(r"(\d+)$")[0].astype(int)
        additions, trial_additions = _run_experiments(
            landscapes,
            references,
            masks,
            method_names=followup_methods,
            include_balanced=False,
            counter_start=int(old_ids.max()),
        )
        experiments = _seed_stability(pd.concat([existing, additions], ignore_index=True))
        tuning_trials = pd.concat([existing_trials[~existing_trials.method.isin(followup_methods)], trial_additions], ignore_index=True)
        tuning_trials = tuning_trials[tuning_trials.run_id.isin(experiments.run_id)]
        experiments.to_csv(raw / "experiments.csv", index=False)
        tuning_trials.to_csv(raw / "tuning_trials.csv", index=False)
        sensitivity = pd.read_csv(raw / "estimand_sensitivity.csv")
        summaries = _aggregate(experiments)
        for name, frame in summaries.items():
            frame.to_csv(aggregated / f"{name}.csv", index=False)
        _figures(experiments, sensitivity, figures)
        manifest = {
            "source_versions": {panel.panel_id: panel.source_version for panel in panels},
            "landscapes": len(landscapes),
            "development_mask_seeds": DEVELOPMENT_MASK_SEEDS,
            "confirmation_mask_seeds_reserved": CONFIRMATION_MASK_SEEDS,
            "total_runs": len(experiments),
            "tuning_trials_retained": len(tuning_trials),
            "total_method_runtime_seconds": float(experiments.runtime.sum()),
            "followup_methods": followup_methods,
            "gpu_hours": 0.0,
        }
        _write_manifest(raw / "run_manifest.json", manifest)
        return
    if args.refresh_analysis_only:
        panels = (load_ishizawa(args.ishizawa), load_diaz_colunga(args.diaz))
        landscapes = _landscapes(panels)
        by_id = {landscape.landscape_id: landscape for landscape in landscapes}
        references = {
            landscape.landscape_id: build_reference_estimand(
                landscape,
                scale=PRIMARY_SCALES[landscape.panel_id],
                n_bootstrap=1000,
                seed=REFERENCE_SEED,
            )
            for landscape in landscapes
        }
        masks = pd.read_csv(raw / "masks.csv")
        experiments = pd.read_csv(raw / "experiments.csv")
        feature_columns = ["measurement_fraction", "design_coherence", "design_coherence_p95", "design_alias_fraction", "design_condition", "replicate_variance", "replicate_snr", "support_sparsity", "pure_hoi_fraction", "positive_support_fraction"]
        group_columns = ["landscape", "measurement_budget", "mask_seed", "adaptive_policy"]
        for key, index in experiments.groupby(group_columns).groups.items():
            landscape_id, budget, seed, policy = key
            landscape = by_id[landscape_id]
            if policy == "row_cosine_v0":
                continue
            selected = design_balanced_mask(landscape.dimension, int(budget), int(seed)) if policy == "d_optimal_rows" else _masks_for(masks, landscape.n_cells, int(budget), int(seed))
            features = _mechanism_features(landscape, reveal(landscape, selected, PRIMARY_SCALES[landscape.panel_id]), references[landscape_id])
            for column in feature_columns:
                experiments.loc[index, column] = features[column]
        experiments.to_csv(raw / "experiments.csv", index=False)
        support_reference = pd.read_csv(raw / "support_reference.csv")
        rule_rows = []
        for (panel_id, landscape_id), group in support_reference.groupby(["panel_id", "landscape_id"]):
            group = group.sort_values("term_mask")
            high = group.order.to_numpy() >= 3
            primary_sign = group.support_sign.to_numpy(dtype=int)
            p_value = np.minimum(1.0, 2.0 * (1.0 - group.sign_stability.to_numpy()))
            high_p = p_value[high]
            order = np.argsort(high_p)
            accepted = high_p[order] <= 0.10 * (np.arange(len(order)) + 1) / len(order)
            cutoff = high_p[order][np.flatnonzero(accepted)[-1]] if accepted.any() else -1.0
            practical = np.abs(group.coefficient.to_numpy()) >= group.practical_threshold.to_numpy()
            candidates = {
                "ci95_practical": primary_sign,
                "sign95_practical": np.where((group.sign_stability.to_numpy() >= 0.95) & practical, np.sign(group.coefficient.to_numpy()), 0).astype(int),
                "bootstrap_sign_bh10_practical": np.where((p_value <= cutoff) & practical, np.sign(group.coefficient.to_numpy()), 0).astype(int),
            }
            for rule, signs in candidates.items():
                rule_rows.append({
                    "panel_id": panel_id,
                    "landscape_id": landscape_id,
                    "rule": rule,
                    "support_count": int(np.count_nonzero(signs[high])),
                    "positive_count": int(np.sum(signs[high] > 0)),
                    "negative_count": int(np.sum(signs[high] < 0)),
                    "jaccard_to_primary": jaccard(signs[high], primary_sign[high]),
                })
        pd.DataFrame(rule_rows).to_csv(raw / "estimand_rule_sensitivity.csv", index=False)
        tuning_trials = pd.read_csv(raw / "tuning_trials.csv")
        summaries = _aggregate(experiments)
        for name, frame in summaries.items():
            frame.to_csv(aggregated / f"{name}.csv", index=False)
        sensitivity = pd.read_csv(raw / "estimand_sensitivity.csv")
        _figures(experiments, sensitivity, figures)
        manifest = json.loads((raw / "run_manifest.json").read_text(encoding="utf-8"))
        manifest.update({"total_runs": len(experiments), "tuning_trials_retained": len(tuning_trials), "mechanism_features_refreshed": True})
        _write_manifest(raw / "run_manifest.json", manifest)
        return
    if args.acquisition_followup_only:
        panels = (load_ishizawa(args.ishizawa), load_diaz_colunga(args.diaz))
        landscapes = _landscapes(panels)
        references = {
            landscape.landscape_id: build_reference_estimand(
                landscape,
                scale=PRIMARY_SCALES[landscape.panel_id],
                n_bootstrap=1000,
                seed=REFERENCE_SEED,
            )
            for landscape in landscapes
        }
        existing = pd.read_csv(raw / "experiments.csv")
        existing.loc[existing.adaptive_policy.eq("design_balanced"), "adaptive_policy"] = "row_cosine_v0"
        methods = ("elastic_net", "noise_weighted", "order_penalty", "ard_support", "combined_v1", "sparse_mobius_iht")
        existing_trials = pd.read_csv(raw / "tuning_trials.csv")
        replaced = (existing.adaptive_policy == "d_optimal_rows") & existing.method.isin(methods)
        replaced_run_ids = set(existing.loc[replaced, "run_id"])
        existing = existing[~replaced]
        existing_trials = existing_trials[~existing_trials.run_id.isin(replaced_run_ids)]
        old_ids = existing.run_id.str.extract(r"(\d+)$")[0].astype(int)
        factories = _method_factories()
        rows, trials, counter = [], [], int(old_ids.max())
        for landscape in landscapes:
            for budget in BUDGETS[landscape.n_cells]:
                for seed in DEVELOPMENT_MASK_SEEDS:
                    selected = design_balanced_mask(landscape.dimension, budget, seed)
                    for method in methods:
                        counter += 1
                        row, trial = _run_one(f"M1-{counter:05d}", landscape, references[landscape.landscape_id], selected, seed, method, factories[method], "d_optimal_rows")
                        rows.append(row); trials.extend(trial)
        additions = _seed_stability(pd.DataFrame(rows))
        experiments = _seed_stability(pd.concat([existing, additions], ignore_index=True))
        tuning_trials = pd.concat([existing_trials, pd.DataFrame(trials)], ignore_index=True)
        tuning_trials = tuning_trials[tuning_trials.run_id.isin(experiments.run_id)]
        experiments.to_csv(raw / "experiments.csv", index=False)
        tuning_trials.to_csv(raw / "tuning_trials.csv", index=False)
        summaries = _aggregate(experiments)
        for name, frame in summaries.items():
            frame.to_csv(aggregated / f"{name}.csv", index=False)
        sensitivity = pd.read_csv(raw / "estimand_sensitivity.csv")
        _figures(experiments, sensitivity, figures)
        manifest = json.loads((raw / "run_manifest.json").read_text(encoding="utf-8"))
        manifest.update({
            "total_runs": len(experiments),
            "tuning_trials_retained": len(tuning_trials),
            "total_method_runtime_seconds": float(experiments.runtime.sum()),
            "acquisition_followup": ["row_cosine_v0 retained", "d_optimal_rows"],
        })
        _write_manifest(raw / "run_manifest.json", manifest)
        return
    if args.hybrid_acquisition_only:
        panels = (load_ishizawa(args.ishizawa), load_diaz_colunga(args.diaz))
        landscapes = _landscapes(panels)
        references = {
            landscape.landscape_id: build_reference_estimand(
                landscape,
                scale=PRIMARY_SCALES[landscape.panel_id],
                n_bootstrap=1000,
                seed=REFERENCE_SEED,
            )
            for landscape in landscapes
        }
        existing = pd.read_csv(raw / "experiments.csv")
        policies = {"hybrid_d25": 0.25, "hybrid_d50": 0.50, "hybrid_d75": 0.75}
        existing_trials = pd.read_csv(raw / "tuning_trials.csv")
        replaced = (existing.method == "elastic_net") & existing.adaptive_policy.isin(policies)
        replaced_run_ids = set(existing.loc[replaced, "run_id"])
        existing = existing[~replaced]
        existing_trials = existing_trials[~existing_trials.run_id.isin(replaced_run_ids)]
        old_ids = existing.run_id.str.extract(r"(\d+)$")[0].astype(int)
        rows, trials, counter = [], [], int(old_ids.max())
        factory = _method_factories()["elastic_net"]
        for landscape in landscapes:
            for budget in BUDGETS[landscape.n_cells]:
                for seed in DEVELOPMENT_MASK_SEEDS:
                    for policy, fraction in policies.items():
                        selected = hybrid_design_mask(landscape.dimension, budget, seed, fraction)
                        counter += 1
                        row, trial = _run_one(f"M1-{counter:05d}", landscape, references[landscape.landscape_id], selected, seed, "elastic_net", factory, policy)
                        rows.append(row); trials.extend(trial)
        additions = _seed_stability(pd.DataFrame(rows))
        experiments = _seed_stability(pd.concat([existing, additions], ignore_index=True))
        tuning_trials = pd.concat([existing_trials, pd.DataFrame(trials)], ignore_index=True)
        tuning_trials = tuning_trials[tuning_trials.run_id.isin(experiments.run_id)]
        experiments.to_csv(raw / "experiments.csv", index=False)
        tuning_trials.to_csv(raw / "tuning_trials.csv", index=False)
        summaries = _aggregate(experiments)
        for name, frame in summaries.items():
            frame.to_csv(aggregated / f"{name}.csv", index=False)
        sensitivity = pd.read_csv(raw / "estimand_sensitivity.csv")
        _figures(experiments, sensitivity, figures)
        manifest = json.loads((raw / "run_manifest.json").read_text(encoding="utf-8"))
        manifest.update({
            "total_runs": len(experiments),
            "tuning_trials_retained": len(tuning_trials),
            "total_method_runtime_seconds": float(experiments.runtime.sum()),
            "hybrid_acquisition_fractions": list(policies.values()),
        })
        _write_manifest(raw / "run_manifest.json", manifest)
        return
    panels = (load_ishizawa(args.ishizawa), load_diaz_colunga(args.diaz))
    landscapes = _landscapes(panels)
    normalized_replicate_frame(panels).to_csv(raw / "panel_replicates.csv", index=False)
    data_audit, replicate_statistics = _data_audit(panels, PRIMARY_SCALES)
    data_audit.to_csv(raw / "data_audit.csv", index=False)
    replicate_statistics.to_csv(raw / "replicate_statistics.csv", index=False)
    references, support_reference, sensitivity = _reference_audit(landscapes)
    support_reference.to_csv(raw / "support_reference.csv", index=False)
    sensitivity.to_csv(raw / "estimand_sensitivity.csv", index=False)
    masks = _mask_table()
    masks.to_csv(raw / "masks.csv", index=False)
    experiments, tuning_trials = _run_experiments(landscapes, references, masks)
    experiments.to_csv(raw / "experiments.csv", index=False)
    tuning_trials.to_csv(raw / "tuning_trials.csv", index=False)
    summaries = _aggregate(experiments)
    for name, frame in summaries.items():
        frame.to_csv(aggregated / f"{name}.csv", index=False)
    _figures(experiments, sensitivity, figures)
    elapsed = perf_counter() - start
    manifest = {
        "source_versions": {panel.panel_id: panel.source_version for panel in panels},
        "landscapes": len(landscapes),
        "development_mask_seeds": DEVELOPMENT_MASK_SEEDS,
        "confirmation_mask_seeds_reserved": CONFIRMATION_MASK_SEEDS,
        "total_runs": len(experiments),
        "tuning_trials_retained": len(tuning_trials),
        "wall_seconds": elapsed,
        "gpu_hours": 0.0,
    }
    _write_manifest(raw / "run_manifest.json", manifest)


if __name__ == "__main__":
    main()
