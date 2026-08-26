# S1.0 heredity audit

Definitions for an active order-k term:

- strong heredity: every immediate order-(k-1) parent is active;
- weak heredity: at least one immediate parent is active;
- pure/non-hereditary: no immediate parent is active.

Labels are defined from the replicate-aware experimental estimand, not from a method's predictions.

## Real complete-panel result

For the 140 strong order>=3 log10-CFU Möbius terms:

| Class | Count | Fraction |
|---|---:|---:|
| strong heredity | 22 | 15.71% |
| weak only | 110 | 78.57% |
| pure non-hereditary | 8 | 5.71% |
| any weak heredity | 132 | 94.29% |

The preregistered diagnostic kills/downgrades the non-hereditary candidate if weak heredity is at least 95% *and* hierarchical methods recover well. The prevalence is just below 95%, while weak-heredity lasso at budget 48 is not sufficient (F1 0.218). Formally, the automatic kill condition is not met.

Scientifically, eight pure effects across one seven-member system are too little evidence for a general method. Lasso pure recall 0.425 and OMP 0.050 show a subgroup failure, but the subgroup is small and dependent. The proper conclusion is **candidate downgraded, not declared impossible**.
