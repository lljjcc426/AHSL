# Project S3.0 Gate Report

## 1. Executive decision

**S3.0-E — NO-GO: CLASSICAL / LATENT-MODEL SATURATION.**

Six families were screened through naturality, real gold, independence,
identifiability, graph/matrix/tensor reduction, classical inverse methods and
recent ML. None satisfies the semifinal requirements; therefore there are zero
semifinals and zero finalists.

The decisive candidate is protein-complex recovery from CF-MS/AP-MS/PPI
evidence. It has the strongest natural observation mechanism and the closest
thing to real structural gold, but standard pipelines already transform
pairwise evidence into overlapping sets through pair scoring and graph
clustering; CORUM/Complex Portal are incomplete positives and often enter the
pipeline itself. This makes **E**, rather than a weaker claim that all candidate
observations are artificial, the most accurate project-level decision.

## 2. Search scope

The search was completed on **2026-08-27**. It screened **50** directly relevant
works, deeply reviewed **22**, and deeply reviewed **14** works dated
2024--2026. Six families were examined: projection, dynamics, pooled assays,
censored events, scientific complexes/modules and low-order marginals. Search
details and row-level count reconciliation are in
`docs/S3_0_SEARCH_LOG.md`.

## 3. Definition of natural partial observation

The estimand is `Y -> H*` under `H* -> O -> Y`, where `H*` includes at least
one order-three relation and the real observation process `O` withholds its
identity. Natural sensor limitation, aggregation, censoring, low-order
projection and dynamical response qualify. Author-generated masking or
projection of an already observed hypergraph is diagnostic only.

Structure recovery is distinct from fitting or predicting `Y`. An unobserved
relation is not a negative label. Exact recovery is only meaningful when the
observation map is injective on an explicitly declared model class.

## 4. Candidate families

| family | strongest domain | disposition |
|---|---|---|
| low-order projection -> hyperedges | social/affiliation/PPI graphs | kill: non-injective and benchmark partiality usually artificial |
| dynamics -> coupling scopes | EEG, oscillators, biochemical dynamics | kill: natural data, but real structural truth and assumptions fail |
| pooled measurements -> interactions | combinatorial CRISPR/group testing | kill: sparse effect estimation, not hidden event-set recovery |
| censored relational events -> full events | wildlife/sensor/privacy logs | kill: unknown MNAR censoring and no paired full gold |
| indirect assays -> complexes | CF-MS/AP-MS/PPI proteomics | kill: incomplete/circular gold and classical/modern saturation |
| low-order marginals -> dependencies | privacy/statistics | kill: operator-kernel non-identifiability and log-linear saturation |

## 5. Observation-mechanism taxonomy

Projection can be natural type D, but the main method benchmarks use type F:
known hyperedges are projected computationally. Dynamics is type E, pooled
screens type B, censored events type A/C, complexes type A/B/D, and released
marginals type B/D. Only the latter five mechanisms are intrinsically natural;
their other gates still fail.

## 6. Latent-structure taxonomy

Projection and censored events target A/B hyperedge identities or weights;
dynamics targets B/C/E weighted, signed or directed mechanisms; complexes target
D latent overlapping sets. Pooled screens usually target C coefficient support,
and marginal models target F factor scopes. Decomposition alone was excluded.

## 7. Real benchmark inventory

The most concrete real routes were:

- 218 resting-state EEG time series aggregated to seven brain areas in THIS;
- CF-MS/SEC protein profiles evaluated with CORUM 5.0, whose resource contains
  7,193 complexes and 5,873 gene products;
- hu.MAP3.0, integrating more than 25,000 proteomic experiments into more than
  15,000 predicted complexes;
- five published dual-CRISPR studies consolidated in a 2025 scoring benchmark;
- small animal group-by-individual/imperfect-detection studies;
- privacy-released low-order contingency marginals.

None provides both one natural route with independent A/B structure gold and a
second route for the same estimand. The complete inventory is in
`docs/S3_0_BENCHMARK_AUDIT.md`.

## 8. Structural-gold audit

Projection benchmarks have A-quality labels only because the original
hypergraph was available before projection; this does not validate a naturally
pairwise-only domain. Real EEG provides C/E evidence, not higher-order support
truth. CORUM can be B-quality under an assay- and publication-disjoint protocol,
but is partial and routinely used for training, filtering or tuning. Unknown
complexes cannot be labeled absent. Pooled coefficients are defined by the same
assay response, while censored-event and privacy routes lack public full truth.

Project-level G3 and G4 fail.

## 9. Identifiability analysis

- Projection: class D generally; class B only under explicit random-uniform,
  sparsity, multiplicity or supervised-prior assumptions.
- Dynamics: class B in a controlled, fully observed and persistently excited
  system with a correct nondecomposable library; class D/E on current real data.
- Pooled designs: class B for sparse coefficients under classical design
  conditions; the target is not event identity.
- Censored events: class D under unknown MNAR detection.
- Complexes: class C/D because co-elution, moonlighting, subcomplexes and shared
  profiles admit several set explanations.
- Marginals: class D because higher-order terms vary in the kernel of the
  marginalization operator.

No candidate supplies an empirically supported A/B identification route for the
requested real structural object.

## 10. Assumption plausibility

The dynamics candidate requires all relevant states to be measured, persistent
nonlinear excitation, correct functional library, sparsity, adequate derivative
estimation and negligible latent confounding. Those assumptions are not
demonstrated for resting-state EEG or observational ecology. Complex inference
requires stable extraction, separable/coherent elution, context agreement and
limited protein moonlighting; observed assay biology directly violates the
strong versions. Projection theory assumes uniform random hypergraphs or rich
side information not justified in candidate natural networks. Calibrated
detection is absent for censored group events.

## 11. Projection / observation ambiguity

For the unweighted clique projection, exhaustive small-case enumeration found:

| nodes | allowed orders | hypergraphs | projection classes | unique classes | ambiguous classes | max preimages |
|---:|---|---:|---:|---:|---:|---:|
| 3 | 2--3 | 16 | 8 | 7 | 1 | 9 |
| 4 | 2--4 | 2,048 | 64 | 41 | 23 | 1,569 |
| 5 | 2--3 | 1,048,576 | 1,024 | 388 | 636 | 608,273 |

Thus even a complete projected graph admits hundreds of thousands of preimages
at five nodes. The saved aggregate is
`results/s3_0/raw/projection_ambiguity.json`. For dynamics, decomposable coupling
functions and local linearization make pairwise and higher-order structures
observationally equivalent. For censoring, event composition is confounded with
detection propensity.

## 12. Graph-reduction audit

Projection candidates reduce to clique cover, Bayesian graph compression,
overlapping community detection or SBM variants. Protein complexes reduce to
pair scoring followed by MCL, MCODE or ClusterONE; these algorithms already
return possibly overlapping node sets. Censored event data can be modeled with
association networks or latent communities when exact event identity is absent.
No measured hypergraph-only advantage was isolated.

## 13. Matrix/tensor collision audit

Pooled measurements are sparse matrix/tensor regression. Complexes admit NMF,
co-clustering and multi-view factorization. Low-order moments identify latent
components under established CP/Kruskal/multi-view conditions. Privacy
marginals are linear constraints on a contingency tensor. In each case the
hypergraph is an interpretation of support or factors, not a distinct
identifiable object with stronger evidence.

## 14. Community/latent-model collision audit

Pairwise evidence -> latent groups is already the task of mixed-membership SBM,
affiliation models, BigCLAM-like overlapping communities and related latent
feature models. Protein-complex algorithms instantiate the same collision in a
scientific domain. Without independent event-set truth, calling a community a
hyperedge changes terminology rather than the estimand.

## 15. System-identification collision audit

SINDy, sparse polynomial regression, Kramers--Moyal inference, reaction-network
lasso, Granger/transfer-entropy variants and nonlinear system identification
already recover active multivariate terms. A higher-order edge names the support
of such a term. THIS, the 2024 algebraic and Kramers--Moyal methods, Bayes-THIS
and multiplex extensions occupy sparse, weighted, directed, Bayesian and
multilayer versions. The missing element is real structural truth, not another
learner.

## 16. Classical inverse-method audit

The strongest collisions are Bayesian/MDL clique cover for projection; SINDy
and sparse nonlinear regression for dynamics; compressed sensing/group testing
for pools; capture--recapture/occupancy models for censoring; pair scoring plus
overlapping graph clustering for complexes; and iterative proportional fitting,
maximum entropy and hierarchical log-linear models for marginals. Their theory
already includes sparsity, design, uniqueness, noise and uncertainty.

## 17. Modern ML audit

ICLR 2024, COLT 2024/25 and MARIOH 2025 cover projected-hypergraph
reconstruction and its thresholds. Dynamics has multiple direct 2024--26
methods. NAIAD covers combinatorial perturbation response and acquisition.
hu.MAP3.0 and mCP demonstrate mature large-scale and FDR-aware complex
pipelines. Modern work does not solve the absent-gold problem, but it does remove
the claimed method novelty where the inverse problem is evaluable.

## 18. Candidate semifinals

**None.** Every family fails at least one of natural partiality, real independent
gold, meaningful identifiability, non-classical residual or direct structural
evaluation. Weak candidates were not retained to fill slots.

## 19. Candidate finalists

**None.** Consequently finalist-specific observation process, primary/second
benchmark and exact remaining gap are not asserted. Protein complexes are the
closest rejected candidate, not a finalist.

## 20. Candidate scoring

| candidate | naturality | meaning | gold | ID | HO need | G/M/T residual | classical residual | modern novelty | eval | benchmark | feasible | theory | publish | depth | total /70 | fatal gates |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| projection | 3 | 4 | 1 | 2 | 4 | 3 | 3 | 2 | 3 | 2 | 5 | 4 | 2 | 2 | 40 | G2/G3/G5/G8 |
| dynamics | 5 | 4 | 1 | 2 | 4 | 3 | 2 | 2 | 2 | 3 | 5 | 5 | 3 | 5 | 46 | G3/G4/G6/G7/G9 |
| pooled | 5 | 3 | 1 | 4 | 2 | 2 | 1 | 2 | 3 | 4 | 5 | 4 | 3 | 4 | 43 | G3/G7/G9/G11 |
| censored events | 5 | 4 | 0 | 1 | 4 | 3 | 3 | 4 | 1 | 1 | 2 | 3 | 2 | 2 | 35 | G3/G4/G5/G10 |
| complexes | 5 | 5 | 2 | 2 | 5 | 2 | 1 | 1 | 3 | 4 | 5 | 2 | 3 | 4 | 44 | G3/G5/G7/G8 |
| marginals | 5 | 3 | 0 | 1 | 3 | 2 | 1 | 2 | 2 | 2 | 4 | 4 | 3 | 4 | 36 | G3/G5/G7 |

Scores are diagnostic and do not compensate for a fatal gate.

## 21. Publication feasibility

A benchmark/provenance paper around assay-disjoint protein-complex evaluation
could become credible if new curation demonstrates independence. A negative
projection or dynamics audit could support a workshop/position paper. Neither
is currently a new structure-learning project: the first is benchmark
engineering and the second lacks structural truth. No S3.1 topic should be
opened from the present evidence.

## 22. Strongest evidence FOR

Natural partial observation is real in dynamics, proteomics, pooled assays,
censored sensing and privacy releases. Complexes and coupling scopes are
scientifically meaningful order-three-or-higher objects. Public data permit a
first computational audit, and projection/system-identification theory offers
clear sample-complexity interfaces.

## 23. Strongest evidence AGAINST

The favorable properties do not coincide. Projection has exact labels only
after author-generated information loss; dynamics has natural observations but
no independent real coupling truth; censoring and marginals are non-identifiable
under realistic unknown mechanisms; pooled screens estimate effects; and
complex recovery is already a mature graph/latent-model task with incomplete,
potentially circular positives. There is no candidate with two real routes and
a residual beyond classical and recent methods.

## 24. Hard-gate table

| gate | status | evidence |
|---|---|---|
| G1 order >=3 | PASS | dynamics terms, complexes and group events include order >=3 |
| G2 natural partiality | PASS | several families have genuine assay/sensing/response mechanisms |
| G3 independent real structural validation | FAIL | no qualifying complete or clean A/B route survives |
| G4 second real route | FAIL | no candidate has two routes for the same estimand |
| G5 meaningful identifiability | FAIL | realistic projection, censoring, marginals and complex maps are non-injective; dynamics is conditional |
| G6 plausible assumptions | FAIL | excitation/state sufficiency/separability/detection assumptions are not established |
| G7 residual beyond ordinary methods | FAIL | graph clustering, tensors, sparse regression and log-linear models cover the meaningful tasks |
| G8 recent ML unsaturated | FAIL | direct projection, dynamics and complex methods are active and close |
| G9 structural evaluation | FAIL | strongest real routes often score response, enrichment or incomplete positives |
| G10 feasible first project | PASS | public projection, EEG, CF-MS/CORUM and hu.MAP resources permit an audit without new wet lab work |
| G11 learning/inference residual | FAIL | remaining credible work is mainly benchmark provenance/sensing, not an isolated learner |

Project-level PASS means at least one family establishes that property; it does
not rescue any candidate. No single row passes G1--G11.

## 25. Final decision

**S3.0-E — NO-GO: CLASSICAL / LATENT-MODEL SATURATION.**

This is not S3.0-C because several observation mechanisms are genuinely natural.
It is not solely S3.0-D because conditional identifiability theory exists for
projection, dynamics and pooling. It is not solely S3.0-F because no one recent
paper defines the entire viable problem. The narrowest apparently real route—
indirect assay to protein complexes—is already covered by classical overlapping
graph/latent methods, while the other families fail gold or identifiability.

## 26. Exact next action

Freeze S3.0 at this decision. Do not create
`docs/S3_CONCRETE_SUBFIELD_PROPOSAL.md`, do not train a model, and do not
automatically expand to another structure-learning family. Return to project
review. Reopen only when new external evidence supplies two real validation
routes, including one independent A/B structural gold, and demonstrates a
specific residual beyond the listed graph, matrix, tensor, classical inverse
and current ML methods.
