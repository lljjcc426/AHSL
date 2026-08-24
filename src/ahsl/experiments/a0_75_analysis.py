"""Paired seed-level analysis for the Phase A0.75 kill-test."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


PRIMARY_ESTIMATORS = [
    "TrueTreeOracle",
    "DataAgnosticRandomTree",
    "BinaryMWST",
    "NoiseCorrectedMWST",
    "BootstrapStabilityMWST",
    "AlternatingTreeIncidenceEstimator",
]
CLASSICAL_ESTIMATORS = [
    "BinaryMWST",
    "NoiseCorrectedMWST",
    "BootstrapStabilityMWST",
    "AlternatingTreeIncidenceEstimator",
]


def primary_control_rows(raw: pd.DataFrame) -> pd.DataFrame:
    random_primary = (raw["estimator"] != "DataAgnosticRandomTree") | raw[
        "random_tree_replicate"
    ].eq(0)
    return raw[random_primary].copy()


def paired_effects(raw: pd.DataFrame) -> pd.DataFrame:
    selected = primary_control_rows(raw)
    keys = ["experiment_type", "seed", "tree_topology", "num_observations"]
    oracle = selected[selected["estimator"] == "TrueTreeOracle"][
        keys + ["clean_hamming_error", "exact_row_recovery"]
    ].rename(
        columns={
            "clean_hamming_error": "oracle_hamming",
            "exact_row_recovery": "oracle_exact_row_recovery",
        }
    )
    paired = selected.merge(oracle, on=keys, how="left")
    paired["downstream_excess"] = (
        paired["clean_hamming_error"] - paired["oracle_hamming"]
    )
    paired["exact_row_difference"] = (
        paired["exact_row_recovery"] - paired["oracle_exact_row_recovery"]
    )
    return paired


def _bootstrap_interval(
    values: pd.Series,
    seed: int,
    samples: int = 5000,
) -> tuple[float, float, float, float]:
    array = values.to_numpy(dtype=float)
    rng = np.random.default_rng(seed)
    bootstrap = array[rng.integers(0, len(array), size=(samples, len(array)))].mean(axis=1)
    standard_deviation = float(array.std(ddof=1)) if len(array) > 1 else np.nan
    return (
        float(array.mean()),
        standard_deviation,
        float(np.quantile(bootstrap, 0.025)),
        float(np.quantile(bootstrap, 0.975)),
    )


def _seed_level(frame: pd.DataFrame, topology: str | None) -> pd.DataFrame:
    selected = frame if topology is None else frame[frame["tree_topology"] == topology]
    numeric = [
        "clean_hamming_error",
        "downstream_excess",
        "exact_row_recovery",
        "clean_f1",
        "valid_clean_join_tree",
        "tree_edge_disagreement",
        "runtime_seconds",
    ]
    return selected.groupby(["estimator", "seed"], as_index=False)[numeric].mean()


def primary_result_table(raw: pd.DataFrame) -> pd.DataFrame:
    effects = paired_effects(raw)
    records: list[dict[str, object]] = []
    scopes: list[tuple[str, str | None]] = [("overall", None)] + [
        (topology, topology) for topology in sorted(effects["tree_topology"].unique())
    ]
    for scope, topology in scopes:
        seed_level = _seed_level(effects, topology)
        for estimator_index, estimator in enumerate(PRIMARY_ESTIMATORS):
            rows = seed_level[seed_level["estimator"] == estimator]
            mean, sd, lower, upper = _bootstrap_interval(
                rows["downstream_excess"], 7500 + estimator_index
            )
            records.append(
                {
                    "scope": scope,
                    "estimator": estimator,
                    "mean_hamming": rows["clean_hamming_error"].mean(),
                    "mean_excess": mean,
                    "excess_sd": sd,
                    "excess_ci_lower": lower,
                    "excess_ci_upper": upper,
                    "exact_row_recovery": rows["exact_row_recovery"].mean(),
                    "clean_f1": rows["clean_f1"].mean(),
                    "valid_clean_join_tree_rate": rows["valid_clean_join_tree"].mean(),
                    "tree_edge_disagreement": rows["tree_edge_disagreement"].mean(),
                    "runtime_seconds": rows["runtime_seconds"].mean(),
                    "num_seeds": len(rows),
                }
            )
    return pd.DataFrame.from_records(records)


def random_tree_diagnostics(raw: pd.DataFrame) -> pd.DataFrame:
    random_rows = raw[raw["estimator"] == "DataAgnosticRandomTree"]
    per_dataset = (
        random_rows.groupby(["experiment_type", "seed", "tree_topology"])
        .agg(
            random_mean_hamming=("clean_hamming_error", "mean"),
            random_best_of_5_hamming=("clean_hamming_error", "min"),
            random_across_tree_sd=("clean_hamming_error", "std"),
            primary_random_hamming=(
                "clean_hamming_error",
                lambda values: values.iloc[0],
            ),
        )
        .reset_index()
    )
    return per_dataset


def alternating_diagnostics(raw: pd.DataFrame) -> pd.DataFrame:
    rows = raw[raw["estimator"] == "AlternatingTreeIncidenceEstimator"]
    records = []
    for scope, group in [("overall", rows)] + [
        (topology, rows[rows["tree_topology"] == topology])
        for topology in sorted(rows["tree_topology"].unique())
    ]:
        records.append(
            {
                "scope": scope,
                "converged_0_fraction": (group["num_iterations"] == 0).mean(),
                "converged_1_fraction": (
                    (group["num_iterations"] == 1) & group["converged"]
                ).mean(),
                "converged_2plus_fraction": (
                    (group["num_iterations"] >= 2) & group["converged"]
                ).mean(),
                "max_iteration_reached_fraction": group[
                    "max_iteration_reached"
                ].mean(),
                "final_tree_differs_fraction": group["tree_changed"].mean(),
            }
        )
    return pd.DataFrame.from_records(records)


def edge_utility_correlations(raw: pd.DataFrame) -> pd.DataFrame:
    effects = paired_effects(raw)
    effects = effects[effects["estimator"] != "TrueTreeOracle"]
    records = []
    for scope, group in [("overall", effects)] + [
        (topology, effects[effects["tree_topology"] == topology])
        for topology in sorted(effects["tree_topology"].unique())
    ]:
        records.append(
            {
                "scope": scope,
                "pearson": group["tree_edge_disagreement"].corr(
                    group["downstream_excess"], method="pearson"
                ),
                "spearman": group["tree_edge_disagreement"].corr(
                    group["downstream_excess"], method="spearman"
                ),
                "num_rows": len(group),
            }
        )
    return pd.DataFrame.from_records(records)


def gate_summary(table: pd.DataFrame) -> pd.DataFrame:
    overall = table[table["scope"] == "overall"].set_index("estimator")
    classical = overall.loc[CLASSICAL_ESTIMATORS]
    best_name = str(classical["mean_excess"].idxmin())
    best = classical.loc[best_name]
    binary_excess = float(overall.loc["BinaryMWST", "mean_excess"])
    best_excess = float(best["mean_excess"])
    gap_closure = (
        1.0 - best_excess / binary_excess if binary_excess > 0.0 else np.nan
    )
    true_tree_value = float(
        overall.loc["DataAgnosticRandomTree", "mean_excess"]
    )
    stop_a = best_excess <= 0.005 and float(best["excess_ci_upper"]) <= 0.010
    stop_b = true_tree_value <= 0.005
    stop_c = gap_closure >= 0.80 and best_excess < 0.01
    return pd.DataFrame(
        [
            {
                "best_classical_estimator": best_name,
                "best_classical_excess": best_excess,
                "best_classical_ci_lower": float(best["excess_ci_lower"]),
                "best_classical_ci_upper": float(best["excess_ci_upper"]),
                "binary_excess": binary_excess,
                "gap_closure_fraction": gap_closure,
                "value_of_true_tree": true_tree_value,
                "hard_stop_a": stop_a,
                "hard_stop_b": stop_b,
                "hard_stop_c": stop_c,
                "profile_search_triggered": best_excess > 0.01,
            }
        ]
    )


def write_analysis_outputs(
    raw: pd.DataFrame,
    output_directory: Path,
    prefix: str,
) -> pd.DataFrame:
    output_directory.mkdir(parents=True, exist_ok=True)
    table = primary_result_table(raw)
    table.to_csv(output_directory / f"{prefix}_table.csv", index=False)
    paired_effects(raw).to_csv(
        output_directory / f"{prefix}_paired_effects.csv", index=False
    )
    random_tree_diagnostics(raw).to_csv(
        output_directory / f"{prefix}_random_tree_diagnostics.csv", index=False
    )
    alternating_diagnostics(raw).to_csv(
        output_directory / f"{prefix}_alternating_diagnostics.csv", index=False
    )
    edge_utility_correlations(raw).to_csv(
        output_directory / f"{prefix}_edge_utility_correlations.csv", index=False
    )
    gate = gate_summary(table)
    gate.to_csv(output_directory / f"{prefix}_gate_summary.csv", index=False)
    return gate
