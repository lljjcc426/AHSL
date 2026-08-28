# META1.6 objective derivation

For the standardized Lasso objective

`(2n)^(-1)||y-Xb||_2^2 + lambda ||b||_1`,

an active set `S` with sign vector `z` satisfies

`bhat_S = beta_S + G_S^(-1)(X_S' eps/n - lambda z)`.

Recovery also requires every evaluated inactive coordinate to satisfy the KKT bound after projecting its noise score through `X_S`. META1.6 estimates the joint event directly with 32 frozen Gaussian draws and evaluates lambda multipliers 0.65, 1.0, and 1.5 around `sigma sqrt(2 log(p)/n)`. The path maximum is part of the frozen objective.

The modified event checks signs of active high-order terms and exclusion of inactive high-order terms while treating active low-order terms as nuisance. Its aggregate is `0.8 * mean + 0.2 * CVaR20` across Pi. This robust mixture was retained because raw maximin/CVaR alone is mostly zero and therefore cannot rank designs. Singular support blocks score zero.
