# R0 Search Log

## Protocol and counts

- Search date: **2026-08-27**.
- Directly relevant primary works/resources screened: **63**.
- Deeply reviewed: **24** (`D` or `D24-26`).
- Deeply reviewed works dated 2024--2026: **11** (`D24-26`).
- Search stopped after the strategy-residual and interface gates could be
  decided; it was not expanded to every learned SAT/MIP paper.

## Query families

`learning exact inference graphical models`, `learned variable elimination`,
`machine learning treewidth heuristic`, `learned hypertree decomposition`,
`GHD FHD heuristic`, `learning bucket elimination`, `algorithm selection exact
inference`, `factor graph runtime prediction`, `FAQ width inference`, `learned
branching CSP`, `learned join order`, `tensor contraction reinforcement
learning`, `learning augmented algorithms consistency robustness`, `UAI
inference benchmarks`, `XCSP3 high arity`, and `HyperBench`.

## Screened works and resources

| # | work/resource | year | depth | R0 role |
|---:|---|---:|---|---|
| 1 | Dechter, *Bucket elimination: A unifying framework for reasoning* | 1999 | D | exact elimination foundation |
| 2 | Dechter, bucket elimination for probabilistic inference | 1996/1998 | screen | ordering/cost foundation |
| 3 | Lauritzen & Spiegelhalter, local computations in graphical structures | 1988 | D | junction-tree foundation |
| 4 | Shafer & Shenoy, probability propagation | 1990 | screen | exact message passing |
| 5 | Darwiche, *Recursive conditioning* | 2001 | D | exact time-space strategy |
| 6 | Dechter & Mateescu, *AND/OR search spaces for graphical models* | 2007 | D | exact search/decomposition |
| 7 | Otten & Dechter, anytime AND/OR depth-first search | 2012 | screen | branch/order analogue |
| 8 | Chavira & Darwiche, compiling Bayesian networks with local structure | 2008 | screen | ACE/knowledge compilation |
| 9 | Mooij, libDAI | 2010 | screen | exact/approximate PGM engine |
| 10 | IJGP and join-graph propagation literature | 2000s | screen | PGM engine contrast |
| 11 | Peyrard et al., *Exact and approximate inference in graphical models: variable elimination and beyond* | 2015 | D | treewidth/order review |
| 12 | Gottlob, Leone & Scarcello, hypertree decompositions and tractable queries | 2002 | D | HD foundation |
| 13 | Gottlob, Greco & Scarcello, generalized hypertree decompositions | 2009 | screen | GHD complexity |
| 14 | Grohe & Marx, constraint solving via fractional edge covers | 2014 | D | FHW/CSP tractability |
| 15 | Marx, *Approximating fractional hypertree width* | 2010 | screen | classical FHW approximation |
| 16 | Fischl, Gottlob & Pichler, *General and Fractional Hypertree Decompositions: Hard and Easy Cases* | 2018/2020 | D | recognition hardness |
| 17 | det-k-decomp backtracking algorithm | 2007 | screen | exact HD construction |
| 18 | BalancedGo, fast/parallel GHD computation | 2022 | screen | classical decomposition solver |
| 19 | GHD computation under updates | 2022 | screen | HyperBench execution data |
| 20 | Gottlob et al., *Fast Parallel Hypertree Decompositions in Logarithmic Recursion Depth* | 2024 | D24-26 | 3,648-instance classical baseline |
| 21 | Lanzinger & Razgon, *FPT Approximation of Generalised Hypertree Width for Bounded Intersection Hypergraphs* | 2024 | D24-26 | recent structural theory |
| 22 | Korchemna et al., *Efficient Approximation of Fractional Hypertree Width* | 2024 | D24-26 | recent FHW theory |
| 23 | He et al., *A Branch-&-Bound Algorithm for Fractional Hypertree Decomposition* | 2024 | D24-26 | exact FHD search and DB evaluation |
| 24 | Surianarayanan et al., *Fast Hypertree Decompositions via Linear Programming: Fractional and Generalized* | 2025 | D24-26 | strong recent classical baseline |
| 25 | Lanzinger, Razgon & Unterberger, *FPT Parameterisations of Fractional and Generalised Hypertree Width* | 2025 | D24-26 | exact parameterized theory |
| 26 | *Rerootable Hypertree Decompositions* | 2026 | D24-26 | newest decomposition functionality |
| 27 | Ngo, Porat, Ré & Rudra, worst-case optimal joins | 2012 | screen | DB join foundation |
| 28 | Veldhuizen, Leapfrog Triejoin | 2014 | screen | WCOJ implementation |
| 29 | Abo Khamis, Ngo & Rudra, *FAQ: Questions Asked Frequently* | 2016 | D | semiring/FAQ-width foundation |
| 30 | AJAR/order-aware join aggregation | 2016 | screen | aggregate-order theory |
| 31 | Arun et al., *Hypertree Decompositions Revisited for PGMs* / JoinInfer | 2018/2019 | D | closest high-order exact system |
| 32 | JoinInfer's HYJAR data-driven hybrid | 2018/2019 | screen | pre-existing strategy selection |
| 33 | System R cost-based join optimization | 1979 | screen | classical plan-selection collision |
| 34 | Neo learned query optimizer | 2019 | screen | learned join-plan collision |
| 35 | Bao learned query optimizer | 2021 | screen | safe/learned plan collision |
| 36 | Balsa learned query optimizer | 2022 | screen | learned cost/search collision |
| 37 | learned cardinality estimation survey | 2024 | screen | candidate-E saturation |
| 38 | *Learned Query Optimizer: What is New and What is Next* | 2024 | screen | modern DB landscape |
| 39 | opt_einsum contraction-path optimization | 2018 | screen | dense VE collision |
| 40 | Gray & Kourtis, hyper-optimized tensor network contraction / cotengra | 2021 | D | strong classical/metaheuristic planner |
| 41 | Meirom et al., *Optimizing Tensor Network Contraction Using Reinforcement Learning* | 2022 | screen | direct learned-order collision |
| 42 | algorithms for tensor-network contraction ordering | 2020 | screen | classical tensor planning |
| 43 | optimal contraction trees for quantum-circuit simulation | 2022 | screen | exact planner collision |
| 44 | RL-TNCO public implementation | 2022 | screen | reproducible learned contraction |
| 45 | Selsam et al., NeuroSAT | 2019 | screen | learned SAT search contrast |
| 46 | Gasse et al., learning to branch in mixed integer programming | 2019 | screen | exact-solver guidance |
| 47 | Bengio, Lodi & Prouvost, ML for combinatorial optimization | 2021 | screen | solver-learning review |
| 48 | Cappart et al., combinatorial optimization and reasoning with GNNs | 2021 | screen | CP/solver-learning review |
| 49 | Zhang, Gao & Nastos, GNN-powered solver framework | 2024 | D24-26 | recent CSP branch framework |
| 50 | *Targeted Branching for the Maximum Independent Set Problem Using Graph Neural Networks* | 2024 | screen | exact learned branching |
| 51 | *Graph Convolutional Branch and Bound* | 2026 | screen | newest generic exact guidance |
| 52 | Rice, algorithm-selection problem | 1976 | screen | portfolio foundation |
| 53 | SATzilla | 2008/2014 | screen | mature solver selection |
| 54 | Hydra portfolio construction | 2010 | screen | configuration/portfolio collision |
| 55 | Lykouris & Vassilvitskii, learning-augmented caching | 2018 | screen | robust-prediction template |
| 56 | Purohit, Svitkina & Kumar, learning-augmented scheduling | 2018 | screen | consistency/robustness template |
| 57 | Mitzenmacher & Vassilvitskii, algorithms with predictions perspective | 2020 | screen | framework survey |
| 58 | Eliáš et al., *Learning-Augmented Algorithms with Explicit Predictors* | 2024 | D24-26 | recent theory contract |
| 59 | UAI 2014 inference competition and model format | 2014 | D | accepted exact/approximate task archive |
| 60 | UAI 2022 benchmark reuse of UAI 2014 PR/MAR/MPE | 2022 | screen | current public access route |
| 61 | Boussemart et al., XCSP3 format | 2016 | D | high-order constraint benchmark format |
| 62 | Proceedings of the XCSP3 Competition 2024 | 2024 | D24-26 | recent accepted solver benchmark |
| 63 | Proceedings of the XCSP3 Competition 2025 | 2025 | D24-26 | recent accepted solver benchmark |

## Benchmark and repository checks

- Downloaded and parsed official UAI 2014 `PR_prob.tar.gz`; committed only
  derived statistics because the archive has no single stated redistribution
  license.
- Inspected UAI 2022 benchmark links, UAI task definitions and file format.
- Inspected XCSP3 competition pages, model/instance availability and recent
  proceedings.
- Inspected HyperBench via the 2022 Zenodo replication artifact: 3,648 source
  hypergraphs; CC BY 4.0 for the Zenodo package.
- Inspected JoinInfer's benchmark construction, factor arity/sparsity ranges,
  induced sparsity, exact-engine settings and data-driven hybrid.
- Inspected cotengra and RL-TNCO interfaces for contraction-path collision.

## Negative searches

- No primary work was found that combines a fixed high-order factor structure,
  learned exact strategy, deterministic certificate, two real factor benchmark
  families and family-disjoint evaluation.
- No public artifact was found coupling HyperBench's certified decompositions
  to factor tables and downstream exact-inference runtimes.
- No UAI study was found establishing a learnable order residual over tuned
  min-fill variants under family-disjoint evaluation.
- No repeated deployed workload was found that justifies the cost of multi-plan
  oracle labels for the high-order instances.
- Learned local branching, plan-cost and contraction-order searches landed in
  mature CP/SAT, DB or tensor interfaces.

## Count reconciliation

Rows marked `D` total 13 and rows marked `D24-26` total 11, for 24 deep works.
The recent-depth target and overall 50-work target are both exceeded.
