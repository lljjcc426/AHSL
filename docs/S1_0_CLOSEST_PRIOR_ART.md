# S1.0 closest prior art

## Collision matrix

| Candidate | Closest ML | Closest statistics/theory | Closest domain method | Remaining distinction | Verdict |
|---|---|---|---|---|---|
| yeast score/support | Dango 2026 | knockoffs, sparse/hierarchical selection | tau-SGA | latent support under replicate error and strict query-background split | scientifically interesting, but unmeasured truth unavailable and architecture route occupied |
| microbial sparse recovery | sparse Möbius 2024/2026 | lasso, OMP, sparse Fourier | Arya 2023 compressed sensing | replicate-aware direct support rather than only response prediction | real residual on one tiny panel, insufficient cross-domain basis |
| FDR support | Diamond 2025 | model-X knockoffs and multiple testing | published p/FDR rules | order>=3 factorial contrasts under heteroscedastic cell noise | possible theorem gap, but no two valid real benchmarks |
| pure HOI | unrestricted l1 | hierNet, glinternet, FAMILY, RAMP | exact Möbius/tau contrasts | non-hereditary recovery | only 5.71% pure effects in one panel |
| active discovery | NAIAD 2025 (pair optimization) | group testing; adaptive sparse Möbius 2026 | sequential combinatorial screens | noisy contrast support/FDR objective rather than best response | core query-efficient novelty occupied; real prospective benchmark absent |
| context-varying drug effects | multi-task prediction families | multi-task/group sparse regression | Bliss/Loewe/HSA/ZIP and hidden suppression | partially shared support across dose | fixed shared signed support contradicted by data |

## Decision-critical details

- Dango already uses six PPI networks, a self-attention hypergraph regressor, random and two gene splits, strong-score AUROC/AUPR, and optional GP uncertainty. Another encoder, embedding, or gene split is not novelty.
- Kang et al. give nonadaptive sparse Möbius recovery and a low-degree noise-tolerant group-testing construction. Erginbas et al. make the queries adaptive with near-optimal dependence under an exact sparse Boolean-polynomial oracle. This is the strongest collision with an active S1 route.
- Arya et al. already apply an order-weighted Walsh basis and compressed sensing to microbial response landscapes. A new method must improve direct support validity, not merely response prediction.
- Diamond gives model-X-knockoff FDR control for pairwise non-additive interactions in trained models. Higher order is not solved there, but merely replacing “pairwise” with “order>=3” without a valid factorial benchmark is not a contribution.
- NAIAD actively selects pairwise combinatorial CRISPR perturbations to find strong responses. Structural support recovery is distinct, but the proposed evaluation data here do not sustain that distinction experimentally.

## Publication-novelty gate

FAIL. No candidate simultaneously has two direct real benchmarks and novelty beyond Dango/sparse-Möbius/classical inference. This supports the stop but the selected final code remains S1.0-C because identifiability/benchmark failure occurs first.
