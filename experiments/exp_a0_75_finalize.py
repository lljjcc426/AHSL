"""Build final A0.75 tables, figures, and the research report."""

from pathlib import Path

import pandas as pd

from ahsl.experiments.a0_75_analysis import write_analysis_outputs
from ahsl.experiments.a0_75_plotting import generate_a0_75_plots
from ahsl.experiments.a0_75_report import generate_a0_75_report


def main() -> None:
    result_root = Path("results/a0_75")
    primary = pd.read_csv(result_root / "raw/a0_75_primary_results.csv")
    profile = pd.read_csv(result_root / "raw/a0_75_profile_search_results.csv")
    r3 = pd.read_csv(result_root / "raw/a0_75_r3_results.csv")
    combined = pd.concat([primary, profile], ignore_index=True, sort=False)
    combined.to_csv(
        result_root / "raw/a0_75_primary_with_profile_results.csv", index=False
    )
    write_analysis_outputs(
        primary, result_root / "aggregated", "a0_75_primary"
    )
    write_analysis_outputs(
        combined, result_root / "aggregated", "a0_75_primary_with_profile"
    )
    write_analysis_outputs(
        combined, result_root / "aggregated", "a0_75_primary_final"
    )
    generate_a0_75_plots(combined, result_root / "plots")
    generate_a0_75_report(
        combined, r3, result_root / "A0_75_RESEARCH_REPORT.md"
    )
    print(
        f"Finalized {len(primary):,} primary rows, {len(profile):,} profile rows, "
        f"and {len(r3):,} R=3 rows"
    )


if __name__ == "__main__":
    main()
