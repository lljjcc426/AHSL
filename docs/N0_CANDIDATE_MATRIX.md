# N0 candidate matrix

Scores use A--J for importance, benchmark, novelty, hypergraph indispensability, ML necessity, theory depth, upside, reproducibility, feasibility, and venue fit; K/L are low-risk scores for classical domination and prior-art collision. A hard failure overrides the total.

## Broad-family screen

| Family | Best concrete formulation found | Main evidence | Failed gate(s) | Broad verdict |
|---|---|---|---|---|
| A learned query optimization | learn binary/WCOJ/factorized plan choice | ADOPT already uses RL with WCOJ and guarantees; CIDR 2025 directly learns when to enable factorization/WCOJ | G8; often G3 on rank-2 graph queries | kill |
| B exact high-order inference | learn elimination/solver strategy on UAI factors | UAI is public, but dense factors are governed by primal treewidth and solver portfolios are mature | G3, G4, G6 | kill |
| C tensor contraction | learn contraction plan or rank plans | cotengra hyperoptimization, RL contraction, and 2026 GPU plan ranking directly occupy the space | G8 | kill |
| D CSP/SAT/WMC | learned branching/portfolio with proof logging | real benchmarks, but generic learning-to-branch/portfolio literature is saturated; hypergraph width is rarely the indispensable object | G3, G8 | kill |
| E relational/factorized ML | learn factorization/materialization plan | AC/DC, LMFAO, F-IVM and adaptive factorization already deliver the structural benefit | G4, G8 | kill |
| F high-order structured prediction | exact learned high-order decoder | existing exact convex/LP methods are narrow; public real training distribution and residual are weak | G2, G4, G6 | kill |
| G scientific high-order ML | reaction/link prediction on biological hypergraphs | real data exist, but pure prediction does not make theory functionally necessary | G5 | kill as broad family |
| H HNN expressivity × width | width-aware HNN architecture | Width Wall (2026) directly establishes a hypertree-width hierarchy and experiments | G8 | kill |
| I causal/probabilistic computation | causal effects with group interference | hypergraph causal learning exists, but width/exactness is not functionally required in the benchmark | G5, G8 | kill |
| J neural CO with certificates | learned exact branching/reduction | generic learned branch-and-bound and certified learning are crowded; hypergraph-specific residual not established | G3, G8 | kill |
| K partition/decomposition | select HD algorithm/separator/decomposition | ML selection for TD/DP and exact-treewidth solvers predates N0; ML hypergraph pruning also exists | G8 | kill |
| L directed pathway inference | learn reaction costs, exact directed-hyperpath decode, uncertainty certificate | public curated pathways; exact cyclic hyperpath algorithm; graph shortest path loses AND-tail semantics | none after narrowing | **advance** |
| M robust metabolic factories | learn factory costs with exact MILP | modern exact factory solver is already fast and robust; clean supervised target is less direct | G4, G6 | merge only as external baseline/future extension |

## Six semifinal candidates

| ID | Candidate | A | B | C | D | E | F | G | H | I | J | K | L | Total | Hard-gate result |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| S1 | CertPath: decision-focused reaction-cost learning with exact directed-hyperpath decoding and robust-optimality abstention | 5 | 5 | 4 | 5 | 4 | 4 | 4 | 4 | 3 | 4 | 3 | 4 | **49** | pass G1--G10; finalist |
| S2 | learned strategy/separator control for exact HD/GHD | 4 | 4 | 2 | 5 | 3 | 4 | 3 | 5 | 4 | 3 | 2 | 2 | 41 | fail G8; generic TD selection and exact treewidth portfolio already exist |
| S3 | width-aware learned hybrid binary/WCOJ execution | 5 | 4 | 1 | 4 | 5 | 4 | 4 | 4 | 2 | 5 | 2 | 0 | 40 | fail G8; ADOPT and adaptive-factorization collision |
| S4 | learned exact inference strategy for sparse high-order factors | 4 | 4 | 3 | 2 | 3 | 3 | 3 | 4 | 3 | 4 | 2 | 3 | 38 | fail G3/G4/G6 |
| S5 | certified tensor contraction-plan ranking | 4 | 4 | 0 | 4 | 5 | 3 | 4 | 5 | 3 | 4 | 2 | 0 | 38 | fail G8; direct 2026 learned plan-ranking collision |
| S6 | learned coarsening/pruning/configuration for hypergraph partitioning | 5 | 5 | 1 | 5 | 4 | 2 | 4 | 5 | 3 | 4 | 2 | 1 | 42 | fail G8 despite score; ML hypergraph pruning exists and classical solvers dominate |

## Final matrix

Only S1 enters the final matrix. Reporting fewer than two finalists is deliberate: all other semifinal candidates have a hard-gate failure.

| Candidate | Native object | Learned object | Theoretical object | Benchmark now | Strongest baseline | Score | Verdict |
|---|---|---|---|---|---|---:|---|
| CertPath | directed reaction hypergraph; each reaction maps a tail set of reactants/regulators to a head set of products | nonnegative reaction costs and calibrated cost intervals from biochemical, provenance, and pathway context | exact cyclic shortest-hyperpath decoding; robust-optimality margin certificate; classical unit/provenance-weight fallback | versioned Reactome BioPAX/CC0; NCI-PID/Pathway Commons external set; 5,066 Reactome target instances in the established construction | Mmunin exact cutting-plane solver; Hhugin heuristic; unit/provenance weights | **49/60** | rank 1; N0-A |

## One-sentence contribution test

> We learn calibrated reaction costs from versioned curated pathways and decode them with an exact directed-hyperpath solver, while a cost-interval margin certificate either proves the selected pathway invariant to admitted cost uncertainty or abstains to a classical cost, improving held-out pathway recovery without sacrificing feasibility or exactness under the deployed objective.

This is a Level-2 target, not Level 3: the novelty is a new decision-focused/certified formulation on a real directed-hypergraph task, not a new universal hypergraph theory.
