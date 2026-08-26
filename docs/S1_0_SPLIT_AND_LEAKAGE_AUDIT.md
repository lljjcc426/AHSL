# S1.0 split and leakage audit

## Yeast split comparison

The public S1 table has no validation partition built in; counts below are audit train/test partitions. Any future fitting must subdivide training only.

| Split | Train | Test | Test prevalence | any train gene | all train genes | any train pair | all train pairs | shared query pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| random triple (diagnostic) | 72,889 | 18,222 | 0.0352 | 1.000 | 1.000 | 1.000 | 0.0059 | 182 |
| any-held-gene test | 45,532 | 45,579 | 0.0303 | 0.902 | 0.000 | 0.271 | 0.000 | 114 |
| query-pair-disjoint | 72,964 | 18,147 | 0.0535 | 1.000 | 0.256 | 0.041 | 0.000 | 0 |
| query-gene-disjoint | 57,715 | 33,396 | 0.0376 | 1.000 | 0.293 | 0.0448 | 0.000 | 0 |

“Any-held-gene test” means training excludes held genes and test contains at least one; it is not an all-three-unseen split. Dango gene split 2 supplies the latter concept by requiring all three test genes held and discarding mixed triples. Query-pair-disjoint is the most direct available background control, yet array genes and other pairs remain shared. Public S1 lacks raw batch IDs, preventing exact plate-disjoint auditing.

Lower-order-background-disjointness is only partial: query-pair split removes the focal double query but 4.14% of test triples have another pair present in training. An order-extrapolation split is conceptually possible using digenic rows for training and trigenic rows for testing, but digenic observations do not identify tau for arbitrary triples; it evaluates transfer/prediction, not direct contrast recovery.

## Microbiome

Ordinary train/test independence is impossible. Valid diagnostics are retrospective random cell masking, leave-one-order-out, subsets-containing-species holdout, and budget curves, always scored against the full measured panel. Results in this phase use budget curves; the other split families are specified but not overinterpreted as independent generalization.

## Drug

Primary split unit must be drug identity set. Dose-context disjointness within a set asks interpolation/extrapolation of context, not new-set discovery. Drug-identity holdout is possible but only eight identities exist. Individual dose-point random split is invalid primary evidence.

## Leakage gate

Leakage-resistant split definitions exist, so the *split-design* gate passes. The benchmark nevertheless fails because strict splitting does not create directly observed truth for unmeasured yeast triples and leaves too few independent structures in the other domains.
