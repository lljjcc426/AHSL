# S0 closest prior art

## Rank 1: sparse high-order combinatorial interaction structure learning

### Five closest works

1. **Kuzmin et al., Science 2018, “Systematic analysis of complex genetic interactions.”** Directly measures ~200,000 yeast triple mutants and defines quantitative trigenic effects. It supplies the strongest real structural labels, but it is an experimental map rather than a general structure learner.
2. **Zhang et al., Cell Systems 2026, “Dango: Predicting higher-order genetic interactions.”** The closest ML collision: a self-attention HGNN predicting ~100,000 measured trigenic scores from six PPI networks, with random and gene splits. It occupies “apply an HGNN to yeast triples.”
3. **Arya, George & O’Dwyer, PNAS 2023, “Sparsity of higher-order landscape interactions enables learning and prediction for microbiomes.”** Uses sparse Boolean/set-function expansions and compressive sensing, including four experimental datasets. It is the strongest classical-ML/theory bridge.
4. **Ishizawa et al., PNAS 2024, “Learning beyond-pairwise interactions enables the bottom–up prediction of microbial community structure.”** Measures all 127 subsets of seven strains and shows that ≥3-member information improves bottom-up prediction. It supplies a near-complete independent factorial route.
5. **Lozano-Huntelman et al., iScience 2021, “Hidden suppressive interactions are common in higher-order drug combinations.”** Measures all lower-order subsets inside 3–5 drug combinations and shows why comparison with singles alone misses structure.

### Additional close threats

- Kang et al. (2024), sparse Möbius recovery: theory-level collision on efficient support recovery.
- Qin et al. (ICML 2025), NAIAD: active discovery but restricted to pairs.
- Faure & Lehner (2024), MoCHI: sparse higher-order epistasis in deep mutational scanning.
- Arellano-García et al. (2021): supervised HOI presence detection on Drosophila experiments, trained from synthetic dynamical samples.
- Wendler et al. (AAAI 2021): sparse set-function learning in non-orthogonal Fourier bases.
- Bien et al. (2013) and Lim & Hastie (2015): hierarchical sparse interaction baselines.

### Exact non-collision claim

S0 does **not** claim the subfield is new. It claims that the cross-domain problem of recovering calibrated order≥3 support/effects from sparse real combinatorial intervention panels—under entity/order-disjoint evaluation and with acquisition-aware extensions—retains a research program beyond the closest works. S1 must locate a concrete gap; it may still return no-go.

## Rank 2: open-world temporal set-event forecasting

Closest works:

1. Gracious & Dukkipati (AAAI 2023), HGDHE/HGBDHE temporal point-process hyperedge forecasting.
2. Behrouz et al. (NeurIPS 2023), CAt-Walk inductive temporal hypergraph representations on ten datasets.
3. Yu et al. (ICDMW 2024), *Prediction Is NOT Classification*, demonstrating evaluation-rank reversals.
4. Gracious, Gupta & Dukkipati (AAAI 2025), directed higher-order event membership/cardinality/time forecasting.
5. Xu et al. (KDD 2025), FastHeP scalable temporal hyperedge prediction.
6. Choo et al. (ICDM 2025), HyperSearch unconstrained static hyperedge retrieval with safe pruning.

Residual: combine temporal generative semantics with truly open-world retrieval, unseen-group/entity evaluation, and calibrated full-set scoring. Risk: this may be benchmark engineering around an already crowded prediction literature.

## Other semifinals: closest-work checks

### Dynamics-to-hypergraph reconstruction

Delabays et al. (2025) THIS; Tabar et al. (PRX 2024); Malizia et al. (2024) coupled-system reconstruction; SINDy (Brunton et al., 2016); NRI (Kipf et al., 2018). Killed because real applications do not provide accepted hyperedge truth.

### Protein-complex set discovery

MCL (van Dongen, 2000); MCODE (Bader & Hogue, 2003); ClusterONE (Nepusz et al., 2012); PCGAN (2023); HPC-Atlas (2023). Killed because classical maturity and incomplete/overlapping gold standards make a clean residual difficult.

### Factor-scope structure learning

Srebro (2003); Lee, Ganapathi & Koller (2007); Korhonen & Parviainen (2013); Berg et al. (2014); Ghandi et al. (2024) SoftLearn/modern probabilistic circuits. Killed because high-order scope truth and graph insufficiency are weak on real benchmarks, while classical and circuit alternatives are mature.

## Closed-line collision audit

No selected or finalist formulation estimates alpha-acyclic incidence, a join tree, reaction costs, or a shortest directed hyperpath. The only transferred lesson is methodological: validate whether the proposed structural target is identifiable and scientifically meaningful before model development.
