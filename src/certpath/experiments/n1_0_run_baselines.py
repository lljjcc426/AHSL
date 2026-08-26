from __future__ import annotations

import argparse
import csv
import pickle
from pathlib import Path
import sys

from certpath.attainability import check_positive_cost_attainability
from certpath.graph_projection import projected_shortest_reactions, projection_semantically_valid
from certpath.reactome_adapter import parse_reactome_biopax
from certpath.task_builder import build_natural_tasks


def f1(predicted: frozenset[str], gold: frozenset[str]) -> tuple[float, float, float]:
    shared = len(predicted & gold)
    precision = shared / len(predicted) if predicted else 0.0
    recall = shared / len(gold) if gold else 0.0
    score = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return precision, recall, score


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--biopax", type=Path, required=True)
    parser.add_argument("--release", type=int, required=True)
    parser.add_argument("--output", type=Path, default=Path("results/n1_0/raw/task_audit_v97.csv"))
    parser.add_argument("--time-limit", type=float, default=30.0)
    parser.add_argument("--with-projection", action="store_true")
    parser.add_argument("--snapshot-cache", type=Path)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    if args.snapshot_cache and args.snapshot_cache.exists():
        with args.snapshot_cache.open("rb") as handle:
            snapshot = pickle.load(handle)
    else:
        snapshot = parse_reactome_biopax(args.biopax, args.release)
        if args.snapshot_cache:
            args.snapshot_cache.parent.mkdir(parents=True, exist_ok=True)
            with args.snapshot_cache.open("wb") as handle:
                pickle.dump(snapshot, handle, protocol=pickle.HIGHEST_PROTOCOL)
    graph = snapshot.hypergraph
    tasks = build_natural_tasks(snapshot)
    fields = [
        "pathway_id", "pathway_name", "family", "gold_size", "source_count",
        "boundary_source_count", "target_count", "gold_feasible", "requires_internal_repair",
        "attainability_status", "minimum_gold_subset_size", "attainable", "cycle",
        "gold_multitail_reactions", "gold_multitail_fraction", "solve_runtime_seconds", "cuts_added",
        "nontrivial", "qualified", "projection_size", "projection_valid", "projection_f1",
        "projection_precision", "projection_recall", "projection_differs",
    ]
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for index, task in enumerate(tasks, 1):
            result = check_positive_cost_attainability(
                graph, task.sources, task.targets, task.gold_reactions, args.time_limit,
                compute_minimum=False,
            )
            multitail = sum(len(graph.edges[e].tail) > 1 for e in task.gold_reactions)
            nontrivial = len(task.gold_reactions) >= 3
            qualified = result.attainable and nontrivial
            projection = (
                projected_shortest_reactions(graph, task.sources, task.targets)
                if args.with_projection else frozenset()
            )
            projection_valid = (
                projection_semantically_valid(graph, task.sources, task.targets, projection)
                if args.with_projection else ""
            )
            precision, recall, score = f1(projection, task.gold_reactions) if args.with_projection else ("", "", "")
            writer.writerow({
                "pathway_id": task.pathway_id,
                "pathway_name": task.pathway_name,
                "family": task.family,
                "gold_size": len(task.gold_reactions),
                "source_count": len(task.sources),
                "boundary_source_count": len(task.boundary_sources),
                "target_count": len(task.targets),
                "gold_feasible": result.feasible,
                "requires_internal_repair": not result.feasible,
                "attainability_status": result.solve.status,
                "minimum_gold_subset_size": result.minimum_size if result.minimum_size is not None else "",
                "attainable": result.attainable,
                "cycle": graph.contains_cycle(task.gold_reactions),
                "gold_multitail_reactions": multitail,
                "gold_multitail_fraction": multitail / len(task.gold_reactions),
                "solve_runtime_seconds": result.solve.runtime_seconds,
                "cuts_added": result.solve.cuts_added,
                "nontrivial": nontrivial,
                "qualified": qualified,
                "projection_size": len(projection) if args.with_projection else "",
                "projection_valid": projection_valid,
                "projection_f1": score,
                "projection_precision": precision,
                "projection_recall": recall,
                "projection_differs": (
                    projection != result.solve.edge_ids
                    if args.with_projection and result.solve.status == "OPTIMAL" else ""
                ),
            })
            if index % 100 == 0:
                handle.flush()
                print(f"audited {index}/{len(tasks)}", file=sys.stderr, flush=True)


if __name__ == "__main__":
    main()
