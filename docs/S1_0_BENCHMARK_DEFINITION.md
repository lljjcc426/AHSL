# S1.0 benchmark definition

## Benchmark ledger

| Field | Yeast tau-SGA | Seven-strain microbial panel | Antibiotic combinations |
|---|---|---|---|
| intervention universe | 1,400 observed genes | seven strains; six companions per focal | eight drugs |
| observed order>=3 units | 91,111 rows / 91,050 unique triples | 127 nonempty communities; seven focal `2^6=64` response landscapes | 20,790 dose contexts for orders 3--5 |
| response | adjusted tau, raw epsilon, fitness and fitness SD | focal-strain CFU, 5--12 flask replicates/cell | growth-derived DA and `E_k` effects/labels |
| context | query pair, array gene, screen/batch | focal strain and community members | drug identity set, dose tuple, order |
| selected estimand | published tau-SGA | log10-CFU Möbius coefficient | dose-specific DA and emergent contrast |
| support label | `p<.05 & tau<-.08`; all else uncertain/null, not error-free negative | 95% bootstrap CI excludes zero and `|beta|>=.10` | source non-additive category; `Inconclusive` remains uncertain |
| identification | measured triple: `IDENTIFIABLE_WITH_NOISE`; unmeasured: `NOT_IDENTIFIABLE` absent a side-information model | full panel: `IDENTIFIABLE_WITH_NOISE`; masked cells: truth retained only retrospectively | dose context with all lower subsets: `DIRECTLY_IDENTIFIABLE`; context-free set support: `PARTIALLY_IDENTIFIABLE` |
| independent experimental unit | query/background screen, not each triple iid | seven dependent focal landscapes from one seven-member system | 182 drug sets, not 20,790 iid structures |
| split/evaluation | query-pair/gene/query-gene disjoint; support F1/AP only on measured test triples | retrospective masking, leave-order/species, budget curves | drug-set/identity/context/order disjoint; no dose-point random split |
| primary metrics | support precision/recall/F1/AP; overlap audit | support precision/recall/F1/AP, sign, coefficient error, pure-HOI recall | context label consistency/sign flips; no cross-set learner fit in S1.0 |

## Scale report

- Yeast: 1,400 genes, 182 query pairs, 410,399 digenic rows, 91,111 trigenic rows, 3,196 strong negative tau labels, 87,915 uncertain/null rows. The paper reports at least two replicate screens; public S1 supplies aggregate scores, p-values, combined fitness SD, and lower-order rows rather than raw plate-level replicates.
- Microbiome: 2,377 CFU measurements, 127 community systems, 5--12 replicates per focal/community cell. Across 294 order>=3 log-scale coefficients: 74 strong positive, 66 strong negative, 154 uncertain/null.
- Drug: 182 independent identity sets: 56 triples, 70 quadruples, 56 quintuples. Measurements are 1,512, 5,670, and 13,608 dose contexts. Order-5 includes 1,138 source-labeled inconclusive emergent cases, which are not support or negatives.

## Unknown rule

An unmeasured tuple is `UNKNOWN`. Retrospective masking is valid only because the underlying real response was measured and is hidden from the estimator; it does not create a biological negative.
