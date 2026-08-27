"""Bounded UAI-2014 structural and exact strategy-variance audit."""

from __future__ import annotations

import argparse
import random
import re
from pathlib import Path

import numpy as np
import pandas as pd

from learning_augmented_inference.elimination import (
    heuristic_order,
    run_exact_elimination,
    simulate_elimination,
)
from learning_augmented_inference.structure import is_alpha_acyclic, primal_graph
from learning_augmented_inference.uai import read_uai


STRATEGIES = ("min_fill", "weighted_min_fill", "min_degree", "min_factor_entries")


def family_name(path: Path) -> str:
    match = re.match(r"[A-Za-z]+", path.stem)
    return match.group(0) if match else "other"


def audit_model(
    path: Path, random_orders: int, *, audit_strategies: bool
) -> tuple[dict, list[dict]]:
    model = read_uai(path)
    arities = np.asarray([len(scope) for scope in model.scopes], dtype=float)
    table_sizes = np.asarray([factor.table_size for factor in model.factors], dtype=float)
    nonzero_rates = np.asarray(
        [factor.nonzero_count / factor.table_size for factor in model.factors], dtype=float
    )
    graph = primal_graph(model.scopes, len(model.domain_sizes))
    unique_scopes = {tuple(sorted(scope)) for scope in model.scopes if scope}
    alpha_acyclic = (
        is_alpha_acyclic(tuple(unique_scopes))
        if len(unique_scopes) <= 200 and len(model.domain_sizes) <= 500
        else None
    )
    stats = {
        "instance": path.name,
        "family": family_name(path),
        "variables": len(model.domain_sizes),
        "factors": len(model.factors),
        "median_arity": float(np.median(arities)),
        "max_arity": int(arities.max()),
        "order3_fraction": float(np.mean(arities >= 3)),
        "median_domain": float(np.median(model.domain_sizes)),
        "max_domain": int(max(model.domain_sizes)),
        "median_table_entries": float(np.median(table_sizes)),
        "max_table_entries": int(table_sizes.max()),
        "median_nonzero_fraction": float(np.median(nonzero_rates)),
        "primal_edges": graph.number_of_edges(),
        "alpha_acyclic": alpha_acyclic,
    }
    rows: list[dict] = []
    if not audit_strategies:
        return stats, rows
    orders: dict[str, tuple[int, ...]] = {
        strategy: heuristic_order(model.scopes, model.domain_sizes, strategy)
        for strategy in STRATEGIES
    }
    rng = random.Random(20260827)
    for index in range(random_orders):
        order = list(range(len(model.domain_sizes)))
        rng.shuffle(order)
        orders[f"random_{index:02d}"] = tuple(order)
    for strategy, order in orders.items():
        cost = simulate_elimination(model.scopes, model.domain_sizes, order)
        rows.append(
            {
                "instance": path.name,
                "family": family_name(path),
                "strategy": strategy,
                "induced_width": cost.induced_width,
                "max_union_arity": cost.max_union_arity,
                "peak_entries": cost.peak_entries,
                "total_join_entries": cost.total_join_entries,
            }
        )
    return stats, rows


def exact_subset(
    input_dir: Path,
    costs: pd.DataFrame,
    peak_cap: int,
    total_cap: int,
    repeats: int,
    per_family: int,
) -> pd.DataFrame:
    columns = [
        "instance",
        "family",
        "strategy",
        "median_seconds",
        "peak_entries",
        "total_join_entries",
        "exact_value",
    ]
    if costs.empty:
        return pd.DataFrame(columns=columns)
    rows = []
    classical = costs[costs["strategy"].isin(STRATEGIES)].copy()
    feasible_instances = []
    for instance, group in classical.groupby("instance"):
        if (
            int(group["peak_entries"].max()) <= peak_cap
            and int(group["total_join_entries"].max()) <= total_cap
        ):
            feasible_instances.append(instance)
    selected = []
    feasible = classical[classical["instance"].isin(feasible_instances)][
        ["family", "instance"]
    ].drop_duplicates()
    for _, group in feasible.groupby("family"):
        selected.extend(group.head(per_family)["instance"].tolist())
    for instance in selected:
        path = input_dir / instance
        model = read_uai(path, load_values=True)
        reference = None
        for strategy in STRATEGIES:
            order = heuristic_order(model.scopes, model.domain_sizes, strategy)
            runs = [run_exact_elimination(model, order) for _ in range(repeats)]
            value = runs[0].value
            if reference is None:
                reference = value
            elif not np.isclose(value, reference, rtol=1e-9, atol=1e-12):
                raise AssertionError(f"strategy changed exact answer for {instance}")
            rows.append(
                {
                    "instance": instance,
                    "family": family_name(path),
                    "strategy": strategy,
                    "median_seconds": float(np.median([run.seconds for run in runs])),
                    "peak_entries": runs[0].peak_entries,
                    "total_join_entries": runs[0].total_join_entries,
                    "exact_value": value,
                }
            )
    return pd.DataFrame(rows, columns=columns)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("results/r0/raw"))
    parser.add_argument("--output-prefix", default="uai2014")
    parser.add_argument("--random-orders", type=int, default=8)
    parser.add_argument("--peak-cap", type=int, default=65_536)
    parser.add_argument("--exact-total-cap", type=int, default=2_000_000)
    parser.add_argument("--exact-repeats", type=int, default=1)
    parser.add_argument("--exact-per-family", type=int, default=1)
    parser.add_argument("--max-strategy-variables", type=int, default=150)
    parser.add_argument("--max-per-family", type=int, default=4)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    stats_rows: list[dict] = []
    cost_rows: list[dict] = []
    family_counts: dict[str, int] = {}
    for path in sorted(args.input_dir.glob("*.uai"), key=lambda item: item.stat().st_size):
        family = family_name(path)
        model_header = read_uai(path)
        use_strategies = (
            len(model_header.domain_sizes) <= args.max_strategy_variables
            and family_counts.get(family, 0) < args.max_per_family
        )
        if use_strategies:
            print(f"strategy audit: {path.name}", flush=True)
        stats, costs = audit_model(
            path, args.random_orders, audit_strategies=use_strategies
        )
        if use_strategies:
            family_counts[family] = family_counts.get(family, 0) + 1
        stats_rows.append(stats)
        cost_rows.extend(costs)
    stats_frame = pd.DataFrame(stats_rows)
    cost_frame = pd.DataFrame(
        cost_rows,
        columns=[
            "instance",
            "family",
            "strategy",
            "induced_width",
            "max_union_arity",
            "peak_entries",
            "total_join_entries",
        ],
    )
    exact_frame = exact_subset(
        args.input_dir,
        cost_frame,
        args.peak_cap,
        args.exact_total_cap,
        args.exact_repeats,
        args.exact_per_family,
    )

    stats_frame.to_csv(
        args.output_dir / f"{args.output_prefix}_instance_stats.csv", index=False
    )
    cost_frame.to_csv(
        args.output_dir / f"{args.output_prefix}_strategy_costs.csv", index=False
    )
    exact_frame.to_csv(
        args.output_dir / f"{args.output_prefix}_exact_runtime.csv", index=False
    )

    classical = cost_frame[cost_frame["strategy"].isin(STRATEGIES)]
    if classical.empty:
        family_summary = pd.DataFrame()
    else:
        instance_gap = classical.groupby(["family", "instance"]).agg(
            best_peak=("peak_entries", "min"),
            worst_peak=("peak_entries", "max"),
            best_total=("total_join_entries", "min"),
            worst_total=("total_join_entries", "max"),
        )
        instance_gap["peak_ratio"] = instance_gap["worst_peak"] / instance_gap["best_peak"]
        instance_gap["total_ratio"] = instance_gap["worst_total"] / instance_gap["best_total"]
        family_summary = instance_gap.groupby("family").agg(
            instances=("peak_ratio", "size"),
            median_peak_ratio=("peak_ratio", "median"),
            median_total_ratio=("total_ratio", "median"),
            max_peak_ratio=("peak_ratio", "max"),
        )
        if not exact_frame.empty:
            runtime_gap = exact_frame.groupby(["family", "instance"])["median_seconds"].agg(
                lambda values: values.max() / values.min()
            )
            family_summary = family_summary.join(
                runtime_gap.groupby("family").median().rename("median_runtime_ratio")
            )
    family_summary.to_csv(args.output_dir / f"{args.output_prefix}_family_summary.csv")
    print(f"audited {len(stats_frame)} UAI models")
    print(f"exact runtime subset: {exact_frame['instance'].nunique()} models")


if __name__ == "__main__":
    main()
