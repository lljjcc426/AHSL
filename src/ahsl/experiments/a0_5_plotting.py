"""Scientific plots for the Phase A0.5 decision."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


TOPOLOGIES = ["random", "path", "star", "balanced"]
COLORS = ["#4C78A8", "#E45756", "#54A24B", "#222222"]


def _paired(
    raw: pd.DataFrame,
    experiment_type: str,
    left_model: str,
    right_model: str,
) -> pd.DataFrame:
    selected = raw[raw["experiment_type"] == experiment_type]
    keys = [
        "experiment_id",
        "seed",
        "tree_topology",
        "noise_setting",
        "p_false_positive",
        "p_false_negative",
        "num_observations",
        "tree_source",
        "requested_tree_swaps",
        "tree_edge_disagreement",
        "requested_offclass_fraction",
        "offclass_fraction",
    ]
    left = selected[selected["model"] == left_model][keys + ["clean_hamming_error"]]
    right = selected[selected["model"] == right_model][keys + ["clean_hamming_error"]]
    merged = left.merge(right, on=keys, suffixes=("_left", "_right"))
    merged["hamming_error_reduction"] = (
        merged["clean_hamming_error_right"]
        - merged["clean_hamming_error_left"]
    )
    return merged


def _topology_axes(ylabel: str) -> tuple[plt.Figure, np.ndarray]:
    figure, axes = plt.subplots(2, 2, figsize=(11, 8.2), sharey=True)
    for axis, topology in zip(axes.flat, TOPOLOGIES, strict=True):
        axis.set_title(topology.capitalize())
        axis.set_ylabel(ylabel)
        axis.grid(alpha=0.25)
    return figure, axes


def _save(figure: plt.Figure, path: Path, legend_columns: int = 3) -> None:
    handles, labels = figure.axes[0].get_legend_handles_labels()
    if handles:
        figure.legend(
            handles,
            labels,
            loc="lower center",
            ncol=legend_columns,
            frameon=False,
        )
        figure.tight_layout(rect=(0.0, 0.08, 1.0, 1.0))
    else:
        figure.tight_layout()
    figure.savefig(path, dpi=180)
    plt.close(figure)


def generate_a0_5_plots(raw: pd.DataFrame, output_directory: Path) -> None:
    output_directory.mkdir(parents=True, exist_ok=True)
    core = _paired(
        raw,
        "core",
        "DPNoiseAwareConnectedMLE",
        "NoiseAwareIndependentNonemptyMLE",
    )
    symmetric = core[
        np.isclose(core["p_false_positive"], core["p_false_negative"])
    ]

    figure, axes = _topology_axes("Hamming error reduction from connectivity")
    for axis, topology in zip(axes.flat, TOPOLOGIES, strict=True):
        topology_rows = symmetric[symmetric["tree_topology"] == topology]
        for index, (repetitions, rows) in enumerate(
            topology_rows.groupby("num_observations")
        ):
            summary = rows.groupby("p_false_positive")["hamming_error_reduction"].agg(
                ["mean", "std"]
            )
            axis.errorbar(
                summary.index,
                summary["mean"],
                yerr=summary["std"],
                marker="o",
                capsize=3,
                color=COLORS[index],
                label=f"R={repetitions}",
            )
        axis.axhline(0.0, color="#777777", linewidth=1)
        axis.set_xlabel("Symmetric noise probability")
    _save(figure, output_directory / "a0_5_structural_gain_vs_noise.png")

    figure, axes = _topology_axes("Hamming error reduction from connectivity")
    for axis, topology in zip(axes.flat, TOPOLOGIES, strict=True):
        topology_rows = symmetric[symmetric["tree_topology"] == topology]
        for index, (noise, rows) in enumerate(topology_rows.groupby("noise_setting")):
            summary = rows.groupby("num_observations")["hamming_error_reduction"].agg(
                ["mean", "std"]
            )
            axis.errorbar(
                summary.index,
                summary["mean"],
                yerr=summary["std"],
                marker="o",
                capsize=3,
                color=COLORS[index],
                label=noise,
            )
        axis.axhline(0.0, color="#777777", linewidth=1)
        axis.set_xlabel("Number of observations R")
    _save(figure, output_directory / "a0_5_structural_gain_vs_R.png")

    scaling = raw[
        (raw["experiment_type"] == "scaling")
        & raw["model"].isin(
            ["DPNearestConnectedSubtree", "DPNoiseAwareConnectedMLE"]
        )
    ]
    for metric, filename, ylabel in (
        ("runtime_seconds", "a0_5_runtime_vs_m.png", "Runtime (seconds)"),
        ("runtime_per_nm", "a0_5_runtime_per_nm_vs_m.png", "Runtime / (n m)"),
    ):
        figure, axes = _topology_axes(ylabel)
        for axis, topology in zip(axes.flat, TOPOLOGIES, strict=True):
            topology_rows = scaling[scaling["tree_topology"] == topology]
            for index, (model, rows) in enumerate(topology_rows.groupby("model")):
                summary = rows.groupby("m")[metric].agg(["mean", "std"])
                axis.errorbar(
                    summary.index,
                    summary["mean"],
                    yerr=summary["std"],
                    marker="o",
                    capsize=3,
                    color=COLORS[index],
                    label=model,
                )
            axis.set_xscale("log", base=2)
            axis.set_yscale("log")
            axis.set_xlabel("Number of tree nodes m")
        _save(figure, output_directory / filename, legend_columns=2)

    wrong = _paired(
        raw,
        "wrong_tree",
        "DPNoiseAwareConnectedMLE",
        "NoiseAwareIndependentNonemptyMLE",
    )
    figure, axes = _topology_axes("Hamming error reduction from connectivity")
    for axis, topology in zip(axes.flat, TOPOLOGIES, strict=True):
        rows = wrong[wrong["tree_topology"] == topology]
        summary = rows.groupby("tree_source").agg(
            disagreement=("tree_edge_disagreement", "mean"),
            gain=("hamming_error_reduction", "mean"),
            standard_deviation=("hamming_error_reduction", "std"),
        ).sort_values("disagreement")
        axis.errorbar(
            summary["disagreement"],
            summary["gain"],
            yerr=summary["standard_deviation"],
            marker="o",
            capsize=3,
            color=COLORS[0],
        )
        axis.axhline(0.0, color="#777777", linewidth=1)
        axis.set_xlabel("Actual labeled-edge disagreement")
    _save(figure, output_directory / "a0_5_wrong_tree_crossover.png")

    offclass = _paired(
        raw,
        "offclass",
        "DPNoiseAwareConnectedMLE",
        "NoiseAwareIndependentNonemptyMLE",
    )
    figure, axes = _topology_axes("Hamming error reduction from connectivity")
    for axis, topology in zip(axes.flat, TOPOLOGIES, strict=True):
        rows = offclass[offclass["tree_topology"] == topology]
        summary = rows.groupby("requested_offclass_fraction").agg(
            actual=("offclass_fraction", "mean"),
            gain=("hamming_error_reduction", "mean"),
            standard_deviation=("hamming_error_reduction", "std"),
        )
        axis.errorbar(
            summary["actual"],
            summary["gain"],
            yerr=summary["standard_deviation"],
            marker="o",
            capsize=3,
            color=COLORS[1],
        )
        axis.axhline(0.0, color="#777777", linewidth=1)
        axis.set_xlabel("Actual off-class row fraction")
    _save(figure, output_directory / "a0_5_offclass_crossover.png")

    a1 = raw[
        (raw["experiment_type"] == "a1_gate")
        & (raw["tree_source"] != "true_tree")
    ].copy()
    validity = (
        a1.assign(valid=lambda frame: frame["estimated_tree_clean_riv"] == 0)
        .groupby(["tree_source", "num_observations"])["valid"]
        .mean()
        .unstack()
    )
    figure, axis = plt.subplots(figsize=(8, 5.2))
    x = np.arange(len(validity.index))
    width = 0.35
    for index, repetitions in enumerate(validity.columns):
        axis.bar(
            x + (index - 0.5) * width,
            validity[repetitions],
            width,
            label=f"R={repetitions}",
            color=COLORS[index],
        )
    axis.set_xticks(x, validity.index, rotation=15)
    axis.set_ylabel("Fraction valid join trees for clean incidence")
    axis.set_ylim(0.0, 1.05)
    axis.grid(axis="y", alpha=0.25)
    axis.legend(frameon=False)
    figure.tight_layout()
    figure.savefig(output_directory / "a0_5_mwst_join_tree_validity.png", dpi=180)
    plt.close(figure)

    oracle = _paired(
        raw,
        "core",
        "GeneratorPriorConnectedMAP",
        "DPNoiseAwareConnectedMLE",
    )
    figure, axes = _topology_axes("Oracle Hamming error reduction over connected MLE")
    for axis, topology in zip(axes.flat, TOPOLOGIES, strict=True):
        rows = oracle[oracle["tree_topology"] == topology]
        for index, (repetitions, group) in enumerate(rows.groupby("num_observations")):
            summary = group.groupby("p_false_positive")["hamming_error_reduction"].agg(
                ["mean", "std"]
            )
            axis.errorbar(
                summary.index,
                summary["mean"],
                yerr=summary["std"],
                marker="o",
                capsize=3,
                color=COLORS[index],
                label=f"R={repetitions}",
            )
        axis.axhline(0.0, color="#777777", linewidth=1)
        axis.set_xlabel("Symmetric noise probability")
    _save(figure, output_directory / "a0_5_generator_prior_oracle_gap.png")

