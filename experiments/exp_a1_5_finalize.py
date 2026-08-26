from pathlib import Path

import pandas as pd

from ahsl.experiments.a1_5_analysis import write_analysis
from ahsl.experiments.a1_5_plotting import generate_plots
from ahsl.experiments.a1_5_report import generate_report


def main() -> None:
    root = Path("results/a1_5")
    raw_dir = root / "raw"
    aggregated = root / "aggregated"
    raw = pd.read_csv(raw_dir / "a1_5_primary_results.csv")
    risk_rows = pd.read_csv(raw_dir / "a1_5_risk_rows.csv")
    validation = pd.read_csv(raw_dir / "a1_5_validation_results.csv")
    scaling = pd.read_csv(raw_dir / "a1_5_scaling_results.csv")
    gate = write_analysis(raw, risk_rows, aggregated)
    pd.DataFrame(
        [
            {
                "posterior_rows": validation["row_comparisons"].sum(),
                "marginal_entries": validation["marginal_entry_comparisons"].sum(),
                "marginal_mismatches": validation["marginal_row_mismatches"].sum(),
                "max_marginal_error": validation["max_marginal_absolute_error"].max(),
                "max_normalization_error": validation["max_posterior_normalization_error"].max(),
                "map_mismatches": validation["map_action_mismatches"].sum(),
                "median_mismatches": validation["median_action_mismatches"].sum(),
                "connected_mbr_mismatches": validation["connected_action_mismatches"].sum(),
                "max_action_risk_error": validation["max_action_risk_error"].max(),
                "max_root_invariance_error": validation["max_root_invariance_error"].max(),
            }
        ]
    ).to_csv(aggregated / "a1_5_validation_summary.csv", index=False)
    generate_plots(raw, risk_rows, root / "plots")
    table = pd.read_csv(aggregated / "a1_5_primary_table.csv")
    decoder = pd.read_csv(aggregated / "a1_5_decoder_gains.csv")
    tree_gains = pd.read_csv(aggregated / "a1_5_tree_gains.csv")
    connectivity = pd.read_csv(aggregated / "a1_5_connectivity_costs.csv")
    exact = pd.read_csv(aggregated / "a1_5_exact_row_tradeoff.csv")
    non_tied = pd.read_csv(aggregated / "a1_5_non_tied_tree_gain.csv")
    generate_report(
        table,
        decoder,
        tree_gains,
        connectivity,
        exact,
        non_tied,
        gate,
        validation,
        scaling,
        root / "A1_5_RESEARCH_REPORT.md",
    )


if __name__ == "__main__":
    main()
