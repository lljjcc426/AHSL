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
