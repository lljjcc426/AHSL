# S1.0 antibiotic-combination audit

## Data hierarchy

Primary source: Lozano-Huntelman et al., *iScience* 2021, DOI `10.1016/j.isci.2021.102355`; public Mendeley dataset `10.17632/ts2hnd72yf.1`.

| Order | Dose contexts | Independent drug sets | DA support | Emergent support |
|---:|---:|---:|---:|---:|
| 3 | 1,512 | 56 | 311 | 676 |
| 4 | 5,670 | 70 | 2,532 | 2,270 |
| 5 | 13,608 | 56 | 7,844 | 7,911 |
| total | 20,790 | 182 | 10,687 | 10,857 |

The universe contains eight drugs. The combinatorial counts match `C(8,k)*3^k`; dose contexts are repeated observations within a drug identity set, not independent hyperedges. Source-labeled `Inconclusive` is preserved as uncertainty and excluded from support; order 5 has 1,138 emergent inconclusive cases.

## Estimands

The paper's DA/net label compares the full combination under its declared additivity scheme. `E_k` asks whether the highest-order combination is emergently suppressive relative to relevant lower-order combinations and therefore detects hidden suppression missed by single-drug comparisons. Bliss, Loewe, HSA, and ZIP are legitimate alternative families, but they encode different null assumptions and are not interchangeable.

## Dose/context stability

Median modal category fraction across identity sets is 0.636 for DA and 0.547 for emergent labels. Numeric effect sign changes across dose contexts in 98.9% of identity sets for both DA and emergent effects. Order-specific median modal fractions are:

| Order | DA | Emergent |
|---:|---:|---:|
| 3 | 0.852 | 0.593 |
| 4 | 0.593 | 0.599 |
| 5 | 0.539 | 0.422 |

Thus `support(S)` or a single signed hyperedge per drug set is contradicted by the data. The defensible object is `support(S,c)` with `beta_S(c)`, perhaps with partially shared structure across contexts. But only 182 sets and eight identities remain for drug-set/entity-disjoint evaluation, and the near-universal sign changes weaken a shared signed-support assumption.

## Split consequences

- Random dose-point splitting within the same drug set is leakage and is prohibited.
- Drug-set disjointness is feasible with 182 units; drug-identity disjointness is very low-entity and creates large distribution shifts.
- Order extrapolation has orders 3--5 but changes both order and the set/dose lattice.
- Direct labels exist only for measured dose contexts with matching lower-order subsets; unmeasured contexts remain unknown.
