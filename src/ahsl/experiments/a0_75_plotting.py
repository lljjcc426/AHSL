"""Decision-aligned plots for the Phase A0.75 kill-test."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from ahsl.experiments.a0_75_analysis import paired_effects, primary_result_table


LABELS = {
    "TrueTreeOracle": "True tree",
    "DataAgnosticRandomTree": "Random tree",
    "BinaryMWST": "Binary MWST",
    "NoiseCorrectedMWST": "Corrected MWST",
    "BootstrapStabilityMWST": "Bootstrap MWST",
    "AlternatingTreeIncidenceEstimator": "Alternating",
    "ProfileLikelihoodTreeSearch": "Profile search",
}
COLORS = {
    "TrueTreeOracle": "#222222",
    "DataAgnosticRandomTree": "#9C755F",
    "BinaryMWST": "#4C78A8",
    "NoiseCorrectedMWST": "#54A24B",
    "BootstrapStabilityMWST": "#F58518",
    "AlternatingTreeIncidenceEstimator": "#B279A2",
    "ProfileLikelihoodTreeSearch": "#E45756",
}


def generate_a0_75_plots(raw: pd.DataFrame, output_directory: Path) -> None:
    output_directory.mkdir(parents=True, exist_ok=True)
    table = primary_result_table(raw)
    overall = table[table["scope"] == "overall"]

    figure, axis = plt.subplots(figsize=(11, 6.2))
    x = np.arange(len(overall))
    means = overall["mean_excess"].to_numpy()
    errors = np.vstack(
        [
            means - overall["excess_ci_lower"].to_numpy(),
            overall["excess_ci_upper"].to_numpy() - means,
        ]
    )
    axis.errorbar(
        x,
        means,
        yerr=errors,
        fmt="none",
        ecolor="#333333",
        capsize=4,
        linewidth=1.4,
    )
    axis.scatter(
        x,
        means,
        s=75,
        c=[COLORS[name] for name in overall["estimator"]],
        zorder=3,
    )
    axis.set_xticks(
        x,
        [LABELS[name] for name in overall["estimator"]],
        rotation=20,
        ha="right",
    )
    axis.set_ylabel("Downstream Hamming excess vs true tree")
    for threshold, style in [(0.0, "-"), (0.005, "--"), (0.010, ":")]:
        axis.axhline(threshold, color="#666666", linestyle=style, linewidth=1.2)
    axis.grid(axis="y", alpha=0.25)
    figure.tight_layout()
    figure.savefig(output_directory / "a0_75_downstream_excess.png", dpi=180)
    plt.close(figure)

    effects = paired_effects(raw)
    effects = effects[effects["estimator"] != "TrueTreeOracle"]
    figure, axis = plt.subplots(figsize=(9.5, 6.3))
    for estimator, group in effects.groupby("estimator"):
        axis.scatter(
            group["tree_edge_disagreement"],
            group["downstream_excess"],
            alpha=0.48,
            s=25,
            color=COLORS[estimator],
            label=LABELS[estimator],
        )
    pearson = effects["tree_edge_disagreement"].corr(
        effects["downstream_excess"], method="pearson"
    )
    spearman = effects["tree_edge_disagreement"].corr(
        effects["downstream_excess"], method="spearman"
    )
    axis.text(
        0.02,
        0.97,
        f"Pearson r={pearson:.3f}\nSpearman rho={spearman:.3f}",
        transform=axis.transAxes,
        va="top",
    )
    axis.axhline(0.0, color="#777777", linewidth=1)
    axis.set_xlabel("Labeled-tree edge disagreement")
    axis.set_ylabel("Downstream Hamming excess vs true tree")
    axis.grid(alpha=0.2)
    axis.legend(frameon=False, ncol=2)
    figure.tight_layout()
    figure.savefig(
        output_directory / "a0_75_edge_disagreement_vs_excess.png", dpi=180
    )
    plt.close(figure)

    selected_estimators = [
        "TrueTreeOracle",
        "DataAgnosticRandomTree",
        "BinaryMWST",
        "NoiseCorrectedMWST",
    ]
    topology_table = table[
        (table["scope"] != "overall")
        & table["estimator"].isin(selected_estimators)
    ]
    topologies = ["random", "path", "star", "balanced"]
    figure, axis = plt.subplots(figsize=(10, 6.2))
    x = np.arange(len(topologies))
    width = 0.19
    for index, estimator in enumerate(selected_estimators):
        rows = topology_table[topology_table["estimator"] == estimator].set_index(
            "scope"
        ).loc[topologies]
        axis.bar(
            x + (index - 1.5) * width,
            rows["mean_excess"],
            width,
            label=LABELS[estimator],
            color=COLORS[estimator],
        )
    axis.set_xticks(x, [topology.capitalize() for topology in topologies])
    axis.axhline(0.0, color="#555555", linewidth=1)
    axis.set_ylabel("Downstream Hamming excess vs true tree")
    axis.grid(axis="y", alpha=0.25)
    axis.legend(frameon=False, ncol=2)
    figure.tight_layout()
    figure.savefig(output_directory / "a0_75_tree_value_by_topology.png", dpi=180)
    plt.close(figure)

