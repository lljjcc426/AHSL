# AP0 benchmark audit

## Primary route: LDBC Social Network Benchmark Interactive v2

| Field | Audit |
|---|---|
| Domain/task | transactional property-graph workload with complex reads, recursive path queries, inserts and deep deletes |
| Real/synthetic | synthetic data with correlated social-network structure; industry-style workload, standardized by LDBC/GDC |
| Input/output | generated graph plus parameter/update streams → exact query results and committed updates |
| Scale | configurable scale factors; reference repositories include generators, drivers and implementations |
| Metrics | throughput, latency percentiles, correctness, update completion; AP1 adds peak RSS and maintained-state bytes |
| Strong systems | Kuzu/GraphflowDB-style recursive execution, Neo4j, PostgreSQL, DuckDB/Umbra references where supported, Feldera/FlowLog translations |
| Open/license | specification, generator, driver and reference implementations public; core repositories Apache-2.0 |
| Reproduction | Docker/build instructions and auditable run rules exist; official audit is not needed for a research kill-test |
| Main failure | deep deletes and recursive queries stress propagation, state and parallel execution simultaneously |
| Residual | no published result establishes one robust state-bounded incremental strategy across recursive query shapes and deletion regimes |
| Community | SIGMOD/PVLDB/ICDE, graph data management |

## Second route: FlowLog public Datalog suite + real public graphs/program analyses

| Field | Audit |
|---|---|
| Domain/task | reachability, SSSP, same-generation, transitive closure, connected components, Andersen/CSPA/CSDA, Dyck reachability, Polonius, DOOP |
| Real/synthetic | mixture; real program-analysis corpora and public graph datasets plus controlled programs |
| Input/output | extensional facts and update batches → exact recursive facts/aggregates |
| Scale | ranges from small diagnostic programs to large DaCapo/CFPQ/SNAP-derived inputs |
| Metrics | batch time, update time, peak memory, scalability, exact output equality |
| Strong systems | FlowLog, Soufflé, RecStep, DDlog/Differential Dataflow, DuckDB and Umbra where expressible |
| Open/license | FlowLog paper artifact publishes code/data; dependencies are open source, with per-dataset terms to be recorded during AP1 freeze |
| Reproduction | public artifact and explicit competing engines; per-program compilation cost must be reported separately |
| Main failure | diverse recursion shapes and non-monotone updates trigger different execution/state regimes |
| Residual | FlowLog improves the state of the art but leaves distributed execution as future work and uses generic integer differences for incremental deletions |
| Community | PVLDB/SIGMOD, Datalog and program analysis |

## Audited non-winning benchmarks

| Benchmark | Scale/metrics | Access | Why not primary |
|---|---|---|---|
| BigANN 2023 filtered/streaming | 10M–30M vectors; QPS@90% recall or recall under update runbook; standardized 8-vCPU/16-GB machine | public framework; dataset-specific CC/O-UDA terms | strong but recent index literature is saturated; limited relational query structure |
| VBench/RVBench | 12 vector-analytic SQL queries over Recipe1M-derived data / hybrid relational-vector workloads | code public, VBench MIT | young benchmark, limited adoption and rapid 2025–2026 collision |
| Spider 2.0 | 632 enterprise workflows; task success/execution | code/data MIT; some cloud tasks incur cost | excellent secondary finalist evidence, but LLM-wrapper and rapidly moving leaderboard risks |
| BIRD | 12,751 pairs, 95 databases, 33.4 GB; execution accuracy and VES | public benchmark/leaderboard | gold noise has been documented; classic setting now partly saturated |
| LiveSQLBench | 600 new tasks over 22 real databases in Base-Full v1; execution/task completion | public, changing releases | useful contamination-resistant route but moving target |
| MiniZinc Challenge | 100 selected instances; solved count, speed, objective quality | models/results and Docker protocol public | solver-centric, not one real application |
| XCSP3 | >23,000 instances; competition tracks and traces | public parsers/models/results | broad constraint language, weak application anchoring |
| PSPLIB | project scheduling instance families and best solutions | public downloads | mature but mostly synthetic/classical; not enough for a new application program alone |
