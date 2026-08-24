import pandas as pd

from ahsl.experiments.analysis import aggregate_results


def test_aggregation_combines_seeds_with_shared_hyperparameters() -> None:
    rows = []
    for seed, clean_f1 in [(0, 0.7), (1, 0.9)]:
        rows.append(
            {
                "n": 10,
                "m": 4,
                "tree_topology": "path",
                "branch_probability": 0.4,
                "p_false_positive": 0.2,
                "p_false_negative": 0.2,
                "num_observations": 1,
                "model": "Unconstrained",
                "hyperparameters": '{"epochs": 10}',
                "seed": seed,
                "clean_f1": clean_f1,
            }
        )
    summary = aggregate_results(pd.DataFrame(rows))
    assert len(summary) == 1
    assert summary.loc[0, "clean_f1_count"] == 2
    assert summary.loc[0, "clean_f1_mean"] == 0.8

