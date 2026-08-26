# S1.0 sparse recovery audit

## Closest mathematical work

| Work | Basis / target | Sampling | Noise / guarantee | Collision with S1.0 |
|---|---|---|---|---|
| Stobbe & Krause 2012 | Fourier-sparse set functions | query access | sparse Fourier recovery | establishes query-efficient sparse set-function learning |
| Wendler et al. 2021 | non-orthogonal Fourier bases including set-function bases | sparse queries | theoretical recovery conditions | directly relevant to coherent set-function dictionaries |
| Kang et al. 2024 | Möbius/AND coefficients | nonadaptive and group-testing constructions | `O(Kn)` generally; low-degree `O(Kt log n)` and a noise-tolerant version under stated assumptions | same sparse low-order coefficient/support target |
| Erginbas et al. 2026 | sparse real Boolean polynomial / Möbius transform | fully or partially adaptive oracle queries | FASMT `O(sd log(n/d))`; PASMT `O(sd^2 log(n/d))`; exact/simulation-focused | directly occupies active sparse support recovery and hypergraph reconstruction under oracle assumptions |
| Arya et al. 2023 | order-weighted Walsh--Hadamard landscape | random limited community observations | l1/compressed-sensing empirical recovery | direct microbiome response-recovery collision |

## What remains different

The strongest unoccupied distinction is not architecture. Biological panels have replicated heteroscedastic measurements, domain-specific contrasts requiring lower-order cells, nonuniform experiment costs, and uncertainty/FDR targets. The sparse-Möbius papers assume a query oracle for a set function and structural sparsity/low degree; they do not directly solve tau-SGA or dose-context null-model uncertainty.

That distinction is scientifically real but presently lacks two direct real benchmark families. The microbial panel supplies one small retrospective test. Yeast unmeasured tau support cannot be calculated without new experimental measurements; drug fixed support is context-unstable. Therefore an uncertainty-aware adaptive Möbius project would currently rest on a single small panel plus simulations, while the noiseless/adaptive mathematical core is already occupied.

## Baseline interpretation

OMP in this audit is the compressed-sensing-style greedy baseline on the coherent AND/Möbius dictionary. It is not an implementation of Kang/Erginbas algorithms because the biological measurement design and missing input assumptions do not match their exact query schemes. Calling it “sparse Möbius transform reproduction” would overstate equivalence.

## Conclusion

Sparse-Möbius prior art is a major novelty collision for candidate D (active structural discovery) and unrestricted sparse recovery. A future project would need a sharply stated noisy-contrast theorem and two valid real evaluation families; S1.0 does not establish those prerequisites.
