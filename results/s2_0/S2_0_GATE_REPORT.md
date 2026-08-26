# S2.0 Gate Report

## 1. Executive decision

**S2.0-E — NO-GO: PRIOR-ART SATURATION.** Two real datasets validate that
novel high-order complete-set forecasting is a meaningful empirical target, and
sampled-negative evaluation is decisively misleading. However, HyperSearch
already combines temporal scoring, novel-set evaluation, unconstrained safe
search, exact complete-set Recall, and multiple real temporal datasets. Local
candidate recall also fails, so no isolated learning residual justifies a new
model.

## 2. Search methodology

Search date 2026-08-27. Forty-four works were screened, nineteen deeply
reviewed, and ten of the deep reviews are from 2024–2026. Evidence came from
full papers, publisher/proceedings records, official data pages, and source
repositories. Exact queries and ledger are in `docs/S2_0_SEARCH_LOG.md`.

## 3. Exact structure-learning task

Given events through time `t`, rank the next complete undirected member set.
Identity is exact set equality, not clique-projection equality. Primary target
is a novel set; repeated, seen-node novel, new-node, and cardinality strata are
reported separately. No fixed candidate list is supplied to the predictor.

## 4. Dataset inventory

Eight XGI/Cornell collections were inspected. Seven current HIF files parsed;
`ndc-substances` lacked `edges`. Ubuntu tags and Congress bills pass D1–D8.
Details and licenses are in `docs/S2_0_BENCHMARK_AUDIT.md`.

## 5. Event cardinality audit

Ubuntu has median/p95 size 3/5, with 65.82% size >=3 and 32.98% size >=4.
Congress has 6/68, with 74.74% and 65.46%. Other loaded datasets either fail
the high-order threshold or the novel-set threshold.

## 6. Repeated-set audit

Sequential test exact-repeat rates are 40.57% Ubuntu and 18.84% Congress. In
contrast, the five other loaded datasets range from 87.18% to 98.50% except
none; they are unsuitable as primary structure-discovery evidence.

## 7. Novel-set audit

Ubuntu contains 19,530 novel test events and Congress 15,477, clearing the
predeclared 1,000-event gate in distinct domains. Novel means not previously
observed at prediction time.

## 8. Node-churn audit

Prequential new-node event rates are 0.11% Ubuntu and 1.29% Congress. Relative
to the fixed train+validation vocabulary, however, 52.23% of Congress test
events contain a node absent at test start, because nodes arrive during test.
An unseen identifier cannot be ranked without features or a declared arrival
vocabulary; the two churn definitions are kept separate.

## 9. Temporal split

Chronological 70/15/15 event blocks are 153,353/32,862/32,861 for Ubuntu and
89,001/19,057/19,069 for Congress. Identical timestamps are never split. All
statistics use past events only.

Local retrieval uses train+validation as a frozen history and predicts a
held-out future batch, matching HyperSearch's evaluation form. Repeat and churn
classes are prequential. The experiment is not presented as a recomputed
next-event ranking after every test event.

## 10. Negative-sampling audit

For 250 novel seen-node events of size <=10, each positive was compared with
100 random same-cardinality or one-member-corruption negatives. Random-negative
Recall@10 reaches 93.2% Ubuntu and 94.8% Congress; harder corruption reduces it
to 80.0% and 75.2% respectively.

## 11. Classification-versus-retrieval comparison

Every implemented scorer has novel search-controlled Recall@10 = 0 on both
survivors. Sampled-negative results above 75% therefore coexist with zero exact
open retrieval. Top-method identity also changes across protocols; sampled
classification is secondary evidence only.

## 12. Candidate-space analysis

With seen nodes and only cardinalities 2–5, the universe is
1,968,274,898,078,042 sets for Ubuntu and 86,025,015,195,889 for Congress.
Congress actually contains sets up to size 400.

## 13. Candidate-generation recall

The frozen one-member replacement generator recalls only 0.973% of Ubuntu and
0.330% of Congress novel events, versus 94.62% and 58.21% of repeats. Ranking
inside this pool cannot validate open-world structural forecasting.

## 14. Search feasibility

Naive enumeration is infeasible. HyperSearch demonstrates feasible top-k
branch-and-bound for its anti-monotone upper bound on six temporal datasets,
but the local heuristic is not adequate and large/open-node Congress remains
ill-specified. Search is a dominant difficulty.

## 15. Recurrence/frequency baselines

Best aggregate exact frequency results: Ubuntu Hit@1 0.207%, Recall@10 1.330%;
Congress 0.461%, 0.577%. Recency gives 0.018%/0.110% and 0/0.010%. All are zero
on novel-set Recall@1/10.

## 16. Pairwise baselines

Pair sum, pair minimum, node product, and decayed pair-Hawkes proxy were tested.
They score artificial negatives well but have zero novel Recall@10. Because
novel candidate recall is below 1%, the experiment cannot isolate whether a
better score would exploit irreducible higher-order information.

## 17. Point-process/classical baselines

The local decayed pair count is a fixed Hawkes-style proxy, not a trained marked
TPP. It reaches random-negative Recall@10 93.2%/94.8% but zero novel open
retrieval. HGDHE and related TPPs are audited from their published protocols;
they rely on sampled/constructed event candidates rather than safe full search.

## 18. Modern method audit

CAt-Walk, FastHeP, Hyper-SAGNN, and most modern encoders primarily classify
supplied/generated candidates. HGDHE and directional TPPs model temporal event
intensity but do not supply HyperSearch-style complete search. HyperSearch is
the strongest correct-protocol comparator.

## 19. Exact-set retrieval results

Local best all-test Recall@10 is 1.330% (Ubuntu exact frequency) and 0.577%
(Congress exact frequency). These gains are mostly repeat retrieval, not novel
group formation.

## 20. Novel-set results

All local methods: Hit@1 = 0 and Recall@10 = 0 on both datasets. Nonzero MRRs
for structural scorers are tiny and arise for the <1% of novel truths included
in the candidate pool.

## 21. Size>=3/4 results

Ubuntu triple support is locally best: Recall@10 0.259% for size >=3 and 0.483%
for size >=4. Congress structural Recall@10 is zero in both strata; recency
alone reaches 0.014% and 0.016% from rare repeated sets.

## 22. Directed-event audit

The HIF inputs used here are undirected and do not retain email sender roles.
Directed identity is implemented and unit-tested, but no directed dataset passes
D1–D8 for empirical claims. Published directional TPP work already covers the
adjacent directed formulation. Direction cannot be appended merely for novelty.

## 23. Calibration audit

Local count scores are unnormalized, so NLL and probability calibration are not
applicable. Temporal intensities in published TPPs do not automatically define
a tractable normalized distribution over all possible sets. Calibration remains
unmeasured, not an established novelty claim.

## 24. Memorization residual

Large novel populations remain after exact memorization, so the global
memorization kill rule does not fire on the two survivors. Yet all local novel
retrieval collapses because search misses the truth.

## 25. Pairwise residual

Pairwise projection does not solve exact retrieval under the tested search, but
search confounding prevents attribution to missing high-order learning. There is
no measured pairwise-versus-higher-order residual under a high-recall common
candidate universe.

## 26. Modern-method residual

HyperSearch leaves numerical error, open-node support, calibration, and
next-event normalization. The first is already its method domain; the others
require exogenous node support or move to generative/point-process modeling.
No clean broad structure-learning residual is isolated.

## 27. Closest prior art

HyperSearch uses chronological 80/20 splits for six timestamped datasets,
excludes train-observed test identities and unseen test nodes, searches unseen
sets with safe pruning, and reports exact Recall at K proportional to test-set
size. On Ubuntu it reports 12.0/15.4/20.6% at K=1x/2x/5x. Neural reranking does
not consistently improve it. This is the decisive G8 collision.

## 28. Candidate concrete problems

A novel-set temporal retrieval; B open-node plus novel-set forecasting; C
calibrated complete-set forecasting; D directed role-aware forecasting; E
learned scoring plus safe combinatorial search. None survives all hard gates.

## 29. Candidate scores

| candidate | A | B | C | D | E | F | G | H | I | J | K | L | total /60 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| A novel-set temporal retrieval | 5 | 4 | 5 | 5 | 4 | 3 | 1 | 5 | 2 | 3 | 3 | 4 | 44 |
| B open-node + novel-set | 5 | 2 | 1 | 4 | 3 | 3 | 2 | 3 | 1 | 3 | 2 | 3 | 32 |
| C calibrated complete-set | 4 | 2 | 3 | 4 | 3 | 3 | 3 | 3 | 1 | 4 | 2 | 2 | 34 |
| D directed role-aware | 5 | 1 | 1 | 4 | 3 | 3 | 2 | 3 | 1 | 4 | 1 | 3 | 31 |
| E learned score + safe search | 4 | 4 | 5 | 4 | 4 | 3 | 1 | 5 | 4 | 2 | 3 | 4 | 43 |

Hard gates override these descriptive scores.

## 30. Publication feasibility

No broad new-method paper is supported. A careful independent reproduction and
protocol paper could be plausible for TMLR or a data-mining/network-science
workshop only after recovering exact HyperSearch preprocessing and running a
matched search baseline. KDD/WWW/WSDM and general ML venues are weak for the
current residual; this is venue fit, not acceptance probability.

## 31. Strongest evidence FOR continuation

Two distinct real domains contain tens of thousands of novel high-order test
events, and protocol changes produce 75–95% sampled Recall@10 versus 0% local
open retrieval. The target is empirically meaningful and evaluation matters.

## 32. Strongest evidence AGAINST continuation

HyperSearch already occupies the correct seen-node novel-set retrieval task and
shows that a non-neural empirical score with safe search outperforms neural
reranking. Locally, candidate recall below 1% means the remaining failure is not
identified as learnable high-order structure.

## 33. Hard-gate table

| gate | result | evidence |
|---|---|---|
| G1 two strong real datasets | PASS | Ubuntu and Congress pass D1–D8 |
| G2 material novel-set population | PASS | 19,530 and 15,477 novel test events |
| G3 active high-order cardinality | PASS | both exceed 30% >=3 and 10% >=4 |
| G4 sampled negatives insufficient | PASS | 75–95% sampled vs 0% novel open Recall@10; rankings change |
| G5 recurrence does not dominate novel task | PASS | novel frequency/recency Recall@10 = 0 |
| G6 pairwise does not solve complete retrieval | PASS | novel Recall@10 = 0; attribution remains confounded |
| G7 search feasible enough for evaluation | PASS | HyperSearch demonstrates safe retrieval on six bounded seen-node temporal datasets; local heuristic itself fails |
| G8 no same-protocol prior art | FAIL | HyperSearch direct collision |
| G9 measurable modern/classical residual | FAIL | no matched high-recall search isolates a learning gain |
| G10 residual remains structure learning | FAIL | residual is search, node arrival, or adjacent generative TPP specification |

## 34. Final decision

**S2.0-E — NO-GO: PRIOR-ART SATURATION.** G8 is the decisive classification;
G9 and G10 independently prevent continuation. S2.0-F was considered, but
the user-requested project is structure learning and the strongest searchable
formulation is already occupied, so prior-art saturation is the more precise
single decision.

## 35. Exact next action

Freeze S2.0. Do not create `docs/S2_CONCRETE_PROBLEM_PROPOSAL.md`, do not train
a temporal HGNN, and do not automatically reopen another S0 candidate. Return
the branch to project review. A later, separately authorized task may reproduce
HyperSearch preprocessing as a benchmark study, but it is not the next phase of
this structure-learning line.
