# AHSL Phase A1 Research Report

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

| row_comparisons | mismatches | max_absolute_error | max_prior_mass_error |
| --- | --- | --- | --- |
| 1440.00000 | 0.00000 | 5.33e-15 | 1.33e-15 |

## 8. Computational complexity

Fixed-tree scoring costs O(nm) time and O(nm) message storage for a batch of n
rows. One full local-search round costs O(|N(T)|nm); at m=16 the measured
neighborhood had 369 unique trees and took about 0.47 seconds for 180 rows.

## 9. q estimation

Known-tree maximum likelihood used a 21-point bounded grid followed by scalar
refinement, with no clean data input.

| n | mean_estimated_q | mean_absolute_error | sd_estimated_q |
| --- | --- | --- | --- |
| 100.00000 | 0.38114 | 0.03783 | 0.04787 |
| 300.00000 | 0.40063 | 0.01597 | 0.02245 |
| 1000.00000 | 0.39982 | 0.01017 | 0.01273 |

In the joint primary estimator, mean absolute q error was
0.03674.

## 10. Global-small-tree validation

| datasets | global_optimum_recovery_rate | mean_objective_gap | mean_downstream_gap |
| --- | --- | --- | --- |
| 12.00000 | 1.00000 | 0.00000 | 0.00000 |

## 11. Held-out experimental protocol

Each n=300 dataset was split by rows into 180 train, 60 validation, and 60 test
rows. Tree fitting saw noisy train rows only. Estimated-q checkpoint selection
used noisy validation rows. Clean test rows were used only for final metrics.

## 12. Classical baseline results

| estimator | mean_test_hamming | mean_test_hamming_excess | excess_ci_lower | excess_ci_upper | mean_exact_row_recovery | mean_test_nll_per_row |
| --- | --- | --- | --- | --- | --- | --- |
| GeneratingTreeOracle | 0.13053 | 0.00000 | 0.00000 | 0.00000 | 0.22319 | 9.61051 |
| DataAgnosticRandomTree | 0.18062 | 0.05009 | 0.04738 | 0.05277 | 0.07486 | 9.89256 |
| BinaryMWST | 0.15301 | 0.02248 | 0.01979 | 0.02529 | 0.13167 | 9.73200 |
| NoiseCorrectedMWST | 0.15425 | 0.02372 | 0.02135 | 0.02623 | 0.13194 | 9.73452 |
| BootstrapStabilityMWST | 0.15564 | 0.02511 | 0.02271 | 0.02740 | 0.13097 | 9.74018 |
| OracleQMarginalTree | 0.15352 | 0.02299 | 0.02070 | 0.02518 | 0.13639 | 9.71606 |
| EstimatedQMarginalTree | 0.15430 | 0.02377 | 0.02162 | 0.02594 | 0.13514 | 9.72122 |

## 13. Oracle-q marginal tree

Its excess was 0.02299. This is an oracle
diagnostic because it receives the generating q.

## 14. Estimated-q marginal tree

Its held-out Hamming excess was 0.02377;
the paired gap closure relative to BinaryMWST was
-5.7%.

## 15. Uniform vs matched decoder

Negative values below favor the matched prior.

| estimator | tree_topology | matched_hamming | uniform_hamming | matched_minus_uniform_hamming |
| --- | --- | --- | --- | --- |
| BinaryMWST | balanced | 0.14493 | 0.18010 | -0.03517 |
| BinaryMWST | path | 0.14587 | 0.17733 | -0.03146 |
| BinaryMWST | random | 0.15201 | 0.18337 | -0.03135 |
| BinaryMWST | star | 0.16924 | 0.21212 | -0.04288 |
| BootstrapStabilityMWST | balanced | 0.14812 | 0.16524 | -0.01712 |
| BootstrapStabilityMWST | path | 0.14094 | 0.16017 | -0.01924 |
| BootstrapStabilityMWST | random | 0.14847 | 0.16604 | -0.01757 |
| BootstrapStabilityMWST | star | 0.18503 | 0.20670 | -0.02167 |
| DataAgnosticRandomTree | balanced | 0.16931 | 0.18962 | -0.02031 |
| DataAgnosticRandomTree | path | 0.16271 | 0.18771 | -0.02500 |
| DataAgnosticRandomTree | random | 0.17212 | 0.19122 | -0.01910 |
| DataAgnosticRandomTree | star | 0.21833 | 0.21649 | 0.00184 |
| EstimatedQMarginalTree | balanced | 0.14441 | 0.16174 | -0.01733 |
| EstimatedQMarginalTree | path | 0.13979 | 0.15722 | -0.01743 |
| EstimatedQMarginalTree | random | 0.14872 | 0.16486 | -0.01615 |
| EstimatedQMarginalTree | star | 0.18427 | 0.20566 | -0.02139 |
| GeneratingTreeOracle | balanced | 0.12274 | 0.13687 | -0.01413 |
| GeneratingTreeOracle | path | 0.11233 | 0.11878 | -0.00646 |
| GeneratingTreeOracle | random | 0.12486 | 0.14028 | -0.01542 |
| GeneratingTreeOracle | star | 0.16219 | 0.21608 | -0.05389 |
| NoiseCorrectedMWST | balanced | 0.14667 | 0.16569 | -0.01903 |
| NoiseCorrectedMWST | path | 0.14132 | 0.16469 | -0.02337 |
| NoiseCorrectedMWST | random | 0.14590 | 0.16580 | -0.01990 |
| NoiseCorrectedMWST | star | 0.18312 | 0.20604 | -0.02292 |
| OracleQMarginalTree | balanced | 0.14469 | 0.15972 | -0.01503 |
| OracleQMarginalTree | path | 0.13753 | 0.14986 | -0.01233 |
| OracleQMarginalTree | random | 0.15024 | 0.16278 | -0.01253 |
| OracleQMarginalTree | star | 0.18163 | 0.20566 | -0.02403 |

## 16. Star analysis

| estimator | tree_topology | matched_hamming | uniform_hamming | matched_minus_uniform_hamming |
| --- | --- | --- | --- | --- |
| BinaryMWST | star | 0.16924 | 0.21212 | -0.04288 |
| BootstrapStabilityMWST | star | 0.18503 | 0.20670 | -0.02167 |
| DataAgnosticRandomTree | star | 0.21833 | 0.21649 | 0.00184 |
| EstimatedQMarginalTree | star | 0.18427 | 0.20566 | -0.02139 |
| GeneratingTreeOracle | star | 0.16219 | 0.21608 | -0.05389 |
| NoiseCorrectedMWST | star | 0.18312 | 0.20604 | -0.02292 |
| OracleQMarginalTree | star | 0.18163 | 0.20566 | -0.02403 |

Under the uniform decoder, EstimatedQMarginalTree beat the generating tree by
0.01042 Hamming on star. Under the matched decoder it was worse by 0.02208,
so the generating-tree advantage was restored. This supports prior
misspecification as the main source of the A0.75 star anomaly, although it does
not make marginal-likelihood tree selection competitive with BinaryMWST.

## 17. Tree identity value

Random-tree minus generating-tree held-out Hamming under the matched decoder was
0.05009.

## 18. Held-out likelihood

| estimator | mean_train_nll_gain | mean_validation_nll_gain | mean_test_nll_gain | validation_worsened_fraction | test_worsened_fraction |
| --- | --- | --- | --- | --- | --- |
| EstimatedQMarginalTree | 0.01282 | 0.01870 | 0.00771 | 0.00000 | 0.11667 |
| OracleQMarginalTree | 0.02591 | 0.01068 | 0.01846 | 0.42500 | 0.38333 |

## 19. Downstream recovery

Topology-specific generating-tree and deployable marginal results are:

| scope | estimator | mean_test_hamming | mean_test_hamming_excess |
| --- | --- | --- | --- |
| balanced | GeneratingTreeOracle | 0.12274 | 0.00000 |
| balanced | EstimatedQMarginalTree | 0.14441 | 0.02167 |
| path | GeneratingTreeOracle | 0.11233 | 0.00000 |
| path | EstimatedQMarginalTree | 0.13979 | 0.02747 |
| random | GeneratingTreeOracle | 0.12486 | 0.00000 |
| random | EstimatedQMarginalTree | 0.14872 | 0.02385 |
| star | GeneratingTreeOracle | 0.16219 | 0.00000 |
| star | EstimatedQMarginalTree | 0.18427 | 0.02208 |

## 20. Identifiability observations

The labeled tree is population-identifiable for m>=2, 0<q<1, and an invertible
known noise channel because clean size-two support probabilities identify the
edges and the full support identifies q. Degeneracies remain at q in {0,1},
p+ + p- = 1, and m=1; finite samples become weak near these boundaries.

## 21. Evidence for continuing tree learning

Tree identity retained material held-out value: random trees were worse than
the generating tree by 0.05009. EstimatedQ retained
more than 0.01 excess in all four topology families, and both marginal variants
improved mean validation and test likelihood relative to their initial trees.
These facts show that the statistical tree problem is not vacuous.

## 22. Evidence against continuing tree learning

OracleQMarginalTree excess was 0.02299, not
better than BinaryMWST's 0.02248; EstimatedQ was worse
at 0.02377, giving negative gap closure.
Thus correctly marginalized likelihood improved held-out likelihood but did not
improve downstream Hamming. The experiment also remains synthetic, assumes
known noise rates, and supplies no realistic observable signal for supervised
tree learning. The prompt's third model-failure rule is therefore met.

## 23. Neural kill-rule evaluation

BinaryExcess=0.02248,
MarginalExcess=0.02377, and gap
closure=-5.7%. Neural kill rule met:
**False**.

## 24. Wider alpha-acyclic stop assessment

The matched subtree prior materially improved denoising and tree identity had
held-out value, so these results do not establish that alpha-acyclic structural
regularization is useless. They also do not show that k=1 is the limiting
factor. Moving to GHW<=k is therefore not justified by A1.

## 25. Final decision

**Decision C: A residual latent-tree problem remains, but current formulation or identifiability is insufficient; do not build neural models yet.**

## 26. Recommended research direction

Do not build a neural join-tree model. Preserve the exact marginal scorer as a
classical diagnostic and pause this direction until external data provide a
concrete tractability target and observable covariates for a shared prior. A
future positive case would favor a feature-conditioned subtree prior over
generic edge scores because it directly targets model mismatch, but A1 does not
justify implementing it.
