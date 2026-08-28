# META1.6 support ensemble

The primary ensemble Pi contains 36 scenarios: `k_H in {2,4,8}`, `k_L in {2,6}`, SNR/effect magnitude in `{0.75,1.5,3.0}`, and two deterministic replicates per cell of the grid. High-order identities are sampled by cycling across orders 3, 4, 5, and 6 before reusing an order, preventing the combinatorial count of order-3 terms from defining the prior. Low-order identities are uniform without replacement. Signs are independent balanced ±1; no heredity is imposed. Noise is iid Gaussian with sigma 1.

The ensemble was generated without Ishizawa support frequencies or F1. Sensitivity variants are `sparser`, `denser`, and `weak`; all use the same identity and sign rules. The exact scenario/term table is `results/meta1_6/raw/support_ensemble.csv`.
