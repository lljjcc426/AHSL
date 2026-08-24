"""Paired seed-level analysis for Phase A1."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ESTIMATORS = [
    "GeneratingTreeOracle",
    "DataAgnosticRandomTree",
    "BinaryMWST",
    "NoiseCorrectedMWST",
    "BootstrapStabilityMWST",
    "OracleQMarginalTree",
    "EstimatedQMarginalTree",
]
DECODERS = ["MatchedPrior", "UniformConnectedMLE"]


def paired_effects(raw: pd.DataFrame) -> pd.DataFrame:
    keys = ["seed", "tree_topology", "decoder"]
    reference = raw[raw["estimator"] == "GeneratingTreeOracle"][
        keys + ["test_hamming_error", "test_exact_row_recovery"]
    ].rename(
        columns={
            "test_hamming_error": "reference_hamming",
            "test_exact_row_recovery": "reference_exact_row_recovery",
        }
    )
    paired = raw.merge(reference, on=keys, how="left")
    paired["test_hamming_excess"] = (
        paired["test_hamming_error"] - paired["reference_hamming"]
    )
    paired["test_exact_row_difference"] = (
        paired["test_exact_row_recovery"]
        - paired["reference_exact_row_recovery"]
    )
    return paired


def _bootstrap_interval(
    values: pd.Series, seed: int, samples: int = 5000
) -> tuple[float, float, float, float]:
    array = values.to_numpy(dtype=float)
    rng = np.random.default_rng(seed)
    resamples = array[
        rng.integers(0, len(array), size=(samples, len(array)))
    ].mean(axis=1)
    return (
        float(array.mean()),
        float(array.std(ddof=1)) if len(array) > 1 else np.nan,
        float(np.quantile(resamples, 0.025)),
        float(np.quantile(resamples, 0.975)),
    )


def _seed_level(frame: pd.DataFrame) -> pd.DataFrame:
    numeric = [
        "test_hamming_error",
        "test_hamming_excess",
        "test_exact_row_recovery",
        "test_clean_f1",
        "train_nll_per_row",
        "validation_nll_per_row",
        "test_nll_per_row",
        "tree_edge_disagreement",
        "tree_runtime_seconds",
        "q_absolute_error",
    ]
    return frame.groupby(["estimator", "decoder", "seed"], as_index=False)[
        numeric
    ].mean()


def primary_result_table(raw: pd.DataFrame) -> pd.DataFrame:
    paired = paired_effects(raw)
    scopes = [("overall", paired)] + [
        (topology, paired[paired["tree_topology"] == topology])
        for topology in sorted(paired["tree_topology"].unique())
    ]
    records = []
    for scope_index, (scope, frame) in enumerate(scopes):
        seed_level = _seed_level(frame)
        for estimator_index, estimator in enumerate(ESTIMATORS):
            for decoder_index, decoder in enumerate(DECODERS):
                rows = seed_level[
                    (seed_level["estimator"] == estimator)
                    & (seed_level["decoder"] == decoder)
                ]
                mean, sd, lower, upper = _bootstrap_interval(
                    rows["test_hamming_excess"],
                    11000 + 100 * scope_index + 10 * estimator_index + decoder_index,
                )
                records.append(
                    {
                        "scope": scope,
                        "estimator": estimator,
                        "decoder": decoder,
                        "mean_test_hamming": rows["test_hamming_error"].mean(),
                        "mean_test_hamming_excess": mean,
                        "excess_sd": sd,
                        "excess_ci_lower": lower,
                        "excess_ci_upper": upper,
                        "mean_exact_row_recovery": rows[
                            "test_exact_row_recovery"
                        ].mean(),
                        "mean_test_clean_f1": rows["test_clean_f1"].mean(),
                        "mean_train_nll_per_row": rows["train_nll_per_row"].mean(),
                        "mean_validation_nll_per_row": rows[
                            "validation_nll_per_row"
                        ].mean(),
                        "mean_test_nll_per_row": rows["test_nll_per_row"].mean(),
                        "mean_tree_edge_disagreement": rows[
                            "tree_edge_disagreement"
                        ].mean(),
                        "mean_tree_runtime_seconds": rows[
                            "tree_runtime_seconds"
                        ].mean(),
                        "mean_q_absolute_error": rows["q_absolute_error"].mean(),
                        "num_seeds": len(rows),
                    }
                )
    return pd.DataFrame.from_records(records)


def decoder_comparison(raw: pd.DataFrame) -> pd.DataFrame:
    pivot = raw.pivot_table(
        index=["estimator", "seed", "tree_topology"],
        columns="decoder",
        values="test_hamming_error",
    ).reset_index()
    pivot["matched_minus_uniform_hamming"] = (
        pivot["MatchedPrior"] - pivot["UniformConnectedMLE"]
    )
    return (
        pivot.groupby(["estimator", "tree_topology"], as_index=False)
        .agg(
            matched_hamming=("MatchedPrior", "mean"),
            uniform_hamming=("UniformConnectedMLE", "mean"),
            matched_minus_uniform_hamming=(
                "matched_minus_uniform_hamming",
                "mean",
            ),
        )
    )


def likelihood_behavior(raw: pd.DataFrame) -> pd.DataFrame:
    rows = raw[
        (raw["decoder"] == "MatchedPrior")
        & raw["estimator"].isin(
            ["OracleQMarginalTree", "EstimatedQMarginalTree"]
        )
    ]
    return (
        rows.groupby("estimator", as_index=False)
        .agg(
            mean_train_nll_gain=("train_nll_gain_vs_initial", "mean"),
            mean_validation_nll_gain=("validation_nll_gain_vs_initial", "mean"),
            mean_test_nll_gain=("test_nll_gain_vs_initial", "mean"),
            validation_worsened_fraction=(
                "validation_nll_gain_vs_initial",
                lambda values: float((values < 0.0).mean()),
            ),
            test_worsened_fraction=(
                "test_nll_gain_vs_initial",
                lambda values: float((values < 0.0).mean()),
            ),
        )
    )


def gate_summary(table: pd.DataFrame, raw: pd.DataFrame) -> pd.DataFrame:
    matched = table[
        (table["scope"] == "overall") & (table["decoder"] == "MatchedPrior")
    ].set_index("estimator")
    excess = matched["mean_test_hamming_excess"]
    binary = float(excess["BinaryMWST"])
    marginal = float(excess["EstimatedQMarginalTree"])
    gap_closure = 1.0 - marginal / binary if binary > 0.0 else np.nan
    true_tree_value = float(excess["DataAgnosticRandomTree"])
    kill_neural = marginal <= 0.005 or (
        gap_closure >= 0.80 and marginal < 0.01
    )
    kill_tree_identity = true_tree_value <= 0.005
    topology_rows = table[
        (table["scope"] != "overall")
        & (table["decoder"] == "MatchedPrior")
        & (table["estimator"] == "EstimatedQMarginalTree")
    ]
    residual_topologies = int(
        (topology_rows["mean_test_hamming_excess"] > 0.01).sum()
    )
    oracle_improves_classical = float(excess["OracleQMarginalTree"]) < float(
        excess[
            ["BinaryMWST", "NoiseCorrectedMWST", "BootstrapStabilityMWST"]
        ].min()
    )
    likelihood = likelihood_behavior(raw).set_index("estimator")
    validation_systematically_worsens = bool(
        (likelihood["validation_worsened_fraction"] > 0.5).any()
    )
    positive_continuation = (
        not kill_neural
        and not kill_tree_identity
        and marginal > 0.01
        and residual_topologies >= 3
        and oracle_improves_classical
        and not validation_systematically_worsens
    )

    if kill_tree_identity:
        decision_code = "B"
        decision = (
            "Kill join-tree identity learning; subtree/structural prior modeling is "
            "the more meaningful problem."
        )
    elif kill_neural:
        decision_code = "A"
        decision = (
            "Kill neural join-tree learning; marginal-likelihood classical "
            "estimation closes the meaningful gap."
        )
    elif positive_continuation:
        decision_code = "D"
        decision = (
            "A robust residual remains after literature-grounded classical "
            "marginal estimation; a learned/shared structural model is "
            "scientifically justified."
        )
    else:
        decision_code = "C"
        decision = (
            "A residual latent-tree problem remains, but current formulation or "
            "identifiability is insufficient; do not build neural models yet."
        )

    return pd.DataFrame(
        [
            {
                "binary_excess": binary,
                "noise_corrected_excess": float(excess["NoiseCorrectedMWST"]),
                "bootstrap_excess": float(excess["BootstrapStabilityMWST"]),
                "oracle_q_marginal_excess": float(excess["OracleQMarginalTree"]),
                "estimated_q_marginal_excess": marginal,
                "gap_closure_fraction": gap_closure,
                "true_tree_value": true_tree_value,
                "kill_neural_rule_met": kill_neural,
                "kill_tree_identity_rule_met": kill_tree_identity,
                "residual_topologies_over_0_01": residual_topologies,
                "oracle_q_improves_classical": oracle_improves_classical,
                "validation_systematically_worsens": (
                    validation_systematically_worsens
                ),
                "positive_continuation_conditions_met": positive_continuation,
                "final_decision_code": decision_code,
                "final_decision": decision,
            }
        ]
    )


def write_primary_analysis(raw: pd.DataFrame, output_directory: Path) -> pd.DataFrame:
    output_directory.mkdir(parents=True, exist_ok=True)
    table = primary_result_table(raw)
    table.to_csv(output_directory / "a1_primary_table.csv", index=False)
    paired_effects(raw).to_csv(
        output_directory / "a1_primary_paired_effects.csv", index=False
    )
    decoder_comparison(raw).to_csv(
        output_directory / "a1_decoder_comparison.csv", index=False
    )
    likelihood_behavior(raw).to_csv(
        output_directory / "a1_likelihood_behavior.csv", index=False
    )
    gate = gate_summary(table, raw)
    gate.to_csv(output_directory / "a1_gate_summary.csv", index=False)
    return gate
