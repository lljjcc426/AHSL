# S2.0 Modern Method Audit

## Complete-set prediction versus supplied-candidate classification

| Method | predicts/searches complete sets? | supplied-candidate classification? | chronological? | novel-set open retrieval? | normalized probability? |
|---|---:|---:|---:|---:|---:|
| HyperSearch | yes | no in primary protocol | yes | yes, seen nodes | no |
| HGDHE/HGBDHE | scores temporal event sets and time | yes for evaluation components | yes | no completeness-guaranteed search | temporal intensity, not tractable probability over all sets |
| Directional temporal TPP | staged directed set generation/scoring | partly | yes | not guaranteed | intensity-based |
| CAt-Walk | no open generator | yes | can be inductive | no | classifier score |
| FastHeP | candidate scoring | yes | yes | no demonstrated safe full search | no established normalized set distribution |
| RRHyperTPP | event/intensity model | NCE-based | yes | no safe full search | approximate intensity objective |
| NHP | event/intensity model | negative-event contrast | yes | no safe full search | point-process likelihood under sampled event construction |
| Hyper-SAGNN | no | yes | no | no | classifier score |
| S3Hyper | no open temporal generator | yes | no/benchmark-specific | no | classifier score |

Headline AUC/AP is not comparable with complete-set Recall. CAt-Walk and most
representation methods answer “does this supplied set look positive?”;
HyperSearch answers “which unseen set should be returned from the combinatorial
space?” Only the latter collides with the primary S2 estimand.

## Reproducibility

HyperSearch code was inspected locally. Search code is public, but the released
repository does not package exact preprocessing and split artifacts. CAt-Walk
has public paper/code but uses a candidate classification protocol. Publication
metadata for HGDHE, directional TPP, FastHeP, NHP and recent methods was checked
through publisher/proceedings/arXiv records; no inaccessible method was
rewritten. Seeds and dependencies are method-specific and not uniformly
recoverable, so no false “fully reproducible” label is assigned.

## Strongest modern reference point

HyperSearch is the strongest comparable baseline and a novelty collision, not
a locally reproduced number. It reports exact novel-hyperedge Recall at
dataset-scaled K on six datasets, including Ubuntu 12.0/15.4/20.6% at
K=1x/2x/5x the number of future new hyperedges. Its neural refinement does not
consistently improve its empirical search score, which further weakens the case
that the remaining bottleneck demands a new temporal HGNN.
