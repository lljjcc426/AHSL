# AP-R0 data-systems audit

## A1: hybrid structured-vector execution

New evidence since AP0 exists. The 2025--2026 landscape now includes a broad
[Hybrid-ANNS experimental evaluation](https://www.vldb.org/pvldb/vol19/p183-zheng.pdf),
[RVBench](https://web.iitd.ac.in/~kbeedkar/publication/27-edbt-rvbench/),
Honeybee, VectraFlow and current ACORN/SIEVE/DIGRA/RangePQ systems. This is
enough to re-screen but not to promote the former runner-up.

The Hybrid-ANNS repository compares many algorithms on real datasets but stores
datasets separately and uses heterogeneous environment scripts. Its frozen
commit was inspected; a fair current multi-system run was not feasible within
the two-hour pre-gate. RVBench likewise did not yield a bounded local execution
route. Without a current residual, selecting only a convenient engine or a
synthetic filter distribution would violate the no-artificial-residual rule.

Prior-art collision is dense: arbitrary filters, workload-aware index
collections, dynamic range filters and mixed vector-stream operators directly
occupy the plausible mechanisms. A1 fails G5 and G10.

## Other data routes

Adaptive query processing, multi-query reuse and lineage remain important, but
the search did not expose a current public primary/secondary benchmark pair plus
a >=2x same-system failure and open nontrivial intervention. Obvious materialized
CTE/cache/configuration comparisons were excluded because they would fail G6/G9.

AP1.0 recursive incremental execution remains closed; no prohibited rescue
route was attempted.
