from __future__ import annotations

import argparse
from collections import Counter
from math import comb
from pathlib import Path

import numpy as np
import pandas as pd

from temporal_group_structure.audits import prequential_classes
from temporal_group_structure.candidate_search import cns_candidates, history_statistics
from temporal_group_structure.datasets import load_hif_events
from temporal_group_structure.metrics import deterministic_ranking, exact_set_metrics
from temporal_group_structure.negative_sampling import (
    one_member_corruption,
    random_same_cardinality,
    recall_at_k_from_ranks,
    sampled_rank,
)
from temporal_group_structure.recurrence import score_edge
from temporal_group_structure.splits import chronological_split

DATASETS = ("tags-ask-ubuntu", "congress-bills")
METHODS = (
    "exact_frequency",
    "most_recent",
    "node_frequency_product",
    "pair_sum",
    "pair_min",
    "pair_hawkes",
    "triple_support",
)


def _subsets(test, labels):
    return {
        "all": list(test),
        "repeat": [event for event, label in zip(test, labels, strict=True) if label == "EXACT_REPEAT"],
        "novel": [event for event, label in zip(test, labels, strict=True) if label != "EXACT_REPEAT"],
        "size_ge3": [event for event in test if len(event.nodes) >= 3],
        "size_ge4": [event for event in test if len(event.nodes) >= 4],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default=Path("data/s2_0/downloads"))
    parser.add_argument("--output-dir", type=Path, default=Path("results/s2_0/raw"))
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    retrieval_rows, negative_rows, space_rows = [], [], []
    rng = np.random.default_rng(20260827)

    for dataset in DATASETS:
        events = load_hif_events(args.data_dir / f"{dataset}.json", minimum_size=2)
        split = chronological_split(events)
        history = (*split.train, *split.validation)
        labels = prequential_classes(history, split.test)
        stats = history_statistics(history)
        generated = cns_candidates(history, statistics=stats)
        observed = set(stats["edge_count"])
        bounded_universe = {edge for edge in observed if len(edge) <= 10} | generated
        subsets = _subsets(split.test, labels)
        seen_nodes = set(stats["node_count"])
        max_eval_size = max(len(event.nodes) for event in split.test)
        bounded_to_5 = sum(comb(len(seen_nodes), size) for size in range(2, min(5, len(seen_nodes)) + 1))
        space_rows.append({
            "dataset": dataset,
            "seen_nodes": len(seen_nodes),
            "max_test_size": max_eval_size,
            "bounded_universe_size_2_to_5": bounded_to_5,
            "observed_candidates": len(observed),
            "generated_novel_candidates": len(generated),
            "search_universe": len(bounded_universe),
            "generated_novel_event_recall": sum(event.nodes in generated for event in subsets["novel"]) / len(subsets["novel"]),
            "generated_repeat_event_recall": sum(event.nodes in bounded_universe for event in subsets["repeat"]) / len(subsets["repeat"]),
        })
        for method in METHODS:
            universe = observed if method in {"exact_frequency", "most_recent"} else bounded_universe
            scores = {edge: score_edge(edge, stats, method) for edge in universe}
            ranking = deterministic_ranking(scores)
            for subset_name, truth in subsets.items():
                retrieval_rows.append({
                    "dataset": dataset,
                    "method": method,
                    "subset": subset_name,
                    "truth_events": len(truth),
                    **exact_set_metrics(truth, ranking),
                })

        eligible = [
            event for event, label in zip(split.test, labels, strict=True)
            if label != "EXACT_REPEAT" and event.nodes <= seen_nodes and len(event.nodes) <= 10
        ]
        if len(eligible) > 250:
            eligible = list(rng.choice(eligible, size=250, replace=False))
        node_list = sorted(seen_nodes)
        forbidden = observed | {event.nodes for event in split.test}
        for protocol in ("random_same_cardinality", "one_member_corruption"):
            sampled = []
            for event in eligible:
                sampler = random_same_cardinality if protocol == "random_same_cardinality" else one_member_corruption
                sampled.append((event, [sampler(event.nodes, node_list, forbidden, rng) for _ in range(100)]))
            for method in METHODS:
                ranks = []
                for event, negatives in sampled:
                    ranks.append(sampled_rank(
                        score_edge(event.nodes, stats, method),
                        [score_edge(edge, stats, method) for edge in negatives],
                    ))
                negative_rows.append({
                    "dataset": dataset,
                    "protocol": protocol,
                    "method": method,
                    "events": len(ranks),
                    "recall_at_1": recall_at_k_from_ranks(ranks, 1),
                    "recall_at_10": recall_at_k_from_ranks(ranks, 10),
                    "mrr": float(np.mean([1 / rank for rank in ranks])) if ranks else 0.0,
                })

    pd.DataFrame(retrieval_rows).to_csv(args.output_dir / "retrieval_baselines.csv", index=False)
    pd.DataFrame(negative_rows).to_csv(args.output_dir / "negative_sampling_audit.csv", index=False)
    pd.DataFrame(space_rows).to_csv(args.output_dir / "candidate_space_audit.csv", index=False)
    print(pd.DataFrame(space_rows).to_string(index=False))
    print(pd.DataFrame(retrieval_rows).query("subset in ['all', 'novel']").to_string(index=False))
    print(pd.DataFrame(negative_rows).to_string(index=False))


if __name__ == "__main__":
    main()
