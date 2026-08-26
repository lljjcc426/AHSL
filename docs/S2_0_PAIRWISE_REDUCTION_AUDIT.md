# S2.0 Pairwise Reduction Audit

## Construction

From history, each event contributes to node counts, every member pair's
co-occurrence count, an exponentially decayed pair count (`pair_hawkes`), and
every member triple's support. Candidate scores are node-frequency log product,
pair sum, minimum pair support, decayed pair sum, and triple support. All are
fixed count rules; no parameters are learned on test events.

Pairwise projection is not injective. For example, the three size-2 events
`{a,b}`, `{a,c}`, `{b,c}` and the single size-3 event `{a,b,c}` have the same
unweighted clique projection but different event identities. Exact-set metrics
preserve this ambiguity; clique-level metrics erase it. A unit test freezes the
example.

## Complete-set retrieval

| Dataset / subset | pair method with strongest Recall@10 | Hit@1 | Recall@10 | MRR | candidate recall |
|---|---|---:|---:|---:|---:|
| Ubuntu / all | pair minimum | 0.128% | 1.260% | 0.502% | 38.96% |
| Ubuntu / novel | pair Hawkes by MRR | 0 | 0 | 0.000611% | 0.973% |
| Ubuntu / size >=3 | pair Hawkes | 0.154% | 0.224% | 0.192% | 25.20% |
| Ubuntu / size >=4 | pair Hawkes | 0.286% | 0.417% | 0.356% | 15.93% |
| Congress / all | pair minimum by MRR | 0 | 0 | 0.00459% | 11.23% |
| Congress / novel | pair minimum by MRR | 0 | 0 | 0.000741% | 0.330% |
| Congress / size >=3 | pair Hawkes by MRR | 0 | 0 | 0.000246% | 1.20% |
| Congress / size >=4 | pair Hawkes by MRR | 0 | 0 | 0.000257% | 0.55% |

Triple support slightly raises Ubuntu size>=3 Recall@10 to 0.259% and size>=4
to 0.483%, but novel Recall@10 remains zero. Thus pairwise methods do not solve
complete-set retrieval under this search. This is not clean proof of a learned
high-order residual: candidate recall below 1% on novel truths confounds scorer
quality with search failure. G6 passes only in the literal “not solved” sense;
G9 fails because no modern-vs-classical scoring residual is isolated.
