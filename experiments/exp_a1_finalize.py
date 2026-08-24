"""Build final Phase A1 tables, figures, and research report."""

from pathlib import Path

import pandas as pd

from ahsl.experiments.a1_analysis import write_primary_analysis
from ahsl.experiments.a1_plotting import generate_a1_plots
from ahsl.experiments.a1_report import generate_a1_report


def main() -> None:
    root = Path("results/a1")
    raw = root / "raw"
    aggregated = root / "aggregated"
    primary = pd.read_csv(raw / "a1_primary_results.csv")
    validation = pd.read_csv(raw / "a1_validation_results.csv")
    q_results = pd.read_csv(raw / "a1_q_identifiability_results.csv")
    global_results = pd.read_csv(raw / "a1_small_global_search_results.csv")
    gate = write_primary_analysis(primary, aggregated)
    generate_a1_plots(primary, root / "plots")
    generate_a1_report(
        pd.read_csv(aggregated / "a1_primary_table.csv"),
        gate,
        validation,
        q_results,
        global_results,
        pd.read_csv(aggregated / "a1_decoder_comparison.csv"),
        pd.read_csv(aggregated / "a1_likelihood_behavior.csv"),
        root / "A1_RESEARCH_REPORT.md",
    )
    print(
        f"Finalized {len(primary):,} primary rows, "
        f"{int(validation['row_comparisons'].sum()):,} validation comparisons, "
        f"{len(q_results):,} q diagnostics, and {len(global_results):,} global cases"
    )


if __name__ == "__main__":
    main()
