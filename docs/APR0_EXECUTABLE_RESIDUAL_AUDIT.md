# AP-R0 executable residual audit

Frozen threshold: at least 2x material latency/memory/wasted-work gap, at least
20 percentage points objective correctness, or an equivalent systematic
failure. Raw rows are retained in
`results/ap_r0/raw/executable_residuals.csv`.

## D1 PyTorch dynamic-shape compilation pre-gate

Same current package, two configurations:

| Configuration | Result | Interpretation |
|---|---|---|
| default locale | failed after about 7 s with `UnicodeDecodeError` in an Inductor template | real packaging/localization defect, but removed by `PYTHONUTF8=1`; fails G6 |
| UTF-8 mode | failed after about 8 s because MSVC `cl` was absent | setup prerequisite, not a runtime/compiler-algorithm residual |

No TorchBench performance row was produced, so no latency ratio is claimed.
More importantly, the PyTorch March 2026 devlog reports backed/unbacked parity
across all tested HuggingFace TorchBench models and 30+ vLLM configurations.
This is direct current negative evidence against the original residual.

## E1 CP-Bench pre-gate

Three published ground-truth APLAI workloads ran correctly in 1.4--2.1 s each.
The artifact's cached generations are from DeepSeek Chat and GPT-4.1-mini in
May 2025. They are not a current 2026 strong baseline. Therefore the metric is
observable, but a current semantic correctness gap was not measured.

## Gate result

Neither candidate passed the complete pre-gate. There were **zero semifinals**
and hence zero finalists. This is not a threshold failure after benchmark
hunting; it is the prescribed artifact/current-baseline stop.
