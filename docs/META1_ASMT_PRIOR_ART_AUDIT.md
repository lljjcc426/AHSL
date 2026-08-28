# META1 ASMT and neighboring prior-art audit

The closest algorithmic threat is Erginbas et al., *Adaptive Sparse Möbius Transforms for Learning Polynomials* (arXiv:2602.06246). It studies exact learning of an \(s\)-sparse real Boolean polynomial of degree \(d\) in the coherent AND basis. FASMT uses \(O(sd\log(n/d))\) adaptive queries and PASMT uses \(O(sd^2\log(n/d))\), with simulated hypergraph reconstruction. This directly occupies generic query-efficient sparse Möbius recovery.

The collision is substantial but not exact. META1's object is a replicate-aware statistical signed-support estimand under heteroscedastic biological noise and non-oracle partial measurement. ASMT assumes an exact sparse function/query model and does not supply the panel-specific bootstrap estimand, empirical FDR audit, or real replicated microbial evaluation used here. Conversely, META1 does not establish new query-complexity theory and its `sparse_mobius_iht` is only a feasible noisy comparator, not an implementation of the full ASMT algorithms.

The IHT comparator is near zero in signed-support F1 on both panels and therefore does not close the empirical gap. That fact is not evidence that ASMT itself fails in this setting; implementing noise-aware ASMT is separate future work.

Other relevant boundaries are:

- Kang et al. (NeurIPS 2024) and Wendler et al. (AAAI 2021) occupy sparse set-function/Möbius learning.
- Classical D-optimal/fractional-factorial design makes a simple pivoted-row contribution difficult to claim as novel by itself.
- Lengerich et al. (AISTATS 2020) emphasize interaction identifiability and functional ANOVA; this reinforces the need to state the Möbius/response-scale estimand explicitly.
- Chen and Caramanis (ICML 2013) study support recovery with noisy or missing covariates, a different noise location from replicate response noise.
- Suzumura et al. (ICML 2017) study selective inference for sparse high-order interaction models, raising the bar for inferential claims.

Conclusion: the current result supports a narrow Development direction, not a paper-ready algorithmic novelty claim. The strongest novelty threat is the combination of ASMT-style active sparse recovery with classical optimal-design literature. Confirmation should be preceded by a targeted collision audit focused on noisy AND-basis recovery and support-aware fractional factorial design.
