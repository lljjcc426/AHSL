# AP0 literature landscape

The audit screened 86 primary works/resources and deeply inspected 31; 18 deep items are from 2024–2026. The itemized ledger is in `AP0_SEARCH_LOG.md` and bibliographic records are in `references/ap0_references.bib`.

## Family A — structured data/query/execution

Classical foundations include relational optimization, multiway joins, recursive SQL/Datalog and approximate nearest-neighbor indexes. Current systems separate into recursive/graph query engines and vector-relational engines. VBASE reports up to three orders of magnitude improvement for complex vector-relational queries; ACORN reports 2–1000× higher throughput at fixed recall; SIEVE, UNIFY, DIGRA and RangePQ further occupy filtered and dynamic filtered search. This density makes generic filtered vector search a poor parent-direction choice.

The remaining credible pain is not “use vectors in SQL”, but execution under changing inputs, recursion, deletions, state growth and mixed query semantics.

## Family B — structured reasoning/constraints

SAT/SMT/CP have mature solvers and annual competitions (SMT-COMP, MiniZinc Challenge, XCSP). Benchmarks and exact metrics are excellent. The weakness for AP0 is application specificity: generic branching, portfolio selection or LLM-to-model translation is already a method-first solver project. Without a chosen real application, the residual is solver-centric rather than application-first.

## Family C — reliable AI with executable backends

Spider 2.0 exposes a major real residual: the reported o1-preview agent solves only 17.0% of 632 enterprise workflows. BIRD and LiveSQLBench provide independent routes. However, CHESS, CHASE-SQL, execution-guided decoding, CEDAR and many agent pipelines already cover schema retrieval, candidate diversity, execution feedback, unit tests, selection and iterative repair. A valid future project would need a new semantic specification, verifier/repair algorithm or execution architecture; filtering invalid outputs is insufficient.

## Family D — dynamic/incremental structured computation

Foundations range from classical delta rules and higher-order IVM to Differential Dataflow. DBSP gives a general, formally checked incrementalization framework for rich query languages, while Materialize and Feldera demonstrate mature implementations. These systems do not eliminate workload-sensitive residuals:

- differentially maintained recursive graph queries can be orders faster than recomputation yet exhaust memory;
- deletions and non-monotone recursion enlarge retained state and propagation work;
- parallel recursive execution is sensitive to source/frontier granularity;
- SQL, Datalog, Cypher/GQL and graph systems retain incompatible recursion features;
- current engines still publish recursion-aware optimization papers (Temporel 2024, robust recursive parallelism 2025, FlowLog 2025, Raqlet 2026).

This is the strongest application-first program because its first paper can be an algorithm/system contribution, while AI remains optional.

## Family E — structured optimization

Scheduling and configuration have clear operational value, mature solvers (CP-SAT, Gurobi, SCIP) and public libraries (PSPLIB, MiniZinc/XCSP). Yet generic public instances often no longer match a specific modern deployment, while the best industrial workloads are frequently private. Selecting “scheduling” before a concrete accessible domain would repeat the method-first error. The family remains viable only after acquiring a domain-specific public workload.

## Literature conclusion

Rank 1 is **dynamic and incremental execution of recursive structured queries**. Its novelty is not generic IVM; it is the still-measurable execution problem at the intersection of changing data, recursion, deletion/non-monotonicity, state cost and exact semantics.
