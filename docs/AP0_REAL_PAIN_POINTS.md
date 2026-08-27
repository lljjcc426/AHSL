# AP0 real pain points

## P1 — state/memory blow-up in recursive incremental computation

**Evidence.** On real graphs, differential maintenance can reduce update time from thousands of seconds to fractions of a second, yet the retained intermediate state can exceed memory. Ammar et al. report a 10 GB limit being exhausted beyond ten concurrent shortest-path queries; their specialized optimizations improve scalability by up to 20×. Speed alone therefore does not solve deployability.

## P2 — deletions and non-monotone recursion

Insert-only demonstrations understate production difficulty. LDBC SNB Interactive v2 introduces deep delete operations; FlowLog falls back to integer differences for incremental insertions/deletions, and recursive aggregates may retract prior facts. Exact deletion propagation creates work and state patterns absent from static or insertion-only benchmarks.

## P3 — unstable recursive parallelism

PVLDB 2025 shows that source-level morsels underutilize cores for few-source queries, while frontier-level scheduling has different failure regimes. A hybrid policy is more robust, proving that one fixed execution granularity is not sufficient across recursive workloads.

## P4 — fragmented recursion semantics and engines

SQL recursive CTEs, SQL/PGQ, Cypher/GQL and Datalog expose different recursion, aggregation and negation semantics. FlowLog reports that nearly half of its benchmark programs cannot be directly run in DuckDB/Umbra because of mutual or nonlinear recursion. Raqlet (CIDR 2026) identifies cross-paradigm portability and semantic reasoning as open problems.

## P5 — reliable executable data workflows

Spider 2.0 contains 632 enterprise-level workflows with databases often exceeding 1,000 columns; its baseline code agent solves 17.0%. This is a severe real failure, but current work already attacks retrieval, generation, testing, ranking and repair. The residual is real but the novelty boundary is narrow.

## P6 — dynamic filtered vector search

Real retrieval combines semantic similarity, hard filters and updates. BigANN includes 10M-vector filtered and streaming tracks. Yet 2024–2026 work already includes ACORN, UNIFY, SIEVE, DIGRA, RangePQ, CleANN and CONDA. The pain is real; the parent-direction headroom is lower because the closest collision is immediate and dense.

## P7 — optimization modeling burden

Constraint modeling remains a human bottleneck, and CP-Bench measures LLM-generated MiniZinc/CPMpy/CP-SAT models. But without a specific public application, success reduces to generic model-generation accuracy or solver competition performance, which violates the application-first rule.
