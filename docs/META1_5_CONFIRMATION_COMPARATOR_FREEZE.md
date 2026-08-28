# Confirmation comparator freeze

## Current status

Confirmation is **not authorized**. META1.5 decided MODIFY, so the current candidate and current reserve must not be used for a publishable confirmation claim.

## Why no baseline was implemented in META1.5

The Stallrich 2025 exact criterion cannot be transferred without choosing a support-size/effect-size ensemble, resolving singular AND supports, deciding how lower-order nuisance coefficients enter, and changing HILS from free factor-entry construction to fixed-row selection. Those choices define the modified method rather than a neutral audit comparator. Literature evidence was sufficient to decide collision, so no post-Development performance run was justified.

## Mandatory META1.6 comparator skeleton

Before creating a new reserve, modified Development must compare:

1. the modified support-robust AND-row method + frozen estimator;
2. `hybrid_d50 + ElasticNet` as the old diagnostic heuristic;
3. `uniform + ElasticNet`;
4. `D-opt + ElasticNet`;
5. one faithful HILS/DCD-inspired `sign_recovery_design_baseline + ElasticNet`.

`uniform + ARD` may remain a secondary estimator comparator, but it is not a substitute for the published support-aware design baseline. No ASMT panel comparator is mandatory unless its observation model can be implemented without changing the estimand; otherwise it remains a synthetic/query-complexity comparator.

## Baseline freeze requirements

For `sign_recovery_design_baseline`, META1.6 must freeze before outcome evaluation:

- support sizes and their weights;
- effect-size/SNR grid or prior;
- sign prior;
- lambda-path summary;
- treatment of zero-variance and singular support subsets;
- lower-order nuisance handling;
- row-exchange initialization and stopping rule.

These choices cannot be tuned against full-panel support labels.

## Future Confirmation set

There is no final future set until modified Development selects and freezes a method. The minimum eligible future Confirmation set is: modified candidate, uniform ElasticNet, old `hybrid_d50` ablation, strongest HILS/DCD-inspired design baseline, and uniform ARD secondary. Weak extra baselines should not be added.
