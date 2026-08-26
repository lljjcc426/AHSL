"""The three preregistered, decision-focused Phase A1.5 figures."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from ahsl.experiments.a1_5_analysis import TREE_SOURCES


LABELS = {
    "GeneratingTreeOracle": "Generating tree",
    "DataAgnosticRandomTree": "Random tree",
    "BinaryMWST": "Binary MWST",
    "NoiseCorrectedMWST": "Corrected MWST",
    "BootstrapStabilityMWST": "Bootstrap MWST",
    "OracleQMarginalTree": "Marginal (oracle-q tree)",
    "EstimatedQMarginalTree": "Marginal (estimated q)",
}


def generate_plots(raw: pd.DataFrame, risk_rows: pd.DataFrame, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    deployable = raw[raw["q_mode"] == "estimated_q"]

    # Figure 1: decision effect on every frozen tree source.
    selected = deployable[
        deployable["decoder"].isin(["PosteriorMAPConnected", "ConnectedBayesHamming"])
    ]
    summary = selected.groupby(["tree_source", "decoder"])["test_hamming_error"].agg(["mean", "sem"])
    figure, axis = plt.subplots(figsize=(11.5, 6.2))
    x = np.arange(len(TREE_SOURCES))
    width = 0.36
    for offset, (decoder, label, color) in enumerate(
        [
            ("PosteriorMAPConnected", "Posterior MAP", "#6B7280"),
            ("ConnectedBayesHamming", "Connected Bayes-Hamming", "#2563A6"),
        ]
    ):
        rows = summary.xs(decoder, level="decoder").loc[TREE_SOURCES]
        axis.bar(
            x + (offset - 0.5) * width,
            rows["mean"],
            width,
            yerr=1.96 * rows["sem"],
            capsize=3,
            color=color,
            label=label,
        )
    axis.set_xticks(x, [LABELS[name] for name in TREE_SOURCES], rotation=20, ha="right")
    axis.set_ylabel("Clean test Hamming error")
    axis.grid(axis="y", alpha=0.25)
    axis.legend(frameon=False)
    figure.tight_layout()
    figure.savefig(output / "a1_5_map_vs_connected_mbr.png", dpi=180)
    plt.close(figure)

    # Figure 2: the primary tree comparison under the same aligned action.
    tree_subset = [
        "GeneratingTreeOracle",
        "DataAgnosticRandomTree",
        "BinaryMWST",
        "EstimatedQMarginalTree",
    ]
    rows = deployable[
        (deployable["decoder"] == "ConnectedBayesHamming")
        & deployable["tree_source"].isin(tree_subset)
    ]
    topology_order = ["random", "path", "balanced", "star"]
    grouped = rows.groupby(["tree_source", "tree_topology"])["test_hamming_error"].mean()
    figure, axis = plt.subplots(figsize=(10.5, 6.1))
    x = np.arange(len(topology_order))
    width = 0.2
    colors = ["#222222", "#A56A43", "#3573B9", "#7B57A6"]
    for index, tree_source in enumerate(tree_subset):
        values = grouped.loc[tree_source].reindex(topology_order)
        axis.bar(
            x + (index - 1.5) * width,
            values,
            width,
            color=colors[index],
            label=LABELS[tree_source],
        )
    axis.set_xticks(x, [name.capitalize() for name in topology_order])
    axis.set_ylabel("Clean test Hamming error")
    axis.grid(axis="y", alpha=0.25)
    axis.legend(frameon=False, ncol=2)
    figure.tight_layout()
    figure.savefig(output / "a1_5_tree_sources_under_connected_mbr.png", dpi=180)
    plt.close(figure)

    # Figure 3: row-level posterior-risk calibration, summarized in deciles.
    calibration_sources = [
        "GeneratingTreeOracle",
        "BinaryMWST",
        "EstimatedQMarginalTree",
    ]
    rows = risk_rows[
        (risk_rows["q_mode"] == "estimated_q")
        & (risk_rows["decoder"] == "ConnectedBayesHamming")
        & risk_rows["tree_source"].isin(calibration_sources)
    ].copy()
    rows["risk_bin"] = rows.groupby("tree_source")["posterior_risk"].transform(
        lambda values: pd.qcut(values, 10, labels=False, duplicates="drop")
    )
    calibration = (
        rows.groupby(["tree_source", "risk_bin"], as_index=False)
        .agg(predicted=("posterior_risk", "mean"), realized=("actual_hamming", "mean"))
    )
    figure, axis = plt.subplots(figsize=(7.1, 6.3))
    colors = ["#222222", "#3573B9", "#7B57A6"]
    for tree_source, color in zip(calibration_sources, colors):
        curve = calibration[calibration["tree_source"] == tree_source]
        axis.plot(
            curve["predicted"],
            curve["realized"],
            marker="o",
            color=color,
            label=LABELS[tree_source],
        )
    limits = [0.04, 0.30]
    axis.plot(limits, limits, linestyle="--", color="#777777", linewidth=1)
    axis.set_xlim(limits)
    axis.set_ylim(limits)
    axis.set_xlabel("Posterior expected Hamming risk")
    axis.set_ylabel("Realized clean Hamming")
    axis.grid(alpha=0.25)
    axis.legend(frameon=False)
    figure.tight_layout()
    figure.savefig(output / "a1_5_posterior_risk_calibration.png", dpi=180)
    plt.close(figure)
