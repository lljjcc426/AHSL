# N0 benchmark and data audit

## Audit rule

For every serious candidate N0 checked availability, license/terms, instance unit, split status, raw high-order object, scale, target, metric, hardware evidence, strongest baselines, and code. No benchmark was downloaded or transformed in N0; this is a source/schema audit only.

## Finalist: Reactome / NCI-PID directed pathway hypergraphs

| Field | Audit result |
|---|---|
| resource | [Reactome downloads](https://reactome.org/download-data), quarterly [Zenodo releases](https://reactome.org/download-data), and the published [Hyperpaths resource](https://hyperpaths.cs.arizona.edu/) |
| license | Reactome database data and derived files are CC0; Reactome code is generally Apache-2.0 subject to repository-specific dependencies. Hyperpaths/Mmunin/Hhugin code is free for noncommercial research but cannot be redistributed without consent. This is usable but requires an independent artifact adapter or reimplementation for a clean redistributable N1 package. |
| instances | established construction has 5,066 Reactome targets (2,432 reachable) and 2,636 NCI-PID-Large targets (2,220 reachable); the 2023 exact paper reports thousands of solved source–target instances |
| split | no ML split is supplied. N1 must create group-disjoint splits by Reactome top-level pathway and a temporal release test (old releases train, later release test). Random reaction/path splits are prohibited because shared reactions would leak. |
| input | BioPAX pathway events converted to a directed hypergraph: physical entities are vertices; reactants plus positive regulators form the tail; products form the head; compartment/modification variants stay distinct |
| target | curated pathway membership / held-out reaction set for a source–target task; secondary target is the exact optimum under learned nonnegative reaction costs |
| primary metrics | reaction-set F1 against curated pathways; precision/recall separately; exact-feasibility rate; certificate coverage and conditional F1; runtime is secondary |
| raw higher-order structure | yes. Reactome audit in the WABI work: 20,458 vertices, 11,802 hyperedges, mean tail 2.4 (max 26), mean head 1.6 (max 28), 433 self-loops. Multiple reactants are conjunctive prerequisites. |
| graph-reduction audit | a simple projected graph permits one reactant to trigger a reaction and therefore changes reachability/path semantics. An incidence/BF graph can encode the object only by retaining AND-node semantics; ordinary shortest-path algorithms are then no longer equivalent. The WABI analysis explicitly notes that hyperpath length cannot be updated as a simple sum/minimum of predecessor path lengths. |
| reported hardware | Hhugin experiments used a 2.9 GHz Intel Core i5 laptop and 16 GB RAM, under 2 GB memory; mean runtime was 55 s on the large sets. The later exact Mmunin study reports median under 10 s and maximum under 30 min. |
| strongest classical/learned baselines | exact Mmunin cutting-plane; Hhugin; acyclic MILP; unit reaction costs; provenance/rate/atom-conservation weights; CHESHIRE and Multi-HGNN as prediction-only comparators, not exact decoders |
| code | Mmunin/Hhugin and constructed datasets are publicly available for research. Reactome exposes downloads, APIs, BioPAX, SBML, and versioned snapshots. |
| benchmark weakness | the standard source is a supersource attached to all input-less entities, not always a biologically specific experimental condition; curated pathway membership is incomplete and overlapping. These are central empirical risks, not bookkeeping issues. |

### Why this benchmark passes now

It is not synthetic, the native direction/tail/head scopes are preserved, thousands of source–target instances exist, curated pathways supply supervision, exact and heuristic baselines exist, and laptop-scale evidence is published. The missing ML split is constructible from public versioned data and does not depend on external permission.

## Semifinal audits

### HyperBench and PACE 2019 HD

| Field | Audit result |
|---|---|
| resource/license | HyperBench (3,648 application-derived hypergraphs) and PACE 2019 exact/heuristic HTD instances; PACE archive on Zenodo; checker `htd_validate` public |
| instances/splits | PACE exact track: 100 instances, odd IDs originally public and even IDs private then released; TODS study uses HyperBench and highlights 465 larger low-width instances |
| input/target | `.hgr` hypergraph; output `.htd`; minimize/certify hypertree width or solve at width k |
| metrics | solved count, runtime, width, recursion depth |
| raw HO | yes, from CQ/CSP/application hypergraphs |
| baselines/code | det-k-decomp, BalSep/log-k-decomp, greedy variants, PACE solvers, exact checker |
| fatal issue | generic ML selection of tree decompositions, DP decompositions, and exact-treewidth solvers already exists. The available exact set is small/heterogeneous, and a pure learned selector is not a Level-2 contribution. |

### Query-optimization resources

| Resource | What is public | Higher-order relevance | Fatal issue |
|---|---|---|---|
| JOB/JOB-Complex | IMDb data; 113 classic JOB queries; JOB-Complex adds 30 queries with 5--14 joins | relation scopes form a query hypergraph | many workloads are reducible to ordinary join trees; direct learned-query-optimizer literature is dense |
| CEB/STATS-CEB | real IMDb/Stack/STATS queries and cardinalities | multi-relation scopes | mainly a cardinality benchmark, not a WCOJ/GHD benchmark |
| CardBench | thousands of queries over 20 real databases; collection/generation scripts | diverse joins | no direct WCOJ plan labels; learned CE is itself crowded |
| ADOPT workloads | TPC-H, JCC-H, JOB, SNAP graph workloads; public code | cyclic WCOJ attribute orders | direct RL + WCOJ + convergence/worst-case guarantee collision |
| adaptive DuckDB factorization | runtime choice between hash, factorized and WCOJ execution | native relation scopes | CIDR 2025 directly trains the desired choice; heuristics are comparable |

### UAI inference competition

- Public UAI-format factors and PR/MAR/MPE/MMAP tasks; 1 CPU, 8 GB RAM, 20 s/20 min/1 h tracks.
- High-order factor scopes exist and sparse/binary formats are documented.
- However, dense table factors already pay exponential arity cost, while variable elimination complexity is governed by the primal graph/treewidth. No accepted cross-instance split for learning an exact sparse-factor decomposition policy is supplied. Toulbar2 and competition solvers are strong.
- Verdict: excellent solver benchmark, weak fit to the required hypergraph-theory × ML novelty.

### Tensor contraction

- Public circuit families and cotengra/KaHyPar tooling exist; costs include FLOPs, peak tensor size, and measured GPU time.
- Native object is a tensor network/hypergraph, and contraction correctness is exact.
- Hyper-optimized contraction already combines hypergraph partitioning with Bayesian search; ICML 2022 learns contraction by RL; a 2026 work directly learns GPU plan rankings across circuits/hardware.
- Verdict: reproducible but fatal novelty collision.

### Hypergraph partitioning

- KaHyPar/Mt-KaHyPar provide GPL code and public benchmark families (VLSI, SAT, scientific computing, social networks); high-quality studies use hundreds of hypergraphs and multiple k values.
- Strong 2025 deterministic/GPU/streaming solvers leave a demanding systems baseline.
- Machine-learning-based hypergraph pruning was published before N0.
- Verdict: public and important, but the generic learned configuration/coarsening candidate fails novelty.

## Benchmark decision

The only benchmark stack admitted to N1 is versioned Reactome as the primary data source, with the published Hyperpaths construction/protocol as the structural baseline and NCI-PID/Pathway Commons as external historical stress data. No benchmark acquisition is required before an N1 kill test, so N0-B does not apply.
