# AP0 closest-prior-art and exact residual

| Candidate | Classical | Recent system | ML/AI | LLM | Theory | Exact remaining gap |
|---|---|---|---|---|---|---|
| Dynamic/incremental recursive execution | delta rules; semi-naive evaluation; DBToaster; Differential Dataflow | DBSP/Feldera; FlowLog; Kuzu robust recursive parallelism; GraphflowDB DC | learned/adaptive query optimization | not necessary | dynamic query/IVM and algebraic incrementalization | predictable exact update latency and retained state across deletions, recursion shapes and execution granularities on accepted changing workloads |
| Reliable enterprise data workflows | semantic parsing; execution-guided decoding | Spider-Agent; CEDAR | CHESS/CHASE-SQL selectors and generators | core component | program semantics/equivalence | distinguish semantically wrong executable SQL and repair it without a wrapper-only contribution or privileged gold intent |
| Dynamic vector-relational | HNSW, DiskANN, relational cost optimization | VBASE, ACORN, UNIFY, SIEVE, DIGRA, RangePQ | learned selectivity/routing | RAG systems motivate workload | ANN guarantees and dynamic indexes | only highly specific combinations of arbitrary predicates, relational operators and updates remain; exact area is moving quickly |
| Constraint model synthesis | CP/SAT/SMT modeling and exact solvers | CP-SAT, MiniZinc/XCSP winners | learned branching/modeling | CP-Bench and solver tool use | constraint semantics and proof | verify that generated constraints encode user intent, not merely that a solver finds a feasible assignment |

## Strongest collision against Rank 1

FlowLog (PVLDB 2025) is the closest current work: it builds a Datalog-aware relational IR atop Differential Dataflow, adds recursion-aware optimization, supports incremental Datalog and publishes a broad artifact. Any AP1 problem that reduces to “optimize recursive Datalog over DD” without a new measurable residual is killed.

## Strongest evidence that a gap remains

FlowLog explicitly uses integer differences for insertion/deletion maintenance and leaves distributed execution for future work; the earlier GraphflowDB study documents memory exhaustion despite large update-time gains; LDBC v2 exposes deep deletes; PVLDB 2025 still required a new hybrid parallel policy for robust static recursive execution. Together these show that general incrementalizability is not equivalent to predictable resource-efficient execution.
