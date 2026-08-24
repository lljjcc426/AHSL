"""Publication-oriented diagnostic plots for the A0 pilot."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


MODEL_STYLES = {
    "Observed": ("#4C78A8", "o"),
    "Unconstrained": ("#F58518", "s"),
    "SparseUnconstrained": ("#54A24B", "^"),
    "NearestConnectedSubtree": ("#B279A2", "D"),
    "NoiseAwareMAPSubtree": ("#E45756", "P"),
    "FixedTreeAHSL": ("#222222", "X"),
}


def _selected_rows(raw: pd.DataFrame, plot_config: dict[str, object]) -> pd.DataFrame:
    selected = raw[
        np.isclose(raw["p_false_positive"], raw["p_false_negative"])
        & (raw["num_observations"] == int(plot_config["num_observations"]))
        & (raw["n"] == int(plot_config["n"]))
        & (raw["m"] == int(plot_config["m"]))
        & np.isclose(raw["branch_probability"], float(plot_config["branch_probability"]))
    ].copy()
    sparse_lambda = float(plot_config["sparse_lambda"])
    keep_sparse = selected["hyperparameters"].map(
        lambda value: json.loads(value).get("lambda_s") == sparse_lambda
        if isinstance(value, str) and value.startswith("{")
        else False
    )
    return selected[(selected["model"] != "SparseUnconstrained") | keep_sparse]


def _metric_vs_noise(
    raw: pd.DataFrame,
    metric: str,
    ylabel: str,
    output: Path,
    plot_config: dict[str, object],
) -> None:
    selected = _selected_rows(raw, plot_config)
    topologies = list(dict.fromkeys(selected["tree_topology"].tolist()))
    if not topologies:
        return
    columns = 2
    rows = int(np.ceil(len(topologies) / columns))
    figure, axes = plt.subplots(rows, columns, figsize=(11, 4.2 * rows), squeeze=False)
    for axis, topology in zip(axes.flat, topologies, strict=False):
        topology_rows = selected[selected["tree_topology"] == topology]
        for model, model_rows in topology_rows.groupby("model", sort=False):
            summary = model_rows.groupby("p_false_positive")[metric].agg(["mean", "std"]).reset_index()
            color, marker = MODEL_STYLES[model]
            axis.plot(
                summary["p_false_positive"],
                summary["mean"],
                label=model,
                color=color,
                marker=marker,
                linewidth=1.8,
            )
            standard_deviation = summary["std"].fillna(0.0)
            axis.fill_between(
                summary["p_false_positive"],
                summary["mean"] - standard_deviation,
                summary["mean"] + standard_deviation,
                color=color,
                alpha=0.12,
            )
        axis.set_title(topology.capitalize())
        axis.set_xlabel("Symmetric incidence corruption probability")
        axis.set_ylabel(ylabel)
        axis.grid(alpha=0.25)
    for axis in axes.flat[len(topologies) :]:
        axis.set_visible(False)
    handles, labels = axes.flat[0].get_legend_handles_labels()
    figure.legend(handles, labels, loc="lower center", ncol=3, frameon=False)
    figure.tight_layout(rect=(0.0, 0.08, 1.0, 1.0))
    figure.savefig(output, dpi=180)
    plt.close(figure)


def generate_plots(
    raw: pd.DataFrame, output_directory: Path, plot_config: dict[str, object]
) -> None:
    """Generate all primary and secondary A0 plots."""
    output_directory.mkdir(parents=True, exist_ok=True)
    _metric_vs_noise(
        raw,
        "clean_f1",
        "Clean incidence F1",
        output_directory / "a0_clean_f1_vs_noise.png",
        plot_config,
    )
    _metric_vs_noise(
        raw,
        "exact_row_recovery",
        "Exact subtree recovery",
        output_directory / "a0_exact_recovery_vs_noise.png",
        plot_config,
    )
    _metric_vs_noise(
        raw,
        "mean_symmetric_difference",
        "Mean symmetric difference per vertex",
        output_directory / "a0_symmetric_difference_vs_noise.png",
        plot_config,
    )
    _metric_vs_noise(
        raw,
        "running_intersection_violations",
        "Violating vertices",
        output_directory / "a0_riv_vs_noise.png",
        plot_config,
    )

    selected = _selected_rows(raw, plot_config)
    figure, axis = plt.subplots(figsize=(7.5, 5.2))
    for model, rows in selected.groupby("model", sort=False):
        color, marker = MODEL_STYLES[model]
        axis.scatter(
            rows["reconstruction_bce"],
            rows["clean_f1"],
            label=model,
            color=color,
            marker=marker,
            alpha=0.7,
        )
    axis.set_xlabel("Reconstruction BCE against noisy observations")
    axis.set_ylabel("Clean incidence F1")
    axis.grid(alpha=0.25)
    axis.legend(frameon=False, fontsize=8)
    figure.tight_layout()
    figure.savefig(output_directory / "a0_reconstruction_bce_vs_clean_f1.png", dpi=180)
    plt.close(figure)

    figure, axis = plt.subplots(figsize=(7.5, 5.2))
    fixed = raw[raw["model"] == "FixedTreeAHSL"]
    for topology, rows in fixed.groupby("tree_topology"):
        summary = rows.groupby("m")["runtime_seconds"].agg(["mean", "std"]).reset_index()
        axis.errorbar(
            summary["m"],
            summary["mean"],
            yerr=summary["std"].fillna(0.0),
            marker="o",
            capsize=3,
            label=topology,
        )
    axis.set_xlabel("Number of hyperedges m")
    axis.set_ylabel("FixedTreeAHSL runtime (seconds)")
    axis.grid(alpha=0.25)
    axis.legend(frameon=False)
    figure.tight_layout()
    figure.savefig(output_directory / "a0_runtime_vs_m.png", dpi=180)
    plt.close(figure)

    figure, axis = plt.subplots(figsize=(7.5, 5.2))
    for topology, rows in fixed.groupby("tree_topology"):
        axis.scatter(
            rows["num_connected_subtrees"],
            rows["clean_f1"],
            alpha=0.65,
            label=topology,
        )
    axis.set_xlabel("Number of connected-subtree candidates")
    axis.set_ylabel("FixedTreeAHSL clean incidence F1")
    axis.grid(alpha=0.25)
    axis.legend(frameon=False)
    figure.tight_layout()
    figure.savefig(output_directory / "a0_performance_vs_candidates.png", dpi=180)
    plt.close(figure)

