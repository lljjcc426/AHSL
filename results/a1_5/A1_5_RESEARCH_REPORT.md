# AHSL Phase A1.5 Research Report

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

| posterior rows | marginal entries | marginal mismatches | max marginal error | max normalization error | MAP mismatches | median mismatches | connected MBR mismatches | max root error |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1760 | 12320 | 0 | 2.55e-15 | 1.89e-15 | 0 | 0 | 0 | 2.11e-15 |

All decision mismatches were zero, including explicit q=0/q=1, zero-noise,
asymmetric-noise, and repeated-observation cases.

## 6. Complexity

All node marginals cost O(m) per row and O(nm) per batch. Measured scaling:

| n | m | runtime_seconds | microseconds_per_nm |
| --- | --- | --- | --- |
| 50.0000000 | 16.0000000 | 0.0016738 | 2.0922500 |
| 50.0000000 | 64.0000000 | 0.0063298 | 1.9780625 |
| 50.0000000 | 256 | 0.0264903 | 2.0695547 |
| 50.0000000 | 1024 | 0.1117880 | 2.1833594 |

## 7. Experimental protocol

The deterministic A1 convention was reused exactly: n=300, m=16, q=0.4,
symmetric 0.20 noise, R=1, four topology families, seeds 0--29, and a
60/20/20 row split. No new tree estimator or broader statistical grid was
introduced. Oracle-q and deployable estimated-q tracks were kept separate.

## 8. MAP results

Deployable estimated-q major-tree results are contained below.

| tree_source | q_mode | decoder | mean_test_hamming | mean_hamming_minus_binary | hamming_difference_ci_lower | hamming_difference_ci_upper | mean_exact_row_recovery | mean_clean_f1 | mean_posterior_expected_hamming | mean_risk_calibration_gap | mean_risk_row_correlation | median_connected_fraction | mean_total_inference_runtime_seconds |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GeneratingTreeOracle | estimated_q | PosteriorMAPConnected | 0.13073 | -0.02219 | -0.02485 | -0.01954 | 0.22319 | 0.60863 | 0.13122 | 0.00049 | 0.40398 | 0.52972 | 0.03436 |
| BinaryMWST | estimated_q | PosteriorMAPConnected | 0.15292 | 0 | 0 | 0 | 0.13069 | 0.50789 | 0.13724 | -0.01568 | 0.43772 | 0.45444 | 0.03154 |
| EstimatedQMarginalTree | estimated_q | PosteriorMAPConnected | 0.15430 | 0.00138 | -0.00037 | 0.00316 | 0.13514 | 0.51679 | 0.13412 | -0.02018 | 0.43366 | 0.51819 | 0.03563 |

## 9. Unconstrained posterior-median results

| tree_source | q_mode | decoder | mean_test_hamming | mean_hamming_minus_binary | hamming_difference_ci_lower | hamming_difference_ci_upper | mean_exact_row_recovery | mean_clean_f1 | mean_posterior_expected_hamming | mean_risk_calibration_gap | mean_risk_row_correlation | median_connected_fraction | mean_total_inference_runtime_seconds |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GeneratingTreeOracle | estimated_q | PosteriorMedianUnconstrained | 0.11840 | -0.02257 | -0.02464 | -0.02052 | 0.10917 | 0.59365 | 0.11841 | 5.90e-06 | 0.40928 | 0.52972 | 0.00269 |
| BinaryMWST | estimated_q | PosteriorMedianUnconstrained | 0.14097 | 0 | 0 | 0 | 0.03958 | 0.46001 | 0.12117 | -0.01980 | 0.48556 | 0.45444 | 0.00261 |
| EstimatedQMarginalTree | estimated_q | PosteriorMedianUnconstrained | 0.14066 | -0.00031 | -0.00202 | 0.00145 | 0.05528 | 0.48994 | 0.12032 | -0.02034 | 0.46101 | 0.51819 | 0.00274 |

The median is diagnostic only: empty or disconnected predictions are outside
the frozen connected-output class.

## 10. Connected Bayes-Hamming results

Both q tracks are shown explicitly. OracleQMarginalTree remains an
oracle-assisted tree source even when its fixed tree is rescored with an
estimated q; it is secondary and does not enter the deployable stop rule.

| tree_source | q_mode | mean_test_hamming | mean_hamming_minus_binary | hamming_difference_ci_lower | hamming_difference_ci_upper | mean_posterior_expected_hamming | mean_risk_calibration_gap |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GeneratingTreeOracle | oracle_q | 0.12593 | -0.02341 | -0.02550 | -0.02142 | 0.12682 | 0.00089 |
| GeneratingTreeOracle | estimated_q | 0.12614 | -0.02270 | -0.02477 | -0.02075 | 0.12680 | 0.00066 |
| BinaryMWST | oracle_q | 0.14934 | 0 | 0 | 0 | 0.13307 | -0.01627 |
| BinaryMWST | estimated_q | 0.14884 | 0 | 0 | 0 | 0.13131 | -0.01752 |
| EstimatedQMarginalTree | oracle_q | 0.14826 | -0.00108 | -0.00301 | 0.00083 | 0.12803 | -0.02023 |
| EstimatedQMarginalTree | estimated_q | 0.14791 | -0.00093 | -0.00285 | 0.00102 | 0.12835 | -0.01956 |

## 11. Decoder gain

Positive values mean MAP Hamming minus ConnectedBayesHamming Hamming.

| tree_source | mean_effect | ci_lower | ci_upper |
| --- | --- | --- | --- |
| GeneratingTreeOracle | 0.00459 | 0.00345 | 0.00580 |
| BinaryMWST | 0.00408 | 0.00247 | 0.00568 |
| EstimatedQMarginalTree | 0.00639 | 0.00484 | 0.00799 |

## 12. Tree gain under aligned decoder

The preregistered deployable quantity was BinaryMWST Hamming minus
EstimatedQMarginalTree Hamming. Its overall value was
0.00093, with paired 95% CI
[-0.00097, 0.00284].

| scope | mean_tree_gain | ci_lower | ci_upper |
| --- | --- | --- | --- |
| balanced | 0.00316 | -0.00108 | 0.00743 |
| path | 0.00733 | 0.00344 | 0.01139 |
| random | 0.00514 | 0.00156 | 0.00865 |
| star | -0.01191 | -0.01656 | -0.00736 |

The unique/non-tied analysis was:

| scope | mean_tree_gain | tree_gain_sd | ci_lower | ci_upper | num_datasets | num_non_tied_test_rows | num_seeds |
| --- | --- | --- | --- | --- | --- | --- | --- |
| overall | 0.00015 | 0.00593 | -0.00193 | 0.00225 | 120 | 5784 | 30.00000 |

## 13. Connectivity cost

Positive empirical cost means the connected constraint worsened realized
Hamming; posterior cost is nonnegative by the Bayes-action definition.

| effect_name | tree_source | mean_effect | ci_lower | ci_upper |
| --- | --- | --- | --- | --- |
| ConnectivityCost_empirical | GeneratingTreeOracle | 0.00773 | 0.00668 | 0.00877 |
| ConnectivityCost_empirical | BinaryMWST | 0.00786 | 0.00692 | 0.00884 |
| ConnectivityCost_empirical | EstimatedQMarginalTree | 0.00725 | 0.00641 | 0.00802 |
| ConnectivityCost_posterior | GeneratingTreeOracle | 0.00839 | 0.00809 | 0.00869 |
| ConnectivityCost_posterior | BinaryMWST | 0.01015 | 0.00976 | 0.01052 |
| ConnectivityCost_posterior | EstimatedQMarginalTree | 0.00803 | 0.00766 | 0.00839 |

## 14. Posterior risk calibration

The gap is posterior predicted risk minus realized clean Hamming.

| tree_source | mean_posterior_expected_hamming | mean_test_hamming | mean_risk_calibration_gap | mean_risk_row_correlation |
| --- | --- | --- | --- | --- |
| GeneratingTreeOracle | 0.12680 | 0.12614 | 0.00066 | 0.37921 |
| BinaryMWST | 0.13131 | 0.14884 | -0.01752 | 0.44634 |
| EstimatedQMarginalTree | 0.12835 | 0.14791 | -0.01956 | 0.41495 |

## 15. Exact-row versus Hamming tradeoff

Positive values favor MAP exact-row recovery over ConnectedBayesHamming.

| tree_source | mean_effect | ci_lower | ci_upper |
| --- | --- | --- | --- |
| GeneratingTreeOracle | 0.02514 | 0.02028 | 0.03028 |
| BinaryMWST | 0.00792 | 0.00250 | 0.01347 |
| EstimatedQMarginalTree | 0.00361 | -0.00222 | 0.00931 |

## 16. Topology analysis

Only 2 topology families exceeded the
required 0.005 TreeGain threshold. The topology-specific paired intervals are
shown in Section 12.

## 17. Star analysis

| tree_source | decoder | mean_test_hamming | mean_risk_calibration_gap |
| --- | --- | --- | --- |
| GeneratingTreeOracle | PosteriorMAPConnected | 0.16316 | 0.00017 |
| GeneratingTreeOracle | PosteriorMedianUnconstrained | 0.14670 | -0.00139 |
| GeneratingTreeOracle | ConnectedBayesHamming | 0.15833 | -4.56e-06 |
| BinaryMWST | PosteriorMAPConnected | 0.16882 | -0.00589 |
| BinaryMWST | PosteriorMedianUnconstrained | 0.15240 | -0.00773 |
| BinaryMWST | ConnectedBayesHamming | 0.16319 | -0.00685 |
| EstimatedQMarginalTree | PosteriorMAPConnected | 0.18427 | -0.02122 |
| EstimatedQMarginalTree | PosteriorMedianUnconstrained | 0.16420 | -0.01991 |
| EstimatedQMarginalTree | ConnectedBayesHamming | 0.17510 | -0.02141 |

Star is reported separately because earlier phases found decoder-sensitive
behavior there; it is not used to override the four-family stop rule.

## 18. Evidence for tree learning

The strongest favorable evidence is path TreeGain
0.00733, with CI
[0.00344, 0.01139]. It must
still satisfy the preregistered three-topology, non-tied, q-fairness, and
calibration criteria.

## 19. Evidence against tree learning

The primary stop rule fired: **True**. The
overall aligned TreeGain and its lower confidence bound are the controlling
evidence. The strongest adverse topology was star at
-0.01191; no additional tree search was attempted.

## 20. Evidence for subtree/posterior modeling

The deployable decoder gains were 0.00459
on the generating tree, 0.00408 on BinaryMWST,
and 0.00639 on
EstimatedQMarginalTree. These distinguish decision-model value from tree-
identity value.

## 21. Alpha-acyclic warning signals

The wider-alpha warning fired: **False**.
It appeared in 0 topology families
under GeneratingTreeOracle with oracle q, using the preregistered >0.01 gap and
a documented substantial-disconnection threshold of 0.10.

| scope | mean_test_hamming | median_empty_fraction | median_disconnected_fraction | empirical_connectivity_cost |
| --- | --- | --- | --- | --- |
| balanced | 0.11035 | 0.42556 | 0.01111 | 0.00583 |
| path | 0.10215 | 0.42111 | 0.01056 | 0.00594 |
| random | 0.11497 | 0.42944 | 0.00500 | 0.00625 |
| star | 0.14667 | 0.55389 | 0 | 0.01156 |

## 22. Literature novelty assessment

ConnectedBayesHamming is an instance of classical constrained centroid/MEA or
MBR decoding: posterior marginals supply additive gains and a combinatorial
optimizer enforces validity. A1.5's value is the falsifiable audit of a specific
tree-learning claim, not a new decision algorithm.

## 23. Stop-rule evaluation

- Mean TreeGain <= 0.005 or CI lower <= 0 or fewer than three positive topology
  families: **True**.
- Survives unique/non-tied analysis: **False**.
- Major-tree posterior risk reasonably calibrated at absolute mean gap <=0.02:
  **True**.
- Full latent-tree continuation condition: **False**.

## 24. Final decision

**Decision A**

> Stop latent-tree learning. Decision-aligned decoding does not rescue marginal-likelihood tree selection, and BinaryMWST is sufficient for the current k=1 research program.

## 25. Recommended next research direction

Freeze BinaryMWST as the k=1 tree component. Retain exact posterior inference as infrastructure, but require a real application and loss model before expanding this line.
