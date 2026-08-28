# META1 scope and estimand

META1 is a Development study of signed order-3-or-higher interaction-support recovery from partially observed, replicated factorial landscapes. It is not a biological-causality study and it does not treat a fitted nonzero coefficient as truth.

For a binary community vector (x\in\{0,1\}^d), the response is represented in the AND basis,

\[
f(x)=\sum_{S\subseteq[d]}\beta_S\prod_{j\in S}x_j.
\]

The primary estimand is the sign of each \(\beta_S\) with \(|S|\ge3\), conditional on a panel-specific response scale. Full-panel cell means define the point Möbius transform. Biological replicates are resampled independently within cells 1,000 times. A coefficient enters the reference signed support only when its 95% percentile bootstrap interval excludes zero and its point magnitude exceeds a frozen practical-effect threshold.

- Ishizawa: log10 CFU; practical threshold 0.10 log10 CFU.
- Díaz-Colunga: raw OD600 quantitative community-function response; threshold 0.05127, equal to 5% of the median nonempty raw response.

These thresholds were selected from measurement semantics and practical scale before downstream method comparison. Sensitivity analyses use raw/log1p alternatives, threshold multipliers 0.8 and 1.2, a 95% bootstrap sign-stability rule, and a bootstrap-sign empirical-p-value rule with Benjamini-Hochberg 10% control.

Primary evaluation is landscape-level signed-support F1, macro-aggregated within panel. Precision, recall, average precision, empirical FDR, pure-HOI recall, coefficient RMSE, held-out response RMSE, runtime, measurement count, and seed stability are guardrails. Cross-panel averaging is secondary because the response semantics and noise laws differ.

The complete panels serve only as reference/evaluation objects. Estimators see the selected communities and all replicates for those communities. The final Development classification is D-B PROMISING: a conditional measurement-design result merits strict Confirmation, while cross-panel generality is not established.
