# S2.0 Classical Baselines

## Implemented fixed rules

| family | score / action | tuning |
|---|---|---|
| exact frequency | count of exact historical identity | none |
| recency | reverse last-observed order | none |
| repeat-if-seen | membership in historical identity table | none |
| decayed exact frequency | exponential recency-weighted count | fixed decay |
| node popularity | product implemented as log-count sum | none |
| pair composition | sum or minimum pair co-occurrence | none |
| pair Hawkes proxy | sum of exponentially decayed pair activity | fixed decay |
| simplicial/closure proxy | triple support plus pair composition | none |
| combinatorial assembly | one-member replacement generator | frozen limits; no test tuning |

Frequent itemset and association-rule information is represented by exact-set,
pair, and triple support. Resource allocation/common-neighbor variants were
audited but not expanded into redundant scorers because the decisive failure is
candidate coverage, not a small reordering inside the same candidate pool.

## Results and compute

Frequency is best in aggregate: Ubuntu Hit@1 0.207%, Recall@10 1.330%; Congress
Hit@1 0.461%, Recall@10 0.577%. It is exactly zero on novel sets. Pair Hawkes is
the strongest sampled-negative point-process proxy (Recall@10 93.2% Ubuntu,
94.8% Congress under random negatives), yet all implemented methods have novel
search-controlled Recall@10 = 0. These are diagnostic classical baselines, not
a fitted marked point process and not claimed equivalent to HGDHE.

Candidate construction plus scoring completed on CPU and produced the checked-in
CSV tables. We do not report wall-clock comparisons across published systems:
hardware and preprocessing are not matched. No neural model, hyperparameter
search, or test-set tuning was run.
