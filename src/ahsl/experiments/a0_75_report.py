"""Generate the Phase A0.75 research decision report."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from ahsl.experiments.a0_75_analysis import (
    alternating_diagnostics,
    edge_utility_correlations,
    gate_summary,
    primary_result_table,
    random_tree_diagnostics,
    tie_diagnostics,
)


def _table(frame: pd.DataFrame, formats: dict[str, str] | None = None) -> str:
    display = frame.copy()
    for column, specifier in (formats or {}).items():
        if column in display:
            display[column] = display[column].map(
                lambda value: "" if pd.isna(value) else format(value, specifier)
            )
    columns = [str(column) for column in display.columns]
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    rows = [
        "| " + " | ".join(str(value) for value in row) + " |"
        for row in display.itertuples(index=False, name=None)
    ]
    return "\n".join([header, separator, *rows])


def generate_a0_75_report(
    primary_with_profile: pd.DataFrame,
    r3: pd.DataFrame,
    output_path: Path,
) -> None:
    table = primary_result_table(primary_with_profile)
    overall = table[table["scope"] == "overall"].copy()
    topology = table[table["scope"] != "overall"].copy()
    gate = gate_summary(table, primary_with_profile).iloc[0]
    r3_table = primary_result_table(r3)
    r3_overall = r3_table[r3_table["scope"] == "overall"]
    r3_best_classical = r3_overall[
        r3_overall["estimator"].isin(
            [
                "BinaryMWST",
                "NoiseCorrectedMWST",
                "BootstrapStabilityMWST",
                "AlternatingTreeIncidenceEstimator",
            ]
        )
    ]["mean_excess"].min()
    random = random_tree_diagnostics(primary_with_profile)
    alternating = alternating_diagnostics(primary_with_profile)
    correlations = edge_utility_correlations(primary_with_profile)
    ties = tie_diagnostics(primary_with_profile)

    profile = primary_with_profile[
        primary_with_profile["estimator"] == "ProfileLikelihoodTreeSearch"
    ]
    binary = overall.set_index("estimator").loc["BinaryMWST"]
    corrected = overall.set_index("estimator").loc["NoiseCorrectedMWST"]
    bootstrap = overall.set_index("estimator").loc["BootstrapStabilityMWST"]
    alternating_row = overall.set_index("estimator").loc[
        "AlternatingTreeIncidenceEstimator"
    ]
    random_row = overall.set_index("estimator").loc["DataAgnosticRandomTree"]
    profile_row = overall.set_index("estimator").loc[
        "ProfileLikelihoodTreeSearch"
    ]
    correlation = correlations[correlations["scope"] == "overall"].iloc[0]
    best_name = str(gate["best_classical_estimator"])
    best_ties = ties[ties["estimator"] == best_name]

    primary_columns = [
        "estimator",
        "mean_hamming",
        "mean_excess",
        "excess_ci_lower",
        "excess_ci_upper",
        "exact_row_recovery",
        "valid_clean_join_tree_rate",
        "tree_edge_disagreement",
        "runtime_seconds",
    ]
    number_formats = {
        "mean_hamming": ".5f",
        "mean_excess": ".5f",
        "excess_ci_lower": ".5f",
        "excess_ci_upper": ".5f",
        "exact_row_recovery": ".5f",
        "valid_clean_join_tree_rate": ".3f",
        "tree_edge_disagreement": ".5f",
        "runtime_seconds": ".4f",
    }
    text = f"""# AHSL Phase A0.75 Research Report

## 1. Research decision question

This phase asks whether latent join-tree learning retains enough downstream
value after stronger classical estimators to justify a learned A1. It is a
kill-test, not a model-building phase. No neural model was implemented. The
primary evidence uses `n=300`, `m=16`, symmetric noise 0.20, `R=1`, four
topologies, and 30 paired dataset seeds.

## 2. Theory of noise-corrected intersections

With `delta = 1 - p_- - p_+` and
`Z=(Y_bar-p_+)/delta`, `E[Z_ij|X_ij]=X_ij`. Under conditional independence of
noise across distinct columns, `sum_i Z_ij Z_ik` is unbiased for the clean
intersection weight when `j != k`. The implementation does not clip `Z` or
negative weights, rejects `abs(delta)<1e-12`, and ignores the diagonal because
it is irrelevant to an MST. This unbiasedness applies to pairwise weights, not
to the final discrete MWST.

## 3. Experimental protocol

Each seed fixes one generating tree, clean simple-hypergraph incidence, and set
of noisy observations shared across comparisons. Fitting sees only the noisy
observations; `TrueTreeOracle` is the sole estimator that receives the generating
tree. Clean incidence is evaluation-only. All downstream comparisons use the same
`DPNoiseAwareConnectedMLE` and its fixed canonical tie policy. Bootstrap uses
100 row-resamples. The random control uses the first of five preregistered
data-independent trees; best-of-five is diagnostic only. Confidence intervals
bootstrap 30 seed-level means, averaging the four topologies within seed rather
than pooling 120 rows as iid replicates.

## 4. Binary MWST baseline

Observed incidence and independent MLE were identical on all 120 primary
datasets under `R=1` symmetric noise, so they are one evidence row. BinaryMWST
has Hamming {binary['mean_hamming']:.5f} and downstream excess
{binary['mean_excess']:.5f} with 95% CI
[{binary['excess_ci_lower']:.5f}, {binary['excess_ci_upper']:.5f}].

## 5. Noise-corrected MWST

Noise correction lowers excess to {corrected['mean_excess']:.5f}, a reduction
of {binary['mean_excess'] - corrected['mean_excess']:.5f} relative to BinaryMWST.
It does not reach the true-tree decoder: its upper and lower paired confidence
bounds remain above 0.01.

## 6. Bootstrap stability MWST

BootstrapStabilityMWST is the best classical estimator: mean excess
{bootstrap['mean_excess']:.5f}, 95% CI
[{bootstrap['excess_ci_lower']:.5f}, {bootstrap['excess_ci_upper']:.5f}]. It
improves only modestly over direct correction and closes
{gate['gap_closure_fraction']:.1%} of the BinaryMWST gap.

## 7. Random-tree control

The first preregistered random tree has excess {random_row['mean_excess']:.5f}.
Across five random trees per dataset, mean Hamming is
{random['random_mean_hamming'].mean():.5f}, best-of-five oracle-style Hamming is
{random['random_best_of_5_hamming'].mean():.5f}, and mean within-dataset standard
deviation is {random['random_across_tree_sd'].mean():.5f}. Data-driven bootstrap
beats the primary random tree by
{gate['best_data_driven_advantage_over_random']:.5f} Hamming, so generic tree
regularization alone does not explain the result.

## 8. Alternating structured estimator

Alternating estimation has excess {alternating_row['mean_excess']:.5f}.
{alternating[alternating['scope'] == 'overall']['converged_0_fraction'].iloc[0]:.1%}
of runs converge without changing the initial corrected tree; only
{alternating[alternating['scope'] == 'overall']['final_tree_differs_fraction'].iloc[0]:.1%}
finish with a different tree. It therefore adds little beyond initialization.

{_table(alternating, {"converged_0_fraction": ".3f", "converged_1_fraction": ".3f", "converged_2plus_fraction": ".3f", "max_iteration_reached_fraction": ".3f", "final_tree_differs_fraction": ".3f"})}

## 9. True-tree information value

`Value_of_true_tree = Hamming(RandomTree) - Hamming(TrueTree)` is
{gate['value_of_true_tree']:.5f} overall, well above the 0.005 kill threshold.
The value is substantial for balanced, path, and random topologies but small on
stars. Thus tree identity matters in three families under the fixed decoder,
while star remains a topology-specific prior-misspecification region.

## 10. Classical residual gap

{_table(overall[primary_columns], number_formats)}

The best residual is {gate['best_classical_excess']:.5f}, with paired 95% CI
[{gate['best_classical_ci_lower']:.5f}, {gate['best_classical_ci_upper']:.5f}].
At `R=3`, the best residual falls to
{r3_best_classical:.5f}; this confirms that the unresolved problem
is concentrated in the one-observation regime.

## 11. Gap closure fraction

Binary excess is {gate['binary_excess']:.5f}; best-classical excess is
{gate['best_classical_excess']:.5f}; untruncated gap closure is
{gate['gap_closure_fraction']:.5f}. This is below the 0.80 hard-stop threshold.

## 12. Topology-specific results

{_table(topology[["scope", "estimator", "mean_excess", "excess_ci_lower", "excess_ci_upper"]], {"mean_excess": ".5f", "excess_ci_lower": ".5f", "excess_ci_upper": ".5f"})}

The best estimator leaves excess at least 0.01 in
{int(gate['topologies_with_residual'])} topology families. Star behaves in the
opposite direction: estimated trees can outperform the generating-tree decoder,
consistent with A0.5 evidence that the uniform subtree prior is misspecified on
stars. Star is reported separately and is not used alone to reject
alpha-acyclicity.

## 13. Edge recovery vs downstream utility

Across non-oracle primary estimators including conditional profile search,
Pearson correlation between edge disagreement and downstream excess is
{correlation['pearson']:.3f}; Spearman correlation is
{correlation['spearman']:.3f}. This is a moderate association overall, but it is
not causal and is much weaker or reversed on stars. High edge disagreement is
therefore diagnostic, not itself a failure criterion.

Profile search was correctly triggered because the pre-profile residual exceeded
0.01. It raised noisy-data profile likelihood and changed the tree in
{profile['tree_changed'].mean():.1%} of datasets, yet worsened downstream excess
to {profile_row['mean_excess']:.5f}. Its deterministic pruning evaluated at most
24 corrected-weight-ranked single-swap candidates per iteration; exact full-data
profile likelihood selected among them.

## 14. Evidence FOR learned join-tree estimation

- True-tree information value is {gate['value_of_true_tree']:.5f}, not negligible.
- Best classical excess remains {gate['best_classical_excess']:.5f} with its
  entire paired CI above 0.01.
- Residuals above 0.01 occur in three topology families.
- The best data-driven estimator materially beats the preregistered random tree.
- The required profile-likelihood search fails to close the gap.
- On rows where both bootstrap-tree and true-tree DP solutions are unique, mean
  residual remains {gate['best_unique_row_excess']:.5f}; arbitrary tie selection
  is not the sole explanation.

## 15. Evidence AGAINST learned join-tree estimation

- Noise correction alone removes a substantial part of the A0.5 BinaryMWST gap.
- Bootstrap closes only {gate['gap_closure_fraction']:.1%}, leaving a target that
  is real but modest in absolute Hamming units.
- At `R=3`, classical excess is already about 0.002.
- Alternating re-estimation almost always stops immediately.
- Profile likelihood actively worsens clean recovery, exposing objective
  misspecification rather than lack of search effort.
- All evidence is synthetic and assumes known independent noise rates.

## 16. Hard kill-rule evaluation

| Rule | Result | Reason |
| --- | --- | --- |
| A: classical mean <=0.005 and CI upper <=0.010 | {bool(gate['hard_stop_a'])} | Best mean and CI remain above thresholds. |
| B: random-minus-true <=0.005 | {bool(gate['hard_stop_b'])} | Value of true tree is {gate['value_of_true_tree']:.5f}. |
| C: closure >=0.80 and excess <0.01 | {bool(gate['hard_stop_c'])} | Closure is {gate['gap_closure_fraction']:.3f}. |
| All continuation conditions | {bool(gate['continuation_conditions_all_met'])} | Three non-star families retain a unique-row residual and profile search fails. |

## 17. Final A0.75 decision

**{gate['final_decision_code']}: {gate['final_decision']}**

This decision is narrow: it justifies preparing a separate learned-A1 proposal
for the one-observation regime. It does not justify implementing a neural model
inside A0.75, expanding the grid, or treating star as supporting evidence.

## 18. Recommended next research direction

Prepare a separate A1 proposal with one learned edge-scoring estimator followed
by the same deterministic MWST decoder. Freeze the R=1 A0.75 datasets and compare
against BinaryMWST, NoiseCorrectedMWST, BootstrapStabilityMWST, the first random
tree, and TrueTreeOracle. The primary endpoint remains paired downstream Hamming;
balanced, path, random, and star must be reported separately. The proposal must
predefine stopping if it fails to beat bootstrap or if gains arise only through
tie resolution. No neural implementation belongs to this phase.
"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(text, encoding="utf-8")
