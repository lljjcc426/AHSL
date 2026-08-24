# Phase A0.75 Audit Notes

Phase A0.75 starts from frozen A0.5 commit
`ab6bafff7afabb8a5811c75712d7ddeefcdc7224`. No A0 or A0.5 result, report, or
configuration was modified.

## Prospective implementation changes

1. The deterministic Kruskal implementation from A0.5 was factored into a
   reusable floating-point-weight function. Binary intersection MWST retains the
   same descending-weight and lexicographic-edge order.
2. NoiseCorrectedMWST retains negative corrected incidences and pairwise weights.
   The only undefined channel is detected by `abs(delta)<1e-12`.
3. ProfileLikelihoodTreeSearch was not implemented until the saved primary run
   produced `BestClassicalExcess > 0.01`. Full single-edge-swap evaluation was
   too costly at 120 datasets, so each iteration deterministically ranks the
   full neighborhood by noise-corrected tree weight and exactly evaluates the
   top 24 candidates using noisy-data profile likelihood. Clean incidence and
   the generating tree are absent from fitting and candidate selection.
4. The first completed A0.75 primary file was rerun with identical seeds and
   configuration to add rowwise tie diagnostics required by the continuation
   rule. This replaced only an A0.75 intermediate file generated on this branch;
   it did not change an estimator or historical evidence.
5. A one-dataset runner integration output was overwritten by the complete
   120-dataset primary run and was never treated as scientific evidence.

## Interpretation notes

Observed incidence and independent MLE produce identical binary decisions for
all primary `R=1` datasets, so they are recorded as one BinaryMWST evidence row.
The profile objective improves while clean downstream performance worsens; this
is a modeling-objective failure, not an engineering failure. No further local
estimator patch was added after the predefined profile search.

No historical bug requiring an A0 or A0.5 result rewrite was found. No project
file was deleted in this phase.

