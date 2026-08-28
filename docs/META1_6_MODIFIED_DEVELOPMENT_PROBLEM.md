# META1.6 modified Development problem

## Status

This document freezes the research question created by META1.5-B. It does not implement the method, train a model, search a regime, or authorize Confirmation.

## Modified problem

Given:

- the fixed complete `d=6` Boolean community pool;
- the hierarchical 63-column nonempty AND dictionary;
- an order>=3 signed-support target over 42 high-order columns;
- lower-order coefficients treated as nuisance;
- budgets 16/24/32 within the previously defined <=50% Development regime;
- additive response noise, initially under a homoscedastic working model;

construct a support-robust row-selection criterion and algorithm that maximize a prespecified aggregate of Lasso/ElasticNet signed-support recovery over an unknown high-order support, sign, and effect-size ensemble, while assigning zero or explicit loss to support scenarios rendered unidentified by zero columns or exact aliases.

## What changes from META1

`hybrid_d50` is no longer the candidate algorithm. It becomes a diagnostic comparator. The new intervention must directly target signed recovery rather than mixing D-optimality and pivot coverage with a tuned fraction.

## What does not change initially

- The scientific response and order>=3 support estimand remain frozen.
- Replicate heteroscedasticity is not the main objective because META1 P1 did not support it as the mechanism.
- FDR control is not the main objective because META1 P2 failed and absolute FDR remains high.
- No new biological panel or broad regime is selected as part of the method definition.

## Required mathematical object

Let `R` be a budget-constrained subset of candidate rows and `X_R` its AND design. Let `Pi` be a prespecified distribution or finite balanced ensemble over high-order active sets, signs, effect magnitudes, and lower-order nuisance states. A candidate objective must have the form

\[
J(R)=\operatorname{RobustAgg}_{\theta\sim\Pi}
P_\theta\{\widehat{\operatorname{sign}}(\beta_{>=3})=
\operatorname{sign}(\beta_{>=3})\mid X_R\}
-\lambda_{\mathrm{alias}}A(R),
\]

where `RobustAgg` is frozen as an average, lower-tail, or maximin summary before outcome evaluation, and `A(R)` explicitly captures unidentified support scenarios. The objective must specify how nuisance lower-order terms enter and how ElasticNet differs from the Lasso-based probability approximation.

## Plausible intervention

A fixed-row exchange or Boolean-lattice search can use Monte Carlo support ensembles and KKT-based sign-recovery approximations, with a separate feasibility term for zero/aliased columns. This is plausible but not yet validated. Simply applying HILS correlation heuristics to all 63 columns is not enough.

## Development gate

META1.6 may advance only if the proposed objective/algorithm:

1. is fully specified without looking at full-panel support outcomes;
2. is demonstrably different from generic HILS/DCD beyond column relabeling;
3. improves the frozen primary metric over uniform, D-opt, `hybrid_d50`, and a faithful HILS/DCD-inspired baseline on Development-only evidence;
4. shows the improvement is tied to the order-targeted/alias-aware objective;
5. is frozen before constructing a new reserve.

If these conditions fail, the remaining novelty is application-only and the direction should stop.
