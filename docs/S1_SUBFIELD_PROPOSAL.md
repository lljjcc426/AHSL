# S1 subfield proposal

## Chosen subfield

**Sparse high-order combinatorial interaction structure learning from intervention–response data.**

This is a search boundary for S1, not a paper or model proposal.

## Canonical scientific question

Given incomplete real measurements of phenotypes under subsets of jointly applied perturbations, which order≥3 subsets have irreducible non-additive effects, with what sign/strength/uncertainty, and which unmeasured combinations should be tested next?

The structural output is a support hypergraph of nonzero interaction contrasts. The effect scale and null composition model are part of the estimand and must be declared before learning.

## Why this subfield

- Real triple-mutant, microbial-community, and multi-drug factorial data exist.
- Published experiments directly show effects missed by pairwise summaries.
- The exponential combination space creates a genuine learning/design problem when full factorial measurement is impossible.
- Statistics, sparse set-function learning, and domain science provide strong baselines and theory interfaces.
- The work can accumulate across support recovery, uncertainty, active design, and transfer without returning to AHSL or CertPath.

## Dominant literature families

1. factorial design, ANOVA/Möbius/Walsh–Hadamard interaction contrasts;
2. hierarchical and non-hereditary sparse interaction selection;
3. compressed sensing and sparse set-function/Fourier recovery;
4. epistasis and τ-SGA quantitative genetic interaction mapping;
5. combinatorial CRISPR and active experiment selection;
6. microbial community landscape learning;
7. higher-order drug-combination null models and factorial assays;
8. neural interaction prediction/extraction, especially Dango and MoCHI.

## Benchmark families

- Primary route A: Kuzmin/Boone yeast τ-SGA triple-mutant data, public via Dryad and the Dango repository.
- Primary route B: experimental microbial combination landscapes, especially the complete seven-strain 127-subset panel and the four real datasets used in the sparse-landscape work.
- Primary route C: full-factorial 3–5 antibiotic combinations with all lower-order subsets.
- Secondary only: deep mutational scanning; HODDI/FAERS (noncausal and negative-construction caveats).

## Unresolved gaps

- estimand stability across response scales and null models;
- support recovery under sparse, nonuniform combination designs;
- pure high-order effects that violate heredity;
- entity/order/context-disjoint evaluation;
- calibrated support/effect uncertainty rather than response intervals alone;
- active selection aimed at structural discovery, not only best-response optimization;
- cross-condition and cross-domain transfer of supports versus effects;
- benchmark protocols that do not label unmeasured combinations as negatives.

## Strongest threats

Strongest classical threat: complete/fractional factorial contrasts plus sparse hierarchical or non-hereditary regression/compressed sensing.

Strongest modern ML threat: Dango for yeast triples. NAIAD is the strongest active-learning adjacency, although its released task is pairwise. Sparse Möbius recovery is the strongest theory collision.

## Possible theory interfaces

- identifiability under incomplete factorial designs;
- support-recovery/sample-complexity bounds using sparsity and maximum order;
- conditions under which heredity is safe or necessarily misses pure interactions;
- uncertainty/FDR for selected hyperedges;
- adaptive design regret or discovery guarantees;
- partial pooling/invariance for shared supports and context-varying effects.

GHW, FHW, join trees, and acyclicity are not current interfaces.

## Concrete problem types for S1 to inspect

1. estimand-robust support recovery across scientifically valid effect scales;
2. non-hereditary sparse recovery of pure order≥3 effects;
3. entity-disjoint and order-extrapolation benchmark design;
4. calibrated hyperedge-support uncertainty and false-discovery control;
5. active measurement for support discovery under experiment budgets;
6. shared-support/context-varying-effect transfer;
7. cross-domain evaluation of simple set-function learners;
8. prospective top-combination selection with abstention under sparse evidence.

## Topics not to pursue

- a Dango clone, generic HGNN, or attention architecture;
- pairwise-only CRISPR/drug synergy;
- post-hoc neural feature interaction explanations without experimental support truth;
- synthetic XOR/SCM labels as main evidence;
- HODDI co-report classification interpreted as causal synergy;
- random tuple splits as primary evidence;
- generic feature-cross/CTR recommendation;
- temporal hyperedge forecasting in this S1;
- AHSL/CertPath revival;
- decorative hypergraph-width theory.

## S1 hard gates

1. At least two real public benchmark families are usable under compatible structural definitions.
2. At least one primary dataset has direct order≥3 measurements and the lower-order subsets needed by the declared contrast.
3. The target support/effect is identifiable or its equivalence class is explicit.
4. Entity/order/context-disjoint splits remain large enough for meaningful evaluation.
5. A classical factorial/sparse baseline leaves a plausible residual.
6. The concrete gap is not already Dango, sparse Möbius recovery, or an existing domain method.
7. Evaluation includes direct support/effect or prospective discovery value, not only response RMSE.
8. The first project fits normal academic compute and does not require new wet-lab experiments for its main evidence.

If any of gates 1–5 fails, stop the concrete S1 topic before model implementation.
