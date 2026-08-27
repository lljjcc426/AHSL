# R0 Learning-Augmented Algorithms Audit

## Applicable contract

The learning-augmented paradigm separates:

- consistency when a prediction is accurate;
- robustness when it is wrong;
- a prediction-error-dependent degradation or a safe fallback.

Exact inference has a particularly clean correctness layer. A poor order or
verified decomposition may be slow but remains exact. A portfolio can fall back
to min-fill or run bounded probes. A proposed pruning bound is not safe unless
the deterministic solver independently proves admissibility.

## Candidate guarantees

Plausible future statements include competitive cost against the best strategy
in a fixed portfolio, regret relative to min-fill, and a fallback bound such as
`cost <= min(predicted plan after probe, classical plan) + probe overhead`.
Prediction-assisted separator search could retain completeness by using the
prediction only to order an exhaustive search.

## Why the framework is insufficient for GO

The framework supplies an architecture, not a problem residual. R0 found no two
factor benchmark families with a >=3x gap among reasonable VE policies. For GHD
search, HyperBench supplies decomposition labels/times but not downstream factor
inference. For solver portfolios, JoinInfer already uses measured structural
quantities and a data-driven hybrid, while generic algorithm-selection
literature supplies the learning machinery.

Oracle labels are also expensive: a full order/decomposition/engine sweep can
cost several exact solves per instance, and timeouts yield censored labels.
Amortization is plausible only for repeated evidence/query workloads or a stable
application generator. UAI and HyperBench are heterogeneous benchmark archives,
not demonstrated deployed repeated workloads.

No predictor was trained. Learnability and family-shift robustness therefore
remain unproven hard gates rather than assumptions.
