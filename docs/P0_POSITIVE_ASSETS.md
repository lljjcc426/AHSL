# P0 positive asset audit

| Asset | Class | Evidence of reuse | Limitation |
|---|---|---|---|
| alpha-acyclicity, join-tree and running-intersection notes | theory | supports exact structural reasoning and decomposition entry point | mostly k=1; does not justify learning |
| exact connected-subtree DP and posterior decoder | theory/code | exact optimization, posterior marginals and constrained Bayes decisions | tied to fixed-tree output class |
| GHD/FHD, fractional-cover and exact-inference audit | theory | directly seeds the P0-B program | current code does not compute exact GHW/FHW |
| UAI factor parser and factor diagnostics | code | preserves scopes, domains, tables and sparsity | UAI alone is not a decomposition-learning benchmark |
| exact variable elimination and strategy-cost simulator | code | provides correctness/cost controls for downstream decomposition studies | dense VE and selected small instances only |
| CertPath attainability and directed-hypergraph tooling | theory/code | reusable exact feasibility and certificate reasoning | original supervised task is closed |
| interaction estimand and leakage audits | methodology | distinguishes prediction from directly identified support | domain-specific data adapters are heterogeneous |
| temporal open-world evaluation tools | benchmark/code | exposes sampled-negative versus open retrieval error | not a new temporal method |
| projection ambiguity audit | theory/methodology | concrete identifiability counterexamples | small exhaustive sizes only |
| phase gates, candidate matrices and stop rules | methodology | early falsification before model development | thresholds remain task-specific |
| versioned reports, raw/aggregate outputs and Git branches | reproducibility | complete phase provenance | no remote CI workflow |

The strongest theory asset is the combined exact structural/decomposition
knowledge. The strongest code asset is the exact connected-subtree and factor
inference infrastructure. The strongest methodology asset is the benchmark,
identifiability and classical-residual gate sequence. Asset reuse does not by
itself justify the next topic.
