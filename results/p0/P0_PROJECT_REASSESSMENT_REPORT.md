# Project P0 reassessment report

Reassessment date: **2026-08-27 (Asia/Shanghai)**
Frozen base: `6f2147a1fb3861105fdd0009f064cc6b78d7ad4c`
Branch: `project-p0-hypergraph-ml-interface-reassessment`

## 1. Executive decision

**P0-B — PIVOT TO HYPERGRAPH ALGORITHMS/THEORY; ML AUXILIARY OR OPTIONAL.**

No mapped interface satisfies both ML necessity and native hypergraph-theory
necessity. This is not evidence that the combination is impossible. It is
evidence that the present project should no longer fund it as the primary line
without new external support.

The strongest positive program is theory-centered:

> Certified reusable hypertree decompositions for evolving query and constraint
> hypergraphs: canonical/rerootable witnesses, update-sensitive maintenance and
> independently verified downstream structure.

This choice is narrower than P0-C because strong, current and benchmark-linked
hypergraph algorithmic questions remain. It is not P0-A because their core
progress does not require ML.

## 2. Scope of reassessment

P0 synthesized 13 frozen phases, mapped 13 interfaces and conducted only four
question-driven searches covering 15 primary works, 12 deeply. It did not train
a model, launch a benchmark campaign, rerun expensive experiments or reinterpret
historical decisions without evidence.

Strong coupling was tested against graph theory, sparse regression, tensor/set
methods, generic solver features and exact/statistical algorithms. A native
hypergraph representation without a necessary theorem or complexity role was
not counted as strong coupling.

## 3. Project history

The project progressed through four conceptually different routes:

1. A0--B0: alpha-acyclic connected-subtree denoising and latent join-tree
   estimation;
2. N0--N1.0: learned reaction costs with exact directed-hyperpath decoding;
3. S0--S3.0: real high-order structure learning, temporal prediction and
   partial-observation recovery;
4. R0: learning to exploit known factor hypergraphs while preserving exactness.

The complete 13-row master matrix is in
`docs/P0_PROJECT_HISTORY_MAP.md`.

## 4. Phase-by-phase evidence

| Phase | Strongest positive evidence | Strongest negative evidence | Frozen outcome |
|---|---|---|---|
| A0 | exact connectedness can denoise | learned estimator lost to exact projection/MAP | modify; abandon neural A0 estimator |
| A0.5 | exact linear-time tree DP; connectedness gain | synthetic and topology-dependent | proceed to bounded tree gate |
| A0.75 | classical residual 0.01714 in three non-star families | modest absolute scale; synthetic | prepare learned-A1 proposal |
| A1 | tree identity has held-out value; population identifiability | likelihood gain did not improve Hamming; no real covariates | pause neural tree learning |
| A1.5 | decoder gain positive for all frozen tree sources | tree gain failed primary rule | stop tree identity; retain posterior modeling |
| B0 | exact infrastructure and one grid conditional hold | no public task jointly fits scaffold, output, covariates and loss | close AHSL ML line |
| N0 | real directed-hyperpath proposal and certificate | supervision still unaudited | CertPath bounded GO |
| N1.0 | 712 qualified tasks, exact attainability theorem | only 59.32% natural attainability; 456 infeasible without repair | close CertPath |
| S0 | two real-data finalists | conditional on direct truth and protocol | choose interaction-support audit |
| S1.0 | identifiable residual on one microbial panel | no second direct domain; estimand/prior-art problems | NO-GO |
| S2.0 | two real domains; sampled evaluation clearly misleading | HyperSearch direct collision; local candidate recall <1% | NO-GO |
| S3.0 | natural observation mechanisms exist | gold, identifiability and residual never coincide | NO-GO |
| R0 | exactness clean; high-order factors and large arbitrary-strategy variance | competent gap <3x; generic solver/DB/tensor collision | NO-GO |

## 5. Failure taxonomy

No parent line stopped primarily for engineering failure F1. Controlling causes
span benchmark failure F2, identifiability/representability F3, classical
saturation F4, prior-art saturation F5, hypergraph-necessity failure F6,
ML-necessity failure F7, amortization F8 and hypothesis failure F9.

The main recurring pattern is a **necessity mismatch**: either native structure
is mathematically meaningful but exact/classical algorithms absorb the benefit,
or ML prediction is meaningful but graph/sparse/tensor/generic formulations
preserve the actual target.

## 6. Independence/correlation of failures

| Evidence group | Correlation | Reason |
|---|---|---|
| AHSL/B0 and parts of S1/S3 benchmark scarcity | partially correlated | several routes lack a matching real structural task |
| S1 and S3 identifiability | partially correlated | both concern latent truth, but observation mechanisms and domains differ |
| S2 protocol/prior-art collision | largely independent | has strong real labels and fails for search protocol/novelty |
| R0 classical/genericity/amortization | largely independent | structure is known and exact truth is available |
| N1.0 representability | largely independent of S2/R0 | curated labels exist but are excluded by the exact objective class |

The strongest independent negative evidence is the combination of S3's
identifiability/reduction result and R0's known-structure solver-learning result:
they fail on opposite sides of the unknown/known-structure boundary.

## 7. Transferability of negative evidence

AHSL transfers strongly to exact-projectable structural priors; N1.0 transfers
to constrained decoding with curated labels; S1/S3 transfer strongly to latent
interactions, partial recovery and causal structure; S2 transfers near-directly
to open temporal event prediction; R0 transfers near-fatally to learned
decomposition, portfolio, cost and certified-fallback formulations.

Transfer is a burden-of-proof update, not a universal theorem. The full matrix
is `docs/P0_TRANSFERABILITY_MATRIX.md`.

## 8. Hypergraph × ML interface inventory

Thirteen interfaces were mapped. I1--I6 and I8/I10/I12 are already effectively
covered; I7 and I9 are untested but strongly threatened; I11 and I13 are
positively motivated only as theory/algorithms interfaces.

No evidence-neutral untested interface remains. “Not implemented” therefore
does not support continuation.

## 9. Q1-Q4 quadrant map

| Quadrant | Count | Interfaces |
|---|---:|---|
| Q1: both necessary | 0 | none |
| Q2: hypergraph theory necessary, ML not | 2 | adaptive/query algorithms; canonical/reusable/dynamic decompositions |
| Q3: ML potentially necessary, native hypergraph theory not | 10 | structure, interactions, events, partial recovery, solver/cost/certified learning, generalization, fixed HGNN and causal mechanisms |
| Q4: neither strongly necessary | 1 | generic hypergraph regularization/inductive bias |

Only Q1 could authorize P0-A; it is empty.

## 10. Strong-coupling definition

Strong coupling requires:

1. ML changes a measurable scientific or algorithmic objective beyond the best
   exact/classical/statistical alternative; and
2. removing a native hypergraph concept changes the target, guarantee or
   complexity.

Using an HGNN, calling a set a hyperedge, or adding GHW features is weak coupling
unless these necessity claims are demonstrated.

## 11. ML-necessity audit

- AHSL: exact projection and posterior decisions captured the positive value.
- CertPath: the supervised task failed before cost learning became necessary.
- S1/S3: sparse recovery, system identification and latent models preserve the
  meaningful tasks.
- S2: ML may score future sets, but the correct task is already occupied and
  no native theory is required.
- R0: no material, predictable and amortizable classical residual was found.
- I11/I13: current progress is produced by exact/randomized algorithms and
  combinatorial theory.

ML necessity therefore fails for every native-theory survivor.

## 12. Hypergraph-theory-necessity audit

Native theory clearly matters for alpha-acyclic DP, directed hyperpaths,
GHD/FHD, fractional covers and hypertree query models. Yet those same routes
failed ML necessity or benchmark fit. The strongest ML tasks—interaction
support, temporal events, fixed-hypergraph prediction and causal mechanism
learning—remain essentially sparse polynomial, set prediction, graph/set
representation or system-identification problems after removing width and
acyclicity theory.

## 13. Real benchmark audit

The repository contains strong individual routes: Reactome, yeast/microbial/drug
panels, Ubuntu/Congress, proteomics/EEG, UAI/XCSP and HyperBench. The problem is
not that no real data exist. The problem is that no Q1 candidate has all of:
accepted primary data, a second route, direct truth, meaningful target and a
measured classical residual.

HyperBench is sufficient for a structural theory program, because a verified
decomposition is itself the target. It is insufficient for R0 strategy
learning, because it lacks factor tables and repeated downstream workloads.

## 14. Identifiability audit

| Target family | Status |
|---|---|
| known-tree synthetic subtree | exactly/conditionally identifiable under declared model |
| latent join tree | population-identifiable away from degeneracies; finite-sample weak |
| CertPath natural labels | directly observed but often unattainable in the objective class |
| microbial Möbius support | identifiable with complete lower subsets; masked retrospective route only |
| temporal observed future set | directly evaluable for observed events |
| projection/censoring/marginals/complexes | generally partial or non-identifiable under realistic mechanisms |
| decomposition certificate | directly verifiable; optimum may be computationally hard |

A learned prior is never counted as restoring identifiability.

## 15. Classical-residual audit

The strongest measured residuals were A0.75's synthetic tree gap and S1.0's
single small microbial panel. Neither has the real, replicated strong-coupling
support required for a parent program. R0's fair classical exact runtime ratios
were 1.28--2.23x, below its 3x two-family threshold. S2 could not isolate a
scorer residual because candidate recall was below 1%.

No surviving Q1 candidate has a material, reproducible, architecture-independent
classical residual.

## 16. Prior-art residual audit

- Closest classical threat: exact projection/DP, sparse recovery, latent models,
  HyperSearch, GHD/FHD exact and approximation algorithms.
- Closest ML threat: Dango, temporal hyperedge methods, generic algorithm
  selection and HGNN generalization work.
- Closest adjacent analogues: graph learning, database join optimization,
  tensor contraction and system identification.

For no Q1 candidate can `EXACT REMAINING CONTRIBUTION` be stated without a
hypothetical dataset, predictor or residual. Architecture substitution is not a
contribution.

## 17. Reopening-condition status

Zero frozen reopening conditions are satisfied. Recent projection, query and
decomposition theorems do not supply the missing real labels, two-family
residuals or amortized strategy benchmarks. Details are in
`docs/P0_REOPENING_CONDITIONS.md`.

## 18. Remaining-interface audit

Four narrow candidates were tested conceptually:

1. width-aware generalization: Q3; native width necessity unproved;
2. learning-augmented parameterized algorithms: Q3 as ML, Q2 after removing ML;
3. adaptive/query algorithms: Q2; algorithms and information theory suffice;
4. certified prediction-selected approximation: effectively R0 portfolio
   learning and therefore covered.

No candidate passes all P0-A gates.

## 19. Theory-only pivot audit

The selected Q2 program is **certified reusable hypertree decompositions for
evolving query and constraint hypergraphs**. It has:

- native HD/GHD/FHD and cover objects;
- independently checkable certificates;
- public HyperBench/CQ/CSP routes;
- active exact, approximation, parameterized, incremental and rerootability
  literature;
- a coherent representation → update → downstream sequence.

Recent fractional-width approximation and exact FPT work confirms that the
mathematical area is active, while rerootability exposes unresolved practical
structure. See [efficient FHW approximation](https://arxiv.org/abs/2409.20172),
[FPT GHW/FHW](https://arxiv.org/abs/2507.11080) and
[rerootable decompositions](https://arxiv.org/abs/2608.17853).

## 20. Positive asset inventory

Theory assets include alpha-acyclicity, exact DP, GHD/FHD and certificate
knowledge. Code assets include connected-subtree DP, posterior decoding, UAI
parsing and exact VE. Benchmark assets include versioned result tables and
source ledgers. The strongest cross-project asset is methodological: separate
benchmark, identifiability, classical residual, prior-art and necessity gates.

## 21. Publication-value audit

No negative result should be forced into publication. The strongest conditional
candidate is an S2 protocol/reproducibility study because sampled Recall@10 of
75--95% coexists with zero local open novel-set Recall@10 on two datasets. It
still requires matched HyperSearch preprocessing and search before a clean
claim. CertPath and S3 may support workshop/position notes; current AHSL and R0
evidence is too synthetic or bounded for a standalone negative paper.

## 22. Research-program coherence

Continuing the strong-coupling parent line would require entering a different
community for each candidate: learning theory for bounds, algorithms with
predictions for guarantees, active acquisition for queries, databases for
decompositions, or domain science for mechanisms. Benchmarks and evaluation
norms would not be shared.

The P0-B program is more coherent: database theory, CSP and parameterized
algorithms share decomposition language, HyperBench-like structures,
certificates and algorithmic evaluation.

## 23. Research-management lessons

The most important lesson is to establish target, real truth and classical
residual before choosing a model. Topic-selection GO decisions should authorize
one bounded kill-test only. Structural validity and ML value must be tested
separately. Oracle-label economics must precede strategy training. A failure
should not be rescued through more complexity.

The A0.75--A1.5 sequence ran longer than later gates, but it was not irrational:
it resolved a preregistered residual, identifiability and decoder alignment.
B0 then stopped promptly when no real task existed.

## 24. Consistency/reproducibility audit

No frozen historical conclusion required correction. Apparent A1 ambiguity is
resolved by distinguishing its neural-small-residual kill rule from the separate
continuation rule: the former did not fire, but the latter failed. All 13 phase
branches exist remotely. External N1.0/S2.0/R0 data are ignored by Git. The
repository has no GitHub Actions workflow; tests reported by phases are local.

## 25. Strongest evidence FOR continuing current parent line

- Native hypergraph structure sometimes has measurable algorithmic/statistical
  value: exact connectedness denoising, directed-hyperpath certificates and
  sparse multiway inference are not vacuous.
- Real high-order data and public structural benchmarks exist.
- Current decomposition and query theory is active and deep.
- Exactness can often be made independent of learned advice.

This supports retaining expertise and a theory program, not the current
strong-coupling investment thesis.

## 26. Strongest evidence AGAINST continuing current parent line

Across unknown structure, partial observation, future events and known-structure
execution, no interface combines direct real truth, two routes, identifiability,
classical residual, prior-art residual and both necessity tests. The failures
are not all caused by one biology dataset or one model. S2 and R0 provide
largely independent negative evidence after real labels or exact truth are
available.

Further continuation would mostly reframe tested tasks as another GNN, another
width feature, another solver policy or another latent prior.

## 27. Hard-gate table

The closest attempted P0-A candidate is robust learning-augmented GHD/FHD
search. One failure is sufficient.

| Gate | Status | Evidence |
|---|---|---|
| G1 ML necessary | FAIL | no material learned residual or predictability |
| G2 native hypergraph theory necessary | PASS | decomposition validity/width are native |
| G3 accepted real benchmark | PASS | HyperBench/CQ/CSP structures |
| G4 second validation route | FAIL | no second paired prediction/execution route |
| G5 identifiable/direct target | PASS, narrow | certificate validity is direct; optimal oracle is costly |
| G6 material classical residual | FAIL | R0 thresholds fail; downstream decomposition residual unmeasured |
| G7 recent prior art residual | FAIL | exact, LP, approximation and FPT methods are active |
| G8 not generic learning | FAIL | advice/ranking remains generic algorithm selection |
| G9 feasible first project | PASS as theory only | bounded theorem/verifier work is feasible |
| G10 2--3 project depth | PASS as theory only | canonicalization, updates and downstream structure form a sequence |
| G11 old negative evidence does not transfer | FAIL | R0 transfers strongly |
| G12 no artificial reopening | PASS | theory program does not reopen R0 |

No Q1 candidate passes G1--G12.

## 28. Final decision

**P0-B — PIVOT TO HYPERGRAPH ALGORITHMS/THEORY; ML AUXILIARY OR OPTIONAL.**

The qualitative posterior on “the current project has a robust primary
strong-coupling hypergraph-theory × ML opportunity” decreases after each of the
largely independent S1/S2/S3/R0 gates. Confidence in “hypergraph algorithms and
structural theory remain scientifically valuable” increases after A0.5, R0 and
the current decomposition/query literature check.

| Evidence | Parent strong-coupling belief | Theory-program belief |
|---|---|---|
| exact connectedness gain | slight increase | increase |
| classical projection/tree saturation | decrease | increase |
| B0 real-task failure | decrease | unchanged |
| CertPath representability failure | decrease | slight increase in certificate methodology |
| S1 one-domain-only residual | decrease | unchanged |
| S2 direct prior-art collision | decrease | unchanged |
| S3 identifiability/reduction | strong decrease | unchanged |
| R0 known-structure/genericity result | strong decrease | increase |
| 2024--2026 decomposition/query advances | no rescue | strong increase |

This is a qualitative evidence update, not a numeric probability or an
impossibility claim.

## 29. Exact next action

Start no new ML phase. Review `docs/P1_THEORY_PROGRAM_PROPOSAL.md`, then prepare
one P1.1 definition-and-prior-art note around exactly one of canonical
representation, rerootability-width trade-off or update recourse. State one
theorem target and one falsifying construction, reconcile them with the five
strongest recent decomposition works, and prove/refute on minimal instances
before performance implementation.

No model was trained in P0.
