"""Aggregation and paired statistical comparisons for A0 results."""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import wilcoxon


SETTING_COLUMNS = [
    "n",
    "m",
    "tree_topology",
    "branch_probability",
    "p_false_positive",
    "p_false_negative",
    "num_observations",
]

METRIC_COLUMNS = [
    "train_loss",
    "clean_precision",
    "clean_recall",
    "clean_f1",
    "hamming_error",
    "exact_row_recovery",
    "mean_symmetric_difference",
    "running_intersection_violations",
    "predicted_density",
    "clean_density",
    "observed_density",
    "reconstruction_bce",
    "average_hyperedge_jaccard",
    "average_hyperedge_f1",
    "exact_hyperedge_recovery",
    "runtime_seconds",
    "num_connected_subtrees",
    "mean_predicted_row_size",
    "singleton_prediction_fraction",
    "mean_categorical_entropy",
    "mean_max_subtree_probability",
]


def aggregate_results(raw: pd.DataFrame) -> pd.DataFrame:
    """Compute mean, standard deviation, and sample count for every setting."""
    group_columns = SETTING_COLUMNS + ["model", "hyperparameters"]
    available_metrics = [column for column in METRIC_COLUMNS if column in raw]
    aggregated = raw.groupby(group_columns, dropna=False)[available_metrics].agg(
        ["mean", "std", "count"]
    )
    aggregated.columns = [f"{metric}_{statistic}" for metric, statistic in aggregated.columns]
    return aggregated.reset_index()


def _bootstrap_interval(
    differences: np.ndarray, samples: int, rng: np.random.Generator
) -> tuple[float, float]:
    indices = rng.integers(0, len(differences), size=(samples, len(differences)))
    means = differences[indices].mean(axis=1)
    lower, upper = np.quantile(means, [0.025, 0.975])
    return float(lower), float(upper)


def paired_statistical_tests(
    raw: pd.DataFrame,
    bootstrap_samples: int = 2000,
    seed: int = 0,
) -> pd.DataFrame:
    """Compare AHSL with each baseline on paired synthetic datasets.

    Wilcoxon tests are reported only with at least five non-identical pairs.
    Effect sizes and paired bootstrap intervals remain the primary quantities.
    """
    ahsl = raw[raw["model"] == "FixedTreeAHSL"]
    baselines = raw[raw["model"] != "FixedTreeAHSL"]
    merge_columns = ["experiment_id", "seed", *SETTING_COLUMNS]
    records: list[dict[str, object]] = []
    rng = np.random.default_rng(seed)

    for (baseline_model, baseline_hyperparameters), baseline in baselines.groupby(
        ["model", "hyperparameters"], dropna=False
    ):
        merged = ahsl.merge(
            baseline,
            on=merge_columns,
            suffixes=("_ahsl", "_baseline"),
        )
        for setting, group in merged.groupby(SETTING_COLUMNS, dropna=False):
            setting_values = dict(zip(SETTING_COLUMNS, setting, strict=True))
            for metric in ("clean_f1", "exact_row_recovery"):
                differences = (
                    group[f"{metric}_ahsl"].to_numpy()
                    - group[f"{metric}_baseline"].to_numpy()
                )
                lower, upper = _bootstrap_interval(differences, bootstrap_samples, rng)
                nonzero = differences[~np.isclose(differences, 0.0)]
                p_value = np.nan
                if len(nonzero) >= 5:
                    p_value = float(wilcoxon(nonzero).pvalue)
                records.append(
                    {
                        **setting_values,
                        "baseline_model": baseline_model,
                        "baseline_hyperparameters": baseline_hyperparameters,
                        "metric": metric,
                        "num_pairs": len(differences),
                        "mean_paired_difference_ahsl_minus_baseline": float(differences.mean()),
                        "std_paired_difference": float(differences.std(ddof=1))
                        if len(differences) > 1
                        else np.nan,
                        "bootstrap_ci_lower": lower,
                        "bootstrap_ci_upper": upper,
                        "proportion_ahsl_better": float((differences > 0).mean()),
                        "wilcoxon_p_value": p_value,
                    }
                )
    return pd.DataFrame.from_records(records)
