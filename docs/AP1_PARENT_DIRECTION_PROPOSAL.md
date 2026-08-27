# AP1 parent-direction proposal

## Canonical direction

**Dynamic and incremental execution of recursive structured queries**
中文：**动态与增量递归结构化查询执行**。

This is a data-systems direction concerned with exact recursive computations over changing relational, graph and deductive data.

## Exact scope

- update-sensitive execution of recursive SQL/Datalog/graph queries;
- insertions, deletions and non-monotone/aggregate recursion;
- retained state, reuse, update work, latency tails and multicore scheduling;
- exact semantics and reproducible public workloads;
- focused extensions to existing engines.

## Out of scope

- generic IVM without recursion or a measured workload failure;
- building a new database from scratch;
- generic learned query optimization;
- static graph algorithms with no changing-data workload;
- vector search, hypergraph decomposition or LLM integration unless later evidence requires it;
- distributed execution in the first project.

## Community and venues

Primary community: database/data-management systems, with graph DB and Datalog subcommunities. Realistic venues: SIGMOD/PACMMOD, PVLDB and ICDE; PODS/ICDT only for a theory-forward result; CIDR for an early systems architecture.

## Three strongest real problems

1. Retained intermediate state can exhaust memory even when incremental update time is excellent.
2. Deletions/non-monotone recursion can retract facts and trigger expensive propagation that insertion-only studies miss.
3. Recursive parallelism and reuse are highly workload-dependent; one granularity or one fixed policy is not robust.

## Two benchmark families

1. **Primary:** LDBC SNB Interactive v2, including complex reads, update streams and deep deletes.
2. **Independent:** FlowLog's public recursive suite, spanning graph analytics and real program-analysis workloads, supplemented by its public competing engines.

## Strongest systems

Feldera/DBSP, FlowLog, Differential Dataflow/DDlog, Kuzu, Soufflé and DuckDB/Umbra where the recursion is expressible. Materialize is an important mature architectural reference but is too large to be the first modification target.

## Why a residual exists

Generality results prove or implement incrementalization, but do not guarantee low retained state or stable tail latency for every recursive query/update regime. Published OOM behavior, deep-delete benchmark design, current recursion-aware system papers and cross-language limitations jointly establish the residual.

## Contribution opportunities

- **Algorithm:** update-sensitive state retention, deletion propagation, reuse or scheduling.
- **System:** integration into a current engine with exact semantics and resource-aware execution.
- **AI:** later selection among exact policies if a classical adaptive rule cannot capture workload variation.
- **Theory:** correctness plus amortized update work, state size or recourse bounds.

## 2–3 year project tree

1. State/tail-latency residual and one focused exact execution method.
2. Generalization across recursion/update classes with correctness and resource analysis.
3. One evidence-driven extension: distributed state, cross-paradigm compilation, or learned policy selection with exact fallback.

## First bounded AP1 problem-discovery task

Duration: at most 3 working days; no new algorithm implementation.

1. Build pinned releases of FlowLog and Feldera, plus Kuzu or DuckDB for supported static/reference queries.
2. Select four recursive workloads: reachability, SSSP, one recursive aggregate and one program-analysis task.
3. Run initial load followed by controlled 1%, 5% and 10% mixed update batches at insertion:deletion ratios 100:0, 50:50 and 0:100 on a small and medium public input.
4. Record exact output agreement with scratch evaluation, p50/p95 update latency, throughput and peak RSS.
5. Attribute any failure to retained state, re-derivation, parallel underutilization, compilation or unsupported semantics using existing engine counters/profiles.

Budget: ≤40 CPU-hours, 0 GPU-hours, ≤64 GB RAM, ≤100 GB storage.

## Stop conditions

Stop or reopen AP0 if any holds:

- latest FlowLog/Feldera already dominate scratch and each other with no ≥2× latency/state deterioration across both routes;
- the only observed gap is an unsupported syntax adapter;
- the exact proposed mechanism is already implemented in a current paper/branch;
- a credible experiment requires proprietary traces or a new DBMS;
- residuals occur only on synthetic adversarial cases and disappear on LDBC/program-analysis workloads.
