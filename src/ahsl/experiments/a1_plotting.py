"""Decision-aligned figures for Phase A1."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from ahsl.experiments.a1_analysis import ESTIMATORS, primary_result_table


LABELS = {
    "GeneratingTreeOracle": "Generating tree",
    "DataAgnosticRandomTree": "Random tree",
    "BinaryMWST": "Binary MWST",
    "NoiseCorrectedMWST": "Corrected MWST",
    "BootstrapStabilityMWST": "Bootstrap MWST",
    "OracleQMarginalTree": "Marginal (oracle q)",
    "EstimatedQMarginalTree": "Marginal (estimated q)",
}
COLORS = ["#222222", "#8C6D5A", "#3B6EA8", "#3A8D5D", "#D17A22", "#B44B4B", "#7A5AA6"]


def generate_a1_plots(raw: pd.DataFrame, output_directory: Path) -> None:
    output_directory.mkdir(parents=True, exist_ok=True)
    table = primary_result_table(raw)
    overall = table[
        (table["scope"] == "overall") & (table["decoder"] == "MatchedPrior")
    ].set_index("estimator").loc[ESTIMATORS]

    figure, axis = plt.subplots(figsize=(11, 6.3))
    x = np.arange(len(overall))
    means = overall["mean_test_hamming_excess"].to_numpy()
    errors = np.vstack(
        [
            means - overall["excess_ci_lower"].to_numpy(),
            overall["excess_ci_upper"].to_numpy() - means,
        ]
    )
    axis.errorbar(x, means, yerr=errors, fmt="none", color="#333333", capsize=4)
    axis.scatter(x, means, c=COLORS, s=70, zorder=3)
    axis.set_xticks(x, [LABELS[name] for name in overall.index], rotation=20, ha="right")
    axis.set_ylabel("Test Hamming excess vs generating tree")
    for threshold, style in [(0.0, "-"), (0.005, "--"), (0.01, ":")]:
        axis.axhline(threshold, color="#666666", linestyle=style, linewidth=1.1)
    axis.grid(axis="y", alpha=0.25)
    figure.tight_layout()
    figure.savefig(output_directory / "a1_matched_decoder_excess.png", dpi=180)
    plt.close(figure)

    topology = table[
        (table["scope"] != "overall")
        & (table["decoder"] == "MatchedPrior")
        & table["estimator"].isin(
            ["GeneratingTreeOracle", "BinaryMWST", "BootstrapStabilityMWST", "EstimatedQMarginalTree"]
        )
    ]
    topology_order = ["random", "path", "balanced", "star"]
    selected = ["GeneratingTreeOracle", "BinaryMWST", "BootstrapStabilityMWST", "EstimatedQMarginalTree"]
    figure, axis = plt.subplots(figsize=(10, 6.2))
    width = 0.2
    x = np.arange(len(topology_order))
    for index, estimator in enumerate(selected):
        rows = topology[topology["estimator"] == estimator].set_index("scope").loc[topology_order]
        axis.bar(
            x + (index - 1.5) * width,
            rows["mean_test_hamming_excess"],
            width,
            label=LABELS[estimator],
            color=COLORS[ESTIMATORS.index(estimator)],
        )
    axis.set_xticks(x, [name.capitalize() for name in topology_order])
    axis.set_ylabel("Test Hamming excess vs generating tree")
    axis.axhline(0.0, color="#555555", linewidth=1)
    axis.grid(axis="y", alpha=0.25)
    axis.legend(frameon=False, ncol=2)
    figure.tight_layout()
    figure.savefig(output_directory / "a1_excess_by_topology.png", dpi=180)
    plt.close(figure)

    matched = table[
        (table["scope"] == "overall") & (table["decoder"] == "MatchedPrior")
    ].set_index("estimator").loc[ESTIMATORS]
    figure, axis = plt.subplots(figsize=(10.5, 6.0))
    x = np.arange(len(ESTIMATORS))
    width = 0.25
    for offset, split in enumerate(["train", "validation", "test"]):
        axis.bar(
            x + (offset - 1) * width,
            matched[f"mean_{split}_nll_per_row"],
            width,
            label=split.capitalize(),
        )
    axis.set_xticks(x, [LABELS[name] for name in ESTIMATORS], rotation=20, ha="right")
    axis.set_ylabel("Negative log likelihood per row")
    axis.grid(axis="y", alpha=0.25)
    axis.legend(frameon=False)
    figure.tight_layout()
    figure.savefig(output_directory / "a1_heldout_nll.png", dpi=180)
    plt.close(figure)
