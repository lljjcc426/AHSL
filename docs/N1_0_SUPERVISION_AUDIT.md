# N1.0 supervision audit

## Release inventory

V89 is the historical snapshot and V97 is the later temporal snapshot. V89 contains 2,711 parsed pathways and 1,530 natural tasks; V97 contains 2,883 parsed pathways, 1,641 leaf pathways with retained reactions, and 1,620 natural tasks.

## Natural universe and construction

Each V97 leaf pathway contributes one whole-pathway reaction-set label. Inputs are the full V97 hypergraph, global sources, declared gold-boundary inputs, and all declared terminal outputs. Internal cyclic repair is prohibited. See `N1_0_SUPERVISION_DEFINITION.md` for the formal query.

## Gate flow

| Stage | Tasks | Fraction of 1,620 |
|---|---:|---:|
| natural candidates / unique pathways | 1,620 | 100.00% |
| gold feasible without internal repair | 1,164 | 71.85% |
| positive-cost attainable | 961 | 59.32% |
| nontrivial gold size at least 3 | 1,341 | 82.78% |
| qualified: feasible + attainable + size at least 3 | 712 | 43.95% |

The 456 infeasible tasks (28.15%) would require internal source repair or a different label/query. They are not repaired. Among the 1,164 feasible tasks, 203 contain a feasible proper gold subset and are unattainable under every strictly positive additive cost vector.

## Attainability and family distribution

The hard-gate denominator is the natural query-valid universe: 961/1,620 = 59.32%, below 70%. The conditional 961/1,164 = 82.56% among feasible tasks is reported for diagnosis only and cannot replace the frozen denominator. Qualified tasks span all 29 observed top-level families; sample scale and family diversity pass but cannot override representability failure. Per-family counts are in `results/n1_0/aggregated/attainability_by_family.csv`.

Stratification confirms that failure is structural rather than confined to one label size: attainability is 89.25% for size 1--2, 69.61% for size 3--5, 48.80% for size 6--10, 37.50% for size 11--25, and 35.44% for size 26+. Acyclic gold sets are attainable in 918/1,049 cases (87.51%), while cyclic gold sets are attainable in only 43/571 (7.53%). Tasks with any multi-tail reaction are attainable in 939/1,596 cases (58.83%); singleton-tail-only tasks are 22/24 (91.67%). By terminal count, the largest well-populated strata decline from 74.05% at one target and 71.03% at two targets to 52.98% at five targets and 44.26% at nine targets; small high-target strata are reported in the raw CSV rather than overinterpreted. V89 contributes 1,530 tasks for temporal matching; the full attainability gate was frozen and evaluated on V97.

## Nontriviality and high-order activity

Gold size: mean 8.45, median 6, p95 25, maximum 66; 61.23% contain at least five reactions. At least one multi-tail reaction occurs in 98.52% of tasks, and the mean fraction of multi-tail reactions within a gold set is 87.72%. This is evidence that the annotated objects are high-order, not proof that graph projection selects different solutions.

## Exclusion bias

Qualified tasks have mean size 8.28 and cycle rate 5.90%; excluded tasks have mean size 8.59 and cycle rate 58.26%. Multi-tail fractions are similar (87.57% versus 87.84%). The filter therefore removes cyclic pathways disproportionately. Reporting only the 712 survivors would materially distort the biological task universe.

## Decision

Sample scale: PASS (712 tasks, 712 unique pathways, 29 families). Source-leakage gate: PASS because no retained task uses internal repair and declared boundaries are exposed in the query. Representability: FAIL (59.32%); the 456 infeasible labels remain in the natural-universe denominator and are not repaired. CertPath must stop before ML.
