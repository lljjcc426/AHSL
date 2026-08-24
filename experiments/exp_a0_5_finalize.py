"""Regenerate Phase A0.5 aggregates, plots, and the decision report."""

from pathlib import Path

import pandas as pd

from ahsl.experiments.a0_5_analysis import write_analysis_outputs
from ahsl.experiments.a0_5_plotting import generate_a0_5_plots
from ahsl.experiments.a0_5_report import generate_a0_5_report


def main() -> None:
    result_root = Path("results/a0_5")
    raw = pd.read_csv(result_root / "raw/a0_5_results.csv")
    validation = pd.read_csv(
        result_root / "aggregated/a0_5_dp_validation.csv"
    )
    write_analysis_outputs(raw, result_root / "aggregated")
    generate_a0_5_plots(raw, result_root / "plots")
    generate_a0_5_report(raw, validation, result_root / "A0_5_RESEARCH_REPORT.md")
    print(f"Finalized {len(raw):,} result rows under {result_root}")


if __name__ == "__main__":
    main()

