# AP0 search log

Search date: 2026-08-27. Counts below are de-duplicated primary papers, benchmark papers/official specifications, competition records and maintained system artifacts. `D` means the problem, workload, comparison, result/residual, artifact and limitation were extracted; `S` means screening only.

**Count: 86 screened; 31 deep; 18 deep from 2024–2026.** Search engines and secondary commentary are not counted.

## Dynamic/incremental and recursive data systems (1–35)

| # | Work/resource | Year | Level | Main audit use |
|---:|---|---:|:---:|---|
| 1 | Maintaining Views Incrementally | 1993 | D | deletion/update delta foundation |
| 2 | Maintenance of Materialized Views: Problems, Techniques, and Applications | 1995 | S | classical taxonomy |
| 3 | DBToaster: Higher-order Delta Processing | 2012 | D | higher-order IVM, latency/state trade-off |
| 4 | Differential Dataflow | 2013 | D | nested iterative incremental foundation |
| 5 | Naiad: A Timely Dataflow System | 2013 | S | distributed dataflow runtime |
| 6 | Shared Arrangements: Practical Inter-query Sharing | 2020 | S | reusable indexed traces |
| 7 | DBSP: Automatic IVM for Rich Query Languages | 2023 | D | strongest general incrementalization theory/system |
| 8 | Optimizing Differentially-Maintained Recursive Queries on Dynamic Graphs | 2022 | D | measured update-time benefit and OOM residual |
| 9 | Materialize engine/artifact | current | S | mature Differential Dataflow SQL system |
| 10 | Feldera engine, current docs and release artifact | 2026 | D | build/license/current limitations |
| 11 | Temporel: Optimizing Nested Recursive Queries | 2024 | D | current recursive optimizer collision |
| 12 | Adaptive Recursive Query Optimization / Carac | 2023 | S | runtime recursive reoptimization |
| 13 | Robust Recursive Query Parallelism in GDBMSs | 2025 | D | workload-sensitive parallelism residual |
| 14 | FlowLog: Efficient and Extensible Datalog via Incrementality | 2025 | D | closest current system and broad suite |
| 15 | Raqlet: Cross-Paradigm Compilation for Recursive Queries | 2026 | D | semantic/engine fragmentation |
| 16 | Enzyme: IVM for Data Engineering | 2026 | D | current lake/data-engineering IVM collision |
| 17 | DuckDB `USING KEY` recursive CTE work | 2025 | S | modern relational recursion baseline |
| 18 | Soufflé: On Synthesis of Program Analyzers | 2016 | S | compiled Datalog baseline |
| 19 | RecStep | 2019 | S | relational Datalog engine baseline |
| 20 | BigDatalog | 2016 | S | distributed Datalog baseline |
| 21 | Differential Datalog (DDlog) | 2020 | S | DD-backed incremental Datalog baseline |
| 22 | VLog | 2019 | S | reasoning/Datalog system |
| 23 | Graphflow | 2017 | S | recursive graph DB lineage |
| 24 | Kuzu graph DB system | 2023 | S | current embeddable GDBMS baseline |
| 25 | LDBC Social Network Benchmark | 2020 | D | primary workload family, scale and rules |
| 26 | LDBC SNB Interactive v2 deep deletes | 2023 | D | primary deletion/update route |
| 27 | LDBC Graphalytics | 2016 | S | independent graph analytics route |
| 28 | CFPQ_Data benchmark collection | current | S | context-free path workloads |
| 29 | Polonius borrow-checker analysis artifact | current | S | real recursive program-analysis workload |
| 30 | DOOP points-to analysis framework | current | S | large rules/program workload |
| 31 | DBToaster journal system article | 2014 | S | mature system evidence |
| 32 | F-IVM: Factorized IVM | 2021 | S | factorized state/maintenance baseline |
| 33 | Dynamic query evaluation lower-bound literature | 2018 | S | theoretical ceiling |
| 34 | Incremental View Maintenance with Triple Lock Factorization | 2020 | S | specialized IVM |
| 35 | Incremental computation and temporal aggregates | 2003 | S | maintained temporal structures |

## Hybrid vector-relational systems (36–52)

| # | Work/resource | Year | Level | Main audit use |
|---:|---|---:|:---:|---|
| 36 | HNSW | 2016 | D | strongest classical in-memory graph index |
| 37 | DiskANN | 2019 | S | disk-scale ANN baseline |
| 38 | Filtered-DiskANN | 2023 | D | label-aware filtered graph baseline |
| 39 | VBASE | 2023 | D | vector-relational query execution baseline |
| 40 | ACORN | 2024 | D | arbitrary-predicate hybrid search collision |
| 41 | UNIFY | 2024 | D | range-filtered unified index collision |
| 42 | SIEVE | 2025 | D | workload-aware index collection collision |
| 43 | DIGRA | 2025 | D | dynamic range-filtered graph index collision |
| 44 | RangePQ | 2025 | D | dynamic range-filtered PQ collision |
| 45 | VectraFlow | 2025 | D | streaming vector operators/current frontier |
| 46 | Results of the BigANN 2023 Competition | 2025 | D | measured filtered/streaming state of art |
| 47 | BigANN filtered/streaming benchmark specification | 2023 | D | scale, metrics, hardware, terms |
| 48 | VBench | 2025 | D | vector analytics with joins/group/filter/top-k |
| 49 | RVBench | 2026 | S | relational-vector benchmark route |
| 50 | CleANN | 2025 | S | fully dynamic ANN collision |
| 51 | CONDA | 2026 | S | evolving-data graph index collision |
| 52 | VectorDBBench | current | S | production-oriented system benchmark tool |

## Reliable executable AI/data workflows (53–68)

| # | Work/resource | Year | Level | Main audit use |
|---:|---|---:|:---:|---|
| 53 | Spider | 2018 | D | classical cross-domain text-to-SQL benchmark |
| 54 | BIRD | 2023 | S | large database/value benchmark |
| 55 | Spider 2.0 | 2024 | D | enterprise workflows and 17% baseline residual |
| 56 | LiveSQLBench | 2025–26 | S | dynamic contamination-resistant second route |
| 57 | CHESS | 2024 | D | retrieval, pruning and LLM unit-test collision |
| 58 | CHASE-SQL | 2024 | D | diverse candidate/selector collision |
| 59 | Execution-Guided Decoding | 2018 | S | executable-filter foundation |
| 60 | DIN-SQL | 2023 | S | decomposition/self-correction baseline |
| 61 | DAIL-SQL | 2023 | S | in-context example-selection baseline |
| 62 | CEDAR | 2025 | D | cost-aware relational claim verification |
| 63 | BIRD-Interact | 2026 | S | interactive task-completion route |
| 64 | SQL-PaLM | 2023 | S | LLM text-to-SQL baseline |
| 65 | RESDSQL | 2023 | S | schema linking/decoupling baseline |
| 66 | PICARD | 2021 | S | constrained decoding baseline |
| 67 | Text-to-SQL survey/current leaderboard systems | 2024 | S | collision density |
| 68 | SWAN hybrid relational-LLM benchmark | 2025 | S | mixed SQL/LLM query reliability |

## Constraint solving and structured optimization (69–86)

| # | Work/resource | Year | Level | Main audit use |
|---:|---|---:|:---:|---|
| 69 | MiniZinc Challenge 2025 | 2025 | S | solver competition protocol/results |
| 70 | XCSP3 Competition 2025 and instance corpus | 2025 | D | >23k instances, solvers, traces and current results |
| 71 | SMT-COMP 2025 incremental/model-validation tracks | 2025 | S | exact incremental competition route |
| 72 | CP-Bench | 2025 | S | LLM constraint-modeling benchmark |
| 73 | OR-Tools CP-SAT | current | S | strongest accessible exact/hybrid solver |
| 74 | PSPLIB | current | S | project-scheduling benchmark library |
| 75 | FrontierCO | 2025 | S | modern ML-based CO benchmark |
| 76 | ML4CO competition | 2022 | S | learning inside SCIP controls |
| 77 | Differentiable Combinatorial Scheduling at Scale | 2024 | S | recent ML scheduling collision |
| 78 | Industrial test-laboratory scheduling benchmark | 2024 | S | rare public real-instance route |
| 79 | iMOPSE multi-skill scheduling benchmark | 2024 | S | independent scheduling route |
| 80 | Taillard job-shop benchmarks | 1993 | S | classical scheduling baseline |
| 81 | OR-Library | 1990 | S | classical reproducible optimization corpus |
| 82 | Contemporary CP solver benchmark for JSSP | 2026 | S | current solver strength |
| 83 | LLM4Solver | 2025 | S | generic LLM-for-exact-CO collision |
| 84 | CP-guided deep learning for dynamic FJSSP | 2024 | S | dynamic learning/CP collision |
| 85 | Renault prototype-car configuration/testing | 2024 | S | real industrial optimization evidence |
| 86 | MiniZinc language/toolchain and handbook | current | S | modeling/build ecosystem |

## Query themes used

Search strings combined venue/domain terms rather than model names alone: incremental view maintenance + recursion/deletes/state; recursive graph query + parallelism; Datalog + Differential Dataflow; LDBC update/deep delete; filtered ANN + arbitrary predicates + updates; vector-relational joins/aggregates; Spider 2.0 + verification/repair; LLM + CP/SMT + semantic validation; public scheduling workload + strong exact solver. Current venue programs and official benchmark/system repositories were checked after paper discovery.
