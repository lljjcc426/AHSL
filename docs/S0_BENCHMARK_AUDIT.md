# S0 benchmark audit

Grades: **A** direct public real structural/effect labels with defensible splits; **B** real and public but incomplete/derived labels or split issues; **C** useful downstream evidence without structural truth; **D** synthetic/constructed main labels or inaccessible.

## Rank 1 benchmark families

| Route | Input and target | Native high-order evidence | Access | Quality | Audit verdict |
|---|---|---|---|---|---|
| Kuzmin/Boone yeast τ-SGA | measured single/double/triple mutant fitness and trigenic scores; recover/predict triple supports/effects | ~200,000 triple mutants; published analysis reports >30% of trigenic interactions not anticipated from doubles | Science supplements and Dryad `10.5061/dryad.tt367` (CC0); processed Dango data/code public | **A-** | strongest direct route; gene-disjoint and query-double-disjoint splits are needed |
| experimental microbial community landscapes | subset of species present → composition/function; infer non-additive species sets | PNAS 2024 measured all `2^7-1=127` communities; PNAS 2023 used four experimental datasets; 2–4 species RB-TnSeq data show interaction reorganization | article supplements/data repositories | **A-/B+** | second independent domain; small ground sets but unusually complete factorial coverage |
| full-factorial antibiotic combinations | drug subset/dose → bacterial growth; identify emergent/hidden higher-order effects | 3-, 4-, and 5-drug combinations with all lower-order subsets; 54% of 20,790 dose-combinations contained hidden suppression | Mendeley Data and article supplements | **A-/B+** | direct, real and structurally complete; repeated dose/context structure must be respected |
| deep mutational scanning / MoCHI | mutation sets → phenotype/energy; infer energetic couplings | supports higher-order epistasis but most panels have limited observed order | public package and study-specific data | **B** | credible extension, not the first frozen benchmark |
| HODDI/FAERS | reported drug set + adverse event | records contain 2–100 drugs, but co-reporting does not identify an interaction effect | public GitHub; 109,744 constructed records | **C** | secondary stress test only; negative construction and confounding bar causal claims |

The two strongest routes are the yeast τ-SGA screen and experimental microbial/full-factorial antimicrobial landscapes. Both contain measured outcomes for real multi-intervention sets and lower-order subsets, so high-order contrasts are not synthetic labels.

## Rank 2 benchmark families

| Route | Structure | Strength | Weakness | Grade |
|---|---|---|---|---|
| email/thread/contact group events | timestamped recipient/thread/contact sets | direct observed future sets, public, repeated events | repeated-group retrieval can dominate; group formation is not necessarily causal | **B+** |
| coauthorship/tags/congress bills | timestamped author/tag/cosponsor sets | semantically genuine group events and public repositories | time granularity, entity churn, and memorization require careful splits | **B+** |
| directed events (email sender/receivers, reactions, transactions) | left/right hyperedge and event time | membership, cardinality, direction, and time are directly observed | current papers often rank against random negatives; some “directed” conversions are constructed | **B** |

The temporal family has more datasets than Rank 1, but lower benchmark quality for structure correctness because most protocols evaluate sampled ranking rather than full set retrieval. *Prediction Is NOT Classification* supplies direct evidence that this distinction changes method rankings.

## Other screened families

| Family | Representative route | Grade | Reason not finalist |
|---|---|---|---|
| factor scopes | UCI/tabular likelihood, synthetic graphical models | C/D | likelihood does not validate the factor scopes; real high-order truth absent |
| dynamics reconstruction | Kuramoto/Lorenz synthetic; real EEG | D/C | synthetic truth or real data without structural truth |
| projected-network reconstruction | project empirical bipartite hypergraph to a graph, then recover | B-/D | labels are real but the missing-information mechanism is artificially imposed |
| protein complexes | CORUM 5.0, CYC2008, MIPS; PPI/AP-MS input | B | incomplete positives, unknown negatives, overlap and curation leakage |
| causal hypergraphs | simulated SCMs; MCI/brain applications | D/C | real outcomes but no validated causal hyperedges |
| n-ary KG/event | JF17K, WikiPeople, WD50K, CombDrugExt | B | established but primarily fixed-field completion/extraction; crowded and candidate-based |

## Minimum S1 benchmark protocol

1. Use at least two public experimental families, with one containing measured order≥3 effects and the corresponding lower-order subsets.
2. Freeze a response scale and interaction contrast before splitting.
3. Report random-combination interpolation only as a diagnostic; primary evidence is entity-disjoint, query-background-disjoint, or order-extrapolation evaluation.
4. Compare direct support/effect recovery and prospective top-combination discovery; response RMSE alone is insufficient.
5. Do not call unmeasured combinations negatives.
