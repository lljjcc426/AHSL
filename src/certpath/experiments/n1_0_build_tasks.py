from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from certpath.reactome_adapter import parse_reactome_biopax
from certpath.task_builder import build_natural_tasks


def _summary(snapshot, tasks):
    graph = snapshot.hypergraph
    tail_sizes = [len(edge.tail) for edge in graph.edges.values()]
    head_sizes = [len(edge.head) for edge in graph.edges.values()]
    return {
        "release": snapshot.release,
        "vertices": len(graph.vertices),
        "hyperedges": len(graph.edges),
        "pathways": len(snapshot.pathways),
        "leaf_pathways_with_reactions": len(snapshot.leaf_pathways()),
        "candidate_tasks": len(tasks),
        "top_level_families": len({task.family for task in tasks}),
        "global_sources": len(graph.global_sources()),
        "self_loops": sum(bool(edge.tail & edge.head) for edge in graph.edges.values()),
        "multi_tail_hyperedges": sum(size > 1 for size in tail_sizes),
        "mean_tail_size": sum(tail_sizes) / len(tail_sizes),
        "max_tail_size": max(tail_sizes),
        "mean_head_size": sum(head_sizes) / len(head_sizes),
        "max_head_size": max(head_sizes),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--v89", type=Path, required=True)
    parser.add_argument("--v97", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("results/n1_0/raw"))
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)

    snapshots = {
        89: parse_reactome_biopax(args.v89, 89),
        97: parse_reactome_biopax(args.v97, 97),
    }
    task_sets = {release: build_natural_tasks(snapshot) for release, snapshot in snapshots.items()}
    for release in (89, 97):
        summary = _summary(snapshots[release], task_sets[release])
        (args.output / f"reactome_v{release}_summary.json").write_text(
            json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        with (args.output / f"tasks_v{release}.csv").open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=[
                "pathway_id", "pathway_name", "family", "gold_size",
                "source_count", "boundary_source_count", "target_count",
            ])
            writer.writeheader()
            for task in task_sets[release]:
                writer.writerow({
                    "pathway_id": task.pathway_id,
                    "pathway_name": task.pathway_name,
                    "family": task.family,
                    "gold_size": len(task.gold_reactions),
                    "source_count": len(task.sources),
                    "boundary_source_count": len(task.boundary_sources),
                    "target_count": len(task.targets),
                })

    old = {task.pathway_id: task for task in task_sets[89]}
    later = {task.pathway_id: task for task in task_sets[97]}
    with (args.output / "temporal_task_status.csv").open("w", newline="", encoding="utf-8") as handle:
        fields = ["pathway_id", "pathway_name", "family", "status", "old_size", "new_size"]
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for pathway_id, task in sorted(later.items()):
            if pathway_id not in old:
                status = "NEW"
                old_size = ""
            else:
                status = "UNCHANGED" if old[pathway_id].gold_reactions == task.gold_reactions else "MODIFIED"
                old_size = len(old[pathway_id].gold_reactions)
            writer.writerow({
                "pathway_id": pathway_id,
                "pathway_name": task.pathway_name,
                "family": task.family,
                "status": status,
                "old_size": old_size,
                "new_size": len(task.gold_reactions),
            })


if __name__ == "__main__":
    main()
