# N0 closest prior art

## Finalist: CertPath

### 1. Krieger and Kececioglu, Shortest Hyperpaths in Directed Hypergraphs for Reaction Pathway Inference (JCB 2023)

- Problem: exact shortest source–target pathway inference, including cyclic paths.
- Structure: directed hypergraph with conjunctive tails and product heads.
- Learning: none; unit or externally specified positive reaction weights.
- Theory: graph-theoretic characterization, ILP, cutting planes, exact optimality.
- Benchmark/result: thousands of NCI-PID/Reactome instances; median exact runtime below 10 s and maximum below 30 min; known-pathway recovery evaluated.
- Code: Mmunin, research-use source.
- Overlap: exact decoder, data construction, and main feasibility machinery.
- Remaining space: learning context-dependent costs, group/temporal generalization, uncertainty calibration, and a certificate that separates cost uncertainty from combinatorial exactness.

### 2. Krieger and Kececioglu, Heuristic/Fast Approximate Shortest Hyperpaths (WABI 2021; AMB 2022)

- Problem: fast shortest directed-hyperpath heuristic.
- Structure: general directed hypergraph, cycles allowed.
- Learning: none.
- Theory: polynomial runtime; exact on singleton-tail hypergraphs; no constant-factor guarantee in general unless P=NP.
- Benchmark/result: over 99% agreement with the acyclic MILP; all enumerated cyclic cases optimal; laptop-scale runtime.
- Code: Hhugin, research-use source.
- Overlap: strongest fast fallback and preprocessing baseline.
- Remaining space: it optimizes hand-set weights and gives no learned biological ranking or calibrated abstention.

### 3. Chen, Liao, and Liu, CHESHIRE (Nature Communications 2023)

- Problem: predict missing reactions in genome-scale metabolic models.
- Structure: metabolic hypergraph incidence plus a decomposed graph.
- Learning: Chebyshev spectral hyperlink predictor.
- Theory: no exact pathway-feasibility/optimality certificate.
- Benchmark/result: 108 BiGG and 818 AGORA models, including phenotype-oriented external validation.
- Code: public GitHub repository.
- Overlap: learns reaction confidence from real metabolic hypergraphs.
- Remaining space: predicted reactions are not decoded into an exact source–target directed hyperpath, and signaling-pathway supervision/temporal splits are different.

### 4. Ma, Zhao, and Yang, Directed Hypergraph Representation Learning for Link Prediction (AISTATS 2024)

- Problem: directed hypergraph link prediction.
- Structure: approximate directed-hypergraph Laplacian.
- Learning: directed hypergraph neural representation.
- Theory: representation/convolution construction, not exact pathway decoding.
- Benchmark: multiple directed-hypergraph domains.
- Code: paper-linked artifact status to be rechecked in N1.
- Overlap: direction-aware high-order representation could be a cost-feature baseline.
- Remaining space: no source–target feasibility, exact objective, robust optimum certificate, or biological pathway decision metric.

### 5. Zhang et al., Multi-HGNN (Information Sciences 2025)

- Problem: missing-reaction prediction in metabolic networks.
- Structure: hybrid directed graph and hypergraph with molecular features.
- Learning: pretrained biochemical features plus directed/hypergraph modules and a DNN predictor.
- Theory: no exact constrained pathway guarantee.
- Benchmark: public BiGG data.
- Code: not established as a clean public artifact in the N0 audit.
- Overlap: multimodal reaction scoring is a strong learned baseline.
- Remaining space: prediction-only task and genome-scale metabolic gap filling, not certified exact pathway selection.

### 6. BPP (Bioinformatics Advances 2024)

- Problem: automatic biochemical pathway prediction/attribute prediction.
- Structure: pathway hypergraphs, with graph and HGNN representation options.
- Learning: link/attribute predictors.
- Theory: none of the exactness/certificate kind required here.
- Benchmark/code: public platform and datasets.
- Overlap: closest end-user application language.
- Remaining space: no exact directed-hyperpath semantics or uncertainty-aware optimality.

### 7. RIPTiDe (PLOS Computational Biology 2019)

- Problem: transcriptome-guided context-specific metabolic flux inference.
- Structure: stoichiometric model/linear programs.
- Learning: transcript abundance is mapped to reaction coefficients; not a trained cross-instance predictor.
- Theory: flux feasibility and optimization.
- Benchmark: genome-scale reconstructions with transcriptomic contexts.
- Overlap: demonstrates that context-dependent reaction weights can improve biological relevance.
- Remaining space: different task and algebra (flux polytope rather than directed source–target hyperpaths), no learned calibrated path costs.

### Collision conclusion

No searched work jointly matches all five defining objects: (i) curated real pathway supervision, (ii) learned context-dependent reaction costs, (iii) exact general directed-hyperpath decoding with cycles, (iv) a verifiable cost-uncertainty/abstention certificate, and (v) grouped temporal/pathway-family evaluation. The project would still fail G8 if N1 reduced to “feed CHESHIRE scores into Mmunin”; the certificate and decision-focused formulation are mandatory.

## Fatal collisions for rejected semifinal candidates

| Candidate | Closest collision | Why fatal |
|---|---|---|
| hybrid WCOJ learning | ADOPT (PVLDB 2023); Adaptive Factorization in DuckDB (CIDR 2025) | RL/ML already chooses WCOJ attribute orders or whether to enable factorization/WCOJ, with real workloads and guarantees |
| tensor plan ranking | Hyper-optimized TN contraction (2021); RL-TNCO (ICML 2022); GPU plan LTR (2026) | hypergraph partitioning, learning, hardware labels and out-of-distribution plan ranking are already combined |
| exact HD/GHD learner | ML selection of TDs for DP (IJCAI 2015); exact treewidth solver selection (Algorithms 2019) | generic learned decomposition/solver selection is established; merely replacing treewidth by hypertree width is Level 1 |
| HNN width expressivity | Width Wall (2026) | direct hypertree-width-indexed expressivity hierarchy plus real experiments |
| hypergraph partitioning | ML-based hypergraph pruning for partitioning (2020) | direct learned pruning exists; a new generic scorer would be incremental |
