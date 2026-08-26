# S2.0 Evaluation Audit

## Protocols compared

1. **Easy sampled negatives:** 250 novel, seen-node, size <=10 truths per
   survivor; each truth is ranked against 100 random same-cardinality sets.
2. **One-member corruption:** the same truths, with 100 negatives formed by
   replacing one member.
3. **Search-controlled retrieval:** rank the truth against the fixed open-world
   search universe built without access to test truths. Missing truths receive
   a conservative rank beyond the candidate list.
4. **Full retrieval:** executed only in unit tests on a toy universe. On the
   real datasets, even the size 2–5 seen-node universe is too large to enumerate.

The test truth is never inserted into the real search universe. That choice is
essential: inserting it would convert candidate generation into supplied-
candidate classification.

The local retrieval experiment is a **frozen-history future-batch audit**:
train+validation define one ranking and the full test block supplies truths.
Repeat/churn labels are additionally computed prequentially. It therefore
matches HyperSearch's held-out-future retrieval formulation but is not a
reproduction of a freshly recomputed `e_(t+1)` ranking after every test event.
Those two protocols are not conflated in the conclusions.

## Protocol gap

| Dataset | protocol | easiest strong result (Recall@10) | top method |
|---|---|---:|---|
| tags-ask-ubuntu | random same-cardinality | 93.2% | pair sum / pair Hawkes |
| tags-ask-ubuntu | one-member corruption | 80.0% | pair sum |
| tags-ask-ubuntu | search-controlled, novel | 0% | all methods tied on Recall@10 |
| congress-bills | random same-cardinality | 94.8% | pair Hawkes |
| congress-bills | one-member corruption | 75.2% | pair Hawkes |
| congress-bills | search-controlled, novel | 0% | all methods tied on Recall@10 |

Top-method identities reverse. For Congress, pair Hawkes wins both sampled
protocols but pair minimum has the highest search-controlled MRR; Spearman is
0.818 and Kendall tau 0.700. For Ubuntu, one-member corruption prefers pair sum
while search-controlled retrieval prefers pair Hawkes; Spearman is 0.818 and
Kendall tau 0.600. This is material protocol dependence, not sampling noise
from a marginal score change.

## Metrics and recommendation

Primary reporting must use exact-set Hit@1, Recall@10, MRR, average true rank,
and candidate recall, stratified by repeat/novel/new-node/cardinality. Jaccard,
member precision/recall/F1, and cardinality error are diagnostics only; a model
can obtain good member overlap while never recovering the event identity.

Recommended protocol: chronological novel-set retrieval with a declared
complete or completeness-audited search procedure. Sampled-negative AUC or
Recall is secondary. Normalized NLL is reportable only if a method defines a
proper probability over the declared universe.
