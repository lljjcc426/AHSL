# S1.0 gate report

Search/analysis date: **2026-08-27 (Asia/Shanghai)**
Frozen base: `283dfbfa88c9e5e1c2ac3cbcf571859523c41d07`
Branch: `project-s1.0-estimand-benchmark-classical-gate`

## 1. Executive decision

**Decision S1.0-C — NO-GO: ESTIMAND / IDENTIFIABILITY.** A defensible coefficient exists in each domain, and the microbial scale-stability gate narrowly passes. The general S1 claim nevertheless stops because only one real family—the seven-strain complete microbial panel—supports clean direct recovery evaluation from partially masked real responses. Yeast unmeasured triples have no direct tau truth without new experiments; drug-set support is strongly dose-dependent. The residual cannot be validated across two real domains.

No new ML model was trained.

## 2. Search methodology

The search screened 42 directly relevant works, deeply inspected 18, and deeply inspected 7 dated 2024--2026. Publisher/proceedings pages, PubMed/PMC, official repositories, data archives, and source code were preferred. Queries and the itemized ledger are in `docs/S1_0_SEARCH_LOG.md`; bibliography is `references/s1_0_references.bib`.

## 3. S0 hypothesis under audit

The audited hypothesis was sparse order>=3 non-additive support discovery from incomplete/noisy intervention-response data—not response prediction, generic hyperedge prediction, or architecture search. A cross-domain method was allowed to use domain-specific contrasts, but needed the same structural problem class in at least two domains.

## 4. Interaction estimand taxonomy

Selected domain estimands are: adjusted tau-SGA for yeast; replicate-aware log10-CFU Möbius coefficients for microbiome; dose-specific DA and emergent `E_k` contrasts for drugs. Raw epsilon/raw CFU and standard drug nulls are sensitivity alternatives. None is invariant under arbitrary monotone transformations, and none is universal biological truth. Full taxonomy is in `docs/S1_0_ESTIMAND_TAXONOMY.md`.

## 5. Estimand stability

Microbial raw/log strong-support median Jaccard is **0.633** and median overlapping-support sign agreement **1.000**, passing frozen thresholds 0.60/0.80. However, DW067 (0.593) and DW155 (0.250) individually fail. Yeast tau/raw-epsilon Jaccard is 0.505 and Spearman 0.267, but tau has the principled domain preference of removing scaled digenic effects. Drug fixed-set stability fails: median modal label fractions are 0.636 DA and 0.547 emergent.

## 6. Structure-label uncertainty

Yeast threshold labels are noisy operational labels, not error-free truth. Microbial labels require a 95% bootstrap interval excluding zero plus `|beta|>=0.10` log10 CFU. Drug `Inconclusive` remains uncertain. Unmeasured combinations are always `UNKNOWN`, never negative.

## 7. Yeast data audit

Public S1 has 501,510 rows: 410,399 digenic and 91,111 trigenic; 91,050 unique triples, 1,400 genes, 182 query pairs. The paper reports 195,666 tested triple mutants, a different experimental count. The published negative rule yields 3,196 strong tau interactions and 87,915 uncertain/null rows. Median combined-fitness SD is 0.0564. Paper validation reports approximately 40% false negatives and 20% false positives for the detailed CLN1--CLN2 check.

## 8. Dango collision audit

Dango already predicts tau scores with six STRING PPI networks, learned/meta embeddings, self-attention Hyper-SAGNN, random and gene splits, strong-score AUROC/AUPR, and optional GP uncertainty. It evaluates score regression plus `|tau|>0.05` classification, not direct uncertainty-aware support recovery under Kuzmin's `p<.05,tau<-.08` rule.

Exact reproduction did not reach metrics. Current repository preprocessing unconditionally references absent `string_yeast_mashup_vectors_d500.txt` and `yeast_genes_baker_adjacency.txt`; no substitute was fabricated. The machine has one 8 GB RTX 4060 Laptop GPU, so missing exact inputs—not a categorical compute impossibility—are the decisive blocker. Reported strict-split metric *types* are Pearson, Spearman, strong-subset correlations, AUROC, and AUPR; exact Figure 2 bar heights are not tabulated, so no numbers are invented.

## 9. Microbiome complete-factorial audit

The Ishizawa panel contains 127 nonempty communities and 2,377 CFU measurements. Each focal strain yields a complete 64-cell landscape over six companions with 5--12 replicates/cell. Exact log-scale expansion gives 294 order>=3 coefficients: 74 strong positive, 66 strong negative, 154 uncertain/null.

## 10. Drug-combination audit

There are 20,790 order-3--5 dose contexts but only 182 independent drug sets over eight drugs: 56 triples, 70 quadruples, 56 quintuples. Source inconclusive labels are not support. Numeric DA and emergent effects flip sign somewhere across dose in 98.9% of sets. The valid output is context-dependent support/effect, not one signed hyperedge per drug set.

## 11. Cross-domain compatibility

The abstract common task “sparse order>=3 support from incomplete measurements” is mathematically coherent. Empirically it survives only on microbiome. Yeast becomes side-information score prediction for unmeasured triples; drug becomes context-indexed effect modeling with few identity sets. Therefore fewer than two domains instantiate the same directly evaluable structural problem.

## 12. Identifiability from partial measurements

An order-k Möbius contrast needs all `2^k` subset responses unless additional assumptions replace missing equations. Tau needs the triple plus relevant singles/doubles. Dose-specific emergent contrasts need matched lower-order dose combinations. Missing lower subsets cannot be imputed and relabeled as ground truth. Microbial masking retains full-panel truth retrospectively; yeast and unmeasured drug contexts do not.

## 13. Heredity / pure-HOI prevalence

Among 140 strong microbial order>=3 effects: 22 satisfy strong heredity, 110 weak-only, and 8 are pure non-hereditary. Weak heredity is 94.29%, narrowly below the 95% diagnostic; pure prevalence is 5.71%. The automatic heredity kill rule is not formally triggered, but the scientific evidence is too small and single-domain for a general pure-HOI project.

## 14. Split and leakage audit

Yeast random split is fully gene/pair/query-overlapping. Query-pair-disjoint yields 72,964 train / 18,147 test, zero shared query pairs, 100% any-gene overlap, 25.56% all-gene overlap, and 4.14% any-pair overlap. Query-gene-disjoint yields 57,715/33,396 and zero shared query pair, but 4.48% any-pair overlap. Public S1 lacks raw batch identifiers. Microbial evidence uses retrospective masks; drug primary unit must be drug set.

## 15. Classical contrast baselines

Full exact Möbius inversion is the direct contrast and recovers the operational full-panel labels by construction; it is not a learned benchmark result. Yeast's published tau score is the domain contrast. Drug DA/emergent scores are direct per-context contrasts.

## 16. Sparse/hierarchical baselines

At microbial budget 48, lasso has precision 0.387, recall 0.204, F1 0.235, AP 0.506, signed-support accuracy 0.142, coefficient RMSE 0.434, and response RMSE 0.102. Weak-heredity lasso has F1 0.218, AP 0.509, pure recall 0.350, response RMSE 0.103. Hyperparameters were selected by held-out response MSE from frozen grids.

## 17. Compressed-sensing baselines

OMP at budget 48 has precision 0.141, recall 0.030, F1 0.047, AP 0.479, signed-support accuracy 0.017, pure recall 0.050, coefficient RMSE 0.438, and response RMSE 0.115. It is a greedy compressed-sensing baseline, not a reproduction of sparse-Möbius query algorithms whose sampling assumptions differ.

## 18. Direct support-recovery results

The best budget-48 direct support F1 is 0.235 (lasso), far below the frozen 0.85 sufficiency threshold; 79.6% of strong effects remain unrecovered on average. This is material on the microbial calibration panel. Yeast query-pair empirical-rate AP drops to prevalence 0.0535 and F1 0 under query-pair holdout, but that is a confounding diagnostic rather than a competitive structure learner.

## 19. Pure-HOI subgroup results

At budget 48, pure-HOI recall is 0.425 for lasso, 0.350 after weak-heredity filtering, and 0.050 for OMP. The subgroup failure exceeds 15%, but concerns only eight effects from one biological panel.

## 20. Response-prediction secondary results

Lasso gives the best budget-48 response RMSE and support F1, while weak-heredity lasso gives slightly higher AP. More importantly, response RMSE near 0.10 coexists with support recall near 0.20; a seemingly usable response predictor need not recover structure.

## 21. Classical residual analysis

A real classical residual exists under microbial masking: coherent AND features, missing cells, replicate noise, and a small pure-HOI subgroup challenge lasso/OMP. It does not become an S1 residual because no second direct domain validates it. “F1 below 1” was not used as the criterion.

## 22. Sparse Möbius prior-art audit

Kang et al. 2024 give sparse/low-degree Möbius recovery, including `O(Kt log n)` low-degree group-testing complexity and a noise-tolerant form under assumptions. Erginbas et al. 2026 give adaptive FASMT `O(sd log(n/d))` and PASMT `O(sd^2 log(n/d))`, with hypergraph-reconstruction simulations. These strongly occupy generic and active sparse support recovery under oracle access.

## 23. Active-design prior-art audit

NAIAD actively selects pairwise CRISPR/drug combinations to optimize response, not order>=3 structural support. The objective distinction is real, but adaptive sparse Möbius/group testing already covers much of the theory, and this project lacks a prospective order>=3 real panel to evaluate the remaining noisy/FDR distinction.

## 24. Candidate concrete problems

Four were scored: uncertainty/FDR support, active structural measurement, pure-HOI recovery, and drug context-varying support. Estimand consensus was rejected as sensitivity analysis rather than a distinct method problem. None survives hard gates.

## 25. Candidate scores

| Candidate | Score |
|---|---:|
| uncertainty/FDR-controlled support | 45/60 |
| active structural measurement | 43/60 |
| non-hereditary pure-HOI recovery | 41/60 |
| shared/context-varying drug support | 39/60 |

Hard-gate failures override scores. Finalists retained: **0**.

## 26. Publication feasibility

The current evidence cannot support a general cross-domain structure-learning paper. Yeast-only novelty is constrained by Dango; microbiome-only evidence is small and collides with compressed sensing; drug-only shared support is empirically unstable. A domain methods note may be possible after new data, but not from the present benchmark alone.

## 27. Strongest evidence FOR continuation

The microbial target is identifiable, median raw/log support passes the frozen stability gate, and tuned classical baselines miss about 80% of strong support at budget 48 while pure-HOI recall remains at most 0.425. Response RMSE also fails to reveal this structural miss.

## 28. Strongest evidence AGAINST continuation

That positive evidence is one seven-member system. Yeast lacks direct unmeasured-triple truth and is already occupied by Dango for PPI-based score prediction; drug signed support changes across dose in 98.9% of identity sets. The second real direct benchmark required for a general claim is absent.

## 29. Hard-gate table

| Gate | Result | Reason |
|---|---|---|
| estimand | PASS, narrow | accepted domain contrasts; microbial median Jaccard/sign 0.633/1.000 |
| identifiability | **FAIL** | only microbial masked recovery has direct complete truth; unmeasured yeast/drug-context structures are not directly identified |
| cross-domain benchmark | **FAIL** | fewer than two domains support the same direct leakage-resistant recovery task |
| leakage design | PASS | strict split units are definable, though they expose rather than solve truth scarcity |
| classical residual | **FAIL for S1** | material residual is confined to one small panel |
| novelty | **FAIL** | Dango, sparse Möbius/adaptive group testing, compressed sensing, and FDR literature occupy the nearest routes |

## 30. Final decision

**S1.0-C — NO-GO: ESTIMAND / IDENTIFIABILITY.** This code is selected because Q3/Q4 fail before model comparison can justify a general S1 method. Prior-art saturation is an additional stop, not the primary decision label.

## 31. Exact next action

Freeze S1.0 at this commit and return to project-level review. Do not start S1 model/theory work and do not automatically move to Rank-2 temporal hypergraph prediction. Reopen only after a second real replicated order>=3 panel with required lower-order responses and leakage-resistant direct truth is identified.
