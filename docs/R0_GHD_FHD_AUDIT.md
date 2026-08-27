# R0 GHD/FHD Audit

## Measures and tractability

For a hypergraph `H`, fractional hypertree width is no larger than generalized
hypertree width, which is no larger than hypertree width. Width one for GHD is
equivalent to alpha-acyclicity. Bounded decompositions support tractable CSP,
conjunctive-query and semiring algorithms when factor/relation representation
cost is included.

These widths are not interchangeable with runtime. A decomposition bag needs a
guard or fractional edge cover, but its actual execution also sees relation
support, domain sizes, deterministic zeros, message sizes and join method.
JoinInfer's `rho`-style total processed entries is an explicit example of a
quantity needed beyond a width ratio.

## Construction difficulty

General and fractional hypertree-width recognition is computationally hard in
the general fixed-width regimes studied by Fischl, Gottlob and Pichler. R0 does
not assume that an optimizer can “simply minimize GHW”. A learned proposal would
need a deterministic decomposition verifier and a complete classical fallback.

Recent work sharpens rather than removes the classical baseline:

- Lanzinger and Razgon give an FPT approximation under bounded intersections
  (STACS 2024);
- Gottlob, Lanzinger, Okulmus and Pichler give fast parallel exact-HD search and
  evaluate 3,648 HyperBench hypergraphs (TODS 2024);
- Korchemna et al. give new approximation algorithms for FHW (2024);
- LP/branch-and-bound methods for FHD were evaluated across HyperBench in
  2024--2025;
- Lanzinger, Razgon and Unterberger give exact FPT parameterizations when
  width, rank and maximum degree are parameters (2025).

## Benchmark mismatch

HyperBench is strong evidence for decomposition construction: it contains
3,648 query/CSP hypergraphs and supports exact/heuristic decomposition timing.
It does not contain factor tables, domain semantics, repeated probabilistic
queries or downstream exact-inference cost. Consequently a learner that lowers
decomposition time or width there does not yet establish inference gain.

UAI factor models provide tables and exact tasks, but published and local R0
evidence chiefly uses primal min-fill junction constructions. No public mapping
was found that couples UAI instances to independently certified GHD/FHD
alternatives and comparable downstream execution traces.

## R0 discipline

No exact GHW or FHW values are claimed in R0. The saved UAI audit reports only
primal induced-width upper bounds, alpha-acyclicity on manageable unique-scope
sets, and factor statistics. This candidate fails the benchmark-to-execution
link before any learned separator model is justified.
