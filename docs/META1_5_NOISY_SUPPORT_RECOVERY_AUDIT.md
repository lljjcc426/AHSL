# Noisy support-recovery audit

## Response noise versus other noise locations

The audit distinguishes four models:

1. response noise in `y = X beta + epsilon`;
2. noisy covariates or design entries;
3. noisy Boolean/group-test outcomes;
4. noise after a transform or hash into spectral bins.

META1 is type 1, with biological replicates used to estimate cell means and variances. Kang 2024 is chiefly type 4. ASMT 2026 is noiseless. Measurement-error Lasso work is type 2 and is not a direct comparator.

## Classical noisy signed-support theory

Wainwright (2009) studies exact signed-support recovery for the Lasso under deterministic designs with sub-Gaussian additive response noise and random Gaussian designs. The decisive quantities include mutual incoherence, active-submatrix eigenvalues, minimum signal, penalty, sample size, and noise. For the standard Gaussian ensemble the sharp threshold is `n = 2 k log(p-k)` asymptotically.

This establishes that additive response noise and signed support are not new. It does not construct a fixed-row factorial design, model replication, control FDR, or handle the nested AND dictionary specifically.

## Heteroscedasticity and replication

The direct design papers reviewed here assume homoscedastic independent errors or exact oracle responses. None jointly optimizes:

- which Boolean communities to measure;
- how many biological replicates to allocate;
- signed high-order support recovery;
- cell-specific empirically estimated variance.

That combination remains under-covered, but META1 does not support elevating it to the central mechanism: P1 failed to show that replicate/noise modeling explained the observed improvement. The Development signal tracks exact-alias removal more clearly than replicate variance. Replicate-aware design is therefore a future extension, not the frozen META1.6 centerpiece.

## Approximate versus exact sparsity

Biological Mobius coefficients are not plausibly exactly sparse. META1 creates a scientific support estimand by thresholding full-panel coefficients. Exact SMT zero tests and exact Lasso model-selection theory do not automatically provide calibrated recovery for this thresholded, uncertain support. Stallrich 2025 itself identifies small nonzero inactive effects and uncertain effect magnitudes as future-work limitations.

This is a credible statistical distinction. It becomes a contribution only with an explicit objective or guarantee; leaving ElasticNet and thresholding unchanged while changing rows is insufficient.

## FDR status

FDR-aware support recovery is open relative to the reviewed design-construction papers, but it is not supported as the next META1 method. Current absolute FDR remains high, and META1 P2 failed. FDR is classified **open and plausible, but future-only**.

## Conclusion

“Replicate-noisy AND-basis support recovery” is not wholly solved, but its components are heavily occupied. The nontrivial residual is the coupling of raw response noise, fixed Boolean row selection, approximate/thresholded high-order support, and support-robust design. META1.5 does not claim that this coupling is already a validated method.
