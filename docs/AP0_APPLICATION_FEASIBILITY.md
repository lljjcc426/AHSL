# AP0 application feasibility

## Canonical direction

**Dynamic and incremental execution of recursive structured queries.** Applications include continuously updated graph/relational analytics, program analysis, access-control/reachability, dependency/lineage analysis and live knowledge/data systems.

## Application test

| Requirement | Finding |
|---|---|
| visible operational metric | update latency, throughput, peak memory/state, exactness, tail latency, cores used |
| accepted public workload | LDBC SNB Interactive v2 |
| independent route | FlowLog suite with real graph and program-analysis inputs |
| strong open baselines | Feldera, FlowLog, Differential Dataflow/DDlog, Soufflé, Kuzu, DuckDB |
| non-hypothetical residual | published OOM/state blow-up; deep deletes; workload-sensitive parallelism; expressiveness gaps |
| small-team prototype | bounded modification or external execution policy over one existing engine |
| industry analogue | graph DBs, CDC/live views, program analysis, dependency/lineage and streaming data products |

## Research-problem sentence

Current incremental engines fail to maintain predictable memory and update latency for recursive queries on changing graph/relational workloads because deletion propagation, recursive intermediate state and execution granularity interact; we need update-sensitive execution that bounds or reduces retained state while preserving exact recursive semantics.

## Hypothetical first-paper sentence

We develop and evaluate an update-sensitive recursive execution method that reuses only state justified by the active update/query regime, reducing peak state and tail update latency on LDBC and public Datalog workloads while preserving exact semantics.

This sentence specifies the required property and evaluation, not the final mechanism. AP1 must first establish which state is redundant and whether a focused intervention is possible.
