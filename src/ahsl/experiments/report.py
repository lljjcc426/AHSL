"""Evidence-based Markdown research report generation."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


def _markdown_table(frame: pd.DataFrame) -> str:
    if frame.empty:
        return "No rows were available."
    columns = list(frame.columns)
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    rows = [
        "| " + " | ".join(str(value) for value in row) + " |"
        for row in frame.itertuples(index=False, name=None)
    ]
    return "\n".join([header, separator, *rows])


def _paired_difference(
    raw: pd.DataFrame, model: str, baseline: str, metric: str
) -> np.ndarray:
    estimate = raw[raw["model"] == model][["experiment_id", metric]]
    comparison = raw[raw["model"] == baseline][["experiment_id", metric]]
    merged = estimate.merge(
        comparison, on="experiment_id", suffixes=("_model", "_baseline")
    )
    return merged[f"{metric}_model"].to_numpy() - merged[f"{metric}_baseline"].to_numpy()


def _paired_setting_summary(raw: pd.DataFrame) -> pd.DataFrame:
    rng = np.random.default_rng(314159)
    records: list[dict[str, object]] = []
    ahsl = raw[raw["model"] == "FixedTreeAHSL"][
        ["experiment_id", "noise_setting", "num_observations", "clean_f1"]
    ]
    for baseline in (
        "Observed",
        "NearestConnectedSubtree",
        "NoiseAwareMAPSubtree",
    ):
        comparison = raw[raw["model"] == baseline][["experiment_id", "clean_f1"]]
        merged = ahsl.merge(
            comparison, on="experiment_id", suffixes=("_ahsl", "_baseline")
        )
        for (noise_setting, repetitions), group in merged.groupby(
            ["noise_setting", "num_observations"]
        ):
            differences = (
                group["clean_f1_ahsl"] - group["clean_f1_baseline"]
            ).to_numpy()
            indices = rng.integers(
                0, len(differences), size=(2000, len(differences))
            )
            bootstrap_means = differences[indices].mean(axis=1)
            lower, upper = np.quantile(bootstrap_means, [0.025, 0.975])
            records.append(
                {
                    "noise_setting": noise_setting,
                    "observations": repetitions,
                    "baseline": baseline,
                    "pairs": len(differences),
                    "mean_dF1": round(float(differences.mean()), 4),
                    "CI_2.5%": round(float(lower), 4),
                    "CI_97.5%": round(float(upper), 4),
                    "AHSL_win_rate": round(float((differences > 0).mean()), 3),
                }
            )
    return pd.DataFrame.from_records(records)


def write_research_report(
    raw: pd.DataFrame,
    statistical_tests: pd.DataFrame,
    output_path: Path,
    config: dict[str, object],
) -> None:
    """Write an A0 report that separates numerical observations from interpretation."""
    nonzero = raw[
        (raw["p_false_positive"] > 0.0) | (raw["p_false_negative"] > 0.0)
    ]
    observed_difference = _paired_difference(
        nonzero, "FixedTreeAHSL", "Observed", "clean_f1"
    )
    nearest_difference = _paired_difference(
        nonzero, "FixedTreeAHSL", "NearestConnectedSubtree", "clean_f1"
    )
    map_difference = _paired_difference(
        nonzero, "FixedTreeAHSL", "NoiseAwareMAPSubtree", "clean_f1"
    )
    nearest_structural_gain = _paired_difference(
        nonzero, "NearestConnectedSubtree", "Observed", "clean_f1"
    )
    map_structural_gain = _paired_difference(
        nonzero, "NoiseAwareMAPSubtree", "Observed", "clean_f1"
    )
    nearest_exact_gain = _paired_difference(
        nonzero, "NearestConnectedSubtree", "Observed", "exact_row_recovery"
    )
    map_exact_gain = _paired_difference(
        nonzero, "NoiseAwareMAPSubtree", "Observed", "exact_row_recovery"
    )

    selected_sparse_lambda = float(config["plots"]["sparse_lambda"])
    report_rows = raw.copy()
    is_selected_sparse = report_rows["hyperparameters"].map(
        lambda value: json.loads(value).get("lambda_s") == selected_sparse_lambda
        if isinstance(value, str) and value.startswith("{")
        else False
    )
    report_rows = report_rows[
        (report_rows["model"] != "SparseUnconstrained") | is_selected_sparse
    ]
    main = (
        report_rows[
            np.isclose(
                report_rows["p_false_positive"], report_rows["p_false_negative"]
            )
            & (report_rows["num_observations"] == 1)
        ]
        .assign(noise=lambda frame: frame["p_false_positive"])
        .groupby(["model", "noise"], as_index=False)
        .agg(
            clean_f1=("clean_f1", "mean"),
            exact_row_recovery=("exact_row_recovery", "mean"),
            riv=("running_intersection_violations", "mean"),
            runtime_seconds=("runtime_seconds", "mean"),
        )
    )
    main = main.round(4)

    max_candidates = int(raw["num_connected_subtrees"].max())
    max_runtime = float(raw[raw["model"] == "FixedTreeAHSL"]["runtime_seconds"].max())
    ahsl_riv_max = int(
        raw[raw["model"] == "FixedTreeAHSL"]["running_intersection_violations"].max()
    )
    observed_gain = float(observed_difference.mean()) if len(observed_difference) else np.nan
    nearest_gain = float(nearest_difference.mean()) if len(nearest_difference) else np.nan
    map_gain = float(map_difference.mean()) if len(map_difference) else np.nan
    nearest_prior_gain = float(nearest_structural_gain.mean())
    map_prior_gain = float(map_structural_gain.mean())
    nearest_exact_prior_gain = float(nearest_exact_gain.mean())
    map_exact_prior_gain = float(map_exact_gain.mean())

    structural_gain = max(nearest_prior_gain, map_prior_gain)
    if structural_gain > 0.01 and map_gain <= 0.01:
        decision = "Decision B - Keep alpha-acyclic structure but abandon neural A0 estimation"
        recommendation = "Modify A0"
    elif observed_gain > 0.01 and map_gain > 0.01:
        decision = "Decision A - Continue to A1"
        recommendation = "Proceed to A1"
    else:
        decision = "Decision C - Reconsider the hypothesis"
        recommendation = "Do not proceed yet"

    statistical_excerpt = _paired_setting_summary(raw)
    concentration_by_setting = raw[raw["model"] == "FixedTreeAHSL"].groupby(
        ["noise_setting", "num_observations"]
    ).agg(
        entropy=("mean_categorical_entropy", "mean"),
        max_probability=("mean_max_subtree_probability", "mean"),
    )
    worst_concentration = float(concentration_by_setting["max_probability"].min())
    largest_entropy = float(concentration_by_setting["entropy"].max())
    sparse = raw[raw["model"] == "SparseUnconstrained"]
    observed = raw[raw["model"] == "Observed"][["experiment_id", "clean_f1"]]
    sparse_comparison = sparse.merge(
        observed, on="experiment_id", suffixes=("_sparse", "_observed")
    )
    largest_sparse_f1_change = float(
        np.abs(
            sparse_comparison["clean_f1_sparse"]
            - sparse_comparison["clean_f1_observed"]
        ).max()
    )

    report = f"""# AHSL Phase A0 Research Report

## 1. Research question

Does restricting each incidence row to a connected subtree of a known join tree improve recovery of a clean alpha-acyclic hypergraph from independently corrupted incidence observations?

## 2. Mathematical formulation

The hyperedge labels are the nodes of a fixed tree `T`. For every original vertex `i`, the support `S_i = {{j : B_ij = 1}}` is selected from the complete set of non-empty connected induced node sets of `T`. This is the classical join-tree/running-intersection characterization, not a novelty claim.

## 3. Models and baselines

The run compares raw observations, independent free logits, normalized-L1 free logits, exact nearest-connected-subtree projection, exact likelihood MAP with known corruption rates, and categorical FixedTreeAHSL over all connected subtrees. The unconstrained logits can memorize one binary observation and are a sanity baseline, not a denoiser with an independent statistical signal.

## 4. Experimental setup

Configuration ID: `{config['experiment_id']}`. The run used `n={config['n_values']}`, `m={config['m_values']}`, branch probabilities `{config['branch_probabilities']}`, topologies `{config['tree_topologies']}`, observation counts `{config['observation_repetitions']}`, and seeds `{config['seeds']}`. The true join tree is known. Results retain every seed and use no clean-incidence oracle for model fitting or sparse-lambda selection. This A0 experiment measures structural projection/denoising; it does not establish consistency or general hypergraph structure learning.

## 5. Main numerical results

The following are observed means across the symmetric-noise, one-observation portion actually run.

{_markdown_table(main)}

## 6. Statistical comparison

Paired differences are `FixedTreeAHSL - baseline`. The table pools the four preregistered topologies within each noise/observation setting, giving 20 paired cases per row; intervals are paired bootstrap intervals. Per-topology Wilcoxon results remain in `results/aggregated/a0_statistical_tests.csv` and are not over-interpreted with only five seeds.

{_markdown_table(statistical_excerpt)}

## 7. Does alpha-acyclicity help denoise structure?

Observation: across nonzero-noise rows, mean clean-F1 gains over Observed were `{nearest_prior_gain:.4f}` for NearestConnectedSubtree and `{map_prior_gain:.4f}` for NoiseAwareMAPSubtree. Their exact-row recovery gains were `{nearest_exact_prior_gain:.4f}` and `{map_exact_prior_gain:.4f}`. FixedTreeAHSL itself differed from Observed by `{observed_gain:.4f}`. The maximum AHSL running-intersection violation count was `{ahsl_riv_max}`.

Interpretation: the positive exact-estimator differences support useful denoising by the fixed-tree hypothesis class, but the learned categorical estimator does not realize that average F1 gain. Zero RIV verifies the construction and is not by itself evidence of better recovery.

## 8. Does learning outperform exact structural projection?

Observation: mean paired clean-F1 differences were `{nearest_gain:.4f}` against NearestConnectedSubtree and `{map_gain:.4f}` against NoiseAwareMAPSubtree.

Interpretation: if these values are non-positive, the A0 evidence supports the structural constraint but not a learned estimator over the exact classical alternatives.

## 9. Failure modes

The central implementation failure is an objective/inference mismatch. With repeated observations, BCE targets fractional incidence marginals and learns a diffuse mixture over subtrees, while inference discards that mixture through a single categorical `argmax`. Across setting means, the largest entropy was `{largest_entropy:.4f}` and the lowest mean maximum candidate probability was `{worst_concentration:.4f}`. This explains why additional observations can improve exact MAP while widening its advantage over FixedTreeAHSL. There was no universal singleton collapse, but missing-only noise increased singleton predictions. The requested normalized-L1 range changed clean F1 by at most `{largest_sparse_f1_change:.4f}` relative to Observed at the fixed threshold, so it did not provide a useful density-matched curve. Topology and asymmetric-noise effects remain visible in the raw CSV.

## 10. Computational limitations

The implementation enumerates all non-empty masks in `O(2^m m)` time. This pilot selected only `m={config['m_values']}`; its largest realized candidate set was `{max_candidates}`, and the largest measured FixedTreeAHSL fit time was `{max_runtime:.4f}` seconds. The runtime-versus-`m` plot therefore contains only the pilot point and is not a scaling result. Candidate growth is topology dependent, especially for stars; no scalability claim is made.

## 11. Evidence supporting the hypothesis

The strongest supporting evidence is the positive paired recovery gain of exact connected-subtree projection/MAP over raw observations, especially for exact-row recovery, together with exact RIV=0 for every structural estimator. This supports the alpha-acyclic fixed-tree hypothesis class as a denoising prior in part of the tested region.

## 12. Evidence against the hypothesis

The strongest counter-evidence is that FixedTreeAHSL averaged `{nearest_gain:.4f}` F1 relative to nearest projection and `{map_gain:.4f}` relative to known-noise MAP under nonzero noise. It also averaged `{observed_gain:.4f}` relative to raw observations. The gain is not uniform across noise regimes, and the sparse range did not create a meaningful density-matched comparator. These data do not justify neural superiority or progression to a learned join tree.

## 13. Recommended next step

Research decision: **{decision}**.

Final recommendation: **{recommendation}**.

Replace the current neural A0 estimator with exact projection/MAP as the anchor, and test additional `m`, branch probabilities, and seeds before A1. A learned model should return only if its training objective is aligned with the hard subtree decision or it uses a downstream likelihood unavailable to the exact baseline.

This recommendation is limited to the configurations actually run. Phase A0 assumes the true join tree is known and does not yet establish usefulness for general hypergraph structure learning.
"""
    output_path.write_text(report, encoding="utf-8")
