# P0 project history map

Reassessment date: **2026-08-27**. This map treats every phase at its frozen
commit. Later phases may narrow an earlier conclusion, but do not rewrite it.

## Master project-level matrix

| Phase | Research question | Learned object | Hypergraph-theory object | ML necessity | Hypergraph necessity | Real benchmark | Independent truth | Identifiability | Classical residual | Prior-art residual | Main failure | Failure class | Transfer strength | Reopening condition | Current status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A0 | Does a known join-tree connected-subtree restriction denoise corrupted incidence rows? | categorical subtree distribution | alpha-acyclicity, running intersection, fixed join tree | failed: exact projection/MAP was stronger | yes for the restricted synthetic object | no; synthetic | clean generator truth only | exact conditional on known tree | exact projection dominated learned estimator | not the controlling issue | learned objective and hard decision were misaligned | F4, F7, F9 | strong for other exact-projectable structural priors | a real task plus a nonclassical residual | neural A0 stopped; structural prior retained |
| A0.5 | Is connectedness gain real and can exact DP remove enumeration cost? | none required; possible future tree estimator | exact connected-subtree DP, join-tree MWST | not established | yes in the declared known-tree class | no; synthetic | clean generator truth | conditional on known tree/noise | positive connectedness gain; noisy MWST left an R=1 gap | not audited broadly | no phase failure; topology and synthetic limits constrained continuation | none as phase; warnings F2/F9 | moderate | proceed only through the preregistered classical gate | completed, proceeded |
| A0.75 | Does a residual remain after stronger classical join-tree estimation? | possible learned edge/tree score | join-tree identity, MWST, subtree DP | plausible but untested | yes for tree identity/decoder | no; synthetic | generating tree and clean incidence | finite-sample weak, population result later | best classical excess 0.01714; residual in three non-star families | not decisive | no stop; a narrow residual survived | none as phase; warnings F2/F9 | weak-to-moderate outside latent-tree estimation | held-out marginal-likelihood kill-test | completed, proceeded |
| A1 | Can marginal likelihood estimate the latent join tree and close the downstream gap? | tree and subtree prior parameter q | alpha-acyclic join tree and exact marginal scorer | not justified | yes for this formulation | no; synthetic | generator tree/rows | population-identifiable away from degeneracies, weak finite-sample signal | marginal estimator did not beat BinaryMWST; negative gap closure | no direct fatal collision | likelihood improved while downstream Hamming did not; no observable real covariates | F2, F4, F9 | strong for latent-structure objectives | external task with observable covariates and tractability target | latent-tree ML paused |
| A1.5 | Does decision-aligned posterior risk reveal tree-learning value? | tree source and posterior decision | exact connected Bayes-Hamming decoding | tree learning failed necessity; posterior modeling retained | connectivity mattered modestly | no; synthetic | generator truth | conditional posterior identifiable under model | tree gain failed the three-topology rule; decoder gain positive | decoder is classical MBR/centroid theory | useful signal came from decoder, not learned tree identity | F4, F7, F9 | strong for latent-structure learning; weak for posterior decoding | real covariates and a transferable conditional prior | tree-identity learning stopped |
| B0 | Is there a public real task for a feature-conditioned subtree prior and exact DP? | shared conditional subtree prior | connected support on a supplied real tree | not established | failed in most natural tasks | eight real task families audited; none passed all gates | domain labels varied | target/scaffold often mismatched or uncertain | no coherent task reached a baseline test | several mature task-specific formulations | no task jointly supplied the right output class, covariates, tree and material exact inference | F2, F6, F7 | near-fatal for the AHSL main line | external dataset satisfying all B0 data/task gates | AHSL ML line closed |
| N0 | Is there a new strong hypergraph-theory/ML project? | reaction costs with uncertainty | exact directed hyperpaths and robust certificate | plausible at proposal stage | plausible and native | Reactome/NCI-PID route identified | curated pathways | not yet audited | not yet audited | no fatal direct collision found | no phase failure; selected CertPath for a bounded gate | none as phase | none until N1 evidence | pass N1 supervision/attainability before modeling | topic selection GO |
| N1.0 | Can curated pathways supervise attainable positive-cost exact hyperpath recovery? | reaction costs | directed cyclic hyperpath optimization and robust optimality | not reached | native hypergraph semantics active | Reactome V89/V97 | curated pathway sets, but task-selected | only 59.32% of natural tasks attainable; 456 infeasible without repair | not reached | no fatal direct collision | objective class excluded a large natural label population | F2, F3, F9 | strong for constrained decoding with curated labels | valid/attainable task universe without repair and leakage | CertPath closed |
| S0 | Which structure-learning subfield has the best evidence? | none; subfield selection | broad high-order structural objects | screened, not trained | screened | several candidate benchmark families | heterogeneous | delegated to S1/S2/S3 | delegated | delegated | no failure; selected high-order interaction recovery | none as phase | none until follow-up gates | survive the concrete estimand/benchmark gate | selection GO |
| S1.0 | Is sparse order>=3 interaction support directly recoverable across real domains? | support/effects/uncertainty | hyperedges as Möbius/ANOVA support | possible on incomplete panels | native hypergraph theory not required; sparse polynomial support sufficed | yeast, microbiome, drug panels | only one complete microbial route supplied retrospective direct truth | one route identifiable; cross-domain target not | material residual only on one seven-strain panel | Dango and sparse/adaptive Möbius recovery occupy nearest routes | no second direct domain; estimand/label changes by domain and dose | F2, F3, F5, F6 | strong for latent interactions and scientific mechanism discovery | second replicated order>=3 panel with required subsets and direct truth | NO-GO |
| S2.0 | Is open-world future complete-set prediction a valid unsaturated problem? | future exact event set/time/roles | set-valued hyperedges; search space | potentially yes | native width/acyclicity unnecessary | Ubuntu and Congress pass real-data gates | future events directly observed | event identity direct for observed future | local search recall below 1%; no isolated scorer residual | HyperSearch directly covers safe novel-set search | correct protocol already occupied; remaining issue is search/node support, not isolated structure learning | F5, F6 | strong for hyperedge prediction/evaluation | new same-protocol residual beyond HyperSearch with adequate search | NO-GO |
| S3.0 | Can natural partial observations identify latent high-order structure? | latent hyperedges/complexes/couplings | projection, scopes, complexes and hypergraph recovery | sometimes, but cannot repair non-identifiability | usually failed necessity against graph/matrix/tensor models | several natural observation routes | no candidate had two routes with independent structural gold | generally partial or non-identifiable | classical inverse/latent models cover viable targets | direct modern projection/dynamics/complex work | favorable naturality, gold, identifiability and residual never coincide | F3, F4, F5, F6, F9 | near-fatal for latent recovery without external gold | two real routes, one independent A/B gold, plus measured hypergraph-only residual | NO-GO |
| R0 | Can learning improve exact inference on known high-order factor structures? | order/decomposition/engine/cost surrogate | GHD/FHD, fractional covers, exact factor inference | failed on current artifacts | native structure matters in some sparse regimes, not in local residual | UAI, XCSP, HyperBench | exact answers/certificates | direct and verifiable | competent classical ratios 1.28--2.23x; no two-family >=3x gap | generic solver learning, joins and tensor contraction collide | no material hypergraph-specific, learnable and amortizable residual | F4, F5, F6, F8 | near-fatal for solver-learning formulations | two repeated factor families, >=3x gap, family-disjoint predictability and hypergraph-feature gain | NO-GO |

## Phase dossiers

### AHSL sequence: A0--B0

The strongest positive result is not an ML result: exact connected-subtree DP
validated a real structural denoising effect in three non-star synthetic
families and scaled to `m=1024`. The strongest negative result is the separation
between structural validity and learned value. Exact projection, matched
posterior decoding and classical tree estimates absorbed most of the gain. The
line ultimately lacked a public task whose output class, scaffold, covariates
and loss matched the mathematics.

### CertPath sequence: N0--N1.0

N0 found a credible native directed-hypergraph proposal with exact decoding and
a robustness certificate. N1.0 then showed that the supervised object was not
representative: 961/1,620 natural tasks were positive-cost attainable and 456
gold sets required prohibited repair or a changed query. This is scientific
representability evidence, not an implementation failure.

### Structure-learning sequence: S0--S3.0

S0's two strongest candidates had better real-data footing than AHSL. Their
follow-up gates failed for different reasons. S1.0 found one identifiable
microbial panel but no second direct domain. S2.0 found two strong real temporal
datasets, but the correct open-search task was already occupied by HyperSearch.
S3.0 found natural partial observations, but not independent gold,
identifiability and a hypergraph-only residual in the same candidate.

### Known-structure exploitation: R0

R0 avoided the unknown-structure problem and preserved exactness. It therefore
supplied evidence independent of S1/S3 identifiability failures. Its stop was
instead classical residual, benchmark coupling, amortization and collision with
generic solver, join-order and tensor-contraction learning.

## Git and reproducibility map

| Phase | Frozen commit / branch evidence | Remote branch | Reproduction status |
|---|---|---|---|
| A0 | `2a8a6f1`, `main` | yes | scripts, raw/aggregate results and tests; local tests only |
| A0.5 | `ab6baff`, `phase-a0.5-dp-robustness` | yes | configs, runner, raw/aggregate results and tests |
| A0.75 | `e6cc495`, `phase-a0.75-classical-a1-kill-test` | yes | configs, runner, logs, raw/aggregate results and tests |
| A1 | `dd275e7`, `phase-a1-marginal-likelihood-latent-tree` | yes | configs, runner, logs, raw/aggregate results and tests |
| A1.5 | `930ebc0`, `phase-a1.5-decision-aligned-posterior-risk` | yes | configs, runner, logs, raw/aggregate results and tests |
| B0 | `674d712`, `phase-b0-real-task-shared-prior-feasibility` | yes | documentation/search audit; no experiment authorized |
| N0 | `3a7839c`, `project-n0-topic-discovery-gate` | yes | documentation/search audit; no model |
| N1.0 | `4f45a6b`, `project-n1.0-supervision-attainability-gate` | yes | data builders/audits/tests; downloaded data ignored |
| S0 | `283dfbf`, `project-s0-high-order-structure-learning-landscape` | yes | documentation/search audit; no model |
| S1.0 | `e21fb3e`, `project-s1.0-estimand-benchmark-classical-gate` | yes | CPU audit/baselines/tests; Dango reproduction blocked by absent upstream inputs |
| S2.0 | `b28a32e`, `project-s2.0-temporal-group-event-gate` | yes | audit/baseline scripts, raw results and tests; external data ignored |
| S3.0 | `f4a360a`, `project-s3.0-natural-partial-observation-structure-gate` | yes | search audit and saved small ambiguity result; no large experiment |
| R0 | `6f2147a`, `project-r0-learning-augmented-exact-inference-gate` | yes | UAI audit script, raw results and tests; external data ignored |

All listed phase branches exist on `origin`. The repository contains no GitHub
Actions workflow, so reported checks are local rather than remote CI checks.
