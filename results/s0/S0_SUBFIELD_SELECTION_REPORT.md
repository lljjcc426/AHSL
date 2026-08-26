# S0 subfield selection report

## Executive decision

**S0-A — GO.** Recommend exactly one subfield for S1:

> **Sparse high-order combinatorial interaction structure learning from intervention–response data.**

This is a subfield choice, not a model proposal. Its canonical object is the support, sign, and magnitude of irreducible order≥3 effects among jointly applied interventions. The main evidence comes from real yeast triple-mutant screens, complete microbial community combinations, and full-factorial antibiotic combinations. The result is positive but conditional on an S1 identifiability/split audit; a Dango-like HGNN paper is explicitly excluded.

## Finalist dossiers

### Rank 1 — sparse high-order combinatorial interaction structure learning

- Canonical problem: measured intervention subsets and contexts → order≥3 non-additive support hypergraph with effects/uncertainty.
- Typical structures: signed weighted hyperedges, sparse set-function supports, optionally context-indexed shared supports.
- Classical/modern baselines: factorial/Möbius contrasts, hierarchical and non-hereditary sparse regression, compressed sensing; Dango, sparse Möbius recovery, MoCHI, and NAIAD-adjacent active learning.
- Why not solved: direct data are sparse and heterogeneous; pure high-order effects can violate heredity; accepted entity/order-disjoint and uncertainty protocols are absent across domains.
- Main failure mode: the recovered “interaction” changes with scale/null or vanishes against simple classical estimators.
- First-paper type: benchmark/estimand plus simple structure learner and one identifiability or error-control result.
- Program path: recovery → uncertainty/active design → transfer/partial observation.
- Entire-subfield kill condition for this project: no two usable real order≥3 routes or no residual beyond contrast/sparse baselines on leakage-resistant splits.

### Rank 2 — open-world temporal/directed group-event structure forecasting

- Canonical problem: event history → next set-valued relation, cardinality, direction/roles, and time.
- Typical structures: timestamped undirected/bipartite/directed hyperedges under node churn.
- Classical/modern baselines: closure/resource allocation, marked point processes, combinatorial search; HGDHE, CAt-Walk, FastHeP, directed HyperTPP, and HyperSearch.
- Why not solved: sampled-negative classification does not measure full retrieval; temporal unconstrained search, calibration, and unseen-group generalization are not jointly settled.
- Main failure mode: apparent gains come from repeated-set memorization or easy negatives.
- First-paper type: evaluation/search formulation plus strong simple baselines and a calibrated set/search property.
- Program path: benchmark → calibrated generative/search models → open-node and partial-observation extensions.
- Entire-subfield kill condition for this project: full-space or justified search-controlled evaluation makes simple recurrence/closure baselines dominant, or novelty reduces to another encoder.

## A–AL exact deliverable

### A. Branch and final SHA

Branch: `project-s0-high-order-structure-learning-landscape`.

Frozen start: `4f45a6bbf6c594b217f18b87ea7ede0900d24ebb`.

Final SHA: reported in the Git/GitHub handoff accompanying this report. A commit cannot contain its own final hash without changing that hash.

### B. Search date

2026-08-27 (Asia/Shanghai).

### C. Total screened

92 unique papers/resources: 84 primary method/empirical works and 8 survey, benchmark, protocol, or data resources.

### D. Substantively reviewed works

34.

### E. Substantive recent works

17 works from 2024–2026.

### F. Number of subfields screened

11.

### G. Candidate subfields screened

1. probabilistic factor-scope structure learning;
2. tractability-constrained structure learning;
3. static open-set hyperedge prediction;
4. open-world temporal/directed group-event structure forecasting;
5. hypergraph reconstruction from pairwise projections;
6. dynamics-to-hypergraph reconstruction;
7. latent high-order mesostructure discovery;
8. protein-complex set discovery;
9. sparse high-order combinatorial interaction structure learning;
10. high-order causal mechanism structure learning;
11. n-ary relational/event structure extraction and completion.

### H. Killed subfields and exact hard-gate reasons

| Subfield | Failed gates | Exact reason |
|---|---|---|
| factor scopes | G4,G5,G6,G7 | real higher-order scope truth and graph insufficiency are weak; classical PGM and circuit alternatives are mature |
| tractability constrained | G1,G4,G5,G6 | learned object is commonly a graph/treewidth-restricted DAG; high-order structure and residual are not established |
| static hyperedge prediction | G3,G6,G7 | literature is dense and frequently evaluates sampled-negative classification rather than actual discovery |
| projected reconstruction | G7,G8 | real hypergraphs are artificially projected/hidden to create labels; identifiability comes from priors |
| dynamics reconstruction | G2,G7,G8 | real trajectories lack accepted hyperedge truth; primary recovery evidence is synthetic |
| latent mesostructure | G4,G7 | pairwise block/community alternatives often suffice; external group truth is weak |
| protein complexes | G5,G7 | strong classical methods plus incomplete, overlapping, often reused gold standards obscure residual |
| causal mechanisms | G2,G7,G8 | explicit hyper-DAG work is new but structural validation is synthetic/indirect |
| n-ary relation/event | G3,G6 | fixed-field candidate completion/extraction is crowded and often reducible by reification |

### I. Semifinal subfields

Five: factor-scope learning; temporal/directed group events; dynamics-to-hypergraph reconstruction; protein-complex discovery; combinatorial interaction support learning.

### J. Final subfields

Two genuine finalists:

1. sparse high-order combinatorial interaction structure learning from intervention–response data;
2. open-world temporal/directed group-event structure forecasting.

### K. Score /75 for each finalist

Rank 1: 67/75. Rank 2: 60/75. Full 15-axis vectors are in `docs/S0_SUBFIELD_MATRIX.md`.

### L. Unknown structural object

- Rank 1: hyperedges `S`, `|S|≥3`, whose non-additive effect `beta_S` is nonzero, plus sign/magnitude/uncertainty.
- Rank 2: next/future event hyperedge membership, cardinality, time, and optionally left/right roles or direction.

### M. Real benchmark families

- Rank 1: Kuzmin/Boone yeast τ-SGA triple-mutant screen; complete microbial community landscapes; full-factorial antibiotic combinations. MoCHI/DMS and HODDI are secondary routes with caveats.
- Rank 2: temporal email/thread/contact sets; coauthorship/tag/bill groups; directed email/reaction/transaction hyperedges.

### N. Strongest classical baseline family

- Rank 1: fixed-scale factorial/Möbius contrasts plus sparse/hierarchical regression or compressed sensing; domain null models are mandatory.
- Rank 2: closure/resource-allocation and marked point processes coupled to explicit combinatorial search; HyperSearch is the strongest search-based threat.

### O. Strongest recent ML threat

- Rank 1: Dango (2026), with NAIAD (2025) adjacent on active pair discovery and sparse Möbius recovery (2024) as the theory threat.
- Rank 2: the 2025 directed HyperTPP, FastHeP, CAt-Walk, and HyperSearch jointly cover most obvious components.

### P. Why pairwise structure is insufficient

- Rank 1: >30% of measured trigenic interactions were not anticipated from doubles; hidden drug suppression requires lower-order subset comparisons; microbial coefficients reorganize with community order.
- Rank 2: two different groups can have the same clique projection; projection loses simultaneous group identity, cardinality, roles, and direction.

### Q. Evaluation target

- Rank 1: support/effect recovery on directly measured panels, response prediction for unseen combinations, and prospective top-combination discovery under entity/order-disjoint splits.
- Rank 2: full or search-controlled next-set retrieval, cardinality/direction correctness, time likelihood/error, calibration, and unseen-group/entity generalization.

### R. Theory interface

- Rank 1: Möbius/ANOVA identifiability, sparse recovery, heredity versus pure interactions, active design, selective error control, transfer invariance.
- Rank 2: marked/set-valued point processes, exchangeability, projective consistency, calibrated set prediction, and safe search bounds.

### S. Tractability relevance

For Rank 1, sparsity, maximum order, and experimental design are functional; GHW/FHW/acyclicity are decorative. For Rank 2, exponential set search and pruning are functional; decomposition width is decorative.

### T. Strongest evidence for each finalist

- Rank 1: multiple real experimental domains contain measured order≥3 effects and direct demonstrations that pairwise summaries miss them.
- Rank 2: many public time-stamped group-event datasets directly reveal the future set and support reproducible temporal splits.

### U. Strongest evidence against each finalist

- Rank 1: the interaction target depends on scale/null; order≥3 large datasets are scarce; Dango directly occupies yeast triple prediction.
- Rank 2: sampled-negative protocols can reverse method rankings; the exact space is crowded and group repetition may make the task retrieval rather than discovery.

### V. First-paper difficulty

- Rank 1: medium overall; low–medium compute, medium data engineering, medium–high theory/evaluation.
- Rank 2: medium–high overall; medium compute, medium–high data engineering, high evaluation risk.

### W. Long-term research depth

- Rank 1: basic support recovery → uncertainty/active design → cross-condition/order/domain transfer.
- Rank 2: open-world benchmark → calibrated directed set process/search → node churn/partial observation/domain semantics.

### X. Publication fit

Rank 1 has strong ML/statistics/computational-biology potential if the work changes structure validity or acquisition, plausible specialist bioinformatics routes, and weak fit for an architecture-only paper. Rank 2 fits KDD/WWW/TMLR and general ML only if it fixes evaluation or adds principled generative/search theory.

### Y. Rank 1 subfield

Sparse high-order combinatorial interaction structure learning from intervention–response data.

### Z. Exact canonical problem statement for Rank 1

Given a sparse, noisy set of experimentally measured responses `D={(A_i,y_i,c_i)}` for jointly applied intervention subsets `A_i⊆N` under contexts `c_i`, and a predeclared response scale/null composition rule, infer the order≥3 support hypergraph `H*={S: beta_S≠0}`, estimate signed effects and uncertainty, and generalize to unseen combinations/contexts without treating unmeasured sets as negatives.

### AA. Five closest prior works for Rank 1

Kuzmin et al. (Science 2018); Zhang et al./Dango (Cell Systems 2026); Arya et al. (PNAS 2023); Ishizawa et al. (PNAS 2024); Lozano-Huntelman et al. (iScience 2021).

### AB. Two strongest real benchmark routes

1. Public yeast τ-SGA triple-mutant measurements (Science/Dryad/Dango repository).
2. Complete experimental microbial and antibiotic factorial landscapes; the seven-strain 127-combination study is the cleanest small complete route.

### AC. Biggest scientific uncertainty

Whether a stable, biologically meaningful order≥3 support exists across response scales, conditions, and assay batches, rather than being a contrast-specific artifact.

### AD. Biggest novelty risk

Dango plus sparse Möbius/compressive-sensing work may cover the obvious method space. S1 must not reduce to a new encoder or regularizer.

### AE. Biggest evaluation risk

Entity overlap and unmeasured-as-negative conventions can make interpolation look like discovery. Direct panels and entity/order-disjoint evaluation are mandatory.

### AF. Whether AHSL negative evidence transfers

Only partially. AHSL showed that a mathematically valid structural restriction may have negligible statistical value. Rank 1 has stronger real labels and pairwise-insufficiency evidence, but any new hypergraph prior must still beat unrestricted and classical sparse baselines. No AHSL estimator or join-tree premise transfers.

### AG. Whether the CertPath representability failure is a major analogous risk

Yes, at the target-definition level. A measured response does not identify a unique “interaction” until the response scale, null composition rule, and required lower-order measurements are fixed. S1 must run an interaction-estimand representability/identifiability gate before learning. The specific positive-cost hyperpath failure does not transfer.

### AH. Exact S1 search boundary

Search only problems that infer order≥3 non-additive support/effects from public real combinatorial intervention–response data, with direct lower-order measurements, defensible entity/order/context splits, a strong classical contrast/sparse baseline, and a plausible theory or uncertainty interface. Search a concrete problem, dataset pair, formulation, and kill-test—not an architecture.

### AI. Topics explicitly prohibited in S1

- Dango replication or generic HGNN architecture search;
- pairwise-only genetic/drug synergy as the primary task;
- HODDI sampled-negative classification as causal interaction discovery;
- post-hoc explanation of a black-box predictor without external structural evaluation;
- synthetic labels as main evidence;
- generic CTR/feature-cross interaction mining;
- temporal hyperedge prediction (belongs to Rank 2, not selected);
- any AHSL join-tree/incidence line or CertPath reaction-cost/hyperpath repair;
- decorative GHW/FHW/acyclicity theory.

### AJ. Exact final decision

**S0-A**.

### AK. Whether any ML model was trained

**NO.**

### AL. Exact recommended next action

After review, start S1 with a benchmark-and-estimand audit of the yeast τ-SGA and complete microbial/antibiotic factorial routes. Freeze one interaction definition and two leakage-resistant split families, then test—analytically and by data feasibility only—whether a concrete residual remains beyond Möbius contrasts, hierarchical/non-hereditary sparse estimators, Dango, and compressed-sensing baselines. Do not implement or train a model before that gate passes.
