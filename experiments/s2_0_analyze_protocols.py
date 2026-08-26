from __future__ import annotations

from pathlib import Path

import pandas as pd
from scipy.stats import kendalltau, spearmanr


def main() -> None:
    root = Path("results/s2_0/raw")
    negative = pd.read_csv(root / "negative_sampling_audit.csv")
    retrieval = pd.read_csv(root / "retrieval_baselines.csv")
    rows = []
    for dataset in sorted(negative.dataset.unique()):
        table = negative[negative.dataset.eq(dataset)].pivot(
            index="method", columns="protocol", values="recall_at_10"
        )
        search = retrieval[
            retrieval.dataset.eq(dataset) & retrieval.subset.eq("novel")
        ].set_index("method")["mrr"].rename("search_controlled")
        table = table.join(search)
        for left, right in (
            ("random_same_cardinality", "one_member_corruption"),
            ("random_same_cardinality", "search_controlled"),
            ("one_member_corruption", "search_controlled"),
        ):
            rows.append({
                "dataset": dataset,
                "protocol_left": left,
                "protocol_right": right,
                "spearman": float(spearmanr(table[left], table[right]).statistic),
                "kendall_tau": float(kendalltau(table[left], table[right]).statistic),
                "top_left": str(table[left].idxmax()),
                "top_right": str(table[right].idxmax()),
            })
    output = pd.DataFrame(rows)
    output.to_csv(root / "protocol_rank_correlation.csv", index=False)
    print(output.to_string(index=False))


if __name__ == "__main__":
    main()
