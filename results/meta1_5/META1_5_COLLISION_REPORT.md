# META1.5 collision report

## 1. Executive decision

**META1.5-B — MODIFY.** The frozen `hybrid_d50 + ElasticNet` result remains a valid Development observation, but not a novel support-aware design algorithm. Direct Lasso sign-recovery design, unknown-support SSD criteria, and noisy sparse Mobius recovery are already established. A narrower fixed-row, order-targeted, alias-feasible AND-dictionary problem remains plausible and requires a new Development phase and a new reserve.

## 2. Frozen META1 candidate

Base `79204a06e5079b6167153edf03cdb8ee0dcda514`; candidate `hybrid_d50 + ElasticNet`; Ishizawa `d=6`, at least five replicates/cell, log10 CFU, budgets 16/24/32 and <=50% rows. Development signed order>=3 macro F1 rose from 0.2001 to 0.2509 (+0.0508). The choice was outcome-adaptive; Diaz-Colunga was negative; only 50/84 mask pairs improved.

## 3. Exact novelty question

The question is not whether microbiome panels have used D-optimal sampling. It is whether observation model, support estimand, design objective, and construction algorithm jointly leave a nontrivial open object: fixed Boolean-row acquisition for unknown signed order>=3 support in a coherent AND dictionary under noisy replicated responses.

## 4. Sign-recovery optimal design

[Stallrich et al. 2025](https://doi.org/10.1093/jrsssb/qkaf026) define exact Lasso sign recovery via active-sign and inactive-exclusion KKT events, then optimize their probability. The local criterion assumes known beta and lambda; practical criteria average over all supports of fixed size and over unknown sign vectors, using specified effect magnitude/SNR. HILS uses coordinate exchange under tractable correlation heuristics and an exact-probability sieve.

Its principle applies to any suitable standardized linear design, so the broad META1 objective is occupied. Its algorithm is not directly transferable to the partial AND matrix because it searches free +/-1 main-effect designs and assumes regular active covariance, homoscedastic noise, and symmetric column targets.

## 5. Classical fractional factorial design

[Box and Hunter 1961](https://doi.org/10.1080/00401706.1961.10489951) established alias/resolution analysis for fractional factorials. Tang-Wu and later supersaturated-design work optimize near-orthogonality and correlation distributions. Jones et al. and Smucker-Drew construct designs robust over large sparse model spaces. Exact-alias elimination and unknown-model averaging are therefore not new.

## 6. Sparse/support-aware experimental design

[Singh and Stufken 2023](https://doi.org/10.1080/00401706.2022.2102080) construct Dantzig-based consistency designs using active-subset restricted-eigenvalue and weak sign-consistency conditions. [Huang et al. 2020](https://doi.org/10.1007/s00184-019-00722-9) optimize debiased-Lasso covariance criteria. These works rule out novelty claims based only on coupling sparse regression with DOE.

## 7. ASMT and sparse Mobius recovery

[Erginbas et al. 2026](https://arxiv.org/abs/2602.06246) exactly learn sparse degree-bounded AND polynomials using adaptive FASMT or few-round PASMT, with `O(sd log(n/d))` and `O(sd^2 log n)` queries respectively under an exact additive oracle and non-cancellation. [Kang et al. 2024](https://proceedings.neurips.cc/paper_files/paper/2024/hash/520b379123d16e41f85472e766846486-Abstract-Conference.html) give nonadaptive sparse Mobius recovery with a robust noisy version.

Thus ASMT supplies a scientifically stronger query strategy than hybrid D-opt in its exact sparse-oracle regime.

## 8. Noisy sparse recovery

[Wainwright 2009](https://doi.org/10.1109/TIT.2009.2016018) already treats exact Lasso signed-support recovery under additive response noise and gives sharp asymptotic thresholds for Gaussian designs. Kang's robust SMT assumes iid Gaussian noise at spectral/bin observations and known magnitude/SNR. Neither directly models cell-level replicate means whose transform errors are correlated and heteroscedastic.

## 9. Replicate/heteroscedastic design

No deep-reviewed method jointly allocates/selects Boolean communities and biological replicates for signed high-order support recovery under empirical cell variances. This is a real gap, but META1 P1 did not identify replicate noise as the gain mechanism. Replicate awareness is therefore future-only rather than the modified core claim.

## 10. FDR/inference-aware design

[Suzumura et al. 2017](https://proceedings.mlr.press/v70/suzumura17a.html) provide selective inference for sparse high-order interaction models. [Chen et al. 2025](https://doi.org/10.1038/s42256-025-01086-8) use model-X knockoffs to control interaction FDR. Neither chooses factorial rows. FDR-aware acquisition remains plausible, but META1's high absolute FDR and failed P2 do not support it as the immediate method.

## 11. Higher-order interaction design

For `d=6`, 42 of the 63 nonempty AND columns are order>=3. Their row supports are nested along the Boolean lattice, unlike freely chosen main-effect SSD columns. The target also distinguishes high-order coefficients from lower-order nuisance terms. These features can change design optimality, but only an objective or algorithm that uses them is novel; column relabeling is not.

## 12. Exact-alias interpretation

Classical DOE already studies exact aliasing. META1's exact-alias fraction 0.0168 to 0 is a useful mechanism-consistent signal, not a discovery. Alias removal is necessary for some support pairs but not sufficient for recovery: near-aliasing, minimum eigenvalues, active/inactive KKT geometry, effect sizes, and noise remain decisive.

## 13. Applicability of prior algorithms to META1

The Stallrich probability can evaluate only well-defined full-rank support blocks after standardization; many partial AND row sets have zero or identical columns. HILS must be reformulated from entry exchange to row exchange, and its support ensemble must distinguish high-order targets and nuisance lower orders. FASMT/PASMT cannot use noisy real-valued zero tests directly. Kang's noise model does not equal raw biological response noise. No prior algorithm is plug-and-play, but their objectives substantially subsume the broad idea.

## 14. Tiny implementation sanity checks

No comparator was implemented or run. Literature and algebra were sufficient for the collision decision. A faithful 2025 baseline would require choices about sparsity, effect size, signs, lambda summary, singular supports, and lower-order nuisance handling; making those choices would constitute the modified method. No Development or reserve outcome was used post hoc.

## 15. Contribution decomposition

The ten components C1-C10 are recorded in `docs/META1_5_CONTRIBUTION_COLLISION_MATRIX.md`. The benchmark/biological pieces C1/C10 are mostly application value. C3-C5 and C7-C9 are heavily occupied. C8 is occupied by sparse Mobius work. The only plausible technical contribution is a nontrivial coupling of fixed Boolean row feasibility, order-targeted recovery, and support robustness.

## 16. Collision matrix

Seventeen deep works are extracted paper-by-paper in the collision matrix. The highest severity is 4/5 for Stallrich 2025, Singh-Stufken 2023, Kang 2024, and Erginbas 2026. No paper scores 5 because none matches the complete fixed-row/noisy/order-targeted biological object.

## 17. What is definitely not novel

Limited-run factorial design, D-optimal sparse polynomial acquisition, alias elimination, unknown-support model averaging, Lasso sign-recovery design, noisy sparse Mobius recovery, and interaction FDR inference are all occupied. `hybrid_d50` is weak as an algorithmic contribution.

## 18. What may still be novel

A recovery objective and construction for fixed candidate rows in a hierarchical AND dictionary that targets only signed order>=3 support, treats lower orders as nuisance, and assigns explicit loss to zero/alias-unidentifiable support scenarios. Response-noise and replicate extensions may later be added if mechanism evidence supports them.

## 19. Strongest argument for CLEAR

No reviewed paper directly handles fixed microbial community rows, threshold-defined high-order Mobius support, nested AND aliases, and replicated biological responses. HILS and ASMT both require material observation/design changes.

This is insufficient for CLEAR because their central objectives already occupy the broad claim and the frozen heuristic does not solve the residual technical problem.

## 20. Strongest argument for COLLISION

Stallrich supplies the exact sign-recovery criterion and unknown-support averaging; HILS supplies construction. Kang supplies noisy sparse Mobius recovery; ASMT supplies direct AND-basis query design. Combining them with a microbiome dataset could be routine application work.

This is insufficient for COLLISION because raw response noise, fixed-row feasibility, singular nested AND supports, and order-targeted nuisance structure prevent direct use and create a concrete reformulation burden.

## 21. Strongest argument for MODIFY

The broad idea is occupied, but the observed alias/F1 signal is directly relevant to a precise remaining failure mode: support-aware criteria designed for regular main-effect blocks can be undefined or misleading on partial hierarchical AND matrices. A row-constrained, alias-feasible, order-targeted robust objective is a plausible algorithmic intervention and is not supplied by the reviewed work.

## 22. Candidate paper boundary

The strongest possible contribution type is **statistical objective plus algorithm**, conditionally supported by an empirical phenomenon. It is not theory yet, not FDR control, and not replicate-aware design. `hybrid_d50` remains a diagnostic ablation, not the paper's method.

## 23. Confirmation comparator implications

Current Confirmation is canceled. META1.6 must first compare a modified candidate with uniform, D-opt, old `hybrid_d50`, and a faithful HILS/DCD-inspired sign-recovery baseline on Development-only evidence. A new reserve may be constructed only after these are frozen. ASMT is a conceptual/synthetic comparator unless its observation model can be matched honestly.

## 24. Reserve integrity

`reserve_consumed = NO`. Seeds 505/606 were not run, regenerated, or inspected. They remain physically untouched but are not valid for a materially modified candidate and must not become the new reserve.

## 25. Final decision

**META1.5-B — MODIFY.** Strongest prior-art severity: **4/5**. `hybrid_d50` itself is **NO/WEAK** as novelty. The exact remaining problem is technically nontrivial but unvalidated.

## 26. Exact next action

Do not execute META2 or the current reserve. Start META1.6 Development by formally specifying the support/effect/sign ensemble, lower-order nuisance model, singular-support loss, and fixed-row search. Implement the HILS/DCD-inspired baseline before evaluating outcomes. If the modified objective fails to beat the strong baselines on Development-only evidence, stop the direction; if it passes, freeze the method and create a new reserve.
