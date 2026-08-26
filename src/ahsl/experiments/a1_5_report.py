"""Generate the 25-section Phase A1.5 research report."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def _markdown(frame: pd.DataFrame, digits: int = 5) -> str:
    display = frame.copy()
    for column in display.select_dtypes(include="number"):
        display[column] = display[column].map(
            lambda value: (
                ""
                if pd.isna(value)
                else "0"
                if value == 0
                else str(int(value))
                if abs(value) >= 100 and float(value).is_integer()
                else f"{value:.2e}"
                if value != 0 and abs(value) < 10 ** (-digits)
                else f"{value:.{digits}f}"
            )
        )
    columns = list(display.columns)
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    lines.extend(
        "| " + " | ".join(str(row[column]) for column in columns) + " |"
        for _, row in display.iterrows()
    )
    return "\n".join(lines)


def generate_report(
    table: pd.DataFrame,
    decoder: pd.DataFrame,
    tree_gains: pd.DataFrame,
    connectivity: pd.DataFrame,
    exact_tradeoff: pd.DataFrame,
    non_tied: pd.DataFrame,
    gate: pd.DataFrame,
    validation: pd.DataFrame,
    scaling: pd.DataFrame,
    output: Path,
) -> None:
    decision = gate.iloc[0]
    primary = table[
        (table["scope"] == "overall")
        & (table["q_mode"] == "estimated_q")
    ][
        [
            "tree_source",
            "q_mode",
            "decoder",
            "mean_test_hamming",
            "mean_hamming_minus_binary",
            "hamming_difference_ci_lower",
            "hamming_difference_ci_upper",
            "mean_exact_row_recovery",
            "mean_clean_f1",
            "mean_posterior_expected_hamming",
            "mean_risk_calibration_gap",
            "mean_risk_row_correlation",
            "median_connected_fraction",
            "mean_total_inference_runtime_seconds",
        ]
    ]
    major = primary[
        primary["tree_source"].isin(
            ["GeneratingTreeOracle", "BinaryMWST", "EstimatedQMarginalTree"]
        )
    ]
    major_both_q = table[
        (table["scope"] == "overall")
        & (table["decoder"] == "ConnectedBayesHamming")
        & table["tree_source"].isin(
            ["GeneratingTreeOracle", "BinaryMWST", "EstimatedQMarginalTree"]
        )
    ][
        [
            "tree_source",
            "q_mode",
            "mean_test_hamming",
            "mean_hamming_minus_binary",
            "hamming_difference_ci_lower",
            "hamming_difference_ci_upper",
            "mean_posterior_expected_hamming",
            "mean_risk_calibration_gap",
        ]
    ]
    topology_gain = tree_gains[
        (tree_gains["scope"] != "overall")
        & (tree_gains["q_mode"] == "estimated_q")
        & (tree_gains["decoder"] == "ConnectedBayesHamming")
    ][["scope", "mean_tree_gain", "ci_lower", "ci_upper"]]
    major_decoder = decoder[
        (decoder["scope"] == "overall")
        & (decoder["q_mode"] == "estimated_q")
        & decoder["tree_source"].isin(
            ["GeneratingTreeOracle", "BinaryMWST", "EstimatedQMarginalTree"]
        )
    ][["tree_source", "mean_effect", "ci_lower", "ci_upper"]]
    major_connectivity = connectivity[
        (connectivity["scope"] == "overall")
        & (connectivity["q_mode"] == "estimated_q")
        & connectivity["tree_source"].isin(
            ["GeneratingTreeOracle", "BinaryMWST", "EstimatedQMarginalTree"]
        )
    ][["effect_name", "tree_source", "mean_effect", "ci_lower", "ci_upper"]]
    exact = exact_tradeoff[
        (exact_tradeoff["scope"] == "overall")
        & (exact_tradeoff["q_mode"] == "estimated_q")
        & exact_tradeoff["tree_source"].isin(
            ["GeneratingTreeOracle", "BinaryMWST", "EstimatedQMarginalTree"]
        )
    ][["tree_source", "mean_effect", "ci_lower", "ci_upper"]]
    validation_summary = pd.DataFrame(
        [
            {
                "posterior rows": validation["row_comparisons"].sum(),
                "marginal entries": validation["marginal_entry_comparisons"].sum(),
                "marginal mismatches": validation["marginal_row_mismatches"].sum(),
                "max marginal error": validation["max_marginal_absolute_error"].max(),
                "max normalization error": validation["max_posterior_normalization_error"].max(),
                "MAP mismatches": validation["map_action_mismatches"].sum(),
                "median mismatches": validation["median_action_mismatches"].sum(),
                "connected MBR mismatches": validation["connected_action_mismatches"].sum(),
                "max root error": validation["max_root_invariance_error"].max(),
            }
        ]
    )
    star = table[
        (table["scope"] == "star")
        & (table["q_mode"] == "estimated_q")
        & table["tree_source"].isin(
            ["GeneratingTreeOracle", "BinaryMWST", "EstimatedQMarginalTree"]
        )
    ][["tree_source", "decoder", "mean_test_hamming", "mean_risk_calibration_gap"]]
    median = major[major["decoder"] == "PosteriorMedianUnconstrained"]
    alpha_median = table[
        (table["scope"] != "overall")
        & (table["tree_source"] == "GeneratingTreeOracle")
        & (table["q_mode"] == "oracle_q")
        & (table["decoder"] == "PosteriorMedianUnconstrained")
    ][
        [
            "scope",
            "mean_test_hamming",
            "median_empty_fraction",
            "median_disconnected_fraction",
        ]
    ]
    alpha_cost = connectivity[
        (connectivity["scope"] != "overall")
        & (connectivity["tree_source"] == "GeneratingTreeOracle")
        & (connectivity["q_mode"] == "oracle_q")
        & (connectivity["effect_name"] == "ConnectivityCost_empirical")
    ][["scope", "mean_effect"]].rename(
        columns={"mean_effect": "empirical_connectivity_cost"}
    )
    alpha_diagnostics = alpha_median.merge(alpha_cost, on="scope")
    calibration = major[major["decoder"] == "ConnectedBayesHamming"][
        [
            "tree_source",
            "mean_posterior_expected_hamming",
            "mean_test_hamming",
            "mean_risk_calibration_gap",
            "mean_risk_row_correlation",
        ]
    ]
    non_tied_primary = non_tied[non_tied["scope"] == "overall"]
    best_topology = topology_gain.loc[topology_gain["mean_tree_gain"].idxmax()]
    worst_topology = topology_gain.loc[topology_gain["mean_tree_gain"].idxmin()]

    recommendations = {
        "A": "Freeze BinaryMWST as the k=1 tree component. Retain exact posterior inference as infrastructure, but require a real application and loss model before expanding this line.",
        "B": "Do not implement a neural subtree prior yet. First identify observable row covariates X_i in a real application and a shared parameterization of P_theta(S_i|X_i,T) that can transfer to unseen vertices instead of fitting per-instance free parameters. Exact posterior decoding remains available only if the conditioned prior preserves a tractable tree factorization. A proposal must name the real task and its loss before choosing features or a model class.",
        "C": "Reassess the observable variables, noise mechanism, and calibration of the subtree posterior before any learned structure method. Do not tune the decoder around a misspecified posterior.",
        "D": "Prepare one bounded proposal for feature-conditioned subtree-prior learning with exact fixed-tree posterior decoding; do not implement a neural tree learner in this phase.",
        "E": "Identify whether real outputs must be connected on one join tree and compare application-grounded losses before considering any wider GHW class.",
        "F": "Keep the empirical audit, cite constrained centroid/MEA decoding, and redirect novelty claims to an application-level statistical question.",
    }

    text = f"""# AHSL Phase A1.5 Research Report

## 1. Research question

Does exact Hamming-risk-aligned posterior decoding reveal a robust advantage of
EstimatedQMarginalTree over BinaryMWST on the frozen A1 primary datasets?

## 2. Literature review

The focused search screened 18 primary works and read 8 in detail. Bayesian
decision theory, posterior decoding, generalized centroid/MEA estimation,
sum-product differentiation, connected-subtree optimization, and posterior
misspecification were covered. The literature gate was **GO**, with an explicit
restriction against claiming the decoder as a novel MBR construction.
The three closest concepts are Carvalho and Lawrence's posterior centroid,
Hamada et al.'s generalized centroid/MEA decoder with structural constraints,
and Lember and Koloydenko's risk-based admissible HMM decoding.

## 3. Decision-theory correction

Posterior MAP minimizes exact-support 0-1 loss, not nodewise Hamming. The
coordinate posterior median minimizes unconstrained Hamming. Within nonempty
connected supports, Hamming Bayes risk equals a constant minus the sum of
weights `2*pi_j-1`, so ConnectedBayesHamming is the exact constrained action.

## 4. Posterior marginal derivation

The A1 log-sum-product likelihood circuit is differentiated analytically in one
reverse pass. The derivative of log evidence with respect to the included-state
local field is `P(X_j=1|Y,T,q)`.

## 5. Exact validation

{_markdown(validation_summary, 12)}

All decision mismatches were zero, including explicit q=0/q=1, zero-noise,
asymmetric-noise, and repeated-observation cases.

## 6. Complexity

All node marginals cost O(m) per row and O(nm) per batch. Measured scaling:

{_markdown(scaling, 7)}

## 7. Experimental protocol

The deterministic A1 convention was reused exactly: n=300, m=16, q=0.4,
symmetric 0.20 noise, R=1, four topology families, seeds 0--29, and a
60/20/20 row split. No new tree estimator or broader statistical grid was
introduced. Oracle-q and deployable estimated-q tracks were kept separate.

## 8. MAP results

Deployable estimated-q major-tree results are contained below.

{_markdown(major[major['decoder'] == 'PosteriorMAPConnected'])}

## 9. Unconstrained posterior-median results

{_markdown(median)}

The median is diagnostic only: empty or disconnected predictions are outside
the frozen connected-output class.

## 10. Connected Bayes-Hamming results

Both q tracks are shown explicitly. OracleQMarginalTree remains an
oracle-assisted tree source even when its fixed tree is rescored with an
estimated q; it is secondary and does not enter the deployable stop rule.

{_markdown(major_both_q)}

## 11. Decoder gain

Positive values mean MAP Hamming minus ConnectedBayesHamming Hamming.

{_markdown(major_decoder)}

## 12. Tree gain under aligned decoder

The preregistered deployable quantity was BinaryMWST Hamming minus
EstimatedQMarginalTree Hamming. Its overall value was
{decision['primary_tree_gain']:.5f}, with paired 95% CI
[{decision['primary_ci_lower']:.5f}, {decision['primary_ci_upper']:.5f}].

{_markdown(topology_gain)}

The unique/non-tied analysis was:

{_markdown(non_tied_primary)}

## 13. Connectivity cost

Positive empirical cost means the connected constraint worsened realized
Hamming; posterior cost is nonnegative by the Bayes-action definition.

{_markdown(major_connectivity)}

## 14. Posterior risk calibration

The gap is posterior predicted risk minus realized clean Hamming.

{_markdown(calibration)}

## 15. Exact-row versus Hamming tradeoff

Positive values favor MAP exact-row recovery over ConnectedBayesHamming.

{_markdown(exact)}

## 16. Topology analysis

Only {int(decision['topologies_over_0_005'])} topology families exceeded the
required 0.005 TreeGain threshold. The topology-specific paired intervals are
shown in Section 12.

## 17. Star analysis

{_markdown(star)}

Star is reported separately because earlier phases found decoder-sensitive
behavior there; it is not used to override the four-family stop rule.

## 18. Evidence for tree learning

The strongest favorable evidence is {best_topology['scope']} TreeGain
{best_topology['mean_tree_gain']:.5f}, with CI
[{best_topology['ci_lower']:.5f}, {best_topology['ci_upper']:.5f}]. It must
still satisfy the preregistered three-topology, non-tied, q-fairness, and
calibration criteria.

## 19. Evidence against tree learning

The primary stop rule fired: **{bool(decision['tree_stop_rule_fired'])}**. The
overall aligned TreeGain and its lower confidence bound are the controlling
evidence. The strongest adverse topology was {worst_topology['scope']} at
{worst_topology['mean_tree_gain']:.5f}; no additional tree search was attempted.

## 20. Evidence for subtree/posterior modeling

The deployable decoder gains were {decision['generating_decoder_gain']:.5f}
on the generating tree, {decision['binary_decoder_gain']:.5f} on BinaryMWST,
and {decision['estimated_marginal_decoder_gain']:.5f} on
EstimatedQMarginalTree. These distinguish decision-model value from tree-
identity value.

## 21. Alpha-acyclic warning signals

The wider-alpha warning fired: **{bool(decision['wider_alpha_warning_fired'])}**.
It appeared in {int(decision['alpha_warning_topologies'])} topology families
under GeneratingTreeOracle with oracle q, using the preregistered >0.01 gap and
a documented substantial-disconnection threshold of 0.10.

{_markdown(alpha_diagnostics)}

## 22. Literature novelty assessment

ConnectedBayesHamming is an instance of classical constrained centroid/MEA or
MBR decoding: posterior marginals supply additive gains and a combinatorial
optimizer enforces validity. A1.5's value is the falsifiable audit of a specific
tree-learning claim, not a new decision algorithm.

## 23. Stop-rule evaluation

- Mean TreeGain <= 0.005 or CI lower <= 0 or fewer than three positive topology
  families: **{bool(decision['tree_stop_rule_fired'])}**.
- Survives unique/non-tied analysis: **{bool(decision['survives_non_tied'])}**.
- Major-tree posterior risk reasonably calibrated at absolute mean gap <=0.02:
  **{bool(decision['reasonably_calibrated'])}**.
- Full latent-tree continuation condition: **{bool(decision['continuation_condition_met'])}**.

## 24. Final decision

**Decision {decision['final_decision_code']}**

> {decision['final_decision']}

## 25. Recommended next research direction

{recommendations[str(decision['final_decision_code'])]}
"""
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding="utf-8")
