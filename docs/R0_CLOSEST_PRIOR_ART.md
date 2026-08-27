# R0 Closest Prior Art

| work | exact problem | strategy/decomposition | high-order interface | benchmark evidence | overlap and residual |
|---|---|---|---|---|---|
| Dechter, bucket elimination | general graphical-model/CSP elimination | variable/bucket order | native scopes become buckets | classical benchmark literature | exact R0 engine and strongest baseline |
| Lauritzen & Spiegelhalter, junction tree | exact probabilistic propagation | triangulation/clique tree | factors assigned to bags | medical/PGM lineage | exactness and reuse already classical |
| Darwiche, recursive conditioning | exact BN inference | decomposition/caching policy | graph/factor structure | BN benchmarks | safe time-space strategy, graph-centric |
| Dechter & Mateescu, AND/OR search | exact graphical-model search | pseudo-tree, branch and caching | factor/constraint scopes | PGM/CSP | local-decision candidate becomes generic search guidance |
| Gottlob et al., hypertree decompositions | CQ/CSP evaluation | guarded hypergraph decomposition | direct | query/CSP | theoretical core of candidate B |
| Fischl, Gottlob & Pichler | GHD/FHD recognition | exact recognition under restrictions | direct | theory | blocks casual learned-width claims |
| Abo Khamis, Ngo & Rudra, FAQ | semiring factor aggregates | variable order/decomposition | fractional covers/FAQ-width | database and inference examples | candidate E closely matches join planning |
| Arun et al., JoinInfer | exact PGM marginals | GHD/WCOJ vs pairwise, data-driven hybrid | sparse high-arity factors, FHW/support metrics | 52 networks; up to 630x | closest complete R0 system; lacks family-disjoint learned predictor |
| Gottlob et al., fast parallel HD (2024) | exact HD construction | balanced separators/parallel search | direct | all 3,648 HyperBench instances | recent strong classical candidate-B baseline |
| Lanzinger & Razgon (STACS 2024) | approximate GHW under bounded intersections | parameterized decomposition algorithm | direct | theory | occupies structural approximation interface |
| Korchemna et al. (2024) | approximate FHW | approximation algorithms | direct | theory | further shrinks unexplored width-learning rationale |
| He et al., branch-and-bound FHD | FHD computation/query evaluation | exact search and LP bounds | direct | 3,648 HyperBench plus DB evaluation | classical search already exploits strong bounds |
| cotengra | exact tensor contraction | contraction-tree/hyperparameter search | tensors as factors | quantum/tensor networks | VE ordering without semiring-specific residual collides |
| Meirom et al., RL-TNCO | exact contraction-cost planning | learned/RL order | network structure | tensor benchmarks | direct learned-order collision |
| modern learned CP/SAT branching | exact search | learned branch/priority/configuration | optional constraint scopes | accepted solver benchmarks | surviving local policy is generic solver learning |
| learned query optimizers | exact relational answer | learned cardinality, cost and join order | join hypergraph | JOB/TPC-style workloads | cost-model candidate is nearly identical |
| learning-augmented algorithms with explicit predictors (NeurIPS 2024) | guaranteed algorithms with predictions | predictor plus robust fallback | problem dependent | theory tasks | supplies contract but no factor-inference residual |

No single prior work exactly satisfies fixed high-order factors, a learned
strategy, exact certificate, two real factor benchmark families and
family-disjoint generalization. The no-go arises because the missing pieces do
not align: where high-order theory is indispensable, downstream labeled
workloads are missing; where strategy-learning benchmarks exist, the task is
generic solver/query/tensor optimization.
