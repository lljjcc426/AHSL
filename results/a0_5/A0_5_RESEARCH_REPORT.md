# AHSL Phase A0.5 Research Report

## 1. Questions and decision scope

Phase A0.5 asks whether exact tree dynamic programming removes the exponential
enumeration bottleneck, whether the observed gain comes from connectedness rather
than the non-empty constraint, how that gain degrades under a wrong tree or
off-class rows, and whether classical maximum-weight spanning-tree (MWST)
recovery already makes learned join-tree estimation unnecessary. This phase does
not claim novelty for the join-tree characterization, MWST criterion, or tree DP.

The saved evidence contains 13,840 result rows. Core, wrong-tree,
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

The official validation covered 600 comparisons across
random, path, star, and balanced trees, split equally among generic weights,
Hamming projection, and noise likelihood. Objective mismatches:
0. Prediction mismatches among unique optima:
0. Tied optima use the fixed policy: maximize objective,
then minimize selected size, then choose the lexicographically smallest node
tuple. This validates the exact solver on small instances; it is not used as a
large-scale smoke test.

| tree_topology | category | comparisons | objective_mismatches | unique_prediction_mismatches |
| --- | --- | --- | --- | --- |
| random | generic_weights | 50 | 0 | 0 |
| random | hamming | 50 | 0 | 0 |
| random | noise_likelihood | 50 | 0 | 0 |
| path | generic_weights | 50 | 0 | 0 |
| path | hamming | 50 | 0 | 0 |
| path | noise_likelihood | 50 | 0 | 0 |
| star | generic_weights | 50 | 0 | 0 |
| star | hamming | 50 | 0 | 0 |
| star | noise_likelihood | 50 | 0 | 0 |
| balanced | generic_weights | 50 | 0 | 0 |
| balanced | hamming | 50 | 0 | 0 |
| balanced | noise_likelihood | 50 | 0 | 0 |

## 4. Complexity and scaling

Both primary DP estimators reached `m=1024` without candidate
enumeration. Mean runtime rises approximately with `n*m`; the normalized
`runtime/(n*m)` stays of the same order at the larger sizes. Absolute Python
timings include data conversion and per-row model bookkeeping, so this is an
empirical scaling check rather than a hardware-independent benchmark.

| model | m | runtime_seconds | runtime_per_nm |
| --- | --- | --- | --- |
| DPNearestConnectedSubtree | 8 | 0.007396 | 1.849e-05 |
| DPNearestConnectedSubtree | 64 | 0.019139 | 5.981e-06 |
| DPNearestConnectedSubtree | 256 | 0.068184 | 5.327e-06 |
| DPNearestConnectedSubtree | 1024 | 0.344386 | 6.726e-06 |
| DPNoiseAwareConnectedMLE | 8 | 0.010768 | 2.692e-05 |
| DPNoiseAwareConnectedMLE | 64 | 0.021945 | 6.858e-06 |
| DPNoiseAwareConnectedMLE | 256 | 0.074783 | 5.842e-06 |
| DPNoiseAwareConnectedMLE | 1024 | 0.372832 | 7.282e-06 |

## 5. Pure structural gain

Observation: relative to the known-noise independent non-empty MLE, the exact
connected MLE reduces mean clean Hamming error by
0.02952, raises exact-row recovery by
0.15269, and has positive Hamming gain in
76.3% of paired cases. The gain is largest at one observation
and under false-positive or symmetric noise; it shrinks as repeated observations
make the likelihood more decisive.

| noise_setting | num_observations | hamming_reduction | exact_gain | f1_gain |
| --- | --- | --- | --- | --- |
| false_negative_only_0.20 | 1 | 0.00613 | 0.05442 | 0.02276 |
| false_negative_only_0.20 | 3 | 0.00028 | 0.00433 | 0.00092 |
| false_negative_only_0.20 | 5 | 0.00002 | 0.00025 | 0.00005 |
| false_positive_only_0.20 | 1 | 0.07809 | 0.29167 | 0.10649 |
| false_positive_only_0.20 | 3 | 0.00213 | 0.05442 | 0.00704 |
| false_positive_only_0.20 | 5 | 0.00008 | 0.00258 | 0.00032 |
| symmetric_0.10 | 1 | 0.02592 | 0.24900 | 0.04593 |
| symmetric_0.10 | 3 | 0.01559 | 0.22008 | 0.04574 |
| symmetric_0.10 | 5 | 0.00576 | 0.08875 | 0.01803 |
| symmetric_0.20 | 1 | 0.04788 | 0.14742 | 0.04181 |
| symmetric_0.20 | 3 | 0.04453 | 0.33692 | 0.09588 |
| symmetric_0.20 | 5 | 0.03128 | 0.33633 | 0.08323 |
| symmetric_0.30 | 1 | 0.05795 | 0.05833 | 0.01751 |
| symmetric_0.30 | 3 | 0.06654 | 0.17358 | 0.07516 |
| symmetric_0.30 | 5 | 0.06070 | 0.27225 | 0.09938 |

Interpretation: a real structural denoising effect exists in the tested known-tree
regime, but it is not uniform over noise, repetition count, or topology.

## 6. Non-empty constraint versus connectivity

Observation: enforcing only non-emptiness contributes essentially zero Hamming
gain in false-positive and symmetric settings and can be slightly harmful under
false-negative noise because the unconstrained likelihood may correctly choose
an all-zero row under the realized sample. The material difference in Section 5
therefore comes from connectedness, not merely from excluding the empty set.

| noise_setting | num_observations | hamming_reduction |
| --- | --- | --- |
| false_negative_only_0.20 | 1 | -0.005422 |
| false_negative_only_0.20 | 3 | -0.000224 |
| false_negative_only_0.20 | 5 | -0.000016 |
| false_positive_only_0.20 | 1 | 0.000000 |
| false_positive_only_0.20 | 3 | 0.000000 |
| false_positive_only_0.20 | 5 | 0.000000 |
| symmetric_0.10 | 1 | -0.000495 |
| symmetric_0.10 | 3 | -0.000333 |
| symmetric_0.10 | 5 | -0.000047 |
| symmetric_0.20 | 1 | -0.000167 |
| symmetric_0.20 | 3 | -0.000359 |
| symmetric_0.20 | 5 | -0.000266 |
| symmetric_0.30 | 1 | -0.000031 |
| symmetric_0.30 | 3 | -0.000177 |
| symmetric_0.30 | 5 | -0.000240 |

## 7. Generator-prior oracle gap

The generator-prior connected MAP oracle improves over the uniform-prior
connected MLE by 0.01465 Hamming error and
0.03298 exact-row recovery overall. This is an
oracle diagnostic: it uses the true synthetic generation probability and does
not constitute a deployable estimator.

| tree_topology | hamming_reduction | exact_gain |
| --- | --- | --- |
| balanced | 0.01289 | 0.03000 |
| path | 0.00496 | 0.00744 |
| random | 0.01218 | 0.02067 |
| star | 0.02859 | 0.07381 |

Interpretation: prior misspecification leaves measurable headroom, especially on
stars, but the oracle gap is smaller than the main connectedness gain.

## 8. Wrong-tree robustness and crossover

No aggregate crossover was observed in the tested range. Mean Hamming reduction
falls from 0.06092 for the true tree to
0.03578 for an independent random tree, whose
mean labeled-edge disagreement is
0.969. This is robustness within the
tested distribution, not a guarantee beyond it.

| tree_source | requested_tree_swaps | actual_edge_disagreement | hamming_reduction |
| --- | --- | --- | --- |
| true_tree | 0 | 0.00000 | 0.06092 |
| swaps_1 | 1 | 0.01587 | 0.06051 |
| swaps_2 | 2 | 0.03122 | 0.05994 |
| swaps_4 | 4 | 0.06190 | 0.05901 |
| swaps_8 | 8 | 0.12103 | 0.05763 |
| independent_random | -1 | 0.96865 | 0.03578 |

The topology-specific exception is decisive: star instances are already harmful
with the true tree (mean gain -0.00621)
and remain harmful for a random tree
(-0.03108).
Thus their crossover occurs before tree misspecification begins.

## 9. Off-class contamination and crossover

No aggregate crossover was observed through requested contamination 0.40. The
actual mean off-class row fraction reaches only
0.240, because contamination is
applied only to eligible rows. The connected gain decreases modestly from
0.06218 to
0.05822.

| requested_offclass_fraction | actual_offclass_fraction | hamming_reduction | exact_gain |
| --- | --- | --- | --- |
| 0.00 | 0.00000 | 0.06218 | 0.33625 |
| 0.05 | 0.02958 | 0.06180 | 0.31692 |
| 0.10 | 0.06483 | 0.06099 | 0.29917 |
| 0.20 | 0.12008 | 0.06049 | 0.27233 |
| 0.40 | 0.23967 | 0.05822 | 0.21708 |

Stars again remain slightly harmful throughout (gain range
-0.00359
to -0.00344).

## 10. Topology dependence

| tree_topology | hamming_reduction | exact_gain | positive_case_fraction |
| --- | --- | --- | --- |
| balanced | 0.03454 | 0.16313 | 0.844 |
| path | 0.04333 | 0.19671 | 0.838 |
| random | 0.03633 | 0.17731 | 0.840 |
| star | 0.00389 | 0.07360 | 0.531 |

Path, random, and balanced trees show consistent aggregate benefits. Stars do
not: at symmetric noise 0.30 their mean gain is
-0.00134. A star has exponentially many
connected subtrees containing its center and a strong combinatorial asymmetry;
the constraint can therefore favor large false-positive-supported subtrees.
Any next phase must treat star-like degree concentration as a prespecified
failure region, not average it away.

## 11. Tie behavior

| model | optimal_tie_fraction |
| --- | --- |
| DPNearestConnectedSubtree | 0.1947 |
| DPNoiseAwareConnectedMLE | 0.1765 |
| GeneratorPriorConnectedMAP | 0.1684 |
| NoiseAwareIndependentNonemptyMLE | 0.0098 |
| NoiseAwareIndependentMLE | 0.0000 |

Ties are common enough that exact recovery and F1 can depend on a canonical
choice even when the objective is identical. All A0.5 exact estimators use the
same minimum-size-then-lexicographic policy. Tie frequency is reported rather
than interpreted as estimator uncertainty.

## 12. Classical MWST gate

On simple hypergraphs, MWST from the clean incidence recovers a valid join tree
in every tested case and matches the generating tree here. With one noisy
observation, observed-majority and independent-MLE incidence both yield valid
join trees only 23.3% of the time; at three observations this rises to 40.0%.

| tree_source | num_observations | valid_join_tree_rate | clean_riv | tree_edge_disagreement | hamming_error | exact_row_recovery |
| --- | --- | --- | --- | --- | --- | --- |
| clean_oracle | 1 | 1.000 | 0.000 | 0.00000 | 0.15436 | 0.17078 |
| clean_oracle | 3 | 1.000 | 0.000 | 0.00000 | 0.06036 | 0.50769 |
| independent_mle | 1 | 0.233 | 63.075 | 0.32778 | 0.18308 | 0.09828 |
| independent_mle | 3 | 0.400 | 10.575 | 0.07278 | 0.06415 | 0.47589 |
| observed_majority | 1 | 0.233 | 63.075 | 0.32778 | 0.18308 | 0.09828 |
| observed_majority | 3 | 0.400 | 10.575 | 0.07278 | 0.06415 | 0.47589 |
| true_tree | 1 | 1.000 | 0.000 | 0.00000 | 0.15436 | 0.17078 |
| true_tree | 3 | 1.000 | 0.000 | 0.00000 | 0.06036 | 0.50769 |

Relative to the true-tree connected estimator, noisy-incidence MWST has the
following downstream shortfall:

| num_observations | hamming_excess | hamming_excess_sd | exact_shortfall |
| --- | --- | --- | --- |
| 1 | 0.02872 | 0.02084 | 0.07250 |
| 3 | 0.00379 | 0.00418 | 0.03181 |

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

**Proceed to A1 neural/learned join-tree research**

Reason: the A0.5 structural hypothesis survives in three of four tested topology
families, exact inference is no longer the bottleneck, and classical MWST has a
material `R=1` recovery gap. The recommendation is scoped, not unconditional:
MWST must remain the mandatory baseline, and star-like degree concentration is a
prespecified abstention/stop condition. If a learned method cannot beat MWST in
paired downstream Hamming error at `R=1`, or if its aggregate gain comes from
masking the star failure, A1 should stop rather than expand model complexity.

## 17. Exact next experiment

Run one controlled A1 comparison on the same simple-hypergraph generator at
`n=300, m=16`, symmetric noise 0.20, `R in {1, 3}`, 30 paired seeds, and the
same four topology families. Compare: clean-oracle MWST, noisy-incidence MWST,
an uncertainty-weighted structured spanning-tree estimator, and one learned
edge-scoring estimator followed by the same deterministic maximum-spanning-tree
decoder. Freeze the downstream `DPNoiseAwareConnectedMLE` and all data splits.
Primary endpoint: paired clean Hamming error at `R=1`; secondary endpoints:
valid-join-tree rate, clean RIV, edge disagreement, exact-row recovery, and the
star-specific endpoint reported separately. Proceed beyond this experiment only
if the learned estimator beats noisy MWST without worsening the star endpoint.
