# N0 literature survey

## Coverage

N0 screened **80 primary works/resources** across 13 candidate families. **26 were substantive deep reads**, including **12 from 2024--2026**. “Deep” means the methods, experimental design, results, and limitations were inspected beyond title/abstract; it does not mean every appendix was line-edited. Bibliographic records are in `references/n0_references.bib` and exact query families are in `docs/N0_SEARCH_LOG.md`.

Legend: **D** deep read; **D-R** deep read dated 2024--2026; S screened.

## A. Learned database query optimization

| ID | Work | Read | Finding for N0 |
|---|---|---|---|
| A1 | AGM, Size Bounds and Query Plans for Relational Joins | S | fractional edge covers make the query hypergraph computationally meaningful |
| A2 | Ngo et al., Worst-case Optimal Join Algorithms | S | establishes the exact classical WCOJ baseline |
| A3 | EmptyHeaded | D | GHD-based plan generation is already systemized |
| A4 | Graphflow hybrid binary/WCO joins | D | data-dependent hybrid plans already address fixed-width limitations |
| A5 | Adopting WCOJ in relational DBs | S | mature hybrid classical baseline |
| A6 | ADOPT | D | direct RL + WCOJ + convergence/worst-case guarantee collision |
| A7 | SkinnerDB | S | RL adaptive join-order baseline |
| A8 | Bao | S | learned plan steering baseline |
| A9 | Balsa | S | learned optimizer with simulation/public JOB |
| A10 | BASE | D | cost labels and latency labels have materially different behavior/cost |
| A11 | LEON | S | learned plan comparison/steering collision |
| A12 | LEAP | **D-R** | 2025 learned comparator and progressive Spark plan search |
| A13 | STATS-CEB | S | realistic CE benchmark, but not native WCOJ-plan supervision |
| A14 | CardBench | **D-R** | 20 real DBs and thousands of queries; join transfer remains hard |
| A15 | JOB-Complex | **D-R** | 30 queries, 5--14 joins; stronger evaluation but still not a GHD learning benchmark |
| A16 | Adaptive Factorization Using Linear-Chained Hash Tables | **D-R** | direct ML choice of factorized/WCOJ runtime mode; heuristics comparable |

Conclusion: high importance and excellent benchmarks, but the precise learned-structural niches are occupied. Many graph-query workloads have rank-2 relations, weakening G3 for a hypergraph-theory paper.

## B. Exact inference in high-order factor graphs

| ID | Work/resource | Read | Finding |
|---|---|---|---|
| B1 | UAI 2022 inference competition/tasks | D | public PR/MAR/MPE/MMAP workload, fixed CPU/RAM/time tracks |
| B2 | UAI 2014/2016 formats and instances | S | high-order factors exist; sparse format available |
| B3 | Toulbar2 | D | extremely strong exact CFN/additive graphical-model baseline |
| B4 | Merlin | S | public exact/approximate solver baseline |
| B5 | Peyrard et al., Variable Elimination and Beyond | S | primal treewidth is the standard exact-complexity control |
| B6 | Tensor Variable Elimination for Plated Factor Graphs | S | repeated factor structure already exploited algebraically |
| B7 | Exact Inference in High-order Structured Prediction | D | exact convex recovery is theoretically strong but benchmark is narrow/generative |
| B8 | Inference in Higher Order Undirected Graphical Models and BPO | **D-R** | 2025 LP formulations/code occupy a broad exact high-order niche |

Conclusion: native factor scopes do not imply that GHW/FHW is the correct complexity parameter; for dense tables the primal graph and domain cardinality dominate. A public cross-instance learning split and a clear residual over exact solvers are absent.

## C. Tensor-network contraction

| ID | Work | Read | Finding |
|---|---|---|---|
| C1 | Markov and Shi, Simulating Quantum Computation by Contracting Tensor Networks | S | treewidth/contraction complexity foundation |
| C2 | Algorithms for Tensor Network Contraction Ordering | S | classical algorithmic baseline |
| C3 | Hyper-optimized Tensor Network Contraction | D | hypergraph partitioning plus Bayesian hyperoptimization already yields large gains |
| C4 | Optimizing TN Contraction Using RL | D | direct learned contraction-order collision |
| C5 | Optimal Linear Contraction Order of Tree TNs | **D-R** | exact polynomial result for the easy structural class |
| C6 | Tensor decision-diagram contraction heuristics | S | hardware/representation-aware classical heuristics are active |
| C7 | Learning to Rank TN Contraction Plans for GPU QCS | **D-R** | exact direct collision: learned measured-GPU plan ranking, ID/OOD and hardware shift |
| C8 | Quantum LEGO scheduling | S | 2026 sparsity-aware exact cost further raises the baseline |

Conclusion: reject on G8. The useful theoretical object is contraction width/line-graph treewidth and measured memory/communication, not a new GHW learner.

## D/K. CSP, SAT, WMC, and learned decomposition

| ID | Work/resource | Read | Finding |
|---|---|---|---|
| D1 | Hypertree Decompositions and Tractable Queries | S | foundational tractability result |
| D2 | det-k-decomp | S | exact backtracking baseline |
| D3 | Fast/Parallel HD (IJCAI 2020) | S | balanced separators and parallelism |
| D4 | Fast Parallel HD in Logarithmic Recursion Depth (TODS 2024) | **D-R** | explicit algorithm-switch opportunity, code, HyperBench, but not enough novelty alone |
| D5 | HyperBench | D | 3,648 real/application-derived hypergraphs; most query widths are low |
| D6 | PACE 2019 HTD exact/heuristic | D | public 100-instance competition set and checker |
| D7 | Efficient Approximation of FHW (FOCS 2024) | **D-R** | first nontrivial polynomial approximation substantially moves theory |
| D8 | General and Fractional HD: Hard and Easy Cases | S | boundaries for recognition/computation |
| D9 | Improving DP on TD via ML (IJCAI 2015) | D | learned selection among decompositions is established |
| D10 | ML Algorithm Selection for Exact Treewidth (Algorithms 2019) | D | exact-solver portfolio is a direct generic collision |
| D11 | Learning to Branch for Exact CO | S | generic learned exact-search guidance is crowded |
| D12 | Automatic Algorithm Selection for PBO (2025) | S | modern time-conditioned solver portfolios occupy another nearby niche |

Conclusion: HD/GHD remains an interesting systems-theory domain, but a publishable N1 cannot be “train a selector on HyperBench.” The benchmark is small for exact labels and generic decomposition-selection novelty is gone.

## E. Relational/factorized ML

| ID | Work | Read | Finding |
|---|---|---|---|
| E1 | AC/DC: In-database Learning Thunderstruck | S | structure-aware aggregates deliver orders-of-magnitude classical gains |
| E2 | LMFAO | S | factorized aggregate computation supports multiple ML workloads |
| E3 | F-IVM | S | view trees/rings support learning analytics under updates |
| E4 | FactorJoin | S | factor-graph cardinality estimation with public code |
| E5 | Fast Factorized Learning (2025) | S | further narrows headroom for a generic learned factorization plan |

Conclusion: the structural theory is already a system design, while the remaining choices resemble mature query optimization. No clean Level-2 learning formulation emerged.

## F/H/I. Structured prediction, HNN expressivity, and causality

| ID | Work | Read | Finding |
|---|---|---|---|
| F1 | Tensorized Hypergraph Neural Networks (SDM 2024) | S | direct tensor high-order message passing |
| F2 | LightHGNN (ICLR 2024) | **D-R** | hypergraph-free distilled inference can match/beat HNNs, warning against assumed necessity |
| F3 | Expressive Higher-Order Link Prediction via Symmetry Breaking (2024) | S | high-order link expressivity is already an active theory niche |
| F4 | Higher-dimensional GWL for HGNNs (2025) | S | direct expressivity escalation |
| F5 | Width Wall (2026) | **D-R** | hypertree-width-indexed expressivity hierarchy directly collides with H |
| F6 | Learning Causal Effects on Hypergraphs | S | real group interference, but no width/exact certificate role |
| F7 | DHG-Bench (ICLR 2026) | S | broad HNN benchmark reinforces field maturity, not a missing exact-theory task |

Conclusion: high-order representation is often useful, but G5 fails when theory only explains an HNN. Width Wall makes the most obvious width-expressivity project non-novel.

## G/L/M. Scientific ML and reaction pathways

| ID | Work/resource | Read | Finding |
|---|---|---|---|
| G1 | Hypergraphs and Cellular Networks | S | establishes native biochemical reaction hypergraphs |
| G2 | Pathway Analysis with Signaling Hypergraphs | S | ordinary graph projection loses reaction logic |
| G3 | Fast Approximate/Heuristic Shortest Hyperpaths | S | real, laptop-scale, public; >99% classical heuristic leaves little runtime residual |
| G4 | Exact Shortest Hyperpaths for Pathway Inference | D | exact cyclic solver and curated recovery create the decoding foundation |
| G5 | Robust Optimal Metabolic Factories (2024) | **D-R** | exact factory solver is already fast; “robust” here means numerical/stoichiometric validity |
| G6 | CHESHIRE | S | strong reaction-prediction baseline on 108 BiGG/818 AGORA models |
| G7 | Directed Hypergraph Representation Learning (AISTATS 2024) | S | direction-aware learned baseline, but prediction-only |
| G8 | BPP biochemical pathway platform (2024) | S | direct prediction platform, graph and hypergraph models |
| G9 | Multi-HGNN (2025) | S | multimodal missing-reaction predictor raises learned baseline |
| G10 | HyperSearch (2025) | S | certified pruning for unrestricted hyperedge prediction occupies generic certificate niche |
| G11 | RIPTiDe | S | context-dependent reaction weights can improve biological realism |
| G12 | NICEpath | S | atom-conserving graph weights are a strong hand-crafted comparator |
| G13 | TIObjFind (2025/2026) | S | learned/optimized metabolic objectives and graph min-cuts are adjacent but not directed hyperpaths |
| G14 | Optimal Chemical Pathways with Ising Machines (2024) | S | exact/optimal pathway computation is active; different representation/hardware |
| G15 | RetSynth | S | exact synthetic-pathway design baseline |

Conclusion: pure missing-reaction prediction fails G5, and pure exact hyperpaths fail G4. Their still-unoccupied, defensible intersection is decision-focused cost learning with exact directed-hyperpath decoding and a cost-uncertainty certificate.

## J. Neural combinatorial optimization with certificates

| ID | Work | Read | Finding |
|---|---|---|---|
| J1 | ML-Augmented Branch and Bound for MILP (2024) | S | generic solver integration is mature and does not create hypergraph novelty |
| J2 | Distributed Constrained CO with HGNNs / HypOp (NMI 2024) | S | broad higher-order CO, but simulated-annealing fine-tuning lacks exact certificate |
| J3 | Learning Decision-Focused Uncertainty Sets | S | supplies adjacent robust-learning theory; must be distinguished from a generic plug-in |

## K. Hypergraph partitioning

| ID | Work/resource | Read | Finding |
|---|---|---|---|
| K1 | KaHyPar / n-level recursive bisection | S | high-quality open classical baseline and public benchmark families |
| K2 | High-Quality Hypergraph Partitioning | S | hundreds of real instances and careful multi-seed protocol |
| K3 | Mt-KaHyPar | S | scalable parallel classical baseline |
| K4 | ML-based Hypergraph Pruning for Partitioning | S | direct learned pruning collision |
| K5 | HyperG GPU partitioner (2025) | S | strong 2025 hardware baseline |
| K6 | Deterministic Parallel High-Quality HGP (2025) | S | reproducible 64-core solver with competitive quality |

## Cross-family conclusions

1. Native high-order representation alone is insufficient; several HNN domains fail the theory gate.
2. Width/decomposition is most useful where it changes tractability or execution, but the obvious learned selectors have prior-art collisions and limited exact-label scale.
3. Learned query and tensor plan selection have the best systems benchmarks but the least novelty headroom.
4. In biochemical reaction networks, direction plus conjunctive reactants makes the graph-reduction failure concrete, and public curated pathways provide a genuine learning distribution.
5. The surviving hypothesis must preserve a strict separation: the exact solver certifies the optimum under predicted costs; calibration/robust margin addresses whether that optimum is stable under admitted cost uncertainty. Exact combinatorial decoding must not be misreported as biological truth.
