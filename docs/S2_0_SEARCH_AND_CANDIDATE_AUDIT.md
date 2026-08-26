# S2.0 Search and Candidate Audit

## Declared local universe

History is train plus validation. We retain all observed historical sets for
recurrence statistics. For structural scoring, candidates are (i) observed
sets of size <=10 and (ii) deterministic one-member replacements from the
5,000 most frequent source sets, at most two replacements per position and
50,000 candidates. The generator sees no test truth. This is type D (heuristic),
not a completeness-guaranteed algorithm. The ranking remains frozen across the
held-out future batch; it is a candidate/search stress test, not a sequentially
updated next-event system.

| Dataset | seen nodes | test max size | all subsets size 2–5 | observed history sets | generated novel | scored universe | novel candidate recall | repeat candidate recall |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| tags-ask-ubuntu | 2,984 | 5 | 1,968,274,898,078,042 | 125,523 | 3,743 | 129,266 | 0.973% | 94.62% |
| congress-bills | 1,596 | 400 | 86,025,015,195,889 | 88,917 | 16,483 | 64,259 | 0.330% | 58.21% |

The bounded count shown for Congress covers only cardinalities 2–5 and already
exceeds 86 trillion; its real maximum is 400. Exhaustive enumeration is not an
evaluation option. The local generator is fast enough to score tens of
thousands of sets, but its candidate recall is scientifically inadequate.

## Safe search and collision

HyperSearch searches unseen subsets with depth-first branch-and-bound and an
anti-monotone upper bound, providing unrestricted search for its score rather
than pre-sampling negatives. Its published chronological novel-hyperedge
evaluation therefore demonstrates that safe top-k search can be feasible for
six real datasets under bounded cardinality. Its theoretical cost and ILP
components remain substantial, and its released repository omits the exact
preprocessing/split artifacts required for a faithful local rerun.

For the frozen-history Congress batch, 52.23% of test events contain a node
absent at test start; under prequential admission, the actual new-node event
rate is only 1.29%. No candidate procedure can emit a currently unseen
identifier without node features or an arrival vocabulary. For Ubuntu seen-node
sets, HyperSearch shows that safe search is feasible but also directly occupies
the intended task. The remaining gap is therefore either prior-art-covered
scoring+search or an adjacent search/new-node specification problem, not a clean
new structure-learning target.
