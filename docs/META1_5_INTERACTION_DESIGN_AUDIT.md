# Higher-order interaction design and inference audit

## Interaction inference

Suzumura et al. (ICML 2017) develop selective inference for sparse high-order interaction models and an algorithm that characterizes the Lasso selection event without explicitly enumerating the enormous interaction space. The work uses observational predictor-response samples and demonstrates an HIV drug-response application. It addresses post-selection statistical inference, not acquisition of factorial communities.

Chen et al. (Nature Machine Intelligence 2025) introduce Diamond, using model-X knockoffs and non-additivity distillation to control FDR for interactions discovered from fitted machine-learning models. It is strongest for pairwise interactions and assumes observational samples from a feature distribution; it does not choose Boolean factorial rows or estimate Mobius coefficients.

These works occupy “high-order interaction inference” and “FDR-controlled interaction discovery” as broad claims. They do not supply META1's design algorithm.

## Interaction-specific structure

With six companion factors, the nonempty AND basis has 63 columns:

- order 1: 6;
- order 2: 15;
- order>=3: 42.

For subsets `S subset T`, the support of AND column `T` is contained in that of `S`. A partial set of factorial rows can therefore make high-order columns zero, identical to lower-order columns, or identical to each other. This is more structured than a generic freely constructed main-effect SSD.

However, generic linear-model sign-recovery formulas remain valid whenever the relevant covariance blocks are nonsingular. Thus “we relabeled columns as interactions” is weak novelty. A substantive interaction-specific contribution must change at least one of:

- the design objective, by weighting only order>=3 recovery while treating lower orders as nuisance;
- the feasible set, by selecting rows from a fixed Boolean lattice;
- the robust support ensemble, by respecting nested/coherent supports;
- the guarantee or algorithm, by exploiting the lattice rather than generic coordinate exchange.

## Exact-alias interpretation

Exact alias elimination is necessary for distinguishing some coefficients but not sufficient for sparse sign recovery. Alias-free designs can still have poor near-alias correlations, weak minimum eigenvalues, low signal-to-noise ratio, or unfavorable inactive/active KKT geometry. Conversely, a design can tolerate some aliases if the true support never contains the aliased pair, which is why support ensembles matter.

META1's exact-alias change from 0.0168 to zero is best interpreted as an empirical phenomenon exposing a failure mode of uniform partial panels. It is not a standalone algorithmic contribution.

## Design status

No deep-reviewed paper simultaneously provides fixed-row factorial acquisition, coherent AND high-order support, unknown signed support, raw replicated biological responses, and an order>=3 recovery objective. But several papers cover every broad ingredient separately, and Stallrich/Kang cover the two central mechanisms. The remaining combination is potentially nontrivial, not presumptively novel.
