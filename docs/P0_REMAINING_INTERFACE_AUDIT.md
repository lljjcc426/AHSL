# P0 remaining-interface audit

## Decision standard

A surviving strong-coupling interface must pass necessity, benchmark,
identifiability, classical residual, prior-art residual and program-depth gates.
Being unimplemented is not positive evidence.

## Candidate A: hypergraph-parameter-aware generalization theory

- Positive: current HGNN bounds show structure can enter PAC-Bayes bounds and
  correlate with loss.
- Theory-necessity result: no evidence that alpha/beta/gamma acyclicity,
  GHW/FHW or fractional covers are indispensable; spectral/incidence quantities
  preserve the problem.
- ML-necessity result: ML is the object of study, but no native-theory residual
  is established.
- Benchmark: standard HGNN classification data, not two benchmarks whose
  outcome depends on decomposition parameters.
- Exact remaining contribution: no non-architectural one-sentence contribution
  can presently be stated.
- Verdict: **reject for P0-A; Q3**.

## Candidate B: learning-augmented parameterized algorithms

- Positive: consistency/robustness/fallback theory is clean; prediction can
  preserve exactness.
- Strongest classical threat: current exact/approximation/FPT GHD/FHD algorithms.
- Strongest modern threat: generic prediction-augmented covering, graph
  approximation and solver-selection frameworks.
- R0 transfer: near-fatal because predictability, residual, two-family
  benchmarks and label amortization all failed.
- Exact remaining contribution would require a proven hypergraph-specific
  advice-error measure that improves an established bound and is learnable on
  real repeated instances. No evidence supplies that object.
- Verdict: **reject for P0-A; retain decomposition problem as Q2**.

## Candidate C: adaptive/query algorithms

- Positive: SP-query hypertree learning, CUT-query connectivity and adaptive
  sparse Möbius transforms exhibit native identifiability and query-complexity
  phenomena.
- ML-necessity result: these are exact/randomized algorithms or computational
  learning theory; a trained predictor is not needed.
- Benchmark: declared oracle families and some real-hypergraph simulations,
  not two accepted scientific acquisition systems.
- Program depth: genuine theory depth exists in query models, adaptivity,
  robustness and restricted classes.
- Verdict: **Q2; useful neighboring theory, not strong coupling**.

## Candidate D: certified approximation selected by predictions

This is not distinct from Candidate B unless it names a hypergraph-specific
prediction and measured workload. “Use learned predictions to choose a GHD/FHD
algorithm while checking the certificate” is generic portfolio selection. R0
already audited this interface. Verdict: **effectively covered; reject**.

## Strongest exact conclusion

No Q1 interface survives. The best positive residual is instead:

> Design and analyze verifiable, reusable and dynamically maintainable
> hypertree decompositions, with exact/approximation guarantees tied to
> conjunctive-query and CSP structure; ML is optional and excluded from the
> core claim unless future evidence independently establishes necessity.

This is a P0-B program, not a rescued P0-A formulation.
