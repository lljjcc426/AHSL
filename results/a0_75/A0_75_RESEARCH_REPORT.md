# AHSL Phase A0.75 Research Report

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
has Hamming 0.18308 and downstream excess
0.02872 with 95% CI
[0.02693, 0.03063].

## 5. Noise-corrected MWST

Noise correction lowers excess to 0.01816, a reduction
of 0.01055 relative to BinaryMWST.
It does not reach the true-tree decoder: its upper and lower paired confidence
bounds remain above 0.01.

## 6. Bootstrap stability MWST

BootstrapStabilityMWST is the best classical estimator: mean excess
0.01714, 95% CI
[0.01562, 0.01872]. It
improves only modestly over direct correction and closes
40.3% of the BinaryMWST gap.

## 7. Random-tree control

The first preregistered random tree has excess 0.04212.
Across five random trees per dataset, mean Hamming is
0.19602, best-of-five oracle-style Hamming is
0.18680, and mean within-dataset standard
deviation is 0.00742. Data-driven bootstrap
beats the primary random tree by
0.02498 Hamming, so generic tree
regularization alone does not explain the result.

## 8. Alternating structured estimator

Alternating estimation has excess 0.01822.
98.3%
of runs converge without changing the initial corrected tree; only
1.7%
finish with a different tree. It therefore adds little beyond initialization.

| scope | converged_0_fraction | converged_1_fraction | converged_2plus_fraction | max_iteration_reached_fraction | final_tree_differs_fraction |
| --- | --- | --- | --- | --- | --- |
| overall | 0.983 | 0.017 | 0.000 | 0.000 | 0.017 |
| balanced | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| path | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| random | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| star | 0.933 | 0.067 | 0.000 | 0.000 | 0.067 |

## 9. True-tree information value

`Value_of_true_tree = Hamming(RandomTree) - Hamming(TrueTree)` is
0.04212 overall, well above the 0.005 kill threshold.
The value is substantial for balanced, path, and random topologies but small on
stars. Thus tree identity matters in three families under the fixed decoder,
while star remains a topology-specific prior-misspecification region.

## 10. Classical residual gap

| estimator | mean_hamming | mean_excess | excess_ci_lower | excess_ci_upper | exact_row_recovery | valid_clean_join_tree_rate | tree_edge_disagreement | runtime_seconds |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TrueTreeOracle | 0.15436 | 0.00000 | 0.00000 | 0.00000 | 0.17078 | 1.000 | 0.00000 | 0.0503 |
| DataAgnosticRandomTree | 0.19648 | 0.04212 | 0.04032 | 0.04393 | 0.06456 | 0.000 | 0.88722 | 0.0510 |
| BinaryMWST | 0.18308 | 0.02872 | 0.02693 | 0.03063 | 0.09828 | 0.233 | 0.32778 | 0.0497 |
| NoiseCorrectedMWST | 0.17253 | 0.01816 | 0.01655 | 0.01980 | 0.11131 | 0.050 | 0.31833 | 0.0502 |
| BootstrapStabilityMWST | 0.17151 | 0.01714 | 0.01562 | 0.01872 | 0.11242 | 0.050 | 0.32444 | 0.0973 |
| AlternatingTreeIncidenceEstimator | 0.17258 | 0.01822 | 0.01659 | 0.01985 | 0.11131 | 0.058 | 0.31722 | 0.0536 |
| ProfileLikelihoodTreeSearch | 0.18779 | 0.03343 | 0.03205 | 0.03480 | 0.09350 | 0.192 | 0.34556 | 4.8889 |

The best residual is 0.01714, with paired 95% CI
[0.01562, 0.01872].
At `R=3`, the best residual falls to
0.00200; this confirms that the unresolved problem
is concentrated in the one-observation regime.

## 11. Gap closure fraction

Binary excess is 0.02872; best-classical excess is
0.01714; untruncated gap closure is
0.40312. This is below the 0.80 hard-stop threshold.

## 12. Topology-specific results

| scope | estimator | mean_excess | excess_ci_lower | excess_ci_upper |
| --- | --- | --- | --- | --- |
| balanced | TrueTreeOracle | 0.00000 | 0.00000 | 0.00000 |
| balanced | DataAgnosticRandomTree | 0.05044 | 0.04721 | 0.05377 |
| balanced | BinaryMWST | 0.03072 | 0.02633 | 0.03511 |
| balanced | NoiseCorrectedMWST | 0.02184 | 0.01812 | 0.02549 |
| balanced | BootstrapStabilityMWST | 0.02102 | 0.01778 | 0.02442 |
| balanced | AlternatingTreeIncidenceEstimator | 0.02184 | 0.01828 | 0.02549 |
| balanced | ProfileLikelihoodTreeSearch | 0.03972 | 0.03641 | 0.04318 |
| path | TrueTreeOracle | 0.00000 | 0.00000 | 0.00000 |
| path | DataAgnosticRandomTree | 0.06492 | 0.06135 | 0.06851 |
| path | BinaryMWST | 0.04782 | 0.04276 | 0.05307 |
| path | NoiseCorrectedMWST | 0.03341 | 0.02965 | 0.03699 |
| path | BootstrapStabilityMWST | 0.03256 | 0.02903 | 0.03613 |
| path | AlternatingTreeIncidenceEstimator | 0.03341 | 0.02977 | 0.03721 |
| path | ProfileLikelihoodTreeSearch | 0.05231 | 0.04793 | 0.05685 |
| random | TrueTreeOracle | 0.00000 | 0.00000 | 0.00000 |
| random | DataAgnosticRandomTree | 0.05124 | 0.04661 | 0.05618 |
| random | BinaryMWST | 0.03647 | 0.03276 | 0.04008 |
| random | NoiseCorrectedMWST | 0.02198 | 0.01840 | 0.02546 |
| random | BootstrapStabilityMWST | 0.02022 | 0.01653 | 0.02412 |
| random | AlternatingTreeIncidenceEstimator | 0.02198 | 0.01831 | 0.02563 |
| random | ProfileLikelihoodTreeSearch | 0.04279 | 0.03890 | 0.04690 |
| star | TrueTreeOracle | 0.00000 | 0.00000 | 0.00000 |
| star | DataAgnosticRandomTree | 0.00188 | -0.00067 | 0.00426 |
| star | BinaryMWST | -0.00014 | -0.00039 | 0.00000 |
| star | NoiseCorrectedMWST | -0.00458 | -0.00592 | -0.00334 |
| star | BootstrapStabilityMWST | -0.00524 | -0.00661 | -0.00387 |
| star | AlternatingTreeIncidenceEstimator | -0.00436 | -0.00571 | -0.00311 |
| star | ProfileLikelihoodTreeSearch | -0.00112 | -0.00205 | -0.00037 |

The best estimator leaves excess at least 0.01 in
3 topology families. Star behaves in the
opposite direction: estimated trees can outperform the generating-tree decoder,
consistent with A0.5 evidence that the uniform subtree prior is misspecified on
stars. Star is reported separately and is not used alone to reject
alpha-acyclicity.

## 13. Edge recovery vs downstream utility

Across non-oracle primary estimators including conditional profile search,
Pearson correlation between edge disagreement and downstream excess is
0.630; Spearman correlation is
0.665. This is a moderate association overall, but it is
not causal and is much weaker or reversed on stars. High edge disagreement is
therefore diagnostic, not itself a failure criterion.

Profile search was correctly triggered because the pre-profile residual exceeded
0.01. It raised noisy-data profile likelihood and changed the tree in
95.0% of datasets, yet worsened downstream excess
to 0.03343. Its deterministic pruning evaluated at most
24 corrected-weight-ranked single-swap candidates per iteration; exact full-data
profile likelihood selected among them.

## 14. Evidence FOR learned join-tree estimation

- True-tree information value is 0.04212, not negligible.
- Best classical excess remains 0.01714 with its
  entire paired CI above 0.01.
- Residuals above 0.01 occur in three topology families.
- The best data-driven estimator materially beats the preregistered random tree.
- The required profile-likelihood search fails to close the gap.
- On rows where both bootstrap-tree and true-tree DP solutions are unique, mean
  residual remains 0.01469; arbitrary tie selection
  is not the sole explanation.

## 15. Evidence AGAINST learned join-tree estimation

- Noise correction alone removes a substantial part of the A0.5 BinaryMWST gap.
- Bootstrap closes only 40.3%, leaving a target that
  is real but modest in absolute Hamming units.
- At `R=3`, classical excess is already about 0.002.
- Alternating re-estimation almost always stops immediately.
- Profile likelihood actively worsens clean recovery, exposing objective
  misspecification rather than lack of search effort.
- All evidence is synthetic and assumes known independent noise rates.

## 16. Hard kill-rule evaluation

| Rule | Result | Reason |
| --- | --- | --- |
| A: classical mean <=0.005 and CI upper <=0.010 | False | Best mean and CI remain above thresholds. |
| B: random-minus-true <=0.005 | False | Value of true tree is 0.04212. |
| C: closure >=0.80 and excess <0.01 | False | Closure is 0.403. |
| All continuation conditions | True | Three non-star families retain a unique-row residual and profile search fails. |

## 17. Final A0.75 decision

**D: A meaningful residual join-tree estimation problem remains; learned A1 is justified.**

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
