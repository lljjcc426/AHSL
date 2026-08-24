"""Aggregation and paired structural-gain tables for Phase A0.5."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


GROUP_COLUMNS = [
    "experiment_type",
    "n",
    "m",
    "tree_topology",
    "branch_probability",
    "noise_setting",
    "p_false_positive",
    "p_false_negative",
    "num_observations",
    "model",
    "tree_source",
    "requested_tree_swaps",
    "requested_offclass_fraction",
]

METRICS = [
    "tree_edge_disagreement",
    "offclass_fraction",
    "clean_riv",
    "predicted_riv",
    "clean_hamming_error",
    "clean_f1",
    "exact_row_recovery",
    "mean_symmetric_difference",
    "average_hyperedge_jaccard",
    "average_hyperedge_f1",
    "clean_density",
    "predicted_density",
    "runtime_seconds",
    "runtime_per_row",
    "runtime_per_nm",
    "optimal_tie_fraction",
    "mean_selected_subtree_size",
    "objective_value",
    "estimated_tree_clean_riv",
    "estimated_incidence_riv",
]


def rebuild_combined_raw(raw_directory: Path) -> pd.DataFrame:
    """Combine completed stage-specific raw files without including dry runs."""
    paths = sorted(
        path
        for path in raw_directory.glob("*_results.csv")
        if path.name != "a0_5_results.csv" and "dry_run" not in path.name
    )
    if not paths:
        return pd.DataFrame()
    combined = pd.concat((pd.read_csv(path) for path in paths), ignore_index=True)
    combined.to_csv(raw_directory / "a0_5_results.csv", index=False)
    return combined


def aggregate_results(raw: pd.DataFrame) -> pd.DataFrame:
    available_groups = [column for column in GROUP_COLUMNS if column in raw]
    available_metrics = [column for column in METRICS if column in raw]
    result = raw.groupby(available_groups, dropna=False)[available_metrics].agg(
        ["mean", "std", "count"]
    )
    result.columns = [f"{metric}_{stat}" for metric, stat in result.columns]
    return result.reset_index()


def _paired_rows(
    raw: pd.DataFrame,
    experiment_type: str,
    left_model: str,
    right_model: str,
) -> pd.DataFrame:
    selected = raw[raw["experiment_type"] == experiment_type]
    identifiers = [
        "experiment_id",
        "seed",
        "n",
        "m",
        "tree_topology",
        "branch_probability",
        "noise_setting",
        "p_false_positive",
        "p_false_negative",
        "num_observations",
        "tree_source",
        "requested_tree_swaps",
        "requested_offclass_fraction",
        "tree_edge_disagreement",
        "offclass_fraction",
    ]
    identifiers = [column for column in identifiers if column in selected]
    metric_columns = [
        "clean_hamming_error",
        "exact_row_recovery",
        "clean_f1",
        "average_hyperedge_f1",
    ]
    left = selected[selected["model"] == left_model][identifiers + metric_columns]
    right = selected[selected["model"] == right_model][identifiers + metric_columns]
    merged = left.merge(right, on=identifiers, suffixes=("_left", "_right"))
    if merged.empty:
        return merged
    merged["hamming_difference_left_minus_right"] = (
        merged["clean_hamming_error_left"] - merged["clean_hamming_error_right"]
    )
    merged["hamming_error_reduction"] = -merged[
        "hamming_difference_left_minus_right"
    ]
    for metric in ("exact_row_recovery", "clean_f1", "average_hyperedge_f1"):
        merged[f"{metric}_gain"] = (
            merged[f"{metric}_left"] - merged[f"{metric}_right"]
        )
    merged["left_model"] = left_model
    merged["right_model"] = right_model
    return merged


def _seed_bootstrap_summary(
    paired: pd.DataFrame,
    group_columns: list[str],
    samples: int = 2000,
    seed: int = 0,
) -> pd.DataFrame:
    if paired.empty:
        return paired
    rng = np.random.default_rng(seed)
    records: list[dict[str, object]] = []
    effect_columns = [
        "hamming_difference_left_minus_right",
        "hamming_error_reduction",
        "exact_row_recovery_gain",
        "clean_f1_gain",
        "average_hyperedge_f1_gain",
    ]
    for setting, group in paired.groupby(group_columns, dropna=False):
        setting_tuple = setting if isinstance(setting, tuple) else (setting,)
        record = dict(zip(group_columns, setting_tuple, strict=True))
        seeds = np.array(sorted(group["seed"].unique()))
        bootstrap_seed_indices = rng.integers(0, len(seeds), size=(samples, len(seeds)))
        for effect in effect_columns:
            per_seed = group.groupby("seed")[effect].mean().reindex(seeds).to_numpy()
            bootstrap_means = per_seed[bootstrap_seed_indices].mean(axis=1)
            record[f"{effect}_mean"] = float(per_seed.mean())
            record[f"{effect}_std"] = float(per_seed.std(ddof=1)) if len(seeds) > 1 else np.nan
            record[f"{effect}_ci_lower"] = float(np.quantile(bootstrap_means, 0.025))
            record[f"{effect}_ci_upper"] = float(np.quantile(bootstrap_means, 0.975))
        record["num_seeds"] = len(seeds)
        records.append(record)
    return pd.DataFrame.from_records(records)


def structural_gain_table(raw: pd.DataFrame) -> pd.DataFrame:
    connected = _paired_rows(
        raw,
        "core",
        "DPNoiseAwareConnectedMLE",
        "NoiseAwareIndependentNonemptyMLE",
    )
    nonempty = _paired_rows(
        raw,
        "core",
        "NoiseAwareIndependentNonemptyMLE",
        "NoiseAwareIndependentMLE",
    )
    paired = pd.concat([connected, nonempty], ignore_index=True)
    groups = [
        "left_model",
        "right_model",
        "n",
        "m",
        "tree_topology",
        "branch_probability",
        "noise_setting",
        "num_observations",
    ]
    return _seed_bootstrap_summary(paired, groups, seed=1001)


def robustness_table(raw: pd.DataFrame, experiment_type: str) -> pd.DataFrame:
    paired = _paired_rows(
        raw,
        experiment_type,
        "DPNoiseAwareConnectedMLE",
        "NoiseAwareIndependentNonemptyMLE",
    )
    if experiment_type == "wrong_tree":
        groups = [
            "tree_topology",
            "tree_source",
            "requested_tree_swaps",
            "tree_edge_disagreement",
        ]
    else:
        groups = [
            "tree_topology",
            "requested_offclass_fraction",
            "offclass_fraction",
        ]
    return _seed_bootstrap_summary(paired, groups, seed=2002)


def generator_prior_gap_table(raw: pd.DataFrame) -> pd.DataFrame:
    paired = _paired_rows(
        raw,
        "core",
        "GeneratorPriorConnectedMAP",
        "DPNoiseAwareConnectedMLE",
    )
    groups = [
        "tree_topology",
        "branch_probability",
        "noise_setting",
        "num_observations",
    ]
    return _seed_bootstrap_summary(paired, groups, seed=3003)


def write_analysis_outputs(raw: pd.DataFrame, aggregate_directory: Path) -> None:
    aggregate_directory.mkdir(parents=True, exist_ok=True)
    aggregate_results(raw).to_csv(
        aggregate_directory / "a0_5_summary.csv", index=False
    )
    structural_gain_table(raw).to_csv(
        aggregate_directory / "a0_5_structural_gain.csv", index=False
    )
    robustness_table(raw, "wrong_tree").to_csv(
        aggregate_directory / "a0_5_tree_robustness.csv", index=False
    )
    robustness_table(raw, "offclass").to_csv(
        aggregate_directory / "a0_5_offclass.csv", index=False
    )
    a1 = raw[raw["experiment_type"] == "a1_gate"].copy()
    a1.to_csv(aggregate_directory / "a0_5_a1_gate.csv", index=False)
    generator_prior_gap_table(raw).to_csv(
        aggregate_directory / "a0_5_generator_prior_gap.csv", index=False
    )

