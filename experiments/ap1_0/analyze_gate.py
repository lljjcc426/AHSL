"""Aggregate AP1.0 raw rows and render only decision-relevant figures."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def main() -> None:
    repo = Path(__file__).resolve().parents[2]
    result_root = repo / "results" / "ap1_0"
    raw = pd.read_csv(result_root / "raw" / "raw_runs.csv")
    measured = raw[raw["measured"].eq(True)].copy()
    numeric = [
        "update_ms", "rss_steady_mb", "rss_update_peak_mb", "rss_post_mb",
        "observed_output_changes", "observed_output_retractions",
        "insert_count", "delete_count",
    ]
    for column in numeric:
        measured[column] = pd.to_numeric(measured[column], errors="coerce")

    keys = ["workload", "workload_class", "scale", "update_regime", "workers", "system"]
    summary = measured.groupby(keys, dropna=False).agg(
        n=("update_ms", "size"),
        latency_median_ms=("update_ms", "median"),
        latency_mean_ms=("update_ms", "mean"),
        latency_p95_ms=("update_ms", lambda x: x.quantile(0.95)),
        latency_p99_ms=("update_ms", lambda x: x.quantile(0.99)),
        latency_min_ms=("update_ms", "min"),
        latency_max_ms=("update_ms", "max"),
        rss_steady_median_mb=("rss_steady_mb", "median"),
        rss_peak_median_mb=("rss_update_peak_mb", "median"),
        rss_post_median_mb=("rss_post_mb", "median"),
        observed_output_changes_median=("observed_output_changes", "median"),
        observed_output_retractions_median=("observed_output_retractions", "median"),
        all_correct=("correct", "all"),
    ).reset_index()

    pivot = summary.pivot_table(
        index=keys[:-1], columns="system",
        values=[
            "latency_median_ms", "latency_p99_ms", "rss_peak_median_mb",
            "rss_post_median_mb", "rss_steady_median_mb",
        ],
    )
    comparison = pd.DataFrame(index=pivot.index)
    comparison["recompute_over_incremental_latency"] = (
        pivot["latency_median_ms"]["FlowLog_recompute"]
        / pivot["latency_median_ms"]["FlowLog_incremental"]
    )
    comparison["incremental_over_recompute_post_rss"] = (
        pivot["rss_post_median_mb"]["FlowLog_incremental"]
        / pivot["rss_post_median_mb"]["FlowLog_recompute"]
    )
    comparison["incremental_over_recompute_peak_rss"] = (
        pivot["rss_peak_median_mb"]["FlowLog_incremental"]
        / pivot["rss_peak_median_mb"]["FlowLog_recompute"]
    )
    comparison["incremental_tail_inflation"] = (
        pivot["latency_p99_ms"]["FlowLog_incremental"]
        / pivot["latency_median_ms"]["FlowLog_incremental"]
    )
    comparison = comparison.reset_index()

    inc = measured[measured.system.eq("FlowLog_incremental")].copy()
    inc["retained_growth_mb"] = inc["rss_post_mb"] - inc["rss_steady_mb"]
    inc["transient_update_mb"] = inc["rss_update_peak_mb"] - inc["rss_steady_mb"]
    inc["observed_derived_change_amplification"] = (
        inc["observed_output_changes"]
        / (inc["insert_count"] + inc["delete_count"]).replace(0, np.nan)
    )
    diagnostics = inc.groupby(keys[:-1], dropna=False).agg(
        retained_growth_median_mb=("retained_growth_mb", "median"),
        retained_growth_max_mb=("retained_growth_mb", "max"),
        transient_update_median_mb=("transient_update_mb", "median"),
        derived_change_amplification_median=("observed_derived_change_amplification", "median"),
        derived_change_amplification_max=("observed_derived_change_amplification", "max"),
    ).reset_index()

    aggregated = result_root / "aggregated"
    figures = result_root / "figures"
    aggregated.mkdir(parents=True, exist_ok=True)
    figures.mkdir(parents=True, exist_ok=True)
    summary.to_csv(aggregated / "cell_summary.csv", index=False)
    comparison.to_csv(aggregated / "same_engine_comparison.csv", index=False)
    diagnostics.to_csv(aggregated / "mechanism_diagnostics.csv", index=False)

    labels = comparison.apply(
        lambda r: f"{r.workload}\n{r.scale}/{r.update_regime}/w{r.workers}", axis=1
    )
    x = np.arange(len(comparison))

    fig, ax = plt.subplots(figsize=(13, 5))
    ax.scatter(x, comparison["recompute_over_incremental_latency"], color="#2463a8")
    ax.axhline(1, color="black", linewidth=0.8)
    ax.set_xticks(x, labels, rotation=55, ha="right")
    ax.set_ylabel("recompute / incremental median latency")
    ax.set_title("Same-engine incremental versus scratch")
    fig.tight_layout()
    fig.savefig(figures / "incremental_vs_scratch.png", dpi=180)
    plt.close(fig)

    inc_summary = summary[summary.system.eq("FlowLog_incremental")].reset_index(drop=True)
    labels_inc = inc_summary.apply(lambda r: f"{r.workload}\n{r.update_regime}", axis=1)
    x = np.arange(len(inc_summary))
    fig, ax = plt.subplots(figsize=(13, 5))
    width = 0.36
    ax.bar(x - width / 2, inc_summary.latency_median_ms, width, label="p50")
    ax.bar(x + width / 2, inc_summary.latency_p99_ms, width, label="p99")
    ax.set_xticks(x, labels_inc, rotation=55, ha="right")
    ax.set_ylabel("update latency (ms)")
    ax.set_title("FlowLog incremental update latency and tail")
    ax.legend()
    fig.tight_layout()
    fig.savefig(figures / "p99_by_workload.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(13, 5))
    ax.bar(x - width, inc_summary.rss_steady_median_mb, width, label="steady")
    ax.bar(x, inc_summary.rss_peak_median_mb, width, label="update peak")
    ax.bar(x + width, inc_summary.rss_post_median_mb, width, label="post")
    ax.set_xticks(x, labels_inc, rotation=55, ha="right")
    ax.set_ylabel("working set (MiB)")
    ax.set_title("FlowLog incremental working-set phases")
    ax.legend()
    fig.tight_layout()
    fig.savefig(figures / "memory_phases.png", dpi=180)
    plt.close(fig)

    regime = inc_summary.groupby(["workload", "update_regime"], as_index=False).agg(
        p50=("latency_median_ms", "median"), p99=("latency_p99_ms", "median")
    )
    fig, ax = plt.subplots(figsize=(11, 5))
    for workload, group in regime.groupby("workload"):
        ax.plot(group.update_regime, group.p99, marker="o", label=workload)
    ax.set_ylabel("p99 update latency (ms)")
    ax.set_title("Update latency by regime")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(figures / "latency_vs_regime.png", dpi=180)
    plt.close(fig)

    diag_labels = diagnostics.apply(
        lambda r: f"{r.workload}\n{r.scale}/{r.update_regime}/w{r.workers}", axis=1
    )
    x_diag = np.arange(len(diagnostics))
    fig, ax = plt.subplots(figsize=(13, 5))
    ax.bar(x_diag, diagnostics.derived_change_amplification_median.fillna(0))
    ax.axhline(2, color="#b33a3a", linestyle="--", label="2x gate")
    ax.set_xticks(x_diag, diag_labels, rotation=55, ha="right")
    ax.set_ylabel("observed output changes / input changes")
    ax.set_title("Observed delete/update amplification (not an internal work counter)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(figures / "observed_delete_amplification.png", dpi=180)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(13, 5))
    ax.bar(x_diag, diagnostics.retained_growth_median_mb)
    ax.set_xticks(x_diag, diag_labels, rotation=55, ha="right")
    ax.set_ylabel("M_post - M_steady (MiB)")
    ax.set_title("Retained working-set growth after quiescence")
    fig.tight_layout()
    fig.savefig(figures / "retained_growth.png", dpi=180)
    plt.close(fig)

    worker = inc_summary[
        inc_summary.workload.isin(["reachability", "connected_components"])
        & inc_summary.scale.eq("small")
        & inc_summary.update_regime.eq("realistic_mixed")
    ]
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    for workload, group in worker.groupby("workload"):
        axes[0].plot(group.workers, group.latency_median_ms, marker="o", label=workload)
        axes[1].plot(group.workers, group.rss_post_median_mb, marker="o", label=workload)
    axes[0].set(xlabel="workers", ylabel="median update latency (ms)")
    axes[1].set(xlabel="workers", ylabel="post working set (MiB)")
    axes[0].legend(fontsize=8)
    axes[1].legend(fontsize=8)
    fig.suptitle("Worker-count causal diagnostic")
    fig.tight_layout()
    fig.savefig(figures / "worker_diagnostic.png", dpi=180)
    plt.close(fig)

    gate = {
        "all_correct": bool(measured.correct.all()),
        "raw_rows": int(len(raw)),
        "measured_rows": int(len(measured)),
        "max_incremental_retained_growth_mb": float(diagnostics.retained_growth_max_mb.max()),
        "max_incremental_peak_over_recompute": float(
            comparison.incremental_over_recompute_peak_rss.max()
        ),
        "max_incremental_tail_inflation": float(comparison.incremental_tail_inflation.max()),
        "min_same_engine_speedup": float(comparison.recompute_over_incremental_latency.min()),
        "max_same_engine_speedup": float(comparison.recompute_over_incremental_latency.max()),
        "primary_residual_class": "R7_NO_ACTIONABLE_RESIDUAL",
        "decision": "AP1.0-C",
    }
    (aggregated / "gate_summary.json").write_text(json.dumps(gate, indent=2), encoding="utf-8")
    print(json.dumps(gate, indent=2))


if __name__ == "__main__":
    main()
