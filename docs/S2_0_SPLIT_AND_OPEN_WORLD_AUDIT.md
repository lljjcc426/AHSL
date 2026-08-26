# S2.0 Split and Open-World Audit

## Protocol

The primary split is chronological 70/15/15. Boundaries are moved so identical
timestamps never straddle partitions. All histories, node statistics, pair
statistics, exact-set counts, and generated candidates are constructed from
train plus validation only before testing. Unit tests verify chronological
ordering and absence of future leakage.

| Dataset | train / validation / test | exact set in train | exact repeat during sequential test | novel test | test events with a new node | cardinality shift note |
|---|---:|---:|---:|---:|---:|---|
| tags-ask-ubuntu | 153,353 / 32,862 / 32,861 | 38.30% | 40.57% | 19,530 | 0.11% | bounded at five; high-order mass remains large |
| congress-bills | 89,001 / 19,057 / 19,069 | 11.00% | 18.84% | 15,477 | 1.29% | p95 68 and maximum 400; severe large-set/search regime |

“Exact in train” freezes history at the start of validation/test construction;
“sequential test repeat” allows an earlier test event to become history. They
answer different questions and must not be interchanged.

## Open-world strata

- `REPEATED-SET`: exact identity occurred earlier.
- `NOVEL-SET`: exact identity never occurred earlier.
- `NOVEL-SET / SEEN-NODES`: novel identity and every member is known.
- `NEW-NODE EVENTS`: at least one member is unseen at the prediction time.
- `ALL-NEW-TOGETHER`: every member is unseen.

Relative to the frozen train+validation vocabulary, 52.23% of Congress test
events contain a node absent at test start; after nodes are admitted as they
first appear, only 1.29% are new-node events at prediction time. These are
different estimands. Ubuntu is nearly transductive (0.11% prequential churn).
Without node attributes or a declared arrival mechanism, predicting an unseen
identifier is undefined for frequency/embedding scorers; this is a benchmark
specification gap, not evidence for a new architecture.

Pair and node overlap are computed only from past events; cardinality and
activity shifts are reported through time-block statistics rather than random
splits. Calendar labels for Ubuntu are not interpreted because its HIF times are
source-relative.
