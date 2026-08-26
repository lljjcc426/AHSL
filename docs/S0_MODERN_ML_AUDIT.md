# S0 modern-ML audit

## Selected subfield

Modern work is active but not yet saturated at the exact S0 boundary.

| Work | What it establishes | Residual left open |
|---|---|---|
| Dango (Zhang et al., 2026; preprint lineage from 2020) | direct HGNN prediction of measured yeast trigenic scores; random and gene-disjoint splits; public code/data | one organism and one triple-screen family; prediction dominates explicit support uncertainty and experimental design |
| NAIAD (Qin et al., ICML 2025) | active learning on four public combinatorial CRISPR datasets | explicitly pairwise gene combinations; does not establish order≥3 structure recovery |
| sparse Möbius recovery (Kang et al., 2024) | sublinear-query recovery under sparse, bounded-degree assumptions | mostly oracle/set-function query setting; biological noise and heterogeneous real interventions remain |
| MoCHI (Faure & Lehner, 2024) | sparse, interpretable energetic couplings from deep mutational scanning | user-specified biophysical structure and mutation-scale focus; not a general multi-intervention support benchmark |
| PNAS microbiome landscape model (Arya et al., 2023) | compressive-sensing view of sparse higher-order community landscapes; four real datasets | focuses response reconstruction; support calibration and cross-dataset protocols remain |
| HODDI (Wang et al., 2025) | public higher-order polypharmacy event dataset | co-reporting is not a controlled combination effect; constructed negatives make causal/synergy claims invalid |
| neural interaction detection and SIAN/HONAM families | scalable interaction extraction or sparse additive prediction | often post-hoc interactions of a learned predictor, not experimentally defined structural truth |

The strongest recent threat is **Dango**, followed by sparse Möbius recovery. The subfield survives because a program centered on target definition, direct support/effect recovery, valid group/order splits, uncertainty, and active measurement across multiple experimental domains is broader than a Dango variant.

## Temporal/directed hyperedge forecasting

Hyper-SAGNN, HGDHE, CAt-Walk, FastHeP, the 2025 directed temporal point-process model, hard-negative methods, and 2026 self-supervised hyperedge predictors make this a crowded representation/scoring area. Two papers materially change the audit:

- *Prediction Is NOT Classification* shows that negative-sample classification can be weakly or negatively correlated with actual retrieval quality and that simple heuristics can beat deep models.
- HyperSearch performs unconstrained static candidate search with safe pruning and strong results on ten real hypergraphs.

The narrower open-world temporal formulation still passes, but with high novelty and evaluation risk. Another encoder plus sampled negatives is explicitly non-novel.

## Reconstruction from dynamics

THIS (2025), the 2024 PRX reconstruction method, directed-acyclic hypergraph topology identification, and 2026 Bayesian/multiplex extensions show a rapidly forming frontier. The mathematical opportunity is real, but accepted structure recovery remains chiefly synthetic; EEG and other real applications lack ground-truth hyperedges. It fails S0 G7/G8 despite strong theory.

## Causal hypergraphs

HyperSCI estimates treatment effects on a known hypergraph; it does not learn the causal hyperedge structure. Higher-order additive causal models and dynamic effective hyper-connectivity began explicit causal-hypergraph discovery in 2025–2026, but structure validation is synthetic or indirect. This family fails G2/G7/G8 now.

## Factor scopes and probabilistic circuits

Modern factor-scope learning competes with mature Bayesian-network/MRF structure learning and with probabilistic circuits that make exact inference tractable by circuit design. SoftLearn and 2024 circuit-semantics work show continuing progress, but there is no compelling public benchmark where recovering a high-order factor hypergraph is both the scientific output and superior to circuit or pairwise alternatives.

## Saturation judgment

- Saturated for this program: generic static hyperedge classification, generic HSL for downstream node/traffic prediction, generic n-ary KG completion.
- Emerging but benchmark-limited: dynamics-to-hypergraph and high-order causal discovery.
- Open with direct recent collision: temporal open-world set-event forecasting.
- Open with a coherent classical/ML interface and multiple real experimental routes: sparse combinatorial interaction structure learning.
