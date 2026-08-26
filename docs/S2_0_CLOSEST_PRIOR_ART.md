# S2.0 Closest Prior Art

## Direct comparison

| Work | task / data | temporal split | universe / negatives | score and search | metrics | repeat / novel | directed | code / reproducibility | overlap with S2 |
|---|---|---|---|---|---|---|---|---|---|
| HyperSearch (ICDM 2025) | predict unseen hyperedges; six temporal datasets | chronological 80/20 | `2^V \\ E`, sizes capped by dataset; no sampled negatives in primary retrieval | empirical score, DFS and anti-monotone bound | exact Recall@K | removes train-observed sets from test target; evaluates new hyperedges | no | public Java search; exact preprocessing/data split absent | **direct collision:** temporal, novel complete sets, unrestricted safe search, multiple real data |
| Prediction Is NOT Classification (ICDMW 2024) | hyperedge prediction formulation; multiple benchmarks | benchmark-dependent | contrasts artificial-negative classification with actual prediction | simple rules and benchmark audit | prediction metrics vs classification metrics | exposes recurrence/candidate artifacts | no | paper/protocol available | supplies the core evaluation objection; reports ranking disagreement |
| HGDHE/HGBDHE (AAAI 2023) | next temporal hyperedge and time; Enron, EU, Congress, NDC | chronological event sequences | negative hyperedges sampled for membership/type terms | dynamic node embeddings + temporal point process | MRR/AUC/type/time metrics | no isolated unrestricted novel-set retrieval | no | paper metadata public; exact end-to-end reproduction not established here | temporal scoring and time, but candidate classification rather than open search |
| Directional temporal TPP (AAAI 2025; preprint 2023) | source/target hyperedge and time | chronological | staged node/size/adjacency candidates and negative sampling | directed embeddings + marked TPP | ranking/time metrics | no completeness-guaranteed novel-set retrieval | yes | publication/paper available | covers direction and time; search protocol weaker than S2 target |
| CAt-Walk (NeurIPS 2023) | inductive candidate-hyperedge classification | supplied train/test candidates | negative hyperedges supplied/generated | set walks + neural classifier; no open search | AUROC/AP | not primary exact next-set retrieval | no | public paper/code | strong representation baseline, but wrong primary estimand for S2 |
| FastHeP (KDD 2025) | fast temporal hyperedge representation/prediction | temporal benchmarks | candidate-scoring protocol | efficient temporal representation; no unrestricted complete-set search demonstrated | classification/ranking metrics | no strong novel-set open-world primary protocol | no | metadata confirmed; ACM artifact access limited in this audit | recent temporal scorer; does not remove HyperSearch collision |
| NHP (CIKM 2020) | neural higher-order event occurrence/time | sequential | contrastive negative event sets | neural point process | likelihood/ranking/time | recurrence not isolated as open retrieval | no | paper/code family public | foundational point-process scorer, no safe full-set retrieval |
| RRHyperTPP (2024) | recurrent-relation temporal hyperedge point process | sequential | NCE approximates exponential event-space terms | neural TPP | likelihood/ranking/time | no unrestricted novel-set exact retrieval | no | preprint available | shows normalization/search difficulty rather than solving it |
| Simplicial Closure (PNAS 2018) | formation of higher-order simplex from faces | chronological higher-order data | candidate tuples whose faces appeared | closure probability / statistics | closure rates, prediction diagnostics | targets closure candidates, not arbitrary next set | no | data/code pages public | essential classical formation baseline; candidate universe constrained |
| Hyper-SAGNN (ICLR 2020) | static hyperedge existence classification | supplied positives and negatives | sampled negatives | self-attention set score | AUROC/AP | no temporal novel-set retrieval | no | public | representative “one more encoder” explicitly excluded |

## Collision judgment

HyperSearch defines the target as unseen sets in `2^V \\ E`, performs
unconstrained top-k search with safe pruning, uses chronological splits on six
timestamped real datasets, and evaluates exact Recall@K. Its published Ubuntu
Recall at K equal to 1x/2x/5x the test-positive count is 12.0%/15.4%/20.6%; these
numbers must not be relabeled Recall@1 or Recall@10.

It excludes test events containing unseen nodes and is batch future-set
retrieval rather than a normalized next-event distribution. Therefore it does
not solve open-node identity or calibrated next-event time. Those residuals do
not rescue a broad structure-learning program here: open-node identity is
undefined without features/arrival support, while normalized time-and-set
forecasting moves into marked point-process/generative modeling already covered
by HGDHE and directed TPP families. A different encoder atop the same
HyperSearch task would fail the novelty gate.

Reproducibility weakness is recorded rather than used as novelty: the public
HyperSearch repository contains the Java search implementation and relative
data paths, but not the paper's exact preprocessing, split files, or packaged
datasets. Reconstructing those unpublished choices was outside this no-new-model
gate and would not change task collision.
