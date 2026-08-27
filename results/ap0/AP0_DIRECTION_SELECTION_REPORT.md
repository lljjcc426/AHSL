# AP0 direction selection report

Search frozen at 2026-08-27. Decision: **AP0-A — GO**.

## 1. Executive decision

Select one parent direction: **dynamic and incremental execution of recursive structured queries** (动态与增量递归结构化查询执行). It scores **80/85** and passes G1–G12. No architecture is selected and no model was trained.

## 2. Why a new parent direction is needed

The prior P0-B conclusion remains unchanged: hypergraph theory/algorithms may be viable, but ML is not a necessary primary component and the former hypergraph × ML coupling is paused. AP0 therefore searched from real CS/AI failures outward. The winning problem is justified by changing-data workloads and modern system limitations, not by code reuse.

## 3. Search methodology

The audit screened 86 de-duplicated primary papers, systems, benchmark specifications and competition resources; 31 were inspected deeply and 18 of those are from 2024–2026. Each family covered foundations, current systems and AI/ML collision. Search snippets and secondary commentary were excluded from counts. Evidence was tested in the order pain → benchmark → collision → residual → feasibility → program depth.

## 4. Candidate-family taxonomy

Five required families were audited. Four bounded semifinal directions survived initial pain/benchmark screening:

1. dynamic/incremental recursive query execution;
2. reliable executable enterprise data workflows;
3. dynamic hybrid vector-relational execution;
4. constraint-model synthesis with verified solving.

Public industrial scheduling was screened but failed before the semifinal because the accessible benchmarks do not establish one modern application residual. No optional family F was warranted.

## 5. Venue/community landscape

The winner has one coherent primary community: data management/database systems, including graph DB and Datalog. SIGMOD/PACMMOD and PVLDB are the high-ceiling venues; ICDE is realistic; PODS/ICDT applies to a theory-forward extension. Current venue programs publish recursive query execution, Datalog engines, graph systems, IVM, benchmarks and AI/data interfaces, demonstrating stable breadth.

## 6. Real pain-point inventory

- differential recursive maintenance can be extremely fast yet retain enough state to exhaust memory;
- deletions/non-monotone recursion can retract derivations and propagate work far beyond an update;
- recursive parallelism changes with source count and frontier shape;
- recursion semantics differ across SQL, Datalog, Cypher/GQL and current engines;
- enterprise text-to-SQL workflows remain unreliable, but current agent/verifier collision is dense;
- filtered vector search under updates is real, but 2024–2026 index collision is denser still.

## 7. Structured data/query systems

VBASE, ACORN, UNIFY and SIEVE establish that vector-relational/filter execution is a serious data-systems topic with strong performance metrics. They also remove the easy novelty. Current work covers arbitrary predicates, range filters, workload-aware index collections and online vector-relational operators. Generic “hybrid vector query engine” is rejected.

Recursive data systems show a different pattern: broad foundations exist, but 2024–2026 papers still introduce nested-recursion optimization, robust recursive parallelism, Datalog-aware Differential Dataflow execution and cross-paradigm compilation. The repeated systems activity is tied to distinct execution failures rather than only benchmark accuracy.

## 8. Structured reasoning/constraint systems

MiniZinc, XCSP3 and SMT-COMP provide strong exact solvers, public instances, annual results and stable communities. This is scientifically healthy but does not itself identify an application-first parent direction. Generic branching, portfolios, cost models or LLM-to-solver translation are explicitly excluded.

## 9. Reliable AI + verified execution

Spider 2.0 is a strong real benchmark: 632 enterprise workflows, schemas often above 1,000 columns, multi-query/multi-dialect tasks and a reported 17.0% o1-preview agent success rate. The residual is large. Nevertheless, CHESS already integrates retrieval, schema pruning, iterative generation and LLM unit tests; CHASE-SQL covers diverse paths and learned selection; CEDAR covers iterative verification and cost-aware routing. A new project needs semantic specification/certified repair or new execution architecture, not another wrapper.

## 10. Dynamic/incremental structured computation

Classical delta maintenance, DBToaster and Differential Dataflow establish the foundation. DBSP gives general heuristic-free incrementalization for rich languages with formally checked results; Materialize and Feldera prove that the idea supports mature systems. This strength narrows, but does not close, the research problem.

The documented residual is resource predictability for exact recursion under changing data. Ammar et al. show differential maintenance orders of magnitude faster than scratch but report memory exhaustion beyond ten concurrent SPSP queries under a 10 GB budget. LDBC SNB v2 adds deep deletes. FlowLog's 2025 system still distinguishes integer-difference incremental deletion, algebraic recursive aggregation and future distributed execution. Robust recursive parallelism (2025) shows fixed scheduling policies fail in different query regimes.

## 11. Structured optimization applications

PSPLIB, MiniZinc, XCSP3, TLSP and iMOPSE provide reproducible routes, and CP-SAT is a formidable open baseline. Yet “scheduling” is too broad: classical public instances often fail to represent current operational constraints, while high-quality industrial data are usually private. Without one accessible domain and documented solver residual, this family fails G4/G5.

## 12. Optional discovered family

None added. Vector-native streaming was considered within A/D rather than inflated into a new family; VectraFlow and recent dynamic ANN systems already provide its correct context.

## 13. Benchmark audit

**Primary:** LDBC SNB Interactive v2. It supplies a correlated graph generator, complex/recursive reads, update streams, deep deletes, drivers and public reference implementations. Metrics can include exactness, throughput, latency percentiles and, for this program, peak state/RSS.

**Second route:** FlowLog's public recursive suite, spanning graph analytics, CFPQ, program analysis (Andersen/CSPA/CSDA, Polonius, DOOP) and multiple recursion shapes, with comparisons to Soufflé, RecStep, DDlog, DuckDB and Umbra where expressible.

These are independent workload families. Synthetic-only evidence cannot carry the project.

## 14. Strong systems audit

The baseline floor is FlowLog + Feldera/DBSP + Differential Dataflow/DDlog, with Kuzu for robust recursive execution and Soufflé/RecStep for compiled/relational Datalog. DuckDB/Umbra are included where their recursion syntax can express the program. Materialize is an architectural reference but too large for the first modification.

All first-gate systems have public code or artifacts. FlowLog and Feldera are the first builds. Exact pinned versions and per-dataset licenses are an AP1 data-freeze task, not an excuse to delay AP0.

## 15. ML/AI collision audit

Learned query optimization, cardinality estimation and LLM query rewriting are crowded. No ML is necessary for Paper 1. A later learned policy is admissible only when AP1 identifies a recurring, unmodeled workload-dependent choice; it must select among correct policies, preserve an exact fallback and beat a classical adaptive rule.

## 16. LLM-wrapper risk audit

The reliable-data-workflow candidate fails the exact-novelty gate today. Execution success is not semantic correctness; adding agents, retries, tool calls or solver feedback is already occupied. Without a new representation, verifier/repair algorithm, execution method, guarantee or benchmark, the work is integration rather than research novelty.

## 17. Engineering feasibility

Paper 1 can extend or instrument one existing single-node engine. Expected components are: build FlowLog/Feldera, workload adapters, exact reference evaluation, state/latency measurement and one bounded execution modification. Rewriting PostgreSQL, building a distributed DB or implementing connectors is unnecessary.

## 18. Compute feasibility

First serious study: 150–450 CPU-hours, 0 GPU-hours, 32–128 GB RAM and 50–250 GB storage. The three-day AP1 discovery gate is capped at 40 CPU-hours, 0 GPU-hours, 64 GB RAM and 100 GB storage. No proprietary API budget is needed.

## 19. Publication ceiling

A focused state/update algorithm with two public routes is a credible systems paper. A strong SIGMOD/PVLDB contribution needs integration into a real engine, broad modern comparisons, exact semantics and causal evidence. A top-ceiling result adds a reusable mechanism and correctness/amortized state or work analysis. The community accepts systems, algorithms, empirical studies and theory.

## 20. Program-depth analysis

- **Project A:** reduce state/tail update cost for exact recursive maintenance under mixed inserts/deletes.
- **Project B:** generalize across recursion/update classes and prove correctness plus resource properties.
- **Project C:** evidence-selected extension to distributed state, cross-paradigm compilation or learned choice among exact policies.

The sequence changes scope at each step and is not an artificial paper split.

## 21. Semifinalists

| Rank | Direction | Research-problem sentence | Outcome |
|---:|---|---|---|
| 1 | dynamic/incremental recursive query execution | Current engines lose predictable state and update latency on recursive changing-data workloads because deletes, intermediate derivations and parallel granularity interact; execution must reduce/bound state while preserving exact semantics. | passes |
| 2 | reliable executable enterprise data workflows | Current agents fail enterprise SQL workflows because executable candidates can still be semantically wrong; a system must verify/repair intent while controlling cost. | fails exact collision/model-independence |
| 3 | dynamic hybrid vector-relational execution | Current indexes lose query/update efficiency under compound filters and evolving vectors because graph connectivity, selectivity and relational operators interact; execution must preserve recall under bounded state/update cost. | fails recent collision |
| 4 | constraint-model synthesis with verified solving | Current generated models can be solver-feasible yet misrepresent intent because syntax/feasibility are weak specifications; a system must validate semantic correspondence. | fails application/benchmark residual |

## 22. Finalists

Only one finalist is retained: dynamic/incremental recursive query execution. Keeping Rank 2 as a finalist would ignore its G6/G11 failures merely to create a tie.

## 23. Candidate scores

| Direction | Score /85 | Hard-gate result |
|---|---:|---|
| Dynamic/incremental recursive query execution | **80** | pass G1–G12 |
| Reliable executable enterprise data workflows | 69 | fail G6, G11 |
| Dynamic hybrid vector-relational execution | 67 | fail G6 |
| Constraint-model synthesis with verified solving | 64 | fail G5, G6 |
| Public industrial scheduling optimization | 61 | fail G4, G5 |

The full 17-axis vectors are in `docs/AP0_CANDIDATE_MATRIX.md`.

## 24. Strongest evidence FOR Rank 1

The gap is triangulated, not inferred from paper count: (i) published real-graph experiments show dramatic incremental speedups and memory exhaustion; (ii) an accepted benchmark now contains deep deletes; (iii) the latest strong system uses general integer differences for deletion maintenance and still identifies scale-out as future work; and (iv) a separate 2025 GDBMS paper proves recursive parallel scheduling remains workload-sensitive. Two public evaluation routes and multiple open systems make the claim falsifiable.

## 25. Strongest evidence AGAINST Rank 1

DBSP/Feldera already incrementalizes rich SQL and recursion, while FlowLog is a 2025 recursion-aware engine over Differential Dataflow with a broad benchmark suite. The remaining gap may collapse to narrow engineering. This is the dominant F1/F4 risk and motivates the cheap AP1 stop gate.

## 26. Hard-gate table

| Gate | Result | Evidence |
|---|:---:|---|
| G1 real CS/AI pain | PASS | OOM/state, delete propagation, tail latency and parallel utilization |
| G2 public primary route | PASS | LDBC SNB Interactive v2 |
| G3 second route | PASS | FlowLog graph/program-analysis suite |
| G4 strong systems leave residual | PASS | DD/DBSP/Feldera/FlowLog/Kuzu audited; published residuals remain |
| G5 not benchmark-only | PASS | same mechanisms occur in graph DB, program analysis, CDC/live views and lineage |
| G6 exact problem unoccupied | PASS | general IVM/recursive optimization occupied; cross-regime exact state/tail objective not established |
| G7 ≥2 contribution types | PASS | algorithm, system and theory; AI optional |
| G8 small-team feasible | PASS | one-engine single-node prototype, public workloads, CPU-only |
| G9 stable venues | PASS | SIGMOD/PVLDB/ICDE/PODS and active systems |
| G10 multi-paper depth | PASS | bounded system → generalization/theory → deployment extension |
| G11 no forced hypergraph/ML/LLM | PASS | none is required |
| G12 bounded falsification | PASS | three-day, ≤40 CPU-hour existing-system audit |

## 27. Final decision

**AP0-A — GO: one parent direction selected.**

Canonical parent: **dynamic and incremental execution of recursive structured queries**. This decision does not authorize a final method or a new engine.

## 28. Exact next action

Run the bounded AP1 discovery task in `docs/AP1_PARENT_DIRECTION_PROPOSAL.md`: build pinned FlowLog and Feldera releases; test four recursive programs over small/medium public inputs and mixed insert/delete batches; record exactness, p50/p95 update latency, throughput and peak RSS; attribute any ≥2× degradation. Stop if the latest systems show no cross-route residual or if the only gap is syntax integration.

## Final handoff A–AI

| Item | Result |
|---|---|
| A | Branch `project-ap0-applied-structured-cs-ai-direction-gate`; final SHA supplied after commit |
| B | 2026-08-27 |
| C | 86 works/resources screened |
| D | 31 deeply inspected |
| E | 18 deep works/resources from 2024–2026 |
| F | five prescribed families; no optional F |
| G | four semifinals |
| H | one finalist |
| I | dynamic and incremental execution of recursive structured queries |
| J | database/data-management systems, graph DB and Datalog |
| K | SIGMOD/PACMMOD, PVLDB, ICDE; PODS/ICDT for theory |
| L | unpredictable retained state and update latency under recursive mixed updates/deletes |
| M | LDBC SNB Interactive v2 |
| N | FlowLog suite with public graph/program-analysis workloads |
| O | FlowLog + Feldera/DBSP + Differential Dataflow; Kuzu recursive execution |
| P | learned/adaptive query optimization is the strongest AI neighbor, but not necessary; no AI baseline is allowed to replace systems baselines |
| Q | incremental execution can be orders faster yet exhaust memory; deletion and parallel regimes remain unstable |
| R | update-sensitive state retention/propagation/scheduling |
| S | exact engine integration with resource-aware recursive execution |
| T | later selection among exact policies only if classical adaptation fails |
| U | correctness and amortized update-work/state/recourse analysis |
| V | 150–450 CPU-hours, 0 GPU-hours, 32–128 GB RAM |
| W | medium: one engine plus adapters/profiling, no new DBMS |
| X | feasible for one primary researcher with limited systems collaboration |
| Y | focused state/tail method → generalization/theory → distributed/cross-paradigm/adaptive extension |
| Z | FlowLog 2025 and DBSP/Feldera generality |
| AA | two public routes plus documented resource residual after mature baselines |
| AB | latest systems may shrink the gap to narrow engineering |
| AC | 80/85 |
| AD | all G1–G12 PASS; table above |
| AE | AP0-A |
| AF | three-day FlowLog/Feldera mixed-update state/latency residual audit, ≤40 CPU-hours, 0 GPU |
| AG | not applicable |
| AH | NO; no new ML model was trained |
| AI | execute AF, then select a bounded AP1 problem only if a cross-route residual survives |
