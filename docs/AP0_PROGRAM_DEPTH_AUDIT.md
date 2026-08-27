# AP0 program-depth audit

## Rank 1: coherent 2–3 year tree

### Project A — bounded first system problem

Identify and reduce retained-state or tail-latency blow-up for exact recursive maintenance under mixed insert/delete updates on one engine. Evaluate LDBC SNB v2 and the FlowLog suite.

### Project B — generalization and theory

Generalize across recursion classes and update regimes; derive correctness and an amortized work/state or recourse characterization. Test robustness against FlowLog, Feldera, Kuzu and scratch/semi-naive execution.

### Project C — extension

Choose one evidence-supported extension: distributed state placement, cross-paradigm recursive compilation, or learned selection among exact execution policies with deterministic fallback. Selection occurs only after A/B expose the bottleneck.

These projects are not artificial slices: A solves a specific system failure, B explains and broadens it, and C changes the deployment setting.

## Other semifinals

- Reliable workflows: semantic verification → interactive repair → cross-dialect workflows is coherent, but rapidly changing models/benchmarks and wrapper collision weaken stability.
- Dynamic vector-relational: dynamic compound filters → mixed joins/aggregates → streams is coherent, but 2025–2026 prior art already occupies much of it.
- Constraint model synthesis: representation → repair → guarantees is coherent only after a concrete application; without one it remains generic LLM+solver.

## Transferable skills

The winner builds database internals, incremental algorithms, graph/Datalog execution, performance measurement, formal semantics and optional adaptive systems. These remain valuable even if the first mechanism fails.
