from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from itertools import combinations
import json
from pathlib import Path
import pickle

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from certpath.task_builder import build_natural_tasks
from certpath.overlap_audit import deterministic_family_split


def as_bool(series: pd.Series) -> pd.Series:
    return series.astype(str).str.lower().eq("true")


class UnionFind:
    def __init__(self, items):
        self.parent = {item: item for item in items}

    def find(self, item):
        while self.parent[item] != item:
            self.parent[item] = self.parent[self.parent[item]]
            item = self.parent[item]
        return item

    def union(self, left, right):
        a, b = self.find(left), self.find(right)
        if a != b:
            self.parent[b] = a


def save_plot(path: Path) -> None:
    plt.tight_layout()
    plt.savefig(path, dpi=180)
    plt.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit", type=Path, required=True)
    parser.add_argument("--temporal", type=Path, required=True)
    parser.add_argument("--snapshot-cache", type=Path, required=True)
    parser.add_argument("--aggregated", type=Path, default=Path("results/n1_0/aggregated"))
    parser.add_argument("--plots", type=Path, default=Path("results/n1_0/plots"))
    args = parser.parse_args()
    args.aggregated.mkdir(parents=True, exist_ok=True)
    args.plots.mkdir(parents=True, exist_ok=True)

    audit = pd.read_csv(args.audit)
    feasible = as_bool(audit.gold_feasible)
    attainable = as_bool(audit.attainable)
    nontrivial = as_bool(audit.nontrivial)
    qualified = as_bool(audit.qualified)
    temporal = pd.read_csv(args.temporal)
    with args.snapshot_cache.open("rb") as handle:
        snapshot = pickle.load(handle)
    task_map = {task.pathway_id: task for task in build_natural_tasks(snapshot)}
    graph = snapshot.hypergraph

    gold_sizes = audit.gold_size.to_numpy()
    summary = {
        "candidate_tasks": int(len(audit)),
        "unique_candidate_pathways": int(audit.pathway_id.nunique()),
        "gold_feasible": int(feasible.sum()),
        "gold_feasible_fraction": float(feasible.mean()),
        "requires_internal_repair": int((~feasible).sum()),
        "attainable_natural": int(attainable.sum()),
        "attainable_natural_fraction": float(attainable.mean()),
        "attainable_among_feasible_fraction": float(attainable.sum() / feasible.sum()),
        "nontrivial": int(nontrivial.sum()),
        "qualified": int(qualified.sum()),
        "unique_qualified_pathways": int(audit.loc[qualified, "pathway_id"].nunique()),
        "qualified_families": int(audit.loc[qualified, "family"].nunique()),
        "gold_size_mean": float(np.mean(gold_sizes)),
        "gold_size_median": float(np.median(gold_sizes)),
        "gold_size_p95": float(np.quantile(gold_sizes, 0.95)),
        "gold_size_max": int(np.max(gold_sizes)),
        "gold_size_ge_3_fraction": float(np.mean(gold_sizes >= 3)),
        "gold_size_ge_5_fraction": float(np.mean(gold_sizes >= 5)),
        "gold_multitail_task_fraction": float(np.mean(audit.gold_multitail_reactions > 0)),
        "cyclic_gold_fraction": float(as_bool(audit.cycle).mean()),
        "temporal_counts": {key: int(value) for key, value in temporal.status.value_counts().items()},
        "representability_gate": "FAIL" if attainable.mean() < 0.70 else "PASS",
        "sample_scale_gate": "PASS" if qualified.sum() >= 300 else "FAIL",
    }

    family = audit.assign(feasible=feasible, attainable=attainable, qualified=qualified).groupby("family").agg(
        candidates=("pathway_id", "size"),
        feasible=("feasible", "sum"),
        attainable=("attainable", "sum"),
        qualified=("qualified", "sum"),
        mean_gold_size=("gold_size", "mean"),
        mean_multitail_fraction=("gold_multitail_fraction", "mean"),
    )
    family["attainable_fraction"] = family.attainable / family.candidates
    family.sort_values("candidates", ascending=False).to_csv(args.aggregated / "attainability_by_family.csv")

    retained = audit.loc[qualified]
    excluded = audit.loc[~qualified]
    selection = pd.DataFrame([
        {
            "group": label,
            "tasks": len(frame),
            "mean_gold_size": frame.gold_size.mean(),
            "cycle_fraction": as_bool(frame.cycle).mean(),
            "mean_multitail_fraction": frame.gold_multitail_fraction.mean(),
            "families": frame.family.nunique(),
        }
        for label, frame in (("qualified", retained), ("excluded", excluded))
    ])
    selection.to_csv(args.aggregated / "selection_bias_summary.csv", index=False)

    # A deterministic family holdout with roughly one fifth of qualified tasks.
    test_families = {"Immune System", "DNA Repair", "Hemostasis", "Vesicle-mediated transport"}
    qualified_ids = set(retained.pathway_id)
    qualified_families = {
        row.pathway_id: row.family for row in retained.itertuples(index=False)
    }
    train_ids, test_ids = map(set, deterministic_family_split(qualified_families, test_families))

    def reaction_union(ids):
        result = set()
        for pid in ids:
            result.update(task_map[pid].gold_reactions)
        return result

    def entity_union(ids):
        result = set()
        for pid in ids:
            for edge_id in task_map[pid].gold_reactions:
                edge = graph.edges[edge_id]
                result.update(edge.tail | edge.head)
        return result

    train_reactions, test_reactions = reaction_union(train_ids), reaction_union(test_ids)
    train_entities, test_entities = entity_union(train_ids), entity_union(test_ids)
    family_split = {
        "train_tasks": len(train_ids),
        "test_tasks": len(test_ids),
        "test_families": sorted(test_families),
        "reaction_ids_train": len(train_reactions),
        "reaction_ids_test": len(test_reactions),
        "reaction_id_overlap": len(train_reactions & test_reactions),
        "reaction_id_test_overlap_fraction": len(train_reactions & test_reactions) / len(test_reactions),
        "entity_ids_train": len(train_entities),
        "entity_ids_test": len(test_entities),
        "entity_id_overlap": len(train_entities & test_entities),
        "entity_id_test_overlap_fraction": len(train_entities & test_entities) / len(test_entities),
        "hierarchy_overlap": 0,
    }

    # Reaction-disjoint stress split by connected components under shared IDs.
    uf = UnionFind(sorted(qualified_ids))
    reaction_to_tasks: dict[str, list[str]] = defaultdict(list)
    for pid in qualified_ids:
        for edge_id in task_map[pid].gold_reactions:
            reaction_to_tasks[edge_id].append(pid)
    for ids in reaction_to_tasks.values():
        for other in ids[1:]:
            uf.union(ids[0], other)
    components: dict[str, set[str]] = defaultdict(set)
    for pid in qualified_ids:
        components[uf.find(pid)].add(pid)
    ordered_components = sorted(components.values(), key=lambda values: (len(values), min(values)))
    stress_test: set[str] = set()
    target_size = round(0.20 * len(qualified_ids))
    for component in ordered_components:
        if len(stress_test) < target_size:
            stress_test.update(component)
    stress_train = qualified_ids - stress_test
    reaction_stress = {
        "components": len(components),
        "largest_component_tasks": max(map(len, components.values())),
        "train_tasks": len(stress_train),
        "test_tasks": len(stress_test),
        "train_families": len({task_map[pid].family for pid in stress_train}),
        "test_families": len({task_map[pid].family for pid in stress_test}),
        "reaction_overlap": len(reaction_union(stress_train) & reaction_union(stress_test)),
        "both_sides_meet_300": len(stress_train) >= 300 and len(stress_test) >= 300,
    }

    # Full candidate overlap distribution; retain only aggregate bins and top pairs.
    sets = {pid: task_map[pid].gold_reactions for pid in audit.pathway_id}
    bins = Counter()
    exact_duplicates = subset_pairs = nonzero = 0
    top_pairs: list[tuple[float, int, str, str]] = []
    for left, right in combinations(sorted(sets), 2):
        a, b = sets[left], sets[right]
        shared = len(a & b)
        union = len(a | b)
        jaccard = shared / union if union else 1.0
        if shared:
            nonzero += 1
        if a == b:
            exact_duplicates += 1
        elif a < b or b < a:
            subset_pairs += 1
        bucket = "0" if jaccard == 0 else "(0,.1]" if jaccard <= .1 else "(.1,.25]" if jaccard <= .25 else "(.25,.5]" if jaccard <= .5 else "(.5,.75]" if jaccard <= .75 else "(.75,1)" if jaccard < 1 else "1"
        bins[bucket] += 1
        if shared and (len(top_pairs) < 100 or (jaccard, shared) > top_pairs[0][:2]):
            top_pairs.append((jaccard, shared, left, right))
            top_pairs = sorted(top_pairs, key=lambda row: (row[0], row[1]))[-100:]
    overlap = {
        "pairs": len(audit) * (len(audit) - 1) // 2,
        "nonzero_overlap_pairs": nonzero,
        "exact_duplicate_pairs": exact_duplicates,
        "strict_subset_pairs": subset_pairs,
        "jaccard_bins": dict(bins),
    }
    pd.DataFrame(
        [dict(jaccard=j, shared_reactions=s, left=l, right=r) for j, s, l, r in reversed(top_pairs)]
    ).to_csv(args.aggregated / "top_pathway_overlaps.csv", index=False)

    summary.update({
        "family_split": family_split,
        "reaction_disjoint_stress": reaction_stress,
        "overlap": overlap,
    })
    (args.aggregated / "n1_0_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    flow_labels = ["candidate", "gold feasible", "attainable", "qualified"]
    flow_values = [len(audit), feasible.sum(), attainable.sum(), qualified.sum()]
    plt.figure(figsize=(7, 4))
    plt.bar(flow_labels, flow_values, color=["#4C78A8", "#59A14F", "#F28E2B", "#E15759"])
    plt.ylabel("tasks")
    plt.title("N1.0 supervision flow")
    for i, value in enumerate(flow_values):
        plt.text(i, value + 20, str(int(value)), ha="center")
    save_plot(args.plots / "supervision_flow.png")

    plt.figure(figsize=(7, 4))
    plt.hist(audit.gold_size, bins=np.arange(1, audit.gold_size.max() + 2), color="#4C78A8")
    plt.xlabel("gold reactions")
    plt.ylabel("tasks")
    plt.title("V97 gold pathway size")
    save_plot(args.plots / "gold_size_distribution.png")

    family_plot = family.sort_values("attainable_fraction")
    plt.figure(figsize=(8, 8))
    plt.barh(family_plot.index, family_plot.attainable_fraction, color="#F28E2B")
    plt.axvline(.70, color="black", linestyle="--", linewidth=1)
    plt.xlabel("attainable fraction of natural candidates")
    plt.title("Positive-cost attainability by top-level family")
    save_plot(args.plots / "attainability_by_family.png")

    order = ["0", "(0,.1]", "(.1,.25]", "(.25,.5]", "(.5,.75]", "(.75,1)", "1"]
    plt.figure(figsize=(7, 4))
    plt.bar(order, [bins[key] for key in order], color="#59A14F")
    plt.yscale("log")
    plt.xlabel("pairwise reaction-set Jaccard bin")
    plt.ylabel("pathway pairs (log scale)")
    plt.title("Candidate curated-pathway overlap")
    save_plot(args.plots / "pathway_overlap.png")

    plt.figure(figsize=(6, 4))
    temporal_counts = temporal.status.value_counts()
    plt.bar(temporal_counts.index, temporal_counts.values, color="#76B7B2")
    plt.ylabel("V97 tasks")
    plt.title("V89 to V97 temporal status")
    save_plot(args.plots / "temporal_status.png")


if __name__ == "__main__":
    main()
