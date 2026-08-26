# S1.0 estimand stability

## Predeclared rule

At least one accepted estimand family must have median strong-support Jaccard at least 0.60 and median sign agreement on overlap at least 0.80. Thresholds were frozen before computation.

## Microbial raw versus log10 CFU

Strong support requires a 95% cell-wise bootstrap interval excluding zero and a material point magnitude. Log scale uses `|beta|>=0.10` log10 CFU; raw scale uses 10% of the focal monoculture mean so that the magnitude screen is scale-aware.

| Focal strain | raw support | log support | Jaccard | sign agreement | rank Spearman | top-k overlap |
|---|---:|---:|---:|---:|---:|---:|
| DW039 | 28 | 25 | 0.767 | 1.000 | 0.937 | 0.800 |
| DW067 | 16 | 27 | 0.593 | 1.000 | 0.891 | 0.625 |
| DW100 | 18 | 19 | 0.609 | 1.000 | 0.956 | 0.889 |
| DW102 | 13 | 15 | 0.867 | 1.000 | 0.986 | 0.923 |
| DW145 | 23 | 19 | 0.826 | 1.000 | 0.971 | 0.842 |
| DW147 | 30 | 19 | 0.633 | 1.000 | 0.885 | 0.737 |
| DW155 | 9 | 16 | 0.250 | 1.000 | 0.668 | 0.444 |

Median Jaccard is **0.633** and median sign agreement **1.000**: the formal gate passes, but 2/7 focal landscapes fail individually and DW155 is strongly unstable. This is a narrow pass, not evidence of universal support invariance.

## Yeast tau versus raw epsilon

Using the same `p<0.05`, magnitude 0.08 rule gives 3,196 strong negative tau labels and 5,125 raw-epsilon labels. Jaccard is **0.505** and score Spearman is **0.267**. Raw epsilon is not an equally preferred final biological estimand: tau deliberately removes scaled digenic contributions. Therefore this is a sensitivity warning, not a reason to discard the accepted tau target. The median combined-fitness SD is 0.0564, 70.5% of the 0.08 magnitude cutoff.

## Drug context

Across the 182 order-3--5 drug identity sets, the median modal label fraction is 0.636 for DA and 0.547 for emergent labels. Both numeric DA and emergent effects change sign somewhere across dose contexts in **98.9%** of sets. Therefore a fixed set-level signed support fails; only context-specific support/effect remains defensible.

Raw tables are in `results/s1_0/raw/` and plot 03/08 visualize scale and context stability.
