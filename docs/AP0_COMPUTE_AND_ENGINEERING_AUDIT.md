# AP0 compute and engineering audit

## First serious study estimate

- CPU: 150–450 CPU-hours for repeated SF1/SF10 and Datalog workload runs; comfortably below 1,000 CPU-hours.
- GPU: 0 hours. No learned component is needed.
- RAM: 32–128 GB depending on selected scale; the kill-test begins at 32 GB and treats OOM as a measured outcome.
- Storage: 50–250 GB including generated LDBC data, build artifacts and traces.
- Proprietary API/cloud: none.

## Engineering burden

Medium. Expected work is one existing Rust/C++ engine build, workload adapters, measurement hooks and a bounded execution/state modification. It does not require a new DBMS, distributed cluster, proprietary logs or custom hardware.

## Small-team feasibility

Feasible for one primary researcher with occasional systems guidance if the first paper stays single-node and targets one execution residual. Distributed execution, full cross-language compilation and production connectors are out of scope for Paper 1.

## Build order

1. Reproduce published baselines on unmodified artifacts.
2. Freeze two workload routes and exact output checks.
3. Measure peak RSS/state, p50/p95 update latency and throughput across insert/delete ratios.
4. Only after a stable residual appears, inspect the narrowest engine component that causes it.

No hash ritual, repeated smoke suite or broad defensive harness is justified. Exact-output comparison is necessary because the topic promises exact semantics; one deterministic reference evaluation per workload configuration is sufficient.
