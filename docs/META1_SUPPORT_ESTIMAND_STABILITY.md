# META1 support-estimand stability

The primary reference rule is `META1-R1-CI95-practical-effect`: exact Möbius transform of complete-panel cell means, 1,000 within-cell replicate bootstrap samples, a 95% interval excluding zero, and the panel-specific practical-effect threshold documented in `META1_SCOPE_AND_ESTIMAND.md`.

## Primary support

| Landscape | support | positive | negative | pure HOI |
|---|---:|---:|---:|---:|
| Ishizawa DW039 | 26 | 13 | 13 | 3 |
| DW067 | 26 | 11 | 15 | 0 |
| DW100 | 19 | 12 | 7 | 2 |
| DW102 | 16 | 9 | 7 | 0 |
| DW145 | 18 | 12 | 6 | 0 |
| DW147 | 17 | 11 | 6 | 0 |
| DW155 | 15 | 5 | 10 | 2 |
| Díaz-Colunga | 28 | 23 | 5 | 0 |

Ishizawa totals 137 signed effects (73 positive, 64 negative), including 7 pure HOIs (5.11%). Díaz contributes 28 (23 positive, 5 negative), with no pure HOI. Across all eight landscapes there are 165 effects and 7 pure HOIs (4.24%). Pure HOI means that the selected higher-order effect lacks a selected lower-order parent under the same reference rule; it is a property of this estimand, not a biological impossibility statement.

## Stability findings

- Bootstrap-seed stability is adequate but not perfect. Median pairwise Jaccard is about 0.94 across Ishizawa focal landscapes, with the worst landscape minimum 0.824; Díaz median is 0.883 and minimum 0.803.
- Threshold multipliers 0.8 and 1.2 barely alter the primary labels on these data.
- Scale dependence is material: Ishizawa raw-to-log10 median Jaccard is about 0.654; Díaz log1p-to-raw is about 0.475. Primary scales therefore remain panel-specific and are not chosen by method wins.
- Rule sensitivity is modest for Ishizawa: the sign-95 rule averages 22.71 effects versus 19.57 for CI95, with mean Jaccard 0.862; BH10 averages 18.86, with mean Jaccard 0.945.
- Díaz is more rule-sensitive: CI95 selects 28 effects, sign-95 selects 42 (Jaccard 0.667), and BH10 selects 9 (Jaccard 0.321).

Conclusion: the primary estimand is stable enough for Development evaluation, so the `ESTIMAND_INSTABILITY` stop condition is not triggered. However, the Díaz rule/scale sensitivity is a substantive limitation and blocks a universal support-recovery claim. Detailed rows are retained in `estimand_sensitivity.csv` and `estimand_rule_sensitivity.csv`.
