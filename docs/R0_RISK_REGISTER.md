# R0 Risk Register

| ID | risk | evidence | consequence | treatment |
|---|---|---|---|---|
| R1 | compare against random rather than tuned classical orders | random UAI orders are catastrophically bad | inflated “ML gain” | use min-fill, weighted min-fill, min-degree and factor-entry greedy |
| R2 | call a primal induced-width upper bound exact treewidth | heuristic orders only | false structural claim | label every local width as an upper bound/proxy |
| R3 | call a heuristic decomposition exact GHW/FHW | recognition/construction hardness | false certificate | no GHW/FHW values claimed without verifier |
| R4 | hide exponential dense factor input | one large hyperedge toy | fake tractability | record table sizes/domains/support representation |
| R5 | infer runtime from width alone | UAI equal-width orders still vary modestly | wrong cost model | report entries and wall time separately |
| R6 | family leakage | UAI arity/domain patterns strongly identify families | memorized strategy choice | require family/generator-disjoint split before learning |
| R7 | oracle labels cost multiple exact solves | strategy sweeps and timeouts | no amortization | require stable repeated workload or trace labels |
| R8 | censored runtime labels treated as exact ranks | timeouts common in exact solving | biased preference model | survival/censored comparison if future work proceeds |
| R9 | learned pruning changes correctness | non-admissible score | false exactness | prediction ranks only; deterministic bound authorizes pruning |
| R10 | HyperBench width gain substitutes for inference gain | no factors/domains | wrong downstream claim | require coupled factor execution artifact |
| R11 | XCSP high arity substitutes for hypergraph necessity | global propagators dominate | cosmetic hypergraph framing | compare native propagator/solver features |
| R12 | cost-model work duplicates databases | FAQ/join equivalence | weak novelty | demand semiring/evidence/repeated-query residual |
| R13 | ordering work duplicates tensor contraction | same contraction tree/FLOP objective | weak novelty | demand sparse deterministic factor-specific evidence |
| R14 | engine portfolio duplicates generic solver selection | JoinInfer and CP portfolios | wrong interface | fail G11 absent indispensable hypergraph feature |
| R15 | tiny classical residual motivates a larger neural model | local exact ratios <3x | wasted modeling | stop at R0; no model training |

The dominant risks are evidenced, not hypothetical. No extra defensive layer is
added beyond the exactness verifier/fallback that the scientific contract
requires.
