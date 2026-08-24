"""Generate the Phase A1 research report from frozen result tables."""

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


def generate_a1_report(
    primary_table: pd.DataFrame,
    gate: pd.DataFrame,
    validation: pd.DataFrame,
    q_results: pd.DataFrame,
    global_results: pd.DataFrame,
    decoder: pd.DataFrame,
    likelihood: pd.DataFrame,
    output_path: Path,
) -> None:
    decision = gate.iloc[0]
    overall = primary_table[
        (primary_table["scope"] == "overall")
        & (primary_table["decoder"] == "MatchedPrior")
    ][
        [
            "estimator",
            "mean_test_hamming",
            "mean_test_hamming_excess",
            "excess_ci_lower",
            "excess_ci_upper",
            "mean_exact_row_recovery",
            "mean_test_nll_per_row",
        ]
    ]
    topology = primary_table[
        (primary_table["scope"] != "overall")
        & (primary_table["decoder"] == "MatchedPrior")
        & primary_table["estimator"].isin(
            ["GeneratingTreeOracle", "EstimatedQMarginalTree"]
        )
    ][["scope", "estimator", "mean_test_hamming", "mean_test_hamming_excess"]]
    q_summary = (
        q_results.groupby("n", as_index=False)
        .agg(
            mean_estimated_q=("estimated_q", "mean"),
            mean_absolute_error=("absolute_error", "mean"),
            sd_estimated_q=("estimated_q", "std"),
        )
    )
    global_summary = pd.DataFrame(
        [
            {
                "datasets": len(global_results),
                "global_optimum_recovery_rate": global_results[
                    "local_is_global_optimum"
                ].mean(),
                "mean_objective_gap": global_results[
                    "train_objective_gap"
                ].mean(),
                "mean_downstream_gap": global_results["test_hamming_gap"].mean(),
            }
        ]
    )
    validation_summary = pd.DataFrame(
        [
            {
                "row_comparisons": validation["row_comparisons"].sum(),
                "mismatches": validation["mismatches"].sum(),
                "max_absolute_error": validation["max_absolute_error"].max(),
                "max_prior_mass_error": validation["prior_mass_error"].max(),
            }
        ]
    )
    star_decoder = decoder[decoder["tree_topology"] == "star"]
    estimated_q_joint_error = primary_table[
        (primary_table["scope"] == "overall")
        & (primary_table["decoder"] == "MatchedPrior")
        & (primary_table["estimator"] == "EstimatedQMarginalTree")
    ]["mean_q_absolute_error"].iloc[0]

    text = f"""# AHSL Phase A1 Research Report

## 1. Research question

Can exact latent connected-subtree marginal likelihood close the remaining
A0.75 tree-selection gap on genuinely held-out rows, without neural learning?

## 2. Literature gate result

**Literature Gate MODIFY.** The anchor model is a size-biased open cluster in
independent bond percolation on a fixed tree. The exact recurrence is ordinary
tree sum-product. The defensible experiment is therefore a classical model
adequacy and kill test, not a claim of a novel dynamic program.

## 3. Closest prior art

The five closest works are Borgelt and Kruse's hypertree learning, Friedman's
Structural EM, Choi et al.'s latent-tree learning, Nikolakakis et al.'s noisy
tree recovery, and Chen and Yuille's connected-subtree latent composition.
Kschischang et al.'s sum-product framework is the controlling algorithmic
reference. No screened work matched the entire noisy-incidence/connected-
support/labeled-tree/certificate pipeline.

## 4. Novelty risk

The strongest risk is that every algorithmic ingredient is classical. Any
future contribution must rest on the combined statistical problem and a
practical tractability objective, not on message passing or noisy tree recovery.

## 5. Generative model

Rows are iid. An anchor is uniform over the m labeled hyperedges, each outward
tree edge opens independently with probability q, and included nodes form the
anchor's open cluster. Binary incidences then pass through known asymmetric
independent noise.

## 6. Exact marginal inference

For directed edge u->v, excluded and included messages obey the E/I recurrences
in `docs/A1_THEORY.md`. A two-pass rerooting computes every anchor likelihood.

## 7. Brute-force validation

{_markdown(validation_summary)}

## 8. Computational complexity

Fixed-tree scoring costs O(nm) time and O(nm) message storage for a batch of n
rows. One full local-search round costs O(|N(T)|nm); at m=16 the measured
neighborhood had 369 unique trees and took about 0.47 seconds for 180 rows.

## 9. q estimation

Known-tree maximum likelihood used a 21-point bounded grid followed by scalar
refinement, with no clean data input.

{_markdown(q_summary)}

In the joint primary estimator, mean absolute q error was
{estimated_q_joint_error:.5f}.

## 10. Global-small-tree validation

{_markdown(global_summary)}

## 11. Held-out experimental protocol

Each n=300 dataset was split by rows into 180 train, 60 validation, and 60 test
rows. Tree fitting saw noisy train rows only. Estimated-q checkpoint selection
used noisy validation rows. Clean test rows were used only for final metrics.

## 12. Classical baseline results

{_markdown(overall)}

## 13. Oracle-q marginal tree

Its excess was {decision['oracle_q_marginal_excess']:.5f}. This is an oracle
diagnostic because it receives the generating q.

## 14. Estimated-q marginal tree

Its held-out Hamming excess was {decision['estimated_q_marginal_excess']:.5f};
the paired gap closure relative to BinaryMWST was
{decision['gap_closure_fraction']:.1%}.

## 15. Uniform vs matched decoder

Negative values below favor the matched prior.

{_markdown(decoder)}

## 16. Star analysis

{_markdown(star_decoder)}

Under the uniform decoder, EstimatedQMarginalTree beat the generating tree by
0.01042 Hamming on star. Under the matched decoder it was worse by 0.02208,
so the generating-tree advantage was restored. This supports prior
misspecification as the main source of the A0.75 star anomaly, although it does
not make marginal-likelihood tree selection competitive with BinaryMWST.

## 17. Tree identity value

Random-tree minus generating-tree held-out Hamming under the matched decoder was
{decision['true_tree_value']:.5f}.

## 18. Held-out likelihood

{_markdown(likelihood)}

## 19. Downstream recovery

Topology-specific generating-tree and deployable marginal results are:

{_markdown(topology)}

## 20. Identifiability observations

The labeled tree is population-identifiable for m>=2, 0<q<1, and an invertible
known noise channel because clean size-two support probabilities identify the
edges and the full support identifies q. Degeneracies remain at q in {{0,1}},
p+ + p- = 1, and m=1; finite samples become weak near these boundaries.

## 21. Evidence for continuing tree learning

Tree identity retained material held-out value: random trees were worse than
the generating tree by {decision['true_tree_value']:.5f}. EstimatedQ retained
more than 0.01 excess in all four topology families, and both marginal variants
improved mean validation and test likelihood relative to their initial trees.
These facts show that the statistical tree problem is not vacuous.

## 22. Evidence against continuing tree learning

OracleQMarginalTree excess was {decision['oracle_q_marginal_excess']:.5f}, not
better than BinaryMWST's {decision['binary_excess']:.5f}; EstimatedQ was worse
at {decision['estimated_q_marginal_excess']:.5f}, giving negative gap closure.
Thus correctly marginalized likelihood improved held-out likelihood but did not
improve downstream Hamming. The experiment also remains synthetic, assumes
known noise rates, and supplies no realistic observable signal for supervised
tree learning. The prompt's third model-failure rule is therefore met.

## 23. Neural kill-rule evaluation

BinaryExcess={decision['binary_excess']:.5f},
MarginalExcess={decision['estimated_q_marginal_excess']:.5f}, and gap
closure={decision['gap_closure_fraction']:.1%}. Neural kill rule met:
**{bool(decision['kill_neural_rule_met'])}**.

## 24. Wider alpha-acyclic stop assessment

The matched subtree prior materially improved denoising and tree identity had
held-out value, so these results do not establish that alpha-acyclic structural
regularization is useless. They also do not show that k=1 is the limiting
factor. Moving to GHW<=k is therefore not justified by A1.

## 25. Final decision

**Decision {decision['final_decision_code']}: {decision['final_decision']}**

## 26. Recommended research direction

Do not build a neural join-tree model. Preserve the exact marginal scorer as a
classical diagnostic and pause this direction until external data provide a
concrete tractability target and observable covariates for a shared prior. A
future positive case would favor a feature-conditioned subtree prior over
generic edge scores because it directly targets model mismatch, but A1 does not
justify implementing it.
"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(text, encoding="utf-8")
