# N1.0 split and leakage audit

All split figures below are diagnostic on the 712 qualified tasks. They do not reopen the failed representability gate.

## Top-level family split

A deterministic holdout uses `DNA Repair`, `Hemostasis`, `Immune System`, and `Vesicle-mediated transport` as test families: 591 train and 121 test tasks. Pathway-hierarchy overlap is zero by construction.

## Identifier overlap

| Object | Train unique | Test unique | Intersection | Test overlap |
|---|---:|---:|---:|---:|
| reaction IDs | 4,671 | 1,098 | 25 | 2.28% |
| entity IDs | 9,169 | 2,202 | 288 | 13.08% |

The low but nonzero overlap means a future scorer must not use reaction-ID lookup parameters. Entity overlap is expected biologically but precludes claims of fully unseen molecular entities.

## Reaction-disjoint stress split

Grouping tasks into connected components under shared reaction IDs yields 628 components; the largest contains 29 tasks. A deterministic approximately 80/20 component split gives 570 train and 142 test tasks with zero reaction overlap, covering 27 and 18 families respectively. It is useful as a stress test, but both sides do not reach the protocol's 300-task scale; it is not a feasible primary evidence split.

## Temporal split

Comparing V97 pathway IDs/reaction sets to V89 gives 104 NEW, 71 MODIFIED, and 1,445 UNCHANGED V97 tasks. Only 175 tasks contain new or changed supervision. Temporal status is **WEAK**: historical feature isolation is possible, but changed-task scale is modest and the upstream task class already fails representability. Unchanged pathways are not called temporal OOD.

## Pathway overlap

Across all 1,620 candidates, 1,311,390 pathway pairs were checked. Only 438 pairs share any reaction; one pair is exactly duplicated and 22 are strict subset relations. Jaccard counts are: 1,310,952 at zero; 330 in (0,.1]; 85 in (.1,.25]; 17 in (.25,.5]; three in (.5,.75]; two in (.75,1); one at 1.

## Recommended split if the upstream gate had passed

The family-disjoint 591/121 split would be the primary evaluation, with the 570/142 reaction-disjoint split as a stress test and V89→V97 changed tasks as weak temporal evidence. Stable IDs, pathway hierarchy, and current-release annotations would be excluded from features. Because N1.0-C closes CertPath, this is an audit conclusion rather than an authorized N1 protocol.
