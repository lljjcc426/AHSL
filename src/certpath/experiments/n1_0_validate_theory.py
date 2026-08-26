from __future__ import annotations

import argparse
import csv
from itertools import combinations
import json
from pathlib import Path
import random

from certpath.attainability import check_positive_cost_attainability
from certpath.hypergraph_builder import DirectedHypergraph, Hyperedge


def powerset(items):
    for size in range(len(items) + 1):
        yield from (frozenset(x) for x in combinations(items, size))


def random_graph(rng: random.Random, index: int) -> DirectedHypergraph:
    vertices = ["s", "a", "b", "c", "t"]
    edges = [
        Hyperedge(f"{index}:seed", frozenset({"s"}), frozenset({"a", "b"})),
        Hyperedge(f"{index}:join", frozenset({"a", "b"}), frozenset({"t"})),
    ]
    for position in range(4):
        tail_size = rng.choice([1, 1, 2])
        head_size = rng.choice([1, 1, 2])
        tail = frozenset(rng.sample(vertices[:-1], tail_size))
        head = frozenset(rng.sample(vertices[1:], head_size))
        edges.append(Hyperedge(f"{index}:r{position}", tail, head))
    return DirectedHypergraph(edges)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("results/n1_0/raw/attainability_bruteforce.csv"))
    parser.add_argument("--graphs", type=int, default=64)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    rng = random.Random(20260826)
    rows = []
    for graph_index in range(args.graphs):
        graph = random_graph(rng, graph_index)
        ids = sorted(graph.edges)
        feasible_sets = [subset for subset in powerset(ids) if graph.is_feasible({"s"}, {"t"}, subset)]
        brute_minimum = min(map(len, feasible_sets))
        exact = check_positive_cost_attainability(
            graph, frozenset({"s"}), frozenset({"t"}), frozenset(ids), time_limit=10, compute_minimum=True
        )
        solver_mismatch = exact.minimum_size != brute_minimum
        for gold in feasible_sets:
            expected = not any(candidate < gold for candidate in feasible_sets)
            observed = not any(graph.is_feasible({"s"}, {"t"}, gold - {edge}) for edge in gold)
            rows.append({
                "graph": graph_index,
                "gold": ";".join(sorted(gold)),
                "gold_size": len(gold),
                "expected_attainable": expected,
                "checker_attainable": observed,
                "decision_mismatch": expected != observed,
                "solver_minimum": exact.minimum_size,
                "brute_minimum": brute_minimum,
                "solver_mismatch": solver_mismatch,
                "has_multitail": any(len(graph.edges[e].tail) > 1 for e in gold),
                "has_cycle": graph.contains_cycle(gold),
                "has_self_loop": any(graph.edges[e].tail & graph.edges[e].head for e in gold),
            })
    with args.output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    summary = {
        "graphs": args.graphs,
        "feasible_gold_sets": len(rows),
        "decision_mismatches": sum(row["decision_mismatch"] for row in rows),
        "solver_mismatches": sum(row["solver_mismatch"] for row in rows),
        "multitail_cases": sum(row["has_multitail"] for row in rows),
        "cyclic_cases": sum(row["has_cycle"] for row in rows),
        "self_loop_cases": sum(row["has_self_loop"] for row in rows),
    }
    args.output.with_suffix(".summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
