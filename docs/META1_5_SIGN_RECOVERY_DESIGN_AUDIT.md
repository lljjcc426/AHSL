# Sign-recovery optimal-design audit

## Primary threat

The strongest collision is Stallrich, Young, Weese, Smucker, and Edwards (JRSS-B, 2025), *An optimal design framework for lasso sign recovery*, DOI `10.1093/jrsssb/qkaf026`.

## Exact statistical object

The model is the homoscedastic Gaussian main-effects linear model

\[
y=\mathbf 1\beta_0+X\beta+\varepsilon,\qquad \varepsilon\sim N(0,\sigma^2 I),
\]

with a two-level supersaturated design. Sign recovery means equality of the estimated and true extended sign vectors: zeros, positive entries, and negative entries must all be correct. This is stricter than unsigned support recovery.

For fixed penalty `lambda` and known coefficient vector, the local criterion is the exact probability of the joint KKT events:

- `S_lambda`: active variables enter with the correct signs;
- `I_lambda`: inactive variables are excluded.

The events are independent under the paper's formulation, so the local sign-recovery probability factors into their probabilities. It depends on the centered/scaled design through active-set covariance, active/inactive cross-correlation, variances, coefficient magnitudes, signs, and noise scale.

## Known and unknown support

The local criterion assumes the full active set and coefficient magnitudes. The paper explicitly recognizes that known support produces a degenerate optimal construction: inactive columns may be confounded with the intercept. Its practical criteria therefore average the probability over all supports of a fixed size and, for unknown signs, over sign vectors up to global reflection. Thus:

- support identities: unknown in the practical criterion;
- sparsity level `k`: specified;
- active effect magnitude or SNR: specified and commonly equal across active factors;
- sign information: either known all-positive or averaged over unknown signs;
- penalty: summarized along a lambda path by maximum or area-type summaries.

This is genuine unknown-support design, not merely design conditional on a guessed support.

## Design variable and construction

The paper searches entries of a two-level factor-level supersaturated design. HILS (Heuristic-Initiated Lasso Sieve) first uses coordinate exchange to obtain a Pareto set under tractable correlation heuristics, then ranks that set using the expensive exact sign-recovery criterion. For unknown signs, orthogonal correlation is the ideal local structure within the completely symmetric relaxation. For known positive signs, small positive constant correlations can dominate orthogonality.

The empirical examples are synthetic main-effect SSDs. They compare HILS designs with Dantzig-based consistency designs and UE(s2)/Var(s+) families. They do not use factorial interaction columns, biological data, repeated measurements, heteroscedasticity, FDR control, or sequential response-adaptive acquisition.

## Can the criterion be applied directly to META1?

**At the level of a fixed full-rank standardized linear design, yes in principle. At the level required by META1, not without a material reformulation.**

The KKT probability is algebraically generic in the columns of `X`; labeling a column as a third-order interaction does not escape the theory. Therefore the basic sign-recovery objective subsumes the scientific principle behind using geometry to improve signed support recovery, and `hybrid_d50` is a weaker heuristic rather than a new optimal-design principle.

Direct deployment nevertheless fails for four concrete reasons:

1. META1 selects rows from a fixed 64-community candidate set; HILS changes factor-level entries of an SSD.
2. The full AND dictionary has nested column supports, zero-variance columns on some partial row sets, and exact aliases. The paper's active-set formulas require invertible active covariance for each evaluated support.
3. META1 targets only order>=3 coefficients while lower-order terms remain nuisance structure; Stallrich treats all columns symmetrically as possible main effects.
4. META1 has replicate-derived cell means and empirically unequal cell variances; Stallrich assumes `sigma^2 I` and no replicate allocation.

These are real technical differences, but they do not preserve novelty for generic “support-aware design” or for `hybrid_d50` itself.

## Closest supporting works

- Singh and Stufken (2023) construct Dantzig-based consistency designs using restricted-eigenvalue and weak sign-consistency diagnostics averaged over active subsets. This independently occupies support-aware SSD construction.
- Young et al. (2024) compare screening designs along exact Lasso support/sign-recovery probability curves and provide supplementary code, reinforcing that post-hoc recovery-probability comparison is already established.
- Huang, Kong, and Ai (2020) optimize approximate-design criteria derived from the asymptotic covariance of a debiased Lasso; this is inference-oriented sparse design, though not exact sign recovery.
- Wainwright (2009) supplies deterministic/random-design conditions and sharp noisy signed-support thresholds; it is recovery theory, not a row-selection algorithm.

## Baseline implementability decision

No `sign_recovery_design_baseline` is implemented in META1.5. The exact 2025 criterion is not a parameter-free evaluator for the current matrix: it requires a sparsity/effect-size specification, treatment of singular support subsets, a decision about nuisance lower orders, and a row-exchange adaptation. Choosing these items would already instantiate the modified research method and would violate the audit-only/no-new-candidate boundary.

Before any later Confirmation, META1.6 must implement a published HILS/DCD-inspired comparator on Development-only data, with its support ensemble and effect-size rule fixed without reference to full-panel support outcomes.

## Collision judgment

Collision severity: **4/5 (same problem and core mechanism)**. It is not 5/5 because no published construction directly solves fixed-row selection for a hierarchical AND dictionary with an order-targeted estimand and replicated biological observations.
