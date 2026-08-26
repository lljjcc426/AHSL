# S2.0 Benchmark Audit

## Frozen definition

An undirected event is identical iff its member set is identical. Events at an
identical timestamp remain in the same chronological block. We keep duplicate
events, remove singletons, and use 70/15/15 chronological splits. Counts below
come from `results/s2_0/raw/dataset_audit.csv`.

## Inventory

| Dataset | Domain / event | Dir.? | usable events | nodes | unique sets | span / resolution | median / p95 | >=3 / >=4 | test repeat | novel test | new-node event | license | existing protocol | main caveat |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---|---|---|
| congress-bills | political / bill cosponsors | no | 127,127 | 1,718 | 104,039 | through 2000; day | 6 / 68 | 74.74% / 65.46% | 18.84% | 15,477 | 1.29% | CC BY 4.0 via XGI | temporal hyperedge benchmarks | size up to 400; 52.23% of test events use a node absent at test start, but most such nodes arrive earlier in test |
| tags-ask-ubuntu | discussion / question tag set | no | 219,076 | 3,021 | 145,053 | source-relative timestamps | 3 / 5 | 65.82% / 32.98% | 40.57% | 19,530 | 0.11% | CC BY 4.0 via XGI | HyperSearch and temporal prediction | timestamps decode to relative years, not meaningful calendar dates |
| email-eu | communication / recipient set | no | 209,508 | 986 | 24,520 | through 2005; seconds | 2 / 5 | 17.29% / 8.71% | 91.25% | 2,749 | 0.07% | CC BY 4.0 via XGI | temporal hyperedge prediction | fails high-order threshold; sender role absent |
| email-enron | communication / recipient set | no | 10,454 | 143 | 1,459 | through 2001; seconds | 2 / 5 | 24.05% / 12.27% | 87.18% | 201 | 0.13% | CC BY 4.0 via XGI | temporal hyperedge prediction | too few novel test sets; sender role absent |
| contact-high-school | proximity / simultaneous contact set | no | 172,035 | 327 | 7,818 | 2013; 20 s | 2 / 2 | 4.68% / 0.34% | 97.04% | 764 | 0% | CC BY 4.0 via XGI | temporal higher-order interaction | effectively pairwise and recurrence-dominated |
| contact-primary-school | proximity / simultaneous contact set | no | 106,879 | 242 | 12,704 | relative 20 s | 2 / 3 | 9.12% / 0.45% | 93.80% | 994 | 0% | CC BY 4.0 via XGI | temporal higher-order interaction | effectively pairwise and just misses novel-count threshold |
| ndc-classes | drug / class label set | no | 46,285 | 1,149 | 1,049 | through 2015; day | 2 / 7 | 44.90% / 29.11% | 98.50% | 104 | 0.68% | CC BY 4.0 via XGI | temporal hyperedge prediction | almost pure exact-set recurrence |
| ndc-substances | drug / substance label set | no | — | — | — | — | — | — | — | — | — | CC BY 4.0 via XGI | advertised temporal collection | current HIF lacks `edges`; unusable without replacing the source artifact |

## D1–D8 survival

Only `tags-ask-ubuntu` and `congress-bills` pass all eight requirements under
the frozen thresholds. They supply distinct domains, more than 1,000 test
events, substantial size >=3 and >=4 mass, and large novel-set subsets.
`email-eu` has enough novel sets but fails D3. Contact data fail D3 and/or D4;
Enron and NDC fail D4. This is a two-dataset pass with no margin for losing a
survivor.

The event log records occurrence, not causality or the unique possible event.
Absence is treated as absence from the observed log only. The two survivors
have comparatively direct public event semantics, but this does not establish
complete coverage of every real-world action.
