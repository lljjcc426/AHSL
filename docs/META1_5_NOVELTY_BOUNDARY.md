# META1.5 novelty boundary

## Unique decision

**META1.5-B — MODIFY.**

## Definitely not novel

- partial/fractional factorial measurement;
- exact-alias diagnosis or elimination;
- D-optimal or correlation-based row selection for sparse polynomial fitting;
- unknown-support robustness obtained merely by averaging a design criterion over supports;
- optimizing or evaluating a design by Lasso support/sign-recovery probability;
- exact or noise-tolerant sparse Mobius recovery as a broad claim;
- high-order interaction selection or FDR-controlled interaction discovery as broad claims;
- `hybrid_d50` as a standalone algorithm.

## Why CLEAR fails

Stallrich 2025 directly occupies support/sign-recovery optimal design and already treats unknown support identities through averaging. Singh-Stufken 2023 supplies a closely related construction tied to sparse recovery conditions. Kang 2024 occupies noise-tolerant low-degree sparse Mobius recovery, and Erginbas 2026 supplies adaptive AND-basis query selection with near-optimal exact-oracle complexity. The frozen candidate therefore cannot proceed as though the broad objective were unoccupied.

## Why COLLISION is too strong

No reviewed method directly solves the joint object:

1. select a subset of rows from a fixed finite Boolean factorial candidate set;
2. fit a coherent nested AND dictionary with zero/alias feasibility failures;
3. target signed support only for order>=3 while lower orders are nuisance;
4. remain robust to unknown support identities and effect signs;
5. operate on noisy biological responses rather than exact or spectral-bin oracles.

Porting HILS is not mechanical because its search variable and regularity assumptions change. Porting noisy SMT is not mechanical because raw cell noise becomes correlated, query-dependent transform noise. This residual is technically plausible, not application-only.

## Exact remaining boundary

The defensible modified question is:

> Given a fixed finite Boolean factorial row pool and a hierarchical AND dictionary, how should a limited row set be selected to maximize robust signed recovery of order>=3 coefficients over an unknown-support/effect-size ensemble, while treating lower-order coefficients as nuisance and explicitly penalizing zero/alias-infeasible support subsets under additive response noise?

The central novelty candidate is a **statistical objective plus row-selection algorithm**. Replicate heteroscedasticity and FDR are not central in the first modified Development because META1 did not establish them as mechanisms.

## Nontriviality requirements

The modified direction survives only if META1.6 demonstrates all of the following:

- a formal order-targeted robust recovery objective that is not just generic HILS evaluated on relabeled columns;
- a row-exchange or lattice-aware construction for the fixed candidate set;
- explicit handling of singular/aliased support subsets rather than silently dropping them;
- support-independent hyperparameters or priors fixed before outcome evaluation;
- improvement over uniform, D-opt, `hybrid_d50`, and a faithful HILS/DCD-inspired comparator on new Development evidence;
- a new untouched reserve created only after the modified method and regime are frozen.

## Current contribution interpretation

`hybrid_d50` is best retained as **I2: a diagnostic heuristic exposing a problem**. It is not supported as I1 (new algorithm) or I3 (final deployable method). The exact-alias/F1 association motivates the modified objective but does not prove it.
