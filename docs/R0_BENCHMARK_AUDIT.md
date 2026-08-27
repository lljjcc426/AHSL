# R0 Benchmark Audit

## Benchmark matrix

| dataset/family | domain | variables | factors/constraints | arity | domains / representation | instances | exact task | baseline | graph-width proxy | hypergraph proxy | observed strategy evidence | real/accepted | access/license | split route | caveat |
|---|---|---:|---:|---|---|---:|---|---|---|---|---|---|---|---|---|
| UAI 2014/2022 PR/MAR/MPE | PGM competition: grids, pedigree/linkage, Promedus, circuits, relational, vision | local audit median 511; range starts at 40 and includes 10,000 | median 225; some families tens of thousands | 85/175 models have max arity >=3; overall max 14 | finite domains; explicit dense UAI tables, zeros retained | 175 PR models locally audited | partition/probability of evidence; archive also supports marginals/MPE | VE/JT, ACE, libDAI, IJGP | min-fill induced-width upper bound | native scopes and factor sparsity; no certified GHD/FHD locally | classical exact ratios 1.28--2.23x on four bounded models | accepted public competition, mixed real/constructed families | public download; page does not state one uniform instance license | model-family-disjoint, then size shift | archive is old/heterogeneous; pairwise and high-order status is strongly family-linked |
| XCSP3 2024--2026 | CSP/COP competition | model dependent | model dependent | unary, binary, n-ary and global constraints | extensional/intensional/global constraints | site reports >23,000; annual selected subsets | satisfiability/optimization with checker | ACE, Choco, CoSoCo, Picat, Toulbar2 and others | primal/incidence and solver features | native constraint scopes; decomposition not standard for every propagator | official traces show solver variability, not R0 factor-plan oracle gap | accepted CP benchmark | public; instance provenance/licenses vary | series/model/generator-disjoint | strongest task is generic CP branching/portfolio selection |
| HyperBench | CQs/CSP hypergraphs | structure only | structure only | varied | scopes without factor tables/domains | 3,648 | exact/heuristic HD/GHD/FHD construction | NewDetKDecomp, HtdLEO, BalancedGo/log-k-decomp | treewidth not the target | certified HD/GHD/FHD where solved | large decomposition-search timing corpus | accepted structural benchmark | Zenodo copy CC BY 4.0 | source-family and size splits | cannot measure downstream probabilistic/CSP execution cost |
| JoinInfer 52-network testbed | UAI'06, PIC 2011, BN Learns | >30 to thousands | varied | 1--10 | sparse listing/trie plus dense-engine contrasts | 52 | all variable/factor marginals | ACE, IJGP, libDAI | min-fill treewidth | FHW ratio plus total bag entries/support | up to 630x cross-engine difference | accepted PGM benchmark collection | paper artifact route; part of sparsity was induced | family/band split conceivable, not reported as learning split | artificial sparsification in some bands; data-driven heuristic already included |
| PACE/treewidth controls | algorithmic graph structures | varied | edges | mostly pairwise | graph | competition scale | decomposition only | exact/heuristic treewidth | direct target | no native high-order advantage | useful control | accepted algorithm benchmark | public by edition | generator/family split | cannot support high-order R0-A |

## Local UAI statistics

The official `PR_prob.tar.gz` archive was downloaded from the UCI/UAI mirror.
All 175 `.uai` models were parsed without copying the archive into Git.

- 21 filename-derived families;
- 85 models with maximum factor arity at least three;
- median 511 variables and 225 factors;
- median factor arity 2; maximum arity 14;
- median model-level median table size 4 entries; maximum single input table
  16,384 entries;
- median model-level median nonzero fraction 0.879.

The smallest models are pairwise DBN/vision/grid families. The first high-order
model has 67 variables (`CSP_12`); many prominent high-order families contain
hundreds to thousands of variables. This makes dense exact oracle sweeps
expensive precisely where native high-order evidence is strongest.

## Representation and gold

UAI supplies the full factor tables and an exact task, so the strategy cost is
not a hidden label. HyperBench supplies structure and decomposition evidence but
not factors. XCSP supplies real solver tasks and high-order constraints but
mixes compact global propagators with extensional scopes; factor-table size and
GHD width are not sufficient cost descriptions.

No benchmark pair simultaneously supplies native high-order factors, repeated
exact inference, certified hypergraph decompositions, multiple fully measured
strategy labels, and a natural family-disjoint amortization workload.
