# N0 publication feasibility

## Rank 1: CertPath

### Paper-level claim

Learn calibrated reaction costs across curated pathway instances, decode with an exact general directed-hyperpath solver, and issue a verifiable robust-optimality certificate or abstain to classical costs; test whether this improves held-out pathway recovery under pathway-family and temporal shift.

### Venue fit

| Venue family | Fit | Reasoning |
|---|---|---|
| RECOMB / ISMB / Bioinformatics | strong | exact pathway algorithms, real curated biology, and reproducible computational evaluation align directly |
| UAI / AISTATS | plausible | decision-focused uncertainty and calibrated abstention fit if the guarantee is nontrivial and experiments are broad |
| NeurIPS / ICML / ICLR | weak-to-plausible | would require a generalizable learning/robust-certificate theorem beyond one biological pipeline and very strong grouped/OOD evidence |
| CP / AAAI / IJCAI | plausible | exact constrained decoding plus learning-augmented search/decision formulation fits, though biological value must remain visible |
| Algorithms/journal crossover | plausible | Journal of Computational Biology, Algorithms for Molecular Biology, or INFORMS-style outlets fit an exact algorithm with empirical biology |

Expected publication level: **plausible**. A strong domain/theory paper is defensible; top general-ML positioning is not assumed.

### Minimum viable paper

- Central guarantee: a sufficient, efficiently checkable margin condition under which the decoded path remains optimal for every reaction-cost vector in a calibrated uncertainty set; otherwise abstain.
- Core algorithm: decision-focused nonnegative reaction-cost learner + exact Mmunin-equivalent decoding + robust margin check.
- Baselines: unit weights/Hhugin, hand-crafted provenance or atom-conservation weights, prediction-only reaction scorer, exact decoder without uncertainty certificate.
- Real benchmarks: versioned Reactome primary; NCI-PID/Pathway Commons historical external test. A second modern metabolic database is optional, not required for the first kill test.
- Primary metric: reaction-set F1 on group-disjoint held-out curated pathways, reported with precision/recall and certificate coverage.
- Decisive ablation: remove exact hyperpath decoding while retaining the same reaction scores; compare unconstrained top-k reactions and graph-shortest-path projection.
- Failure analysis: performance by tail arity, cycle presence, pathway family, release shift, and source specification.

### Reviewer stress test

1. **Why ML?** Curated pathways repeat reaction motifs and biochemical/provenance contexts across thousands of source–target decisions; unit weights explicitly ignore this signal. Group and temporal splits test whether signal transfers.
2. **Why hypergraphs?** A reaction requires all tail entities and produces a head set. Pairwise projection changes reachability and admits chemically invalid shortcuts.
3. **Why GHW/FHW instead of treewidth?** It should not use GHW/FHW. The indispensable theory is directed hyperpath reachability/optimality. Forcing width theory would weaken the project.
4. **Why not use the existing solver?** It is retained as the exact decoder and strongest baseline; the residual is the objective, because existing studies largely use unit/external weights.
5. **Why does exactness matter?** It ensures scores are compared over feasible reaction systems and prevents learned local scores from producing an invalid set. It is exact only under the learned objective, not a biological truth claim.
6. **Why is the benchmark realistic?** Reactome is expert-curated, versioned, open, and already used for pathway inference; however, supersource construction is imperfect and is explicitly stress-tested.
7. **Why is this not just a learned heuristic?** The learned object is a calibrated decision objective; decoding is exact; the certificate is deterministic conditional on the declared cost set; abstention preserves a classical fallback.
8. **What is new?** The joint decision-focused formulation, uncertainty-stability certificate, and leakage-resistant temporal/family protocol. Feeding a predictor into Mmunin without these is not novel enough.
9. **Does it generalize?** Only grouped and release-shift results can answer. Random-edge splits are not accepted evidence.
10. **Would anyone use it?** A positive result gives ranked feasible pathways with a confidence/abstention interface; a negative result establishes that learned reaction costs do not improve over curated structural priors.

### Resource analysis

- Data: tens of thousands of vertices/edges per union hypergraph and a few thousand target tasks; storage is modest.
- Labels: exact solves reported from seconds to at most tens of minutes. The first kill test needs only 300--500 tasks and cached exact solutions.
- Learning: start with linear/gradient-boosted cost model; one consumer GPU is optional, not required.
- Compute budget for kill test: <=500 CPU-hours total labeling/decoding, <=24 GPU-hours if a neural scorer is included, <=7 elapsed days on a small academic workstation/server.
- No proprietary infrastructure.

### Novelty level

Level 2 if and only if the certificate and decision-focused grouped/OOD evaluation are delivered. Level 1 if it is only a learned reaction score with exact decoding. Level 0 if it is only another HGNN link predictor.

## Why the other semifinals are not papers to pursue now

- HD/GHD selector: plausible CP/algorithm-engineering paper only with a new robust learning-augmented theorem and downstream solver, but current benchmark/novelty evidence is below threshold.
- WCOJ selector: excellent SIGMOD/VLDB fit in the abstract, but direct ADOPT and CIDR collisions make the proposed contribution incremental.
- Tensor ranking: direct collision makes it indefensible.
- Hypergraph partitioning: strong systems venues, but classical baselines and prior ML pruning require much larger infrastructure and a sharper novelty object.
- Sparse factor inference: UAI fit but no evidence that hypergraph width, rather than treewidth/domain size, is indispensable on accepted workloads.
