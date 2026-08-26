"""Paired seed-level analysis and preregistered gates for Phase A1.5."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


TREE_SOURCES = [
    "GeneratingTreeOracle",
    "DataAgnosticRandomTree",
    "BinaryMWST",
    "NoiseCorrectedMWST",
    "BootstrapStabilityMWST",
    "OracleQMarginalTree",
    "EstimatedQMarginalTree",
]
DECODERS = [
    "PosteriorMAPConnected",
    "PosteriorMedianUnconstrained",
    "ConnectedBayesHamming",
]


def _bootstrap_interval(
    values: pd.Series, seed: int, samples: int = 10000
) -> tuple[float, float, float, float]:
    array = values.to_numpy(dtype=float)
    rng = np.random.default_rng(seed)
    means = array[rng.integers(0, len(array), size=(samples, len(array)))].mean(axis=1)
    return (
        float(array.mean()),
        float(array.std(ddof=1)) if len(array) > 1 else np.nan,
        float(np.quantile(means, 0.025)),
        float(np.quantile(means, 0.975)),
    )


def _scope_frames(frame: pd.DataFrame):
    yield "overall", frame
    for topology in sorted(frame["tree_topology"].unique()):
        yield topology, frame[frame["tree_topology"] == topology]


def primary_table(raw: pd.DataFrame) -> pd.DataFrame:
    reference_keys = ["dataset_id", "q_mode", "decoder"]
    reference = raw[raw["tree_source"] == "BinaryMWST"][
        reference_keys + ["test_hamming_error"]
    ].rename(columns={"test_hamming_error": "binary_hamming"})
    paired = raw.merge(reference, on=reference_keys, how="left")
    paired["hamming_minus_binary"] = (
        paired["test_hamming_error"] - paired["binary_hamming"]
    )
    records = []
    for scope_index, (scope, scoped) in enumerate(_scope_frames(paired)):
        seed_level = (
            scoped.groupby(["tree_source", "q_mode", "decoder", "seed"], as_index=False)
            .mean(numeric_only=True)
        )
        for tree_index, tree_source in enumerate(TREE_SOURCES):
            for q_index, q_mode in enumerate(["oracle_q", "estimated_q"]):
                for decoder_index, decoder in enumerate(DECODERS):
                    rows = seed_level[
                        (seed_level["tree_source"] == tree_source)
                        & (seed_level["q_mode"] == q_mode)
                        & (seed_level["decoder"] == decoder)
                    ]
                    mean, sd, lower, upper = _bootstrap_interval(
                        rows["hamming_minus_binary"],
                        15000 + 1000 * scope_index + 100 * tree_index + 10 * q_index + decoder_index,
                    )
                    records.append(
                        {
                            "scope": scope,
                            "tree_source": tree_source,
                            "q_mode": q_mode,
                            "decoder": decoder,
                            "mean_test_hamming": rows["test_hamming_error"].mean(),
                            "mean_hamming_minus_binary": mean,
                            "hamming_difference_sd": sd,
                            "hamming_difference_ci_lower": lower,
                            "hamming_difference_ci_upper": upper,
                            "mean_exact_row_recovery": rows["test_exact_row_recovery"].mean(),
                            "mean_clean_f1": rows["test_clean_f1"].mean(),
                            "mean_posterior_expected_hamming": rows["posterior_expected_hamming"].mean(),
                            "mean_risk_calibration_gap": rows["risk_calibration_gap"].mean(),
                            "mean_risk_row_correlation": rows["risk_row_correlation"].mean(),
                            "median_connected_fraction": rows["median_connected_fraction"].mean(),
                            "median_empty_fraction": rows["median_empty_fraction"].mean(),
                            "median_disconnected_fraction": rows["median_disconnected_fraction"].mean(),
                            "mean_decision_tie_fraction": rows["decision_tie_fraction"].mean(),
                            "mean_tree_edge_disagreement": rows["tree_edge_disagreement"].mean(),
                            "mean_test_nll_per_row": rows["test_nll_per_row"].mean(),
                            "mean_total_inference_runtime_seconds": rows["total_inference_runtime_seconds"].mean(),
                            "num_seeds": len(rows),
                        }
                    )
    return pd.DataFrame.from_records(records)


def _paired_effect(
    raw: pd.DataFrame,
    left_decoder: str,
    right_decoder: str,
    value: str,
    effect_name: str,
) -> pd.DataFrame:
    index = ["dataset_id", "seed", "tree_topology", "tree_source", "q_mode"]
    pivot = raw.pivot(index=index, columns="decoder", values=value).reset_index()
    pivot["effect"] = pivot[left_decoder] - pivot[right_decoder]
    records = []
    for scope_index, (scope, scoped) in enumerate(_scope_frames(pivot)):
        seed_level = scoped.groupby(["tree_source", "q_mode", "seed"], as_index=False)["effect"].mean()
        for tree_index, tree_source in enumerate(TREE_SOURCES):
            for q_index, q_mode in enumerate(["oracle_q", "estimated_q"]):
                values = seed_level[
                    (seed_level["tree_source"] == tree_source)
                    & (seed_level["q_mode"] == q_mode)
                ]["effect"]
                mean, sd, lower, upper = _bootstrap_interval(
                    values, 25000 + 1000 * scope_index + 100 * tree_index + q_index
                )
                records.append(
                    {
                        "effect_name": effect_name,
                        "scope": scope,
                        "tree_source": tree_source,
                        "q_mode": q_mode,
                        "mean_effect": mean,
                        "effect_sd": sd,
                        "ci_lower": lower,
                        "ci_upper": upper,
                        "num_seeds": len(values),
                    }
                )
    return pd.DataFrame.from_records(records)


def decoder_gains(raw: pd.DataFrame) -> pd.DataFrame:
    return _paired_effect(
        raw,
        "PosteriorMAPConnected",
        "ConnectedBayesHamming",
        "test_hamming_error",
        "DecoderGain_MAP_minus_ConnectedMBR",
    )


def connectivity_costs(raw: pd.DataFrame) -> pd.DataFrame:
    empirical = _paired_effect(
        raw,
        "ConnectedBayesHamming",
        "PosteriorMedianUnconstrained",
        "test_hamming_error",
        "ConnectivityCost_empirical",
    )
    posterior = _paired_effect(
        raw,
        "ConnectedBayesHamming",
        "PosteriorMedianUnconstrained",
        "posterior_expected_hamming",
        "ConnectivityCost_posterior",
    )
    return pd.concat([empirical, posterior], ignore_index=True)


def exact_row_tradeoff(raw: pd.DataFrame) -> pd.DataFrame:
    return _paired_effect(
        raw,
        "PosteriorMAPConnected",
        "ConnectedBayesHamming",
        "test_exact_row_recovery",
        "ExactRow_MAP_minus_ConnectedMBR",
    )


def tree_gains(raw: pd.DataFrame) -> pd.DataFrame:
    selected = raw[raw["tree_source"].isin(["BinaryMWST", "EstimatedQMarginalTree"])]
    index = ["dataset_id", "seed", "tree_topology", "q_mode", "decoder"]
    pivot = selected.pivot(index=index, columns="tree_source", values="test_hamming_error").reset_index()
    pivot["tree_gain"] = pivot["BinaryMWST"] - pivot["EstimatedQMarginalTree"]
    records = []
    for scope_index, (scope, scoped) in enumerate(_scope_frames(pivot)):
        seed_level = scoped.groupby(["q_mode", "decoder", "seed"], as_index=False)["tree_gain"].mean()
        for q_index, q_mode in enumerate(["oracle_q", "estimated_q"]):
            for decoder_index, decoder in enumerate(DECODERS):
                values = seed_level[
                    (seed_level["q_mode"] == q_mode)
                    & (seed_level["decoder"] == decoder)
                ]["tree_gain"]
                mean, sd, lower, upper = _bootstrap_interval(
                    values, 35000 + 1000 * scope_index + 100 * q_index + decoder_index
                )
                records.append(
                    {
                        "scope": scope,
                        "q_mode": q_mode,
                        "decoder": decoder,
                        "mean_tree_gain": mean,
                        "tree_gain_sd": sd,
                        "ci_lower": lower,
                        "ci_upper": upper,
                        "num_seeds": len(values),
                    }
                )
    return pd.DataFrame.from_records(records)


def non_tied_tree_gain(risk_rows: pd.DataFrame) -> pd.DataFrame:
    selected = risk_rows[
        (risk_rows["q_mode"] == "estimated_q")
        & (risk_rows["decoder"] == "ConnectedBayesHamming")
        & risk_rows["tree_source"].isin(["BinaryMWST", "EstimatedQMarginalTree"])
    ]
    index = ["dataset_id", "seed", "tree_topology", "test_row"]
    actual = selected.pivot(index=index, columns="tree_source", values="actual_hamming")
    tied = selected.pivot(index=index, columns="tree_source", values="decision_tied")
    valid = ~(tied["BinaryMWST"] | tied["EstimatedQMarginalTree"])
    paired = actual.loc[valid].reset_index()
    paired["tree_gain"] = paired["BinaryMWST"] - paired["EstimatedQMarginalTree"]
    dataset = (
        paired.groupby(["dataset_id", "seed", "tree_topology"], as_index=False)
        .agg(tree_gain=("tree_gain", "mean"), non_tied_test_rows=("tree_gain", "size"))
    )
    records = []
    for scope_index, (scope, scoped) in enumerate(_scope_frames(dataset)):
        seed_level = scoped.groupby("seed")["tree_gain"].mean()
        mean, sd, lower, upper = _bootstrap_interval(seed_level, 45000 + scope_index)
        records.append(
            {
                "scope": scope,
                "mean_tree_gain": mean,
                "tree_gain_sd": sd,
                "ci_lower": lower,
                "ci_upper": upper,
                "num_datasets": len(scoped),
                "num_non_tied_test_rows": int(scoped["non_tied_test_rows"].sum()),
                "num_seeds": len(seed_level),
            }
        )
    return pd.DataFrame.from_records(records)


def gate_summary(
    table: pd.DataFrame,
    gains: pd.DataFrame,
    decoder: pd.DataFrame,
    connectivity: pd.DataFrame,
    non_tied: pd.DataFrame,
) -> pd.DataFrame:
    primary = gains[
        (gains["scope"] == "overall")
        & (gains["q_mode"] == "estimated_q")
        & (gains["decoder"] == "ConnectedBayesHamming")
    ].iloc[0]
    topology = gains[
        (gains["scope"] != "overall")
        & (gains["q_mode"] == "estimated_q")
        & (gains["decoder"] == "ConnectedBayesHamming")
    ]
    topology_count = int((topology["mean_tree_gain"] > 0.005).sum())
    stop_tree = bool(
        primary["mean_tree_gain"] <= 0.005
        or primary["ci_lower"] <= 0.0
        or topology_count < 3
    )
    major_decoder = decoder[
        (decoder["scope"] == "overall")
        & (decoder["q_mode"] == "estimated_q")
    ].set_index("tree_source")
    binary_decoder_gain = float(major_decoder.loc["BinaryMWST", "mean_effect"])
    estimated_decoder_gain = float(
        major_decoder.loc["EstimatedQMarginalTree", "mean_effect"]
    )
    generating_decoder_gain = float(
        major_decoder.loc["GeneratingTreeOracle", "mean_effect"]
    )
    non_tied_overall = non_tied[non_tied["scope"] == "overall"].iloc[0]
    survives_non_tied = bool(
        non_tied_overall["mean_tree_gain"] > 0.005
        and non_tied_overall["ci_lower"] > 0.0
    )
    calibration = table[
        (table["scope"] == "overall")
        & (table["q_mode"] == "estimated_q")
        & (table["decoder"] == "ConnectedBayesHamming")
        & (table["tree_source"].isin(["BinaryMWST", "EstimatedQMarginalTree"]))
    ]
    max_abs_calibration_gap = float(calibration["mean_risk_calibration_gap"].abs().max())
    reasonably_calibrated = max_abs_calibration_gap <= 0.02

    oracle_connectivity = connectivity[
        (connectivity["effect_name"] == "ConnectivityCost_empirical")
        & (connectivity["scope"] != "overall")
        & (connectivity["q_mode"] == "oracle_q")
        & (connectivity["tree_source"] == "GeneratingTreeOracle")
    ]
    oracle_table = table[
        (table["scope"] != "overall")
        & (table["q_mode"] == "oracle_q")
        & (table["decoder"] == "PosteriorMedianUnconstrained")
        & (table["tree_source"] == "GeneratingTreeOracle")
    ][["scope", "median_disconnected_fraction"]]
    alpha = oracle_connectivity.merge(oracle_table, on="scope")
    alpha_topologies = int(
        (
            (alpha["mean_effect"] > 0.01)
            & (alpha["median_disconnected_fraction"] >= 0.10)
        ).sum()
    )
    wider_alpha_warning = alpha_topologies >= 3
    continuation = bool(
        not stop_tree
        and survives_non_tied
        and reasonably_calibrated
        and topology_count >= 3
    )
    posterior_dominates = binary_decoder_gain > 0.005 and estimated_decoder_gain > 0.005
    if wider_alpha_warning:
        decision_code = "E"
    elif continuation:
        decision_code = "D"
    elif posterior_dominates:
        decision_code = "B"
    elif not reasonably_calibrated and generating_decoder_gain <= 0.005:
        decision_code = "C"
    else:
        decision_code = "A"
    decisions = {
        "A": "Stop latent-tree learning. Decision-aligned decoding does not rescue marginal-likelihood tree selection, and BinaryMWST is sufficient for the current k=1 research program.",
        "B": "Stop tree-identity learning as the primary direction. The meaningful positive signal is probabilistic subtree/posterior modeling rather than improved latent tree estimation.",
        "C": "The posterior model itself is insufficient or miscalibrated; stop latent-tree development and reassess the probabilistic model before any learned structure method.",
        "D": "Decision-aligned inference reveals a robust residual tree-selection advantage; a future learned/shared structural model may be scientifically justified.",
        "E": "The connected alpha-acyclic output restriction shows substantial task-loss misalignment; reassess the wider alpha-acyclic hypothesis before further work.",
        "F": "Prior literature substantially subsumes the proposed decision-theoretic contribution; retain the empirical result but do not pursue it as a novelty direction.",
    }
    return pd.DataFrame(
        [
            {
                "primary_tree_gain": primary["mean_tree_gain"],
                "primary_ci_lower": primary["ci_lower"],
                "primary_ci_upper": primary["ci_upper"],
                "topologies_over_0_005": topology_count,
                "tree_stop_rule_fired": stop_tree,
                "non_tied_tree_gain": non_tied_overall["mean_tree_gain"],
                "non_tied_ci_lower": non_tied_overall["ci_lower"],
                "survives_non_tied": survives_non_tied,
                "generating_decoder_gain": generating_decoder_gain,
                "binary_decoder_gain": binary_decoder_gain,
                "estimated_marginal_decoder_gain": estimated_decoder_gain,
                "max_abs_major_calibration_gap": max_abs_calibration_gap,
                "reasonably_calibrated": reasonably_calibrated,
                "alpha_warning_topologies": alpha_topologies,
                "wider_alpha_warning_fired": wider_alpha_warning,
                "continuation_condition_met": continuation,
                "final_decision_code": decision_code,
                "final_decision": decisions[decision_code],
            }
        ]
    )


def write_analysis(raw: pd.DataFrame, risk_rows: pd.DataFrame, output: Path) -> pd.DataFrame:
    output.mkdir(parents=True, exist_ok=True)
    table = primary_table(raw)
    decoder = decoder_gains(raw)
    gains = tree_gains(raw)
    connectivity = connectivity_costs(raw)
    exact = exact_row_tradeoff(raw)
    non_tied = non_tied_tree_gain(risk_rows)
    gate = gate_summary(table, gains, decoder, connectivity, non_tied)
    table.to_csv(output / "a1_5_primary_table.csv", index=False)
    decoder.to_csv(output / "a1_5_decoder_gains.csv", index=False)
    gains.to_csv(output / "a1_5_tree_gains.csv", index=False)
    connectivity.to_csv(output / "a1_5_connectivity_costs.csv", index=False)
    exact.to_csv(output / "a1_5_exact_row_tradeoff.csv", index=False)
    non_tied.to_csv(output / "a1_5_non_tied_tree_gain.csv", index=False)
    gate.to_csv(output / "a1_5_gate_summary.csv", index=False)
    return gate
