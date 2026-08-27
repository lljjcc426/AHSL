# R0 Candidate Matrix

Scores are diagnostic; one failed hard gate removes a candidate.

| candidate | exact task / learned decision | high-order necessity | benchmark | strategy variance | classical residual | learnability | certificate | strongest collision | score /75 | fatal gates | verdict |
|---|---|---|---|---|---|---|---|---|---:|---|---|
| A. VE/factor order | partition/marginals; full order | weak-to-moderate; dense cost mostly primal/domain | UAI accepted, XCSP not same task | random huge, classical exact <3x | not established | untested family-disjoint | order always exact | tensor contraction/treewidth | 39 | G3/G6/G7/G8 | kill |
| B. verified GHD/FHD search | exact factor/CSP evaluation; separator/guard moves | strong in theory | HyperBench structure, UAI factors, but no joined execution artifact | decomposition search varies; downstream variance unavailable | recent exact/approximation algorithms strong | untested | deterministic decomposition verifier | DB/CSP decomposition | 49 | G3/G4/G5/G7/G12 | kill |
| C. local separator/bucket ranking | exact elimination/search; next move | unclear beyond graph features | UAI/XCSP | no separate measured residual | min-fill/min-degree strong | untested | complete continuation/fallback | generic learned branching | 41 | G6/G7/G8/G11 | kill |
| D. hypergraph-aware exact-engine portfolio | marginals/CSP; choose JoinInfer/JT/AND-OR | factor sparsity/arity can matter | JoinInfer 52 models, UAI/XCSP | published engine gap up to 630x | hybrid/data-driven rule already exists | no family-disjoint evidence | exact-only portfolio | generic algorithm selection | 51 | G7/G10/G11/G12 | kill |
| E. plan execution-cost model | exact plan ranking | support/cardinality features can use scopes | UAI plans; no repeated workload | cross-plan costs can vary | analytic width/cardinality baselines mature | labels costly/censored | exact execution | learned DB cardinality/cost model | 47 | G6/G7/G11/G12 | kill |
| F. safe proposal + fallback | any exact task; rank candidates | depends on embedded problem | no independent benchmark | inherits embedded problem | inherits embedded problem | no concrete signal | clean fallback | learning-augmented algorithms framework | 41 | G3/G6/G7/G11 | kill |

## Fifteen-axis score detail

| candidate | A | B | C | D | E | F | G | H | I | J | K | L | M | N | O | total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| A | 5 | 3 | 4 | 2 | 1 | 1 | 1 | 5 | 3 | 2 | 2 | 4 | 2 | 2 | 2 | 39 |
| B | 5 | 5 | 2 | 3 | 2 | 1 | 5 | 5 | 3 | 2 | 1 | 3 | 5 | 3 | 4 | 49 |
| C | 5 | 4 | 3 | 2 | 1 | 1 | 3 | 5 | 2 | 2 | 2 | 4 | 3 | 2 | 2 | 41 |
| D | 5 | 3 | 4 | 5 | 3 | 3 | 2 | 5 | 2 | 3 | 4 | 4 | 2 | 3 | 3 | 51 |
| E | 5 | 3 | 4 | 4 | 2 | 2 | 2 | 5 | 2 | 3 | 3 | 4 | 2 | 3 | 3 | 47 |
| F | 5 | 3 | 2 | 2 | 1 | 1 | 2 | 5 | 3 | 2 | 2 | 4 | 4 | 2 | 3 | 41 |

Axes A--O follow the prompt exactly. Zero candidates meet every relevant hard
gate; semifinal and finalist sets are empty.
