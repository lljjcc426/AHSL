# META1.6 identifiability analysis

The design matrix has 64 feasible rows and 63 nonempty AND columns. Columns are split into `X_L` (21 order-1/2 nuisance terms) and `X_H` (42 target terms). Diagnostics in `results/meta1_6/raw/identifiability.csv` record full, nuisance, target, and residual target ranks; zero columns; exact target-target and target-low aliases; coherence; restricted nonzero singular value; and bounded sparse-nullspace tests.

For dense unpenalized nuisance, `M_L X_H` is the relevant target information. At budget 16, the 15 nonempty response contrasts can be spanned by `X_L`, so the residual target space collapses. At budgets 24 and 32 its dimension is at most 2 and 10 respectively when `rank(X_L)=21`. Thus N0 does not identify arbitrary high-order coefficients under the studied budgets. This is an algebraic limitation, not a low-power empirical finding.

Sparse-nullspace enumeration is exact for support sizes 1–3 and uses a fixed sample of 128 four-term supports. No claim is made that this proves uniform recovery for larger supports.
