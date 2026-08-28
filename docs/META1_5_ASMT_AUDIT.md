# ASMT and sparse Mobius audit

## Kang et al. 2024: nonadaptive noisy SMT

Kang, Erginbas, Butler, Pedarsani, and Ramchandran study a sparse low-degree Mobius transform of a real-valued set function. Their nonadaptive sampling hashes coefficients into bins and uses sparse-graph peeling and group-testing delays. With `K` nonzero coefficients, the general construction uses `O(Kn)` samples; under maximum degree `t`, the group-testing construction uses `O(K t log n)` samples.

This paper is the strongest collision with any claim of “noise-tolerant sparse Mobius recovery.” Its robust theory assumes i.i.d. **spectral/bin noise**: delayed subsampled coefficients are corrupted as `U_i(k)=signal+Z_i(k)` with independent Gaussian `Z_i(k)`. The singleton test assumes known nonzero magnitude `|F(k)|=rho` or a fixed SNR. Support locations follow random/independence assumptions used by the sparse-graph analysis.

That noise is not META1's observation model. Independent cell-level biological errors are linearly mixed by Mobius/bin operations, producing correlated, query-dependent and potentially heteroscedastic spectral noise. Replicates estimate cell-specific uncertainty rather than supplying repeated independent noisy versions of each abstract spectral bin. The adaptation is therefore not a one-line variance substitution.

## Erginbas et al. 2026: FASMT/PASMT

Erginbas, Kang, Polito, and Ramchandran study exact learning of an `s`-sparse degree-`d` real Boolean polynomial in the AND basis from an exact additive evaluation oracle.

- FASMT: fully adaptive binary-splitting/peeling, `O(s d log(n/d))` queries.
- PASMT: few-round group-testing construction, `O(s d^2 log n)` queries in `O(d^2 log n)` rounds.
- Guarantee: exact support and coefficient recovery under affine-slice non-cancellation.
- Lower bound: `Omega(s d log(n/d)/log s)` for the stated coefficient class.
- Evaluation: synthetic hypergraphs plus circuit and metabolic-network hypergraphs; oracle responses remain exact.

The paper explicitly lists noise robustness as open and suggests robust group testing, particularly for PASMT, as a possible route. That statement shows both sides of the novelty question: noisy adaptation is not completed, but the authors view part of it as a natural extension. A contribution must therefore address the statistical gap concretely, not just add Gaussian noise in simulation.

## Precursor set-function recovery

Wendler et al. (2021) give adaptive algorithms for sparse set functions in nonorthogonal Fourier bases, including an AND-related basis, with at most `n k - k log2(k) + k` queries under non-cancellation/generic coefficient assumptions. Stobbe and Krause (2012) recover Fourier-sparse set functions from random queries when the support lies in a known candidate collection. Both use exact oracle evaluations and do not provide replicated-response inference.

## Answers to the kill questions

### Q1. Can FASMT/PASMT run directly on META1 landscapes?

No. Exact zero tests, residual subtraction, and affine-slice non-cancellation are not stable under continuous replicated response noise. The real-valued signs do not fix this.

### Q2. Is adding noise routine?

Not for the META1 observation model. Robust group testing is a credible ingredient, so “some noisy extension” is expected. But mapping raw heteroscedastic cell noise and replication into correlated Mobius/bin errors, setting detection thresholds for approximate sparsity, and preserving a signed order-targeted estimand requires a new statistical formulation. This is nontrivial, though not automatically publishable.

### Q3. Does ASMT make hybrid D-opt secondary?

Yes for the exact sparse-query model: ASMT chooses queries from the algebraic support-search problem and has query-complexity guarantees, whereas `hybrid_d50` is a geometry heuristic. For a fixed finite panel with noisy outcomes and no adaptive oracle, ASMT is not directly executable.

### Q4. Is META1's estimand different?

Yes. META1 defines support by a full-panel biological effect threshold and scores signed order>=3 recovery. SMT/ASMT target exact nonzero coefficients of an exactly sparse set function. The difference is substantive only if future design and inference explicitly respect threshold uncertainty, nuisance lower orders, and raw-response noise.

## Collision judgment

- Kang 2024 severity: **4/5**.
- Erginbas 2026 severity: **4/5**.
- Wendler 2021 severity: **3/5**.

No single ASMT work directly solves META1, but the wide claim “sparse/noisy Mobius query design” is occupied.
