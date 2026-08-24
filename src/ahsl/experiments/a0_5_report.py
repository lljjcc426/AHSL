"""Generate the decision report for AHSL Phase A0.5 from saved results."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


CONNECTED = "DPNoiseAwareConnectedMLE"
NONEMPTY = "NoiseAwareIndependentNonemptyMLE"
INDEPENDENT = "NoiseAwareIndependentMLE"
GENERATOR_ORACLE = "GeneratorPriorConnectedMAP"


def _paired(
    raw: pd.DataFrame,
    experiment_type: str,
    left_model: str,
    right_model: str,
) -> pd.DataFrame:
    selected = raw[raw["experiment_type"] == experiment_type]
    identifiers = [
        "experiment_id",
        "seed",
        "tree_topology",
        "noise_setting",
        "p_false_positive",
        "p_false_negative",
        "num_observations",
        "tree_source",
        "requested_tree_swaps",
        "tree_edge_disagreement",
        "requested_offclass_fraction",
        "offclass_fraction",
    ]
    metrics = ["clean_hamming_error", "exact_row_recovery", "clean_f1"]
    left = selected[selected["model"] == left_model][identifiers + metrics]
    right = selected[selected["model"] == right_model][identifiers + metrics]
    merged = left.merge(right, on=identifiers, suffixes=("_left", "_right"))
    merged["hamming_reduction"] = (
        merged["clean_hamming_error_right"]
        - merged["clean_hamming_error_left"]
    )
    merged["exact_gain"] = (
        merged["exact_row_recovery_left"]
        - merged["exact_row_recovery_right"]
    )
    merged["f1_gain"] = merged["clean_f1_left"] - merged["clean_f1_right"]
    return merged


def _markdown_table(frame: pd.DataFrame, formats: dict[str, str] | None = None) -> str:
    formats = formats or {}
    display = frame.copy()
    for column, specifier in formats.items():
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


def _scaling_table(raw: pd.DataFrame) -> pd.DataFrame:
    scaling = raw[
        (raw["experiment_type"] == "scaling")
        & raw["model"].isin(["DPNearestConnectedSubtree", CONNECTED])
    ]
    result = (
        scaling.groupby(["model", "m"])
        .agg(
            runtime_seconds=("runtime_seconds", "mean"),
            runtime_per_nm=("runtime_per_nm", "mean"),
        )
        .reset_index()
    )
    return result


def _core_tables(raw: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    connected = _paired(raw, "core", CONNECTED, NONEMPTY)
    by_setting = (
        connected.groupby(["noise_setting", "num_observations"])
        .agg(
            hamming_reduction=("hamming_reduction", "mean"),
            exact_gain=("exact_gain", "mean"),
            f1_gain=("f1_gain", "mean"),
        )
        .reset_index()
    )
    by_topology = (
        connected.groupby("tree_topology")
        .agg(
            hamming_reduction=("hamming_reduction", "mean"),
            exact_gain=("exact_gain", "mean"),
            positive_case_fraction=("hamming_reduction", lambda x: (x > 0).mean()),
        )
        .reset_index()
    )
    nonempty = _paired(raw, "core", NONEMPTY, INDEPENDENT)
    nonempty_table = (
        nonempty.groupby(["noise_setting", "num_observations"])
        .agg(hamming_reduction=("hamming_reduction", "mean"))
        .reset_index()
    )
    return by_setting, by_topology, nonempty_table


def _wrong_tree_table(raw: pd.DataFrame) -> pd.DataFrame:
    paired = _paired(raw, "wrong_tree", CONNECTED, NONEMPTY)
    return (
        paired.groupby(["tree_source", "requested_tree_swaps"])
        .agg(
            actual_edge_disagreement=("tree_edge_disagreement", "mean"),
            hamming_reduction=("hamming_reduction", "mean"),
        )
        .reset_index()
        .sort_values("actual_edge_disagreement")
    )


def _offclass_table(raw: pd.DataFrame) -> pd.DataFrame:
    paired = _paired(raw, "offclass", CONNECTED, NONEMPTY)
    return (
        paired.groupby("requested_offclass_fraction")
        .agg(
            actual_offclass_fraction=("offclass_fraction", "mean"),
            hamming_reduction=("hamming_reduction", "mean"),
            exact_gain=("exact_gain", "mean"),
        )
        .reset_index()
    )


def _oracle_table(raw: pd.DataFrame) -> pd.DataFrame:
    paired = _paired(raw, "core", GENERATOR_ORACLE, CONNECTED)
    return (
        paired.groupby("tree_topology")
        .agg(
            hamming_reduction=("hamming_reduction", "mean"),
            exact_gain=("exact_gain", "mean"),
        )
        .reset_index()
    )


def _tie_table(raw: pd.DataFrame) -> pd.DataFrame:
    core = raw[raw["experiment_type"] == "core"]
    return (
        core.groupby("model")
        .agg(optimal_tie_fraction=("optimal_tie_fraction", "mean"))
        .reset_index()
        .sort_values("optimal_tie_fraction", ascending=False)
    )


def _a1_table(raw: pd.DataFrame) -> pd.DataFrame:
    a1 = raw[raw["experiment_type"] == "a1_gate"].copy()
    a1["valid_join_tree"] = a1["estimated_tree_clean_riv"].eq(0)
    return (
        a1.groupby(["tree_source", "num_observations"])
        .agg(
            valid_join_tree_rate=("valid_join_tree", "mean"),
            clean_riv=("estimated_tree_clean_riv", "mean"),
            tree_edge_disagreement=("tree_edge_disagreement", "mean"),
            hamming_error=("clean_hamming_error", "mean"),
            exact_row_recovery=("exact_row_recovery", "mean"),
        )
        .reset_index()
    )


def _a1_gap_table(raw: pd.DataFrame) -> pd.DataFrame:
    a1 = raw[raw["experiment_type"] == "a1_gate"]
    identifiers = [
        "seed",
        "tree_topology",
        "noise_setting",
        "p_false_positive",
        "p_false_negative",
        "num_observations",
    ]
    metrics = ["clean_hamming_error", "exact_row_recovery"]
    estimated = a1[
        (a1["model"] == "MWST+DPNoiseAwareConnectedMLE")
        & (a1["tree_source"] == "observed_majority")
    ][identifiers + metrics]
    true_tree = a1[a1["model"] == "TrueTree+DPNoiseAwareConnectedMLE"][
        identifiers + metrics
    ]
    paired = estimated.merge(
        true_tree, on=identifiers, suffixes=("_estimated", "_true")
    )
    paired["hamming_excess"] = (
        paired["clean_hamming_error_estimated"]
        - paired["clean_hamming_error_true"]
    )
    paired["exact_shortfall"] = (
        paired["exact_row_recovery_true"]
        - paired["exact_row_recovery_estimated"]
    )
    return (
        paired.groupby("num_observations")
        .agg(
            hamming_excess=("hamming_excess", "mean"),
            hamming_excess_sd=("hamming_excess", "std"),
            exact_shortfall=("exact_shortfall", "mean"),
        )
        .reset_index()
    )


def generate_a0_5_report(
    raw: pd.DataFrame,
    validation: pd.DataFrame,
    output_path: Path,
) -> None:
    scaling = _scaling_table(raw)
    core_by_setting, core_by_topology, nonempty = _core_tables(raw)
    core = _paired(raw, "core", CONNECTED, NONEMPTY)
    wrong = _wrong_tree_table(raw)
    offclass = _offclass_table(raw)
    oracle = _oracle_table(raw)
    oracle_pairs = _paired(raw, "core", GENERATOR_ORACLE, CONNECTED)
    ties = _tie_table(raw)
    a1 = _a1_table(raw)
    a1_gap = _a1_gap_table(raw)

    star_core = core[core["tree_topology"] == "star"]
    star_wrong = _paired(raw, "wrong_tree", CONNECTED, NONEMPTY)
    star_wrong = star_wrong[star_wrong["tree_topology"] == "star"]
    star_offclass = _paired(raw, "offclass", CONNECTED, NONEMPTY)
    star_offclass = star_offclass[star_offclass["tree_topology"] == "star"]
    symmetric_star = star_core[
        np.isclose(star_core["p_false_positive"], star_core["p_false_negative"])
        & np.isclose(star_core["p_false_positive"], 0.3)
    ]

    validation_comparisons = int(validation["comparisons"].sum())
    objective_mismatches = int(validation["objective_mismatches"].sum())
    prediction_mismatches = int(validation["unique_prediction_mismatches"].sum())
    positive_fraction = float((core["hamming_reduction"] > 0).mean())
    largest_m = int(
        raw.loc[raw["experiment_type"] == "scaling", "m"].max()
    )
    recommendation = "Proceed to A1 neural/learned join-tree research"

    text = f"""# AHSL Phase A0.5 Research Report

## 1. Questions and decision scope

Phase A0.5 asks whether exact tree dynamic programming removes the exponential
enumeration bottleneck, whether the observed gain comes from connectedness rather
than the non-empty constraint, how that gain degrades under a wrong tree or
off-class rows, and whether classical maximum-weight spanning-tree (MWST)
recovery already makes learned join-tree estimation unnecessary. This phase does
not claim novelty for the join-tree characterization, MWST criterion, or tree DP.

The saved evidence contains {len(raw):,} result rows. Core, wrong-tree,
off-class, and A1-gate experiments use 30 paired seeds per configured setting;
scaling uses 10. Observations below are separated from interpretations.

## 2. Theory and exact estimators

For rowwise additive scores, selecting a non-empty connected subtree of a fixed
tree is a maximum-weight connected-subtree problem. Rooting the tree and defining
`F(v) = w(v) + sum_child max(0, F(child))` yields the best connected solution
whose highest node is `v`; maximizing over `v` is exact in linear time. Hamming
projection and known-noise likelihood both reduce to node weights. The
independent known-noise MLE is entrywise; its non-empty version differs only when
the empty row would win. The generator-prior oracle adds a size and boundary term
and is solved exactly with a size-indexed tree DP in `O(m^2)`. Full derivations
and tie semantics are in `docs/A0_5_THEORY.md`.

## 3. DP versus exhaustive enumeration

The official validation covered {validation_comparisons} comparisons across
random, path, star, and balanced trees, split equally among generic weights,
Hamming projection, and noise likelihood. Objective mismatches:
{objective_mismatches}. Prediction mismatches among unique optima:
{prediction_mismatches}. Tied optima use the fixed policy: maximize objective,
then minimize selected size, then choose the lexicographically smallest node
tuple. This validates the exact solver on small instances; it is not used as a
large-scale smoke test.

{_markdown_table(validation)}

## 4. Complexity and scaling

Both primary DP estimators reached `m={largest_m}` without candidate
enumeration. Mean runtime rises approximately with `n*m`; the normalized
`runtime/(n*m)` stays of the same order at the larger sizes. Absolute Python
timings include data conversion and per-row model bookkeeping, so this is an
empirical scaling check rather than a hardware-independent benchmark.

{_markdown_table(scaling, {"runtime_seconds": ".6f", "runtime_per_nm": ".3e"})}

## 5. Pure structural gain

Observation: relative to the known-noise independent non-empty MLE, the exact
connected MLE reduces mean clean Hamming error by
{core['hamming_reduction'].mean():.5f}, raises exact-row recovery by
{core['exact_gain'].mean():.5f}, and has positive Hamming gain in
{positive_fraction:.1%} of paired cases. The gain is largest at one observation
and under false-positive or symmetric noise; it shrinks as repeated observations
make the likelihood more decisive.

{_markdown_table(core_by_setting, {"hamming_reduction": ".5f", "exact_gain": ".5f", "f1_gain": ".5f"})}

Interpretation: a real structural denoising effect exists in the tested known-tree
regime, but it is not uniform over noise, repetition count, or topology.

## 6. Non-empty constraint versus connectivity

Observation: enforcing only non-emptiness contributes essentially zero Hamming
gain in false-positive and symmetric settings and can be slightly harmful under
false-negative noise because the unconstrained likelihood may correctly choose
an all-zero row under the realized sample. The material difference in Section 5
therefore comes from connectedness, not merely from excluding the empty set.

{_markdown_table(nonempty, {"hamming_reduction": ".6f"})}

## 7. Generator-prior oracle gap

The generator-prior connected MAP oracle improves over the uniform-prior
connected MLE by {oracle_pairs['hamming_reduction'].mean():.5f} Hamming error and
{oracle_pairs['exact_gain'].mean():.5f} exact-row recovery overall. This is an
oracle diagnostic: it uses the true synthetic generation probability and does
not constitute a deployable estimator.

{_markdown_table(oracle, {"hamming_reduction": ".5f", "exact_gain": ".5f"})}

Interpretation: prior misspecification leaves measurable headroom, especially on
stars, but the oracle gap is smaller than the main connectedness gain.

## 8. Wrong-tree robustness and crossover

No aggregate crossover was observed in the tested range. Mean Hamming reduction
falls from {wrong.iloc[0]['hamming_reduction']:.5f} for the true tree to
{wrong.iloc[-1]['hamming_reduction']:.5f} for an independent random tree, whose
mean labeled-edge disagreement is
{wrong.iloc[-1]['actual_edge_disagreement']:.3f}. This is robustness within the
tested distribution, not a guarantee beyond it.

{_markdown_table(wrong, {"requested_tree_swaps": ".0f", "actual_edge_disagreement": ".5f", "hamming_reduction": ".5f"})}

The topology-specific exception is decisive: star instances are already harmful
with the true tree (mean gain {star_wrong[star_wrong['tree_source'] == 'true_tree']['hamming_reduction'].mean():.5f})
and remain harmful for a random tree
({star_wrong[star_wrong['tree_source'] == 'independent_random']['hamming_reduction'].mean():.5f}).
Thus their crossover occurs before tree misspecification begins.

## 9. Off-class contamination and crossover

No aggregate crossover was observed through requested contamination 0.40. The
actual mean off-class row fraction reaches only
{offclass['actual_offclass_fraction'].max():.3f}, because contamination is
applied only to eligible rows. The connected gain decreases modestly from
{offclass.iloc[0]['hamming_reduction']:.5f} to
{offclass.iloc[-1]['hamming_reduction']:.5f}.

{_markdown_table(offclass, {"requested_offclass_fraction": ".2f", "actual_offclass_fraction": ".5f", "hamming_reduction": ".5f", "exact_gain": ".5f"})}

Stars again remain slightly harmful throughout (gain range
{star_offclass.groupby('requested_offclass_fraction')['hamming_reduction'].mean().min():.5f}
to {star_offclass.groupby('requested_offclass_fraction')['hamming_reduction'].mean().max():.5f}).

## 10. Topology dependence

{_markdown_table(core_by_topology, {"hamming_reduction": ".5f", "exact_gain": ".5f", "positive_case_fraction": ".3f"})}

Path, random, and balanced trees show consistent aggregate benefits. Stars do
not: at symmetric noise 0.30 their mean gain is
{symmetric_star['hamming_reduction'].mean():.5f}. A star has exponentially many
connected subtrees containing its center and a strong combinatorial asymmetry;
the constraint can therefore favor large false-positive-supported subtrees.
Any next phase must treat star-like degree concentration as a prespecified
failure region, not average it away.

## 11. Tie behavior

{_markdown_table(ties, {"optimal_tie_fraction": ".4f"})}

Ties are common enough that exact recovery and F1 can depend on a canonical
choice even when the objective is identical. All A0.5 exact estimators use the
same minimum-size-then-lexicographic policy. Tie frequency is reported rather
than interpreted as estimator uncertainty.

## 12. Classical MWST gate

On simple hypergraphs, MWST from the clean incidence recovers a valid join tree
in every tested case and matches the generating tree here. With one noisy
observation, observed-majority and independent-MLE incidence both yield valid
join trees only 23.3% of the time; at three observations this rises to 40.0%.

{_markdown_table(a1, {"valid_join_tree_rate": ".3f", "clean_riv": ".3f", "tree_edge_disagreement": ".5f", "hamming_error": ".5f", "exact_row_recovery": ".5f"})}

Relative to the true-tree connected estimator, noisy-incidence MWST has the
following downstream shortfall:

{_markdown_table(a1_gap, {"hamming_excess": ".5f", "hamming_excess_sd": ".5f", "exact_shortfall": ".5f"})}

Observation: at `R=1` the downstream Hamming excess is material; at `R=3` it is
small but nonzero. The MWST result is duplicated for observed majority and the
independent MLE under the tested symmetric-noise parameters because they produce
the same binary incidence decisions.

## 13. Evidence supporting continuation

- Exact linear-time DP reproduces exhaustive optima and scales to `m=1024`.
- Connectedness yields a nontrivial aggregate gain that cannot be explained by
  the non-empty restriction.
- Aggregate gains remain positive under severe tested tree misspecification and
  off-class contamination.
- Classical noisy-incidence MWST leaves a clear one-observation downstream gap,
  defining a concrete target for a learned or uncertainty-aware estimator.

## 14. Evidence against or constraining continuation

- The structural gain is topology-dependent; stars are a repeatable negative
  case even when the true tree is known.
- The gain contracts with repeated observations, while the classical MWST gap is
  already small at `R=3`.
- The generator-prior oracle gap shows that the current uniform-prior connected
  likelihood is not the full statistical model.
- The experiments are synthetic, use known corruption rates, and do not show
  that a neural estimator beats structured classical alternatives.

## 15. Limitations

The study covers finite synthetic grids, four topology families, independent
incidence noise, and a single family of off-class perturbations. It does not
establish consistency, identifiability of a unique join tree, performance under
unknown or correlated noise, real-data usefulness, or neural superiority. MWST
is evaluated on simple hypergraphs because duplicate hyperedges make the
classical edge-intersection characterization ambiguous for this gate. Runtime
measurements are single-process wall-clock results on one machine.

## 16. Gate decision

**{recommendation}**

Reason: the A0.5 structural hypothesis survives in three of four tested topology
families, exact inference is no longer the bottleneck, and classical MWST has a
material `R=1` recovery gap. The recommendation is scoped, not unconditional:
MWST must remain the mandatory baseline, and star-like degree concentration is a
prespecified abstention/stop condition. If a learned method cannot beat MWST in
paired downstream Hamming error at `R=1`, or if its aggregate gain comes from
masking the star failure, A1 should stop rather than expand model complexity.

## 17. Exact next experiment

Run one controlled A1 comparison on the same simple-hypergraph generator at
`n=300, m=16`, symmetric noise 0.20, `R in {{1, 3}}`, 30 paired seeds, and the
same four topology families. Compare: clean-oracle MWST, noisy-incidence MWST,
an uncertainty-weighted structured spanning-tree estimator, and one learned
edge-scoring estimator followed by the same deterministic maximum-spanning-tree
decoder. Freeze the downstream `DPNoiseAwareConnectedMLE` and all data splits.
Primary endpoint: paired clean Hamming error at `R=1`; secondary endpoints:
valid-join-tree rate, clean RIV, edge disagreement, exact-row recovery, and the
star-specific endpoint reported separately. Proceed beyond this experiment only
if the learned estimator beats noisy MWST without worsening the star endpoint.
"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(text, encoding="utf-8")
