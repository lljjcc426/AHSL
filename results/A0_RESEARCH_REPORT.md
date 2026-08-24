# AHSL Phase A0 Research Report

## 1. Research question

Does restricting each incidence row to a connected subtree of a known join tree improve recovery of a clean alpha-acyclic hypergraph from independently corrupted incidence observations?

## 2. Mathematical formulation

The hyperedge labels are the nodes of a fixed tree `T`. For every original vertex `i`, the support `S_i = {j : B_ij = 1}` is selected from the complete set of non-empty connected induced node sets of `T`. This is the classical join-tree/running-intersection characterization, not a novelty claim.

## 3. Models and baselines

The run compares raw observations, independent free logits, normalized-L1 free logits, exact nearest-connected-subtree projection, exact likelihood MAP with known corruption rates, and categorical FixedTreeAHSL over all connected subtrees. The unconstrained logits can memorize one binary observation and are a sanity baseline, not a denoiser with an independent statistical signal.

## 4. Experimental setup

Configuration ID: `a0_pilot`. The run used `n=[50]`, `m=[8]`, branch probabilities `[0.4]`, topologies `['random', 'path', 'star', 'balanced']`, observation counts `[1, 3]`, and seeds `[0, 1, 2, 3, 4]`. The true join tree is known. Results retain every seed and use no clean-incidence oracle for model fitting or sparse-lambda selection. This A0 experiment measures structural projection/denoising; it does not establish consistency or general hypergraph structure learning.

## 5. Main numerical results

The following are observed means across the symmetric-noise, one-observation portion actually run.

| model | noise | clean_f1 | exact_row_recovery | riv | runtime_seconds |
| --- | --- | --- | --- | --- | --- |
| FixedTreeAHSL | 0.0 | 1.0 | 1.0 | 0.0 | 0.1259 |
| FixedTreeAHSL | 0.1 | 0.8263 | 0.553 | 0.0 | 0.1121 |
| FixedTreeAHSL | 0.2 | 0.7057 | 0.295 | 0.0 | 0.1473 |
| FixedTreeAHSL | 0.3 | 0.5645 | 0.134 | 0.0 | 0.1363 |
| NearestConnectedSubtree | 0.0 | 1.0 | 1.0 | 0.0 | 0.0007 |
| NearestConnectedSubtree | 0.1 | 0.8463 | 0.601 | 0.0 | 0.0006 |
| NearestConnectedSubtree | 0.2 | 0.7176 | 0.326 | 0.0 | 0.0006 |
| NearestConnectedSubtree | 0.3 | 0.5624 | 0.167 | 0.0 | 0.0005 |
| NoiseAwareMAPSubtree | 0.0 | 1.0 | 1.0 | 0.0 | 0.0006 |
| NoiseAwareMAPSubtree | 0.1 | 0.8463 | 0.601 | 0.0 | 0.0007 |
| NoiseAwareMAPSubtree | 0.2 | 0.7176 | 0.326 | 0.0 | 0.0006 |
| NoiseAwareMAPSubtree | 0.3 | 0.5624 | 0.167 | 0.0 | 0.0006 |
| Observed | 0.0 | 1.0 | 1.0 | 0.0 | 0.0001 |
| Observed | 0.1 | 0.8391 | 0.472 | 15.55 | 0.0 |
| Observed | 0.2 | 0.7088 | 0.192 | 25.95 | 0.0 |
| Observed | 0.3 | 0.5573 | 0.068 | 32.95 | 0.0 |
| SparseUnconstrained | 0.0 | 1.0 | 1.0 | 0.0 | 0.0364 |
| SparseUnconstrained | 0.1 | 0.8391 | 0.472 | 15.55 | 0.0323 |
| SparseUnconstrained | 0.2 | 0.7088 | 0.192 | 25.95 | 0.0358 |
| SparseUnconstrained | 0.3 | 0.5573 | 0.068 | 32.95 | 0.0363 |
| Unconstrained | 0.0 | 1.0 | 1.0 | 0.0 | 0.2067 |
| Unconstrained | 0.1 | 0.8391 | 0.472 | 15.55 | 0.0281 |
| Unconstrained | 0.2 | 0.7088 | 0.192 | 25.95 | 0.0306 |
| Unconstrained | 0.3 | 0.5573 | 0.068 | 32.95 | 0.0285 |

## 6. Statistical comparison

Paired differences are `FixedTreeAHSL - baseline`. The table pools the four preregistered topologies within each noise/observation setting, giving 20 paired cases per row; intervals are paired bootstrap intervals. Per-topology Wilcoxon results remain in `results/aggregated/a0_statistical_tests.csv` and are not over-interpreted with only five seeds.

| noise_setting | observations | baseline | pairs | mean_dF1 | CI_2.5% | CI_97.5% | AHSL_win_rate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| false_negative_only_0.20 | 1 | Observed | 20 | -0.0054 | -0.0128 | 0.0027 | 0.4 |
| false_negative_only_0.20 | 3 | Observed | 20 | 0.0115 | 0.0047 | 0.0189 | 0.75 |
| false_positive_only_0.20 | 1 | Observed | 20 | -0.0188 | -0.0288 | -0.0089 | 0.15 |
| false_positive_only_0.20 | 3 | Observed | 20 | 0.0492 | 0.0423 | 0.0563 | 1.0 |
| symmetric_0.00 | 1 | Observed | 20 | 0.0 | 0.0 | 0.0 | 0.0 |
| symmetric_0.00 | 3 | Observed | 20 | 0.0 | 0.0 | 0.0 | 0.0 |
| symmetric_0.10 | 1 | Observed | 20 | -0.0129 | -0.021 | -0.0037 | 0.35 |
| symmetric_0.10 | 3 | Observed | 20 | -0.0005 | -0.0054 | 0.0046 | 0.45 |
| symmetric_0.20 | 1 | Observed | 20 | -0.0031 | -0.0135 | 0.0082 | 0.3 |
| symmetric_0.20 | 3 | Observed | 20 | -0.033 | -0.0494 | -0.0171 | 0.3 |
| symmetric_0.30 | 1 | Observed | 20 | 0.0072 | -0.0017 | 0.0166 | 0.65 |
| symmetric_0.30 | 3 | Observed | 20 | -0.0559 | -0.0696 | -0.0398 | 0.05 |
| false_negative_only_0.20 | 1 | NearestConnectedSubtree | 20 | 0.0151 | 0.0069 | 0.023 | 0.8 |
| false_negative_only_0.20 | 3 | NearestConnectedSubtree | 20 | -0.0045 | -0.0091 | 0.0001 | 0.25 |
| false_positive_only_0.20 | 1 | NearestConnectedSubtree | 20 | -0.0335 | -0.0406 | -0.0256 | 0.05 |
| false_positive_only_0.20 | 3 | NearestConnectedSubtree | 20 | -0.0088 | -0.0183 | 0.0006 | 0.35 |
| symmetric_0.00 | 1 | NearestConnectedSubtree | 20 | 0.0 | 0.0 | 0.0 | 0.0 |
| symmetric_0.00 | 3 | NearestConnectedSubtree | 20 | 0.0 | 0.0 | 0.0 | 0.0 |
| symmetric_0.10 | 1 | NearestConnectedSubtree | 20 | -0.0201 | -0.0262 | -0.014 | 0.1 |
| symmetric_0.10 | 3 | NearestConnectedSubtree | 20 | -0.0194 | -0.0243 | -0.0144 | 0.0 |
| symmetric_0.20 | 1 | NearestConnectedSubtree | 20 | -0.0119 | -0.0239 | -0.0014 | 0.3 |
| symmetric_0.20 | 3 | NearestConnectedSubtree | 20 | -0.069 | -0.085 | -0.0528 | 0.05 |
| symmetric_0.30 | 1 | NearestConnectedSubtree | 20 | 0.0021 | -0.0098 | 0.014 | 0.6 |
| symmetric_0.30 | 3 | NearestConnectedSubtree | 20 | -0.0863 | -0.1018 | -0.0699 | 0.0 |
| false_negative_only_0.20 | 1 | NoiseAwareMAPSubtree | 20 | -0.0149 | -0.0218 | -0.0087 | 0.0 |
| false_negative_only_0.20 | 3 | NoiseAwareMAPSubtree | 20 | -0.0429 | -0.0536 | -0.0332 | 0.0 |
| false_positive_only_0.20 | 1 | NoiseAwareMAPSubtree | 20 | -0.0539 | -0.0623 | -0.0451 | 0.0 |
| false_positive_only_0.20 | 3 | NoiseAwareMAPSubtree | 20 | -0.0571 | -0.0684 | -0.0473 | 0.0 |
| symmetric_0.00 | 1 | NoiseAwareMAPSubtree | 20 | 0.0 | 0.0 | 0.0 | 0.0 |
| symmetric_0.00 | 3 | NoiseAwareMAPSubtree | 20 | 0.0 | 0.0 | 0.0 | 0.0 |
| symmetric_0.10 | 1 | NoiseAwareMAPSubtree | 20 | -0.0201 | -0.0264 | -0.0141 | 0.1 |
| symmetric_0.10 | 3 | NoiseAwareMAPSubtree | 20 | -0.0194 | -0.0243 | -0.0145 | 0.0 |
| symmetric_0.20 | 1 | NoiseAwareMAPSubtree | 20 | -0.0119 | -0.023 | -0.0009 | 0.3 |
| symmetric_0.20 | 3 | NoiseAwareMAPSubtree | 20 | -0.069 | -0.0851 | -0.0534 | 0.05 |
| symmetric_0.30 | 1 | NoiseAwareMAPSubtree | 20 | 0.0021 | -0.0096 | 0.0141 | 0.6 |
| symmetric_0.30 | 3 | NoiseAwareMAPSubtree | 20 | -0.0863 | -0.1026 | -0.0696 | 0.0 |

## 7. Does alpha-acyclicity help denoise structure?

Observation: across nonzero-noise rows, mean clean-F1 gains over Observed were `0.0175` for NearestConnectedSubtree and `0.0312` for NoiseAwareMAPSubtree. Their exact-row recovery gains were `0.1380` and `0.1745`. FixedTreeAHSL itself differed from Observed by `-0.0061`. The maximum AHSL running-intersection violation count was `0`.

Interpretation: the positive exact-estimator differences support useful denoising by the fixed-tree hypothesis class, but the learned categorical estimator does not realize that average F1 gain. Zero RIV verifies the construction and is not by itself evidence of better recovery.

## 8. Does learning outperform exact structural projection?

Observation: mean paired clean-F1 differences were `-0.0236` against NearestConnectedSubtree and `-0.0373` against NoiseAwareMAPSubtree.

Interpretation: if these values are non-positive, the A0 evidence supports the structural constraint but not a learned estimator over the exact classical alternatives.

## 9. Failure modes

The central implementation failure is an objective/inference mismatch. With repeated observations, BCE targets fractional incidence marginals and learns a diffuse mixture over subtrees, while inference discards that mixture through a single categorical `argmax`. Across setting means, the largest entropy was `1.7629` and the lowest mean maximum candidate probability was `0.3359`. This explains why additional observations can improve exact MAP while widening its advantage over FixedTreeAHSL. There was no universal singleton collapse, but missing-only noise increased singleton predictions. The requested normalized-L1 range changed clean F1 by at most `0.0000` relative to Observed at the fixed threshold, so it did not provide a useful density-matched curve. Topology and asymmetric-noise effects remain visible in the raw CSV.

## 10. Computational limitations

The implementation enumerates all non-empty masks in `O(2^m m)` time. This pilot selected only `m=[8]`; its largest realized candidate set was `135`, and the largest measured FixedTreeAHSL fit time was `0.5483` seconds. The runtime-versus-`m` plot therefore contains only the pilot point and is not a scaling result. Candidate growth is topology dependent, especially for stars; no scalability claim is made.

## 11. Evidence supporting the hypothesis

The strongest supporting evidence is the positive paired recovery gain of exact connected-subtree projection/MAP over raw observations, especially for exact-row recovery, together with exact RIV=0 for every structural estimator. This supports the alpha-acyclic fixed-tree hypothesis class as a denoising prior in part of the tested region.

## 12. Evidence against the hypothesis

The strongest counter-evidence is that FixedTreeAHSL averaged `-0.0236` F1 relative to nearest projection and `-0.0373` relative to known-noise MAP under nonzero noise. It also averaged `-0.0061` relative to raw observations. The gain is not uniform across noise regimes, and the sparse range did not create a meaningful density-matched comparator. These data do not justify neural superiority or progression to a learned join tree.

## 13. Recommended next step

Research decision: **Decision B - Keep alpha-acyclic structure but abandon neural A0 estimation**.

Final recommendation: **Modify A0**.

Replace the current neural A0 estimator with exact projection/MAP as the anchor, and test additional `m`, branch probabilities, and seeds before A1. A learned model should return only if its training objective is aligned with the hard subtree decision or it uses a downstream likelihood unavailable to the exact baseline.

This recommendation is limited to the configurations actually run. Phase A0 assumes the true join tree is known and does not yet establish usefulness for general hypergraph structure learning.
