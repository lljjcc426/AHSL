# META1 Confirmation reserve

No Confirmation run was performed in META1. Seeds 505 and 606 are stored in `results/meta1/raw/masks.csv` for all panel/budget combinations and were not used in method development or the final D-B decision.

The proposed one-shot Confirmation package is:

- Population: the seven Ishizawa focal-response landscapes only.
- Budgets: 16, 24, 32 distinct communities.
- Candidate: `hybrid_d50 + ElasticNet` exactly as implemented at the META1 final SHA.
- Primary comparator: uniform-mask Elastic Net with the same revealed-response tuning procedure.
- Secondary comparator: ARD support on the same uniform reserve masks; it guards against a weak-support-baseline explanation.
- Primary statistic: landscape-macro signed order>=3 support F1, paired by landscape, budget, and reserve seed.
- Required guardrails: signed precision/recall, AP, empirical FDR, held-out response RMSE, coefficient RMSE, seed stability, and runtime.
- Frozen success interpretation: a positive paired macro-F1 effect across both reserve seeds and most landscapes/budgets, without material FDR inflation or response-RMSE degradation. Exact uncertainty intervals should be reported; no pass threshold will be relaxed after seeing reserve outcomes.

Before spending the reserve, conduct a bounded novelty audit of noisy/adaptive sparse Möbius recovery and support-aware factorial design. If that audit shows the exact hybrid mechanism and inferential target are already covered, do not claim algorithmic novelty even if Confirmation succeeds.

Do not use reserve results to tune D-opt fraction, response scale, support threshold, or the budget boundary. Any such change returns the work to Development and requires a new reserve.
