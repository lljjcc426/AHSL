# AP0 systems and baseline audit

## Winning direction: strongest baselines

| System/work | Capability | Artifact/build reality | Residual relevant to AP0 |
|---|---|---|---|
| Differential Dataflow | nested iterative and incremental dataflows | mature Rust implementation; permissive ecosystem; low-level programming model | users assemble dataflows; retained traces can dominate memory |
| Materialize | SQL views maintained by Differential Dataflow | large active Rust codebase; BSL 1.1 converting to Apache-2.0 after four years; single-node self-managed use allowed | substantial integration burden; broad SQL support does not imply robust recursive/deletion performance for every workload |
| DBSP/Feldera | automatic incrementalization for rich SQL, monotone and non-monotone recursion | active MIT-licensed engine, Docker and docs, frequent releases; Rust compiler/runtime | nonstandard recursion semantics, unsupported SQL corners and documented O(N)/O(M) operators; cost/state optimization remains workload-sensitive |
| GraphflowDB DC | optimized differential maintenance of recursive graph queries | research code/artifact availability must be reconfirmed in AP1 | paper reports severe baseline memory blow-up and specializes a bounded query class |
| FlowLog | relational IR and recursion-aware optimization atop Differential Dataflow | PVLDB artifact publishes code/data; Rust; compares Soufflé, RecStep, DDlog, DuckDB, Umbra | current strongest collision; distributed execution is future work and incremental deletion uses general integer differences |
| Kuzu recursive engine | robust recursive-query parallelism in an embeddable GDBMS | open-source Kuzu artifact and paper branch | primarily static execution; not a complete answer to incremental state and deletes |
| Soufflé | mature compiled Datalog and optimizer | open source, established build; per-program compilation | lacks recursive aggregation in the FlowLog comparison and is not designed as a general continuous-update engine |
| DuckDB/Umbra | highly optimized relational execution | DuckDB readily buildable/open; Umbra research access is narrower | SQL recursion cannot express nearly half of FlowLog's mutual/nonlinear programs |

## Reproduction judgment

AP1 should begin with FlowLog, Feldera and Kuzu/DuckDB, not Materialize internals or a new engine. These cover the closest recent system, a general incremental engine and a strong recursive relational/graph baseline. The first gate needs only existing builds and bounded workloads; no reason exists to rewrite PostgreSQL or implement distributed infrastructure.

## Other families

- Vector-relational: HNSW/FAISS, Filtered-DiskANN, ACORN, VBASE, UNIFY, SIEVE and recent dynamic indexes are strong and mostly artifact-backed. Collision is fatal to a generic proposal.
- Reliable SQL: CHESS and CHASE-SQL are the strongest recent AI pipelines; Spider-Agent is the benchmark-native baseline. Reproduction can depend on proprietary APIs and large context costs.
- Constraints: OR-Tools CP-SAT, Gurobi/SCIP, Choco, Picat and competition winners create a very high baseline bar.
- Scheduling: CP-SAT and domain-specific CP/MIP hybrids often already solve standard instances well; a new project needs a new accessible workload, not only another heuristic.
