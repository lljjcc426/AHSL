# AP0 venue and community map

| Direction | Primary community | Realistic venues | Evidence of fit | Ceiling condition |
|---|---|---|---|---|
| Dynamic/incremental recursive query execution | data management, graph DB, deductive DB | SIGMOD/PACMMOD, PVLDB, ICDE; PODS/ICDT for theory; CIDR for early architecture | PVLDB 2025 published FlowLog and robust recursive parallelism; SIGMOD/PVLDB scopes include engines, graph/network data, languages and theory | new execution method plus broad public workloads, strong modern engines, exactness and end-to-end resource evidence |
| Dynamic vector-relational execution | data management, IR | SIGMOD, PVLDB, ICDE, WWW | ACORN (SIGMOD 2024), SIEVE/UNIFY (PVLDB), VBASE (OSDI) | must exceed dense recent collision and evaluate realistic compound predicates plus updates |
| Reliable enterprise SQL/data workflows | data systems + NLP/ML | SIGMOD/PVLDB, ICLR, ACL/EMNLP, AAAI/IJCAI | Spider 2.0 is ICLR 2025 Oral; CEDAR is PVLDB 2025 | semantic verifier/repair/execution novelty, not another prompting/agent wrapper |
| Constraint model synthesis and verified solving | CP, SAT/SMT, AI | CP, SAT, SMT Workshop, AAAI/IJCAI/KR | stable annual competitions and CP venue | needs a concrete application and contribution beyond generic LLM-to-solver translation |
| Reproducible industrial scheduling | OR/CP/AI | CP, AAAI/IJCAI; domain OR journals | mature solver and benchmark community | strong public real instances and domain-specific algorithmic novelty |

The winning community is stable and publishes systems, algorithms, benchmarks and theory. SIGMOD and PVLDB are the primary high-ceiling targets; ICDE is a realistic systems target; PODS/ICDT become relevant only if the work produces a general complexity or update-bound result.
