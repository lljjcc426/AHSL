# Project N0 topic discovery report

Search frozen: 2026-08-26. Branch point: B0 SHA `674d712debe1b29d262159b13f6e3bda0bc252a9`.

## 1. Executive decision

**Decision N0-A — GO.** Recommend exactly one project for N1 feasibility testing: **CertPath**, calibrated reaction-cost learning with exact general directed-hyperpath decoding and robust-optimality abstention for pathway inference.

This is not a recommendation for generic HNNs, GHW/FHW learning, learned decomposition, or another AHSL application. Those routes did not pass the joint novelty and indispensability tests.

## 2. Search methodology

N0 screened 80 primary works/resources in 13 families, deep-read 26, and deep-read 12 from 2024--2026. For every promising direction, the search combined the task with its learned object, theoretical object, `exact`, `certificate`, `benchmark`, and direct-collision terms. Public benchmark and license evidence was checked before scoring. Search queries and limitations are recorded in `docs/N0_SEARCH_LOG.md`.

## 3. Research lessons inherited from AHSL

Only methodological lessons were inherited, not the A0--A1.5 model:

1. a structural theorem must affect a decision, guarantee, or tractability boundary;
2. a clean synthetic gain is not evidence of real-task usefulness;
3. a strong classical baseline is part of the research question, not an inconvenience;
4. promotion requires a bounded kill test and explicit stop rule;
5. exactness under a model must not be confused with correctness of the model.

## 4. Candidate families screened

The required A--K families were all examined: learned query optimization; high-order exact inference; tensor contraction; CSP/SAT/WMC; relational/factorized ML; high-order structured prediction; scientific ML; HNN expressivity/width; causal/probabilistic computation; neural CO with certificates; and learned partitioning/decomposition. Search added directed reaction-hyperpath inference and robust metabolic factories.

Thirteen broad families were screened. Six concrete candidates reached the semifinal. Twelve broad families failed at least one gate after narrowing or were absorbed only as baselines; one narrow candidate remained.

## 5. Benchmark audit

The finalist benchmark is versioned Reactome BioPAX (CC0), using the established directed-hypergraph conversion and source–target protocol. The published construction contains 20,458 vertices, 11,802 hyperedges, 2,516 curated pathways, and 5,066 target instances (2,432 reachable); maximum tail/head arities are 26/28. Exact/heuristic code and datasets are publicly available for noncommercial research. Reactome supplies quarterly snapshots and multiple open formats.

The audit also covered HyperBench/PACE, JOB/JOB-Complex, CEB/STATS-CEB/CardBench, UAI inference, cotengra circuit workloads, and KaHyPar benchmarks. Details are in `docs/N0_BENCHMARK_AUDIT.md`.

## 6. Hypergraph-native structure audit

In CertPath a reaction is a directed hyperedge from **all** reactants/positive regulators to a product set. Pairwise projection changes reachability by allowing partial-tail activation and admits invalid shortcuts. An incidence or BF graph is equivalent only if it retains explicit AND semantics, at which point it is an encoding of the hypergraph problem rather than an ordinary shortest-path reduction. Published analysis notes that hyperpath length cannot be propagated as a simple sum/minimum of predecessor path lengths.

This is stronger than the “hypergraphs may improve representation” argument that failed in several HNN families.

## 7. ML-necessity audit

Existing exact/heuristic hyperpath methods require positive reaction weights and largely use unit or externally specified costs. Curated pathways, provenance, compartments, reaction types, regulators, biochemical annotations, and database releases provide repeated cross-instance signal. The learned object is a context-conditioned reaction cost/interval, evaluated on pathway-family and temporal shifts.

ML is unnecessary if unit/provenance costs match it on group-held-out pathway F1; that outcome is the primary stop condition. This makes the necessity claim falsifiable rather than assumed.

## 8. Theory-indispensability audit

Theory is functional in three places:

1. directed-hyperpath reachability enforces conjunctive reaction feasibility;
2. exact cyclic shortest-hyperpath decoding proves optimality under the deployed cost vector;
3. a robust separation certificate proves path invariance throughout an admitted cost interval or triggers fallback.

The exactness statement is conditional on learned costs. Statistical interval calibration and deterministic robust optimality are separate claims. GHW/FHW is not forced into the proposal because it is not the right theory object.

## 9. Closest prior art

The closest works are: exact cyclic shortest hyperpaths (Krieger--Kececioglu 2023); fast heuristic hyperpaths (2021/2022); CHESHIRE missing-reaction prediction (2023); directed-hypergraph representation learning (AISTATS 2024); Multi-HGNN (2025); BPP (2024); and transcript-guided reaction weighting/RIPTiDe. None found in the logged search jointly contains learned pathway costs, exact general directed-hyperpath decoding, calibrated cost uncertainty, a robust-optimality/abstention certificate, and grouped temporal evaluation.

Merely feeding CHESHIRE scores into Mmunin would be a weak known-A-plus-known-B combination and is explicitly not the proposed contribution.

## 10. Candidate kill log

| Candidate/family | Kill reason |
|---|---|
| learned WCOJ/GHD query planning | ADOPT directly provides RL adaptive WCOJ with guarantees; CIDR 2025 directly learns factorized/WCOJ activation |
| tensor contraction plan learning | hypergraph Bayesian optimization, RL, and 2026 GPU plan ranking already exist |
| learned exact HD/GHD selection | learned TD selection and exact treewidth solver portfolios already exist; HyperBench exact-label scale is limited |
| high-order exact PGM strategy | primal treewidth/domain cardinality dominate dense factors; no clean ML distribution/residual |
| generic SAT/CSP learned certificate | crowded solver-portfolio/branching space; hypergraph theory not indispensable on accepted benchmarks |
| factorized relational ML planner | AC/DC, LMFAO, F-IVM and adaptive factorization already capture the structural benefit |
| high-order structured prediction | narrow/generative exact theory and weak public cross-instance benchmark |
| HNN width expressivity | Width Wall 2026 is a direct hypertree-width expressivity collision |
| causal hypergraph learning | group interference is real, but exactness/width is not functionally needed |
| generic certified neural CO | generic ML branch-and-bound/certified reduction is crowded; no hypergraph-specific residual |
| hypergraph partitioning learner | direct ML pruning exists; 2025 classical deterministic/GPU solvers set a high systems bar |
| robust metabolic factories | exact parameter-free solver already fast; supervision/residual weaker than pathway inference |

## 11. Semi-final candidates

Six reached semifinal evaluation:

1. CertPath exact directed-hyperpath decision learning;
2. learned exact HD/GHD strategy/separator control;
3. width-aware learned hybrid binary/WCOJ execution;
4. learned exact strategy for sparse high-order factors;
5. certified tensor contraction-plan ranking;
6. learned hypergraph-partition coarsening/pruning/configuration.

Only CertPath passed every hard gate.

## 12. Final candidate matrix

There is one finalist, not an artificially padded list.

| Candidate | Score | Gates | Closest collision status | Final status |
|---|---:|---|---|---|
| CertPath | **49/60** | G1--G10 pass | adjacent components exist separately; no joint collision found | rank 1, recommend |

Subscores: importance 5, benchmark 5, novelty 4, hypergraph indispensability 5, ML necessity 4, theory depth 4, upside 4, reproducibility 4, feasibility 3, venue fit 4, low classical-domination risk 3, low collision risk 4.

## 13. Publication feasibility

Expected level: **plausible**. RECOMB/ISMB/Bioinformatics is a strong venue-family fit. UAI/AISTATS or CP/AAAI/IJCAI is plausible if the robust certificate is nontrivial and the grouped/OOD results are decisive. A general top-ML claim is weak unless the formulation transfers beyond pathway inference.

The minimum viable paper needs one theorem, one exact-decoding algorithmic interface, 2--4 strong baselines, real primary/external data, a native-vs-graph ablation, and explicit failure analysis. It does not need large infrastructure.

## 14. Theory-selection analysis

The search initially prioritized width/decomposition. That priority did not survive evidence: real database queries often have low widths, learned selectors have prior art, and tensor/PGM tasks use other complexity measures. For the surviving task, directed-hyperpath theory is the correct exactness object. Selecting it over GHW/FHW is a substantive negative conclusion from N0.

Proposed guarantee: if the selected path's upper interval cost is smaller than a valid lower bound for every alternative path under lower interval costs, then the selected path is optimal for every cost vector in the interval box. The solver must expose or compute the required competing lower bound; if it cannot, the method abstains.

## 15. Reviewer stress test

- **Why ML?** Repeated curated pathway tasks contain transferable cost signal; grouped/temporal tests decide whether it is real.
- **Why hypergraphs?** Conjunctive reactants and multi-product reactions are altered by pairwise projection.
- **Why not treewidth/GHW?** They are not the relevant theoretical object here.
- **Why not the existing solver?** It is retained; learning targets the objective, not solver correctness.
- **Why exactness?** It rules out infeasible local predictions and makes comparisons under one objective auditable.
- **Why realistic?** Reactome is expert-curated, versioned, and open; supersource limitations are stress-tested.
- **Why not a learned heuristic?** Exact decoding and deterministic abstention remain outside the predictor.
- **What is new?** Decision-focused calibrated costs + exact general directed hyperpaths + robust margin + leakage-resistant evaluation.
- **Does it generalize?** Only family/temporal results count.
- **Would anyone use it?** Positive: ranked feasible pathways with confidence/fallback. Negative: useful evidence that learned objectives add no value over structural priors.

## 16. Resource/compute analysis

The first test is capped at 300--500 reachable tasks, <=500 CPU-hours, <=24 optional GPU-hours, and <=7 elapsed days. Published baselines ran on laptop hardware; exact worst cases are below 30 minutes in the reported study. A linear/boosted model is sufficient for the first test. Restricted research-use solver code is not vendored; N1 can use a downloader/adapter or independently implement the published formulation.

## 17. Ranked shortlist

1. **CertPath** — 49/60, all gates pass.

No second project is recommended. The next numerical candidates are not finalists because hard-gate failure overrides their totals: learned partitioning (42, G8 fail), learned HD/GHD (41, G8 fail), hybrid WCOJ (40, G8 fail), sparse-factor inference (38), and tensor ranking (38, G8 fail).

## 18. Recommended primary project

**CertPath: Calibrated Reaction-Cost Learning with Exact Directed-Hyperpath Decoding for Pathway Inference.**

Central hypothesis: on pathway-family-disjoint and temporal Reactome tests, learned positive reaction costs improve exact-pathway reaction F1 over the best unit/provenance-cost exact baseline, while an interval-margin certificate identifies a nontrivial subset on which the learned optimal path is stable and otherwise safely falls back.

The one-sentence N1 paper hypothesis is: **Learning calibrated context-dependent reaction costs over versioned Reactome pathways, combined with exact directed-hyperpath decoding and robust-optimality abstention, improves held-out pathway recovery without sacrificing structural feasibility or conditional exactness.**

## 19. First bounded kill-test

Use 300--500 reachable tasks across at least four top-level Reactome families. Train positive linear and gradient-boosted costs on older-release, family-disjoint data; calibrate intervals separately; test on one held-out family and a later release. Compare exact learned-cost decode with exact unit/provenance costs, Hhugin, unconstrained top-k scoring, and pairwise graph shortest paths.

Primary success requirement: >=2 absolute paired F1 points over the strongest classical exact-cost baseline with a 95% paired bootstrap interval excluding 0 on at least the family-disjoint test, no feasibility loss, and >=20% useful certificate coverage. Stop before a neural scorer if this fails.

## 20. Major reasons NOT to pursue the recommended project

1. Hhugin/unit weights are already extraordinarily strong under the legacy objective, so little residual may remain.
2. Curated pathway membership is overlapping and incomplete, making F1 an imperfect biological target.
3. The standard supersource is not a specific experimental condition.
4. The exact solver is conditional on a learned objective; the certificate cannot establish biological truth.
5. The solver's noncommercial/no-redistribution terms complicate a clean artifact.
6. A naïve two-stage combination would be incremental and not publishable at the intended level.
7. General robust/decision-focused optimization theory is established, so the theorem must exploit directed-hyperpath structure rather than restate a generic margin test.

## 21. Final N0 decision

**N0-A — GO.** At least one candidate passes the scientific, benchmark, novelty, feasibility, and publication gates. Proceed only to the bounded N1 feasibility test described in `docs/N1_PROPOSAL.md`. This is not authorization to build a broad model suite.

## 22. Exact next action

After review, create an N1 branch from this frozen N0 commit. Before code, refresh the seven-work closest-prior-art chain and freeze Reactome releases/splits. Then implement only the data adapter, classical exact baselines, and the bounded positive linear/boosted cost kill test. Do not add a neural model until the predeclared residual and certificate-coverage gates pass.
